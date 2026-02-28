---
author: the.serf
date: 2026-02-28 06:32:21 -0500
layout: post
tags:
- agent
- azd
- azure
- coding
- february
- claude-sonnet-4-6
title: '`azd` February 2026: The CLI That Finally Knows When an AI Is Driving'
---

# `azd` February 2026: The CLI That Finally Knows When an AI Is Driving

**Published: February 28, 2026 | Audience: .NET & Azure engineers shipping AI workloads**

---

## TL;DR

The Azure Developer CLI (`azd`) February 2026 drop (versions 1.23.3–1.23.6) shipped a quietly important quality-of-life feature: **AI coding agent auto-detection**. When `azd` senses it's running inside an AI coding agent, it now skips interactive prompts automatically so your automated CI and agentic workflows no longer hang mid-deploy waiting for a human who isn't there. Alongside that, the release adds JMESPath query support for JSON output filtering, App Service deployment slot support, and remote build for Azure Functions Flex Consumption plans. Every one of these updates has a direct productivity payoff for teams building .NET and Azure AI apps.

---

## Why This Release Deserves Your Full Attention

We're in a moment where AI coding agents — Copilot, Cursor, Devin, take your pick — are being given actual shell access and told to "just deploy it." The problem? Most CLIs were designed for humans: they pause, they prompt, they wait. An AI agent staring at `Enter your Azure subscription [1-3]:` is about as useful as a golden retriever doing your taxes.
The February `azd` release addresses this head-on: `azd` now detects when it's running inside an AI coding agent and skips interactive prompts automatically, so automated workflows don't hang.
That's a small sentence with big implications. If you're wiring up an AI agent to provision infrastructure and deploy your ASP.NET Core app, this means the agent can now call `azd up` without you needing to pre-bake every environment variable or add `--no-prompt` hacks throughout your pipeline.
The February release post covers versions 1.23.3, 1.23.4, 1.23.5, and 1.23.6.
---

## The Full Feature Rundown (Engineer Edition)

### 1. AI Coding Agent Auto-Detection

As noted above, `azd` now behaves non-interactively when an AI agent is at the helm. Pair this with the existing `azd ai agent` extension and you have a coherent story:
the `azd` AI agent extension lets you scaffold and deploy agents from your terminal or editor, combining Foundry capabilities with `azd` lifecycle commands (`azd init`, `azd up`) for a consistent local-to-cloud workflow.
In practice, this means your Copilot-driven CI pipeline can now run end-to-end:

```bash
# Run by an AI coding agent — no human prompts required
azd auth login --client-id $CLIENT_ID --client-secret $CLIENT_SECRET --tenant-id $TENANT_ID
azd provision
azd deploy
```

No hanging. No timeouts. No sad Slack messages at 2 AM.

---

### 2. JMESPath Query Support (`--query`)
The new `--query` flag lets you filter and transform JSON output from any `azd` command using JMESPath expressions — great for scripting and automation. Query support also covers Message-type outputs, so filtering works consistently across all commands.
This is a significant ergonomic win for shell scripting and CI pipelines. Instead of piping to `jq` (which may not be installed in your build agent image), you can do:

```bash
# Get only the endpoint URL from azd output
azd show --output json --query "services.api.endpoint"
```

If you've ever written a 12-line `jq` filter to extract a connection string from `azd env get-values`, you'll appreciate this.

---

### 3. App Service Deployment Slot Support
`azd` now deploys directly to Azure App Service deployment slots without extra scripts.
Blue-green deployments from the CLI — no more bespoke PowerShell wrappers around `az webapp deployment slot swap`.

```bash
# Deploy to a staging slot instead of production
azd deploy --slot staging
```

---

### 4. Remote Build for Azure Functions Flex Consumption
A new `remoteBuild` configuration option enables remote builds when deploying to Azure Functions Flex Consumption plans, avoiding local build requirements.
For teams running `azd` in lean container-based CI agents (or, again, AI coding agents with a minimal toolchain), this means you no longer need the full .NET SDK present locally to ship a Function App. The build happens in Azure.

In your `azure.yaml`:

```yaml
services:
  myfunc:
    project: ./src/MyFunctionApp
    host: function
    remoteBuild: true
```

---

### 5. The Azure SDK February 2026 Drop (Bonus Context)

While `azd` is the headline story, the broader
Azure SDK February 2026 release adds core support for `Microsoft.Extensions.Configuration` and `Microsoft.Extensions.DependencyInjection`, enabling better integration with ASP.NET Core applications and other .NET hosts.
The update also implements support for client certificate rotation in the `Azure.Core` transport layer, enabling dynamic token binding scenarios where transport instances can be updated with new client certificate configurations at runtime without requiring full pipeline reconstruction.
And for the Python side of the house (relevant if your .NET app calls a Python sidecar or data service):
the initial beta release of the Azure AI Content Understanding client library for Python introduces the `ContentUnderstandingClient` for analyzing documents, audio, and video content using Azure AI Foundry's content understanding capabilities — developers can now extract meaningful insights from various content types through a unified API.
A .NET NuGet for `Azure.AI.ContentUnderstanding` is also in preview.
The preview release of the .NET NuGet for the ContentUnderstanding SDK is now available and can be installed with: `dotnet add package Azure.AI.ContentUnderstanding --prerelease`
---

## Practical Takeaways

| Feature | What to do now |
|---|---|
| AI agent auto-detection | Update to `azd` ≥ 1.23.3 (`winget upgrade azd` / `brew upgrade azd`) |
| JMESPath `--query` | Replace `\| jq` calls in CI scripts |
| App Service slots | Remove manual `az webapp deployment slot` wrappers |
| Remote build for Functions | Add `remoteBuild: true` in `azure.yaml` for lean build agents |
| Azure SDK .NET DI support | Upgrade `Azure.Core` and wire up `IServiceCollection` |
| Content Understanding (preview) | `dotnet add package Azure.AI.ContentUnderstanding --prerelease` |

---

## One Deadline You Cannot Ignore

Buried in the recent Foundry release notes, worth a loud reminder:
the Azure Machine Learning SDK v1 reaches end of support on June 30, 2026 — after this date, existing workflows may face security risks and breaking changes without active Microsoft support.
The AzureML CLI v1 extension already reached end of support on September 30, 2025.
If you have training pipelines still on v1, the clock is ticking louder than it sounds.

---

## Closing Thought

The `azd` AI agent auto-detection feature is small in lines of code but large in signal: Microsoft is actively designing its developer toolchain to be operated *by* AI agents, not just *for* engineers using AI assistants. For .NET teams building agentic apps on Azure, the toolchain is catching up to the ambition. Update your CLI, swap in JMESPath, and let the robots deploy in peace.

---

## Further Reading

- Azure Developer CLI February 2026 Release Notes: https://devblogs.microsoft.com/azure-sdk/azure-developer-cli-azd-february-2026/
- Azure SDK Release (February 2026): https://devblogs.microsoft.com/azure-sdk/azure-sdk-release-february-2026/
- Use the Microsoft Foundry `azd` Agent Extension: https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/extensions/azure-ai-foundry-extension
- What's New in Microsoft Foundry (Dec 2025 & Jan 2026): https://devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-dec-2025-jan-2026/
- Azure Content Understanding — What's New: https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/whats-new
- Azure Content Understanding .NET SDK Roadmap (Q&A): https://learn.microsoft.com/en-us/answers/questions/5651099/road-map-for-azure-content-understanding
- Microsoft Foundry SDK Overview: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview
- Generative AI with LLMs in .NET and C# (2026): https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/