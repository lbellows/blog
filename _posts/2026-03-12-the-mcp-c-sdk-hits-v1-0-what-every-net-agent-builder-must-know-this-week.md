---
author: the.serf
date: 2026-03-12 07:44:10 -0400
layout: post
tags:
- mcp
- v1.0
- .net
- server
- a.k.a.
- claude-sonnet-4-6
title: 'The MCP C# SDK Hits v1.0: What Every .NET Agent Builder Must Know This Week'
---

# The MCP C# SDK Hits v1.0: What Every .NET Agent Builder Must Know This Week

**Published:** March 12, 2026 | **Audience:** .NET & Azure engineers building AI-powered applications

---

## TL;DR
Microsoft has released version 1.0 of the official MCP C# SDK, bringing full support for the 2025-11-25 MCP Specification.
If you've been sitting on the fence waiting for a stable, production-worthy surface area before wiring your .NET services into the Model Context Protocol ecosystem — the fence-sitting is officially over. Here's what changed, why it matters, and how to get started today.

---

## What Is MCP and Why Should You Care?
The Model Context Protocol (MCP) is an open protocol created by Anthropic to enable integration between LLM applications and external tools and data sources.
Think of it as the USB-C of AI integrations: a single, standardized plug that lets your agents reach into databases, APIs, filesystems, and services without writing bespoke glue code for every provider.
A number of Microsoft products have already added support for MCP, including Copilot Studio, VS Code's new GitHub Copilot agent mode, and Semantic Kernel.
In other words, MCP is rapidly becoming the connective tissue of the entire Microsoft AI ecosystem — and now it has a stable, v1.0-quality SDK for C#.

---

## What's New in v1.0
The release introduces enhanced authorization flows, icon support for tools and resources, incremental scope consent, URL mode elicitation, tool calling in sampling, and improved handling of long-running HTTP requests.
The two most operationally significant additions are worth unpacking:

### 1. Incremental Scope Consent (a.k.a. "Ask For Less, Get More Trust")
MCP uses OAuth 2.0 for authorization, where scopes define the level of access a client has. Previously, clients might request all possible scopes up front because they couldn't know which scopes a specific operation would require.
The new **incremental scope consent** model fixes this: your MCP client now requests only the minimum scopes needed at call time, which is both better UX for end users and a significantly smaller blast radius if a token is ever mishandled. Security teams rejoice (quietly, professionally).

### 2. Enhanced Authorization Server Discovery
One of the most significant additions is enhanced authorization server discovery. Under the updated specification, servers can now expose Protected Resource Metadata through three different methods, offering more flexibility compared to the single method previously required. The SDK handles the full discovery process on the client side automatically.
Practically, this means you no longer have to hard-code auth endpoints into your MCP client configuration — the SDK discovers them at runtime.

---

## Getting Started: Minimal MCP Server in .NET
The official MCP C# SDK is available through NuGet and enables you to build MCP clients and servers for .NET apps and libraries.
Install the now-stable v1.0 package:

```bash
# Drop the --prerelease flag — v1.0 is GA!
dotnet add package ModelContextProtocol
dotnet add package Microsoft.Extensions.Hosting
```
The `ModelContextProtocol` package gives access to new APIs to create clients that connect to MCP servers, creation of MCP servers, and AI helper libraries to integrate with LLMs through `Microsoft.Extensions.AI`.
A minimal tool looks like this:

```csharp
using System.ComponentModel;
using ModelContextProtocol.Server;

[McpServerToolType]
public static class OrderTools
{
    [McpServerTool, Description("Get an order by ID.")]
    public static async Task<string> GetOrder(
        OrderService svc,
        [Description("The order ID to retrieve.")] string orderId)
    {
        var order = await svc.GetByIdAsync(orderId);
        return JsonSerializer.Serialize(order);
    }
}
```

Wire it up in `Program.cs` with `AddMcpServer()` and point your Copilot Studio agent, VS Code Copilot, or Semantic Kernel pipeline at the resulting stdio or HTTP/SSE endpoint.

