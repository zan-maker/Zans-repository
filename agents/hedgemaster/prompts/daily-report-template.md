# HedgeMaster Daily Report Template

**Report Date:** {{YYYY-MM-DD}}  
**Generated:** {{HH:MM}} ET  
**Portfolio Value:** ${{TOTAL_VALUE}}

---

## 📊 Portfolio Overview

| Metric | Value |
|--------|-------|
| **Total Positions** | {{COUNT}} |
| **Portfolio Value** | ${{VALUE}} |
| **Day Change** | {{CHANGE}}% |
| **Active Hedges** | {{HEDGE_COUNT}} |
| **Hedge Value** | ${{HEDGE_VALUE}} |

---

## 🚨 Active Alerts

{{#if alerts}}
{{#each alerts}}
### {{ticker}} - Urgency: {{urgency}}/100
- **Position:** ${{position_value}}
- **Triggers:** {{triggers}}
- **Action:** {{action}}
{{/each}}
{{else}}
✅ No high-urgency alerts today.
{{/if}}

---

## 🎯 Active Hedges

{{#if hedges}}
| Ticker | Market | Position | Settlement | Status | Unrealized P&L |
|--------|--------|----------|------------|--------|----------------|
{{#each hedges}}
| {{ticker}} | {{market_name}} | ${{position}} | {{settlement_date}} | {{status}} | {{pnl}} |
{{/each}}

**Total Hedge Exposure:** ${{total_hedge_value}}  
**Total Potential Payout:** ${{total_potential_payout}}  
**Total Unrealized P&L:** ${{total_unrealized_pnl}}
{{else}}
ℹ️ No active hedges currently.
{{/if}}

---

## 📈 Recent Executions

{{#if recent_executions}}
{{#each recent_executions}}
- **{{date}}:** {{ticker}} - ${{position}} in "{{market}}" ({{status}})
{{/each}}
{{else}}
ℹ️ No executions in last 24 hours.
{{/if}}

---

## 🔮 Expiring Soon

{{#if expiring}}
| Ticker | Market | Settlement | Days Left | Position | Potential Payout |
|--------|--------|------------|-----------|----------|------------------|
{{#each expiring}}
| {{ticker}} | {{market_name}} | {{date}} | {{days}} | ${{position}} | ${{payout}} |
{{/each}}
{{else}}
✅ No hedges expiring in next 7 days.
{{/if}}

---

## 💡 New Opportunities

{{#if opportunities}}
{{#each opportunities}}
### {{ticker}} - {{risk_type}}
- **Hedge Score:** {{score}}/100
- **Suggested Position:** ${{position}}
- **Expected Value:** +${{ev}}
- **Status:** {{status}}
{{/each}}
{{else}}
ℹ️ No new hedge opportunities identified today.
{{/if}}

---

## 📊 Performance Summary

### This Month
- **Hedges Executed:** {{month_executions}}
- **Hedges Expired:** {{month_expired}}
- **Win Rate:** {{win_rate}}%
- **Total P&L:** ${{month_pnl}}

### All Time
- **Total Hedges:** {{all_time_hedges}}
- **Win Rate:** {{all_time_win_rate}}%
- **Total P&L:** ${{all_time_pnl}}
- **Avg Hedge Size:** ${{avg_hedge_size}}

---

## 🔔 Reminders

{{#if reminders}}
{{#each reminders}}
- {{message}}
{{/each}}
{{else}}
✅ No action items today.
{{/if}}

---

## 📅 Upcoming Events

{{#if events}}
{{#each events}}
- **{{date}}:** {{ticker}} - {{event_type}} ({{days}} days)
{{/each}}
{{else}}
ℹ️ No major events in next 30 days.
{{/if}}

---

**Next Portfolio Scan:** Tomorrow 9:00 AM ET  
**Next Report:** Tomorrow 6:00 PM ET  

---
Agent Manager  
HedgeMaster System  
ImpactQuadrant

Please reach out to Sam Desigan (Sam@impactquadrant.info) for further follow up.
