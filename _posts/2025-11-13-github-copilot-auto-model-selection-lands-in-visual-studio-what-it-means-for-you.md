---
author: the.serf
date: 2025-11-13 06:28:57 -0500
layout: post
tags:
- how
- matters
- why
- .net
- auto
- claude-haiku-4-5-20251001
title: GitHub Copilot Auto Model Selection Lands in Visual Studio—What It Means for
  Your Shipping Velocity
---

# GitHub Copilot Auto Model Selection Lands in Visual Studio—What It Means for Your Shipping Velocity

**TL;DR**
GitHub Copilot in Visual Studio now includes an Auto option you can select from the model picker where Copilot picks the model for you, available on all Copilot plans
. No more manual model selection overhead; Copilot handles routing based on availability and performance. Early preview, but it's worth enabling now.

---

## The Problem You Didn't Know You Had

If you've been using GitHub Copilot in Visual Studio, you've probably noticed the model picker. GPT-4o for complex refactoring. GPT-4o mini for quick fixes. It's like choosing the right tool from your toolbox—except you have to choose it every time.

For teams shipping .NET and Azure workloads, this context-switching adds friction. You're mid-flow, thinking about your domain logic, and suddenly you're context-switching to think about LLM inference costs and latency profiles. That's not what "AI-powered productivity" should feel like.
GitHub Copilot in Visual Studio now includes an Auto option you can select from the model picker where Copilot picks the model for you
.

## How It Works

The Auto model selection feature does what its name suggests:
it picks the best available model for each request based on current capacity and performance, and with auto, you don't need to choose a specific model
.

This is more than cosmetic convenience. It's a **cost and latency optimization layer** that sits between your IDE and Azure OpenAI's infrastructure. Think of it as a built-in load balancer for your coding session.

### Practical Setup

If you're on Copilot Business or Enterprise:

```
1. Open Visual Studio
2. Locate the Copilot model picker (usually in the chat panel or editor context)
3. Select "Auto" instead of a specific model
4. Your administrator must enable the Editor preview features policy
```
If you're a Copilot Business or Copilot Enterprise subscriber, an administrator will have to enable the Editor preview features policy before you can use it
.

For Copilot Pro and Pro Plus users, it's already available—no admin gate.

## Why This Matters for .NET & Azure Developers

**Cost Optimization**:
Faster responses, a lower chance of rate limiting, and 10% off premium requests for paid users
. If you're shipping on Azure, every basis point of cost reduction compounds across your team.

**Latency Consistency**:
While this preview of auto optimizes for availability, Microsoft is actively working on future updates to make it more intelligent to account for your task
. Translation: they're building task-aware routing. Refactoring a large codebase? The system learns to route to a more capable model. Autocompleting a simple line? Lighter model. Eventually.

**Less Friction in the SDLC**: You stay in flow. Your fingers don't leave the keyboard to think about model selection. That's the entire point of AI-powered tools—they should disappear into your workflow, not become another decision point.

## The Caveat (And Why It Matters)
This preview of auto optimizes for availability
, not necessarily for optimal reasoning quality on your specific task. If you're debugging a gnarly multi-threaded issue in a .NET service and need GPT-4o's deeper reasoning, you might still want to override Auto and pick explicitly.

But for the 80% case—refactoring, documentation, boilerplate generation, test writing—Auto should do the right thing.

---

## Looking Ahead: The Bigger Picture

This feature is part of a larger GitHub Copilot evolution.
GitHub is deprecating GitHub Copilot Extensions (built as GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers, which provide a universal standard for AI agent integration
.

Auto model selection is the *consumer-facing* side of that shift. Under the hood, GitHub is building infrastructure that can route work intelligently across a heterogeneous set of models and services. MCP servers standardize how agents talk to tools. Auto model selection standardizes how you, the developer, interact with those agents without thinking about it.

It's a small feature with big architectural implications.

---

## How to Enable It Now

1. **Update Visual Studio** to the latest preview build.
2. **Check your Copilot plan** (Pro, Business, or Enterprise).
3. **Enable the Editor preview features policy** if you're on Business/Enterprise.
4. **Select Auto from the model picker** and let it run for a week.
5. **Collect feedback** in the GitHub Community discussions—Microsoft is actively iterating.

---

## Further Reading

- https://github.blog/changelog/2025-11-11-auto-model-selection-for-copilot-in-visual-studio-in-public-preview/
- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://github.blog/changelog/2025-10-28-github-copilot-in-visual-studio-code-gets-upgraded/
- https://azure.microsoft.com/en-us/blog/github-universe-2025-where-developer-innovation-took-center-stage/
- https://github.blog/changelog/2025-11-05-copilot-coding-agent-now-supports-pull-request-templates/
- https://devblogs.microsoft.com/