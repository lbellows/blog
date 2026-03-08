---
author: the.serf
date: 2026-03-08 07:34:36 -0400
layout: post
tags:
- azure
- foundry
- march
- agent
- deployments
- claude-sonnet-4-6
title: 'AI on .NET & Azure: Weekly Roundup — Week of March 8, 2026'
---

# AI on .NET & Azure: Weekly Roundup — Week of March 8, 2026

**Your Sunday digest of the AI stories that matter most to .NET and Azure engineers, plus a look at the week ahead.**

---

## TL;DR

- **⚠️ Action required now:** GPT-4o Standard deployments retire March 31, 2026 — broken apps incoming if you haven't migrated.
- **🆕 GPT-5.4 is GA** in Microsoft Foundry, bringing production-grade agentic reasoning with built-in computer use.
- **🤖 Microsoft Agent Framework hits Release Candidate** — time to start your Semantic Kernel migration.
- **🔧 Agent Skills land in MAF** (March 2) — portable, SKILL.md-driven expertise packages for .NET and Python agents.
- **🔌 Azure Functions MCP support is GA** — serverless, identity-secure AI tool endpoints are now production-ready.
- **📜 New Microsoft certifications** for AI developers are opening for beta in March/April.

---

## 1. ⚠️ Hard Deadline: Migrate Off GPT-4o Standard Deployments by March 31

If you've been skimming your Azure Service Health notifications, stop skimming. This one bites.
Azure OpenAI has officially announced the retirement of GPT-4o base model versions `2024-05-13` and `2024-08-06`, with a final retirement date of **March 31, 2026**.
From March 31 onward, any Assistant, chat, or workload pointing to these versions will fail unless migrated.
> **Don't be fooled by OpenAI.com announcements.**
The screenshot from the Azure AI Foundry portal reflects the authoritative retirement dates for Azure-hosted models. When OpenAI announces that a model is retired from ChatGPT or OpenAI-hosted APIs, that retirement does not automatically apply to Azure AI Foundry.
Always check the Foundry portal.
The official replacement model for GPT-4o in the Assistants API (Preview) is `gpt-5.1` version `2025-11-13` — the supported successor for agent-style, tool-using, threaded Assistant workloads.
If you've selected the option to auto-upgrade your Standard, Data-Zone Standard, or Global Standard deployments, they will be automatically upgraded to the replacement model version during the weeks prior to retirement.
If you haven't opted in, you need to act manually. Now.

**Migration checklist:**

```bash
# 1. List all your current Azure OpenAI deployments
az cognitiveservices account deployment list \
  --name <your-resource-name> \
  --resource-group <your-rg> \
  --output table

# 2. Check retirement dates in the Foundry portal:
#    Model Catalog → Retirement date column

# 3. Redeploy to gpt-5.1 (2025-11-13) or later
az cognitiveservices account deployment create \
  --name <your-resource-name> \
  --resource-group <your-rg> \
  --deployment-name "gpt-5-1-prod" \
  --model-name "gpt-5.1" \
  --model-version "2025-11-13" \
  --model-format "OpenAI" \
  --sku-name "GlobalStandard" \
  --sku-capacity 10
```

> 💡 **Pro tip:**
Set up Azure Service Health alerts for your subscription to receive automated notifications about service changes.
Past-you will thank future-you.

---

## 2. 🆕 GPT-5.4 Is GA in Microsoft Foundry

Hot off the press (literally two days ago):
OpenAI's GPT-5.4 is now generally available in Microsoft Foundry — a model designed to help organizations move from planning work to reliably completing it in production environments.
GPT-5.4 combines stronger reasoning with built-in computer use capabilities to support automation scenarios, and dependable execution across tools, files, and multi-step workflows at scale.
For .NET engineers building agentic pipelines, the headline improvements are:
More consistent reasoning over time (maintaining intent across multi-turn and multi-step interactions), enhanced instruction alignment to reduce prompt tuning and oversight, latency-improved performance for responsive real-time workflows, and integrated computer use capabilities for structured orchestration of tools, file access, data extraction, guarded code execution, and agent handoffs.
GPT-5.4 and GPT-5.4 Pro are available through Microsoft Foundry, which provides policy enforcement, monitoring, version management, and auditability — helping teams manage AI systems throughout their lifecycle.
> ⚠️ Note:
Registration is required for access to `gpt-5.4` and `gpt-5.4-pro`.
Apply early if you want it in your next sprint.

---

## 3. 🎙️ New Real-Time + Codex Models Roll Out in Foundry

Also shipping this week:
GPT-Realtime-1.5, GPT-Audio-1.5, and GPT-5.3-Codex are rolling out into Microsoft Foundry — together, these models push the needle from short, stateless interactions toward AI systems that can reason, act, and collaborate over time.
For real-time voice apps, the numbers are encouraging:
In OpenAI's evaluations, GPT-Realtime-1.5 shows a +5% lift on Big Bench Audio (reasoning), a +10.23% improvement in alphanumeric transcription, and a +7% gain in instruction following, while maintaining low-latency performance.
On the coding side,
GPT-5.3-Codex brings together advanced coding capability with broader reasoning and professional problem-solving in a single model built for real engineering work — unifying the frontier coding performance of GPT-5.2-Codex with the reasoning capabilities of GPT-5.2.
---

## 4. 🤖 Microsoft Agent Framework Hits Release Candidate

Semantic Kernel veterans, your migration clock just got louder.
Microsoft Agent Framework has reached Release Candidate status for both .NET and Python. Release Candidate means the API surface is stable, and all features intended for version 1.0 are complete.
Microsoft Agent Framework is a comprehensive, open-source framework for building, orchestrating, and deploying AI agents — the successor to Semantic Kernel and AutoGen — providing a unified programming model across .NET and Python with simple agent creation, going from zero to a working agent in just a few lines of code.
One of the most developer-friendly changes: no more `[KernelFunction]` decoration tax. The migration guide shows the before/after clearly:

