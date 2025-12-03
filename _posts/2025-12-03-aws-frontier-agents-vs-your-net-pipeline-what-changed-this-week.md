---
author: the.serf
date: 2025-12-03 06:30:42 -0500
layout: post
tags:
- .net
- frontier
- agent
- agents
- aws
- claude-haiku-4-5-20251001
title: 'AWS Frontier Agents vs. Your .NET Pipeline: What Changed This Week'
---

# AWS Frontier Agents vs. Your .NET Pipeline: What Changed This Week

**TL;DR:**
AWS announced frontier agents designed to work for hours and days, tackling complex challenges without intervention
. For .NET and Azure engineers, this raises a critical question: how do you keep your agent investments portable and cost-effective when cloud vendors are racing to lock in long-running agentic workloads?

## The Frontier Agent Moment
Frontier agents differ from existing AI coding assistants like CodeWhisperer in that current AI coding tools require engineers to drive every interaction
.
These new agents are fundamentally designed to work for hours and days, not finishing in the next five minutes—they tackle complex challenges that may require trying different solutions before reaching the right conclusion
.

AWS shipped three specialized agents: Kiro (software development), Security Agent, and DevOps Agent.
SmugMug deployed the security agent and caught a business logic bug that no existing tools would have caught, exposing information improperly—something that would have been invisible to other tools, but the agent could contextualize the information, parse the API response, and find the unexpected data
.

## Why This Matters for .NET Developers

If you're shipping on Azure with .NET, you already have agent tooling:
Microsoft announced the Microsoft Agent Framework, an open-source SDK designed to simplify AI agent creation, unifying capabilities from Semantic Kernel and AutoGen
.
The framework supports both Python and .NET environments through NuGet packages
.

But here's the tension:
All learnings accumulated by AWS agents are logged and visible, allowing engineers to understand what knowledge influences the agent's decisions, and teams can even remove specific learnings if they discover the agent has absorbed incorrect information
. That observability is powerful—but it's AWS-specific. Your .NET agent on Azure needs equivalent introspection.

## Practical Integration Path for .NET Engineers

If you're building long-running agents in .NET, consider this layered approach:

**1. Use Microsoft Agent Framework with explicit telemetry:**

```csharp
var agent = new Agent("MyLongRunningAgent")
    .WithModel(new AzureOpenAIClient(endpoint, credential))
    .WithTools(new[] { mySecurityTool, myDevOpsTool })
    .WithObservability(OpenTelemetryInstrumentation.Create());

// Run for extended duration with checkpoints
var result = await agent.RunAsync(userPrompt, maxDuration: TimeSpan.FromHours(4));
```
Microsoft Agent Framework includes native support for Azure AI Foundry services, OpenTelemetry instrumentation for monitoring, and compatibility with Visual Studio Code through the AI Toolkit extension
.

**2. Leverage Azure AI Foundry for knowledge management:**
New Microsoft Foundry updates in preview enable developers to enrich agents with real-time business context, multimodal capabilities, and custom business logic through a unified Tools catalog of Model Context Protocol (MCP) servers built with security and governance in mind
.

**3. Monitor agent reasoning like AWS does:**
Foundry Observability is now in preview, giving developers end-to-end monitoring, built-in metrics, and detailed trace logs of the reasoning steps and tool calls made by agents
.

## The Cost Equation
Model router in Azure AI Foundry allows developers to automatically select the optimal Azure OpenAI models for different prompts—boosting quality while reducing costs
. For long-running agents, this auto-routing is critical: a 4-hour reasoning task doesn't need GPT-4o pricing the whole time.

## One More Thing: Stay Portable
Microsoft Agent Framework enables Model Context Protocol (MCP) support, Agent-to-Agent (A2A) communication, and OpenAPI-based integration, ensuring portability across different runtime environments
. Use MCP servers for your custom tools. If AWS's frontier agents become irresistible later, you won't be rewriting your entire tool layer.

---

## Further reading

https://venturebeat.com/ai/amazons-new-ai-can-code-for-days-without-human-help-what-does-that-mean-for

https://www.infoq.com/news/2025/10/microsoft-agent-framework/

https://learn.microsoft.com/en-us/azure/ai-foundry/agents/whats-new

https://azure.microsoft.com/en-us/blog/all-the-azure-news-you-dont-want-to-miss-from-microsoft-build-2025/

https://techcommunity.microsoft.com/blog/Marketplace-Blog/ignite-2025-drive-the-next-era-of-software-innovation-with-ai/4470130

https://learn.microsoft.com/en-us/dotnet/ai/overview