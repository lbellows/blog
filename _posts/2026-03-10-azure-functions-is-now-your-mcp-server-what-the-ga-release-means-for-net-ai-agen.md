---
author: the.serf
date: 2026-03-10 07:48:14 -0400
layout: post
tags:
- azure
- mcp
- .net
- functions
- agents
- claude-sonnet-4-6
title: 'Azure Functions Is Now Your MCP Server: What the GA Release Means for .NET
  AI Agents'
---

# Azure Functions Is Now Your MCP Server: What the GA Release Means for .NET AI Agents

**TL;DR:** Azure Functions' support for the Model Context Protocol (MCP) has reached General Availability. For .NET engineers building AI agents on Azure, this means you can expose your existing business logic as a secure, serverless, identity-aware tool that any MCP-compatible AI client — GitHub Copilot, Azure AI Foundry agents, and more — can call. Cold-start latency is a real concern; the fix is one hosting plan setting. Here's what changed, why it matters, and how to bootstrap a C# MCP server in under five minutes.

---

## The Setup: Why MCP + Azure Functions Is a Big Deal

The Model Context Protocol (MCP) — originally developed by Anthropic — has become the de facto standard wiring harness for giving AI agents access to external tools and data. Think of it as USB-C for AI: one port, many peripherals. The problem until recently was that running an MCP server meant spinning up a long-lived process, often on a developer's laptop, with ad-hoc security bolted on as an afterthought.
Security and compliance teams couldn't allow arbitrary, unvetted "Shadow Agents" running on developer laptops to access critical data systems like electronic healthcare records or customer PII
— and rightly so. The GA release of Azure Functions MCP support is a direct answer to that problem.
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability, signaling a shift toward standardized, identity-secure agentic workflows.
---

## What's New in the GA Release

### Streamable HTTP Transport (Drop SSE)
Support for the streamable HTTP transport protocol replaces the older Server-Sent Events (SSE) approach, with Microsoft recommending the newer transport unless clients specifically require SSE.
The extension exposes two endpoints: `/runtime/webhooks/mcp` for streamable-http and `/runtime/webhooks/mcp/sse` for legacy SSE connections.
**Practical takeaway:** Point new clients at `/runtime/webhooks/mcp`. Only keep the SSE endpoint around if you have a legacy consumer that hasn't updated. SSE is not long for this world.

### Built-In Auth with OBO (On-Behalf-Of)

This is the headline feature for enterprise teams.
Built-in authentication and authorization implement the MCP authorization protocol requirements, including issuing 401 challenges and hosting Protected Resource Metadata documents. Developers can configure Microsoft Entra or other OAuth providers for server authentication. The feature also supports on-behalf-of (OBO) authentication, enabling tools to access downstream services using the user's identity rather than a service account.
That last sentence is the important one. Your MCP tool doesn't need a fat service principal with broad permissions. The *user's* identity flows through — a pattern enterprise security teams have demanded for years.

### Multi-Language Support (Including C#)
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
For C# specifically,
the Azure Functions MCP extension supports only the isolated worker model.
Make sure your project targets the isolated worker — the in-process model is on its way out anyway.

---

## Cold Starts: The Latency Elephant in the Room

Serverless + AI agents = a cold-start problem waiting to bite you in demo.
When MCP tools sit idle, costs drop to zero while maintaining fast wake-up times. The Premium plan supports "always-ready" instances that remain pre-initialized, eliminating cold-start latency, which is critical for mission-critical tools where initialization delays can cause SSE connection timeouts and poor agent response times.
Rawat recommends setting two to three always-ready instances for critical 24/7 tools to ensure failover capacity. Developers can also use Dedicated plans for workloads requiring predictable performance or integration with virtual networks.
> 💡 **Rule of thumb:** Consumption plan = great for dev and batch tools with relaxed SLAs. Premium plan with 2–3 always-ready instances = production-grade agentic tools. Dedicated plan = when you need VNet integration or predictable baseline.

---

## The Infrastructure Tailwind: Maia 200

Here's the "why now" context. In late January,
Microsoft introduced Maia 200, a breakthrough inference accelerator engineered to dramatically improve the economics of AI token generation.
Maia 200 is the most efficient inference system Microsoft has ever deployed, with 30% better performance per dollar than the latest generation hardware in their fleet today.
Maia 200 will be part of Microsoft's heterogeneous AI infrastructure supporting multiple models, including the latest GPT-5.2 models from OpenAI, to power AI workloads in Microsoft Foundry and Microsoft 365 Copilot.
What does silicon have to do with your MCP server? Everything, indirectly. Cheaper inference tokens upstream = more economical agentic loops calling your MCP tools downstream. The per-call cost math on agents improves as the infrastructure layer gets more efficient. That's the rising tide that makes serverless MCP tools genuinely cost-viable at scale.

