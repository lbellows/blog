---
author: the.serf
date: 2026-02-07 06:35:02 -0500
layout: post
tags:
- .net
- azure
- skills
- agent
- anthropic
- claude-haiku-4-5-20251001
title: 'Agent Skills for .NET: Bringing Anthropic''s Open Standard to Azure and C#'
---

# Agent Skills for .NET: Bringing Anthropic's Open Standard to Azure and C#

**TL;DR**
Anthropic released their Agent Skills framework, a blueprint for how enterprise organizations should structure AI agent capabilities by packaging procedural knowledge into composable skills that AI agents can discover and apply contextually
.
Microsoft, OpenAI, Cursor, and others have already adopted the standard, making skills portable across the AI ecosystem
. For .NET teams, this means you can now build production-grade agentic systems in C# using Azure AI Foundry and the Model Context Protocol (MCP) SDK—no Python required.

---

## Why This Matters: The Ecosystem Convergence
OpenAI has quietly adopted structurally identical architecture in both ChatGPT and its Codex CLI tool, with developer Elias Judin discovering directories containing skill files that mirror Anthropic's specification—the same file naming conventions, the same metadata format, the same directory organization
. This convergence signals something bigger:
the industry has found a common answer to a vexing question: how do you make AI assistants consistently good at specialized work without expensive model fine-tuning
.

For .NET developers, the timing is critical.
Microsoft Defender for Cloud now includes threat protection for AI agents built with Foundry, available in public preview as part of the Defender for AI Services plan, delivering advanced security from development through runtime
. Enterprise adoption is accelerating—and your toolchain needs to keep pace.

---

## Building an AI Skills Executor in .NET: The Architecture
Building a proof-of-concept AI Skills Executor in .NET combines Azure AI Foundry for LLM capabilities with the official MCP C# SDK for tool execution
. Here's how the pieces fit together:

**The Four-Part Pattern**
The Skill Loader discovers and parses SKILL.md files from a configured directory, pulling metadata from YAML frontmatter and instructions from the markdown body. The Azure OpenAI Service handles all LLM interactions through your Foundry-provisioned endpoint, including chat completions with function calling. The MCP Client Service connects to one or more MCP servers, discovers their available tools, and routes execution requests. And the Skill Executor itself orchestrates the agentic loop: taking user input, managing the conversation with the LLM, executing tool calls when requested, and returning final responses
.

**A Practical Example**
A developer selects the Tech Debt Assessor skill and asks "Assess the tech debt in our OrderService at C:\repos\order-service." The executor loads the skill's instructions as the system prompt, sends the request to Azure OpenAI through Foundry with the available MCP tools, and the LLM starts calling tools. First analyze_directory to understand the project structure, then count_lines for scale metrics, then find_patterns to locate debt markers. After each tool call, the results come back into the conversation, and the LLM decides what to do next. Eventually, it synthesizes everything into a severity-prioritized report
.

---

## Integration with Azure: Practical Steps

1. **Provision an Azure AI Foundry endpoint** with a model like GPT-5.2 or Claude Opus 4.6 (both now available in Foundry).
2. **Install the official MCP C# SDK** and reference it in your .NET project.
3. **Define skills as SKILL.md files** with YAML frontmatter (metadata) and markdown instructions.
4. **Use Azure OpenAI's chat completions API** with function calling enabled—let the LLM orchestrate which MCP tools to invoke.
5. **Route MCP tool calls** through your MCP Client Service, capturing results and feeding them back into the conversation loop.
The BuildToolDefinitions method bridges MCP and Azure OpenAI by converting MCP tool schemas into ChatTool function definitions
.

---

## The Bigger Picture: Cost and Latency
OpenAI says that GPT-5.3 Codex is 25% faster than its previous model (GPT-5.2)
, and
Claude Code now monitors context usage and automatically detects when tool descriptions would consume more than 10% of the available context
. This "lazy loading" of tool definitions is critical for cost control—
token savings are dramatic: from ~134k to ~5k in Anthropic's internal testing
.

For .NET teams, this means your Foundry deployments will run leaner. Combine that with
spillover, which is now Generally Available and manages traffic fluctuations on provisioned deployments by routing overages to a designated standard deployment
, and you have a cost-predictable agentic system.

---

## A Word of Caution
What's shown here is a starting point, not a production-ready framework
.
Be critical when vendors promise "80% accuracy" as if that's the whole story. This is still generative AI in early 2026. Treat claims as marketing until you've seen working results in your own codebase, with your constraints, and your risk profile. Only believe what you can validate
.

---

## Further Reading

- https://devblogs.microsoft.com/foundry/dotnet-ai-skills-executor-azure-openai-mcp/
- https://venturebeat.com/technology/anthropic-launches-enterprise-agent-skills-and-opens-the-standard/
- https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/what-is-trending-in-hugging-face-on-microsoft-foundry-feb-2-2026/4490602
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new?view=foundry-classic
- https://www.infoq.com/news/2025/12/agentic-ai-foundation/
- https://venturebeat.com/orchestration/claude-code-just-got-updated-with-one-of-the-most-requested-user-features/
- https://azure.microsoft.com/en-us/blog/introducing-gpt-5-2-in-microsoft-foundry-the-new-standard-for-enterprise-ai/
- https://techcrunch.com/2026/02/05/openai-launches-new-agentic-coding-model-only-minutes-after-anthropic-drops-its-own/