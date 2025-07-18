#!/bin/bash

# 🚀 Run China Super League Analysis Comparison - July 18, 2025
# รันการวิเคราะห์ China Super League ด้วย Advanced ML และ Ultra Advanced ML และเปรียบเทียบผลลัพธ์

echo "🚀 Starting China Super League Analysis Comparison - July 18, 2025"
echo "======================================================"

# 1. Run Advanced ML Analysis
echo -e "\n📊 Step 1: Running Advanced ML Analysis..."
python3 analyze_china_super_league_advanced.py

# 2. Run Ultra Advanced ML Analysis
echo -e "\n📊 Step 2: Running Ultra Advanced ML Analysis..."
python3 analyze_china_super_league_ultra.py

# 3. Compare ML Models
echo -e "\n📊 Step 3: Comparing ML Models..."
python3 compare_ml_models.py

echo -e "\n✅ Analysis Complete!"
echo "======================================================"
echo "📊 Results:"
echo "- Advanced ML Predictions: api_data/china_super_league/china_super_league_predictions_advanced_ml.csv"
echo "- Ultra Advanced ML Predictions: api_data/china_super_league/china_super_league_predictions_ultra_ml.csv"
echo "- Comparison CSV: api_data/china_super_league/china_super_league_predictions_comparison.csv"
echo "- Comparison HTML: api_data/china_super_league/china_super_league_comparison.html"
echo "======================================================"
