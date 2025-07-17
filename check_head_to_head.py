#!/usr/bin/env python3
"""
🚀 Check Head to Head Data - July 17-18, 2025
ตรวจสอบข้อมูล head to head
"""

import json

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Check Head to Head Data - July 17-18, 2025")
    print("=" * 60)
    
    # โหลดข้อมูลผลการวิเคราะห์
    try:
        with open('uefa_competitions_real_data_analysis_with_score_improved.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Head to head data for Europa League:")
        for i, match in enumerate(data['europa_league']):
            print(f"{i+1}. {match['home_team']} vs {match['away_team']}: {match['head_to_head']}")
            print("-" * 40)
        
        print("\nHead to head data for Conference League (first 3 matches):")
        for i, match in enumerate(data['conference_league'][:3]):
            print(f"{i+1}. {match['home_team']} vs {match['away_team']}: {match['head_to_head']}")
            print("-" * 40)
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
