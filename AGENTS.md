# Startup routine
Check for TODOs in the README. Once a TODO is complete, add an entry to CHANGELOG.md (linked from README) with a short descrition of the change. If none are found or all are complete ask for instructions.

# Repository Guidelines

## Generators & Shared Utilities
- Anthropic workflow entry point: `scripts/generate_post_claude.py`
- Azure Foundry workflow entry point: `scripts/generate_post_websearch.py`
- Shared prompt/cadence/meme helpers live under `scripts/common/` (always update these rather than duplicating logic).

## Azure AI SDK
### Install the following dependencies: azure.identity and azure-ai-inference
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = os.getenv("AZURE_INFERENCE_SDK_ENDPOINT", "https://xxx.services.ai.azure.com/models")
model_name = os.getenv("DEPLOYMENT_NAME", "GPT-5")
key = os.getenv("AZURE_INFERENCE_SDK_KEY", "YOUR_KEY_HERE")
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

response = client.complete(
  messages=[
    SystemMessage(content="You are a helpful assistant."),
    UserMessage(content="What are 3 things to visit in Seattle?")
  ],
  model = model_name,
  max_tokens=1000
)

print(response)

## Project Structure & Module Organization
Jekyll powers this GitHub Pages blog. `_config.yml` controls metadata, `_includes/` holds partials, and `index.html` is the landing page. Assets sit in `assets/css/styles.css` and `assets/images/`. Automation lives under `scripts/`; sample posts for spot checks are in `tests/posts/`. The generator creates `_posts/` at runtime (left untracked); keep filenames `YYYY-MM-DD-title.md` so Jekyll picks them up.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` isolates dependencies.
- `pip install -r requirements.txt` installs the Anthropics, Foundry, and slugify helpers.
- `python scripts/generate_post_claude.py` generates a post using Anthropic; export `ANTHROPIC_API_KEY` (plus `TOPIC_HINT`, etc.) first.
- `python scripts/generate_post_websearch.py` generates a post using Azure Foundry; set `FOUNDARY_API_KEY`, `ENDPOINT_URL`, and optional `TOPIC_HINT` first.
- `bundle exec jekyll serve --livereload` previews the site locally after installing the `github-pages` gem.

## Coding Style & Naming Conventions
Follow PEP 8: four-space indentation, snake_case functions, and UPPER_SNAKE_CASE env keys. Keep helpers pure and return text, as `parse_foundry_response_dict` does. Generated front matter should mimic `tests/posts/test-post.md`, using lowercase tags and minimal quoting. CSS stays in one file—use descriptive classes such as `.post-summary` and cluster overrides by feature.

## Testing Guidelines
There is no automated CI, so smoke-test locally. When tweaking Foundry parsing, capture responses and load them with `from scripts.tests_helper import parse_foundry_response_file`. After generating a post, review it via the local Jekyll preview and confirm external links resolve. Store regression samples in `tests/posts/` to document expected structure.

## Commit & Pull Request Guidelines
Commit messages stay short and imperative (`clean up`, `testing multi llm via azure`), with optional scopes for post runs (`chore(posts): ...`). Keep commits focused and avoid mixing regenerated posts with script changes. Pull requests should summarize publishing impact, link related issues, attach preview screenshots for UI tweaks, and call out new env vars or secrets.

## Security & Configuration Tips
Store `FOUNDARY_API_KEY` and `ANTHROPIC_API_KEY` as GitHub secrets; never commit `.env` artifacts. Export env vars per shell session when testing locally. Review `_config.yml` before enabling plugins to stay within the GitHub Pages allowlist.
