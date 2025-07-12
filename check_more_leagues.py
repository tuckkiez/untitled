#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Check More Leagues and Matches Today
ตรวจสอบลีกและการแข่งขันเพิ่มเติม
"""

import requests
import json
from datetime import datetime, timedelta

def check_multiple_leagues():
    """ตรวจสอบหลายลีกจาก TheSportsDB"""
    print("🌍 Checking Multiple Leagues...")
    
    # League IDs from TheSportsDB
    leagues = {
        'J-League Division 1': '4346',
        'J-League Division 2': '4347', 
        'Premier League': '4328',
        'La Liga': '4335',
        'Serie A': '4332',
        'Bundesliga': '4331',
        'Ligue 1': '4334',
        'MLS': '4346',
        'A-League': '4356',
        'K-League': '4371',
        'Chinese Super League': '4370',
        'Argentine Primera': '4368',
        'Brazilian Serie A': '4351'
    }
    
    today = datetime.now().date()
    all_matches = []
    
    for league_name, league_id in leagues.items():
        try:
            print(f"   🔍 Checking {league_name}...")
            url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={league_id}"
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('events'):
                    today_matches = []
                    
                    for event in data['events'][:10]:  # Check first 10 upcoming
                        event_date = event.get('dateEvent')
                        if event_date:
                            try:
                                match_date = datetime.strptime(event_date, '%Y-%m-%d').date()
                                if match_date == today:
                                    today_matches.append({
                                        'league': league_name,
                                        'home': event.get('strHomeTeam', 'Unknown'),
                                        'away': event.get('strAwayTeam', 'Unknown'),
                                        'time': event.get('strTime', 'TBD'),
                                        'date': event_date
                                    })
                            except:
                                continue
                    
                    if today_matches:
                        print(f"      ✅ Found {len(today_matches)} matches today")
                        all_matches.extend(today_matches)
                        for match in today_matches:
                            print(f"         ⚽ {match['home']} vs {match['away']} ({match['time']})")
                    else:
                        print(f"      ❌ No matches today")
                else:
                    print(f"      ❌ No data")
            else:
                print(f"      ❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    return all_matches

def check_live_matches():
    """ตรวจสอบการแข่งขันที่กำลังเล่นอยู่"""
    print("\n🔴 Checking Live Matches...")
    
    try:
        # TheSportsDB live events
        url = "https://www.thesportsdb.com/api/v1/json/3/livescore.php?l=4346"  # Soccer
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('events'):
                print(f"   ✅ Found {len(data['events'])} live matches")
                for event in data['events'][:5]:
                    home = event.get('strHomeTeam', 'Unknown')
                    away = event.get('strAwayTeam', 'Unknown')
                    score_home = event.get('intHomeScore', '0')
                    score_away = event.get('intAwayScore', '0')
                    status = event.get('strStatus', 'Unknown')
                    print(f"      🔴 LIVE: {home} {score_home}-{score_away} {away} ({status})")
            else:
                print("   ❌ No live matches")
        else:
            print(f"   ❌ Live API Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Live matches error: {e}")

def suggest_betting_sites():
    """แนะนำเว็บดูราคาพนัน"""
    print("\n💰 Betting Odds Sources:")
    
    sites = [
        "🎯 Bet365: https://www.bet365.com/",
        "⚽ William Hill: https://www.williamhill.com/",
        "📊 Pinnacle: https://www.pinnacle.com/",
        "🏆 Betfair: https://www.betfair.com/",
        "💎 1xBet: https://1xbet.com/",
        "🎲 Unibet: https://www.unibet.com/",
        "⭐ 888sport: https://www.888sport.com/"
    ]
    
    for site in sites:
        print(f"   {site}")

def main():
    print("🔍 Comprehensive Match Finder")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # Check all leagues
    matches = check_multiple_leagues()
    
    # Check live matches
    check_live_matches()
    
    # Show summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    if matches:
        print(f"🔥 Total matches found today: {len(matches)}")
        print("\n📋 All Today's Matches:")
        
        for i, match in enumerate(matches, 1):
            print(f"{i:2d}. [{match['league']}] {match['home']} vs {match['away']} ({match['time']})")
        
        print(f"\n💡 Recommendation:")
        print(f"   Choose one of these {len(matches)} matches for analysis")
        print(f"   Get real odds from betting sites")
        print(f"   Update the analyzer with real data")
        
    else:
        print("❌ No matches found for today")
        print("💡 Suggestions:")
        print("   1. Check tomorrow's matches")
        print("   2. Look for live matches")
        print("   3. Use demo data for testing")
    
    # Show betting sites
    suggest_betting_sites()
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Pick a match from the list above")
    print(f"   2. Get odds from betting sites")
    print(f"   3. Update corrected_value_bet_analyzer.py")
    print(f"   4. Deploy to website")

if __name__ == "__main__":
    main()
