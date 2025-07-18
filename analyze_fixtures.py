#!/usr/bin/env python3
import json
import os
from datetime import datetime
import pytz

# Define the leagues we're interested in
LEAGUES_OF_INTEREST = {
    "Norway - Tippeligaen": ["Norway", "Eliteserien"],
    "Danish SAS Ligaen": ["Denmark", "Superliga"],
    "Ireland FAI Cup": ["Ireland", "FAI Cup"],
    "Finnish Premier - Veikkausliiga": ["Finland", "Veikkausliiga"],
    "Russian Premier League": ["Russia", "Premier League"],
    "Romania Super League": ["Romania", "Liga I"],
    "Poland Division 1": ["Poland", "Ekstraklasa"],
    "Denmark Division 1": ["Denmark", "1. Division"],
    "Finland Ykkonen": ["Finland", "Ykkönen"],
    "Iceland Division 1": ["Iceland", "1. Deild"]
}

def load_fixtures_data(file_path):
    """Load fixtures data from a JSON file"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    with open(file_path, 'r') as f:
        return json.load(f)

def is_league_of_interest(fixture, leagues_of_interest):
    """Check if a fixture belongs to one of our leagues of interest"""
    league_country = fixture["league"]["country"]
    league_name = fixture["league"]["name"]
    
    for league_key, (country, name) in leagues_of_interest.items():
        if country.lower() in league_country.lower() and name.lower() in league_name.lower():
            return league_key
    
    return None

def is_before_noon_bangkok(fixture_date_str):
    """Check if a fixture is before noon Bangkok time"""
    fixture_date = datetime.fromisoformat(fixture_date_str.replace('Z', '+00:00'))
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    fixture_date_bangkok = fixture_date.astimezone(bangkok_tz)
    return fixture_date_bangkok.hour < 12

def analyze_fixtures(fixtures_data, leagues_of_interest, check_time=False):
    """Analyze fixtures and count matches by league of interest"""
    if not fixtures_data or "response" not in fixtures_data:
        return {}
    
    league_counts = {league: [] for league in leagues_of_interest.keys()}
    
    for fixture in fixtures_data["response"]:
        league_key = is_league_of_interest(fixture, leagues_of_interest)
        if league_key:
            fixture_date = fixture["fixture"]["date"]
            
            # If check_time is True, only include fixtures before noon Bangkok time
            if not check_time or is_before_noon_bangkok(fixture_date):
                home_team = fixture["teams"]["home"]["name"]
                away_team = fixture["teams"]["away"]["name"]
                match_info = {
                    "home": home_team,
                    "away": away_team,
                    "date": fixture_date
                }
                league_counts[league_key].append(match_info)
    
    return league_counts

def main():
    # Load fixtures data
    fixtures_day1 = load_fixtures_data("fixtures_2025-07-18.json")
    fixtures_day2 = load_fixtures_data("fixtures_2025-07-19.json")
    
    if not fixtures_day1 or not fixtures_day2:
        print("Failed to load fixtures data")
        return
    
    # Analyze fixtures for day 1
    league_counts_day1 = analyze_fixtures(fixtures_day1, LEAGUES_OF_INTEREST)
    
    # Analyze fixtures for day 2 (before noon Bangkok time)
    league_counts_day2 = analyze_fixtures(fixtures_day2, LEAGUES_OF_INTEREST, check_time=True)
    
    # Combine results
    combined_counts = {league: [] for league in LEAGUES_OF_INTEREST.keys()}
    for league in LEAGUES_OF_INTEREST.keys():
        combined_counts[league] = league_counts_day1.get(league, []) + league_counts_day2.get(league, [])
    
    # Print results
    print("Fixtures for July 18-19, 2025 (until noon Bangkok time on July 19):")
    print("=" * 80)
    
    total_matches = 0
    for league, matches in combined_counts.items():
        print(f"{league}: {len(matches)} matches")
        total_matches += len(matches)
        
        # Print match details
        for match in matches:
            print(f"  {match['home']} vs {match['away']} - {match['date']}")
    
    print("=" * 80)
    print(f"Total matches: {total_matches}")

if __name__ == "__main__":
    main()
