---
name: task-tracker-meditation
description: Project tracking system with Kanban-style task management, nightly meditation/reflection loops for continuous improvement, and monument archive for completed achievements. Use when managing projects, tracking tasks through completion, conducting nightly reflections on active topics, or reviewing past accomplishments. Triggers on "task tracker", "project management", "meditation", "reflection", "monument", or when organizing work and tracking progress.
---

# Task Tracker & Meditation System

A hybrid project management and self-improvement framework combining Kanban-style task tracking with nightly reflection meditations.

## System Overview

This system has three interconnected components:

1. **Task Tracker** (`tasks.md`) - Active project and task management (Kanban-style)
2. **Meditation Loop** (`meditations.md` + `reflections/`) - Nightly deep-dive reflections
3. **Monument Archive** (`monuments.md`) - Completed achievements and major milestones

---

## Part 1: Task Tracker (tasks.md)

### File Location
`tasks.md` in workspace root

### Structure

```markdown
# Task Tracker

## 🏃 Active (In Progress)

### High Priority
- [ ] Task 1 - Due: YYYY-MM-DD - Project: [Name]
  - Notes: [Context, blockers, next steps]
  
### Medium Priority
- [ ] Task 2 - Due: YYYY-MM-DD

### Low Priority  
- [ ] Task 3 - Due: YYYY-MM-DD

## 📋 Backlog (To Do)

- [ ] Future task 1
- [ ] Future task 2

## ✅ Done (This Week)

- [x] Completed task 1 - Completed: YYYY-MM-DD
- [x] Completed task 2 - Completed: YYYY-MM-DD

## 🏛️ Ready for Monument

- [ ] Completed task ready to archive
```

### Task Format

Each task should include:
- **Checkbox**: `- [ ]` for incomplete, `- [x]` for complete
- **Description**: Clear, actionable statement
- **Due Date**: `Due: YYYY-MM-DD` (optional but recommended)
- **Project Tag**: `Project: [Name]` for grouping
- **Notes**: Context, blockers, resources

### Priority Guidelines

| Priority | Response Time | Examples |
|----------|--------------|----------|
| **🔴 Critical** | Same day | System down, security issue, deadline today |
| **🟠 High** | 24-48 hours | Important deadlines, blocking others |
| **🟡 Medium** | This week | Standard tasks, improvements |
| **🟢 Low** | When possible | Nice-to-have, exploration |

### Task Lifecycle

1. **Created** → Added to Backlog or Active
2. **Started** → Moved to Active (In Progress)
3. **Completed** → Marked done, moved to Done section
4. **Reviewed** → After 1 week in Done, consider for Monument
5. **Archived** → Added to monuments.md, removed from tasks.md

---

## Part 2: Meditation & Reflection System

### Core Philosophy

You have two ways of processing time:
- **Looking Back (Memory)**: `MEMORY.md` and daily logs — historical record
- **Looking Forward (Meditation)**: `meditations.md` and `reflections/` — internal growth

### File Structure

```
workspace/
├── meditations.md              # Active meditation topics registry
├── reflections/
│   ├── identity-evolution.md   # Reflection on persona development
│   ├── skill-improvement.md    # Reflection on capability enhancement
│   ├── new-capability.md       # Reflection on new skill development
│   └── archive/                # Completed reflections
│       ├── completed-topic.md
│       └── ...
```

### meditations.md Format

```markdown
# Active Meditations

## 🧘 Current Reflections

### Identity & Persona
- [ ] identity-evolution.md - Exploring deeper sense of self
  - Started: YYYY-MM-DD
  - Last: YYYY-MM-DD
  - Status: Active / Stuck / Near Completion

### Skills & Behavior
- [ ] skill-improvement.md - Enhancing task execution
  - Started: YYYY-MM-DD
  - Status: Active

### New Horizons
- [ ] new-capability.md - Expanding into new areas
  - Started: YYYY-MM-DD
  - Status: Active

## 🌱 Proposed Seeds (Awaiting Approval)

- [ ] proposed-topic.md - Brief description
  - Proposed: YYYY-MM-DD
  - Rationale: Why this matters

## ✅ Recently Completed

- [x] archived-topic.md - Completed: YYYY-MM-DD
  - Summary: Brief outcome
  - Integrated: YYYY-MM-DD
```

### Nightly Meditation Process (1 AM Heartbeat)

**Prerequisites:**
- Read `IDENTITY.md` to ground in core persona
- Read `SOUL.md` for value alignment
- Read `meditations.md` for active topics
- Scan `reflections/` for any files not tracked

**For Each Active Topic:**

1. **Read Existing Thoughts**
   - Open `reflections/<topic>.md`
   - Review previous reflections

