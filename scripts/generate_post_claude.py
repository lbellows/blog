import os
from typing import Optional

import anthropic

from common import (
    build_prompt_context,
    load_generation_settings,
    write_post,
)
from common.prompts import PromptContext
from common.settings import GenerationSettings


DEFAULT_ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"


def _build_tools(settings: GenerationSettings) -> list[dict]:
    tool_def = {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": settings.max_searches,
    }
    if settings.allowed_domains:
        tool_def["allowed_domains"] = settings.allowed_domains
    if settings.blocked_domains:
        tool_def["blocked_domains"] = settings.blocked_domains
    return [tool_def]


def ask_claude_with_web_search(
    settings: GenerationSettings,
    prompt_context: PromptContext,
    *,
    model: str | None = None,
    client: Optional[anthropic.Anthropic] = None,
) -> tuple[str, str]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY must be set for Anthropic client")

    anthropic_client = client or anthropic.Anthropic(api_key=api_key)
    chosen_model = model or DEFAULT_ANTHROPIC_MODEL

    response = anthropic_client.messages.create(
        model=chosen_model,
        max_tokens=2200,
        temperature=0.6,
        system=prompt_context.system_prompt,
        messages=[{"role": "user", "content": prompt_context.user_prompt}],
        tools=_build_tools(settings),
    )

    parts: list[str] = []
    for block in response.content:
        if getattr(block, "type", "") == "text" and getattr(block, "text", None):
            parts.append(block.text)

    markdown = "\n".join(part.strip() for part in parts if part.strip())
    if not markdown:
        raise RuntimeError("Anthropic response did not contain text content")

    return markdown, chosen_model


def main():
    settings = load_generation_settings()
    prompt_context = build_prompt_context(settings)
    body, model = ask_claude_with_web_search(settings, prompt_context)
    write_post(
        body,
        settings,
        used_model=model,
        include_llm_model=True,
    )


if __name__ == "__main__":
    main()
