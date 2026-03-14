using BlogGenerator.Core.Configuration;
using BlogGenerator.Core.Prompts;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel;

namespace BlogGenerator.Core.Providers.AzureFoundry;

public sealed class AzureFoundryProvider : IAIProvider
{
    public string ProviderName => "foundry";

    public async Task<AIProviderResponse> GeneratePostAsync(
        PromptContext promptContext,
        GenerationSettings settings,
        CancellationToken ct = default)
    {
        var endpoint = ResolveEndpoint();
        var apiKey = ResolveApiKey();
        var models = settings.FoundryModels.Count > 0
            ? settings.FoundryModels.ToList()
            : [settings.FoundryDefaultModel];

        var rng = Random.Shared;
        for (var i = models.Count - 1; i > 0; i--)
        {
            var j = rng.Next(i + 1);
            (models[i], models[j]) = (models[j], models[i]);
        }

        Exception? lastErr = null;
        foreach (var candidate in models)
        {
            Console.WriteLine($"Trying Foundry model: {candidate}");
            try
            {
                var markdown = await CallFoundryAsync(
                    promptContext,
                    settings,
                    candidate,
                    endpoint,
                    apiKey,
                    ct: ct);
                Console.WriteLine($"Found working model: {candidate}");
                return new AIProviderResponse(markdown, candidate);
            }
            catch (ClientResultException ex) when (ex.Status == 404 || ex.Message.Contains("DeploymentNotFound"))
            {
                lastErr = ex;
                Console.WriteLine($"Deployment {candidate} not found, trying next model...");
            }
            catch (Exception ex)
            {
                lastErr = ex;
                Console.WriteLine($"Foundry call failed for {candidate}: {ex.Message}");
            }
        }

        throw new InvalidOperationException(
            $"No available Foundry deployment found after trying models: [{string.Join(", ", models)}]. Last error: {lastErr?.Message}");
    }

    private static async Task<string> CallFoundryAsync(
        PromptContext promptContext,
        GenerationSettings settings,
        string deploymentModel,
        Uri endpoint,
        string apiKey,
        string? retryInstruction = null,
        CancellationToken ct = default)
    {
        ChatClient client = new(
            credential: new ApiKeyCredential(apiKey),
            model: deploymentModel,
            options: new OpenAIClientOptions
            {
                Endpoint = endpoint,
            });

        var messages = new List<ChatMessage>
        {
            new SystemChatMessage(promptContext.SystemPrompt),
            new UserChatMessage(promptContext.UserPrompt),
        };
        if (!string.IsNullOrWhiteSpace(retryInstruction))
            messages.Add(new UserChatMessage(retryInstruction));

        var options = new ChatCompletionOptions
        {
            MaxOutputTokenCount = settings.FoundryMaxTokens,
        };

        if (settings.FoundryTemperature.HasValue)
            options.Temperature = (float)settings.FoundryTemperature.Value;
        if (settings.FoundryTopP.HasValue)
            options.TopP = (float)settings.FoundryTopP.Value;

        var completion = await client.CompleteChatAsync(messages, options, ct);
        var markdown = string.Join(
            "\n",
            completion.Value.Content
                .Select(part => part.Text?.Trim())
                .Where(text => !string.IsNullOrWhiteSpace(text)))?.Trim() ?? string.Empty;

        if (string.IsNullOrWhiteSpace(markdown) && retryInstruction == null)
        {
            return await CallFoundryAsync(
                promptContext,
                settings,
                deploymentModel,
                endpoint,
                apiKey,
                EmptyResponseRetryText(),
                ct);
        }

        var lower = markdown.ToLowerInvariant();
        var hasHeading = markdown.Contains('#') || lower.StartsWith("h1:");
        var hasTldr = lower.Contains("tl;dr");
        var hasFurther = lower.Contains("further reading");
        var toolMarkup = markdown.Contains("<|") || lower.Contains("web_search");

        if (retryInstruction == null && (!(hasHeading && hasTldr && hasFurther) || toolMarkup))
        {
            return await CallFoundryAsync(
                promptContext,
                settings,
                deploymentModel,
                endpoint,
                apiKey,
                MarkupRetryText(toolMarkup),
                ct);
        }

        return markdown;
    }

    private static Uri ResolveEndpoint()
    {
        var rawEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_OPENAI_ENDPOINT")
            ?? throw new InvalidOperationException("FOUNDRY_OPENAI_ENDPOINT must be set");

        var normalized = rawEndpoint.Trim();
        if (!normalized.EndsWith("/", StringComparison.Ordinal))
            normalized += "/";
        if (!normalized.Contains("/openai/v1/", StringComparison.OrdinalIgnoreCase))
            normalized = normalized.TrimEnd('/') + "/openai/v1/";

        return new Uri(normalized, UriKind.Absolute);
    }

    private static string ResolveApiKey() =>
        Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_API_KEY")
        ?? throw new InvalidOperationException("FOUNDRY_PROJECT_API_KEY must be set");

    private static string EmptyResponseRetryText() =>
        "The previous response was empty. Provide the complete Markdown article now with an H1 title, " +
        "a **TL;DR** section, practical sections, and a **Further reading** list. Do not mention tool usage.";

    private static string MarkupRetryText(bool toolMarkupPresent)
    {
        var intro = toolMarkupPresent
            ? "The previous response included raw tool-call markup."
            : "The previous response did not deliver the final Markdown article.";

        return $"{intro} Web search is unavailable in this environment. Reply now with a complete Markdown post " +
               "that includes an H1 title, a **TL;DR** section, practical sections, and a **Further reading** list. " +
               "Do not emit tool-call markup, <|...|> tokens, or describe the attempt; output only the article.";
    }
}
