#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ScoreBat API Checker
ตรวจสอบ API ของ ScoreBat ที่พบ
"""

import requests
import json
from datetime import datetime, timedelta

def print_header():
    print("🔍 ScoreBat API Checker")
    print("=" * 40)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 40)

def check_scorebat_api():
    """ตรวจสอบ ScoreBat API"""
    print("\n📡 Checking ScoreBat API...")
    
    try:
        url = "https://www.scorebat.com/video-api/v3/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Response received")
            print(f"   📊 Keys: {list(data.keys())}")
            
            if 'response' in data:
                matches = data['response']
                print(f"   🎯 Found {len(matches)} total matches")
                
                # Filter for today's matches
                today_matches = filter_todays_matches(matches)
                
                # Filter for J-League
                jleague_matches = filter_jleague_matches(matches)
                
                return matches, today_matches, jleague_matches
            else:
                print(f"   ❌ No 'response' key in data")
                print(f"   📄 Data structure: {data}")
                
        else:
            print(f"   ❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ API Error: {e}")
    
    return [], [], []

def filter_todays_matches(matches):
    """กรองการแข่งขันวันนี้"""
    print("\n📅 Filtering today's matches...")
    
    today_matches = []
    today = datetime.now().date()
    
    for match in matches:
        try:
            # Check various date fields
            date_fields = ['date', 'matchDate', 'kickoff', 'datetime']
            match_date = None
            
            for field in date_fields:
                if field in match:
                    date_str = match[field]
                    try:
                        # Try different date formats
                        for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']:
                            try:
                                match_date = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d').date()
                                break
                            except:
                                continue
                        break
                    except:
                        continue
            
            if match_date == today:
                today_matches.append(match)
                
        except Exception as e:
            continue
    
    print(f"   🎯 Found {len(today_matches)} matches today")
    
    if today_matches:
        for i, match in enumerate(today_matches[:5], 1):
            home = match.get('side1', {}).get('name', 'Unknown')
            away = match.get('side2', {}).get('name', 'Unknown')
            competition = match.get('competition', {}).get('name', 'Unknown')
            print(f"      {i}. [{competition}] {home} vs {away}")
    
    return today_matches

def filter_jleague_matches(matches):
    """กรองการแข่งขัน J-League"""
    print("\n🇯🇵 Filtering J-League matches...")
    
    jleague_matches = []
    
    for match in matches:
        try:
            competition = match.get('competition', {}).get('name', '').lower()
            title = match.get('title', '').lower()
            
            # Look for J-League indicators
            jleague_indicators = ['j-league', 'j league', 'japan', 'jleague']
            
            is_jleague = any(indicator in competition or indicator in title 
                           for indicator in jleague_indicators)
            
            if is_jleague:
                jleague_matches.append(match)
                
        except Exception as e:
            continue
    
    print(f"   🎯 Found {len(jleague_matches)} J-League matches")
    
    if jleague_matches:
        for i, match in enumerate(jleague_matches[:5], 1):
            home = match.get('side1', {}).get('name', 'Unknown')
            away = match.get('side2', {}).get('name', 'Unknown')
            competition = match.get('competition', {}).get('name', 'Unknown')
            date = match.get('date', 'Unknown date')
            print(f"      {i}. [{competition}] {home} vs {away} ({date})")
    
    return jleague_matches

def analyze_match_structure(matches):
    """วิเคราะห์โครงสร้างข้อมูลการแข่งขัน"""
    print("\n🔍 Analyzing match data structure...")
    
    if not matches:
        print("   ❌ No matches to analyze")
        return
    
    # Take first match as sample
    sample_match = matches[0]
    print(f"   📊 Sample match structure:")
    
    def print_dict_structure(d, indent=0):
        for key, value in d.items():
            spaces = "   " + "  " * indent
            if isinstance(value, dict):
                print(f"{spaces}📁 {key}:")
                print_dict_structure(value, indent + 1)
            elif isinstance(value, list):
                print(f"{spaces}📋 {key}: [{len(value)} items]")
                if value and isinstance(value[0], dict):
                    print(f"{spaces}   Sample item:")
                    print_dict_structure(value[0], indent + 2)
            else:
                value_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                print(f"{spaces}📄 {key}: {value_str}")
    
    print_dict_structure(sample_match)

def extract_useful_matches(matches):
    """แยกการแข่งขันที่มีประโยชน์"""
    print("\n⚽ Extracting useful match data...")
    
    useful_matches = []
    
    for match in matches[:10]:  # Check first 10 matches
        try:
            # Extract basic info
            match_info = {
                'home': match.get('side1', {}).get('name', 'Unknown'),
                'away': match.get('side2', {}).get('name', 'Unknown'),
                'competition': match.get('competition', {}).get('name', 'Unknown'),
                'date': match.get('date', 'Unknown'),
                'title': match.get('title', ''),
                'url': match.get('matchviewUrl', ''),
            }
            
            # Only include if we have team names
            if match_info['home'] != 'Unknown' and match_info['away'] != 'Unknown':
                useful_matches.append(match_info)
                
        except Exception as e:
            continue
    
    print(f"   ✅ Extracted {len(useful_matches)} useful matches")
    
    for i, match in enumerate(useful_matches[:5], 1):
        print(f"      {i}. [{match['competition']}] {match['home']} vs {match['away']}")
        print(f"         📅 {match['date']}")
    
    return useful_matches

def main():
    print_header()
    
    # Check API
    all_matches, today_matches, jleague_matches = check_scorebat_api()
    
    if all_matches:
        # Analyze structure
        analyze_match_structure(all_matches)
        
        # Extract useful data
        useful_matches = extract_useful_matches(all_matches)
        
        print("\n" + "=" * 40)
        print("📊 SUMMARY")
        print("=" * 40)
        print(f"📈 Total matches in API: {len(all_matches)}")
        print(f"📅 Today's matches: {len(today_matches)}")
        print(f"🇯🇵 J-League matches: {len(jleague_matches)}")
        print(f"⚽ Useful matches: {len(useful_matches)}")
        
        if today_matches:
            print(f"\n🔥 TODAY'S MATCHES FOUND!")
            print("   Recommended action: Use these for analysis")
        elif jleague_matches:
            print(f"\n🇯🇵 J-LEAGUE MATCHES FOUND!")
            print("   Recommended action: Check dates for upcoming matches")
        else:
            print(f"\n💡 NO TARGET MATCHES TODAY")
            print("   Recommended action: Use demo data or wait")
        
    else:
        print("\n❌ No match data retrieved")
        print("💡 Fallback options:")
        print("   1. Manual check on ScoreBat website")
        print("   2. Use existing demo data")
        print("   3. Try other APIs")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Choose best available match")
    print(f"   2. Get betting odds")
    print(f"   3. Update analyzer")
    print(f"   4. Deploy to website")

if __name__ == "__main__":
    main()
