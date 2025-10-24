import os, re, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import frontmatter
from slugify import slugify
import random
import json
import requests


# ---- Config from env ----
TOPIC_HINT      = os.getenv("TOPIC_HINT", "Artificial Intelligence news for software engineers")
TOPIC_URL       = os.getenv("TOPIC_URL") or os.getenv("TOPIC_LINK") or os.getenv("SOURCE_LINK")
POST_WORDS_MIN  = int(os.getenv("POST_WORDS_MIN", "200"))
POST_WORDS_MAX  = int(os.getenv("POST_WORDS_MAX", "800"))
MAX_SEARCHES    = int(os.getenv("MAX_SEARCHES", "5"))
RECENT_WINDOW_DAYS = int(os.getenv("RECENT_WINDOW_DAYS", "2"))

# Default Foundry models (from your screenshot). You can override via FOUNDARY_MODELS env var (comma-separated).
FOUNDARY_MODELS_DEFAULT = [
    "DeepSeek-V3.1",
    "gpt-5-mini",
    "gpt-oss-120b",
    # "Llama-4-Maverick-17B-128E-Instruct-FP8",
]

_allowed = [d.strip() for d in os.getenv("ALLOWED_DOMAINS", "").split(",") if d.strip()]
_blocked = [d.strip() for d in os.getenv("BLOCKED_DOMAINS", "").split(",") if d.strip()]

TODAY = datetime.date.today()
RECENT_START_DATE = TODAY - datetime.timedelta(days=RECENT_WINDOW_DAYS)
WEEKDAY_INDEX = TODAY.weekday()  # Monday=0
IS_SUNDAY = WEEKDAY_INDEX == 6

if IS_SUNDAY:
    MODE_INSTRUCTIONS = (
        "Sunday is synopsis day: weave the freshest breaking stories into a cohesive weekly roundup "
        "that also previews what's next (e.g., 2025 readiness tips, roadmap considerations)."
    )
else:
    MODE_INSTRUCTIONS = (
        f"Pick one laser-focused story or product update from the last {RECENT_WINDOW_DAYS} day(s) "
        "and dive deep into its implications. Avoid broad grab-bag summaries."
    )

TECH_GUIDANCE = (
    "Highlight at least one of these ecosystems where relevant: .NET, Azure, or GitHub. "
    "Choose whichever best fits the story; covering all three is optional."
)
HUMOR_GUIDANCE = (
    "Keep the tone professional yet witty—sprinkle in light, tasteful humor or asides that help the reader stay engaged."
)
IMAGE_GUIDANCE = (
    "Embed at least one Markdown image that works as a meme (reuse assets/images/robot.webp or another credited meme) "
    "with a descriptive, humorous alt text."
)

USER_INSTRUCTION_ITEMS = [
    f"Use the web_search tool to find 4-6 fresh, reputable sources published between {RECENT_START_DATE.isoformat()} and {TODAY.isoformat()} (or as close as possible).",
    MODE_INSTRUCTIONS,
    "Synthesize the key points that matter to engineers (cost, latency, APIs, integration steps).",
    "Cite sources inline where appropriate and list all links at the end in a 'Further reading' list.",
]

if TOPIC_URL:
    USER_INSTRUCTION_ITEMS.insert(
        2,
        "Treat the primary requested link as the anchor narrative—summarize it first, then expand with corroborating context."
    )

USER_INSTRUCTION_TEXT = "\n".join(f"{idx + 1}) {item}" for idx, item in enumerate(USER_INSTRUCTION_ITEMS))
PRIMARY_LINK_LINE = f"Primary requested link: {TOPIC_URL}\n" if TOPIC_URL else ""

REPO_ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR  = REPO_ROOT / "_posts"
POSTS_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = f"""
You are a senior technical writer for software engineers working with .NET, Azure, and GitHub.
Use the web_search tool to gather several fresh, reputable sources about current AI developments
that impact developers. Then write a grounded Markdown blog post with:

- A single H1 title on the first line (non-clickbait, specific).
- A short **TL;DR** section.
- Clear sections with practical takeaways (code or CLI snippets welcome).
- {TECH_GUIDANCE}
- {HUMOR_GUIDANCE}
- {IMAGE_GUIDANCE}
- Cautious language for claims; avoid speculation and hallucinations.
- A **Further reading** section listing all source links as plain URLs.

Length: {POST_WORDS_MIN}-{POST_WORDS_MAX} words. US English. Markdown only (no HTML).
If web search fails or yields little, write a pragmatic evergreen piece for the same audience.
If the web_search tool is unavailable, do not emit tool-call markup (e.g., <|start|> tokens); respond directly with the final article.
"""

