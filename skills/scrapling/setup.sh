#!/bin/bash
# Scrapling Setup Script for OpenClaw

echo "🧪 Setting up Scrapling AI Web Scraper..."
echo ""

PYTHON_BIN="/opt/venv/bin/python"
SCRAPLING_PATH="/home/node/.openclaw/workspace/scrapling"

# Verify Python exists
if [ ! -x "$PYTHON_BIN" ]; then
    echo "❌ Python environment not found at $PYTHON_BIN"
    exit 1
fi

echo "✅ Python found: $($PYTHON_BIN --version)"
echo ""

echo "📦 Installing Scrapling from local source..."
$PYTHON_BIN -m pip install -e "$SCRAPLING_PATH"

echo ""
echo "🔎 Verifying installation..."

if $PYTHON_BIN -c "import scrapling" &> /dev/null; then
    echo "✅ Scrapling installed successfully!"
    echo ""
    echo "🧪 Running verification test..."
    cd "$(dirname "$0")"
    $PYTHON_BIN simple_test.py
    echo ""
    echo "✅ Setup complete!"
else
    echo "❌ Scrapling installation failed."
    exit 1
fi
