#!/usr/bin/env python3
"""
Analyze CSV and find projects with actual GitHub links
Filter by projects that have direct GitHub repositories
"""
import csv
import re

csv_file = "/home/node/.openclaw/media/inbound/a697739e-116b-4674-9216-198c54c719f7.csv"

github_projects = []

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    
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
            projects.append({
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
projects.sort(key=lambda x: int(x.get('viability', '0')) if x.get('viability', '0').isdigit() else 0, reverse=True)

# Display results
print("="*80)
print(f"🎯 Direct GitHub Projects from Hackathon: {len(projects)} total")
print("="*80)
print()

for i, project in enumerate(projects, 1):
    viab_score = project['viability']
    print(f"{i}. {project['name']} [Viability: {viab_score}/5]")
    print(f"   📊 Category: {project['category']}")
    print(f"   💰 Pricing: {project['pricing']}")
    print(f"   💵 Revenue: {project['revenue']}")
    print(f"   ⏱️ Build Time: {project['build_time']}")
    print(f"   🎯 Source: {project['source']}")
    print(f"   🔗 GitHub: {project['github_url']}")
    print()

print("="*80)
print(f"📊 Total direct GitHub projects: {len(projects)}")
print(f"🎯 Top {min(10, len(projects))} most viable projects listed above")
print()
print("💡 Note: Devpost URLs are excluded. Only direct GitHub repositories listed.")