USER_PROMPT = f"""
Topic focus / audience: {TOPIC_HINT}
{PRIMARY_LINK_LINE}

Instructions:
{USER_INSTRUCTION_TEXT}
"""

def ask_azure_foundry_with_web_search(foundry_model: str | None = None, post_fn=None, _extra_messages=None):
    """Call Azure OpenAI (Foundry) using the AzureOpenAI SDK.

    Maps env vars:
      - FOUNDARY_URL -> endpoint (falls back to ENDPOINT_URL)
      - FOUNDARY_API_KEY -> api key (falls back to AZURE_OPENAI_API_KEY)
      - foundry_model -> deployment name (falls back to FOUNDARY_MODEL or DEPLOYMENT_NAME)
    """

    # Use ENDPOINT_URL (service root) if present, otherwise try FOUNDARY_URL
    endpoint = os.environ.get("ENDPOINT_URL") or os.environ.get("FOUNDARY_URL")
    if not endpoint:
        raise RuntimeError("ENDPOINT_URL or FOUNDARY_URL must be set to the Azure OpenAI service root")

    # Normalize endpoint (no trailing slash)
    endpoint = endpoint.rstrip("/")

    subscription_key = os.environ.get("FOUNDARY_API_KEY") or os.environ.get("AZURE_OPENAI_API_KEY")
    deployment = foundry_model or os.environ.get("FOUNDARY_MODEL") or os.environ.get("DEPLOYMENT_NAME") or "gpt-oss-120b"

    if not subscription_key:
        raise RuntimeError("FOUNDARY_API_KEY or AZURE_OPENAI_API_KEY not set for REST Foundry client")

    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2025-01-01-preview"

    # Build messages as content blocks similar to your curl example
    messages = [
        {"role": "system", "content": [{"type": "text", "text": SYSTEM_PROMPT}]},
        {"role": "user", "content": [{"type": "text", "text": USER_PROMPT}]},
    ]
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

    # Allow injection of a requests-like post function for testing
    post = post_fn or requests.post
    # Try a request, and if a model rejects `max_tokens` (some Foundry models
    # expect `max_completion_tokens`) retry once with the alternate param.
    resp = post(url, json=payload, headers=headers, timeout=60)

    # If the model rejects the parameter, attempt a retry using
    # `max_completion_tokens` instead of `max_tokens`.
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

        # Detect common message that 'max_tokens' is unsupported and retry
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
            # Build a new payload replacing the key
            new_payload = dict(payload)
            val = new_payload.pop('max_tokens', None)
            if val is None:
                # nothing to retry with
                pass
            else:
                new_payload['max_completion_tokens'] = val
                resp = post(url, json=new_payload, headers=headers, timeout=60)

        # If still not ok, try removing unsupported temperature settings.
        if not resp.ok:
            try:
                msg = json.dumps(body) if isinstance(body, dict) else str(body)
            except Exception:
                msg = str(body)
            if resp.status_code == 400 and 'temperature' in msg and 'unsupported' in msg:
                resp = _maybe_retry_with(drop_keys=("temperature",))
                if not resp.ok:
                    resp = _maybe_retry_with({"top_p": 1.0}, drop_keys=("temperature",))

        # After optional retry, if still not ok raise a helpful error
        if not resp.ok:
            body = None
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            raise RuntimeError(f"Foundry REST call failed: {resp.status_code} {resp.reason}: {body}")

    data = resp.json()

    # Parse response: choices -> message -> content
    texts = []
    if isinstance(data, dict):
        choices = data.get("choices") or []
        for c in choices:
            # c.message.content may be a list of blocks or a string
            msg = c.get("message") or {}
            content = msg.get("content") or c.get("text") or c.get("delta")
            if isinstance(content, list):
                # join text blocks
                for block in content:
                    if isinstance(block, dict):
                        # prefer 'text' key
                        if "text" in block and isinstance(block["text"], str):
                            texts.append(block["text"])
                        elif "content" in block and isinstance(block["content"], str):
                            texts.append(block["content"])
            elif isinstance(content, str):
                texts.append(content)

    # Fallback: try top-level 'choices[0].message' string conversion
    if not texts:
        try:
            # try common nested path
            first = data.get("choices", [None])[0]
            if first:
                msg = first.get("message") or first.get("delta") or first.get("text")
                if isinstance(msg, str):
                    texts.append(msg)
                elif isinstance(msg, dict) and isinstance(msg.get("content"), str):
                    texts.append(msg.get("content"))
        except Exception:
            pass

    if not texts:
        # last resort: serialize the response
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
            foundry_model=foundry_model,
            post_fn=post_fn,
            _extra_messages=fallback_instruction,
        )

    return markdown


