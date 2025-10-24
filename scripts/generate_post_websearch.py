import json
import os
import random
from typing import Callable, Optional, Sequence

import requests

from common import (
    build_prompt_context,
    load_generation_settings,
    write_post,
)
from common.prompts import PromptContext
from common.settings import GenerationSettings


# Default Foundry models (from your screenshot). You can override via FOUNDARY_MODELS env var (comma-separated).
FOUNDARY_MODELS_DEFAULT = [
    "DeepSeek-V3.1",
    "gpt-5-mini",
    "gpt-oss-120b",
    # "Llama-4-Maverick-17B-128E-Instruct-FP8",
]


def _build_messages(prompt_context: PromptContext) -> list[dict]:
    return [
        {"role": "system", "content": [{"type": "text", "text": prompt_context.system_prompt}]},
        {"role": "user", "content": [{"type": "text", "text": prompt_context.user_prompt}]},
    ]


def ask_azure_foundry_with_web_search(
    settings: GenerationSettings,
    prompt_context: PromptContext,
    *,
    foundry_model: str | None = None,
    post_fn: Optional[Callable[..., requests.Response]] = None,
    _extra_messages: Optional[Sequence[dict]] = None,
) -> str:
    """Call Azure OpenAI (Foundry) using the REST API."""

    endpoint = os.environ.get("ENDPOINT_URL") or os.environ.get("FOUNDARY_URL")
    if not endpoint:
        raise RuntimeError("ENDPOINT_URL or FOUNDARY_URL must be set to the Azure OpenAI service root")
    endpoint = endpoint.rstrip("/")

    subscription_key = os.environ.get("FOUNDARY_API_KEY") or os.environ.get("AZURE_OPENAI_API_KEY")
    deployment = foundry_model or os.environ.get("FOUNDARY_MODEL") or os.environ.get("DEPLOYMENT_NAME") or "gpt-oss-120b"

    if not subscription_key:
        raise RuntimeError("FOUNDARY_API_KEY or AZURE_OPENAI_API_KEY not set for REST Foundry client")

    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2025-01-01-preview"

    messages = _build_messages(prompt_context)
    if _extra_messages:
        messages.extend(_extra_messages)

    payload = {
        "messages": messages,
        "max_tokens": 2048,
    }
    temp = os.getenv("FOUNDARY_TEMPERATURE")
    top_p = os.getenv("FOUNDARY_TOP_P")
    try:
        if temp is not None:
            payload["temperature"] = float(temp)
    except ValueError:
        pass
    try:
        if top_p is not None:
            payload["top_p"] = float(top_p)
    except ValueError:
        pass

    headers = {
        "Content-Type": "application/json",
        "api-key": subscription_key,
    }

    post = post_fn or requests.post
    resp = post(url, json=payload, headers=headers, timeout=60)

    def _maybe_retry_with(payload_override: dict | None = None, drop_keys: tuple[str, ...] = ()):
        updated = dict(payload)
        for key in drop_keys:
            updated.pop(key, None)
        if payload_override:
            updated.update(payload_override)
        return post(url, json=updated, headers=headers, timeout=60)

    if not resp.ok:
        body = None
        try:
            body = resp.json()
        except Exception:
            body = resp.text

        try_retry = False
        try:
            if isinstance(body, dict):
                msg = json.dumps(body)
            else:
                msg = str(body)
            if resp.status_code == 400 and 'max_tokens' in msg and ('unsupported' in msg or 'not supported' in msg or 'unsupported_parameter' in msg):
                try_retry = True
        except Exception:
            try_retry = False

        if try_retry:
            new_payload = dict(payload)
            val = new_payload.pop('max_tokens', None)
            if val is not None:
                new_payload['max_completion_tokens'] = val
                resp = post(url, json=new_payload, headers=headers, timeout=60)

        if not resp.ok:
            try:
                msg = json.dumps(body) if isinstance(body, dict) else str(body)
            except Exception:
                msg = str(body)
            if resp.status_code == 400 and 'temperature' in msg and 'unsupported' in msg:
                resp = _maybe_retry_with(drop_keys=("temperature",))
                if not resp.ok:
                    resp = _maybe_retry_with({"top_p": 1.0}, drop_keys=("temperature",))

        if not resp.ok:
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            raise RuntimeError(f"Foundry REST call failed: {resp.status_code} {resp.reason}: {body}")

    data = resp.json()
    texts: list[str] = []
    if isinstance(data, dict):
        choices = data.get("choices") or []
        for choice in choices:
            message = choice.get("message") or {}
            content = message.get("content") or choice.get("text") or choice.get("delta")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        if "text" in block and isinstance(block["text"], str):
                            texts.append(block["text"])
                        elif "content" in block and isinstance(block["content"], str):
                            texts.append(block["content"])
            elif isinstance(content, str):
                texts.append(content)

    if not texts:
        try:
            first = data.get("choices", [None])[0]
            if first:
                message = first.get("message") or first.get("delta") or first.get("text")
                if isinstance(message, str):
                    texts.append(message)
                elif isinstance(message, dict) and isinstance(message.get("content"), str):
                    texts.append(message.get("content"))
        except Exception:
            pass

    if not texts:
        return json.dumps(data)

    markdown = "\n".join(t.strip() for t in texts if t).strip()
    if not markdown and not _extra_messages:
        fallback_instruction = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "The previous response was empty. Provide the complete Markdown article now with an H1 title, "
                            "a **TL;DR** section, practical sections, and a **Further reading** list. "
                            "Do not mention tool usage."
                        ),
                    }
                ],
            }
        ]
        return ask_azure_foundry_with_web_search(
            settings,
            prompt_context,
            foundry_model=foundry_model,
            post_fn=post_fn,
            _extra_messages=fallback_instruction,
        )
    elif not markdown:
        return markdown

    lower = markdown.lower()
    has_heading = "#" in markdown or lower.startswith("h1:")
    has_tldr = "tl;dr" in lower
    has_further = "further reading" in lower
    tool_markup = "<|" in markdown or "web_search" in lower

    if not _extra_messages and (not (has_heading and has_tldr and has_further) or tool_markup):
        fallback_instruction = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            ("The previous response included raw tool-call markup." if tool_markup else "The previous response did not deliver the final Markdown article.")
                            + " Web search is unavailable in this environment. Reply now with a complete Markdown post "
                            "that includes an H1 title, a **TL;DR** section, practical sections, and a **Further reading** list. "
                            "Do not emit tool-call markup, <|...|> tokens, or describe the attempt; output only the article."
                        ),
                    }
                ],
            }
        ]
        return ask_azure_foundry_with_web_search(
            settings,
            prompt_context,
            foundry_model=foundry_model,
            post_fn=post_fn,
            _extra_messages=fallback_instruction,
        )

    return markdown


