# blog
Tech Thoughts

Trying out some github pages features

link: https://lbellows.github.io/blog/

[Contributor guide →](AGENTS.md)
[Changelog →](CHANGELOG.md)

# About AI blog posting

I needed an easy solution for this because I was holding my daughter, so not too much typing could be involed:

* git workflows
* executes python
* calls claude API with search tool enabled
* writes the blog post in MD & commits
* triggers jekyll build which updates the blog

That is my AI-slop-posting pipeline.  Costs about $0.20 per post (sonnet 4.5). Haiku brings it down to about $0.07. This is mostly exploratory and I hope to test out some other tools/solutions in the future integration with social media.

## Quick start — clone the repo

Open a terminal and run:

```sh
git clone https://github.com/lbellows/blog.git
cd blog
```

## Where the workflow and generator live

- Anthropic generator: `scripts/generate_post_claude.py`
- Azure Foundry generator: `scripts/generate_post_websearch.py`
- Scheduled workflow: `.github/workflows/daily-post-rag.yml`
- Shared helpers for prompts, cadence, and memes: `scripts/common/`

Azure Foundry runs now only read `ENDPOINT_URL` (or `AZURE_OPENAI_ENDPOINT`) plus `FOUNDARY_API_KEY`/`AZURE_OPENAI_API_KEY` from your environment. All other knobs live in `scripts/common/settings.py`.

## Run the generator locally (for testing)

Install the same dependencies the workflow uses and run the script with your Anthropic key exported:

```sh
python -m pip install --upgrade pip
pip install anthropic python-frontmatter python-slugify pyyaml Pillow

export ANTHROPIC_API_KEY="sk-..."
python scripts/generate_post_claude.py
```

Tip: both generators automatically load a `.env` file at the repository root if it exists—only secret values (e.g., API keys) are read from the environment.

## Content defaults (adjust in `scripts/common/settings.py`)

- `TOPIC_HINT` — short instruction describing audience/angle (example: "AI + .NET + Azure + GitHub + LLM").
- `MAX_SEARCHES` — maximum number of web-search calls the model may perform (integer).
- `ALLOWED_DOMAINS` — comma-separated domains to bias results toward (optional). Defaults include Microsoft/GitHub properties plus tech press (`learn.microsoft.com`, `azure.microsoft.com`, `techcommunity.microsoft.com`, `blogs.microsoft.com`, `devblogs.microsoft.com`, `developer.microsoft.com`, `github.blog`, `techcrunch.com`, `venturebeat.com`, `infoq.com`).
- `BLOCKED_DOMAINS` — comma-separated domains to avoid (optional).
- `POST_WORDS_MIN` — minimum desired words in the generated post (int).
- `POST_WORDS_MAX` — maximum desired words in the generated post (int).
- `RECENT_WINDOW_DAYS` — how many days back the web search should look when hunting for breaking news (int, defaults to `2`).
- `TOPIC_URL` — optional primary link to anchor the article around (aliases: `TOPIC_LINK`, `SOURCE_LINK`).
- `POST_AUTHOR` — default author name injected into front matter.
- `ANTHROPIC_MODEL` — default Claude deployment slug used by `scripts/generate_post_claude.py`.
- `ANTHROPIC_MAX_TOKENS` / `ANTHROPIC_TEMPERATURE` — controls Claude response length and creativity.
- `FOUNDRY_MODELS` — ordered list of Azure Foundry deployments the REST client will try.
- `FOUNDRY_DEFAULT_MODEL`/`FOUNDRY_MAX_TOKENS`/`FOUNDRY_TEMPERATURE`/`FOUNDRY_TOP_P` — chat parameters applied to Azure Foundry calls.
- `MEME_GUIDANCE_ENABLED` — toggles whether prompts instruct the model to embed a meme image.
- Generated posts automatically add a `llm_model:<model>` tag (default `claude`) so you can filter by source model.

These are defined as constants in `scripts/common/settings.py` and are no longer read from environment variables. Edit the constants directly if you need to change the publishing defaults.

Tags are derived automatically from section headings/TL;DR content plus the model name (e.g., `claude`). No manual tag list is required.

## Add the secret to GitHub Actions (alternate: CLI)

You already have the UI instruction above (Repo → Settings → Secrets and variables → Actions). As an alternative you can set the secret using the GitHub CLI:

```sh
# securely set your secret value (recommended: read from environment or file)
gh secret set ANTHROPIC_API_KEY --body "$ANTHROPIC_API_KEY"
```

Note: the workflow expects `ANTHROPIC_API_KEY` in repository secrets.

## Secrets to add (one-time) via UI

Repo → Settings → Secrets and variables → Actions:

ANTHROPIC_API_KEY — from your Anthropic account.

## Notes & tips

Models with web search: Claude 3.7 Sonnet and newer (plus several others) support this tool; see the docs for the supported list. 

Pricing: Web search calls are billed in addition to tokens ($10 / 1,000 searches). Keep MAX_SEARCHES low (e.g., 3–6) to control cost. 

Citations: Claude will include citations automatically in its response when using web search. Your post will then carry those links in the “Further reading” section the prompt asks for. 

Domain control: Set ALLOWED_DOMAINS to bias sources you trust (e.g., arxiv.org,blogs.microsoft.com,developer.nvidia.com). BLOCKED_DOMAINS can filter out low-quality sites. 

Schedule & publish time: Adjust cron and the front-matter timestamp to your preference.

Manual test: Use the workflow’s Run workflow button to test once you add the secret.

# Content cadence & tone

- Weekday posts now dive deep on one breaking story from the most recent `RECENT_WINDOW_DAYS` window.
- Sunday runs switch to a weekly synopsis that blends news and forward-looking tips (e.g., 2025 planning).
- Each post highlights at least one of .NET, Azure, or GitHub while keeping a light, professional sense of humor.
- The generator prompts for a meme image (reuse `assets/images/robot.webp` for now) to keep things playful, and the same setting drives whether we render a contextual meme into each post.
- During generation a contextual meme is rendered from `assets/images/robot.webp` with captions pulled from the title and TL;DR.

# Future

* check if search tool is getting recent items in azure models
* figure out how to monetize
* revisit automatic meme generation once styling and asset library are settled
