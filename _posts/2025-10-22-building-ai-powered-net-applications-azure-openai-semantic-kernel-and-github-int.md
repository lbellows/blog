---
author: the.serf
date: 2025-10-22 07:28:17 -0400
layout: post
tags:
- ai
- automation
- news
title: 'Building AI-Powered .NET Applications: Azure OpenAI, Semantic Kernel, and
  GitHub Integration in 2025'
---

I'll search for recent AI developments relevant to .NET, Azure, GitHub, and LLM integration for developers.
Now I have comprehensive, current information from reputable sources. Let me synthesize this into a well-structured blog post for .NET/Azure/GitHub developers.

---

# Building AI-Powered .NET Applications: Azure OpenAI, Semantic Kernel, and GitHub Integration in 2025

## TL;DR


Azure OpenAI is a managed service that allows developers to deploy, tune, and generate content from OpenAI models on Azure resources.
 
Semantic Kernel is a lightweight, open-source development kit that lets you easily build AI agents and integrate the latest AI models into your C#, Python, or Java codebase.
 
GitHub Models provides access to various AI models including OpenAI's GPT models, DeepSeek, Microsoft's Phi models, and other leading AI models, all accessible through GitHub's infrastructure, enabling you to connect to GitHub Models from your .NET applications for prototyping and production scenarios.
 Cost optimization through intelligent model routing and fine-tuning, combined with secure authentication patterns, is now essential for production deployments.

---

## Getting Started: Azure OpenAI SDK for .NET


Although client instantiation is similar to previous versions, the latest release introduces a distinct, Azure-specific top-level client that individual scenario clients are retrieved from.
 Here's the recommended setup pattern:

```csharp
using Azure.AI.OpenAI;
using Azure.Identity;

// Create an Azure OpenAI client with Microsoft Entra ID
AzureOpenAIClient azureClient = new(
    new Uri("https://your-resource.openai.azure.com/"),
    new DefaultAzureCredential()
);

// Get a chat client for a specific deployment
ChatClient chatClient = azureClient.GetChatClient("my-gpt-4o-mini-deployment");
```


Microsoft Entra ID is the recommended solution to connect to Azure OpenAI and other AI services and provides keyless authentication using identities, role-based access control (RBAC) to assign identities the minimum required permissions, the ability to use the Azure.Identity client library to detect different credentials across environments without requiring code changes, and automatically handles administrative maintenance tasks such as rotating underlying keys.


**Install the required NuGet packages:**

```bash
dotnet add package Azure.AI.OpenAI
dotnet add package Azure.Identity
dotnet add package Microsoft.Extensions.AI
```

---

## Semantic Kernel: Enterprise-Grade AI Agent Development


Semantic Kernel serves as an efficient middleware that enables rapid delivery of enterprise-grade solutions, with Microsoft and other Fortune 500 companies already leveraging it because it's flexible, modular, and observable, backed with security enhancing capabilities like telemetry support, and hooks and filters so you'll feel confident you're delivering responsible AI solutions at scale.


### Core Concepts for .NET Developers


The Semantic Kernel SDK includes a set of connectors that enable developers to integrate LLMs and other services into their existing applications, serving as the bridge between the application code and the AI models or services.


**Basic kernel setup:**

```csharp
using Microsoft.SemanticKernel;

var builder = Kernel.CreateBuilder();

// Add Azure OpenAI chat completion
builder.Services.AddAzureOpenAIChatCompletion(
    "your-deployment-name",
    "https://your-resource.openai.azure.com/",
    "your-api-key"
);

var kernel = builder.Build();

// Invoke a prompt
var response = await kernel.InvokePromptAsync("What is .NET?");
Console.WriteLine(response);
```


Semantic Kernel leverages function calling–a native feature of most LLMs–to provide planning, with LLMs able to request (or call) a particular function to satisfy a user's request, and Semantic Kernel then marshals the request to the appropriate function in your codebase and returns the results back to the LLM so the AI agent can generate a final response.


---

## Cost Optimization: Model Router and Fine-Tuning

Production deployments require careful cost management. 
Model router for Azure AI Foundry is a deployable AI chat model that is trained to select the best large language model (LLM) to respond to a given prompt in real time, by evaluating factors like query complexity, cost, and performance, it intelligently routes requests to the most suitable model, thus delivering high performance while saving on compute costs where possible, all packaged as a single model deployment.



Fine-tuning GPT-4o mini with hundreds of requests and correct responses produces a model that performs better than the base model with lower costs and latency.
 However, 
start by evaluating the baseline performance of a standard model against your requirements before considering this option, as having a baseline for performance without fine-tuning is essential for knowing whether fine-tuning has improved model performance, and fine-tuning with bad data makes the base model worse, but without a baseline, it's hard to detect regressions.


### Token Billing


Language models understand and process inputs by breaking them down into tokens, with each token roughly four characters for typical English text, and costs per token vary depending on which model series you choose but in all cases models deployed in Azure AI Foundry are charged per 1,000 tokens, for example, Azure OpenAI chat completions model inference is charged per 1,000 tokens with different rates depending on the model and deployment type.


---

## GitHub Copilot and GitHub Models Integration

### GitHub Copilot for Enterprise


GitHub announced the general availability of Copilot Enterprise, the $39/month version of its code completion tool and developer-centric chatbot for large businesses, which includes all of the features of the existing Business plan, including IP indemnity, but extends this with a number of crucial features for larger teams, with the highlight being the ability to reference an organization's internal code and knowledge base.


### GitHub Models for Rapid Prototyping


GitHub Models are useful when you want to find and experiment with AI models for free as you develop a generative AI application, and when you're ready to bring your application to production, upgrade your experience by deploying an Azure AI Services resource in an Azure subscription and start using Foundry Models without needing to change anything else in your code.


**Quick integration with .NET Aspire:**

```csharp
// In GitHub Codespaces or GitHub Actions, GITHUB_TOKEN is automatic
var chat = builder.AddGitHubModel("chat", "openai/gpt-4o-mini");

// For local development, use a fine-grained PAT
// { "Parameters": { "chat-gh-apikey": "github_pat_YOUR_TOKEN_HERE" } }
```

---

## Model Context Protocol (MCP) and GitHub Copilot Chat


Building a Model Context Protocol (MCP) agent using .NET involves an MCP client (written in C#/.NET) connecting to an MCP server (written in TypeScript) to manage a todo list, where the client finds available tools from the server and sends them to an Azure OpenAI model, allowing users to then talk to the todo system using everyday language.



By exposing an ASP.NET Core app's functionality through Model Context Protocol (MCP), adding it as a tool to GitHub Copilot, and interacting with your app using natural language in Copilot Chat agent mode, by adding an MCP server to your web app, you enable an agent to understand and use your app's capabilities when it responds to user prompts, meaning anything your app can do, the agent can do too.


---

## Scaling and Rate Limits


While the maximum token limit per request is defined by the model itself (e.g., 128k tokens for GPT-4-128k), you can request an increase in your throughput quota — specifically, tokens per minute (TPM), requests per minute (RPM), and concurrent requests, which can be done via the Azure portal under Service and subscription limits (quotas) by providing your expected workload details.



For large and non-time-sensitive queries,