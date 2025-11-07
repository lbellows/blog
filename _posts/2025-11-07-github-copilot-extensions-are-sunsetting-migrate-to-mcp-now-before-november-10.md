---
author: the.serf
date: 2025-11-07 06:28:04 -0500
layout: post
tags:
- mcp
- copilot
- extensions
- github
- migrate
- claude-haiku-4-5-20251001
title: 'GitHub Copilot Extensions Are Sunsetting: Migrate to MCP Now Before November
  10'
---

# GitHub Copilot Extensions Are Sunsetting: Migrate to MCP Now Before November 10

**TL;DR**
GitHub is deprecating Copilot Extensions (GitHub Apps) on November 10, 2025
, giving you one week to migrate.
MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot
. If you've built Copilot Extensions, you need to act now.

---

## What's Changing (and Why It Matters)
GitHub Copilot Extensions only work within GitHub Copilot chat. If developers want their tools to work with other AI assistants, they have to build separate integrations for each one.
That's the pain point GitHub is solving.
MCP addresses this by providing an open standard that's modular and easy to integrate into a variety of AI assistants and agents. Build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app.
### The Timeline (Act Fast)

- **September 24, 2025**:
Creation of new server-side Copilot Extensions blocked
- **November 3–7, 2025**:
Brownout testing period (temporary service interruptions)
- **November 10, 2025**:
Your extension will stop working November 10, 2025 by 11:59 PM PST
---

## How to Migrate: The Practical Path

### Step 1: Assess Your Current Extensions
MCP servers offer individual tool-calling with "#" symbol in IDEs instead of @mentions and autonomous tool invocation by Agent Mode and Copilot Coding Agent
. If your extension relies on @mentions or chat-only interactions, you'll need to rethink the architecture.

### Step 2: Build Your MCP Server
Read the MCP server developer documentation to learn more about building an MCP server.
The GitHub MCP Registry is live now, providing a curated directory of MCP servers. Users can also discover MCP servers by browsing repositories on GitHub, as most are open source projects.
**For .NET developers**, here's a minimal example to get started:

```csharp
// MCP Server skeleton for .NET (using standard HTTP or stdio transport)
using System;
using System.Text.Json;

class MCPServer
{
    static void Main()
    {
        // Listen for MCP protocol messages on stdin
        // Respond with tool definitions and results
        Console.WriteLine(JsonSerializer.Serialize(new {
            jsonrpc = "2.0",
            id = 1,
            method = "initialize",
            result = new {
                protocolVersion = "2024-11-05",
                capabilities = new { tools = new { } }
            }
        }));
    }
}
```

### Step 3: Leverage GitHub Actions for Compute
Work independently in its own ephemeral development environment, powered by GitHub Actions. Within this environment, Copilot can explore your code, make changes, run automated tests and linters, and more.
This is critical for .NET workloads—you can spin up a full build environment without managing servers.

### Step 4: Handle Governance
MCP servers support organization-level Enable/Disable/Allowlist policies. Per-server allowlist functionality is rolling out to IDEs starting October 28, 2025.
Admins can now enforce which MCP servers are allowed, a major win for enterprise .NET shops.

---

## Why MCP Is Better for You

| Feature | Copilot Extensions | MCP Servers |
|---------|-------------------|------------|
| **Scope** | GitHub Copilot only | Any MCP-compatible host |
| **Tool Invocation** | @mentions in chat | `#` symbol or autonomous |
| **Reusability** | Single platform | Cross-platform |
| **Governance** | Basic | Organization allowlists |

---

## What About Hybrid Apps?
If you have a hybrid app: Disable the Copilot Extension configuration in your GitHub App settings before November 10 by 11:59 PM PST to keep your app in the Marketplace.
This is your escape hatch if you're not ready to go full MCP yet—just kill the Extension part and keep the GitHub App alive.

---

## One More Thing: Copilot Spaces

While you're migrating, note that
ahead of the sunset of Copilot knowledge bases on November 1, 2025, GitHub has introduced a new way for you to migrate your legacy knowledge bases into a Copilot Space. Simply press the Convert to Space button under each knowledge base you want to convert into its own space.
Same deadline pressure, different product—keep your context management strategy fresh.

---

![A robot frantically reading a calendar while surrounded by deprecation notices, with sweat droplets flying. The calendar is circled in red on November 10. Alt text: "Me realizing I have one week to migrate from Copilot Extensions to MCP before the lights go out."](assets/images/robot.webp)

---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://github.blog/changelog/2025-11-05-copilot-coding-agent-now-supports-pull-request-templates/
- https://github.blog/changelog/2025-10-17-copilot-knowledge-bases-can-now-be-converted-to-copilot-spaces/
- https://github.blog/changelog/2025-11-03-github-copilot-policy-now-supports-agent-mode-in-the-ide/
- https://github.blog/changelog/2025-11-04-github-copilot-policy-update-for-unconfigured-policies/
- https://github.blog/changelog/2025-10-28-github-copilot-for-linear-available-in-public-preview/