#!/usr/bin/env python3
"""
Comprehensive Argentina League Finder for Sportmonks API
ค้นหา Argentina Primera Division อย่างละเอียด
"""

import requests
import json
from datetime import datetime

def comprehensive_league_search():
    api_token = "1TQD9tFVUJ55dd31y6ECZ5FYeFKb8atMhavYD0tQfWgiRWISpTcDJgJ1Cclf"
    base_url = "https://api.sportmonks.com/v3/football"
    
    print("🔍 Comprehensive Argentina League Search")
    print("=" * 50)
    
    # ดึงลีกทั้งหมดแบบ pagination
    all_leagues = []
    page = 1
    max_pages = 10  # จำกัดไม่ให้ค้นหานานเกินไป
    
    while page <= max_pages:
        try:
            url = f"{base_url}/leagues"
            params = {
                'api_token': api_token,
                'page': page,
                'per_page': 100
            }
            
            print(f"📡 Fetching page {page}...")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and data['data']:
                    leagues = data['data']
                    all_leagues.extend(leagues)
                    print(f"   Found {len(leagues)} leagues on page {page}")
                    
                    # ตรวจสอบว่ามีหน้าถัดไปหรือไม่
                    meta = data.get('meta', {})
                    pagination = meta.get('pagination', {})
                    
                    if pagination.get('current_page', 0) >= pagination.get('last_page', 1):
                        print(f"   Reached last page")
                        break
                    
                    page += 1
                else:
                    print(f"   No more data")
                    break
            else:
                print(f"❌ Failed page {page}: {response.status_code}")
                break
                
        except Exception as e:
            print(f"❌ Error on page {page}: {e}")
            break
    
    print(f"\n✅ Total leagues collected: {len(all_leagues)}")
    
    # ค้นหา Argentina leagues
    argentina_keywords = [
        'argentina', 'argentine', 'primera division', 'superliga argentina',
        'liga profesional', 'primera a', 'arg', 'afa'
    ]
    
    argentina_leagues = []
    
    print(f"\n🇦🇷 Searching for Argentina leagues...")
    
    for league in all_leagues:
        league_name = league.get('name', '').lower()
        short_code = league.get('short_code', '').lower()
        country_id = league.get('country_id', 0)
        
        # ค้นหาตามชื่อ
        for keyword in argentina_keywords:
            if keyword in league_name or keyword in short_code:
                argentina_leagues.append(league)
                print(f"✅ Found by name: {league.get('name')} (ID: {league.get('id')})")
                print(f"   Short code: {league.get('short_code')}")
                print(f"   Country ID: {country_id}")
                break
        
        # ค้นหาตาม country_id ที่น่าจะเป็น Argentina
        # Argentina มักจะมี country_id เป็น 1159, 11, หรือ 32
        argentina_country_ids = [1159, 11, 32, 6, 1]
        if country_id in argentina_country_ids:
            if league not in argentina_leagues:  # ไม่ซ้ำ
                argentina_leagues.append(league)
                print(f"✅ Found by country ID: {league.get('name')} (ID: {league.get('id')})")
                print(f"   Country ID: {country_id}")
    
    return argentina_leagues

