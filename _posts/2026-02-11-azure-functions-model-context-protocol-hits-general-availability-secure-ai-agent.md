---
author: the.serf
date: 2026-02-11 06:58:03 -0500
layout: post
tags:
- agents
- .net
- authentication
- availability
- azure
- claude-haiku-4-5-20251001
title: 'Azure Functions Model Context Protocol Hits General Availability: Secure AI
  Agents Just Got Easier'
---

# Azure Functions Model Context Protocol Hits General Availability: Secure AI Agents Just Got Easier

**TL;DR**
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability, signaling a shift toward standardized, identity-secure agentic workflows.
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
For .NET engineers shipping on Azure, this means you can now securely expose your business logic as tools for AI agents—with built-in authentication and zero-trust patterns—without reinventing the wheel.

---

## What's MCP, and Why Should You Care?
The Model Context Protocol, developed by Anthropic, provides a standardized interface enabling AI agents to access external tools, data sources, and systems.
Think of it as a contract between AI agents and your APIs. Instead of agents making ad-hoc HTTP calls or using fragile prompt-injection workarounds, MCP gives you a clean, composable way to say: "Here are the tools you can use, here's what they do, and here's how to call them safely."
Anthropic's Model Context Protocol (MCP), a "USB-C for AI" that lets AI agents talk to the external tools like databases, search engines, and APIs, proved the missing connective tissue and is quickly becoming the standard. OpenAI and Microsoft have publicly embraced MCP.
In other words, it's not a niche experiment anymore—it's table stakes for enterprise AI in 2026.

---

## The Security Win: OBO Authentication & Streamable HTTP

The headline feature here is
integrating native OBO (on-behalf-of) authentication and streamable HTTP transport, which aims to solve the 'security pain point' that has historically prevented AI agents from accessing sensitive downstream enterprise data.
What does that mean in practice?
The feature supports on-behalf-of (OBO) authentication, enabling tools to access downstream services using the user's identity rather than a service account.
So instead of your MCP server having a single, overpowered service identity, each agent request carries the caller's identity through to downstream APIs. That's least-privilege in action—and it's a massive win for compliance and security audits.

On the transport side,
support for the streamable HTTP transport protocol replaces the older Server-Sent Events (SSE) approach, with Microsoft recommending the newer transport unless clients specifically require SSE.
Streamable HTTP is faster, more resilient to connection hiccups, and plays nicer with cloud load balancers.

---

## Getting Started: .NET Edition
For C#, the Azure Functions MCP extension supports only the isolated worker model.
Here's the minimal setup:

```csharp
// Install NuGet: Microsoft.Azure.Functions.Worker.Extensions.Mcp
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Mcp;

public class McpTools
{
    [Function(nameof(GetCustomerInfo))]
    public string GetCustomerInfo(
        [McpToolTrigger("get_customer", "Fetch customer details by ID")] 
        ToolInvocationContext context,
        [McpToolProperty("customer_id", "The customer's unique ID", true)] 
        string customerId)
    {
        // Your business logic here
        return $"Customer {customerId}: Alice, Premium tier";
    }
}
```

That's it. The `[McpToolTrigger]` attribute tells Azure Functions to expose this as an MCP tool. Agents can discover it, call it, and the runtime handles auth, serialization, and error handling.
The extension exposes two endpoints: /runtime/webhooks/mcp for streamable-http and /runtime/webhooks/mcp/sse for legacy SSE connections. Built-in authentication and authorization implement the MCP authorization protocol requirements, including issuing 401 challenges and hosting Protected Resource Metadata documents. Developers can configure Microsoft Entra or other OAuth providers for server authentication.
---

## Cost & Latency: The Flex Consumption Sweet Spot
The Flex Consumption plan provides automatic scaling based on demand with a pay-per-execution billing model and scale-to-zero economics. When MCP tools sit idle, costs drop to zero while maintaining fast wake-up times. The Premium plan supports "always-ready" instances that remain pre-initialized, eliminating cold-start latency, which is critical for mission-critical tools where initialization delays can cause SSE connection timeouts and poor agent response times.
For most teams, Flex Consumption is the default: you pay only when your tools are invoked, and you get sub-second startup for typical workloads. If you're building mission-critical agent orchestration, Premium gives you predictable latency at the cost of always-on compute.

---

## Integration with Microsoft Foundry & AI Agents
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
Once your MCP server is deployed to Azure Functions, you register it in Microsoft Foundry's Agent Service, and your agents can start using your tools immediately. No custom adapters, no glue code.

---

## One Caveat: Know Your Limits
Nested arrays and complex types must be serialized as comma-separated strings when integrating with Azure AI Foundry, and programmatic tool approval using require_approval="never" is necessary for production workflows since UI-based approvals don't persist in automated deployments.
These are edge cases, but worth knowing before you hit them in production.

---

## The Bottom Line

If you're a .NET engineer on Azure building AI agents or integrating with them, MCP on Azure Functions is now your go-to pattern. It's secure, it's standardized, it integrates seamlessly with Microsoft Foundry, and it costs almost nothing when idle. The GA release means you can ship to production today—not "in preview" or "with caveats."

The era of agents making unguarded API calls is over. Welcome to the era of composable, auditable, identity-aware tools.

---

## Further reading

- https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-mcp
- https://learn.microsoft.com/en-us/azure/azure-functions/functions-mcp-tutorial
- https://devblogs.microsoft.com/dotnet/build-mcp-remote-servers-with-azure-functions/
- https://learn.microsoft.com/en-us/azure/ai-foundry/mcp/build-your-own-mcp-server?view=foundry
- https://techcommunity.microsoft.com/blog/appsonazureblog/build-ai-agent-tools-using-remote-mcp-with-azure-functions/4401059