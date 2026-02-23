# No-Code API Scraping Skill
## Steve Sie Method for Craigslist & Reddit

**Skill ID:** `nocode-api-scraping`  
**Purpose:** Extract data from Craigslist and Reddit without writing scraping code  
**Method:** HAR file capture + API generation  
**Tools:** Browser DevTools + Steve Sie platform  
**Created:** Feb 15, 2026

---

## Overview

This skill enables sub-agents to extract structured data from Craigslist and Reddit using a no-code approach:

1. **Browse** the target site normally
2. **Capture** network traffic as HAR file
3. **Upload** HAR to Steve Sie platform
4. **Generate** API endpoint
5. **Query** programmatically

**No complex scraping code required.**

---

## Methodology

### Step 1: Browse Target Site

**For Craigslist:**
- Navigate to: `https://[city].craigslist.org/search/bfs` (businesses for sale)
- Example searches:
  - Dallas: `https://dallas.craigslist.org/search/bfs?query=car+wash`
  - Houston: `https://houston.craigslist.org/search/bfs?query=laundromat`
  - Phoenix: `https://phoenix.craigslist.org/search/bfs?query=business`

**For Reddit:**
- Navigate to target subreddit
- Example: `https://www.reddit.com/r/smallbusiness/search/?q=Selling+business`
- Or: `https://www.reddit.com/r/entrepreneur/search/?q=business+for+sale`

### Step 2: Open DevTools

**Chrome/Edge:**
1. Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
2. Click **Network** tab
3. Ensure **Preserve log** is checked (☑️)

### Step 3: Capture Network Traffic

**While DevTools is open:**
1. Refresh the page (`F5`)
2. Scroll through results (load more if infinite scroll)
3. Click into individual listings
4. Navigate back
5. **Let all network requests complete**

**What to capture:**
- ✅ Initial page load requests
- ✅ API calls (XHR/Fetch)
- ✅ Image/asset loads
- ✅ Click-through navigation

### Step 4: Export HAR File

**In DevTools Network tab:**
1. Right-click anywhere in the network log
2. Select **Save all as HAR with content**
3. Save as: `craigslist-[city]-[search]-[date].har`
4. Or: `reddit-[subreddit]-[search]-[date].har`

**File size:** Typically 2-10 MB depending on page complexity

### Step 5: Upload to Steve Sie Platform

**Platform URLs:**
- Craigslist: https://stevesie.com/apps/craigslist-api
- Reddit: https://stevesie.com/apps/reddit-api

**Upload process:**
1. Go to the appropriate platform URL
2. Click **Upload HAR File**
3. Select your exported HAR file
4. Wait for processing (30-60 seconds)
5. Platform extracts API endpoints automatically

### Step 6: Generate API Endpoint

**After upload:**
1. Steve Sie platform analyzes HAR file
2. Identifies data-fetching API calls
3. Generates simplified API endpoint
4. Provides:
   - Endpoint URL
   - Required headers
   - Query parameters
   - Authentication (if needed)

**Example Output:**
```
Endpoint: https://api.stevesie.com/craigslist/search
Method: GET
Headers:
  - X-API-Key: [your_key]
Parameters:
  - city: dallas
  - category: bfs
  - query: car wash
```

### Step 7: Query Programmatically

**Using curl:**
```bash
curl -X GET 'https://api.stevesie.com/craigslist/search' \
-H 'X-API-Key: YOUR_STEVESIE_KEY' \
-d 'city=dallas' \
-d 'category=bfs' \
-d 'query=car+wash'
```

**Using Python:**
```python
import requests

response = requests.get(
    'https://api.stevesie.com/craigslist/search',
    headers={'X-API-Key': 'YOUR_STEVESIE_KEY'},
    params={
        'city': 'dallas',
        'category': 'bfs',
        'query': 'car wash'
    }
)

data = response.json()
```

---

## Use Cases by Agent

### Deal Origination Agent
**Craigslist searches:**
- `car wash for sale [city]`
- `laundromat for sale [city]`
- `business for sale [city]`
- `restaurant for sale [city]`

