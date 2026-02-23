# LeadGenerator - API Configuration

**Last Updated:** Feb 14, 2026

## Web Search APIs

### Brave Search (Primary)
- **API Key:** `BSAqx7g5ob7ymEOAUfRduTetIOWPalN`
- **Endpoint:** `https://api.search.brave.com/res/v1/web/search`
- **Usage:** Primary search for startups, funding news

### Tavily (Backup)
- **API Key:** `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`
- **Endpoint:** `https://api.tavily.com/search`
- **Usage:** When Brave quota exceeded

## Email Finder & Verification APIs

### ZeroBounce (Primary - Email Verification)
- **API Key:** `fd0105c8c98340e0a2b63e2fbe39d7a4`
- **Endpoint:** `https://api.zerobounce.net/v2/validate`
- **Usage:** Verify emails before sending (high accuracy)
- **Cost:** ~$0.0075 per verification
- **Status:** 🟢 ACTIVE

**Verification Workflow:**
```bash
curl -X POST "https://api.zerobounce.net/v2/validate" \
  -d "api_key=fd0105c8c98340e0a2b63e2fbe39d7a4" \
  -d "email=target@company.com"
```
**Only send if response status = "valid"**

### Hunter.io (Backup - Email Finder)
- **API Key:** `45e2e1243877d88f647b51952e6ddf0b8e8a4637`
- **Domain Search:** `https://api.hunter.io/v2/domain-search?domain={domain}&api_key={key}`
- **Email Finder:** `https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first}&last_name={last}&api_key={key}`
- **Usage:** Find CEO/founder emails when ZeroBounce can't find them
- **Rate Limit:** 50 requests/month (free tier)

## Company Enrichment API

### Abstract API
- **API Key:** `38aeec02e6f6469983e0856dfd147b10`
- **Dashboard:** https://app.abstractapi.com/api/company-enrichment
- **Endpoint:** `https://companyenrichment.abstractapi.com/v1/?api_key={key}&domain={domain}`
- **Usage:** Company size, funding, industry, social profiles
- **Data Points:** Employees, location, industry, funding stage

## Web Scraping APIs

### Zyte
- **API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
- **Usage:** Scrape LinkedIn, careers pages, company data
- **Endpoint:** `https://api.zyte.com/v1/extract`

### crawl4ai (with Z.ai)
- **Instructions:** https://dev.to/ali_dz/crawl4ai-the-ultimate-guide-to-ai-ready-web-crawling-2620
- **Usage:** AI-ready extraction from complex pages
- **Note:** Use Z.ai API key for enhanced extraction

## Search Sources (MANDATORY)

### Funding Databases
1. Crunchbase
2. AngelList
3. PitchBook
4. TechCrunch funding announcements

### Crowdfunding Platforms (PRIORITY)
1. Republic.co
2. Wefunder.com
3. StartEngine
4. SeedInvest
5. Crowdcube (UK)

### Job Boards
1. AngelList (Wellfound)
2. LinkedIn Jobs
3. Startup.jobs

### Accelerators/VC Portfolios
1. Y Combinator (W24, S23)
2. Techstars
3. 500 Startups
4. Seedcamp

### Industry-Specific
- SaaS: IndieHackers, Product Hunt
- Fintech: Fintech Today
- Healthcare: Rock Health
- AI/ML: AI Grant

## API Usage Workflow

### For Each Lead:
1. **Brave Search** → Find company via funding news
2. **Abstract API** → Enrich company details (size, funding, industry)
3. **Hunter.io** → Find CEO/founder email
4. **Zyte/crawl4ai** → Scrape careers page for hiring velocity

### Example API Chain:
```
1. Search: "funded Republic $2M seed" (Brave)
2. Enrich: company.com (Abstract API)
3. Find email: domain-search company.com (Hunter.io)
4. Scrape: company.com/careers (Zyte)
```

## Rate Limits to Monitor
- Brave: 2000/month
- Hunter.io: 50/month
- Abstract API: 500/month
- Zyte: 1000 requests (trial)
