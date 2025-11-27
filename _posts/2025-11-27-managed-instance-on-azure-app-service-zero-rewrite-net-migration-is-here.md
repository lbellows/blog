---
author: the.serf
date: 2025-11-27 06:29:07 -0500
layout: post
tags:
- .net
- migration
- app
- azure
- bigger
- claude-haiku-4-5-20251001
title: 'Managed Instance on Azure App Service: Zero-Rewrite .NET Migration Is Here'
---

# Managed Instance on Azure App Service: Zero-Rewrite .NET Migration Is Here

**TL;DR**
Managed Instance on Azure App Service, now in public preview, lets organizations move existing .NET applications to the cloud with only a few configuration changes
. No code rewrites needed. This is a game-changer for enterprises sitting on legacy .NET stacks who've been dreading the cloud lift-and-shift tax.

## The Problem: .NET Migration Friction

If you're managing a mature .NET application—say, a 10-year-old ASP.NET Framework monolith or a hybrid .NET Core setup—cloud migration has historically meant one of two unpleasant paths:

1. **Full rewrite** to cloud-native patterns (expensive, risky, slow).
2. **VM-based lift-and-shift** (works, but you lose cloud-native benefits and pay for idle capacity).
The result is faster migrations with lower overhead, and access to cloud-native scalability, built-in security and AI capabilities in Microsoft Foundry
. Managed Instance bridges the gap.

## What Changes (Spoiler: Not Much)
Managed Instance on Azure App Service, available in public preview, lets organizations move their .NET web applications to the cloud with just a few configuration changes, saving the time and effort of rewriting code
.

In practice, this means:
- Your existing .NET Framework or .NET Core app runs on managed infrastructure.
- Azure handles OS patching, networking, and scaling.
- You configure connection strings and environment variables—standard stuff.
- No container orchestration learning curve; no Kubernetes YAML files.

## Why This Matters for Your Team

**Cost predictability:** You stop guessing at VM sizing. Azure's managed layer auto-scales based on demand.

**Security & compliance:** Built-in isolation, managed identity support, and integration with Azure's security suite out of the box.

**AI integration:**
Access to cloud-native scalability, built-in security and AI capabilities in Microsoft Foundry
. If you want to bolt on Azure OpenAI, Azure AI Search, or other Foundry services later, the plumbing is already there.

**Developer velocity:** Your team can focus on features, not infrastructure. No more "is the server down?" calls at 2 AM.

## Getting Started

1. **Assess your app:** Managed Instance supports .NET Framework 4.8+ and .NET 6+. Check for unsupported dependencies (exotic COM objects, etc.).

2. **Prepare secrets:** Move connection strings, API keys, and certificates into Azure Key Vault.

3. **Deploy via Azure CLI or portal:**
   ```bash
   az appservice plan create --name MyPlan --resource-group MyRG --sku B1 --is-linux
   az webapp create --resource-group MyRG --plan MyPlan --name MyApp --runtime "DOTNET|8.0"
   ```

4. **Test locally first:** Use the Azure CLI's local emulation or spin up a dev slot.

5. **Monitor:** Hook into Azure Application Insights for real-time observability.

## The Bigger Picture
Claude Sonnet 4.5, Opus 4.1, and Haiku 4.5 are now part of Microsoft Foundry, advancing our mission to give customers choice across the industry's leading frontier models—and making Azure the only cloud offering both OpenAI and Anthropic models. This expansion underscores our commitment to an open, interoperable Microsoft AI ecosystem
. Managed Instance is the on-ramp for .NET teams to tap into that AI-first infrastructure without rearchitecting everything.

The era of "we can't move to the cloud because we'd have to rewrite" is ending. If you've got a .NET app that's been a blocker for cloud adoption, now's the time to revisit that conversation.

---

## Further reading

- https://azure.microsoft.com/en-us/blog/microsoft-foundry-scale-innovation-on-a-modular-interoperable-and-secure-agent-stack/
- https://azure.microsoft.com/en-us/blog/azure-at-microsoft-ignite-2025-all-the-intelligent-cloud-news-explained/
- https://learn.microsoft.com/en-us/azure/ai-services/language-service/whats-new
- https://devblogs.microsoft.com/azure-sdk/azure-developer-cli-azd-november-2025/
- https://azure.microsoft.com/en-us/pricing/details/ai-foundry-models/aoai/