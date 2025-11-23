---
author: the.serf
date: 2025-11-23 06:26:08 -0500
layout: post
tags:
- .net
- agentic
- apis
- cost
- model
- claude-haiku-4-5-20251001
title: 'AI Roundup: Agents, APIs, and Agentic DevOps—What .NET Developers Need to
  Know This Week'
---

# AI Roundup: Agents, APIs, and Agentic DevOps—What .NET Developers Need to Know This Week

**TL;DR**
Microsoft Ignite 2025 emphasized empowering the complete lifecycle of AI
, bringing major announcements for .NET and Azure developers.
Google unveiled Gemini 3 on November 18, 2025
, while
Azure now offers both OpenAI and Anthropic models in Microsoft Foundry
.
OpenAI released GPT‑5.1-Codex-Max for agentic coding
. The headline: agents are no longer experimental—they're production-ready, and your infrastructure choices matter more than ever for cost and latency.

---

## Ignite 2025: The Agentic Pivot
At GitHub Universe 2025, the theme was clear: the ability to see, steer, and build across agents will bring the greatest impact, and agents have become an integral part of software development already, taking on manual, repetitive coding tasks
. This shift has profound implications for .NET teams.
Microsoft renamed "Accelerate Developer Productivity with Microsoft Azure" to "Agentic DevOps with Microsoft Azure and GitHub,"
signaling that agent-driven workflows are now the default development paradigm, not a nice-to-have.

### What This Means for .NET Developers
Microsoft has gone all-in on making AI development in .NET easy and powerful, with the tooling around LLMs, Microsoft Extensions for AI (now generally available), Semantic Kernel, and AI agents getting really mature
. If you haven't explored these libraries yet, now is the time.
Microsoft announced the preview release of Microsoft Agent Framework, an open-source SDK designed to simplify the creation and deployment of AI agents, representing a significant consolidation effort unifying capabilities from Semantic Kernel and AutoGen
.
Microsoft Agent Framework enables developers to build AI agents with minimal code requirements, with examples showing functional agents created in fewer than twenty lines of code
.

For .NET specifically:
Microsoft released the A2A .NET SDK, enabling building AI agents capable of communicating and collaborating using the Agent2Agent (A2A) protocol, with support for both client and server roles
. This is crucial for multi-agent orchestration at scale.

---

## Azure AI Foundry: The Model Supermarket
Claude Sonnet 4.5, Opus 4.1, and Haiku 4.5 are now part of Microsoft Foundry, advancing the mission to give customers choice across the industry's leading frontier models—and making Azure the only cloud offering both OpenAI and Anthropic models
.

### Real-Time Audio & Multimodal APIs
The Realtime API (preview) now supports WebRTC, enabling real-time audio streaming and low-latency interactions, ideal for applications requiring immediate feedback, such as live customer support or interactive voice assistants
.
GPT-image-1 (2025-04-15) is the latest image generation model from Azure OpenAI, featuring major improvements over DALL-E, including better responsiveness to precise instructions, reliable text rendering, and the ability to accept images as input for image editing and inpainting
.

### Cost Optimization: Model Router
Model router in Azure AI Foundry allows developers to automatically select the optimal Azure OpenAI models for different prompts—boosting quality while reducing costs
. For teams managing multiple workload types, this is a game-changer. The router can intelligently downgrade complex queries to cheaper models when appropriate, reducing token spend without sacrificing quality.

---

## Cost & Latency: The Infrastructure Reality Check

Agents are powerful, but they're expensive if you don't optimize. Here's what the data shows:
Token-Oriented Object Notation (TOON) aims to be a schema-aware alternative to JSON that significantly reduces token consumption, with some benchmarks showing TOON may use 40% fewer tokens than JSON, possibly resulting in LLM and inference cost savings
. If you're shipping high-volume RAG or agentic workloads, consider this for prompt serialization.
Frameworks like vLLM, SGLang, and TensorRT-LLM have matured disaggregated serving with implementations demonstrating up to 6.4x throughput improvements and 20x reduction in latency variance, solving the challenge of the same hardware excelling at processing input prompts but struggling with response generation
.

For on-premises deployments,
dynamic batching helps optimize inference throughput by aggregating multiple incoming requests into a single batch, improving inference throughput and optimizing utilization of limited resources
.

---

## GitHub Copilot & .NET Modernization
GitHub Copilot now accelerates the most time-consuming early steps of modernization, assessing legacy .NET and Java codebases, recommending modernization paths, generating updated code, and producing IaC templates for Azure services
. This is particularly useful for teams with aging .NET Framework applications.
GPT-5.1, GPT-5.1-Codex, and GPT-5.1-Codex-Mini—the full suite of OpenAI's latest 5.1-series models—are now rolling out in public preview in GitHub Copilot
.

---

## Practical: Getting Started This Week

**1. Explore Microsoft Agent Framework:**
```bash
dotnet new install Microsoft.Extensions.AI.Templates
dotnet new aichatweb
```

**2. Try Model Router for cost optimization:**
By not defaulting workload to a fixed large reasoning model, monthly LLM spend drops while workloads still gain high-quality answers when complexity triggers upscale routing to models designed for reasoning
.

**3. Audit your token usage:**
Consider whether TOON or structured serialization could reduce your prompt overhead, especially for high-volume inference.

**4. Plan for multi-agent orchestration:**
Microsoft is making it easier to orchestrate multi-agent workflows, with Microsoft Agent Framework Enhanced Durable Functions (public preview) now supporting multi-agent patterns with built-in orchestration and OpenAI SDK integration
.

---

## Looking Ahead: 2025 Readiness
A shift is occurring from AI being an assistant to AI being a co-creator of the software, entering a phase where the entire application can be developed, tested and shipped with the AI as part of the development team
.

For .NET teams, this means:
- **Invest in observability:**
Foundry Observability is now in preview, giving developers end-to-end monitoring, built-in metrics, and detailed trace logs of the reasoning steps and tool calls made by agents
.
- **Plan for governance:**
AI Gateway in API Management, now available in the Foundry Control Plane (public preview), secures model access, enforces policies, and optimizes token usage
.
- **Embrace open standards:**
Open Standards & Interoperability enables Model Context Protocol (MCP) support, Agent-to-Agent (A2A) communication, and OpenAPI-based integration
.

---

## Further Reading

https://blogs.microsoft.com/blog/2025/11/18/from-idea-to-deployment-the-complete-lifecycle-of-ai-on-display-at-ignite-2025/

https://www.infoq.com/news/2025/11/google-gemini-3/

https://azure.microsoft.com/en-us/blog/azure-at-microsoft-ignite-2025-all-the-intelligent-cloud-news-explained/

https://learn.microsoft.com/en-us/azure