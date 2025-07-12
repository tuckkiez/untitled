#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Find Today's Matches from Multiple APIs
หาการแข่งขันวันนี้จาก API ต่างๆ
"""

import requests
import json
from datetime import datetime, timedelta
import time

def print_header():
    print("🔍 Finding Today's Football Matches")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 50)

def check_football_data_org():
    """ตรวจสอบ football-data.org API"""
    print("\n🏈 Checking Football-Data.org...")
    
    try:
        # Free tier - limited competitions
        url = "https://api.football-data.org/v4/matches"
        headers = {
            'X-Auth-Token': 'YOUR_API_KEY_HERE'  # ต้องสมัคร free API key
        }
        
        params = {
            'dateFrom': datetime.now().strftime('%Y-%m-%d'),
            'dateTo': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Note: ต้องมี API key จริงถึงจะใช้ได้
        print("   ⚠️  Need API key from football-data.org")
        print("   📝 Sign up at: https://www.football-data.org/client/register")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

def check_free_apis():
    """ตรวจสอบ Free APIs ที่ไม่ต้อง key"""
    print("\n🆓 Checking Free APIs...")
    
    # API 1: TheSportsDB (Free)
    try:
        print("   🔍 TheSportsDB...")
        today = datetime.now().strftime('%Y-%m-%d')
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Soccer"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('events'):
                print(f"   ✅ Found {len(data['events'])} matches")
                for event in data['events'][:5]:  # Show first 5
                    home = event.get('strHomeTeam', 'Unknown')
                    away = event.get('strAwayTeam', 'Unknown')
                    time_str = event.get('strTime', 'TBD')
                    league = event.get('strLeague', 'Unknown League')
                    print(f"      🏆 {league}: {home} vs {away} ({time_str})")
            else:
                print("   ❌ No matches found")
        else:
            print(f"   ❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ TheSportsDB Error: {e}")
    
    time.sleep(1)  # Rate limiting
    
    # API 2: API-Football (Free tier)
    try:
        print("   🔍 API-Football (RapidAPI)...")
        print("   ⚠️  Need RapidAPI key for API-Football")
        print("   📝 Sign up at: https://rapidapi.com/api-sports/api/api-football")
        
    except Exception as e:
        print(f"   ❌ API-Football Error: {e}")

def check_j_league_specific():
    """ตรวจสอบ J-League โดยเฉพาะ"""
    print("\n🇯🇵 Checking J-League Specific Sources...")
    
    try:
        # J-League official might have some data
        print("   🔍 Looking for J-League data...")
        
        # ลอง TheSportsDB สำหรับ J-League
        url = "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4346"  # J-League ID
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('events'):
                print(f"   ✅ Found {len(data['events'])} upcoming J-League matches")
                
                today = datetime.now().date()
                today_matches = []
                
                for event in data['events']:
                    event_date = event.get('dateEvent')
                    if event_date:
                        try:
                            match_date = datetime.strptime(event_date, '%Y-%m-%d').date()
                            if match_date == today:
                                today_matches.append(event)
                        except:
                            continue
                
                if today_matches:
                    print(f"   🔥 J-League matches TODAY: {len(today_matches)}")
                    for match in today_matches:
                        home = match.get('strHomeTeam', 'Unknown')
                        away = match.get('strAwayTeam', 'Unknown')
                        time_str = match.get('strTime', 'TBD')
                        print(f"      ⚽ {home} vs {away} ({time_str})")
                else:
                    print("   ❌ No J-League matches today")
            else:
                print("   ❌ No J-League data found")
        else:
            print(f"   ❌ J-League API Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ J-League Error: {e}")

def check_alternative_sources():
    """ตรวจสอบแหล่งข้อมูลอื่นๆ"""
    print("\n🌐 Alternative Data Sources...")
    
    sources = [
        {
            'name': 'ESPN API',
            'url': 'http://site.api.espn.com/apis/site/v2/sports/soccer/matches',
            'note': 'Free but limited'
        },
        {
            'name': 'OpenLigaDB',
            'url': 'https://api.openligadb.de/',
            'note': 'German leagues mainly'
        },
        {
            'name': 'Football API',
            'url': 'https://apiv3.apifootball.com/',
            'note': 'Need API key'
        }
    ]
    
    for source in sources:
        print(f"   📡 {source['name']}: {source['note']}")
        print(f"      🔗 {source['url']}")

def show_manual_sources():
    """แสดงแหล่งข้อมูลที่ต้องตรวจสอบด้วยตนเอง"""
    print("\n📋 Manual Check Sources:")
    
    sources = [
        "🇯🇵 J-League Official: https://www.jleague.jp/",
        "⚽ FlashScore: https://www.flashscore.com/",
        "📊 SofaScore: https://www.sofascore.com/",
        "🏆 ESPN: https://www.espn.com/soccer/",
        "📈 FotMob: https://www.fotmob.com/",
        "🎯 LiveScore: https://www.livescore.com/",
    ]
    
    for source in sources:
        print(f"   {source}")

def main():
    print_header()
    
    # Check various APIs
    check_free_apis()
    check_j_league_specific()
    check_football_data_org()
    check_alternative_sources()
    show_manual_sources()
    
    print("\n" + "=" * 50)
    print("💡 Recommendations:")
    print("1. Sign up for free API keys (football-data.org, RapidAPI)")
    print("2. Check manual sources for today's matches")
    print("3. Focus on leagues with confirmed matches")
    print("4. Update our system with real match data")
    
    print("\n🚀 Next Steps:")
    print("- Find a match with real odds")
    print("- Update corrected_value_bet_analyzer.py")
    print("- Deploy updated analysis to website")

if __name__ == "__main__":
    main()
