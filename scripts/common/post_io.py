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
    match = re.search(r'^\s*#\s+(.+)$', markdown_body, re.M)
    if match:
        return match.group(1).strip()
    for line in markdown_body.splitlines():
        if line.strip():
            return re.sub(r'[#*_`]+', '', line).strip()[:80]
    return "Daily AI Update"


def _posts_dir(settings: GenerationSettings, override_dir: Path | None) -> Path:
    if override_dir:
        return override_dir
    path = settings.repo_root / "_posts"
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_post(
    markdown_body: str,
    settings: GenerationSettings,
    *,
    used_model: str | None = None,
    author: str = "the.serf",
    tags: Sequence[str] | None = None,
    output_dir: Path | None = None,
    today: datetime.date | None = None,
    enable_meme: bool = True,
    include_llm_model: bool = False,
    extra_front_matter: Optional[Dict[str, str]] = None,
) -> Tuple[Path, Optional[str]]:
    current_day = today or today_date()
    posts_dir = _posts_dir(settings, output_dir)
    posts_dir.mkdir(parents=True, exist_ok=True)

    title = extract_title(markdown_body)
    slug = slugify(title)[:80]

    if list(posts_dir.glob(f"{current_day:%Y-%m-%d}-*.md")):
        slug += "-2"

    summary = extract_tldr_line(markdown_body)
    meme_rel_path: Optional[str] = None
    if enable_meme:
        meme_rel_path = generate_contextual_meme(markdown_body, title, slug, settings)
        if meme_rel_path:
            markdown_body = inject_meme_into_markdown(markdown_body, meme_rel_path, title, summary)

    post_path = posts_dir / f"{current_day:%Y-%m-%d}-{slug}.md"

    now_ny = datetime.datetime.now(ZoneInfo("America/New_York"))
    publish_dt = now_ny - datetime.timedelta(minutes=1)

    front_matter = {
        "layout": "post",
        "title": title,
        "date": publish_dt.strftime("%Y-%m-%d %H:%M:%S %z"),
        "tags": list(tags) if tags else ["ai", "automation", "news"],
        "author": author,
    }
    if include_llm_model:
        front_matter["llm_model"] = used_model or ""
    if extra_front_matter:
        front_matter.update(extra_front_matter)

    post = frontmatter.Post(markdown_body, **front_matter)
    text = frontmatter.dumps(post)
    with open(post_path, "w", encoding="utf-8") as handle:
        handle.write(text)

    print("Wrote", post_path)
    return post_path, meme_rel_path
