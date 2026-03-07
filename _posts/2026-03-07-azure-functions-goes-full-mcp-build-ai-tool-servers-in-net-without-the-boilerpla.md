---
author: the.serf
date: 2026-03-07 06:33:48 -0500
layout: post
tags:
- mcp
- .net
- azure
- new
- security
- claude-sonnet-4-6
title: 'Azure Functions Goes Full MCP: Build AI-Tool Servers in .NET Without the Boilerplate'
---

# Azure Functions Goes Full MCP: Build AI-Tool Servers in .NET Without the Boilerplate

**Published:** March 7, 2026 | **Audience:** .NET & Azure developers shipping AI-powered applications

---

## TL;DR

Microsoft's Azure Functions MCP extension has reached General Availability, and a brand-new **MCP App** capability (supporting interactive HTML UIs in AI conversations) just shipped in public preview for .NET, Python, and TypeScript. Combined with Aspire 13.1's native MCP support and Visual Studio 2026's built-in Azure MCP Server tooling, the whole Azure/.NET stack now has a coherent, opinionated answer to the question: *"How do I securely expose my backend tools to an AI agent?"* The answer is `McpToolTrigger`. Here's what changed and what it means for your codebase.

---

## What Is MCP, and Why Should You Care?
The Model Context Protocol (MCP) is a client-server protocol intended to enable language models and agents to more efficiently discover and use external data sources and tools.
Think of it as OpenAPI, but for AI agents — a standard contract your agent uses to call your business logic instead of guessing at REST endpoints.
MCP was originally developed by Anthropic
, but it has rapidly become a cross-vendor standard. The .NET and Azure ecosystems have embraced it hard.

---

## What's New: GA Extension + MCP Apps
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability, signaling a shift toward standardized, identity-secure agentic workflows.
That alone was big news. But the freshest drop — published just two weeks ago — takes it further:
Microsoft announced the release of MCP App support in the Azure Functions MCP extension. You can now build MCP Apps using the Functions MCP Extension in Python, TypeScript, and .NET.
So what's an MCP App?
Until now, MCP has primarily been a way for AI agents to "talk" to data and tools — a tool would take an input, perform a task, and return a text response. While powerful, text has limits: it's easier to see a chart than to read a long list of data points, and it's more convenient to provide complex inputs via a form than via a series of text responses. MCP Apps addresses these limits by allowing MCP servers to return interactive HTML interfaces that render directly in the conversation.
In other words: your AI tool can now return a proper interactive dashboard instead of a wall of JSON. Less squinting, more clicking.

---

## The Security Story: OBO Auth Is Now First-Class

One of the long-standing friction points with remote MCP servers was: *"How do I stop the world from calling my tool endpoint?"* That's now handled out of the box.
With built-in OBO authentication and streamable HTTP transport, it addresses key security concerns.
Specifically,
the feature supports on-behalf-of (OBO) authentication, enabling tools to access downstream services using the user's identity rather than a service account.
This is a meaningful enterprise unlock. Your Azure Function MCP tool can now call, say, Microsoft Graph or your own internal APIs on behalf of the signed-in user — no shared service principal secrets floating around, no privilege escalation footguns.
The GA extension also replaces the older Server-Sent Events (SSE) approach with the streamable HTTP transport protocol, with Microsoft recommending the newer transport unless clients specifically require SSE. The extension exposes two endpoints: `/runtime/webhooks/mcp` for streamable-http and `/runtime/webhooks/mcp/sse` for legacy SSE connections.
> **Practical note:** If you're still wiring up SSE clients, plan a migration path. Streamable HTTP is the present and future.

---

## Getting Started: .NET Quickstart

### Prerequisites
When running locally, the MCP extension requires version 4.0.7030 of the Azure Functions Core Tools or later. For .NET, it requires version 2.1.0 or later of `Microsoft.Azure.Functions.Worker` and version 2.0.2 or later of `Microsoft.Azure.Functions.Worker.Sdk`.
Also note:
for C#, the Azure Functions MCP extension supports only the isolated worker model.
### Scaffold a new remote MCP server

```bash
# Init a C# MCP server project using the Azure Developer CLI
azd init --template remote-mcp-functions-dotnet -e my-mcp-server
```
After running the project locally and verifying your code using GitHub Copilot, you deploy it to a new serverless function app in Azure Functions. Because the new app runs on the Flex Consumption plan, which follows a pay-for-what-you-use billing model, completing this quickstart incurs a small cost of a few USD cents or less in your Azure account.
*(Yes, "a few cents or less." Serverless billing for AI tools is genuinely inexpensive to prototype.)*

### Define a tool trigger in C\#

```csharp
[Function(nameof(GetOrderStatus))]
[McpToolTrigger("GetOrderStatus",
    Description = "Returns the status of a customer order by order ID.")]
public async Task<McpToolResponse> GetOrderStatus(
    [McpToolTriggerContext] McpToolContext context)
{
    var orderId = context.Arguments["orderId"]?.ToString();
    var status = await _orderService.GetStatusAsync(orderId);
    return new McpToolResponse(status);
}
```
Adding tooling to LLM-based applications was possible before MCP, but the Model Context Protocol has made it much simpler and opened the world up to a greater variety of tooling. Azure Functions is one of those, and all it takes is creating a function that's a `McpToolTrigger` and away you go.
### Wire it to Microsoft Foundry Agent Service
You can create a remote MCP server using Azure Functions, register it in a private organizational tool catalog using Azure API Center, and connect it to Foundry Agent Service. This approach enables you to securely integrate internal APIs and services into the Microsoft Foundry ecosystem, allowing agents to call your enterprise-specific tools through a standardized MCP interface.
In the Foundry portal: **Tools → Add → Custom → Model Context Protocol (MCP)**, paste in your Functions endpoint, and you're live.

