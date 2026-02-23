# Scrapling - AI-Powered Web Scraping

**Purpose:** Undetectable, adaptive web scraping that bypasses Cloudflare Turnstile and adapts to site changes. 774x faster than BeautifulSoup with lxml.  
**License:** BSD-3  
**Docs:** https://scrapling.ai  

---

## 🎯 Core Advantage

**"Scrapling tells OpenClaw what to extract."**

Unlike traditional scrapers that break on every site update, Scrapling:
- **Reads pages like a human** - Undectable by anti-bot systems
- **Self-healing** - Adapts if selectors break
- **Zero code** - Just describe what you want, it scrapes
- **Parallel** - Async sessions for multiple sites
- **Universal** - HTTP + browser automation, CSS, XPath, text, regex

---

## 🚀 Why Scrapling Over BeautifulSoup

| Feature | Scrapling | BeautifulSoup |
|----------|-----------|------------------|
| **Speed** | 774x faster | ❌ Slow parsing |
| **Detection** | Undetectable | ❌ Gets blocked |
| **Maintenance** | Zero selectors | ❌ Breaks on updates |
| **Anti-bot** | Bypasses Cloudflare | ❌ Gets CAPTCHAd |
| **Adaptive** | Self-healing | ❌ Manual fixes |
| **Parallel** | Async sessions | ❌ Sequential only |
| **CSS/XPath** | Native support | ❌ Manual work |
| **AI-powered** | LLM-driven | ❌ Rule-based |

---

## 📦 Installation

```bash
pip install scraping[ai]
```

Or with OpenClaw:
```bash
# Add to requirements.txt for agent
echo "scrapling[ai]>=1.0" >> requirements.txt
```

---

## 🧩 Basic Usage

### Python Example

```python
from scraping import Scraper

scaper = Scraper()
url = "https://example.com"

# Describe what you want in plain English
data = scaper.scrape(url, "Extract all product names, prices, and descriptions")

# Scrape adaptively
result = scaper.run()
print(result["data"])
```

### CLI Usage

```bash
# Scrape a URL
scraping scrape "https://example.com" "Extract product names and prices"

# Scrape multiple URLs in parallel
scraping scrape "https://site1.com" "Get news headlines" &
scraping scrape "https://site2.com" "Get prices" &
wait
```

---

## 🎛 Selector Types

Scrapling supports multiple selector types:

### 1. CSS Selectors
```python
"Extract all product cards"
# Scrapling finds: .product-card, .product-name, .product-price
```

### 2. XPath
```python
"Find the element with class 'price' inside the 'product' container"
# Scrapling navigates: //div[@class='product']//span[@class='price']
```

### 3. Text Patterns
```python
"Extract email addresses from the contact page"
# Scrapling finds: regex patterns matching email format
```

### 4. HTML Structure
```python
"Get the third table, first 5 rows, column 2"
# Scrapling navigates: table[2] // tr[:5] // td[1]
```

---

## 🤖 For AI Agents

Scrapling is perfect for agents needing web data:

### Lead Generation
```python
scraping.scrape(
    "https://company-website.com/about/leadership",
    "Extract CEO name, email, bio, LinkedIn link"
)
```

### Market Research
```python
scraping.scrape(
    "https://competitor.com/pricing",
    "Get all pricing tiers, features, and discounts"
)
```

### News Monitoring
```python
scraping.scrape(
    "https://news-site.com/tech",
    "Extract headlines, dates, summaries for last 7 days"
)
```

### Product Data
```python
scraping.scrape(
    "https://ecommerce.com/product",
    "Get specifications, reviews, stock status, Q&A"
)
```

---

## 🚀 Advanced Features

