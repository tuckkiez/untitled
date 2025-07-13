#!/usr/bin/env python3
"""
🚀 Main Script for Real Predictions System
สคริปต์หลักสำหรับระบบทำนายจริงและอัปเดต GitHub
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from real_predictions_updater import RealPredictionsUpdater
from html_generator import HTMLGenerator
import subprocess
import time

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Starting Advanced Real Predictions System...")
    print("=" * 60)
    
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # Step 1: ดึงข้อมูลและทำนาย
    print("📊 Step 1: Fetching matches and generating real predictions...")
    updater = RealPredictionsUpdater(api_key)
    matches_with_predictions = updater.run_predictions()
    
    if not matches_with_predictions:
        print("❌ No matches found! Exiting...")
        return
    
    # Step 2: สร้าง HTML
    print("🎨 Step 2: Generating HTML...")
    html_generator = HTMLGenerator()
    html_content = html_generator.generate_full_html(matches_with_predictions)
    
    # Step 3: บันทึกไฟล์
    print("💾 Step 3: Saving index.html...")
    index_path = '/Users/80090/Desktop/Project/untitle/index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ index.html updated successfully!")
    
    # Step 4: Git operations
    print("📤 Step 4: Pushing to GitHub...")
    try:
        # Change to project directory
        os.chdir('/Users/80090/Desktop/Project/untitle')
        
        # Git add
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Git commit
        total_matches = sum(len(matches) for matches in matches_with_predictions.values())
        total_leagues = len(set(match['league']['name'] for matches in matches_with_predictions.values() for match in matches))
        
        commit_message = f"""🚀 Real Predictions Update: Advanced 4-Value Analysis

✨ Features:
- Real statistical data analysis from team performance
- 4-Value predictions: Result | Handicap | Over/Under | Corners
- FIFA Club World Cup special analysis (Chelsea vs PSG)
- Cross-league data integration for international matches
- Advanced confidence scoring with color-coded indicators

📊 Coverage:
- {total_matches} matches analyzed
- {total_leagues} leagues covered
- Real-time API data integration
- Statistical model predictions

🎯 Prediction Types:
1. Match Result (Home/Draw/Away) with probabilities
2. Handicap lines with confidence levels
3. Over/Under 2.5 goals analysis
4. Corner predictions (Half-time & Full-time)

🏆 Special Features:
- FIFA Club World Cup: Combined league stats analysis
- Priority-based league weighting system
- Responsive design with confidence bars
- Real-time status indicators

🔧 Technical:
- Advanced statistical algorithms
- Team form analysis (last 5 games)
- Head-to-head historical data
- ELO rating calculations
- Cross-league performance metrics"""

        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Git push
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Successfully pushed to GitHub!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return
    
    # Step 5: สรุปผล
    print("\n" + "=" * 60)
    print("🎉 REAL PREDICTIONS SYSTEM COMPLETED!")
    print("=" * 60)
    
    total_matches = sum(len(matches) for matches in matches_with_predictions.values())
    total_leagues = len(set(match['league']['name'] for matches in matches_with_predictions.values() for match in matches))
    
    print(f"📊 Total Matches Analyzed: {total_matches}")
    print(f"🏆 Leagues Covered: {total_leagues}")
    print(f"🎯 Prediction Types: 4 (Result, Handicap, O/U, Corners)")
    print(f"🌐 Website: https://tuckkiez.github.io/untitled/")
    print(f"📁 Local File: {index_path}")
    
    # แสดงรายละเอียดลีกที่ครอบคลุม
    print("\n🏆 Leagues Analyzed:")
    leagues_summary = {}
    for matches in matches_with_predictions.values():
        for match in matches:
            league_name = match['league']['name']
            country = match['league']['country']
            key = f"{league_name} ({country})"
            if key not in leagues_summary:
                leagues_summary[key] = 0
            leagues_summary[key] += 1
    
    for league, count in sorted(leagues_summary.items()):
        print(f"  • {league}: {count} matches")
    
    print("\n🔥 Special Highlights:")
    fifa_matches = []
    for matches in matches_with_predictions.values():
        for match in matches:
            if "FIFA Club World Cup" in match['league']['name']:
                fifa_matches.append(f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}")
    
    if fifa_matches:
        print("  🏆 FIFA Club World Cup Matches:")
        for match in fifa_matches:
            print(f"    - {match}")
    
    print("\n✅ All systems operational! Check the website for live predictions.")

if __name__ == "__main__":
    main()
