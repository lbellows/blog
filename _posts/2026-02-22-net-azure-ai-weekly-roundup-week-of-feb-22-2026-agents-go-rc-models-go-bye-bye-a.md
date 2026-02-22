---
author: the.serf
date: 2026-02-22 06:34:59 -0500
layout: post
tags:
- story
- ide
- microsoft
- .net
- agent
- claude-sonnet-4-6
title: '.NET & Azure AI Weekly Roundup: Week of Feb 22, 2026 — Agents Go RC, Models
  Go Bye-Bye, and Your IDE Leveled Up'
---

# .NET & Azure AI Weekly Roundup: Week of Feb 22, 2026 — Agents Go RC, Models Go Bye-Bye, and Your IDE Leveled Up

**TL;DR:** The Microsoft Agent Framework hit Release Candidate for .NET and Python this week — it's the official successor to Semantic Kernel and AutoGen, and GA is now within spitting distance. Meanwhile, model retirement deadlines are creeping up fast (eyes on that March 31 gpt-4o-mini Standard cutoff), Visual Studio 2026 shipped fresh IDE updates with built-in NuGet MCP support, and a global AI hackathon is live through mid-March. Busy week. Grab a coffee. Let's go.

---

## 🤖 Story 1: Microsoft Agent Framework Reaches Release Candidate

The biggest news for .NET AI developers this week dropped on February 19:
Microsoft Agent Framework hit Release Candidate status for both .NET and Python — a milestone that signals the API surface is stable and all v1.0 features are complete.
It's a comprehensive, open-source framework for building, orchestrating, and deploying AI agents — and the successor to both Semantic Kernel and AutoGen. The unified programming model supports simple agent creation, type-safe function tools, graph-based workflows (sequential, concurrent, handoff, group chat), multi-provider support (Foundry, Azure OpenAI, OpenAI, Anthropic Claude, AWS Bedrock, Ollama, and more), and interoperability via A2A, AG-UI, and MCP standards.
That's not just a framework — that's a whole Swiss Army knife. And importantly:
now is the time to move your Semantic Kernel project to Microsoft Agent Framework and give feedback before the final release.
Here's a minimal C# agent wired up to Azure OpenAI, straight from the docs:

```csharp
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using OpenAI;

var chatClient = new OpenAIClient(
    new BearerTokenPolicy(new AzureCliCredential(), "https://ai.azure.com/.default"),
    new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1")
    })
    .GetChatClient("gpt-4.1")
    .AsIChatClient();

ChatClientAgent writer = new(chatClient,
    "You are a concise copywriter. Provide a single, punchy marketing sentence.",
    "writer");
```
For more information, check out the documentation and examples on GitHub, and install the latest packages from NuGet (.NET) or PyPI (Python).
**Takeaway:** If you're still shipping Semantic Kernel or AutoGen, block time this sprint to evaluate the migration. RC means breakage risk is low; waiting for GA means you're always behind.

---

## ⚠️ Story 2: Model Retirement Deadlines — Don't Let Production Go 500

There's a pattern emerging in the Azure AI community that deserves a flashing warning sign: confusing OpenAI's ChatGPT retirement dates with Azure AI Foundry retirement dates. They are **not the same thing**.
The ChatGPT retirement date (Feb 13, 2026) and the Azure Foundry retirement date (Mar 31, 2026) are different timelines — and Azure Foundry is what matters for your production workload. The OpenAI announcement dated Feb 13, 2026 applies only to the ChatGPT UI experience.
That said, some Standard deployments of `gpt-4o-mini` in Azure AI Foundry **do** have a March 31, 2026 retirement date.
When a model is retired, it's no longer available for use, and Azure OpenAI deployments of a retired model always return error responses.
That's a hard HTTP error in production — not a graceful degradation. Not fun.
OpenAI (ChatGPT) and Azure AI Foundry operate on independent lifecycle policies. When OpenAI announces that a model is retired from ChatGPT or OpenAI-hosted APIs, that retirement does not automatically apply to Azure AI Foundry.
**How to stay sane:**
Set up Azure Service Health alerts for your subscription to receive automated notifications about service changes.
Then bookmark only one source of truth:

```
https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-retirements
```
Microsoft Learn documentation is the official and correct source for Azure OpenAI model expiration and retirement dates. The portal may show earlier or shifting dates, but the Learn page governs the true lifecycle schedule.
**Takeaway:** Audit your deployments today. Check the **Foundry portal → Model Catalog → Retirement date column** for each deployed model. Set Service Health alerts. Do not trust a random Google result from 2025.

