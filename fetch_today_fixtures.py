#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Fetch Today's Football Fixtures
ดึงตารางฟุตบอลวันนี้จาก API-Football
"""

import requests
import json
from datetime import datetime
import pytz

# API configuration
API_HOST = "api-football-v1.p.rapidapi.com"
API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"  # Replace with your actual API key if needed
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

# Headers for API requests
headers = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

def get_today_fixtures(timezone="Asia/Bangkok"):
    """
    Get fixtures for today
    """
    url = f"{BASE_URL}/fixtures"
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime("%Y-%m-%d")
    
    params = {
        "date": today,
        "timezone": timezone
    }
    
    print(f"Fetching fixtures for {today} ({timezone})...")
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def summarize_fixtures(fixtures_data):
    """
    Summarize fixtures by league
    """
    if not fixtures_data or "response" not in fixtures_data:
        print("No fixtures data available")
        return
    
    fixtures = fixtures_data["response"]
    print(f"Total fixtures found: {len(fixtures)}")
    
    # Group fixtures by league
    leagues = {}
    for fixture in fixtures:
        league_id = fixture["league"]["id"]
        league_name = fixture["league"]["name"]
        league_country = fixture["league"]["country"]
        
        league_key = f"{league_country} - {league_name}"
        
        if league_key not in leagues:
            leagues[league_key] = {
                "id": league_id,
                "name": league_name,
                "country": league_country,
                "fixtures": []
            }
        
        home_team = fixture["teams"]["home"]["name"]
        away_team = fixture["teams"]["away"]["name"]
        fixture_time = fixture["fixture"]["date"]
        fixture_id = fixture["fixture"]["id"]
        
        # Convert time to Bangkok time
        fixture_datetime = datetime.fromisoformat(fixture_time.replace("Z", "+00:00"))
        bangkok_tz = pytz.timezone("Asia/Bangkok")
        fixture_datetime_bangkok = fixture_datetime.astimezone(bangkok_tz)
        fixture_time_bangkok = fixture_datetime_bangkok.strftime("%H:%M")
        
        leagues[league_key]["fixtures"].append({
            "id": fixture_id,
            "home_team": home_team,
            "away_team": away_team,
            "time": fixture_time_bangkok,
            "full_time": fixture_time
        })
    
    # Sort leagues by country and name
    sorted_leagues = sorted(leagues.items(), key=lambda x: (x[1]["country"], x[1]["name"]))
    
    # Print summary
    print("\nFixtures by league:")
    print("-" * 80)
    
    total_leagues = len(sorted_leagues)
    total_fixtures = sum(len(league[1]["fixtures"]) for league in sorted_leagues)
    
    print(f"Total: {total_leagues} leagues with {total_fixtures} fixtures\n")
    
    for league_key, league_data in sorted_leagues:
        fixtures_count = len(league_data["fixtures"])
        print(f"{league_key}: {fixtures_count} matches")
    
    # Return the data for further processing
    return {
        "total_leagues": total_leagues,
        "total_fixtures": total_fixtures,
        "leagues": dict(sorted_leagues)
    }

def save_fixtures_to_file(fixtures_data, filename="today_fixtures.json"):
    """
    Save fixtures data to a JSON file
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(fixtures_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nFixtures data saved to {filename}")

def print_detailed_fixtures(fixtures_data, max_leagues=None, max_fixtures_per_league=None):
    """
    Print detailed fixtures information
    """
    if not fixtures_data or "response" not in fixtures_data:
        print("No fixtures data available")
        return
    
    fixtures = fixtures_data["response"]
    
    # Group fixtures by league
    leagues = {}
    for fixture in fixtures:
        league_id = fixture["league"]["id"]
        league_name = fixture["league"]["name"]
        league_country = fixture["league"]["country"]
        
        league_key = f"{league_country} - {league_name}"
        
        if league_key not in leagues:
            leagues[league_key] = {
                "id": league_id,
                "name": league_name,
                "country": league_country,
                "fixtures": []
            }
        
        home_team = fixture["teams"]["home"]["name"]
        away_team = fixture["teams"]["away"]["name"]
        fixture_time = fixture["fixture"]["date"]
        
        # Convert time to Bangkok time
        fixture_datetime = datetime.fromisoformat(fixture_time.replace("Z", "+00:00"))
        bangkok_tz = pytz.timezone("Asia/Bangkok")
        fixture_datetime_bangkok = fixture_datetime.astimezone(bangkok_tz)
        fixture_time_bangkok = fixture_datetime_bangkok.strftime("%H:%M")
        
        leagues[league_key]["fixtures"].append({
            "home_team": home_team,
            "away_team": away_team,
            "time": fixture_time_bangkok
        })
    
    # Sort leagues by country and name
    sorted_leagues = sorted(leagues.items(), key=lambda x: (x[1]["country"], x[1]["name"]))
    
    # Limit the number of leagues if specified
    if max_leagues:
        sorted_leagues = sorted_leagues[:max_leagues]
    
    print("\nDetailed fixtures:")
    print("=" * 80)
    
    for league_key, league_data in sorted_leagues:
        print(f"\n{league_key} ({len(league_data['fixtures'])} matches):")
        
        # Sort fixtures by time
        sorted_fixtures = sorted(league_data["fixtures"], key=lambda x: x["time"])
        
        # Limit the number of fixtures per league if specified
        if max_fixtures_per_league:
            sorted_fixtures = sorted_fixtures[:max_fixtures_per_league]
        
        for fixture in sorted_fixtures:
            print(f"  {fixture['time']} - {fixture['home_team']} vs {fixture['away_team']}")
    
    print("=" * 80)

def main():
    # Get today's fixtures
    fixtures_data = get_today_fixtures()
    
    if not fixtures_data:
        print("Failed to fetch fixtures data")
        return
    
    # Summarize fixtures
    summary = summarize_fixtures(fixtures_data)
    
    # Save fixtures to file
    save_fixtures_to_file(fixtures_data)
    
    # Print detailed fixtures (limit to 10 leagues, 5 fixtures per league)
    print_detailed_fixtures(fixtures_data, max_leagues=10, max_fixtures_per_league=5)
    
    return summary

if __name__ == "__main__":
    main()
