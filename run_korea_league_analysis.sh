#!/bin/bash

# 🚀 Run Korea K League 1 Analysis - July 18, 2025
# รันการวิเคราะห์ K League 1 ทั้งหมด

echo "🚀 Starting Korea K League 1 Analysis - July 18, 2025"
echo "======================================================"

# 1. Fetch Korea League data
echo -e "\n📊 Step 1: Fetching Korea League data..."
python3 fetch_korea_league_data.py

# 2. Run Ultra Advanced ML Analysis
echo -e "\n📊 Step 2: Running Ultra Advanced ML Analysis..."
python3 analyze_korea_league_ultra.py

# 3. Update Index with Korea League Analysis
echo -e "\n🔄 Step 3: Updating Index with Korea League Analysis..."
python3 update_index_with_korea_league.py

echo -e "\n✅ Analysis Complete!"
echo "======================================================"
echo "📊 Results:"
echo "- Korea League Data: api_data/korea_league/korea_league_20250718.json"
echo "- Predictions CSV: api_data/korea_league/korea_league_predictions_ultra_ml.csv"
echo "- JSON with Predictions: api_data/korea_league/korea_league_20250718_with_predictions.json"
echo "- Updated Index: index.html"
echo "======================================================"
