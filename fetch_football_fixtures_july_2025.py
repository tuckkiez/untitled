#!/usr/bin/env python3
"""
🚀 Football Fixtures Fetcher - July 17-18, 2025
ดึงข้อมูลการแข่งขันฟุตบอลวันที่ 17-18 กรกฎาคม 2025 จาก RapidAPI
"""

import requests
import json
from datetime import datetime
import pytz
import time

# API key และ host
API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
API_HOST = "api-football-v1.p.rapidapi.com"
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

# Headers สำหรับ API request
headers = {
    'x-rapidapi-host': API_HOST,
    'x-rapidapi-key': API_KEY
}

def fetch_fixtures_by_date(date):
    """ดึงข้อมูลการแข่งขันตามวันที่"""
    url = f"{BASE_URL}/fixtures"
    params = {'date': date}
    
    print(f"📥 กำลังดึงข้อมูลการแข่งขันวันที่ {date}...")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ ดึงข้อมูลสำเร็จ: {data.get('results', 0)} รายการ")
            return data
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"🚨 Request Error: {e}")
        return None

def process_fixtures(data):
    """แปลงข้อมูลการแข่งขันให้อยู่ในรูปแบบที่ต้องการ"""
    if not data or 'response' not in data:
        return []
    
    thai_tz = pytz.timezone('Asia/Bangkok')
    processed_fixtures = []
    
    for fixture in data['response']:
        # ข้อมูลพื้นฐาน
        fixture_data = {
            'fixture_id': fixture['fixture']['id'],
            'league_id': fixture['league']['id'],
            'league_name': fixture['league']['name'],
            'league_country': fixture['league']['country'],
            'league_logo': fixture['league']['logo'],
            'league_flag': fixture['league']['flag'],
            'round': fixture['league']['round'],
            'home_team': fixture['teams']['home']['name'],
            'away_team': fixture['teams']['away']['name'],
            'home_id': fixture['teams']['home']['id'],
            'away_id': fixture['teams']['away']['id'],
            'home_logo': fixture['teams']['home']['logo'],
            'away_logo': fixture['teams']['away']['logo'],
            'kickoff_utc': fixture['fixture']['date'],
            'venue': f"{fixture['fixture']['venue']['name'] if fixture['fixture']['venue']['name'] else 'TBD'}, {fixture['fixture']['venue']['city'] if fixture['fixture']['venue']['city'] else 'TBD'}",
            'referee': fixture['fixture']['referee'] if fixture['fixture']['referee'] else 'TBA',
            'status': fixture['fixture']['status']['short'],
            'status_long': fixture['fixture']['status']['long'],
        }
        
        # แปลงเวลาเป็น Thai Time
        if fixture_data['kickoff_utc']:
            utc_time = datetime.fromisoformat(fixture_data['kickoff_utc'].replace('Z', '+00:00'))
            thai_time = utc_time.astimezone(thai_tz)
            fixture_data['kickoff_thai'] = thai_time.strftime('%Y-%m-%d %H:%M')
            fixture_data['kickoff_thai_time'] = thai_time.strftime('%H:%M')
            fixture_data['match_date'] = thai_time.strftime('%Y-%m-%d')
            fixture_data['match_day'] = thai_time.strftime('%d')
            fixture_data['match_month'] = thai_time.strftime('%m')
        
        # เพิ่มผลการแข่งขันถ้าจบแล้ว
        if fixture['fixture']['status']['short'] == 'FT':
            fixture_data['home_goals'] = fixture['goals']['home']
            fixture_data['away_goals'] = fixture['goals']['away']
            fixture_data['score'] = f"{fixture['goals']['home']} - {fixture['goals']['away']}"
            fixture_data['winner'] = fixture['teams']['home']['winner'] and 'home' or fixture['teams']['away']['winner'] and 'away' or 'draw'
        
        processed_fixtures.append(fixture_data)
    
    return processed_fixtures

