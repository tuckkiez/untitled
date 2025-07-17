#!/usr/bin/env python3
"""
🚀 Check Head to Head Data from API - July 17-18, 2025
ตรวจสอบข้อมูล head to head จาก API
"""

import json
import os
import glob

def check_h2h_file(file_path):
    """ตรวจสอบข้อมูล head to head จากไฟล์"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # ดึงชื่อทีมจากชื่อไฟล์
        filename = os.path.basename(file_path)
        team_ids = filename.replace('h2h_', '').replace('.json', '').split('_')
        
        print(f"Head to head data for teams {team_ids[0]} vs {team_ids[1]}:")
        print(f"จำนวนการเจอกัน: {len(data['response'])}")
        
        for i, match in enumerate(data['response']):
            home_team = match['teams']['home']['name']
            away_team = match['teams']['away']['name']
            home_goals = match['goals']['home']
            away_goals = match['goals']['away']
            match_date = match['fixture']['date'][:10]
            
            print(f"{i+1}. {home_team} {home_goals} - {away_goals} {away_team} ({match_date})")
        
        print("-" * 40)
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Check Head to Head Data from API - July 17-18, 2025")
    print("=" * 60)
    
    # ตรวจสอบข้อมูล head to head ของคู่ Aktobe vs Legia Warszawa
    check_h2h_file("/Users/80090/Desktop/Project/untitle/api_data/uefa_real_data/h2h_4563_339.json")
    
    # ตรวจสอบข้อมูล head to head ของคู่ Ilves vs Shakhtar Donetsk
    check_h2h_file("/Users/80090/Desktop/Project/untitle/api_data/uefa_real_data/h2h_663_385.json")
    
    # ตรวจสอบข้อมูล head to head ของคู่ Prishtina vs Sheriff Tiraspol
    check_h2h_file("/Users/80090/Desktop/Project/untitle/api_data/uefa_real_data/h2h_3499_2030.json")

if __name__ == "__main__":
    main()