def ask_with_web_search():
    """Select a provider at random and ask it to produce the markdown post.

    The selection is weighted: if FOUNDARY is configured we pick between
    'foundry' and 'claude' with equal weight. Any failure from the chosen
    provider falls back to Claude.
    """


    # Only use Azure Foundry models for testing per request. Choose a model
    # at random from FOUNDARY_MODELS_DEFAULT or an override in FOUNDARY_MODELS.
    if not os.environ.get("FOUNDARY_API_KEY"):
        raise RuntimeError("FOUNDARY_API_KEY not set; cannot call Azure Foundry")

    env_models = [m.strip() for m in os.environ.get("FOUNDARY_MODELS", "").split(",") if m.strip()]
    models = env_models or FOUNDARY_MODELS_DEFAULT

    # Try models in a random (non-weighted) order and fall back if a deployment
    # wasn't found. For other errors (authentication, 4xx/5xx), raise immediately.
    random.shuffle(models)
    last_err = None
    for candidate in models:
        print("Trying Foundry model:", candidate)
        try:
            body = ask_azure_foundry_with_web_search(foundry_model=candidate)
            print("Found working model:", candidate)
            return body, candidate
        except RuntimeError as e:
            last_err = e
            # If the server explicitly reported DeploymentNotFound or 404, try next
            msg = str(e)
            if "DeploymentNotFound" in msg or "404" in msg:
                print(f"Deployment {candidate} not found, trying next model...")
                continue
            # For any other runtime error, re-raise so the caller can see it
            raise

    # If we exhausted models, raise the last error
    raise RuntimeError(f"No available Foundry deployment found after trying models: {models}. Last error: {last_err}")

def extract_title(md: str) -> str:
    m = re.search(r'^\s*#\s+(.+)$', md, re.M)
    if m: return m.group(1).strip()
    # fallback: first non-empty line
    for line in md.splitlines():
        if line.strip():
            return re.sub(r'[#*_`]+', '', line).strip()[:80]
    return "Daily AI Update"

def write_post(markdown_body: str, used_model: str | None = None, output_dir: Path | None = None):
    title = extract_title(markdown_body)
    slug  = slugify(title)[:80]

    target_dir = output_dir or POSTS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    # Avoid duplicate per day
    existing = list(target_dir.glob(f"{TODAY:%Y-%m-%d}-*.md"))
    if existing:
        slug += "-2"

    path = target_dir / f"{TODAY:%Y-%m-%d}-{slug}.md"

    now_ny = datetime.datetime.now(ZoneInfo("America/New_York"))
    publish_dt = now_ny - datetime.timedelta(minutes=1)

    fm = {
        "layout": "post",
        "title": title,
        "date": publish_dt.strftime("%Y-%m-%d %H:%M:%S %z"),
        "tags": ["ai", "automation", "news"],
        "author": f"the.serf (model: {used_model})" if used_model else "the.serf",
        "llm_model": used_model or "",
    }
    post = frontmatter.Post(markdown_body, **fm)
    # frontmatter.dump attempts to write bytes when given an encoding; use dumps to get
    # a text string and write that using a text-mode file with utf-8 encoding.
    text = frontmatter.dumps(post)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Wrote", path)

def main():
    # Skip if a same-day post already exists (optional—comment out if you want multiple/day)
    # if list(POSTS_DIR.glob(f"{TODAY:%Y-%m-%d}-*.md")):
    #     print("Post for today already exists. Exiting.")
    #     return

    body, used_model = ask_with_web_search()
    write_post(body, used_model=used_model)

if __name__ == "__main__":
    main()
