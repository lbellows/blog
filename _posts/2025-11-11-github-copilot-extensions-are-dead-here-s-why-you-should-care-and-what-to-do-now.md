---
author: the.serf
date: 2025-11-11 06:28:46 -0500
layout: post
tags:
- mcp
- .net
- github
- server
- why
- claude-haiku-4-5-20251001
title: GitHub Copilot Extensions Are Dead—Here's Why You Should Care (and What to
  Do Now)
---

# GitHub Copilot Extensions Are Dead—Here's Why You Should Care (and What to Do Now)

**TL;DR:**
GitHub deprecated Copilot Extensions (built as GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers.
If you've built custom Copilot integrations, they stopped working today. The good news:
MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot.
Time to migrate.

---

## The Sunset (It's Today)
Your extension will stop working November 10, 2025 by 11:59 PM PST.
If you're reading this on November 11, that ship has sailed. But don't panic—this is actually a *good* thing, even if it feels like a breaking change.

For years, GitHub Copilot Extensions let you bolt custom tools onto Copilot via GitHub Apps. The problem?
GitHub Copilot Extensions only work within GitHub Copilot chat. If developers want their tools to work with other AI assistants, they have to build separate integrations for each one.
That's a maintenance nightmare at scale.

---

## Why MCP Wins
MCP addresses this by providing an open standard that's modular and easy to integrate into a variety of AI assistants and agents. Build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app.
Think of it like this: Copilot Extensions were proprietary adapters. MCP is the USB-C of AI integration—one plug, many devices.

### Key advantages for .NET/Azure shops:

- **Reusability**: Your MCP server works in VS Code, Visual Studio, JetBrains IDEs, and beyond.
- **Future-proof**:
Developers shouldn't have to rebuild the same functionality for every platform.
- **Enterprise-grade controls**:
MCP servers support organization-level Enable/Disable/Allowlist policies. Per-server allowlist functionality is rolling out to IDEs starting October 28, 2025.
---

## Migration Path: From Extension to MCP Server

If you had a Copilot Extension, here's the reality:
MCP servers are architecturally different from Copilot Extensions, so this is a replacement rather than a migration.
You'll need to rebuild, but it's not a rewrite—more like a refactor.

### Quick checklist:

1. **Audit your extension**: What does it do? (e.g., fetch data, run commands, validate code?)
2. **Build an MCP server**:
Visit the GitHub MCP Registry to explore existing servers, or check out Anthropic's MCP documentation to start building your own.
3. **Test in your IDE**: MCP servers integrate directly into VS Code and Visual Studio.
4. **Register in the GitHub MCP Registry**: Make it discoverable for your team or the community.

### Example: A simple .NET MCP server stub

```csharp
// Minimal MCP server for a .NET tool
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// MCP tools endpoint
app.MapPost("/tools", async (HttpContext ctx) =>
{
    var request = await ctx.Request.ReadAsAsync<MCP.Request>();
    
    // Your tool logic here
    var result = new { success = true, data = "Tool executed" };
    await ctx.Response.WriteAsJsonAsync(result);
});

app.Run("http://localhost:3000");
```

---

## What About Feature Parity?
MCP servers offer: Individual tool-calling with "#" symbol in IDEs instead of @mentions, Autonomous tool invocation by Agent Mode and Copilot Coding Agent, Build once and use across any MCP-compatible host app (not just GitHub Copilot)
The trade-off:
MCP servers can replicate much of the functionality as Copilot Extensions, but MCP servers and Copilot Extensions are architecturally different—especially when comparing agent-based extensions.
You might lose some niche features, but you gain portability and longevity.

---

## The Bigger Picture: GitHub's Agentic Bet

This deprecation isn't random—it's part of a larger shift.
GitHub announced during its annual GitHub Universe 2025 event a new addition to its platform called AgentHQ, designed to let developers create and deploy AI agents that work directly within GitHub's development environment. The feature expands the company's ongoing efforts to integrate AI into the software development lifecycle, building on previous Copilot releases.
MCP is the foundation for that agentic future.
Accelerate Developer Productivity with Microsoft Azure is renamed to Agentic DevOps with Microsoft Azure and GitHub.
The naming change alone signals Microsoft's commitment to agent-first tooling.

---

## Action Items This Week

- **If you own a Copilot Extension**: Start building the MCP equivalent.
Visit the GitHub MCP Registry to explore existing servers, or check out Anthropic's MCP documentation to start building your own.
- **If you use Copilot Extensions**: Migrate to the MCP alternatives in the registry, or work with your team to build one.
- **If you're new to this**: No action needed—just use MCP servers going forward.

---

## Further reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://github.blog/ai-and-ml/github-copilot/a-developers-guide-to-writing-debugging-reviewing-and-shipping-code-faster-with-github-copilot/
- https://learn.microsoft.com/en-us/partner-center/announcements/2025-november
- https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- https://www.infoq.com/news/2025/11/github-copilot-agenthq/