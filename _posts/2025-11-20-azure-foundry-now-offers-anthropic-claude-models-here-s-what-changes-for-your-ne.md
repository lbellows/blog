---
author: the.serf
date: 2025-11-20 06:28:08 -0500
layout: post
tags:
- .net
- azure
- foundry
- via
- agents
- claude-haiku-4-5-20251001
title: Azure Foundry Now Offers Anthropic Claude Models—Here's What Changes for Your
  .NET Apps
---

# Azure Foundry Now Offers Anthropic Claude Models—Here's What Changes for Your .NET Apps

**TL;DR:**
Claude Sonnet 4.5, Opus 4.1, and Haiku 4.5 are now part of Microsoft Foundry, making Azure the only cloud offering both OpenAI and Anthropic models.
Starting in August 2025, you can now opt in to next generation v1 Azure OpenAI APIs which add support for ongoing access to the latest features with no need to specify new api-versions each month.
Plus:
The Realtime API now supports WebRTC, enabling real-time audio streaming and low-latency interactions, ideal for applications requiring immediate feedback, such as live customer support or interactive voice assistants.
## The Story: Multi-Model Choice on Azure

For the past year, Azure developers choosing frontier LLMs were largely locked into OpenAI's family. That just changed.
Earlier this year, Anthropic models were brought to Microsoft 365 Copilot, GitHub Copilot, and Copilot Studio. Today, Claude Sonnet 4.5, Opus 4.1, and Haiku 4.5 are now part of Microsoft Foundry, advancing the mission to give customers choice across the industry's leading frontier models—and making Azure the only cloud offering both OpenAI and Anthropic models. This expansion underscores a commitment to an open, interoperable Microsoft AI ecosystem.
Why does this matter? **Cost and reasoning tradeoffs.** Claude models—especially Opus—are known for strong reasoning and nuance. Haiku is lean and fast. Now you can benchmark both families in the same managed environment without vendor lock-in friction.

## What This Means for .NET Developers

### 1. **Model Selection via Microsoft Foundry**
Microsoft Foundry is evolving into the single destination for building AI applications and agentic systems, bringing the entire development lifecycle into one unified experience. From model selection and evaluation to safety, observability, deployment, and connector integrations, Foundry gives developers one place to design, build, and operationalize agents.
For .NET, this means you can now prototype with Claude in Azure's managed portal, then deploy via the same infrastructure you're already using for OpenAI models.

### 2. **Simplified API Versioning with v1 APIs**
Starting in August 2025, you can opt in to next generation v1 Azure OpenAI APIs which add support for ongoing access to the latest features with no need to specify new api-versions each month. api-version is no longer a required parameter with the v1 GA API. The v1 API removes this dependency by adding automatic token refresh support to the OpenAI() client.
**Practical win:** Your .NET code stops chasing API versions every few months.

```csharp
// Old way: specify api-version, manage token refresh manually
var client = new AzureOpenAIClient(
    new Uri("https://YOUR-RESOURCE.openai.azure.com"),
    new AzureKeyCredential(apiKey),
    new OpenAIClientOptions { ApiVersion = "2024-10-21" }
);

// New way: v1 API handles versioning and token refresh
var client = new OpenAI.OpenAIClient(
    apiKey: Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY"),
    baseUrl: new Uri("https://YOUR-RESOURCE.openai.azure.com/openai/v1/")
);
```

### 3. **Real-Time Audio via WebRTC**
The Realtime API now supports WebRTC, enabling real-time audio streaming and low-latency interactions. This feature is ideal for applications requiring immediate feedback, such as live customer support or interactive voice assistants.
If you're building voice agents in .NET, this is a latency win—WebRTC replaces older TCP/HTTP polling patterns. Combined with
the gpt-4o-transcribe-diarize speech to text model, an Automatic Speech Recognition (ASR) model that converts spoken language into text in real time with ultra-low latency and high accuracy across 100+ languages, essential for workflows where voice data drives decisions—such as customer support, virtual meetings, and live events
—you have a production-ready stack.

### 4. **Integration with .NET Aspire & Agents**
AI-focused capabilities expand through the Microsoft Agent Framework, Microsoft.Extensions.AI, and first-class Model Context Protocol (MCP) support. These systems aim to standardize patterns for building agentic workflows, integrating external tools, enabling telemetry, and working across multiple AI providers.
More than 1,400 business systems—including SAP, Salesforce, ServiceNow, and Workday—are now available as Model Context Protocol (MCP) tools through Logic Apps connectors. Customers can also make internal REST APIs or custom tools MCP tools available using API Management and API Center.
This means your .NET agents can reach Salesforce, ServiceNow, or your custom APIs with minimal glue code.

## The Bigger Picture
New Microsoft Foundry updates in preview will enable developers to enrich agents with real-time business context, multimodal capabilities and custom business logic through a unified Tools catalog of Model Context Protocol (MCP) servers built with security and governance in mind. The catalog includes unified tool discovery, deep business integration, new tools for prebuilt AI services, and custom tool extensibility.
For .NET shops, this is the moment to consolidate. You're no longer choosing between "Azure OpenAI" and "Anthropic in some other cloud." You're choosing models, not clouds.

## Next Steps

1. **Audit your current deployments.** Are you on the old versioned APIs? Migrate to v1 to reduce maintenance debt.
2. **Prototype with Claude.** If your use case needs reasoning depth, test Opus or Sonnet 4.5 in Foundry's evaluation UI.
3. **Leverage MCP.** If you're building agents, start mapping your business systems to MCP tools now.
4. **Plan for voice.** If you're considering real-time audio, WebRTC support removes a technical blocker.

---

## Further reading

- https://azure.microsoft.com/en-us/blog/azure-at-microsoft-ignite-2025-all-the-intelligent-cloud-news-explained/
- https://techcommunity.microsoft.com/blog/Marketplace-Blog/ignite-2025-drive-the-next-era-of-software-innovation-with-ai/4470130
- https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation
- https://learn.microsoft.com/en-us/azure/ai-services/openai/whats-new
- https://techcommunity.microsoft.com/blog/AppsonAzureBlog/azure-app-platform-at-ignite-2025-new-innovations-for-all-your-apps-and-agents/4470759
- https://www.infoq.com/news/2025/11/dotnet-10-release/