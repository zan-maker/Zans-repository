# Lead Magnets Deployment Guide

## Overview
Deploy the lead magnet system to production with GitHub Pages for static files and VPS for webhook/API processing.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              GITHUB PAGES (Static Hosting)                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │ /wellness-  │ │ /expense-   │ │ /cfo-scorecard/     │   │
│  │ calculator/ │ │ audit/      │ │ index.html          │   │
│  │ index.html  │ │ index.html  │ └─────────────────────┘   │
│  └─────────────┘ └─────────────┘ ┌─────────────────────┐   │
│                                  │ /pe-deal-finder/    │   │
│                                  │ index.html          │   │
│                                  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                     POST /api/submit-lead
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              VPS WEBHOOK SERVER (Node.js)                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  api/webhook-server.js                              │   │
│  │  - Receives form submissions                        │   │
│  │  - Calls Kimi API for validation                    │   │
│  │  - Generates PDF with Puppeteer                     │   │
│  │  - Queues follow-up emails                          │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  api/follow-up-manager.js                           │   │
│  │  - Runs every 2 hours (cron)                        │   │
│  │  - Sends Day 0, 3, 7 emails                         │   │
│  │  - Updates lead status                              │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  data/                                              │   │
│  │  - leads.json (SQLite in future)                    │   │
│  │  - rejected-leads.json                              │   │
│  │  - PDFs generated/                                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                    ┌───────┴───────┐
                    ▼               ▼
            ┌──────────────┐ ┌──────────────┐
            │  Kimi API    │ │ ZeroBounce   │
            │  (Validation)│ │ (Email Verify)│
            └──────────────┘ └──────────────┘
                    │               │
                    └───────┬───────┘
                            ▼
                    ┌──────────────┐
                    │ Agentmail.to │
                    │ (Send Email) │
                    └──────────────┘
```

---

## Step 1: GitHub Pages Setup

### 1.1 Create Repository Structure

```
impactquadrant-lead-magnets/
├── index.html              # Landing page with links to all calculators
├── wellness-calculator/
│   └── index.html
├── expense-audit/
│   └── index.html
├── cfo-scorecard/
│   └── index.html
├── pe-deal-finder/
│   └── index.html
├── assets/
│   ├── css/
│   └── js/
│       └── alpine.min.js
└── .github/
    └── workflows/
        └── deploy.yml
```

### 1.2 GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 1.3 Enable GitHub Pages

1. Go to Repository Settings → Pages
2. Source: GitHub Actions
3. Branch: main
4. Domain: www.impactquadrant.info (custom domain)

---

## Step 2: VPS Webhook Server Setup

### 2.1 Prerequisites

```bash
# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 for process management
sudo npm install -g pm2

# Install Chrome dependencies for Puppeteer
sudo apt-get install -y \
  ca-certificates \
  fonts-liberation \
  libappindicator3-1 \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libc6 \
  libcairo2 \
  libcups2 \
  libdbus-1-3 \
  libexpat1 \
  libfontconfig1 \
  libgbm1 \
  libgcc1 \
  libglib2.0-0 \
  libgtk-3-0 \
  libnspr4 \
  libnss3 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libstdc++6 \
  libx11-6 \
  libx11-xcb1 \
  libxcb1 \
  libxcomposite1 \
  libxcursor1 \
  libxdamage1 \
  libxext6 \
  libxfixes3 \
  libxi6 \
  libxrandr2 \
  libxrender1 \
  libxss1 \
  libxtst6 \
  lsb-release \
  wget \
  xdg-utils
```

### 2.2 Deploy Application

```bash
# Clone repository
cd /var/www
git clone https://github.com/YOUR_USERNAME/impactquadrant-lead-magnets.git
cd impactquadrant-lead-magnets

# Install dependencies
npm install

# Create data directory
mkdir -p data

# Set environment variables
cat > .env << EOF
KIMI_API_KEY=${KIMI_API_KEY}
ZEROBOUNCE_API_KEY=${ZEROBOUNCE_API_KEY}
AGENTMAIL_ZANE_KEY=${AGENTMAIL_ZANE_KEY}
AGENTMAIL_ZANDER_KEY=${AGENTMAIL_ZANDER_KEY}
WEBHOOK_PORT=3000
NODE_ENV=production
EOF

