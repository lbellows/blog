using BlogGenerator.Core.Memes;

namespace BlogGenerator.Tests;

public class MemeInjectorTests
{
    [Fact]
    public void InjectsAfterTldr()
    {
        var md = "# Title\n**TL;DR** Summary\n\nMore content.";
        var result = MemeInjector.InjectMemeIntoMarkdown(md, "assets/images/memes/test.png", "Title", "Summary");
        Assert.Contains("![", result);
        Assert.Contains("assets/images/memes/test.png", result);
    }

    [Fact]
    public void ReplacesExistingImage()
    {
        var md = "# Title\n![old](old.png)\nContent.";
        var result = MemeInjector.InjectMemeIntoMarkdown(md, "new.png", "Title", null);
        Assert.Contains("new.png", result);
        Assert.DoesNotContain("old.png", result);
    }

    [Fact]
    public void PrependsWhenNoTldrOrImage()
    {
        var md = "# Title\nContent only.";
        var result = MemeInjector.InjectMemeIntoMarkdown(md, "meme.png", "Title", null);
        Assert.StartsWith("![", result);
    }

    [Fact]
    public void ReturnsUnchangedForEmptyPath()
    {
        var md = "# Title\nContent.";
        Assert.Equal(md, MemeInjector.InjectMemeIntoMarkdown(md, "", "Title", null));
    }
}
