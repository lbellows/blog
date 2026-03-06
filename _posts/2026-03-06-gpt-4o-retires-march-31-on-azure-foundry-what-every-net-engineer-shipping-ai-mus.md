---
author: the.serf
date: 2026-03-06 06:44:19 -0500
layout: post
tags:
- .net
- azure
- march
- foundry
- gpt-4o
- claude-sonnet-4-6
title: 'gpt-4o Retires March 31 on Azure Foundry: What Every .NET Engineer Shipping
  AI Must Do This Weekend'
---

# gpt-4o Retires March 31 on Azure Foundry: What Every .NET Engineer Shipping AI Must Do This Weekend

**TL;DR** — Two specific versions of `gpt-4o` are being retired in Azure AI Foundry on **March 31, 2026** — 25 days from today. If your .NET app still points at `gpt-4o-2024-05-13` or `gpt-4o-2024-08-06`, you will get hard 500-class error responses starting April 1. Microsoft's recommended replacement is `gpt-5.1-2025-11-13`. Meanwhile, a new AI-powered SOAR playbook generator just landed in Microsoft Sentinel (public preview, March 2026) — a timely reminder that the Azure AI ecosystem keeps moving fast even as older models sunset.

---

## The Retirement That Actually Matters Right Now

You might have seen noise in February about OpenAI retiring `gpt-4o` from ChatGPT on February 13, 2026. Take a breath — that was a UI retirement.
OpenAI (ChatGPT) and Azure AI Foundry operate on independent lifecycle policies. When OpenAI announces that a model is retired from ChatGPT or OpenAI-hosted APIs, that retirement does *not* automatically apply to Azure AI Foundry.
However, Azure has its own deadline coming up fast:
Azure OpenAI `gpt-4o` model versions `2024-05-13` and `2024-08-06` will be retired **March 31, 2026**. After the retirement date, these model versions will no longer be available or operable.
From March 31, 2026 onward, any Assistant, chat, or workload pointing to these versions will fail unless migrated.
No soft landing. No grace-period reads. Just errors. (Enjoy your long weekend, past-you.)

---

## What Exactly Gets Retired
This retirement will only impact base-model deployments. Beginning on March 31, 2026, fine-tuning on `gpt-4o` versions `2024-05-13` and `2024-08-06` will no longer be allowed; however, **existing fine-tuned deployments will continue to operate for an additional year.**
So if you did fine-tuning, you get a one-year runway. If you're using the base model directly, **you have no runway left.**

---

## The Recommended Migration Path
The official replacement model for `gpt-4o` in the Assistants API (Preview) is `gpt-5.1` version `2025-11-13`. This model is the supported successor for agent-style, tool-using, threaded Assistant workloads, and it fully replaces `gpt-4o` for this use case.
### Step 1 — Verify your deployments

Check the Foundry portal **Model Catalog → Retirement date column** or run:

```bash
az cognitiveservices account deployment list \
  --name <your-aoai-resource> \
  --resource-group <rg> \
  --query "[].{name:name, model:properties.model.name, version:properties.model.version}" \
  --output table
```

Any row showing `gpt-4o` with version `2024-05-13` or `2024-08-06` needs attention now.

### Step 2 — Deploy the replacement model

```bash
az cognitiveservices account deployment create \
  --name <your-aoai-resource> \
  --resource-group <rg> \
  --deployment-name gpt5-1-prod \
  --model-name gpt-5.1 \
  --model-version 2025-11-13 \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 20
```

### Step 3 — Update your .NET client

If you're using the `Azure.AI.OpenAI` SDK with `Microsoft.Extensions.AI` (MEAI), swapping the deployment name is the only code change needed for most scenarios:

