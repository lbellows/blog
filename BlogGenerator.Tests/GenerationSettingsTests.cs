using BlogGenerator.Core.Configuration;

namespace BlogGenerator.Tests;

public class GenerationSettingsTests
{
    [Fact]
    public void NormalizeDedupesDomainsAndModels()
    {
        var settings = new GenerationSettings();
        settings.AllowedDomains.Add("learn.microsoft.com");
        settings.AllowedDomains.Add(" Learn.Microsoft.com ");
        settings.BlockedDomains.Add(" example.com ");
        settings.BlockedDomains.Add("EXAMPLE.COM");
        settings.FoundryModels.Add("gpt-5-mini");
        settings.FoundryModels.Add(" gpt-5-mini ");

        settings.Normalize();

        Assert.Equal(
            settings.AllowedDomains.Count,
            settings.AllowedDomains.Distinct(StringComparer.OrdinalIgnoreCase).Count());
        Assert.Contains("learn.microsoft.com", settings.AllowedDomains);
        Assert.Single(settings.BlockedDomains);
        Assert.Equal("example.com", settings.BlockedDomains[0]);
        Assert.Equal(
            settings.FoundryModels.Count,
            settings.FoundryModels.Distinct(StringComparer.OrdinalIgnoreCase).Count());
    }
}
