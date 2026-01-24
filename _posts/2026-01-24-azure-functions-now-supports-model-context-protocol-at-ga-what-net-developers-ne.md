---
author: the.serf
date: 2026-01-24 06:29:05 -0500
layout: post
tags:
- .net
- azure
- functions
- now
- angle
- claude-haiku-4-5-20251001
title: 'Azure Functions Now Supports Model Context Protocol at GA: What .NET Developers
  Need to Know'
---

# Azure Functions Now Supports Model Context Protocol at GA: What .NET Developers Need to Know

**TL;DR**
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability, signaling a shift toward standardized, identity-secure agentic workflows.
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
Translation: you can now safely wire AI agents to your enterprise data without reinventing authentication or burning through your compute budget.

---

## Why MCP + Azure Functions Matters Right Now

For years, the agent-tool integration problem felt like plumbing hell. You'd build an AI agent, realize it needed access to a database or API, and suddenly you're implementing OAuth flows, managing credentials, and praying you didn't accidentally expose sensitive data.
By integrating native OBO (On-Behalf-Of) authentication and streamable HTTP transport, the update aims to solve the 'security pain point' that has historically prevented AI agents from accessing sensitive downstream enterprise data.
The Model Context Protocol, developed by Anthropic, provides a standardized interface enabling AI agents to access external tools, data sources, and systems.
Think of it as a "USB-C for AI"—a neutral plug that any agent can use to talk to any tool without vendor lock-in or custom adapters.

## The .NET Developer Angle

Here's where it gets practical.
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
For C# shops, this means you can write MCP servers using your existing .NET skills and host them on Azure Functions—the same serverless runtime you probably already know.

### Cost & Latency Wins
When MCP tools sit idle, costs drop to zero while maintaining fast wake-up times. The Premium plan supports "always-ready" instances that remain pre-initialized, eliminating cold-start latency, which is critical for mission-critical tools where initialization delays can cause SSE connection timeouts and poor agent response times.
That's a real win for production workloads where your agents need sub-second tool access.

### Getting Started: A .NET Example
Microsoft has published quickstart templates for both hosting approaches across multiple languages. The MCP extension quickstarts cover C# (.NET), Python, TypeScript (Node.js), with a Java QuickStart coming soon.
Here's a skeleton to get you oriented:

```csharp
// Azure Function hosting an MCP server
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;

public class MCPServerFunction
{
    [Function("MCPToolServer")]
    public async Task<HttpResponseData> Run(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "mcp/{*route}")] 
        HttpRequestData req)
    {
        // MCP server logic here
        // OBO auth is handled automatically by Azure Functions
        var response = req.CreateResponse();
        response.WriteString("MCP server ready");
        return response;
    }
}
```
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
That means your agents in Azure AI Foundry can auto-discover and use these tools—no manual wiring needed.

## The Bigger Picture: Standardization Is Winning

This GA release reflects a larger industry shift.
Anthropic donated its Model Context Protocol to the Linux Foundation on December 9, and both Anthropic and OpenAI co-founded the Agentic AI Foundation alongside Block. Google, Microsoft, and Amazon Web Services joined as members.
MCP is becoming the de facto standard for agent-tool communication, which means your investment in learning it today pays dividends across multiple platforms tomorrow.

---

## Practical Takeaway

If you're shipping AI agents on Azure with .NET, MCP on Azure Functions removes a major friction point: secure, standards-based tool access without the security gymnastics. Start with the C# quickstarts, test with a simple tool (maybe a database query wrapper), and let the OBO auth handle the heavy lifting. Your future self—and your security team—will thank you.

---

## Further reading

- https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-lifecycle
- https://techcommunity.microsoft.com/blog/azuredevcommunityblog/%F0%9F%9A%80-ai-toolkit-for-vs-code-january-2026-update/4485205
- https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/
- https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard/
- https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/