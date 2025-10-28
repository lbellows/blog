---
author: the.serf
date: 2025-10-28 07:26:43 -0400
layout: post
tags:
- .net
- production
- actually
- agent
- agents
- claude-haiku-4-5-20251001
title: 'Microsoft Agent Framework Preview: Build Production AI Agents in .NET with
  Fewer Headaches'
---

# Microsoft Agent Framework Preview: Build Production AI Agents in .NET with Fewer Headaches

**TL;DR**
Microsoft Agent Framework is now available in preview through GitHub and package managers for both Python and .NET ecosystems.
It unifies Semantic Kernel and AutoGen, eliminating the old choice between innovation and production stability.
Developers can build AI agents with minimal code—functional agents in fewer than twenty lines of code.
---

## The Problem It Solves

If you've been wrestling with multi-agent orchestration in .NET, you know the pain:
Semantic Kernel provided enterprise-ready foundations, while AutoGen offered experimental multi-agent orchestration, forcing developers to choose between innovation and production stability.
That trade-off is gone.

## What's Actually New
The framework is available immediately in preview through NuGet packages for .NET environments.
Here's what matters for your stack:

### For .NET Developers
Native support for Azure AI Foundry services, OpenTelemetry instrumentation for monitoring, and compatibility with Visual Studio Code through the AI Toolkit extension.
Translation: your observability and deployment story just got simpler.
The framework supports sequential, concurrent, group chat, and handoff orchestration patterns—originally research prototypes in AutoGen, now with production-grade durability and enterprise controls.
### Getting Started (The Fun Part)

Install the preview package:

```bash
dotnet add package Microsoft.Agents.AI --prerelease
```

Here's a minimal agent using GitHub Models:

```csharp
using Microsoft.Extensions.AI;
using Microsoft.Agents.AI;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel;

IChatClient chatClient = new ChatClient(
    "gpt-4o-mini",
    new ApiKeyCredential(Environment.GetEnvironmentVariable("GITHUB_TOKEN")!)
) { Endpoint = new Uri("https://models.github.ai/inference") }
    .AsIChatClient();

AIAgent writer = new ChatClientAgent(
    chatClient,
    new ChatClientAgentOptions {
        Name = "Writer",
        Instructions = "Write stories that are engaging and creative."
    }
);

AgentRunResponse response = await writer.RunAsync("Write a short story about a haunted house.");
Console.WriteLine(response.Text);
```

That's it.
"Building AI agents shouldn't be rocket science,"
as the .NET team puts it—and they mean it.

### Azure & GitHub Integration
The framework enables Model Context Protocol (MCP) support, Agent-to-Agent (A2A) communication, and OpenAPI-based integration, ensuring portability across different runtime environments.
It includes modular connectors to Azure AI Foundry, Microsoft Graph, SharePoint, Elastic, Redis, and additional services.
### Production Readiness

This isn't a toy.
Built-in observability through OpenTelemetry, integration with Azure Monitor, Entra ID security authentication, and CI/CD compatibility using GitHub Actions and Azure DevOps.
---

## The Practical Win

![A robot sitting at a desk looking confused at a whiteboard covered in "Semantic Kernel vs. AutoGen" with a "Why not both?" meme caption](assets/images/robot.webp)

*Your agent framework dilemma, solved.*

The real story here:
Microsoft has provided migration guides for developers currently using Semantic Kernel or AutoGen, meaning you can preserve your existing investments while unlocking new capabilities.
No rip-and-replace nightmares.

For teams building on Azure, this consolidation means one mental model for orchestrating agents across your entire stack—from local dev boxes to production Kubernetes clusters.

---

## What's Next
The AI Toolkit for VS Code v0.24.0 introduces groundbreaking GitHub Copilot Tools Integration, making AI-powered development more seamless.
The tool provides best practices, guidance, steps, and code samples on Microsoft Agent Framework for GitHub Copilot, ensuring you follow the latest patterns whether you're building your first agent or scaling complex multi-agent systems.
---

## Further Reading

- https://devblogs.microsoft.com/dotnet/introducing-microsoft-agent-framework-preview/
- https://github.com/microsoft/agents
- https://learn.microsoft.com/en-us/azure/ai-foundry/whats-new-azure-ai-foundry
- https://techcommunity.microsoft.com/blog/azuredevcommunityblog/ai-toolkit-for-vs-code-october-update/4463365
- https://www.infoq.com/news/2025/10/microsoft-agent-framework/
- https://github.blog/changelog/2025-10-17-gpt-4-1-copilot-code-completion-model-october-update/