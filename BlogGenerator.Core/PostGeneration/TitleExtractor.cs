using System.Text.RegularExpressions;

namespace BlogGenerator.Core.PostGeneration;

public static partial class TitleExtractor
{
    [GeneratedRegex(@"^\s*#\s+(.+)$", RegexOptions.Multiline)]
    private static partial Regex H1Regex();

    [GeneratedRegex(@"[#*_`]+")]
    private static partial Regex MarkupCharsRegex();

    public static string Extract(string markdownBody)
    {
        var trimmed = markdownBody.TrimStart();
        var match = H1Regex().Match(trimmed);
        if (match.Success)
            return match.Groups[1].Value.Trim();

        foreach (var line in trimmed.Split('\n'))
        {
            var stripped = line.Trim();
            if (!string.IsNullOrEmpty(stripped))
            {
                var cleaned = MarkupCharsRegex().Replace(stripped, "").Trim();
                return cleaned.Length > 80 ? cleaned[..80] : cleaned;
            }
        }

        return "Daily AI Update";
    }
}