def categorize_by_league(fixtures):
    """จัดกลุ่มการแข่งขันตามลีก"""
    categorized = {}
    
    for fixture in fixtures:
        league_id = fixture['league_id']
        league_name = fixture['league_name']
        
        if league_id not in categorized:
            categorized[league_id] = {
                'league_name': league_name,
                'league_country': fixture['league_country'],
                'league_logo': fixture['league_logo'],
                'league_flag': fixture['league_flag'],
                'fixtures': []
            }
        
        categorized[league_id]['fixtures'].append(fixture)
    
    # เรียงลำดับตามชื่อลีก
    return {k: categorized[k] for k in sorted(categorized.keys(), key=lambda x: categorized[x]['league_name'])}

def categorize_by_uefa_competitions(fixtures):
    """แยกการแข่งขัน UEFA Europa League และ UEFA Europa Conference League"""
    uefa_competitions = {
        'europa_league': [],
        'conference_league': [],
        'other_uefa': [],
        'other': []
    }
    
    for fixture in fixtures:
        league_name = fixture['league_name'].lower()
        
        if 'europa league' in league_name:
            uefa_competitions['europa_league'].append(fixture)
        elif 'conference league' in league_name:
            uefa_competitions['conference_league'].append(fixture)
        elif 'uefa' in league_name or 'champions league' in league_name:
            uefa_competitions['other_uefa'].append(fixture)
        else:
            uefa_competitions['other'].append(fixture)
    
    return uefa_competitions

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Football Fixtures Fetcher - July 17-18, 2025")
    print("=" * 60)
    
    # วันที่ต้องการดึงข้อมูล
    dates = ['2025-07-17', '2025-07-18']
    all_fixtures = []
    
    # ดึงข้อมูลทุกวัน
    for date in dates:
        data = fetch_fixtures_by_date(date)
        if data:
            fixtures = process_fixtures(data)
            all_fixtures.extend(fixtures)
            print(f"📊 วันที่ {date}: {len(fixtures)} รายการ")
        
        # หน่วงเวลาเล็กน้อยเพื่อไม่ให้ API โดน rate limit
        time.sleep(1)
    
    if not all_fixtures:
        print("❌ ไม่พบข้อมูลการแข่งขัน")
        return
    
    # จัดกลุ่มตามลีก
    leagues = categorize_by_league(all_fixtures)
    
    # แยกการแข่งขัน UEFA
    uefa_competitions = categorize_by_uefa_competitions(all_fixtures)
    
    # สรุปข้อมูล
    print("\n📊 สรุปข้อมูล:")
    print(f"📅 จำนวนการแข่งขันทั้งหมด: {len(all_fixtures)} รายการ")
    print(f"🏆 จำนวนลีกทั้งหมด: {len(leagues)} ลีก")
    print(f"🇪🇺 UEFA Europa League: {len(uefa_competitions['europa_league'])} รายการ")
    print(f"🇪🇺 UEFA Europa Conference League: {len(uefa_competitions['conference_league'])} รายการ")
    print(f"🇪🇺 UEFA อื่นๆ: {len(uefa_competitions['other_uefa'])} รายการ")
    
    # บันทึกข้อมูลลงไฟล์
    output = {
        'all_fixtures': all_fixtures,
        'leagues': leagues,
        'uefa_competitions': uefa_competitions,
        'fetch_time': datetime.now().isoformat(),
        'summary': {
            'total_fixtures': len(all_fixtures),
            'total_leagues': len(leagues),
            'europa_league_count': len(uefa_competitions['europa_league']),
            'conference_league_count': len(uefa_competitions['conference_league']),
            'other_uefa_count': len(uefa_competitions['other_uefa']),
            'other_count': len(uefa_competitions['other'])
        }
    }
    
    output_file = "football_fixtures_july_17_18_2025.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 บันทึกข้อมูลลงไฟล์: {output_file}")
    
    # บันทึกข้อมูล UEFA แยกไฟล์
    uefa_output = {
        'europa_league': uefa_competitions['europa_league'],
        'conference_league': uefa_competitions['conference_league'],
        'fetch_time': datetime.now().isoformat()
    }
    
    uefa_output_file = "uefa_competitions_fixtures_july_17_18_2025.json"
    with open(uefa_output_file, 'w', encoding='utf-8') as f:
        json.dump(uefa_output, f, ensure_ascii=False, indent=2)
    
    print(f"💾 บันทึกข้อมูล UEFA ลงไฟล์: {uefa_output_file}")
    print(f"✅ เสร็จสมบูรณ์!")

if __name__ == "__main__":
    main()
