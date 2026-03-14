namespace BlogGenerator.Core.Configuration;

public sealed class GenerationSettings
{
    public string TopicHint { get; set; } = "Artificial Intelligence news for software engineers shipping on .NET and Azure.";
    public string? TopicUrl { get; set; }
    public int PostWordsMin { get; set; } = 200;
    public int PostWordsMax { get; set; } = 1000;
    public int MaxSearches { get; set; } = 7;
    public int RecentWindowDays { get; set; } = 2;

    public List<string> AllowedDomains { get; set; } =
    [
        "learn.microsoft.com",
        "azure.microsoft.com",
        "techcommunity.microsoft.com",
        "blogs.microsoft.com",
        "devblogs.microsoft.com",
        "github.blog",
        "developer.microsoft.com",
        "techcrunch.com",
        "venturebeat.com",
        "infoq.com",
    ];

    public List<string> BlockedDomains { get; set; } = [];

    public string RepoRoot { get; set; } = string.Empty;
    public string DefaultAuthor { get; set; } = "the.serf";

    // Anthropic
    public string AnthropicModel { get; set; } = "claude-sonnet-4-6";
    public int AnthropicMaxTokens { get; set; } = 4096;
    public double? AnthropicTemperature { get; set; } = 0.9;

    // Azure Foundry
    public List<string> FoundryModels { get; set; } = ["DeepSeek-V3.1", "gpt-5-mini", "gpt-oss-120b"];
    public string FoundryDefaultModel { get; set; } = "gpt-oss-120b";
    public int FoundryMaxTokens { get; set; } = 4096;
    public double? FoundryTemperature { get; set; }
    public double? FoundryTopP { get; set; }

    public bool MemeGuidanceEnabled { get; set; }
}
