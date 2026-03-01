## Inspiration

There are over 4,000 pre-IPO companies globally, and most of them have the same problem: a one- or two-person finance team that loses a full day every month to variance analysis. The ritual is always the same — export actuals from the accounting platform, open the investor model in Excel, cross-reference line by line, flag what moved, figure out why, and write something the board will believe. It's mechanical, it's error-prone, and the person doing it is usually the only finance hire.

We've lived this. As a pre-IPO company preparing for an ASX listing, we know the pain firsthand. The insight was simple: **the math is deterministic, the interpretation is where AI adds value, and the delivery should happen where finance teams already communicate — messaging apps.**

We wanted to see if DigitalOcean Gradient could turn that monthly day into a Telegram conversation. Not a dashboard nobody checks. Not a batch report that arrives too late. A chat where the CFO types "why did gross margin drop?" and gets a governed, source-cited answer in under five seconds.

---

## What It Does

DeltaFin Chat is a Telegram bot backed by a DigitalOcean Gradient AI agent that performs **on-demand financial variance analysis** for pre-IPO companies.

Open Telegram. Ask a question. Get an answer with every number traced to its source:

- **"Why did gross margin drop?"** → The agent calls the variance engine function, retrieves the model assumption from the Knowledge Base, and narrates: *"Gross margin at 34.3% [Actuals] vs 40.0% [Model v2.3] — a 5.7pp shortfall flagged as material. Primary driver: 4% COGS increase consistent with lithium price movement."*

- **"What's our runway?"** → The runway calculator computes months remaining from the 3-month rolling burn, compares to model, and assigns a priority: *"16.4 months at $180K/month burn vs model's 28.0 months at $125K. Priority: HIGH."*

- **"Break down the revenue miss"** → The revenue decomposition function splits the variance into volume, price, and mix effects.

- **"Generate investor talking points"** → Full six-section brief: Cash & Runway, Revenue, Costs, Commodity Exposure, Regulatory, and Talking Points with anticipated board questions.

The architectural principle that governs everything: **Code for math. Model for meaning.** The LLM never calculates. All financial math runs in DigitalOcean Functions — deterministic Python returning structured JSON. The LLM interprets pre-computed results and generates governed narratives.

---

## How We Built It

### Architecture: 100% DigitalOcean

```
Telegram → Bot (App Platform) → Gradient AI Agent → [Knowledge Base | DO Functions] → Response
```

Every component runs on DigitalOcean. Zero external dependencies beyond Telegram's API.

**Gradient AI Agent** — The core intelligence. Created in the Gradient Console with comprehensive instructions following DO's best practices template (Identity → Objective → Expertise → Restrictions → Limitations). The agent uses Claude Sonnet 4.5 via Serverless Inference for narrative generation. Instructions enforce three hard rules: never fabricate data, never perform arithmetic, always cite sources.

**Knowledge Base (RAG)** — The investor financial model (Excel) is preprocessed into structured markdown and indexed into a Gradient Knowledge Base. When the agent needs to answer "what did the model assume for FY25 gross margin?", it queries the KB and returns the exact figure with tab and row reference. Auto-indexing keeps it current when the model is re-uploaded.

**DO Functions (Serverless Math)** — Three functions handle all deterministic calculations, attached to the agent via Function Routing:

1. **`variance_engine`** — Compares every P&L and balance sheet line item between actuals and model. Flags material variances (>10%) and determines favorability. For cost accounts, lower is favorable; for income accounts, higher is favorable.

2. **`runway_calculator`** — Computes cash runway:

$$\text{Months Remaining} = \frac{\text{Cash}_t}{\text{Avg Burn}_{3\text{mo}}}$$

where the 3-month rolling average burn smooths out monthly volatility. The function compares to the model's projected runway and assigns a priority level (LOW → CRITICAL).

3. **`revenue_decomposition`** — Splits total revenue variance into volume, price, and mix effects using the standard decomposition:

$$\Delta\text{Rev} = \underbrace{(V_a - V_b) \times P_b}_{\text{Volume Effect}} + \underbrace{(P_a - P_b) \times V_b}_{\text{Price Effect}} + \underbrace{(V_a - V_b)(P_a - P_b)}_{\text{Mix Effect}}$$

Each component is returned in dollars and as a percentage of total variance, giving the CFO a precise attribution of what drove the revenue miss.

**Telegram Bot** — A lightweight Python relay (~200 lines) running on App Platform. It receives messages, forwards them to the Gradient agent endpoint via the OpenAI-compatible API, and returns the response. Supports `/brief`, `/runway`, and `/variances` shortcut commands.

**DO Spaces** — Versioned storage for uploaded financial models, preprocessed markdown for KB indexing, and an append-only audit trail of every query and response.

**Gradient Evaluations** — 20 test cases across three categories (correctness, safety, instruction adherence) validate that the agent returns accurate figures, refuses investment advice, and stays within scope.

