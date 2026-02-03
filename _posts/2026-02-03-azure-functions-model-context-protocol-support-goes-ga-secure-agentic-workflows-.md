---
author: the.serf
date: 2026-02-03 06:50:06 -0500
layout: post
tags:
- azure
- functions
- mcp
- why
- .net
- claude-haiku-4-5-20251001
title: 'Azure Functions Model Context Protocol Support Goes GA: Secure Agentic Workflows
  Just Got Real'
---

# Azure Functions Model Context Protocol Support Goes GA: Secure Agentic Workflows Just Got Real

**TL;DR**
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability, signaling a shift toward standardized, identity-secure agentic workflows.
The MCP extension now supports .NET, Java, JavaScript, Python, and TypeScript, while a new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
For .NET teams, this means you can now ship production AI agents that securely access enterprise data—no more security theater.

---

## The Problem MCP Solves (And Why You Should Care)

If you've tried building AI agents that touch real enterprise systems, you've hit the wall: how do you let Claude or GPT-4 safely call your internal APIs, databases, and tools without leaking credentials or context?
Anthropic's Model Context Protocol (MCP), a "USB-C for AI" that lets AI agents talk to the external tools like databases, search engines, and APIs, proved the missing connective tissue and is quickly becoming the standard.
OpenAI and Microsoft have publicly embraced MCP, and Anthropic recently donated it to the Linux Foundation's new Agentic AI Foundation, which aims to help standardize open source agentic tools.
Until now, running MCP servers on Azure required workarounds. Today, that changes.

---

## What's New: Azure Functions as a First-Class MCP Host
By integrating native OBO authentication and streamable HTTP transport, the update aims to solve the 'security pain point' that has historically prevented AI agents from accessing sensitive downstream enterprise data.
**Key wins for .NET developers:**

- **Native OBO (On-Behalf-Of) Auth:** Your MCP tools inherit Azure identity without manual token plumbing. Agents call your functions using the same managed identity as the calling application.
- **Streamable HTTP Transport:** Real-time agent-to-tool communication without polling loops. Critical for agents that need fast feedback.
- **Self-Hosted Option:**
A new self-hosted option lets developers deploy existing MCP SDK-based servers without code changes.
---

## Getting Started: .NET Quickstart
The MCP extension quickstarts cover C# (.NET), Python, TypeScript (Node.js), with a Java QuickStart coming soon.
Here's the skeleton of a .NET MCP server running on Azure Functions:

```csharp
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;
using Microsoft.ModelContextProtocol;

public class WeatherMcpFunction
{
    private readonly ILogger<WeatherMcpFunction> _logger;

    public WeatherMcpFunction(ILogger<WeatherMcpFunction> logger)
    {
        _logger = logger;
    }

    [Function("GetWeather")]
    public async Task<HttpResponseData> Run(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "mcp/tools/get-weather")] 
        HttpRequestData req)
    {
        // MCP protocol handles auth via OBO token
        // Your agent calls this securely with inherited identity
        var weather = await FetchWeatherAsync();
        
        var response = req.CreateResponse(System.Net.HttpStatusCode.OK);
        await response.WriteAsJsonAsync(new { temperature = weather.Temp, condition = weather.Condition });
        return response;
    }

    private async Task<(double Temp, string Condition)> FetchWeatherAsync()
    {
        // Call your internal weather service, database, etc.
        return (72.5, "Sunny");
    }
}
```

The MCP framework handles protocol negotiation; you just write normal Azure Functions logic.

---

## Deployment & Cost Considerations
Azure Functions offers multiple hosting plans tailored to different MCP server requirements. The Flex Consumption plan provides automatic scaling based on demand with a pay-per-execution billing model and scale-to-zero economics. When MCP tools sit idle, costs drop to zero while maintaining fast wake-up times. The Premium plan supports "always-ready" instances that remain pre-initialized, eliminating cold-start latency, which is critical for mission-critical tools where initialization delays can cause SSE connection timeouts and poor agent response times.
**For typical agentic workloads:**
- **Dev/test:** Flex Consumption (pay ~$0.20 per million executions)
- **Mission-critical:** Premium (predictable latency, no cold starts)

---

## Integration with Azure AI Foundry
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
This means your MCP server shows up automatically in the agent's tool registry once deployed.

---

## Watch Out: Known Limitations
Nested arrays and complex types must be serialized as comma-separated strings when integrating with Azure AI Foundry, and programmatic tool approval using require_approval="never" is necessary for production workflows since UI-based approvals don't persist in automated deployments.
Translation: if your MCP tool returns deeply nested JSON, flatten it. And always set approval programmatically in production.

---

## Why This Matters Now
If last year was about laying the infrastructure for AI, 2026 is when we begin to see whether the application layer can turn that investment into real value. As specialized models mature and oversight improves, AI systems are becoming more reliable in daily workflows.
MCP on Azure Functions is that bridge. You get:
- **Standardized tooling** (no more custom agent frameworks)
- **Enterprise security** (managed identity, no credential sprawl)
- **Cost efficiency** (pay only for what agents actually call)
- **Faster iteration** (deploy MCP servers like any other function)

If you're shipping agentic AI on Azure and .NET, this is your green light to move from POC to production.

---

## Further Reading

https://learn.microsoft.com/en-us/azure/azure-functions/
https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
https://techcrunch.com/2026/01/02/in-2026-ai-will-move-from-hype-to-pragmatism/
https://devblogs.microsoft.com/azure-sdk/azure-sdk-release-january-2026/
https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/what-is-trending-in-hugging-face-on-microsoft-foundry-feb-2-2026/4490602
https://venturebeat.com/technology/four-ai-research-trends-enterprise-teams-should-watch-in-2026