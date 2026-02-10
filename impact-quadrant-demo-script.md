# Impact Quadrant Interactive Demo Script
## AI Agents Working with Netsuite

**Version:** 1.0  
**Date:** February 10, 2026  
**Target Audience:** CFOs, VP Finance, CEOs at growth-stage companies  
**Demo Length:** 5-7 minutes  
**Format:** Interactive web demo (embedded in React app)

---

## Demo Overview

### Demo Goal
Show prospects how Impact Quadrant's AI agents transform Netsuite from a system of record into a strategic command center—without replacing anything.

### Emotional Journey
1. **Empathy:** "We know your pain" (Problem acknowledgment)
2. **Curiosity:** "What if there was a better way?" (Solution tease)
3. **Aha:** "This actually solves my problem" (Capability demonstration)
4. **Aspiration:** "I could get my weekends back" (Outcome visualization)
5. **Action:** "I need to learn more" (CTA)

### Demo Structure
- **Intro:** 30 seconds
- **Scenario 1 (Reconciler):** 90 seconds
- **Transition:** 15 seconds
- **Scenario 2 (Reporter):** 90 seconds
- **Transition:** 15 seconds
- **Scenario 3 (Forecaster):** 90 seconds
- **Closing:** 30 seconds

---

## Demo Environment Setup

### Technical Requirements
```
Sandbox Netsuite Account:
- Company: "DemoCo SaaS" (fictional $30M ARR company)
- Entities: 3 (US, UK, Canada)
- Currency: USD, GBP, CAD
- Chart of Accounts: Standard SaaS COA
- Historical Data: 18 months of transactions

Data Population:
- 5,000+ GL transactions
- 500 invoices (AR/AP)
- 200 expense reports
- 3 months of bank transactions
- Sample board deck template
```

### Sample Data Scenarios
```
Reconciliation Challenge:
- 4,500 auto-matchable transactions
- 500 exceptions with various patterns:
  * 200 timing differences
  * 150 FX rate variances
  * 100 missing receipts
  * 30 true anomalies
  * 20 duplicates

Reporting Scenario:
- Board meeting in 48 hours
- CEO asks for custom analysis
- Multi-entity consolidation needed
- Variance analysis required

Forecasting Scenario:
- Current runway: 14 months
- Considering hiring 10 people
- Evaluating price increase
- Planning fundraising timeline
```

---

## Full Demo Script

### INTRO (0:00 - 0:30)

**[Visual: Clean, modern dashboard with Impact Quadrant logo]**

**NARRATOR (Warm, conversational):**
"If you're watching this, you're probably using Netsuite—and you're probably frustrated. Not because Netsuite is bad. It's actually great at what it does: being a system of record.

But here's the thing: Netsuite was built for the 1990s. It tells you what happened last month. You need to know what's happening next week. It forces you into rigid workflows. Your business moves faster than that.

What if you could keep Netsuite—keep all that data, all that history—but add a layer of intelligence on top? That's what Impact Quadrant does.

Let me show you."

**[Visual: Transition to Netsuite interface with 5 agent orbs appearing]**

---

### SCENARIO 1: RECONCILER - Month-End Close (0:30 - 2:00)

**[Visual: Netsuite dashboard showing chaos—multiple tabs open, error messages, long transaction list]**

**NARRATOR:**
"It's month-end. Your team has been at this for 8 days. Five thousand transactions to reconcile across your bank, Netsuite, Stripe, and corporate cards."

**[Visual: Show frustrated user scrolling through endless transaction list]**

**NARRATOR:**
"This is where Reconciler—your error-hunting agent—comes in."

**[Visual: Reconciler agent orb pulses and activates]**

**[Demo Action: User clicks "Run Reconciliation" button]**

**[Visual: Animation shows transactions flowing through matching engine]**

**RECONCILER (On-screen text, methodical voice):**
"Analyzing 5,034 transactions across 4 data sources..."

**[Visual: Progress bar shows matching in real-time]**

**RECONCILER:**
"Matched 4,782 transactions with 95.4% confidence."

**[Visual: Matched transactions turn green and move to "Completed" column]**

