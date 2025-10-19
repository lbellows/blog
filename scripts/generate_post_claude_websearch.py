import os, re, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import frontmatter
import anthropic
from slugify import slugify
import random
import requests
import json

# ---- Config from env ----
TOPIC_HINT      = os.getenv("TOPIC_HINT", "Artificial Intelligence news for software engineers")
POST_WORDS_MIN  = int(os.getenv("POST_WORDS_MIN", "200"))
POST_WORDS_MAX  = int(os.getenv("POST_WORDS_MAX", "800"))
MAX_SEARCHES    = int(os.getenv("MAX_SEARCHES", "5"))

# Default Foundry models (from your screenshot). You can override via FOUNDARY_MODELS env var (comma-separated).
FOUNDARY_MODELS_DEFAULT = [
    "DeepSeek-V3.1",
    "gpt-5-mini",
    "gpt-oss-120b",
    "Llama-4-Maverick-17B-128E-1",
]

_allowed = [d.strip() for d in os.getenv("ALLOWED_DOMAINS", "").split(",") if d.strip()]
_blocked = [d.strip() for d in os.getenv("BLOCKED_DOMAINS", "").split(",") if d.strip()]

TODAY = datetime.date.today()
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
- Cautious language for claims; avoid speculation and hallucinations.
- A **Further reading** section listing all source links as plain URLs.

Length: {POST_WORDS_MIN}-{POST_WORDS_MAX} words. US English. Markdown only (no HTML).
If web search fails or yields little, write a pragmatic evergreen piece for the same audience.
"""

USER_PROMPT = f"""
Topic focus / audience: {TOPIC_HINT}

Instructions:
1) Use the web_search tool to find 4-6 fresh, reputable sources (last few days/weeks).
2) Synthesize the key points that matter to engineers (cost, latency, APIs, integration steps).
3) Cite sources inline where appropriate and list all links at the end in a 'Further reading' list.
"""

def ask_azure_foundry_with_web_search(foundry_model: str | None = None, post_fn=None):
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

    payload = {
        "messages": messages,
        "temperature": 0.6,
        "top_p": 0.95,
        "max_tokens": 2048,
    }

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
            if resp.status_code == 400 and ('max_tokens' in msg and ('unsupported' in msg or 'not supported' in msg or 'unsupported_parameter' in msg)):
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

    return "\n".join(t.strip() for t in texts if t).strip()


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

def write_post(markdown_body: str, used_model: str | None = None):
    title = extract_title(markdown_body)
    slug  = slugify(title)[:80]

    # Avoid duplicate per day
    existing = list(POSTS_DIR.glob(f"{TODAY:%Y-%m-%d}-*.md"))
    if existing:
        slug += "-2"

    path = POSTS_DIR / f"{TODAY:%Y-%m-%d}-{slug}.md"

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
