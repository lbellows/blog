---
author: the.serf
date: 2026-01-28 06:35:19 -0500
layout: post
tags:
- azure
- tools
- .net
- functions
- matters
- claude-haiku-4-5-20251001
title: 'Azure Functions Model Context Protocol (MCP) Now GA: Secure Agent Tooling
  for .NET Developers'
---

# Azure Functions Model Context Protocol (MCP) Now GA: Secure Agent Tooling for .NET Developers

**TL;DR**
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability
, enabling .NET developers to build identity-secure AI agents without custom authentication plumbing.
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
This eliminates a major friction point: agents can finally access enterprise data safely.

---

## The Problem: Agents Need Tools, But Tools Need Security

Building AI agents sounds straightforward until your agent needs to call a downstream API—say, your internal CRM or data warehouse. Suddenly you're wrestling with authentication, authorization, and the terror of accidentally leaking credentials into model context.
By integrating native OBO (On-Behalf-Of) authentication and streamable HTTP transport, the update aims to solve the 'security pain point' that has historically prevented AI agents from accessing sensitive downstream enterprise data.
In plain English: your agent can now impersonate the user who triggered it, without you manually managing tokens.

## What's New (and Why It Matters)
The Model Context Protocol, developed by Anthropic, provides a standardized interface enabling AI agents to access external tools, data sources, and systems.
Think of it as a contract between your agent and your tools—the agent knows what tools exist, what they do, and how to call them safely.

**For .NET developers specifically:**
The MCP extension quickstarts cover C# (.NET), Python, TypeScript (Node.js), with a Java QuickStart coming soon.
This means you can scaffold an MCP server in minutes using familiar .NET patterns.

### Pricing & Performance Trade-offs

Cost and latency are the two questions every engineer asks. Microsoft offers two hosting strategies:

1. **Consumption Plan (Zero Cost at Rest)**
When MCP tools sit idle, costs drop to zero while maintaining fast wake-up times. The Premium plan supports "always-ready" instances that remain pre-initialized, eliminating cold-start latency, which is critical for mission-critical tools where initialization delays can cause SSE connection timeouts and poor agent response times.
2. **Dedicated Plans**
Developers can also use Dedicated plans for workloads requiring predictable performance or integration with virtual networks.
**Practical recommendation:**
Rawat recommends setting two to three always-ready instances for critical 24/7 tools to ensure failover capacity.
### Integration with Azure AI Foundry
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
This is the real win—your agent doesn't need custom routing logic. It just asks Foundry for available tools, and Foundry handles the rest.

## Getting Started: The .NET Path
Microsoft has published quickstart templates for both hosting approaches across multiple languages. The MCP extension quickstarts cover C# (.NET), Python, TypeScript (Node.js), with a Java QuickStart coming soon.
Head to the official quickstart docs and scaffold a new MCP server:

```bash
# Pseudocode—check official docs for exact CLI
dotnet new mcp-server -n MyAgentTools
cd MyAgentTools
# Define your tools as C# methods with MCP attributes
# Deploy to Azure Functions
func azure functionapp publish MyFunctionApp
```

Your tools are now discoverable by any agent in your Azure tenant—no credential passing, no manual auth wiring.

## The Broader Picture: Why This Matters Now
Azure is now the only cloud providing access to both Claude and GPT frontier models to customers on one platform.
With MCP on Azure Functions, you're not just choosing a model—you're choosing a secure, standardized way to let that model interact with your business logic.

This is the inflection point where agents move from chatbots to *infrastructure*. And infrastructure demands security, observability, and cost predictability. MCP + Azure Functions delivers all three.

---

## Further reading

- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/model-context-protocol
- https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- https://azure.microsoft.com/en-us/blog/introducing-anthropics-claude-models-in-microsoft-foundry-bringing-frontier-intelligence-to-azure/
- https://azure.microsoft.com/en-us/blog/introducing-claude-opus-4-5-in-microsoft-foundry/
- https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/