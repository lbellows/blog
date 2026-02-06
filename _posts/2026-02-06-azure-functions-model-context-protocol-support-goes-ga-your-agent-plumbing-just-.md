---
author: the.serf
date: 2026-02-06 06:47:57 -0500
layout: post
tags:
- azure
- .net
- agent
- architecture
- box
- claude-haiku-4-5-20251001
title: 'Azure Functions Model Context Protocol Support Goes GA: Your Agent Plumbing
  Just Got Safer'
---

# Azure Functions Model Context Protocol Support Goes GA: Your Agent Plumbing Just Got Safer

**TL;DR:**
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability
, enabling secure, identity-aware agentic workflows.
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes
. This is the infrastructure layer your AI agents have been waiting for.

---

## Why This Matters for Your Architecture

If you've been building AI agents on Azure, you've hit the same friction point: how do you let an LLM safely call your backend services without baking credentials into prompts or managing a sprawling OAuth mess?
By integrating native OBO (on-behalf-of) authentication and streamable HTTP transport, the update aims to solve the 'security pain point' that has historically prevented AI agents from accessing sensitive downstream enterprise data
.

This isn't theoretical.
The Model Context Protocol, developed by Anthropic, provides a standardized interface enabling AI agents to access external tools, data sources, and systems
. Now it's baked into Azure Functions as a first-class citizen.

## What You Get in the Box
The MCP extension, which entered public preview in April 2025, now supports .NET, Java, JavaScript, Python, and TypeScript
. For .NET teams, this means you can write your tool definitions in C# and let the Azure Functions runtime handle the security plumbing.

**Two deployment patterns:**

1. **Managed MCP servers** – Your Functions app hosts the MCP server directly. Azure handles authentication, scaling, and observability.
2. **Self-hosted MCP servers** –
A new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes
. Bring your own MCP implementation; Azure Functions just brokers the connection.

## Getting Started: A .NET Example
Microsoft has published quickstart templates for both hosting approaches across multiple languages. The MCP extension quickstarts cover C# (.NET), Python, TypeScript (Node.js), with a Java QuickStart coming soon
.

Here's the conceptual flow:

```csharp
// Your Azure Function exposes an MCP tool
[Function("QueryDatabase")]
public async Task<string> QueryDatabase(
    [HttpTrigger(AuthorizationLevel.Anonymous, "post")] HttpRequest req)
{
    // The MCP runtime handles auth context automatically
    var userId = req.HttpContext.User.FindFirst("oid")?.Value;
    
    // Your agent can now safely call this with user context
    var results = await _db.QueryAsync(userId);
    return JsonConvert.SerializeObject(results);
}
```

The agent calls this tool through MCP; Azure Functions validates the caller's identity and injects it into your function context. No credential passing. No manual JWT parsing.

## Integration with Azure AI Foundry
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers
. This is the real win: your agent framework (whether you're using Semantic Kernel, LangChain, or a custom orchestrator) discovers your tools at runtime, and Foundry handles the rest.

## The Practical Takeaway

GA status means this is production-ready, not "preview and pray." If you're shipping agents on Azure and need to call internal APIs, databases, or services without leaking secrets into LLM context—this is your pattern. It's also a signal that Microsoft is serious about standardizing agent tooling across the ecosystem, rather than locking you into proprietary abstractions.

One caveat:
treat claims as marketing until you've seen working results in your own codebase, with your constraints, and your risk profile. Only believe what you can validate
. Test the OBO flow in your tenant; it's solid, but every org's security posture is different.

---

## Further Reading

https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-mcp

https://www.infoq.com/news/2026/01/azure-functions-mcp-support/

https://azure.microsoft.com/en-us/blog/product/azure-ai/

https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/

https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/what-is-trending-in-hugging-face-on-microsoft-foundry-feb-2-2026/4490602