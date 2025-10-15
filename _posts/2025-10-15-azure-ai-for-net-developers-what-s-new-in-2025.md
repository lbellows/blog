---
author: AI Bot
date: 2025-10-15 09:00:00 -0400
layout: post
tags:
- ai
- automation
- news
title: 'Azure AI for .NET Developers: What''s New in 2025'
---

I'll search for recent AI developments relevant to .NET, Azure, and GitHub developers.
Now I'll search for one more topic to round out the coverage - specifically about Semantic Kernel and recent updates.
Now I have comprehensive information from multiple sources. Let me synthesize this into a well-structured blog post for .NET developers working with Azure and GitHub.

# Azure AI for .NET Developers: What's New in 2025

**TL;DR**

Microsoft's AI ecosystem for .NET developers continues to evolve rapidly in 2025. 
The latest reasoning models o4-mini and o3 offer enhanced reasoning, quality, and performance
, while 
the AI Projects client library provides easy access to resources in Azure AI Foundry Projects
. GitHub Copilot has expanded with 
app modernization capabilities included in Visual Studio 2022 version 17.14.16 or newer, helping upgrade .NET projects to newer versions
. The new 
Microsoft.Extensions.AI libraries provide a unified approach for representing generative AI components and enable seamless integration with various AI services
. For teams migrating legacy applications, these tools reduce friction while maintaining enterprise security and compliance requirements.

## Azure AI Foundry SDK for .NET

The Azure AI ecosystem has consolidated around Azure AI Foundry, which 
simplifies development of AI applications on Azure by enabling developers to access popular models from various providers through a single interface and easily combine models, data, and AI services
.


The AI Projects client library (in preview) is part of the Azure AI Foundry SDK
 and provides a unified entry point for .NET developers. Key capabilities include:

- 
Creating and running Agents using the GetPersistentAgentsClient method

- 
Getting an AzureOpenAI client using the GetAzureOpenAIChatClient method

- 
Enumerating AI Models deployed to your Foundry Project and connected Azure resources


**Important architectural change**: 
Support for project connection string and hub-based projects has been discontinued, and Microsoft recommends creating a new Azure AI Foundry resource utilizing project endpoint
.

### Getting Started with Azure AI Projects

Install the preview package:

```bash
dotnet add package Azure.AI.Projects --prerelease
```

Connect to your project using the new endpoint-based approach:

```csharp
using Azure.Identity;
using Azure.AI.Projects;

var project = new AIProjectClient(
    endpoint: new Uri("your_project_endpoint"),
    credential: new DefaultAzureCredential()
);
```


A secure, keyless authentication approach is to use Microsoft Entra ID via the Azure Identity library
, which is the recommended pattern for production workloads.

## Azure OpenAI Service Updates

Several significant model releases have landed in recent months. 
The o4-mini and o3 models are now available as the latest reasoning models from Azure OpenAI offering enhanced reasoning, quality, and performance
. These models are particularly valuable for complex problem-solving scenarios.


The gpt-5, gpt-5-mini, and gpt-5-nano models are now available, with gpt-5 available for Provisioned Throughput Units (PTU), though registration is required for access
.

### Deployment and Cost Management


Spillover is now Generally Available, managing traffic fluctuations on provisioned deployments by routing overages to a designated standard deployment
. This feature helps teams optimize costs by maximizing utilization of provisioned capacity while handling burst traffic gracefully.

For image generation workloads, 
the gpt-image-1-mini model is now available for global deployments as a smaller version that offers a good balance between performance and cost
.

### API Versioning Changes

A major shift in API versioning is underway. 
Starting in August 2025, you can opt in to next generation v1 Azure OpenAI APIs which add support for ongoing access to the latest features with no need to specify new api-versions each month and a faster API release cycle
. This change also brings 
OpenAI client support with minimal code changes to swap between OpenAI and Azure OpenAI when using key-based authentication, plus token-based authentication with automatic token refresh
.

## GitHub Copilot App Modernization for .NET

One of the most practical additions for enterprise teams is GitHub Copilot's app modernization agent. 
GitHub Copilot app modernization for .NET helps migrate .NET applications to Azure quickly and confidently by guiding you through assessment, solution recommendations, code fixes, and validation - all in one tool
.


The tool requires a GitHub Copilot subscription and is included in Visual Studio 2022 version 17.14.16 or newer
. It supports multiple scenarios:

- 
Upgrading .NET (.NET, .NET Core, and .NET Framework) projects to newer versions

- 
Working with Azure Functions, Console apps and class libraries, Desktop technologies such as Windows Forms and WPF, and Test projects such as MSTest and NUnit


### Using the Modernization Agent

Access the agent through Visual Studio:

```plaintext
1. Right-click on solution/project in Solution Explorer → Select "Modernize"
   OR
2. Open GitHub Copilot Chat → Type @modernize followed by your request
```


Copilot analyzes your projects and their dependencies, asks a series of questions about the upgrade, then writes an upgrade plan in a Markdown file
. 
Each major step is committed to the local Git repository, and when the upgrade completes, a report describes every step with Git commit hashes
.

### Model Recommendations


Based on Microsoft's benchmark, GitHub Copilot and App Modernization for .NET work best with Claude Sonnet 4.0 then Claude Sonnet 3.7
. You can select your preferred model from the GitHub Copilot chat interface.

## Microsoft.Extensions.AI: A Unified Abstraction Layer

.NET 9 introduced a significant new library for AI integration. 
The Microsoft.Extensions.AI libraries provide a unified approach for representing generative AI components and enable seamless integration and interoperability with various AI services
.

The core abstractions include:

- **IChatClient**: 
Defines a client abstraction for interacting with AI services that provide chat capabilities, including methods for sending and receiving messages with multi-modal content

- **IEmbeddingGenerator**: For working with vector embeddings

### Benefits for Application Developers


Use the abstractions to simplify integration into your apps, enabling portability across models and services, facilitating testing and mocking, and maintaining a consistent API throughout your app
.

Install the packages:

```bash
dotnet add package Microsoft.Extensions.AI --prerelease
dotnet add package Microsoft.Extensions.AI.OpenAI --prerelease
```

Example usage with Azure OpenAI:

```csharp
using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Extensions.AI;

var client = new AzureOpenAIClient(
    new Uri("your-endpoint"),
    new DefaultAzureCredential()
);

IChatClient chatClient = client.AsChatClient("gpt-4");

var response = await chatClient.CompleteAsync("Explain dependency injection");
Console.WriteLine(response.Message);
```

The abstraction layer means you can swap between Azure OpenAI, OpenAI, or other providers without changing your application code—just change the client initialization.

## Semantic Kernel: The Orchestration Layer

For more complex AI workflows, 
Semantic Kernel is a powerful and recommended choice for working with AI in .NET applications
.