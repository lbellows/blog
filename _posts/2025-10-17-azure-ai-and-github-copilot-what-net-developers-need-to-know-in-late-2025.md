---
author: the.serf
date: 2025-10-17 08:33:30 -0400
layout: post
tags:
- ai
- automation
- news
title: 'Azure AI and GitHub Copilot: What .NET Developers Need to Know in Late 2025'---
# Azure AI and GitHub Copilot: What .NET Developers Need to Know in Late 2025

**TL;DR**: Microsoft has unified its AI development stack with Azure AI Foundry SDK for .NET (in preview), expanded GitHub Copilot with app modernization agents in Visual Studio 2022 v17.14+, and introduced new Azure OpenAI API patterns. Key changes include keyless authentication via managed identity, new GPT-5 reasoning models, and Semantic Kernel reaching v1.0+ stability. If you're building AI-powered .NET apps, now is the time to consolidate around these tools.

---

## Azure AI Foundry SDK: One Client to Rule Them All


The AI Projects client library (in preview) is part of the Azure AI Foundry SDK and provides easy access to resources in your Azure AI Foundry Project.
 This represents a significant shift from the fragmented approach of managing separate SDKs for different Azure AI services.


The Azure AI Foundry SDK is a comprehensive toolchain designed to simplify the development of AI applications on Azure. It enables developers to: Access popular models from various model providers through a single interface · Easily combine together models, data, and AI services to build AI-powered applications · Evaluate, debug, and improve application quality & safety across development, testing, and production environments


### What This Means for Your Code

The new `Azure.AI.Projects` NuGet package (currently in preview) gives you a unified `AIProjectClient` that connects to a single project endpoint. 
Agents are now implemented in a separate package Azure.AI.Agents.Persistent, which will get installed automatically when you install Azure.AI.Projects.


**Important architectural change**: 
Support for project connection string and hub-based projects has been discontinued. We recommend creating a new Azure AI Foundry resource utilizing project endpoint. If this is not possible, please pin the version of Azure.AI.Projects to version 1.0.0-beta.8 or earlier.


Here's the basic setup pattern:

```csharp
using Azure.Identity;
using Azure.AI.Projects;

var client = new AIProjectClient(
    endpoint: new Uri("https://your-project.azure.ai"),
    credential: new DefaultAzureCredential()
);
```

This client gives you access to agents, Azure OpenAI chat clients, model deployments, and datasets—all from one entry point.

---

## Azure OpenAI for .NET: Authentication and API Evolution


The Azure OpenAI client library for .NET is a companion to the official OpenAI client library for .NET. The Azure OpenAI library configures a client for use with Azure OpenAI and provides additional strongly typed extension support for request and response models specific to Azure OpenAI scenarios.


### Keyless Authentication Is Now the Standard

The recommended authentication pattern has shifted to **Microsoft Entra ID (formerly Azure AD)** with managed identities. 
A secure, keyless authentication approach is to use Microsoft Entra ID (formerly Azure Active Directory) via the Azure Identity library.


```csharp
using Azure.AI.OpenAI;
using Azure.Identity;

var client = new AzureOpenAIClient(
    new Uri("https://your-resource.openai.azure.com"),
    new DefaultAzureCredential()
);

var chatClient = client.GetChatClient("gpt-4o-deployment");
```

This approach works seamlessly in both local development (using your Azure CLI credentials) and production (using system-assigned or user-assigned managed identities). No more rotating API keys in environment variables.

### API Versioning: Stability vs. Preview Features


Azure OpenAI API version 2024-10-21 is currently the latest GA API release. This API version is the replacement for the previous 2024-06-01 GA API release.


Microsoft is also introducing a new v1 API approach: 
Starting in August 2025, you can now opt in to our next generation v1 Azure OpenAI APIs which add support for: Ongoing access to the latest features with no need to specify new api-version's each month. Faster API release cycle with new features launching more frequently. OpenAI client support with minimal code changes to swap between OpenAI and Azure OpenAI when using key-based authentication.


**Practical takeaway**: If you need stable production APIs, stick with `2024-10-21`. If you want early access to new features like GPT-5 reasoning models or improved real-time audio, use the `2025-04-01-preview` version with feature-specific headers.

---

## GitHub Copilot: From Code Completion to App Modernization

GitHub Copilot has evolved far beyond autocomplete. 
The tool requires one of the following GitHub Copilot subscriptions: ... GitHub Copilot app modernization is included in Visual Studio 2022 version 17.14.16 or newer.


### The @modernize Agent


The modernization agent combines automated analysis, AI-driven code remediation, build and vulnerability checks, and deployment automation to simplify migrations to Azure.


You can invoke it by right-clicking a project in Solution Explorer and selecting "Modernize," or by typing `@modernize` in the Copilot Chat window. 
Once the process starts, Copilot analyzes your projects and their dependencies, and then asks you a series of questions about the upgrade. After you answer these questions, an upgrade plan is written in the form of a Markdown file.


**What it handles**:
- 
GitHub Copilot app modernization helps you upgrade your .NET (.NET, .NET Core, and .NET Framework) projects to newer versions of .NET.

- 
Migrate to Managed Identity based Database on Azure, including Azure SQL DB, Azure SQL MI, and Azure PostgreSQL

- 
Replace on-premises or cross-cloud object storage, or local file system file I/O, with Azure Blob Storage for unstructured data.


Each step is committed to your local Git repository, so you can roll back changes easily. 
When the upgrade completes, a report is generated that describes every step of the upgrade. The tool creates a Git commit for every portion of the upgrade process, so you can easily roll back the changes or get detailed information about what changed.


### Agent Mode and MCP Servers


Copilot Agent Mode is the next evolution in AI-assisted development and has moved out of preview. Over the past few months, we've made significant updates to Agent Mode to improve reliability, responsiveness, and overall usability.


Visual Studio now supports Model Context Protocol (MCP) servers: 
Copilot can then pull in context and take action using your existing systems. Note: You will need to be in Agent Mode to access and interact with MCP servers.


---

## Semantic Kernel: Production-Ready Orchestration


Semantic Kernel is a powerful and recommended choice for working with AI in .NET applications.
 
Version 1.0+ support across C#, Python, and Java means it's reliable, committed to non breaking changes.


### Core Concepts


Semantic Kernel is built around several core concepts: Connections: Interface with external AI services and data sources. Plugins: Encapsulate functions that applications can use. Planner: Orchestrates execution plans and strategies based on user behavior. Memory: Abstracts and simplifies context management for AI apps.


Install it via NuGet:

```bash
dotnet add package Microsoft.SemanticKernel
```

Basic kernel setup:

```csharp
using Microsoft.SemanticKernel;

var builder = Kernel.CreateBuilder();

builder.Services.AddAzureOpenAIChatCompletion(
    deploymentName: "gpt-4o",
    endpoint: "https://your-resource.openai.azure.com",
    credential: new DefaultAzureCredential()
);

var kernel = builder.Build();
```
