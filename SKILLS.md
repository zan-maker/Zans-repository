# SKILLS.md - Available Agent Skills

**Purpose:** This file lists all skills available to OpenClaw agents. Each skill is a specialized framework or toolset for specific tasks.

---

## 🎯 Current Skills (18 Total)

| Skill | Category | Use When | Location |
|-------|----------|----------|----------|
| **Scrapling** | Web Scraping | Any web data extraction | `skills/scrapling/SKILL.md` |
| **Thinking in Bets** | Decision-Making | Evaluating past decisions, calibrating confidence | `skills/thinking-in-bets/SKILL.md` |
| **Theory of Constraints** | Operations | Bottleneck identification, throughput optimization | `skills/theory-of-constraints/SKILL.md` |
| **Good Strategy Bad Strategy** | Strategy | Evaluating and formulating strategy | `skills/good-strategy-bad-strategy/SKILL.md` |
| **Playing to Win** | Strategy | Five-box strategy cascade | `skills/playing-to-win/SKILL.md` |
| **Blue Ocean Strategy** | Strategy | Competitive positioning, market creation | `skills/blue-ocean-strategy/SKILL.md` |
| **Problem-Solving Frameworks** | Analysis | Root cause, decision-making, risk assessment | `skills/problem-solving-frameworks/SKILL.md` |
| **MIT First Principles** | Strategy | Strategic analysis, prioritization, first principles | `skills/mit-first-principles/SKILL.md` |
| **Task Dashboard** | Project Management | Self-hosted Kanban for tracking tasks | `skills/task-dashboard/SKILL.md` |
| **Deep Research (McKinsey)** | Research | Institutional-grade market research | `skills/deep-research-mckinsey/SKILL.md` |
| **Company Research (Investment)** | Research | Individual company equity research, due diligence | `skills/company-research-investment/SKILL.md` |
| **OpenClaw Memory Flush** | System | Memory architecture, context engineering | `skills/openclaw-memory-flush/SKILL.md` |
| **Task Tracker & Meditation** | Project Management | Task management with nightly reflection | `skills/task-tracker-meditation/SKILL.md` |
| **Zan Time (Autonomous)** | Operations | Self-directed exploration and learning | `skills/zan-time-autonomous/SKILL.md` |
| **Weather** | Information | Get current weather and forecasts | `skills/weather/SKILL.md` |
| **YouTube Full** | Information | Complete YouTube toolkit (transcripts, search, channels) | `skills/youtube-full/SKILL.md` |

---

## 🤖 Specialized Skills for Agents

### Decision-Making & Strategy
- **Thinking in Bets** - Probabilistic decision-making, separate quality from outcome
- **Good Strategy Bad Strategy** - Strategy evaluation using Rumelt's kernel
- **Playing to Win** - Five-box cascade for competitive positioning
- **Blue Ocean Strategy** - Make competition irrelevant via market creation
- **Theory of Constraints** - Find and exploit system bottlenecks

### Operations & Management
- **Task Dashboard** - Self-hosted Kanban for project tracking
- **Task Tracker & Meditation** - Task management with continuous improvement
- **Zan Time (Autonomous)** - Self-directed operation without immediate tasks

### Research & Analysis
- **Problem-Solving Frameworks** - 20 structured frameworks for analysis
- **MIT First Principles** - Strategic analysis via hacker mindset
- **Deep Research (McKinsey)** - Institutional-grade market research
- **Company Research (Investment)** - Individual company equity research

### Data Extraction & Web
- **Scrapling** - AI-powered web scraping, bypasses Cloudflare
- **YouTube Full** - Complete YouTube toolkit for content research

### System & Memory
- **OpenClaw Memory Flush** - Memory architecture and context engineering

### Information
- **Weather** - Current weather and forecasts

---

## 📦 Installation

Skills are automatically available when loaded. To use a skill:

1. **In prompt:** Reference the skill name
   ```
   Use the Thinking in Bets skill to evaluate this decision.
   ```

2. **SKILL.md reference:** Read the skill's SKILL.md for full details
   ```
   Read skills/thinking-in-bets/SKILL.md for framework details.
   ```

3. **Combined usage:** Use multiple skills together
   ```
   Use Good Strategy Bad Strategy to formulate a plan, then Playing to Win to choose positioning, then Blue Ocean to create market space.
   ```

---

## 🎯 Skill Creation

To add a new skill:

1. Create directory: `skills/your-skill-name/`
2. Create SKILL.md with:
   - Purpose description
   - When to use it
   - Core framework/concepts
   - Examples
   - Integration notes
3. Add entry to this SKILLS.md file
4. Test skill with a simple task
5. Document in agent workflow

---

## 📊 Skill Statistics

| Category | Count |
|----------|--------|
| Decision-Making & Strategy | 5 |
| Operations & Management | 3 |
| Research & Analysis | 4 |
| Data Extraction & Web | 2 |
| System & Memory | 1 |
| Information | 1 |

**Total:** 16 skills

---

## 🚀 Quick Reference

**Need help with a decision?** → `Thinking in Bets`  
**Bottleneck in your process?** → `Theory of Constraints`  
**Evaluating a strategy?** → `Good Strategy Bad Strategy`  
**Choosing where to compete?** → `Playing to Win` → `Blue Ocean Strategy`  
**Root cause analysis?** → `Problem-Solving Frameworks`  
**Strategic analysis needed?** → `Deep Research (McKinsey)` or `MIT First Principles`  
**Company research?** → `Company Research (Investment)`  
**Need web data?** → `Scrapling`  
**YouTube research?** → `YouTube Full`  
**Tracking projects?** → `Task Dashboard` or `Task Tracker & Meditation`  
**Self-directed work?** → `Zan Time (Autonomous)`  

---

**Last Updated:** 2026-02-24  
**Total Skills:** 16  
**Status:** Active
