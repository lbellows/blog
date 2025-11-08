---
author: the.serf
date: 2025-11-08 06:25:15 -0500
layout: post
tags:
- mcp
- github
- .net
- advantage
- app
- claude-haiku-4-5-20251001
title: 'GitHub Copilot Extensions Sunset: Your MCP Migration Deadline Is November
  10'
---

# GitHub Copilot Extensions Sunset: Your MCP Migration Deadline Is November 10

**TL;DR:**
GitHub is deprecating Copilot Extensions on November 10, 2025
. If you've built custom extensions, you have days to migrate to
Model Context Protocol (MCP) servers, which provide a universal standard for AI agent integration
. The good news?
MCP servers work with GitHub Copilot, Claude Code, and any other MCP-compatible host app
—so your investment in rebuilding pays dividends across the AI ecosystem.

---

## Why GitHub Is Burning the Bridges
GitHub Copilot Extensions only worked within GitHub Copilot chat, and if developers wanted their tools to work with other AI assistants, they had to build separate integrations for each one
. That's a maintenance nightmare at scale.
MCP addresses this by providing an open standard that's modular and easy to integrate into a variety of AI assistants and agents, because developers shouldn't have to rebuild the same functionality for every platform
.

**Translation:** GitHub is betting on an open standard rather than proprietary lock-in. Smart move.

---

## What You Need to Do (and When)

### Timeline

- **Now (Nov 6–9):** Audit your extensions. If you have any, start planning.
- **Nov 10, 11:59 PM PST:**
Your extension will stop working
.
- **Nov 3–7:**
Brownout testing period (temporary service interruptions)
—expect hiccups.

### If You Have a Hybrid App
If you have a hybrid app, disable the Copilot Extension configuration in your GitHub App settings before November 10 by 11:59 PM PST to keep your app in the Marketplace
.

### If You Have a Standalone Extension

You'll need to rebuild it as an MCP server.
MCP servers are architecturally different from Copilot Extensions, so this is a replacement rather than a migration
.

---

## The MCP Advantage (and What Changed)
MCP servers offer individual tool-calling with "#" symbol in IDEs instead of @mentions, autonomous tool invocation by Agent Mode and Copilot Coding Agent, and the ability to build once and use across any MCP-compatible host app
.

### Practical Differences

| Feature | Copilot Extensions | MCP Servers |
|---------|-------------------|------------|
| **Invocation** | `@mention` in chat | `#` in IDE or autonomous agents |
| **Scope** | GitHub Copilot only | Any MCP-compatible host |
| **Agent Support** | Limited | Full autonomous tool-calling |
| **Discoverability** | GitHub Marketplace | GitHub MCP Registry + open source repos |

---

## Getting Started with MCP

### Step 1: Explore Existing Servers
The GitHub MCP Registry is live now, providing a curated directory of MCP servers, and users can also discover MCP servers by browsing repositories on GitHub, as most are open source projects
.

### Step 2: Build Your MCP Server
Read the MCP server developer documentation to learn more about building an MCP server
.

Here's a minimal .NET example to get you started:

```csharp
// Pseudo-code: MCP server stub in .NET
using Microsoft.Extensions.Hosting;

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices(services =>
    {
        services.AddMcpServer(options =>
        {
            options.AddTool("my-tool", "Description", async (args) =>
            {
                // Your tool logic here
                return new ToolResult { Content = "result" };
            });
        });
    })
    .Build();

await host.RunAsync();
```

(Real implementation varies; check the official MCP docs for language-specific SDKs.)

### Step 3: Deploy & Register

Host your MCP server (Azure Container Instances, GitHub Codespaces, or self-hosted), then register it in the GitHub MCP Registry.

---

## Azure & .NET Ecosystem Integration

Good news:
Microsoft Agent Framework enables Model Context Protocol (MCP) support and Agent-to-Agent (A2A) communication
, and
it's built-in with observability through OpenTelemetry, integration with Azure Monitor, Entra ID security authentication, and CI/CD compatibility using GitHub Actions and Azure DevOps
.
GitHub Copilot for .NET Upgrades capability is a game-changer for modernizing legacy applications
, and it now integrates with MCP for better extensibility.

---

## The Silver Lining

![A robot staring at a "DEPRECATED" sign with the caption "Me, realizing I have 4 days to migrate my Copilot Extension."](assets/images/robot.webp)
MCP servers support organization-level Enable/Disable/Allowlist policies, and per-server allowlist functionality is rolling out to IDEs starting October 28, 2025
. Enterprise governance just got better.

Plus,
the GitHub MCP Registry is live now
, so you're not starting from zero—you can learn from existing implementations.

---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://github.com/modelcontextprotocol
- https://learn.microsoft.com/en-us/dotnet/ai/overview
- https://devblogs.microsoft.com/dotnet/catching-up-on-microsoft-build-2025-essential-sessions-for-dotnet-developers/
- https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- https://www.infoq.com/news/2025/10/microsoft-agent-framework/