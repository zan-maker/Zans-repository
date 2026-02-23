#!/bin/bash
# Setup script for Chatterbox TTS Integration
# Resemble AI Open Source Text-to-Speech

set -e

echo "=========================================="
echo "Chatterbox TTS Setup"
echo "Resemble AI Open Source Voice AI"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}Step 1: Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${GREEN}✅ Python 3.8+ detected${NC}"
else
    echo "❌ Python 3.8+ required"
    exit 1
fi

echo ""
echo -e "${BLUE}Step 2: Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️ Virtual environment already exists${NC}"
fi

echo ""
echo -e "${BLUE}Step 3: Activating virtual environment...${NC}"
source venv/bin/activate

echo ""
echo -e "${BLUE}Step 4: Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo -e "${BLUE}Step 5: Checking for GPU...${NC}"
if python3 -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
    gpu_name=$(python3 -c "import torch; print(torch.cuda.get_device_name(0))")
    echo -e "${GREEN}✅ GPU detected: $gpu_name${NC}"
    echo "   Chatterbox will use CUDA for faster inference"
else
    echo -e "${YELLOW}⚠️ No GPU detected - will use CPU${NC}"
    echo "   Inference will be slower but still functional"
fi

echo ""
echo -e "${BLUE}Step 6: Creating output directory...${NC}"
mkdir -p output
mkdir -p voices

echo ""
echo -e "${BLUE}Step 7: Checking for Resemble API key (optional)...${NC}"
if [ -z "$RESEMBLE_API_KEY" ]; then
    echo -e "${YELLOW}⚠️ RESEMBLE_API_KEY not set${NC}"
    echo "   Set it with: export RESEMBLE_API_KEY='your_key'"
    echo "   Get key at: https://www.resemble.ai/"
    echo "   (Only needed for API fallback mode)"
else
    echo -e "${GREEN}✅ RESEMBLE_API_KEY found${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup complete!${NC}"
echo "=========================================="
echo ""
echo "Quick start:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run test: python chatterbox_tts.py"
echo "  3. See examples/: for usage patterns"
echo ""
echo "Model downloads happen on first use (~2-3GB)"
echo "Models are cached in: ~/.cache/huggingface/"
echo ""
