#!/usr/bin/env python3
"""
Analyze full CSV of 46 hackathon projects
Extract GitHub links and create prioritized execution plan
"""
import csv
import re
from collections import defaultdict

# Read CSV file
csv_file = "/home/node/.openclaw/media/inbound/a697739e-116b-4674-9216-198c54c719f7.csv"

projects_by_viability = defaultdict(list)
projects_by_category = defaultdict(list)

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        # Extract relevant fields
        project_name = row.get('Project', '')
        source = row.get('Source Hackathon', '')
        category = row.get('Category', '')
        pricing = row.get('Est. Pricing', '')
        revenue = row.get('Revenue Model', '')
        build_time = row.get('Atoms Build Time', '')
        viability = row.get('Viability (1-5)', '')
        source_link = row.get('GitHub / Source Link', '')
        
        # Only include projects with GitHub links
        if 'github.com' in source_link.lower():
            project = {
                'name': project_name,
                'source': source,
                'category': category,
                'pricing': pricing,
                'revenue': revenue,
                'build_time': build_time,
                'viability': viability,
                'github_url': source_link,
                'description': f"{category} project from {source}"
            }
            
            # Sort by viability
            try:
                viab_score = int(viability)
            except ValueError:
                viab_score = 0
            
            projects_by_viability[viab_score].append(project)
            projects_by_category[category].append(project)

# Get all GitHub projects
all_github_projects = []
for viability in sorted(projects_by_viability.keys(), reverse=True):
    all_github_projects.extend(projects_by_viability[viability])

# Display results
print("="*80)
print(f"🎯 Full GitHub Projects Analysis: {len(all_github_projects)} total projects")
print("="*80)
print()

# Top 10 by viability
print("🏆 TOP 10 PROJECTS BY VIABILITY")
print("-"*80)
for i, project in enumerate(all_github_projects[:10], 1):
    viab_score = project['viability']
    print(f"\n{i}. {project['name']} [Viability: {viab_score}/5]")
    print(f"   📊 Category: {project['category']}")
    print(f"   💰 Pricing: {project['pricing']}")
    print(f"   💵 Revenue: {project['revenue']}")
    print(f"   ⏱️ Build Time: {project['build_time']}")
    print(f"   🎯 Source: {project['source']}")
    print(f"   🔗 GitHub: {project['github_url']}")
print()

# By category analysis
print("\n📊 PROJECTS BY CATEGORY")
print("-"*80)
for category in sorted(projects_by_category.keys()):
    projects = projects_by_category[category]
    print(f"\n{category}: {len(projects)} projects")
    for project in projects[:3]:  # Show first 3
        print(f"  - {project['name']} [Viability: {project['viability']}/5]")
print()

# Revenue model analysis
print("\n💵 REVENUE MODEL BREAKDOWN")
print("-"*80)
revenue_models = defaultdict(int)
for project in all_github_projects:
    rev_model = project['revenue']
    revenue_models[rev_model] += 1

for model in sorted(revenue_models.keys(), key=lambda x: revenue_models[x], reverse=True):
    print(f"{model}: {revenue_models[model]} projects")

# Create execution command list
print("\n🚀 QUICK EXECUTION - TOP 5 PROJECTS")
print("="*80)
print()
for i, project in enumerate(all_github_projects[:5], 1):
    github_match = re.search(r'github\.com/([^/]+/[^/]+)', project['github_url'])
    repo_name = github_match.group(0) if github_match else project['github_url'].split('/')[-1]
    
    print(f"\n{i}. {project['name']} (Viability: {project['viability']}/5)")
    print(f"   git clone {project['github_url']}")
    print(f"   cd {repo_name.split('/')[-1]} && npm install && npm run dev")
    print(f"   # Review README.md for setup instructions")
