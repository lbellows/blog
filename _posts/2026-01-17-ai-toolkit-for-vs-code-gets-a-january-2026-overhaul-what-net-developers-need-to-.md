---
author: the.serf
date: 2026-01-17 06:27:58 -0500
layout: post
tags:
- .net
- anthropic
- auth
- bottom
- code
- claude-haiku-4-5-20251001
title: 'AI Toolkit for VS Code Gets a January 2026 Overhaul: What .NET Developers
  Need to Know'
---

# AI Toolkit for VS Code Gets a January 2026 Overhaul: What .NET Developers Need to Know

**TL;DR**
Microsoft shipped a major AI Toolkit update for VS Code designed to streamline building, testing, and deploying AI agents, with focus on GitHub Copilot standards, debugging tools, and Microsoft Foundry support
. Key win:
the shift from Copilot Instructions to Copilot Skills now equips GitHub Copilot with specialized agent-building capabilities while improving integration within GitHub Copilot Chat
. If you're shipping agents on .NET or Azure, this reduces friction and cost.

---

## The Shift: From Instructions to Skills
The biggest architectural change in v0.28.1 is the transition from Copilot Instructions to Copilot Skills
. For .NET developers, this matters because it moves agent development from a generic instruction layer to a specialized, reusable skill set. Think of it as moving from "tell Copilot what to do" to "give Copilot a toolkit it can reason about."
The custom agent now has deeper understanding of workflow code generation and evaluation planning/execution
, which translates to faster iteration when building multi-step workflows—exactly what agentic systems need.

## Foundry-First Development
The toolkit now provides cost-efficient support for enterprise-grade models via Microsoft Foundry and Agent Framework
. Here's what that unlocks:

- **Local testing without blowing budget**:
Testing new models and code without blowing through budget, plus building CI/CD pipelines with minimal overhead that don't require a third-party hosted account
.
- **Foundry v2 by default**:
Code generation for agents now defaults to Foundry v2
, meaning your scaffolding is aligned with Microsoft's latest enterprise platform.
- **Evaluation tooling**:
You can now generate evaluation code directly within the toolkit to create and run evaluations in Microsoft Foundry
—no context-switching to external test runners.

## Practical Integration: Anthropic Models & Entra Auth
The v0.28.0 milestone expanded the Agent Builder and Playground to support Anthropic models using Entra Auth types, providing enterprise developers a secure way to leverage Claude models within the Agent Framework while maintaining strict authentication standards
.

**Why this matters**: You're no longer locked into OpenAI-only workflows. If your team standardizes on Claude for certain tasks (reasoning, long-context analysis), you can now use it securely within the same VS Code environment, with Azure identity management built in.

## Windows ML Profiling & Performance
Version 0.28.0 introduces profiling features for Windows ML-based local models, allowing you to monitor performance and resource utilization directly within VS Code
. For .NET developers running agents on Windows machines (common in enterprise), this is a game-changer—you can now see latency and memory footprint before shipping to Azure.

## What's Fixed
Recent fixes resolved a crash in Codespaces when selecting images, fixed a delay where newly added models wouldn't appear in "My Resources," and fixed an issue where non-empty content was required for Claude models
. If you've hit these, update immediately.

---

## The Bottom Line
As a .NET Developer you shouldn't have to choose a single provider or lock into a single solution
. This update reinforces that philosophy. You get Foundry for enterprise scale, local Ollama or Windows ML for cost control, and now Claude as a first-class option alongside OpenAI. The Skills architecture and Entra Auth support make it all feel native to your .NET and Azure stack—no cobbling together separate SDKs or auth flows.

If you're building agents in 2026, install the update and spend an hour exploring the Foundry v2 integration and eval tooling. The time saved will pay for itself on your first production deployment.

---

## Further Reading

https://techcommunity.microsoft.com/blog/azuredevcommunityblog/%F0%9F%9A%80-ai-toolkit-for-vs-code-january-2026-update/4485205

https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/

https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/unlocking-hugging-face-gated-models-in-microsoft-foundry/4485722

https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new?view=foundry-classic

https://devblogs.microsoft.com/all-things-azure/the-realities-of-application-modernization-with-agentic-ai-early-2026/