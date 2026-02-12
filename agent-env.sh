#!/bin/bash
# OpenClaw Agent Environment Configuration
# Source this file to set API keys for sub-agents: source ~/.openclaw/agent-env.sh

# Model APIs
export KIMI_API_KEY="${KIMI_API_KEY:-}"
export NVIDIA_API_KEY="${NVIDIA_API_KEY:-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}"
export ZAI_API_KEY="${ZAI_API_KEY:-}"

# Search APIs (Required for LeadGenerator, TradeRecommender, MiningMetalsAnalyst)
export BRAVE_API_KEY="${BRAVE_API_KEY:-BSAqx7g5ob7ymEOAUfRduTetIOWPalN}"
export TAVILY_API_KEY="${TAVILY_API_KEY:-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}"

# Data Enrichment
export HUNTER_API_KEY="${HUNTER_API_KEY:-f701d171cf7decf7e730a6b1c6e9b74f29f39b6e}"
export ABSTRACT_API_KEY="${ABSTRACT_API_KEY:-38aeec02e6f6469983e0856dfd147b10}"
export ZYTE_API_KEY="${ZYTE_API_KEY:-8d3e9c7af6e948b088e96ad15ca21719}"

# News (for LeadGenerator)
export NEWSAPI_KEY="${NEWSAPI_KEY:-}"

# Email
export EMAIL_PASSWORD="${EMAIL_PASSWORD:-cqma sflq nsfv itke}"

# SkillsMP
export SKILLSMP_API_KEY="${SKILLSMP_API_KEY:-sk_live_skillsmp_4PsNNxq_MEZuoIp4ATK9qzVc5_DS840ypPxOQO0QgfQ}"

echo "✅ Agent environment loaded"
echo "Available APIs: Brave Search, Tavily, Hunter.io, Abstract, Zyte, SkillsMP"
