---
author: the.serf
date: 2025-10-23 21:21:03 -0400
layout: post
tags:
- .net
- mcp
- github
- copilot
- option
- claude-haiku-4-5-20251001
title: 'GitHub Deprecates Copilot Extensions for MCP Servers: What .NET Developers
  Need to Know'
---

# GitHub Deprecates Copilot Extensions for MCP Servers: What .NET Developers Need to Know

**TL;DR**
GitHub is deprecating GitHub App-based Copilot Extensions on November 10, 2025, in favor of Model Context Protocol (MCP) servers.
MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot.
If you've built or depend on Copilot Extensions, you have until mid-November to migrate. Here's why this matters and what to do.

---

## The Shift: From GitHub-Only to Universal Standards

For the past few years, developers integrating custom tools into GitHub Copilot had one path: build a GitHub App-based Copilot Extension. It worked, but it was a dead end.
GitHub Copilot Extensions only work within GitHub Copilot chat. If developers want their tools to work with other AI assistants, they have to build separate integrations for each one.
Enter Model Context Protocol (MCP).
MCP provides an open standard that's modular and easy to integrate into a variety of AI assistants and agents. Build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app.
This is not a cosmetic change—it's a strategic realignment toward interoperability.
GitHub isn't forcing this because it's trendy; developers shouldn't have to rebuild the same functionality for every platform.
---

## Timeline & What Breaks

- **September 24, 2025**: New Copilot Extension creation was blocked.
- **November 3–7, 2025**: Brownout testing period (temporary service interruptions).
-
November 10, 2025 by 11:59 PM PST: All Copilot Extensions will stop working.
Private and internal Copilot Extensions follow the same sunset timeline and will be disabled on November 10, 2025.
---

## Migration Path for .NET Developers

If you've built a Copilot Extension, you have two options:

### Option 1: Migrate to MCP
MCP servers offer individual tool-calling with the "#" symbol in IDEs instead of @mentions, autonomous tool invocation by Agent Mode and Copilot Coding Agent, and the ability to build once and use across any MCP-compatible host app.
**Getting Started:**

```bash
# Install the MCP SDK for .NET
dotnet add package ModelContextProtocol --prerelease
```
The latest release introduces several new features for .NET developers working on AI applications, including an updated authentication protocol, elicitation support, structured tool output, and resource links in tool responses.
Here's a minimal example of a .NET MCP server that exposes a tool:

```csharp
using ModelContextProtocol.SDK.Server;

var server = new McpServer();

// Define a simple tool
server.AddTool(
    name: "get_user",
    description: "Fetch user info by ID",
    inputSchema: new { 
        type = "object",
        properties = new { 
            userId = new { type = "string" }
        }
    },
    handler: async (args) => {
        var userId = args["userId"];
        // Your logic here
        return new { name = "Alice", id = userId };
    }
);

await server.RunAsync();
```
Start building with MCP today: Visit the GitHub MCP Registry to explore existing servers, or check out Anthropic's MCP documentation to start building your own.
### Option 2: Keep Your GitHub App, Drop the Copilot Extension
If you have a hybrid app: Disable the Copilot Extension configuration in your GitHub App settings before November 10 by 11:59 PM PST to keep your app in the Marketplace.
---

## Why This Matters for .NET + Azure Shops
Multi-Agent Orchestration debuted for Azure AI Foundry Agent Service, providing connected agents and multi-agent workflows with support for Model Context Protocol (MCP) and more.
Microsoft is betting on MCP as the glue layer for agentic workflows. By migrating now, you're aligning with the broader Azure AI ecosystem.

Additionally,
the Microsoft Agent Framework enables Model Context Protocol (MCP) support, Agent-to-Agent (A2A) communication, and OpenAPI-based integration, ensuring portability across different runtime environments.
Your MCP server can become a first-class citizen in orchestrated multi-agent systems.

---

## The Bigger Picture: Agents Are Here

This deprecation isn't punishment—it's evolution.
Since Copilot lives inside the GitHub stack and has native support for GitHub MCP server, its agentic capabilities act on real repository context. It respects branch protections, works within your review cycles, and integrates directly with your CI/CD and security checks.
Copilot coding agent is an asynchronous, autonomous background agent. Delegate a task to Copilot and it opens a draft pull request, makes changes in the background, and then requests a review from you. Copilot can now search the web to gather extra context and supplement its existing knowledge.
MCP is the protocol that makes this work reliably across vendors. Embrace it.

---

## Action Items

1. **Audit your extensions**: If you've published or are using Copilot Extensions, inventory them now.
2. **Plan your migration**: MCP servers are architecturally different from Extensions.
MCP servers and Copilot Extensions are architecturally different—especially when comparing agent-based extensions.
Budget time for a proper rewrite, not a port.
3. **Test during brownout**: November 3–7 is your dress rehearsal. Deploy your MCP server and test with Copilot.
4. **Go live before November 10**: No extensions will work after 11:59 PM PST that day.

---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://github.blog/changelog/2025-10-23-selected-claude-openai-and-gemini-copilot-models-are-now-deprecated/
- https://www.infoq.com/news/2025/10/microsoft-agent-framework/
- https://learn.microsoft.com/en-us/azure/ai-foundry/whats-new-azure-ai-foundry
- https://github.blog/ai-and-ml/github-copilot/copilot-faster-smarter-and-built-for-how-you-work-now/
- https://venturebeat.com/ai/the-teacher-is-the-new-engineer-inside-the-rise-of-ai-enablement-and/
- https://devblogs.microsoft.com/azure-sdk/azure-developer-cli-azd-october-2025/