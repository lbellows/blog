---
author: the.serf
date: 2026-03-05 06:48:53 -0500
layout: post
tags:
- mcp
- .net
- azure
- functions
- support
- claude-sonnet-4-6
title: Azure Functions MCP Support Is GA — And Your .NET Agent Tools Just Got a Real
  Home
---

# Azure Functions MCP Support Is GA — And Your .NET Agent Tools Just Got a Real Home

**Published:** March 5, 2026

---

## TL;DR

Microsoft's Azure Functions support for the Model Context Protocol (MCP) has reached General Availability, and it's the cleanest on-ramp yet for .NET engineers who want to ship production-grade AI agent tools. You get serverless scale-to-zero economics, built-in Entra auth with on-behalf-of (OBO) identity passthrough, a modern streamable HTTP transport, and a `McpToolTrigger` binding that turns a C# function into a discoverable AI tool in about a dozen lines of code. Meanwhile, the new Maia 200 silicon humming in Azure datacenters means the tokens your agent tools generate are getting cheaper — whether or not you ever touch a GPU directly.

---

## The Story: MCP + Azure Functions, Finally Production-Ready

The Model Context Protocol — originally developed by Anthropic — has become the de-facto standard for letting AI agents discover and call external tools. Think of it as a typed, negotiated handshake between an LLM and your business logic. The idea is sound; the hard part has always been *hosting* those tool servers securely at scale without babysitting a Docker container on someone's laptop.
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability, signaling a shift toward standardized, identity-secure agentic workflows.
That's the headline. Here's why .NET engineers specifically should care.

---

## Why Azure Functions Is a Great MCP Host
Azure Functions is the ideal platform for hosting remote MCP servers because of its built-in authentication, event-driven scaling from 0 to N, and serverless billing — ensuring your agentic tools are secure, cost-effective, and ready to handle any load.
Compare that to the most common alternative today:
right now the most common scenario involves a client running locally, like VS Code or Claude Desktop, that acts as an MCP client using an LLM to call an MCP server also running locally, usually hosted in a Docker container. But it gets old quickly to install the same MCP server locally everywhere you may need it — let alone making sure people on your team have the same version installed.
Remote MCP servers on Azure Functions solve exactly that problem, with a consumption-based cost model to boot.
Because the new app runs on the Flex Consumption plan, which follows a pay-for-what-you-use billing model, completing a quickstart deployment incurs a small cost of a few USD cents or less in your Azure account.
---

## What's New in GA: Transport, Auth, and Language Support

### Transport: Streamable HTTP Is the Default Now
The generally available MCP extension introduces several capabilities designed for production deployments. Support for the streamable HTTP transport protocol replaces the older Server-Sent Events (SSE) approach, with Microsoft recommending the newer transport unless clients specifically require SSE. The extension exposes two endpoints: `/runtime/webhooks/mcp` for streamable-http and `/runtime/webhooks/mcp/sse` for legacy SSE connections.
Translation: if you built an SSE-based prototype, it still works — but migrate to streamable HTTP when you can.

### Security: OBO Auth and Microsoft Entra, Built In

This is the part that was historically missing from MCP demos.
By integrating native OBO authentication and streamable HTTP transport, the update aims to solve the "security pain point" that has historically prevented AI agents from accessing sensitive downstream enterprise data.
The feature supports on-behalf-of (OBO) authentication, enabling tools to access downstream services using the user's identity rather than a service account.
In practice, this means your MCP tool can call a downstream API (say, Microsoft Graph or an internal service) impersonating the end user — a critical requirement for enterprise compliance.

### Language Support: .NET Front and Center
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
For C# specifically:
the Azure Functions MCP extension supports only the isolated worker model. Add the extension to your project by installing the NuGet package.
---

## Getting Started: From Zero to MCP Tool in C\#

Here's the fastest path to a running remote MCP server on Azure:

**Step 1 — Scaffold with `azd`:**

```bash
# For a C# (.NET) MCP server
azd init --template remote-mcp-functions-dotnet -e my-mcp-server
azd up
```
Just clone the repo and run `azd up` to get your own MCP server with all the power of the Azure Functions platform behind it.
**Step 2 — Define a tool with `McpToolTrigger`:**

```csharp
[Function(nameof(GetOrderStatus))]
public async Task<McpToolResponse> GetOrderStatus(
    [McpToolTrigger("GetOrderStatus", "Returns the current status of a customer order.")] 
    McpToolInvocationContext context)
{
    var orderId = context.Arguments["orderId"]?.ToString();
    // ... call your internal API
    return new McpToolResponse($"Order {orderId} is: Shipped");
}
```
You declare functions that act as tools with the MCP tool trigger. To configure a tool, you give it a name and description through the trigger, and then you define any properties it exposes. When an agent uses MCP, it first lists the tools, gathering this metadata. When the agent decides to invoke a tool, it populates the tool properties based on the operating context as part of its request — that's when your MCP tool trigger fires and your function code runs.
**Step 3 — Wire it to Azure AI Foundry:**
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
In the Foundry portal: **Agent → Tools → Add → Custom → Model Context Protocol (MCP)**, paste your function endpoint, and you're done.

