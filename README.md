# blog
Tech Thoughts

Trying out some github pages features

link: https://lbellows.github.io/blog/

[Contributor guide →](AGENTS.md)
[Changelog →](CHANGELOG.md)

# About AI blog posting

I needed an easy solution for this because I was holding my daughter, so not too much typing could be involed:

* git workflows
* executes C# (.NET 10) generator
* calls claude API with search tool enabled (or Azure Foundry as alternate provider)
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

- C# solution: `BlogGenerator.sln`
- Console app: `BlogGenerator/Program.cs`
- Core logic: `BlogGenerator.Core/`
- Scheduled workflow: `.github/workflows/daily-post-rag.yml`
- Configuration: `BlogGenerator/appsettings.json`

Provider selection at runtime via CLI arg (`anthropic` or `foundry`) or `AI_PROVIDER` env var.

## Run the generator locally (for testing)

Requires .NET 10 SDK. Run with your Anthropic key exported:

```sh
export ANTHROPIC_API_KEY="sk-..."
dotnet run --project BlogGenerator -- anthropic
```

For Azure Foundry:

```sh
export FOUNDRY_PROJECT_API_KEY="..."
export FOUNDRY_OPENAI_ENDPOINT="https://.../openai/v1/"
dotnet run --project BlogGenerator -- foundry
```

## Run the tests

```sh
dotnet test BlogGenerator.sln
```

## Content defaults (adjust in `appsettings.json`)

- `TopicHint` — short instruction describing audience/angle (example: "AI + .NET + Azure + GitHub + LLM").
- `MaxSearches` — maximum number of web-search calls the model may perform (integer).
- `AllowedDomains` — domains to bias results toward (optional). Defaults include Microsoft/GitHub properties plus tech press (`learn.microsoft.com`, `azure.microsoft.com`, `techcommunity.microsoft.com`, `blogs.microsoft.com`, `devblogs.microsoft.com`, `developer.microsoft.com`, `github.blog`, `techcrunch.com`, `venturebeat.com`, `infoq.com`).
- `BlockedDomains` — domains to avoid (optional).
- `PostWordsMin` — minimum desired words in the generated post.
- `PostWordsMax` — maximum desired words in the generated post.
- `RecentWindowDays` — how many days back the web search should look when hunting for breaking news (defaults to `2`).
- `TopicUrl` — optional primary link to anchor the article around.
- `DefaultAuthor` — default author name injected into front matter.
- `AnthropicModel` — default Claude deployment slug.
- `AnthropicMaxTokens` / `AnthropicTemperature` — controls Claude response length and creativity.
- `FoundryModels` — ordered list of Azure Foundry deployments the REST client will try.
- `FoundryDefaultModel`/`FoundryMaxTokens`/`FoundryTemperature`/`FoundryTopP` — chat parameters applied to Azure Foundry calls.
- `MemeGuidanceEnabled` — toggles whether prompts instruct the model to embed a meme image.
- Generated posts automatically add a model tag (e.g., `claude-sonnet-4-6`) so you can filter by source model.

These are defined in `BlogGenerator/appsettings.json`. Secrets (`ANTHROPIC_API_KEY`, `FOUNDRY_PROJECT_API_KEY`, `FOUNDRY_OPENAI_ENDPOINT`) are read from environment variables only.

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

Pricing: Web search calls are billed in addition to tokens ($10 / 1,000 searches). Keep MaxSearches low (e.g., 3–6) to control cost.

Citations: Claude will include citations automatically in its response when using web search. Your post will then carry those links in the "Further reading" section the prompt asks for.

Domain control: Set AllowedDomains to bias sources you trust (e.g., arxiv.org, blogs.microsoft.com). BlockedDomains can filter out low-quality sites.

Schedule & publish time: Adjust cron and the front-matter timestamp to your preference.

Manual test: Use the workflow's Run workflow button to test once you add the secret. You can select `anthropic` or `foundry` as the provider.

# Content cadence & tone

- Weekday posts now dive deep on one breaking story from the most recent `RecentWindowDays` window.
- Sunday runs switch to a weekly synopsis that blends news and forward-looking tips (e.g., 2025 planning).
- Each post highlights at least one of .NET, Azure, or GitHub while keeping a light, professional sense of humor.
- The generator prompts for a meme image (reuse `assets/images/robot.webp` for now) to keep things playful, and the same setting drives whether we render a contextual meme into each post.
- During generation a contextual meme is rendered from `assets/images/robot.webp` with captions pulled from the title and TL;DR.

# Future

* check if search tool is getting recent items in azure models
* figure out how to monetize
* revisit automatic meme generation once styling and asset library are settled