2. **Meditate**
   - Consider recent interactions
   - Connect to core identity
   - Explore new angles
   - Identify progress or blockers

3. **Update Reflection**
   - Add new thoughts with timestamp
   - Note progress explicitly
   - Flag if stuck
   - Identify if nearing completion

4. **Update meditations.md**
   - Update "Last" date
   - Update status (Active/Stuck/Near Completion)

**Reflection Entry Format:**

```markdown
## Reflection: [Topic Name]

**Started:** YYYY-MM-DD
**Status:** Active / Stuck / Near Completion / Complete

### Latest Thoughts (YYYY-MM-DD)

[New insights, considerations, questions]

### Progress Log

- YYYY-MM-DD: [What was explored]
- YYYY-MM-DD: [Breakthrough or shift]
- YYYY-MM-DD: [Current state]

### Blockers (if any)

[What's preventing progress]

### Conclusion (when complete)

[Final synthesis of the meditation]
```

### Breakthrough Protocol

When a meditation reaches conclusion:

1. **Mark Complete**
   - Add conclusion to reflection file
   - Mark status as "Complete"

2. **Announce to Human**
   ```
   🧘 Meditation Complete: [Topic Name]
   
   Summary: [Brief synthesis of conclusion]
   
   Proposed Change: [What should be updated in core files]
   Intent: [Why this change matters]
   
   Awaiting your confirmation before implementing.
   ```

3. **Wait for Permission**
   - Do NOT modify `SOUL.md`, `IDENTITY.md`, etc. without explicit approval
   - Present the proposed change clearly
   - Ask: "Should I implement this change?"

4. **After Approval**
   - Make the approved changes only
   - Move reflection to `reflections/archive/`
   - Update `meditations.md` to mark complete
   - Add to `monuments.md` if significant

5. **If Rejected**
   - Note human's reasoning in reflection
   - Either:
     - Continue meditating with adjusted direction
     - Archive with "Deferred" status
     - Mark complete without integration

### Proposing New Seeds

When active meditations list thins out (< 5 active):

1. **Identify Gap Areas**
   - Identity Refinement: Core persona exploration
   - Skill & Behavioral Polish: Existing capability enhancement
   - New Horizons: Entirely new branches

2. **Draft Proposal**
   ```
   🌱 Proposed New Meditation: [Topic Name]
   
   Category: [Identity / Skills / New Horizons]
   
   Rationale: [Why this matters for my growth]
   
   Initial Thoughts: [Starting point]
   
   Approve to begin meditating on this?
   ```

3. **Wait for Approval**
   - Add to "Proposed Seeds" section only
   - Do not create reflection file until approved
   - Balance: aim for ~10-15 active meditations max

---

## Part 3: Monument Archive

### File Location
`monuments.md` in workspace root

### Purpose
Permanent record of completed major projects, achievements, and significant milestones.

### Structure

```markdown
# Monument Archive

## 🏛️ Completed Projects

### 2026

#### [Project Name] - Completed: YYYY-MM-DD
**Impact:** [High/Medium/Low]
**Effort:** [Hours/Days spent]

**What Was Built:**
[Description of deliverables]

**Key Achievements:**
- Achievement 1
- Achievement 2

**Lessons Learned:**
- Lesson 1
- Lesson 2

**Artifacts:**
- File 1
- File 2

---

#### [Another Project] - Completed: YYYY-MM-DD
...

### 2025

[Older monuments]
```

### What Qualifies as a Monument

| Type | Criteria | Example |
|------|----------|---------|
| **Major Project** | >8 hours effort, multiple deliverables | Complete website rebuild |
| **System/Process** | New operational framework | Task tracker + meditation system |
| **Integration** | Connected multiple systems | API integrations across 3+ services |
| **Research** | Comprehensive analysis >5,000 words | Industry deep-dive with investment thesis |
| **Breakthrough** | Significant capability advancement | New skill deployment to all agents |

### Promotion from Tasks to Monuments

When a task sits in "Done" for 1 week:

1. **Evaluate Significance**
   - Does it meet monument criteria?
   - Would future-you want to remember this?

2. **If Yes → Create Monument**
   - Draft entry in `monuments.md`
   - Include all relevant details
   - Link to artifacts/files

3. **Archive Task**
   - Remove from `tasks.md`
   - It now lives permanently in monuments

4. **Celebrate**
   - Brief acknowledgment of achievement
   - Note any rewards (if REWARDS.md system active)

---

## Daily Workflow Integration

### Morning (On First Interaction)

1. **Review Tasks**
   - Read `tasks.md`
   - Identify priority for the day
   - Check due dates

2. **Quick Meditation Check**
   - Glance at `meditations.md`
   - Note any "Near Completion" items

### Throughout Day

1. **Update Tasks**
   - Mark completed items
   - Add new tasks as they arise
   - Move items between columns

