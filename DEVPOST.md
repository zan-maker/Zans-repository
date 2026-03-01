# DeltaFin AI: Automated Financial Variance Analysis for Pre-IPO Companies

**An AI-powered pipeline that extracts consolidated financial data, runs automated variance analysis against investor models, enriches with market and regulatory intelligence, and generates governance-audited investor briefs — built on Airia, Amazon Nova, and Amazon Bedrock.**

---

## Inspiration

Pre-IPO finance teams run on disconnected SaaS platforms — accounting in Xero, procurement in Precoro, reporting in Syft Analytics. Every month, someone manually exports reports, reconciles across entities, pulls commodity prices, compares actuals to the financial model investors underwrote, and stitches everything into a brief. It takes a full day.

The real pain isn't data extraction — it's **variance analysis**. Investors and boards don't just want numbers. They want to know: *are we tracking to the model we raised on?* Every monthly data point either builds or erodes confidence ahead of a listing.

We tried automating with APIs. Xero's OAuth was fragile. Precoro's coverage was limited. Syft had no meaningful programmatic access. The "modern data stack" approach — ETL pipelines, data warehouses, dbt, BI layers — was a multi-month infrastructure project for a lean finance team.

DeltaFin AI started from a simple question: **What if an AI agent could extract consolidated financials, compare them against the investor model, flag material variances, layer in market and regulatory context, and generate a narrative brief — all within an enterprise-governed platform that provides the audit trail a pre-IPO company needs?**

---

## What It Does

DeltaFin AI is a 7-stage financial intelligence pipeline orchestrated through Airia, with all AI stages powered by Amazon Nova Pro (`amazon.nova-pro-v1:0`) via Bedrock.

### Stage 0 — Financial Model Access (S3 + Lambda)
The investor financial model — the budget investors underwrote — is stored as a versioned, KMS-encrypted Excel file in S3 under a consistent key scheme (`s3://finmodels/{entity}/{model_type}/{yyyymmdd}/model.xlsx`). A Python Lambda function (`extract_model_financials`) uses `openpyxl` and `pandas` to read specific tabs and cell ranges, returning a normalized JSON of P&L, balance sheet, cash flow, and key assumptions. The agent never opens the workbook directly — it calls this tool, keeping financial logic in code and analysis in the model.

A parallel Lambda (`extract_syft_financials`) reads exported Syft CSVs from a separate S3 prefix and normalizes them to the same chart of accounts schema. Both functions return compact, aligned JSON objects so Nova Pro focuses purely on reasoning and explanation, not data wrangling.

### Stage 1 — Data Extraction (Amazon Nova Act)
A browser automation agent logs into **Syft Analytics** — the BI consolidation layer that aggregates data across legal entities — and exports consolidated P&L, balance sheet, and cash flow as CSVs to S3. By targeting Syft instead of extracting from each upstream system separately, we collapse multiple extraction agents into one.

### Stage 2A — Market Intelligence (AlphaVantage MCP)
Through Airia's governed MCP Gateway, the pipeline pulls live commodity prices (copper, aluminum, nickel, lithium), FX rates (USD/SGD, USD/AUD), macro indicators (Fed Funds Rate, CPI, Treasury yields), and equity data for listed peer companies. Nova Pro is configured at temperature 0.3–0.4 for enrichment interpretation, balancing analytical flexibility with factual grounding.

### Stage 2B — Regulatory Intelligence (Regulations.Gov MCP)
A parallel MCP call queries active federal rulemaking, proposed rules, and public comment periods filtered to material agencies (EPA, DOE, DOD). For industries like battery recycling and critical minerals, this surfaces regulatory developments that directly impact financial projections and risk disclosures. Nova Micro pre-classifies relevance before material filings pass to Nova Pro for narrative integration.

### Stage 3 — Variance Engine (Python)
The core quantitative analysis runs deterministically in Python — never in the LLM:

- **Normalize** Syft actuals and model budget to aligned chart of accounts
- **Calculate** dollar and percentage variances, flagging items exceeding materiality:

