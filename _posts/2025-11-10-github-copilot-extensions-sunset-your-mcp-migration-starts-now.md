---
author: the.serf
date: 2025-11-10 06:28:07 -0500
layout: post
tags:
- mcp
- github
- extensions
- now
- sunset
- claude-haiku-4-5-20251001
title: 'GitHub Copilot Extensions Sunset: Your MCP Migration Starts Now'
---

# GitHub Copilot Extensions Sunset: Your MCP Migration Starts Now

**TL;DR**
GitHub is deprecating Copilot Extensions (built as GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers
. If you've built extensions, they stop working today.
MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot
. This is a hard deadline with real consequences—here's what you need to do.

---

## The Sunset Is Today (Literally)
Your extension will stop working November 10, 2025 by 11:59 PM PST
. If you have a Copilot Extension deployed right now, it's a zombie in a few hours.
GitHub Copilot Extensions only work within GitHub Copilot chat. If developers want their tools to work with other AI assistants, they have to build separate integrations for each one
—which is why GitHub is pulling the plug.

The good news?
MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot
.
Build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app
.

---

## Why MCP Wins (And Why GitHub Chose It)
MCP addresses this by providing an open standard that's modular and easy to integrate into a variety of AI assistants and agents. We're focusing on MCP because developers shouldn't have to rebuild the same functionality for every platform
.

This isn't just a GitHub move.
Open Standards & Interoperability enables Model Context Protocol (MCP) support, Agent-to-Agent (A2A) communication, and OpenAPI-based integration, ensuring portability across different runtime environments
—this is baked into Microsoft's own Agent Framework for .NET.

---

## What Developers Need to Do Right Now

### 1. **Audit Your Extensions**

If you have a Copilot Extension deployed:

-
Plan your replacement strategy. Your extension will stop working November 10, 2025 by 11:59 PM PST
.
-
If you have a hybrid app: Disable the Copilot Extension configuration in your GitHub App settings before November 10 by 11:59 PM PST to keep your app in the Marketplace
.

### 2. **Build an MCP Server**
MCP servers offer: Individual tool-calling with "#" symbol in IDEs instead of @mentions, Autonomous tool invocation by Agent Mode and Copilot Coding Agent, Build once and use across any MCP-compatible host app (not just GitHub Copilot)
.

Start here:

```bash
# Visit the GitHub MCP Registry to explore existing servers
https://github.com/modelcontextprotocol/servers

# Or check Anthropic's documentation to build your own
https://modelcontextprotocol.io/
```

### 3. **Leverage Discovery & Admin Controls**
The GitHub MCP Registry is live now, providing a curated directory of MCP servers. Users can also discover MCP servers by browsing repositories on GitHub, as most are open source projects
.

For enterprise teams:
MCP servers support organization-level Enable/Disable/Allowlist policies. Per-server allowlist functionality is rolling out to IDEs starting October 28, 2025
.

---

## The Broader Ecosystem Shift

This move aligns with a bigger trend.
Microsoft Agent Framework is available immediately in preview form through Microsoft's GitHub repository and package managers for both Python and .NET ecosystems
.
Open Standards & Interoperability enables Model Context Protocol (MCP) support
, meaning MCP is becoming the lingua franca for AI agents across platforms.

For .NET engineers specifically,
the integration includes native support for Azure AI Foundry services, OpenTelemetry instrumentation for monitoring, and compatibility with existing Microsoft development tools including Visual Studio Code through the AI Toolkit extension
.

---

## What "Architecturally Different" Really Means

⚠️ **Important caveat:**
MCP servers are architecturally different from Copilot Extensions, so this is a replacement rather than a migration. MCP servers can replicate much of the functionality as Copilot Extensions, but MCP servers and Copilot Extensions are architecturally different—especially when comparing agent-based extensions
.

Translation: You can't just swap your extension code into MCP. You'll need to refactor tool invocation patterns and how context flows. But the effort pays off—your MCP server works everywhere.

---

## The Meme-Worthy Moment

![A robot holding a "DEPRECATED" sign, looking sad, with the caption "Me, my Copilot Extension, and the November 10 deadline"](assets/images/robot.webp)

*Your extension's final hours, colorized.*

---

## Action Items (This Week)

1. **Audit:** Check if you have live Copilot Extensions.
2. **Plan:** Review the MCP Registry and Anthropic's docs.
3. **Migrate:** Start building or converting to MCP servers.
4. **Test:** Use the GitHub MCP Registry to publish and validate.
5. **Deploy:** Update your GitHub App marketplace listing if you have a hybrid app.
Start building with MCP today: Visit the GitHub MCP Registry to explore existing servers, or check out Anthropic's MCP documentation to start building your own
.

---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://github.blog/ai-and-ml/github-copilot/a-developers-guide-to-writing-debugging-reviewing-and-shipping-code-faster-with-github-copilot/
- https://github.blog/changelog/2025-11-05-copilot-coding-agent-now-supports-pull-request-templates/
- https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- https://www.infoq.com/news/2025/11/github-copilot-agenthq/
- https://www.infoq.com/news/2025/10/microsoft-agent-framework/
- https://modelcontextprotocol.io/
- https://github.com/modelcontextprotocol/servers