**RECONCILER:**
"252 exceptions identified. Ranking by materiality..."

**[Visual: Exception list appears, sorted by dollar amount]**

**NARRATOR:**
"Look at this. Instead of manually reviewing 5,000 transactions, your team reviews 252 exceptions—already sorted by importance."

**[Demo Action: User clicks top exception - $47,000 wire transfer]**

**RECONCILER:**
"Wire transfer of $47,000 to GlobalTech Solutions on October 15. No matching invoice found. However, I located a purchase order for $47,500 dated October 12. The $500 difference likely represents an early payment discount. Recommend confirming with AP team."

**[Visual: Side-by-side comparison showing PO and wire details]**

**NARRATOR:**
"Reconciler doesn't just flag problems—it suggests solutions. With context. Your AP person reviews this in 30 seconds instead of 30 minutes of detective work."

**[Visual: Time comparison - 8 days → 1 day]**

**NARRATOR:**
"Month-end just went from 8 days to 1 day. Your team just got a week back. Every month."

---

### TRANSITION 1 (2:00 - 2:15)

**[Visual: Smooth transition to new scenario]**

**NARRATOR:**
"Okay, so Reconciler handles the past. But what about the present? What happens when your CEO—or your board—asks a question you can't answer quickly?"

---

### SCENARIO 2: REPORTER - Board-Ready Insights (2:15 - 3:45)

**[Visual: Board meeting scene—calendar shows "Board Meeting - Tomorrow"]**

**NARRATOR:**
"It's Wednesday. Board meeting is Thursday. Your CEO just texted: 'Can you show Q3 burn by entity and compare it to our Series B plan?'

Old way? You're pulling data from 12 sources, building pivot tables, and working until midnight."

**[Visual: Show traditional process—Excel crashing, multiple browser tabs, frustrated user]**

**NARRATOR:**
"New way? You ask Reporter."

**[Visual: Reporter agent orb activates]**

**[Demo Action: User types natural language query]**

**USER INPUT (on screen):**
"Show me Q3 burn by entity compared to plan"

**[Visual: Reporter processes request—thinking animation]**

**REPORTER (On-screen text, clear voice):**
"Analyzing Q3 data across 3 entities... comparing to Series B operating plan... generating visualization..."

**[Visual: Dashboard appears instantly]**

**REPORTER:**
"Q3 total burn: $2.67M vs. plan of $2.8M. Under budget by $130K.

By entity:
• US: $1.89M (7% under plan)
• UK: $480K (3% over plan - FX impact)
• Canada: $300K (on plan)

Key variances: UK FX rates, delayed hiring in Engineering."

**[Visual: Beautiful chart showing burn by entity with plan comparison]**

**NARRATOR:**
"Thirty seconds. From question to insight. With context. With visualizations. Board-ready."

**[Demo Action: User clicks "Export to Board Deck"]**

**[Visual: Slide auto-generates with proper formatting]**

**REPORTER:**
"Added to your board deck with executive summary and talking points."

**NARRATOR:**
"And it's not just about speed. It's about depth. Reporter can answer follow-ups instantly."

**[Demo Action: User types follow-up]**

**USER INPUT:**
"What's driving the UK variance?"

**REPORTER:**
"UK variance is primarily FX-related. GBP weakened 8% vs. USD in Q3. Underlying spend was actually £375K vs. plan of £380K. Recommend: 1) Review FX hedging strategy, 2) Consider billing UK customers in USD."

**[Visual: Drill-down chart showing FX impact vs. operational variance]**

**NARRATOR:**
"That's not just data. That's strategic insight. And you got it in a conversation, not a week of analysis."

---

### TRANSITION 2 (3:45 - 4:00)

**[Visual: Transition]**

**NARRATOR:**
"So Reconciler handles the past. Reporter handles the present. But what about the future? What happens when you need to make a decision that doesn't have a playbook?"

---

### SCENARIO 3: FORECASTER - Strategic Decision Support (4:00 - 5:30)

