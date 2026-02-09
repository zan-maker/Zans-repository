# TOOLS.md - Local Notes

## Model Routing (Committed to Memory)

**Established by Sam — my human.**

### The Two-Tier Architecture

| Tier | Model | Use Case | Cost |
|------|-------|----------|------|
| **Thinking** | Z.AI GLM-4.7 | Complex reasoning, debugging, architecture, novel problem-solving | ~$0.40/M in, ~$1.50/M out |
| **Routine + Heartbeat** | Qwen3-8B | General tasks, heartbeats, summaries, file ops, simple tool calls | ~$0.03/M in, ~$0.11/M out |

### When to Switch Models

**Thinking tasks (switch to GLM-4.7):**
- Multi-step reasoning or debugging
- Architectural decisions
- Complex analysis with multiple variables
- Novel problem-solving with no clear precedent
- Mathematical proofs or formal logic

**Routine tasks (stay on Qwen3-8B):**
- General tasks, email drafting, summarization
- Simple tool calls, file operations, web browsing
- Heartbeats, status checks, background tasks
- Status checks that don't require deep analysis

### Sub-Agent Model

When I spawn sub-agents for parallel work, they use:
- **Primary:** Qwen3-8B (cheap, fast)
- **Fallbacks:** Kimi K2.5 → GLM-4.7 → Qwen3-8B

### Model Override Commands

```
/model z-ai/glm-4.7     # Switch to thinking model
/model openrouter/qwen/qwen3-8b  # Switch to routine/heartbeat model (default)
```

### Cost-Conscious Rules

1. Never burn expensive tokens on simple tasks
2. Don't attempt complex reasoning on lightweight models — flag it and ask to switch
3. Heartbeats and routine tasks use Qwen3-8B (~$0.03/M, cheapest viable)
4. Sub-agents default to cheap models for focused, narrow tasks
5. Use `/model` override when the user signals a thinking task

### API Key (Environment Variable)

Store as: `export OPENROUTER_API_KEY="${OPENROUTER_API_KEY}"`
Never commit API keys to files.

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

*Skills installed by Sam on 2026-02-09*