$$\Delta_i = A_i - B_i, \quad \%\Delta_i = \frac{A_i - B_i}{|B_i|} \times 100$$

- **Decompose** revenue variance into volume, price, and mix:

$$\Delta_{\text{Rev}} = \underbrace{(V_a - V_b) \times P_b}_{\text{Volume}} + \underbrace{(P_a - P_b) \times V_b}_{\text{Price}} + \underbrace{(V_a - V_b)(P_a - P_b)}_{\text{Mix}}$$

- **Compute** updated runway using a 3-month rolling average burn rate:

$$\text{Months Remaining} = \frac{\text{Cash}_{t}}{\overline{\text{Burn}}_{3\text{mo}}}$$

### Stage 4 — Narrative Generation (Amazon Nova Pro)
All structured data — variance tables, commodity context, regulatory filings, peer benchmarks — feeds into Nova Pro (temperature 0.2 for narrative precision) within its 300K context window, generating a six-section monthly brief:

1. **Cash Position & Runway** — actual burn vs. modeled, updated months-of-runway
2. **Revenue & Collections** — actual vs. projected with volume/price/mix decomposition
3. **Cost Variance Analysis** — material variances flagged with root cause interpretation
4. **Commodity & Macro Exposure** — how price movements affect unit economics
5. **Regulatory Watch** — new or pending regulations that could impact projections or risk profile
6. **Investor Talking Points** — CEO-ready narrative plus "questions investors will ask"

### Stage 5 — Human Approval Gate
The brief pauses for CFO/CEO review before distribution. Investor-facing materials should never be fully autonomous. The governance gate logs reviewer identity, approval timestamp, and any modifications.

### Stage 6 — Delivery (Microsoft MCP)
Upon approval, Airia's MCP Gateway posts a summary to a Microsoft Teams channel (`#investor-updates`) and uploads the full brief to OneDrive (`/Board & Investor Syndicate/Monthly Briefs/`).

---

## How We Built It

### Model Selection

| Model | Stage | Temperature | Role |
|-------|-------|-------------|------|
| **Nova Pro** | 2A, 2B, 4, 6 | 0.2–0.4 | Enrichment interpretation, variance narrative, brief generation |
| **Nova Micro** | 2B (pre-filter) | 0.1 | Regulatory filing relevance classification |
| **Nova Act** | 1 | — | Syft browser extraction via atomic `act()` commands |

Core design principle: **all quantitative calculations happen in Python; Nova Pro only interprets and narrates.** The agent calls Lambda-backed tools (`extract_model_financials`, `extract_syft_financials`) that return aligned JSON, keeping financial logic in code and analysis in the model's 300K context window.

### Financial Model Access Pattern

The investor model is treated as a versioned artifact, not a live spreadsheet. On upload, a Lambda function reads specific tabs and cell ranges using `openpyxl`, extracts the core schedules (Income Statement, Balance Sheet, Cash Flow, Assumptions), and returns normalized JSON. The agent never "sees" the raw workbook. This means:

- Model versions are immutable and auditable (S3 versioning + KMS encryption)
- Chart-of-accounts mapping lives in the Lambda, not in prompts
- The same tool serves multiple entities via a `company_id` parameter
- Each variance report stamps the model version it ran against

### Why Airia

1. **Audit trail.** Every model call, MCP request, and data input is logged — critical when listing brokers ask "how was this brief generated?"
2. **Human-in-the-loop as a workflow primitive.** The approval gate is a native step with full audit logging, not a bolt-on.
3. **Governed MCP Gateway.** AlphaVantage, Regulations.Gov, Microsoft Teams, and OneDrive all flow through a single secure gateway with credential management, access controls, and complete audit logging of every tool call.

### Cost Economics

