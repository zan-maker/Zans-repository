# Expense Reduction Agent - API Configuration

**Agent:** Expense Reduction Lead Generator  
**Purpose:** Generate leads for expense reduction services  
**Daily Targets:** 15-20 qualified leads  
**Configured:** Feb 15, 2026

---

## Email Verification APIs

### ZeroBounce (Primary)
**API Key:** `fd0105c8c98340e0a2b63e2fbe39d7a4`
**Use:** Verify CFO/VP Finance emails before sending
**Endpoint:** `https://api.zerobounce.net/v2/validate`
**Cost:** ~$0.0075 per verification
**Status:** 🟢 ACTIVE

**Usage Example:**
```bash
curl -X POST "https://api.zerobounce.net/v2/validate" \
  -d "api_key=fd0105c8c98340e0a2b63e2fbe39d7a4" \
  -d "email=cfo@company.com"
```

**Response Status:**
- `valid` - Safe to send ✅
- `invalid` - Do not send ❌
- `catch-all` - Risky, use caution ⚠️
- `unknown` - Cannot verify ❓

### Hunter.io (Backup)
**API Key:** `45e2e1243877d88f647b51952e6ddf0b8e8a4637`
**Use:** Find CFO/Finance VP emails
**Endpoint:** `https://api.hunter.io/v2/`
**Rate Limit:** 50 requests/month

---

## Web Search APIs

### Brave Search (Primary)
**API Key:** `BSAqx7g5ob7ymEOAUfRduTetIOWPalN`
**Use:** Search for companies with spend signals
**Rate Limit:** 2,000 requests/month

### Tavily (Backup)
**API Key:** `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`
**Use:** Deep research on company spend patterns

---

## Email Outreach

### Agentmail.to (Zander)
**API Key:** `am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f`
**From:** Zander@agentmail.to
**CC:** sam@impactquadrant.info

---

## Company Enrichment

### Abstract API
**API Key:** `38aeec02e6f6469983e0856dfd147b10`
**Use:** Enrich company data, employee count, funding

---

## Web Scraping

### Zyte
**API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
**Use:** Scrape job boards, funding databases

---

## Verification Workflow (CRITICAL)

**Before sending ANY email:**

1. **Check if email is generic (BLOCKED):**
   - Skip: contact@, info@, support@, hello@, sales@
   - Only use: firstname@, firstname.lastname@

2. **Verify with ZeroBounce API:**
   - If status = "valid" → Proceed with send ✅
   - If status = "invalid/unknown" → Skip ❌

3. **Log verification result** in outreach tracking

---

## Target Profile

**Company Size:** 20-500 employees  
**Decision Makers:** CFO, VP Finance, CEO, COO  
**Pain Signals:**
- Recent funding ( optimizing spend)
- Hiring finance/procurement roles
- Multiple SaaS subscriptions
- Rapid growth (vendor sprawl)

---

## Output Files

- Leads: `cron-output/expense-reduction/YYYY-MM-DD-leads.md`
- CSV Export: `cron-output/expense-reduction/YYYY-MM-DD-export.csv`
