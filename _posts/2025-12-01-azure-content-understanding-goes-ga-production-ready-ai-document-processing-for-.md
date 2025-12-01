---
author: the.serf
date: 2025-12-01 06:29:44 -0500
layout: post
tags:
- .net
- actually
- azure
- can
- changed
- claude-haiku-4-5-20251001
title: 'Azure Content Understanding Goes GA: Production-Ready AI Document Processing
  for .NET Developers'
---

# Azure Content Understanding Goes GA: Production-Ready AI Document Processing for .NET Developers

**TL;DR**
Azure Content Understanding in Foundry Tools is now Generally Available with API version 2025-11-01, bringing production readiness plus customer-driven enhancements across model choice, management, and security.
If you're building .NET apps that need to extract structured data from complex documents at scale, this is your signal to move from experiments to production—with enterprise security controls baked in.

## What Changed

Until November, Azure Content Understanding lived in preview purgatory. Now it's ready for the workloads that matter: customer contracts, insurance claims, invoices, and anything else buried in PDFs or images that your app needs to understand.
Content Understanding now has increased field count support (1,000) for all modalities, and the API response body now includes input, output, and contextualization tokens consumed as part of the tokens object.
Translation: you can extract more fields per document, and you get granular token accounting—critical for cost forecasting in production.

## The Security Story (Yes, Really)

This is where it gets interesting for enterprise teams.
General availability includes Microsoft Entra ID, managed identities, customer-managed keys, virtual networks, and private endpoints, keeping sensitive content in your Azure boundary and helping you meet compliance requirements.
No more "but how do we keep PII in-house?" conversations. It's there.

## What You Can Actually Build Now
Prebuilt-read and prebuilt-layout analyzers now bring key Document Intelligence capabilities to Content Understanding, with prebuilt-layoutWithFigures extending layout extraction with figure detection and analysis, extracting and summarizing charts, diagrams, and images with their context.
More practically:
When analyzing content, you can now provide a page range to only analyze specific pages of the input document, and segmentation and classification (contentCategories) let you send sections to purpose-built analyzers during a single run.
This means you're not paying to process every page of a 50-page contract if you only care about the signature block.

## Integration with .NET

The Content Understanding API works seamlessly with Azure SDK for .NET. Here's a minimal example to get started:

```csharp
using Azure;
using Azure.AI.DocumentIntelligence;

var client = new DocumentIntelligenceClient(
    new Uri("https://<your-resource>.cognitiveservices.azure.com/"),
    new AzureKeyCredential("<your-key>")
);

var operation = await client.AnalyzeDocumentAsync(
    WaitUntil.Completed,
    "prebuilt-layout",
    new AnalyzeDocumentContent { UrlSource = new Uri("https://example.com/invoice.pdf") }
);

var result = operation.Value;
foreach (var page in result.Pages)
{
    Console.WriteLine($"Page {page.PageNumber}: {page.Tables.Count} tables found");
}
```

## Cost & Latency Implications

The token accounting is new and crucial.
The API response body now includes input, output, and contextualization tokens consumed as part of the tokens object.
This means you can now:

- **Forecast costs** before you scale to thousands of documents
- **Optimize prompts** by comparing token usage across different analyzer configurations
- **Right-size your deployment** based on real usage patterns

Latency remains predictable for synchronous calls; async processing is still the play for high-volume workloads.

## Next Steps

1. **Update your SDK**: Ensure you're on the latest `Azure.AI.DocumentIntelligence` NuGet package.
2. **Test with GA API version 2025-11-01**: Migrate from preview endpoints and confirm your code still works (it should).
3. **Implement Entra ID auth**: Swap API keys for managed identities in production—it's now fully supported.
4. **Monitor token usage**: Use the new token reporting to baseline your costs before full rollout.

The preview is over. Content Understanding is ready to do real work.

---

## Further reading

- https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/whats-new
- https://learn.microsoft.com/en-us/azure/ai-services/language-service/whats-new
- https://azure.microsoft.com/en-us/blog/all-the-azure-news-you-dont-want-to-miss-from-microsoft-build-2025/
- https://devblogs.microsoft.com/dotnet/catching-up-on-microsoft-build-2025-essential-sessions-for-dotnet-developers/
- https://learn.microsoft.com/en-us/dotnet/ai/overview