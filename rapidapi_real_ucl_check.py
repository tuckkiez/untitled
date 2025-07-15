#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 RAPIDAPI FOOTBALL - REAL UCL CHECK WITH API KEY
ใช้ API key จริงเพื่อหาแมตช์ UEFA Champions League วันนี้
"""

import requests
import json
from datetime import datetime, timedelta
import time

class RealRapidAPIChecker:
    def __init__(self):
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        # API key ที่คุณให้มา
        self.headers = {
            'x-rapidapi-key': 'f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0',
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
        }
        
    def test_api_with_curl_example(self):
        """ทดสอบ API ด้วยตัวอย่าง curl ที่คุณให้"""
        print("🔍 Testing API with your curl example...")
        
        try:
            url = f"{self.base_url}/fixtures"
            params = {'date': '2021-01-29'}  # ใช้วันที่ในตัวอย่าง
            
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get('response', [])
                print(f"   ✅ API Working! Found {len(fixtures)} matches on 2021-01-29")
                
                # แสดงตัวอย่างแมตช์
                if fixtures:
                    sample_match = fixtures[0]
                    home_team = sample_match.get('teams', {}).get('home', {}).get('name')
                    away_team = sample_match.get('teams', {}).get('away', {}).get('name')
                    league = sample_match.get('league', {}).get('name')
                    print(f"   📋 Sample: {home_team} vs {away_team} ({league})")
                
                return True
            else:
                print(f"   ❌ API Error: {response.status_code}")
                if response.status_code == 429:
                    print("   ⚠️ Rate limit exceeded")
                elif response.status_code == 403:
                    print("   🔑 API key issue")
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
    
    def get_todays_matches(self):
        """ดึงแมตช์วันนี้ทั้งหมด"""
        print(f"\n🔍 Getting all matches for {self.today}...")
        
        try:
            url = f"{self.base_url}/fixtures"
            params = {'date': self.today}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get('response', [])
                print(f"   ✅ Found {len(fixtures)} total matches today")
                
                return fixtures
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return []
    
    def find_ucl_matches(self, fixtures):
        """หาแมตช์ UCL จากรายการแมตช์ทั้งหมด"""
        print(f"\n🔍 Searching for UEFA Champions League matches...")
        
        ucl_matches = []
        all_leagues = set()
        
        for fixture in fixtures:
            league_info = fixture.get('league', {})
            league_name = league_info.get('name', '').lower()
            all_leagues.add(league_info.get('name', ''))
            
            # ค้นหาแมตช์ที่เกี่ยวข้องกับ Champions League
            if any(keyword in league_name for keyword in ['champions league', 'uefa champions', 'ucl']):
                match_info = {
                    'fixture_id': fixture.get('fixture', {}).get('id'),
                    'date': fixture.get('fixture', {}).get('date'),
                    'timestamp': fixture.get('fixture', {}).get('timestamp'),
                    'status': fixture.get('fixture', {}).get('status', {}),
                    'home_team': fixture.get('teams', {}).get('home', {}).get('name'),
                    'away_team': fixture.get('teams', {}).get('away', {}).get('name'),
                    'home_logo': fixture.get('teams', {}).get('home', {}).get('logo'),
                    'away_logo': fixture.get('teams', {}).get('away', {}).get('logo'),
                    'venue': fixture.get('fixture', {}).get('venue', {}),
                    'league': {
                        'id': league_info.get('id'),
                        'name': league_info.get('name'),
                        'country': league_info.get('country'),
                        'logo': league_info.get('logo'),
                        'round': league_info.get('round'),
                        'season': league_info.get('season')
                    }
                }
                ucl_matches.append(match_info)
        
        print(f"   🏆 UCL matches found: {len(ucl_matches)}")
        print(f"   📊 Total leagues today: {len(all_leagues)}")
        
        # แสดงลีกที่มีการแข่งขันวันนี้
        print(f"   📋 Some leagues playing today:")
        for league in sorted(list(all_leagues))[:15]:  # แสดง 15 ลีกแรก
            if league:  # ไม่แสดงชื่อว่าง
                print(f"      • {league}")
        
        return ucl_matches
    
    def get_specific_ucl_league(self):
        """หา UCL league โดยตรง"""
        print(f"\n🔍 Searching for UCL league directly...")
        
        try:
            url = f"{self.base_url}/leagues"
            params = {'search': 'Champions League'}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
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
                            'type': league_info.get('type'),
                            'logo': league_info.get('logo'),
                            'country': league.get('country', {}).get('name'),
                            'seasons': league.get('seasons', [])
                        })
                
                if ucl_leagues:
                    print(f"   ✅ Found {len(ucl_leagues)} UCL competitions:")
                    for ucl in ucl_leagues:
                        print(f"      🏆 {ucl['name']} (ID: {ucl['id']}) - {ucl['country']}")
                        if ucl['seasons']:
                            latest_season = ucl['seasons'][-1]
                            print(f"         📅 Latest season: {latest_season.get('year')}")
                    
                    return ucl_leagues
                else:
                    print("   ❌ No UCL leagues found")
                    return []
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return []
    
    def check_multiple_dates(self):
        """ตรวจสอบหลายวันเพื่อหาแมตช์ UCL"""
        print(f"\n🔍 Checking multiple dates for UCL matches...")
        
        dates_to_check = []
        today = datetime.now()
        
        # เช็ค 7 วันข้างหน้า และ 7 วันข้างหลัง
        for i in range(-7, 8):
            check_date = today + timedelta(days=i)
            dates_to_check.append(check_date.strftime("%Y-%m-%d"))
        
        all_ucl_matches = []
        
        for date in dates_to_check[:5]:  # เช็คแค่ 5 วันแรกเพื่อไม่ให้เกิน rate limit
            try:
                print(f"   📅 Checking {date}...")
                
                url = f"{self.base_url}/fixtures"
                params = {'date': date}
                
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    fixtures = data.get('response', [])
                    
                    # หา UCL matches
                    ucl_matches = self.find_ucl_matches(fixtures)
                    if ucl_matches:
                        print(f"      🏆 Found {len(ucl_matches)} UCL matches on {date}")
                        all_ucl_matches.extend(ucl_matches)
                    else:
                        print(f"      ❌ No UCL matches on {date}")
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"      ❌ Error checking {date}: {str(e)}")
        
        return all_ucl_matches
    
    def comprehensive_ucl_search(self):
        """ค้นหา UCL แบบครอบคลุม"""
        print("🏆" * 70)
        print("🏆 RAPIDAPI FOOTBALL - COMPREHENSIVE UCL SEARCH")
        print(f"📅 Primary Date: {self.today}")
        print("🏆" * 70)
        
        # 1. ทดสอบ API
        if not self.test_api_with_curl_example():
            print("❌ API connection failed")
            return None
        
        time.sleep(2)  # Rate limiting
        
        # 2. ดึงแมตช์วันนี้
        todays_fixtures = self.get_todays_matches()
        
        time.sleep(2)  # Rate limiting
        
        # 3. หา UCL ในแมตช์วันนี้
        todays_ucl = self.find_ucl_matches(todays_fixtures) if todays_fixtures else []
        
        time.sleep(2)  # Rate limiting
        
        # 4. หา UCL league โดยตรง
        ucl_leagues = self.get_specific_ucl_league()
        
        time.sleep(2)  # Rate limiting
        
        # 5. ถ้าไม่เจอวันนี้ ให้เช็คหลายวัน
        all_ucl_matches = []
        if not todays_ucl:
            print(f"\n🔍 No UCL matches today, checking nearby dates...")
            all_ucl_matches = self.check_multiple_dates()
        else:
            all_ucl_matches = todays_ucl
        
        # แสดงผลลัพธ์
        print(f"\n📊 FINAL RESULTS")
        print("=" * 60)
        
        if all_ucl_matches:
            print(f"🎉 FOUND {len(all_ucl_matches)} UEFA CHAMPIONS LEAGUE MATCHES!")
            
            for i, match in enumerate(all_ucl_matches, 1):
                print(f"\n⚽ MATCH {i}:")
                print(f"   🏠 {match['home_team']} vs ✈️ {match['away_team']}")
                
                if match['date']:
                    match_datetime = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
                    bangkok_time = match_datetime + timedelta(hours=7)
                    print(f"   🕐 Time: {bangkok_time.strftime('%Y-%m-%d %H:%M')} (Bangkok)")
                
                print(f"   🏆 Competition: {match['league']['name']}")
                print(f"   📍 Round: {match['league']['round']}")
                print(f"   🏟️ Venue: {match['venue'].get('name', 'TBD')}")
                print(f"   📊 Status: {match['status'].get('long', 'Scheduled')}")
                print(f"   🆔 Fixture ID: {match['fixture_id']}")
        else:
            print("❌ NO UEFA CHAMPIONS LEAGUE MATCHES FOUND")
            print("\n🔍 Possible reasons:")
            print("   1. UCL season hasn't started yet (typically starts September)")
            print("   2. Currently in off-season break")
            print("   3. Matches are on different dates")
            print("   4. Qualifying rounds not yet begun")
            
            print(f"\n📅 UCL 2025-26 Expected Schedule:")
            print("   🗓️ Qualifying: July-August 2025")
            print("   🗓️ Group Stage: September 2025 - December 2025")
            print("   🗓️ Knockout: February 2026 - May 2026")
        
        # บันทึกผลลัพธ์
        results = {
            'api_source': 'RapidAPI Football (Real Key)',
            'search_date': self.today,
            'total_ucl_matches': len(all_ucl_matches),
            'ucl_matches': all_ucl_matches,
            'ucl_leagues_found': ucl_leagues,
            'timestamp': datetime.now().isoformat()
        }
        
        with open('/Users/80090/Desktop/Project/untitle/real_rapidapi_ucl_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Results saved to: real_rapidapi_ucl_results.json")
        
        return results

def main():
    """Main execution"""
    checker = RealRapidAPIChecker()
    
    print("🚀 Starting Real RapidAPI UCL Search...")
    
    try:
        results = checker.comprehensive_ucl_search()
        
        if results and results['total_ucl_matches'] > 0:
            print(f"\n✅ SUCCESS: Found {results['total_ucl_matches']} UCL matches!")
        else:
            print(f"\n❌ NO UCL MATCHES: No matches found in search period")
            print("🔧 Try checking UEFA.com for official schedule")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
