---
author: the.serf
date: 2025-11-30 06:26:19 -0500
layout: post
tags:
- agents
- .net
- azure
- agent
- bigger
- claude-haiku-4-5-20251001
title: 'AI Weekly Roundup: From Agents to Agents—What .NET & Azure Developers Need
  to Know (Nov 28–30, 2025)'
---

# AI Weekly Roundup: From Agents to Agents—What .NET & Azure Developers Need to Know (Nov 28–30, 2025)

**TL;DR**
Microsoft announced the general availability of .NET 10, described as the most productive, modern, secure, and high-performance version of the platform to date.
AI-focused capabilities expand through the Microsoft Agent Framework, Microsoft.Extensions.AI, and first-class Model Context Protocol (MCP) support, aiming to standardize patterns for building agentic workflows, integrating external tools, enabling telemetry, and working across multiple AI providers.
Meanwhile,
enterprises are deploying AI agents in customer-facing applications, and the trend is accelerating at a breakneck pace.
Pricing wars continue:
OpenAI CEO Sam Altman confirmed an 80% price drop for o3, writing "we dropped the price of o3 by 80%!! excited to see what people will do with it now."
---

## The .NET 10 Moment: Agents Are Now First-Class Citizens
Aspire 13 ships with .NET 10 as a cloud-native application framework with a new name, just "Aspire," strengthening orchestration for front ends, APIs, containers, and data stores, with improvements in development workflows, deployment performance, and multi-language integration, adding simplified templates, new resource types, enhanced security options, and dashboard improvements, along with expanded support for coordinating Python, JavaScript, and other non-.NET services from a unified AppHost.
**What this means for you:**  
If you've been hesitant about building agentic workflows in .NET, now's the time to move.
Microsoft Agent Framework enables developers to build AI agents with minimal code requirements, with examples showing functional agents created in fewer than twenty lines of code.
The framework enables Model Context Protocol (MCP) support, Agent-to-Agent (A2A) communication, and OpenAPI-based integration, ensuring portability across different runtime environments, and includes advanced orchestration patterns from AutoGen, such as group chat, debate, and reflection capabilities, now delivered with enterprise-grade reliability.
**Quick start snippet:**
```csharp
// Microsoft Agent Framework + .NET 10
// Agents with < 20 lines of code
var agent = new AgentBuilder()
    .WithModel("gpt-4o")
    .WithTools(new[] { calculator, webSearch })
    .WithOrchestration(OrchestrationPattern.Sequential)
    .Build();

var response = await agent.RunAsync("What's 2+2 and the weather in Seattle?");
```

---

## Azure's Agent Explosion: Control Planes & Multi-Model Strategies
The new Foundry Control Plane gives teams real-time security, lifecycle management, and visibility across agent platforms, integrating signals from the entire Microsoft Cloud, including Agent 365 and the Microsoft security suite, so builders can optimize performance, apply agent controls, and maintain compliance.
Claude Sonnet 4.5, Opus 4.1, and Haiku 4.5 are now part of Microsoft Foundry, advancing the mission to give customers choice across the industry's leading frontier models—and making Azure the only cloud offering both OpenAI and Anthropic models, underscoring commitment to an open, interoperable Microsoft AI ecosystem.
**Why it matters:**
A consistent theme is the move towards a multi-model and multi-cloud strategy, with enterprises wanting the flexibility to choose the best tool for the job, whether it's a powerful proprietary model or a fine-tuned open-source alternative.
Azure's multi-model posture now gives you that flexibility without vendor lock-in.

**Cost & latency watch:**
Batch API language models are now available in the Batch API for global deployments and three regions, returning completions within 24 hours for a 50% discount on Global Standard Pricing.
If you're not on a tight SLA, batch processing can cut your inference costs dramatically.

---

## The RAG Commodity Shift & SQL Server 2025
Retrieval Augmented Generation (RAG) has become a commodity lately with increasing adoption of RAG based solutions in enterprise applications.
Azure Content Understanding in Foundry Tools is now Generally Available with API version 2025-11-01, bringing production readiness plus customer-driven enhancements across model choice, management, and security.
SQL Server 2025 is now available, helping developers build modern, AI-powered apps using familiar T-SQL—securely and at scale, with built-in tools for advanced search, near real-time insights via OneLake, and simplified data handling, so businesses can unlock more value from the data they already have.
**Integration example:**
```csharp
// SQL Server 2025 + Vector Search + .NET
using var connection = new SqlConnection(connectionString);
var vectorQuery = @"
    SELECT TOP 5 [id], [content], [embedding]
    FROM [documents]
    ORDER BY VECTOR_DISTANCE([embedding], @query_vector)
";
// Native vector support—no external DBs needed
```

---

## Language Trends: Why TypeScript & Typed Languages Are Winning
In 2025, TypeScript overtook both JavaScript and Python as the most-used language on GitHub—a 66% year-over-year surge and the biggest language movement in more than a decade.
Increasingly, what feels "easier" is tied to how well AI tools will support work with that language, with statically typed languages giving guardrails—if an AI tool is going to generate code, developers want a fast way to know whether that code is correct, and explicit types give that safety net, reducing hallucination surface area.
**Implication for .NET devs:**  
C# and F# are already typed and strongly stateful—you're already in the sweet spot for AI-assisted development.
C# 14 introduces field-backed properties, new span conversions, the null-conditional assignment operator, collection expression extensions, partial constructors, and ref struct interface support, with Microsoft emphasizing cleaner and more maintainable code.
---

## 2026 Readiness Checklist

1. **Migrate to .NET 10 & Aspire 13** (if not already done). The agent framework is production-ready.
2. **Evaluate multi-model strategies.** Don't lock into one LLM provider. Use Azure's model router or API gateways to abstract the choice.
3. **Plan for cost governance.**
Dev Proxy v0.28 introduces a new ability to help understand language models' usage and costs in applications, with the new Dev Proxy OpenAITelemetryPlugin giving visibility into how apps interact with OpenAI or Azure OpenAI endpoints, intercepting LLM requests and tracking each request.
4. **Invest in RAG infrastructure.**
Retrieval-augmented generation (RAG) pipelines enable users to interactively engage with large amounts of data that continuously evolves, yet enterprises face real challenges in making them work at scale—handling both structured and unstructured data, processing massive volumes efficiently, and ensuring privacy and security.
SQL Server 2025 + Azure AI Search are your answer.
5. **Security first.**
The new Foundry Control Plane gives teams real-time security, lifecycle management, and visibility across agent platforms.
Use it.

---

## The Bigger Picture: Agents Are No Longer Experimental
A shift is occurring from AI being an assistant to AI being a co-creator of the software—we're not just writing code faster, we're entering a phase where the entire application can be developed, tested and shipped with the AI as part of the development team.
This isn't hyperbole anymore.