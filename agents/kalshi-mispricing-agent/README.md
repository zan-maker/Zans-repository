# Kalshi Sportsbook Mispricing Agent

AI-driven arbitrage and mispricing engine between Kalshi event markets and sportsbook APIs.

## Overview

This system identifies arbitrage opportunities and mispricings between:
- **Kalshi**: Regulated event contracts (prediction markets)
- **Sportsbooks**: Traditional odds-based betting platforms

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA CONNECTORS                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ KalshiClient │  │ Sportsbook A │  │ Sportsbook B │      │
│  │   (REST)     │  │   Adapter    │  │   Adapter    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼─────────────────┼─────────────────┼──────────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                 CANONICAL EVENT LAYER                       │
│  - Normalize events across venues                           │
│  - Map Kalshi contracts ↔ Sportsbook markets                │
│  - Store event metadata (teams, timing, league)             │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              PRICING & MISPRICING ENGINE                    │
│  - Convert odds → implied probabilities                     │
│  - Vig adjustment for sportsbooks                           │
│  - Kalshi fee structure modeling                            │
│  - Arbitrage detection                                       │
│  - Value opportunity ranking                                 │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              EXECUTION & RISK MANAGEMENT                    │
│  - Exposure limits (per-market, per-venue, global)          │
│  - Order placement/cancellation                             │
│  - Partial fill handling                                     │
│  - Kill switch & logging                                     │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                     AI AGENT                                │
│  - Orchestrate scanning & selection                         │
│  - Natural language interface                               │
│  - Performance learning & refinement                        │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. KalshiClient

Authenticated REST API client for Kalshi markets.

**Features:**
- RSA-signed request authentication
- Rate limit handling
- Market data ingestion
- Order placement/management
- Portfolio tracking

### 2. Sportsbook Adapters

Standardized interface for multiple sportsbooks.

**Supported Books:**
- DraftKings (planned)
- FanDuel (planned)
- BetMGM (planned)
- Caesars (planned)

### 3. Mispricing Engine

Core logic for detecting arbitrage and value.

**Algorithms:**
- Implied probability conversion
- Vig adjustment (sportsbooks charge ~4-10% margin)
- Kalshi fee modeling (trading fees, settlement)
- Arbitrage detection (risk-free profit)
- Expected value calculation

### 4. Risk Manager

Enforces trading limits and safety controls.

**Limits:**
- Per-outcome exposure cap
- Per-market exposure cap
- Per-venue daily limit
- Global drawdown limit
- Kill switch (emergency stop)

### 5. AI Agent

Orchestrates the full workflow.

**Capabilities:**
- Continuous market scanning
- Trade proposal generation
- Natural language queries
- Performance tracking
- Adaptive thresholds

## Configuration

Create `.env` file:

```bash
# Kalshi API
KALSHI_API_KEY_ID=your_key_id
KALSHI_PRIVATE_KEY_PATH=./keys/kalshi_private.pem

# Sportsbook APIs (add as implemented)
DRAFTKINGS_API_KEY=your_key
FANDUEL_API_KEY=your_key

# Risk Parameters
MAX_PER_OUTCOME_EXPOSURE=500
MAX_PER_MARKET_EXPOSURE=1000
MAX_DAILY_LOSS=2000
GLOBAL_KILL_SWITCH=false

# Agent Settings
SCAN_INTERVAL_SECONDS=30
MIN_ARBITRAGE_PROFIT_PERCENT=2.0
MIN_EV_PERCENT=5.0
```

## Usage

```bash
# Install dependencies
npm install

# Run data feeder (odds ingestion)
npm run feeder

# Run mispricing engine (detection)
npm run engine

# Run trader (execution)
npm run trader

# Run AI agent (orchestration)
npm run agent

# Or run all in one
npm start
```

## API Examples

### Check for Arbitrage Opportunities

```bash
curl http://localhost:3000/api/arbitrage
```

### Get Top Mispricings

```bash
curl http://localhost:3000/api/mispricings?sport=NBA&min_ev=5
```

### Place Arbitrage Trade

```bash
curl -X POST http://localhost:3000/api/trade \
  -H "Content-Type: application/json" \
  -d '{
    "kalshi_contract_id": "KC-XXX",
    "kalshi_side": "yes",
    "kalshi_stake": 100,
    "sportsbook": "draftkings",
    "sportsbook_market_id": "DK-XXX",
    "sportsbook_outcome": "team_a_win",
    "sportsbook_stake": 95
  }'
```

## Data Storage

**SQLite Database Schema:**
- `events`: Canonical event data
- `kalshi_markets`: Kalshi contract info
- `sportsbook_markets`: Sportsbook market info
- `odds_snapshots`: Historical odds data
- `trades`: Executed trades
- `performance`: P&L tracking

## Monitoring

- Real-time arbitrage dashboard
- Exposure tracking
- P&L by sport/market
- Alert system for opportunities

## Roadmap

- [ ] Basic Kalshi integration
- [ ] First sportsbook adapter (DraftKings)
- [ ] Mispricing engine v1
- [ ] Risk management system
- [ ] AI agent orchestration
- [ ] Additional sportsbooks
- [ ] ML-based event matching
- [ ] Predictive mispricing models
