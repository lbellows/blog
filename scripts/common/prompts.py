from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List

from .settings import GenerationSettings, today_date


TECH_GUIDANCE = (
    "Highlight at least one of these ecosystems where relevant: .NET, Azure, or any AI related software. "
    "Choose whichever best fits the story; covering all three is optional."
)
HUMOR_GUIDANCE = (
    "Keep the tone professional yet witty—sprinkle in light, tasteful humor or asides that help the reader stay engaged."
)
IMAGE_GUIDANCE = (
    "Embed at least one Markdown image that works as a meme (reuse assets/images/robot.webp or another credited meme) "
    "with a descriptive, humorous alt text."
)


@dataclass(frozen=True)
class PromptContext:
    today: datetime.date
    recent_start_date: datetime.date
    mode_instructions: str
    system_prompt: str
    user_prompt: str
    user_instruction_items: List[str]
    primary_link_line: str


def _mode_instructions(today: datetime.date, recent_window_days: int) -> str:
    if today.weekday() == 6:  # Sunday
        return (
            "Sunday is synopsis day: weave the freshest breaking stories into a cohesive weekly roundup "
            "that also previews what's next (e.g., 2025 readiness tips, roadmap considerations)."
        )
    return (
        f"Pick one laser-focused story or product update from the last {recent_window_days} day(s) "
        "and dive deep into its implications. Avoid broad grab-bag summaries."
    )


def _user_instruction_items(settings: GenerationSettings, today: datetime.date, recent_start_date: datetime.date) -> List[str]:
    items = [
        f"Use the web_search tool to find 4-6 fresh, reputable sources published between "
        f"{recent_start_date.isoformat()} and {today.isoformat()} (or as close as possible).",
        _mode_instructions(today, settings.recent_window_days),
        "Synthesize the key points that matter to engineers (cost, latency, APIs, integration steps).",
        "Cite sources inline where appropriate and list all links at the end in a 'Further reading' list.",
    ]
    if settings.topic_url:
        items.insert(
            2,
            "Treat the primary requested link as the anchor narrative—summarize it first, then expand with corroborating context."
        )
    return items


def build_prompt_context(
    settings: GenerationSettings,
    *,
    today: datetime.date | None = None,
) -> PromptContext:
    current_day = today or today_date()
    recent_start = current_day - datetime.timedelta(days=settings.recent_window_days)
    mode_text = _mode_instructions(current_day, settings.recent_window_days)
    user_items = _user_instruction_items(settings, current_day, recent_start)
    user_instruction_text = "\n".join(f"{idx + 1}) {item}" for idx, item in enumerate(user_items))
    primary_line = f"Primary requested link: {settings.topic_url}\n" if settings.topic_url else ""

    system_prompt = f"""
You are a senior technical writer for software engineers working with .NET, Azure, and AI Software.
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

Length: {settings.post_words_min}-{settings.post_words_max} words. US English. Markdown only (no HTML).
If web search fails or yields little, write a pragmatic evergreen piece for the same audience.
If the web_search tool is unavailable, do not emit tool-call markup (e.g., <|start|> tokens); respond directly with the final article.
""".strip()

    user_prompt = f"""
Topic focus / audience: {settings.topic_hint}
{primary_line}

Instructions:
{user_instruction_text}
""".strip()

    return PromptContext(
        today=current_day,
        recent_start_date=recent_start,
        mode_instructions=mode_text,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        user_instruction_items=user_items,
        primary_link_line=primary_line,
    )
