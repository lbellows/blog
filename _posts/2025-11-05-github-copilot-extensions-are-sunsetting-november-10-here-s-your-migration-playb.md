---
author: the.serf
date: 2025-11-05 06:28:56 -0500
layout: post
tags:
- mcp
- here
- why
- copilot
- extensions
- claude-haiku-4-5-20251001
title: GitHub Copilot Extensions Are Sunsetting November 10—Here's Your Migration
  Playbook
---

# GitHub Copilot Extensions Are Sunsetting November 10—Here's Your Migration Playbook

**TL;DR**
GitHub is deprecating GitHub App-based Copilot Extensions on November 10, 2025
, giving you one week to migrate. The good news:
MCP (Model Context Protocol) provides an open standard for AI agent integration—build once and use across any compatible agent or chatbot, not just GitHub Copilot
. This is actually a *win* for portability, but you need to act now.

---

## What's Changing (and Why It Matters)

If you've built or rely on GitHub Copilot Extensions as GitHub Apps, your integration stops working in **seven days**.
Your extension will stop working November 10, 2025 by 11:59 PM PST
.

The silver lining? GitHub isn't killing extensibility—it's standardizing on
MCP, which provides an open standard that's modular and easy to integrate into a variety of AI assistants and agents
. This means your investment in building an MCP server won't be locked to GitHub alone.

### Why This Shift Matters for .NET & Azure Developers
Build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app
. If you're shipping on .NET and Azure, this opens doors:

- **Unified tooling**: One MCP server can power Copilot, Claude, and future AI agents without rebuilding.
- **Enterprise flexibility**:
GitHub admins can now manage access to Copilot agent mode for IDE via the Copilot policies page, allowing for enabling and disabling access to Copilot agent mode in the IDE for enterprises and organizations
.
- **Future-proofing**: As the agentic web expands, MCP becomes the lingua franca.

---

## The Migration Path: Three Steps

### 1. **Audit Your Extensions (This Week)**
If you have a hybrid app: Disable the Copilot Extension configuration in your GitHub App settings before November 10 by 11:59 PM PST to keep your app in the Marketplace
.

Check the GitHub Marketplace and your internal tools for any Copilot Extensions you've deployed.

### 2. **Build Your MCP Server**
MCP servers are architecturally different from Copilot Extensions, so this is a replacement rather than a migration. MCP servers offer: Individual tool-calling with "#" symbol in IDEs instead of @mentions, Autonomous tool invocation by Agent Mode and Copilot Coding Agent, Build once and use across any MCP-compatible host app (not just GitHub Copilot)
.

**Quick example (pseudocode):**

```python
# MCP Server - works with GitHub Copilot, Claude, and beyond
from mcp.server import Server

server = Server("my-azure-tools")

@server.tool()
def deploy_to_azure(resource_group: str, app_name: str):
    """Deploy a .NET app to Azure App Service"""
    # Your deployment logic here
    return f"Deployed {app_name} to {resource_group}"

@server.tool()
def query_cosmos_db(query: str):
    """Query Cosmos DB for your app"""
    # Your query logic here
    return results

server.run()
```

### 3. **Register with the MCP Registry**
Visit the GitHub MCP Registry to explore existing servers, or check out Anthropic's MCP documentation to start building your own
.

---

## The Broader Picture: Why MCP Wins
Azure MCP Server is now generally available, giving your agents the power of cloud and redefining how developers interact with Azure. Built on Model Context Protocol (MCP), it can create a secure, standards-based bridge between Azure services—like AKS, ACA, App Service, Cosmos DB
.

This is part of a larger shift:
AI is now the default expectation in software development, and agentic workflows are becoming the new standard
. MCP isn't just a GitHub thing—it's becoming the plumbing for the entire agentic ecosystem.

---

## Action Items (Do This Now)

- [ ] Inventory your Copilot Extensions by November 3
- [ ] Read the [MCP server developer documentation](https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/)
- [ ] Start building your first MCP server this week
- [ ] Test with GitHub Copilot and Claude to verify cross-compatibility
- [ ] Deploy to the MCP Registry before November 10

---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/reference
- https://azure.microsoft.com/en-us/blog/github-universe-2025-where-developer-innovation-took-center-stage/
- https://github.blog/changelog/2025-11-03-github-copilot-policy-now-supports-agent-mode-in-the-ide/
- https://github.blog/changelog/2025-10-28-new-public-preview-features-in-copilot-code-review-ai-reviews-that-see-the-full-picture/