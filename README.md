# blog
Tech Thoughts

Trying out some github pages features

link: https://lbellows.github.io/blog/

[Contributor guide →](AGENTS.md)

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

- Generator script: `scripts/generate_post_claude_websearch.py`
- Scheduled workflow: `.github/workflows/daily-post-rag.yml`

## Run the generator locally (for testing)

Install the same dependencies the workflow uses and run the script with your Anthropic key exported:

```sh
python -m pip install --upgrade pip
pip install anthropic python-frontmatter python-slugify pyyaml

export ANTHROPIC_API_KEY="sk-..."
python scripts/generate_post_claude_websearch.py
```

You can also export tunables for a single run (these are the same env names used in the workflow):

```sh
export TOPIC_HINT="Security + AI + .NET"
export MAX_SEARCHES=8
export ALLOWED_DOMAINS="learn.microsoft.com,arxiv.org"
python scripts/generate_post_claude_websearch.py
```

## Tunables (names used in the workflow and what they do)

- `TOPIC_HINT` — short instruction describing audience/angle (example: "AI + .NET + Azure + GitHub + LLM").
- `MAX_SEARCHES` — maximum number of web-search calls the model may perform (integer).
- `ALLOWED_DOMAINS` — comma-separated domains to bias results toward (optional).
- `BLOCKED_DOMAINS` — comma-separated domains to avoid (optional).
- `POST_WORDS_MIN` — minimum desired words in the generated post (int).
- `POST_WORDS_MAX` — maximum desired words in the generated post (int).

These are defined in the `env:` section of `.github/workflows/daily-post-rag.yml`; edit those values to tune scheduled runs.

Example snippet to change them in the workflow `env:` block:

```yaml
TOPIC_HINT: "Security + AI + .NET"
MAX_SEARCHES: "8"
POST_WORDS_MIN: "300"
POST_WORDS_MAX: "1200"
ALLOWED_DOMAINS: "learn.microsoft.com,arxiv.org"
BLOCKED_DOMAINS: "example.com"
```

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

# TODO

* use more breaking news: time box search to only include up to 36 hrs
* less click baity titles
* mix up content - breaking news + larger synopsis (ie. 2025 tips...) - 6:1
* mix styles: news synopsis vs how to tech walkthrough
* add humorous tone
* add images (memes)
* workflow to create article based on specific topic or link
* figure out how to monetize
