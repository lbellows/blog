# Changelog

## 2025-11-14
- Consolidated Claude/Foundry defaults (models, token/temperature caps, meme guidance toggle) inside `scripts/common/settings.py` so only secrets and endpoints rely on environment variables.
- Cleaned up the Azure Foundry generator to drop the unused `FOUNDARY_URL` fallback, use the shared settings object, and relocate retry prompts into `scripts/common/prompts.py`.
- Updated `README.md` to describe the new configuration knobs and cleared the completed TODO list.

## 2025-10-23
- Refined `generate_post_websearch.py` to enforce a 2-day breaking-news window, weekday vs. Sunday cadence, humor, and meme prompts.
- Added optional `TOPIC_URL` workflow input plus documentation updates covering the new tunables and tone guidelines.
- Added contextual meme generation with Pillow so each post includes a fresh image saved under `assets/images/memes/`.
- Use more breaking news: time box search to only include up to last 2 days (`RECENT_WINDOW_DAYS`).
- Mix up content cadence: focused weekday posts, Sunday synopsis mode.
- Relax technology coverage: require at least one of .NET/Azure/GitHub per post.
- Add a light humorous tone.
- Prompt for meme-friendly images in the generated markdown.
- Allow workflow input to drive a specific topic or link (`TOPIC_URL`).
- Refactored generators to consume shared prompt, cadence, and meme utilities in `scripts/common/` for both Anthropic and Azure workflows.
- Automatically load local `.env` files when running generators to simplify secret management.
- Strip leading LLM instruction blocks before writing posts so published articles start at the H1 title.
- Expanded default `ALLOWED_DOMAINS` to include Microsoft ecosystem sources and high-signal tech press for fresher breaking news (replacing blocked domains like `theverge.com` and `zdnet.com` with crawler-friendly alternatives).
- Simplified GitHub Actions workflow to lean entirely on code defaults instead of duplicating tunable env vars.
- Locked generator tunables to code-level constants so only secrets come from environment variables.
- Tags are now inferred from post headings/TL;DR and include the source model name (defaulting to Claude); existing posts were retagged accordingly.
