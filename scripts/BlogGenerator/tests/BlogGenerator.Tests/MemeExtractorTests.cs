using BlogGenerator.Core.Memes;

namespace BlogGenerator.Tests;

public class MemeExtractorTests
{
    [Fact]
    public void ExtractsTldrFromSameLine()
    {
        var md = "# Title\n**TL;DR** Azure is great.\nMore content.";
        Assert.Equal("Azure is great.", MemeExtractor.ExtractTldrLine(md));
    }

    [Fact]
    public void ExtractsTldrFromNextLine()
    {
        var md = "# Title\n**TL;DR**\nAzure is great.\nMore content.";
        Assert.Equal("Azure is great.", MemeExtractor.ExtractTldrLine(md));
    }

    [Fact]
    public void ReturnsNullWhenNoTldr()
    {
        var md = "# Title\nNo summary here.";
        Assert.Null(MemeExtractor.ExtractTldrLine(md));
    }
}
