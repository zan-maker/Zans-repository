# ImpactQuadrant Lead Magnet System

AI-powered lead generation system replacing $60/month in SaaS tools with open-source alternatives.

## 🎯 Lead Magnets

### 1. Wellness 125 Calculator
**URL:** `/wellness-calculator/index.html`
- Section 125 Cafeteria Plan savings calculator
- FICA tax reduction analysis
- Employee benefit cost estimator
- **Target:** HR managers, CFOs at 20+ employee companies

### 2. Expense Reduction Audit
**URL:** `/expense-audit/index.html`
- SaaS spend optimization
- Vendor contract analysis
- Travel & telecom cost reduction
- **Target:** CFOs, Finance Directors, Controllers

### 3. CFO Financial Health Scorecard
**URL:** `/cfo-scorecard/index.html`
- 4-category financial assessment
- Profitability, cash flow, working capital, growth readiness
- Industry benchmark comparison
- **Target:** CFOs, Finance VPs, Controllers

### 4. PE Deal Finder
**URL:** `/pe-deal-finder/index.html`
- Business valuation estimator (EBITDA/SDE multiples)
- Buyer match algorithm
- Industry comparables
- **Target:** Business owners, founders considering exit

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GITHUB PAGES (Static)                    │
│  - HTML + Tailwind CSS + Alpine.js                          │
│  - No server-side rendering needed                         │
│  - CDN-served for fast global access                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼ Webhook POST
┌─────────────────────────────────────────────────────────────┐
│                VPS WEBHOOK SERVER (Node.js)                 │
│  - Receives form submissions                               │
│  - Validates with Kimi API                                 │
│  - Generates PDFs with Puppeteer                           │
│  - Queues follow-up emails                                 │
└─────────────────────────┬───────────────────────────────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
      ┌─────────┐   ┌─────────┐   ┌─────────┐
      │  Kimi   │   │   PDF   │   │  Email  │
      │   API   │   │Generator│   │ Queue   │
      └─────────┘   └─────────┘   └─────────┘
```

## 📁 File Structure

```
lead-magnets/
├── wellness-calculator/
│   └── index.html          # Wellness 125 form
├── expense-audit/
│   └── index.html          # Expense reduction form
├── cfo-scorecard/
│   └── index.html          # Financial health scorecard
├── pe-deal-finder/
│   └── index.html          # Business valuation tool
├── api/
│   ├── webhook-server.js   # Express server for submissions
│   ├── process-submission.js  # Main processing logic
│   └── follow-up-manager.js   # Email queue manager
├── data/                   # Lead storage (JSON)
├── deploy.sh               # Deployment script
└── .github/workflows/
    └── deploy.yml          # GitHub Actions CI/CD
```

## 🚀 Deployment

### Option 1: Manual Deployment
```bash
cd lead-magnets
./deploy.sh
```

This will:
1. Build static files
2. Deploy to GitHub Pages
3. Start webhook server on VPS

### Option 2: GitHub Actions (Automatic)
Push to `main` branch triggers automatic deployment.

### Webhook Server Management
```bash
# Start server
cd lead-magnets && node api/webhook-server.js

# Or use PM2 for production
pm2 start api/webhook-server.js --name lead-magnets

# Check status
pm2 status

# View logs
pm2 logs lead-magnets
```

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```bash
# Kimi API (for validation)
KIMI_API_KEY=your_kimi_key

# ZeroBounce (email verification)
ZEROBOUNCE_API_KEY=your_zerobounce_key

# Agentmail.to (email sending)
AGENTMAIL_ZANE_KEY=your_zane_key
AGENTMAIL_ZANDER_KEY=your_zander_key

# Server config
WEBHOOK_PORT=3000
DATA_DIR=./data
```

### Domain Setup
For custom domain (e.g., `tools.impactquadrant.info`):
1. Add CNAME record pointing to `cubiczan.github.io`
2. Create `CNAME` file in repo with your domain
3. Enable HTTPS in GitHub Pages settings

## 📊 Lead Processing Flow

```
1. User submits form
        ↓
2. Webhook receives POST
        ↓
3. Kimi API validates submission
   ├─ Valid → Continue
   └─ Invalid → Save to rejected-leads.json
        ↓
4. Generate PDF report
        ↓
5. Save lead to leads.json
        ↓
6. Queue follow-up emails
   ├─ Immediate: PDF delivery
   ├─ Day 3: Case study + social proof
   └─ Day 7: CTA with calendar link
        ↓
7. Cron job sends emails (every 2 hours)
   ├─ Verify with ZeroBounce
   ├─ Send via Agentmail.to
   └─ Update lead status
```

## 🔄 Cron Jobs

### Follow-Up Manager
**Schedule:** Every 2 hours
**Job ID:** `5988d24a-0dc7-4535-80ea-6b78d8b049ce`

Checks for leads needing:
- Day 0 (immediate): PDF delivery
- Day 3: Educational content
- Day 7: Call-to-action

## 💰 Cost Savings

| Tool | Replaced | Monthly Cost |
|------|----------|--------------|
| Lovable | Custom HTML | $20 |
| n8n | OpenClaw Cron | $20 |
| ChatGPT Plus | Kimi API | $20 |
| **Total** | | **$60/month** |
| **Annual Savings** | | **$720** |

## 🛡️ Security

- ✅ Kimi API validation filters spam/test data
- ✅ ZeroBounce email verification before sending
- ✅ No sensitive data in client-side code
- ✅ Environment variables for API keys
- ✅ Rejected leads saved for analysis

## 📈 Analytics

Track lead metrics in `data/leads.json`:
- Total submissions
- Conversion by lead magnet
- Email open rates (via Agentmail.to)
- PDF download tracking

## 📝 API Endpoints

### Submit Lead
```bash
POST /api/submit-lead
Content-Type: application/json

{
  "service": "wellness-125",
  "companyName": "Acme Corp",
  "employeeCount": 50,
  "email": "contact@acme.com",
  ...
}
```

### Response
```json
{
  "success": true,
  "leadId": "1234567890",
  "pdfUrl": "/data/report-1234567890.pdf",
  "message": "Lead processed successfully"
}
```

## 🎨 Customization

### Adding New Lead Magnet
1. Create `new-service/index.html`
2. Add to `deploy.sh` build step
3. Update GitHub Actions workflow
4. Add to main index page

### Modifying PDF Template
Edit `generatePDFTemplate()` in `api/process-submission.js`:
- Service-specific colors
- Branded headers
- Custom sections

## 🐛 Troubleshooting

### Webhook server not starting
```bash
# Check port availability
lsof -i :3000

# Kill existing process
kill $(cat webhook.pid)

# Restart
node api/webhook-server.js
```

### PDF generation failing
```bash
# Install Puppeteer dependencies
npm install

# Check Chrome/Chromium
node -e "console.log(require('puppeteer').executablePath())"
```

### GitHub Pages 404
- Ensure `gh-pages` branch exists
- Check repository Settings > Pages
- Verify CNAME file if using custom domain

## 📞 Support

**Email:** sam@impactquadrant.info
**Webhook:** http://localhost:3000/api/submit-lead
**Cron Status:** Check OpenClaw admin panel

## 📄 License

Private - ImpactQuadrant internal use only
