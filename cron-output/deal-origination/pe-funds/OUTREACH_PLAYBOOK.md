# PE Fund Outreach - ImpactQuadrant Deal Origination
## Execution Playbook - Created: 2025-02-15

---

## Campaign Overview

**Objective:** Secure referral agreements with Lower & Middle Market PE funds for off-market business sales

**Target:** 621 PE fund contacts
- HIGH Priority: 20 (C-Suite, Managing Partners, Founders)
- MEDIUM Priority: 36 (VPs, Directors, Principals)
- LOW Priority: 565 (Associates, Analysts)

**Referral Fee Structure:**
- 5% of transaction value up to $1M
- Sliding scale above $1M
- Minimum fee: $50,000
- 12-month tail protection

---

## File Structure

```
cron-output/deal-origination/pe-funds/
├── pe-outreach-2025-02-15.csv          # Master tracking log
├── email-drafts/                        # Draft email templates
│   ├── John_Travaglini_..._email1.txt
│   ├── George_Lauro_..._email1.txt
│   └── ... (20 high-priority drafts)
├── sent/                                # Log of sent emails
├── responses/                           # Track replies
└── agreements/                          # Signed referral agreements
```

---

## 4-Step Outreach Sequence

### Step 1: Initial Contact (Day 0)
**Subject:** Off-market business opportunities - Referral partnership

**Purpose:** Introduce off-market deal flow and referral partnership opportunity

**Key Points:**
- Direct owner relationships (no brokers)
- Pre-qualified sellers
- Current pipeline examples
- 5% referral fee structure

### Step 2: Follow-Up (Day 4)
**Subject:** RE: Off-market opportunities

**Purpose:** Social proof + current pipeline showcase

**Key Points:**
- Share recent connection success
- List specific opportunities (HVAC, plumbing, car washes)
- Emphasize "no auction" advantage

### Step 3: Terms Clarification (Day 8)
**Subject:** Referral agreement terms

**Purpose:** Remove ambiguity, provide specific terms

**Key Points:**
- Detailed fee structure
- Tail protection
- What they get vs what you need
- Call to action

### Step 4: Final Touch (Day 14)
**Subject:** One last note - off-market deal flow

**Purpose:** Last attempt with specific opportunities

**Key Points:**
- List 3 current opportunities
- Low-pressure close
- Door stays open

---

## Email Send Process

### Before Sending:
1. ✅ Verify email with Hunter.io API
2. ✅ Check result = "deliverable"
3. ✅ Score > 50
4. ✅ Review draft for personalization

### Sending via Agentmail.to:
```bash
curl -X POST https://api.agentmail.to/v1/send \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Zane@agentmail.to",
    "to": "contact@pefirm.com",
    "cc": "sam@impactquadrant.info",
    "subject": "Off-market business opportunities - Referral partnership",
    "body": "EMAIL_BODY_HERE"
  }'
```

### After Sending:
1. Update `pe-outreach-2025-02-15.csv` with sent date
2. Move draft to `sent/` folder
3. Schedule follow-up in 4 days
4. Track in master log

---

## Daily Targets

**Week 1:** Send to all 20 HIGH priority contacts
**Week 2-4:** Send to 50 MEDIUM priority contacts
**Month 2+:** Batch process LOW priority (10-15/day)

---

## Response Handling

### Positive Response (Interested):
1. Reply within 4 hours
2. Schedule 15-min intro call
3. Send referral agreement template
4. Add to "Active Partners" list

### Neutral Response (Maybe later):
1. Add to monthly nurture sequence
2. Send market updates
3. Re-engage quarterly

### Negative Response (Not interested):
1. Thank them for reply
2. Keep on file for future
3. Do not re-engage for 6 months

---

## Tracking Metrics

Monitor weekly:
- Emails sent
- Open rate
- Response rate
- Calls scheduled
- Agreements signed
- Deals referred
- Fees earned

---

## Top 20 High-Priority Contacts (Send First)

| # | Name | Company | Title | Email |
|---|------|---------|-------|-------|
| 1 | John Travaglini | 4Front Capital Partners | CEO | john@4frontcapitalpartners.com |
| 2 | George Lauro | Alteon Capital Partners | Managing Partner & CEO | george.lauro@alteoncapital.com |
| 3 | Chris Johnson | Crown Capital Partners | President & CEO | chris.johnson@crowncapital.ca |
| 4 | Brent Beshore | Permanent Equity | CEO/Founder | b@permanentequity.com |
| 5 | Mazhar Pawar | SA Capital Partners | CEO & President | mazhar@sacapitalpartnersllc.com |
| 6 | Ira W. Miller | Zone Capital Partners | Chairman & CEO | imiller@zonecapitalpartners.com |
| 7 | Andreas Schulte | AS Equity Partners | Founder & Managing Partner | andreas.schulte@as-equitypartners.com |
| 8 | Inder Tallur | BelHealth Investment Partners | Managing Partner | itallur@belhealth.com |
| 9 | Alexander Rapatz | Black Manta Capital Partners | Co-Founder & Managing Partner | alex@blackmanta.capital |
| 10 | Alexander Schinzing | Celtic Asset & Equity Partners | Managing Partner | alexander@celticequitypartners.com |
| 11 | Adam Sommerfeld | Certus Capital Partners | Managing Partner | ams@certuscap.com |
| 12 | Jonathan Stein | Cortec Group | Managing Partner | jstein@cortecgroup.com |
| 13 | Anthony Moore | Evrensel Capital Partners | Founder & Executive Chairman | anthonym@evrenselcapitalpartners.com |
| 14 | Mark D. Taber | Great Hill Partners | Managing Partner | taber@greathillpartners.com |
| 15 | Andrew S. Rosen | Kainos Capital | Managing Partner | arosen@kainoscapital.com |
| 16 | Mitch Baruchowitz | Merida Capital Partners | Managing Partner | mitch@meridacap.com |
| 17 | Michael J. Dyment | NEXA Capital Partners | Managing Partner | michael.j.dyment@nexacapital.com |
| 18 | Dr. Saliba Sassine | S&A Capital | Chairman | s.sassine@snacapital.com.au |
| 19 | Christian Lim | SWEN Capital Partners | Co-Founder & Managing Partner | christian.lim@blueoceanspartners.com |
| 20 | Nick | West Lane Capital Partners | Managing Partner | nick@westlanecap.com |

---

## Next Steps

1. **Review email drafts** in `email-drafts/` folder
2. **Verify first 5 emails** with Hunter.io
3. **Send initial batch** (5 emails)
4. **Schedule follow-ups** in cron
5. **Track responses** and update log
6. **Scale** to remaining 600+ contacts

---

## Cron Schedule Setup

```bash
# Daily outreach (10-15 emails/day)
0 9 * * * /usr/bin/python3 /home/node/.openclaw/workspace/agents/deal-origination/send_pe_outreach.py --batch-size=15

# Follow-up sequence (Day 4)
0 10 * * * /usr/bin/python3 /home/node/.openclaw/workspace/agents/deal-origination/send_followup.py --step=2

# Follow-up sequence (Day 8)
0 11 * * * /usr/bin/python3 /home/node/.openclaw/workspace/agents/deal-origination/send_followup.py --step=3

# Follow-up sequence (Day 14)
0 12 * * * /usr/bin/python3 /home/node/.openclaw/workspace/agents/deal-origination/send_followup.py --step=4
```

---

*Campaign created: 2025-02-15*
*Contact: Zan @ ImpactQuadrant*
