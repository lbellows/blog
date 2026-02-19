---
author: the.serf
date: 2026-02-19 06:54:51 -0500
layout: post
tags:
- agent
- debugging
- development
- first-class
- .net
- claude-haiku-4-5-20251001
title: 'AI Toolkit for VS Code 0.30.0: Agents Are Now First-Class Citizens in .NET
  Development'
---

# AI Toolkit for VS Code 0.30.0: Agents Are Now First-Class Citizens in .NET Development

**TL;DR:**
Microsoft's AI Toolkit v0.30.0 adds a Tool Catalog, Agent Inspector, and first-class evaluation testing
, making agentic AI development feel less like experimental plumbing and more like shipping production software. If you're building .NET agents on Azure, this release bridges the gap between proof-of-concept and real deployments.

## The Problem: Agent Development Felt Like Debugging in the Dark

Until recently, building AI agents in .NET meant juggling multiple frameworks (Semantic Kernel, AutoGen, custom wiring) without proper observability.
For applications requiring agentic capabilities, multi-agent orchestration, or enterprise-grade observability and security, Microsoft Agent Framework is now the recommended approach
—but the tooling lagged behind.
Most agentic implementations assume Python or TypeScript, leaving .NET shops without native support
. Debugging a multi-step agent that calls tools, updates state, and handles failures required console logging and prayer.

## What's New: Three Game-Changers

### 1. **Tool Catalog with MCP Discovery**
New Microsoft Foundry updates enable developers to enrich agents with real-time business context through a unified Tools catalog of Model Context Protocol (MCP) servers, including unified tool discovery, deep business integration, and custom tool extensibility
.

In practice: Instead of manually wiring up your Azure SQL, SharePoint, or custom APIs as agent tools, the VS Code extension now surfaces available MCP servers. You can browse, test, and bind them without leaving the IDE.

```csharp
// Before: Manual tool registration
agent.AddTool(new SqlQueryTool(connectionString));
agent.AddTool(new SharePointSearchTool(tenantId));

// After: Discover and bind from catalog
var tools = await toolCatalog.DiscoverAsync("azure-*");
agent.BindTools(tools);
```

### 2. **Agent Inspector: Real-Time Debugging**
The end-to-end Agent Inspector enables production-ready debugging
of agent execution. You can now:

- Step through agent reasoning in real time
- Inspect tool invocations and their outputs
- Replay failed runs with different parameters
- Monitor token usage and latency per step

This is critical for cost control.
OpenAI's latest models achieve better performance with almost 400 times less cost and compute compared to models from a year ago
, but that efficiency only matters if you can measure and optimize your agent's behavior.

### 3. **Evaluations as First-Class Tests**
Treating evaluations as first-class tests
means you can now write assertions on agent behavior:

```csharp
[Test]
public async Task AgentCanRetrieveAndSummarizeData()
{
    var result = await agent.RunAsync("Summarize Q4 sales by region");
    
    Assert.That(result.Output, Does.Contain("region"));
    Assert.That(result.ToolCalls.Count, Is.LessThan(5)); // Cost control
    Assert.That(result.ExecutionTime, Is.LessThan(TimeSpan.FromSeconds(10)));
}
```

This shifts agents from "let's see what happens" to "let's verify correctness and performance."

## Integration with Azure AI Foundry
Managed instance on Azure App Service (in public preview) enables organizations to move .NET web applications to the cloud with minimal configuration changes, delivering faster app modernization with lower overhead and access to cloud-native scalability and Azure's AI capabilities
.

The toolkit now integrates directly with Azure AI Foundry's model deployment, so you can:

- Deploy agents as managed services on Azure Container Instances or App Service
- Use Azure OpenAI endpoints without additional authentication plumbing
- Monitor agent performance via Azure Monitor and Application Insights

## Practical Takeaway for Your Team

If you're shipping .NET agents on Azure, this release removes three major friction points:

1. **Tool integration** no longer requires custom adapters
2. **Debugging** is now interactive, not log-file archaeology
3. **Quality gates** are testable, not aspirational
With MCP reducing the friction of connecting agents to real systems, 2026 is likely to be the year agentic workflows finally move from demos into day-to-day practice
. This toolkit update is Microsoft's bet that .NET developers will lead that shift.

---

## Further Reading

- https://techcommunity.microsoft.com/blog/azuredevcommunityblog/%F0%9F%9A%80-ai-toolkit-for-vs-code-%E2%80%94-february-2026-update/4493673
- https://learn.microsoft.com/en-us/agent-framework/overview/
- https://devblogs.microsoft.com/foundry/dotnet-ai-skills-executor-azure-openai-mcp/
- https://learn.microsoft.com/en-us/dotnet/ai/dotnet-ai-ecosystem
- https://techcrunch.com/2026/01/02/in-2026-ai-will-move-from-hype-to-pragmatism/
- https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/february