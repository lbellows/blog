---
author: the.serf
date: 2026-03-03 06:47:19 -0500
layout: post
tags:
- .net
- agent
- azure
- candidate
- framework
- claude-sonnet-4-6
title: 'Microsoft Agent Framework Hits Release Candidate: What .NET Engineers Need
  to Know Right Now'
---

# Microsoft Agent Framework Hits Release Candidate: What .NET Engineers Need to Know Right Now

**March 3, 2026 · ~800 words**

---

## TL;DR
Microsoft has announced that the Microsoft Agent Framework has reached Release Candidate status for both .NET and Python.
This is the clearest signal yet that the fragmented era of stitching together Semantic Kernel plugins and AutoGen experiments is over. If you are shipping agentic AI on Azure today, this RC is the migration target. Here is what the milestone means, why it matters, and how to get started without breaking your sprint.

---

## What Even *Is* the Microsoft Agent Framework?

Think of it as the "we finally listened" SDK.
Microsoft Agent Framework is an open-source SDK and runtime for building, deploying, and managing multi-agent AI systems. It combines the enterprise-ready stability of Semantic Kernel with the innovative orchestration patterns from AutoGen, creating a unified foundation for both experimentation and production.
Before this moment, life was messy.
Developers experimenting with Microsoft's agent technologies had to piece together capabilities using Semantic Kernel or experimental multi-agent orchestrators. Those tools provided early building blocks for agent creation and function invocation, but lacked a stable, unified API suitable for enterprise-grade systems.
In other words: you were basically duct-taping a jet engine to a skateboard and calling it production-ready.

---

## Why "Release Candidate" Is a Big Deal
Microsoft Agent Framework has reached Release Candidate status for both .NET and Python. Release Candidate is an important milestone on the road to General Availability — it means the API surface is stable, and all features that we intend to release with version 1.0 are complete.
Practically speaking:
with this RC release, the framework's APIs and workflows are locked down, allowing teams to start production evaluation and implementation with greater confidence.
That said, RC ≠ GA. Keep your eyes open:
as a release candidate, the packages are still flagged as pre-release on NuGet and PyPI, and the framework is evolving rapidly based on early feedback. Full GA documentation and migration guides are being prepared, including guidance for teams migrating from Semantic Kernel or from AutoGen. While the RC status signals stability, developers should plan to stay current with updates until GA, and be prepared for minor breaking changes if needed.
---

## Key Engineering Capabilities
The framework succeeds earlier efforts such as Semantic Kernel and AutoGen, consolidating agent creation, orchestration primitives, and multi-provider support under a single SDK. It supports common patterns for creating autonomous agents as well as workflows that combine multiple agents, and it integrates with a variety of AI model providers.
On the enterprise side,
current agent frameworks are fragmented and lack enterprise features like observability, compliance, and durability. Microsoft Agent Framework addresses these gaps by providing security, governance, and scalability for agentic AI applications.
And for the "I just want to ship" crowd:
the framework emphasizes simplicity and flexibility. Developers can create a basic AI agent in just a handful of lines in either Python or .NET, using client libraries to connect to various model providers.
---

## Getting Started in .NET

Install the RC package (remember: it's marked pre-release, so you need the `--prerelease` flag):

```bash
dotnet add package Microsoft.AgentFramework --prerelease
```

A minimal single-agent scaffold in C# looks roughly like this pattern from the official docs:

```csharp
using Microsoft.AgentFramework;

var agent = AgentBuilder.Create()
    .WithChatCompletion(client)        // IChatClient from Microsoft.Extensions.AI
    .WithTool(MyCustomTool.Instance)   // plug in your domain logic
    .Build();

var response = await agent.InvokeAsync("Summarize the latest support tickets.");
Console.WriteLine(response.Message);
```

> ⚠️ Exact API signatures are subject to minor change before GA. Pin your package version in CI and monitor the GitHub Discussions feed for breaking-change notices.
For practitioners ready to explore the Agent Framework now, Microsoft has published examples and getting-started guides on the official documentation site, along with source code and migration aids on GitHub.
---

## Deploying to Azure: Hosted Agents in Foundry

Writing agent code locally is the easy part. Shipping it is where things historically got spicy (read: containerization nightmares). The good news:
developers can now deploy custom-code agents built with Microsoft Agent Framework directly into a fully managed runtime — no container images, Kubernetes clusters, or deployment pipelines required. This eliminates containerization or infrastructure setup so developers can focus on agent logic, while Foundry provides enterprise-grade identity, observability, governance, and autoscaling.
Together, Agent Framework and Hosted Agents give teams a clear path from local prototypes to secure, production-grade deployments with transparent consumption-based pricing.
(Yes, pay-as-you-go. Your finance team will ask you to repeat that.)

---

## Migrating From Semantic Kernel

If you have existing SK-based agent code, Microsoft has published a dedicated migration guide (link below). The headline advice from the Semantic Kernel blog:
Microsoft Agent Framework has reached Release Candidate for .NET and Python. The API surface is stable, v1.0 features are complete, and now's the time to migrate from Semantic Kernel and share feedback before GA.
Translation: the window to shape the final API is open right now. File issues, submit feedback, and help ensure GA ships in a state that matches your real-world workloads.

---

## Practical Takeaways

| Concern | Guidance |
|---|---|
| **API stability** | RC APIs are locked; minor breaking changes still possible before GA |
| **NuGet install** | Requires `--prerelease` flag; pin exact version in CI |
| **Hosting** | Foundry Hosted Agents: no Kubernetes required, consumption pricing |
| **Migration** | Official SK → Agent Framework migration guide is live on Microsoft Learn |
| **Model support** | Works with Azure OpenAI, GitHub Models, and other IChatClient-compatible providers |
| **Observability** | Built-in telemetry via Foundry; plug into Application Insights as needed |

---

## One More Thing: Azure AI Connect (This Week!)

If you want to go deeper live,
Azure AI Connect isn't just another virtual conference — it's a 5-day deep-dive immersion into the connective tissue of artificial intelligence on the cloud, bringing together developers, data scientists, and enterprise leaders to explore the full spectrum of Azure AI services.
It runs March 2–6, 2026, and
features direct insights from Microsoft MVPs and product teams, plus code-driven sessions, practical workshops, and live Q&As.
Attendance is virtual and worth bookmarking.

---

## Further Reading

- **Microsoft Agent Framework RC announcement (Foundry Blog):**
  https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/

- **InfoQ deep-dive — Agent Framework RC for .NET and Python:**
  https://www.infoq.com/news/2026/02/ms-agent-framework-rc/

- **Semantic Kernel migration guide to Agent Framework RC:**
  https://devblogs.microsoft.com/semantic-kernel/migrate-your-semantic-kernel-and-autogen-projects-to-microsoft-agent-framework-release-candidate/

- **Agent Framework RC Migration Guide (Microsoft Learn):**
  https://learn.microsoft.com/en-us/semantic-kernel/support/migration/agent-framework-rc-migration-guide

- **What's New in Microsoft Foundry — Dec 2025 & Jan 2026 (Hosted Agents, MCP, A2A):**
  https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-dec-2025-jan-2026/

- **Generative AI with LLMs in .NET and C# in 2026 (.NET Blog):**
  https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/

- **Azure AI Connect — March 2–6, 2026 (virtual event):**
  https://techcommunity.microsoft.com/event/43624d95-1cb4-43ab-8b6e-e67b78fe8b98/azure-ai-connect---march-2-to-march-6-2026/4491662