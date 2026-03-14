using System.Text.RegularExpressions;

namespace BlogGenerator.Core.PostGeneration;

public static partial class TagInferrer
{
    private static readonly HashSet<string> Stopwords = new(StringComparer.OrdinalIgnoreCase)
    {
        "the", "and", "for", "with", "that", "this", "into", "from", "your", "you",
        "are", "was", "will", "have", "using", "about", "what", "need", "know",
        "over", "its", "their", "those", "these",
        "such", "tips", "guide", "latest", "today", "tomorrow", "overview", "intro",
        "developers", "developer", "engineers", "engineer", "update", "updates",
        "insights", "insight", "future", "news", "deep", "dive", "focus", "weekly",
        "daily", "report", "analysis", "roundup", "learn", "learning", "build",
        "building", "powered", "power", "next", "gen", "generative", "recent",
        "versus", "plus", "look", "back", "ahead", "quick", "start", "setup",
        "create", "creating", "created", "some", "page", "pages", "step", "steps",
    };

    [GeneratedRegex(@"[A-Za-z0-9\+\.\-]+")]
    private static partial Regex TokenRegex();

    [GeneratedRegex(@"[a-z]")]
    private static partial Regex HasLowerRegex();

    [GeneratedRegex(@"[^\w\+\-\.]")]
    private static partial Regex NonTagCharRegex();

    [GeneratedRegex(@"-{2,}")]
    private static partial Regex MultiDashRegex();

    public static List<string> Infer(string markdownBody, string? model)
    {
        var candidates = new Dictionary<string, int>(StringComparer.Ordinal);
        var sections = new List<string>();

        foreach (var line in markdownBody.Split('\n'))
        {
            var stripped = line.Trim();
            if (stripped.StartsWith('#'))
                sections.Add(stripped.TrimStart('#').Trim());
            else if (stripped.StartsWith("**TL;DR**", StringComparison.OrdinalIgnoreCase))
                sections.Add(stripped.Split("**TL;DR**", 2)[^1].Trim(' ', ':'));
        }

        var textBlob = sections.Count > 0 ? string.Join(" ", sections) : markdownBody;

        foreach (Match m in TokenRegex().Matches(textBlob))
        {
            var normalized = NormalizeTag(m.Value);
            if (!string.IsNullOrEmpty(normalized))
                candidates[normalized] = candidates.GetValueOrDefault(normalized) + 1;
        }

        var tags = new List<string>();
        foreach (var (token, _) in candidates.OrderByDescending(kv => kv.Value).ThenBy(kv => kv.Key))
        {
            if (!tags.Contains(token))
                tags.Add(token);
            if (tags.Count >= 5)
                break;
        }

        var lowerMd = markdownBody.ToLowerInvariant();
        if (lowerMd.Contains("ai") && !tags.Contains("ai"))
            tags.Add("ai");

        var modelTag = (model ?? "claude").Trim().ToLowerInvariant();
        if (!string.IsNullOrEmpty(modelTag) && !tags.Contains(modelTag))
            tags.Add(modelTag);

        if (tags.Count == 0)
            tags = ["ai", string.IsNullOrEmpty(modelTag) ? "claude" : modelTag];

        if (tags.Count > 6)
        {
            var core = tags.Where(t => t != modelTag).Take(5).ToList();
            if (!string.IsNullOrEmpty(modelTag))
                core.Add(modelTag);
            tags = core;
        }

        return tags;
    }

    internal static string NormalizeTag(string token)
    {
        token = token.Trim().ToLowerInvariant();
        if (string.IsNullOrEmpty(token) || Stopwords.Contains(token) || token.Length < 3)
            return "";
        if (!HasLowerRegex().IsMatch(token))
            return "";
        token = NonTagCharRegex().Replace(token, "-");
        token = MultiDashRegex().Replace(token, "-").Trim('-');
        return token;
    }
}