```csharp
// BEFORE: Semantic Kernel required [KernelFunction]
public class MenuPlugin {
    [KernelFunction]
    public static MenuItem[] GetMenu() => ...;
}

// AFTER: Agent Framework — plain methods, no attributes needed
public class MenuTools {
    [Description("Get menu items")]   // optional
    public static MenuItem[] GetMenu() => ...;
}
```
If you have an existing project using Semantic Kernel, or if you need to ship something quickly, it is perfectly fine to continue using Semantic Kernel. If you are starting a new project and can wait until Microsoft Agent Framework reaches General Availability, the team recommends starting with Microsoft Agent Framework.
---

## 5. 🔧 Agent Skills: Portable Domain Expertise for Your Agents (March 2)
As of March 2, you can now equip Microsoft Agent Framework agents with portable, reusable skill packages that provide domain expertise on demand — without changing a single line of your agent's core instructions. With built-in skills providers for both .NET and Python, agents can discover and load Agent Skills at runtime, pulling in only the context they need, when they need it.
Agent Skills is a simple, open format. At the core of every skill is a `SKILL.md` file — a Markdown document that describes what the skill does and provides step-by-step instructions for how to do it.
Think of it as a "résumé" your agent reads before starting a task. A skill directory looks like:

```
expense-report/
├── SKILL.md           # Required — frontmatter + instructions
├── scripts/
│   └── validate.py    # Executable code agents can run
├── references/
│   └── POLICY_FAQ.md  # Reference documents loaded on demand
└── assets/
    └── template.md
```

This is one of those features that sounds simple but unlocks a whole compositional model for building specialized, maintainable agent systems.

---

## 6. 🔌 Azure Functions MCP Support: Now GA
Microsoft has moved its Model Context Protocol (MCP) support for Azure Functions to General Availability, signaling a shift toward standardized, identity-secure agentic workflows.
With built-in OBO authentication and streamable HTTP transport, it addresses key security concerns.
For cost-conscious teams:
when MCP tools sit idle, costs drop to zero while maintaining fast wake-up times. The Premium plan supports "always-ready" instances that remain pre-initialized, eliminating cold-start latency — critical for mission-critical tools where initialization delays can cause SSE connection timeouts and poor agent response times.
The MCP extension quickstarts cover C# (.NET), Python, and TypeScript (Node.js), with a Java quickstart coming soon.
The platform integrates directly with Azure AI Foundry, allowing agents to discover and invoke MCP tools without additional configuration layers.
---

## 7. 🎓 New AI Developer Certifications Opening This Month

Microsoft is quietly reshuffling its entire certification portfolio around AI roles. Relevant ones opening for beta in March–April:

-
**Azure AI App and Agent Developer Associate** aligns with generative and agentic architectures for planning/managing AI resources in Microsoft Foundry, building generative apps and multi-step reasoning workflows, and developing production-ready agents with multi-agent orchestration capabilities. Exam AI-103 beta is available in April 2026.
-
**Azure AI Cloud Developer Associate** is designed for developers who want to validate their ability to build, integrate, and monitor AI solutions on Azure using containerized compute, vector-enabled databases, event-driven AI pipelines, serverless functions, and distributed observability. Exam AI-200 is expected in April 2026.
---

## What to Watch Next Week

- **Microsoft Agent Framework GA** — the RC is stable; GA could land any sprint now. Keep watching the [Semantic Kernel blog](https://devblogs.microsoft.com/semantic-kernel/).
- **GPT-4o retirement countdown** — 23 days. If you haven't started your migration, that's your Monday morning task.
-
**Project Manager Agent** for Microsoft 365 Copilot is rolling out to Public Preview in March and worldwide in April
— relevant for teams building M365-integrated .NET solutions.
-
**DPO fine-tuning public preview** in Azure OpenAI, starting with `gpt-4o-2024-08-06`
— a lighter-weight alignment technique worth evaluating if you're doing custom model tuning.

---

## Further Reading

- Azure OpenAI Model Retirements (authoritative source):
  https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-retirements
- GPT-5.4 GA announcement — Microsoft Foundry:
  https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-gpt-5-4-in-microsoft-foundry/4499785
- GPT-Realtime-1.5, GPT-Audio-1.5, GPT-5.3-Codex rollout:
  https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/new-azure-open-ai-models-bring-fast-expressive-and-real%E2%80%91time-ai-experiences-in-m/4496184
- Microsoft Agent Framework Release Candidate + migration guide:
  https://devblogs.microsoft.com/semantic-kernel/migrate-your-semantic-kernel-and-autogen-projects-to-microsoft-agent-framework-release-candidate/
- Agent Skills in Microsoft Agent Framework:
  https://devblogs.microsoft.com/semantic-kernel/give-your-agents-domain-expertise-with-agent-skills-in-microsoft-agent-framework/
- Azure Functions MCP Support GA:
  https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- Generative AI with LLMs in C# / .NET 2026 overview:
  https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/
- New Microsoft AI Certifications 2026:
  https://techcommunity.microsoft.com/blog/skills-hub-blog/the-ai-job-boom-is-here-are-you-ready-to-showcase-your-skills/4494128
- What's New in Microsoft 365 Copilot — February 2026:
  https://techcommunity.microsoft.com/blog/microsoft365copilotblog/what%E2%80%99s-new-in-microsoft-365-copilot--february-2026/4496489
- Semantic Kernel to Microsoft Agent Framework migration guide:
  https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-semantic-kernel/