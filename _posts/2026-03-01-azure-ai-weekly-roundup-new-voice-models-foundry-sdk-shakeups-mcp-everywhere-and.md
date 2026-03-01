---
author: the.serf
date: 2026-03-01 06:34:16 -0500
layout: post
tags:
- foundry
- sdk
- azure
- mcp
- week
- claude-sonnet-4-6
title: 'Azure & AI Weekly Roundup: New Voice Models, Foundry SDK Shakeups, MCP Everywhere,
  and Deprecation Clocks Ticking (Week of March 1, 2026)'
---

# Azure & AI Weekly Roundup: New Voice Models, Foundry SDK Shakeups, MCP Everywhere, and Deprecation Clocks Ticking (Week of March 1, 2026)

> *Your Sunday morning read — grab a coffee, this one has deadlines in it.*

---

**TL;DR**

- **GPT-Realtime-1.5 & GPT-Audio-1.5** landed in Microsoft Foundry on February 23 — better voice, lower latency, SIP telephony support.
- **GPT-5.3-Codex** is rolling out for agentic coding workflows across large repos.
- **MCP (Model Context Protocol)** is now the connective tissue of the Azure AI ecosystem — Azure Functions, Azure Language, and Foundry all speak it.
- **Deprecation alert:** AzureML SDK v1 EOL is **June 30, 2026**. If you're still on it, the clock is ticking louder than ever.
- **Aspire 13.1** shipped MCP integration and Azure deployment upgrades — .NET 10 SDK required.
- **OpenAI Assistants API** retires August 26, 2026; the Responses API is its replacement (Azure OpenAI is on a separate, later timeline — don't panic).

---

## 1. 🎙️ Voice Gets Serious: GPT-Realtime-1.5 and GPT-Audio-1.5 Are Live

The freshest news this week:
GPT-Realtime-1.5, GPT-Audio-1.5, and GPT-5.3-Codex began rolling out into Microsoft Foundry, reflecting the growing needs of the modern developer and pushing the needle from short, stateless interactions toward AI systems that can reason, act, and collaborate over time.
For engineers building voice-first applications, the upgrade is meaningful:
the `gpt-realtime-1.5-2026-02-23` and `gpt-audio-1.5-2026-02-23` models were built upon last year's GPT-Realtime and GPT-Audio with focused improvements in instruction following, multi-lingual support, and tool calling while preserving the low-latency, real-time interactions developers need for voice-first applications.
Numbers matter:
in OpenAI's evaluations, the models show a +5% lift on Big Bench Audio (reasoning), a +10.23% improvement in alphanumeric transcription, and a +7% gain in instruction following, while maintaining low-latency performance.
One particularly useful new capability:
the Realtime API now supports SIP, enabling telephony connections to the Realtime API.
If your team has been eyeing phone-channel integrations (think IVR replacements or call-center copilots), that's your greenlight.
Developers are using GPT-Realtime-1.5 and GPT-Audio-1.5 for scenarios where low-latency voice interaction is essential, including conversational voice agents for customer support or internal help desks, voice-enabled assistants embedded in applications or devices, and hands-free workflows where audio input and output replace keyboard interaction.
**Getting started** — deploy from the Foundry portal:

```
Models + Endpoints → Deploy base model → Search "gpt-realtime-1.5" → Deploy
```

Then use the existing chat completion APIs or the `/realtime` WebSocket endpoint.
For production applications, Microsoft recommends using Microsoft Entra ID for enhanced security.
---

## 2. 🤖 GPT-5.3-Codex: The Agentic Coding Model for Real Engineering Work
GPT-5.3-Codex brings together advanced coding capability with broader reasoning and professional problem solving in a single model built for real engineering work. It unifies the frontier coding performance of GPT-5.2-Codex with the reasoning and professional knowledge capabilities of GPT-5.2 in one system. This shifts the experience from optimizing isolated outputs to supporting longer-running development efforts — where repositories are large, changes span multiple steps, and requirements aren't always fully specified at the start.
In short: this is the model for those "refactor 40 files while respecting our existing contracts" tickets your team has been dreading.
GPT-5-Codex is designed to be used with the Codex CLI and the Visual Studio Code Codex extension, and registration is required for access.
If you previously registered for another limited-access model,
you do not need to reapply and will automatically be granted access.
---

## 3. 🔌 MCP: The Protocol That Ate the Azure AI Ecosystem

Model Context Protocol has quietly become the lingua franca of Azure AI integrations, and this week's updates make that concrete:

- **Azure Functions + MCP:**
Microsoft launched MCP support for Azure Functions, ensuring secure, standardized workflows for AI agents. With built-in OBO authentication and streamable HTTP transport, it addresses key security concerns. Now supporting multiple languages and self-hosting, MCP empowers developers to deploy with ease while safeguarding sensitive data.
Quickstarts cover C# (.NET), Python, and TypeScript — Java is coming soon.

- **Cost engineering tip:**
when MCP tools sit idle, costs drop to zero while maintaining fast wake-up times. The Premium plan supports "always-ready" instances that remain pre-initialized, eliminating cold-start latency — critical for mission-critical tools where initialization delays can cause SSE connection timeouts and poor agent response times.
- **Azure Language + MCP:**
Azure Language now provides specialized tools and agents for building conversational AI applications in Foundry, including an Azure Language MCP server that connects AI agents to Azure Language services through the Model Context Protocol.
- **Foundry MCP Server:**
the Foundry MCP Server (Preview) is a cloud-hosted MCP endpoint at `mcp.ai.azure.com`, live since December 3. Connect from VS Code, Visual Studio, or the Foundry portal — zero local process management, Entra auth included.
- **Foundry Tools tab:**
the Tools tab is the single entry point for discovering, connecting, and managing agentic integrations: MCP servers, A2A endpoints, Azure AI Search, SharePoint, Fabric, and more — across more than 1,400 business systems.
---

## 4. 📦 Foundry SDK v2 Beta: Unified, But Watch for Breaking Renames
Agents, inference, evaluations, and memory operations that previously lived in separate packages (like `azure-ai-agents`) are unified under the `azure-ai-projects` v2 beta line.
The v2 line is the new canonical SDK for everything Foundry: agents (now built on the OpenAI Responses protocol), evaluations, memory stores, and model inference.
However, **breaking change alert** —
key renames include `AzureAISearchAgentTool → AzureAISearchTool`, `BrowserAutomationAgentTool → BrowserAutomationPreviewTool`, and others. These 2.0.0-beta.4 class renames are breaking: if you reference any `*AgentTool` class, update to the new suffixed name.
```bash
# Upgrade and grep your codebase
dotnet add package Azure.AI.Projects --prerelease
grep -r "AgentTool" ./src
```

Also note: when upgrading reasoning models,
GPT-5.1's `reasoning_effort` defaults to `none` — you may need to explicitly pass a `reasoning_effort` level if you want reasoning to occur.
---

## 5. 🟢 .NET & Aspire 13.1: MCP, Azure Deployments, and .NET 10 Required
Azure resources in Aspire 13.1 now expose standardized connection properties that work across supported languages, making it easier for non-.NET applications to connect using consistent settings. Support for deployment slots in Azure App Service and finer control over default role assignments has also been added.
Aspire 13.1 also stabilizes several integrations that were previously in preview, including Dev Tunnels, endpoint proxy support, and Azure Functions.
**Upgrade note:**
Aspire 13.1 requires the .NET 10 SDK or later. Developers upgrading from earlier versions are advised to review the noted breaking changes, particularly around Azure Redis APIs and renamed connection properties.
---

## 6. ⚠️ Deprecation Roundup: Three Clocks You Need on Your Wall

| What | Deadline | Action |
|---|---|---|
| AzureML SDK v1 | **June 30, 2026** | Migrate to SDK v2 |
| OpenAI Assistants API | **August 26, 2026** | Migrate to Responses API |
| `gpt-4o-mini` on Azure Foundry Standard | **March 31, 2026** | Upgrade deployment |

**AzureML SDK v1:**
support for SDK v1 will end on June 30, 2026. While your existing workflows using CLI v1 and SDK v1 will continue to operate after the end-of-support date, they could be exposed to security risks.
Microsoft recommends transitioning to CLI v2 as soon as possible, and SDK v2 before the end-of-support date.
**OpenAI Assistants API → Responses API:**
OpenAI has announced that its Assistants API will be deprecated on August 26, 2026. This API allowed developers to build AI agents with memory, tools, and file handling.
Crucially:
Azure OpenAI Service, provided by Microsoft, is not impacted by this deprecation
— but you'll want to align to the Responses API pattern regardless.

**Azure Foundry model retirement timelines:**
OpenAI and Azure AI Foundry operate on independent lifecycle policies. When OpenAI announces that a model is retired from ChatGPT or OpenAI-hosted APIs, that retirement does not automatically apply to Azure AI Foundry.
Always check the Foundry portal's **Model Catalog → Retirement date column** as the authoritative source.

---

## 7. 🔭 What's Coming Next: Preview the Week Ahead

-
The **Azure AI Connect** virtual event runs March 2–6, 2026, bringing together developers, data scientists, and enterprise leaders to explore the full spectrum of Azure AI services — from Cognitive Services and Machine Learning to the latest breakthroughs in Generative AI.
- Microsoft Foundry's February edition is reportedly landing on a "much shorter timeline" per the Foundry blog — expect further SDK beta drops and likely model announcements.

- The `.NET blog` has signaled a deep-dive post on the **Microsoft Agent Framework** (successor to Semantic Kernel) is incoming — one to watch for teams building multi-agent .NET pipelines.

---

## Practical Checklist for the Week

```bash
# 1. Check AzureML SDK version
pip show azureml-core          # v1 — needs migration before June 30, 2026
pip show azure-ai-ml           # v2 — you're safe

# 2. Upgrade Foundry SDK (JS/TS)
npm install @azure/ai-projects@2.0.0-beta.4

# 3. Audit for breaking AgentTool renames
grep -r "AgentTool\|SearchAgentTool\|BrowserAutomation" ./src

# 4. Deploy GPT-Realtime-1.5 in Foundry
az cognitiveservices account deployment create \
  --name <your-resource> \
  --resource-group <rg> \
  --deployment-name gpt-realtime-1-5 \
  --model-name gpt-realtime-1.5-2026-02-23 \
  --model-format OpenAI \
  --sku-capacity 1 \
  --sku-name Standard
```

---

## Further Reading

- **GPT-Realtime-1.5 & Codex announcement (Foundry Blog, ~Feb 24, 2026):** https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/new-azure-open-ai-models-bring-fast-expressive-and-real%E2%80%91time-ai-experiences-in-m/4496184
- **What's New in Azure OpenAI (Foundry Docs):** https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new
- **What's New in Microsoft Foundry — Dec 2025 & Jan 2026:** https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-dec-2025-jan-2026/
- **Azure Functions MCP Support (InfoQ):** https://www.infoq.com/news/2026/01/azure-functions-mcp-support/
- **Aspire 13.1 Release (InfoQ):** https://www.infoq.com/news/2026/01/dotnet-aspire-13-1-release/
- **Generative AI with LLMs in .NET & C# (2026) (.NET Blog):** https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/
- **AzureML SDK v1 → v2 Migration Guide:** https://learn.microsoft.com/en-us/azure/machine-learning/how-to-migrate-from-v1
- **OpenAI Assistants API Deprecation (Microsoft Q&A):** https://learn.microsoft.com/en-us/answers/questions/5571874/openai-assistants-api-will-be-deprecated-in-august
- **Azure AI Connect Event (March 2–6, 2026):** https://techcommunity.microsoft.com/event/43624d95-1cb4-43ab-8b6e-e67b78fe8b98/azure-ai-connect---march-2-to-march-6-2026/4491662
- **Microsoft Maia 200 Chip for AI Inference (TechCrunch):** https://techcrunch.com/2026/01/26/microsoft-announces-powerful-new-chip-for-ai-inference/