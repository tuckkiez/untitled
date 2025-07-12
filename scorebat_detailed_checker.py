#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ScoreBat Detailed Checker
ตรวจสอบข้อมูลการแข่งขันจาก ScoreBat อย่างละเอียด
"""

import requests
import json
from datetime import datetime

def print_header():
    print("🔍 ScoreBat Detailed Checker")
    print("=" * 45)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 45)

def get_scorebat_data():
    """ดึงข้อมูลจาก ScoreBat API"""
    print("\n📡 Fetching ScoreBat data...")
    
    try:
        url = "https://www.scorebat.com/video-api/v3/"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Response: {response.status_code}")
            print(f"   📊 Data keys: {list(data.keys())}")
            
            if 'response' in data:
                matches = data['response']
                print(f"   🎯 Total matches: {len(matches)}")
                return matches
            else:
                print(f"   ❌ No 'response' key found")
                print(f"   📄 Available data: {data}")
                
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return []

def analyze_first_few_matches(matches):
    """วิเคราะห์การแข่งขันแรกๆ"""
    print(f"\n🔍 Analyzing first 5 matches...")
    
    for i, match in enumerate(matches[:5], 1):
        print(f"\n   📊 Match {i}:")
        print(f"      Type: {type(match)}")
        
        if isinstance(match, dict):
            # Show all keys
            print(f"      Keys: {list(match.keys())}")
            
            # Show important fields
            important_fields = ['title', 'date', 'competition', 'side1', 'side2', 'matchviewUrl']
            for field in important_fields:
                if field in match:
                    value = match[field]
                    if isinstance(value, dict):
                        print(f"      {field}: {list(value.keys())} (dict)")
                    else:
                        print(f"      {field}: {value}")
        else:
            print(f"      Raw data: {str(match)[:100]}...")

def find_todays_matches_safe(matches):
    """หาการแข่งขันวันนี้อย่างปลอดภัย"""
    print(f"\n📅 Finding today's matches (safe method)...")
    
    today_matches = []
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    for i, match in enumerate(matches):
        try:
            if isinstance(match, dict):
                # Check various date fields
                date_found = False
                match_date = None
                
                # Try different date field names
                date_fields = ['date', 'matchDate', 'kickoff', 'datetime', 'time']
                
                for field in date_fields:
                    if field in match:
                        date_value = match[field]
                        if isinstance(date_value, str) and today_str in date_value:
                            today_matches.append(match)
                            date_found = True
                            match_date = date_value
                            break
                
                if date_found:
                    title = match.get('title', 'Unknown match')
                    print(f"      ✅ Match {i+1}: {title} ({match_date})")
                    
        except Exception as e:
            print(f"      ❌ Error processing match {i+1}: {e}")
            continue
    
    print(f"   🎯 Found {len(today_matches)} matches today")
    return today_matches

def find_jleague_matches_safe(matches):
    """หาการแข่งขัน J-League อย่างปลอดภัย"""
    print(f"\n🇯🇵 Finding J-League matches (safe method)...")
    
    jleague_matches = []
    jleague_keywords = ['j-league', 'j league', 'jleague', 'japan', 'japanese']
    
    for i, match in enumerate(matches):
        try:
            if isinstance(match, dict):
                # Check title and competition fields
                text_to_check = []
                
                if 'title' in match:
                    text_to_check.append(str(match['title']).lower())
                
                if 'competition' in match:
                    comp = match['competition']
                    if isinstance(comp, dict) and 'name' in comp:
                        text_to_check.append(str(comp['name']).lower())
                    elif isinstance(comp, str):
                        text_to_check.append(comp.lower())
                
                # Check for J-League keywords
                for text in text_to_check:
                    if any(keyword in text for keyword in jleague_keywords):
                        jleague_matches.append(match)
                        title = match.get('title', 'Unknown match')
                        print(f"      ✅ J-League {i+1}: {title}")
                        break
                        
        except Exception as e:
            print(f"      ❌ Error processing match {i+1}: {e}")
            continue
    
    print(f"   🎯 Found {len(jleague_matches)} J-League matches")
    return jleague_matches

def extract_match_details(matches, label="matches"):
    """แยกรายละเอียดการแข่งขัน"""
    print(f"\n⚽ Extracting details from {len(matches)} {label}...")
    
    extracted_matches = []
    
    for i, match in enumerate(matches):
        try:
            if isinstance(match, dict):
                # Extract basic info safely
                match_info = {
                    'title': match.get('title', 'Unknown'),
                    'date': match.get('date', 'Unknown'),
                    'url': match.get('matchviewUrl', ''),
                }
                
                # Extract competition
                comp = match.get('competition', {})
                if isinstance(comp, dict):
                    match_info['competition'] = comp.get('name', 'Unknown Competition')
                else:
                    match_info['competition'] = str(comp) if comp else 'Unknown Competition'
                
                # Extract teams
                side1 = match.get('side1', {})
                side2 = match.get('side2', {})
                
                if isinstance(side1, dict):
                    match_info['home'] = side1.get('name', 'Unknown Team')
                else:
                    match_info['home'] = str(side1) if side1 else 'Unknown Team'
                
                if isinstance(side2, dict):
                    match_info['away'] = side2.get('name', 'Unknown Team')
                else:
                    match_info['away'] = str(side2) if side2 else 'Unknown Team'
                
                extracted_matches.append(match_info)
                
                print(f"      {i+1}. [{match_info['competition']}] {match_info['home']} vs {match_info['away']}")
                print(f"         📅 {match_info['date']}")
                
        except Exception as e:
            print(f"      ❌ Error extracting match {i+1}: {e}")
            continue
    
    return extracted_matches

def main():
    print_header()
    
    # Get data from ScoreBat
    matches = get_scorebat_data()
    
    if not matches:
        print("\n❌ No data retrieved from ScoreBat API")
        return
    
    # Analyze structure
    analyze_first_few_matches(matches)
    
    # Find today's matches
    today_matches = find_todays_matches_safe(matches)
    
    # Find J-League matches
    jleague_matches = find_jleague_matches_safe(matches)
    
    # Extract details
    if today_matches:
        print("\n" + "="*45)
        print("🔥 TODAY'S MATCHES DETAILS")
        print("="*45)
        today_details = extract_match_details(today_matches, "today's matches")
    
    if jleague_matches:
        print("\n" + "="*45)
        print("🇯🇵 J-LEAGUE MATCHES DETAILS")
        print("="*45)
        jleague_details = extract_match_details(jleague_matches, "J-League matches")
    
    # Summary
    print("\n" + "="*45)
    print("📊 FINAL SUMMARY")
    print("="*45)
    print(f"📈 Total matches in API: {len(matches)}")
    print(f"📅 Today's matches found: {len(today_matches)}")
    print(f"🇯🇵 J-League matches found: {len(jleague_matches)}")
    
    if today_matches:
        print(f"\n🎯 RECOMMENDATION: Use today's matches!")
        print(f"   1. Pick a match from today's list")
        print(f"   2. Get betting odds for that match")
        print(f"   3. Update analyzer with real data")
    elif jleague_matches:
        print(f"\n🎯 RECOMMENDATION: Check J-League match dates!")
        print(f"   1. Look for upcoming J-League matches")
        print(f"   2. Use the closest match date")
    else:
        print(f"\n💡 FALLBACK: Use existing demo data")
        print(f"   Current: Aldosivi vs Central Córdoba")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Choose best match from results above")
    print(f"   2. Visit betting sites for odds")
    print(f"   3. Update corrected_value_bet_analyzer.py")
    print(f"   4. Deploy: ./quick_deploy.sh 'New match data'")

if __name__ == "__main__":
    main()
