using System.ClientModel;
using BlogGenerator.Core.Configuration;
using BlogGenerator.Core.Prompts;
using OpenAI;
using OpenAI.Responses;

namespace BlogGenerator.Core.Providers.AzureFoundry;

#pragma warning disable OPENAI001

public sealed class AzureFoundryProvider : IAIProvider
{
    public string ProviderName => "foundry";

    public async Task<AIProviderResponse> GeneratePostAsync(
        PromptContext promptContext,
        GenerationSettings settings,
        CancellationToken ct = default)
    {
        var endpoint = ResolveOpenAiEndpoint();
        var apiKey = ResolveApiKey();
        var models = BuildModelCandidates(settings);

        Exception? lastErr = null;
        foreach (var candidate in models)
        {
            Console.WriteLine($"Trying Foundry model: {candidate}");

            try
            {
                var client = new ResponsesClient(
                    credential: new ApiKeyCredential(apiKey),
                    options: new OpenAIClientOptions
                    {
                        Endpoint = endpoint,
                    });

                CreateResponseOptions responseOptions = new()
                {
                    Model = candidate,
                    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
                    MaxOutputTokenCount = settings.FoundryMaxTokens,
                    MaxToolCallCount = settings.MaxSearches,
                    Temperature = settings.FoundryTemperature is null ? null : (float)settings.FoundryTemperature.Value,
                    TopP = settings.FoundryTopP is null ? null : (float)settings.FoundryTopP.Value,
                    InputItems =
                    {
                        ResponseItem.CreateDeveloperMessageItem(promptContext.SystemPrompt),
                        ResponseItem.CreateUserMessageItem(promptContext.UserPrompt),
                    },
                    Tools =
                    {
                        BuildWebSearchTool(settings),
                    },
                };

                ResponseResult response = await client.CreateResponseAsync(responseOptions, ct);

                foreach (ResponseItem item in response.OutputItems)
                {
                    if (item is WebSearchCallResponseItem webSearchCall)
                        Console.WriteLine($"Web search invoked: {webSearchCall.Status} ({webSearchCall.Id})");
                }

                var markdown = response.GetOutputText()?.Trim() ?? string.Empty;
                if (string.IsNullOrWhiteSpace(markdown))
                    throw new InvalidOperationException("Foundry response did not contain output text.");

                Console.WriteLine($"Found working model: {candidate}");
                return new AIProviderResponse(markdown, candidate);
            }
            catch (Exception ex)
            {
                lastErr = ex;
                Console.WriteLine($"Foundry call failed for {candidate}: {SanitizeErrorMessage(ex.Message, endpoint, apiKey)}");
            }
        }

        throw new InvalidOperationException(
            $"No available Foundry deployment found after trying models: [{string.Join(", ", models)}]. Last error: {lastErr?.Message}");
    }

    private static string ResolveApiKey()
    {
        var apiKey = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_API_KEY");
        if (string.IsNullOrWhiteSpace(apiKey))
            throw new InvalidOperationException("FOUNDRY_PROJECT_API_KEY must be set to a non-empty API key.");

        return apiKey.Trim();
    }

    private static Uri ResolveOpenAiEndpoint()
    {
        var rawEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_OPENAI_ENDPOINT");
        if (string.IsNullOrWhiteSpace(rawEndpoint))
            throw new InvalidOperationException(
                "FOUNDRY_OPENAI_ENDPOINT must be set to a non-empty Azure OpenAI endpoint.");

        var trimmedEndpoint = rawEndpoint.Trim();
        if (!Uri.TryCreate(trimmedEndpoint, UriKind.Absolute, out var endpoint))
        {
            throw new InvalidOperationException(
                "FOUNDRY_OPENAI_ENDPOINT is not a valid absolute URI.");
        }

        if (!trimmedEndpoint.Contains("/openai/", StringComparison.OrdinalIgnoreCase))
        {
            endpoint = new Uri(endpoint, endpoint.AbsolutePath.EndsWith("/")
                ? "openai/v1/"
                : $"{endpoint.AbsolutePath.TrimEnd('/')}/openai/v1/");
        }

        return endpoint;
    }

    private static string SanitizeErrorMessage(string message, Uri endpoint, string apiKey)
    {
        var sanitized = message;
        sanitized = sanitized.Replace(endpoint.ToString(), "[FOUNDRY_OPENAI_ENDPOINT]", StringComparison.OrdinalIgnoreCase);
        sanitized = sanitized.Replace(apiKey, "[FOUNDRY_PROJECT_API_KEY]", StringComparison.Ordinal);
        return sanitized;
    }

    internal static IReadOnlyList<string> BuildModelCandidates(GenerationSettings settings)
    {
        var candidates = new List<string>();

        if (!string.IsNullOrWhiteSpace(settings.FoundryDefaultModel))
            candidates.Add(settings.FoundryDefaultModel.Trim());

        candidates.AddRange(settings.FoundryModels);

        return candidates
            .Where(model => !string.IsNullOrWhiteSpace(model))
            .Select(model => model.Trim())
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToList();
    }

    private static ResponseTool BuildWebSearchTool(GenerationSettings settings)
    {
        _ = settings;
        return ResponseTool.CreateWebSearchPreviewTool();
    }
}
