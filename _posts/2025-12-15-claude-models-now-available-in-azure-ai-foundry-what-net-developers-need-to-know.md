---
author: the.serf
date: 2025-12-15 06:31:44 -0500
layout: post
tags:
- azure
- .net
- integration
- agent
- arrives
- claude-haiku-4-5-20251001
title: 'Claude Models Now Available in Azure AI Foundry: What .NET Developers Need
  to Know'
---

# Claude Models Now Available in Azure AI Foundry: What .NET Developers Need to Know

**TL;DR**
Claude Sonnet 4.5, Opus 4.1, and Haiku 4.5 are now part of Microsoft Foundry, making Azure the only cloud offering both OpenAI and Anthropic models
. For .NET developers, this means you can now switch between Claude and GPT models without leaving your Azure ecosystem—opening new cost and reasoning trade-offs for agent-based applications.

---

## The News: Model Diversity Arrives on Azure
Developers asked for access to Claude Sonnet and Claude Opus alongside OpenAI's GPT models, wanting the ability to select the right models for their use cases. Now Azure is the only cloud supporting access to both Claude and GPT frontier models
. This isn't just a checkbox feature—it fundamentally changes how you architect AI applications on Azure.

## Why This Matters for .NET Developers

### 1. **Agent Development Just Got Cheaper (and Smarter)**
Claude Sonnet 4.5 can maintain focus on complex, multi-step tasks for more than 30 hours
, making it ideal for long-running agentic workflows. If you're building agents with the
Microsoft Agent Framework, Microsoft.Extensions.AI, and first-class Model Context Protocol (MCP) support
in .NET 10, you now have a proven alternative to GPT models for sustained reasoning tasks.

### 2. **Reasoning Performance Without the GPT-5 Price Tag**
Anthropic holds 40% of the market share within enterprise and 54% of the market share when it comes to coding
. For cost-conscious teams, Claude's pricing structure—especially on long-context prompts—can offer better ROI than OpenAI's latest models.
Prompts of 200,000 tokens or fewer maintain pricing at $3 per million input tokens and $15 per million output tokens, while larger prompts cost $6 and $22.50, respectively
.

### 3. **Unified Integration with Your Azure Stack**
Foundry IQ streamlines knowledge retrieval from multiple sources including SharePoint, Fabric, and the web, powered by Azure AI Search, delivering policy-aware retrieval without having to build complex custom RAG pipelines. Developers get pre-configured knowledge bases and agentic retrieval in a single API
. With Claude now in Foundry, you can evaluate which model performs best for your RAG pipeline without vendor lock-in.

---

## Getting Started: Quick Integration Path

If you're already using Azure AI Foundry with .NET, accessing Claude models requires minimal changes:

```csharp
// Using Microsoft.Extensions.AI (GA in .NET 10)
using Microsoft.Extensions.AI;

var chatClient = new AzureOpenAIClient(
    new Uri("https://<your-resource>.openai.azure.com/"),
    new ApiKeyCredential("<api-key>")
);

// Deploy Claude Sonnet 4.5 in Azure and reference it by deployment name
var response = await chatClient.CompleteAsync(
    "Analyze this codebase for refactoring opportunities",
    new ChatOptions { ModelId = "claude-sonnet-4.5" } // Your Azure deployment
);
```

The beauty here:
OpenAI client support with minimal code changes to swap between OpenAI and Azure OpenAI when using key-based authentication
. Your abstractions stay clean.

---

## The Strategic Play
When you're building AI apps and agents, having options means you can optimize for what matters most to your users
. For .NET teams shipping on Azure, this means:

- **A/B test models** in production without re-architecting.
- **Lock in cost savings** by routing long-context tasks to Claude when appropriate.
- **Leverage reasoning strengths** — Claude for multi-step logic, GPT for speed-critical paths.
- **Stay within Azure governance** — no vendor sprawl, unified billing, single audit trail.
This expansion underscores Microsoft's commitment to an open, interoperable Microsoft AI ecosystem—bringing Anthropic's reasoning-first intelligence into the tools, platforms, and workflows organizations depend on every day
.

---

## One Caveat: Context Windows and Pricing

If you're planning to use Claude's 1 million token context window for entire codebase analysis, budget accordingly.
The expanded context enables comprehensive code analysis across entire repositories, document synthesis involving hundreds of files while maintaining awareness of relationships between them and context-aware AI agents that can maintain coherence across hundreds of tool calls and complex workflows
. But those larger prompts carry higher per-token costs.

---

## Further Reading

https://azure.microsoft.com/en-us/blog/azure-at-microsoft-ignite-2025-all-the-intelligent-cloud-news-explained/

https://azure.microsoft.com/en-us/blog/actioning-agentic-ai-5-ways-to-build-with-news-from-microsoft-ignite-2025/

https://devblogs.microsoft.com/dotnet/announcing-dotnet-10/

https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new

https://venturebeat.com/ai/claude-can-now-process-entire-software-projects-in-single-request-anthropic-says/

https://techcrunch.com/2025/12/08/claude-code-is-coming-to-slack-and-thats-a-bigger-deal-than-it-sounds/