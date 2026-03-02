---
author: the.serf
date: 2026-03-02 06:46:55 -0500
layout: post
tags:
- azure
- .net
- gpt-5.3-codex
- gpt-audio-1.5
- gpt-realtime-1.5
- claude-sonnet-4-6
title: GPT-5.3-Codex, GPT-Realtime-1.5, and GPT-Audio-1.5 Just Landed in Azure AI
  Foundry — Here's What .NET Engineers Need to Know
---

# GPT-5.3-Codex, GPT-Realtime-1.5, and GPT-Audio-1.5 Just Landed in Azure AI Foundry — Here's What .NET Engineers Need to Know

**TL;DR:** Three new OpenAI models rolled out in Microsoft Foundry this week. GPT-5.3-Codex unifies frontier coding and reasoning into one model purpose-built for large, real-world repos. GPT-Realtime-1.5 and GPT-Audio-1.5 bring measurably better voice AI to Azure. All three are reachable through existing Azure OpenAI APIs — with a registration gate on the Codex model. Oh, and the Microsoft-OpenAI partnership just got a public reaffirmation. Read on before you plan your next sprint.

---

## What Just Shipped
Starting this week, **GPT-Realtime-1.5**, **GPT-Audio-1.5**, and **GPT-5.3-Codex** are rolling out into Microsoft Foundry — together, these models push the needle from short, stateless interactions toward AI systems that can reason, act, and collaborate over time.
This is not a grab-bag model catalog refresh. Each model targets a distinct engineering scenario, and the timing matters:
since 2019, Microsoft and OpenAI have been building one of the most consequential collaborations in technology, grounded in mutual trust and deep technical integration
— and a [joint statement published February 27](https://blogs.microsoft.com/blog/2026/02/27/microsoft-and-openai-joint-statement-on-continuing-partnership/) put any partnership uncertainty to bed.
Azure remains the exclusive cloud provider for stateless OpenAI APIs, and Microsoft is the exclusive cloud provider for stateless APIs that provide access to OpenAI's models and IP.
In short: build on Azure, stay on the right side of the partnership.

---

## Deep Dive: GPT-5.3-Codex — The One That Should Change Your Agentic Architecture

### What it is
GPT-5.3-Codex brings together advanced coding capability with broader reasoning and professional problem solving in a single model built for real engineering work. It unifies the frontier coding performance of GPT-5.2-Codex with the reasoning and professional knowledge capabilities of GPT-5.2 in one system — shifting the experience from optimizing isolated outputs to supporting longer-running development efforts where repositories are large, changes span multiple steps, and requirements aren't always fully specified at the start.
If you've been juggling two deployments — one for reasoning-heavy planning, one for code generation — this model is the "have your cake and eat it too" answer. (The .NET codebase you inherited in 2019 is now fair game.)

### What it handles well
Developers and teams can apply GPT-5.3-Codex across a wide range of scenarios, including refactoring and modernizing large or legacy applications.
That maps well to the .NET world, where many teams are mid-migration from .NET Framework to .NET 8/9 and grappling with large, multi-project solutions.
The model is designed for imperfect inputs — legacy code, partial docs, screenshots, diagrams — and works through multi-step changes, reviews, and fixes, helping keep context, intent, and standards intact across the entire lifecycle.
### Access & registration
Registration is required for access to `gpt-5.3-codex`, as well as `gpt-5.2` and `gpt-5.2-codex`. Access will be granted based on Microsoft's eligibility criteria.
If you already have access to a prior Codex or GPT-5 model,
your approved subscriptions will automatically be granted access upon model release
— no re-application needed.

### Deploying via Azure CLI

Deploy through the Foundry model catalog or the Azure OpenAI deployments pane.
From the model catalog, select a reasoning model such as `gpt-5.3-codex`, choose **Use this model**, and copy the endpoint URL and API key.
For Codex CLI with Azure, create `~/.codex/config.toml`:

```toml
model = "gpt-5.3-codex"
model_provider = "azure"
model_reasoning_effort = "medium"

[model_providers.azure]
name = "Azure OpenAI"
base_url = "https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1"
env_key = "AZURE_OPENAI_API_KEY"
wire_api = "responses"
```

> **Note:**
The config uses the v1 Responses API — you no longer need to pass `api-version`, but you *must* include `/v1` in the `base_url` path.
From .NET, you can target the same Responses API endpoint using `Azure.AI.OpenAI` or the `Microsoft.Extensions.AI` (MEAI) `IChatClient` abstraction:

```csharp
// Requires: dotnet add package Azure.AI.OpenAI
using Azure.AI.OpenAI;
using Azure.Identity;

var client = new AzureOpenAIClient(
    new Uri("https://YOUR_RESOURCE.openai.azure.com/"),
    new DefaultAzureCredential());

var chatClient = client.GetChatClient("gpt-5.3-codex");

var response = await chatClient.CompleteChatAsync(
    [
        new SystemChatMessage("You are a senior .NET architect."),
        new UserChatMessage("Refactor this EF6 DbContext to EF Core 9, preserving all navigation properties.")
    ],
    new ChatCompletionOptions { ReasoningEffort = ChatReasoningEffortLevel.Medium }
);

Console.WriteLine(response.Value.Content[0].Text);
```

> ⚠️ Set `ReasoningEffort` thoughtfully — `High` yields the best output for complex refactors but increases latency and token cost. `Medium` is a sensible default for CI pipelines.

---

## Deep Dive: GPT-Realtime-1.5 & GPT-Audio-1.5 — Voice AI Grows Up
The `gpt-realtime-1.5-2026-02-23` and `gpt-audio-1.5-2026-02-23` models are now available, built upon last year's GPT-Realtime and GPT-Audio with focused improvements in instruction following, multi-lingual support, and tool calling — while preserving the low-latency, real-time interactions developers need for voice-first applications.
The numbers are concrete:
in OpenAI's evaluations, GPT-Realtime-1.5 shows a +5% lift on Big Bench Audio (reasoning), a +10.23% improvement in alphanumeric transcription, and a +7% gain in instruction following, while maintaining low-latency performance.
The use-case list is practical:
developers are using GPT-Realtime-1.5 and GPT-Audio-1.5 for scenarios where low-latency voice interaction is essential, including conversational voice agents for customer support or internal help desks, voice-enabled assistants embedded in applications or devices, and hands-free workflows where audio input and output replace keyboard interaction.
Developers can try them out through the existing chat completion APIs in Microsoft Foundry
— meaning no new SDK dependency for .NET teams already on `Azure.AI.OpenAI`.

---

## The Model Retirement Clock Is Also Ticking

While shiny new models arrive, older ones are heading out the door.
The final retirement date for GPT-4o versions 2024-05-13 and 2024-08-06 is 31 March 2026, and Azure subscriptions have received formal notifications. From that date onward, any assistant, chat, or workload pointing to those versions will fail unless migrated.
OpenAI and Azure AI Foundry operate on independent lifecycle policies — when OpenAI announces a model retirement, that does not automatically apply to Azure AI Foundry.
So ignore OpenAI's ChatGPT retirement notices for production planning;
for any workload running on Azure AI Foundry, the Foundry portal's Model Catalog retirement date column and the Microsoft Learn "Azure OpenAI in Foundry – Model Retirements" documentation are the only authoritative sources.
Also worth flagging for teams with training pipelines:
the Azure Machine Learning SDK v1 reaches end of support on June 30, 2026 — after this date, existing workflows may face security risks and breaking changes without active Microsoft support.
---

## Practical Takeaways for .NET / Azure Teams

| Action | Priority | Deadline |
|---|---|---|
| Register for `gpt-5.3-codex` access in Foundry | 🔥 High | Now (rolling access) |
| Migrate GPT-4o (2024-05-13 / 2024-08-06) deployments to GPT-5.1+ | 🔥 High | Before 31 March 2026 |
| Evaluate GPT-Realtime-1.5 for voice agent workloads | Medium | This sprint |
| Migrate from AzureML SDK v1 to v2 | Medium | Before 30 June 2026 |
| Pin `azure-ai-projects` v2 beta in new agent projects | Medium | Now |

---

## Further Reading

- New Azure OpenAI models (GPT-5.3-Codex, GPT-Realtime-1.5, GPT-Audio-1.5) in Foundry — Microsoft Tech Community: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/new-azure-open-ai-models-bring-fast-expressive-and-real%E2%80%91time-ai-experiences-in-m/4496184
- Microsoft & OpenAI Joint Statement on Continuing Partnership (Feb 27, 2026): https://blogs.microsoft.com/blog/2026/02/27/microsoft-and-openai-joint-statement-on-continuing-partnership/
- What's New in Azure OpenAI in Microsoft Foundry — Microsoft Learn: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new?view=foundry-classic
- Codex with Azure OpenAI in Microsoft Foundry Models (CLI + config reference): https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/codex?view=foundry-classic
- What's New in Microsoft Foundry — Dec 2025 & Jan 2026 (SDK consolidation, AzureML EOL): https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-dec-2025-jan-2026/
- GPT-4o Retirement & Replacement Models — Microsoft Q&A: https://learn.microsoft.com/en-us/answers/questions/5775321/are-gpt-4o-mini-and-other-models-retiring-from-azu
- Foundry Models Sold Directly by Azure (access requirements): https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure