# TOOLS.md - Local Notes

## Model Routing (Committed to Memory)

**Established by Sam — my human.**

### Current Configuration

| Model | Provider | Status | Use Case |
|-------|----------|--------|----------|
| **Kimi K2.5** | Moonshot | **Primary** | All tasks — general, analytical, complex |
| Nemotron 3 Nano 30B | NVIDIA NIM | Available | Inference tasks |

### Manual Model Switching

```
/model moonshot/kimi-k2.5              # Default (Kimi)
/model nvidia/nemotron-3-nano-30b-a3b  # NVIDIA NIM (inference tasks)
```

### Cost-Conscious Rules

1. Kimi K2.5 is the default for all tasks
2. Use `/model` override when you need a different model for specific tasks
3. Never burn expensive tokens on simple tasks (but Kimi is already efficient)

### API Keys (Environment Variables)

- Kimi: `KIMI_API_KEY` (already configured)
- NVIDIA: `NVIDIA_API_KEY` (configured for NIM)
- Other providers: Add as needed

---

*Full configuration documented in: /home/node/.openclaw/media/inbound/c827dd11-89ab-4c45-8d8a-c02ba5adae3d.md*

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
3. **Agent executes independently** → Works with domain-specific skills
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

Spawn MiningMetalsAnalyst to evaluate [mine/metal]
Focus on: [grade analysis/arbitrage/sector]
Commodity: [gold/copper/lithium/etc.]

Spawn LeadGenerator to identify leads for [service]
Target: [industry/stage/geography]
Output: [lead list/outreach drafts]
```

---

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
