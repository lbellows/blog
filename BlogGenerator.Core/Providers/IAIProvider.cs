using BlogGenerator.Core.Configuration;
using BlogGenerator.Core.Prompts;

namespace BlogGenerator.Core.Providers;

public interface IAIProvider
{
    string ProviderName { get; }

    Task<AIProviderResponse> GeneratePostAsync(
        PromptContext promptContext,
        GenerationSettings settings,
        CancellationToken ct = default);
}
