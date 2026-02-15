#!/usr/bin/env python3
"""
Generate PE Fund Outreach Email Drafts
Creates personalized email drafts for high-priority PE fund contacts
"""

import csv
from datetime import datetime

TRACKING_FILE = "/home/node/.openclaw/workspace/cron-output/deal-origination/pe-funds/pe-outreach-2025-02-15.csv"
OUTPUT_DIR = "/home/node/.openclaw/workspace/cron-output/deal-origination/pe-funds/email-drafts"

EMAIL_TEMPLATE_1 = """Subject: Off-market business opportunities - Referral partnership

Hi {name},

I came across {company} and see you're actively acquiring lower-to-middle market businesses.

I specialize in sourcing off-market opportunities - businesses that haven't listed with brokers and aren't on the major marketplaces.

**What I offer:**
- Direct relationships with business owners
- Pre-qualified sellers (motivated, realistic expectations)
- No broker intermediaries = better economics for everyone
- Focus on blue-collar services: HVAC, plumbing, electrical, car washes, commercial cleaning

**Current pipeline includes:**
- HVAC businesses (TX, FL, GA markets)
- Plumbing contractors (various metros)
- Car wash operations (metro areas)
- Other blue-collar services ($1M-$10M EBITDA range)

All off-market, all owner-direct.

I'd welcome the opportunity to discuss a referral partnership where I bring you qualified off-market deals in exchange for a standard referral fee (5% of transaction value, minimum $50K).

Worth a brief 15-minute call?

Best regards,
{sender_name}
ImpactQuadrant
{sender_email}

P.S. I can share detailed business summaries from my current pipeline if helpful.
"""

def generate_email_drafts():
    """Generate email drafts for high-priority contacts"""
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(TRACKING_FILE, 'r') as f:
        reader = csv.DictReader(f)
        high_priority = [row for row in reader if row['Priority'] == 'HIGH']
    
    print(f"Generating email drafts for {len(high_priority)} HIGH priority contacts...")
    
    for contact in high_priority[:20]:  # First batch - top 20
        name = contact['Name']
        company = contact['Company']
        email = contact['Email']
        agentmail = contact['Agentmail']
        
        sender_name = "Zane" if "Zane" in agentmail else "Zander"
        
        email_body = EMAIL_TEMPLATE_1.format(
            name=name.split()[0],  # First name only
            company=company,
            sender_name=sender_name,
            sender_email=agentmail
        )
        
        # Create filename
        safe_name = name.replace(' ', '_').replace('/', '_')[:30]
        filename = f"{OUTPUT_DIR}/{safe_name}_{company[:20].replace(' ', '_')}_email1.txt"
        
        with open(filename, 'w') as f:
            f.write(f"To: {email}\n")
            f.write(f"From: {agentmail}\n")
            f.write(f"CC: sam@impactquadrant.info\n")
            f.write(f"Company: {company}\n")
            f.write(f"Priority: {contact['Priority']}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("="*60 + "\n\n")
            f.write(email_body)
        
        print(f"  ✓ Created: {safe_name} @ {company[:30]}...")
    
    print(f"\nEmail drafts saved to: {OUTPUT_DIR}/")
    print(f"\nTo send these emails:")
    print(f"  1. Review each draft in {OUTPUT_DIR}/")
    print(f"  2. Verify email deliverability with Hunter.io")
    print(f"  3. Send via Agentmail.to API")
    print(f"  4. Update tracking log with sent dates")

if __name__ == "__main__":
    generate_email_drafts()
