# Changelog

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
