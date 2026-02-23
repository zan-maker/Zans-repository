# SMB Lead Generator - API Configuration

**Agent:** SMB Lead Generator  
**Purpose:** Generate leads for Wellness 125 Cafeteria Plans  
**Daily Targets:** 15-20 qualified employer leads  
**Configured:** Feb 15, 2026

---

## Email Verification APIs

### ZeroBounce (Primary)
**API Key:** `fd0105c8c98340e0a2b63e2fbe39d7a4`
**Use:** Verify employer contact emails before sending
**Endpoint:** `https://api.zerobounce.net/v2/validate`
**Cost:** ~$0.0075 per verification
**Status:** 🟢 ACTIVE

**Usage Example:**
```bash
curl -X POST "https://api.zerobounce.net/v2/validate" \
  -d "api_key=fd0105c8c98340e0a2b63e2fbe39d7a4" \
  -d "email=ceo@company.com"
```

**Response Status:**
- `valid` - Safe to send ✅
- `invalid` - Do not send ❌
- `catch-all` - Risky, use caution ⚠️
- `unknown` - Cannot verify ❓

### Hunter.io (Backup)
**API Key:** `45e2e1243877d88f647b51952e6ddf0b8e8a4637`
**Use:** Find and verify emails when ZeroBounce unavailable
**Endpoint:** `https://api.hunter.io/v2/`
**Rate Limit:** 50 requests/month

---

## Web Search APIs

### Brave Search (Primary)
**API Key:** `BSAqx7g5ob7ymEOAUfRduTetIOWPalN`
**Use:** Search for employers in target industries
**Rate Limit:** 2,000 requests/month

### Tavily (Backup)
**API Key:** `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`
**Use:** Deep research when Brave limit reached

---

## Email Outreach

### Agentmail.to (Zane)
**API Key:** `am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68`
**From:** Zane@agentmail.to
**CC:** sam@impactquadrant.info

---

## Company Enrichment

### Abstract API
**API Key:** `38aeec02e6f6469983e0856dfd147b10`
**Use:** Enrich company data (size, industry, location)

---

## Web Scraping

### Zyte
**API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
**Use:** Scrape business directories, career pages

### Yellow Pages (Zembra)
**API Key:** `8qYVrLzjNYZVcnPSM0N3gPRddFsWXWb58k4GmTCEMQhlx0gUUhehQsPmTztblnINSC3smdyiQWeJKvASsyYNB8CT3n5eJS46Nqh90kavcdVuS2AaWBtutYyiayxdjvS7`
**Use:** Find local businesses by category and location

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

## Target Industries

1. Healthcare (medical practices, clinics, home health)
2. Hospitality (hotels, restaurants, event venues)
3. Manufacturing (light manufacturing, assembly)
4. Transportation (logistics, trucking, delivery)

---

## Output Files

- Leads: `cron-output/smb-leads/YYYY-MM-DD-leads.md`
- CSV Export: `cron-output/smb-leads/YYYY-MM-DD-export.csv`
