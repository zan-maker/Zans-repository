#!/bin/bash
# deploy.sh - Deploy lead magnets to GitHub Pages and start webhook server

set -e

echo "🚀 Starting deployment..."

# Configuration
REPO_URL="https://github.com/cubiczan/lead-magnets.git"
DEPLOY_BRANCH="gh-pages"
WEBHOOK_PORT="3000"
WEBHOOK_DIR="/home/node/.openclaw/workspace/lead-magnets"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Building static files...${NC}"

# Create dist directory
mkdir -p dist

# Copy all lead magnet HTML files
cp wellness-calculator/index.html dist/wellness-125.html
cp expense-audit/index.html dist/expense-reduction.html
cp cfo-scorecard/index.html dist/cfo-scorecard.html
cp pe-deal-finder/index.html dist/pe-deal-finder.html

# Create index page with links
cat > dist/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ImpactQuadrant - Lead Magnets</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-gray-50 min-h-screen">
    <header class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-12">
        <div class="max-w-4xl mx-auto px-4 text-center">
            <h1 class="text-4xl font-bold mb-2">ImpactQuadrant</h1>
            <p class="text-xl opacity-90">Business Growth Tools & Resources</p>
        </div>
    </header>
    
    <main class="max-w-4xl mx-auto px-4 py-12">
        <div class="grid md:grid-cols-2 gap-6">
            <a href="wellness-125.html" class="block bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
                <div class="text-3xl mb-3">🏥</div>
                <h2 class="text-xl font-bold text-gray-800 mb-2">Wellness 125 Calculator</h2>
                <p class="text-gray-600">Calculate FICA tax savings with Section 125 cafeteria plans</p>
            </a>
            
            <a href="expense-reduction.html" class="block bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
                <div class="text-3xl mb-3">💰</div>
                <h2 class="text-xl font-bold text-gray-800 mb-2">Expense Reduction Audit</h2>
                <p class="text-gray-600">Identify savings across SaaS, vendors, and operational costs</p>
            </a>
            
            <a href="cfo-scorecard.html" class="block bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
                <div class="text-3xl mb-3">📊</div>
                <h2 class="text-xl font-bold text-gray-800 mb-2">CFO Financial Health Scorecard</h2>
                <p class="text-gray-600">Comprehensive assessment of financial readiness for growth</p>
            </a>
            
            <a href="pe-deal-finder.html" class="block bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
                <div class="text-3xl mb-3">💼</div>
                <h2 class="text-xl font-bold text-gray-800 mb-2">PE Deal Finder</h2>
                <p class="text-gray-600">Business valuation and connection with qualified buyers</p>
            </a>
        </div>
    </main>
    
    <footer class="bg-gray-800 text-gray-400 py-8 text-center">
        <p>© 2026 ImpactQuadrant. All rights reserved.</p>
    </footer>
</body>
</html>
EOF

echo -e "${GREEN}✓ Static files built${NC}"

echo -e "${YELLOW}Step 2: Deploying to GitHub Pages...${NC}"

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not a git repository${NC}"
    echo "Please run: git init && git remote add origin $REPO_URL"
    exit 1
fi

# Deploy to gh-pages branch
if git ls-remote --exit-code origin gh-pages 2>/dev/null; then
    echo "Updating existing gh-pages branch..."
    git checkout gh-pages || git checkout -b gh-pages
    git rm -rf .
else
    echo "Creating new gh-pages branch..."
    git checkout --orphan gh-pages
    git rm -rf .
fi

# Copy dist files to root
cp -r dist/* .

# Commit and push
git add .
git commit -m "Deploy lead magnets - $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
git push origin gh-pages --force

echo -e "${GREEN}✓ Deployed to GitHub Pages${NC}"
echo -e "${GREEN}  URL: https://cubiczan.github.io/lead-magnets/${NC}"

# Return to main branch
git checkout main 2>/dev/null || git checkout master 2>/dev/null || echo "Staying on gh-pages"

echo -e "${YELLOW}Step 3: Starting webhook server...${NC}"

# Check if webhook server is already running
if pgrep -f "webhook-server.js" > /dev/null; then
    echo -e "${YELLOW}Webhook server already running${NC}"
else
    echo "Starting webhook server on port $WEBHOOK_PORT..."
    cd "$WEBHOOK_DIR"
    nohup node api/webhook-server.js > webhook.log 2>&1 &
    echo $! > webhook.pid
    sleep 2
    
    if pgrep -f "webhook-server.js" > /dev/null; then
        echo -e "${GREEN}✓ Webhook server started${NC}"
        echo -e "${GREEN}  PID: $(cat webhook.pid)${NC}"
        echo -e "${GREEN}  Port: $WEBHOOK_PORT${NC}"
    else
        echo -e "${RED}✗ Failed to start webhook server${NC}"
        echo "Check webhook.log for errors"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}🎉 Deployment complete!${NC}"
echo ""
echo "Public URLs:"
echo "  Main:     https://cubiczan.github.io/lead-magnets/"
echo "  Wellness: https://cubiczan.github.io/lead-magnets/wellness-125.html"
echo "  Expense:  https://cubiczan.github.io/lead-magnets/expense-reduction.html"
echo "  CFO:      https://cubiczan.github.io/lead-magnets/cfo-scorecard.html"
echo "  PE Deal:  https://cubiczan.github.io/lead-magnets/pe-deal-finder.html"
echo ""
echo "Webhook: http://localhost:$WEBHOOK_PORT/api/submit-lead"
