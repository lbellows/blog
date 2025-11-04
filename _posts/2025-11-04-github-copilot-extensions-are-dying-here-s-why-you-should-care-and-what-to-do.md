---
author: the.serf
date: 2025-11-04 06:29:12 -0500
layout: post
tags:
- extensions
- github
- why
- .net
- action
- claude-haiku-4-5-20251001
title: GitHub Copilot Extensions Are Dying—Here's Why You Should Care (and What to
  Do)
---

# GitHub Copilot Extensions Are Dying—Here's Why You Should Care (and What to Do)

**TL;DR**
GitHub is deprecating Copilot Extensions (built as GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers.
If you've built or rely on Copilot Extensions, you need to migrate now.
MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot.
For .NET developers, this means rewriting your integrations—but with a huge upside: portability.

---

## Why GitHub Is Killing Extensions (And It's Actually Smart)
GitHub Copilot Extensions only work within GitHub Copilot chat, and if developers want their tools to work with other AI assistants, they have to build separate integrations for each one.
That fragmentation was always going to break at scale. Now that AI agents are becoming the default development experience, GitHub realized: why lock developers into a proprietary format?

Enter Model Context Protocol.
MCP addresses this by providing an open standard that's modular and easy to integrate into a variety of AI assistants and agents—build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app. Developers shouldn't have to rebuild the same functionality for every platform.
This is a rare case of a platform vendor choosing openness over lock-in. Respect the play.

---

## The Migration Path for .NET Developers
Your extension will stop working November 10, 2025 by 11:59 PM PST.
Here's what you need to do:

### Step 1: Assess Your Extension

Ask yourself:
- Does it call external APIs or databases?
- Does it perform tool-like actions (search, fetch, transform)?
- Does it need to work with other AI agents beyond Copilot?

If you answered yes to any of these, MCP is your friend.

### Step 2: Build an MCP Server
MCP servers offer individual tool-calling with "#" symbol in IDEs instead of @mentions and autonomous tool invocation by Agent Mode and Copilot Coding Agent.
Here's a minimal .NET example using the MCP SDK:

```csharp
// MCP Server in C# (pseudo-code)
using McpDotnet;

var server = new McpServer();

server.AddTool("search_docs", "Search internal documentation", async (query) =>
{
    var results = await DocumentSearch.ExecuteAsync(query);
    return new ToolResult { Content = results };
});

await server.RunAsync();
```

Then register it in the GitHub MCP Registry or allow your organization to discover it via allowlist.

### Step 3: Update Admin Policies
MCP servers support organization-level Enable/Disable/Allowlist policies, with per-server allowlist functionality rolling out to IDEs starting October 28, 2025.
Your GitHub Enterprise admins can now control which MCP servers are available—much cleaner governance than the old Extension model.

---

## The Real Win: Portability

Here's the kicker: once you build an MCP server, it's not locked to GitHub.
Microsoft is delivering broad first-party support for Model Context Protocol (MCP) across its agent platform and frameworks, spanning GitHub, Copilot Studio, Dynamics 365, Azure AI Foundry, Semantic Kernel and Windows 11.
That means your .NET MCP server can:
- Power Copilot in VS Code
- Integrate with Azure AI Foundry agents
- Work with Claude Code
- Theoretically run anywhere MCP is supported

You're no longer betting on a single platform.

---

## Timeline & Action Items

| Date | What Happens |
|------|---|
| **Nov 3–7, 2025** | Brownout testing period (temporary service interruptions) |
| **Nov 10, 2025** | Full sunset—all Copilot Extensions disabled |

**Action items:**
1. Audit your Extensions *today*.
2.
Visit the GitHub MCP Registry to explore existing servers, or check out Anthropic's MCP documentation to start building your own.
3. Test your MCP server in a staging environment.
4. Deploy and register before November 10.

---

## A Gentle Reminder: This Is Progress

It's easy to grumble about breaking changes. But this one actually makes sense.
AI is now the default expectation in software development, and agentic workflows are becoming the new standard.
Forcing every integration to be Copilot-specific would've been the real mistake. MCP lets you build once and deploy everywhere—that's the future.

Your .NET skills are still gold. You're just building for a bigger ecosystem now.

---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://github.blog/changelog/2025-11-03-github-copilot-policy-now-supports-agent-mode-in-the-ide/
- https://blogs.microsoft.com/blog/2025/05/19/microsoft-build-2025-the-age-of-ai-agents-and-building-the-open-agentic-web/
- https://learn.microsoft.com/en-us/azure/ai-foundry/whats-new-azure-ai-foundry
- https://azure.microsoft.com/en-us/blog/all-the-azure-news-you-dont-want-to-miss-from-microsoft-build-2025/
- https://github.blog/news-insights/company-news/welcome-home-agents/