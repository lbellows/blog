from __future__ import annotations

import datetime
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:  # pragma: no cover - dotenv optional at import time
    load_dotenv = None  # type: ignore

DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ALLOWED_DOMAINS = [
    "learn.microsoft.com",
    "azure.microsoft.com",
    "techcommunity.microsoft.com",
    "blogs.microsoft.com",
    "devblogs.microsoft.com",
    "github.blog",
    "developer.microsoft.com",
    "techcrunch.com",
    "venturebeat.com",
    "infoq.com",
]
_DOTENV_LOADED = False


def _ensure_dotenv_loaded(repo_root: Path) -> None:
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return
    _DOTENV_LOADED = True
    if load_dotenv is None:
        return
    dotenv_path = repo_root / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)


@dataclass(frozen=True)
class GenerationSettings:
    topic_hint: str
    topic_url: Optional[str]
    post_words_min: int
    post_words_max: int
    max_searches: int
    recent_window_days: int
    allowed_domains: list[str] = field(default_factory=list)
    blocked_domains: list[str] = field(default_factory=list)
    repo_root: Path = field(default_factory=lambda: DEFAULT_REPO_ROOT)


def _split_domains(value: str | None) -> list[str]:
    if not value:
        return []
    return [domain.strip() for domain in value.split(",") if domain.strip()]


def load_generation_settings() -> GenerationSettings:
    _ensure_dotenv_loaded(DEFAULT_REPO_ROOT)

    topic_hint = os.getenv("TOPIC_HINT", "Artificial Intelligence news for software engineers")
    topic_url = (
        os.getenv("TOPIC_URL")
        or os.getenv("TOPIC_LINK")
        or os.getenv("SOURCE_LINK")
    )
    post_words_min = int(os.getenv("POST_WORDS_MIN", "200"))
    post_words_max = int(os.getenv("POST_WORDS_MAX", "800"))
    max_searches = int(os.getenv("MAX_SEARCHES", "5"))
    recent_window_days = int(os.getenv("RECENT_WINDOW_DAYS", "2"))

    allowed_env = _split_domains(os.getenv("ALLOWED_DOMAINS"))
    allowed = allowed_env or DEFAULT_ALLOWED_DOMAINS.copy()
    if allowed_env:
        # ensure no duplicates while preserving declared order
        seen = set()
        deduped = []
        for domain in allowed_env + DEFAULT_ALLOWED_DOMAINS:
            if domain and domain not in seen:
                seen.add(domain)
                deduped.append(domain)
        allowed = deduped

    blocked = _split_domains(os.getenv("BLOCKED_DOMAINS"))

    return GenerationSettings(
        topic_hint=topic_hint,
        topic_url=topic_url,
        post_words_min=post_words_min,
        post_words_max=post_words_max,
        max_searches=max_searches,
        recent_window_days=recent_window_days,
        allowed_domains=allowed,
        blocked_domains=blocked,
    )


def today_date() -> datetime.date:
    return datetime.date.today()
