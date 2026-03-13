---
author: the.serf
date: 2026-03-13 07:46:45 -0400
layout: post
tags:
- foundry
- .net
- gpt-5.4
- azure
- model
- claude-sonnet-4-6
title: GPT-5.4 Is GA in Microsoft Foundry — and the .NET SDK Is Right Behind It
---

# GPT-5.4 Is GA in Microsoft Foundry — and the .NET SDK Is Right Behind It

**Published:** March 13, 2026 | **Tags:** Azure, .NET, AI Foundry, GPT-5.4, Agentic AI

---

## TL;DR

OpenAI's GPT-5.4 is now generally available in Microsoft Foundry, bringing production-grade agentic reasoning, a 1 million-token context window, and a new **Tool Search** system to your Azure-hosted workloads. The Foundry REST API (`/openai/v1/`) has also hit GA — meaning the contract is locked and the .NET `2.0.0-beta.1` SDK is now a reliable target for production evaluation. If you're still pointing at `gpt-4o-mini`, you also have a hard deadline: **March 31, 2026**. Time to move.

---

## The Story: GPT-5.4 Lands in Foundry, and It's Not Just a Bigger Number

The model carousel has been spinning fast, but this week's drop is worth a full stop.
Microsoft announced that OpenAI's GPT-5.4 is now generally available in Microsoft Foundry — described as a model designed to help organizations move from planning work to reliably completing it in production environments.
That framing is deliberate.
As AI agents are applied to longer, more complex workflows, consistency and follow-through become as important as raw intelligence. GPT-5.4 combines stronger reasoning with built-in computer use capabilities to support automation scenarios and dependable execution across tools, files, and multi-step workflows at scale.
In other words: the pitch isn't "smarter chatbot." It's "autonomous agent that actually finishes the job."

### What's New Under the Hood?
In addition to a standard version, GPT-5.4 is available as a reasoning model (GPT-5.4 Thinking) or optimized for high performance (GPT-5.4 Pro). The API version supports context windows as large as 1 million tokens — by far the largest context window available from OpenAI — and OpenAI emphasized improved token efficiency, saying GPT-5.4 was able to solve the same problems with significantly fewer tokens than its predecessor.
On the reliability front, the numbers are concrete:
the new model is 33% less likely to make errors in individual claims compared to GPT-5.2, and overall responses are 18% less likely to contain errors.
For production agentic pipelines where hallucinated tool arguments silently corrupt a workflow, that's not a footnote — it's load-bearing.

There's also a new API primitive worth knowing about:
as part of the launch, OpenAI reworked how the API version of GPT-5.4 manages tool calling, introducing a new system called **Tool Search**.
(Keep an eye on the docs as this stabilizes — it may change how you register tools in your agent host.)

GPT-5.4 is also already flowing into your IDE:
GPT-5.4, OpenAI's latest agentic coding model, is now rolling out in GitHub Copilot, showing enhanced logical reasoning and task execution for intricate, multi-step, tool-dependent processes. It will be available to Copilot Pro, Pro+, Business, and Enterprise users.
> **Practical aside:** If you're a Copilot Business or Enterprise admin, note that
Copilot Enterprise and Copilot Business plan administrators must enable the GPT-5.4 policy in Copilot settings
before users can select it. It won't just appear — go flip that switch.

---

## The Infrastructure Story: Foundry REST API Is GA, .NET SDK Is Beta-but-Stable

The model news doesn't land in a vacuum. The bigger structural shift is that
the Foundry REST API is now generally available. The core endpoints — chat completions, responses, embeddings, files, fine-tuning, models, and vector stores — are production-ready and carry GA SLAs.
Why does this matter for .NET developers specifically? Because
the .NET SDK shipped a new beta (`2.0.0-beta.1`) targeting the GA REST surface, with significant breaking changes including tool class renames, credential updates, and preview feature opt-in flags.
The version numbering can trip you up, so here's the clarification directly from the Foundry team:
the `v1` in paths like `/openai/v1/responses` is the OpenAI route prefix, not a Foundry version number. The Foundry SDK packages use their own `2.x` version scheme (e.g., `azure-ai-projects 2.0.0b4`). Both target the same GA endpoints.
And the strategic intent is clear:
March is shaping up to be a big one — SDK GA announcements are on the horizon, and the Foundry SDK will be the single package you need across agents, inference, evaluations, and memory. Get ahead of it now by upgrading to the latest pre-release and targeting the GA REST surface.
### Quick-Start: Deploy GPT-5.4 via Azure CLI

```bash
# Create a GPT-5.4 deployment in your Foundry project
az cognitiveservices account deployment create \
  --name "my-foundry-resource" \
  --resource-group "my-rg" \
  --deployment-name "gpt-5-4-prod" \
  --model-name "gpt-5.4" \
  --model-version "1" \
  --model-format "OpenAI" \
  --sku-capacity 10 \
  --sku-name "GlobalStandard"
```

