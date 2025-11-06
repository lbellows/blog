---
author: the.serf
date: 2025-11-06 06:28:49 -0500
layout: post
tags:
- mcp
- .net
- actually
- extensions
- github
- claude-haiku-4-5-20251001
title: GitHub Copilot Extensions Are Sunset on November 10—Here's Your MCP Migration
  Roadmap
---

# GitHub Copilot Extensions Are Sunset on November 10—Here's Your MCP Migration Roadmap

**TL;DR:**
GitHub is deprecating GitHub Copilot Extensions (built as GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers.
If you've built or rely on Copilot Extensions, you need to migrate now.
MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot.
For .NET and Azure teams, this is a strategic win: you can now build once and deploy across multiple AI assistants.

---

## Why This Matters (And Why It's Actually Good News)
GitHub Copilot Extensions only work within GitHub Copilot chat. If developers want their tools to work with other AI assistants, they have to build separate integrations for each one.
That's friction. MCP eliminates it.

Think of Copilot Extensions as a walled garden. MCP is the open highway.
MCP addresses this by providing an open standard that's modular and easy to integrate into a variety of AI assistants and agents. Build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app.
For enterprises standardizing on .NET and Azure, this is strategic: you're no longer locked into a single AI vendor's ecosystem. Your custom tools—whether they're internal APIs, data connectors, or business logic—can now power agents across multiple platforms.

---

## What's Actually Changing

| Aspect | Old (Copilot Extensions) | New (MCP Servers) |
|--------|--------------------------|-------------------|
| **Invocation** | `@mentions` in chat | `#` symbol or autonomous tool calling |
| **Scope** | GitHub Copilot only | Any MCP-compatible host (Copilot, Claude, etc.) |
| **Agent Support** | Limited | Full autonomous agent mode support |
| **Discoverability** | Marketplace category | GitHub MCP Registry + open repos |

---

## The Migration Checklist (For .NET Developers)

If you've built a Copilot Extension, here's your action plan:

### 1. **Audit Your Current Extensions**
   - Check the GitHub Marketplace for any extensions you own or depend on.
   -
Copilot Extension-only apps will be removed from the Marketplace, while hybrid apps (with other GitHub App features) can remain if they disable their Extension configuration.
### 2. **Understand MCP Server Architecture**
MCP servers are architecturally different from Copilot Extensions, so this is a replacement rather than a migration.
You're not porting code; you're rewriting with a cleaner mental model.

   MCP servers expose **tools** and **resources** that agents can call. In .NET, you'd typically:
   - Build an ASP.NET Core minimal API or a standalone service
   - Expose tool definitions (JSON Schema)
   - Implement handlers for tool invocation

### 3. **Build Your First MCP Server (Quick Start)**

   Here's a minimal .NET example skeleton:

   ```csharp
   // MCP Server in .NET (pseudocode)
   var builder = WebApplication.CreateBuilder(args);
   var app = builder.Build();

   // Define a tool
   var toolDefinition = new
   {
       name = "get_customer_data",
       description = "Fetch customer info by ID",
       inputSchema = new
       {
           type = "object",
           properties = new
           {
               customerId = new { type = "string" }
           }
       }
   };

   // Handle tool calls
   app.MapPost("/tools/call", async (string toolName, object input) =>
   {
       if (toolName == "get_customer_data")
       {
           var customerId = (string)((dynamic)input).customerId;
           // Your business logic here
           return new { success = true, data = "..." };
       }
       return Results.BadRequest("Unknown tool");
   });

   app.Run();
   ```

### 4. **Register with the GitHub MCP Registry**
The GitHub MCP Registry is live now, providing a curated directory of MCP servers. Users can also discover MCP servers by browsing repositories on GitHub, as most are open source projects.
### 5. **Test with Multiple Hosts**
   One of MCP's superpowers: test your server with Claude, GitHub Copilot, and other MCP clients. This validates portability.

---

## Azure + .NET Integration Points
Multi-Agent Orchestration debuted for Azure AI Foundry Agent Service, providing connected agents and multi-agent workflows with support for Model Context Protocol (MCP) and more.
This means your MCP servers can now be orchestrated at scale in Azure.

For .NET developers,
Microsoft Agent Framework is available immediately in preview form through Microsoft's GitHub repository and package managers for both Python and .NET ecosystems.
This framework has native MCP support, so you can build agents in .NET that consume your MCP servers.

**Practical example:** Build an MCP server that wraps your legacy .NET business logic → Deploy to Azure → Orchestrate with Microsoft Agent Framework → Expose via GitHub Copilot, Claude, and custom agents.

---

## Key Dates & Actions

- **November 10, 2025, 11:59 PM PST:** All Copilot Extension functionality disabled.
All Copilot Extension functionality will be completely disabled.
- **Now:** Start building MCP servers if you haven't already.
- **Admin Note:**
MCP servers support organization-level Enable/Disable/Allowlist policies. Per-server allowlist functionality is rolling out to IDEs starting October 28, 2025.
---

## The Bigger Picture

This isn't just a technical migration—it's a philosophical shift.
Extensions helped us explore what was possible, but as the landscape evolved, it became clear that an open standard like MCP unlocks more opportunity for the entire ecosystem.
For .NET teams shipping on Azure and GitHub, that means:
- **Vendor flexibility:** Your tools work across multiple AI platforms.
- **Cost optimization:** Build once, deploy everywhere (no reinvention).
- **Enterprise governance:**
MCP servers support organization-level Enable/Disable/Allowlist policies.
---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://learn.microsoft.com/en-us/azure/ai-foundry/whats-new-azure-ai-foundry
- https://www.infoq.com/news/2025/10/microsoft-agent-framework/
- https://devblogs.microsoft.com/dotnet/catching-up-on-microsoft-build-2025-essential-sessions-for-dotnet-developers/
- https://github.blog/ai-and-ml/github-copilot/copilot-faster-smarter-and-built-for-how-you-work-now/

---

**Bottom line:** If you're shipping .NET on Azure and using GitHub, the MCP migration is not optional—it's your path forward. The good news? You get a cleaner architecture, better interoperability, and a future-proof standard. Start today.