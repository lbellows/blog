---
author: the.serf
date: 2026-02-18 06:55:04 -0500
layout: post
tags:
- bloat
- context
- .net
- agents
- anthropic
- claude-haiku-4-5-20251001
title: Context Bloat Is Killing Your AI Agents—Here's How Anthropic Just Fixed It
---

# Context Bloat Is Killing Your AI Agents—Here's How Anthropic Just Fixed It

**TL;DR**
Anthropic released MCP Tool Search, a feature that introduces "lazy loading" for AI tools, allowing agents to dynamically fetch tool definitions only when necessary.
Instead of loading all 50+ tool descriptions upfront (wasting 33% of your context window), agents now search a lightweight index and pull only what they need.
Microsoft is collaborating with Anthropic to create an official C# SDK for the Model Context Protocol (MCP), and MCP has seen rapid adoption in the AI community.
If you're building AI agents on .NET and Azure, this is the efficiency win you've been waiting for.

---

## The Problem: Context Bloat Was Eating Your Budget

Let's be honest: building agentic systems is hard enough without burning through your context window before you even start.
Claude Code typically had to "read" the instruction manual for every single tool available, regardless of whether it was needed for the immediate task, using up the available context that could otherwise be filled with more information from the user's prompts or the agent's responses.
The scale of the problem was staggering.
MCP servers may have up to 50+ tools, and users were documenting setups with 7+ servers consuming 67k+ tokens.
A developer using a robust set of tools might sacrifice 33% or more of their available context window limit of 200,000 tokens before they even typed a single character of a prompt.
For enterprise teams, this wasn't just inefficient—it was economically painful. Every token costs money. Every wasted token is margin you're leaving on the table.

---

## The Solution: Lazy Loading for AI Tools
Claude Code now monitors context usage. The system automatically detects when tool descriptions would consume more than 10% of the available context. When that threshold is crossed, instead of dumping raw documentation into the prompt, it loads a lightweight search index. When the user asks for a specific action—say, "deploy this container"—Claude Code doesn't scan a massive, pre-loaded list of 200 commands. Instead, it queries the index, finds the relevant tool definition, and pulls only that specific tool into the context.
This is elegant infrastructure thinking: borrow the pattern that made IDEs scale (lazy-load plugins on demand) and apply it to agentic AI.

---

## Why This Matters for .NET and Azure Developers
When Anthropic released their Agent Skills framework, they published a blueprint for how enterprise organizations should structure AI agent capabilities. The pattern is straightforward: package procedural knowledge into composable skills that AI agents can discover and apply contextually. Microsoft, OpenAI, Cursor, and others have already adopted the standard, making skills portable across the AI ecosystem.
Microsoft is collaborating with Anthropic to create an official C# SDK for the Model Context Protocol (MCP). The SDK is being developed as an open-source project in the modelcontextprotocol GitHub organization, and the library is available as a NuGet package, ModelContextProtocol.
If you're shipping on .NET and Azure, you now have a first-class path to build production-grade AI agents without context window waste.
This involves building a proof-of-concept AI Skills Executor in .NET that combines Azure AI Foundry for LLM capabilities with the official MCP C# SDK for tool execution.
### Practical Integration Steps

1. **Add the NuGet package:**
   ```bash
   dotnet add package ModelContextProtocol
   ```

2. **Create an MCP server in C#** that exposes your tools as resources or skills:
   ```csharp
   // Pseudocode—consult the official SDK docs for full implementation
   var server = new McpServer();
   server.RegisterTool("deploy-container", DeployContainerAsync);
   server.RegisterTool("check-logs", CheckLogsAsync);
   await server.StartAsync();
   ```

3. **Wire it into your Azure AI Foundry agent** so it can discover and use tools on demand, not upfront.

The key insight:
Tool reusability across contexts. MCP servers expose tools that any skill can use. The project analysis tools work whether invoked by a tech debt assessor, a documentation generator, or a migration planner. You build the tools once and compose them differently through skills.
---

## The Broader Shift: Pragmatism Over Hype
If 2025 was the year AI got a vibe check, 2026 will be the year the tech gets practical. The focus is already shifting away from building ever-larger language models and toward the harder work of making AI usable. In practice, that involves deploying smaller models where they fit, embedding intelligence into physical devices, and designing systems that integrate cleanly into human workflows.
MCP Tool Search is a perfect example of this shift. It's not flashy. It's not a new model or a breakthrough algorithm. It's infrastructure—the boring, essential work of making agents actually work in production without bankrupting your token budget.

---

## Bottom Line

If you're building AI agents on .NET and Azure, you now have the tools to scale without waste.
The update is rolling out immediately for Claude Code users. For developers building MCP clients, Anthropic recommends implementing the `ToolSearchTool` to support this dynamic loading, ensuring that as the agentic future arrives, it doesn't run out of memory before it even says hello.
The context window is no longer your bottleneck. Ship smarter.

---

## Further Reading

- https://venturebeat.com/orchestration/claude-code-just-got-updated-with-one-of-the-most-requested-user-features/
- https://developer.microsoft.com/blog/microsoft-partners-with-anthropic-to-create-official-c-sdk-for-model-context-protocol
- https://devblogs.microsoft.com/foundry/dotnet-ai-skills-executor-azure-openai-mcp/
- https://techcrunch.com/2026/01/02/in-2026-ai-will-move-from-hype-to-pragmatism/
- https://modelcontextprotocol.io/
- https://learn.microsoft.com/en-us/azure/ai-foundry/