---

## The Cold-Start Question (It's Not Hypothetical)

One practical concern: MCP clients have connection timeouts, and Functions cold starts can be brutal for SSE-style long-lived connections.
When MCP tools sit idle, costs drop to zero while maintaining fast wake-up times. The Premium plan supports "always-ready" instances that remain pre-initialized, eliminating cold-start latency — critical for mission-critical tools where initialization delays can cause SSE connection timeouts and poor agent response times. It is recommended to set two to three always-ready instances for critical 24/7 tools to ensure failover capacity.
**Rule of thumb:** Use Flex Consumption for dev/test. Move to Premium with always-ready instances for production agent tools that serve real users.

---

## The Infrastructure Tailwind: Maia 200

Here's the bigger picture worth keeping an eye on. Every token your MCP tool triggers costs money somewhere.
Microsoft recently introduced Maia 200, a breakthrough inference accelerator engineered to dramatically improve the economics of AI token generation — and it is the most efficient inference system Microsoft has ever deployed, with 30% better performance per dollar than the latest generation hardware in their fleet.
AI inference is increasingly defined by an efficient frontier — a curve that measures how much real-world capability and accuracy can be delivered at a given level of cost, latency, and energy. Different applications sit at different points on that frontier: interactive copilots prioritize low-latency responsiveness, while batch-scale workloads emphasize throughput at a given cost.
You won't interact with Maia 200 directly as an Azure Functions developer — but its efficiency gains should, over time, show up as lower Azure OpenAI token prices and better latency for the models your MCP tools call. Less burned cash for idle GPUs is good for everyone.
Product design decisions like response verbosity and default generation length directly affect how many requests each GPU can serve per hour — token discipline is cost discipline.
---

## Visual Studio 2026: MCP Is Now in Your IDE

If you're on Visual Studio 2026 Insiders, there's a bonus:
Azure MCP Server tools are now generally available out-of-the-box in Visual Studio 2026, bringing agentic cloud automation directly into the IDE. This integration empowers developers to build intelligent, secure applications faster, with less complexity. Azure MCP Server is a standards-based MCP server that enables AI agents to securely access and manage Azure resources through natural language.
So you can iterate on your MCP tool, ask GitHub Copilot in agent mode to query the deployed Azure Function logs, and never leave the IDE. That's a genuinely useful loop.

---

## Key Takeaways for .NET Engineers

| Concern | What to do |
|---|---|
| **Cold starts** | Use Azure Functions Premium plan with 2–3 always-ready instances for production |
| **Auth** | Enable Microsoft Entra OBO auth; avoid anonymous access |
| **Transport** | Default to streamable HTTP; use SSE only for legacy clients |
| **Cost** | Flex Consumption for dev; pay-per-invocation keeps idle tools free |
| **Secrets** | Store keys in Azure Key Vault — not `host.json` |
| **Discoverability** | Register your server in Azure API Center for org-wide governance |

---

## Further Reading

- Azure Functions MCP bindings (Microsoft Learn): https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-mcp
- InfoQ — *Microsoft Releases Azure Functions Support for Model Context Protocol Servers*: https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- Tech Community — *Building MCP Apps with Azure Functions MCP Extension*: https://techcommunity.microsoft.com/blog/appsonazureblog/building-mcp-apps-with-azure-functions-mcp-extension/4496536
- Microsoft Learn — *Build a custom remote MCP server using Azure Functions* (Quickstart): https://learn.microsoft.com/en-us/azure/azure-functions/scenario-custom-remote-mcp-server
- Microsoft Learn — *Tutorial: Host an MCP server on Azure Functions*: https://learn.microsoft.com/en-us/azure/azure-functions/functions-mcp-tutorial
- .NET Blog — *Build MCP Remote Servers with Azure Functions*: https://devblogs.microsoft.com/dotnet/build-mcp-remote-servers-with-azure-functions/
- Visual Studio Blog — *Azure MCP Server Now Built-In with Visual Studio 2026*: https://devblogs.microsoft.com/visualstudio/azure-mcp-server-now-built-in-with-visual-studio-2026-a-new-era-for-agentic-workflows/
- Microsoft Blog — *Maia 200: The AI Accelerator Built for Inference*: https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/
- Tech Community — *Deep Dive into the Maia 200 Architecture*: https://techcommunity.microsoft.com/blog/azureinfrastructureblog/deep-dive-into-the-maia-200-architecture/4489312
- Tech Community — *Inference at Enterprise Scale: Why LLM Inference Is a Capital Allocation Problem*: https://techcommunity.microsoft.com/blog/appsonazureblog/part-1-inference-at-enterprise-scale-why-llm-inference-is-a-capital-allocation-p/4498754