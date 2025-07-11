#!/usr/bin/env python3
"""
Simple Sportmonks API Test - No Complex Includes
ทดสอบ Sportmonks API แบบง่ายๆ เพื่อหาข้อมูล Argentina
"""

import requests
import json
from datetime import datetime

def test_sportmonks_simple():
    api_token = "1TQD9tFVUJ55dd31y6ECZ5FYeFKb8atMhavYD0tQfWgiRWISpTcDJgJ1Cclf"
    base_url = "https://api.sportmonks.com/v3/football"
    
    print("🔍 Simple Sportmonks API Test")
    print("=" * 40)
    
    # ทดสอบ endpoints พื้นฐาน
    endpoints = [
        'leagues',
        'seasons', 
        'teams',
        'fixtures'
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}/{endpoint}"
            params = {'api_token': api_token}
            
            print(f"\n📡 Testing: {endpoint}")
            response = requests.get(url, params=params, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data:
                    items = data['data']
                    print(f"✅ Success: {len(items)} items")
                    
                    # แสดงตัวอย่างข้อมูล
                    if items:
                        first_item = items[0]
                        print(f"   Keys: {list(first_item.keys())}")
                        print(f"   Sample: {first_item}")
                        
                        # หา Argentina ในข้อมูล
                        argentina_items = []
                        for item in items:
                            item_str = str(item).lower()
                            if 'argentina' in item_str or 'primera' in item_str:
                                argentina_items.append(item)
                        
                        if argentina_items:
                            print(f"🇦🇷 Found {len(argentina_items)} Argentina-related items:")
                            for arg_item in argentina_items[:3]:
                                print(f"      {arg_item}")
                else:
                    print(f"✅ Response: {list(data.keys())}")
            else:
                print(f"❌ Failed: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # ลองดึงข้อมูลเฉพาะ
    print(f"\n🎯 Trying specific league ID...")
    
    # ลองใช้ ID ที่รู้จัก (Argentina Primera Division มักจะเป็น ID 501, 271, หรือ 384)
    argentina_league_ids = [501, 271, 384, 128, 2]
    
    for league_id in argentina_league_ids:
        try:
            url = f"{base_url}/leagues/{league_id}"
            params = {'api_token': api_token}
            
            print(f"\n📡 Testing League ID: {league_id}")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    league = data['data']
                    league_name = league.get('name', 'Unknown')
                    print(f"✅ Found: {league_name}")
                    
                    if 'argentina' in league_name.lower() or 'primera' in league_name.lower():
                        print(f"🇦🇷 BINGO! Argentina League Found!")
                        print(f"   ID: {league_id}")
                        print(f"   Name: {league_name}")
                        print(f"   Full data: {league}")
                        
                        # ลองดึงซีซั่น
                        seasons_url = f"{base_url}/seasons"
                        seasons_params = {
                            'api_token': api_token,
                            'filters': f'leagueId:{league_id}'
                        }
                        
                        print(f"\n🏆 Getting seasons for league {league_id}...")
                        seasons_response = requests.get(seasons_url, params=seasons_params, timeout=10)
                        
                        if seasons_response.status_code == 200:
                            seasons_data = seasons_response.json()
                            if 'data' in seasons_data:
                                seasons = seasons_data['data']
                                print(f"✅ Found {len(seasons)} seasons")
                                
                                for season in seasons[-3:]:  # แสดง 3 ซีซั่นล่าสุด
                                    print(f"   Season: {season.get('name')} (ID: {season.get('id')})")
                        
                        return league_id, league
            else:
                print(f"   Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing league {league_id}: {e}")
    
    return None, None

def test_fixtures_for_league(league_id, api_token):
    """ทดสอบดึงแมทช์สำหรับลีก"""
    base_url = "https://api.sportmonks.com/v3/football"
    
    print(f"\n⚽ Getting fixtures for league {league_id}...")
    
    # ดึงซีซั่นล่าสุดก่อน
    seasons_url = f"{base_url}/seasons"
    seasons_params = {
        'api_token': api_token,
        'filters': f'leagueId:{league_id}'
    }
    
    try:
        seasons_response = requests.get(seasons_url, params=seasons_params, timeout=10)
        
        if seasons_response.status_code == 200:
            seasons_data = seasons_response.json()
            if 'data' in seasons_data and seasons_data['data']:
                latest_season = seasons_data['data'][-1]  # ซีซั่นล่าสุด
                season_id = latest_season.get('id')
                season_name = latest_season.get('name')
                
                print(f"✅ Using season: {season_name} (ID: {season_id})")
                
                # ดึงแมทช์
                fixtures_url = f"{base_url}/fixtures"
                fixtures_params = {
                    'api_token': api_token,
                    'filters': f'seasonId:{season_id}'
                }
                
                fixtures_response = requests.get(fixtures_url, params=fixtures_params, timeout=10)
                
                if fixtures_response.status_code == 200:
                    fixtures_data = fixtures_response.json()
                    if 'data' in fixtures_data:
                        fixtures = fixtures_data['data']
                        print(f"✅ Found {len(fixtures)} fixtures")
                        
                        # แสดงตัวอย่าง
                        for i, fixture in enumerate(fixtures[:5]):
                            print(f"   {i+1}. Fixture ID: {fixture.get('id')}")
                            print(f"      Date: {fixture.get('starting_at')}")
                            print(f"      State: {fixture.get('state', {})}")
                        
                        return fixtures
                else:
                    print(f"❌ Fixtures failed: {fixtures_response.status_code}")
        else:
            print(f"❌ Seasons failed: {seasons_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return []

def main():
    print("🇦🇷 Simple Sportmonks API Test for Argentina")
    print("=" * 50)
    
    # ทดสอบพื้นฐาน
    league_id, league_data = test_sportmonks_simple()
    
    if league_id:
        api_token = "1TQD9tFVUJ55dd31y6ECZ5FYeFKb8atMhavYD0tQfWgiRWISpTcDJgJ1Cclf"
        
        # ทดสอบดึงแมทช์
        fixtures = test_fixtures_for_league(league_id, api_token)
        
        if fixtures:
            print(f"\n🚀 SUCCESS!")
            print(f"   League ID: {league_id}")
            print(f"   League Name: {league_data.get('name')}")
            print(f"   Fixtures: {len(fixtures)}")
            print(f"   Ready to create real predictor!")
        else:
            print(f"\n⚠️ League found but no fixtures")
    else:
        print(f"\n❌ No Argentina league found")
        print(f"💡 Try checking Sportmonks documentation for correct league IDs")

if __name__ == "__main__":
    main()
