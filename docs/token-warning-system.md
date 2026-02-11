# Token Limit Early Warning System

## Purpose
Alert before hitting model context limits so you can start a new thread proactively.

## Current Model Limits

| Model | Context Window | 75% Warning | 90% Critical |
|-------|---------------|-------------|--------------|
| Kimi K2.5 | 256K tokens | 192K | 230K |
| ZAI GLM-4.7 | 128K tokens | 96K | 115K |

## How It Works

### Automatic Monitoring
I will append a token status line to my responses when usage exceeds thresholds:

- **🟡 Yellow:** >75% of context window — consider wrapping up or starting new thread
- **🔴 Red:** >90% of context window — start new thread recommended

### Manual Check
Use `/status` anytime to see current session usage.

## Best Practices

1. **Long research tasks:** Start fresh thread per major topic
2. **Multi-step coding:** New thread per feature/module
3. **Document analysis:** New thread per document

## Proactive Strategy

When you see 🟡 or 🔴:
1. Let me summarize current progress
2. Copy key context you need carried forward
3. Start new thread with: "Continuing from [summary]..."

---
*Created: 2026-02-11*