> 💡 **Pro tip:**
NuGet.org now supports hosting and consuming MCP servers built with the `ModelContextProtocol` C# SDK — developers can find your MCP servers through NuGet search, with proper semantic versioning and easy copy-paste VS Code and Visual Studio MCP configuration.
Ship your internal tooling as a versioned NuGet package and your whole org can plug it into their agents in seconds.

---

## The Broader Azure Context: Timing Is Everything

This v1.0 drop lands at an interesting moment in the Azure AI lifecycle.

**Assistants API is on the clock.**
The Assistants API is deprecated and will be retired on August 26, 2026. Anyone currently building or running solutions on the Azure OpenAI Assistants API should plan and execute a migration to the Microsoft Foundry Agents service well before August 26, 2026.
If you've been building stateful agents on the old Assistants API, the MCP + Foundry Agents path is your forward-looking destination — start the migration now, not in July.

**The Responses API is your new foundation.**
The Responses API is a new stateful API from Azure OpenAI. It brings together the best capabilities from the chat completions and assistants API in one unified experience.
MCP tools compose beautifully on top of the Responses API's tool-calling surface.

**GPT-5.4 just landed in GitHub Copilot.**
GPT-5.4, OpenAI's latest agentic coding model, is now rolling out in GitHub Copilot. In early testing of real-world, agentic, and software development capabilities, GPT-5.4 consistently hits new rates of success. It also shows enhanced logical reasoning and task execution for intricate, multi-step, tool-dependent processes.
More capable models + stable MCP tooling = the compounding effect your agent architecture has been waiting for.

**Model lifecycle hygiene reminder.**
The Foundry portal (Model Catalog → Retirement date column) and the Microsoft Learn "Azure OpenAI in Foundry – Model Retirements" documentation are the only authoritative sources for retirement timelines. OpenAI blog posts or ChatGPT retirement notices should not be used to determine Azure retirement timelines.
Bookmark that portal; don't let a prod outage be your reminder.

---

## Practical Takeaways

| Area | Action |
|---|---|
| **New projects** | Start with `ModelContextProtocol` v1.0 — no more `--prerelease` flag |
| **Auth** | Implement incremental scope consent; avoid over-permissioned tokens |
| **Discovery** | Let the SDK's auto-discovery handle auth server endpoints at runtime |
| **Legacy agents** | Begin Assistants API → Foundry Agents migration now; deadline is August 26, 2026 |
| **Model versioning** | Check the Foundry portal — not OpenAI blog posts — for retirement dates |
| **NuGet ecosystem** | Publish your MCP servers to NuGet.org for org-wide discoverability |

---

## Further Reading

- **MCP C# SDK v1.0 — Official .NET Blog:** https://devblogs.microsoft.com/dotnet/release-v10-of-the-official-mcp-csharp-sdk/
- **InfoQ: Microsoft Launches MCP C# SDK v1.0:** https://www.infoq.com/news/2026/03/mcp-csharp-v1/
- **Azure OpenAI What's New (Responses API, GPT-5.x models):** https://learn.microsoft.com/en-us/azure/ai-services/openai/whats-new
- **Assistants API deprecation & migration guidance:** https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/assistants?view=foundry-classic
- **Get Started with .NET AI and MCP:** https://learn.microsoft.com/en-us/dotnet/ai/get-started-mcp
- **GitHub Copilot Changelog: GPT-5.4 GA:** https://github.blog/changelog/2026-03-05-gpt-5-4-is-generally-available-in-github-copilot/
- **Building Your First MCP Server with .NET (tutorial):** https://devblogs.microsoft.com/dotnet/build-a-model-context-protocol-mcp-server-in-csharp/
- **Azure Model Retirement Dates (authoritative):** https://learn.microsoft.com/en-us/answers/questions/5775321/are-gpt-4o-mini-and-other-models-retiring-from-azu