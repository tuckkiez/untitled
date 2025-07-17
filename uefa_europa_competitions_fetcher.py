#!/usr/bin/env python3
"""
🚀 UEFA Europa Competitions Fetcher - July 17, 2025
ดึงข้อมูลการแข่งขัน UEFA Europa League และ UEFA Europa Conference League 2025-2026
"""

import requests
import json
from datetime import datetime
import pytz
from typing import Dict, List, Any
import time

class UEFAEuropaCompetitionsFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        
        # UEFA competitions IDs
        self.competitions = {
            3: {"name": "UEFA Europa League", "short_name": "UEL", "flag": "🇪🇺"},
            848: {"name": "UEFA Europa Conference League", "short_name": "UECL", "flag": "🇪🇺"}
        }
        
        # Thai timezone for conversion
        self.thai_tz = pytz.timezone('Asia/Bangkok')
        
    def fetch_competition_fixtures(self, league_id: int, season: int = 2025) -> Dict:
        """ดึงข้อมูลการแข่งขันของลีกที่กำหนด"""
        url = f"{self.base_url}/fixtures"
        params = {'league': league_id, 'season': season}
        
        try:
            print(f"📥 กำลังดึงข้อมูลการแข่งขัน League ID: {league_id}, Season: {season}...")
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ ดึงข้อมูลสำเร็จ: {data.get('results', 0)} รายการ")
                return data
            else:
                print(f"❌ API Error: {response.status_code}")
                return {}
        except Exception as e:
            print(f"🚨 Request Error: {e}")
            return {}
    
    def process_fixtures(self, api_data: Dict, competition_info: Dict) -> List[Dict]:
        """แปลงข้อมูลการแข่งขันให้อยู่ในรูปแบบที่ต้องการ"""
        if not api_data or 'response' not in api_data:
            return []
        
        processed_fixtures = []
        
        for fixture in api_data['response']:
            # ข้อมูลพื้นฐาน
            fixture_data = {
                'fixture_id': fixture['fixture']['id'],
                'competition': competition_info['name'],
                'competition_short': competition_info['short_name'],
                'flag': competition_info['flag'],
                'round': fixture['league']['round'],
                'home_team': fixture['teams']['home']['name'],
                'away_team': fixture['teams']['away']['name'],
                'home_id': fixture['teams']['home']['id'],
                'away_id': fixture['teams']['away']['id'],
                'kickoff_utc': fixture['fixture']['date'],
                'venue': f"{fixture['fixture']['venue']['name'] if fixture['fixture']['venue']['name'] else 'TBD'}, {fixture['fixture']['venue']['city'] if fixture['fixture']['venue']['city'] else 'TBD'}",
                'referee': fixture['fixture']['referee'] if fixture['fixture']['referee'] else 'TBA',
                'status': fixture['fixture']['status']['short'],
            }
            
            # แปลงเวลาเป็น Thai Time
            if fixture_data['kickoff_utc']:
                utc_time = datetime.fromisoformat(fixture_data['kickoff_utc'].replace('Z', '+00:00'))
                thai_time = utc_time.astimezone(self.thai_tz)
                fixture_data['kickoff_thai'] = thai_time.strftime('%Y-%m-%d %H:%M')
                fixture_data['kickoff_thai_time'] = thai_time.strftime('%H:%M')
                fixture_data['match_date'] = thai_time.strftime('%Y-%m-%d')
            
            # เพิ่มผลการแข่งขันถ้าจบแล้ว
            if fixture['fixture']['status']['short'] == 'FT':
                fixture_data['home_goals'] = fixture['goals']['home']
                fixture_data['away_goals'] = fixture['goals']['away']
                fixture_data['score'] = f"{fixture['goals']['home']} - {fixture['goals']['away']}"
                fixture_data['winner'] = fixture['teams']['home']['winner'] and 'home' or fixture['teams']['away']['winner'] and 'away' or 'draw'
            
            processed_fixtures.append(fixture_data)
        
        # เรียงตามวันที่และเวลา
        processed_fixtures.sort(key=lambda x: x['kickoff_utc'])
        
        return processed_fixtures
    
    def categorize_by_round(self, fixtures: List[Dict]) -> Dict[str, List[Dict]]:
        """จัดกลุ่มการแข่งขันตามรอบ"""
        categorized = {}
        
        for fixture in fixtures:
            round_key = fixture['round']
            if round_key not in categorized:
                categorized[round_key] = []
            
            categorized[round_key].append(fixture)
        
        return categorized
    
    def get_competition_summary(self, fixtures: List[Dict]) -> Dict:
        """สรุปข้อมูลการแข่งขัน"""
        if not fixtures:
            return {}
            
        # จัดกลุ่มตามรอบ
        rounds = {}
        for fixture in fixtures:
            round_name = fixture['round']
            if round_name not in rounds:
                rounds[round_name] = []
            rounds[round_name].append(fixture)
        
        # นับสถานะ
        status_count = {
            'upcoming': len([f for f in fixtures if f['status'] in ['NS', 'TBD']]),
            'finished': len([f for f in fixtures if f['status'] == 'FT']),
            'live': len([f for f in fixtures if f['status'] in ['1H', '2H', 'HT']])
        }
        
        # หาวันที่แข่งขันที่เร็วที่สุดและช้าที่สุด
        dates = [datetime.fromisoformat(f['kickoff_utc'].replace('Z', '+00:00')) for f in fixtures if f['kickoff_utc']]
        first_match = min(dates).strftime('%Y-%m-%d') if dates else 'N/A'
        last_match = max(dates).strftime('%Y-%m-%d') if dates else 'N/A'
        
        return {
            'competition': fixtures[0]['competition'],
            'total_fixtures': len(fixtures),
            'rounds': {round_name: len(matches) for round_name, matches in rounds.items()},
            'status': status_count,
            'first_match': first_match,
            'last_match': last_match
        }

    def fetch_all_competitions(self) -> Dict:
        """ดึงข้อมูลทั้งหมดจากทุกการแข่งขัน"""
        all_data = {
            'europa_league': [],
            'conference_league': [],
            'summary': {},
            'fetch_time': datetime.now().isoformat()
        }
        
        # ดึงข้อมูล Europa League
        print("\n🏆 กำลังดึงข้อมูล UEFA Europa League 2025-2026...")
        uel_data = self.fetch_competition_fixtures(3, 2025)
        if uel_data:
            uel_fixtures = self.process_fixtures(uel_data, self.competitions[3])
            all_data['europa_league'] = uel_fixtures
            all_data['europa_league_by_round'] = self.categorize_by_round(uel_fixtures)
            all_data['summary']['europa_league'] = self.get_competition_summary(uel_fixtures)
            print(f"✅ ดึงข้อมูล UEFA Europa League สำเร็จ: {len(uel_fixtures)} รายการ")
        
        # หน่วงเวลาเล็กน้อยเพื่อไม่ให้ API โดน rate limit
        time.sleep(1)
        
        # ดึงข้อมูล Europa Conference League
        print("\n🏆 กำลังดึงข้อมูล UEFA Europa Conference League 2025-2026...")
        uecl_data = self.fetch_competition_fixtures(848, 2025)
        if uecl_data:
            uecl_fixtures = self.process_fixtures(uecl_data, self.competitions[848])
            all_data['conference_league'] = uecl_fixtures
            all_data['conference_league_by_round'] = self.categorize_by_round(uecl_fixtures)
            all_data['summary']['conference_league'] = self.get_competition_summary(uecl_fixtures)
            print(f"✅ ดึงข้อมูล UEFA Europa Conference League สำเร็จ: {len(uecl_fixtures)} รายการ")
        
        return all_data

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 UEFA Europa Competitions Fetcher - July 17, 2025")
    print("=" * 60)
    
    # API key จาก RapidAPI
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # สร้าง fetcher
    fetcher = UEFAEuropaCompetitionsFetcher(api_key)
    
    # ดึงข้อมูลทั้งหมด
    all_data = fetcher.fetch_all_competitions()
    
    # แสดงสรุป
    print("\n📊 สรุปข้อมูล:")
    
    if 'europa_league' in all_data and all_data['europa_league']:
        uel_summary = all_data['summary']['europa_league']
        print(f"\n🏆 UEFA Europa League 2025-2026:")
        print(f"   📅 ทั้งหมด: {uel_summary['total_fixtures']} นัด")
        print(f"   🗓️ ช่วงเวลา: {uel_summary['first_match']} ถึง {uel_summary['last_match']}")
        print(f"   🔄 สถานะ: จบแล้ว {uel_summary['status']['finished']} นัด, กำลังแข่ง {uel_summary['status']['live']} นัด, ยังไม่เริ่ม {uel_summary['status']['upcoming']} นัด")
        print(f"   🏅 รอบการแข่งขัน:")
        for round_name, count in uel_summary['rounds'].items():
            print(f"      - {round_name}: {count} นัด")
    else:
        print("❌ ไม่พบข้อมูล UEFA Europa League")
    
    if 'conference_league' in all_data and all_data['conference_league']:
        uecl_summary = all_data['summary']['conference_league']
        print(f"\n🏆 UEFA Europa Conference League 2025-2026:")
        print(f"   📅 ทั้งหมด: {uecl_summary['total_fixtures']} นัด")
        print(f"   🗓️ ช่วงเวลา: {uecl_summary['first_match']} ถึง {uecl_summary['last_match']}")
        print(f"   🔄 สถานะ: จบแล้ว {uecl_summary['status']['finished']} นัด, กำลังแข่ง {uecl_summary['status']['live']} นัด, ยังไม่เริ่ม {uecl_summary['status']['upcoming']} นัด")
        print(f"   🏅 รอบการแข่งขัน:")
        for round_name, count in uecl_summary['rounds'].items():
            print(f"      - {round_name}: {count} นัด")
    else:
        print("❌ ไม่พบข้อมูล UEFA Europa Conference League")
    
    # บันทึกข้อมูลลงไฟล์
    output_file = "uefa_europa_competitions_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 บันทึกข้อมูลลงไฟล์: {output_file}")
    print(f"✅ เสร็จสมบูรณ์!")

if __name__ == "__main__":
    main()
