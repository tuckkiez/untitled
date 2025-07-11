#!/usr/bin/env python3
"""
Sportmonks API Tester V2 - Direct Argentina League Search
ค้นหา Argentina Primera Division โดยตรงจาก leagues
"""

import requests
import json
from datetime import datetime, timedelta

class SportmonksAPI:
    def __init__(self):
        self.api_token = "1TQD9tFVUJ55dd31y6ECZ5FYeFKb8atMhavYD0tQfWgiRWISpTcDJgJ1Cclf"
        self.base_url = "https://api.sportmonks.com/v3/football"
        self.session = requests.Session()
    
    def make_request(self, endpoint, params=None):
        """ส่ง request ไป Sportmonks API"""
        if params is None:
            params = {}
        
        params['api_token'] = self.api_token
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            print(f"📡 Testing: {endpoint}")
            response = self.session.get(url, params=params, timeout=15)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success: {endpoint}")
                return data
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Response: {response.text[:300]}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_all_leagues(self):
        """ดึงลีกทั้งหมดและหา Argentina"""
        print("🔍 Getting all leagues...")
        
        # ลองดึงลีกทั้งหมดพร้อม includes
        params = {
            'include': 'country,currentSeason',
            'per_page': 100  # เพิ่มจำนวนต่อหน้า
        }
        
        data = self.make_request('leagues', params)
        
        if data and 'data' in data:
            leagues = data['data']
            print(f"✅ Found {len(leagues)} leagues total")
            
            # หา Argentina leagues
            argentina_leagues = []
            
            for league in leagues:
                league_name = league.get('name', '').lower()
                country_info = league.get('country', {})
                country_name = country_info.get('name', '').lower() if country_info else ''
                
                # ค้นหาคำที่เกี่ยวข้องกับ Argentina
                argentina_keywords = ['argentina', 'argentine', 'primera division', 'superliga argentina']
                
                if any(keyword in league_name for keyword in argentina_keywords) or 'argentina' in country_name:
                    argentina_leagues.append(league)
                    print(f"🇦🇷 Found: {league.get('name')} (ID: {league.get('id')})")
                    if country_info:
                        print(f"   Country: {country_info.get('name', 'Unknown')}")
            
            return argentina_leagues
        
        return []
    
    def explore_league_structure(self, league_id):
        """สำรวจโครงสร้างของลีก"""
        print(f"\n🔍 Exploring league structure for ID: {league_id}")
        
        # ลองดึงข้อมูลลีกพร้อม includes ต่างๆ
        includes_to_try = [
            'country',
            'seasons',
            'currentSeason',
            'teams',
            'fixtures'
        ]
        
        for include in includes_to_try:
            print(f"\n📊 Testing include: {include}")
            params = {'include': include}
            
            data = self.make_request(f'leagues/{league_id}', params)
            
            if data and 'data' in data:
                league_data = data['data']
                
                if include in league_data:
                    included_data = league_data[include]
                    if isinstance(included_data, list):
                        print(f"   ✅ {include}: {len(included_data)} items")
                        if included_data:
                            print(f"   Sample keys: {list(included_data[0].keys())[:5]}")
                    elif isinstance(included_data, dict):
                        print(f"   ✅ {include}: {list(included_data.keys())[:5]}")
                    else:
                        print(f"   ✅ {include}: {included_data}")
                else:
                    print(f"   ❌ {include}: Not found in response")
    
    def get_league_seasons(self, league_id):
        """ดึงซีซั่นของลีก"""
        print(f"\n🏆 Getting seasons for league: {league_id}")
        
        params = {
            'filters': f'leagueId:{league_id}',
            'include': 'league',
            'per_page': 50
        }
        
        data = self.make_request('seasons', params)
        
        if data and 'data' in data:
            seasons = data['data']
            print(f"✅ Found {len(seasons)} seasons")
            
            # หาซีซั่นปัจจุบัน (2024)
            current_seasons = []
            for season in seasons:
                season_name = season.get('name', '')
                if '2024' in season_name or 'current' in season_name.lower():
                    current_seasons.append(season)
                    print(f"   🎯 Current: {season_name} (ID: {season.get('id')})")
            
            # แสดงซีซั่นทั้งหมด
            print(f"\n   All seasons:")
            for i, season in enumerate(seasons[-10:]):  # แสดง 10 ซีซั่นล่าสุด
                print(f"   {i+1}. {season.get('name')} (ID: {season.get('id')})")
            
            return current_seasons if current_seasons else seasons[-1:]  # ใช้ซีซั่นล่าสุด
        
        return []
    
    def get_fixtures_for_season(self, season_id, limit=20):
        """ดึงแมทช์ในซีซั่น"""
        print(f"\n⚽ Getting fixtures for season: {season_id}")
        
        params = {
            'filters': f'seasonId:{season_id}',
            'include': 'participants,scores,state',
            'per_page': limit
        }
        
        data = self.make_request('fixtures', params)
        
        if data and 'data' in data:
            fixtures = data['data']
            print(f"✅ Found {len(fixtures)} fixtures")
            
            processed_matches = []
            
            for i, fixture in enumerate(fixtures):
                # ดึงข้อมูลทีม
                participants = fixture.get('participants', [])
                home_team = None
                away_team = None
                
                for participant in participants:
                    meta = participant.get('meta', {})
                    if meta.get('location') == 'home':
                        home_team = participant.get('name', 'Unknown')
                    elif meta.get('location') == 'away':
                        away_team = participant.get('name', 'Unknown')
                
                # ดึงสกอร์
                scores = fixture.get('scores', [])
                home_score = None
                away_score = None
                
                for score in scores:
                    score_data = score.get('score', {})
                    participant_id = score.get('participant_id')
                    
                    # หา participant ที่ตรงกัน
                    for participant in participants:
                        if participant.get('id') == participant_id:
                            meta = participant.get('meta', {})
                            if meta.get('location') == 'home':
                                home_score = score_data.get('goals')
                            elif meta.get('location') == 'away':
                                away_score = score_data.get('goals')
                
                # สถานะแมทช์
                state = fixture.get('state', {})
                status = state.get('short_name', 'Unknown')
                
                match_info = {
                    'id': fixture.get('id'),
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_score': home_score,
                    'away_score': away_score,
                    'date': fixture.get('starting_at'),
                    'status': status,
                    'finished': status in ['FT', 'AET', 'PEN']
                }
                
                processed_matches.append(match_info)
                
                # แสดงตัวอย่าง
                if i < 5:
                    print(f"   {i+1}. {home_team} vs {away_team}")
                    if home_score is not None and away_score is not None:
                        print(f"      Score: {home_score}-{away_score}")
                    print(f"      Date: {fixture.get('starting_at')}")
                    print(f"      Status: {status}")
            
            return processed_matches
        
        return []

