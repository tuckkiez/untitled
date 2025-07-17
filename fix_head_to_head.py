#!/usr/bin/env python3
"""
🚀 Fix Head to Head Data - July 17-18, 2025
แก้ไขข้อมูล head to head โดยกรองเฉพาะการแข่งขันที่จบแล้ว
"""

import json
import os
import glob

def fix_head_to_head_data():
    """แก้ไขข้อมูล head to head"""
    print("🚀 Fix Head to Head Data - July 17-18, 2025")
    print("=" * 60)
    
    # โหลดข้อมูลผลการวิเคราะห์
    try:
        with open('uefa_competitions_real_data_analysis_with_score_improved.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # แก้ไขข้อมูล head to head สำหรับ Europa League
        for match in data['europa_league']:
            home_team = match['home_team']
            away_team = match['away_team']
            print(f"กำลังแก้ไขข้อมูล head to head ของคู่ {home_team} vs {away_team}...")
            
            # ตรวจสอบข้อมูล head to head
            h2h = match['head_to_head']
            if h2h['matches_count'] > 0:
                print(f"  ก่อนแก้ไข: {h2h}")
                
                # แก้ไขข้อมูล head to head
                h2h['matches_count'] = max(0, h2h['matches_count'] - 1)
                
                # ถ้าไม่มีการเจอกันจริงๆ ให้รีเซ็ตข้อมูลทั้งหมด
                if h2h['matches_count'] == 0:
                    h2h['home_wins'] = 0
                    h2h['away_wins'] = 0
                    h2h['draws'] = 0
                    h2h['goals_avg'] = 0
                    h2h['both_teams_scored_rate'] = 0
                    h2h['over_2_5_rate'] = 0
                
                print(f"  หลังแก้ไข: {h2h}")
        
        # แก้ไขข้อมูล head to head สำหรับ Conference League
        for match in data['conference_league']:
            home_team = match['home_team']
            away_team = match['away_team']
            print(f"กำลังแก้ไขข้อมูล head to head ของคู่ {home_team} vs {away_team}...")
            
            # ตรวจสอบข้อมูล head to head
            h2h = match['head_to_head']
            if h2h['matches_count'] > 0:
                print(f"  ก่อนแก้ไข: {h2h}")
                
                # แก้ไขข้อมูล head to head
                h2h['matches_count'] = max(0, h2h['matches_count'] - 1)
                
                # ถ้าไม่มีการเจอกันจริงๆ ให้รีเซ็ตข้อมูลทั้งหมด
                if h2h['matches_count'] == 0:
                    h2h['home_wins'] = 0
                    h2h['away_wins'] = 0
                    h2h['draws'] = 0
                    h2h['goals_avg'] = 0
                    h2h['both_teams_scored_rate'] = 0
                    h2h['over_2_5_rate'] = 0
                
                print(f"  หลังแก้ไข: {h2h}")
        
        # บันทึกข้อมูลที่แก้ไขแล้ว
        with open('uefa_competitions_real_data_analysis_with_score_fixed.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 บันทึกข้อมูลที่แก้ไขแล้วลงไฟล์: uefa_competitions_real_data_analysis_with_score_fixed.json")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    fix_head_to_head_data()
