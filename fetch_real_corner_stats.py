#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 REAL CORNER STATISTICS FETCHER
Fetch actual corner stats from API-Sports for Chelsea vs PSG analysis
"""

import requests
import json
import time
from datetime import datetime

class RealCornerStatsFetcher:
    def __init__(self):
        # API-Sports endpoints
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'X-RapidAPI-Host': 'v3.football.api-sports.io',
            'X-RapidAPI-Key': 'YOUR_API_KEY_HERE'  # ต้องใส่ API key จริง
        }
        
    def search_team_id(self, team_name):
        """ค้นหา team ID"""
        try:
            url = f"{self.base_url}/teams"
            params = {'search': team_name}
            
            print(f"🔍 Searching for team: {team_name}")
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['results'] > 0:
                    teams = data['response']
                    for team in teams[:3]:  # แสดง 3 ทีมแรก
                        print(f"   📋 {team['team']['name']} (ID: {team['team']['id']}) - {team['team']['country']}")
                    return teams[0]['team']['id']
                else:
                    print(f"   ❌ No teams found for: {team_name}")
                    return None
            else:
                print(f"   ❌ API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error searching team: {str(e)}")
            return None
    
    def get_team_fixtures(self, team_id, season=2025, last_matches=10):
        """ดึงข้อมูลการแข่งขันล่าสุด"""
        try:
            url = f"{self.base_url}/fixtures"
            params = {
                'team': team_id,
                'season': season,
                'last': last_matches
            }
            
            print(f"🔍 Fetching last {last_matches} fixtures for team ID: {team_id}")
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['results'] > 0:
                    return data['response']
                else:
                    print("   ❌ No fixtures found")
                    return []
            else:
                print(f"   ❌ API Error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Error fetching fixtures: {str(e)}")
            return []
    
    def get_fixture_statistics(self, fixture_id):
        """ดึงสถิติการแข่งขัน รวมเตะมุม"""
        try:
            url = f"{self.base_url}/fixtures/statistics"
            params = {'fixture': fixture_id}
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['results'] > 0:
                    return data['response']
                else:
                    return []
            else:
                print(f"   ❌ Statistics API Error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Error fetching statistics: {str(e)}")
            return []
    
    def extract_corner_stats(self, statistics):
        """แยกข้อมูลเตะมุมจากสถิติ"""
        corner_stats = {}
        
        for team_stat in statistics:
            team_name = team_stat['team']['name']
            corner_stats[team_name] = {}
            
            for stat in team_stat['statistics']:
                if 'corner' in stat['type'].lower():
                    corner_stats[team_name][stat['type']] = stat['value']
        
        return corner_stats
    
    def analyze_team_corners(self, team_name):
        """วิเคราะห์สถิติเตะมุมของทีม"""
        print(f"\n🏆 ANALYZING CORNER STATS FOR: {team_name}")
        print("=" * 60)
        
        # ค้นหา team ID
        team_id = self.search_team_id(team_name)
        if not team_id:
            print(f"❌ Cannot find team: {team_name}")
            return None
        
        time.sleep(1)  # Rate limiting
        
        # ดึงข้อมูลการแข่งขัน
        fixtures = self.get_team_fixtures(team_id)
        if not fixtures:
            print(f"❌ No fixtures found for: {team_name}")
            return None
        
        print(f"✅ Found {len(fixtures)} recent matches")
        
        corner_data = []
        
        for i, fixture in enumerate(fixtures[:5]):  # วิเคราะห์ 5 นัดล่าสุด
            fixture_id = fixture['fixture']['id']
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            date = fixture['fixture']['date']
            
            print(f"\n📅 Match {i+1}: {home_team} vs {away_team}")
            print(f"   🕐 Date: {date}")
            
            time.sleep(1)  # Rate limiting
            
            # ดึงสถิติ
            stats = self.get_fixture_statistics(fixture_id)
            if stats:
                corner_stats = self.extract_corner_stats(stats)
                if corner_stats:
                    print(f"   ⚽ Corner Stats:")
                    for team, corners in corner_stats.items():
                        if corners:
                            for stat_type, value in corners.items():
                                print(f"      {team}: {stat_type} = {value}")
                    
                    corner_data.append({
                        'fixture_id': fixture_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'date': date,
                        'corner_stats': corner_stats
                    })
                else:
                    print("   ❌ No corner statistics available")
            else:
                print("   ❌ No statistics available")
        
        return corner_data
    
    def fetch_chelsea_psg_corners(self):
        """ดึงข้อมูลเตะมุม Chelsea และ PSG"""
        print("🔥" * 60)
        print("🏆 FETCHING REAL CORNER STATISTICS")
        print("📅 Chelsea vs PSG Analysis")
        print("🔥" * 60)
        
        # ตรวจสอบ API Key
        if 'YOUR_API_KEY_HERE' in str(self.headers):
            print("❌ ERROR: API Key not configured!")
            print("📝 Please get API key from: https://www.api-football.com/")
            print("🔧 Update the API key in the script")
            return None
        
        results = {}
        
        # วิเคราะห์ Chelsea
        chelsea_corners = self.analyze_team_corners("Chelsea")
        if chelsea_corners:
            results['chelsea'] = chelsea_corners
        
        time.sleep(2)  # Rate limiting
        
        # วิเคราะห์ PSG
        psg_corners = self.analyze_team_corners("Paris Saint Germain")
        if psg_corners:
            results['psg'] = psg_corners
        
        return results

def main():
    """Main execution"""
    fetcher = RealCornerStatsFetcher()
    
    print("🚀 Starting Real Corner Statistics Fetch...")
    
    # ลองดึงข้อมูลจริง
    try:
        results = fetcher.fetch_chelsea_psg_corners()
        
        if results:
            # บันทึกผลลัพธ์
            with open('/Users/80090/Desktop/Project/untitle/real_corner_stats.json', 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print("\n✅ SUCCESS: Real corner statistics fetched!")
            print("💾 Results saved to: real_corner_stats.json")
        else:
            print("\n❌ FAILED: Could not fetch real corner statistics")
            print("🔧 Possible issues:")
            print("   1. API Key not configured")
            print("   2. API rate limit exceeded")
            print("   3. No recent match data available")
            print("   4. Network connection issues")
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        print("🔧 Please check:")
        print("   1. Internet connection")
        print("   2. API key validity")
        print("   3. API service status")

if __name__ == "__main__":
    main()