# Start with PM2
pm2 start api/webhook-server.js --name lead-magnets-api
pm2 startup
pm2 save
```

### 2.3 Nginx Reverse Proxy

Create `/etc/nginx/sites-available/lead-magnets`:

```nginx
server {
    listen 80;
    server_name api.impactquadrant.info;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/lead-magnets /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2.4 SSL with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.impactquadrant.info
```

---

## Step 3: Environment Variables

Create `.env` file on VPS:

```bash
# API Keys (from TOOLS.md)
KIMI_API_KEY=sk-...
ZEROBOUNCE_API_KEY=fd0105c8c98340e0a2b63e2fbe39d7a4
AGENTMAIL_ZANE_KEY=am_800b9649c9b5919fe722634e153074fd921b88deab8d659fe6042bb4f6bc1a68
AGENTMAIL_ZANDER_KEY=am_77026a53e8d003ce63a3187d06d61e897ee389b9ec479d50bdaeefeda868b32f

# Server Config
WEBHOOK_PORT=3000
NODE_ENV=production

# Optional: Sentry for error tracking
SENTRY_DSN=...
```

---

## Step 4: Cron Job Setup

The follow-up manager is already scheduled via OpenClaw cron:
- **Job ID:** `5988d24a-0dc7-4535-80ea-6b78d8b049ce`
- **Schedule:** Every 2 hours
- **Command:** `cd /var/www/impactquadrant-lead-magnets && node api/follow-up-manager.js`

---

## Step 5: DNS Configuration

### 5.1 DNS Records

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_VPS_IP | 3600 |
| A | www | YOUR_VPS_IP | 3600 |
| A | api | YOUR_VPS_IP | 3600 |
| CNAME | _github-pages-challenge | _github-pages-challenge-impactquadrant.impactquadrant.info | 3600 |

### 5.2 GitHub Custom Domain

1. Add `CNAME` file to repo root with `www.impactquadrant.info`
2. Enable HTTPS in GitHub Pages settings

---

## Step 6: Testing

### 6.1 Test Local

```bash
cd lead-magnets
npm start

# Test submission
curl -X POST http://localhost:3000/api/submit-lead \
  -H "Content-Type: application/json" \
  -d '{
    "service": "wellness-125",
    "companyName": "Test Company",
    "employeeCount": 50,
    "monthlyBenefitsCost": 200,
    "calculatedSavings": 64260,
    "contactName": "Test User",
    "email": "test@example.com"
  }'
```

### 6.2 Test Production

1. Visit: `https://www.impactquadrant.info/wellness-calculator/`
2. Submit test data
3. Check: 
   - PDF generated in `data/report-{id}.pdf`
   - Lead saved in `data/leads.json`
   - Email queued in `data/emails/{id}/`

---

## Step 7: Monitoring

### 7.1 PM2 Monitoring

```bash
pm2 monit              # Real-time monitoring
pm2 logs lead-magnets-api  # View logs
pm2 restart lead-magnets-api  # Restart
```

### 7.2 Log Files

- Application: `~/.pm2/logs/lead-magnets-api-out.log`
- Errors: `~/.pm2/logs/lead-magnets-api-error.log`
- Leads: `/var/www/impactquadrant-lead-magnets/data/leads.json`

### 7.3 Health Check

Add endpoint to webhook-server.js:

```javascript
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    version: process.env.npm_package_version
  });
});
```

Test: `curl https://api.impactquadrant.info/health`

---

## Step 8: Backup Strategy

### 8.1 Automated Backups

Create `/var/www/backup-script.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/lead-magnets"
mkdir -p $BACKUP_DIR

# Backup data
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /var/www/impactquadrant-lead-magnets/data/

# Keep only last 30 backups
ls -t $BACKUP_DIR/*.tar.gz | tail -n +31 | xargs rm -f
```

Add to crontab:
```bash
0 2 * * * /var/www/backup-script.sh
```

### 8.2 Git Backup

```bash
cd /var/www/impactquadrant-lead-magnets
git add data/leads.json
git commit -m "Backup leads $(date +%Y-%m-%d)"
git push origin main
```

---

## Troubleshooting

### Issue: Puppeteer fails to launch

```bash
# Reinstall with proper flags
npm uninstall puppeteer
npm install puppeteer --save

# Or use bundled Chrome
PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
```

### Issue: CORS errors from GitHub Pages

Update webhook-server.js CORS config:

```javascript
app.use(cors({
  origin: ['https://www.impactquadrant.info', 'https://impactquadrant.github.io'],
  methods: ['POST', 'GET'],
  allowedHeaders: ['Content-Type']
}));
```

### Issue: High memory usage

Add to PM2 config:

```bash
pm2 start api/webhook-server.js --name lead-magnets-api --max-memory-restart 512M
```

---

## Cost Summary

| Component | Monthly Cost | Annual Cost |
|-----------|--------------|-------------|
| GitHub Pages | $0 | $0 |
| VPS (1GB RAM) | $5 | $60 |
| Domain | $12/year | $12 |
| **Total** | **$5/mo** | **$72/year** |

**vs. SaaS Alternative:** $60/mo = $720/year

**Annual Savings: $648**

---

## Next Steps

1. [ ] Set up GitHub repository
2. [ ] Configure GitHub Pages
3. [ ] Deploy to VPS
4. [ ] Configure DNS
5. [ ] Test end-to-end
6. [ ] Set up monitoring
7. [ ] Configure backups
8. [ ] Document in MEMORY.md
