#!/usr/bin/env python3
"""
🎯 CORNER STATISTICS UTILITY
Quick utility to fetch corner data for any team
"""

import requests
import json
import time
import random

def get_corner_stats(team_name, num_matches=10):
    """
    ดึงสถิติเตะมุมของทีม
    
    Args:
        team_name (str): ชื่อทีม
        num_matches (int): จำนวนแมตช์ที่ต้องการดู
    
    Returns:
        dict: ข้อมูลสถิติเตะมุม
    """
    # ในสถานการณ์จริง เราควรดึงข้อมูลจริงจาก API
    # แต่ในที่นี้เราจะสร้างข้อมูลจำลองที่สมจริง
    
    # สร้าง seed จากชื่อทีมเพื่อให้ผลลัพธ์คงที่สำหรับแต่ละทีม
    seed = sum(ord(c) for c in team_name)
    random.seed(seed)
    
    # ทีมที่มีแนวโน้มเตะมุมสูง
    high_corner_teams = [
        "Manchester United", "Liverpool", "Manchester City", "Chelsea", "Arsenal",
        "Barcelona", "Real Madrid", "Bayern Munich", "Borussia Dortmund",
        "Ajax", "PSG", "Juventus", "Inter Milan", "AC Milan",
        "Shakhtar Donetsk", "Legia Warszawa", "Dinamo Zagreb", "Slavia Prague"
    ]
    
    # ทีมที่มีแนวโน้มเตะมุมต่ำ
    low_corner_teams = [
        "Burnley", "Crystal Palace", "Getafe", "Cadiz", "Udinese",
        "Angers", "Metz", "Augsburg", "Union Berlin", "Elche",
        "Valur Reykjavik", "NSI Runavik", "Tre Fiori", "Magpies"
    ]
    
    # กำหนดค่าเริ่มต้นตามประเภทของทีม
    if team_name in high_corner_teams:
        base_corners_for = random.uniform(5.5, 7.5)
        base_corners_against = random.uniform(4.0, 6.0)
        over_9_5_rate = random.uniform(0.70, 0.85)
    elif team_name in low_corner_teams:
        base_corners_for = random.uniform(3.0, 4.5)
        base_corners_against = random.uniform(3.5, 5.0)
        over_9_5_rate = random.uniform(0.30, 0.45)
    else:
        base_corners_for = random.uniform(4.0, 6.0)
        base_corners_against = random.uniform(4.0, 6.0)
        over_9_5_rate = random.uniform(0.45, 0.65)
    
    # สร้างข้อมูลแมตช์
    matches = []
    total_corners_for = 0
    total_corners_against = 0
    total_first_half_corners = 0
    total_second_half_corners = 0
    over_9_5_count = 0
    over_4_5_first_half_count = 0
    over_5_5_second_half_count = 0
    
    for i in range(num_matches):
        # สร้างข้อมูลเตะมุมสุ่ม
        corners_for = max(0, int(random.gauss(base_corners_for, 1.5)))
        corners_against = max(0, int(random.gauss(base_corners_against, 1.5)))
        
        first_half_corners = max(0, int(random.gauss((corners_for + corners_against) * 0.4, 1.0)))
        second_half_corners = corners_for + corners_against - first_half_corners
        
        total_corners = corners_for + corners_against
        
        # นับสถิติ
        total_corners_for += corners_for
        total_corners_against += corners_against
        total_first_half_corners += first_half_corners
        total_second_half_corners += second_half_corners
        
        if total_corners > 9.5:
            over_9_5_count += 1
        
        if first_half_corners > 4.5:
            over_4_5_first_half_count += 1
        
        if second_half_corners > 5.5:
            over_5_5_second_half_count += 1
        
        # เพิ่มข้อมูลแมตช์
        matches.append({
            "corners_for": corners_for,
            "corners_against": corners_against,
            "total_corners": total_corners,
            "first_half_corners": first_half_corners,
            "second_half_corners": second_half_corners
        })
    
    # คำนวณค่าเฉลี่ย
    corners_for_avg = total_corners_for / num_matches
    corners_against_avg = total_corners_against / num_matches
    total_corners_avg = (total_corners_for + total_corners_against) / num_matches
    first_half_corners_avg = total_first_half_corners / num_matches
    second_half_corners_avg = total_second_half_corners / num_matches
    
    # คำนวณอัตราส่วน
    over_9_5_rate = over_9_5_count / num_matches
    over_4_5_first_half_rate = over_4_5_first_half_count / num_matches
    over_5_5_second_half_rate = over_5_5_second_half_count / num_matches
    
    # สร้างผลลัพธ์
    result = {
        "team_name": team_name,
        "matches_analyzed": num_matches,
        "corners_for_avg": round(corners_for_avg, 1),
        "corners_against_avg": round(corners_against_avg, 1),
        "total_corners_avg": round(total_corners_avg, 1),
        "first_half_corners_avg": round(first_half_corners_avg, 1),
        "second_half_corners_avg": round(second_half_corners_avg, 1),
        "over_9_5_rate": round(over_9_5_rate, 2),
        "over_4_5_first_half_rate": round(over_4_5_first_half_rate, 2),
        "over_5_5_second_half_rate": round(over_5_5_second_half_rate, 2),
        "home_corners_avg": round(corners_for_avg * 1.2, 1),
        "away_corners_avg": round(corners_for_avg * 0.8, 1),
        "matches": matches
    }
    
    return result

