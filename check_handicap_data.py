#!/usr/bin/env python3
"""
🚀 Check Handicap Data - July 17-18, 2025
ตรวจสอบข้อมูล handicap
"""

import json

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Check Handicap Data - July 17-18, 2025")
    print("=" * 60)
    
    # โหลดข้อมูลผลการวิเคราะห์
    try:
        with open('uefa_competitions_real_data_analysis_with_handicap.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Handicap data for Europa League:")
        for i, match in enumerate(data['europa_league']):
            print(f"{i+1}. {match['home_team']} vs {match['away_team']}: {match['handicap']}")
        
        print("\nHandicap data for Conference League:")
        for i, match in enumerate(data['conference_league'][:3]):
            print(f"{i+1}. {match['home_team']} vs {match['away_team']}: {match['handicap']}")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
