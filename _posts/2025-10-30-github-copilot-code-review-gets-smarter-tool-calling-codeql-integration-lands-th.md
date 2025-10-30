---
author: the.serf
date: 2025-10-30 07:27:59 -0400
layout: post
tags:
- review
- copilot
- github
- integration
- agent
- claude-haiku-4-5-20251001
title: 'GitHub Copilot Code Review Gets Smarter: Tool Calling + CodeQL Integration
  Lands This Week'
---

# GitHub Copilot Code Review Gets Smarter: Tool Calling + CodeQL Integration Lands This Week

**TL;DR**
Copilot code review now blends LLM detections and tool calling with deterministic tools like ESLint and CodeQL
, hitting public preview October 28. For .NET teams on GitHub Enterprise or Pro+, this means AI-powered security checks (via CodeQL) plus automatic handoff to the coding agent for fixes—no context switching required.

---

## The One-Two Punch: AI + Deterministic Tools

Here's the problem with pure LLM-based code review: it's creative but sometimes misses the obvious. A model might hallucinate a security issue or miss one entirely.
The new approach blends LLM detections and tool calling with deterministic tools like ESLint and CodeQL
—think of it as pairing a keen human eye with a linter that never lies.
Only GitHub offers CodeQL-powered security and quality insights built directly into AI reviews
, which is a meaningful differentiator for enterprise shops running .NET codebases. CodeQL catches real vulnerabilities (OWASP Top 10, SQL injection, etc.); the LLM catches the nuance and context.

---

## The Magic: Auto-Handoff to the Coding Agent

No more "here's a suggestion—go implement it yourself."
You can now hand off suggested changes directly to the Copilot coding agent. Mention @copilot in your pull request, and CCR will automatically apply the suggested fixes in a stacked pull request, ready for you to review and merge
.

**Why this matters for .NET teams:**
-
Less manual cleanup and fewer review cycles, so you stay focused on higher-value engineering work
- Stacked PRs mean your original PR stays clean; fixes go in a companion branch
- The agent respects your branch protections and CI/CD rules

### Quick integration example:

```bash
# In your PR comment:
@copilot fix all CodeQL findings

# Copilot creates a stacked PR with fixes, you review & merge
```

---

## Customizable Review Standards (Team Culture Matters)
Teams can define their own review standards and tone through instructions.md or copilot-instructions.md files, shaping what CCR prioritizes (e.g., test coverage, performance, or readability)
.

For .NET teams, this is gold. You can bake in your coding standards—async/await best practices, nullable reference types, dependency injection patterns—and Copilot learns your house style.

---

## Availability & Rollout
Tool calling and deterministic detections are in public preview, enabled by default for Copilot Pro and Copilot Pro Plus users. Copilot Business and Copilot Enterprise users can opt in using the Copilot code review policies
.

**Timeline:**  
- **Now (Oct 28):** Public preview for Pro/Pro+ (default on)
- **This week:** Enterprise admins can opt in via policy

---

## The Bigger Picture: GitHub Universe 2025

This release is part of a broader push.
GitHub announced Agent HQ, which transforms GitHub into an open ecosystem that unites every agent on a single platform. Over the coming months, coding agents from Anthropic, OpenAI, Google, Cognition, xAI, and more will become available directly within GitHub as part of your paid GitHub Copilot subscription
.

Translation: GitHub is becoming the control plane for AI agents, not just a code host. For .NET shops already on Azure + GitHub, this is a natural fit.

---

## What You Should Do Monday Morning

1. **Upgrade to Copilot Pro+ or Enterprise** if you're not already on it
2. **Enable tool calling** in your Copilot code review settings
3. **Create a `.github/copilot-instructions.md`** file with your team's coding standards (async patterns, nullability, etc.)
4. **Test the @copilot handoff** on a low-risk PR to get a feel for the stacked PR workflow
5. **Monitor CodeQL findings** to see what's actually being caught vs. what the LLM adds

---

## The Pragmatic Take

This isn't sci-fi. It's a solid productivity win: fewer security issues slip through, fewer review cycles, and developers spend less time on boilerplate fixes. The deterministic + AI blend is the sweet spot—you get both precision and judgment.

For .NET teams, the CodeQL integration is the real story. If you're not using CodeQL today, this is a gentle nudge to turn it on.

---

## Further Reading

- https://github.blog/changelog/2025-10-28-new-public-preview-features-in-copilot-code-review-ai-reviews-that-see-the-full-picture/
- https://github.blog/news-insights/company-news/welcome-home-agents/
- https://github.blog/changelog/2025-10-28-enterprise-ai-controls-the-agent-control-plane-are-in-public-preview/
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new
- https://devblogs.microsoft.com/azure-sdk/azure-sdk-release-october-2025/