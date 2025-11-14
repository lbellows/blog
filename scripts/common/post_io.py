from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Dict, Iterable, Optional, Sequence, Tuple

import frontmatter
from slugify import slugify
from zoneinfo import ZoneInfo

from .memes import (
    extract_tldr_line,
    generate_contextual_meme,
    inject_meme_into_markdown,
)
from .settings import GenerationSettings, today_date


def extract_title(markdown_body: str) -> str:
    markdown_body = markdown_body.lstrip()
    match = re.search(r'^\s*#\s+(.+)$', markdown_body, re.M)
    if match:
        return match.group(1).strip()
    for line in markdown_body.splitlines():
        if line.strip():
            return re.sub(r'[#*_`]+', '', line).strip()[:80]
    return "Daily AI Update"


def _posts_dir(settings: GenerationSettings) -> Path:

    path = settings.repo_root / "_posts"
    path.mkdir(parents=True, exist_ok=True)
    return path


STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "into", "from", "your", "you",
    "are", "was", "will", "have", "using", "about", "what", "need", "know",
    "into", "over", "its", "their", "those", "these",
    "such", "tips", "guide", "latest", "today", "tomorrow", "overview", "intro",
    "developers", "developer", "engineers", "engineer", "update", "updates",
    "insights", "insight", "future", "news", "deep", "dive", "focus", "weekly",
    "daily", "report", "analysis", "roundup", "learn", "learning", "build",
    "building", "powered", "power", "next", "gen", "generative", "recent",
    "versus", "plus", "look", "back", "ahead", "quick", "start", "setup",
    "create", "creating", "created", "some", "page", "pages", "step", "steps",
}


def _strip_leading_instructions(markdown_body: str) -> str:
    lines = markdown_body.splitlines()
    cleaned: list[str] = []
    found_heading = False
    for line in lines:
        if not found_heading:
            if line.strip().startswith("#"):
                found_heading = True
                cleaned.append(line)
            else:
                # drop preamble lines (LLM instructions, etc.)
                continue
        else:
            cleaned.append(line)
    if found_heading:
        return "\n".join(cleaned).lstrip("\n")
    return markdown_body.strip()


def _normalize_tag(token: str) -> str:
    token = token.strip().lower()
    if not token or token in STOPWORDS or len(token) < 3:
        return ""
    if not re.search(r"[a-z]", token):
        return ""
    token = re.sub(r"[^\w\+\-\.]", "-", token)
    token = re.sub(r"-{2,}", "-", token).strip("-")
    return token


def _infer_tags(markdown_body: str, model: str | None) -> list[str]:
    candidates: Dict[str, int] = {}
    sections = []
    for line in markdown_body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            sections.append(stripped.lstrip("#").strip())
        elif stripped.lower().startswith("**tl;dr**"):
            sections.append(stripped.split("**TL;DR**", 1)[-1].strip(" :"))
    text_blob = " ".join(sections) or markdown_body
    for token in re.findall(r"[A-Za-z0-9\+\.\-]+", text_blob):
        normalized = _normalize_tag(token)
        if normalized:
            candidates[normalized] = candidates.get(normalized, 0) + 1
    tags: list[str] = []
    for token, _ in sorted(candidates.items(), key=lambda item: (-item[1], item[0])):
        if token not in tags:
            tags.append(token)
        if len(tags) >= 5:
            break
    lowermd = markdown_body.lower()
    if "ai" in lowermd and "ai" not in tags:
        tags.append("ai")
    model_tag = (model or "claude").strip().lower()
    if model_tag and model_tag not in tags:
        tags.append(model_tag)
    if not tags:
        tags = ["ai", model_tag or "claude"]
    if len(tags) > 6:
        core = [tag for tag in tags if tag != model_tag]
        trimmed = core[:5]
        if model_tag:
            trimmed.append(model_tag)
        tags = trimmed
    return tags


def write_post(
    markdown_body: str,
    settings: GenerationSettings,
    *,
    used_model: str | None = None
) -> Tuple[Path, Optional[str]]:
    markdown_body = _strip_leading_instructions(markdown_body)

    current_day = today_date()
    posts_dir = _posts_dir(settings)
    posts_dir.mkdir(parents=True, exist_ok=True)

    title = extract_title(markdown_body)
    slug = slugify(title)[:80]

    if list(posts_dir.glob(f"{current_day:%Y-%m-%d}-*.md")):
        slug += "-2"

    summary = extract_tldr_line(markdown_body)
    effective_author = settings.default_author
    meme_flag = settings.meme_guidance_enabled
    meme_rel_path: Optional[str] = None
    if meme_flag:
        meme_rel_path = generate_contextual_meme(markdown_body, title, slug, settings)
        if meme_rel_path:
            markdown_body = inject_meme_into_markdown(markdown_body, meme_rel_path, title, summary)

    post_path = posts_dir / f"{current_day:%Y-%m-%d}-{slug}.md"

    now_ny = datetime.datetime.now(ZoneInfo("America/New_York"))
    publish_dt = now_ny - datetime.timedelta(minutes=1)

    model_tag = (used_model or "claude").strip()
    merged_tags = _infer_tags(markdown_body, model_tag)

    front_matter = {
        "layout": "post",
        "title": title,
        "date": publish_dt.strftime("%Y-%m-%d %H:%M:%S %z"),
        "tags": merged_tags,
        "author": effective_author,
    }

    post = frontmatter.Post(markdown_body, **front_matter)
    text = frontmatter.dumps(post)
    with open(post_path, "w", encoding="utf-8") as handle:
        handle.write(text)

    print("Wrote", post_path)
    return post_path, meme_rel_path
