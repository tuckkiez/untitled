#!/usr/bin/env python3
"""
Test Free APIs for Argentina Primera Division Data
ทดสอบ Free APIs สำหรับข้อมูลฟุตบอลอาร์เจนติน่า
"""

import requests
import json
from datetime import datetime, timedelta

def test_thesportsdb():
    """ทดสอบ TheSportsDB API"""
    print("🔍 Testing TheSportsDB for Argentina data...")
    
    try:
        # ค้นหาลีกอาร์เจนติน่า
        url = "https://www.thesportsdb.com/api/v1/json/3/search_all_leagues.php"
        params = {'c': 'Argentina'}
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            leagues = data.get('countries', []) or []
            
            print(f"✅ Found {len(leagues)} Argentina leagues:")
            for league in leagues:
                if league:
                    print(f"   - {league.get('strLeague', 'Unknown')}")
            
            # ลองหาข้อมูลแมทช์
            if leagues:
                league_name = leagues[0].get('strLeague', '')
                print(f"\n🏆 Looking for matches in {league_name}...")
                
                # ค้นหาแมทช์ล่าสุด
                match_url = "https://www.thesportsdb.com/api/v1/json/3/eventslast.php"
                match_params = {'id': leagues[0].get('idLeague', '')}
                
                match_response = requests.get(match_url, params=match_params)
                if match_response.status_code == 200:
                    match_data = match_response.json()
                    events = match_data.get('results', []) or []
                    
                    print(f"✅ Found {len(events)} recent matches")
                    for i, event in enumerate(events[:3]):  # แสดง 3 แมทช์แรก
                        if event:
                            print(f"   {i+1}. {event.get('strHomeTeam')} vs {event.get('strAwayTeam')}")
                            print(f"      Score: {event.get('intHomeScore', '?')}-{event.get('intAwayScore', '?')}")
                            print(f"      Date: {event.get('dateEvent')}")
            
            return leagues
        else:
            print(f"❌ Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def test_football_api_free():
    """ทดสอบ Football API ฟรี"""
    print("\n🔍 Testing Football API (Free)...")
    
    # ลอง API ฟรีที่ไม่ต้อง key
    free_apis = [
        "https://api.football-data-api.com/league-list",
        "https://free-football-soccer-videos.p.rapidapi.com/",
        "http://api.cup2018.ir/api/v1/match"
    ]
    
    for api_url in free_apis:
        try:
            print(f"📡 Testing: {api_url}")
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Success: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   Data type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"   Keys: {list(data.keys())[:5]}")
                    elif isinstance(data, list):
                        print(f"   Items: {len(data)}")
                except:
                    print(f"   Content length: {len(response.text)}")
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def check_live_score_apis():
    """ตรวจสอบ Live Score APIs"""
    print("\n🔍 Testing Live Score APIs...")
    
    live_apis = [
        {
            'name': 'LiveScore API',
            'url': 'https://livescore-api.com/api-client/scores/live.json',
            'method': 'GET'
        },
        {
            'name': 'Football Data',
            'url': 'https://api.openligadb.de/getmatchdata/bl1/2024',
            'method': 'GET'
        }
    ]
    
    for api in live_apis:
        try:
            print(f"📡 Testing {api['name']}...")
            response = requests.get(api['url'], timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {api['name']}: Success")
                try:
                    data = response.json()
                    print(f"   Data received: {len(str(data))} chars")
                except:
                    print(f"   Text data: {len(response.text)} chars")
            else:
                print(f"❌ {api['name']}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {api['name']}: {e}")

def search_argentina_specific():
    """ค้นหาข้อมูลอาร์เจนติน่าเฉพาะ"""
    print("\n🇦🇷 Searching Argentina-specific data...")
    
    try:
        # ลองค้นหาทีมอาร์เจนติน่า
        teams_url = "https://www.thesportsdb.com/api/v1/json/3/search_all_teams.php"
        params = {'l': 'Argentine Primera División'}
        
        response = requests.get(teams_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            teams = data.get('teams', []) or []
            
            print(f"✅ Found {len(teams)} teams in Argentine Primera División:")
            for i, team in enumerate(teams[:10]):  # แสดง 10 ทีมแรก
                if team:
                    print(f"   {i+1}. {team.get('strTeam', 'Unknown')}")
                    print(f"      Stadium: {team.get('strStadium', 'Unknown')}")
            
            # ถ้าหาทีมเจอ ลองหาแมทช์ของทีมแรก
            if teams:
                team_id = teams[0].get('idTeam')
                print(f"\n🏆 Looking for matches of {teams[0].get('strTeam')}...")
                
                match_url = "https://www.thesportsdb.com/api/v1/json/3/eventslast.php"
                match_params = {'id': team_id}
                
                match_response = requests.get(match_url, params=match_params)
                if match_response.status_code == 200:
                    match_data = match_response.json()
                    events = match_data.get('results', []) or []
                    
                    print(f"✅ Found {len(events)} recent matches:")
                    for i, event in enumerate(events[:5]):
                        if event:
                            print(f"   {i+1}. {event.get('strHomeTeam')} vs {event.get('strAwayTeam')}")
                            print(f"      Score: {event.get('intHomeScore', '?')}-{event.get('intAwayScore', '?')}")
                            print(f"      Date: {event.get('dateEvent')}")
                            
                            # ตรวจสอบข้อมูลเพิ่มเติม
                            if event.get('intHomeScore') and event.get('intAwayScore'):
                                total_goals = int(event.get('intHomeScore', 0)) + int(event.get('intAwayScore', 0))
                                print(f"      Total Goals: {total_goals}")
            
            return teams
        else:
            print(f"❌ Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    print("🇦🇷 Free Argentina Football API Tester")
    print("=" * 50)
    
    # ทดสอบ APIs ต่างๆ
    thesportsdb_leagues = test_thesportsdb()
    test_football_api_free()
    check_live_score_apis()
    argentina_teams = search_argentina_specific()
    
    print("\n📋 Summary:")
    print(f"- TheSportsDB leagues: {len(thesportsdb_leagues)}")
    print(f"- Argentina teams found: {len(argentina_teams) if argentina_teams else 0}")
    
    if argentina_teams:
        print("\n✅ SUCCESS: Found Argentina Primera División data!")
        print("📊 Available data:")
        print("   - Team information")
        print("   - Recent match results")
        print("   - Scores and dates")
        print("\n🚀 Next step: Create Argentina predictor with real data")
    else:
        print("\n❌ No comprehensive Argentina data found in free APIs")
        print("💡 Recommendation: Need paid API for complete data")

if __name__ == "__main__":
    main()
