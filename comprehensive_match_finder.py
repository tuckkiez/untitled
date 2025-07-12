#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Comprehensive Match Finder
หาการแข่งขันจากทุกแหล่งที่เป็นไปได้
"""

import requests
import json
from datetime import datetime, timedelta
import time

def print_header():
    print("🔍 COMPREHENSIVE FOOTBALL MATCH FINDER")
    print("=" * 60)
    print(f"📅 Today: {datetime.now().strftime('%A, %B %d, %Y')}")
    print(f"🕐 Time: {datetime.now().strftime('%H:%M %Z')}")
    print("=" * 60)

def check_espn_api():
    """ตรวจสอบ ESPN API"""
    print("\n🏈 ESPN API...")
    
    try:
        # ESPN Soccer API
        url = "http://site.api.espn.com/apis/site/v2/sports/soccer/matches"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'events' in data:
                today_matches = []
                today = datetime.now().date()
                
                for event in data['events']:
                    event_date = event.get('date')
                    if event_date:
                        try:
                            match_date = datetime.fromisoformat(event_date.replace('Z', '+00:00')).date()
                            if match_date == today:
                                competition = event.get('competitions', [{}])[0]
                                competitors = competition.get('competitors', [])
                                
                                if len(competitors) >= 2:
                                    home_team = competitors[0].get('team', {}).get('displayName', 'Unknown')
                                    away_team = competitors[1].get('team', {}).get('displayName', 'Unknown')
                                    league = event.get('league', {}).get('name', 'Unknown League')
                                    
                                    today_matches.append({
                                        'home': home_team,
                                        'away': away_team,
                                        'league': league,
                                        'time': event_date
                                    })
                        except:
                            continue
                
                if today_matches:
                    print(f"   ✅ Found {len(today_matches)} matches")
                    for match in today_matches[:5]:
                        print(f"      ⚽ [{match['league']}] {match['home']} vs {match['away']}")
                    return today_matches
                else:
                    print("   ❌ No matches today")
            else:
                print("   ❌ No events data")
        else:
            print(f"   ❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ ESPN Error: {e}")
    
    return []

def check_tomorrow_matches():
    """ตรวจสอบการแข่งขันพรุ่งนี้"""
    print("\n📅 Tomorrow's Matches...")
    
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={tomorrow}&s=Soccer"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('events'):
                print(f"   ✅ Found {len(data['events'])} matches tomorrow")
                for event in data['events'][:5]:
                    home = event.get('strHomeTeam', 'Unknown')
                    away = event.get('strAwayTeam', 'Unknown')
                    league = event.get('strLeague', 'Unknown League')
                    time_str = event.get('strTime', 'TBD')
                    print(f"      ⚽ [{league}] {home} vs {away} ({time_str})")
                return data['events']
            else:
                print("   ❌ No matches tomorrow")
        else:
            print(f"   ❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Tomorrow matches error: {e}")
    
    return []

def check_this_weekend():
    """ตรวจสอบการแข่งขันสุดสัปดาห์นี้"""
    print("\n🏁 This Weekend's Matches...")
    
    weekend_matches = []
    
    # Check Saturday and Sunday
    for days_ahead in [1, 2, 3]:  # Tomorrow, day after, etc.
        try:
            check_date = (datetime.now() + timedelta(days=days_ahead))
            date_str = check_date.strftime('%Y-%m-%d')
            day_name = check_date.strftime('%A')
            
            url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={date_str}&s=Soccer"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('events'):
                    print(f"   📅 {day_name} ({date_str}): {len(data['events'])} matches")
                    weekend_matches.extend(data['events'][:3])  # Take first 3
                    
                    for event in data['events'][:3]:
                        home = event.get('strHomeTeam', 'Unknown')
                        away = event.get('strAwayTeam', 'Unknown')
                        league = event.get('strLeague', 'Unknown League')
                        time_str = event.get('strTime', 'TBD')
                        print(f"      ⚽ [{league}] {home} vs {away} ({time_str})")
                else:
                    print(f"   📅 {day_name}: No matches")
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"   ❌ {day_name} error: {e}")
    
    return weekend_matches

def suggest_manual_check():
    """แนะนำการตรวจสอบด้วยตนเอง"""
    print("\n🔍 MANUAL CHECK REQUIRED")
    print("=" * 40)
    
    print("📱 Mobile Apps:")
    apps = [
        "FotMob - Football Live Scores",
        "ESPN - Sports News & Scores", 
        "FlashScore - Live Sports Results",
        "SofaScore - Live Sports Results",
        "LiveScore - Live Sport Updates"
    ]
    
    for app in apps:
        print(f"   📲 {app}")
    
    print("\n🌐 Websites to Check:")
    websites = [
        ("🇯🇵 J-League Official", "https://www.jleague.jp/en/"),
        ("⚽ FIFA.com", "https://www.fifa.com/"),
        ("🏆 UEFA.com", "https://www.uefa.com/"),
        ("📊 ESPN Soccer", "https://www.espn.com/soccer/"),
        ("🎯 BBC Sport", "https://www.bbc.com/sport/football"),
        ("📈 Sky Sports", "https://www.skysports.com/football"),
    ]
    
    for name, url in websites:
        print(f"   {name}: {url}")

def create_demo_match():
    """สร้างการแข่งขันจำลองสำหรับทดสอบ"""
    print("\n🎭 DEMO MATCH FOR TESTING")
    print("=" * 40)
    
    demo_matches = [
        {
            'home': 'FC Tokyo',
            'away': 'Yokohama F. Marinos', 
            'league': 'J-League Division 1',
            'time': '19:00 JST',
            'note': 'Popular J-League rivalry'
        },
        {
            'home': 'Kashima Antlers',
            'away': 'Urawa Red Diamonds',
            'league': 'J-League Division 1', 
            'time': '18:30 JST',
            'note': 'Classic matchup'
        },
        {
            'home': 'Ventforet Kofu',
            'away': 'Montedio Yamagata',
            'league': 'J-League Division 2',
            'time': '19:00 JST', 
            'note': 'J2 League match'
        }
    ]
    
    print("💡 Use these demo matches for testing:")
    for i, match in enumerate(demo_matches, 1):
        print(f"   {i}. [{match['league']}] {match['home']} vs {match['away']}")
        print(f"      ⏰ {match['time']} - {match['note']}")

def main():
    print_header()
    
    all_matches = []
    
    # Check various sources
    espn_matches = check_espn_api()
    all_matches.extend(espn_matches)
    
    tomorrow_matches = check_tomorrow_matches()
    weekend_matches = check_this_weekend()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    
    if all_matches:
        print(f"🔥 Found {len(all_matches)} matches today!")
        print("\n📋 TODAY'S MATCHES:")
        for i, match in enumerate(all_matches, 1):
            print(f"   {i}. [{match.get('league', 'Unknown')}] {match['home']} vs {match['away']}")
        
        print(f"\n💡 RECOMMENDATION:")
        print(f"   ✅ Use match #{1} for analysis")
        print(f"   📊 Get real odds from betting sites")
        print(f"   🚀 Update analyzer and deploy")
        
    else:
        print("❌ NO MATCHES FOUND TODAY")
        
        if tomorrow_matches:
            print(f"📅 But found {len(tomorrow_matches)} matches tomorrow")
        
        if weekend_matches:
            print(f"🏁 And {len(weekend_matches)} matches this weekend")
        
        print("\n💡 OPTIONS:")
        print("   1. Wait for tomorrow's matches")
        print("   2. Use demo data for testing")
        print("   3. Check manual sources")
        print("   4. Focus on weekend matches")
    
    # Show manual check options
    suggest_manual_check()
    
    # Show demo options
    create_demo_match()
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"   1. Choose a match (real or demo)")
    print(f"   2. Get odds from betting sites")
    print(f"   3. Run: python corrected_value_bet_analyzer.py")
    print(f"   4. Deploy: ./quick_deploy.sh 'New match analysis'")

if __name__ == "__main__":
    main()