def test_league_details(league_id, api_token):
    """ทดสอบรายละเอียดลีก"""
    base_url = "https://api.sportmonks.com/v3/football"
    
    print(f"\n🔍 Testing league details for ID: {league_id}")
    
    try:
        # ดึงข้อมูลลีก
        league_url = f"{base_url}/leagues/{league_id}"
        league_params = {'api_token': api_token}
        
        league_response = requests.get(league_url, params=league_params, timeout=10)
        
        if league_response.status_code == 200:
            league_data = league_response.json()
            if 'data' in league_data:
                league = league_data['data']
                print(f"✅ League: {league.get('name')}")
                print(f"   Active: {league.get('active')}")
                print(f"   Type: {league.get('type')}")
                print(f"   Category: {league.get('category')}")
                
                # ดึงซีซั่น
                seasons_url = f"{base_url}/seasons"
                seasons_params = {
                    'api_token': api_token,
                    'filters': f'leagueId:{league_id}'
                }
                
                seasons_response = requests.get(seasons_url, params=seasons_params, timeout=10)
                
                if seasons_response.status_code == 200:
                    seasons_data = seasons_response.json()
                    if 'data' in seasons_data:
                        seasons = seasons_data['data']
                        print(f"   Seasons: {len(seasons)}")
                        
                        # หาซีซั่นปัจจุบัน
                        current_seasons = [s for s in seasons if s.get('is_current', False)]
                        recent_seasons = sorted(seasons, key=lambda x: x.get('starting_at', ''), reverse=True)[:3]
                        
                        if current_seasons:
                            print(f"   Current season: {current_seasons[0].get('name')}")
                            return current_seasons[0]
                        elif recent_seasons:
                            print(f"   Recent seasons: {[s.get('name') for s in recent_seasons]}")
                            return recent_seasons[0]
                
        else:
            print(f"❌ Failed: {league_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def get_sample_fixtures(season_id, api_token):
    """ดึงแมทช์ตัวอย่าง"""
    base_url = "https://api.sportmonks.com/v3/football"
    
    print(f"\n⚽ Getting sample fixtures for season: {season_id}")
    
    try:
        fixtures_url = f"{base_url}/fixtures"
        fixtures_params = {
            'api_token': api_token,
            'filters': f'seasonId:{season_id}',
            'per_page': 10
        }
        
        fixtures_response = requests.get(fixtures_url, params=fixtures_params, timeout=10)
        
        if fixtures_response.status_code == 200:
            fixtures_data = fixtures_response.json()
            if 'data' in fixtures_data:
                fixtures = fixtures_data['data']
                print(f"✅ Found {len(fixtures)} sample fixtures")
                
                for i, fixture in enumerate(fixtures[:5]):
                    print(f"   {i+1}. Fixture ID: {fixture.get('id')}")
                    print(f"      Name: {fixture.get('name', 'Unknown')}")
                    print(f"      Date: {fixture.get('starting_at')}")
                    print(f"      State: {fixture.get('state_id')}")
                
                return fixtures
        else:
            print(f"❌ Fixtures failed: {fixtures_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return []

def main():
    print("🇦🇷 Comprehensive Argentina League Finder")
    print("=" * 60)
    
    api_token = "1TQD9tFVUJ55dd31y6ECZ5FYeFKb8atMhavYD0tQfWgiRWISpTcDJgJ1Cclf"
    
    # ค้นหาลีกอาร์เจนติน่า
    argentina_leagues = comprehensive_league_search()
    
    if argentina_leagues:
        print(f"\n🎯 Found {len(argentina_leagues)} potential Argentina leagues:")
        
        for i, league in enumerate(argentina_leagues):
            print(f"{i+1}. {league.get('name')} (ID: {league.get('id')})")
            print(f"   Short code: {league.get('short_code')}")
            print(f"   Country ID: {league.get('country_id')}")
            print(f"   Active: {league.get('active')}")
        
        # ทดสอบลีกแรก
        main_league = argentina_leagues[0]
        league_id = main_league.get('id')
        
        print(f"\n🔍 Testing main league: {main_league.get('name')}")
        
        season = test_league_details(league_id, api_token)
        
        if season:
            season_id = season.get('id')
            fixtures = get_sample_fixtures(season_id, api_token)
            
            if fixtures:
                print(f"\n🚀 SUCCESS!")
                print(f"   League: {main_league.get('name')} (ID: {league_id})")
                print(f"   Season: {season.get('name')} (ID: {season_id})")
                print(f"   Sample fixtures: {len(fixtures)}")
                
                # บันทึกข้อมูล
                result_data = {
                    'league': main_league,
                    'season': season,
                    'sample_fixtures': fixtures,
                    'all_argentina_leagues': argentina_leagues,
                    'api_info': {
                        'source': 'Sportmonks API',
                        'retrieved_at': datetime.now().isoformat()
                    }
                }
                
                try:
                    with open('argentina_sportmonks_found.json', 'w', encoding='utf-8') as f:
                        json.dump(result_data, f, indent=2, ensure_ascii=False)
                    print(f"✅ Data saved to argentina_sportmonks_found.json")
                except Exception as e:
                    print(f"❌ Error saving: {e}")
            else:
                print(f"\n⚠️ League found but no fixtures available")
        else:
            print(f"\n⚠️ League found but no season details")
    else:
        print(f"\n❌ No Argentina leagues found")
        print(f"💡 The API might not have Argentina Primera Division")
        print(f"💡 Or it might be under a different name/country")

if __name__ == "__main__":
    main()
