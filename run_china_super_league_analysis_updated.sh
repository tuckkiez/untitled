#!/bin/bash

# 🚀 Run China Super League Analysis with Corners - July 18, 2025
# รันการวิเคราะห์ China Super League ทั้งหมดในขั้นตอนเดียว รวมถึงการวิเคราะห์เตะมุม

echo "🚀 Starting China Super League Analysis with Corners - July 18, 2025"
echo "======================================================"

# 1. Run Ultra Advanced ML Analysis with Corners
echo -e "\n📊 Step 1: Running Ultra Advanced ML Analysis with Corners..."
python3 analyze_china_super_league_with_corners.py

# 2. Create HTML Report with Corners
echo -e "\n📄 Step 2: Creating HTML Report with Corners..."
python3 create_china_super_league_html_with_corners.py

# 3. Update Index with China Super League Analysis including Corners
echo -e "\n🔄 Step 3: Updating Index with China Super League Analysis including Corners..."
python3 update_index_with_china_super_league_corners.py

echo -e "\n✅ Analysis Complete!"
echo "======================================================"
echo "📊 Results:"
echo "- Predictions CSV: api_data/china_super_league/china_super_league_predictions_20250718_updated.csv"
echo "- JSON with Predictions: api_data/china_super_league/china_super_league_20250718_updated_with_predictions.json"
echo "- HTML Report: api_data/china_super_league/china_super_league_report_20250718_updated.html"
echo "- Updated Index: index.html"
echo "======================================================"
