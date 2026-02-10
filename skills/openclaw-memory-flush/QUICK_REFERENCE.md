# OpenClaw Memory Flush & Agent Memory Architecture

**Source:** Comprehensive guide from JIN (Medium, Feb 2026)  
**File:** `skills/openclaw-memory-flush/REFERENCE.md`

---

## Quick Reference

### The Core Insight
> Bigger windows don't solve the compression problem; they only delay it.

**Traditional:** Context fills → summarize → hope nothing critical lost  
**OpenClaw:** Context fills → **save critical to disk** → then summarize safely

### Two-Layer Memory Architecture

```
~/.openclaw/workspace/
├── MEMORY.md              # Layer 2: Curated profile (long-term)
└── memory/
    ├── 2026-02-10.md      # Layer 1: Today's daily log
    ├── 2026-02-09.md      # Yesterday's log
    └── ...
```

| Layer | Purpose | Content |
|-------|---------|---------|
| **Daily Notes** | Journal | Temporal events, decisions, errors |
| **MEMORY.md** | Profile | Durable knowledge, preferences, patterns |

### Pre-Compaction Memory Flush

**How it works:**
1. Token estimate crosses threshold (e.g., 176K of 200K)
2. System triggers: "Store durable memories now"
3. Agent writes to `memory/YYYY-MM-DD.md`
4. Returns `NO_REPLY` (invisible to user)
5. Compaction proceeds safely

**Configuration:**
```json
{
  "compaction": {
    "reserveTokensFloor": 20000,
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 4000
    }
  }
}
```

### Context Engineering Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Reduction** | High recency, low density | Compress old conversation turns |
| **Offloading** | High density, low recency | Save 50-page paper to disk, keep reference |
| **Isolation** | Large scope, specialized | Delegate search to sub-agent |
| **Memory Flush** | Critical facts, any age | Persist decisions to disk before compaction |

### Long-Term Memory Solutions Comparison

| System | LoCoMo Score | Latency | Best For |
|--------|-------------|---------|----------|
| **Mem0** | 67% | 1.44s p95 | Managed service, cost/accuracy balance |
| **Letta** | 74% | Varies | Full control, self-hosted |
| **OpenClaw Native** | — | Fast | Simple setups, local control |
| **MemoryOS** | 49% F1 | Moderate | Multi-session workflows |

### Cost Model (10K DAU × 5 queries/day)

| Approach | Monthly Cost |
|----------|-------------|
| Stateless | ~$7,500 |
| Basic memory (Mem0) | ~$26,250 |
| Full context replay | ~$262,500 |

### Writing Effective Memory

**Do:**
- Tell agent explicitly: "Remember our API uses Rust"
- Keep MEMORY.md curated and calm
- Let daily logs be messy
- Use section headers and cross-references
- Commit to git for version control

**Don't:**
- Store credentials in memory files (plain text!)
- Rely solely on summarization
- Ignore pre-compaction flush

### Diagnostics

**Agent "forgot" something?**
1. Same session? → Check if compaction ran, flush was enabled
2. Different session? → Was it written to MEMORY.md or daily log?
3. Used /new or /reset? → Flush doesn't cover manual resets
4. Cross-device? → Native memory is local-only

### Key Takeaways

1. **Persistence over compression** — save before summarizing
2. **Hybrid approaches win** — layer short, long, and external memory
3. **Infrastructure matters** — latency/cost dominate UX
4. **Simplicity scales** — start simple, optimize when metrics demand

---

## Full Reference

See complete guide at: `skills/openclaw-memory-flush/REFERENCE.md`

**Includes:**
- Detailed architecture explanations
- Configuration examples
- Plugin landscape (Mem0, Cognee, QMD)
- Known gaps and workarounds
- Operational best practices
- Cost/latency/accuracy tradeoffs
