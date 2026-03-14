using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;
using Azure.Identity;
using BlogGenerator.Core.Configuration;
using BlogGenerator.Core.Prompts;
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
        var projectEndpoint = ResolveProjectEndpoint();
        var models = BuildModelCandidates(settings);

        Exception? lastErr = null;
        foreach (var candidate in models)
        {
            Console.WriteLine($"Trying Foundry model: {candidate}");

            var agentName = BuildAgentName(candidate);
            AIProjectClient? projectClient = null;
            AgentVersion? agentVersion = null;

            try
            {
                projectClient = new AIProjectClient(
                    projectEndpoint,
                    new DefaultAzureCredential());

                PromptAgentDefinition agentDefinition = new(model: candidate)
                {
                    Instructions = promptContext.SystemPrompt,
                    Temperature = settings.FoundryTemperature is null ? null : (float)settings.FoundryTemperature.Value,
                    TopP = settings.FoundryTopP is null ? null : (float)settings.FoundryTopP.Value,
                    Tools =
                    {
                        BuildWebSearchTool(settings),
                    },
                };

                agentVersion = projectClient.Agents.CreateAgentVersion(
                    agentName: agentName,
                    options: new(agentDefinition));

                ProjectResponsesClient responsesClient =
                    projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

                CreateResponseOptions responseOptions = new()
                {
                    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
                    MaxOutputTokenCount = settings.FoundryMaxTokens,
                    InputItems =
                    {
                        ResponseItem.CreateUserMessageItem(promptContext.UserPrompt),
                    },
                };

                ResponseResult response = await responsesClient.CreateResponseAsync(
                    responseOptions,
                    cancellationToken: ct);

                var markdown = response.GetOutputText()?.Trim() ?? string.Empty;
                if (string.IsNullOrWhiteSpace(markdown))
                    throw new InvalidOperationException("Foundry agent response did not contain output text.");

                Console.WriteLine($"Found working model: {candidate}");
                return new AIProviderResponse(markdown, candidate);
            }
            catch (Exception ex)
            {
                lastErr = ex;
                Console.WriteLine($"Foundry call failed for {candidate}: {ex.Message}");
            }
            finally
            {
                if (projectClient is not null && agentVersion is not null)
                {
                    try
                    {
                        projectClient.Agents.DeleteAgentVersion(agentVersion.Name, agentVersion.Version);
                    }
                    catch (Exception cleanupEx)
                    {
                        Console.WriteLine($"Cleanup failed for agent {agentName}: {cleanupEx.Message}");
                    }
                }
            }
        }

        throw new InvalidOperationException(
            $"No available Foundry deployment found after trying models: [{string.Join(", ", models)}]. Last error: {lastErr?.Message}");
    }

    private static Uri ResolveProjectEndpoint()
    {
        var rawEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
            ?? throw new InvalidOperationException("FOUNDRY_PROJECT_ENDPOINT must be set");

        return new Uri(rawEndpoint, UriKind.Absolute);
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
        WebSearchToolFilters? filters = null;
        if (settings.AllowedDomains.Count > 0)
        {
            filters = new WebSearchToolFilters();
            foreach (var domain in settings.AllowedDomains)
                filters.AllowedDomains.Add(domain);
        }

        return ResponseTool.CreateWebSearchTool(filters: filters);
    }

    private static string BuildAgentName(string modelName)
    {
        var sanitized = new string(
            modelName
                .ToLowerInvariant()
                .Select(ch => char.IsLetterOrDigit(ch) ? ch : '-')
                .ToArray())
            .Trim('-');

        if (sanitized.Length > 24)
            sanitized = sanitized[..24].Trim('-');

        var suffix = Guid.NewGuid().ToString("N")[..8];
        return $"blog-{sanitized}-{suffix}";
    }
}
