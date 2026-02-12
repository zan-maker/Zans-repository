# Cron Job File-Based Delivery System

**Implemented:** 2026-02-12
**Purpose:** Reliable delivery of sub-agent outputs via file-based workflow

## Problem
Sub-agent cron jobs were running successfully but failing to deliver to Discord (`"cron announce delivery failed"`). Isolated sessions cannot use the `announce` delivery mode.

## Solution
File-based delivery with publisher cron job.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Sub-Agent Cron │────▶│  Output File     │────▶│  Publisher Cron │────▶ Discord
│  (Isolated)     │     │  (Markdown)      │     │  (Main Session) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
     5:30 PM EST             Write to file            11:35 PM EST
     11:05 PM EST                                    (reads + posts)
     12:15 AM EST
```

## Workflow

### 1. Sub-Agent Execution (Isolated Sessions)
Each agent runs at scheduled time and writes output to file:

| Agent | Schedule (EST) | Output File |
|-------|---------------|-------------|
| TradeRecommender | 5:30 PM | `cron-output/trade-recommender/YYYY-MM-DD.md` |
| MiningMetalsAnalyst | 11:05 PM | `cron-output/mining-metals-analyst/YYYY-MM-DD.md` |
| LeadGenerator | 12:15 AM | `cron-output/lead-generator/YYYY-MM-DD.md` |

### 2. Publisher Execution (Main Session)
- **Schedule:** 11:35 PM EST (after TradeRecommender + buffer)
- **Task:** Reads all output files from today
- **Action:** Posts contents to `#cron-output` Discord channel
- **Delivery Mode:** Can use Discord (main session has channel access)

## File Structure

```
cron-output/
├── trade-recommender/
│   ├── 2026-02-11.md
│   ├── 2026-02-12.md
│   └── ...
├── mining-metals-analyst/
│   ├── 2026-02-11.md
│   ├── 2026-02-12.md
│   └── ...
└── lead-generator/
    ├── 2026-02-11.md
    ├── 2026-02-12.md
    └── ...
```

## Updates Made

### Cron Jobs Modified
1. Changed `delivery.mode` from `"announce"` to `"none"`
2. Updated agent prompts to write to specific file paths
3. Adjusted schedules to prevent collisions
4. Added standardized output templates

### New Cron Job Added
- **Name:** Cron Output Publisher
- **ID:** d2b877c9-ac24-43c7-a3b5-7f9c210a8938
- **Schedule:** 11:35 PM EST daily
- **Function:** Reads files and posts to Discord

### Agent Instructions Updated
Each agent now receives explicit instructions:
- Where to write output (`cron-output/<agent>/YYYY-MM-DD.md`)
- File format (Markdown with headers)
- Required sections (varies by agent)

## Benefits

1. **Reliable:** No dependency on sub-agent Discord delivery
2. **Persistent:** Files serve as archive/searchable history
3. **Debuggable:** Can inspect output before/after posting
4. **Flexible:** Publisher can format/filter before posting
5. **Scalable:** Easy to add more agents or outputs

## Next Runs

| Agent | Date | Time (EST) |
|-------|------|-----------|
| TradeRecommender | Tonight | 5:30 PM |
| Publisher | Tonight | 11:35 PM |
| MiningMetalsAnalyst | Tonight | 11:05 PM |
| LeadGenerator | Tomorrow | 12:15 AM |

## Monitoring

Check `#cron-output` channel after 11:35 PM EST for daily reports.

If no output appears:
1. Check `cron-output/` directory for files
2. Verify cron job status with `openclaw cron list`
3. Check session logs if files exist but weren't posted