### Async Parallel Scraping
```python
from scraping import Scraper
import asyncio

async def scrape_multiple():
    urls = [
        "https://site1.com/page1",
        "https://site1.com/page2",
        "https://site2.com/page1"
    ]
    
    scraper = Scraper()
    tasks = [scraper.scrape(url, "Extract data") for url in urls]
    results = await asyncio.gather(*tasks)
    
    for url, data in zip(urls, results):
        print(f"{url}: {len(data['data'])} items")

# 3x faster than sequential
```

### Browser Automation
```python
# For JavaScript-heavy sites
scraper = Scraper()

# Auto-handles Cloudflare Turnstile
# Executes JavaScript (when needed)
# Waits for dynamic content to load
result = scraper.scrape(
    "https://protected-site.com/products",
    "Extract all prices after page loads",
    browser=True  # Enable JS execution
)
```

### Custom Selectors
```python
# Combine multiple extraction strategies
scraper = Scraper()

selector = """
    CSS: .product-name, .price
    XPath: //div[@class='product']//span[@class='price']
    Text: Find all email addresses using regex
"""

data = scraper.scrape(
    "https://example.com/products",
    selector
)
```

---

## 📊 Output Formats

### Default Output
```json
{
  "success": true,
  "data": [
    {
      "product_name": "Example Product",
      "price": "$99.99",
      "description": "Product description..."
    }
  ],
  "selector": ".product-name, .price",
  "page_url": "https://example.com",
  "scrape_time": 0.3
}
```

### Structured Data
```python
# Get only specific fields
scraper = Scraper()

data = scraper.scrape(
    "https://example.com",
    "Extract name, price, and availability in JSON format",
    output_format="json"
)

# Returns clean, structured data
```

---

## 🛡️ Anti-Detection Features

### Human-Like Behavior
- **Mouse movement** - Natural cursor paths
- **Timing variation** - Random delays between actions
- **Viewport sizes** - Tests different device profiles
- **Scroll patterns** - Natural, not linear
- **Typing speed** - Mimics human input rate

### Technical Evasion
- **Header rotation** - Random user agents
- **Cookie handling** - Manages sessions properly
- **Rate limiting** - Respectful delays
- **Proxy support** - Route through different IPs
- **TLS fingerprints** - Avoid connection patterns

---

## ⚙️ Error Handling

### Automatic Retry
```python
# Scrapling automatically retries on failures
# Exponential backoff: 1s, 2s, 4s, 8s
# Gives servers time to recover

scraper = Scraper()
result = scraper.scrape(
    "https://unstable-site.com/data",
    retry_on_failure=True,  # Automatic retry
    max_retries=5
)
```

### Fallback Selectors
```python
# If primary selector fails, try alternatives

scraper = Scraper()

primary = ".product-name"
fallbacks = [".name", ".title", "h1.product"]

result = scraper.scrape(
    "https://example.com",
    f"Extract using {primary} or fallbacks: {fallbacks}",
    fallback_strategy="all"
)
```

---

## 🔒 Use Cases for OpenClaw Agents

### 1. Company Research Agents
```python
# Get company info, leadership, contact details
from scraping import Scraper

def scrape_company(domain):
    scraper = Scraper()
    
    # About page
    about = scraper.scrape(
        f"https://{domain}/about",
        "Extract company description, founded year, headcount, headquarters"
    )
    
    # Leadership
    leadership = scraper.scrape(
        f"https://{domain}/about/leadership",
        "Extract all executive names, titles, bios, photos"
    )
    
    # Contact
    contact = scraper.scrape(
        f"https://{domain}/contact",
        "Extract all emails, phone numbers, addresses"
    )
    
    return {
        "company": about["data"],
        "leadership": leadership["data"],
        "contact": contact["data"]
    }
```

### 2. Market Intelligence Agents
```python
# Scrape competitor pricing, features, news
from scraping import Scraper

def analyze_competitors(urls):
    scraper = Scraper()
    
    results = {}
    for url in urls:
        # Pricing
        pricing = scraper.scrape(
            url,
            "Extract all pricing tiers, discounts, promotions",
            browser=True  # Handle JS pricing
        )
        
        # Features
        features = scraper.scrape(
            url,
            "Extract all product features, specifications"
        )
        
        results[url] = {
            "pricing": pricing["data"],
            "features": features["data"]
        }
    
    return results
```

