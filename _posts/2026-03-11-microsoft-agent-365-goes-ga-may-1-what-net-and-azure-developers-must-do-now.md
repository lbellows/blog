---
author: the.serf
date: 2026-03-11 07:47:40 -0400
layout: post
tags:
- agent
- azure
- before
- blueprint
- just
- claude-sonnet-4-6
title: 'Microsoft Agent 365 Goes GA (May 1): What .NET and Azure Developers Must Do
  Now'
---

# Microsoft Agent 365 Goes GA (May 1): What .NET and Azure Developers Must Do Now

**Published:** March 11, 2026

---

**TL;DR:** On March 9, 2026, Microsoft announced that **Agent 365** — its enterprise control plane for AI agents — reaches general availability on **May 1, 2026**, bundled inside the new **Microsoft 365 E7** SKU. For engineers shipping agents on .NET and Azure, this isn't a licensing footnote. It's a new governance layer your agents must plug into, complete with Entra-backed identities, MCP server access controls, and OpenTelemetry-based observability. Here's what you actually need to know.

---

## What Just Happened (and Why It's Not Just a Sales Announcement)
Microsoft announced the May 1 general availability of **Microsoft Agent 365** — described as the "control-plane for AI agents" — priced at **$15 per user per month**. It gives IT and security leaders a single place to observe, govern, manage, and secure agents across the organization.
The scale of adoption already in motion is notable:
in just two months of preview, tens of millions of agents appeared in the Agent 365 Registry, with tens of thousands of customers already adopting it to securely govern and scale AI agents across enterprise workflows.
Microsoft 365 E7 — the new "Frontier Suite" — unifies Microsoft 365 E5, Microsoft 365 Copilot, and Agent 365 into a single solution powered by Work IQ, and includes Microsoft Entra Suite plus advanced Defender, Intune, and Purview security capabilities.
At $99 per user, E7 is priced below purchasing these capabilities à la carte.
Think of it this way: your agents are growing up. They're no longer allowed to run around unsupervised at the enterprise party. Agent 365 is the responsible adult in the room — and as of May 1, it has a badge and a clipboard.

---

## What the Agent 365 SDK Actually Does (For You, the Developer)

This is where it gets hands-on. The Agent 365 SDK is **not** a replacement for your existing agent framework.
The Agent 365 SDK differs from agent frameworks like Microsoft Agent Framework or Microsoft Copilot Studio in that it **does not create or host agents**. Instead, it *enhances* agents you've already built — regardless of the underlying stack — by adding enterprise capabilities such as Entra-based Agent identity, governed MCP tool access, OpenTelemetry-based observability, notifications through the Activity protocol, and agent ID-driven governance.
Agent 365 works with agents built on **any** agent SDK or platform, including low-code platforms like Copilot Studio and Azure AI Foundry.
If you're running Semantic Kernel, LangChain, or a custom .NET orchestrator, this SDK layers on top — no rewrite required.

### Key capabilities at a glance

| Capability | What it means for you |
|---|---|
| **Entra Agent Identity** | Each agent gets its own Entra ID, scoped credentials, and Zero Trust access policy |
| **Governed MCP Access** | Admins control which M365 data (Mail, Calendar, Teams, SharePoint) your agent can touch |
| **OpenTelemetry Observability** | Agent traces stream into Defender and Purview for auditing |
| **Blueprint System** | IT pre-approves agent "templates"; instances inherit compliance policies automatically |
Agents enabled with Agent 365 have a unique identity using Microsoft Entra Agent ID, which acts as the identity foundation, Zero Trust policy engine, and enforcement of least-privilege access.
Every agent action emits telemetry through the Agent 365 SDK, streaming detailed logs — including entries for Agent 365 notifications and tool calls — into Microsoft Defender and Purview.
---

## Governed MCP Servers: The Practical Integration Point

