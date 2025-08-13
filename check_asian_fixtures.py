#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Check Asian Fixtures
ตรวจสอบข้อมูลการแข่งขันของลีกเอเชีย
"""

import json
from datetime import datetime
import pytz

def load_fixtures_data():
    """Load fixtures data from JSON file"""
    try:
        with open('today_fixtures.json', 'r') as f:
            return json.load(f)
    except:
        print("Error: Could not load fixtures data")
        return None

def find_asian_leagues(fixtures_data):
    """Find Asian leagues in fixtures data"""
    if not fixtures_data or "response" not in fixtures_data:
        print("No fixtures data available")
        return {}
    
    asian_leagues = {
        "China - Super League": [],
        "Japan - J1 League": [],
        "South-Korea - K League 1": [],
        "South-Korea - K League 2": []
    }
    
    for fixture in fixtures_data["response"]:
        league_country = fixture["league"]["country"]
        league_name = fixture["league"]["name"]
        
        league_key = None
        if league_country == "China" and league_name == "Super League":
            league_key = "China - Super League"
        elif league_country == "Japan" and league_name == "J1 League":
            league_key = "Japan - J1 League"
        elif league_country == "South-Korea" and league_name == "K League 1":
            league_key = "South-Korea - K League 1"
        elif league_country == "South-Korea" and league_name == "K League 2":
            league_key = "South-Korea - K League 2"
        
        if league_key:
            home_team = fixture["teams"]["home"]["name"]
            away_team = fixture["teams"]["away"]["name"]
            
            # Convert time to Bangkok time
            fixture_time = fixture["fixture"]["date"]
            fixture_datetime = datetime.fromisoformat(fixture_time.replace("Z", "+00:00"))
            bangkok_tz = pytz.timezone("Asia/Bangkok")
            fixture_datetime_bangkok = fixture_datetime.astimezone(bangkok_tz)
            fixture_time_bangkok = fixture_datetime_bangkok.strftime("%H:%M")
            
            asian_leagues[league_key].append({
                "home_team": home_team,
                "away_team": away_team,
                "time": fixture_time_bangkok,
                "date": fixture_time
            })
    
    return asian_leagues

def main():
    # Load fixtures data
    fixtures_data = load_fixtures_data()
    
    if not fixtures_data:
        print("Failed to load fixtures data")
        return
    
    # Find Asian leagues
    asian_leagues = find_asian_leagues(fixtures_data)
    
    # Print results
    print("\nAsian leagues fixtures for today:")
    print("=" * 80)
    
    total_fixtures = 0
    for league_name, fixtures in asian_leagues.items():
        print(f"\n{league_name}: {len(fixtures)} matches")
        total_fixtures += len(fixtures)
        
        for fixture in fixtures:
            print(f"  {fixture['time']} - {fixture['home_team']} vs {fixture['away_team']}")
    
    print("\n" + "=" * 80)
    print(f"Total: {total_fixtures} matches in Asian leagues")

if __name__ == "__main__":
    main()