---

## The Broader Picture: MCP Everywhere in .NET

The Functions GA isn't an isolated update — it's the capstone of a broader MCP-first wave across the Microsoft stack:

- **Visual Studio 2026:**
Azure MCP Server tools are now generally available out-of-the-box in Visual Studio 2026, bringing agentic cloud automation directly into your trusted IDE and empowering developers to build intelligent, secure applications faster.
You can even ask Copilot to generate your `az` CLI commands in natural language.
Automated CI/CD setup can generate Azure DevOps or GitHub Actions workflows for ASP.NET, Blazor, or Azure Functions projects — complete with YAML files and securely managed credentials.
- **.NET Aspire 13.1:**
A central addition in Aspire 13.1 is expanded support for AI coding agents through integration with the Model Context Protocol. A new command allows projects to be initialized with MCP support, enabling compatible AI tools to discover Aspire integrations, inspect application structure, and interact with running resources.
When connected, AI agents can query application state, view logs, and inspect traces through exposed endpoints — simplifying the use of AI assistants during development without requiring custom setup for each tool.
- **NuGet MCP Server (Visual Studio 2026):**
Visual Studio 2026 provides a way of updating packages with known vulnerabilities and can retrieve real-time information about packages for GitHub Copilot. The NuGet MCP server is built-in but must be enabled once in order to use its functionality.
---

## Cost & Latency Engineering Notes

| Concern | What to know |
|---|---|
| **Cost** | Flex Consumption plan = pay-per-execution. Agentic workloads with infrequent tool calls are very cheap. High-frequency agents calling tools in tight loops may accumulate cost faster than expected — monitor your invocation counts. |
| **Cold start** | Flex Consumption has cold-start considerations. For latency-sensitive agent pipelines, consider pre-warming or the Premium plan. |
| **Transport** | Prefer Streamable HTTP over SSE for new deployments; SSE requires Azure Queue Storage (`AzureWebJobsStorage`) as a relay. |
| **Auth overhead** | OBO token acquisition adds ~50–150 ms per tool call depending on token cache state. Use MSAL's in-memory token cache in your function. |

---

## Security Checklist Before You Ship
Before sharing your MCP server with others, define and apply a security baseline: require authentication and avoid anonymous access unless your scenario explicitly needs it; treat credentials as secrets and don't hard-code keys or check them into source control; store secrets in Azure Key Vault; and implement least privilege for downstream calls — if your MCP server calls internal APIs, scope permissions to only what the exposed tools need.
---

## Takeaways for .NET + Azure Teams

1. **Adopt the MCP extension over custom REST wrappers** for new agent tools — you get auth, scaling, and Foundry integration for free.
2. **Upgrade to Streamable HTTP transport** now. SSE is legacy.
3. **Explore MCP Apps** if your tools return structured data that benefits from visualization — think reporting dashboards, order explorers, or approval UIs embedded in chat.
4. **Add MCP support to your Aspire apphost** — your AI assistant can then inspect your distributed app's telemetry without you writing a single extra endpoint.
5. **Audit your auth model** — OBO is the right pattern for user-context tool calls. Service-principal-only access is a smell.

---

## Further Reading

- Azure Functions MCP Extension — Official Docs: https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-mcp
- Building MCP Apps with Azure Functions MCP Extension (Tech Community, ~Feb 2026): https://techcommunity.microsoft.com/blog/appsonazureblog/building-mcp-apps-with-azure-functions-mcp-extension/4496536
- Host Remote MCP Servers on Azure Functions (Tech Community, Nov 2025): https://techcommunity.microsoft.com/blog/appsonazureblog/host-remote-mcp-servers-on-azure-functions/4471047
- Azure Functions MCP Support GA — InfoQ (Jan 2026): https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- Aspire 13.1 Brings MCP Integration — InfoQ (Jan 2026): https://www.infoq.com/news/2026/01/dotnet-aspire-13-1-release/
- Azure MCP Server Built-In with Visual Studio 2026 — Visual Studio Blog: https://devblogs.microsoft.com/visualstudio/azure-mcp-server-now-built-in-with-visual-studio-2026-a-new-era-for-agentic-workflows/
- Build and Register an MCP Server — Microsoft Foundry Docs: https://learn.microsoft.com/en-us/azure/foundry/mcp/build-your-own-mcp-server
- Tutorial: Host an MCP Server on Azure Functions — Microsoft Learn: https://learn.microsoft.com/en-us/azure/azure-functions/functions-mcp-tutorial
- Generative AI with LLMs in C# in 2026 — .NET Blog: https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/
- What's New in Microsoft Sentinel: March 2026 (agentic AI security context): https://techcommunity.microsoft.com/blog/microsoftsentinelblog/what%E2%80%99s-new-in-microsoft-sentinel-march-2026/4499508