#!/usr/bin/env python3
"""
PE Fund Database Merger
Merges existing priority list with new contacts, deduplicates, and assigns tiers
"""

import csv
import os
from datetime import datetime

# Read existing database
existing_emails = set()
existing_records = []

with open('pe-funds-priority.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row.get('Email Address', '').lower().strip()
        if email:
            existing_emails.add(email)
        existing_records.append(row)

print(f"Existing records: {len(existing_records)}")
print(f"Unique emails in existing: {len(existing_emails)}")

# Read new contacts
new_records = []
try:
    with open('new-pe-contacts.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_records.append(row)
    print(f"New contacts to process: {len(new_records)}")
except FileNotFoundError:
    print("Error: new-pe-contacts.csv not found")
    exit(1)

# Deduplicate and merge
duplicates = 0
added = 0
tier_1 = []
tier_2 = []
tier_3 = []

# Define Tier 1 criteria (High Priority)
tier_1_keywords = ['managing partner', 'partner', 'ceo', 'principal', 'managing director']
tier_1_firms = ['4front', 'a* capital', 'afi capital', 'alpine investors', 
                'arsenal capital', 'audax', 'nexa capital', 'abry partners']

# Define Tier 3 criteria (Large PE or Inactive/Cold)
tier_3_firms = ['arclight', 'blackstone', 'kkr', 'carlyle', 'bain capital', 
                'warburg pincus', 'advent', 'silver lake', 'thoma bravo']

for record in new_records:
    email = record.get('Email Address', '').lower().strip()
    
    # Skip if already exists
    if email in existing_emails:
        duplicates += 1
        continue
    
    # Determine tier
    job_title = record.get('Job Title', '').lower()
    company = record.get('Company Name', '').lower()
    status = record.get('Contact Status', '').upper()
    interaction = record.get('Interaction Status', '').upper()
    
    # Default to Tier 2
    tier = 2
    
    # Tier 1: Managing Partner/CEO/Principal level + Active + Target firms
    if any(keyword in job_title for keyword in tier_1_keywords):
        if status == 'VALID' and interaction != 'COLD':
            if any(firm in company for firm in tier_1_firms) or 'capital' in company:
                tier = 1
    
    # Tier 3: Large PE firms or COLD/INACTIVE status
    if any(firm in company for firm in tier_3_firms):
        tier = 3
    elif interaction == 'COLD' or status != 'VALID':
        tier = 3
    elif 'associate' in job_title or 'analyst' in job_title:
        tier = 3
    
    # Add to appropriate tier
    record['Tier'] = tier
    record['Priority'] = 'High' if tier == 1 else ('Medium' if tier == 2 else 'Low')
    record['Agentmail'] = 'Zane' if 'toronto' in company or 'canada' in record.get('Location - Full', '').lower() else 'Zander'
    record['Outreach_Status'] = 'Pending'
    
    if tier == 1:
        tier_1.append(record)
    elif tier == 2:
        tier_2.append(record)
    else:
        tier_3.append(record)
    
    added += 1

print(f"\n=== Merge Results ===")
print(f"Duplicates skipped: {duplicates}")
print(f"New records added: {added}")
print(f"  - Tier 1 (High Priority): {len(tier_1)}")
print(f"  - Tier 2 (Medium Priority): {len(tier_2)}")
print(f"  - Tier 3 (Monitor): {len(tier_3)}")
print(f"Total merged database: {len(existing_records) + added}")

# Create output directory
os.makedirs('pe-lists-by-tier', exist_ok=True)

# Write merged master database
fieldnames = ['Full Name', 'Company Name', 'Job Title', 'Email Address', 'Primary Phone', 
              'Location - Full', 'Tier', 'Priority', 'Agentmail', 'Outreach_Status', 'Notes']

with open('pe-lists-by-tier/pe-funds-merged-master.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    # Write existing with tier info
    for record in existing_records:
        row = {k: record.get(k, '') for k in fieldnames}
        row['Tier'] = '1' if record.get('Priority') == 'High' else ('2' if record.get('Priority') == 'Medium' else '3')
        writer.writerow(row)
    
    # Write new records
    for record in tier_1 + tier_2 + tier_3:
        row = {k: record.get(k, '') for k in fieldnames}
        writer.writerow(row)

# Write Tier 1 list (for immediate outreach)
with open('pe-lists-by-tier/tier-1-high-priority.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for record in tier_1:
        row = {k: record.get(k, '') for k in fieldnames}
        writer.writerow(row)

# Write Tier 2 list
with open('pe-lists-by-tier/tier-2-medium-priority.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for record in tier_2:
        row = {k: record.get(k, '') for k in fieldnames}
        writer.writerow(row)

# Write Tier 3 list
with open('pe-lists-by-tier/tier-3-monitor.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for record in tier_3:
        row = {k: record.get(k, '') for k in fieldnames}
        writer.writerow(row)

print(f"\n=== Output Files Created ===")
print(f"pe-lists-by-tier/pe-funds-merged-master.csv ({len(existing_records) + added} records)")
print(f"pe-lists-by-tier/tier-1-high-priority.csv ({len(tier_1)} records)")
print(f"pe-lists-by-tier/tier-2-medium-priority.csv ({len(tier_2)} records)")
print(f"pe-lists-by-tier/tier-3-monitor.csv ({len(tier_3)} records)")

# Show Tier 1 sample
print(f"\n=== Tier 1 Contacts (Ready for Outreach) ===")
for i, record in enumerate(tier_1[:10], 1):
    print(f"{i}. {record.get('Full Name')} - {record.get('Company Name')} - {record.get('Job Title')}")

print(f"\n{'='*60}")
print("MERGE COMPLETE - Ready to launch Tier 1 outreach")
print(f"{'='*60}")
