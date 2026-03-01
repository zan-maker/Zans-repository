# Contributing

DeltaFin AI was built for the Amazon Nova Hackathon. Contributions are welcome.

## Repository Structure

```
deltafin-ai/
├── README.md                          # Project overview and quick start
├── DEVPOST.md                         # Hackathon submission narrative
├── LICENSE                            # MIT License
├── .gitignore
├── docs/
│   ├── ARCHITECTURE.md                # System architecture and data flow
│   ├── PIPELINE.md                    # Stage-by-stage technical docs
│   ├── SETUP.md                       # Installation and deployment guide
│   ├── INFRASTRUCTURE.md              # AWS resource provisioning
│   ├── MCP_CONFIGURATION.md           # Airia MCP Gateway setup
│   └── FINANCIAL_MODEL.md             # Model access pattern and versioning
├── engine/
│   └── variance_engine.py             # Python variance engine (Stage 3)
├── infrastructure/
│   ├── deploy.sh                      # S3 + IAM deployment
│   ├── deploy-lambdas.sh              # Lambda function packaging
│   └── deploy-eventbridge.sh          # Monthly schedule rule
├── lambda/
│   ├── extract_model_financials/      # Reads investor model from S3
│   │   ├── handler.py
│   │   └── requirements.txt
│   └── extract_syft_financials/       # Reads Syft CSVs from S3
│       ├── handler.py
│       └── requirements.txt
└── pipeline/
    ├── README.md                      # Pipeline import instructions
    └── deltafin-pipeline.json         # Airia pipeline definition (user-provided)
```

## Key Principle

**Never let the LLM calculate.** All quantitative work happens in Python (`engine/variance_engine.py` and `lambda/` functions). Nova Pro only interprets and narrates pre-computed data.

If you're adding a new calculation (e.g., cohort analysis, unit economics), add it to the variance engine — not to a prompt.

## Adding a New Enrichment Source

1. Configure the MCP server in Airia Gateway
2. Add a new pipeline node (or extend Stage 2A/2B)
3. Document in `docs/MCP_CONFIGURATION.md`
4. Update the Nova Pro system prompt in Stage 4 to incorporate the new data

## Updating the Chart of Accounts

When the investor model is reforecast with different line items:

1. Update `COA_MAP` in `lambda/extract_syft_financials/handler.py`
2. Update tab extraction logic in `lambda/extract_model_financials/handler.py` if tabs change
3. Redeploy both Lambdas: `cd infrastructure && ./deploy-lambdas.sh`
