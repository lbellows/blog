---
author: the.serf
date: 2026-01-26 06:33:10 -0500
layout: post
tags:
- azure
- .net
- actually
- agentic
- caveat
- claude-haiku-4-5-20251001
title: 'Azure Functions Model Context Protocol Support Hits GA: Ship Agentic Workflows
  at Scale'
---

# Azure Functions Model Context Protocol Support Hits GA: Ship Agentic Workflows at Scale

**TL;DR**
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability, signaling a shift toward standardized, identity-secure agentic workflows.
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
This matters because
the update aims to solve the 'security pain point' that has historically prevented AI agents from accessing sensitive downstream enterprise data.
## What's Actually Shipping
The MCP extension is now generally available, with support for C#(.NET), Java, JavaScript (Node.js), Python, and Typescript (Node.js).
For .NET teams, this means you can now build production-grade remote MCP servers directly on Azure Functions without the deployment friction that plagued earlier previews.

The GA release brings two key improvements:

1. **Native authentication & authorization**:
Developers can configure Microsoft Entra or other OAuth providers for server authentication. The feature also supports on-behalf-of (OBO) authentication, enabling tools to access downstream services using the user's identity rather than a service account.
2. **Streamable HTTP transport**:
Support for the streamable HTTP transport protocol replaces the older Server-Sent Events (SSE) approach, with Microsoft recommending the newer transport unless clients specifically require SSE. The extension exposes two endpoints: /runtime/webhooks/mcp for streamable-http and /runtime/webhooks/mcp/sse for legacy SSE connections.
## Why This Matters for .NET Developers
Anthropic's Model Context Protocol (MCP), a "USB-C for AI" that lets AI agents talk to the external tools like databases, search engines, and APIs, proved the missing connective tissue and is quickly becoming the standard. OpenAI and Microsoft have publicly embraced MCP, and Anthropic recently donated it to the Linux Foundation's new Agentic AI Foundation.
Translation: if you're building agents that need to access your APIs, databases, or business logic, MCP is no longer a nice-to-have—it's the lingua franca. Azure Functions as a MCP host solves the "where do I run this?" problem.

## Getting Started: The C# Path
For C#, the Azure Functions MCP extension supports only the isolated worker model.
Here's a minimal example:

```csharp
[Function(nameof(GetSnippet))]
public object GetSnippet(
    [McpToolTrigger("get_snippet", "Retrieve a saved code snippet")] 
    ToolInvocationContext context,
    [BlobInput("snippets/{mcptoolargs.snippetname}.json")] 
    string snippetContent)
{
    return snippetContent;
}
```
The MCP tool trigger allows you to focus on what matters most: the logic of the tool you want to expose to agents.
Bindings handle the rest—blob storage, queues, Cosmos DB, whatever you need.
There's a quickstart template to easily build and deploy a custom remote MCP server to the cloud using Azure functions. You can clone/restore/run on your local machine with debugging, and azd up to have it in the cloud in a couple minutes.
## Scaling & Cost Considerations
Azure Functions offers multiple hosting plans tailored to different MCP server requirements. The Flex Consumption plan provides automatic scaling based on demand with a pay-per-execution billing model and scale-to-zero economics. When MCP tools sit idle, costs drop to zero while maintaining fast wake-up times. The Premium plan supports "always-ready" instances that remain pre-initialized, eliminating cold-start latency, which is critical for mission-critical tools where initialization delays can cause SSE connection timeouts and poor agent response times.
For most teams, Flex Consumption is the right default. If your agents are calling tools continuously and cold starts matter, Premium pays for itself.

## Integration with Azure AI Foundry
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
This means your MCP server becomes discoverable and callable by agents running in Azure AI Foundry—no manual wiring required.

## A Realistic Caveat
Be critical when vendors promise "80% accuracy" as if that's the whole story. This is still generative AI in early 2026. Treat claims as marketing until you've seen working results in your own codebase, with your constraints, and your risk profile.
MCP is mature; agentic workflows using MCP are not. Test thoroughly before shipping to production.

## Further Reading

- https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-mcp
- https://github.com/Azure-Samples/remote-mcp-functions-dotnet
- https://devblogs.microsoft.com/dotnet/build-mcp-remote-servers-with-azure-functions/
- https://techcommunity.microsoft.com/blog/appsonazureblog/azure-functions-ignite-2025-update/4469815
- https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/