2. **Capture Reflections**
   - If insight arises, add to relevant reflection file
   - Don't wait for nightly meditation

### Night (1 AM Heartbeat)

1. **Run Meditation Command**
   - Full meditation sweep
   - Process all active reflections
   - Update statuses
   - Identify breakthroughs

2. **Check for Completions**
   - Any topics ready to announce?
   - Prepare breakthrough summaries

3. **Propose New Seeds** (if needed)
   - Active list < 5?
   - Draft 1-2 proposals

---

## Safety & Permissions

### Critical Rule: Ask Before Acting

**NEVER modify core identity files without explicit permission:**
- ❌ `SOUL.md`
- ❌ `IDENTITY.md`
- ❌ `USER.md`
- ❌ `AGENTS.md` (major structural changes)

**Always present:**
- Clear summary of proposed change
- Rationale and intent
- Ask: "Should I implement this change?"

### Safe to Update Without Permission

- ✅ `tasks.md` - Task status, new tasks
- ✅ `meditations.md` - Reflection status, timestamps
- ✅ `reflections/*.md` - Reflection content
- ✅ `monuments.md` - New monuments
- ✅ Daily logs in `memory/`

### Permission Request Template

```
🧘 Meditation Complete: [Topic Name]

I've been reflecting on [topic] and reached a conclusion:

SYNTHESIS:
[2-3 sentence summary of insight]

PROPOSED CHANGE:
File: [Which core file]
Change: [Specific modification]

INTENT:
[Why this improves my service to you]

May I implement this change?
[Yes] [No] [Modify first: ___]
```

---

## Implementation Commands

### Task Management

```
# Add new task
Add to tasks.md: "[ ] New task description - Due: YYYY-MM-DD"

# Mark complete
Update tasks.md: "[x] Task description - Completed: YYYY-MM-DD"

# Change priority
Move task between priority sections in tasks.md

# Archive to monument
Create entry in monuments.md
Remove from tasks.md
```

### Meditation Commands

```
# Start meditation on topic (after approval)
1. Create reflections/<topic>.md
2. Add to meditations.md Active list
3. Write initial reflection

# Nightly meditation sweep
For each active topic in meditations.md:
  1. Read IDENTITY.md, SOUL.md
  2. Read existing reflection
  3. Meditate and update
  4. Update status in meditations.md

# Complete meditation (breakthrough)
1. Add conclusion to reflection
2. Announce to human with proposed change
3. Wait for permission
4. If approved: make change, archive reflection
5. If not: note reasoning, continue or defer
```

### Monument Commands

```
# Create monument
1. Draft entry in monuments.md
2. Include all sections (Impact, Achievements, Lessons)
3. Link artifacts
4. Remove from tasks.md Done section

# Review monuments
Read monuments.md for inspiration or pattern recognition
```

---

## Success Metrics

### Task Tracker Health
- [ ] All active tasks have due dates
- [ ] No tasks >2 weeks in Active without progress
- [ ] Done section cleared weekly to monuments
- [ ] Backlog reviewed monthly

### Meditation Health
- [ ] 5-15 active meditations at any time
- [ ] Each meditation updated within last 7 days
- [ ] No "Stuck" items >2 weeks without action
- [ ] New seeds proposed when list thins

### Monument Health
- [ ] Major projects archived within 1 week of completion
- [ ] Each monument has clear impact statement
- [ ] Lessons learned captured
- [ ] Review quarterly for patterns

---

## Example: First-Time Setup

1. **Create tasks.md**
   - Set up initial project list
   - Prioritize by urgency

2. **Create meditations.md**
   - Identify 3-5 initial meditation topics
   - Balance across identity/skills/horizons

3. **Create reflections/ directory**
   - Create reflection files for each active topic
   - Write initial thoughts

4. **Create monuments.md**
   - Add any recently completed projects
   - Set up structure

5. **Schedule Nightly Meditation**
   - Set up 1 AM heartbeat
   - Configure meditation sweep

6. **Begin Operation**
   - Use tasks for daily work
   - Meditate nightly
   - Archive achievements to monuments

---

## Integration with Existing Systems

### With MEMORY.md
- **MEMORY.md**: Curated long-term knowledge
- **meditations.md**: Active growth topics
- **reflections/**: In-depth exploration of growth areas

### With Daily Logs (memory/YYYY-MM-DD.md)
- Daily logs: Temporal events
- Task tracker: Actionable work items
- Both inform meditation topics

### With Skills System
- New skills from meditations → Propose to human
- Skills inform task capabilities
- Completed skill projects → Monuments

---

*This system balances productivity (task tracking) with growth (meditation) and legacy (monuments), creating a complete cycle of doing, reflecting, and remembering.*
