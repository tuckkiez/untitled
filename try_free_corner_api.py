#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 TRY FREE CORNER STATISTICS APIs
Attempt to fetch real corner data from free football APIs
"""

import requests
import json
import time
from datetime import datetime

class FreeCornerAPITester:
    def __init__(self):
        self.apis_to_try = [
            {
                'name': 'Football-Data.org',
                'base_url': 'https://api.football-data.org/v4',
                'headers': {'X-Auth-Token': 'free_tier_token'},
                'description': 'Free tier available'
            },
            {
                'name': 'TheSportsDB',
                'base_url': 'https://www.thesportsdb.com/api/v1/json',
                'headers': {},
                'description': 'Completely free'
            },
            {
                'name': 'API-Football (Free)',
                'base_url': 'https://v3.football.api-sports.io',
                'headers': {},
                'description': 'Free tier with limits'
            }
        ]
    
    def test_football_data_org(self):
        """ทดสอบ Football-Data.org API"""
        print("\n🔍 Testing Football-Data.org API...")
        
        try:
            # ลองดึงข้อมูล Premier League
            url = "https://api.football-data.org/v4/competitions/PL/matches"
            params = {'status': 'FINISHED', 'limit': 5}
            
            response = requests.get(url, params=params, timeout=10)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Found {len(data.get('matches', []))} matches")
                
                # ตรวจสอบว่ามีข้อมูลสถิติไหม
                for match in data.get('matches', [])[:2]:
                    print(f"   📅 {match['homeTeam']['name']} vs {match['awayTeam']['name']}")
                    if 'statistics' in match:
                        print("   📊 Statistics available!")
                    else:
                        print("   ❌ No detailed statistics")
                
                return True
            else:
                print(f"   ❌ Failed: {response.status_code}")
                if response.status_code == 403:
                    print("   🔑 Requires API token")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
    
    def test_thesportsdb(self):
        """ทดสอบ TheSportsDB API"""
        print("\n🔍 Testing TheSportsDB API...")
        
        try:
            # ค้นหา Chelsea
            url = "https://www.thesportsdb.com/api/v1/json/3/searchteams.php"
            params = {'t': 'Chelsea'}
            
            response = requests.get(url, params=params, timeout=10)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                teams = data.get('teams', [])
                
                if teams:
                    chelsea = teams[0]
                    print(f"   ✅ Found: {chelsea['strTeam']} (ID: {chelsea['idTeam']})")
                    
                    # ลองดึงข้อมูลการแข่งขันล่าสุด
                    matches_url = f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php"
                    matches_params = {'id': chelsea['idTeam']}
                    
                    matches_response = requests.get(matches_url, params=matches_params, timeout=10)
                    if matches_response.status_code == 200:
                        matches_data = matches_response.json()
                        events = matches_data.get('results', [])
                        
                        print(f"   📅 Found {len(events)} recent matches")
                        
                        # ตรวจสอบข้อมูลสถิติ
                        for event in events[:2]:
                            print(f"   ⚽ {event.get('strHomeTeam')} vs {event.get('strAwayTeam')}")
                            
                            # ตรวจสอบว่ามีข้อมูลเตะมุมไหม
                            corner_fields = ['intHomeCorners', 'intAwayCorners', 'strHomeCorners', 'strAwayCorners']
                            corner_found = False
                            
                            for field in corner_fields:
                                if field in event and event[field]:
                                    print(f"   🎯 Corner data found: {field} = {event[field]}")
                                    corner_found = True
                            
                            if not corner_found:
                                print("   ❌ No corner statistics")
                        
                        return len(events) > 0
                    else:
                        print("   ❌ Cannot fetch match data")
                        return False
                else:
                    print("   ❌ Team not found")
                    return False
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
    
    def test_free_apis(self):
        """ทดสอบ API ฟรีทั้งหมด"""
        print("🔥" * 60)
        print("🔍 TESTING FREE FOOTBALL APIs FOR CORNER STATISTICS")
        print("🎯 Target: Chelsea vs PSG corner data")
        print("🔥" * 60)
        
        results = {}
        
        # ทดสอบ Football-Data.org
        results['football_data_org'] = self.test_football_data_org()
        time.sleep(2)
        
        # ทดสอบ TheSportsDB
        results['thesportsdb'] = self.test_thesportsdb()
        time.sleep(2)
        
        print("\n📊 API TEST RESULTS")
        print("=" * 40)
        
        working_apis = []
        for api_name, status in results.items():
            status_icon = "✅" if status else "❌"
            print(f"{status_icon} {api_name}: {'Working' if status else 'Failed'}")
            if status:
                working_apis.append(api_name)
        
        if working_apis:
            print(f"\n🎉 SUCCESS: {len(working_apis)} API(s) working!")
            print("📝 Available APIs:", ", ".join(working_apis))
        else:
            print("\n❌ FAILED: No free APIs with corner statistics found")
            print("🔧 Recommendations:")
            print("   1. Get API key from api-football.com (free tier available)")
            print("   2. Use paid API services for detailed statistics")
            print("   3. Manual data collection from sports websites")
        
        return working_apis
    
    def manual_corner_search(self):
        """แนะนำการหาข้อมูลเตะมุมแบบ manual"""
        print("\n🔍 MANUAL CORNER DATA SOURCES")
        print("=" * 50)
        print("📊 Recommended websites for corner statistics:")
        print("   1. 🌐 FlashScore.com - Detailed match statistics")
        print("   2. 🌐 SofaScore.com - Live and historical stats")
        print("   3. 🌐 ESPN.com - Match center with statistics")
        print("   4. 🌐 BBC Sport - Match reports with stats")
        print("   5. 🌐 UEFA.com - Official European competition stats")
        
        print("\n📋 What to look for:")
        print("   🎯 Corner kicks per match")
        print("   🎯 Corner kicks per half")
        print("   🎯 Corner conversion rate")
        print("   🎯 Average corners home vs away")
        
        print("\n🔧 Alternative approach:")
        print("   📊 Use historical averages from league statistics")
        print("   📊 Team-specific corner tendencies")
        print("   📊 Head-to-head corner patterns")

def main():
    """Main execution"""
    tester = FreeCornerAPITester()
    
    print("🚀 Starting Free API Corner Statistics Search...")
    
    # ทดสอบ API ฟรี
    working_apis = tester.test_free_apis()
    
    if not working_apis:
        print("\n" + "❌" * 30)
        print("❌ ไม่เจอข้อมูลเตะมุมจาก API ฟรี")
        print("❌" * 30)
        
        # แนะนำทางเลือก
        tester.manual_corner_search()
        
        print("\n💡 CONCLUSION:")
        print("   🔍 Real corner statistics require paid API access")
        print("   📊 Free APIs don't provide detailed match statistics")
        print("   🎯 Manual data collection recommended for accurate corner analysis")
    else:
        print(f"\n✅ Found {len(working_apis)} working API(s)")
        print("🔧 Further development needed to extract corner statistics")

if __name__ == "__main__":
    main()
