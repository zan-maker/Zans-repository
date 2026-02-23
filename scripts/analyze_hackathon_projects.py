#!/usr/bin/env python3
"""
Extract GitHub projects from Hackathon CSV file
Finds projects with GitHub links and suggests execution/revenue strategies
"""
import csv
import re

# Read CSV file
csv_file = "/home/node/.openclaw/media/inbound/72309347-9563-4c97-864b-8153cfb1be40.csv"

projects = []

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
print("🎯 GitHub Projects from Hackathon - Ranked by Viability")
print("="*80)
print()

for i, project in enumerate(projects[:30], 1):
    # Extract repo name from URL
    github_match = re.search(r'github\.com/([^/]+/[^/]+)', project['github_url'])
    repo_name = github_match.group(0) if github_match else project['github_url']
    
    # Build command suggestion
    clone_cmd = f"git clone {project['github_url']}"
    run_cmd = f"cd {repo_name.split('/')[-1]} && python3 -m pip install -r requirements.txt && python3 app.py"
    
    print(f"{i}. {project['name']}")
    print(f"   📊 Category: {project['category']}")
    print(f"   💰 Pricing: {project['pricing']}")
    print(f"   💵 Revenue: {project['revenue']}")
    print(f"   ⏱️ Build Time: {project['build_time']}")
    print(f"   🎯 Viability: {project['viability']}/5")
    print(f"   🔗 GitHub: {project['github_url']}")
    print(f"   📝 Description: {project['description']}")
    print()
    print("   🚀 Execution Strategy:")
    print(f"      {clone_cmd}")
    print(f"      {run_cmd}")
    print()
    print("   💡 Revenue Strategy:")
    if 'subscription' in project['pricing'].lower() or 'B2B' in project['pricing']:
        print("      • Focus on MRR (Monthly Recurring Revenue)")
        print("      • Offer annual plans at 20% discount")
        print("      • Implement usage-based pricing tiers")
    elif 'per transaction' in project['pricing'].lower() or '/check' in project['pricing'].lower():
        print("      • Focus on transaction volume")
        print("      • Implement tiered processing fees")
        print("      • Consider B2B2B marketplace model")
    elif 'freemium' in project['pricing'].lower() or 'B2B + usage' in project['pricing'].lower():
        print("      • Free tier for user acquisition")
        print("      • Premium features for power users")
        print("      • Usage-based upsell opportunities")
    else:
        print("      • Analyze competitors' pricing models")
        print("      • Test different price points")
        print("      • Implement A/B testing for conversion")
    print()
    print("   🛡️ Tech Stack Suggestion:")
    if 'AI' in project['category'].lower() or 'LLM' in project['name'].lower():
        print("      • Backend: Python/FastAPI")
        print("      • Frontend: React/Vue with Tailwind")
        print("      • AI/ML: OpenAI API, Hugging Face models")
        print("      • Database: PostgreSQL + pgvector")
        print("      • Caching: Redis for high-speed queries")
    elif 'SaaS' in project['category'].lower() or 'subscription' in project['pricing'].lower():
        print("      • Backend: Django REST API")
        print("      • Frontend: Next.js with shadcn/ui")
        print("      • Payments: Stripe billing integration")
        print("      • Auth: OAuth2 + JWT tokens")
        print("      • Email: SendGrid for transactional emails")
    else:
        print("      • Backend: Node.js/Express")
        print("      • Frontend: React with Material UI")
        print("      • Database: MongoDB for flexible schemas")
        print("      • Hosting: Vercel/Netlify for frontend")
        print("      • CI/CD: GitHub Actions for deployment")
    print()
    print("-"*80)
    print()

print("="*80)
print(f"📊 Total GitHub projects found: {len(projects)}")
print(f"🎯 Top {min(30, len(projects))} most viable projects listed above")
print()
print("💡 Quick Execution Commands:")
print()
print("# Clone and run top 3 projects:")
print("git clone https://github.com/D4Vinci/Scrapling")
print("git clone https://github.com/scrappydevs/Yumi")
print("git clone https://github.com/gl26/bdev.ai")
