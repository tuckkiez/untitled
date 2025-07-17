#!/usr/bin/env python3
"""
🚀 Fix Head to Head Data Correctly - July 17-18, 2025
แก้ไขข้อมูล head to head ให้ถูกต้อง
"""

import json
import os

def fix_head_to_head_data():
    """แก้ไขข้อมูล head to head ให้ถูกต้อง"""
    print("🚀 Fix Head to Head Data Correctly - July 17-18, 2025")
    print("=" * 60)
    
    # โหลดข้อมูลผลการวิเคราะห์
    try:
        with open('uefa_competitions_real_data_analysis_with_score_fixed.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # แก้ไขข้อมูล head to head สำหรับ Ilves vs Shakhtar Donetsk
        for match in data['europa_league']:
            if match['home_team'] == 'Ilves' and match['away_team'] == 'Shakhtar Donetsk':
                print(f"กำลังแก้ไขข้อมูล head to head ของคู่ {match['home_team']} vs {match['away_team']}...")
                print(f"  ก่อนแก้ไข: {match['head_to_head']}")
                
                # แก้ไขข้อมูล head to head
                match['head_to_head'] = {
                    'matches_count': 1,
                    'home_wins': 0,
                    'away_wins': 1,
                    'draws': 0,
                    'goals_avg': 6.0,
                    'both_teams_scored_rate': 0.0,
                    'over_2_5_rate': 1.0
                }
                
                print(f"  หลังแก้ไข: {match['head_to_head']}")
        
        # ตรวจสอบและแก้ไขข้อมูล head to head ของคู่อื่นๆ
        # ตรวจสอบทุกคู่ในทั้ง Europa League และ Conference League
        for league in ['europa_league', 'conference_league']:
            for match in data[league]:
                h2h = match['head_to_head']
                
                # ถ้า matches_count เป็น 0 แต่มี home_wins, away_wins, หรือ draws ที่ไม่ใช่ 0
                if h2h['matches_count'] == 0 and (h2h['home_wins'] > 0 or h2h['away_wins'] > 0 or h2h['draws'] > 0):
                    print(f"พบข้อมูลที่ไม่สอดคล้องกันในคู่ {match['home_team']} vs {match['away_team']}...")
                    print(f"  ก่อนแก้ไข: {h2h}")
                    
                    # แก้ไขให้ matches_count เท่ากับผลรวมของ home_wins, away_wins, และ draws
                    h2h['matches_count'] = h2h['home_wins'] + h2h['away_wins'] + h2h['draws']
                    
                    print(f"  หลังแก้ไข: {h2h}")
        
        # บันทึกข้อมูลที่แก้ไขแล้ว
        with open('uefa_competitions_real_data_analysis_with_score_correct.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 บันทึกข้อมูลที่แก้ไขแล้วลงไฟล์: uefa_competitions_real_data_analysis_with_score_correct.json")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    fix_head_to_head_data()
