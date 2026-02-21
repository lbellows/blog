from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:  # pragma: no cover - dotenv optional at import time
    load_dotenv = None  # type: ignore

DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TOPIC_HINT = "Artificial Intelligence news for software engineers shipping on .NET and Azure."
DEFAULT_POST_WORDS_MIN = 200
DEFAULT_POST_WORDS_MAX = 1000
DEFAULT_MAX_SEARCHES = 7
DEFAULT_RECENT_WINDOW_DAYS = 2
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
DEFAULT_BLOCKED_DOMAINS: list[str] = []
DEFAULT_TOPIC_URL: Optional[str] = None
DEFAULT_POST_AUTHOR = "the.serf"
DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-6"
DEFAULT_ANTHROPIC_MAX_TOKENS = 4096
DEFAULT_ANTHROPIC_TEMPERATURE: Optional[float] = 0.9
DEFAULT_FOUNDRY_MODELS = [
    "DeepSeek-V3.1",
    "gpt-5-mini",
    "gpt-oss-120b",
]
DEFAULT_FOUNDRY_MODEL = "gpt-oss-120b"
DEFAULT_FOUNDRY_MAX_TOKENS = 4096
DEFAULT_FOUNDRY_TEMPERATURE: Optional[float] = None
DEFAULT_FOUNDRY_TOP_P: Optional[float] = None
DEFAULT_MEME_GUIDANCE_ENABLED = False
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
    default_author: str = DEFAULT_POST_AUTHOR
    anthropic_model: str = DEFAULT_ANTHROPIC_MODEL
    anthropic_max_tokens: int = DEFAULT_ANTHROPIC_MAX_TOKENS
    anthropic_temperature: Optional[float] = DEFAULT_ANTHROPIC_TEMPERATURE
    foundry_models: list[str] = field(default_factory=list)
    foundry_default_model: str = DEFAULT_FOUNDRY_MODEL
    foundry_max_tokens: int = DEFAULT_FOUNDRY_MAX_TOKENS
    foundry_temperature: Optional[float] = DEFAULT_FOUNDRY_TEMPERATURE
    foundry_top_p: Optional[float] = DEFAULT_FOUNDRY_TOP_P
    meme_guidance_enabled: bool = DEFAULT_MEME_GUIDANCE_ENABLED


def load_generation_settings() -> GenerationSettings:
    _ensure_dotenv_loaded(DEFAULT_REPO_ROOT)

    return GenerationSettings(
        topic_hint=DEFAULT_TOPIC_HINT,
        topic_url=DEFAULT_TOPIC_URL,
        post_words_min=DEFAULT_POST_WORDS_MIN,
        post_words_max=DEFAULT_POST_WORDS_MAX,
        max_searches=DEFAULT_MAX_SEARCHES,
        recent_window_days=DEFAULT_RECENT_WINDOW_DAYS,
        allowed_domains=DEFAULT_ALLOWED_DOMAINS.copy(),
        blocked_domains=DEFAULT_BLOCKED_DOMAINS.copy(),
        foundry_models=DEFAULT_FOUNDRY_MODELS.copy(),
    )


def today_date() -> datetime.date:
    return datetime.date.today()
