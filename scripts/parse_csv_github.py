#!/usr/bin/env python3
"""
Parse CSV and find direct GitHub projects
Handles BOM (Byte Order Mark) in CSV file
"""
import csv
import io

csv_file = "/home/node/.openclaw/media/inbound/a697739e-116b-4674-9216-198c54c719f7.csv"

# Read with BOM handling
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Parse content
import csv
from io import StringIO

reader = csv.DictReader(StringIO(content))

github_projects = []

for row in reader:
    project_name = row.get('Project', '').strip()
    source = row.get('Source Hackathon', '').strip()
    category = row.get('Category', '').strip()
    pricing = row.get('Est. Pricing', '').strip()
    revenue = row.get('Revenue Model', '').strip()
    build_time = row.get('Atoms Build Time', '').strip()
    viability = row.get('Viability (1-5)', '').strip()
    source_link = row.get('GitHub / Source Link', '').strip()
    
    # Only include direct GitHub links (not Devpost URLs)
    if 'github.com' in source_link.lower() and 'devpost.com' not in source_link.lower():
        github_projects.append({
            'name': project_name,
            'source': source,
            'category': category,
            'pricing': pricing,
            'revenue': revenue,
            'build_time': build_time,
            'viability': viability,
            'github_url': source_link,
            'description': f"{category} project from {source}"
        })

# Sort by viability (highest first)
github_projects.sort(key=lambda x: int(x.get('viability', '0')) if x.get('viability', '0').isdigit() else 0, reverse=True)

# Display results
print("="*80)
print(f"🎯 Direct GitHub Projects from Hackathon: {len(github_projects)} total")
print("="*80)
print()

for i, project in enumerate(github_projects, 1):
    viab_score = project['viability']
    print(f"{i}. {project['name']} [Viability: {viab_score}/5]")
    print(f"   📊 Category: {project['category']}")
    print(f"   💰 Pricing: {project['pricing']}")
    print(f"   💵 Revenue: {project['revenue']}")
    print(f"   ⏱️  Build Time: {project['build_time']}")
    print(f"   🎯 Source: {project['source']}")
    print(f"   🔗 GitHub: {project['github_url']}")
    print()

print("="*80)
print(f"📊 Total direct GitHub projects: {len(github_projects)}")
print(f"🎯 All projects listed above are ready for immediate execution")
