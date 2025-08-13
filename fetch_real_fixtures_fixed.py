#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Fetch Real Fixtures from API-Football (Fixed)
ดึงข้อมูลการแข่งขันจริงจาก API-Football (แก้ไขแล้ว)
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

def get_leagues_by_country(country):
    """
    Get all leagues for a specific country
    """
    url = f"{BASE_URL}/leagues"
    
    params = {
        "country": country
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_fixtures_for_countries(countries, date_str, timezone="Asia/Bangkok"):
    """
    Get fixtures for multiple countries on a specific date
    """
    all_fixtures = []
    
    for country in countries:
        print(f"Searching for leagues in {country}...")
        
        leagues_data = get_leagues_by_country(country)
        
        if leagues_data and "response" in leagues_data and leagues_data["response"]:
            print(f"Found {len(leagues_data['response'])} leagues in {country}")
            
            for league in leagues_data["response"]:
                league_id = league["league"]["id"]
                league_name = league["league"]["name"]
                
                print(f"Checking fixtures for {league_name} (ID: {league_id})...")
                
                url = f"{BASE_URL}/fixtures"
                
                params = {
                    "league": league_id,
                    "date": date_str,
                    "timezone": timezone
                }
                
                response = requests.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    fixtures_data = response.json()
                    
                    if fixtures_data and "response" in fixtures_data and fixtures_data["response"]:
                        print(f"Found {len(fixtures_data['response'])} fixtures in {league_name}")
                        
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
                                "league": f"{country} - {league_name}",
                                "time": fixture_time_bangkok,
                                "date": fixture_time
                            })
        else:
            print(f"No leagues found for {country}")
    
    return all_fixtures

def main():
    # Date to search for
    date_str = "2025-07-19"
    
    # Countries to search for
    countries = [
        "Norway",
        "Sweden",
        "Poland",
        "Iceland",
        "Denmark",
        "Finland"
    ]
    
    # Get fixtures for the specified countries
    fixtures = get_fixtures_for_countries(countries, date_str)
    
    if fixtures:
        print(f"\nFound {len(fixtures)} fixtures for the specified countries on {date_str}")
        
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
