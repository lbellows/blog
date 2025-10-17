import os, re, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import frontmatter
import anthropic
from slugify import slugify

# ---- Config from env ----
TOPIC_HINT      = os.getenv("TOPIC_HINT", "Artificial Intelligence news for software engineers")
POST_WORDS_MIN  = int(os.getenv("POST_WORDS_MIN", "200"))
POST_WORDS_MAX  = int(os.getenv("POST_WORDS_MAX", "800"))
MAX_SEARCHES    = int(os.getenv("MAX_SEARCHES", "3"))

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

def ask_claude_with_web_search():

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Build tool definition per Anthropic docs
    tool_def = {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": MAX_SEARCHES
    }
    if _allowed:
        tool_def["allowed_domains"] = _allowed
    if _blocked:
        tool_def["blocked_domains"] = _blocked

    resp = client.messages.create(
        model="claude-sonnet-4-5-20250929",  # pick any supported web-search-capable Claude model
        max_tokens=2200,
        temperature=0.6,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": USER_PROMPT}],
        tools=[tool_def]
    )

    # Join text blocks from response
    parts = []
    for block in resp.content:
        if block.type == "text":
            parts.append(block.text)
    return "\n".join(parts).strip()

def extract_title(md: str) -> str:
    m = re.search(r'^\s*#\s+(.+)$', md, re.M)
    if m: return m.group(1).strip()
    # fallback: first non-empty line
    for line in md.splitlines():
        if line.strip():
            return re.sub(r'[#*_`]+', '', line).strip()[:80]
    return "Daily AI Update"

def write_post(markdown_body: str):
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
        "author": "LB Helper",
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
    if list(POSTS_DIR.glob(f"{TODAY:%Y-%m-%d}-*.md")):
        print("Post for today already exists. Exiting.")
        return

    body = ask_claude_with_web_search()
    write_post(body)

if __name__ == "__main__":
    main()
