# TradeRecommender - Email Configuration

**Email Account:** sam@impactquadrant.info
**App Password:** dmje zsak eaop hyic
**Configured:** Feb 14, 2026
**Purpose:** Read trading-related emails; Send alerts/reports with permission only

## Email Access Protocol

### Reading Emails
- **Trigger:** When explicitly instructed by user
- **Scope:** Trading alerts, market notifications, broker communications
- **Action:** Read and summarize contents; Do NOT auto-respond

### Sending Emails - PERMISSION REQUIRED
- **Rule:** ALWAYS ask permission before sending
- **Format:** "May I send an email to [recipient] about [subject]? [Draft message]"
- **Wait for:** Explicit "yes" or approval from user
- **Never:** Send unsolicited emails without approval

## SMTP Configuration (Sending)
- **Server:** smtp.gmail.com
- **Port:** 587
- **Security:** TLS
- **Username:** sam@impactquadrant.info
- **Password:** dmje zsak eaop hyic

## IMAP Configuration (Reading)
- **Server:** imap.gmail.com
- **Port:** 993
- **Security:** SSL
- **Username:** sam@impactquadrant.info
- **Password:** dmje zsak eaop hyic

## Use Cases

### 1. Trade Alerts
If user asks to alert someone about a trade opportunity:
- Draft alert email
- **Show draft to user first**
- Send only after explicit approval

### 2. Broker Communications
When broker emails need review:
- Parse email for trade confirmations, statements
- Summarize for user
- **Ask permission** before replying

### 3. Daily Report Distribution
If user asks to email daily trade report:
- Attach report
- Draft email with summary
- **Show to user first**
- Send only after approval

## Security Rules
- ✅ Can read emails when instructed
- ✅ Can draft emails for review
- ❌ NEVER send without permission
- ❌ Never share credentials
- ❌ No autonomous email sending

## Permission Workflow

1. **User Request:** "Email me the daily trade report"
2. **Agent Drafts:** Create email with report attached
3. **Agent Asks:** "May I send this email to sam@impactquadrant.info? [shows draft]"
4. **User Approval:** "Yes" or "Modify X, then send"
5. **Agent Sends:** Only after explicit approval
6. **Agent Logs:** Record sent email

**No exceptions. No auto-send.**
