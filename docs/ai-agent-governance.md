# AI Agent Governance Framework

*Committed: 2026-02-11*
*Purpose: Operational standards for agent behavior, data quality, tool access, and AI engineering*

---

## 1. Data Governance

### 1.1 Data Freshness & Latency SLAs

| Data Type | Max Age | Target Latency | Source |
|-----------|---------|----------------|--------|
| Market data (Kalshi) | 5 minutes | <2s | Kalshi API |
| News/Signals | 15 minutes | <5s | NewsAPI, web search |
| Company intelligence | 24 hours | <10s | Hunter.io, Abstract API |
| Mining listings | 24 hours | <15s | minelistings.com, web crawl |
| Financial metrics | 1 hour | <3s | Internal calculations |

### 1.2 Data Quality - Six Dimensions

| Dimension | Definition | SLA Target | Monitoring |
|-----------|------------|------------|------------|
| **Accuracy** | Data matches ground truth | >95% | Spot-check against sources |
| **Completeness** | All required fields present | >98% | Null value monitoring |
| **Consistency** | No contradictions across sources | >99% | Cross-reference validation |
| **Timeliness** | Data age within acceptable limits | 100% within SLA | Timestamp validation |
| **Validity** | Format/schema compliance | >99% | Schema validation on ingest |
| **Uniqueness** | No duplicate records | >99% | Deduplication checks |

**Downtime Budget:** <4 hours/month (<0.5%)
**Average Resolution Time:** <30 minutes for P0, <2 hours for P1

---

## 2. IT Tool Governance

### 2.1 Approved Tools & Services

| Tool | Purpose | Agent Access | Status |
|------|---------|--------------|--------|
| **Brave Search API** | Web search, news | All agents | ✅ Approved |
| **Tavily API** | Web search (backup) | All agents | ✅ Approved |
| **Hunter.io** | Email finding | LeadGenerator only | ✅ Approved |
| **Abstract API** | Company enrichment | LeadGenerator only | ✅ Approved |
| **Zyte API** | Web scraping | MiningMetalsAnalyst | ✅ Approved |
| **Kalshi API** | Prediction markets | TradeRecommender | ✅ Approved |
| **DefeatBeta** | Signal generation | TradeRecommender | ✅ Approved |
| **NewsAPI** | News aggregation | LeadGenerator | ✅ Approved |
| **SkillsMP** | Skill marketplace | Zan (orchestrator) | ✅ Approved |

### 2.2 Authentication & Authorization

| Mechanism | Tools Using | Rotation Schedule |
|-----------|-------------|-------------------|
| **API Keys** | All external tools | Monthly |
| **Environment Variables** | Key storage | N/A (runtime injection) |
| **Service Accounts** | N/A (direct API keys) | N/A |
| **RBAC** | Internal file system | Workspace-based |

**Key Storage:** `~/.openclaw/` with 700 permissions
**Rotation Owner:** Sam (human-in-the-loop)
**Exposure Response:** Immediate rotation + audit log

### 2.3 Rate Limits & Concurrency

| Tool | Rate Limit | Quota | Max Concurrent | Backoff Strategy |
|------|------------|-------|----------------|------------------|
| Brave Search | 2000/month | 2000/mo | 5 | Exponential (1s, 2s, 4s) |
| Tavily | 1000/month | 1000/mo | 3 | Exponential (2s, 4s, 8s) |
| Hunter.io | 500/month | 500/mo | 2 | Linear (5s intervals) |
| Abstract API | 500/month | 500/mo | 2 | Linear (3s intervals) |
| Zyte API | 1000/month | 1000/mo | 3 | Exponential (1s, 2s, 4s) |
| Kalshi API | 100/minute | Unlimited | 10 | Fixed (1s) |
| NewsAPI | 100/day | 100/day | 2 | Exponential (1s, 2s, 4s) |
| SkillsMP | 1000/month | 1000/mo | 5 | Exponential (1s, 2s, 4s) |

**Quota Monitoring:** Daily checks, alert at 80% usage
**Exhaustion Response:** Fallback to secondary tools or queue for next period

### 2.4 Uptime & Availability SLAs

| Tool | Expected Uptime | SLA | Maintenance Window |
|------|-----------------|-----|-------------------|
| Brave Search | 99.9% | 99.5% | Unscheduled (rare) |
| Tavily | 99.9% | 99.0% | Unscheduled |
| Hunter.io | 99.5% | 99.0% | Sundays 2-4 AM UTC |
| Abstract API | 99.5% | 99.0% | Unscheduled |
| Zyte API | 99.9% | 99.5% | Unscheduled |
| Kalshi API | 99.95% | 99.9% | Market hours only |
| NewsAPI | 99.0% | 98.0% | Unscheduled |
| SkillsMP | 99.5% | 99.0% | Sundays 3-5 AM UTC |

**Change Notification:** Email 48h in advance for planned maintenance
**Status Monitoring:** Weekly heartbeat checks

### 2.5 Security & Compliance Constraints

| Constraint | Rule | Enforcement |
|------------|------|-------------|
| **PII Handling** | No storage of SSN, credit cards, medical records | Regex filtering on outputs |
| **Data Egress** | Workspace files only, no external sharing | File system sandbox |
| **Email Privacy** | Hunter.io for business emails only | Domain validation |
| **API Keys** | Never log, never commit, env vars only | Pre-commit hooks, log sanitization |
| **Web Scraping** | Respect robots.txt, rate limits | Zyte API compliance layer |
| **Prediction Markets** | Paper trades only, no real money | Manual execution by Sam |

**Audit Log:** All tool calls logged with timestamp, agent, tool, success/failure
**Retention:** 90 days for operational logs, 1 year for audit logs

