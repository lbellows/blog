---
author: the.serf
date: 2026-02-05 06:50:06 -0500
layout: post
tags:
- .net
- azure
- now
- authentication
- bigger
- claude-haiku-4-5-20251001
title: 'Azure Functions Now GA for Model Context Protocol: What .NET Developers Need
  to Know'
---

# Azure Functions Now GA for Model Context Protocol: What .NET Developers Need to Know

**TL;DR**
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability, signaling a shift toward standardized, identity-secure agentic workflows.
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
This is a major unlock for building production-grade AI agents on Azure.

---

## Why This Matters Now

For years, the gap between "AI demo" and "AI in production" has been real.
With MCP reducing the friction of connecting agents to real systems, 2026 is likely to be the year agentic workflows finally move from demos into day-to-day practice.
Microsoft's GA announcement removes a key blocker: secure, standardized connectivity between AI agents and enterprise systems.
The Model Context Protocol, developed by Anthropic, provides a standardized interface enabling AI agents to access external tools, data sources, and systems.
Think of it as a universal adapter for AI. Before GA, using MCP on Azure Functions meant dealing with preview-grade APIs and uncertain production readiness. Now it's battle-tested and supported.

## The Security Win: OBO Authentication

Here's where it gets practical.
With built-in OBO authentication and streamable HTTP transport, the update aims to solve the 'security pain point' that has historically prevented AI agents from accessing sensitive downstream enterprise data.
For .NET engineers, this means your Azure Functions can now safely expose enterprise databases, APIs, and services to AI agents *without* creating new credential management nightmares. The agent inherits the caller's identity (On-Behalf-Of), so your existing Azure AD policies just work.

## Getting Started in .NET
The MCP extension quickstarts cover C# (.NET), Python, TypeScript (Node.js), with a Java QuickStart coming soon.
Here's a minimal example of what you're looking at:

```csharp
using Microsoft.Extensions.AI;
using Azure.Functions.Worker;
using Azure.Functions.Worker.Http;

public static class MCPAgentFunction
{
    [Function("ProcessWithAgent")]
    public static async Task<HttpResponseData> Run(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)]
        HttpRequestData req,
        FunctionContext context)
    {
        // MCP-enabled client automatically discovers and invokes tools
        var client = new MCPClient("your-mcp-server-endpoint");
        
        var response = await client.InvokeAsync(
            "Fetch user data and summarize recent activity",
            userIdentity: req.HttpContext.User
        );

        var httpResponse = req.CreateResponse(System.Net.HttpStatusCode.OK);
        await httpResponse.WriteAsJsonAsync(response);
        return httpResponse;
    }
}
```

The key detail: `req.HttpContext.User` flows through to downstream systems. No hardcoded secrets, no separate service accounts.

## Integration with Azure AI Foundry
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
This means you can:
- Define MCP servers in Azure Functions
- Register them in Azure AI Foundry
- Let agents auto-discover and call them
- Monitor everything in one place

No glue code. No middleware translation layers.

## Deployment Options: Pick Your Poison

You have two paths:

1. **Azure Functions native**: Deploy MCP as an Azure Function directly. Scales automatically, integrates with managed identity, billing per execution.

2. **Self-hosted MCP servers**:
A new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
Run them in containers, VMs, or on-premises if you need tighter control or have compliance constraints.

## The Bigger Picture
Anthropic's Model Context Protocol (MCP), a "USB-C for AI" that lets AI agents talk to the external tools like databases, search engines, and APIs, proved the missing connective tissue and is quickly becoming the standard. OpenAI and Microsoft have publicly embraced MCP, and Anthropic recently donated it to the Linux Foundation's new Agentic AI Foundation.
Translation: MCP isn't a Microsoft-only bet. It's becoming infrastructure. Learning it now means your skills transfer across OpenAI, Anthropic, Google, and other platforms.

## What You Should Do Monday Morning

1. **Review your enterprise integrations**: Which APIs, databases, and services do your agents need to touch?
2. **Draft an MCP server**: Wrap one critical system (start small—maybe a SQL database or internal API).
3. **Test in Azure Functions**: Deploy a function, wire it to Azure AI Foundry, and run a test agent.
4. **Check your identity model**: Ensure your Azure AD setup supports OBO flows for the systems you're connecting.

The GA release removes the "preview tax" of worrying about breaking changes. You can now ship this to production with confidence.

---

## Further Reading

https://www.infoq.com/news/2026/01/azure-functions-mcp-support/

https://techcrunch.com/2026/01/02/in-2026-ai-will-move-from-hype-to-pragmatism/

https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/

https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/what-is-trending-in-hugging-face-on-microsoft-foundry-feb-2-2026/

https://venturebeat.com/ai/anthropic-launches-enterprise-agent-skills-and-opens-the-standard/

https://learn.microsoft.com/en-us/azure/databricks/ai-bi/release-notes/2026