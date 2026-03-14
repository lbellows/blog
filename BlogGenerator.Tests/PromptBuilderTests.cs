using BlogGenerator.Core.Configuration;
using BlogGenerator.Core.Prompts;

namespace BlogGenerator.Tests;

public class PromptBuilderTests
{
    [Fact]
    public void BuildProducesSundaySynopsisMode()
    {
        var settings = new GenerationSettings();
        var sunday = new DateOnly(2025, 6, 1); // Sunday
        var ctx = PromptBuilder.Build(settings, today: sunday);
        Assert.Contains("synopsis day", ctx.ModeInstructions);
    }

    [Fact]
    public void BuildProducesWeekdayDeepDiveMode()
    {
        var settings = new GenerationSettings();
        var monday = new DateOnly(2025, 6, 2); // Monday
        var ctx = PromptBuilder.Build(settings, today: monday);
        Assert.Contains("laser-focused", ctx.ModeInstructions);
    }

    [Fact]
    public void SystemPromptContainsWordLimits()
    {
        var settings = new GenerationSettings { PostWordsMin = 300, PostWordsMax = 800 };
        var ctx = PromptBuilder.Build(settings, today: new DateOnly(2025, 6, 2));
        Assert.Contains("300-800", ctx.SystemPrompt);
    }

    [Fact]
    public void UserPromptContainsTopicHint()
    {
        var settings = new GenerationSettings { TopicHint = "Custom topic hint" };
        var ctx = PromptBuilder.Build(settings, today: new DateOnly(2025, 6, 2));
        Assert.Contains("Custom topic hint", ctx.UserPrompt);
    }

    [Fact]
    public void PrimaryLinkLineIncludedWhenSet()
    {
        var settings = new GenerationSettings { TopicUrl = "https://example.com/article" };
        var ctx = PromptBuilder.Build(settings, today: new DateOnly(2025, 6, 2));
        Assert.Contains("https://example.com/article", ctx.PrimaryLinkLine);
        Assert.True(ctx.UserInstructionItems.Count >= 5); // extra instruction added
    }

    [Fact]
    public void MemeGuidanceIncludedWhenEnabled()
    {
        var settings = new GenerationSettings { MemeGuidanceEnabled = true };
        var ctx = PromptBuilder.Build(settings, today: new DateOnly(2025, 6, 2));
        Assert.Contains("meme", ctx.SystemPrompt, StringComparison.OrdinalIgnoreCase);
    }

    [Fact]
    public void RecentStartDateIsCorrectDaysBack()
    {
        var settings = new GenerationSettings { RecentWindowDays = 3 };
        var today = new DateOnly(2025, 6, 10);
        var ctx = PromptBuilder.Build(settings, today: today);
        Assert.Equal(new DateOnly(2025, 6, 7), ctx.RecentStartDate);
    }
}
