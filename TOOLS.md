# TOOLS.md - Local Notes

## Model Routing (Committed to Memory)

**Established by Sam — my human.**

### Current Configuration

| Model | Provider | Status | Use Case |
|-------|----------|--------|----------|
| **Kimi K2.5** | Moonshot | **Primary** | All tasks — general, analytical, complex |
| Nemotron 3 Nano 30B | NVIDIA NIM | Available | Inference tasks |
| **GLM-4.7** | Z.AI | **Deep Research** | Complex reasoning, multi-step analysis, deep research |

### Model Switching Commands

```
/model moonshot/kimi-k2.5              # Default (Kimi)
/model nvidia/nemotron-3-nano-30b-a3b  # NVIDIA NIM (inference tasks)
/model zai/glm-4.7                     # Deep research model (Z.AI)
```

### When to Use GLM-4.7 (Deep Research)
- Multi-step reasoning and analysis
- Complex research requiring synthesis across sources
- Debugging and architecture decisions
- Novel problem-solving with no clear precedent
- Tasks requiring preserved thinking across turns

### Cost-Conscious Rules

1. Kimi K2.5 is the default for all tasks
2. Use GLM-4.7 for deep research and complex reasoning
3. Use Nemotron for lightweight inference tasks
4. Never burn expensive tokens on simple tasks

### API Keys (Environment Variables)

- **Kimi:** `KIMI_API_KEY` (already configured)
- **NVIDIA:** `NVIDIA_API_KEY` (configured for NIM)
- **Z.AI:** `ZAI_API_KEY` (for GLM-4.7 deep research)

---

## Web Access & Research APIs

### Search APIs

#### Primary: Brave Search API
- **API Key:** `BSAqx7g5ob7ymEOAUfRduTetIOWPalN`
- **Use:** Web search, news, general research
- **Status:** Primary search provider

#### Backup: Tavily API
- **API Key:** `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`
- **Use:** Fallback when Brave limits reached
- **Status:** Backup search provider

### Data Enrichment APIs

#### Hunter.io (Email Finder)
- **API Key:** `f65adb440d1d4be20ae1b75f972b637b3e04b8fa`
- **Use:** Find email addresses for lead generation
- **Domain:** `hunter.io`

#### Abstract API (Company Enrichment)
- **API Key:** `38aeec02e6f6469983e0856dfd147b10`
- **Use:** Company data enrichment
- **Dashboard:** https://app.abstractapi.com/api/company-enrichment

#### Zyte API (Web Scraping)
- **API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
- **Use:** Web scraping, target list building
- **Status:** Configured for crawling

### Web Scraping Tools

#### crawl4ai
- **Status:** To be installed
- **Use:** AI-ready web crawling
- **Guide:** https://dev.to/ali_dz/crawl4ai-the-ultimate-guide-to-ai-ready-web-crawling-2620
- **Model:** Uses GLM-4.7 (Z.AI) for content extraction

### Environment Variables Setup

```bash
# Model APIs
export KIMI_API_KEY="your-kimi-key"
export NVIDIA_API_KEY="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"
export ZAI_API_KEY="your-zai-key"

# Search APIs
export BRAVE_API_KEY="BSAqx7g5ob7ymEOAUfRduTetIOWPalN"
export TAVILY_API_KEY="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"

# Data Enrichment
export HUNTER_API_KEY="f701d171cf7decf7e730a6b1c6e9b74f29f39b6e"
export ABSTRACT_API_KEY="38aeec02e6f6469983e0856dfd147b10"
export ZYTE_API_KEY="8d3e9c7af6e948b088e96ad15ca21719"

# Email
export EMAIL_PASSWORD="cqma sflq nsfv itke"
```

---

## Installed Skills

| Skill | Path | Use Case |
|-------|------|----------|
| **Problem-Solving Frameworks** | `skills/problem-solving-frameworks/` | 20 structured frameworks for analysis, root cause, decision-making, risk assessment |
| **MIT First Principles** | `skills/mit-first-principles/` | Strategic analysis via hacker mindset, fire hose test, founder thinking |
| **Task Dashboard** | `skills/task-dashboard/` | Self-hosted Kanban board spec for tracking OpenClaw tasks |

### When to Use Each Skill

**Problem-Solving Frameworks** — Use when:
- User asks for structured analysis or frameworks
- Complex problem needs systematic decomposition
- Comparing options or validating assumptions
- Root cause diagnosis needed
- Available frameworks: 5 Whys, MECE Tree, Weighted Decision Grid, Pre-Mortem, OODA Cycle, SWOT+, etc.

