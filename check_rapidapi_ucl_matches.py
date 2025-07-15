#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 RAPIDAPI FOOTBALL - UEFA CHAMPIONS LEAGUE CHECKER
ตรวจสอบแมตช์ UCL จริงจาก RapidAPI Football API
"""

import requests
import json
from datetime import datetime, timedelta
import time

class RapidAPIFootballChecker:
    def __init__(self):
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        # RapidAPI headers (ต้องใส่ API key จริง)
        self.headers = {
            'X-RapidAPI-Key': 'YOUR_RAPIDAPI_KEY_HERE',  # ต้องใส่ key จริง
            'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
        }
        
    def test_api_connection(self):
        """ทดสอบการเชื่อมต่อ API"""
        print("🔍 Testing RapidAPI Football connection...")
        
        try:
            # ทดสอบด้วย endpoint ง่ายๆ
            url = f"{self.base_url}/status"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ API Connection successful!")
                print(f"   📊 API Status: {data}")
                return True
            elif response.status_code == 403:
                print("   🔑 API Key required or invalid")
                return False
            else:
                print(f"   ❌ API Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Connection error: {str(e)}")
            return False
    
    def get_ucl_league_id(self):
        """หา League ID ของ UEFA Champions League"""
        print("\n🔍 Finding UEFA Champions League ID...")
        
        try:
            url = f"{self.base_url}/leagues"
            params = {
                'search': 'Champions League',
                'current': 'true'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                leagues = data.get('response', [])
                
                ucl_leagues = []
                for league in leagues:
                    league_info = league.get('league', {})
                    if 'champions league' in league_info.get('name', '').lower():
                        ucl_leagues.append({
                            'id': league_info.get('id'),
                            'name': league_info.get('name'),
                            'country': league.get('country', {}).get('name'),
                            'season': league.get('seasons', [{}])[-1] if league.get('seasons') else {}
                        })
                
                if ucl_leagues:
                    print(f"   ✅ Found {len(ucl_leagues)} Champions League competitions:")
                    for ucl in ucl_leagues:
                        print(f"      🏆 {ucl['name']} (ID: {ucl['id']}) - {ucl['country']}")
                    
                    return ucl_leagues[0]['id']  # Return first UCL ID
                else:
                    print("   ❌ No Champions League found")
                    return None
            else:
                print(f"   ❌ Failed to get leagues: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error finding UCL ID: {str(e)}")
            return None
    
    def get_ucl_matches_today(self, league_id):
        """ดึงแมตช์ UCL วันนี้"""
        print(f"\n🔍 Getting UCL matches for {self.today}...")
        
        try:
            url = f"{self.base_url}/fixtures"
            params = {
                'league': league_id,
                'date': self.today,
                'timezone': 'Asia/Bangkok'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get('response', [])
                
                if fixtures:
                    print(f"   ✅ Found {len(fixtures)} UCL matches today!")
                    
                    matches = []
                    for fixture in fixtures:
                        match_info = {
                            'id': fixture.get('fixture', {}).get('id'),
                            'date': fixture.get('fixture', {}).get('date'),
                            'status': fixture.get('fixture', {}).get('status', {}).get('long'),
                            'home_team': fixture.get('teams', {}).get('home', {}).get('name'),
                            'away_team': fixture.get('teams', {}).get('away', {}).get('away'),
                            'venue': fixture.get('fixture', {}).get('venue', {}).get('name'),
                            'round': fixture.get('league', {}).get('round'),
                            'league_name': fixture.get('league', {}).get('name')
                        }
                        matches.append(match_info)
                    
                    return matches
                else:
                    print("   ❌ No UCL matches found for today")
                    return []
            else:
                print(f"   ❌ Failed to get fixtures: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Error getting matches: {str(e)}")
            return []
    
    def get_all_leagues_today(self):
        """ดึงการแข่งขันทั้งหมดวันนี้เพื่อหา UCL"""
        print(f"\n🔍 Getting all matches today to find UCL...")
        
        try:
            url = f"{self.base_url}/fixtures"
            params = {
                'date': self.today,
                'timezone': 'Asia/Bangkok'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get('response', [])
                
                print(f"   📊 Total matches today: {len(fixtures)}")
                
                # หาแมตช์ที่เกี่ยวข้องกับ Champions League
                ucl_matches = []
                all_leagues = set()
                
                for fixture in fixtures:
                    league_name = fixture.get('league', {}).get('name', '').lower()
                    all_leagues.add(fixture.get('league', {}).get('name', ''))
                    
                    if 'champions league' in league_name or 'uefa' in league_name:
                        match_info = {
                            'id': fixture.get('fixture', {}).get('id'),
                            'date': fixture.get('fixture', {}).get('date'),
                            'status': fixture.get('fixture', {}).get('status', {}).get('long'),
                            'home_team': fixture.get('teams', {}).get('home', {}).get('name'),
                            'away_team': fixture.get('teams', {}).get('away', {}).get('name'),
                            'venue': fixture.get('fixture', {}).get('venue', {}).get('name'),
                            'round': fixture.get('league', {}).get('round'),
                            'league_name': fixture.get('league', {}).get('name')
                        }
                        ucl_matches.append(match_info)
                
                print(f"   🏆 UCL matches found: {len(ucl_matches)}")
                
                # แสดงลีกทั้งหมดที่มีวันนี้ (สำหรับ debug)
                print(f"   📋 Leagues playing today: {len(all_leagues)}")
                for league in sorted(list(all_leagues))[:10]:  # แสดง 10 ลีกแรก
                    print(f"      • {league}")
                
                return ucl_matches
            else:
                print(f"   ❌ Failed to get all fixtures: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Error getting all matches: {str(e)}")
            return []
    
    def comprehensive_ucl_check(self):
        """ตรวจสอบ UCL แบบครบถ้วน"""
        print("🏆" * 70)
        print("🏆 RAPIDAPI FOOTBALL - UEFA CHAMPIONS LEAGUE CHECK")
        print(f"📅 Date: {self.today}")
        print("🏆" * 70)
        
        # ตรวจสอบ API key
        if 'YOUR_RAPIDAPI_KEY_HERE' in str(self.headers):
            print("❌ ERROR: RapidAPI Key not configured!")
            print("🔧 Steps to fix:")
            print("   1. Go to https://rapidapi.com/api-sports/api/api-football")
            print("   2. Subscribe to get API key")
            print("   3. Replace 'YOUR_RAPIDAPI_KEY_HERE' with your actual key")
            return None
        
        # 1. ทดสอบการเชื่อมต่อ
        if not self.test_api_connection():
            print("❌ Cannot connect to RapidAPI Football")
            return None
        
        time.sleep(1)  # Rate limiting
        
        # 2. หา UCL League ID
        ucl_id = self.get_ucl_league_id()
        
        time.sleep(1)  # Rate limiting
        
        ucl_matches = []
        
        # 3. ถ้าหา UCL ID ได้ ให้ดึงแมตช์
        if ucl_id:
            ucl_matches = self.get_ucl_matches_today(ucl_id)
        
        time.sleep(1)  # Rate limiting
        
        # 4. ถ้าไม่เจอ ให้ค้นหาจากการแข่งขันทั้งหมด
        if not ucl_matches:
            ucl_matches = self.get_all_leagues_today()
        
        # แสดงผลลัพธ์
        print(f"\n📊 FINAL RESULTS")
        print("=" * 50)
        
        if ucl_matches:
            print(f"🎉 FOUND {len(ucl_matches)} UEFA CHAMPIONS LEAGUE MATCHES!")
            
            for i, match in enumerate(ucl_matches, 1):
                print(f"\n⚽ MATCH {i}:")
                print(f"   🏠 {match['home_team']} vs ✈️ {match['away_team']}")
                
                if match['date']:
                    match_time = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
                    bangkok_time = match_time + timedelta(hours=7)  # Convert to Bangkok time
                    print(f"   🕐 Time: {bangkok_time.strftime('%H:%M')} (Bangkok)")
                
                print(f"   🏆 Competition: {match['league_name']}")
                print(f"   📍 Round: {match['round']}")
                print(f"   🏟️ Venue: {match['venue']}")
                print(f"   📊 Status: {match['status']}")
        else:
            print("❌ NO UEFA CHAMPIONS LEAGUE MATCHES FOUND TODAY")
            print("\n🔍 This could mean:")
            print("   1. No UCL matches scheduled for today")
            print("   2. UCL season hasn't started yet")
            print("   3. API doesn't have current UCL data")
            print("   4. Need to check different date range")
        
        # บันทึกผลลัพธ์
        results = {
            'api_source': 'RapidAPI Football',
            'check_date': self.today,
            'total_matches': len(ucl_matches),
            'matches': ucl_matches,
            'timestamp': datetime.now().isoformat()
        }
        
        with open('/Users/80090/Desktop/Project/untitle/rapidapi_ucl_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Results saved to: rapidapi_ucl_results.json")
        
        return results

def main():
    """Main execution"""
    checker = RapidAPIFootballChecker()
    
    print("🚀 Starting RapidAPI Football UCL Check...")
    
    try:
        results = checker.comprehensive_ucl_check()
        
        if results and results['total_matches'] > 0:
            print(f"\n✅ SUCCESS: Found {results['total_matches']} UCL matches!")
        else:
            print(f"\n❌ NO MATCHES: No UCL matches found for today")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("🔧 Please check API key and try again")

if __name__ == "__main__":
    main()