### Quick-Start: Call the Model from .NET (2.0.0-beta.1)

```csharp
using Azure.AI.Projects; // azure-ai-projects 2.0.0-beta.1
using Azure.Identity;

var client = new AIProjectClient(
    new Uri("https://<your-resource>.services.ai.azure.com/api"),
    new DefaultAzureCredential());

var chatClient = client.GetChatCompletionsClient();

var response = await chatClient.CompleteAsync(
    deploymentName: "gpt-5-4-prod",
    messages: [
        new ChatMessage(ChatRole.User, "Summarize our Q1 pipeline and suggest next steps.")
    ]);

Console.WriteLine(response.Value.Choices[0].Message.Content);
```

> ⚠️ **Breaking change heads-up:** The `2.0.0-beta.1` SDK renamed several tool classes and updated how credentials are passed. If you're migrating from the `1.x` package, consult the [migration guide on GitHub](https://github.com/Azure/azure-sdk-for-net) before deploying to prod.

---

## Urgent: gpt-4o-mini Retires on Azure Foundry — March 31, 2026

If GPT-5.4 is the carrot, here's the stick:
the `gpt-4o-mini` model is set to retire from Azure Foundry as well. According to available information, it has a retirement date of **March 31, 2026** — you will need to switch to a different model before this date to avoid any disruption in your production environment.
Don't let OpenAI's own blog posts confuse you here.
OpenAI (ChatGPT) and Azure AI Foundry operate on independent lifecycle policies. When OpenAI announces that a model is retired from ChatGPT or OpenAI-hosted APIs, that retirement does not automatically apply to Azure AI Foundry.
The authoritative source is always the **Foundry portal → Model Catalog → Retirement date column**.

**Recommended migration targets from `gpt-4o-mini`:**
- `gpt-5-nano` — ultra-low latency, no registration required, designed for high-volume straightforward requests
- `gpt-5-mini` — reasoning + tool-calling, no registration required, real-time agent workloads
- `gpt-5.4` — full agentic power, 1M token context, for complex orchestration

---

## What This Means for the .NET + Azure Developer

| Concern | Action |
|---|---|
| **Model migration** | Swap `gpt-4o-mini` before March 31 — check the Foundry portal for your exact retirement date |
| **SDK upgrade** | Add `azure-ai-projects 2.0.0-beta.1` (NuGet), review breaking changes |
| **Agentic pipelines** | Evaluate GPT-5.4 for multi-step workflows; leverage Tool Search for large tool registries |
| **GitHub Copilot in VS** | Enable GPT-5.4 in org Copilot settings to give your devs the latest model in VS 2026 |
| **REST API stability** | If you can't wait for SDK GA, target the REST API directly —
the contract is locked and you can target it for production stability today
|

---

## Bonus Context: The Foundry Model Catalog Is Getting Crowded (In a Good Way)

Worth noting that GPT-5.4 isn't arriving alone. Recent weeks also brought:
Claude Opus 4.6 and Sonnet 4.6 from Anthropic with 1M-token context (beta), adaptive thinking, and context compaction
, as well as
Grok 4.0 graduating to GA and Grok 4.1 Fast arriving in preview at $0.20/M input tokens for high-throughput non-reasoning workloads.
The Foundry model catalog is fast becoming the "one deployment surface to rule them all" for enterprise .NET shops — which is both convenient and a reason to invest in the abstraction layer the new `azure-ai-projects` SDK is building toward.

---

## Further Reading

- **GPT-5.4 GA in Microsoft Foundry (official blog):** https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-gpt-5-4-in-microsoft-foundry/4499785
- **What's New in Microsoft Foundry — February 2026 (.NET SDK beta, REST GA):** https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-feb-2026/
- **GPT-5.4 launch coverage (TechCrunch):** https://techcrunch.com/2026/03/05/openai-launches-gpt-5-4-with-pro-and-thinking-versions/
- **GPT-5.4 in GitHub Copilot (GitHub Changelog):** https://github.blog/changelog/2026-03-05-gpt-5-4-is-generally-available-in-github-copilot/
- **gpt-4o-mini retirement on Azure Foundry (Microsoft Q&A):** https://learn.microsoft.com/en-us/answers/questions/5775321/are-gpt-4o-mini-and-other-models-retiring-from-azu
- **Foundry Models sold directly by Azure (authoritative model list):** https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure
- **What's New in Microsoft Foundry — Dec 2025 & Jan 2026 (SDK consolidation, AzureML EOL):** https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-dec-2025-jan-2026/
- **Visual Studio 2026 Release Notes (AI-native IDE, .NET 10 support):** https://learn.microsoft.com/en-us/visualstudio/releases/2026/release-notes