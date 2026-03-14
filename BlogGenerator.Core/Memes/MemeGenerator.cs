using BlogGenerator.Core.Configuration;
using SixLabors.Fonts;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Drawing.Processing;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;

namespace BlogGenerator.Core.Memes;

public static class MemeGenerator
{
    private static readonly string[] FontCandidates =
    [
        // Bundled font (relative to solution root)
        "fonts/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ];

    public static string? GenerateContextualMeme(
        string markdownBody,
        string title,
        string slug,
        GenerationSettings settings,
        string? baseImagePath = null,
        string? outputDir = null)
    {
        var repoRoot = settings.RepoRoot;
        var basePath = baseImagePath ?? Path.Combine(repoRoot, "assets", "images", "robot.webp");
        if (!File.Exists(basePath))
        {
            Console.WriteLine("Base meme image not found; skipping meme generation.");
            return null;
        }

        Image<Rgba32> image;
        try
        {
            image = Image.Load<Rgba32>(basePath);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Unable to open base meme image: {ex.Message}");
            return null;
        }

        var targetDir = outputDir ?? Path.Combine(repoRoot, "assets", "images", "memes");
        Directory.CreateDirectory(targetDir);

        var topText = title.ToUpperInvariant();
        var bottomText = MemeExtractor.ExtractTldrLine(markdownBody) ?? "Azure devs react.";

        var font = LoadMemeFont(Math.Max(24, image.Width / 18), repoRoot);

        DrawCaptionBlock(image, topText, font, "top");
        DrawCaptionBlock(image, bottomText, font, "bottom");

        var filename = $"{DateTime.UtcNow:yyyyMMddHHmmss}-{slug}.png";
        var outputPath = Path.Combine(targetDir, filename);

        try
        {
            image.SaveAsPng(outputPath);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Failed to save generated meme: {ex.Message}");
            return null;
        }
        finally
        {
            image.Dispose();
        }

        var relPath = Path.GetRelativePath(repoRoot, outputPath).Replace('\\', '/');
        return relPath;
    }

    private static Font LoadMemeFont(int size, string repoRoot)
    {
        var collection = new FontCollection();
        foreach (var candidate in FontCandidates)
        {
            var path = candidate.StartsWith('/')
                ? candidate
                : Path.Combine(repoRoot, candidate);
            if (File.Exists(path))
            {
                try
                {
                    var family = collection.Add(path);
                    return family.CreateFont(size, FontStyle.Bold);
                }
                catch
                {
                    // try next
                }
            }
        }
        // Fallback: use SystemFonts if available
        if (SystemFonts.TryGet("DejaVu Sans", out var sysFamily))
            return sysFamily.CreateFont(size, FontStyle.Bold);

        throw new InvalidOperationException("No suitable font found for meme generation.");
    }

    private static void DrawCaptionBlock(Image<Rgba32> image, string text, Font font, string position)
    {
        if (string.IsNullOrEmpty(text)) return;

        var width = image.Width;
        var height = image.Height;
        const int topMargin = 20;
        const int bottomMargin = 20;
        const int padding = 24;
        const int spacing = 10;

        // Shorten text if needed
        if (text.Length > 220)
            text = text[..217] + "...";

        var lines = WrapTextPixels(text, font, width - 80);
        if (lines.Count == 0) lines = [text];

        var lineHeight = (int)TextMeasurer.MeasureSize("Ay", new TextOptions(font)).Height;
        var textHeight = lines.Count * lineHeight + spacing * (lines.Count - 1);

        int rectTop, rectBottom;
        if (position == "top")
        {
            rectTop = topMargin;
            rectBottom = rectTop + textHeight + padding * 2;
        }
        else
        {
            rectBottom = height - bottomMargin;
            rectTop = rectBottom - (textHeight + padding * 2);
        }

        rectTop = Math.Max(0, rectTop);
        rectBottom = Math.Min(height, rectBottom);

        // Draw semi-transparent background
        image.Mutate(ctx =>
        {
            ctx.Fill(Color.FromRgba(0, 0, 0, 180),
                new SixLabors.ImageSharp.Drawing.RectangularPolygon(0, rectTop, width, rectBottom - rectTop));
        });

        // Draw text lines
        var y = rectTop + padding;
        foreach (var line in lines)
        {
            var measured = TextMeasurer.MeasureSize(line, new TextOptions(font));
            var x = (width - measured.Width) / 2;

            // Shadow outlines
            image.Mutate(ctx =>
            {
                var shadowColor = Color.FromRgba(0, 0, 0, 230);
                foreach (var (dx, dy) in new[] { (-2, -2), (-2, 2), (2, -2), (2, 2) })
                {
                    ctx.DrawText(line, font, shadowColor, new PointF(x + dx, y + dy));
                }
                ctx.DrawText(line, font, Color.White, new PointF(x, y));
            });

            y += lineHeight + spacing;
        }
    }

    private static List<string> WrapTextPixels(string text, Font font, int maxWidth)
    {
        var words = text.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        if (words.Length == 0) return [];

        var lines = new List<string>();
        var current = words[0];

        for (var i = 1; i < words.Length; i++)
        {
            var testLine = $"{current} {words[i]}";
            var size = TextMeasurer.MeasureSize(testLine, new TextOptions(font));
            if (size.Width <= maxWidth)
            {
                current = testLine;
            }
            else
            {
                lines.Add(current);
                current = words[i];
            }
        }
        lines.Add(current);
        return lines;
    }
}