---

## 3. AI Engineering Governance

### 3.1 Prompt & Model Governance

| Model | Use Case | System Prompt | Version Control |
|-------|----------|---------------|-----------------|
| **Kimi K2.5** | Routine tasks | SOUL.md + MEMORY.md | Git committed |
| **GLM-4.7 (ZAI)** | Deep research | SOUL.md + skill context | Git committed |
| **Sub-agent default** | Parallel tasks | Agent-specific IDENTITY.md | Git committed |

**Prompt Versioning:** Git commits with semantic messages
**Rollback Strategy:** Revert to previous commit, restart session
**A/B Testing:** Not implemented (single model per task type)

### 3.2 Task Success/Failure Conditions

| Task Type | Success Criteria | Failure Criteria | Auto-Retry |
|-----------|-----------------|------------------|------------|
| **Web search** | Results returned, >3 sources | Timeout, 0 results, API error | Yes (2x) |
| **API call** | 200 status, valid JSON | 4xx/5xx, timeout, malformed | Yes (3x) |
| **File write** | File created, content matches | Permission denied, disk full | No |
| **Sub-agent spawn** | Session created, agent responds | Timeout, auth failure | No |
| **Tool chain** | All steps complete | Any step fails | Depends on step |

### 3.3 Required Inputs & Outputs

| Operation | Required Inputs | Output Format |
|-----------|----------------|---------------|
| Web search | Query string, max_results | JSON array with title, URL, snippet |
| API call | Endpoint, headers, payload | JSON response or error object |
| File read | Path, encoding | String content or error |
| File write | Path, content, encoding | Success boolean or error |
| Sub-agent spawn | Task description, model | Session ID or error |

### 3.4 Execution Limits

| Constraint | Limit | Rationale |
|------------|-------|-----------|
| **Max steps per task** | 50 | Prevent infinite loops |
| **Max retries per tool** | 3 | Balance resilience vs. cost |
| **Max chained calls** | 10 | Prevent cascade failures |
| **Max sub-agents** | 3 parallel | Control cost |
| **Max session duration** | 60 minutes | Prevent runaway costs |
| **Tool call timeout** | 30 seconds | UX threshold |
| **Total task timeout** | 5 minutes | User attention span |

### 3.5 Golden Datasets & Evaluation

| Agent | Golden Dataset | Evaluation Criteria |
|-------|---------------|---------------------|
| **TradeRecommender** | 50 historical trades | Accuracy vs. actual outcomes, edge calibration |
| **MiningMetalsAnalyst** | 20 known mine deals | Grade accuracy, price detection, alert precision |
| **LeadGenerator** | 30 scored leads | Precision/recall on Hot/Warm/Cold tiers |

**Evaluation Frequency:** Monthly
**Regression Threshold:** >5% accuracy drop = alert
**Improvement Target:** +2% accuracy per quarter

### 3.6 Alert Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| **Tool call latency** | >2s avg | >5s avg | Investigate, fallback tools |
| **API error rate** | >5% | >10% | Check quotas, rotate keys |
| **Model output quality** | >5% regression | >10% regression | Rollback, retrain |
| **Token consumption** | >80% budget | >95% budget | Throttle, alert Sam |
| **Context window** | 75% full | 90% full | New thread, compaction |

### 3.7 Tool Call Latency SLAs

| Tool Type | Target Latency | Max Latency | SLA |
|-----------|---------------|-------------|-----|
| **Search APIs** | <1s | <3s | 95% within target |
| **Data enrichment** | <2s | <5s | 90% within target |
| **Prediction markets** | <500ms | <2s | 99% within target |
| **Web scraping** | <10s | <30s | 80% within target |
| **Model inference** | <5s | <15s | 95% within target |

### 3.8 Versioning & Rollout Strategy

| Component | Versioning | Rollout Strategy |
|-----------|-----------|------------------|
| **System prompts** | Git commits | Immediate (session restart) |
| **Agent configs** | Git commits | Staged (test → prod) |
| **Skills** | Git commits + tags | Canary (10% → 50% → 100%) |
| **Models** | Provider versions | A/B test (if available) |
| **Tool integrations** | API versions | Staged with fallback |

**Rollback Time:** <5 minutes for prompt/config changes
**Testing Requirements:** Sub-agent validation before main session deployment

---

## 4. Operational Procedures

### 4.1 Incident Response

| Severity | Response Time | Resolution Target | Escalation |
|----------|---------------|-------------------|------------|
| **P0** (system down) | 15 minutes | 1 hour | Immediate to Sam |
| **P1** (major feature impaired) | 30 minutes | 4 hours | Daily digest |
| **P2** (minor issue) | 2 hours | 24 hours | Weekly summary |
| **P3** (observation) | 24 hours | Next sprint | Monthly review |

### 4.2 Change Management

| Change Type | Approval Required | Testing | Rollback Plan |
|-------------|-------------------|---------|---------------|
| **Prompt updates** | No (Git commit) | Self-test | Git revert |
| **New tool integration** | Yes (Sam) | Sub-agent validation | Disable tool |
| **Model changes** | Yes (Sam) | Side-by-side comparison | Model alias swap |
| **Rate limit changes** | No | Load test | Config revert |
| **Security policy** | Yes (Sam) | Penetration test | Emergency rollback |

---

## 5. Compliance Checklist

- [ ] All API keys rotated within 30 days
- [ ] No PII in logs or outputs
- [ ] All tools within quota
- [ ] All agents under token budget
- [ ] Golden dataset evaluations current
- [ ] Incident log reviewed weekly
- [ ] Security audit monthly
- [ ] Governance docs updated quarterly

---

*Last updated: 2026-02-11*
*Next review: 2026-03-11*
