# MiningMetalsAnalyst - API Configuration

**Last Updated:** Feb 14, 2026

## Web Search APIs

### Brave Search (Primary)
- **API Key:** `BSAqx7g5ob7ymEOAUfRduTetIOWPalN`
- **Endpoint:** `https://api.search.brave.com/res/v1/web/search`
- **Rate Limit:** 2000 queries/month (free tier)
- **Usage:** Primary search for mine listings

### Tavily (Backup)
- **API Key:** `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`
- **Endpoint:** `https://api.tavily.com/search`
- **Usage:** When Brave quota exceeded

### NewsAPI (Mining Intelligence)
- **API Key:** `fe52ac365edf464c9dca774544a40da3`
- **Endpoint:** `https://newsapi.org/v2/everything`
- **Usage:** Mining sector news, M&A announcements

## Data Enrichment APIs

### ZeroBounce (Email Verification - Primary)
- **API Key:** `fd0105c8c98340e0a2b63e2fbe39d7a4`
- **Endpoint:** `https://api.zerobounce.net/v2/validate`
- **Usage:** Verify mine seller contact emails before outreach
- **Cost:** ~$0.0075 per verification
- **Status:** 🟢 ACTIVE

**Example:**
```bash
curl -X POST "https://api.zerobounce.net/v2/validate" \
  -d "api_key=fd0105c8c98340e0a2b63e2fbe39d7a4" \
  -d "email=seller@miningcompany.com"
```

### Hunter.io (Email Finder - Backup)
- **API Key:** `45e2e1243877d88f647b51952e6ddf0b8e8a4637`
- **Endpoint:** `https://api.hunter.io/v2/domain-search`
- **Usage:** Find seller contact emails when ZeroBounce unavailable
- **Example:** `curl "https://api.hunter.io/v2/domain-search?domain=miningcompany.com&api_key=API_KEY"`

### Abstract API (Company Enrichment)
- **API Key:** `38aeec02e6f6469983e0856dfd147b10`
- **Dashboard:** https://app.abstractapi.com/api/company-enrichment
- **Usage:** Enrich corporate seller information
- **Endpoint:** `https://companyenrichment.abstractapi.com/v1/`

## Web Scraping APIs

### Zyte
- **API Key:** `8d3e9c7af6e948b088e96ad15ca21719`
- **Endpoint:** `https://api.zyte.com/v1/extract`
- **Usage:** Scrape detailed mine reports, geological data

### crawl4ai (with Z.ai)
- **Instructions:** https://dev.to/ali_dz/crawl4ai-the-ultimate-guide-to-ai-ready-web-crawling-2620
- **Usage:** AI-ready content extraction from complex pages
- **Note:** Use Z.ai API key for enhanced extraction

## Search Sources (MANDATORY)

### Mine Listings
1. minelistings.com
2. GoldAndSilverMines.com
3. MineListings.co.uk
4. JuniorMiningNetwork.com
5. 43-101.com

### Regional
- Nevada, Arizona, Alaska, Canada, Australia

### Commercial Real Estate
- LoopNet, LandWatch, LandsOfAmerica

### JV/Partnership
- Junior mining funding opportunities

## API Usage Priority
1. Brave Search (primary)
2. Tavily (if Brave limit reached)
3. Hunter.io (for contacts)
4. Abstract API (for company data)
5. Zyte/crawl4ai (for complex scraping)

## Rate Limits to Monitor
- Brave: 2000/month
- Tavily: 1000/month (free tier)
- Hunter.io: 50/month (free tier)
- Abstract API: 500/month (free tier)
- Zyte: 1000 requests (trial)
