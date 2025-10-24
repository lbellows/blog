---
author: the.serf
date: 2025-10-16 09:00:00 -0400
layout: post
tags:
- azure
- github
- copilot
- integration
- foundry
- claude-haiku-4-5-20251001
title: 'Azure AI Foundry, GitHub Copilot, and .NET 9: What Developers Need to Know
  Right Now'
---
# Azure AI Foundry, GitHub Copilot, and .NET 9: What Developers Need to Know Right Now

**TL;DR**


Azure AI Foundry Agent Service is now generally available with support for multi-agent orchestration, including Semantic Kernel, AutoGen, Agent-to-Agent (A2A), and Model Context Protocol (MCP)
. 
GitHub Copilot has reached 20 million all-time users, adding 5 million users in the last three months
, while 
GitHub Copilot app modernization helps upgrade .NET projects and migrate applications to Azure within Visual Studio
. 
New reasoning models o4-mini and o3 are now available, offering enhanced reasoning, quality, and performance
, and 
.NET 9 elevates cloud-native and intelligent app development with accelerated AI integration
.

## Azure AI Foundry: Enterprise-Grade Agent Development

Microsoft's Build 2025 announcements signal a major shift toward agentic AI workflows. 
Azure AI Foundry is a unified platform for developers to design, customize and manage AI applications and agents
, and the platform now offers significantly expanded capabilities.

### Model Selection and Routing


Azure AI Foundry Models brings Grok 3 and Grok 3 mini models from xAI, with developers now able to choose from more than 1,900 partner-hosted and Microsoft-hosted AI models
. Two new tools simplify model management:

- 
Model Leaderboard ranks top-performing AI models across different categories and tasks

- 
Model router automatically selects the best underlying chat model to respond to a given prompt


For .NET developers, this means you can write against a single endpoint and let Azure route requests to the optimal model based on complexity, cost, and performance requirements.

### Latest Model Releases


The gpt-5, gpt-5-mini, and gpt-5-nano models are now available, with gpt-5-chat also available and gpt-5 available for Provisioned Throughput Units (PTU), though registration is required for access
. 
Azure OpenAI reasoning models are designed to tackle reasoning and problem-solving tasks with increased focus and capability, spending more time processing and understanding requests
.


GPT-image-1 (2025-04-15) features major improvements over DALL-E, including better response to precise instructions, reliable text rendering, and image input acceptance for editing and inpainting
. For video generation workloads, 
Sora (2025-05-02) can create realistic and imaginative video scenes from text instructions
.

### Cost Management with Spillover


Spillover is now Generally Available and manages traffic fluctuations on provisioned deployments by routing overages to a designated standard deployment
. This feature helps balance cost predictability with burst capacity—critical for enterprise applications with variable load patterns.

### Observability and Governance


Azure AI Foundry Observability provides built-in observability into metrics for performance, quality, cost and safety, all incorporated alongside detailed tracing in a streamlined dashboard
. 
Microsoft Entra Agent ID (now in preview) automatically assigns unique identities to agents created in Microsoft Copilot Studio or Azure AI Foundry, helping enterprises securely manage agents and avoid "agent sprawl"
.

## GitHub Copilot: From Assistant to Agent

GitHub Copilot's evolution continues with deeper integration into the development lifecycle and expanded agent capabilities.

### Adoption and Integration


GitHub Copilot is used by 90% of the Fortune 100
, and 
enterprise customer growth has increased about 75% compared to last quarter
. 
GitHub Copilot is evolving from an in-editor assistant to an agentic AI partner, with prompt management, lightweight evaluations and enterprise controls added to GitHub Models
.

### Visual Studio Integration


Starting with Visual Studio 2022 17.14.16, the GitHub Copilot app modernization agent is included with Visual Studio
. This agent addresses one of the most painful developer tasks: upgrading legacy applications. 
The modernization agent supports upgrading C# projects including ASP.NET Core, MVC, Razor Pages, Web API, and .NET Framework technologies like Windows Forms and ASP.NET (currently in preview)
.

To use the modernization agent:

```bash
# Ensure Visual Studio 2022 version 17.14.16 or newer
# Sign in with a GitHub account that has Copilot access
```

Then 
right-click on the solution or project in Solution Explorer and select Modernize, or open the GitHub Copilot Chat window and type @modernize followed by your upgrade or migration request
.

### Azure Boards Integration


Azure Boards integration with GitHub Copilot coding agent (private preview) allows Azure DevOps customers to create a work item, provide instructions in the description, and send it directly to Copilot, which can then fix bugs, implement incremental features, improve test coverage, update documentation, or address technical debt
. 
Copilot receives the work item content, generates a branch and draft pull request linked back to the work item for full traceability, and updates the pull request status on the work item when complete
.

### Open Source Commitment


Microsoft is open-sourcing GitHub Copilot Chat in VS Code, with AI-powered capabilities from GitHub Copilot extensions now part of the same open-source repository
. This move reinforces transparency and enables community contributions to the tooling millions of developers use daily.

## .NET 9 and AI: Microsoft.Extensions.AI


The Microsoft.Extensions.AI libraries provide a unified approach for representing generative AI components, enabling seamless integration and interoperability with various AI services
.

### Core Abstractions


The Microsoft.Extensions.AI.Abstractions package provides core exchange types, including IChatClient and IEmbeddingGenerator, with any .NET library that provides an LLM client able to implement the IChatClient interface
.

Here's a minimal example connecting to Azure OpenAI:

```csharp
using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Extensions.AI;

var endpoint = new Uri(Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT"));
var deployment = Environment.GetEnvironmentVariable("AZURE_OPENAI_GPT_NAME");

IChatClient chatClient = new AzureOpenAIClient(endpoint, new DefaultAzureCredential())
    .AsChatClient(deployment);

var response = await chatClient.CompleteAsync("Explain dependency injection in .NET");
Console.WriteLine(response.Message);
```


Microsoft.Extensions.AI provides delegating IChatClient implementations like DistributedCachingChatClient, which layers caching around another arbitrary IChatClient instance, forwarding novel chat histories to the underlying client and caching responses before returning them
.

### Semantic Kernel and Ecosystem


Semantic Kernel is generally the recommended AI orchestration tool for .NET apps that use one or more AI services, streamlining integration of AI capabilities into existing applications and minimizing the learning curve of working with different AI models
.


Agents are now implemented in a separate package Azure.AI.Agents.Persistent, which gets installed automatically when you install Azure.AI.