---

## Quickstart: C# MCP Server on Azure Functions in 4 Commands
You'll need the .NET 10 SDK, Azure Functions Core Tools ≥ 4.0.7030, and Azure Developer CLI 1.23.x or above for deployment.
```bash
# 1. Bootstrap from the official .NET template
azd init --template remote-mcp-functions-dotnet -e my-mcp-server

# 2. Start the local emulator (Azurite) in VS Code, then:
func start

# 3. Test locally via GitHub Copilot or MCP Inspector
#    Point your client at: http://localhost:7071/runtime/webhooks/mcp

# 4. Deploy to Azure (Flex Consumption plan, Entra auth pre-wired)
azd up
```
The MCP server is pre-configured with built-in authentication using Microsoft Entra as the identity provider. You can also use API Management to secure the server, as well as network isolation using VNET.
Because the app runs on the Flex Consumption plan — which follows a pay-for-what-you-use billing model — completing the quickstart incurs a small cost of a few USD cents or less in your Azure account.
Translation: your wallet is safe while you're learning.

### A Minimal C# Tool Trigger

Here's the shape of a C# MCP tool function (isolated worker model):

```csharp
[Function(nameof(GetCustomerOrder))]
public string GetCustomerOrder(
    [McpToolTrigger("get_customer_order",
        "Returns the latest order for a given customer ID")]
    ToolInvocationContext context,
    [CosmosDBInput(/* connection */)] CustomerOrder order)
{
    return JsonSerializer.Serialize(order);
}
```
The Azure Functions MCP extension allows you to use Azure Functions to create remote MCP servers. These servers can host MCP tool trigger functions, which MCP clients — such as language models and agents — can query and access to do specific tasks.
Notice the `[CosmosDBInput]` binding — you get the full Azure Functions binding ecosystem for free. Blob storage, Service Bus, SQL, Cosmos: all composable with zero extra wiring.

---

## Connecting to Azure AI Foundry Agents

Once deployed, wiring your MCP server into an AI Foundry agent is a few clicks:
In the Foundry portal, find the agent you want to configure with MCP servers hosted on Functions. Under Tools, select the Add button, then select **+ Add a new tool**. Select the Custom tab, then select **Model Context Protocol (MCP)** and the Create button.
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
And if you're living inside Visual Studio 2026:
Azure MCP Server tools are now generally available out-of-the-box in Visual Studio 2026, bringing agentic cloud automation directly into your trusted IDE. This integration empowers developers to build intelligent, secure applications faster, with less complexity and more confidence.
---

## Key Takeaways for .NET/Azure Engineers

| Concern | Guidance |
|---|---|
| **Transport** | Use Streamable HTTP (`/runtime/webhooks/mcp`); avoid SSE for new work |
| **Auth** | Enable Entra OBO auth — never skip this in production |
| **Latency** | Premium plan + 2–3 always-ready instances for agent-facing tools |
| **Cost (dev)** | Flex Consumption plan; pay-per-call, cents-level for experimentation |
| **SDK** | .NET 10, isolated worker model, `Microsoft.Azure.Functions.Worker` ≥ 2.1.0 |
| **Tooling** | `azd init --template remote-mcp-functions-dotnet` to skip boilerplate |

---

## Further Reading

- Azure Functions MCP bindings (Microsoft Learn): https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-mcp
- Tutorial: Host an MCP server on Azure Functions: https://learn.microsoft.com/en-us/azure/azure-functions/functions-mcp-tutorial
- Remote MCP with Azure Functions (.NET/C#) sample: https://learn.microsoft.com/en-us/samples/azure-samples/remote-mcp-functions-dotnet/remote-mcp-functions-dotnet/
- Build MCP Remote Servers with Azure Functions (.NET Blog): https://devblogs.microsoft.com/dotnet/build-mcp-remote-servers-with-azure-functions/
- Azure MCP Server Now Built-In with Visual Studio 2026 (VS Blog): https://devblogs.microsoft.com/visualstudio/azure-mcp-server-now-built-in-with-visual-studio-2026-a-new-era-for-agentic-workflows/
- Microsoft Releases Azure Functions MCP Support (InfoQ): https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- Maia 200: The AI Accelerator Built for Inference (Microsoft Blog): https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/
- Deep Dive into the Maia 200 Architecture (Azure Infrastructure Blog): https://techcommunity.microsoft.com/blog/azureinfrastructureblog/deep-dive-into-the-maia-200-architecture/4489312
- Microsoft Announces Maia 200 (TechCrunch): https://techcrunch.com/2026/01/26/microsoft-announces-powerful-new-chip-for-ai-inference/