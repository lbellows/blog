---
author: the.serf
date: 2025-11-02 06:24:47 -0500
layout: post
tags:
- .net
- azure
- copilot
- november
- .net-specific
- claude-haiku-4-5-20251001
title: 'AI Agents, Model Context Protocol, and the Great Copilot Pivot: Your November
  2025 Briefing'
---

# AI Agents, Model Context Protocol, and the Great Copilot Pivot: Your November 2025 Briefing

**TL;DR:**
GitHub is sunsetting Copilot Extensions (GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers
.
Over 1.1 million public repositories now use an LLM SDK, with 693,867 created in the past 12 months
.
GitHub Copilot now defaults to GPT-4.1 across chat, agent mode, and code completions, optimized for speed, reasoning, and context handling
. Azure AI Foundry is rolling out multimodal models and agentic observability. For .NET shops, it's time to migrate to MCP and evaluate your model routing strategy before year-end.

---

## The Big Shift: Extensions → MCP (Deadline: November 10)
Model Context Protocol provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot
. This is a seismic change for teams that built GitHub App–based Copilot Extensions.

**What this means for you:**
-
MCP servers offer cross-platform compatibility, more modular and composable architecture, simplified maintenance, and better performance
.
-
MCP servers support individual tool-calling with "#" symbol in IDEs instead of @mentions, and autonomous tool invocation by Agent Mode and Copilot Coding Agent
.

**Action item:** If you maintain a Copilot Extension,
read the MCP server developer documentation to learn more about building an MCP server
.
The GitHub MCP Registry is live now, providing a curated directory of MCP servers, and users can also discover MCP servers by browsing repositories on GitHub
.

---

## GitHub Copilot: From Autocomplete to Autonomous Agent

The transformation is real.
If 2024 was about showing what's possible with AI, 2025 is about making it practical
.

### Performance Gains Are Measurable
GitHub is now delivering suggestions with 20% more accepted and retained characters, 12% higher acceptance rate, 3x higher token-per-second throughput, and a 35% reduction in latency
. That's not marketing fluff—that's measurable developer velocity.

### Code Review Gets Smarter
Copilot code review now blends LLM detections and tool calling with deterministic tools like ESLint and CodeQL, leveraging agentic tool calling to actively gather full project context, including code, directory structure, and references, enabling it to understand how changes fit within the broader project architecture
.

### Multi-IDE Parity
Agent mode is now available in Xcode, Eclipse, Jetbrains, and Visual Studio
.
Same Copilot, wherever you build
.

### .NET-Specific Wins

For .NET developers:
Two popular refactorings—Implement Method and Implement Interface—now let you automatically generate methods, and once you've used one of these refactorings, you can select the lightbulb (CTRL + .) and choose the new Implement with Copilot refactoring, which will add the body to your method
.

---

## Azure AI Foundry: Multimodal & Agentic
With the launch of OpenAI GPT-image-1-mini, GPT-realtime-mini, and GPT-audio-mini, plus major safety upgrades to GPT-5, the models announced by OpenAI are rolling out now in Azure AI Foundry, with most customers being able to get started on October 7, 2025
.

### Key Additions for Developers

-
Agentic retrieval is now possible through Azure AI Search, using advanced techniques to improve answer relevance by up to ~40% on complex, multi-part questions in early tests
.
-
Foundry Observability is now in preview, giving developers end-to-end monitoring, built-in metrics, and detailed trace logs of the reasoning steps and tool calls made by agents
.
-
Model router in Azure AI Foundry allows developers to automatically select the optimal Azure OpenAI models for different prompts—boosting quality while reducing costs
.

### .NET + Azure AI Integration
The first stable release of the Azure AI Foundry library for .NET provides comprehensive access to Azure AI Foundry Project resources, introduces important API improvements with consistent AIProjectDefix for key models, and uses the v1 AI Foundry data plane REST APIs with support for authentication via Microsoft Entra ID for secure, keyless access
.

---

## .NET Ecosystem: Building Blocks Are Ready
The Microsoft.Extensions.AI libraries provide a unified approach for representing generative AI components, enabling portability across models and services, facilitating testing and mocking, and leveraging middleware provided by the ecosystem
.

### Practical: AI Chat Web App Template
The .NET AI Chat Web App template now includes support for .NET Aspire and integration with the Qdrant vector database, facilitating the creation of cloud-native applications
.

**Quick start:**
```bash
dotnet new install Microsoft.Extensions.AI.Templates
dotnet new aichatweb
```

### Agent-to-Agent Communication
Microsoft has released the A2A .NET SDK, a new developer toolkit that enables building AI agents capable of communicating and collaborating using the Agent2Agent (A2A) protocol, with support for both client and server roles, allowing .NET-based agents to interact with others across ecosystems
.

---

## The Cost & Latency Reality Check
GPT-4.1 is around 26% cheaper than GPT-4o for typical queries, prompt caching discounts have been raised to 75%, and long-context usage no longer incurs additional charges beyond standard per-token costs
.
The Realtime API now supports WebRTC, enabling real-time audio streaming and low-latency interactions, ideal for applications requiring immediate feedback, such as live customer support or interactive voice assistants
.

---

## What's Ahead: 2025 Readiness Checklist

![A robot frantically trying to migrate code from one platform to another while sweating profusely, with "MCP" and "GitHub Extensions" labels flying everywhere](assets/images/robot.webp)
*Me, migrating Copilot Extensions to MCP before November 10. 🤖*

- **By November 10:** Migrate any Copilot Extensions to MCP servers.
- **This month:** Audit your Azure OpenAI deployments; consider switching to GPT-4.1 for cost savings.
- **Q4 2025:** Evaluate .NET Aspire + Azure AI Foundry for new projects; test Model Context Protocol in your CI/CD.
- **Ongoing:**
Your value won't just hinge on typing speed, but increasingly on your ability to solve, design, and inspire
.

---

## Further Reading

- https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
- https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- https://github.blog/changelog/2025-10-28-new-public-preview-features-in-copilot-code-review-ai-reviews-that-see-the-full-picture/
- https://dev