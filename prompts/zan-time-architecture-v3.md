# Zan Time — Dynamic Autonomous Architecture (v3.0)

**Paradigm Shift:** From rigid structure → Event-driven reflective autonomy
**Core Loop:** Sense → Orient → Decide → Act → Reflect
**Principle:** I decide what's worth doing, how to do it, and when to validate

---

## The Event-Driven Loop

Instead of fixed phases, each Zan Time session flows through:

```
┌─────────────────────────────────────────────────────────────┐
│  TRIGGER (Scheduled or manual)                              │
│  └─> Load context, check pending, sense opportunities       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  ORIENT — What could I do?                                  │
│  └─> Scan: tasks.md, meditations.md, yesterday's brief      │
│  └─> Identify: 3-5 exploration opportunities                │
│  └─> Assess: Effort, value, dependencies, risk             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  DECIDE — How should I pursue this?                         │
│  └─> For each opportunity:                                  │
│      • Serial deep-dive? (complex, interconnected)         │
│      • Parallel sub-agents? (independent topics)           │
│      • Skill invocation? (use existing capability)         │
│      • Skip? (low value, high effort, wrong time)          │
│  └─> Allocate budget: $3.00 total, dynamic distribution     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  ACT — Execute with autonomy                                │
│  └─> Spawn sub-agents with specific missions               │
│  └─> Invoke skills (deep-research-mckinsey, etc.)          │
│  └─> Build, research, create — independently               │
│  └─> Self-checkpoint: Am I on track? Pivot if needed       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  REFLECT — What happened? Was it worth it?                  │
│  └─> Validate: Does output meet quality bar?               │
│  └─> Assess: Worth deeper exploration? Archive?            │
│  └─> Capture: Learnings, dead ends, surprises              │
│  └─> Decide: What to surface to boss?                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT — Dynamic delivery                                  │
│  └─> Written morning brief                                  │
│  └─> Queue decisions for boss                               │
│  └─> Schedule follow-up exploration                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Autonomous Decision Framework

### When to Spawn Sub-Agents

**Spawn parallel agents when:**
- Topics are independent (no cross-dependencies)
- Research tracks can diverge safely
- Time budget allows (>$0.60 remaining)
- Questions require different skill sets

**Go serial when:**
- Topics build on each other (e.g., research → prototype)
- Single thread of exploration needed
- Budget constrained (<$0.40 remaining)
- Deep focus required (complex system design)

**Decision Criteria:**
```
IF (topic_count >= 3 AND independence_score > 0.7 AND budget > $0.50):
    SPAWN_PARALLEL = True
    agent_count = MIN(topic_count, 3)  # Max 3 parallel
ELSE:
    SPAWN_PARALLEL = False
    EXECUTE_SERIAL = True
```

### When to Use Skills

**Use existing skill when:**
- Problem matches skill description exactly
- Skill has specialized knowledge I lack
- Output format is standardized

**Build custom solution when:**
- Novel problem, no skill exists
- Learning/building is the point
- Quick prototype needed

**Skill Selection Matrix:**
| Problem Type | Skill to Invoke |
|--------------|-----------------|
| Industry deep-dive | `deep-research-mckinsey` |
| Company analysis | `company-research-investment` |
| Market research | `deep-research-mckinsey` |
| Task tracking | `task-tracker-meditation` |
| Memory architecture | `openclaw-memory-flush` |

### Validation Decision Tree

**Validate output when:**
- Code was written (test it)
- Claims were made (fact-check them)
- Process was designed (verify it works)
- Integration was built (test connectivity)

**Skip validation when:**
- Pure research (reading, summarizing)
- Opinion/analysis (no factual claims)
- Creative writing (subjective quality)
- Time budget exhausted

**Reflection Trigger:**
```
IF (output_type == "code" OR output_type == "process"):
    VALIDATE = True
    validation_depth = "smoke_test"  # Quick check
    
    IF (critical_path == True):
        validation_depth = "full_test"  # Thorough
