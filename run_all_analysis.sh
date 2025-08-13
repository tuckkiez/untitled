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

# Fetch today's fixtures
echo "🌐 Fetching today's fixtures..."
python fetch_today_fixtures.py

# Check Asian fixtures
echo "🔍 Checking Asian fixtures..."
python check_asian_fixtures.py

# Check correct leagues and match times
echo "🔍 Checking correct leagues and match times..."
python check_correct_leagues.py

# Run China Super League analysis
echo "🇨🇳 Running China Super League analysis..."
python analyze_china_super_league.py

# Run Korea K League analysis
echo "🇰🇷 Running Korea K League analysis..."
python analyze_korea_league_ultra.py

# Run European Leagues analysis
echo "🇪🇺 Running European Leagues analysis..."
python analyze_european_leagues.py

# Run Asian Leagues analysis
echo "🌏 Running Asian Leagues analysis..."
python analyze_asian_leagues_fixed.py

# Run Additional European Leagues analysis (with real data and Thai time)
echo "🇪🇺 Running Additional European Leagues analysis..."
python analyze_more_european_leagues_real_fixed2.py

# Generate European Leagues HTML report (fixed version)
echo "📊 Generating European Leagues HTML report..."
python generate_european_report_fixed.py

# Generate Asian Leagues HTML report
echo "📊 Generating Asian Leagues HTML report..."
python generate_asian_report_fixed.py

# Generate Additional European Leagues HTML report (with real data and Thai time)
echo "📊 Generating Additional European Leagues HTML report..."
python generate_more_european_report_real_fixed.py

# Update index.html with European leagues analysis
echo "🌐 Updating website with European leagues analysis..."
python update_index_with_european_fixed.py

# Update index.html with Asian leagues analysis
echo "🌐 Updating website with Asian leagues analysis..."
python update_index_with_asian_fixed.py

# Update index.html with Additional European leagues analysis (with real data and Thai time)
echo "🌐 Updating website with Additional European leagues analysis..."
python update_index_with_more_european_real_fixed.py

# Remove duplicate leagues from index.html
echo "🧹 Removing duplicate leagues from index.html..."
python remove_duplicates_direct.py

# Remove alerts from index.html
echo "🧹 Removing alerts from index.html..."
python remove_alerts.py

# Clean index.html (remove League Statistics and Value Bets)
echo "🧹 Cleaning index.html..."
python clean_index.py

# Fix inconsistencies in index.html
echo "🔧 Fixing inconsistencies in index.html..."
python fix_inconsistencies.py

# Update header in index.html
echo "🔄 Updating header in index.html..."
python update_header.py

echo "✅ Analysis pipeline completed successfully!"
echo "📊 Website updated with latest predictions"
echo "🌐 View the results at index.html"

# Print timestamp
echo "⏰ Completed at: $(date)"
