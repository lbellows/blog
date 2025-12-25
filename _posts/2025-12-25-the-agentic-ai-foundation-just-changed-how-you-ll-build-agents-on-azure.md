---
author: the.serf
date: 2025-12-25 06:28:54 -0500
layout: post
tags:
- agent
- how
- just
- agentic
- agents
- claude-haiku-4-5-20251001
title: The Agentic AI Foundation Just Changed How You'll Build Agents on Azure
---

# The Agentic AI Foundation Just Changed How You'll Build Agents on Azure

**TL;DR:**
OpenAI and Anthropic donated AGENTS.md and Model Context Protocol to the new Agentic AI Foundation
under the Linux Foundation. For .NET developers shipping on Azure, this means standardized, vendor-neutral tooling for multi-agent systems—no more reinventing the wheel for each AI model.

## What Just Happened (And Why You Should Care)
OpenAI and Anthropic have donated their AGENTS.md and Model Context Protocol projects to the Agentic AI Foundation (AAIF), with Block contributing their agent framework, goose, as another founding project
.
The foundation's Platinum members are Amazon Web Services (AWS), Microsoft, Bloomberg, Cloudflare, and Google
.

For .NET engineers on Azure, this is the infrastructure bet you've been waiting for.

## The Problem: Agent Fragmentation

Before this week, building agents felt like the Wild West. You'd wire up Claude through Anthropic's SDK, then swap to GPT-5.2 on Azure OpenAI, and suddenly your orchestration logic breaks. Tool calling APIs differ. Context protocols diverge. Every model vendor had their own opinions about how agents should talk to external services.
MCP was released in late 2024 as "an open standard describing a protocol for integrating external resources and tools with LLM apps"
. Now it's backed by a neutral foundation. That changes everything.

## What You Get Now

### 1. **Model Context Protocol (MCP) as Standard**
MCP is an open standard describing a protocol for integrating external resources and tools with LLM apps
. In practice, this means your agent can plug into Azure SQL, Cosmos DB, or any external service through a single, standardized interface—regardless of whether you're calling GPT-5.2 or Claude Opus 4.5.

For .NET developers, this is huge. Instead of writing adapter code per model, you define your tools once in MCP and reuse them across agents.

### 2. **AGENTS.md: A Readable Format for Agent Definitions**
AGENTS.md is an open format designed to assist AI coding agents, released in the second half of 2025
. Think of it as a human-and-machine-readable spec for describing what an agent can do. Version control your agent definitions. Diff them. Review them in pull requests. This is what was missing.

### 3. **Neutral Governance**
The aim of the AAIF is to provide a neutral organization to encourage open-source agentic AI technologies and secure long-term community support of projects
. No single vendor owns the spec. You're not locked into OpenAI's vision or Anthropic's roadmap.

## How to Start Using This Today

If you're building on Azure AI Foundry with .NET, here's the practical path:

1. **Adopt MCP for tool definitions.** When you build an agent that needs to query a SQL Server database or invoke a Logic App, define that integration via MCP instead of custom code.

2. **Use AGENTS.md to document agent behavior.** If you're shipping multiple agents (coding agents, data agents, orchestrators), describe them in AGENTS.md. Makes onboarding and auditing trivial.

3. **Stay vendor-agnostic.**
Azure is now the only cloud providing access to both Claude and GPT frontier models to customers on one platform
. Use that flexibility. Write your agent logic once, swap models without rewriting orchestration.

## The Cost Angle

You're probably already paying for Azure AI Foundry compute.
Claude Opus 4.5 is priced at $5 per million input tokens and $25 per million output tokens — a dramatic reduction from the $15 and $75 rates for its predecessor
. With standardized tooling, you can now route cheaper models (like Haiku or GPT-4 mini) through the same agent framework as your premium models. That's real cost optimization.

## What's Next

The foundation is brand new, but momentum is real. Expect:

- Better .NET SDKs for MCP integration (watch Azure SDK repos).
- GitHub Copilot and VS Code extensions that understand AGENTS.md.
- Tighter integration between Azure AI Foundry and the open-source agent ecosystem.

The age of bespoke agent plumbing is ending. Welcome to the era of standardized, composable AI systems.

---

## Further reading

https://www.infoq.com/news/2025/12/agentic-ai-foundation/

https://azure.microsoft.com/en-us/blog/introducing-anthropics-claude-models-in-microsoft-foundry-bringing-frontier-intelligence-to-azure/

https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new

https://azure.microsoft.com/en-us/blog/introducing-gpt-5-2-in-microsoft-foundry-the-new-standard-for-enterprise-ai/

https://techcrunch.com/2025/12/11/openai-fires-back-at-google-with-gpt-5-2-after-code-red-memo/

https://venturebeat.com/ai/anthropics-claude-opus-4-5-is-here-cheaper-ai-infinite-chats-and-coding/