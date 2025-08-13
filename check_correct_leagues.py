#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Check Correct Leagues and Match Times
ตรวจสอบข้อมูลลีกที่ถูกต้องและเวลาเตะ
"""

import json
import pytz
from datetime import datetime

def load_fixtures():
    """Load fixtures from today_fixtures.json"""
    try:
        with open('today_fixtures.json', 'r') as f:
            return json.load(f)
    except:
        print("Error: Could not load today_fixtures.json")
        return None

def convert_to_thai_time(utc_time_str):
    """Convert UTC time to Thai time"""
    try:
        # Parse the UTC time string
        utc_time = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        
        # Convert to Thai time (UTC+7)
        thai_tz = pytz.timezone('Asia/Bangkok')
        thai_time = utc_time.astimezone(thai_tz)
        
        # Format as HH:MM
        return thai_time.strftime('%H:%M')
    except Exception as e:
        print(f"Error converting time: {e}")
        return utc_time_str

def check_leagues(fixtures_data):
    """Check for specific leagues in fixtures data"""
    if not fixtures_data or "response" not in fixtures_data:
        print("No fixtures data available")
        return
    
    # Define target leagues
    target_leagues = [
        {"country": "Finland", "name": "Ykkönen"},
        {"country": "Denmark", "name": "1. Division"},
        {"country": "Sweden", "name": "Superettan"}
    ]
    
    # Find matches for target leagues
    for target in target_leagues:
        print(f"\nSearching for {target['country']} - {target['name']}:")
        found = False
        
        for fixture in fixtures_data["response"]:
            country = fixture["league"]["country"]
            league_name = fixture["league"]["name"]
            
            if country == target["country"] and target["name"].lower() in league_name.lower():
                found = True
                home_team = fixture["teams"]["home"]["name"]
                away_team = fixture["teams"]["away"]["name"]
                fixture_time = fixture["fixture"]["date"]
                thai_time = convert_to_thai_time(fixture_time)
                
                print(f"  {thai_time} - {home_team} vs {away_team} ({league_name})")
        
        if not found:
            print(f"  No matches found for {target['country']} - {target['name']}")
            
            # Try to find similar leagues
            print("  Searching for similar leagues:")
            for fixture in fixtures_data["response"]:
                country = fixture["league"]["country"]
                league_name = fixture["league"]["name"]
                
                if country == target["country"]:
                    print(f"    Found league: {league_name}")

def main():
    fixtures_data = load_fixtures()
    if fixtures_data:
        check_leagues(fixtures_data)
    else:
        print("Failed to load fixtures data")

if __name__ == "__main__":
    main()
