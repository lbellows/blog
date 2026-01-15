---
author: the.serf
date: 2026-01-15 06:32:49 -0500
layout: post
tags:
- .net
- agents
- api
- azure
- bigger
- claude-haiku-4-5-20251001
title: 'Azure OpenAI''s Realtime API with WebRTC: Building Low-Latency Voice Agents
  in .NET'
---

# Azure OpenAI's Realtime API with WebRTC: Building Low-Latency Voice Agents in .NET

**TL;DR**
OpenAI's GPT RealTime and Audio models are now generally available on Azure AI Foundry, with WebRTC support enabling real-time audio streaming and low-latency interactions
. This means .NET developers can build voice-first agents without round-trip latency penalties—ideal for customer support bots, voice assistants, and interactive applications.

## What Just Shipped
The Realtime API (preview) now supports WebRTC, enabling real-time audio streaming and low-latency interactions ideal for applications requiring immediate feedback, such as live customer support or interactive voice assistants
.

Translation: no more waiting for HTTP request-response cycles. Your voice agents can respond in near-real-time, matching human conversation rhythm.

## Why This Matters for .NET Engineers

**Latency is the enemy of voice UX.** A 200ms delay in a voice conversation feels broken; humans expect sub-100ms response times.
Improved function calling enables enhanced ability to call custom code defined by developers, with async function calling supported, allowing sessions to continue while a function call is pending
. This means your agent can:

- Fetch data from a database without blocking the audio stream
- Call multiple APIs in parallel while the user is still speaking
- Return results mid-conversation without awkward silences

## Integration Path for .NET
AI-focused capabilities expand through the Microsoft Agent Framework, Microsoft.Extensions.AI, and first-class Model Context Protocol (MCP) support, aiming to standardize patterns for building agentic workflows, integrating external tools, enabling telemetry, and working across multiple AI providers
.

Here's a minimal setup:

```csharp
// Install via NuGet
// dotnet add package Azure.AI.OpenAI --prerelease
// dotnet add package Microsoft.Extensions.AI

using Azure;
using Azure.AI.OpenAI;
using Microsoft.Extensions.AI;

var client = new AzureOpenAIClient(
    new Uri("https://<your-instance>.openai.azure.com/"),
    new AzureKeyCredential("<your-key>"));

// Use the Realtime API via Azure AI Foundry
var chatClient = client.GetChatClient("gpt-4o-realtime");

// WebRTC connection is handled by the SDK
// Stream audio in, get audio out—no HTTP round-trips
```
Improved instruction following enhances capabilities to follow tone, pacing, and escalation instructions more accurately and reliably, and can also switch languages
. This means your agent can adapt personality on the fly—critical for customer service scenarios where tone shifts based on sentiment.

## Cost & Performance Considerations
Improved instruction following: Enhanced capabilities to follow tone, pacing, and escalation instructions more accurately and reliably
comes with the standard Azure OpenAI pricing model. The WebRTC transport itself is more efficient than repeated HTTP calls, so you'll see lower per-call costs for high-volume voice interactions.
New standard voices, Marin and Cedar, bring improved naturalness and clarity to speech synthesis, with glitch-free output, improved alphanumeric reproduction, and modality control
. Quality matters—these new voices are production-ready.

## Practical Next Steps

1. **Upgrade your Azure OpenAI resource** to the latest API version via Azure AI Foundry.
2. **Test with the Realtime API playground** before integrating into .NET code.
3. **Leverage async function calling** to keep the audio stream responsive while your backend does work.
4. **Monitor latency metrics** using OpenTelemetry instrumentation (built into Microsoft Agent Framework).

## The Bigger Picture
2026 will be the year AI gets practical, with focus shifting away from building ever-larger language models and toward the harder work of making AI usable
. Real-time voice is a cornerstone of that pragmatism. No more chatbot gimmicks—agents that actually talk.

---

## Further reading

- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new?view=foundry-classic
- https://devblogs.microsoft.com/dotnet/generative-ai-with-large-language-models-in-dotnet-and-csharp/
- https://learn.microsoft.com/en-us/dotnet/ai/dotnet-ai-ecosystem
- https://devblogs.microsoft.com/all-things-azure/the-realities-of-application-modernization-with-agentic-ai-early-2026/
- https://techcrunch.com/2026/01/02/in-2026-ai-will-move-from-hype-to-pragmatism/
- https://blogs.microsoft.com/blog/2026/01/05/microsoft-announces-acquisition-of-osmos-to-accelerate-autonomous-data-engineering-in-fabric/