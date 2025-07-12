#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ScoreBat J-League 2 Scraper
ดึงข้อมูลการแข่งขัน J-League 2 จาก ScoreBat
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import re

def print_header():
    print("🔍 ScoreBat J-League 2 Scraper")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

def scrape_scorebat():
    """ดึงข้อมูลจาก ScoreBat"""
    print("\n🌐 Scraping ScoreBat.com...")
    
    try:
        url = "https://www.scorebat.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"   📡 Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📄 Content length: {len(response.text)} chars")
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for J-League 2 section
            print("\n🔍 Looking for J-League 2...")
            
            # Find all spans with text containing "J-League"
            jleague_spans = soup.find_all('span', string=re.compile(r'J-League', re.IGNORECASE))
            
            if jleague_spans:
                print(f"   ✅ Found {len(jleague_spans)} J-League mentions")
                for i, span in enumerate(jleague_spans):
                    print(f"      {i+1}. {span.get_text()}")
                    
                    # Look for J-League 2 specifically
                    if '2' in span.get_text():
                        print(f"         🎯 Found J-League 2!")
                        return find_matches_near_span(span)
            else:
                print("   ❌ No J-League spans found")
                
                # Try alternative search
                print("   🔍 Trying alternative search...")
                return search_alternative_patterns(soup)
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Scraping error: {e}")
    
    return []

def find_matches_near_span(span):
    """หาการแข่งขันใกล้ๆ กับ span ที่พบ"""
    print("   🔍 Looking for matches near J-League 2 span...")
    
    matches = []
    
    try:
        # Look for parent containers
        parent = span.parent
        while parent and len(matches) == 0:
            # Look for match containers
            match_divs = parent.find_all('div', class_=re.compile(r'match|game|fixture', re.IGNORECASE))
            
            for div in match_divs[:10]:  # Check first 10
                match_info = extract_match_info(div)
                if match_info:
                    matches.append(match_info)
            
            parent = parent.parent
            
        if matches:
            print(f"      ✅ Found {len(matches)} matches")
            for match in matches:
                print(f"         ⚽ {match['home']} vs {match['away']} ({match['time']})")
        else:
            print("      ❌ No matches found near span")
            
    except Exception as e:
        print(f"      ❌ Error finding matches: {e}")
    
    return matches

def search_alternative_patterns(soup):
    """ค้นหาด้วยรูปแบบอื่น"""
    print("   🔍 Alternative search patterns...")
    
    matches = []
    
    try:
        # Pattern 1: Look for any text containing team names
        japanese_teams = [
            'FC Tokyo', 'Yokohama', 'Kashima', 'Urawa', 'Gamba', 'Cerezo',
            'Vissel', 'Sanfrecce', 'Kawasaki', 'Nagoya', 'Sagan', 'Shonan',
            'Ventforet', 'Montedio', 'Machida', 'Roasso', 'Fagiano', 'Tokushima'
        ]
        
        for team in japanese_teams[:5]:  # Check first 5 teams
            team_mentions = soup.find_all(string=re.compile(team, re.IGNORECASE))
            if team_mentions:
                print(f"      🎯 Found {team}: {len(team_mentions)} mentions")
                
                # Try to extract match info from context
                for mention in team_mentions[:2]:
                    parent = mention.parent if hasattr(mention, 'parent') else None
                    if parent:
                        match_info = extract_match_from_context(parent, team)
                        if match_info:
                            matches.append(match_info)
        
        # Pattern 2: Look for score patterns (0-0, 1-1, etc.)
        score_pattern = re.compile(r'\d+\s*[-:]\s*\d+')
        score_elements = soup.find_all(string=score_pattern)
        
        if score_elements:
            print(f"      📊 Found {len(score_elements)} score patterns")
            for score in score_elements[:3]:
                print(f"         📈 Score: {score.strip()}")
        
    except Exception as e:
        print(f"      ❌ Alternative search error: {e}")
    
    return matches

def extract_match_info(div):
    """แยกข้อมูลการแข่งขันจาก div"""
    try:
        text = div.get_text().strip()
        
        # Look for vs pattern
        if ' vs ' in text or ' v ' in text:
            parts = re.split(r'\s+vs?\s+', text, flags=re.IGNORECASE)
            if len(parts) >= 2:
                return {
                    'home': parts[0].strip(),
                    'away': parts[1].strip(),
                    'time': 'TBD',
                    'source': 'ScoreBat'
                }
    except:
        pass
    
    return None

def extract_match_from_context(element, team_name):
    """แยกข้อมูลการแข่งขันจาก context"""
    try:
        text = element.get_text().strip()
        
        # Simple pattern matching
        if 'vs' in text.lower() and team_name.lower() in text.lower():
            return {
                'home': 'Team A',
                'away': 'Team B', 
                'time': 'TBD',
                'context': text[:100],
                'source': 'ScoreBat Context'
            }
    except:
        pass
    
    return None

def check_scorebat_api():
    """ตรวจสอบว่า ScoreBat มี API หรือไม่"""
    print("\n🔌 Checking for ScoreBat API...")
    
    try:
        # Try common API endpoints
        api_urls = [
            "https://www.scorebat.com/api/",
            "https://api.scorebat.com/",
            "https://www.scorebat.com/video-api/",
        ]
        
        for url in api_urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ Found API: {url}")
                    print(f"      📄 Response: {response.text[:200]}...")
                    return True
                else:
                    print(f"   ❌ {url}: {response.status_code}")
            except:
                print(f"   ❌ {url}: Connection failed")
        
        print("   ❌ No API endpoints found")
        return False
        
    except Exception as e:
        print(f"   ❌ API check error: {e}")
        return False

def suggest_alternatives():
    """แนะนำทางเลือกอื่น"""
    print("\n💡 Alternative Approaches:")
    
    alternatives = [
        {
            'method': 'Direct J-League API',
            'url': 'https://www.jleague.jp/',
            'note': 'Official source, might have API'
        },
        {
            'method': 'FlashScore Scraping',
            'url': 'https://www.flashscore.com/',
            'note': 'Rich match data'
        },
        {
            'method': 'SofaScore API',
            'url': 'https://www.sofascore.com/',
            'note': 'Has mobile API'
        },
        {
            'method': 'ESPN Soccer API',
            'url': 'https://www.espn.com/soccer/',
            'note': 'Free tier available'
        }
    ]
    
    for alt in alternatives:
        print(f"   🔧 {alt['method']}")
        print(f"      🔗 {alt['url']}")
        print(f"      💡 {alt['note']}")

def main():
    print_header()
    
    # Try scraping ScoreBat
    matches = scrape_scorebat()
    
    # Check for API
    has_api = check_scorebat_api()
    
    # Show results
    print("\n" + "=" * 50)
    print("📊 RESULTS")
    print("=" * 50)
    
    if matches:
        print(f"✅ Found {len(matches)} matches:")
        for i, match in enumerate(matches, 1):
            print(f"   {i}. {match['home']} vs {match['away']}")
            print(f"      ⏰ {match['time']} | 📡 {match['source']}")
    else:
        print("❌ No matches found from scraping")
    
    if not has_api:
        print("❌ No direct API access found")
    
    # Show alternatives
    suggest_alternatives()
    
    print("\n🚀 Next Steps:")
    print("   1. Try manual check on ScoreBat website")
    print("   2. Use alternative data sources")
    print("   3. Focus on confirmed matches")
    print("   4. Update system with real data")

if __name__ == "__main__":
    main()
