# 🔒 Pre-IPO Compliance Gate

**AI-powered pull request compliance scanning for companies preparing to go public.**

A multi-agent Airia pipeline that chains three specialized AI agents to scan every pull request for license contamination, exposed secrets, and financial data — producing investor-grade audit reports.

---

## The Problem

Over 4,000 companies are preparing for IPO at any given time. Every one faces the same risk: a developer commits a GPL dependency, an API key, or a financial model to the repo — and it surfaces during due diligence months later.

Manual code reviews catch functional bugs, not IP risk. The compliance review bottleneck costs pre-IPO companies 25–200 hours per month of legal and engineering time.

## The Solution

Pre-IPO Compliance Gate automates the compliance checks that investment banks and legal counsel perform during due diligence — at the pull request level, before problems compound.

### Architecture

```
GitHub PR Webhook → AWS API Gateway
        │
        ▼
┌──────────────────────────────┐
│  Airia Multi-Agent Pipeline   │
│                               │
│  ┌─────────────────────────┐ │
│  │ Agent 1: License Audit   │ │  Gemini 2.5 Pro (t=0.3)
│  │ ← AWS Lambda tool        │ │  Scans manifests for GPL/AGPL/SSPL
│  └───────────┬─────────────┘ │
│              │ JSON            │
│  ┌───────────▼─────────────┐ │
│  │ Agent 2: Secrets Scanner │ │  Gemini 2.5 Pro (t=0.3)
│  │ ← AWS Lambda tool        │ │  Detects API keys, cap tables, PII
│  └───────────┬─────────────┘ │
│              │ JSON            │
│  ┌───────────▼─────────────┐ │
│  │ Agent 3: Compliance      │ │  Gemini 2.5 Pro (t=0.7)
│  │ Reporter ← Lambda tool   │ │  Posts PR comment, creates issues
│  └───────────┬─────────────┘ │
│              │                 │
│  ┌───────────▼─────────────┐ │
│  │ Memory (Write)           │ │  Airia Memory — audit trail
│  └─────────────────────────┘ │
└──────────────────────────────┘
        │
        ▼
  GitHub PR Comment + S3 Audit Log + SNS Alert
```

### Verdict Matrix

| Verdict | Trigger | Actions |
|---------|---------|---------|
| ✅ PASS | No CRITICAL or HIGH findings | PR comment, `compliance:passed` label |
| ⚠️ REVIEW_REQUIRED | HIGH findings only | PR comment, `compliance:review-required` label |
| ⛔ BLOCKED | Any CRITICAL finding | PR comment, blocking issue, `compliance:blocked` label, SNS alert |

---

## Tech Stack

| Layer | Service | Purpose |
|-------|---------|---------|
| **Orchestration** | Airia Pipeline | Multi-agent sequencing, memory, conditional routing |
| **LLM** | Gemini 2.5 Pro (via Airia) | All three agents |
| **Repo Access** | GitHub REST API | PR diffs, file contents, manifests |
| **Tool Execution** | AWS Lambda (Python 3.12) | License scanner, secrets scanner, PR reporter |
| **API Gateway** | AWS API Gateway | Webhook relay: GitHub → Lambda → Airia |
| **Audit Storage** | Amazon S3 | Compliance reports, scan history, audit trail |
| **Alerting** | Amazon SNS | Compliance team notifications on BLOCKED verdicts |
| **Alt. Storage** | Google Cloud Storage | Optional GCS backend via `GCS_AUDIT_BUCKET` env var |
| **Alt. Alerting** | Google Cloud Pub/Sub | Optional Pub/Sub backend via `PUBSUB_TOPIC` env var |
| **Secrets Mgmt** | AWS Secrets Manager | GitHub token, Airia API key storage |

---

## Quick Start

### 1. Prerequisites

- Airia account with pipeline creation access
- AWS account with Lambda, API Gateway, S3, SNS, Secrets Manager
- GitHub repo with admin access (webhook configuration)
- Python 3.12+ locally (for Lambda packaging)

