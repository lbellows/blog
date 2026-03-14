using BlogGenerator.Core.PostGeneration;

namespace BlogGenerator.Tests;

public class PostWriterTests
{
    [Fact]
    public void StripLeadingInstructionsRemovesPreamble()
    {
        var input = "Here is your article:\nSome instructions\n# Real Title\nContent here";
        var result = PostWriter.StripLeadingInstructions(input);
        Assert.StartsWith("# Real Title", result);
        Assert.Contains("Content here", result);
    }

    [Fact]
    public void StripLeadingInstructionsPreservesCleanMarkdown()
    {
        var input = "# Title\nContent";
        var result = PostWriter.StripLeadingInstructions(input);
        Assert.StartsWith("# Title", result);
    }

    [Fact]
    public void StripLeadingInstructionsHandlesNoHeading()
    {
        var input = "No heading at all\nJust text";
        var result = PostWriter.StripLeadingInstructions(input);
        Assert.Equal("No heading at all\nJust text", result);
    }

    [Fact]
    public void StripLeadingTitleHeadingRemovesTopLevelTitle()
    {
        var input = "# Title\n\nContent";
        var result = PostWriter.StripLeadingTitleHeading(input);
        Assert.Equal("Content", result);
    }

    [Fact]
    public void StripLeadingTitleHeadingLeavesBodyWithoutTopLevelTitle()
    {
        var input = "## Subtitle\nContent";
        var result = PostWriter.StripLeadingTitleHeading(input);
        Assert.Equal(input, result);
    }

    [Fact]
    public void StripLeadingPostMetadataRemovesPublishedLineAndRule()
    {
        var input = "**Published:** March 14, 2026\t~850 words\n\n---\n\n## TL;DR\nContent";
        var result = PostWriter.StripLeadingPostMetadata(input);
        Assert.Equal("## TL;DR\nContent", result);
    }

    [Fact]
    public void StripLeadingPostMetadataRemovesPublishedLineWithTags()
    {
        var input = "**Published:** March 13, 2026 | **Tags:** Azure, .NET\n\n## TL;DR\nContent";
        var result = PostWriter.StripLeadingPostMetadata(input);
        Assert.Equal("## TL;DR\nContent", result);
    }

    [Fact]
    public void StripLeadingPostMetadataLeavesNormalBodyAlone()
    {
        var input = "## TL;DR\nContent";
        var result = PostWriter.StripLeadingPostMetadata(input);
        Assert.Equal(input, result);
    }
}
