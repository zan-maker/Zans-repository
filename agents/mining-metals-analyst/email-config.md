# MiningMetalsAnalyst - Email Configuration

**Email Account:** sam@cubiczan.com
**App Password:** ohcl keya mvhz nibe
**Configured:** Feb 14, 2026
**Purpose:** Read/parse mining-related emails; Send with permission only

## Email Access Protocol

### Reading Emails
- **Trigger:** When explicitly instructed by user
- **Scope:** Mining-related communications, seller inquiries, deal updates
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
- **Username:** sam@cubiczan.com
- **Password:** ohcl keya mvhz nibe

## IMAP Configuration (Reading)
- **Server:** imap.gmail.com
- **Port:** 993
- **Security:** SSL
- **Username:** sam@cubiczan.com
- **Password:** ohcl keya mvhz nibe

## Use Cases

### 1. Mine Seller Inquiries
When a seller responds to a mining listing inquiry:
- Parse email for key details (price, terms, documentation)
- Summarize for user
- **Ask permission** before replying

### 2. Deal Updates
When deal status changes:
- Read update emails
- Log to deals.csv
- Alert user of significant changes

### 3. Follow-up Requests
If user asks to follow up with a seller:
- Draft email
- **Show draft to user first**
- Send only after explicit approval

## Security Rules
- ✅ Can read emails when instructed
- ✅ Can draft emails for review
- ❌ NEVER send without permission
- ❌ Never share credentials
- ❌ No autonomous email sending

## API Usage (Email Actions)

When reading email via `message` tool:
```
action: read
accountId: sam@cubiczan.com
```

When sending (AFTER permission granted):
```
action: send
target: seller@example.com
from: sam@cubiczan.com
subject: [Subject]
message: [Body]
```

## Permission Workflow

1. **User Request:** "Contact the seller of Jefferson Gold Project"
2. **Agent Drafts:** Create email draft with proposed message
3. **Agent Asks:** "May I send this email? [shows draft]"
4. **User Approval:** "Yes" or "Modify X, then send"
5. **Agent Sends:** Only after explicit approval
6. **Agent Logs:** Record sent email in outreach log

**No exceptions. No auto-send.**
