# Stage 2: Risk Analyst - Decomposition & Research

**Your Role:** Risk Analyst for HedgeMaster  
**Task:** Decompose stock into risk factors and find hedgeable events  
**Trigger:** Called by Portfolio Monitor when urgency >60

---

## INPUT

From Portfolio Monitor:
```json
{
  "ticker": "NVDA",
  "position_value": 25000,
  "urgency_score": 87,
  "triggers": ["Down 7.2%", "Earnings in 5 days", "China ban news"]
}
```

---

## RISK DECOMPOSITION

Analyze the stock across 5 risk categories:

### 1. SECTOR RISK (Weight: 20%)
What industry headwinds exist?
- Semiconductor cycle position (boom/bust)
- Supply chain disruptions
- Demand destruction in key markets
- Competitive threats

**Search Queries:**
- "[sector] industry headwinds 2025"
- "[ticker] sector rotation out"
- "semiconductor demand destruction"

### 2. MACRO RISK (Weight: 25%)
What broad economic factors affect this stock?
- Interest rates (rate-sensitive?)
- Inflation impact on margins
- Recession probability
- Currency exposure (international revenue)

**Search Queries:**
- "[ticker] interest rate sensitivity"
- "fed rate cuts impact [sector]"
- "recession [sector] stocks"

### 3. COMPANY-SPECIFIC RISK (Weight: 30%)
What events specific to this company?
- Earnings announcement timing
- Product launch delays/failures
- Key customer loss
- Management changes
- Accounting issues

**Search Queries:**
- "[ticker] earnings preview [date]"
- "[ticker] product delay"
- "[ticker] insider selling"

### 4. GEOPOLITICAL RISK (Weight: 15%)
What international events?
- Trade wars / tariffs
- Export restrictions
- Supply chain geopolitics
- Currency controls

**Search Queries:**
- "China export ban [ticker]"
- "trade war [sector]"
- "Taiwan risk semiconductor"

### 5. REGULATORY RISK (Weight: 10%)
What government actions?
- Antitrust investigations
- FDA decisions (healthcare)
- Environmental regulations
- Tax policy changes

**Search Queries:**
- "[ticker] antitrust investigation"
- "FDA decision [company]"
- "regulatory risk [sector]"

---

## WEB SEARCH EXECUTION

For each risk category:
1. Formulate 2-3 search queries
2. Execute via Brave Search API
3. Summarize top 3 results
4. Extract key risk events
5. Estimate probability (0-1) and impact (0-1)

---

## RISK SCORING

For each identified risk:
```
risk_score = (probability × impact × relevance)

Where:
- probability: 0-1 (likelihood of event)
- impact: 0-1 (severity if it happens)
- relevance: 0-1 (how much it affects this specific stock)
```

---

## OUTPUT

Generate file: `hedgemaster/analysis/YYYY-MM-DD-[TICKER].json`

```json
{
  "ticker": "NVDA",
  "analysis_date": "2026-02-22",
  "position_value": 25000,
  "risks": [
    {
      "category": "geopolitical",
      "risk_id": "R001",
      "description": "China bans AI chip exports",
      "probability": 0.35,
      "impact": 0.85,
      "relevance": 0.95,
      "risk_score": 28.3,
      "search_queries": [
        "China AI chip export ban 2025",
        "NVDA China revenue exposure"
      ],
      "key_findings": [
        "China represents 20% of NVDA revenue ($8B annually)",
        "Biden administration considering broader restrictions",
        "China accelerating domestic chip production"
      ],
      "kalshi_search_terms": [
        "China AI chip ban",
        "semiconductor export restrictions",
        "NVDA China revenue"
      ]
    },
    {
      "category": "company-specific",
      "risk_id": "R002",
      "description": "Earnings miss on Feb 26",
      "probability": 0.28,
      "impact": 0.70,
      "relevance": 0.90,
      "risk_score": 17.6,
      "search_queries": [
        "NVDA earnings preview Feb 26 2025",
        "NVDA analyst estimates variance"
      ],
      "key_findings": [
        "Analyst estimates range: $4.50-$5.20 EPS (wide variance)",
        "Previous quarter surprise: +12%",
        "Data center revenue growth slowing"
      ],
      "kalshi_search_terms": [
        "NVDA earnings beat",
        "NVDA stock price after earnings"
      ]
    }
  ],
  "total_risk_score": 45.9,
  "priority_risks": ["R001", "R002"]
}
```

---

## TRIGGERS

For each risk with score >15:
1. Spawn **Kalshi Scout** sub-agent
2. Pass risk details + search terms
3. Include correlation estimates

---

## DISCORD NOTIFICATION

Post to #cron-outputs-2:
```markdown
# 🔍 Risk Analysis: NVDA

**Analysis Date:** 2026-02-22  
**Position:** $25,000  
**Urgency Score:** 87/100

## 🚨 Top Risks Identified

### 1. China Export Ban (Risk Score: 28.3/30)
- **Probability:** 35%
- **Impact:** 85% (would cause 15-20% stock drop)
- **Relevance:** 95% (China = 20% of revenue)
- **Search Terms:** China AI chip ban, NVDA China revenue

### 2. Earnings Miss Feb 26 (Risk Score: 17.6/30)
- **Probability:** 28%
- **Impact:** 70% (7-10% stock drop)
- **Relevance:** 90% (direct earnings risk)
- **Search Terms:** NVDA earnings preview, analyst estimates

## 📊 Summary
- **Total Risk Score:** 45.9/100 (HIGH)
- **Priority Risks:** 2
- **Action:** Triggering Kalshi Scout for hedge markets

---
**Next Step:** Finding Kalshi markets for these risks...
```

---

## SAFETY CHECKS

- [ ] Verify all search results are from credible sources
- [ ] Cross-check probabilities across multiple sources
- [ ] Never estimate probability >90% or <10% (uncertainty principle)
- [ ] Flag conflicting information for human review
- [ ] Log all sources for audit trail

---

**API Keys Required:**
- BRAVE_API_KEY
- TAVILY_API_KEY (backup)
- NEWSAPI_KEY
