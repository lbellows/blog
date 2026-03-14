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
}
