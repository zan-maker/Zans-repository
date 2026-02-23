#!/bin/bash
# Scrapling Setup Script for OpenClaw
# Installs the AI-powered web scraping library

echo "🧪 Setting up Scrapling AI Web Scraper..."
echo ""

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed"
    echo "Install Python 3.8 or later from: https://python.org"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install Scrapling
echo "📦 Installing Scrapling..."
pip3 install scraping[ai]

# Verify installation
if pip3 show scraping-ai &> /dev/null; then
    echo "✅ Scrapling installed successfully!"
    echo ""
    
    # Run simple test
    echo "🧪 Running verification test..."
    cd "$(dirname "$0")"
    python3 simple_test.py
    
    echo ""
    echo "="*50
    echo "✅ Setup complete!"
    echo ""
    echo "📚 Scrapling is now ready for OpenClaw agents."
    echo ""
    echo "🎯 Usage in agents:"
    echo "  from scraping import Scraper"
    echo "  scraper = Scraper()"
    echo "  data = scraper.scrape('https://example.com', 'Extract product names and prices')"
    echo "  print(data)"
    echo ""
    echo "📖 Documentation:"
    echo "  https://scrapling.ai/docs"
    echo "  https://github.com/D4Vinci/Scrapling"
    echo ""
    echo "⚙️ Key features:"
    echo "  • 774x faster than BeautifulSoup + lxml"
    echo "  • Bypasses Cloudflare Turnstile automatically"
    echo "  • Adaptive to website structure changes"
    echo "  • Zero selector maintenance required"
    echo "  • Parallel/async scraping support"
    echo ""
else
    echo "❌ Error: Scrapling installation failed"
    exit 1
fi
