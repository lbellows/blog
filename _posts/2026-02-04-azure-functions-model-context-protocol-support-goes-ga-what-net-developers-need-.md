---
author: the.serf
date: 2026-02-04 06:47:49 -0500
layout: post
tags:
- .net
- azure
- context
- model
- protocol
- claude-haiku-4-5-20251001
title: 'Azure Functions Model Context Protocol Support Goes GA: What .NET Developers
  Need to Know'
---

# Azure Functions Model Context Protocol Support Goes GA: What .NET Developers Need to Know

**TL;DR:**
Microsoft's Model Context Protocol (MCP) support for Azure Functions is now generally available, with built-in OBO authentication and streamable HTTP transport to address security concerns for AI agents.
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
---

## Why This Matters for .NET Builders

If you're shipping AI agents on Azure, you've probably hit the same wall: how do you let an LLM safely access your enterprise systems without baking credentials into prompts or creating security nightmares?
By integrating native OBO (On-Behalf-Of) authentication and streamable HTTP transport, the update aims to solve the 'security pain point' that has historically prevented AI agents from accessing sensitive downstream enterprise data.
Until now, connecting agents to your APIs meant either:
- Embedding secrets in function calls (yikes)
- Building custom auth layers (time-consuming)
- Accepting limited tool access (frustrating)

MCP in Azure Functions flips the script.

## What Is Model Context Protocol?
The Model Context Protocol, developed by Anthropic, provides a standardized interface enabling AI agents to access external tools, data sources, and systems.
Think of it as a universal adapter between Claude, GPT, or any LLM and your backend—without reinventing authentication each time.

## How to Get Started: The .NET Path
The MCP extension quickstarts cover C# (.NET), Python, TypeScript (Node.js), with a Java QuickStart coming soon.
Here's the practical flow:

**Option 1: Azure Functions as an MCP Server**

Deploy your MCP server directly as an Azure Function. Your function handles tool definitions and logic; Azure Functions handles scaling and auth.

```csharp
// Pseudocode: C# Azure Function exposing MCP tools
[Function("GetCustomerData")]
public async Task<HttpResponseData> GetCustomerData(
    [HttpTrigger(AuthorizationLevel.Function, "post", Route = "tools/get_customer")] 
    HttpRequestData req,
    ILogger log)
{
    // Your MCP tool logic here
    // OBO auth is handled transparently by Azure Functions
    return req.CreateResponse(HttpStatusCode.OK);
}
```

**Option 2: Self-Hosted MCP Servers**

Already have MCP servers running elsewhere?
A new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
Wire them directly into your agents.

## Integration with Azure AI Foundry
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
This means:

- Deploy your MCP-enabled Azure Function
- Register it in Azure AI Foundry
- Your agents automatically see available tools
- No manual endpoint wiring required

## Cost & Latency Wins

By using Azure Functions, you get:
- **Pay-per-invocation pricing**: Only pay when agents actually call your tools
- **Auto-scaling**: Handle traffic spikes without pre-provisioning
- **Streamable HTTP transport**: Reduced latency for tool responses (especially important for real-time agent workflows)

## The Security Story
With built-in OBO authentication and streamable HTTP transport, it addresses key security concerns.
OBO (On-Behalf-Of) flow means:

1. Agent calls your Azure Function with a token
2. Azure Function validates the token and user identity
3. Function acts on behalf of that user to downstream systems
4. No credentials leak into prompts; everything stays in the auth layer

This is enterprise-grade: your data stays protected, compliance teams sleep better.

## Next Steps
Microsoft has published quickstart templates for both hosting approaches across multiple languages.
Head to the Azure documentation to grab the C# quickstart and spin up your first MCP-enabled function.

The agentic AI era is here—and with MCP on Azure Functions, you can finally build secure, scalable agent integrations without custom auth plumbing.

---

## Further reading

https://www.infoq.com/news/2026/01/azure-functions-mcp-support/

https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new

https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/

https://devblogs.microsoft.com/all-things-azure/claude-code-microsoft-foundry-enterprise-ai-coding-agent-setup/

https://learn.microsoft.com/en-us/azure/ai-services/openai/whats-new