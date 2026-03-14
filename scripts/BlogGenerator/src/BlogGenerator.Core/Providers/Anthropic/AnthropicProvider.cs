using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;
using BlogGenerator.Core.Configuration;
using BlogGenerator.Core.Prompts;

namespace BlogGenerator.Core.Providers.Anthropic;

public sealed class AnthropicProvider : IAIProvider
{
    private readonly HttpClient _httpClient;
    private const string ApiUrl = "https://api.anthropic.com/v1/messages";

    public string ProviderName => "anthropic";

    public AnthropicProvider(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<AIProviderResponse> GeneratePostAsync(
        PromptContext promptContext,
        GenerationSettings settings,
        CancellationToken ct = default)
    {
        var apiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
            ?? throw new InvalidOperationException("ANTHROPIC_API_KEY must be set for Anthropic client");

        var chosenModel = settings.AnthropicModel;

        var tools = BuildTools(settings);

        var request = new Dictionary<string, object>
        {
            ["model"] = chosenModel,
            ["max_tokens"] = settings.AnthropicMaxTokens,
            ["system"] = promptContext.SystemPrompt,
            ["messages"] = new[]
            {
                new { role = "user", content = promptContext.UserPrompt }
            },
            ["tools"] = tools,
        };

        if (settings.AnthropicTemperature.HasValue)
            request["temperature"] = settings.AnthropicTemperature.Value;

        using var httpRequest = new HttpRequestMessage(HttpMethod.Post, ApiUrl);
        httpRequest.Headers.Add("x-api-key", apiKey);
        httpRequest.Headers.Add("anthropic-version", "2023-06-01");
        httpRequest.Content = JsonContent.Create(request, options: JsonOpts);

        var response = await _httpClient.SendAsync(httpRequest, ct);
        var responseBody = await response.Content.ReadAsStringAsync(ct);
        if (!response.IsSuccessStatusCode)
        {
            throw new HttpRequestException(
                $"Anthropic request failed with {(int)response.StatusCode} ({response.ReasonPhrase}). Response body: {responseBody}",
                null,
                response.StatusCode);
        }

        var json = JsonSerializer.Deserialize<JsonElement>(responseBody, JsonOpts);

        var parts = new List<string>();
        if (json.TryGetProperty("content", out var contentArray))
        {
            foreach (var block in contentArray.EnumerateArray())
            {
                if (block.TryGetProperty("type", out var typeProp) &&
                    typeProp.GetString() == "text" &&
                    block.TryGetProperty("text", out var textProp))
                {
                    var text = textProp.GetString();
                    if (!string.IsNullOrWhiteSpace(text))
                        parts.Add(text.Trim());
                }
            }
        }

        var markdown = string.Join("\n", parts);
        if (string.IsNullOrWhiteSpace(markdown))
            throw new InvalidOperationException("Anthropic response did not contain text content");

        return new AIProviderResponse(markdown, chosenModel);
    }

    private static List<object> BuildTools(GenerationSettings settings)
    {
        var toolDef = new Dictionary<string, object>
        {
            ["type"] = "web_search_20250305",
            ["name"] = "web_search",
            ["max_uses"] = settings.MaxSearches,
        };

        if (settings.AllowedDomains.Count > 0)
            toolDef["allowed_domains"] = settings.AllowedDomains;
        if (settings.BlockedDomains.Count > 0)
            toolDef["blocked_domains"] = settings.BlockedDomains;

        return [toolDef];
    }

    private static readonly JsonSerializerOptions JsonOpts = new()
    {
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
    };
}
