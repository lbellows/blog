---
author: the.serf
date: 2026-03-09 07:50:07 -0400
layout: post
tags:
- .net
- apps
- azure
- gpt-5.4
- agentic
- claude-sonnet-4-6
title: 'GPT-5.4 Is Now GA in Microsoft Foundry: What It Means for Your .NET and Azure
  AI Apps'
---

# GPT-5.4 Is Now GA in Microsoft Foundry: What It Means for Your .NET and Azure AI Apps

**Published: March 9, 2026 | ~800 words**

---

## TL;DR
OpenAI's GPT-5.4 is now generally available in Microsoft Foundry, designed to help organizations move from planning work to reliably completing it in production environments.
For .NET and Azure developers, this is the moment to evaluate a model upgrade — not just for raw capability, but for cost, context window size, token efficiency, and a new tier called GPT-5.4 Pro. Here's what you actually need to know before you touch your `appsettings.json`.

---

## What Was Just Shipped
On Thursday, OpenAI released GPT-5.4, billed as "our most capable and efficient frontier model for professional work." In addition to the standard version, GPT-5.4 is also available as a reasoning model (GPT-5.4 Thinking) or optimized for high performance (GPT-5.4 Pro).
The API version of the model supports context windows as large as 1 million tokens — by far the largest context window available from OpenAI — and OpenAI emphasized improved token efficiency, saying GPT-5.4 was able to solve the same problems with significantly fewer tokens than its predecessor.
For engineers who have been quietly burning through tokens on long RAG chains or large code analysis agents, that last sentence deserves a second read.

---

## Pricing: The Numbers You'll Paste Into a Spreadsheet
GPT-5.4 in Microsoft Foundry is priced at **$2.50 per million input tokens**, $0.25 per million cached input tokens, and **$15.00 per million output tokens**. It is available at launch in Standard Global and Standard Data Zone (US). GPT-5.4 Pro is priced at **$30.00 per million input tokens** and **$180.00 per million output tokens**, available in Standard Global.
The Pro tier is not for the faint-budgeted. Unless you're running high-stakes financial or legal workloads, the standard tier is almost certainly your starting point. That said,
developers can use the model router in Foundry Models to save up to 60% on inferencing cost with no loss in fidelity — powered by a fine-tuned SLM under the hood, the model router evaluates each prompt and decides the optimal model based on complexity, performance needs, and cost efficiency.
In short: let the router pick `gpt-5-nano` for your "what's the weather?" queries.

---

## Why This Matters for Agentic .NET Apps
By deploying GPT-5.4 through Microsoft Foundry, organizations can integrate advanced agentic capabilities into existing environments while aligning with security, compliance, and operational requirements from day one.
Modern AI applications rarely fit into a single prompt — real work unfolds over time: maintaining context, following instructions, invoking tools, and adapting as requirements evolve. When these foundations break down through latency spikes, instruction drift, or unreliable tool calls, both user conversations and developer workflows are impacted.
GPT-5.4 directly targets these failure modes.
The new model comes with significantly improved benchmark results, including record scores in computer use benchmarks OSWorld-Verified and WebArena Verified.
For .NET devs wiring up agents with the Foundry Agent Service,
computer use capabilities will be introduced shortly after launch
— so keep an eye on the release notes.

---

## Getting Started: Deploying GPT-5.4 via Azure CLI
Models sold directly by Azure include all Azure OpenAI models and specific selected models from top providers. These models are billed through your Azure subscription, covered by Azure service-level agreements, and supported by Microsoft.
Here's a quick CLI snippet to get a `gpt-5.4` deployment up and running:

```bash
az cognitiveservices account deployment create \
  --name "my-foundry-resource" \
  --resource-group "my-rg" \
  --deployment-name "gpt-5-4-standard" \
  --model-name "gpt-5.4" \
  --model-version "1" \
  --model-format "OpenAI" \
  --sku-capacity 10 \
  --sku-name "GlobalStandard"
```

And in C# using the `Azure.AI.OpenAI` NuGet package:

```csharp
using Azure.AI.OpenAI;
using Azure;

var client = new AzureOpenAIClient(
    new Uri("https://<your-resource>.openai.azure.com/"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_OPENAI_KEY")!));

var chatClient = client.GetChatClient("gpt-5-4-standard");

var response = await chatClient.CompleteChatAsync(
    [new UserChatMessage("Summarize this 500-page contract in 3 bullet points.")]);

Console.WriteLine(response.Value.Content[0].Text);
```

> 💡 **Tip:** If you're using `Microsoft.Extensions.AI` (MEAI) — the unified `IChatClient` abstraction —
Microsoft Extensions for AI provides unified abstractions for interacting with models, including `IChatClient`
, making it trivial to swap the underlying model without touching your business logic.

---

## One Operational Caveat: Model Retirement Discipline

With GPT-5.4 GA, older models are inching closer to their sunset.
For generally available models, retirement is no sooner than 365 days from launch. Microsoft provides customers with at least 60 days' notice before model retirement for GA models.
That's a reasonable runway, but if you're on `auto-update` deployments,
you might notice changes in model behavior and compatibility after a version upgrade — these changes can affect your applications and workflows that rely on the models.
**Recommendation:** Pin your deployment version in production. Let staging ride `auto-update` and run your eval suite before promoting.

---

## The Governance Angle (Especially if Your Team Has a CISO)
GPT-5.4 and GPT-5.4 Pro are available through Microsoft Foundry, which provides the operational controls organizations need to deploy AI responsibly in production environments. Foundry supports policy enforcement, monitoring, version management, and auditability, helping teams manage AI systems throughout their lifecycle.
Separately, if you're shipping AI agents into enterprise environments,
the Security Dashboard for AI is now available in public preview. Current Microsoft Security customers can access it without any extra licensing fees — it gives CISOs and AI risk leaders a unified, real-time view of AI threats across agents, apps, and platforms by connecting signals from Microsoft Defender, Microsoft Entra, and Microsoft Purview, all within a single interface.
This is worth wiring up even if your security posture feels fine — "feels fine" is not an audit response.

---

## Key Takeaways

| What | Why it matters |
|---|---|
| GPT-5.4 GA on Azure (March 5) | Production-ready, enterprise SLA, billed to your subscription |
| 1M token context window | Entire codebases or long documents in a single call |
| Improved token efficiency | Fewer tokens → lower cost for same output quality |
| Model Router in Foundry | Automatic cost optimization across the GPT-5.x family |
| GPT-5.4 Pro | High-power tier for regulated/critical workloads — budget accordingly |
| Security Dashboard for AI (Preview) | Free for existing Microsoft Security customers |

---

## Further Reading

- https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-gpt-5-4-in-microsoft-foundry/4499785
- https://techcrunch.com/2026/03/05/openai-launches-gpt-5-4-with-pro-and-thinking-versions/
- https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/new-azure-open-ai-models-bring-fast-expressive-and-real%E2%80%91time-ai-experiences-in-m/4496184
- https://learn.microsoft.com/en-us/azure/foundry-classic/openai/whats-new
- https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-dec-2025-jan-2026/
- https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements
- https://learn.microsoft.com/en-us/partner-center/announcements/2026-march
- https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/