def ask_with_web_search(settings: GenerationSettings, prompt_context: PromptContext) -> tuple[str, str]:
    if not os.environ.get("FOUNDARY_API_KEY") and not os.environ.get("AZURE_OPENAI_API_KEY"):
        raise RuntimeError("FOUNDARY_API_KEY or AZURE_OPENAI_API_KEY must be set; cannot call Azure Foundry")

    env_models = [m.strip() for m in os.environ.get("FOUNDARY_MODELS", "").split(",") if m.strip()]
    models = env_models or FOUNDARY_MODELS_DEFAULT
    random.shuffle(models)

    last_err: Exception | None = None
    for candidate in models:
        print("Trying Foundry model:", candidate)
        try:
            body = ask_azure_foundry_with_web_search(settings, prompt_context, foundry_model=candidate)
            print("Found working model:", candidate)
            return body, candidate
        except RuntimeError as exc:
            last_err = exc
            message = str(exc)
            if "DeploymentNotFound" in message or "404" in message:
                print(f"Deployment {candidate} not found, trying next model...")
                continue
            raise

    raise RuntimeError(f"No available Foundry deployment found after trying models: {models}. Last error: {last_err}")


def main():
    settings = load_generation_settings()
    prompt_context = build_prompt_context(settings)
    body, used_model = ask_with_web_search(settings, prompt_context)
    write_post(
        body,
        settings,
        used_model=used_model,
        include_llm_model=True,
    )


if __name__ == "__main__":
    main()
