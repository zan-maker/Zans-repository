# API Usage Tracker
## ImpactQuadrant System Monitor

**Last Updated:** 2025-02-15
**Purpose:** Track API usage, limits, and recharge needs

---

## CRITICAL APIS - DAILY LIMITS

| API | Provider | Monthly Limit | Current Usage | Status | Recharge Date | Action Needed |
|-----|----------|---------------|---------------|--------|---------------|---------------|
| Brave Search | Brave | 2,000 req/mo | Unknown | ⚠️ CHECK | N/A | Verify usage |
| Hunter.io | Hunter | 50 req/mo | 44 credits, 88 verifs | 🟢 ACTIVE | 2026-03-01 | Use for OTHER cron jobs |
| **ZeroBounce** | **Active** | **Pay-as-you-go** | **TBD** | **🟢 ACTIVE** | **N/A** | **API Key: fd0105c8c98340e0a2b63e2fbe39d7a4** |
| **NeverBounce** | **Alternative** | **Pay-as-you-go** | **0** | **⏳ SETUP** | **N/A** | **~$0.003/verification - For OTHER jobs** |
| AlphaVantage | AlphaVantage | 25 calls/day | Unknown | ⚠️ CHECK | N/A | Verify usage |
| Agentmail.to | Agentmail | TBD | Unknown | ⚠️ CHECK | N/A | Verify usage |
| Tavily | Tavily | Dev tier | Unknown | ⚠️ CHECK | N/A | Verify usage |
| **TranscriptAPI** | **YouTube** | **100 credits** | **100** | **🟢 ACTIVE** | **20 remaining** | **Video transcripts, search, channels** |

---

## PAID/ENTERPRISE APIs - MONITOR CREDITS

| API | Provider | Plan | Credits/Limits | Status | Alert At | Dashboard |
|-----|----------|------|----------------|--------|----------|-----------|
| Zyte | Zyte | Pay-as-you-go | $20/mo est. | ✅ ACTIVE | $15 | https://app.zyte.com |
| Abstract API | Abstract | Free tier | 100 req/day | ✅ ACTIVE | 80 req | https://app.abstractapi.com |
| Serper | Serper | Free tier | 2,500 req/mo | ✅ ACTIVE | 2,000 | https://serper.dev |

---

## MODEL APIs - USAGE TRACKING

| API | Provider | Rate Limit | Usage This Month | Est. Cost | Alert Threshold |
|-----|----------|------------|------------------|-----------|-----------------|
| Kimi K2.5 | Moonshot | High | Unknown | ~$0.10-0.50/call | $50/mo |
| GLM-4.7 | Z.AI | High | Unknown | ~$0.50-2.00/call | $100/mo |
| Nemotron | NVIDIA | N/A | Unknown | Free tier | N/A |

---

## API STATUS DASHBOARD

### Search APIs
```
Brave Search:     [████████░░] 80% (est.) - Check before heavy research
Tavily:           [░░░░░░░░░░] 10% (est.) - Backup ready
Serper:           [░░░░░░░░░░] 5% (est.) - Tertiary option
```

### Data Enrichment
```
Hunter.io:        [██████████] ??% - 50/mo limit - CRITICAL
Abstract API:     [░░░░░░░░░░] 10% (est.) - 100/day
Zyte:             [░░░░░░░░░░] 20% (est.) - Pay as you go
```

### Market Data
```
AlphaVantage:     [██████████] ??% - 25/day limit - CRITICAL
NewsAPI:          [░░░░░░░░░░] 10% (est.) - 100/day
```

### Email/Outreach
```
Agentmail (Zane): [░░░░░░░░░░] ??% - Unknown limit
Agentmail (Zander): [░░░░░░░░░░] ??% - Unknown limit
```

---

## RECOMMENDED API MONITORING SETUP

### Option 1: Heartbeat Check (Recommended)
Add to `HEARTBEAT.md` to check API status daily:
- Check Hunter.io remaining calls (if API supports it)
- Check Brave Search usage
- Check AlphaVantage daily limit
- Alert when <20% remaining

### Option 2: Cron Job
Create a daily cron job that:
- Calls API status endpoints where available
- Logs usage to this file
- Sends alert when limits approaching

### Option 3: Manual Weekly Review
Schedule calendar reminder to check this file every Monday.

---

## KNOWN LIMITS & GOTCHAS

### Hunter.io - CRITICAL
- **Limit:** 50 requests/month
- **Current:** Unknown
- **Impact:** Email verification stops if depleted
- **Action:** Verify usage before PE outreach (616 contacts to check)

### AlphaVantage - CRITICAL
- **Limit:** 25 calls/day
- **Current:** Unknown
- **Impact:** TradeRecommender stops if depleted
- **Action:** Batch calls, use only for high-value signals

### Brave Search
- **Limit:** 2,000 requests/month
- **Current:** Unknown
- **Impact:** All research stops if depleted
- **Action:** Tavily is backup, Serper is tertiary

### Agentmail.to
- **Limit:** Unknown (need to verify)
- **Current:** Unknown
- **Impact:** Email outreach stops
- **Action:** Check dashboard at https://app.agentmail.to

---

## RECHARGE/REFILL PROCESS

### When API is depleted:

1. **Hunter.io** - 🟢 ACTIVE (key updated 2025-02-15)
   - **Plan:** Free tier
   - **Credits:** 44/50 remaining (6 used)
   - **Verifications:** 88/100 remaining (12 used)
   - **Reset Date:** March 1, 2026
   - **Status:** ✅ Working
   - **Limitation:** Only 88 verifications available - need upgrade for 616-contact campaign
   - **Upgrade:** $49/mo for 500 requests at https://hunter.io/pricing

2. **AlphaVantage**
   - Upgrade: https://www.alphavantage.co/premium/
   - Cost: $29.99/mo for 75 calls/min
   - Alternative: Cache results, reduce call frequency

3. **Brave Search**
   - Upgrade: https://brave.com/search/api/
   - Cost: $3 per 1,000 queries (pay-as-you-go)
   - Alternative: Switch to Tavily/Serper

4. **Zyte**
   - Auto-recharges or monthly bill
   - Monitor: https://app.zyte.com/billing
   - Alert threshold: $15/mo

---

## IMMEDIATE ACTIONS NEEDED

### Before PE Outreach Campaign:
- [ ] Verify Hunter.io remaining calls (need ~50 for email verification)
- [ ] Check Agentmail.to account status and limits
- [ ] Confirm Zane/Zander accounts have sufficient credits

### Before Trade Recommendations:
- [ ] Check AlphaVantage daily usage (only 25/day)
- [ ] Verify NewsAPI status

### Weekly:
- [ ] Update this tracker with actual usage
- [ ] Check Zyte billing
- [ ] Review any API errors in logs

---

## API ERROR LOG

| Date | API | Error | Action Taken |
|------|-----|-------|--------------|
| 2025-02-15 | Memory | No API key for search | Using keyword search instead |

---

## CONTACTS FOR SUPPORT

| API | Support URL | Status Page |
|-----|-------------|-------------|
| Brave | https://support.brave.com | https://status.brave.com |
| Hunter | support@hunter.io | N/A |
| Tavily | https://tavily.com | N/A |
| Zyte | support@zyte.com | https://status.zyte.com |
| AlphaVantage | support@alphavantage.co | N/A |

---

**This file should be updated weekly with actual API usage data.**
