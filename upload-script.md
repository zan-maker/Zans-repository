# Upload Script — USGS Critical Minerals Demo

## Script: `upload-script.sh`

```bash
#!/bin/bash
# Upload script for USGS Critical Minerals Demo

echo "🚀 Uploading USGS Critical Minerals Demo to GitHub..."
echo "📦 Repository: zan-maker/Zans-repository"
echo "🌿 Branch: usgs-critical-minerals-2026-02-28"

# Create directory structure
mkdir -p usgs-critical-minerals/2026-02-28/media

# Copy files (replace with actual file paths)
cp demo-index.html usgs-critical-minerals/2026-02-28/
cp dashboard-demo.jpg usgs-critical-minerals/2026-02-28/media/
cp enhanced-report.md usgs-critical-minerals/2026-02-28/
cp full-analysis.md usgs-critical-minerals/2026-02-28/
cp README.md usgs-critical-minerals/2026-02-28/
cp INDEX.md usgs-critical-minerals/2026-02-28/

echo "✅ Files ready for upload"
echo ""
echo "📁 Upload to: usgs-critical-minerals/2026-02-28/"
echo "📝 Commit message: USGS Critical Minerals Demo - Complete Package"
```

## Details

- **Repository:** `zan-maker/Zans-repository`
- **Branch:** `usgs-critical-minerals-2026-02-28`
- **Target Directory:** `usgs-critical-minerals/2026-02-28/`
- **Media Subdirectory:** `usgs-critical-minerals/2026-02-28/media/`
