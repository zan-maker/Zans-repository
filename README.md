# DeltaFin AI

**Automated financial variance analysis for pre-IPO companies — built on Airia, Amazon Nova, and Amazon Bedrock.**

DeltaFin AI is a 7-stage financial intelligence pipeline that extracts consolidated financial data from enterprise platforms, runs automated variance analysis against investor models, enriches with live market and regulatory intelligence, and generates governance-audited investor briefs. Total cost per run: under $1.

---

## The Problem

Pre-IPO finance teams run on disconnected SaaS platforms — accounting in Xero, procurement in Precoro, reporting in Syft Analytics. Every month, someone manually exports reports, reconciles across entities, pulls commodity prices, compares actuals to the financial model investors underwrote, and stitches everything into an investor brief. It takes a full day.

The real pain isn't data extraction — it's **variance analysis**. Investors and boards don't just want numbers. They want to know: *are we tracking to the model we raised on?*

## The Solution

DeltaFin AI automates the entire workflow: extraction → normalization → variance calculation → market enrichment → regulatory intelligence → narrative generation → governed delivery. What previously took a full day runs in under 10 minutes, with a complete audit trail and human approval gate before distribution.

---

## Architecture

```
┌──────────────┐  ┌──────────────────┐  ┌──────────────────────────────────┐
│  S3 Buckets   │  │  Amazon Nova Act  │  │        AIRIA PLATFORM             │
│               │  │                   │  │                                  │
│ finmodels-*   │  │  Browser Agent    │  │  7-Stage Agent Workflow:          │
│ (versioned,   │  │  • Login to Syft  │  │                                  │
│  KMS encrypt) │  │  • Export CSV     │  │  0. Lambda → Model + Syft JSON   │
│               │  │                   │  │  1. Nova Act → Syft extraction   │
│ syft-exports-*│  └───────┬──────────┘  │  2A. MCP → AlphaVantage          │
│               │          │ CSV         │  2B. MCP → Regulations.Gov        │
│ deltafin-     │          ▼             │  3. Python → Variance engine      │
│  output       │◄─────────┬─────────────│  4. Nova Pro → Narrative (t=0.2)  │
└──────────────┘          │             │  5. Human approval gate           │
                           │             │  6. MCP → Teams + OneDrive       │
┌──────────────┐          │             │                                  │
│  Lambda       │──────────┘             │  Governance: full audit trail,    │
│               │                        │  policy enforcement, cost monitor │
│ extract_model │                        └──────────────────────────────────┘
│ extract_syft  │
│ (Python 3.12) │
└──────────────┘
```

## Technology Stack

| Component | Technology | Role |
|-----------|-----------|------|
| Orchestration | Airia Enterprise AI Platform | Agent workflow, MCP Gateway, governance |
| Browser Automation | Amazon Nova Act SDK | Syft Analytics data extraction |
| Financial Analysis | Amazon Nova Pro (Bedrock) | Variance interpretation, narrative generation |
| Data Classification | Amazon Nova Micro (Bedrock) | CSV classification, regulatory pre-filtering |
| Financial Model Access | AWS Lambda + S3 | Versioned Excel model extraction via `openpyxl` |
| Market Data | AlphaVantage MCP | Commodities, FX, macro indicators, peer equities |
| Regulatory Data | Regulations.Gov MCP | Federal rulemaking, proposed rules, comment periods |
| Delivery | Microsoft Teams + OneDrive MCP | Governed brief distribution |
| Scheduling | AWS EventBridge | Monthly automated pipeline trigger |
| Variance Engine | Python (`pandas`) | All quantitative calculations |

---

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/ARCHITECTURE.md) | Technical architecture and design decisions |
| [Pipeline](docs/PIPELINE.md) | Stage-by-stage pipeline specification |
| [Setup](docs/SETUP.md) | Airia configuration and MCP tool attachment |
| [Deployment](docs/DEPLOYMENT.md) | AWS infrastructure (S3, Lambda, EventBridge, IAM) |
| [Financial Model Access](docs/FINANCIAL-MODEL-ACCESS.md) | S3 + Lambda extraction pattern |
| [Devpost](DEVPOST.md) | Hackathon project story |

---

## Quick Start

```bash
# 1. Deploy AWS infrastructure
aws s3api create-bucket --bucket finmodels-deltafin \
  --versioning-configuration Status=Enabled \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms"}}]
  }'
aws s3api create-bucket --bucket syft-exports-deltafin
aws s3api create-bucket --bucket deltafin-output

# 2. Upload financial model
aws s3 cp model.xlsx s3://finmodels-deltafin/{entity}/budget/20250301/model.xlsx

# 3. Configure MCP servers in Airia (see docs/SETUP.md)
# 4. Attach tools to pipeline nodes (see docs/SETUP.md)
# 5. Run pipeline in Airia or wait for EventBridge schedule
```

See individual docs for complete instructions.

## Design Principles

1. **Never let the LLM touch the spreadsheet.** Lambda reads the workbook; Nova Pro reasons over structured JSON.
2. **Separate calculation from narration.** All math runs in Python. The LLM interprets pre-computed variance data.
3. **Governance is a feature, not overhead.** Audit trails, versioned models, and human approval gates are the product.
4. **MCP as the governed data backbone.** All external data flows through Airia's MCP Gateway.
5. **Atomic commands for browser automation.** Nova Act workflows decompose into precise, verifiable steps.

## Cost Per Monthly Run

| Component | Cost |
|-----------|------|
| Nova Pro (all AI stages) | $0.15 – $0.50 |
| AlphaVantage API | $0.02 – $0.05 |
| Regulations.Gov API | Free |
| Lambda + S3 | $0.06 |
| Microsoft Graph API | Free (M365) |
| **Total** | **$0.23 – $0.61** |

Scales to 50 companies for under $50/month.

---

## License

MIT

*Built for the Amazon Nova Hackathon.*