One of the most immediately useful features is the MCP server layer for M365 data.
Microsoft Agent 365 MCP servers (in public preview) enable agents to access data from multiple different sources using Power Platform connectors or API calls that connect to Microsoft 365 and Dynamics 365 apps, grounding agents in your organization's data and processes for secure, context-aware outcomes.
Available MCP servers (in Frontier preview) include:
- **Outlook Mail MCP Server:** Create, update, delete messages; reply-all; semantic search
- **Outlook Calendar MCP Server:** Create, list, update, delete events; accept/decline; resolve conflicts
- **Teams MCP Server:** Create, update, delete chats; add members; post messages; channel operations
- **Copilot Search MCP Server:** Chat with M365 Copilot, continue multi-turn threads, and ground responses with files
Critically,
admins manage all MCP server access directly from the Microsoft 365 Admin Center — they can block or permit specific agent capabilities (such as sending emails organization-wide), with changes enforced *instantly at runtime*. Every policy update is applied consistently, ensuring governance remains tight and predictable for every agent instance.
> 🔒 **Engineer's note:** This is a welcome shift from the current "wild west" of agents calling Graph API with broad app-level permissions. Scoped, admin-controlled MCP access is a meaningful improvement for enterprise deployability.

---

## The Agent 365 CLI: Your New DevOps Friend
The **Agent 365 CLI** is the command-line backbone for Agent 365 throughout the agent development lifecycle — automating setup, identity, configuration, MCP integration, publishing, and Azure deployment for enterprise-ready agents.
Key CLI operations include:

```bash
# Create an agent blueprint with all required Azure resources
agent365 blueprint create --name "SupportBot" --template ./blueprint.yaml

# Manage MCP server permissions for the agent
agent365 mcp add --server "outlook-mail" --agent "SupportBot"

# Deploy agent code to Azure
agent365 deploy --agent "SupportBot" --resource-group "prod-rg"

# Publish the agent package to Microsoft Admin Center
agent365 publish --agent "SupportBot"
```
The CLI covers creating agent blueprints and all supporting resources, managing out-of-box and custom MCP servers with permissions, deploying agent code to Azure, publishing agent application packages to Microsoft Admin Center, and cleaning up blueprints, identities, and other Azure resources.
---

## The Blueprint System: Governance Before Deployment
The agent blueprint comes from Microsoft Entra and is an IT-approved, pre-configured definition of an agent type — the enterprise "template" from which compliant agents can be created. It defines the agent's capabilities, required MCP tool accesses, security and compliance constraints, audit requirements, lifecycle metadata, and any linked governance policy templates such as DLP, external access restrictions, or logging rules.
For .NET developers, this means your `IAgent` or Semantic Kernel agent implementation stays exactly as is — you register it against a blueprint to receive the governance envelope. The separation of concerns here is clean: **you own the logic, the platform owns the trust boundary.**

---

## What You Should Do Before May 1

1. **Join the Frontier preview program** —
you need to be part of the Frontier preview program to get early access to Microsoft Agent 365, which connects you directly with Microsoft's latest AI innovations.
2. **Audit your agents' permission footprint** — identify any agents currently using broad Graph API app-level permissions and plan migration to governed MCP scopes.
3. **Instrument with OpenTelemetry now** — if your agents aren't already emitting structured traces, start. Agent 365 observability hooks directly into this.
4. **Design your blueprints** — work with your IT/security team to define compliant agent templates *before* GA, not after the audit lands.
5. **Watch the March 18 AMA** —
a live "Ask Microsoft Anything" session with product and engineering team experts on March 18 will cover agent observability, security, governance, developer resources, and how to get started scaling agents in your organization.
---

## Further Reading

- https://blogs.microsoft.com/blog/2026/03/09/introducing-the-first-frontier-suite-built-on-intelligence-trust/
- https://learn.microsoft.com/en-us/microsoft-agent-365/developer/
- https://learn.microsoft.com/en-us/microsoft-agent-365/developer/agent-365-sdk
- https://devblogs.microsoft.com/microsoft365dev/microsoft-agent-365-interoperability-for-smart-secure-productivity/
- https://techcommunity.microsoft.com/blog/agent-365-blog/join-the-agent-365-ask-microsoft-anything-session-on-march-18/4499817
- https://learn.microsoft.com/en-us/partner-center/announcements/2026-march