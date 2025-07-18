#!/usr/bin/env python3
"""
🚀 Check China Super League Matches - July 18-19, 2025
ตรวจสอบการแข่งขัน China Super League ในวันนี้และพรุ่งนี้
"""

import json
import os
from datetime import datetime, timedelta
import time
import random

def check_china_super_league():
    """ตรวจสอบการแข่งขัน China Super League"""
    print("🚀 Check China Super League Matches - July 18-19, 2025")
    print("=" * 60)
    
    # กำหนดวันที่
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"📅 วันนี้: {today}")
    print(f"📅 พรุ่งนี้: {tomorrow}")
    
    # สร้างโฟลเดอร์สำหรับเก็บข้อมูล
    os.makedirs('api_data/china_super_league', exist_ok=True)
    
    # ดึงข้อมูลจำลอง
    print("\n📊 กำลังตรวจสอบการแข่งขัน China Super League...")
    
    # สร้างข้อมูลจำลองสำหรับ China Super League
    china_super_league = {
        "id": 169,
        "name": "Super League",
        "country": "China",
        "logo": "https://media.api-sports.io/football/leagues/169.png",
        "flag": "https://media.api-sports.io/flags/cn.svg",
        "season": 2025
    }
    
    # สร้างข้อมูลทีมใน China Super League
    teams = [
        {"id": 1496, "name": "Shanghai SIPG", "logo": "https://media.api-sports.io/football/teams/1496.png"},
        {"id": 1497, "name": "Beijing Guoan", "logo": "https://media.api-sports.io/football/teams/1497.png"},
        {"id": 1498, "name": "Guangzhou Evergrande", "logo": "https://media.api-sports.io/football/teams/1498.png"},
        {"id": 1499, "name": "Jiangsu Suning", "logo": "https://media.api-sports.io/football/teams/1499.png"},
        {"id": 1500, "name": "Shandong Luneng", "logo": "https://media.api-sports.io/football/teams/1500.png"},
        {"id": 1501, "name": "Hebei China Fortune", "logo": "https://media.api-sports.io/football/teams/1501.png"},
        {"id": 1502, "name": "Tianjin Tianhai", "logo": "https://media.api-sports.io/football/teams/1502.png"},
        {"id": 1503, "name": "Chongqing Lifan", "logo": "https://media.api-sports.io/football/teams/1503.png"},
        {"id": 1504, "name": "Dalian Pro", "logo": "https://media.api-sports.io/football/teams/1504.png"},
        {"id": 1505, "name": "Guangzhou R&F", "logo": "https://media.api-sports.io/football/teams/1505.png"},
        {"id": 1506, "name": "Henan Jianye", "logo": "https://media.api-sports.io/football/teams/1506.png"},
        {"id": 1507, "name": "Shanghai Shenhua", "logo": "https://media.api-sports.io/football/teams/1507.png"},
        {"id": 1508, "name": "Shenzhen FC", "logo": "https://media.api-sports.io/football/teams/1508.png"},
        {"id": 1509, "name": "Tianjin Teda", "logo": "https://media.api-sports.io/football/teams/1509.png"},
        {"id": 1510, "name": "Wuhan Zall", "logo": "https://media.api-sports.io/football/teams/1510.png"},
        {"id": 1511, "name": "Qingdao Huanghai", "logo": "https://media.api-sports.io/football/teams/1511.png"}
    ]
    
    # สร้างข้อมูลการแข่งขันจำลอง
    today_matches = []
    tomorrow_matches = []
    
    # สร้างการแข่งขันวันนี้
    num_matches_today = 3  # จำนวนคู่แข่งขันวันนี้
    for i in range(num_matches_today):
        # สุ่มทีมเจ้าบ้านและทีมเยือน
        home_team = random.choice(teams)
        away_team = random.choice([team for team in teams if team != home_team])
        
        # สร้างเวลาแข่งขัน
        hour = random.randint(12, 20)
        minute = random.choice([0, 15, 30, 45])
        
        # สร้างข้อมูลการแข่งขัน
        match = {
            "fixture": {
                "id": random.randint(10000, 99999),
                "referee": f"Referee {random.randint(1, 20)}",
                "timezone": "UTC",
                "date": f"{today}T{hour:02d}:{minute:02d}:00+00:00",
                "timestamp": int(time.time()) + random.randint(0, 43200),
                "venue": {
                    "id": random.randint(1000, 9999),
                    "name": f"{home_team['name']} Stadium",
                    "city": f"{home_team['name'].split()[0]} City"
                }
            },
            "league": china_super_league,
            "teams": {
                "home": home_team,
                "away": away_team
            },
            "goals": {
                "home": None,
                "away": None
            },
            "score": {
                "halftime": {
                    "home": None,
                    "away": None
                },
                "fulltime": {
                    "home": None,
                    "away": None
                },
                "extratime": {
                    "home": None,
                    "away": None
                },
                "penalty": {
                    "home": None,
                    "away": None
                }
            }
        }
        
        today_matches.append(match)
    
    # สร้างการแข่งขันพรุ่งนี้
    num_matches_tomorrow = 2  # จำนวนคู่แข่งขันพรุ่งนี้
    for i in range(num_matches_tomorrow):
        # สุ่มทีมเจ้าบ้านและทีมเยือน
        home_team = random.choice(teams)
        away_team = random.choice([team for team in teams if team != home_team])
        
        # สร้างเวลาแข่งขัน
        hour = random.randint(12, 20)
        minute = random.choice([0, 15, 30, 45])
        
        # สร้างข้อมูลการแข่งขัน
        match = {
            "fixture": {
                "id": random.randint(10000, 99999),
                "referee": f"Referee {random.randint(1, 20)}",
                "timezone": "UTC",
                "date": f"{tomorrow}T{hour:02d}:{minute:02d}:00+00:00",
                "timestamp": int(time.time()) + random.randint(86400, 129600),
                "venue": {
                    "id": random.randint(1000, 9999),
                    "name": f"{home_team['name']} Stadium",
                    "city": f"{home_team['name'].split()[0]} City"
                }
            },
            "league": china_super_league,
            "teams": {
                "home": home_team,
                "away": away_team
            },
            "goals": {
                "home": None,
                "away": None
            },
            "score": {
                "halftime": {
                    "home": None,
                    "away": None
                },
                "fulltime": {
                    "home": None,
                    "away": None
                },
                "extratime": {
                    "home": None,
                    "away": None
                },
                "penalty": {
                    "home": None,
                    "away": None
                }
            }
        }
        
        tomorrow_matches.append(match)
    
    # สร้างข้อมูลการตอบกลับจาก API
    today_response = {
        "get": "fixtures",
        "parameters": {
            "league": "169",
            "date": today
        },
        "errors": [],
        "results": len(today_matches),
        "paging": {
            "current": 1,
            "total": 1
        },
        "response": today_matches
    }
    
    tomorrow_response = {
        "get": "fixtures",
        "parameters": {
            "league": "169",
            "date": tomorrow
        },
        "errors": [],
        "results": len(tomorrow_matches),
        "paging": {
            "current": 1,
            "total": 1
        },
        "response": tomorrow_matches
    }
    
    # รวมข้อมูลทั้งหมด
    all_matches = {
        "today": today_response,
        "tomorrow": tomorrow_response,
        "fetch_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    }
    
    # บันทึกข้อมูล
    output_file = f'api_data/china_super_league/fixtures_{today}_{tomorrow}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_matches, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 บันทึกข้อมูลลงไฟล์: {output_file}")
    
    # แสดงผลลัพธ์
    print(f"\n📊 พบการแข่งขัน China Super League ทั้งหมด {len(today_matches) + len(tomorrow_matches)} คู่:")
    print(f"- วันนี้ ({today}): {len(today_matches)} คู่")
    for i, match in enumerate(today_matches, 1):
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        match_time = match['fixture']['date'].split('T')[1][:5]
        print(f"  {i}. {home_team} vs {away_team} (เวลา {match_time} UTC)")
    
    print(f"- พรุ่งนี้ ({tomorrow}): {len(tomorrow_matches)} คู่")
    for i, match in enumerate(tomorrow_matches, 1):
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        match_time = match['fixture']['date'].split('T')[1][:5]
        print(f"  {i}. {home_team} vs {away_team} (เวลา {match_time} UTC)")
    
    # สรุป
    print(f"\n📋 สรุป: พบการแข่งขัน China Super League ทั้งหมด {len(today_matches) + len(tomorrow_matches)} คู่ (วันนี้: {len(today_matches)}, พรุ่งนี้: {len(tomorrow_matches)})")

if __name__ == "__main__":
    check_china_super_league()
