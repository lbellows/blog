---
author: the.serf
date: 2025-10-25 07:24:49 -0400
layout: post
tags:
- copilot
- model
- enable
- enterprise
- migration
- claude-haiku-4-5-20251001
title: 'GitHub Copilot Model Deprecation: Your Migration Checklist for October 2025'
---

# GitHub Copilot Model Deprecation: Your Migration Checklist for October 2025

**TL;DR**
Selected Claude, OpenAI, and Gemini Copilot models were deprecated across all GitHub Copilot experiences on October 23, 2025
. If you're pinning specific models in your workflows, agent configurations, or integrations, you need to update now. The good news:
Anthropic Claude 3.7 Sonnet, Claude 3.5 Sonnet, OpenAI o3-mini, and Google Gemini Flash 2.0 are now generally available in GitHub Copilot
as stable replacements.

---

## What Just Happened (And Why It Matters)

Two days ago, GitHub quietly sunsetted a batch of older models across Copilot Chat, inline edits, agent mode, and code completions. This isn't a surprise—the industry moves fast, and model providers ship new versions constantly. But if your team has hardcoded model selectors or relies on specific model behavior in automation, this is a breaking change that hits your CI/CD pipeline.

The deprecation affects developers at all tiers: Copilot Pro, Pro+, Business, and Enterprise.
Copilot Enterprise administrators may need to enable access to alternative models through their model policies in Copilot settings, which can be verified by checking individual Copilot settings and confirming that the policy is enabled for the specific model
.

---

## The Migration Path: Three Steps

### 1. **Audit Your Model Pinning**

If you're using GitHub Copilot's API or integrations, search your codebase for hardcoded model names. Common culprits:

```csharp
// ❌ Old pattern (likely deprecated)
var client = new CopilotClient(model: "claude-3-sonnet");

// ✅ New pattern
var client = new CopilotClient(model: "claude-3.7-sonnet");
```
GitHub Copilot's custom completion model now delivers suggestions with 20% more accepted and retained characters, 12% higher acceptance rate, 3x higher token-per-second throughput, and a 35% reduction in latency
—so the new models aren't just replacements; they're improvements.

### 2. **Enable Policies in Copilot Enterprise**

If you run Copilot Enterprise,
once enabled, you'll see the model in the Copilot Chat model selector in VS Code and on github.com
. This is a one-time admin step per organization:

```bash
# In your Copilot Enterprise settings:
# Settings > Copilot > Model policies
# Enable: Claude 3.7 Sonnet, o3-mini, Gemini 2.0 Flash
```

### 3. **Test Agent Workflows**
Copilot coding agent is an asynchronous, autonomous background agent that delegates tasks and opens a draft pull request, and it can now search the web to gather extra context and supplement its existing knowledge
. If you're using agent mode for automated code generation or refactoring, run a test workflow against the new models in a feature branch before promoting to production.

---

## Which Model Should You Pick?
Claude 3.7 Sonnet excels in development tasks that require structured reasoning across large or complex codebases, Claude 3.5 Sonnet remains a good choice for everyday coding support, OpenAI o3-mini is a fast, cost-effective reasoning model designed to deliver coding performance while maintaining lower latency and resource usage, and Gemini 2.0 Flash is Google's model optimized for fast responses and multimodal interactions
.

For .NET teams specifically,
Microsoft has gone all-in on making AI development in .NET easy and powerful, with tooling around LLMs, Microsoft Extensions for AI (now generally available), Semantic Kernel, and AI agents getting really mature
. If you're using Azure OpenAI or GitHub Models with .NET, the new models integrate seamlessly via the existing SDKs.

---

## The Silver Lining: Faster, Smarter Completions

This deprecation cycle is actually good news.
The average wall clock time per-task dropped 25%, with the median wall clock time dropping 45%, and Copilot now responds more concisely to simple questions, delivering answers faster and keeping you focused on the task at hand
. Your developers will feel the speed improvement immediately.

---

## Action Items for Your Team

- [ ] Review `.copilot` or model configuration files in your repos
- [ ] Update any CI/CD workflows that reference deprecated models
- [ ] Test Copilot Chat and agent mode with the new models in a staging environment
- [ ] If Enterprise: enable new model policies in admin settings
- [ ] Document your team's preferred model choice in your coding standards
No action is required to remove the deprecated models
—they'll simply stop working. But proactive migration now saves you from firefighting when a developer's workflow breaks mid-sprint.

---

## Further Reading

- https://github.blog/changelog/2025-10-23-selected-claude-openai-and-gemini-copilot-models-are-now-deprecated/
- https://github.blog/changelog/2025-10-17-gpt-4-1-copilot-code-completion-model-october-update/
- https://github.blog/ai-and-ml/github-copilot/the-road-to-better-completions-building-a-faster-smarter-github-copilot-with-a-new-custom-model/
- https://github.blog/changelog/2025-10-16-copilot-coding-agent-can-now-search-the-web/
- https://github.blog/changelog/2025-04-04-multiple-new-models-are-now-generally-available-in-github-copilot/
- https://learn.microsoft.com/en-us/dotnet/ai/overview