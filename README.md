# blog
Tech Thoughts

Trying out some github pages features

link: https://lbellows.github.io/blog/

# About AI blog posting

I needed an easy solution for this because I was holding my daughter, so not too much typing could be involed:

* git workflows
* executes python
* calls claude API with search tool enabled
* writes the blog post in MD & commits
* triggers jekyll build which updates the blog

That is my AI-slop-posting pipeline.  Costs about $0.40 per post (sonnet 4.5). This is mostly exploratory and I hope to test out some other tools/solutions in the future integration with social media.

# TODO:
## Secrets to add (one-time)

Repo → Settings → Secrets and variables → Actions:

ANTHROPIC_API_KEY — from your Anthropic account.

## Notes & tips

Models with web search: Claude 3.7 Sonnet and newer (plus several others) support this tool; see the docs for the supported list. 

Pricing: Web search calls are billed in addition to tokens ($10 / 1,000 searches). Keep MAX_SEARCHES low (e.g., 3–6) to control cost. 

Citations: Claude will include citations automatically in its response when using web search. Your post will then carry those links in the “Further reading” section the prompt asks for. 

Domain control: Set ALLOWED_DOMAINS to bias sources you trust (e.g., arxiv.org,blogs.microsoft.com,developer.nvidia.com). BLOCKED_DOMAINS can filter out low-quality sites. 

Schedule & publish time: Adjust cron and the front-matter timestamp to your preference.

Manual test: Use the workflow’s Run workflow button to test once you add the secret.