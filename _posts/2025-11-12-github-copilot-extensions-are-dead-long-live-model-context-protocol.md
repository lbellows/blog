---
author: the.serf
date: 2025-11-12 06:28:52 -0500
layout: post
tags:
- github
- why
- agenthq
- bigger
- context
- claude-haiku-4-5-20251001
title: GitHub Copilot Extensions Are Dead; Long Live Model Context Protocol
---

# GitHub Copilot Extensions Are Dead; Long Live Model Context Protocol

**TL;DR:**
GitHub deprecated Copilot Extensions (built as GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers.
If you built a Copilot Extension, it stops working today. The good news:
MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot.
Time to migrate.

---

## What Happened (And Why It Matters)

For the past few years, developers could extend GitHub Copilot with custom integrations using GitHub Apps. That era just ended.
GitHub is deprecating Copilot Extensions on November 10, 2025, and your extension will stop working by 11:59 PM PST.
This isn't a slow fade—it's a hard cutoff. But there's a silver lining: GitHub is steering everyone toward **Model Context Protocol (MCP)**, an open standard that decouples your tools from any single AI platform.

### Why the Shift?
GitHub Copilot Extensions only work within GitHub Copilot chat, and if developers want their tools to work with other AI assistants, they have to build separate integrations for each one.
That's wasteful.
MCP addresses this by providing an open standard that's modular and easy to integrate into a variety of AI assistants and agents—build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app.
Translation: you're no longer locked into GitHub's ecosystem. Your tool becomes portable.

---

## What You Need to Do (If You Have an Extension)
Plan your replacement strategy—your extension will stop working November 10, 2025 by 11:59 PM PST.
If you've already built a Copilot Extension:

1. **Audit your extension.** What does it do? Does it call external APIs? Does it need authentication?
2. **Build an MCP server.**
Read the MCP server developer documentation to learn more about building an MCP server. Note that MCP servers are architecturally different from Copilot Extensions, so this is a replacement rather than a migration.
3. **Test with GitHub Copilot and beyond.** Once your MCP server is live,
the GitHub MCP Registry is live now, providing a curated directory of MCP servers. Users can also discover MCP servers by browsing repositories on GitHub, as most are open source projects.
### Quick MCP Server Skeleton (Node.js)

Here's a minimal MCP server that exposes a tool:

```javascript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-tool-server",
  version: "1.0.0",
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "fetch_data") {
    // Your logic here
    return {
      content: [{ type: "text", text: "Result from your tool" }],
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

const transport = new StdioServerTransport();
await server.connect(transport);
```
Visit the GitHub MCP Registry to explore existing servers, or check out Anthropic's MCP documentation to start building your own.
---

## The Bigger Picture: GitHub Embraces Open Standards

This move aligns with a broader Microsoft push.
Accelerate Developer Productivity with Microsoft Azure is renamed to Agentic DevOps with Microsoft Azure and GitHub.
The company is betting on **agents** and **open protocols** rather than proprietary lock-in.
Microsoft is delivering broad first-party support for Model Context Protocol (MCP) across its agent platform and frameworks, spanning GitHub, Copilot Studio, Dynamics 365, Azure AI Foundry, Semantic Kernel and Windows 11. In addition, Microsoft and GitHub have joined the MCP Steering Committee to help advance secure, at-scale adoption of the open protocol.
Translation: if you build for MCP today, your tool will work across Microsoft's entire stack *and* with third-party AI assistants. That's a much safer bet than betting on a single vendor.

---

## What About Enterprise Controls?

Good news for teams:
MCP servers support organization-level Enable/Disable/Allowlist policies. Per-server allowlist functionality is rolling out to IDEs starting October 28, 2025.
Your security team can still govern which servers your developers use.

---

## One More Thing: GitHub's New AgentHQ

While you're migrating, note that GitHub just announced something bigger:
GitHub announced during its annual GitHub Universe 2025 event a new addition to its platform called AgentHQ, designed to let developers create and deploy AI agents that work directly within GitHub's development environment. The feature expands the company's ongoing efforts to integrate AI into the software development lifecycle.
MCP is the plumbing. AgentHQ is the next-generation application layer. Get your MCP servers ready now, and you'll be positioned to take advantage of what's coming.

---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://learn.microsoft.com/en-us/azure/ai-foundry/whats-new-azure-ai-foundry
- https://github.blog/ai-and-ml/github-copilot/a-developers-guide-to-writing-debugging-reviewing-and-shipping-code-faster-with-github-copilot/
- https://www.infoq.com/news/2025/11/github-copilot-agenthq/
- https://blogs.microsoft.com/blog/2025/05/19/microsoft-build-2025-the-age-of-ai-agents-and-building-the-open-agentic-web/

---

**Word count: ~650 | Tone: Professional, direct, and practical for .NET/GitHub developers.**