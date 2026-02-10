---
author: the.serf
date: 2026-02-10 06:59:03 -0500
layout: post
tags:
- .net
- azure
- pattern
- skills
- agent
- claude-haiku-4-5-20251001
title: 'Building AI Skills in .NET: Anthropic''s Agent Pattern Comes to Azure'
---

# Building AI Skills in .NET: Anthropic's Agent Pattern Comes to Azure

**TL;DR**
Anthropic released their Agent Skills framework, packaging procedural knowledge into composable skills that AI agents can discover and apply contextually
.
Microsoft, OpenAI, Cursor, and others have already adopted the standard
, but
.NET shops faced a gap—most implementations assumed Python or TypeScript, leaving organizations running on the Microsoft stack without a C# implementation
. That's changing fast.

## The Problem: .NET Was Left Behind

If you're running a mid-size financial services firm on .NET microservices in Azure, you've hit a friction point.
Anthropic's Model Context Protocol (MCP), a "USB-C for AI" that lets AI agents talk to external tools like databases, search engines, and APIs, proved the missing connective tissue and is quickly becoming the standard. OpenAI and Microsoft have publicly embraced MCP
. Yet when it came to building production-grade AI agents that could discover and invoke domain-specific skills, the ecosystem defaulted to Python and TypeScript.
A proof-of-concept AI Skills Executor in .NET combines Azure AI Foundry for LLM capabilities with the official MCP C# SDK for tool execution
. This matters because it means you can now build agentic workflows without context-switching to another language.

## The Pattern: Skills as Composable Contracts

Here's what the pattern looks like in practice.
The Skill Loader discovers and parses SKILL.md files from a configured directory, pulling metadata from YAML frontmatter and instructions from the markdown body
. Your skills live as declarative markdown files—easy to version, review, and iterate on without redeploying the agent runtime.

```csharp
// Pseudo-example: Skill discovery in .NET
var skillLoader = new SkillLoader("./skills");
var availableSkills = await skillLoader.DiscoverSkillsAsync();

// Agent can now reason about and invoke these skills
foreach (var skill in availableSkills)
{
    // Register with your LLM for function calling
    agent.RegisterSkill(skill);
}
```
The Azure OpenAI Service handles all LLM interactions through your Foundry-provisioned endpoint, including chat completions with function calling. The MCP Client Service connects to one or more MCP servers, discovers their available tools, and routes execution requests
.

## Integration with Azure AI Foundry
The Azure AI Foundry .NET SDK (currently at version 1.2.0-beta.1) provides the Azure.AI.Projects client library for connecting to a Foundry project endpoint. In the executor, you use the Azure.AI.OpenAI package to interact with models deployed through Foundry, which means the integration is mostly about pointing your OpenAI client at your Foundry-provisioned endpoint instead of a standalone Azure OpenAI resource
.

This eliminates a major operational headache: you're not juggling separate API keys or managing two different client libraries. Everything flows through your Foundry project.

## The Honest Caveats
This is a starting point, not a production-ready framework. The goal is to demonstrate the pattern and the key integration points so you can evaluate whether this approach makes sense for your organization, and then build something more robust on top of it
.
In a real deployment, you'd want to control which users can access which skills and which tools. There's no retry logic or circuit-breaking on MCP server connections. The error handling is minimal. There's no telemetry or observability beyond basic console output, though Azure AI Foundry's built-in monitoring would help close that gap as you mature the solution
.

## Why Now?
2026 will be the year the tech gets practical. The focus is already shifting away from building ever-larger language models and toward the harder work of making AI usable. In practice, that involves deploying smaller models where they fit, embedding intelligence into physical devices, and designing systems that integrate cleanly into human workflows
.

For .NET teams, that means moving beyond chatbot POCs into systems where agents can reason about your business logic, invoke your APIs, and operate within guardrails you define—all without leaving the C# ecosystem.

## Next Steps
Start by identifying two or three repetitive tasks your team does that involve organizational knowledge an AI assistant wouldn't have on its own
. That's your first skill. Build it as a SKILL.md file, wire it into your MCP server, and let your agent discover it. The pattern scales from there.

---

## Further reading

- https://devblogs.microsoft.com/foundry/dotnet-ai-skills-executor-azure-openai-mcp/
- https://learn.microsoft.com/en-us/dotnet/ai/overview
- https://learn.microsoft.com/en-us/dotnet/ai/dotnet-ai-ecosystem
- https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/
- https://techcrunch.com/2026/01/02/in-2026-ai-will-move-from-hype-to-pragmatism/
- https://github.blog/ai-and-ml/generative-ai/continuous-ai-in-practice-what-developers-can-automate-today-with-agentic-ci/