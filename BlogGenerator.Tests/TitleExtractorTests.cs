using BlogGenerator.Core.PostGeneration;

namespace BlogGenerator.Tests;

public class TitleExtractorTests
{
    [Fact]
    public void ExtractsH1Title()
    {
        var md = "# Azure AI Gets a Major Upgrade\n\nSome content here.";
        Assert.Equal("Azure AI Gets a Major Upgrade", TitleExtractor.Extract(md));
    }

    [Fact]
    public void ExtractsH1WithLeadingWhitespace()
    {
        var md = "\n\n  # My Title\n\nContent";
        Assert.Equal("My Title", TitleExtractor.Extract(md));
    }

    [Fact]
    public void FallsBackToFirstNonEmptyLine()
    {
        var md = "No heading here\nJust text";
        Assert.Equal("No heading here", TitleExtractor.Extract(md));
    }

    [Fact]
    public void FallsBackToDefault()
    {
        Assert.Equal("Daily AI Update", TitleExtractor.Extract(""));
    }

    [Fact]
    public void StripsMarkupCharacters()
    {
        var md = "**Bold Title**\nContent";
        Assert.Equal("Bold Title", TitleExtractor.Extract(md));
    }

    [Fact]
    public void TruncatesLongTitles()
    {
        var md = new string('A', 200) + "\nContent";
        Assert.Equal(80, TitleExtractor.Extract(md).Length);
    }
}