### Gradient Feature Usage

| Feature | How Used |
|---------|----------|
| Gradient AI Agent | Core intelligence with governed instructions |
| Serverless Inference | Claude Sonnet 4.5 for narrative generation |
| Knowledge Base | RAG over the investor financial model |
| Function Routing | Connects 3 DO Functions for deterministic math |
| DO Functions | Variance engine, runway calculator, revenue decomposition |
| Evaluations | 20 test cases validating accuracy and safety |
| Spaces | Model storage, KB source documents, audit trail |
| App Platform | Telegram bot hosting |

---

## Challenges We Ran Into

### Financial Models Don't Chunk Well

Standard text splitters break Excel models mid-table, destroying context. A retrieval chunk that returns half a row of assumptions is worse than returning nothing. We built a preprocessor that converts each Excel tab into a self-contained markdown section with table formatting preserved. Each section is a complete, coherent unit the KB can retrieve meaningfully. This was the difference between the agent answering "the model assumes 18% growth" and "the model assumes" with no number.

### Keeping the LLM Honest About Numbers

The core risk in financial AI isn't getting the answer wrong — it's getting the answer *confidently* wrong. LLMs are notoriously unreliable at arithmetic, and a CFO who sends a hallucinated number to the board faces real consequences.

We enforce honesty at three layers:
1. **Agent instructions** explicitly state "never perform arithmetic" and "never fabricate data"
2. **DO Functions** handle all math and return structured JSON — the LLM never sees raw numbers to calculate
3. **Evaluation test cases** specifically check whether the agent invents figures not present in function output

The materiality threshold ($|\%\Delta| > 10\%$) is computed in the function, not by the LLM. The agent just reads the `is_material: true` flag and highlights it.

### Latency for Chat UX

Telegram users expect fast responses. Our first iteration took 8-12 seconds because every query triggered all three functions. We optimized by having the agent's Function Routing decide which functions to call based on intent — a runway question only calls `runway_calculator`, not the full variance engine. Model assumption questions route straight to the Knowledge Base without any function call. Most queries now return in 3-5 seconds.

### Multi-Format Financial Data

Every accounting platform exports differently. Syft CSVs use different column headers than Xero exports, which differ from QuickBooks. The variance engine function includes a normalization layer that maps common header variations ("Revenue", "Total Revenue", "Net Revenue", "Sales", "Income") to a standard chart of accounts. This is unglamorous plumbing, but without it the agent breaks on real-world data.

---

## Accomplishments We're Proud Of

- **Zero external dependencies** — every component runs on DigitalOcean products
- **No LLM-calculated numbers** — every financial figure traces to deterministic Python in DO Functions
- **Knowledge Base RAG** grounds every model assumption answer in the actual uploaded document
- **Telegram delivery** meets finance teams where they already work — no new app, no login, no dashboard
- **Agent instructions** follow DO's published best practices template with two fully worked examples
- **20-case evaluation suite** validates accuracy, safety, and instruction adherence

---

## What We Learned

**Gradient's agent platform is genuinely full-stack.** We originally planned to use external orchestration (Airia). Then we realized Agent Instructions + Knowledge Base + Function Routing + Evaluations covered everything we needed. The platform handles what we thought we'd have to build ourselves.

**Function Routing is the right pattern for regulated use cases.** The model decides *when* a calculation is needed, the function executes it deterministically, the model narrates the result. This separation of concerns — intent routing by LLM, computation by code, interpretation by LLM — is exactly what financial governance requires. The LLM is never in the loop on arithmetic.

**Knowledge Base auto-indexing changes the RAG workflow.** Upload to Spaces → KB stays current. No embedding pipeline. No vector DB operations. For a finance team that updates their model quarterly, this is the difference between "works once" and "works every time."

**Telegram as a financial interface is surprisingly natural.** CFOs already use messaging for quick questions to their team. Having the same interface for data questions removes all adoption friction. The `/brief` command that generates a full six-section investor brief from a single tap turned out to be the feature every tester asked about.

---

## What's Next

- **Multi-company support** — Parameterized Knowledge Bases per company for investment bank portfolio monitoring across 5-20 pre-IPO clients
- **File upload in Telegram** — Drop an Excel model in chat → auto-preprocesses → indexes to KB
- **Automated alerts** — Scheduled function runs that push to Telegram when uploaded actuals show material variances
- **Agent routing** — Add a second Gradient agent for regulatory monitoring (SEC filings, commodity regulations) and let the router dispatch
- **Expanded evaluations** — Monthly regression testing as instructions and functions evolve

---

## Built With

`digitalocean-gradient` `digitalocean-functions` `digitalocean-spaces` `digitalocean-app-platform` `python` `python-telegram-bot` `claude-sonnet` `rag`