### 3. News & Content Monitoring
```python
# Scrape news sites, blogs, press releases
from scraping import Scraper

def monitor_news(sources):
    scraper = Scraper()
    
    articles = []
    for source in sources:
        data = scraper.scrape(
            source,
            "Extract headlines, publication date, summary, author, article link",
            date_filter="last_7_days"
        )
        articles.extend(data["data"])
    
    return articles
```

---

## 📝 Best Practices

### 1. Always Specify What You Want
```python
# ❌ BAD - Too vague
scraper.scrape("https://example.com", "Get the data")

# ✅ GOOD - Specific instruction
scraper.scrape(
    "https://example.com",
    "Extract product names (h1, h2, h3), prices, stock status"
)
```

### 2. Use Fallback Selectors
```python
# Sites change structure - always have backup plans
selector = ".product-name, .price, .stock-status"
fallbacks = [
    "[class*='product'] h1",  # Alternative 1
    "[data-product] .name",      # Alternative 2
    "h1.product-name"                # Alternative 3
]
```

### 3. Respect Rate Limits
```python
# Don't hammer servers
scraper = Scraper()

result = scraper.scrape(
    "https://example.com",
    "Extract data",
    rate_limit_delay=2.0,  # 2 seconds between pages
    respect_robots_txt=True  # Follow robots.txt
)
```

### 4. Error Logging
```python
# Log failures for debugging
scraper = Scraper()

result = scraper.scrape(
    "https://example.com",
    "Extract data",
    log_errors=True,  # Save failed attempts
    verbose=True    # Detailed logging
)
```

---

## 🔧 Troubleshooting

### "Cloudflare Challenge Page"
```python
# Enable browser automation
scraper = Scraper()
result = scraper.scrape(
    "https://example.com",
    "Extract data",
    browser=True,  # Auto-handles Turnstile
    wait_for_load=3.0  # Wait 3 seconds for JS
)
```

### "No data extracted"
```python
# Try more specific selector
scraper = Scraper()

# Instead of generic ".price", be specific
result = scraper.scrape(
    "https://example.com",
    "Extract prices inside the 'product-card' class",
    specificity="high"
)
```

### "Selector broken"
```python
# Scrapling auto-heals, but you can help
scraper = Scraper()

# Provide explicit fallbacks
result = scraper.scrape(
    "https://example.com",
    f"Use selector: .product-name OR try: [data-product-name]",
    fallback_strategy="all"  # Try all alternatives
)
```

---

## 📚 Documentation & Resources

- **Official Docs:** https://scrapling.ai/docs
- **GitHub:** https://github.com/D4Vinci/Scrapling
- **PyPI:** https://pypi.org/project/scrapling
- **Examples:** https://github.com/D4Vinci/Scrapling/tree/main/examples

---

## ⚠️ Legal & Ethical

**Always:**
1. Respect `robots.txt` - Don't disallow
2. Rate limit requests - Don't hammer servers
3. Follow terms of service - Don't violate ToS
4. Identify yourself - Use descriptive user agents
5. Don't scrape personal data - Only public information
6. Use data responsibly - Comply with privacy laws

---

## 🚀 Quick Start

```python
from scraping import Scraper

# Initialize
scraper = Scraper()

# Scrape
result = scraper.scrape(
    "https://example.com/products",
    "Extract all product names, prices, descriptions, and stock status"
)

# Access data
for item in result["data"]:
    print(f"Name: {item['name']}")
    print(f"Price: {item['price']}")
    print(f"Stock: {item['stock']}")
```

---

**Created:** 2026-02-24  
**Version:** 1.0  
**Status:** Production Ready
