#!/usr/bin/env python3
"""
🚀 Check All Head to Head Data - July 17-18, 2025
ตรวจสอบข้อมูล head to head ของทุกคู่
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
        
        # ดึงชื่อทีมจากข้อมูล
        team1_name = None
        team2_name = None
        results = []
        
        for match in data['response']:
            if match['fixture']['status']['short'] == 'FT':  # เฉพาะการแข่งขันที่จบแล้ว
                home_team = match['teams']['home']['name']
                away_team = match['teams']['away']['name']
                home_goals = match['goals']['home']
                away_goals = match['goals']['away']
                match_date = match['fixture']['date'][:10]
                
                if team1_name is None and match['teams']['home']['id'] == int(team_ids[0]):
                    team1_name = home_team
                elif team1_name is None and match['teams']['away']['id'] == int(team_ids[0]):
                    team1_name = away_team
                
                if team2_name is None and match['teams']['home']['id'] == int(team_ids[1]):
                    team2_name = home_team
                elif team2_name is None and match['teams']['away']['id'] == int(team_ids[1]):
                    team2_name = away_team
                
                results.append({
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_goals': home_goals,
                    'away_goals': away_goals,
                    'match_date': match_date
                })
        
        return {
            'team1_id': team_ids[0],
            'team2_id': team_ids[1],
            'team1_name': team1_name,
            'team2_name': team2_name,
            'results': results
        }
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        return None

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Check All Head to Head Data - July 17-18, 2025")
    print("=" * 60)
    
    # ค้นหาไฟล์ head to head ทั้งหมด
    h2h_files = glob.glob("/Users/80090/Desktop/Project/untitle/api_data/uefa_real_data/h2h_*.json")
    
    # ตรวจสอบข้อมูล head to head ของทุกคู่
    all_h2h_data = {}
    
    for file_path in h2h_files:
        h2h_data = check_h2h_file(file_path)
        if h2h_data and h2h_data['team1_name'] and h2h_data['team2_name']:
            key = f"{h2h_data['team1_name']} vs {h2h_data['team2_name']}"
            all_h2h_data[key] = h2h_data
    
    # แสดงผลลัพธ์
    print(f"พบข้อมูล head to head ทั้งหมด {len(all_h2h_data)} คู่")
    
    for key, h2h_data in all_h2h_data.items():
        print(f"\n{key}:")
        if h2h_data['results']:
            for result in h2h_data['results']:
                print(f"  {result['home_team']} {result['home_goals']} - {result['away_goals']} {result['away_team']} ({result['match_date']})")
        else:
            print("  ไม่มีประวัติการเจอกัน")
    
    # บันทึกข้อมูล head to head ทั้งหมด
    with open('all_head_to_head_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_h2h_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 บันทึกข้อมูล head to head ทั้งหมดลงไฟล์: all_head_to_head_data.json")

if __name__ == "__main__":
    main()
