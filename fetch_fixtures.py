#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta
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

# League IDs mapping (these need to be verified with the actual API)
LEAGUE_IDS = {
    "Norway - Tippeligaen": 103,  # Eliteserien (formerly Tippeligaen)
    "Danish SAS Ligaen": 119,     # Danish Superliga (formerly SAS Ligaen)
    "Ireland FAI Cup": 528,       # FAI Cup
    "Finnish Premier - Veikkausliiga": 244,  # Veikkausliiga
    "Russian Premier League": 235, # Russian Premier League
    "Romania Super League": 283,   # Romania Liga I
    "Poland Division 1": 106,      # Ekstraklasa
    "Denmark Division 1": 120,     # 1. Division
    "Finland Ykkonen": 245,        # Ykkonen
    "Iceland Division 1": 265      # 1. deild
}

def get_fixtures_by_date_range(from_date, to_date, timezone="Asia/Bangkok"):
    """
    Get fixtures between two dates for all leagues of interest
    """
    url = f"{BASE_URL}/fixtures"
    
    # Convert dates to required format (YYYY-MM-DD)
    from_date_str = from_date.strftime("%Y-%m-%d")
    to_date_str = to_date.strftime("%Y-%m-%d")
    
    params = {
        "from": from_date_str,
        "to": to_date_str,
        "timezone": timezone
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def filter_fixtures_by_leagues(fixtures_data, league_ids):
    """
    Filter fixtures to only include those from specified leagues
    """
    if not fixtures_data or "response" not in fixtures_data:
        return []
    
    filtered_fixtures = []
    
    for fixture in fixtures_data["response"]:
        league_id = fixture["league"]["id"]
        if league_id in league_ids.values():
            filtered_fixtures.append(fixture)
    
    return filtered_fixtures

def get_league_name_by_id(league_id, league_ids):
    """
    Get league name from league ID
    """
    for name, id in league_ids.items():
        if id == league_id:
            return name
    return "Unknown League"

def count_fixtures_by_league(fixtures):
    """
    Count fixtures by league
    """
    league_counts = {}
    
    for fixture in fixtures:
        league_id = fixture["league"]["id"]
        league_name = get_league_name_by_id(league_id, LEAGUE_IDS)
        
        if league_name in league_counts:
            league_counts[league_name] += 1
        else:
            league_counts[league_name] = 1
    
    return league_counts

def main():
    # Set date range (July 18-19, 2025, until noon Thai time on the 19th)
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    
    # July 18, 2025 00:00 Bangkok time
    from_date = datetime(2025, 7, 18, 0, 0, 0)
    
    # July 19, 2025 12:00 Bangkok time
    to_date = datetime(2025, 7, 19, 12, 0, 0)
    
    print(f"Searching for fixtures from {from_date} to {to_date} (Bangkok time)")
    
    # Get fixtures
    fixtures_data = get_fixtures_by_date_range(from_date, to_date)
    
    if not fixtures_data:
        print("No data retrieved from API")
        return
    
    # Filter fixtures by leagues of interest
    filtered_fixtures = filter_fixtures_by_leagues(fixtures_data, LEAGUE_IDS)
    
    # Count fixtures by league
    league_counts = count_fixtures_by_league(filtered_fixtures)
    
    # Print results
    print("\nFixtures found by league:")
    print("-" * 40)
    
    total_fixtures = 0
    for league, count in league_counts.items():
        print(f"{league}: {count} matches")
        total_fixtures += count
    
    print("-" * 40)
    print(f"Total: {total_fixtures} matches")
    
    # Print details of each fixture
    print("\nDetailed fixtures:")
    print("=" * 80)
    
    for fixture in filtered_fixtures:
        league_name = get_league_name_by_id(fixture["league"]["id"], LEAGUE_IDS)
        home_team = fixture["teams"]["home"]["name"]
        away_team = fixture["teams"]["away"]["name"]
        fixture_date = fixture["fixture"]["date"]
        
        print(f"{league_name}: {home_team} vs {away_team} - {fixture_date}")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
