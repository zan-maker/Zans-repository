# Pre-IPO Compliance Gate — Devpost Submission

## Inspiration

Over 4,000 companies are preparing for IPO at any given time. Every one faces the same risk: compliance gaps that slip through code review and surface during due diligence. A GPL dependency means forced source disclosure. An exposed API key means a security incident report. A financial model in the repo means investor terms are discoverable.

We've seen this firsthand at a pre-IPO battery recycling company preparing for ASX listing. The compliance review bottleneck costs 25–200 hours per month of legal and engineering time — and it's almost entirely automatable.

## What It Does

Pre-IPO Compliance Gate is a multi-agent Airia pipeline that scans every pull request for three categories of pre-IPO compliance risk:

**Agent 1 — License Audit:** Scans dependency manifests (package.json, requirements.txt, Gemfile, etc.) and classifies every license by IPO risk tier. GPL/AGPL/SSPL = CRITICAL (blocks due diligence). LGPL/MPL = HIGH (requires legal review). MIT/Apache = LOW (safe).

**Agent 2 — Secrets & Financial Data Scanner:** Detects 15+ categories of hardcoded secrets (AWS keys, GitHub tokens, Stripe keys, private keys, database connection strings). Also flags financial data files (cap tables, term sheets, valuation models) and PII that should never be in source control.

**Agent 3 — Compliance Report Generator:** Aggregates findings from both scanners, determines a verdict (PASS / REVIEW_REQUIRED / BLOCKED), posts an investor-grade compliance report as a PR comment, creates blocking issues for CRITICAL findings, and writes an immutable audit log to S3.

## How We Built It

**Airia Pipeline Architecture:**
- 3 AI Operation nodes using Gemini 2.5 Pro with tuned temperatures (0.3 for deterministic scanning, 0.7 for natural language reporting)
- Sequential pipeline with structured JSON hand-off between agents
- Memory (Write) node for compliance history and trend analysis
- MCP Tool integration connecting agents to AWS Lambda functions

**AWS Infrastructure:**
- 3 Lambda functions (Python 3.12) registered as Airia MCP tools
- API Gateway for GitHub webhook → pipeline trigger relay
- S3 with versioning for 7-year audit trail retention
- SNS for compliance team alerts on BLOCKED verdicts
- Secrets Manager for credential storage

**Design Decisions:**
- Read-only scanners / write-only reporter: Clean security boundary
- Structured JSON inter-agent communication: No unstructured text parsing
- External tool execution: All code, API keys, and cloud access outside LLM context
- AWS-first with GCP alternatives documented

## Challenges We Ran Into

**License identification from manifests:** Package managers don't always include license metadata. We had to build a multi-source lookup strategy — manifest parsing, registry API queries, and LICENSE file heuristics.

**Financial data detection nuance:** Not every .xlsx is a financial model. We use keyword matching (cap table, term sheet, valuation) combined with directory analysis (/finance, /investor, /board) to reduce false positives.

**Inter-agent data passing:** Airia's chat history mechanism passes context between agents. We had to design prompts that produce strictly valid JSON to avoid parsing failures downstream.

**Pipeline export gaps:** The Airia JSON export captured the default template state rather than our built pipeline — requiring us to document the full build process as code-ready instructions.

## Accomplishments We're Proud Of

- **Zero external dependencies** beyond AWS — no third-party SaaS, no proprietary scanning engines
- **Three-agent orchestration** with structured hand-off and clear separation of concerns
- **Investor-grade output** — compliance reports formatted for audit trails with severity tables, remediation steps, and traceability UUIDs
- **Real-world domain expertise** — license tiers based on actual IPO due diligence requirements, not generic security scanning
- **Financial data detection** — unique to pre-IPO context (no existing tool flags cap tables or term sheets in repos)

## What We Learned

- **Airia's pipeline architecture** supports genuine multi-agent orchestration — not just prompt chaining
- **MCP Tool integration** turns agents into systems that can read, write, and act on external infrastructure
- **Temperature tuning matters** — 0.3 for scanning produces deterministic, reproducible findings; 0.7 for reporting produces natural compliance language
- **Memory nodes** enable historical analysis that single-execution pipelines can't provide
- **Structured JSON contracts** between agents are essential — natural language hand-off creates compounding parsing errors

## What's Next

- **Expanded license detection:** Direct npm/PyPI/RubyGems registry lookups for accurate SPDX classification
- **Git history scanning:** Check full commit history, not just current PR diff
- **SOC 2 / SOX modules:** Additional compliance frameworks beyond IPO
- **Auto-remediation:** Agent 3 proposes and applies fixes (replace GPL deps, rotate exposed keys)
- **Compliance dashboard:** React frontend aggregating Memory data into trend charts
- **Google Cloud Functions:** Full GCP alternative deployment alongside AWS

## Built With

- Airia (multi-agent pipeline orchestration)
- Gemini 2.5 Pro (AI model)
- AWS Lambda (tool execution)
- AWS API Gateway (webhook relay)
- Amazon S3 (audit storage)
- Amazon SNS (alerting)
- GitHub REST API (PR access)
- Python 3.12