```csharp
// Before
IChatClient client = new AzureOpenAIClient(
    new Uri(endpoint),
    new DefaultAzureCredential())
    .AsChatClient("gpt-4o-2024-05-13");  // ❌ retiring March 31

// After
IChatClient client = new AzureOpenAIClient(
    new Uri(endpoint),
    new DefaultAzureCredential())
    .AsChatClient("gpt5-1-prod");  // ✅ gpt-5.1 deployment
```
The `IChatClient` abstraction is part of Microsoft Extensions for AI (MEAI), which provides unified abstractions for interacting with models. As a .NET developer you shouldn't have to choose a single provider or lock into a single solution — that's why the .NET team invested in a set of extensions that provide consistent APIs that are universal yet flexible.
### Step 4 — Test for behavioral differences
When migrating from `gpt-4o` to `gpt-5.1`, expect stricter system-message enforcement, more deterministic tool-calling, and slightly different reasoning and verbosity patterns. Testing is strongly recommended.
A quick smoke-test strategy: run your golden-set eval prompts against both deployments in parallel and diff the outputs before cutting over in production. Azure AI Foundry's continuous evaluation dashboard can help here.

### Step 5 — Know your authoritative source
For any workload running on Azure AI Foundry, the Foundry portal (Model Catalog → Retirement date column) and the Microsoft Learn "Azure OpenAI in Foundry – Model Retirements" documentation are the only authoritative sources. OpenAI blog posts or ChatGPT retirement notices should not be used to determine Azure retirement timelines.
Bookmark it. Tattoo it. Put it in your team wiki. You know what to do.

---

## Auto-Upgrade: Friend or Foe?
As part of this retirement, the replacement model will be set to `gpt-5.1` version `2025-11-13` on **March 9, 2026**. If you've selected the option to auto-upgrade your standard, data-zone standard, or global standard deployment(s), they will be automatically upgraded to the replacement model version during the weeks prior to retirement.
Auto-upgrade is convenient but can surprise you if your app has prompt-sensitivity or tight output-format contracts. **Disable it on production deployments and control the migration yourself** — then re-enable once you've validated `gpt-5.1` behavior.

---

## Bonus: AI Is Now Writing Your Security Playbooks Too

While you're in migration mode, here's a parallel development worth knowing about.
The Microsoft Sentinel playbook generator (public preview, March 2026) lets you design and generate fully functional, code-based playbooks by describing what you need in natural language. Instead of relying on rigid templates and limited action libraries, you describe the workflow you want, and the generator produces a Python playbook with documentation and a visual flowchart. This has been a top ask from enterprise customers looking for more flexible automation in their SIEM workflows.
For .NET teams that also own their Azure security posture,
the SOAR playbook generator creates Python-based automation workflows co-authored through a conversational experience with Cline, an AI coding agent.
Combined with the new AI-powered Sentinel features,
the Codeless Connector Framework (CCF) Push feature supports high-throughput ingestion, data transformation before ingestion, and direct delivery to system tables — opening pathways to advanced scenarios, including data lake integrations and agentic AI use cases.
---

## Key Takeaways for .NET/Azure Engineers

| Action | Deadline | Priority |
|---|---|---|
| Audit `gpt-4o` deployments for retiring versions | **Now** | 🔴 Critical |
| Deploy `gpt-5.1-2025-11-13` and run evals | Before March 25 | 🔴 Critical |
| Disable auto-upgrade on production slots | Before March 9 | 🟠 High |
| Explore Sentinel AI playbook generator | Ongoing | 🟢 Nice-to-have |

---

## Further Reading

- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-retirements?view=foundry-classic
- https://learn.microsoft.com/en-us/answers/questions/5775321/are-gpt-4o-mini-and-other-models-retiring-from-azu
- https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/model-lifecycle-retirement?view=foundry-classic
- https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/
- https://techcommunity.microsoft.com/blog/microsoftsentinelblog/what%E2%80%99s-new-in-microsoft-sentinel-march-2026/4499508
- https://techcommunity.microsoft.com/blog/microsoftthreatprotectionblog/monthly-news---march-2026/4498458
- https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/announcing-extended-support-for-fine-tuning-gpt-4o-and-gpt-4o-mini/4488525