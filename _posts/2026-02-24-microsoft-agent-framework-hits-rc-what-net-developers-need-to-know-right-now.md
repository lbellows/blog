---
author: the.serf
date: 2026-02-24 06:56:10 -0500
layout: post
tags:
- agent
- .net
- care
- framework
- microsoft
- claude-sonnet-4-6
title: 'Microsoft Agent Framework Hits RC: What .NET Developers Need to Know Right
  Now'
---

# Microsoft Agent Framework Hits RC: What .NET Developers Need to Know Right Now

**Published:** February 24, 2026 | **Audience:** .NET & Azure engineers shipping AI features

---

## TL;DR
On February 19, 2026, Microsoft announced that the **Microsoft Agent Framework** has reached **Release Candidate status** for both .NET and Python. RC means the API surface is stable and all v1.0 features are complete.
If you are still on Semantic Kernel or AutoGen, now is the time to start your migration plan — the GA finish line is in sight.

---

## What Is the Microsoft Agent Framework, and Why Should You Care?
Microsoft Agent Framework is a comprehensive, open-source framework for building, orchestrating, and deploying AI agents. It is the successor to Semantic Kernel and AutoGen, and it provides a unified programming model across .NET and Python.
Think of it as the "one framework to rule them all" moment Microsoft has been building toward for the past year. Rather than choosing between Semantic Kernel's enterprise stability and AutoGen's orchestration flexibility,
Agent Framework combines AutoGen's simple agent abstractions with Semantic Kernel's enterprise features — session-based state management, type safety, middleware, and telemetry — and adds graph-based workflows for explicit multi-agent orchestration.
Semantic Kernel and AutoGen pioneered the concepts of AI agents and multi-agent orchestration. The Agent Framework is the direct successor, created by the same teams.
So don't expect a total rewrite of your mental model — expect a cleaner, more opinionated surface built on the shoulders of what came before.

---

## The Feature Set Engineers Actually Care About

### 1. Multi-Provider Model Support (No Vendor Lock-In)
Multi-provider support means it works with Microsoft Foundry, Azure OpenAI, OpenAI, GitHub Copilot, Anthropic Claude, AWS Bedrock, Ollama, and more.
In practical terms: you can swap model backends without rewriting your agent logic. Your CI/CD pipeline can also point at a local Ollama instance to avoid burning budget on API calls during automated tests.

### 2. Interoperability Standards
Agent Framework supports A2A (Agent-to-Agent), AG-UI, and MCP (Model Context Protocol) standards
— the emerging open protocols that let agents from different vendors talk to each other. If you've been watching the MCP hype train, this is where it plugs into your .NET stack.

### 3. Workflow Orchestration Patterns
Agent Framework ships with a workflow engine that lets you compose agents into orchestration patterns — sequential, concurrent, handoff, and group chat — all with streaming support built in.
That last point matters: streaming in multi-agent pipelines is notoriously tricky to wire up by hand.

### 4. Enterprise-Grade Observability
The `UseOpenTelemetry()` call ensures that all agent interactions are logged and can be observed through Application Insights or other monitoring tools.
No more flying blind with opaque LLM calls in production.

---

## Getting Started in .NET: From Zero to Agent in ~5 Lines

Install the core packages (still prerelease at RC, so `--prerelease` is required):

```bash
dotnet add package Azure.AI.OpenAI --prerelease
dotnet add package Azure.Identity
dotnet add package Microsoft.Agents.AI.OpenAI --prerelease
```
Wire up your first agent using `AzureOpenAIClient` with `AzureCliCredential`, call `.GetChatClient("gpt-4o-mini")`, then `.AsAIAgent()` with your system instructions. That's it — an agent that calls an LLM and returns a response.
```csharp
using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Agents.AI;

AIAgent agent = new AzureOpenAIClient(
        new Uri(Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")!),
        new AzureCliCredential())
    .GetChatClient("gpt-4o-mini")
    .AsAIAgent(instructions: "You are a friendly assistant. Keep your answers brief.");

Console.WriteLine(await agent.RunAsync("What is the capital of France?"));
```
From here you can add tools, multi-turn conversations, middleware, and workflows to build production applications.
### Adding a Second Agent and Wiring a Workflow

For multi-agent scenarios, add the workflows package:

```bash
dotnet add package Microsoft.Agents.AI.Workflows --prerelease
```
Agent Framework makes multi-agent orchestration as simple as connecting building blocks. You create a specialized editor agent and then connect agents in a workflow.
The DI registration looks like this:

```csharp
// In Program.cs / your composition root
builder.AddAIAgent("Writer", (sp, key) => {
    var chatClient = sp.GetRequiredService<IChatClient>();
    return new ChatClientAgent(chatClient, name: key,
        instructions: "Draft a compelling story based on the user's prompt.");
});

builder.AddAIAgent("Editor", (sp, key) => {
    var chatClient = sp.GetRequiredService<IChatClient>();
    return new ChatClientAgent(chatClient, name: key,
        instructions: "Improve the writer's draft: fix grammar, enhance the plot.");
});
```
Keyed service registration with `builder.AddAIAgent()` allows you to register multiple agents in the same application.
Dependency injection resolves them cleanly — no static singletons, no ambient state nightmares.

---

## Migrating from Semantic Kernel or AutoGen
Now is the time to move your Semantic Kernel project to Microsoft Agent Framework and give feedback before the final release.
Microsoft has published dedicated migration guides for both Semantic Kernel and AutoGen on the official docs site (links below). The teams caution that while conceptual parity is high, you should expect some class and namespace changes — don't assume a find-and-replace will be sufficient for anything beyond toy projects.

> **Pro tip:**
Foundry Local brings the Foundry developer experience offline, making it a great option for testing new models, testing new code without blowing through budget, and building CI/CD pipelines with minimal overhead.
Pair it with Agent Framework RC and your test suite doesn't need a live Azure subscription to run.

---

## Watch Out: AzureML SDK v1 EOL Is Coming

While you're modernizing your agent stack, don't forget:
the Azure Machine Learning SDK v1 reaches end of support on June 30, 2026. After that date, existing workflows may face security risks and breaking changes without active Microsoft support.
If any of your ML pipelines still use the v1 SDK, that migration clock is ticking.

---

## Practical Takeaways

| Decision point | Recommendation |
|---|---|
| **Still on Semantic Kernel?** | Start migration planning now; RC = stable API |
| **Still on AutoGen?** | Same — migration guide is published |
| **New greenfield agent project?** | Start directly on Agent Framework RC |
| **Multi-model strategy?** | Agent Framework supports Foundry, Azure OpenAI, Claude, Bedrock, Ollama |
| **Observability** | Wire up `UseOpenTelemetry()` on day one, not as an afterthought |
| **AzureML SDK v1** | Migrate to v2 before June 30, 2026 |

---

## Further Reading

- https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/
- https://devblogs.microsoft.com/semantic-kernel/migrate-your-semantic-kernel-and-autogen-projects-to-microsoft-agent-framework-release-candidate/
- https://learn.microsoft.com/en-us/agent-framework/overview/
- https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start
- https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/run-agent
- https://devblogs.microsoft.com/dotnet/introducing-microsoft-agent-framework-preview/
- https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-dec-2025-jan-2026/
- https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/