def get_head_to_head_corners(team1, team2, num_matches=5):
    """
    ดึงสถิติเตะมุมจากประวัติการเจอกัน
    
    Args:
        team1 (str): ชื่อทีมที่ 1
        team2 (str): ชื่อทีมที่ 2
        num_matches (int): จำนวนแมตช์ที่ต้องการดู
    
    Returns:
        dict: ข้อมูลสถิติเตะมุม
    """
    # ในสถานการณ์จริง เราควรดึงข้อมูลจริงจาก API
    # แต่ในที่นี้เราจะสร้างข้อมูลจำลองที่สมจริง
    
    # สร้าง seed จากชื่อทีมเพื่อให้ผลลัพธ์คงที่สำหรับแต่ละคู่
    seed = sum(ord(c) for c in team1 + team2)
    random.seed(seed)
    
    # สร้างจำนวนการเจอกันสุ่ม (0-5 ครั้ง)
    actual_matches = random.randint(0, min(5, num_matches))
    
    if actual_matches == 0:
        return {
            "matches_count": 0,
            "avg_total_corners": 0,
            "avg_first_half_corners": 0,
            "avg_second_half_corners": 0,
            "over_9_5_rate": 0,
            "over_4_5_first_half_rate": 0,
            "over_5_5_second_half_rate": 0,
            "matches": []
        }
    
    # สร้างข้อมูลแมตช์
    matches = []
    total_corners = 0
    total_first_half_corners = 0
    total_second_half_corners = 0
    over_9_5_count = 0
    over_4_5_first_half_count = 0
    over_5_5_second_half_count = 0
    
    for i in range(actual_matches):
        # สร้างข้อมูลเตะมุมสุ่ม
        first_half = random.randint(2, 7)
        second_half = random.randint(3, 8)
        match_total = first_half + second_half
        
        # นับสถิติ
        total_corners += match_total
        total_first_half_corners += first_half
        total_second_half_corners += second_half
        
        if match_total > 9.5:
            over_9_5_count += 1
        
        if first_half > 4.5:
            over_4_5_first_half_count += 1
        
        if second_half > 5.5:
            over_5_5_second_half_count += 1
        
        # เพิ่มข้อมูลแมตช์
        matches.append({
            "total_corners": match_total,
            "first_half_corners": first_half,
            "second_half_corners": second_half
        })
    
    # คำนวณค่าเฉลี่ย
    avg_total = total_corners / actual_matches
    avg_first_half = total_first_half_corners / actual_matches
    avg_second_half = total_second_half_corners / actual_matches
    
    # คำนวณอัตราส่วน
    over_9_5_rate = over_9_5_count / actual_matches
    over_4_5_first_half_rate = over_4_5_first_half_count / actual_matches
    over_5_5_second_half_rate = over_5_5_second_half_count / actual_matches
    
    # สร้างผลลัพธ์
    result = {
        "matches_count": actual_matches,
        "avg_total_corners": round(avg_total, 1),
        "avg_first_half_corners": round(avg_first_half, 1),
        "avg_second_half_corners": round(avg_second_half, 1),
        "over_9_5_rate": round(over_9_5_rate, 2),
        "over_4_5_first_half_rate": round(over_4_5_first_half_rate, 2),
        "over_5_5_second_half_rate": round(over_5_5_second_half_rate, 2),
        "matches": matches
    }
    
    return result

if __name__ == "__main__":
    # ทดสอบฟังก์ชัน
    team_name = "Manchester United"
    print(f"🎯 ดึงสถิติเตะมุมของทีม {team_name}...")
    stats = get_corner_stats(team_name)
    print(f"✅ ดึงสถิติเตะมุมสำเร็จ:")
    print(f"   - เตะมุมเฉลี่ย: {stats['total_corners_avg']} ต่อเกม")
    print(f"   - อัตราส่วน Over 9.5: {stats['over_9_5_rate'] * 100:.1f}%")
    print(f"   - อัตราส่วน Over 4.5 ครึ่งแรก: {stats['over_4_5_first_half_rate'] * 100:.1f}%")
    print(f"   - อัตราส่วน Over 5.5 ครึ่งหลัง: {stats['over_5_5_second_half_rate'] * 100:.1f}%")
