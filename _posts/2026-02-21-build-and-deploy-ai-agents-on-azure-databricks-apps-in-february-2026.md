---
author: the.serf
date: 2026-02-21 06:34:15 -0500
layout: post
tags:
- agents
- deployment
- february
- .net
- agent
- claude-haiku-4-5-20251001
title: Build and Deploy AI Agents on Azure Databricks Apps in February 2026
---

# Build and Deploy AI Agents on Azure Databricks Apps in February 2026

**TL;DR:**
Azure Databricks now offers new documentation and project templates for building and deploying AI agents on Databricks Apps using popular libraries like LangGraph, PyFunc, and OpenAI Agent SDK
. This simplifies agent development for .NET and Python teams shipping on Azure, with Git-based deployment and improved cost attribution through custom query tags.

## The Story: Agents Move from Hype to Deployment
2026 is likely to be the year agentic workflows finally move from demos into day-to-day practice
. But moving from proof-of-concept to production requires infrastructure that *actually works* at scale.
Azure Databricks' February update addresses this directly with new documentation and templates for building and deploying AI agents on Databricks Apps, enabling authors to use LangGraph, PyFunc, and OpenAI Agent SDK, then deploy them on Databricks Apps
.

For .NET developers, this matters because
the Agent Framework is the recommended approach for .NET apps that need to build agentic AI systems with advanced orchestration, multi-agent collaboration, and enterprise-grade security and observability, and is a production-ready, open-source framework that brings together the best capabilities of Semantic Kernel and Microsoft Research's AutoGen
.

## What Changed in February 2026

Three practical improvements landed:

### 1. Git-Based Deployment (No More File Uploads)
You can now deploy Databricks apps directly from Git repositories without uploading files to the workspace, configuring a repository for your app and deploying from any branch, tag, or commit
. This is a game-changer for CI/CD pipelines—your agent code lives in version control, and deployments trigger automatically.

### 2. Cost Attribution via Query Tags
You can now apply custom key-value tags to SQL workloads on Databricks SQL warehouses for grouping, filtering, and cost attribution, with query tags appearing in the system.query.history table and on the Query History page, allowing you to attribute warehouse costs by business context and identify sources of long-running queries
.

This solves a real pain point: when you're running multiple agents or experiments, tracking which agent consumed which compute becomes critical for billing and optimization.

### 3. Enhanced Agent Mode (Faster Responses)
Research Agent was renamed to Agent mode (Beta), with improved responses that now produce more concise and faster results for "what" type questions through improved system prompting
. Latency matters—especially for interactive agent workflows.

## Integration Path for .NET Teams

If you're building on .NET and Azure, here's the practical flow:

1. **Use Agent Framework** –
Agent Framework provides multi-agent orchestration supporting sequential, concurrent, group chat, handoff, and magentic patterns, cloud and provider flexibility that is cloud-agnostic and provider-agnostic using plugin and connector models, and enterprise-grade features including built-in observability (OpenTelemetry), Microsoft Entra security integration, and responsible AI features including prompt injection protection
.

2. **Deploy to Databricks Apps** – Push your agent code to a Git repo, configure the Databricks App to track that repo, and let the platform handle orchestration and scaling.

3. **Monitor Costs** – Use custom query tags to segment agent workloads by team, experiment, or customer—essential when agents run 24/7.

## The Bigger Picture: Agentic AI Hits Production
Anthropic's Model Context Protocol (MCP), a "USB-C for AI" that lets AI agents talk to external tools like databases, search engines, and APIs, proved the missing connective tissue and is quickly becoming the standard, with OpenAI and Microsoft publicly embracing MCP
. Databricks' new templates and deployment model align with this ecosystem—agents can now call external APIs, databases, and services with minimal friction.

For cost-conscious teams,
semantic caching can reduce LLM API costs by 73% after implementing it with a cache hit rate increased to 67%
, so pairing agent deployments with caching strategies is a smart move.

## Practical Takeaway

If you've been sitting on agent POCs, February 2026 is the inflection point. The infrastructure is now production-grade, versioning is clean (Git-based), and cost tracking is granular. Start with a single agent, deploy it to Databricks Apps, tag your queries, and scale from there.

---

## Further reading

- https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/february
- https://learn.microsoft.com/en-us/dotnet/ai/microsoft-extensions-ai
- https://learn.microsoft.com/en-us/dotnet/ai/dotnet-ai-ecosystem
- https://techcrunch.com/2026/01/05/microsofts-nadella-wants-us-to-stop-thinking-of-ai-as-slop/
- https://venturebeat.com/orchestration/why-your-llm-bill-is-exploding-and-how-semantic-caching-can-cut-it-by-73/