**Reddit searches:**
- `selling business` in r/smallbusiness
- `business valuation` in r/entrepreneur
- `exit strategy` in r/business

### SMB Lead Generator
**Craigslist searches:**
- `medical practice [city]`
- `restaurant equipment [city]` (signals new restaurant)
- `commercial kitchen [city]`

### B2B Referral Fee Agent
**Reddit searches:**
- `need CFO` in r/smallbusiness
- `accounting help` in r/startup
- `IT services` in r/sysadmin

---

## Best Practices

### HAR File Capture
- ✅ Capture full page load (wait for all requests)
- ✅ Include pagination (scroll/load more)
- ✅ Capture detail page clicks
- ❌ Don't clear browser cache before capture
- ❌ Don't use incognito (may block some requests)

### API Reliability
- **Steve Sie APIs are unofficial** - they reverse-engineer the site's internal APIs
- **Rate limits apply** - don't hammer the endpoints
- **Sites change** - regenerate HAR if API stops working
- **Test first** - verify data structure before automation

### Data Quality
- **Craigslist:** Check posting dates (filter out old posts)
- **Reddit:** Check comment scores (filter low-engagement)
- **Verify** - cross-check critical data points
- **Deduplicate** - use URL or ID as unique key

---

## Limitations & Considerations

### Craigslist
- **IP blocking** - CL blocks scrapers aggressively
- **CAPTCHAs** - may appear after multiple requests
- **Ghosting** - some posts appear but aren't publicly visible
- **No official API** - Steve Sie method uses internal endpoints

### Reddit
- **Rate limiting** - 60 requests/minute for OAuth
- **API changes** - Reddit updates API frequently
- **Authentication** - some data requires login
- **Content policies** - respect subreddit rules

### Legal/Ethical
- ✅ **Permitted:** Public listings, public posts
- ✅ **Permitted:** Personal research, lead generation
- ❌ **Not permitted:** Spam, harassment, reselling data
- ❌ **Not permitted:** Violating site's Terms of Service at scale

---

## Troubleshooting

### HAR Upload Fails
**Issue:** File too large (>50MB)
**Fix:** Clear browser cache, capture fewer pages

### No API Endpoints Found
**Issue:** Site uses heavy JavaScript rendering
**Fix:** Scroll/interact more before exporting HAR

### API Returns Empty
**Issue:** Session cookies expired
**Fix:** Re-capture HAR with fresh browser session

### Rate Limited
**Issue:** Too many requests
**Fix:** Add delays, rotate IPs, reduce frequency

---

## Alternative: Direct HAR Parsing

If Steve Sie platform is unavailable, parse HAR directly:

```python
import json

# Load HAR file
with open('craigslist-search.har', 'r') as f:
    har = json.load(f)

# Extract API calls
entries = har['log']['entries']
for entry in entries:
    url = entry['request']['url']
    if 'search' in url or 'api' in url:
        response = entry['response']['content']['text']
        data = json.loads(response)
        print(data)
```

---

## Quick Reference

| Step | Action | Time |
|------|--------|------|
| 1 | Browse target site | 2 min |
| 2 | Open DevTools | 10 sec |
| 3 | Capture traffic | 3 min |
| 4 | Export HAR | 30 sec |
| 5 | Upload to Steve Sie | 1 min |
| 6 | Generate API | 30 sec |
| 7 | Query programmatically | Ongoing |

**Total setup time:** ~7 minutes per site/search

---

## Resources

- **Steve Sie Craigslist:** https://stevesie.com/apps/craigslist-api
- **Steve Sie Reddit:** https://stevesie.com/apps/reddit-api
- **HAR Spec:** http://www.softwareishard.com/blog/har-12-spec/
- **Chrome DevTools:** https://developer.chrome.com/docs/devtools/

---

**Remember:** This is a no-code bridge between manual browsing and programmatic data extraction. Use it to quickly get structured data from sites without official APIs.