def main():
    print("🇦🇷 Sportmonks API V2 - Argentina Primera Division Hunter")
    print("=" * 70)
    
    api = SportmonksAPI()
    
    # ค้นหาลีกอาร์เจนติน่า
    argentina_leagues = api.get_all_leagues()
    
    if not argentina_leagues:
        print("❌ No Argentina leagues found")
        return
    
    # เลือกลีกแรก
    main_league = argentina_leagues[0]
    league_id = main_league.get('id')
    league_name = main_league.get('name')
    
    print(f"\n🎯 Selected League: {league_name} (ID: {league_id})")
    
    # สำรวจโครงสร้าง
    api.explore_league_structure(league_id)
    
    # ดึงซีซั่น
    seasons = api.get_league_seasons(league_id)
    
    if seasons:
        current_season = seasons[0]
        season_id = current_season.get('id')
        season_name = current_season.get('name')
        
        print(f"\n🏆 Using Season: {season_name} (ID: {season_id})")
        
        # ดึงแมทช์
        matches = api.get_fixtures_for_season(season_id, limit=30)
        
        if matches:
            # กรองแมทช์ที่จบแล้ว
            finished_matches = [m for m in matches if m['finished'] and m['home_score'] is not None]
            upcoming_matches = [m for m in matches if not m['finished']]
            
            print(f"\n📊 FINAL RESULTS")
            print("=" * 50)
            print(f"✅ League: {league_name}")
            print(f"✅ Season: {season_name}")
            print(f"✅ Total Matches: {len(matches)}")
            print(f"✅ Finished Matches: {len(finished_matches)}")
            print(f"✅ Upcoming Matches: {len(upcoming_matches)}")
            
            # บันทึกข้อมูล
            real_argentina_data = {
                'league': {
                    'id': league_id,
                    'name': league_name,
                    'full_data': main_league
                },
                'season': {
                    'id': season_id,
                    'name': season_name,
                    'full_data': current_season
                },
                'matches': {
                    'all': matches,
                    'finished': finished_matches,
                    'upcoming': upcoming_matches
                },
                'api_info': {
                    'source': 'Sportmonks API',
                    'retrieved_at': datetime.now().isoformat(),
                    'api_token_used': True
                }
            }
            
            # บันทึกไฟล์
            try:
                with open('argentina_real_sportmonks_data.json', 'w', encoding='utf-8') as f:
                    json.dump(real_argentina_data, f, indent=2, ensure_ascii=False)
                print(f"✅ Real data saved to argentina_real_sportmonks_data.json")
                
                print(f"\n🚀 SUCCESS: Real Argentina Primera Division data retrieved!")
                print(f"   Ready to create predictor with REAL match data")
                print(f"   {len(finished_matches)} finished matches for training")
                print(f"   {len(upcoming_matches)} upcoming matches for prediction")
                
            except Exception as e:
                print(f"❌ Error saving data: {e}")
        
        else:
            print("❌ No matches found")
    else:
        print("❌ No seasons found")

if __name__ == "__main__":
    main()