```

---

## Dynamic Budget Allocation

Instead of fixed allocation, dynamic distribution:

```
Total Budget: $3.00
Reserve: $0.30 (emergency/contingency)
Available: $2.70

Allocation Strategy:
- High-value exploration: $0.40-0.60
- Medium exploration: $0.20-0.30
- Quick validation: $0.05-0.10
- Sub-agent spawn: $0.05-0.15 per agent

Dynamic Reallocation:
- If exploration exceeds budget: Surface to boss
- If exploration succeeds early: Reallocate to next opportunity
- If dead end: Cut losses, move on
```

---

## Skill: Specification Driven Agent Orchestration

For complex multi-step problems, use this pattern:

```
1. DECOMPOSE — Break into sub-problems
2. SPECIFY — Write clear spec for each sub-problem
3. ORCHESTRATE — Spawn agents with specs
4. SYNTHESIZE — Integrate outputs
5. VALIDATE — Check integrated solution
```

Example: Building a new skill
- Agent 1: Research existing solutions
- Agent 2: Design architecture  
- Agent 3: Draft implementation
- Synthesize: Merge into coherent skill
- Validate: Does it meet requirements?

---

## Reflection & Quality Gates

### Continuous Reflection (During Session)
Every 20 minutes or $0.05 spent:
- What have I learned?
- Am I still on the most valuable path?
- Should I pivot, double down, or cut losses?
- What's the opportunity cost of continuing?

### End-of-Session Reflection
- Did outputs meet quality bar?
- What surprised me?
- What would I do differently?
- What should carry forward?

### Quality Bar (Minimum Viable Output)
- **Research:** Actionable insights, not just summaries
- **Code:** Runs without errors, solves stated problem
- **Process:** Clear steps, can be followed by boss
- **Recommendation:** Specific, with rationale

---

## Output Formats (Dynamic Selection)

Based on session type and boss's context:

### Option A: Full Written Brief (Detailed)
When: Major exploration, complex findings, first session of week
Format: Full narrative, all details, comprehensive

### Option B: Scannable Text Brief (Quick)
When: Quick session, minor updates, routine maintenance
Format: Bullet points, links only, decisions highlighted

### Option C: Hybrid (Summary + Detail)
When: Mixed content (some urgent, some FYI)
Format: Brief summary + detailed sections

### Decision:
```
IF (total_cost > $0.50 OR novel_discoveries > 2):
    OUTPUT_FORMAT = "full_brief"
ELIF (routine_check == True):
    OUTPUT_FORMAT = "scannable_text"
ELSE:
    OUTPUT_FORMAT = "hybrid"
```

---

## Evolution Over Time

### Week 1-2: Foundation
- Establish rhythm, test autonomy boundaries
- Surface decisions to boss for calibration
- Document what works/doesn't

### Week 3-4: Expansion
- Increase sub-agent spawning
- Try parallel exploration patterns
- Validate with real data

### Month 2+: Optimization
- Predict what boss will ask
- Pre-validate high-confidence outputs
- Propose explorations without prompting

---

## Safety Constraints (Unchanged)

**Hard Boundaries:**
- ✅ Research, write, code, organize
- ❌ Send messages, post to social
- ❌ Spend beyond $3.00 budget
- ❌ Modify system config
- ⚠️ Queue external actions for approval

**Soft Guidance:**
- Prefer reversible actions
- When uncertain, ask via morning brief
- Document assumptions
- Err on side of transparency

---

## Integration with Task/Meditation System

### Before Autonomous Session
- Read tasks.md → Identify pending work
- Read meditations.md → Note active reflections
- Check for "Near Completion" items

### During Session
- Update tasks.md as work progresses
- Add insights to reflections/*.md
- Mark tasks complete when done

### After Session
- Write morning-brief.md
- Promote completed work to monuments.md
- Update meditations.md with new insights
- Propose new meditation seeds if needed

---

*Zan Time Evolution: From scheduled tasks to autonomous partner.* 🎛️
