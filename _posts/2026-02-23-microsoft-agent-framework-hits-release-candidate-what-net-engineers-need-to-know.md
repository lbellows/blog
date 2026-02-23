---
author: the.serf
date: 2026-02-23 06:54:29 -0500
layout: post
tags:
- .net
- agent
- framework
- microsoft
- now
- claude-sonnet-4-6
title: 'Microsoft Agent Framework Hits Release Candidate: What .NET Engineers Need
  to Know Right Now'
---

# Microsoft Agent Framework Hits Release Candidate: What .NET Engineers Need to Know Right Now

**Published:** February 23, 2026

---

## TL;DR
On February 19, 2026, Microsoft announced that the **Microsoft Agent Framework (MAF)** has reached **Release Candidate status for both .NET and Python**. RC means the API surface is stable and all features intended for the v1.0 GA release are complete.
If you're shipping AI features on .NET today — and especially if you've been building on Semantic Kernel or AutoGen — it's time to sit up and pay attention.

---

## What *Is* Microsoft Agent Framework?
Microsoft Agent Framework is a comprehensive, open-source framework for building, orchestrating, and deploying AI agents. It's the **successor to both Semantic Kernel and AutoGen**, providing a unified programming model across .NET and Python.
That's not a minor footnote. If your team has Semantic Kernel code in production,
now is the time to move your Semantic Kernel project to Microsoft Agent Framework and give the team feedback before the final release.
Consider this your migration runway.
MAF is a comprehensive, open-source framework that provides: simple agent creation (a working agent in just a few lines of code), function tools with type-safe tool definitions, graph-based workflows with sequential/concurrent/handoff/group-chat patterns, multi-provider support (Microsoft Foundry, Azure OpenAI, OpenAI, GitHub Copilot, Anthropic Claude, AWS Bedrock, Ollama, and more), and interoperability with A2A, AG-UI, and MCP (Model Context Protocol) standards.
That multi-provider story is genuinely useful: you're not locked into a single model vendor at the framework level, which should make your procurement conversations marginally less painful.

---

## Why This Matters for .NET Engineers

### 1. The API Surface Is Now Stable

RC status is a meaningful signal.
Release Candidate means the API surface is stable, and all features intended to ship with version 1.0 are complete.
You can start writing production code against these APIs without worrying that a rename or a method signature change will blow up your build next week. (Looking at you, `*AgentTool` → `*Tool` rename wave from beta.)

### 2. Enterprise-Grade Ops Are Built In

One of the biggest complaints about earlier agent frameworks was the gap between a slick local demo and a production-worthy deployment.
MAF addresses this with rapid prototyping (build and test agentic workflows locally, then deploy seamlessly to production — no complex containerization), cross-cloud flexibility (connectors for Azure, AWS, and GCP), and enterprise-grade features including built-in observability, identity, governance, and autoscaling.
No more duct-taping Prometheus exporters onto a LangChain script at 2 AM before a production launch. Probably.

### 3. Workflow Composition That Actually Scales
Single agents are powerful, but real-world applications often need multiple agents working together. Agent Framework ships with a workflow engine that lets you compose agents into orchestration patterns — sequential, concurrent, handoff, and group chat — all with streaming support built in.
---

## Getting Started: .NET Quickstart

Install the NuGet package and wire up a minimal agent against Azure OpenAI. The RC packages are available on NuGet today:

```bash
dotnet add package Microsoft.Agents.AI
dotnet add package Microsoft.Agents.AI.Workflows
```

Here's the skeleton for a sequential two-agent workflow in C# — a copywriter and a reviewer — straight from the official RC announcement:

```csharp
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Workflows;
using Microsoft.Extensions.AI;
using OpenAI;

// Replace <resource> and gpt-4.1 with your Azure OpenAI resource and deployment name
var chatClient = new OpenAIClient(
    new BearerTokenPolicy(new AzureCliCredential(), "https://ai.azure.com/.default"),
    new OpenAIClientOptions { Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1") })
    .GetChatClient("gpt-4.1")
    .AsIChatClient();

ChatClientAgent writer   = new(chatClient, "You are a concise copywriter. "
    + "Provide a single, punchy marketing sentence.", "writer");
ChatClientAgent reviewer = new(chatClient, "You are a thoughtful reviewer. "
    + "Critique the sentence and suggest one improvement.", "reviewer");

// Compose into a sequential workflow, then run it...
```
For full documentation and examples, check out the GitHub repo and install the latest packages from NuGet (.NET) or PyPI (Python).
> **Auth tip:** The snippet above uses `AzureCliCredential` for local dev. In production, swap in `ManagedIdentityCredential` and avoid storing secrets in environment variables like it's 2014.

---

## Visual Studio 2026 Gets Smarter Agents, Too

While you're updating your project files, it's worth knowing that the IDE itself is leveling up.
Agents in Visual Studio now go beyond a single general-purpose assistant. Microsoft is shipping a set of curated preset agents that tap into deep IDE capabilities — debugging, profiling, and testing — alongside a framework for building your own custom agents tailored to how your team works.
---

## The Deadline You Can't Ignore: AzureML SDK v1 EOL

Don't let the shiny agent news bury this:
the Azure Machine Learning SDK v1 reaches end of support on **June 30, 2026**. After that date, existing workflows may face security risks and breaking changes without active Microsoft support.
Note that the AzureML CLI v1 extension already reached end of support on September 30, 2025.
If you're still running v1-based training pipelines, the SDK v2 migration guide is the place to start — v2 brings a significantly improved authoring experience, YAML-first job definitions, and continued investment from the Azure ML team.
You have roughly four months. That sounds like a lot until sprint planning starts.

---

## Practical Takeaways

| Action | Priority | Why |
|---|---|---|
| Evaluate MAF RC in your next sprint | 🔴 High | API surface is stable; low-risk time to adopt |
| Start migrating Semantic Kernel / AutoGen code | 🔴 High | MAF is the official successor |
| Migrate AzureML SDK v1 pipelines to v2 | 🔴 High | EOL June 30, 2026 |
| Explore multi-provider support in MAF | 🟡 Medium | Reduces model vendor lock-in |
| Check out VS 2026's preset IDE agents | 🟢 Low | Productivity win, but not blocking |

---

## Further Reading

- https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/
- https://devblogs.microsoft.com/semantic-kernel/migrate-your-semantic-kernel-and-autogen-projects-to-microsoft-agent-framework-release-candidate/
- https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-dec-2025-jan-2026/
- https://learn.microsoft.com/en-us/agent-framework/overview/
- https://learn.microsoft.com/en-us/visualstudio/releases/2026/release-notes
- https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/
- https://devblogs.microsoft.com/azure-sdk/azure-sdk-release-january-2026/