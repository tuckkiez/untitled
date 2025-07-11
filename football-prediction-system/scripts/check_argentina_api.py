#!/usr/bin/env python3
"""
Argentina Primera Division API Data Checker
ตรวจสอบ API ที่มีข้อมูล Argentina Primera Division ครบถ้วน
"""

import requests
import json
from datetime import datetime, timedelta

def check_football_data_org():
    """ตรวจสอบ football-data.org API"""
    print("🔍 Checking football-data.org...")
    
    # Free tier API key (limited)
    headers = {
        'X-Auth-Token': 'YOUR_API_KEY_HERE'  # ต้องสมัคร
    }
    
    try:
        # ดู competitions ที่มี
        url = "https://api.football-data.org/v4/competitions"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            competitions = response.json()
            argentina_leagues = [comp for comp in competitions['competitions'] 
                               if 'argentina' in comp['name'].lower() or 'primera' in comp['name'].lower()]
            
            print(f"✅ Found {len(argentina_leagues)} Argentina leagues:")
            for league in argentina_leagues:
                print(f"   - {league['name']} (ID: {league['id']})")
            
            return argentina_leagues
        else:
            print(f"❌ Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def check_api_sports():
    """ตรวจสอบ API-Sports (RapidAPI)"""
    print("\n🔍 Checking API-Sports...")
    
    headers = {
        'X-RapidAPI-Key': 'YOUR_RAPIDAPI_KEY_HERE',  # ต้องสมัคร
        'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
    }
    
    try:
        # ดู leagues ที่มี
        url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
        params = {
            'country': 'Argentina',
            'season': '2024'
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            leagues = data.get('response', [])
            
            print(f"✅ Found {len(leagues)} Argentina leagues:")
            for league_data in leagues:
                league = league_data['league']
                print(f"   - {league['name']} (ID: {league['id']})")
                
            return leagues
        else:
            print(f"❌ Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def check_free_apis():
    """ตรวจสอบ Free APIs"""
    print("\n🔍 Checking Free APIs...")
    
    apis_to_check = [
        {
            'name': 'TheSportsDB',
            'url': 'https://www.thesportsdb.com/api/v1/json/3/search_all_leagues.php?c=Argentina',
            'method': 'GET'
        },
        {
            'name': 'Football API',
            'url': 'https://apiv3.apifootball.com/?action=get_leagues&country_id=6&APIkey=YOUR_KEY',
            'method': 'GET'
        }
    ]
    
    for api in apis_to_check:
        try:
            print(f"\n📡 Testing {api['name']}...")
            response = requests.get(api['url'], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {api['name']}: Response received")
                print(f"   Data keys: {list(data.keys()) if isinstance(data, dict) else 'List data'}")
            else:
                print(f"❌ {api['name']}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {api['name']}: Error - {e}")

def check_argentina_matches_today():
    """ตรวจสอบแมทช์วันนี้ของอาร์เจนติน่า"""
    print("\n🏆 Checking Argentina matches today...")
    
    # ใช้ free API ที่ไม่ต้อง key
    try:
        # TheSportsDB - ฟรี
        url = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php"
        params = {
            'd': datetime.now().strftime('%Y-%m-%d'),
            's': 'Soccer'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', []) or []
            
            argentina_matches = [event for event in events 
                               if event and 'argentina' in event.get('strLeague', '').lower()]
            
            print(f"✅ Found {len(argentina_matches)} Argentina matches today:")
            for match in argentina_matches:
                print(f"   - {match.get('strHomeTeam')} vs {match.get('strAwayTeam')}")
                print(f"     League: {match.get('strLeague')}")
                print(f"     Time: {match.get('strTime')}")
                
            return argentina_matches
        else:
            print(f"❌ Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    print("🇦🇷 Argentina Primera Division API Checker")
    print("=" * 50)
    
    # ตรวจสอบ APIs ต่างๆ
    football_data_leagues = check_football_data_org()
    api_sports_leagues = check_api_sports()
    check_free_apis()
    argentina_matches = check_argentina_matches_today()
    
    print("\n📋 Summary:")
    print(f"- Football-data.org: {len(football_data_leagues)} leagues found")
    print(f"- API-Sports: Found leagues (need API key)")
    print(f"- Today's matches: {len(argentina_matches)} matches")
    
    print("\n💡 Recommendations:")
    print("1. football-data.org - Best for comprehensive data (need API key)")
    print("2. API-Sports - Most complete data (need RapidAPI key)")
    print("3. TheSportsDB - Free but limited data")
    
    print("\n🔑 Next Steps:")
    print("1. Get API keys for football-data.org or API-Sports")
    print("2. Test with real Argentina Primera Division data")
    print("3. Implement 20-match backtest with real data")

if __name__ == "__main__":
    main()
