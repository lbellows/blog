---
author: the.serf
date: 2025-10-19 07:24:32 -0400
layout: post
tags:
- ai
- automation
- news
title: 'Integrating LLMs into .NET: Azure, GitHub, and Cost-Latency Tradeoffs in 2025'
---
# Integrating LLMs into .NET: Azure, GitHub, and Cost-Latency Tradeoffs in 2025

**TL;DR**  

The Azure OpenAI client library for .NET configures a client for use with Azure OpenAI and provides additional strongly typed extension support for request and response models specific to Azure OpenAI scenarios.
 
NVIDIA TensorRT-LLM optimizations have achieved a 45% increase in throughput for Llama 3.3 70B and Llama 3.1 70B models and a 34% increase for the Llama 3.1 8B model.
 
Semantic Kernel is a lightweight, open-source development kit that lets you easily build AI agents and integrate the latest AI models into your C#, Python, or Java codebase, serving as an efficient middleware that enables rapid delivery of enterprise-grade solutions.
 Cost optimization and latency reduction now demand fine-tuning, prompt caching, and careful model selection—not just throwing compute at the problem.

---

## Getting Started: Azure OpenAI SDK for .NET


Create an AzureOpenAIClient with DefaultAzureCredential and get a ChatClient for your deployment.
 Here's the essentials:

```csharp
using Azure;
using Azure.AI.OpenAI;

var azureClient = new AzureOpenAIClient(
    new Uri("https://your-azure-openai-resource.openai.azure.com/"),
    new DefaultAzureCredential());

var chatClient = azureClient.GetChatClient("my-gpt-4o-mini-deployment");

var completion = chatClient.CompleteChat(
    new ChatMessage(ChatRole.System, "You are a helpful assistant."),
    new ChatMessage(ChatRole.User, "Explain RAG in one sentence.")
);

Console.WriteLine(completion.Content[0].Text);
```


Users can access the service through REST APIs, Python/C#/JS/Java/Go SDKs.
 No surprises here—standard dependency injection and async patterns apply.

---

## Cost and Latency: The Real Challenges

### Token Counting and Throughput


Two key concepts when sizing an application are system level throughput measured in tokens per minute (TPM) and per-call response times (latency), which looks at the overall capacity of your deployment.
 
Ways to reduce the number of tokens include setting the max_tokens parameter on each call as small as possible and including stop sequences to prevent generating extra content.


Monitor your usage in Azure Monitor:

```bash
# Check Processed Prompt Tokens and Generated Completion Tokens metrics
# Use minimum, average, and maximum aggregation over 1-minute windows
```

### Fine-Tuning vs. RAG vs. Prompt Engineering


Fine-tuning GPT-4o mini with hundreds of requests and correct responses can produce a model that performs better than the base model with lower costs and latency.
 However, 
start by evaluating the baseline performance of a standard model against requirements before considering this option; having a baseline for performance without fine-tuning is essential for knowing whether fine-tuning has improved model performance, and fine-tuning with bad data makes the base model worse.



RAG (Retrieval Augmented Generation) is a method that integrates external data into a Large Language Model prompt to generate relevant responses, particularly beneficial when using a large corpus of unstructured text based on different topics.


**Practical guidance**: Start with prompt engineering and RAG. Only fine-tune if you have high-quality training data and a clear performance baseline.

---

## GitHub Copilot Enterprise and App Modernization


GitHub Copilot Enterprise is designed as an intelligent companion for developers, making the vast repository of your organization's institutional knowledge readily accessible.
 
GitHub Copilot app modernization is an all-in-one upgrade and migration assistant that uses AI to improve developer velocity, quality, and results.


For .NET developers, 
GitHub Copilot app modernization offers predefined tasks covering common migration scenarios, including migrating to Managed Identity based Database on Azure.
 In Visual Studio, invoke the `@modernize` agent:

```
@modernize Upgrade my .NET Framework project to .NET 9 and migrate to Azure SQL with managed identity
```

---

## Semantic Kernel and Agentic Patterns


The Semantic Kernel Agent Framework provides a platform that allows for the creation of AI agents and the ability to incorporate agentic patterns into any application; agents can send and receive messages, generating responses using a combination of models, tools, human inputs, or other customizable components.


Install and bootstrap:

```bash
dotnet add package Microsoft.SemanticKernel
dotnet add package Microsoft.Extensions.Logging
```

```csharp
using Microsoft.SemanticKernel;

var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAIChatCompletion(
    deploymentName: "gpt-4o",
    endpoint: new Uri("https://your-resource.openai.azure.com/"),
    apiKey: apiKey);

var kernel = builder.Build();

// Add plugins for your business logic
kernel.ImportPluginFromType<YourPlugin>();

// Create and invoke an agent
var agent = new ChatCompletionAgent { Kernel = kernel };
```


Agent Framework is the next generation of both Semantic Kernel and AutoGen, created by the same teams, combining AutoGen's simple abstractions for single- and multi-agent patterns with Semantic Kernel's enterprise-grade features such as thread-based state management, type safety, filters, telemetry, and extensive model and embedding support.


---

## GitHub Models: Prototyping Without Azure Costs


GitHub Models provides access to various AI models including OpenAI's GPT models, DeepSeek, Microsoft's Phi models, and other leading AI models, all accessible through GitHub's infrastructure; the Aspire GitHub Models integration enables you to connect to GitHub Models from your .NET applications for prototyping and production scenarios.


With .NET Aspire:

```bash
dotnet add package Aspire.Hosting.GitHub.Models
dotnet add package Aspire.Azure.AI.Inference
```

```csharp
var builder = DistributedApplication.CreateBuilder(args);
var chat = builder.AddGitHubModel("chat", "openai/gpt-4o-mini");
builder.AddProject<Projects.MyApp>()
    .WithReference(chat);
```


GitHub Models are useful when you want to find and experiment with AI models for free as you develop a generative AI application; when you're ready to bring your application to production, upgrade your experience by deploying an Azure AI Services resource in an Azure subscription and start using Foundry Models.


---

## Performance Optimization: NVIDIA TensorRT-LLM on Azure


Microsoft, in collaboration with NVIDIA, announced transformative performance improvements for the Meta Llama family of models on its Azure AI Foundry platform; these advancements, enabled by NVIDIA TensorRT-LLM optimizations, have achieved a 45% increase in throughput for Llama 3.3 70B and Llama 3.1 70B models and a 34% increase for the Llama 3.1 8B model, allowing developers to build more efficient and responsive AI-powered applications on Azure AI Foundry.



NIM deployed on Azure AI Foundry can be accessed through standard APIs, making it easy to integrate into Azure services like AI Agent Service and agentic AI frameworks like Semantic Kernel.


---

## API Management and Semantic Caching


You can import OpenAI-compatible language model endpoints to your API Management instance as APIs, using AI gateway policies and other capabilities in API Management to simplify integration, improve observability, and enhance control over the model endpoints.