**MIT First Principles** — Use when:
- Strategic analysis needed
- Prioritizing competing demands
- Challenging assumptions
- "Impossible" workload situations
- Key principles: Master the System, Fire Hose Test (Three I Model), Founder Thinking

**Task Dashboard** — Use when:
- User asks about task tracking or Kanban setup
- Need to integrate OpenClaw with self-hosted dashboard
- Technical spec for SQLite + Deno/Node API + React/Vue frontend

---

## Email Configuration

**Account:** zan@impactquadrant.info (Gmail)

### SMTP (Sending)
- Server: smtp.gmail.com
- Port: 587
- Security: TLS
- Auth: App password (stored as `EMAIL_PASSWORD` env var)

### IMAP (Receiving)
- Server: imap.gmail.com
- Port: 993
- Security: SSL

### Environment Variable
```bash
export EMAIL_PASSWORD="cqma sflq nsfv itke"
```

### Usage
- Send emails: `message` tool with email target
- Check inbox: Available via email/IMAP tools

---

## Sub-Agent Orchestration

**Primary:** Zan (orchestrator)  
**Specialized Agents:** 3 domain-specific sub-agents

### Sub-Agent Roster

| Agent | Domain | Location | Use When |
|-------|--------|----------|----------|
| **TradeRecommender** | Trading (stocks, Polymarket, Kalshi) | `agents/trade-recommender/` | Trading opportunities, market analysis |
| **MiningMetalsAnalyst** | Mining operations, metal arbitrage | `agents/mining-metals-analyst/` | Mine analysis, commodity arbitrage |
| **LeadGenerator** | Fractional CFO leads, B2B consulting | `agents/lead-generator/` | Lead gen, prospect research, outreach |

### Orchestration Workflow

1. **Sam requests task** → Zan receives and interprets
2. **Zan routes to appropriate agent** → Spawns sub-agent in isolated session
3. **Agent executes independently** → Works with domain-specific skills + web access
4. **Agent returns output** → Submits analysis to Zan
5. **Zan synthesizes** → Reviews, formats, presents to Sam
6. **Sam decides** → Reviews recommendations, executes if approved

### Key Constraints

- **No autonomous execution** — All recommendations reviewed by Sam
- **Recommendations only** — Agents analyze; Sam decides
- **Risk disclosure required** — All downsides highlighted
- **Confidence scoring** — 1-10 scale on all outputs

### Spawn Commands

```
Spawn TradeRecommender to analyze [market/opportunity]
Focus on: [stocks/Polymarket/Kalshi]
Timeframe: [daytrade/swing/position]
Use web search: [yes/no]

Spawn MiningMetalsAnalyst to evaluate [mine/metal]
Focus on: [grade analysis/arbitrage/sector]
Commodity: [gold/copper/lithium/etc.]
Use web search: [yes/no]

Spawn LeadGenerator to identify leads for [service]
Target: [industry/stage/geography]
Output: [lead list/outreach drafts]
Use web search: [yes/no]
Use Hunter.io: [yes/no]
Use Abstract API: [yes/no]
```

---

## Sub-Agent Skills

Skills are domain-specific and attached to individual sub-agents:

### TradeRecommender (`agents/trade-recommender/skills/`)
| Skill | Purpose |
|-------|---------|
| Deep Research Best Practices | Evidence-based decision making, source grading |
| Hayakawa Ladder of Abstraction | Strategic vs. concrete communication |
| Options Research | Quant-grade options analysis (Greeks, IV, skew) |
| Bregman Projection Arbitrage | Prediction market arbitrage (Frank-Wolfe, Polymarket) |

### MiningMetalsAnalyst (`agents/mining-metals-analyst/skills/`)
| Skill | Purpose |
|-------|---------|
| Deep Research Best Practices | Evidence-based decision making, source grading |
| Hayakawa Ladder of Abstraction | Strategic vs. concrete communication |
| Metals Pricing MVP | Scraping-based metal price monitoring |
| Mine Grading Classification | Grade bands by commodity and mining method |

### LeadGenerator (`agents/lead-generator/skills/`)
| Skill | Purpose |
|-------|---------|
| Deep Research Best Practices | Evidence-based prospect research |
| Hayakawa Ladder of Abstraction | Strategic vs. concrete messaging |

---

*Skills installed by Sam on 2026-02-09*  
*Email configured on 2026-02-10*  
*Sub-agents configured on 2026-02-10*  
*Sub-agent skills attached on 2026-02-10*  
*GLM-4.7 deep research model added on 2026-02-10*  
*Web access APIs configured on 2026-02-10*
