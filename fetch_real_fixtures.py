#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Fetch Real Fixtures from API-Football
ดึงข้อมูลการแข่งขันจริงจาก API-Football
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

def get_fixtures_by_date(date_str, timezone="Asia/Bangkok"):
    """
    Get fixtures for a specific date
    """
    url = f"{BASE_URL}/fixtures"
    
    params = {
        "date": date_str,
        "timezone": timezone
    }
    
    print(f"Fetching fixtures for {date_str} ({timezone})...")
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_league_id(league_name, country=None):
    """
    Get league ID from league name
    """
    url = f"{BASE_URL}/leagues"
    
    params = {
        "name": league_name
    }
    
    if country:
        params["country"] = country
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"] > 0:
            for league in data["response"]:
                if league["league"]["name"].lower() == league_name.lower():
                    if not country or league["country"]["name"].lower() == country.lower():
                        return league["league"]["id"]
    
    return None

def get_fixtures_by_league(league_id, date_str, timezone="Asia/Bangkok"):
    """
    Get fixtures for a specific league on a specific date
    """
    url = f"{BASE_URL}/fixtures"
    
    params = {
        "league": league_id,
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

def get_fixtures_for_leagues(leagues, date_str, timezone="Asia/Bangkok"):
    """
    Get fixtures for multiple leagues on a specific date
    """
    all_fixtures = []
    
    for league_info in leagues:
        league_name = league_info["name"]
        country = league_info.get("country")
        
        print(f"Searching for {league_name} ({country if country else 'any country'})...")
        
        league_id = get_league_id(league_name, country)
        
        if league_id:
            print(f"Found league ID: {league_id}")
            
            fixtures_data = get_fixtures_by_league(league_id, date_str, timezone)
            
            if fixtures_data and "response" in fixtures_data and fixtures_data["response"]:
                print(f"Found {len(fixtures_data['response'])} fixtures")
                
                for fixture in fixtures_data["response"]:
                    home_team = fixture["teams"]["home"]["name"]
                    away_team = fixture["teams"]["away"]["name"]
                    
                    # Convert time to Bangkok time
                    fixture_time = fixture["fixture"]["date"]
                    fixture_datetime = datetime.fromisoformat(fixture_time.replace("Z", "+00:00"))
                    bangkok_tz = pytz.timezone("Asia/Bangkok")
                    fixture_datetime_bangkok = fixture_datetime.astimezone(bangkok_tz)
                    fixture_time_bangkok = fixture_datetime_bangkok.strftime("%H:%M")
                    
                    all_fixtures.append({
                        "home_team": home_team,
                        "away_team": away_team,
                        "league": f"{country if country else fixture['league']['country']} - {league_name}",
                        "time": fixture_time_bangkok,
                        "date": fixture_time
                    })
            else:
                print(f"No fixtures found for {league_name}")
        else:
            print(f"League not found: {league_name}")
    
    return all_fixtures

def main():
    # Date to search for
    date_str = "2025-07-19"
    
    # Leagues to search for
    leagues = [
        {"name": "Tippeligaen", "country": "Norway"},
        {"name": "Allsvenskan", "country": "Sweden"},
        {"name": "Ekstraklasa", "country": "Poland"},
        {"name": "Premier League", "country": "Iceland"},
        {"name": "Superettan", "country": "Sweden"},
        {"name": "1. Division", "country": "Denmark"},
        {"name": "Ykkonen", "country": "Finland"}
    ]
    
    # Get fixtures for the specified leagues
    fixtures = get_fixtures_for_leagues(leagues, date_str)
    
    if fixtures:
        print(f"\nFound {len(fixtures)} fixtures for the specified leagues on {date_str}")
        
        # Group fixtures by league
        fixtures_by_league = {}
        for fixture in fixtures:
            league = fixture["league"]
            if league not in fixtures_by_league:
                fixtures_by_league[league] = []
            fixtures_by_league[league].append(fixture)
        
        # Print fixtures by league
        for league, league_fixtures in fixtures_by_league.items():
            print(f"\n{league} ({len(league_fixtures)} matches):")
            for fixture in league_fixtures:
                print(f"  {fixture['time']} - {fixture['home_team']} vs {fixture['away_team']}")
        
        # Save fixtures to JSON
        with open("real_fixtures.json", "w") as f:
            json.dump(fixtures, f, indent=2)
        
        print(f"\nFixtures saved to real_fixtures.json")
    else:
        print("No fixtures found")

if __name__ == "__main__":
    main()
