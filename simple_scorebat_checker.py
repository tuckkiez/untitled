#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Simple ScoreBat Checker
ตรวจสอบ ScoreBat โดยไม่ใช้ external libraries
"""

import requests
import re
import json
from datetime import datetime

def print_header():
    print("🔍 Simple ScoreBat Checker")
    print("=" * 40)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 40)

def check_scorebat_simple():
    """ตรวจสอบ ScoreBat แบบง่าย"""
    print("\n🌐 Checking ScoreBat.com...")
    
    try:
        url = "https://www.scorebat.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        print(f"   📡 Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html = response.text
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📄 Content length: {len(html)} chars")
            
            # Simple text search for J-League
            jleague_matches = find_jleague_in_text(html)
            
            return jleague_matches
            
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return []

def find_jleague_in_text(html):
    """หา J-League ในข้อความ HTML"""
    print("\n🔍 Searching for J-League content...")
    
    matches = []
    
    try:
        # Search for J-League mentions
        jleague_pattern = re.compile(r'J-League\s*2?', re.IGNORECASE)
        jleague_matches = jleague_pattern.findall(html)
        
        if jleague_matches:
            print(f"   ✅ Found {len(jleague_matches)} J-League mentions")
            for match in set(jleague_matches):  # Remove duplicates
                print(f"      📝 {match}")
        else:
            print("   ❌ No J-League mentions found")
        
        # Search for Japanese team names
        japanese_teams = [
            'FC Tokyo', 'Yokohama', 'Kashima', 'Urawa', 'Gamba', 'Cerezo',
            'Vissel', 'Sanfrecce', 'Kawasaki', 'Nagoya', 'Ventforet', 'Montedio',
            'Machida', 'Roasso', 'Fagiano', 'Tokushima', 'Renofa', 'Ehime'
        ]
        
        found_teams = []
        for team in japanese_teams:
            if team.lower() in html.lower():
                found_teams.append(team)
        
        if found_teams:
            print(f"   🎯 Found Japanese teams: {len(found_teams)}")
            for team in found_teams[:5]:  # Show first 5
                print(f"      ⚽ {team}")
        else:
            print("   ❌ No Japanese team names found")
        
        # Look for match patterns
        match_patterns = [
            r'(\w+)\s+vs?\s+(\w+)',  # Team vs Team
            r'(\w+)\s+[-–]\s+(\w+)',  # Team - Team
            r'(\d+)\s*[-:]\s*(\d+)',  # Score patterns
        ]
        
        for pattern in match_patterns:
            matches_found = re.findall(pattern, html, re.IGNORECASE)
            if matches_found:
                print(f"   📊 Pattern '{pattern}': {len(matches_found)} matches")
                for match in matches_found[:3]:  # Show first 3
                    print(f"      🔍 {match}")
        
        # Search for time patterns
        time_patterns = [
            r'\d{1,2}:\d{2}',  # HH:MM
            r'\d{1,2}h\d{2}',  # HHhMM
            r'(today|tomorrow|yesterday)',  # Relative dates
        ]
        
        for pattern in time_patterns:
            times_found = re.findall(pattern, html, re.IGNORECASE)
            if times_found:
                print(f"   ⏰ Time pattern '{pattern}': {len(set(times_found))} unique")
        
    except Exception as e:
        print(f"   ❌ Text search error: {e}")
    
    return matches

def check_scorebat_json():
    """ตรวจสอบว่ามี JSON data หรือไม่"""
    print("\n📋 Checking for JSON data...")
    
    try:
        # Try to find JSON endpoints
        json_urls = [
            "https://www.scorebat.com/video-api/v3/",
            "https://www.scorebat.com/api/",
            "https://www.scorebat.com/data/",
        ]
        
        for url in json_urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   ✅ JSON found at: {url}")
                        print(f"      📊 Keys: {list(data.keys()) if isinstance(data, dict) else 'Array'}")
                        return data
                    except:
                        print(f"   📄 Text response at: {url}")
                        print(f"      📝 Content: {response.text[:100]}...")
                else:
                    print(f"   ❌ {url}: {response.status_code}")
            except:
                print(f"   ❌ {url}: Connection failed")
        
    except Exception as e:
        print(f"   ❌ JSON check error: {e}")
    
    return None

def manual_check_guide():
    """คู่มือการตรวจสอบด้วยตนเอง"""
    print("\n📖 Manual Check Guide:")
    print("=" * 30)
    
    steps = [
        "1. Open https://www.scorebat.com/ in browser",
        "2. Scroll down to find 'J-League 2' section",
        "3. Look for today's matches",
        "4. Note team names and match times",
        "5. Get odds from betting sites"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🎯 What to look for:")
    print("   - Match format: 'Team A vs Team B'")
    print("   - Time: Usually in JST (Japan Standard Time)")
    print("   - Status: 'Live', 'FT' (Full Time), or future time")
    
    print("\n💰 Betting sites for odds:")
    betting_sites = [
        "Bet365", "William Hill", "Pinnacle", "1xBet", "Unibet"
    ]
    for site in betting_sites:
        print(f"   • {site}")

def suggest_next_steps():
    """แนะนำขั้นตอนต่อไป"""
    print("\n🚀 Suggested Next Steps:")
    
    options = [
        {
            'option': 'Manual ScoreBat Check',
            'action': 'Visit scorebat.com and find J-League 2 matches',
            'time': '2-3 minutes'
        },
        {
            'option': 'Use Demo Data',
            'action': 'Continue with current Aldosivi vs Central Córdoba',
            'time': 'Immediate'
        },
        {
            'option': 'Wait for Tomorrow',
            'action': 'Use Melbourne Victory vs Western Sydney',
            'time': '1 day'
        },
        {
            'option': 'Install BeautifulSoup',
            'action': 'pip install beautifulsoup4 for better scraping',
            'time': '5 minutes'
        }
    ]
    
    for i, opt in enumerate(options, 1):
        print(f"   {i}. {opt['option']}")
        print(f"      📋 {opt['action']}")
        print(f"      ⏱️  {opt['time']}")
        print()

def main():
    print_header()
    
    # Check ScoreBat
    matches = check_scorebat_simple()
    
    # Check for JSON
    json_data = check_scorebat_json()
    
    # Show manual guide
    manual_check_guide()
    
    # Suggest next steps
    suggest_next_steps()
    
    print("\n" + "=" * 40)
    print("💡 RECOMMENDATION")
    print("=" * 40)
    print("Since automated scraping is limited without BeautifulSoup:")
    print("1. 🌐 Manually check https://www.scorebat.com/")
    print("2. 📝 Find J-League 2 matches")
    print("3. 💰 Get odds from betting sites")
    print("4. 🔄 Update our analyzer with real data")
    print("5. 🚀 Deploy updated analysis")

if __name__ == "__main__":
    main()
