# Startup routine
Check for TODOs in the README. Once a TODO is complete, remove from the README and add an entry to CHANGELOG.md (linked from README) with a short description of the change. If none are found or all are complete ask for instructions.

# Repository Guidelines

## Generators & Shared Utilities
The blog generator is a C# .NET 10 solution at `scripts/BlogGenerator/`.
- Console app entry point: `scripts/BlogGenerator/src/BlogGenerator/Program.cs`
- Core logic (providers, prompts, post writing, memes): `scripts/BlogGenerator/src/BlogGenerator.Core/`
- Unit tests: `scripts/BlogGenerator/tests/BlogGenerator.Tests/`
- Configuration: `scripts/BlogGenerator/src/BlogGenerator/appsettings.json` (non-secret settings only)
- Provider selection at runtime via CLI arg or `AI_PROVIDER` env var: `anthropic` or `foundry`

## Project Structure & Module Organization
Jekyll powers this GitHub Pages blog. `_config.yml` controls metadata, `_includes/` holds partials, and `index.html` is the landing page. Assets sit in `assets/css/styles.css` and `assets/images/`. Automation lives under `scripts/BlogGenerator/`; sample posts for spot checks are in `tests/posts/`. The generator creates `_posts/` at runtime (left untracked); keep filenames `YYYY-MM-DD-title.md` so Jekyll picks them up.

## Build, Test, and Development Commands
- `dotnet build scripts/BlogGenerator/BlogGenerator.sln` builds the solution.
- `dotnet test scripts/BlogGenerator/BlogGenerator.sln` runs unit tests (title extraction, tag inference, prompt building, meme injection, etc.).
- `dotnet run --project scripts/BlogGenerator/src/BlogGenerator -- anthropic` generates a post using Anthropic Claude; export `ANTHROPIC_API_KEY` first.
- `dotnet run --project scripts/BlogGenerator/src/BlogGenerator -- foundry` generates a post using Azure Foundry; set `FOUNDARY_API_KEY`/`ENDPOINT_URL` secrets first.
- `bundle exec jekyll serve --livereload` previews the site locally after installing the `github-pages` gem.
- Default allowed domains bias search toward Microsoft/.NET announcements and reputable tech press; edit `AllowedDomains` in `appsettings.json` if you need changes.
- Posts must retain the model-name tag (e.g., `claude`) that the generator derives from content.
- Scheduled workflow relies on the defaults in `appsettings.json`; avoid reintroducing duplicate tunables into `.github/workflows/daily-post-rag.yml`.

## Coding Style & Naming Conventions
Follow standard C# conventions: PascalCase for public members, camelCase for locals, four-space indentation. Generated front matter should mimic `tests/posts/test-post.md`, using lowercase tags and minimal quoting. CSS stays in one file—use descriptive classes such as `.post-summary` and cluster overrides by feature.

## Testing Guidelines
Run `dotnet test` to execute the xUnit test suite covering prompt building, title extraction, tag inference, slug generation, meme extraction/injection, and post output. After generating a post, review it via the local Jekyll preview and confirm external links resolve. Store regression samples in `tests/posts/` to document expected structure.

## Commit & Pull Request Guidelines
Commit messages stay short and imperative (`clean up`, `testing multi llm via azure`), with optional scopes for post runs (`chore(posts): ...`). Keep commits focused and avoid mixing regenerated posts with script changes. Pull requests should summarize publishing impact, link related issues, attach preview screenshots for UI tweaks, and call out new env vars or secrets.

## Security & Configuration Tips
Store `FOUNDARY_API_KEY` and `ANTHROPIC_API_KEY` as GitHub secrets; never commit `.env` artifacts. Only secrets should come from env vars—content defaults are maintained in `appsettings.json`. Review `_config.yml` before enabling plugins to stay within the GitHub Pages allowlist.