### 2. Deploy AWS Lambda Tools

```bash
cd tools/
chmod +x deploy_all.sh
./deploy_all.sh
```

This deploys three Lambda functions and creates the API Gateway trigger.

### 3. Build Airia Pipeline

Open Airia visual editor and follow `docs/SETUP.md` step-by-step:

1. Create new pipeline from template
2. Add 2 more AI Operation nodes (3 total)
3. Paste prompts from `config/airia_agent_prompts.md`
4. Register Lambda endpoints as MCP tools
5. Link nodes sequentially
6. Add Memory (Write) node

### 4. Configure Webhook

```bash
python3 scripts/setup_webhook.py \
  --repo owner/repo \
  --gateway-url https://xxx.execute-api.us-east-1.amazonaws.com/prod/compliance
```

### 5. Test

Create a PR with a known GPL dependency — see `examples/demo_scenarios.md`.

---

## Project Structure

```
pre-ipo-compliance-gate/
├── README.md
├── LICENSE                            # MIT
├── .env.example                       # All required environment variables
├── .gitignore
│
├── config/
│   ├── airia_pipeline_spec.json       # Target pipeline architecture
│   ├── airia_agent_prompts.md         # All 3 agent system prompts (copy-paste ready)
│   ├── license_policy.yml             # SPDX license tiers: approved/review/denied
│   ├── secrets_patterns.yml           # 30+ detection regex patterns
│   └── compliance_rules.yml           # Verdict logic, templates, escalation rules
│
├── tools/
│   ├── deploy_all.sh                  # One-command Lambda + API Gateway deployment
│   ├── license_scanner/
│   │   ├── handler.py                 # Lambda: fetch manifests, classify licenses
│   │   └── requirements.txt
│   ├── secrets_scanner/
│   │   ├── handler.py                 # Lambda: pattern-match secrets, financial data
│   │   └── requirements.txt
│   └── pr_reporter/
│       ├── handler.py                 # Lambda: post PR comment, create issue, S3 log
│       └── requirements.txt
│
├── scripts/
│   ├── setup_webhook.py               # GitHub → API Gateway webhook config
│   ├── setup_s3.py                    # Create S3 audit bucket with versioning
│   └── trigger_pipeline.py            # Manual Airia pipeline trigger for testing
│
├── docs/
│   ├── ARCHITECTURE.md                # Design decisions, data flow, security model
│   ├── SETUP.md                       # Step-by-step Airia + AWS setup guide
│   ├── AIRIA_FEATURES.md              # Platform features used (for hackathon judging)
│   └── GAP_ANALYSIS.md               # JSON export vs build log discrepancies
│
├── examples/
│   ├── sample_pr_output.md            # Example BLOCKED compliance report
│   └── demo_scenarios.md              # 3 test scenarios with setup instructions
│
├── DEVPOST.md                         # Full hackathon submission narrative
└── SHORT_DESCRIPTION.md               # 200-char elevator pitch
```

---

## Platform Features Used

| Airia Feature | How Used |
|--------------|----------|
| AI Operation nodes | 3 specialized agents with custom prompts |
| Sequential pipeline | Agent chaining with structured JSON hand-off |
| Memory (Write) | Compliance history storage for audit trails |
| MCP Tool integration | 3 AWS Lambda tools registered as agent capabilities |
| Conditional Branch | Verdict-based routing (BLOCKED → issue creation path) |
| Model configuration | Gemini 2.5 Pro at tuned temperatures per agent |

| AWS Service | How Used |
|-------------|----------|
| Lambda | Tool execution for all 3 agents |
| API Gateway | GitHub webhook → Airia pipeline trigger |
| S3 | Audit trail storage with versioning |
| SNS | BLOCKED verdict alerts to compliance team |
| Secrets Manager | Secure credential storage |

---

## License

MIT — See [LICENSE](LICENSE) for details.