---

## 🛠️ Story 3: Visual Studio 2026 — Your IDE Now Has an NuGet AI Sidekick
Visual Studio 2026 shipped its latest update on February 18, 2026.
Among the highlights relevant to .NET developers: a built-in NuGet MCP (Model Context Protocol) server.
The NuGet MCP server provides a way of updating packages with known vulnerabilities and can retrieve real-time information about packages for GitHub Copilot. It's built-in but must be enabled once to use its functionality.
To enable it:

```
1. Open the GitHub Copilot Chat window (sign in required).
2. Click the tools icon in the bottom toolbar → Tools menu.
3. Find the MCP server named "nuget" and check the box to enable it.
```

Also noteworthy:
agents in Visual Studio now go beyond a single general-purpose assistant — a set of curated preset agents tap into deep IDE capabilities including debugging, profiling, and testing, alongside a framework for building custom agents tailored to how your team works.
Visual Studio 2026 is fully compatible with your projects and extensions from Visual Studio 2022
— so no migration tax, just free upgrades.

---

## 🏗️ Story 4: Agentic Modernization — A Realistic Field Report

The Microsoft dev blog published a detailed (and admirably skeptical) look at using agentic AI for application modernization in early 2026. The key insight?
The agent acts less like an autonomous developer and more like a multiplier for experienced engineers — it accelerates repetitive work and explores alternatives, while humans decide which changes are acceptable. Skipping validation or trusting large automated changes too early almost always backfires.
Agentic AI is most useful when applied to
proposing small, reviewable refactorings behind stable contracts, assisting with framework, runtime, or language upgrades where the transformation pattern is known, and generating repetitive changes across many modules while preserving agreed-upon behavior.
**Takeaway:** Agents are a force multiplier, not a magic wand. Keep humans in the loop and gate every automated change behind a CI/CD test suite. Your future self will thank you.

---

## 🔬 Story 5: Maia 200 SDK — Microsoft's Custom Silicon Opens Up

For teams optimizing inference costs at scale:
Microsoft is inviting developers, AI startups, and academics to begin exploring early model and workload optimization with the new Maia 200 SDK, which includes a Triton Compiler and support for PyTorch.
Fabricated on TSMC's cutting-edge 3-nanometer process, each Maia 200 chip contains over 140 billion transistors and is tailored for large-scale AI workloads.
Maia 200 is deployed in the US Central datacenter region near Des Moines, Iowa, with US West 3 near Phoenix coming next.
This is more of a horizon item for most .NET/Azure teams — but if your org is negotiating PTU (provisioned throughput) contracts or building inference infrastructure, it's worth a look at the preview SDK.

---

## 📅 What's Coming Up

- **Microsoft Global AI Hackathon** —
running February 10 through March 15, 2026, focused on building production-ready AI using Microsoft's latest AI, agent, and dev tools.
There are prizes. Ship something.
- **Microsoft Agent Framework GA** — RC is here; GA is imminent. Start migrating from Semantic Kernel now.
- **Model retirement crunch** — gpt-4o-mini Standard deployments retiring March 31, 2026. Clock is ticking.

---

## Further Reading

- Microsoft Agent Framework Reaches Release Candidate: https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/
- Migrate from Semantic Kernel/AutoGen to Agent Framework RC: https://devblogs.microsoft.com/semantic-kernel/migrate-your-semantic-kernel-and-autogen-projects-to-microsoft-agent-framework-release-candidate/
- Azure OpenAI Model Retirements (source of truth): https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-retirements
- Visual Studio 2026 Release Notes: https://learn.microsoft.com/en-us/visualstudio/releases/2026/release-notes
- Visual Studio 2026 GA Blog Post: https://devblogs.microsoft.com/visualstudio/visual-studio-2026-is-here-faster-smarter-and-a-hit-with-early-adopters/
- The Realities of Application Modernization with Agentic AI (Early 2026): https://devblogs.microsoft.com/all-things-azure/the-realities-of-application-modernization-with-agentic-ai-early-2026/
- Maia 200: The AI Accelerator Built for Inference: https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/
- Generative AI with LLMs in C# in 2026 (.NET Blog): https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/
- Microsoft Agent Framework Overview (Learn docs): https://learn.microsoft.com/en-us/agent-framework/overview/