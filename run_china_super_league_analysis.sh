#!/bin/bash

# 🚀 Run China Super League Analysis - July 18, 2025
# รันการวิเคราะห์ China Super League ทั้งหมดในขั้นตอนเดียว

echo "🚀 Starting China Super League Analysis - July 18, 2025"
echo "======================================================"

# 1. Run Ultra Advanced ML Analysis
echo -e "\n📊 Step 1: Running Ultra Advanced ML Analysis..."
python3 analyze_china_super_league.py

# 2. Create HTML Report
echo -e "\n📄 Step 2: Creating HTML Report..."
python3 create_china_super_league_html.py

# 3. Update Index with China Super League Analysis
echo -e "\n🔄 Step 3: Updating Index with China Super League Analysis..."
python3 update_index_with_china_super_league.py

echo -e "\n✅ Analysis Complete!"
echo "======================================================"
echo "📊 Results:"
echo "- Predictions CSV: api_data/china_super_league/china_super_league_predictions_20250718.csv"
echo "- JSON with Predictions: api_data/china_super_league/china_super_league_20250718_with_predictions.json"
echo "- HTML Report: api_data/china_super_league/china_super_league_report_20250718.html"
echo "- Updated Index: index.html"
echo "======================================================"
