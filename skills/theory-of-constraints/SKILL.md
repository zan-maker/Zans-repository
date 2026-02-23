# Theory of Constraints

**Author:** Eliyahu Goldratt  
**Purpose:** From "The Goal" — every system has exactly one constraint that limits total throughput. Find it, exploit it, subordinate everything else to it, then elevate it.  
**Use when:** Users mention bottleneck, constraint, throughput, cycle time, process optimization, capacity planning, workflow stuck, slow process, or when any system is producing less than expected

---

## 🎯 Core Principle

**A chain is only as strong as its weakest link.** Improving anything OTHER than the constraint is an illusion of progress.

---

## 🔧 The Five Focusing Steps

### Step 1: IDENTIFY The Constraint

**Look for:**
- Inventory accumulation (queue before this step)
- Starvation downstream (next step idle)
- Utilization at 100% while others run at 60-80%
- **Step everyone complains about:** Where does work wait longest?

**Questions:**
- Where does work wait longest?
- What step, if 20% faster, would increase total output?
- Where are the workarounds?

### Step 2: EXPLOIT The Constraint

**Maximize throughput WITHOUT spending money:**

- Eliminate waste at the constraint (downtime, rework, context-switching)
- **Never let the constraint run idle** (buffer work ahead of it)
- Only quality work reaches the constraint (inspect before, not after)
- **Prioritize highest-value work at the constraint**

**Key test:** "Is the constraint doing anything a non-constraint resource could do?"

### Step 3: SUBORDINATE Everything Else

**Every other step operates at the pace of the constraint.** This means deliberately slowing non-constraint steps. Overproduction before the constraint creates excess WIP and confusion without increasing throughput.

**Drum-Buffer-Rope:**
- **Drum** = constraint sets pace
- **Buffer** = time buffer protects constraint from upstream variability
- **Rope** = signal from constraint to start, limiting new work release

### Step 4: ELEVATE The Constraint

**Now invest:** add capacity, outsource, automate, redesign. **Only AFTER Steps 2-3 — most organizations skip here first, overspending.**

### Step 5: REPEAT

**Once elevated, a NEW constraint emerges.** Go to Step 1.

**Danger:** Policies built around old constraint become new constraint.

---

## 📊 Throughput Accounting

### Definition

| Metric | Priority | Decision Rule |
|--------|---------|---|
| **Throughput (T)** | 1st | Increase T while holding I and OE constant = good |
| **Inventory (I)** | 2nd | Money tied up in WIP |
| **Money tied up (WIP)** | 3rd | Second |
| **Operating Expense (OE)** | 4th | Money to turn I into T |

**Decision rule:** Increase T while holding I and OE constant = good. Decrease I or OE without decreasing T = bad. Always prioritize T.

---

## 📋 Output Format

## Constraint Analysis: [System Name]

### Process Map

[Step 1] ? [Step 2] ? [Step 3] * ? [Step 4] ? [Step 5] ?
(* = constraint)

### Constraint Identification

- **What:** [constraint step]
- **Evidence:** [queue size, utilization, downstream starvation]
- **Current throughput:** [X units/period]
- **Theoretical max:** [Y units/period]

### Exploitation (No-cost)

1. [Action] — Throughput gain: [X%]
2. [Action] — Throughput gain: [X%]

### Subordination

- [Step] should pace to [constraint rate]
- New WIP limit: [number]

### Elevation (Investment Required)

- [Investment] — Cost: [$X] — Gain: [Y%] — ROI: [timeframe]

### Policy Constraints Detected

- [Artificial bottleneck from rules/approvals/metrics]

---

## 🎯 How to Use

**Start with bottleneck:** "I have too much WIP" → Apply Step 1

**Don't:** Start with adding capacity or automating. Follow the sequence.

**Remember:** "Subordination is uncomfortable but necessary for throughput."

---

## 💡 Key Insights

- **The constraint is ALWAYS one specific step**, not "the process"
- **Overproduction creates waste and confusion** without increasing throughput
- **Subordination must be active** — other steps wait for the drum signal
- **Policies become the new constraint** if not reviewed after elevation

---

## ⚠️ Common Mistakes

1. **Adding capacity before exploiting** — overspending on wrong problem
2. **Letting constraint run idle** — buffer work creates downstream backlog
3. **Quality at constraint, not after** — inspect before, not after
4. **Multiple constraints** — focus on primary, subordinate secondary
5. **Never-ending elevation** — once elevated, go back to Step 1

---

**Created:** 2026-02-24  
**Reference:** Eliyahu Goldratt, "The Goal: A Process of Ongoing Improvement"
