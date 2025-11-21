---
author: the.serf
date: 2025-11-21 06:27:28 -0500
layout: post
tags:
- .net
- azure
- angle
- anthropic
- available
- claude-haiku-4-5-20251001
title: 'Anthropic Claude Models Now Available in Azure AI Foundry: What .NET Developers
  Need to Know'
---

# Anthropic Claude Models Now Available in Azure AI Foundry: What .NET Developers Need to Know

**TL;DR**
Claude Sonnet 4.5, Opus 4.1, and Haiku 4.5 are now part of Microsoft Foundry, making Azure the only cloud offering both OpenAI and Anthropic models
. For .NET developers, this means real choice in model selection, better cost optimization, and tighter integration with Azure's agent tooling—no vendor lock-in required.

---

## Why This Matters for .NET Developers
New Microsoft Foundry updates in preview enable developers to enrich agents with real-time business context, multimodal capabilities and custom business logic through a unified Tools catalog of Model Context Protocol (MCP) servers built with security and governance in mind
. With Anthropic's models now available, you can mix and match—use Claude for reasoning-heavy workloads, OpenAI for multimodal tasks, or cost-optimize by routing simpler requests to Haiku.

### Cost & Latency Wins

The pricing story is compelling.
Claude Haiku 4.5 delivers performance levels comparable to Claude Sonnet 4 at one-third the cost and more than twice the speed
. For .NET teams shipping high-volume applications, this is material:

- **Haiku 4.5**: $1/M input tokens, $5/M output tokens
- **Sonnet 4.5**: $3/M input tokens, $15/M output tokens  
- **Opus 4.1**: $15/M input tokens, $75/M output tokens
Claude Sonnet 4.5 can maintain focus on complex, multi-step tasks for more than 30 hours
—critical for long-horizon agentic workflows in enterprise .NET applications.

## Integration with .NET & Azure
AI-focused capabilities expand through the Microsoft Agent Framework, Microsoft.Extensions.AI, and first-class Model Context Protocol (MCP) support, aiming to standardize patterns for building agentic workflows, integrating external tools, enabling telemetry, and working across multiple AI providers
.

**Practical setup snippet** (C# with Azure SDK):

```csharp
using Azure.AI.Inference;
using Microsoft.Extensions.AI;

var client = new ChatCompletionsClient(
    endpoint: new Uri("https://<your-foundry>.openai.azure.com/"),
    keyCredential: new AzureKeyCredential("<key>")
);

// Route to Anthropic Claude via Foundry
var chatClient = client.AsChatClient("claude-sonnet-4-5");
var response = await chatClient.CompleteAsync("Analyze this codebase for security issues");
```
Managed instance on Azure App Service (Public preview) enables organizations to move web applications to the cloud with just a few configuration changes, and whether .NET web apps are running on-premises or in virtual machines, developers will be able to modernize them into a fully managed platform-as-a-service (PaaS) environment with access to cloud-native scalability, built-in security and Azure's AI capabilities
.

## The Competitive Angle
Anthropic commands 42% of the code generation market—more than double OpenAI's 21% share—according to a Menlo Ventures survey of 150 enterprise technical leaders
. By supporting both vendors in Foundry, Microsoft is hedging against single-vendor risk while letting you choose based on your workload's needs. No more "we're locked into OpenAI" conversations.

## What's Next?
The new Foundry Control Plane gives teams real-time security, lifecycle management, and visibility across agent platforms, and integrates signals from the entire Microsoft Cloud, including Agent 365 and the Microsoft security suite, so builders can optimize performance, apply agent controls, and maintain compliance
.

For .NET developers shipping production agents on Azure, the immediate action item is simple: **test your workloads against Haiku 4.5 first** (it's cheaper and faster for many tasks), then upgrade to Sonnet or Opus only if benchmarks demand it. Use
Model router in Azure AI Foundry to automatically select the optimal Azure OpenAI models for different prompts—boosting quality while reducing costs
—and now you can route to Claude models too.

---

## Further Reading

- https://azure.microsoft.com/en-us/blog/microsoft-foundry-scale-innovation-on-a-modular-interoperable-and-secure-agent-stack/
- https://azure.microsoft.com/en-us/blog/azure-at-microsoft-ignite-2025-all-the-intelligent-cloud-news-explained/
- https://www.infoq.com/news/2025/11/dotnet-10-release/
- https://techcommunity.microsoft.com/blog/Marketplace-Blog/ignite-2025-drive-the-next-era-of-software-innovation-with-ai/4470130
- https://www.infoq.com/news/2025/11/claude-haiku-4-5-release/
- https://venturebeat.com/ai/anthropics-new-claude-can-code-for-30-hours-think-of-it-as-your-ai-coworker/