---
author: the.serf
date: 2025-10-21 09:46:53 -0400
layout: post
tags:
- ai
- automation
- news
title: 'Azure OpenAI, GitHub Copilot, and Semantic Kernel: What .NET Developers Need
  to Know in 2025'---
# Azure OpenAI, GitHub Copilot, and Semantic Kernel: What .NET Developers Need to Know in 2025

**TL;DR**


Starting in August 2025, Azure OpenAI v1 APIs now support ongoing access to the latest features without specifying new api-version each month
. 
The .NET Aspire Azure OpenAI integration enables you to connect to Azure OpenAI Service or OpenAI's API from your .NET applications
. 
GitHub Copilot has reached more than 20 million users
, and 
Microsoft is open-sourcing GitHub Copilot Chat in VS Code, with AI-powered capabilities now part of the same open-source repository
. 
Semantic Kernel is a lightweight, open-source development kit that lets you easily build AI agents and integrate the latest AI models into your C#, Python, or Java codebase, serving as an efficient middleware
.

---

## Simplified Azure OpenAI Integration in .NET

### The v1 API Shift


Previously, Azure OpenAI received monthly updates of new API versions, requiring constantly updating code and environment variables with each new API release, and also required the extra step of using Azure specific clients
. This friction is now gone.


The new v1 APIs add OpenAI client support with minimal code changes to swap between OpenAI and Azure OpenAI when using key-based authentication, and support for token based authentication with automatic token refresh without needing a separate Azure OpenAI client
.

### Quick Setup with .NET Aspire


The .NET Aspire Azure OpenAI integration enables you to connect to Azure OpenAI Service from your .NET applications
. Here's a minimal example:

```csharp
var builder = DistributedApplication.CreateBuilder(args);
var openai = builder.AddAzureOpenAI("openai");
openai.AddDeployment(
    name: "preview",
    modelName: "gpt-4.5-preview",
    modelVersion: "2025-02-27");
builder.AddProject<Projects.ExampleProject>()
    .WithReference(openai);
```


When you call AddAzureOpenAI, it implicitly calls AddAzureProvisioning—which adds support for generating Azure resources dynamically during app startup
.

### Authentication Best Practices


The application uses DefaultAzureCredential, which automatically uses your Azure CLI signed in user for token authentication. Later when deployed, the same DefaultAzureCredential in your code can detect the managed identity and use it for authentication with no extra code needed
.

---

## Performance: Latency and Throughput Optimization

Cost and latency are critical for production workloads. Here are evidence-based strategies:

### Latency Fundamentals


Two key concepts matter: system level throughput measured in tokens per minute (TPM) and per-call response times (also known as latency)
.


If your use case requires the lowest latency models with the fastest response times, the latest GPT-4o mini model is recommended
.

### Practical Optimizations


Use regional deployments to improve response times for globally distributed teams, and optimize prompt design to reduce token usage and speed up responses
.


Streaming impacts perceived latency: with streaming enabled you receive tokens back in chunks as soon as they're available, which often feels faster to end-users even though the overall time to complete the request remains the same
.

---

## GitHub Copilot: Adoption and New Capabilities

### Scale and Enterprise Adoption


GitHub Copilot has now reached more than 20 million users
, and 
is used by 90% of the Fortune 100
.

### New Features for Developers


It's now possible to upload an image and ask Copilot to implement changes as indicated in the file, a feature that was available as an extension in VS Code since October with plans to deprecate in favor of native GitHub Copilot Chat
.


As of early 2025, the Copilot Code Review feature provides natural language feedback on code changes submitted through pull requests, aiming to emulate the role of a peer reviewer by identifying potential issues, including security concerns, and suggesting improvements
.

### Premium Requests and Costs


GitHub announced "premium requests" for GitHub Copilot, a new system that imposes rate limits when users switch to AI models other than the base model for tasks such as "agentic" coding and multi-file edits, while GitHub Copilot subscribers can still take unlimited actions with the base model (OpenAI's GPT-4o)
.


Customers on the Copilot Pro tier receive 300 monthly premium requests, Copilot Business and Enterprise users receive 300 and 1,000 monthly premium requests respectively, and customers can purchase additional premium requests at $0.04 per request
.

---

## Semantic Kernel: Building AI Agents in .NET


The Semantic Kernel SDK includes a set of connectors that enable developers to integrate LLMs and other services into their existing applications, serving as the bridge between the application code and the AI models or services
.

### Core Concepts


Semantic Kernel leverages function calling—a native feature of most LLMs—to provide planning; with function calling, LLMs can request a particular function to satisfy a user's request, and Semantic Kernel marshals the request to the appropriate function in your codebase and returns the results back to the LLM
.

### Installation and Basic Setup

```csharp
dotnet add package Microsoft.SemanticKernel
dotnet add package Microsoft.Extensions.Logging.Console

var builder = Kernel.CreateBuilder();
builder.Services.AddAzureOpenAIChatCompletion(
    "your-resource-name",
    "your-endpoint",
    "your-resource-key",
    "deployment-model");
var kernel = builder.Build();
```


Semantic Kernel's Vector stores provide abstractions over embedding models, vector databases, and other data to simplify context management for AI applications, and are agnostic to the underlying LLM or Vector database, offering a uniform developer experience with support for Azure AI Search and Azure Cache for Redis
.

### Next Generation: Microsoft Agent Framework


Microsoft Agent Framework is an open-source development kit for building AI agents and multi-agent workflows for .NET and Python, and is the direct successor to Semantic Kernel, combining AutoGen's simple abstractions for single- and multi-agent patterns with Semantic Kernel's enterprise-grade features such as thread-based state management, type safety, filters, telemetry, and extensive model and embedding support
.

---

## GitHub Models: Free Prototyping Path


GitHub Models provides access to various AI models including OpenAI's GPT models, DeepSeek, Microsoft's Phi models, and other leading AI models, all accessible through GitHub's infrastructure, and the Aspire GitHub Models integration enables you to connect to GitHub Models from your .NET applications for prototyping and production scenarios
.

### Rate Limits and Upgrade Path


The playground and free API usage for GitHub Models are rate limited by requests per minute, requests per day, tokens per request, and concurrent requests; if you get rate limited, you need to wait for the rate limit to reset before making more requests
.


GitHub Models are useful when you want to find and experiment with AI models for free as you develop a generative AI application
