#!/bin/bash
# PE Fund Database Merge Script
# Merges existing priority list with new CSV, deduplicates, and segments by tier

EXISTING="pe-funds-priority.csv"
OUTPUT_DIR="pe-lists-by-tier"
mkdir -p $OUTPUT_DIR

echo "=== PE Fund Database Merge ==="
echo "Date: $(date)"
echo ""

# Count existing records (excluding header)
EXISTING_COUNT=$(tail -n +2 $EXISTING | wc -l)
echo "Existing funds in database: $EXISTING_COUNT"

# The new data needs to be processed from the CSV attachment
# For now, we'll create the framework for the merge

echo ""
echo "=== Merge Plan ==="
echo "Step 1: Deduplicate by email address"
echo "Step 2: Assign tier based on criteria"
echo "Step 3: Create segmented lists"
echo ""

echo "=== Tier Assignment Criteria ==="
echo ""
echo "TIER 1 (High Priority) - Target: 75 funds"
echo "  - Lower/Middle Market focus"
echo "  - US/Canada/Europe geography"
echo "  - Managing Partner/Principal level"
echo "  - Active status"
echo ""
echo "TIER 2 (Medium Priority) - Target: 150 funds"
echo "  - Broader PE with LMM division"
echo "  - Regional specialists"
echo "  - VP/Senior Associate level"
echo ""
echo "TIER 3 (Monitor) - Target: 260 funds"
echo "  - Large PE (may have LMM affiliate)"
echo "  - Inactive/Cold contacts"
echo "  - International (non-target)"
echo ""

echo "=== Output Files ==="
echo "$OUTPUT_DIR/tier-1-high-priority.csv"
echo "$OUTPUT_DIR/tier-2-medium-priority.csv"
echo "$OUTPUT_DIR/tier-3-monitor.csv"
echo "$OUTPUT_DIR/pe-funds-merged-master.csv"
echo ""

echo "Ready to execute merge upon approval."
