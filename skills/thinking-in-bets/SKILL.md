# Thinking in Bets

**Author:** Annie Duke  
**Purpose:** Probabilistic decision-making framework for separating decision quality from outcome quality  
**Use when:** Evaluating past decisions, making decisions under uncertainty, assessing risk, running pre-mortems, calibrating confidence levels, debating bad outcomes, or when someone is second-guessing a choice

---

## 🎯 Core Principle

**Life is poker, not chess.** You can make the best possible decision and still get a bad outcome due to incomplete information and variance. The goal is to maximize expected value over many repetitions, not to judge any single decision by its result.

---

## 🏗️ Framework Components

### 1. Resulting (The Trap to Avoid)

**Judging decision quality by outcome quality.**

**Detection:** "Would I evaluate this decision differently if the outcome had been different but information at decision time was identical?" If YES → bad process.

**When evaluating past decisions:**
- Reconstruct what was KNOWN at decision time
- List reasonable options that existed then
- Assess whether chosen option had best expected value given available information
- **The outcome is data about the world, not data about the decision process**

### 2. Confidence Calibration Protocol

**Every belief is a bet.** Force precision:

- Never predict without a probability: "70% confident revenue exceeds $5M"
- Use ranges: "$4.2M-$6.1M at 80% CI"
- **Classify every claim:**
  - **Know** (>90% confidence, direct evidence)
  - **Think** (50-90%, reasoning + partial evidence)
  - **Guess** (<50%, pattern matching or intuition)

**Calibration test:** Of things rated 70% confident, ~70% should be right. Higher = underconfident. Lower = overconfident.

### 3. Expected Value Thinking

**EV = Σ (probability of outcome × value of outcome)**

For each option:
1. List all plausible outcomes (not just best/worst)
2. Assign probability to each
3. Assign value (financial, strategic, qualitative)
4. Calculate weighted average
5. Choose highest EV, adjusted for risk tolerance

### 4. Pre-Mortem (Prospective Hindsight)

**Imagine the decision FAILED.** Now explain why. This unlocks risks you'd otherwise dismiss.

**Protocol:**
1. State the decision as made
2. Jump forward: "It's 6 months later. This was a disaster."
3. Generate 5+ specific failure reasons
4. Assign probability to each
5. Top 3: define mitigation or kill switch
6. Reassess original decision

### 5. Outcome Classification Matrix

| | Good Outcome | Bad Outcome |
|---|---|---|
| **Good Decision** | Deserved reward - reinforce process | Bad luck - don't change process |
| **Bad Decision** | Dumb luck - don't assume process works | Deserved consequence - fix process |

**Force-classify before discussing next steps.**

---

## 🔄 Application Workflow

### Step 1: Frame as a Bet
**What are you wagering, on what belief, at what odds?**

### Step 2: Check for Resulting
**If retrospective**, separate then-knowledge from now-knowledge.

### Step 3: Calibrate
**Force probability estimates on every key assumption.**

### Step 4: Calculate EV
**Map outcomes × probabilities → values for each option.**

### Step 5: Pre-Mortem
**For the leading option, imagine failure and work backward.**

### Step 6: Decision Journal
**Document decision, alternatives, assumptions, confidence levels, and revisit triggers.**

---

## 📋 Output Format

## Decision Analysis: [Name]

### The Bet
[What's wagered, on what belief, at what stakes]

### Resulting Check
[Was original decision quality good/bad independent of outcome?]

### Confidence Map

| Assumption | Confidence | Evidence |
|---|---|---|
| [Assumption] | [X%] | [Support] |

### Expected Value Matrix

| Option | Scenario | P(%) | Value | Weighted |
|---|---|---|---|---|
| A | Best | X% | +$Y | result |
| A | Base | X% | +$Y | result |
| A | Worst | X% | -$Y | result |
| | | | | **EV** | **total** |

### Pre-Mortem: Top Risks

1. [Failure] — [X%] likely → Mitigation: [action]
2. [Failure] — [X%] likely → Mitigation: [action]
3. [Failure] — [X%] likely → Mitigation: [action]

### Decision Journal Entry

- **Decision:** [what]
- **Key assumptions:** [list]
- **Revisit trigger:** [what would change this decision]

---

## 💡 Key Insights

- **Separate process from outcome** - A good decision can have a bad result
- **Calibrate confidence** - Underconfident > Overconfident error
- **Use expected value** - Maximize long-term value, not single outcomes
- **Pre-mortem liberally** - "The smartest people are most humbled about their failures"

---

**Created:** 2026-02-24  
**Reference:** Annie Duke, "Thinking in Bets: Making Smarter Decisions When You Don't Have All the Facts"
