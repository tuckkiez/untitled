#!/bin/bash

# 🚀 Run All Analysis - July 18, 2025
# รันการวิเคราะห์ทั้งหมดและอัพเดท index.html

# Set up directories
PROJECT_DIR="/Users/80090/Desktop/Project/untitle"
OUTPUT_DIR="$PROJECT_DIR/output"
DATA_DIR="$PROJECT_DIR/data"

# Create directories if they don't exist
mkdir -p "$OUTPUT_DIR"
mkdir -p "$DATA_DIR"

# Print header
echo "🚀 Ultra Advanced Multi-League Football Predictor"
echo "================================================="
echo "Running complete analysis for July 18, 2025"
echo "================================================="

# Run China Super League analysis
echo ""
echo "🇨🇳 Running China Super League analysis..."
python "$PROJECT_DIR/analyze_china_super_league.py"

# Run Korea K League 1 analysis (using Ultra Advanced ML)
echo ""
echo "🇰🇷 Running Korea K League 1 analysis..."
python "$PROJECT_DIR/analyze_korea_league_ultra.py"

# Update index.html
echo ""
echo "🔄 Updating index.html..."
python "$PROJECT_DIR/update_index.py"

# Print summary
echo ""
echo "================================================="
echo "✅ Analysis complete!"
echo "📊 Results available in $OUTPUT_DIR"
echo "🌐 Updated index.html"
echo "================================================="

# Open index.html in browser
echo "Opening index.html in browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$PROJECT_DIR/index.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$PROJECT_DIR/index.html"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    start "$PROJECT_DIR/index.html"
else
    echo "Could not open browser automatically. Please open $PROJECT_DIR/index.html manually."
fi

echo "Done!"
