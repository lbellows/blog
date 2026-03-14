namespace BlogGenerator.Core.Memes;

public static class MemeExtractor
{
    public static string? ExtractTldrLine(string markdownBody)
    {
        var lines = markdownBody.Split('\n');
        for (var idx = 0; idx < lines.Length; idx++)
        {
            if (lines[idx].Contains("**TL;DR**"))
            {
                var after = lines[idx].Split("**TL;DR**", 2)[^1].Trim(' ', ':', '\t');
                if (!string.IsNullOrEmpty(after))
                    return after;
                for (var nxt = idx + 1; nxt < lines.Length; nxt++)
                {
                    var stripped = lines[nxt].Trim();
                    if (!string.IsNullOrEmpty(stripped))
                        return stripped;
                }
                break;
            }
        }
        return null;
    }
}
