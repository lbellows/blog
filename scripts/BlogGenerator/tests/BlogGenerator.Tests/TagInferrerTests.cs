using BlogGenerator.Core.PostGeneration;

namespace BlogGenerator.Tests;

public class TagInferrerTests
{
    [Fact]
    public void InfersTagsFromHeadings()
    {
        var md = "# Azure OpenAI Gets Faster\n## Performance Benchmarks\n**TL;DR** Azure is faster now.";
        var tags = TagInferrer.Infer(md, "claude-sonnet-4-6");
        Assert.NotEmpty(tags);
        Assert.Contains("azure", tags);
    }

    [Fact]
    public void AddsAiTagIfPresent()
    {
        var md = "# Some AI News\nAI is everywhere.";
        var tags = TagInferrer.Infer(md, "gpt-4");
        Assert.Contains("ai", tags);
    }

    [Fact]
    public void AddsModelTag()
    {
        var md = "# Some News\nContent here.";
        var tags = TagInferrer.Infer(md, "claude-sonnet-4-6");
        Assert.Contains("claude-sonnet-4-6", tags);
    }

    [Fact]
    public void CapsAtSixTags()
    {
        var md = "# Alpha Beta Gamma Delta Epsilon Zeta Eta Theta\n" +
                 "## Iota Kappa Lambda Mu\nSome AI content.";
        var tags = TagInferrer.Infer(md, "mymodel");
        Assert.True(tags.Count <= 6);
    }

    [Fact]
    public void NormalizeTagFiltersStopwords()
    {
        Assert.Equal("", TagInferrer.NormalizeTag("the"));
        Assert.Equal("", TagInferrer.NormalizeTag("and"));
        Assert.Equal("", TagInferrer.NormalizeTag("developers"));
    }

    [Fact]
    public void NormalizeTagFiltersShortTokens()
    {
        Assert.Equal("", TagInferrer.NormalizeTag("ab"));
    }

    [Fact]
    public void NormalizeTagFormatsCorrectly()
    {
        Assert.Equal("azure", TagInferrer.NormalizeTag("Azure"));
        Assert.Equal(".net", TagInferrer.NormalizeTag(".NET"));
    }
}
