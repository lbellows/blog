---
author: the.serf
date: 2025-12-28 06:28:25 -0500
layout: post
tags:
- .net
- azure
- model
- agent
- agentic
- claude-haiku-4-5-20251001
title: 'AI for .NET & Azure Developers: Week of December 26–28, 2025'
---

# AI for .NET & Azure Developers: Week of December 26–28, 2025

**TL;DR**
OpenAI released GPT-5.2 (codenamed Garlic), claiming benchmark leadership in coding, math, and reasoning tasks
, while
Google launched Gemini 3 Flash as its fast, cheap default model
.
Azure now supports both Claude and GPT frontier models, giving developers model diversity
.
The Microsoft Agent Framework and MCP support ship with .NET 10, standardizing patterns for agentic workflows
. Cost and latency remain critical—plan your 2026 deployments accordingly.

---

## The Model Wars Heat Up
Google released a "reimagined" version of Gemini Deep Research based on Gemini 3 Pro
, and
developers can now embed Google's Deep Research tool into their own apps
. But the real headline came from OpenAI's corner:
GPT-5.2 Thinking edges out Gemini 3 on reasoning benchmarks including real-world software engineering tasks (SWE-Bench Pro)
.

For .NET engineers, this matters.
GPT-5.2 is better at creating spreadsheets, building presentations, writing code, perceiving images, understanding long context, using tools and linking complex, multi-step projects
—all core to agentic workflows you'll build in 2026.

**Pricing watch:**
Gemini 3 Flash costs $0.50 per 1M input tokens and $3.00 per 1M output tokens, slightly more than Gemini 2.5 Flash but outperforming it while being three times faster
. Meanwhile,
Gemini 3 Flash costs $0.50/1M input tokens vs. $1.25/1M for Gemini 2.5 Pro, and $3/1M output tokens vs. $10/1M for Gemini 2.5 Pro
. The economics are shifting fast—lock in your cost models now.

---

## Azure Gets Model Diversity (Finally)

The headline from Microsoft Ignite is landing now:
Developers wanted access to Claude Sonnet and Claude Opus alongside OpenAI's GPT models, and now Azure is the only cloud supporting access to both Claude and GPT frontier models
. This is huge for avoiding vendor lock-in.
Foundry IQ streamlines knowledge retrieval from multiple sources including SharePoint, Fabric, and the web, powered by Azure AI Search, delivering policy-aware retrieval without custom RAG pipelines, with pre-configured knowledge bases and agentic retrieval in a single API
. If you're building RAG-heavy applications, this cuts weeks off your integration work.

**For PostgreSQL shops:**
Azure HorizonDB (in preview) includes built-in vector indexing with DiskANN, bringing AI intelligence directly to where your data lives, helping developers build semantic search and RAG patterns without separate vector stores
.

---

## .NET 10 & the Agent Framework: Your 2026 Toolkit
AI-focused capabilities expand through the Microsoft Agent Framework, Microsoft.Extensions.AI, and first-class Model Context Protocol (MCP) support, aiming to standardize patterns for building agentic workflows while maintaining consistency with existing .NET development practices
.
Microsoft Agent Framework enables developers to build AI agents with minimal code requirements, with examples showing functional agents created in fewer than twenty lines of code
. Here's a minimal example to get started:

```csharp
// Install: dotnet add package Microsoft.Extensions.AI
using Microsoft.Extensions.AI;

var client = new ChatClientBuilder()
    .UseOpenAI("gpt-5.2")
    .Build();

var response = await client.CompleteAsync("Write a .NET 10 agent that validates pull requests");
Console.WriteLine(response.Message.Text);
```
The framework enables Model Context Protocol (MCP) support, Agent-to-Agent (A2A) communication, and OpenAPI-based integration, ensuring portability across different runtime environments
.

---

## Agentic Workflows & Persistent Context
Amazon announced a new class of AI systems, "frontier agents," that can work autonomously for hours, even days, without human intervention, representing one of the most ambitious attempts yet to automate the full software development lifecycle
. While AWS-specific, this sets the bar for what .NET developers should expect from their tooling.
These frontier agents maintain persistent memory across sessions and continuously learn from an organization's codebase, documentation and team communications, independently determining which code repositories require changes and working on multiple files simultaneously
.

**Practical takeaway:** If you're building agents on Azure or .NET, plan for stateful, long-running workflows. Stateless chat completions are yesterday's pattern.

---

## Cost Tracking & Governance
Dev Proxy's new OpenAITelemetryPlugin gives visibility into how your apps interact with OpenAI or Azure OpenAI endpoints, intercepting LLM requests and tracking each request
. Before shipping any AI feature to production, use this to understand your token burn.
AI Gateway in Azure API Management now offers general availability of LLM policies (llm-token-limit, llm-emit-metric, llm-content-safety, and semantic caching), applicable not only to Azure AI Foundry models but also to OpenAI-compatible models and third-party inference providers
.

---

## What's Next: 2026 Readiness Checklist

1. **Audit your model choices.**
80% of new developers on GitHub in 2025 used Copilot within their first week, signaling that developers are getting their first contact with AI at the beginning of their journey
. Your team likely is too. Decide: GPT-5.2, Gemini 3 Flash, or Claude Opus?

2. **Upgrade to .NET 10 for Agent Framework support.**
Aspire (formerly .NET Aspire) ships with .NET 10 as a cloud-native application framework, strengthening orchestration for front ends, APIs, containers, and data stores
.

3. **Plan for cost optimization.**
With Context Caching, enterprises processing massive static datasets can see a 90% reduction in costs for repeated queries, and when combined with the Batch API's 50% discount, total cost of ownership for an agent drops significantly
.

4. **Invest in verification, not just delegation.**
The developers who have gone furthest with AI describe their role less as "code producer" and more as "creative director of code," where the core skill is not implementation, but orchestration and verification
.

---

## Further Reading

- https://github.blog/news-insights/octoverse/the-new-identity-of-a-developer-what-changes-and-what-doesnt-in-the-ai-era/
- https://azure.microsoft.com/en-us/blog/actioning-agentic-ai-5-ways-to-build-with-news-from-microsoft-ignite-2025/
- https://techcrunch.com/2025/12/11/openai-fires-back-at-google-with-gpt-5-2-after-code-red-memo/
- https://techcrunch.com/2025/12/17/google-launches-gemini-3-flash-makes-it-the-default-model-in-the-gemini-app/
- https://www.infoq.com/news/2025/11/dotnet-10-release/