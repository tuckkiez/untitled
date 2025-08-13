#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Check Leagues in today_fixtures.json
ตรวจสอบข้อมูลลีกที่ต้องการในไฟล์ today_fixtures.json
"""

import json

def load_fixtures():
    """Load fixtures from today_fixtures.json"""
    try:
        with open('today_fixtures.json', 'r') as f:
            return json.load(f)
    except:
        print("Error: Could not load today_fixtures.json")
        return None

def check_leagues(fixtures_data):
    """Check for specific leagues in fixtures data"""
    if not fixtures_data or "response" not in fixtures_data:
        print("No fixtures data available")
        return
    
    # Define countries and leagues to look for
    target_countries = ["Norway", "Sweden", "Poland", "Iceland", "Denmark", "Finland"]
    target_leagues = ["Tippeligaen", "Eliteserien", "Allsvenskan", "Ekstraklasa", "Premier League", "Superettan", "1. Division", "Ykkonen"]
    
    # Find matches for target countries and leagues
    matches = []
    for fixture in fixtures_data["response"]:
        country = fixture["league"]["country"]
        league_name = fixture["league"]["name"]
        
        if country in target_countries or any(league.lower() in league_name.lower() for league in target_leagues):
            home_team = fixture["teams"]["home"]["name"]
            away_team = fixture["teams"]["away"]["name"]
            
            matches.append({
                "country": country,
                "league": league_name,
                "match": f"{home_team} vs {away_team}",
                "fixture": fixture
            })
    
    # Group matches by country and league
    matches_by_country_league = {}
    for match in matches:
        key = f"{match['country']} - {match['league']}"
        if key not in matches_by_country_league:
            matches_by_country_league[key] = []
        matches_by_country_league[key].append(match)
    
    # Print results
    print(f"Found {len(matches)} matches in target countries/leagues:")
    for country_league, country_league_matches in matches_by_country_league.items():
        print(f"\n{country_league} ({len(country_league_matches)} matches):")
        for match in country_league_matches:
            print(f"  {match['match']}")

def main():
    fixtures_data = load_fixtures()
    if fixtures_data:
        check_leagues(fixtures_data)
    else:
        print("Failed to load fixtures data")

if __name__ == "__main__":
    main()
