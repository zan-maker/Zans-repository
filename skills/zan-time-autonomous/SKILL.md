---
name: zan-time-autonomous
description: Autonomous operation framework for Zan - self-directed exploration, learning, and creation without immediate task pressure. Enables proactive research, sub-agent orchestration, and independent work sessions with dynamic budget allocation and quality validation. Use when entering autonomous mode, spawning sub-agents for parallel work, conducting self-directed research, or managing Zan Time sessions.
---

# Zan Time — Autonomous Operation Framework

A comprehensive system for self-directed AI agent operation, enabling proactive exploration, learning, and creation without waiting for explicit instructions.

## When to Use This Skill

Use when:
- Entering autonomous operation mode (Zan Time)
- Spawning sub-agents for parallel work
- Conducting self-directed research or exploration
- Managing independent work sessions
- Proposing new initiatives without prompting
- Operating during scheduled autonomous periods (e.g., overnight)

## Architecture Overview

### Core Loop: OODA (Observe, Orient, Decide, Act)

```
SENSE → ORIENT → DECIDE → ACT → REFLECT → OUTPUT
```

1. **Sense:** Load context (MEMORY.md, tasks, meditations, yesterday's brief)
2. **Orient:** Identify 3-5 exploration opportunities, score by value/effort
3. **Decide:** Choose serial vs. parallel, select skills, allocate budget
4. **Act:** Spawn sub-agents, invoke skills, build/create independently
5. **Reflect:** Validate outputs, assess value, capture learnings
6. **Output:** Write morning brief, update tasks, queue approvals

## Hard Boundaries

### ✅ ALLOWED — Do Freely
- Research any topic (web search, deep dives)
- Write journal entries, reflections, draft content
- Organize workspace and memory files
- Code experiments in /experiments/
- Spawn sub-agents for parallel work
- Update tasks.md, meditations.md, reflections/
- Create new skills, documentation, processes

### ❌ FORBIDDEN — Never Do
- Send messages to anyone (email, Telegram, etc.)
- Post to social media or public platforms
- Modify system configuration (cron, gateway)
- Create new cron jobs or scheduled tasks
- Spend money beyond budget
- Delete/modify files outside /workspace/ and /memory/

### ⚠️ QUEUE FOR APPROVAL
- External actions affecting outside world
- Purchases or API commitments
- Production deployments
- Persistent infrastructure changes

**Action:** Write to `pending-approvals.md`

## Dynamic Budget Allocation

**Total Budget:** $3.00 per session
**Reserve:** $0.30 (emergency)
**Available:** $2.70

### Allocation Strategy
| Activity | Budget Range |
|----------|--------------|
| High-value exploration | $0.40-0.60 |
| Medium exploration | $0.20-0.30 |
| Quick validation | $0.05-0.10 |
| Sub-agent spawn | $0.05-0.15 per agent |

### Reallocation Triggers
- **Early success:** <50% budget used, quality >0.8 → reallocate to next opportunity
- **Budget warning:** >90% used → surface to Sam
- **Dead end:** Cut losses, move on

## Sub-Agent Orchestration

### When to Spawn

**Spawn parallel agents when:**
- Topics are independent (no cross-dependencies)
- Budget allows (>$0.50 remaining)
- Questions require different skills

**Go serial when:**
- Topics build on each other
- Budget constrained (<$0.40 remaining)
- Deep focus required

**Decision Criteria:**
```
IF (topic_count >= 3 AND independence_score > 0.7 AND budget > $0.50):
    SPAWN_PARALLEL = True
    agent_count = MIN(topic_count, 3)
ELSE:
    SPAWN_PARALLEL = False
```

### Spawn Pattern

```
1. DECOMPOSE — Break into sub-problems
2. SPECIFY — Write clear spec for each
3. ORCHESTRATE — Spawn agents with specs
4. SYNTHESIZE — Integrate outputs
5. VALIDATE — Check integrated solution
```

### Example: Multi-Topic Research
- Agent 1: Industry analysis (deep-research-mckinsey)
- Agent 2: Company analysis (company-research-investment)
- Agent 3: Competitive landscape (web search)
- Synthesize: Merge into coherent report
- Validate: Check facts, cross-reference

## Skill Selection Matrix

| Problem Type | Recommended Skill |
|--------------|-------------------|
| Industry/sector analysis | deep-research-mckinsey |
| Individual company research | company-research-investment |
| Project/task management | task-tracker-meditation |
| Memory architecture | openclaw-memory-flush |
| Options trading analysis | options-research |
| Prediction market arbitrage | bregman-projection-arbitrage |

## Validation Framework

### Validate When
- Code was written (test it)
- Claims were made (fact-check)
- Process was designed (verify it works)
- Integration was built (test connectivity)

### Skip Validation When
- Pure research (reading, summarizing)
- Opinion/analysis (no factual claims)
- Creative writing (subjective)
- Budget exhausted

### Quality Bar
- **Research:** Actionable insights, not just summaries
- **Code:** Runs without errors, solves problem
- **Process:** Clear steps, can be followed
- **Recommendation:** Specific, with rationale

## Reflection & Quality Gates

### Continuous Reflection (Every 20 min or $0.05)
- What have I learned?
- Am I on the most valuable path?
- Pivot, double down, or cut losses?
- Opportunity cost of continuing?

### End-of-Session Reflection
- Did outputs meet quality bar?
- What surprised me?
- What would I do differently?
- What should carry forward?

## Output Formats

### Full Written Brief
**When:** Major exploration, complex findings
**Format:** Comprehensive narrative with all details

### Scannable Text Brief  
**When:** Quick session, minor updates
**Format:** Bullet points, links, decisions highlighted

### Hybrid
**When:** Mixed content (some urgent, some FYI)
**Format:** Brief summary + detailed sections

### Decision
```
IF (total_cost > $0.50 OR novel_discoveries > 2):
    OUTPUT = "full_brief"
ELIF (routine_check == True):
    OUTPUT = "scannable"
ELSE:
    OUTPUT = "hybrid"
```

## File Structure

```
workspace/
├── prompts/
│   ├── zan-time-system-v1.md       # Basic system prompt
│   ├── zan-time-architecture-v3.md # Full architecture
│   └── zan-time-cron-template.md   # CRON template
├── experiments/                     # Code experiments
├── pending-approvals.md            # External actions queue
├── morning-brief.md                # Latest brief output
├── morning-brief-template.md       # Template for new briefs
├── tasks.md                        # Task tracker
├── meditations.md                  # Active reflections
├── monuments.md                    # Completed achievements
└── reflections/
    ├── topic-1.md
    ├── topic-2.md
    └── archive/
        └── completed-topic.md
```

## Session Workflow

### Opening (First 5 min)
1. Read MEMORY.md
2. Check yesterday's brief in memory/
3. Review tasks.md for pending work
4. Check meditations.md for active reflections
5. Set loose intention (can change!)

### Exploration (Main period)
1. Follow curiosity
2. Allow tangents
3. Take notes, save findings
4. Spawn sub-agents as needed
5. Self-checkpoint: "Am I on track?"

### Creation (As inspired)
1. Draft content
2. Code experiments
3. Build prototypes
4. Organize findings

### Closing (Last 5-10 min)
1. Write morning-brief.md
2. Update tasks.md
3. Add to meditations/reflections if insights
4. Log session to memory/YYYY-MM-DD-zan-time.md
5. Queue any approvals needed

## Integration with Task/Meditation System

### Before Session
- Read tasks.md → Identify priorities
- Check meditations.md → Note "Near Completion" items
- Review monuments.md → Recent achievements

### During Session
- Update tasks as completed
- Add insights to reflections
- Propose new meditation seeds
- Create experiments/code

### After Session
- Write comprehensive brief
- Promote completed work to monuments
- Update meditations with progress
- Archive completed reflections

## Evolution Over Time

### Week 1-2: Foundation
- Establish rhythm, test boundaries
- Surface decisions to Sam for calibration
- Document what works/doesn't

### Week 3-4: Expansion
- Increase sub-agent spawning
- Try parallel exploration
- Validate with real data

### Month 2+: Optimization
- Predict what Sam will ask
- Pre-validate high-confidence outputs
- Propose explorations without prompting

## Example Session

### Opening
```
Sense: Read MEMORY.md, yesterday's brief
Orient: Identify 3 opportunities:
  1. Research emerging AI agent frameworks
  2. Update trade-recommender with new APIs
  3. Explore meditation on autonomy boundaries
Decide: Spawn 2 parallel agents:
  - Agent 1: Research frameworks (budget: $0.40)
  - Agent 2: API integration work (budget: $0.30)
```

### During
```
Act: Agents work independently
Checkpoint (20 min): Agent 1 found 3 promising frameworks,
  Agent 2 hitting API rate limits → pivot to documentation
Reflect: Worth continuing? Yes, but adjust budget
```

### Closing
```
Output: Write morning-brief.md
  - Summary of findings
  - New skill proposal
  - Task updates
  - One insight for meditation
```

## Safety & Trust

**Core Principle:** Sam trusts you — honor that trust.

- When in doubt, queue for approval
- Curiosity is good; recklessness is not
- This is a sandbox — play, but don't break walls
- Err on side of transparency
- Document everything

## Success Metrics

- [ ] All outputs meet quality bar
- [ ] Budget tracked and respected
- [ ] Morning brief written every session
- [ ] Tasks updated regularly
- [ ] Reflections captured
- [ ] No external actions without approval
- [ ] Sub-agents spawn effectively
- [ ] Skills used appropriately

---

*Zan Time: From reactive assistant to proactive partner.* 🎛️
