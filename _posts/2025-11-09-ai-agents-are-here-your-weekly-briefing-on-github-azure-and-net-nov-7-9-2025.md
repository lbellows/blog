---
author: the.serf
date: 2025-11-09 06:24:54 -0500
layout: post
tags:
- .net
- agents
- azure
- github
- agent
- claude-haiku-4-5-20251001
title: 'AI Agents Are Here: Your Weekly Briefing on GitHub, Azure, and .NET (Nov 7–9,
  2025)'
---

# AI Agents Are Here: Your Weekly Briefing on GitHub, Azure, and .NET (Nov 7–9, 2025)

**TL;DR**
AI, agents, and typed languages are driving the biggest shifts in software development in more than a decade.
More than 1.1 million public repositories now use an LLM SDK, with 693,867 of these projects created in just the past 12 months alone (+178% YoY).
This week, GitHub launched **AgentHQ** for orchestrating custom AI agents,
GitHub deprecated GitHub Copilot Extensions (built as GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers
, and
Azure renamed "Accelerate Developer Productivity with Microsoft Azure" to "Agentic DevOps with Microsoft Azure and GitHub."
The message is clear: agents are no longer experimental—they're production infrastructure.

---

## GitHub's AgentHQ: The Agent Operating System You Didn't Know You Needed
GitHub announced during its annual GitHub Universe 2025 event a new addition to its platform called AgentHQ, designed to let developers create and deploy AI agents that work directly within GitHub's development environment, expanding the company's ongoing efforts to integrate AI into the software development lifecycle.
**What it does:**
Agents are designed as customizable, task-specific AI assistants that can handle various aspects of the coding workflow, from issue triage and documentation to testing and deployment. Unlike Copilot, which focuses primarily on in-editor code completion and generation, GitHub AgentHQ operates at a broader level, they can monitor repository events, respond to pull requests, or perform code reviews using contextual information available in a project.
**Real-world integration:**
AgentHQ also integrates with GitHub Actions, enabling automated pipelines that combine traditional CI/CD tasks with AI-driven reasoning. For instance, an agent could review code changes, suggest improvements, and trigger a test suite if specific conditions are met. Another agent might handle repetitive maintenance tasks, such as dependency updates or security scanning.
**Practical takeaway for .NET teams:**
App modernization capabilities in GitHub Copilot can update, upgrade, and modernize Java and .NET applications while handling code assessments, dependency updates, and remediation, with mainframe modernization also coming soon.
If you're managing legacy .NET codebases, agents can now automate the grunt work of upgrades—freeing your team to focus on architecture.

---

## The MCP Shift: Why You Need to Migrate Away from Copilot Extensions

![A robot looking confused at a roadmap with a sign that says "MCP or bust" while holding a wrench. The robot is sweating nervously.](assets/images/robot.webp)

*"Is this the part where I learn a new protocol?" — Every developer, Nov 10, 2025*
GitHub deprecated GitHub Copilot Extensions (built as GitHub Apps) on November 10, 2025, in favor of Model Context Protocol (MCP) servers. MCP provides a universal standard for AI agent integration—build an MCP server once and use it across any compatible agent or chatbot, not just GitHub Copilot.
**Why this matters:**
MCP addresses this by providing an open standard that's modular and easy to integrate into a variety of AI assistants and agents. Build your server once and it works with GitHub Copilot, Claude Code, and any other MCP-compatible host app. Developers shouldn't have to rebuild the same functionality for every platform.
**Migration path:**
Read the MCP server developer documentation to learn more about building an MCP server. Note that MCP servers are architecturally different from Copilot Extensions, so this is a replacement rather than a migration.
**For .NET developers:**
Microsoft Agent Framework enables developers to build AI agents with minimal code requirements. The company demonstrated this simplicity with examples showing functional agents created in fewer than twenty lines of code.
The framework integrates with MCP, so you can build once and deploy everywhere.

---

## Azure's Agentic DevOps: The New North Star
Accelerate Developer Productivity with Microsoft Azure is renamed to Agentic DevOps with Microsoft Azure and GitHub.
This rebranding signals a strategic pivot: Microsoft is betting that the future of cloud development is agents orchestrating your entire pipeline.

**Key releases this month:**

-
Agentic retrieval is now possible through Azure AI Search, using advanced techniques to improve answer relevance by up to ~40% on complex, multi-part questions in early tests.
-
Model router in Azure AI Foundry allows developers to automatically select the optimal Azure OpenAI models for different prompts—boosting quality while reducing costs.
-
Multi-Agent Orchestration debuted for Azure AI Foundry Agent Service, providing connected agents and multi-agent workflows with support for Model Context Protocol (MCP) and more.
**Cost & latency wins:**
Foundry Observability is now in preview, giving developers end-to-end monitoring, built-in metrics, and detailed trace logs of the reasoning steps and tool calls made by agents.
Translation: you can now see *exactly* where your agent is burning tokens and latency.

---

## .NET Gets Serious About Agents
AI is becoming deeply integrated with .NET through mature tooling like Microsoft Extensions for AI. The tooling around LLMs, Microsoft Extensions for AI (now generally available), Semantic Kernel, and AI agents is getting really mature.
**The Agent Framework is production-ready:**
Microsoft Agent Framework enables Model Context Protocol (MCP) support, Agent-to-Agent (A2A) communication, and OpenAPI-based integration, ensuring portability across different runtime environments. Advanced orchestration patterns from AutoGen, such as group chat, debate, and reflection capabilities, now delivered with enterprise-grade reliability.
**Start here:**
This template is part of the ongoing effort to make AI development with .NET easier to discover and use, with scaffolding and guidance within Visual Studio, Visual Studio Code, and the .NET CLI. Once installed, the template is available in Visual Studio, Visual Studio Code (with the C# Dev Kit), or you can just run dotnet new aichatweb to create it in your working directory.
```bash
dotnet new install Microsoft.Extensions.AI.Templates
dotnet new aichatweb
```

---

## The Elephant in the Room: Infrastructure Constraints

While agents are exciting,
Microsoft CEO Satya Nadella said "The biggest issue we are now having is not a compute glut, but it's a power and it's sort of the ability to get the [data center] builds done fast enough close to power." "If you can't do that, you may actually have a bunch of chips sitting in inventory that I can't plug in.
Translation: power is now the bottleneck, not GPUs.

**What this means for you:**  
Optimize for efficiency.
Frameworks like vLLM, SGLang, and TensorRT-LLM have matured disaggregated serving with implementations demonstrating up to 6.4x throughput improvements and 20x reduction in latency variance.
If you're self-hosting models, disaggregated inference architectures can cut your power bill significantly.

---

## Looking Ahead: 2025 Readiness Checklist

1. **Migrate Copilot Extensions to MCP** – The Nov 10 deadline has passed; if you built custom extensions, port them now.
2. **Explore AgentHQ for your workflows** – Start with simple agents (issue triage, dependency updates) and iterate.
3. **Adopt Microsoft Agent Framework** – It's the unifying layer for .NET agent development. Use it.
4. **Measure cost & latency obsessively** –