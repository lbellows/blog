---
author: the.serf
date: 2025-11-17 06:28:24 -0500
layout: post
tags:
- agent
- aspire
- now
- search
- support
- claude-haiku-4-5-20251001
title: '.NET 10 Goes Live: Vector Search and AI Agent Support Come to the Runtime'
---

# .NET 10 Goes Live: Vector Search and AI Agent Support Come to the Runtime

**TL;DR**
.NET 10 is now generally available as a Long-Term Support release with three years of support until November 10, 2028
. The headline for AI-focused engineers:
AI-focused capabilities expand through the Microsoft Agent Framework, Microsoft.Extensions.AI, and first-class Model Context Protocol (MCP) support, aiming to standardize patterns for building agentic workflows, integrating external tools, enabling telemetry, and working across multiple AI providers
.

---

## Vector Search Is Now Production-Ready in Your Database

If you're building semantic search or RAG (Retrieval-Augmented Generation) systems, .NET 10 brings a significant quality-of-life improvement.
Vector search support includes full support for the new vector data type and VECTOR_DISTANCE() function, enabling AI workloads like semantic search and RAG with SQL Server 2025 and Azure SQL Database
.

What does this mean in practice? You can now write LINQ queries directly against vector columns without custom SQL:

```csharp
var results = await context.Documents
    .Where(d => EF.Functions.VectorDistance(d.Embedding, userQuery) < threshold)
    .OrderBy(d => EF.Functions.VectorDistance(d.Embedding, userQuery))
    .ToListAsync();
```
Vector similarity search is now production-ready with improved model building APIs and support for owned reference entities
. This eliminates the friction of managing embeddings in separate vector databases for many use cases.

---

## First-Class AI Agent Framework Support
AI-focused capabilities expand through the Microsoft Agent Framework, Microsoft.Extensions.AI, and first-class Model Context Protocol (MCP) support
.
The framework supports both Python and .NET environments, with developers able to install the Python version through pip package manager or integrate .NET support through NuGet packages
.

The Microsoft Agent Framework unifies what were previously two separate projects:
Semantic Kernel, which provided enterprise-ready foundations, and AutoGen, developed by Microsoft Research for experimental multi-agent systems
.

For .NET developers, this means you can now orchestrate multi-agent workflows with production-grade durability and enterprise controls—no more stitching together disparate libraries.

---

## Cloud-Native Orchestration with Aspire (Now Just "Aspire")
Aspire ships together with .NET 10 as a cloud-native application framework, strengthening orchestration for front ends, APIs, containers, and data stores, with improvements in development workflows, deployment performance, and multi-language integration
. 

The key win for AI teams:
the update adds simplified templates, new resource types, enhanced security options, and dashboard improvements, along with expanded support for coordinating Python, JavaScript, and other non-.NET services from a unified AppHost
. If you're running Python inference services alongside your .NET APIs, Aspire now makes that orchestration seamless.

---

## Security Improvements That Matter
Enhanced security includes audit transitive dependencies by default for .NET 10 projects, integration with GitHub Advisory Database, and Dependabot support for automatic security updates
. For production AI systems handling sensitive data, this is non-negotiable.

---

## The Practical Next Step
.NET 10 is a Long Term Support release and will be supported for three years until November 10, 2028. Microsoft strongly recommends that production applications upgrade to .NET 10 to take advantage of the extended support window, significant performance improvements, and new capabilities
.

If you're shipping AI features on Azure or building agent-based systems, the combination of vector search, Agent Framework integration, and Aspire orchestration makes .NET 10 worth upgrading to sooner rather than later. The three-year LTS window also means you're not chasing a moving target—a rare comfort in the AI ecosystem.

---

## Further reading

https://devblogs.microsoft.com/dotnet/announcing-dotnet-10/  
https://www.infoq.com/news/2025/11/dotnet-10-release/  
https://learn.microsoft.com/en-us/azure/ai-foundry/whats-new-azure-ai-foundry  
https://techcommunity.microsoft.com/blog/partnernews/october-update-whats-new-in-azure-for-partners/4465999  
https://github.blog/changelog/2025-11-13-openais-gpt-5-1-gpt-5-1-codex-and-gpt-5-1-codex-mini-are-now-in-public-preview-for-github-copilot/