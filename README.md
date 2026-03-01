# DeltaFin Chat

**Financial variance analysis agent on Telegram — powered by DigitalOcean Gradient™**

Upload your financial model. Ask questions in plain English. Get governed, source-cited answers.

> Built for the [DigitalOcean Gradient™ AI Hackathon](https://digitalocean.devpost.com/)

---

## How It Works

```
You (Telegram) → Bot → Gradient Agent → [Knowledge Base + DO Functions] → Response
```

A Gradient AI agent handles natural language understanding and narrative generation. Three DO Functions handle all financial math deterministically. A Knowledge Base provides RAG over the investor model. A Telegram bot relays messages.

**Core principle: Code for math. Model for meaning.**

## Quick Start

### 1. Set Up DigitalOcean

- Sign up at [digitalocean.com](https://mlh.link/digitalocean-signup) ($200 free credits)
- Enable **Gradient AI** in your Console

### 2. Create the Agent

1. Console → Gradient AI → Create Agent
2. Name: `DeltaFin Chat`
3. Model: Claude Sonnet 4.5 (or GPT-4.1)
4. Paste instructions from [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md)
5. Save → copy **Agent Endpoint** and **Access Key**

### 3. Set Up Knowledge Base

1. Preprocess your model: `python knowledge_base/preprocessor.py model.xlsx`
2. Upload output `.md` to DO Spaces
3. Console → Knowledge Bases → Create → add Spaces source
4. Attach KB to your agent in Resources tab

### 4. Deploy Functions

```bash
doctl serverless install     # one-time setup
cd functions
doctl serverless deploy .    # deploys all 3 functions
```

Attach each function to the agent via **Resources → Functions** in Console.

### 5. Create Telegram Bot

1. Message `@BotFather` on Telegram → `/newbot` → save token
2. Configure environment:
   ```bash
   cp .env.example .env
   # Fill in TELEGRAM_BOT_TOKEN, AGENT_ENDPOINT, AGENT_ACCESS_KEY
   ```
3. Run locally: `cd telegram_bot && pip install -r requirements.txt && python bot.py`
4. Or deploy to App Platform (see below)

### 6. Deploy Bot to App Platform

```yaml
# app-spec.yml
name: deltafin-telegram-bot
services:
  - name: bot
    github:
      repo: your-org/deltafin-chat
      branch: main
      deploy_on_push: true
    source_dir: telegram_bot
    run_command: python bot.py
    environment_slug: python
    instance_size_slug: apps-s-1vcpu-0.5gb
    envs:
      - key: TELEGRAM_BOT_TOKEN
        value: ${TELEGRAM_BOT_TOKEN}
        type: SECRET
      - key: AGENT_ENDPOINT
        value: ${AGENT_ENDPOINT}
      - key: AGENT_ACCESS_KEY
        value: ${AGENT_ACCESS_KEY}
        type: SECRET
```

```bash
doctl apps create --spec app-spec.yml
```

## Project Structure

```
deltafin-chat/
├── AGENT_INSTRUCTIONS.md       # Paste into Gradient agent
├── DEVPOST.md                  # Hackathon submission narrative
├── SHORT_DESCRIPTION.md        # 500-char Devpost blurb
├── README.md                   # This file
├── LICENSE
├── .gitignore
├── .env.example
│
├── telegram_bot/
│   ├── bot.py                  # Telegram ↔ Gradient agent relay
│   └── requirements.txt
│
├── functions/                  # DO Functions (serverless math)
│   ├── project.yml             # Functions deployment config
│   ├── variance_engine/
│   │   └── __main__.py         # Line-item variance analysis
│   ├── runway_calculator/
│   │   └── __main__.py         # Cash runway projection
│   └── revenue_decomposition/
│       └── __main__.py         # Volume/price/mix decomposition
│
├── knowledge_base/
│   ├── preprocessor.py         # Excel → markdown for KB indexing
│   └── SETUP.md                # KB creation guide
│
├── evaluation/
│   └── test_cases.csv          # 20 test cases for Gradient Evaluations
│
└── docs/
    ├── ARCHITECTURE.md         # System design
    └── GRADIENT_USAGE.md       # DO feature map for judges
```

## DigitalOcean Products Used

| Product | Purpose |
|---------|---------|
| Gradient AI Agent | Core intelligence + routing |
| Gradient Serverless Inference | LLM (Claude Sonnet 4.5) |
| Gradient Knowledge Base | RAG over financial model |
| Gradient Evaluations | Agent accuracy testing |
| DO Functions | Deterministic financial math |
| App Platform | Telegram bot hosting |
| Spaces | File storage + KB source |

## License

MIT — see [LICENSE](LICENSE)
