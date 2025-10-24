---
author: the.serf
date: 2025-10-23 07:27:54 -0400
layout: post
tags:
- ai
- automation
- news
title: 'Building AI-Powered .NET Apps on Azure: SDKs, Costs, and Integration Patterns'---
# Building AI-Powered .NET Apps on Azure: SDKs, Costs, and Integration Patterns

**TL;DR**


Azure OpenAI is a managed service that allows developers to deploy, tune, and generate content from OpenAI models on Azure resources.
 
Semantic Kernel is a lightweight, open-source SDK that lets you build AI agents and integrate the latest AI models into your .NET apps.
 
GitHub Copilot app modernization is an AI-powered agent in Visual Studio that helps you upgrade .NET projects to newer versions and migrate applications to Azure.
 Billing is per-token (~4 characters each), and 
model router for Azure AI Foundry is a deployable AI chat model that is trained to select the best large language model (LLM) to respond to a given prompt in real time. By evaluating factors like query complexity, cost, and performance, it intelligently routes requests to the most suitable model. Thus, it delivers high performance while saving on compute costs where possible.


---

## Getting Started: Azure OpenAI SDK for .NET


Azure OpenAI is a managed service that allows developers to deploy, tune, and generate content from OpenAI models on Azure resources.
 The primary entry point is the Azure.AI.OpenAI NuGet package.

### Basic Setup


Microsoft Entra ID is the recommended solution to connect to Azure OpenAI and other AI services and provides the following benefits: Keyless authentication using identities. Role-based access control (RBAC) to assign identities the minimum required permissions. Can use the Azure.Identity client library to detect different credentials across environments without requiring code changes. Automatically handles administrative maintenance tasks such as rotating underlying keys.


```csharp
// Install packages
// dotnet add package Azure.AI.OpenAI
// dotnet add package Azure.Identity

using Azure;
using Azure.AI.OpenAI;

var client = new AzureOpenAIClient(
    new Uri("https://your-resource.openai.azure.com/"),
    new DefaultAzureCredential()
);

var chatClient = client.GetChatClient("your-deployment-name");
```


The workflow to implement Microsoft Entra authentication in your app generally includes the following steps: Sign-in to Azure using a local dev tool such as the Azure CLI or Visual Studio. Configure your code to use the Azure.Identity client library and DefaultAzureCredential class. Assign a role to the security principal used by DefaultAzureCredential to connect to an Azure AI service, whether that's an individual user, group, service principal, or managed identity. Assign roles such as Cognitive Services OpenAI User (role ID: 5e0bd9bd-7b93-4f28-af87-19fc36ad61bd) to the relevant identity using tools such as the Azure CLI, Bicep, or the Azure Portal.


---

## Building with Semantic Kernel


Semantic Kernel is a lightweight, open-source development kit that lets you easily build AI agents and integrate the latest AI models into your C#, Python, or Java codebase. It serves as an efficient middleware that enables rapid delivery of enterprise-grade solutions.


### Quick Start

```csharp
// Install core packages
// dotnet add package Microsoft.SemanticKernel
// dotnet add package Microsoft.Extensions.Logging.Console

using Microsoft.SemanticKernel;

var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion(
    deploymentName: "gpt-4o-mini",
    endpoint: "https://your-resource.openai.azure.com/",
    apiKey: Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")
);

var kernel = builder.Build();
var response = await kernel.InvokePromptAsync("What is the capital of France?");
Console.WriteLine(response);
```


The Semantic Kernel SDK includes a set of connectors that enable developers to integrate LLMs and other services into their existing applications. These connectors serve as the bridge between the application code and the AI models or services. Semantic Kernel handles many common connection concerns and challenges for you so you can focus on building your own workflows and features.


### Agent Framework: The Next Generation


Microsoft Agent Framework is an open-source development kit for building AI agents and multi-agent workflows for .NET and Python. It brings together and extends ideas from Semantic Kernel and AutoGen projects, combining their strengths while adding new capabilities. Built by the same teams, it is the unified foundation for building AI agents going forward.


---

## GitHub Copilot Integration for .NET Developers

### App Modernization Agent


GitHub Copilot app modernization is an AI-powered agent in Visual Studio that helps you upgrade .NET projects to newer versions and migrate applications to Azure.
 
Starting with Visual Studio 2022 17.14.16, the GitHub Copilot app modernization agent is included with Visual Studio. If you're using an older version of Visual Studio 2022, upgrade to the latest release.


### Model Context Protocol (MCP) Integration


This article shows you how to build a Model Context Protocol (MCP) agent using .NET. In this sample, the MCP client (written in C#/.NET) connects to an MCP server (written in TypeScript) to manage a todo list. The client finds available tools from the server and sends them to an Azure OpenAI model. Users can then talk to the todo system using everyday language.



Empower GitHub Copilot Chat with your existing .NET web apps by integrating their capabilities as Model Context Protocol servers, enabling Copilot Chat to perform real-world tasks.


---

## Cost Optimization and Billing

### Token-Based Pricing


Language models understand and process inputs by breaking them down into tokens. For reference, each token is roughly four characters for typical English text.
 
Costs per token vary depending on which model series you choose but in all cases models deployed in Azure AI Foundry are charged per 1,000 tokens. For example, Azure OpenAI chat completions model inference is charged per 1,000 tokens with different rates depending on the model and deployment type.


### Billing Models


Two billing models are available for Azure AI services: Serverless API: With serverless API pricing, you're billed according to the Azure AI services offering that you use, based on its billing information. Commitment tiers: With commitment tier pricing, you commit to using several service features for a fixed fee, enabling you to have a predictable total cost based on the needs of your workload.


### Smart Model Routing


Model router for Azure AI Foundry is a deployable AI chat model that is trained to select the best large language model (LLM) to respond to a given prompt in real time. By evaluating factors like query complexity, cost, and performance, it intelligently routes requests to the most suitable model. Thus, it delivers high performance while saving on compute costs where possible. Model router intelligently selects the best underlying model for a given prompt to optimize costs while maintaining quality. Smaller and cheaper models are used when they're sufficient for the task, but larger and more expensive models are available for more complex tasks.


### Fine-Tuning Costs


They fine-tune GPT-4o mini with hundreds of requests and correct responses and produce a model that performs better than the base model with lower costs and latency.
 However, 
fine-tuning has upfront costs for training the model.
 Consider establishing a baseline before investing in fine-tuning.

---

## Scaling and Quota Management


Tokens per minute (TPM) and requests per minute (RPM) limits are defined per region, per subscription, and per model or deployment type. For example, if the gpt-4.1 Global Standard model is
