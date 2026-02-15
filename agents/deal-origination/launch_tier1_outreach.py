#!/usr/bin/env python3
"""
Tier 1 Outreach Launcher
Generates and sends emails to high-priority PE funds
"""

import csv
import os
from datetime import datetime

# Read Tier 1 list - Use existing HIGH priority contacts
tier_1_contacts = []
print("Loading high-priority PE contacts from database...")

# Use existing high-priority from database
with open('pe-funds-priority.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('Priority') in ['High', 'PRIORITY', 'Priority']:
            tier_1_contacts.append(row)

# Also add any new tier 1 contacts if available
try:
    with open('pe-lists-by-tier/tier-1-high-priority.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Full Name') and row.get('Email Address'):
                tier_1_contacts.append(row)
except FileNotFoundError:
    pass

print(f"=== Tier 1 Outreach Launch ===")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"Contacts ready: {len(tier_1_contacts)}")
print()

# Outreach Sequence A - Direct LMM Approach
sequence_a_template = """Subject: Business for sale - $3-5M EBITDA [Industry]

Hi {first_name},

I'm working with a profitable {industry} business in {location} generating $3.5M EBITDA with strong recurring revenue.

The owners are looking for a strategic partner to support their next growth phase, and given {company}'s focus on lower middle market investments, this might align well with your strategy.

Key highlights:
• $3.5M EBITDA, 25% margins
• 15+ year track record
• Recurring revenue model
• Growth runway with capital

Worth a brief call to discuss?

Best regards,
Sam
Fractional CFO & Deal Origination
sam@impactquadrant.info
"""

# Generate emails
outreach_dir = 'outreach-emails'
os.makedirs(outreach_dir, exist_ok=True)

emails_generated = []

for i, contact in enumerate(tier_1_contacts, 1):
    full_name = contact.get('Full Name', '').strip()
    company = contact.get('Company Name', '').strip()
    email = contact.get('Email Address', '').strip()
    
    if not all([full_name, company, email]):
        continue
    
    first_name = full_name.split()[0]
    
    # Customize template
    email_body = sequence_a_template.format(
        first_name=first_name,
        company=company,
        industry="manufacturing",  # Can be customized
        location="Southeast US"    # Can be customized
    )
    
    # Save to file
    filename = f"{outreach_dir}/tier1_email_{i:03d}_{first_name.lower()}_{company.replace(' ', '_').lower()[:20]}.txt"
    with open(filename, 'w') as f:
        f.write(f"To: {email}\n")
        f.write(f"From: sam@impactquadrant.info\n")
        f.write(f"Subject: Business for sale - $3-5M EBITDA\n")
        f.write(f"\n{email_body}\n")
    
    emails_generated.append({
        'id': i,
        'name': full_name,
        'company': company,
        'email': email,
        'file': filename,
        'status': 'Ready to send'
    })

print(f"Emails generated: {len(emails_generated)}")
print()

# Create outreach summary
with open(f'{outreach_dir}/outreach-summary.csv', 'w', newline='') as f:
    fieldnames = ['id', 'name', 'company', 'email', 'file', 'status', 'sent_date', 'response']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for email in emails_generated:
        writer.writerow(email)

print("=== Generated Emails ===")
for email in emails_generated[:5]:
    print(f"{email['id']}. {email['name']} ({email['company']}) - {email['email']}")

if len(emails_generated) > 5:
    print(f"... and {len(emails_generated) - 5} more")

print()
print(f"=== Output ===")
print(f"Emails saved to: {outreach_dir}/")
print(f"Summary: {outreach_dir}/outreach-summary.csv")
print()
print("Next Steps:")
print("1. Review emails in outreach-emails/ folder")
print("2. Customize industry/location details as needed")
print("3. Send via agentmail.to (Zane or Zander)")
print("4. Update outreach-summary.csv with sent dates")
