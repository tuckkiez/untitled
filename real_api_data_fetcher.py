#!/usr/bin/env python3
"""
🚀 Real API Data Fetcher - ดึงข้อมูลจริงจาก API-Sports
ดึงข้อมูลการแข่งขันวันที่ 13 กรกฎาคม 2025 และจัดกลุ่มตามลีกสำคัญ
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any
import time

class RealAPIDataFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        
        # ลีกสำคัญที่เราสนใจ
        self.major_leagues = {
            39: {"name": "Premier League", "country": "England", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
            140: {"name": "La Liga", "country": "Spain", "flag": "🇪🇸"},
            78: {"name": "Bundesliga", "country": "Germany", "flag": "🇩🇪"},
            135: {"name": "Serie A", "country": "Italy", "flag": "🇮🇹"},
            61: {"name": "Ligue 1", "country": "France", "flag": "🇫🇷"},
            293: {"name": "K League 2", "country": "South Korea", "flag": "🇰🇷"},
            253: {"name": "Major League Soccer", "country": "USA", "flag": "🇺🇸"},
            262: {"name": "Liga MX", "country": "Mexico", "flag": "🇲🇽"},
            71: {"name": "Serie A", "country": "Brazil", "flag": "🇧🇷"},
            239: {"name": "Primera A", "country": "Colombia", "flag": "🇨🇴"},
            113: {"name": "Allsvenskan", "country": "Sweden", "flag": "🇸🇪"},
            103: {"name": "Eliteserien", "country": "Norway", "flag": "🇳🇴"},
            244: {"name": "Veikkausliiga", "country": "Finland", "flag": "🇫🇮"},
            170: {"name": "League One", "country": "China", "flag": "🇨🇳"},
            497: {"name": "Japan Football League", "country": "Japan", "flag": "🇯🇵"}
        }
        
    def fetch_todays_matches(self, date: str = "2025-07-13") -> Dict:
        """ดึงข้อมูลการแข่งขันวันที่กำหนด"""
        url = f"{self.base_url}/fixtures"
        params = {'date': date}
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ API Error: {response.status_code}")
                return {}
        except Exception as e:
            print(f"🚨 Request Error: {e}")
            return {}
    
    def categorize_matches(self, api_data: Dict) -> Dict[str, List[Dict]]:
        """จัดกลุ่มการแข่งขันตามลีก"""
        if not api_data or 'response' not in api_data:
            return {}
        
        categorized = {}
        other_matches = []
        
        for match in api_data['response']:
            league_id = match['league']['id']
            league_name = match['league']['name']
            country = match['league']['country']
            
            # ตรวจสอบว่าเป็นลีกสำคัญหรือไม่
            if league_id in self.major_leagues:
                league_info = self.major_leagues[league_id]
                category_key = f"{league_info['flag']} {league_info['name']} ({league_info['country']})"
            else:
                # ลีกอื่นๆ ที่น่าสนใจ
                if any(keyword in league_name.lower() for keyword in ['premier', 'liga', 'league', 'championship', 'cup']):
                    category_key = f"🌍 {league_name} ({country})"
                else:
                    other_matches.append(match)
                    continue
            
            if category_key not in categorized:
                categorized[category_key] = []
            
            # เก็บเฉพาะข้อมูลที่จำเป็น
            match_info = {
                'fixture_id': match['fixture']['id'],
                'home_team': match['teams']['home']['name'],
                'away_team': match['teams']['away']['name'],
                'home_id': match['teams']['home']['id'],
                'away_id': match['teams']['away']['id'],
                'date': match['fixture']['date'],
                'status': match['fixture']['status']['short'],
                'venue': match['fixture']['venue']['name'] if match['fixture']['venue'] else 'TBD',
                'league_id': league_id,
                'league_name': league_name,
                'country': country
            }
            
            # เพิ่มผลการแข่งขันถ้าจบแล้ว
            if match['fixture']['status']['short'] == 'FT':
                match_info['home_goals'] = match['goals']['home']
                match_info['away_goals'] = match['goals']['away']
            
            categorized[category_key].append(match_info)
        
        # เรียงลำดับตามความสำคัญ
        sorted_categories = {}
        
        # ลีกใหญ่ก่อน
        for league_id, info in self.major_leagues.items():
            key = f"{info['flag']} {info['name']} ({info['country']})"
            if key in categorized:
                sorted_categories[key] = categorized[key]
        
        # ลีกอื่นๆ ตาม
        for key in sorted(categorized.keys()):
            if key not in sorted_categories:
                sorted_categories[key] = categorized[key]
        
        return sorted_categories
    
    def get_match_summary(self, categorized_matches: Dict) -> Dict:
        """สรุปข้อมูลการแข่งขัน"""
        summary = {
            'total_leagues': len(categorized_matches),
            'total_matches': sum(len(matches) for matches in categorized_matches.values()),
            'leagues_breakdown': {}
        }
        
        for league, matches in categorized_matches.items():
            finished = len([m for m in matches if m['status'] == 'FT'])
            upcoming = len([m for m in matches if m['status'] in ['NS', 'TBD']])
            live = len([m for m in matches if m['status'] in ['1H', '2H', 'HT']])
            
            summary['leagues_breakdown'][league] = {
                'total': len(matches),
                'finished': finished,
                'upcoming': upcoming,
                'live': live
            }
        
        return summary

if __name__ == "__main__":
    # ทดสอบระบบ
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    fetcher = RealAPIDataFetcher(api_key)
    
    print("🚀 Real API Data Fetcher - July 13, 2025")
    print("=" * 60)
    
    # ดึงข้อมูล
    print("📥 กำลังดึงข้อมูลจาก API...")
    api_data = fetcher.fetch_todays_matches()
    
    if api_data:
        print(f"✅ ดึงข้อมูลได้ {api_data.get('results', 0)} การแข่งขัน")
        
        # จัดกลุ่ม
        print("📊 กำลังจัดกลุ่มตามลีก...")
        categorized = fetcher.categorize_matches(api_data)
        
        # สรุป
        summary = fetcher.get_match_summary(categorized)
        
        print(f"\n📈 สรุปผล:")
        print(f"🏆 ลีกทั้งหมด: {summary['total_leagues']}")
        print(f"⚽ การแข่งขันทั้งหมด: {summary['total_matches']}")
        
        print(f"\n🔥 ลีกที่มีการแข่งขัน:")
        for league, info in summary['leagues_breakdown'].items():
            print(f"   {league}: {info['total']} นัด (จบแล้ว: {info['finished']}, กำลังแข่ง: {info['live']}, ยังไม่เริ่ม: {info['upcoming']})")
        
        # แสดงตัวอย่างการแข่งขันจากลีกสำคัญ
        print(f"\n⚽ ตัวอย่างการแข่งขัน:")
        count = 0
        for league, matches in categorized.items():
            if count >= 10:  # แสดงแค่ 10 นัดแรก
                break
            for match in matches[:2]:  # แสดงแค่ 2 นัดต่อลีก
                status_emoji = "✅" if match['status'] == 'FT' else "🔴" if match['status'] in ['1H', '2H', 'HT'] else "⏰"
                print(f"   {status_emoji} {match['home_team']} vs {match['away_team']} ({league})")
                count += 1
                if count >= 10:
                    break
        
        # บันทึกข้อมูลลงไฟล์
        output_file = f"real_matches_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': summary,
                'categorized_matches': categorized,
                'fetch_time': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 บันทึกข้อมูลลงไฟล์: {output_file}")
        
    else:
        print("❌ ไม่สามารถดึงข้อมูลได้")
