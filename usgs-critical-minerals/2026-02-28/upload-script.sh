#!/bin/bash

# Simple GitHub upload script
# Replace with your repository details

REPO="your-username/usgs-critical-minerals-data"
BRANCH="usgs-data-$(date +%Y-%m-%d)"
GITHUB_TOKEN="your-personal-access-token"

echo "🚀 Uploading to GitHub..."

# Initialize git if not already
if [ ! -d .git ]; then
    git init
    git checkout -b "$BRANCH"
fi

# Add all files
git add .

# Commit
git commit -m "USGS Critical Minerals Data - $(date +%Y-%m-%d)"

# Set remote (update with your repo)
git remote add origin "https://github.com/$REPO.git" 2>/dev/null || git remote set-url origin "https://github.com/$REPO.git"

# Push with token
git push -u origin "$BRANCH"

echo "✅ Upload complete!"
echo "🔗 Demo Link: https://github.com/$REPO/tree/$BRANCH"
