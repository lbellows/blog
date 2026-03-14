using System.Text.RegularExpressions;

namespace BlogGenerator.Core.Memes;

public static partial class MemeInjector
{
    [GeneratedRegex(@"!\[[^\]]*\]\([^)]+\)")]
    private static partial Regex ImagePattern();

    public static string InjectMemeIntoMarkdown(string markdownBody, string imagePath, string title, string? summary)
    {
        if (string.IsNullOrEmpty(imagePath))
            return markdownBody;

        var altSummary = summary ?? "meme reaction";
        var altText = $"{title} meme - {altSummary}";
        if (altText.Length > 80) altText = altText[..77] + "...";
        var imageMarkdown = $"![{altText}]({imagePath})";

        var match = ImagePattern().Match(markdownBody);
        if (match.Success)
            return string.Concat(markdownBody.AsSpan(0, match.Index), imageMarkdown, markdownBody.AsSpan(match.Index + match.Length));

        var lines = markdownBody.Split('\n').ToList();
        for (var idx = 0; idx < lines.Count; idx++)
        {
            if (lines[idx].Contains("**TL;DR**"))
            {
                var insertAt = idx + 1;
                while (insertAt < lines.Count && string.IsNullOrWhiteSpace(lines[insertAt]))
                    insertAt++;
                lines.Insert(insertAt, imageMarkdown);
                lines.Insert(insertAt + 1, "");
                return string.Join("\n", lines);
            }
        }

        return imageMarkdown + "\n\n" + markdownBody;
    }
}
