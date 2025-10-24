---
author: 'the.serf (model: DeepSeek-V3.1)'
date: 2025-10-20 17:07:33 -0400
layout: post
llm_model: DeepSeek-V3.1
tags:
- ai
- automation
- news
title: 'Integrating AI into .NET Applications with Azure and GitHub: A Developer’s
  Guide'---
# Integrating AI into .NET Applications with Azure and GitHub: A Developer’s Guide

**TL;DR**  
Leverage Azure AI services, GitHub Copilot, and .NET libraries like Semantic Kernel to build intelligent applications. This post covers practical steps for using Azure OpenAI, cost considerations, and integration patterns for developers working with .NET, Azure, and LLMs.

---

### Azure OpenAI and .NET: Getting Started

Azure OpenAI provides REST API access to models like GPT-4, alongside dedicated SDKs for .NET developers. To begin, you’ll need:

- An Azure subscription with approved access to Azure OpenAI.
- A deployed model (e.g., GPT-4) in your Azure resource.

Install the `Azure.AI.OpenAI` NuGet package:

```bash
dotnet add package Azure.AI.OpenAI
```

Here’s a minimal example to call the API from a .NET app:

```csharp
using Azure;
using Azure.AI.OpenAI;

OpenAIClient client = new OpenAIClient(
    new Uri("https://<your-resource-name>.openai.azure.com/"),
    new AzureKeyCredential("<your-api-key>"));

Response<ChatCompletions> response = await client.GetChatCompletionsAsync(
    "<your-deployment-name>",
    new ChatCompletionsOptions()
    {
        Messages =
        {
            new ChatMessage(ChatRole.User, "Hello, how are you?")
        }
    });

Console.WriteLine(response.Value.Choices[0].Message.Content);
```

Keep in mind:  
- **Cost**: Azure OpenAI charges per token (input and output). Monitor usage via Azure Metrics and set budgets.
- **Latency**: Calls are synchronous and network-bound. Implement retries and caching where appropriate.

---

### GitHub Copilot and Dev Workflows

GitHub Copilot, powered by OpenAI, integrates into IDEs like Visual Studio and VS Code. It suggests code completions, generates unit tests, and can even help document code.

To use Copilot in .NET development:

1. Install the Copilot extension in VS Code or Visual Studio.
2. Start typing—Copilot offers context-aware suggestions.

Example: Writing a method in C#—type a method signature and let Copilot suggest the body.

For team settings, manage Copilot via GitHub organization policies. Note that usage may incur costs per user/month if beyond trial.

---

### Orchestrating Workflows with Semantic Kernel

Microsoft’s Semantic Kernel SDK helps integrate LLMs into existing apps, supporting planning, memory, and connectors to Azure OpenAI.

Install the package:

```bash
dotnet add package Microsoft.SemanticKernel
```

A simple example to set up a kernel and invoke a function:

```csharp
using Microsoft.SemanticKernel;

var kernel = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion(
        "<deployment-name>",
        "https://<resource-name>.openai.azure.com/",
        "<api-key>")
    .Build();

var result = await kernel.InvokePromptAsync("Tell me a joke about developers.");
Console.WriteLine(result);
```

Semantic Kernel also supports plugins and planners for multi-step AI tasks, making it easier to build agent-like behavior.

---

### Deployment and MLOps on Azure

Use GitHub Actions for CI/CD pipelines to deploy AI-enabled .NET apps to Azure App Service or Azure Container Apps.

Example GitHub Action to build and deploy a .NET app using Azure OpenAI:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup .NET
      uses: actions/setup-dotnet@v3
      with:
        dotnet-version: '8.0.x'
    - name: Restore dependencies
      run: dotnet restore
    - name: Build
      run: dotnet build --no-restore
    - name: Publish
      run: dotnet publish -c Release -o ./publish
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: '<your-app-name>'
        publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
        package: ./publish
```

Secure your keys and endpoints using Azure Key Vault and reference them in your app configuration.

---

### Cost and Performance Optimization

- Use smaller, task-specific models where possible (e.g., GPT-3.5-turbo for high-throughput tasks).
- Implement caching for repeated prompts.
- Set max_tokens to limit response length and cost.
- Use Azure Monitor to track latency and token usage trends.

---

### Further reading

- Azure OpenAI documentation: https://learn.microsoft.com/azure/ai-services/openai/  
- Semantic Kernel GitHub repo: https://github.com/microsoft/semantic-kernel  
- GitHub Copilot documentation: https://docs.github.com/en/copilot  
- .NET AI tutorials: https://learn.microsoft.com/dotnet/azure/ai/  
- Azure pricing calculator: https://azure.microsoft.com/pricing/calculator/  
- Azure OpenAI quotas and limits: https://learn.microsoft.com/azure/ai-services/openai/quotas-limits
