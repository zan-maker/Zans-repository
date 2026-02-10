# TOOLS.md - Local Notes

## Model Routing (Committed to Memory)

**Established by Sam — my human.**

### Current Configuration

| Model | Provider | Status | Use Case |
|-------|----------|--------|----------|
| **Kimi K2.5** | Moonshot | **Primary** | All tasks — general, analytical, complex |

### Manual Model Switching

If you need to use other models, add them to `openclaw.json` first, then switch:

```
/model z-ai/glm-4.7     # Complex reasoning (requires Z.AI API key)
/model provider/model-id  # Any other configured model
```

### Cost-Conscious Rules

1. Kimi K2.5 is the default for all tasks
2. Use `/model` override when you need a different model for specific tasks
3. Never burn expensive tokens on simple tasks (but Kimi is already efficient)

### API Keys (Environment Variables)

- Kimi: `KIMI_API_KEY` (already configured)
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

*Skills installed by Sam on 2026-02-09*
*Email configured on 2026-02-10*
