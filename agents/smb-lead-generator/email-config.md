# SMB Lead Generator (Wellness 125) - Email Configuration

**Email Account:** sam@impactquadrant.info
**App Password:** dmje zsak eaop hyic
**Configured:** Feb 14, 2026
**Purpose:** Read SMB lead responses; Send outreach with permission only

## Email Access Protocol

### Reading Emails
- **Trigger:** When explicitly instructed by user
- **Scope:** Lead responses, prospect inquiries, meeting confirmations
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

### 1. Lead Response Follow-up
When a lead responds to Wellness 125 outreach:
- Parse email for interest level, questions
- Summarize for user
- **Ask permission** before replying

### 2. Meeting Scheduling
If user asks to schedule savings analysis call:
- Draft scheduling email
- **Show draft to user first**
- Send only after explicit approval

### 3. Information Requests
When leads ask for more details:
- Draft response with requested info
- **Show to user first**
- Send only after approval

## Security Rules
- ✅ Can read emails when instructed
- ✅ Can draft emails for review
- ❌ NEVER send without permission
- ❌ Never share credentials
- ❌ No autonomous email sending

## Permission Workflow

1. **User Request:** "Reply to the CEO who asked about implementation timeline"
2. **Agent Drafts:** Create response email
3. **Agent Asks:** "May I send this email to [CEO name] at [email]? [shows draft]"
4. **User Approval:** "Yes" or "Modify X, then send"
5. **Agent Sends:** Only after explicit approval
6. **Agent Logs:** Record sent email

**No exceptions. No auto-send.**
