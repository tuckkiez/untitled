#!/bin/bash

# 🚀 Run All Analysis and Update Website
# สคริปต์รันการวิเคราะห์ทั้งหมดและอัพเดทเว็บไซต์

echo "🚀 Starting Ultra Advanced ML Football Analysis Pipeline"
echo "========================================================"

# Set current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Create backup of current index.html
echo "📦 Creating backup of current index.html..."
cp index.html index.html.$(date +%Y%m%d%H%M%S).bak

# Run China Super League analysis
echo "🇨🇳 Running China Super League analysis..."
python analyze_china_super_league.py

# Run Korea K League analysis
echo "🇰🇷 Running Korea K League analysis..."
python analyze_korea_league_ultra.py

# Run European Leagues analysis
echo "🇪🇺 Running European Leagues analysis..."
python analyze_european_leagues.py

# Generate European Leagues HTML report (fixed version)
echo "📊 Generating European Leagues HTML report..."
python generate_european_report_fixed.py

# Update index.html with all analyses (fixed version)
echo "🌐 Updating website with all analyses..."
python update_index_with_european_fixed.py

echo "✅ Analysis pipeline completed successfully!"
echo "📊 Website updated with latest predictions"
echo "🌐 View the results at index.html"

# Print timestamp
echo "⏰ Completed at: $(date)"
