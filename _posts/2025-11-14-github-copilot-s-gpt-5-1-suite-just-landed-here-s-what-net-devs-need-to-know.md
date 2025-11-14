---
author: the.serf
date: 2025-11-14 06:28:07 -0500
layout: post
tags:
- .net
- just
- agent
- better
- bigger
- claude-haiku-4-5-20251001
title: GitHub Copilot's GPT-5.1 Suite Just Landed—Here's What .NET Devs Need to Know
---

# GitHub Copilot's GPT-5.1 Suite Just Landed—Here's What .NET Devs Need to Know

**TL;DR**
GPT-5.1, GPT-5.1-Codex, and GPT-5.1-Codex-Mini are now rolling out in public preview in GitHub Copilot
. The new models are available across VS Code, JetBrains, and Xcode with specialized variants for code tasks. If you're shipping .NET on Azure and GitHub, this is your upgrade path—but billing changes and admin policies are coming, so plan accordingly.

---

## What Just Shipped
GitHub Copilot now offers GPT-5.1, GPT-5.1-Codex, and GPT-5.1-Codex-Mini to Copilot Pro, Pro+, Business, and Enterprise subscribers
. The key differentiator: GPT-5.1-Codex and GPT-5.1-Codex-Mini are purpose-built for code generation and reasoning, not just general text.

**Model availability by IDE:**
GPT-5.1 is available in Visual Studio Code in all modes (chat, ask, edit, agent), JetBrains in all modes (ask, edit, agent), Xcode in all modes (ask, agent), Eclipse in all modes (ask, agent), github.com, GitHub Mobile (iOS and Android), and Copilot CLI. GPT-5.1-Codex and GPT-5.1-Codex-Mini are available in Visual Studio Code versions 1.104.1 and later in all modes, and GitHub Copilot for JetBrains versions 1.5.61 and later in all modes
.

---

## Why This Matters for .NET Developers

If you're building on .NET with Azure and GitHub, this release addresses three pain points:

### 1. **Better Reasoning for Complex Refactoring**
AI-focused capabilities expand through the Microsoft Agent Framework, Microsoft.Extensions.AI, and first-class Model Context Protocol (MCP) support, aiming to standardize patterns for building agentic workflows, integrating external tools, enabling telemetry, and working across multiple AI providers
. The GPT-5.1-Codex models excel at understanding your .NET architecture and suggesting multi-file refactors.

### 2. **Faster Agent Mode Workflows**
GitHub Copilot is evolving from an in-editor assistant to an agentic AI partner with a first-of-its-kind asynchronous coding agent integrated into the GitHub platform
. With GPT-5.1-Codex handling the reasoning, agent mode can now tackle longer-running tasks—like generating Entity Framework migrations or scaffolding ASP.NET Core endpoints—without hallucinating.

### 3. **Cost Predictability**
Starting in November 2025, each AI tool will have a dedicated SKU for tracking and managing premium request usage, beginning with coding agent and Spark
. This means you can now budget separately for Copilot code review vs. agent tasks vs. chat—critical for enterprise teams.

---

## How to Enable It

**For Pro and Pro+ users:**
Users can enable the model by selecting it in the model picker and confirming the one-time prompt
.

**For Business and Enterprise:**
Administrators must enable the OpenAI GPT-5.1, GPT-5.1-Codex, or GPT-5.1-Codex-Mini policy in Copilot settings, and once enabled, users in that organization will see the respective model in the Copilot Chat model picker
.

**Bring-your-own-key option:**
Select Manage Models from the picker, choose OpenAI GPT-5.1, GPT-5.1-Codex, or GPT-5.1-Codex-Mini, and enter your API key when prompted
.

---

## A Quick Integration Pattern for .NET

Here's a minimal example of how to wire up the new models in a .NET agent using Microsoft.Extensions.AI:

```csharp
var client = new OpenAIClient(new ApiKeyCredential(apiKey));

var chatClient = client.AsChatClient("gpt-5.1-codex");

var messages = new List<ChatMessage>
{
    new UserChatMessage("Refactor this Entity Framework query to use async/await")
};

var response = await chatClient.CompleteAsync(messages);
Console.WriteLine(response.Content[0].Text);
```

The agent can now run this in the background while you work on other tasks.

---

## Watch Out: Billing Changes Ahead
Starting December 2, 2025, GitHub will remove all $0 Copilot premium request budgets for enterprise and team accounts created before August 22, 2025, and as a result, premium request paid usage will be governed by your account's premium request paid usage policy, not a static $0 budget
.

**Action item:** If you're on an enterprise plan with a $0 budget, either set a spending cap or enable paid premium requests before December 2.

---

## Rollout Timeline
Rollout will be gradual, and if you don't see the new models yet, check back soon
. Early adopters in the community are already reporting faster code generation and fewer off-topic suggestions.

---

## The Bigger Picture

This release slots neatly into Microsoft's broader AI strategy:
Microsoft announced the general availability of .NET 10, described as the most productive, modern, secure, and high-performance version of the platform to date, with improvements across the runtime, libraries, languages, tools, frameworks, and workloads
. Combined with
Entity Framework Core 10 bringing powerful improvements for data access, including AI-ready vector search, enhanced JSON support, and better complex type handling
, you've got a cohesive stack for shipping AI-native applications on Azure.

---

## Further Reading

- https://github.blog/changelog/2025-11-13-openais-gpt-5-1-gpt-5-1-codex-and-gpt-5-1-codex-mini-are-now-in-public-preview-for-github-copilot/
- https://devblogs.microsoft.com/dotnet/announcing-dotnet-10/
- https://github.blog/changelog/2025-11-10-raptor-mini-is-rolling-out-in-public-preview-for-github-copilot/
- https://devblogs.microsoft.com/all-things-azure/announcing-general-availability-of-github-copilot-for-azure-now-with-agent-mode/
- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://learn.microsoft.com/en-us/dotnet/ai/overview
- https://devblogs.microsoft.com/semantic-kernel/microsoft-extensions-ai-simplifying-ai-integration-for-net-partners/