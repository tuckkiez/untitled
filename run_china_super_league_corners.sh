#!/bin/bash

# 🚀 Run China Super League Corner Analysis - July 18, 2025
# รันการวิเคราะห์เตะมุมในการแข่งขัน China Super League ที่เส้น 10 ลูก

echo "🚀 Starting China Super League Corner Analysis - July 18, 2025"
echo "======================================================"

# 1. Run Corner Analysis
echo -e "\n📊 Running Corner Analysis at 10.0 line..."
python3 analyze_china_super_league_corners.py

echo -e "\n✅ Analysis Complete!"
echo "======================================================"
echo "📊 Results:"
echo "- Corner Predictions CSV: api_data/china_super_league/china_super_league_corner_predictions.csv"
echo "- JSON with Predictions: api_data/china_super_league/china_super_league_20250718_updated_corner_predictions.json"
echo "======================================================"
