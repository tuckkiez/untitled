#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Ultra Advanced ML Football Analysis for Additional European Leagues (Real Data, Fixed)
วิเคราะห์การแข่งขันฟุตบอลลีกยุโรปเพิ่มเติมด้วย Ultra Advanced ML (ข้อมูลจริง, แก้ไขแล้ว)
"""

import json
import random
import datetime
import numpy as np
from datetime import datetime, timedelta
import pytz

# Import the analyzer class from the first part
from analyze_more_european_leagues_real_fixed import MoreEuropeanLeaguesAnalyzer

def get_more_european_fixtures_real_fixed():
    """Get real fixtures for additional European leagues with correct Thai time"""
    fixtures = []
    
    # Norway - Eliteserien
    fixtures.extend([
        {"home_team": "KFUM Oslo", "away_team": "Brann", "league": "Norway - Eliteserien", "time": "00:00"},
        {"home_team": "Molde", "away_team": "Stromsgodset", "league": "Norway - Eliteserien", "time": "02:00"},
        {"home_team": "Viking", "away_team": "Bodo/Glimt", "league": "Norway - Eliteserien", "time": "04:00"}
    ])
    
    # Sweden - Allsvenskan
    fixtures.extend([
        {"home_team": "Djurgardens IF", "away_team": "IF Elfsborg", "league": "Sweden - Allsvenskan", "time": "00:00"},
        {"home_team": "Osters IF", "away_team": "Malmo FF", "league": "Sweden - Allsvenskan", "time": "02:00"},
        {"home_team": "Degerfors IF", "away_team": "Gais", "league": "Sweden - Allsvenskan", "time": "04:00"}
    ])
    
    # Poland - Ekstraklasa
    fixtures.extend([
        {"home_team": "Lech Poznan", "away_team": "Cracovia Krakow", "league": "Poland - Ekstraklasa", "time": "00:45"},
        {"home_team": "Widzew Łódź", "away_team": "Zaglebie Lubin", "league": "Poland - Ekstraklasa", "time": "00:45"},
        {"home_team": "Wisla Plock", "away_team": "Korona Kielce", "league": "Poland - Ekstraklasa", "time": "03:30"}
    ])
    
    # Iceland - Úrvalsdeild
    fixtures.extend([
        {"home_team": "Breidablik", "away_team": "Vestri", "league": "Iceland - Úrvalsdeild", "time": "01:00"},
        {"home_team": "KA Akureyri", "away_team": "IA Akranes", "league": "Iceland - Úrvalsdeild", "time": "03:15"}
    ])
    
    # Sweden - Superettan
    fixtures.extend([
        {"home_team": "Oddevold", "away_team": "Orgryte IS", "league": "Sweden - Superettan", "time": "20:00"},
        {"home_team": "Umeå FC", "away_team": "Orebro SK", "league": "Sweden - Superettan", "time": "20:00"},
        {"home_team": "Ostersunds FK", "away_team": "falkenbergs FF", "league": "Sweden - Superettan", "time": "20:00"},
        {"home_team": "Sandviken", "away_team": "Vasteras SK FK", "league": "Sweden - Superettan", "time": "22:00"}
    ])
    
    # Denmark - 1. Division
    fixtures.extend([
        {"home_team": "Hvidovre", "away_team": "B 93", "league": "Denmark - 1. Division", "time": "00:00"},
        {"home_team": "Kolding IF", "away_team": "Aalborg", "league": "Denmark - 1. Division", "time": "19:00"},
        {"home_team": "Hillerød", "away_team": "Middelfart", "league": "Denmark - 1. Division", "time": "19:00"},
        {"home_team": "AC Horsens", "away_team": "Aarhus Fremad", "league": "Denmark - 1. Division", "time": "21:00"}
    ])
    
    # Finland - Ykkönen
    fixtures.extend([
        {"home_team": "Rops", "away_team": "Inter Turku II", "league": "Finland - Ykkönen", "time": "20:00"},
        {"home_team": "EPS", "away_team": "OLS", "league": "Finland - Ykkönen", "time": "20:00"},
        {"home_team": "JJK", "away_team": "Tampere United", "league": "Finland - Ykkönen", "time": "21:00"},
        {"home_team": "PKKU", "away_team": "Atlantis", "league": "Finland - Ykkönen", "time": "22:00"}
    ])
    
    return fixtures

def analyze_more_european_fixtures_real_fixed():
    """Analyze real fixtures for additional European leagues"""
    analyzer = MoreEuropeanLeaguesAnalyzer()
    
    # Get fixtures
    fixtures = get_more_european_fixtures_real_fixed()
    
    if not fixtures:
        print("No fixtures found")
        return []
    
    print(f"Found {len(fixtures)} fixtures to analyze")
    
    # Analyze each fixture
    results = []
    for fixture in fixtures:
        home_team = fixture["home_team"]
        away_team = fixture["away_team"]
        league = fixture["league"]
        match_time = fixture["time"]
        
        analysis = analyzer.analyze_match(home_team, away_team, league, match_time)
        results.append(analysis)
        
        print(f"Analyzed: {home_team} vs {away_team} ({league})")
    
    # Save results to JSON
    with open('more_european_leagues_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Analysis complete. Analyzed {len(results)} matches.")
    
    return results

def main():
    # Analyze fixtures
    results = analyze_more_european_fixtures_real_fixed()
    
    # Print high confidence predictions
    high_confidence = [match for match in results if match["high_confidence"]]
    print(f"Found {len(high_confidence)} high confidence predictions.")
    
    for match in high_confidence:
        print(f"\n{match['match']} ({match['league']}):")
        
        if match["match_result"]["confidence"] >= 70:
            print(f"  Match Result: {match['match_result']['prediction']} ({match['match_result']['confidence']}%)")
        
        if match["over_under"]["confidence"] >= 70:
            print(f"  Over/Under: {match['over_under']['prediction']} ({match['over_under']['confidence']}%)")
        
        if match["btts"]["confidence"] >= 70:
            print(f"  BTTS: {match['btts']['prediction']} ({match['btts']['confidence']}%)")
        
        if match["corners"]["confidence"] >= 70:
            print(f"  Corners: {match['corners']['prediction']} ({match['corners']['confidence']}%)")

if __name__ == "__main__":
    main()
