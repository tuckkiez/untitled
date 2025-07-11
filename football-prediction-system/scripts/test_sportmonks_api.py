#!/usr/bin/env python3
"""
Sportmonks API Tester for Argentina Primera Division
ทดสอบ Sportmonks API เพื่อหาข้อมูล Argentina Primera Division จริง
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
                print(f"   Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def test_basic_endpoints(self):
        """ทดสอบ endpoints พื้นฐาน"""
        print("🔍 Testing Basic Endpoints...")
        print("=" * 50)
        
        endpoints = [
            'leagues',
            'countries', 
            'seasons',
            'teams',
            'fixtures'
        ]
        
        results = {}
        
        for endpoint in endpoints:
            data = self.make_request(endpoint)
            if data:
                results[endpoint] = data
                
                # แสดงข้อมูลตัวอย่าง
                if 'data' in data:
                    items = data['data']
                    print(f"   Found {len(items)} items")
                    if items:
                        first_item = items[0]
                        print(f"   Sample: {list(first_item.keys())[:5]}")
                else:
                    print(f"   Data structure: {list(data.keys())}")
            
            print()
        
        return results
    
    def find_argentina_league(self):
        """หาลีกอาร์เจนติน่า"""
        print("🇦🇷 Searching for Argentina Leagues...")
        print("=" * 50)
        
        # ค้นหาประเทศอาร์เจนติน่า
        countries_data = self.make_request('countries')
        
        argentina_country_id = None
        if countries_data and 'data' in countries_data:
            for country in countries_data['data']:
                if 'argentina' in country.get('name', '').lower():
                    argentina_country_id = country.get('id')
                    print(f"✅ Found Argentina: ID {argentina_country_id}")
                    break
        
        if not argentina_country_id:
            print("❌ Argentina country not found")
            return None
        
        # ค้นหาลีกในอาร์เจนติน่า
        leagues_data = self.make_request('leagues', {'filters': f'countryId:{argentina_country_id}'})
        
        argentina_leagues = []
        if leagues_data and 'data' in leagues_data:
            for league in leagues_data['data']:
                league_name = league.get('name', '')
                if any(keyword in league_name.lower() for keyword in ['primera', 'division', 'superliga']):
                    argentina_leagues.append(league)
                    print(f"✅ Found: {league_name} (ID: {league.get('id')})")
        
        return argentina_leagues
    
    def get_league_details(self, league_id):
        """ดึงรายละเอียดลีก"""
        print(f"📊 Getting league details for ID: {league_id}")
        
        # ดึงข้อมูลลีกพร้อม includes
        includes = [
            'country',
            'seasons',
            'seasons.stages',
            'currentSeason'
        ]
        
        params = {
            'include': ','.join(includes)
        }
        
        data = self.make_request(f'leagues/{league_id}', params)
        
        if data and 'data' in data:
            league = data['data']
            print(f"✅ League: {league.get('name')}")
            print(f"   Country: {league.get('country', {}).get('name', 'Unknown')}")
            
            # แสดงซีซั่น
            seasons = league.get('seasons', [])
            print(f"   Seasons: {len(seasons)}")
            
            current_season = league.get('currentSeason')
            if current_season:
                print(f"   Current Season: {current_season.get('name')} (ID: {current_season.get('id')})")
                return current_season.get('id')
        
        return None
    
    def get_season_fixtures(self, season_id):
        """ดึงแมทช์ในซีซั่น"""
        print(f"🏆 Getting fixtures for season: {season_id}")
        
        includes = [
            'participants',
            'scores',
            'statistics',
            'corners'
        ]
        
        params = {
            'filters': f'seasonId:{season_id}',
            'include': ','.join(includes)
        }
        
        data = self.make_request('fixtures', params)
        
        if data and 'data' in data:
            fixtures = data['data']
            print(f"✅ Found {len(fixtures)} fixtures")
            
            # แสดงตัวอย่างแมทช์
            for i, fixture in enumerate(fixtures[:3]):
                participants = fixture.get('participants', [])
                home_team = next((p.get('name') for p in participants if p.get('meta', {}).get('location') == 'home'), 'Unknown')
                away_team = next((p.get('name') for p in participants if p.get('meta', {}).get('location') == 'away'), 'Unknown')
                
                scores = fixture.get('scores', [])
                home_score = next((s.get('score', {}).get('goals') for s in scores if s.get('participant_id') == next((p.get('id') for p in participants if p.get('meta', {}).get('location') == 'home'), None)), None)
                away_score = next((s.get('score', {}).get('goals') for s in scores if s.get('participant_id') == next((p.get('id') for p in participants if p.get('meta', {}).get('location') == 'away'), None)), None)
                
                print(f"   {i+1}. {home_team} vs {away_team}")
                if home_score is not None and away_score is not None:
                    print(f"      Score: {home_score}-{away_score}")
                print(f"      Date: {fixture.get('starting_at')}")
                print(f"      Status: {fixture.get('state', {}).get('short_name')}")
            
            return fixtures
        
        return []
    
    def get_teams_in_league(self, season_id):
        """ดึงทีมในลีก"""
        print(f"👥 Getting teams for season: {season_id}")
        
        params = {
            'filters': f'seasonId:{season_id}',
            'include': 'country,venue'
        }
        
        data = self.make_request('teams/seasons', params)
        
        if data and 'data' in data:
            teams = data['data']
            print(f"✅ Found {len(teams)} teams")
            
            for i, team in enumerate(teams[:10]):  # แสดง 10 ทีมแรก
                print(f"   {i+1}. {team.get('name')} (ID: {team.get('id')})")
            
            return teams
        
        return []

def main():
    print("🇦🇷 Sportmonks API Tester for Argentina Primera Division")
    print("=" * 70)
    
    api = SportmonksAPI()
    
    # ทดสอบ endpoints พื้นฐาน
    basic_results = api.test_basic_endpoints()
    
    # หาลีกอาร์เจนติน่า
    argentina_leagues = api.find_argentina_league()
    
    if argentina_leagues:
        # เลือกลีกแรก (น่าจะเป็น Primera Division)
        main_league = argentina_leagues[0]
        league_id = main_league.get('id')
        
        print(f"\n🎯 Testing main league: {main_league.get('name')} (ID: {league_id})")
        
        # ดึงรายละเอียดลีก
        current_season_id = api.get_league_details(league_id)
        
        if current_season_id:
            # ดึงแมทช์
            fixtures = api.get_season_fixtures(current_season_id)
            
            # ดึงทีม
            teams = api.get_teams_in_league(current_season_id)
            
            # สรุปข้อมูลที่ได้
            print(f"\n📊 DATA SUMMARY")
            print("=" * 50)
            print(f"✅ League: {main_league.get('name')}")
            print(f"✅ Season ID: {current_season_id}")
            print(f"✅ Fixtures: {len(fixtures)}")
            print(f"✅ Teams: {len(teams)}")
            
            # บันทึกข้อมูล
            argentina_data = {
                'league': main_league,
                'season_id': current_season_id,
                'fixtures': fixtures[:20],  # เก็บ 20 แมทช์แรก
                'teams': teams,
                'api_info': {
                    'source': 'Sportmonks API',
                    'retrieved_at': datetime.now().isoformat(),
                    'total_fixtures': len(fixtures)
                }
            }
            
            # บันทึกไฟล์
            try:
                with open('argentina_sportmonks_data.json', 'w', encoding='utf-8') as f:
                    json.dump(argentina_data, f, indent=2, ensure_ascii=False)
                print(f"✅ Data saved to argentina_sportmonks_data.json")
            except Exception as e:
                print(f"❌ Error saving data: {e}")
            
            print(f"\n🚀 SUCCESS: Real Argentina data retrieved!")
            print(f"   Ready to create predictor with real data")
            
        else:
            print("❌ Could not get current season")
    else:
        print("❌ No Argentina leagues found")

if __name__ == "__main__":
    main()