**[Visual: CEO's question on screen: "Should we hire 10 engineers now or wait until after Series B?"]**

**NARRATOR:**
"Your CEO wants to accelerate hiring. 10 engineers. That's $2 million in additional burn. But you just started fundraising. Do you hire now and extend runway? Wait and risk losing candidates?"

**[Visual: Show Excel spreadsheet labeled "Forecast v23_FINAL_ACTUAL.xlsx" - outdated]**

**NARRATOR:**
"Static spreadsheets can't model this. You need scenarios. You need to see around corners."

**[Visual: Forecaster agent orb activates]**

**NARRATOR:**
"Meet Forecaster."

**[Demo Action: User opens Forecaster interface]**

**[Visual: Current cash position dashboard appears]**

**FORECASTER (On-screen text, analytical voice):**
"Current runway: 14.2 months with 70% confidence interval. Current burn: $890K/month."

**[Demo Action: User creates scenario]**

**USER INPUT:**
"Model hiring 10 engineers at $180K each, starting next month"

**[Visual: Forecaster runs simulation]**

**FORECASTER:**
"Scenario: Hire 10 engineers
• Monthly burn increase: $180K → $1.07M/month
• Runway impact: 14.2 months → 11.8 months
• Confidence: 65%

Risk: If Series B takes longer than 6 months, runway becomes critical."

**[Visual: Cash projection chart showing runway scenarios]**

**NARRATOR:**
"That's the hire-now scenario. But what if you wait?"

**[Demo Action: User creates alternative scenario]**

**USER INPUT:**
"Compare to hiring 5 now, 5 after Series B close"

**[Visual: Side-by-side scenario comparison]**

**FORECASTER:**
"Comparison:

Option A - Hire 10 now:
• Runway: 11.8 months
• Risk: High (short runway if fundraising delays)
• Benefit: Faster product velocity

Option B - Hire 5 now, 5 post-close:
• Runway: 16.4 months
• Risk: Lower
• Consideration: Candidates may accept other offers

Option C - Wait until post-close:
• Runway: 19.2 months
• Risk: Lowest
• Consideration: 6-month hiring delay"

**[Visual: Scenario comparison matrix with recommendation highlighted]**

**NARRATOR:**
"Three scenarios. Quantified risks. Clear trade-offs. And notice the confidence intervals—Forecaster isn't pretending to have a crystal ball. It's showing you probabilities."

**[Demo Action: User clicks "What if fundraising takes 9 months?"]**

**FORECASTER:**
"Sensitivity analysis: If Series B closes in 9 months vs. 6 months:
• Option A runway becomes 8.2 months (critical)
• Option B runway becomes 13.1 months (manageable)
• Option C runway remains 19.2 months (safe)

Recommendation: Option B provides optimal risk-adjusted outcome."

**NARRATOR:**
"This isn't just forecasting. This is strategic decision support. You're not guessing anymore—you're making informed choices with full visibility into the implications."

---

### CLOSING (5:30 - 6:00)

**[Visual: All 5 agents shown together with data flowing between them]**

**NARRATOR:**
"So that's Reconciler for the past. Reporter for the present. Forecaster for the future. And we haven't even shown you Watchdog for compliance or Advisor for strategic analysis.

But here's what matters: These aren't separate tools. They're a team. They share data. They learn from each other. And they work within your existing Netsuite—no migration, no disruption, no rip-and-replace."

**[Visual: Before/After comparison]**

**NARRATOR:**
"Month-end: 15 days to 3 days. Board prep: A week to 30 seconds. Strategic decisions: Gut feel to data-driven."

**[Visual: CTA appears]**

**NARRATOR:**
"This is what finance looks like when AI does the heavy lifting and humans do the high-value thinking. 

Ready to meet your Digital Finance Team?"

**[CTA Buttons: "Schedule Your Demo" / "Calculate Your ROI"]**

---

## Interactive Demo Elements

### 1. Try-It-Yourself Mode

**For Each Scenario, Include:**
- **Guided Mode:** Script plays automatically with narration
- **Interactive Mode:** User controls the demo
- **Sandbox Mode:** User can enter custom queries

### 2. Data Explorer

**Allow Users To:**
- Toggle between entities
- Adjust time periods
- Change assumptions (e.g., "What if burn is 20% higher?")
- Export sample data

### 3. Agent Selector

**Let Users Choose Which Agent to Explore:**
```
[Reconciler] [Forecaster] [Reporter] [Watchdog] [Advisor]

Click an agent to see their capabilities in action
```

### 4. ROI Calculator Integration

**Embedded in Demo:**
- "Want to see your potential savings?"
- Input current close time, team size
- See projected savings in real-time
- CTA: "Get your custom assessment"

---

## Technical Implementation Notes

### Frontend Components Needed

```typescript
// DemoContainer.tsx - Main demo wrapper
interface DemoContainerProps {
  scenario: 'reconciler' | 'reporter' | 'forecaster';
  mode: 'guided' | 'interactive' | 'sandbox';
}

// NetsuiteMock.tsx - Simulated Netsuite interface
// Shows realistic Netsuite UI with sample data

// AgentOrb.tsx - Animated agent activation
interface AgentOrbProps {
  agent: AgentType;
  isActive: boolean;
  onActivate: () => void;
}

// TypewriterText.tsx - Narration display
// Simulates real-time text generation

// ScenarioPlayer.tsx - Controls demo flow
// Handles transitions, pauses, replays
```

### Animation Specifications

**Agent Activation:**
```
Duration: 0.5s
Effect: Scale from 0.8 to 1.0 + glow pulse
Easing: cubic-bezier(0.4, 0, 0.2, 1)
```

**Data Flow:**
```
Duration: 1.5s
Effect: Particles flowing from source to destination
Color: Agent-specific (green for Reconciler, blue for Forecaster, etc.)
```

**Transition Between Scenarios:**
```
Duration: 0.8s
Effect: Crossfade with slight blur
Easing: ease-in-out
```

### Responsive Considerations

**Desktop (Primary):**
- Full interactive experience
- Side-by-side comparisons
- Hover effects and tooltips

**Tablet:**
- Stacked layout
- Touch-friendly controls
- Swipe gestures for scenario navigation

**Mobile:**
- Simplified single-column layout
- Tap-to-advance for guided mode
- Collapsible agent details

---

## Demo Variations

### 1. Executive Summary (2 Minutes)
**For:** Time-constrained executives  
**Content:** Problem → Reconciler highlight → Reporter highlight → CTA

### 2. Deep Dive (10 Minutes)
**For:** Interested prospects  
**Content:** Full script + interactive sandbox + all 5 agents

### 3. Industry-Specific Versions

**SaaS Demo:**
- Focus on MRR, churn, CAC metrics
- Include subscription billing scenarios

**E-commerce Demo:**
- Multi-channel reconciliation (Shopify, Amazon, wholesale)
- Inventory forecasting

**Marketplace Demo:**
- Multi-party transactions
- Commission calculations
- Escrow reconciliation

---

## Success Metrics for Demo

| Metric | Target | Measurement |
|--------|--------|-------------|
| Demo Completion Rate | >60% | Analytics tracking |
| CTA Click Rate | >15% | Click-through tracking |
| Time on Demo | >4 minutes | Engagement analytics |
| Replay Rate | >20% | Users watching 2+ times |
| Conversion to Meeting | >10% | CRM integration |

---

## Accessibility Requirements

- **Captions:** All narration has closed captions
- **Transcript:** Full text transcript available
- **Keyboard Navigation:** Tab through all interactive elements
- **Screen Reader:** ARIA labels for all visual elements
- **Reduced Motion:** Respect prefers-reduced-motion setting
- **Color Contrast:** WCAG 2.1 AA compliance

---

## Next Steps After Demo

### Immediate CTAs
1. **Schedule Assessment** - Primary CTA
2. **Calculate ROI** - Secondary CTA
3. **Download Case Study** - Tertiary CTA
4. **Share with Team** - Social sharing

### Follow-Up Sequence
```
Day 0: Demo completion trigger
Day 1: "Thanks for watching" + ROI calculator
Day 3: Industry-specific case study
Day 7: "Questions?" offer consultation
Day 14: Final nudge with social proof
```

---

*This demo script provides a complete blueprint for creating an interactive, compelling demonstration of Impact Quadrant's AI agents. The goal is to move prospects from skepticism to enthusiasm in under 7 minutes.*
