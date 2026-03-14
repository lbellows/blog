using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;
using BlogGenerator.Core.Configuration;
using BlogGenerator.Core.Prompts;

namespace BlogGenerator.Core.Providers.AzureFoundry;

public sealed class AzureFoundryProvider : IAIProvider
{
    private readonly HttpClient _httpClient;

    public string ProviderName => "foundry";

    public AzureFoundryProvider(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<AIProviderResponse> GeneratePostAsync(
        PromptContext promptContext,
        GenerationSettings settings,
        CancellationToken ct = default)
    {
        if (string.IsNullOrEmpty(Environment.GetEnvironmentVariable("FOUNDARY_API_KEY")) &&
            string.IsNullOrEmpty(Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")))
            throw new InvalidOperationException("FOUNDARY_API_KEY or AZURE_OPENAI_API_KEY must be set");

        var models = settings.FoundryModels.Count > 0
            ? settings.FoundryModels.ToList()
            : [settings.FoundryDefaultModel];

        // Shuffle models for load distribution
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
                var markdown = await CallFoundryAsync(settings, promptContext, candidate, ct: ct);
                Console.WriteLine($"Found working model: {candidate}");
                return new AIProviderResponse(markdown, candidate);
            }
            catch (InvalidOperationException ex) when (
                ex.Message.Contains("DeploymentNotFound") || ex.Message.Contains("404"))
            {
                lastErr = ex;
                Console.WriteLine($"Deployment {candidate} not found, trying next model...");
            }
        }

        throw new InvalidOperationException(
            $"No available Foundry deployment found after trying models: [{string.Join(", ", models)}]. Last error: {lastErr?.Message}");
    }

    private async Task<string> CallFoundryAsync(
        GenerationSettings settings,
        PromptContext promptContext,
        string deploymentModel,
        List<Dictionary<string, object>>? extraMessages = null,
        CancellationToken ct = default)
    {
        var endpoint = (Environment.GetEnvironmentVariable("ENDPOINT_URL")
            ?? Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
            ?? throw new InvalidOperationException("ENDPOINT_URL or AZURE_OPENAI_ENDPOINT must be set"))
            .TrimEnd('/');

        var subscriptionKey = Environment.GetEnvironmentVariable("FOUNDARY_API_KEY")
            ?? Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")
            ?? throw new InvalidOperationException("FOUNDARY_API_KEY or AZURE_OPENAI_API_KEY not set");

        var url = $"{endpoint}/openai/deployments/{deploymentModel}/chat/completions?api-version=2025-01-01-preview";

        var messages = PromptBuilder.BuildChatMessages(promptContext);
        if (extraMessages != null)
            messages.AddRange(extraMessages);

        var payload = new Dictionary<string, object>
        {
            ["messages"] = messages,
            ["max_tokens"] = settings.FoundryMaxTokens,
        };

        if (settings.FoundryTemperature.HasValue)
            payload["temperature"] = settings.FoundryTemperature.Value;
        if (settings.FoundryTopP.HasValue)
            payload["top_p"] = settings.FoundryTopP.Value;

        var headers = new Dictionary<string, string>
        {
            ["api-key"] = subscriptionKey,
        };

        var response = await PostJsonAsync(url, payload, headers, ct);

        // Retry: max_tokens unsupported → swap to max_completion_tokens
        if (!response.IsSuccess && response.StatusCode == 400)
        {
            var bodyText = response.BodyText ?? "";
            if (bodyText.Contains("max_tokens") &&
                (bodyText.Contains("unsupported") || bodyText.Contains("not supported") || bodyText.Contains("unsupported_parameter")))
            {
                var newPayload = new Dictionary<string, object>(payload);
                newPayload.Remove("max_tokens");
                newPayload["max_completion_tokens"] = settings.FoundryMaxTokens;
                response = await PostJsonAsync(url, newPayload, headers, ct);
            }
        }

        // Retry: temperature unsupported
        if (!response.IsSuccess && response.StatusCode == 400)
        {
            var bodyText = response.BodyText ?? "";
            if (bodyText.Contains("temperature") && bodyText.Contains("unsupported"))
            {
                var newPayload = new Dictionary<string, object>(payload);
                newPayload.Remove("temperature");
                response = await PostJsonAsync(url, newPayload, headers, ct);

                if (!response.IsSuccess)
                {
                    newPayload["top_p"] = 1.0;
                    response = await PostJsonAsync(url, newPayload, headers, ct);
                }
            }
        }

        if (!response.IsSuccess)
            throw new InvalidOperationException(
                $"Foundry REST call failed: {response.StatusCode} {response.ReasonPhrase}: {response.BodyText}");

        var texts = ExtractTexts(response.Json);

        if (texts.Count == 0)
            return response.BodyText ?? JsonSerializer.Serialize(response.Json);

        var markdown = string.Join("\n", texts.Select(t => t.Trim()).Where(t => t.Length > 0)).Trim();

        // Empty response retry
        if (string.IsNullOrWhiteSpace(markdown) && extraMessages == null)
        {
            return await CallFoundryAsync(settings, promptContext, deploymentModel,
                PromptBuilder.EmptyResponseRetryInstruction(), ct);
        }

        if (string.IsNullOrWhiteSpace(markdown))
            return markdown;

        // Content quality check & retry
        var lower = markdown.ToLowerInvariant();
        var hasHeading = markdown.Contains('#') || lower.StartsWith("h1:");
        var hasTldr = lower.Contains("tl;dr");
        var hasFurther = lower.Contains("further reading");
        var toolMarkup = markdown.Contains("<|") || lower.Contains("web_search");

        if (extraMessages == null && (!(hasHeading && hasTldr && hasFurther) || toolMarkup))
        {
            return await CallFoundryAsync(settings, promptContext, deploymentModel,
                PromptBuilder.MarkupRetryInstruction(toolMarkup), ct);
        }

        return markdown;
    }

    private static List<string> ExtractTexts(JsonElement? json)
    {
        var texts = new List<string>();
        if (json is not { ValueKind: JsonValueKind.Object } data)
            return texts;

        if (!data.TryGetProperty("choices", out var choices))
            return texts;

        foreach (var choice in choices.EnumerateArray())
        {
            string? content = null;

            if (choice.TryGetProperty("message", out var message))
            {
                if (message.TryGetProperty("content", out var contentProp))
                {
                    if (contentProp.ValueKind == JsonValueKind.String)
                    {
                        content = contentProp.GetString();
                    }
                    else if (contentProp.ValueKind == JsonValueKind.Array)
                    {
                        foreach (var block in contentProp.EnumerateArray())
                        {
                            if (block.ValueKind == JsonValueKind.Object)
                            {
                                if (block.TryGetProperty("text", out var textProp) && textProp.ValueKind == JsonValueKind.String)
                                    texts.Add(textProp.GetString()!);
                                else if (block.TryGetProperty("content", out var cProp) && cProp.ValueKind == JsonValueKind.String)
                                    texts.Add(cProp.GetString()!);
                            }
                        }
                        continue;
                    }
                }
            }

            content ??= choice.TryGetProperty("text", out var textVal) ? textVal.GetString() : null;
            content ??= choice.TryGetProperty("delta", out var deltaVal) ? deltaVal.GetString() : null;

            if (!string.IsNullOrEmpty(content))
                texts.Add(content);
        }

        return texts;
    }

    private async Task<FoundryResponse> PostJsonAsync(
        string url,
        Dictionary<string, object> payload,
        Dictionary<string, string> headers,
        CancellationToken ct)
    {
        using var request = new HttpRequestMessage(HttpMethod.Post, url);
        foreach (var (key, value) in headers)
            request.Headers.TryAddWithoutValidation(key, value);
        request.Content = JsonContent.Create(payload, options: JsonOpts);

        var httpResponse = await _httpClient.SendAsync(request, ct);
        var bodyText = await httpResponse.Content.ReadAsStringAsync(ct);
        JsonElement? json = null;
        try { json = JsonSerializer.Deserialize<JsonElement>(bodyText); } catch { /* not JSON */ }

        return new FoundryResponse(
            (int)httpResponse.StatusCode,
            httpResponse.ReasonPhrase,
            httpResponse.IsSuccessStatusCode,
            bodyText,
            json);
    }

    private sealed record FoundryResponse(
        int StatusCode,
        string? ReasonPhrase,
        bool IsSuccess,
        string? BodyText,
        JsonElement? Json);

    private static readonly JsonSerializerOptions JsonOpts = new()
    {
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
    };
}