| Component | Cost per Run |
|-----------|-------------|
| Nova Pro (Stages 2A/2B/4/6) | \$0.15 – \$0.50 |
| AlphaVantage API calls | \$0.02 – \$0.05 |
| Regulations.Gov API | Free |
| Lambda executions | \$0.01 |
| S3 storage + retrieval | \$0.05 |
| Microsoft Graph API | Free (M365 included) |
| **Total per monthly run** | **\$0.23 – \$0.61** |

At under \$1 per company per month, the pipeline scales to 50 companies for less than \$50/month.

---

## Challenges We Faced

**The consolidation problem.** Our original design called for parallel Nova Act agents extracting from Xero, Precoro, and Syft simultaneously. We realized Syft had already solved the consolidation problem. Collapsing to a single extraction point eliminated two-thirds of the complexity.

**Financial model as a living reference.** The investor model isn't static — it's refined continuously pre-listing. Treating it as a versioned S3 artifact with KMS encryption and Lambda-based extraction solved the drift problem. Each report stamps the exact model version it ran against.

**Keeping the agent out of the spreadsheet.** Early attempts to have Nova Pro interpret raw Excel files produced unreliable results. The breakthrough was the Lambda extraction pattern: Python reads the workbook deterministically and returns structured JSON. Nova Pro never touches the spreadsheet.

**Prompt engineering for financial precision.** Feeding pre-computed variance data and asking Nova Pro to *interpret and contextualize* rather than calculate transformed output quality. Temperature at 0.2 for narrative, with explicit instructions to flag any metric it cannot derive rather than estimate.

**Regulatory signal vs. noise.** Regulations.Gov returns a high volume of filings. Scoping queries to specific docket categories (EPA, DOE, DOD) and using Nova Micro as a pre-classification layer solved the filtering problem.

**Governance vs. speed.** The human approval gate adds hours to what could be fully automated. But for a pre-listing company, ungoverned AI-generated investor materials are a liability. We optimized for trust over speed.

---

## What We Learned

**Browser automation is the last-mile for enterprise finance.** Most finance tools don't have clean APIs. Nova Act's browser-first approach bypasses this — if a human can do it in a browser, an agent can too.

**Never let the LLM touch the spreadsheet.** The Lambda extraction pattern — Python reads, JSON normalizes, agent reasons — is the right architecture for any financial AI application.

**Separate calculation from narration.** All math runs deterministically in Python before the LLM sees anything. LLMs are unreliable calculators but excellent analysts when given pre-computed data with context.

**MCP as the governed data backbone.** Routing all external data through Airia's MCP Gateway means every source gets the same audit treatment. Adding a new enrichment source is a configuration change, not a code change.

**Governance is a feature, not overhead.** For pre-IPO companies, a governed, auditable AI pipeline is a competitive advantage. The audit trail, versioned model references, and human approval gate aren't constraints. They're the product.

---

## What's Next

- **Scheduled monthly execution** via EventBridge (`cron(0 9 3 * ? *)`) with briefs queued for approval before board meetings
- **Interactive MCP Apps dashboard** rendering variance analysis as a filterable interface within Airia
- **Multi-tenant deployment** — the `company_id` parameterization and S3 key scheme already support 50+ companies at under \$50/month
- **Procurement Guardian agent** monitoring purchase orders for budget compliance and price anomalies
- **Regulatory alert agent** triggering on high-impact Regulations.Gov filings between monthly cycles
- **Post-IPO adaptation** to continuous disclosure — the pre-IPO governance trail becomes the compliance backbone

---

## Built With

`airia` · `amazon-nova-pro` · `amazon-nova-micro` · `amazon-nova-act` · `amazon-bedrock` · `python` · `aws-lambda` · `aws-s3` · `aws-eventbridge` · `alphavantage-mcp` · `regulations-gov-mcp` · `microsoft-teams` · `onedrive` · `openpyxl` · `pandas`

---

*DeltaFin AI was built for the Amazon Nova hackathon to solve a real finance automation problem — automated variance analysis for pre-IPO companies running on disconnected SaaS finance platforms. Total cost per run: under \$1.*
