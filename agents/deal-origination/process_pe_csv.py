#!/usr/bin/env python3
"""
PE Fund Outreach Processor
Processes CSV of PE fund contacts, prioritizes by seniority, creates tracking log
"""

import csv
import re
from datetime import datetime

INPUT_FILE = "/home/node/.openclaw/media/inbound/11dd2996-779a-4a08-b12e-a4168e8ea668.csv"
OUTPUT_FILE = "/home/node/.openclaw/workspace/cron-output/deal-origination/pe-funds/pe-outreach-2025-02-15.csv"

# Seniority scoring
SENIORITY_RANKS = {
    # C-Suite (Highest priority)
    'ceo': 10, 'chief executive': 10, 'chief executive officer': 10,
    'cfo': 10, 'chief financial': 10,
    'cio': 10, 'chief investment': 10,
    'managing partner': 9, 'founder': 9, 'founding partner': 9,
    'chairman': 9,
    
    # Partners (High priority)
    'partner': 8, 'general partner': 8, 'principal': 8,
    'managing director': 8, 'co-founder': 8,
    
    # Directors (Medium-high priority)
    'director': 7, 'investment director': 7,
    'executive director': 7, 'senior director': 7,
    
    # Vice Presidents (Medium priority)
    'vice president': 6, 'vp': 6, 'svp': 6,
    
    # Associates (Lower priority)
    'senior associate': 5, 'associate': 4,
    
    # Analysts (Lowest priority)
    'analyst': 3, 'investment analyst': 3,
    
    # Business development (Medium priority)
    'business development': 5, 'bd': 5,
    'head of business': 6,
}

def get_seniority_score(job_title):
    """Calculate seniority score based on job title"""
    if not job_title:
        return 1
    
    job_lower = job_title.lower()
    score = 1
    
    for title_pattern, rank in SENIORITY_RANKS.items():
        if title_pattern in job_lower:
            score = max(score, rank)
    
    return score

def get_agentmail_for_fund(company_name, job_title):
    """Determine which Agentmail account to use"""
    company_lower = company_name.lower() if company_name else ""
    job_lower = job_title.lower() if job_title else ""
    
    # Tech/software focused funds -> Zander
    tech_keywords = ['software', 'technology', 'tech', 'saas', 'digital', 'fintech', 'healthcare it']
    for kw in tech_keywords:
        if kw in company_lower or kw in job_lower:
            return "Zander@agentmail.to"
    
    # Traditional/industrial -> Zane
    return "Zane@agentmail.to"

def process_csv():
    """Process the input CSV and create prioritized output"""
    contacts = []
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Full Name', '').strip()
            company = row.get('Company Name', '').strip()
            title = row.get('Job Title', '').strip()
            email = row.get('Email Address', '').strip()
            phone = row.get('Primary Phone', '').strip()
            location = row.get('Location - Full', '').strip()
            status = row.get('Contact Status', '').strip()
            
            # Skip if no email
            if not email:
                continue
            
            # Calculate priority score
            seniority = get_seniority_score(title)
            agentmail = get_agentmail_for_fund(company, title)
            
            # Priority label
            if seniority >= 9:
                priority = "HIGH"
            elif seniority >= 6:
                priority = "MEDIUM"
            else:
                priority = "LOW"
            
            contacts.append({
                'name': name,
                'company': company,
                'title': title,
                'email': email,
                'phone': phone,
                'location': location,
                'seniority_score': seniority,
                'priority': priority,
                'agentmail': agentmail,
                'status': 'Pending',
                'last_contact': '',
                'notes': ''
            })
    
    # Sort by seniority score (descending)
    contacts.sort(key=lambda x: x['seniority_score'], reverse=True)
    
    # Write output CSV
    fieldnames = ['Priority', 'Seniority_Score', 'Name', 'Company', 'Title', 'Email', 'Phone', 'Location', 'Agentmail', 'Status', 'Last_Contact', 'Notes']
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for contact in contacts:
            writer.writerow({
                'Priority': contact['priority'],
                'Seniority_Score': contact['seniority_score'],
                'Name': contact['name'],
                'Company': contact['company'],
                'Title': contact['title'],
                'Email': contact['email'],
                'Phone': contact['phone'],
                'Location': contact['location'],
                'Agentmail': contact['agentmail'],
                'Status': contact['status'],
                'Last_Contact': contact['last_contact'],
                'Notes': contact['notes']
            })
    
    # Print summary
    high = sum(1 for c in contacts if c['priority'] == 'HIGH')
    medium = sum(1 for c in contacts if c['priority'] == 'MEDIUM')
    low = sum(1 for c in contacts if c['priority'] == 'LOW')
    
    print(f"Processed {len(contacts)} contacts")
    print(f"  HIGH priority (C-Suite, Partners, MDs): {high}")
    print(f"  MEDIUM priority (VPs, Directors): {medium}")
    print(f"  LOW priority (Associates, Analysts): {low}")
    print(f"\nOutput saved to: {OUTPUT_FILE}")
    
    # Show top 10
    print("\nTop 10 Highest Priority Contacts:")
    for i, c in enumerate(contacts[:10], 1):
        print(f"  {i}. {c['name']} - {c['title']} @ {c['company'][:30]}... (Score: {c['seniority_score']})")

if __name__ == "__main__":
    process_csv()
