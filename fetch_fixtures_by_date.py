#!/usr/bin/env python3
import requests
import json
from datetime import datetime

# API configuration
API_HOST = "api-football-v1.p.rapidapi.com"
API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

# Headers for API requests
headers = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

def get_fixtures_by_date(date_str, timezone="Asia/Bangkok"):
    """
    Get fixtures for a specific date
    """
    url = f"{BASE_URL}/fixtures"
    
    params = {
        "date": date_str,
        "timezone": timezone
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def print_fixtures_summary(fixtures_data):
    """
    Print a summary of fixtures
    """
    if not fixtures_data or "response" not in fixtures_data:
        print("No fixtures data available")
        return
    
    fixtures = fixtures_data["response"]
    print(f"Total fixtures found: {len(fixtures)}")
    
    # Group fixtures by league
    leagues = {}
    for fixture in fixtures:
        league_name = f"{fixture['league']['country']} - {fixture['league']['name']}"
        if league_name not in leagues:
            leagues[league_name] = []
        leagues[league_name].append(fixture)
    
    # Print summary by league
    print("\nFixtures by league:")
    print("-" * 80)
    for league_name, league_fixtures in leagues.items():
        print(f"{league_name}: {len(league_fixtures)} matches")
    
    # Print detailed fixtures for specific leagues of interest
    leagues_of_interest = [
        "Norway - Eliteserien",
        "Denmark - Superliga",
        "Ireland - FAI Cup",
        "Finland - Veikkausliiga",
        "Russia - Premier League",
        "Romania - Liga I",
        "Poland - Ekstraklasa",
        "Denmark - 1. Division",
        "Finland - Ykkonen",
        "Iceland - 1. deild"
    ]
    
    print("\nDetailed fixtures for leagues of interest:")
    print("=" * 80)
    
    for league_name, league_fixtures in leagues.items():
        # Check if this league matches any of our leagues of interest
        is_league_of_interest = False
        for interest_league in leagues_of_interest:
            if interest_league.lower() in league_name.lower():
                is_league_of_interest = True
                break
        
        if is_league_of_interest:
            print(f"\n{league_name} ({len(league_fixtures)} matches):")
            for fixture in league_fixtures:
                home_team = fixture["teams"]["home"]["name"]
                away_team = fixture["teams"]["away"]["name"]
                fixture_date = fixture["fixture"]["date"]
                print(f"  {home_team} vs {away_team} - {fixture_date}")

def main():
    # Check fixtures for July 18, 2025
    date_str_1 = "2025-07-18"
    print(f"Searching for fixtures on {date_str_1}...")
    fixtures_data_1 = get_fixtures_by_date(date_str_1)
    print_fixtures_summary(fixtures_data_1)
    
    # Check fixtures for July 19, 2025 (until noon)
    date_str_2 = "2025-07-19"
    print(f"\n\nSearching for fixtures on {date_str_2}...")
    fixtures_data_2 = get_fixtures_by_date(date_str_2)
    print_fixtures_summary(fixtures_data_2)
    
    # Save the raw data to files for further analysis
    with open(f"fixtures_{date_str_1}.json", "w") as f:
        json.dump(fixtures_data_1, f, indent=2)
    
    with open(f"fixtures_{date_str_2}.json", "w") as f:
        json.dump(fixtures_data_2, f, indent=2)
    
    print(f"\nRaw data saved to fixtures_{date_str_1}.json and fixtures_{date_str_2}.json")

if __name__ == "__main__":
    main()
