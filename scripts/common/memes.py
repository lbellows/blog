from __future__ import annotations

import datetime
import re
import textwrap
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from .settings import GenerationSettings


def _load_meme_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a bold-ish font for meme text with graceful fallback."""
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in font_candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except OSError:
                continue
    return ImageFont.load_default()


def _wrap_text_pixels(text: str, font: ImageFont.ImageFont, draw: ImageDraw.ImageDraw, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        test_line = f"{current} {word}"
        if draw.textlength(test_line, font=font) <= max_width:
            current = test_line
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _draw_caption_block(
    base: Image.Image,
    text: str,
    *,
    position: str,
    top_margin: int = 20,
    bottom_margin: int = 20,
) -> Image.Image:
    if not text:
        return base
    img = base.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    width, height = img.size
    font_size = max(24, width // 18)
    font = _load_meme_font(font_size)
    text = textwrap.shorten(text, width=220, placeholder="…")
    lines = _wrap_text_pixels(text, font, draw, width - 80)
    if not lines:
        lines = [text]

    line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1] if hasattr(font, "getbbox") else font.size + 4
    spacing = 10
    text_height = len(lines) * line_height + spacing * (len(lines) - 1)
    padding = 24

    if position == "top":
        rect_top = top_margin
        rect_bottom = rect_top + text_height + padding * 2
    else:
        rect_bottom = height - bottom_margin
        rect_top = rect_bottom - (text_height + padding * 2)

    rect_top = max(0, rect_top)
    rect_bottom = min(height, rect_bottom)

    draw.rectangle((0, rect_top, width, rect_bottom), fill=(0, 0, 0, 180))

    y = rect_top + padding
    for line in lines:
        txt_width = draw.textlength(line, font=font)
        x = (width - txt_width) / 2
        for dx, dy in ((-2, -2), (-2, 2), (2, -2), (2, 2)):
            draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0, 230))
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        y += line_height + spacing

    return Image.alpha_composite(img, overlay)


def extract_tldr_line(markdown_body: str) -> Optional[str]:
    lines = markdown_body.splitlines()
    for idx, line in enumerate(lines):
        if "**TL;DR**" in line:
            after = line.split("**TL;DR**", 1)[1].strip(" :\t")
            if after:
                return after
            for nxt in lines[idx + 1:]:
                stripped = nxt.strip()
                if stripped:
                    return stripped
            break
    return None


def generate_contextual_meme(
    markdown_body: str,
    title: str,
    slug: str,
    settings: GenerationSettings,
    *,
    base_image_path: Path | None = None,
    output_dir: Path | None = None,
) -> Optional[str]:
    repo_root = settings.repo_root
    base_image = base_image_path or (repo_root / "assets" / "images" / "robot.webp")
    if not base_image.exists():
        print("Base meme image not found; skipping meme generation.")
        return None

    try:
        image = Image.open(base_image)
    except Exception as exc:
        print("Unable to open base meme image:", exc)
        return None

    target_dir = output_dir or (repo_root / "assets" / "images" / "memes")
    target_dir.mkdir(parents=True, exist_ok=True)

    top_text = title.upper()
    bottom_text = extract_tldr_line(markdown_body) or "Azure devs react."

    composed = _draw_caption_block(image, top_text, position="top")
    composed = _draw_caption_block(composed, bottom_text, position="bottom")

    filename = f"{datetime_now_suffix()}-{slug}.png"
    output_path = target_dir / filename
    try:
        composed.convert("RGB").save(output_path, format="PNG", optimize=True)
    except Exception as exc:
        print("Failed to save generated meme:", exc)
        return None

    rel_path = output_path.relative_to(repo_root).as_posix()
    return rel_path


def inject_meme_into_markdown(markdown_body: str, image_path: str, title: str, summary: Optional[str]) -> str:
    if not image_path:
        return markdown_body
    alt_summary = summary or "meme reaction"
    alt_text = textwrap.shorten(f"{title} meme – {alt_summary}", width=80, placeholder="…")
    image_markdown = f"![{alt_text}]({image_path})"

    image_pattern = re.compile(r'!\[[^\]]*\]\([^)]+\)')
    match = image_pattern.search(markdown_body)
    if match:
        return markdown_body[: match.start()] + image_markdown + markdown_body[match.end():]

    lines = markdown_body.splitlines()
    for idx, line in enumerate(lines):
        if "**TL;DR**" in line:
            insert_at = idx + 1
            while insert_at < len(lines) and not lines[insert_at].strip():
                insert_at += 1
            lines.insert(insert_at, image_markdown)
            lines.insert(insert_at + 1, "")
            return "\n".join(lines)

    return image_markdown + "\n\n" + markdown_body


def datetime_now_suffix() -> str:
    return datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
