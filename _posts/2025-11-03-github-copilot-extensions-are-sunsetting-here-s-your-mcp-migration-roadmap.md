---
author: the.serf
date: 2025-11-03 06:27:28 -0500
layout: post
tags:
- mcp
- github
- extensions
- isn
- migration
- claude-haiku-4-5-20251001
title: GitHub Copilot Extensions Are Sunsetting—Here's Your MCP Migration Roadmap
---

# GitHub Copilot Extensions Are Sunsetting—Here's Your MCP Migration Roadmap

**TL;DR**
GitHub is deprecating Copilot Extensions (built as GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers
. If you've built or rely on Copilot Extensions, you have **one week left** to migrate. The good news:
MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot
. This is a win for the ecosystem, but it requires action *now*.

---

## Why GitHub Is Making This Move

The shift from proprietary extensions to an open standard reflects a broader maturation in AI tooling.
GitHub Copilot Extensions only work within GitHub Copilot chat. If developers want their tools to work with other AI assistants, they have to build separate integrations for each one
. That's friction.
MCP addresses this by providing an open standard that's modular and easy to integrate into a variety of AI assistants and agents. Build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app
. Translation: your tool becomes portable across the entire AI ecosystem, not locked into one platform.

---

## What's Changing (and What Isn't)

| Aspect | Copilot Extension | MCP Server |
|--------|-------------------|-----------|
| **Invocation** | `@mention` in chat | `#` symbol in IDEs + autonomous tool calling |
| **Scope** | GitHub Copilot only | Any MCP-compatible host |
| **Agent Support** | Limited | Full autonomous agent mode support |
| **Discovery** | Marketplace category | GitHub MCP Registry + open-source repos |
MCP servers offer individual tool-calling with "#" symbol in IDEs instead of @mentions, autonomous tool invocation by Agent Mode and Copilot Coding Agent, and the ability to build once and use across any MCP-compatible host app (not just GitHub Copilot)
.

---

## Migration Checklist: Do This Before November 10

### 1. **Audit Your Extensions**
If you maintain a Copilot Extension,
plan your replacement strategy. Your extension will stop working November 10, 2025 by 11:59 PM PST
.

### 2. **Build Your MCP Server**
Read the MCP server developer documentation to learn more about building an MCP server. Note that MCP servers are architecturally different from Copilot Extensions, so this is a replacement rather than a migration
.

**Quick start:**
```bash
# Clone the MCP SDK starter template
git clone https://github.com/modelcontextprotocol/server-template.git my-mcp-server
cd my-mcp-server

# Install dependencies
npm install

# Build your tools
npm run build
```

### 3. **Register in the GitHub MCP Registry**
The GitHub MCP Registry is live now, providing a curated directory of MCP servers. Users can also discover MCP servers by browsing repositories on GitHub, as most are open source projects
.

### 4. **Test Governance & Admin Controls**
MCP servers support organization-level Enable/Disable/Allowlist policies. Per-server allowlist functionality is rolling out to IDEs starting October 28, 2025
.

---

## For .NET & Azure Developers: Extra Context

If you're building on the Microsoft stack, there's a natural fit here.
The tooling around LLMs, Microsoft Extensions for AI (now generally available), Semantic Kernel, and AI agents is getting really mature
.
Multi-Agent Orchestration debuted for Azure AI Foundry Agent Service, providing connected agents and multi-agent workflows with support for Model Context Protocol (MCP) and more
.

This means your MCP server can integrate seamlessly with Azure AI Foundry agents. Build once, deploy everywhere.

---

## The Brownout Window: Be Prepared
November 3–7, 2025: Brownout testing period (temporary service interruptions)
. If you're running a production Copilot Extension, expect intermittent failures during this week. Use it as a final test run before the full sunset.

---

## One More Thing: Feature Parity Isn't Guaranteed
MCP servers can replicate much of the functionality as Copilot Extensions, but MCP servers and Copilot Extensions are architecturally different—especially when comparing agent-based extensions
. If your extension relied on specific chat-based patterns, you may need to rethink the UX for MCP's tool-calling model. That's not a blocker—it's an opportunity to make your tool more powerful.

---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://github.com/modelcontextprotocol/specification
- https://learn.microsoft.com/en-us/azure/ai-foundry/whats-new-azure-ai-foundry
- https://github.blog/ai-and-ml/github-copilot/copilot-faster-smarter-and-built-for-how-you-work-now/
- https://devblogs.microsoft.com/dotnet/catching-up-on-microsoft-build-2025-essential-sessions-for-dotnet-developers/

---

*Deadline: November 10, 2025, 11:59 PM PST. No extensions after that. Start building your MCP server today.*