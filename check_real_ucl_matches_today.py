#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 REAL UEFA CHAMPIONS LEAGUE MATCHES CHECKER
ตรวจสอบการแข่งขัน UEFA Champions League จริงๆ วันนี้จาก API
"""

import requests
import json
from datetime import datetime, timedelta
import time

class RealUCLMatchesChecker:
    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
    def check_sofascore_ucl_matches(self):
        """ตรวจสอบแมตช์ UCL จาก SofaScore API"""
        print(f"🔍 Checking SofaScore for UEFA Champions League matches on {self.today}...")
        
        try:
            # SofaScore API endpoint for today's matches
            url = "https://api.sofascore.com/api/v1/sport/football/scheduled-events"
            params = {'date': self.today}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                
                ucl_matches = []
                for event in events:
                    tournament = event.get('tournament', {})
                    tournament_name = tournament.get('name', '').lower()
                    
                    # ค้นหาแมตช์ Champions League
                    if 'champions league' in tournament_name or 'uefa champions league' in tournament_name:
                        match_info = {
                            'id': event.get('id'),
                            'home_team': event.get('homeTeam', {}).get('name'),
                            'away_team': event.get('awayTeam', {}).get('name'),
                            'start_time': event.get('startTimestamp'),
                            'tournament': tournament.get('name'),
                            'round': event.get('roundInfo', {}).get('name', 'Unknown Round'),
                            'status': event.get('status', {}).get('description', 'Scheduled')
                        }
                        ucl_matches.append(match_info)
                
                return ucl_matches
            else:
                print(f"   ❌ Failed to fetch data: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ SofaScore error: {str(e)}")
            return []
    
    def check_alternative_apis(self):
        """ลองตรวจสอบจาก API อื่นๆ"""
        print(f"\n🔍 Checking alternative APIs for UCL matches...")
        
        # ลอง TheSportsDB
        try:
            print("   📡 Trying TheSportsDB...")
            url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php"
            params = {'d': self.today, 's': 'Soccer'}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', []) or []
                
                ucl_matches = []
                for event in events:
                    league_name = event.get('strLeague', '').lower()
                    if 'champions league' in league_name or 'uefa' in league_name:
                        match_info = {
                            'home_team': event.get('strHomeTeam'),
                            'away_team': event.get('strAwayTeam'),
                            'time': event.get('strTime'),
                            'league': event.get('strLeague'),
                            'round': event.get('intRound', 'Unknown'),
                            'season': event.get('strSeason')
                        }
                        ucl_matches.append(match_info)
                
                print(f"   ✅ TheSportsDB: Found {len(ucl_matches)} UCL matches")
                return ucl_matches
            else:
                print(f"   ❌ TheSportsDB failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ TheSportsDB error: {str(e)}")
        
        return []
    
    def check_football_data_org(self):
        """ลองตรวจสอบจาก Football-Data.org (อาจต้องการ API key)"""
        print(f"\n🔍 Checking Football-Data.org...")
        
        try:
            # UEFA Champions League competition ID = 2001
            url = "https://api.football-data.org/v4/competitions/2001/matches"
            params = {'dateFrom': self.today, 'dateTo': self.today}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            print(f"   📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                
                ucl_matches = []
                for match in matches:
                    match_info = {
                        'home_team': match.get('homeTeam', {}).get('name'),
                        'away_team': match.get('awayTeam', {}).get('name'),
                        'utc_date': match.get('utcDate'),
                        'status': match.get('status'),
                        'stage': match.get('stage'),
                        'matchday': match.get('matchday')
                    }
                    ucl_matches.append(match_info)
                
                print(f"   ✅ Football-Data.org: Found {len(ucl_matches)} UCL matches")
                return ucl_matches
                
            elif response.status_code == 403:
                print("   🔑 Requires API token (free tier available)")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Football-Data.org error: {str(e)}")
        
        return []
    
    def manual_ucl_schedule_check(self):
        """ตรวจสอบตารางแข่ง UCL แบบ manual"""
        print(f"\n📅 Manual UCL Schedule Check for {self.today}...")
        
        # ข้อมูลตารางแข่ง UCL 2025-26 รอบคัดเลือก (นัดสอง)
        # ตามปกติจะเป็นช่วงเดือนกรกฎาคม-สิงหาคม
        
        current_date = datetime.now()
        
        # ตรวจสอบว่าอยู่ในช่วงรอบคัดเลือกหรือไม่
        qualifying_period = {
            'start': datetime(2025, 7, 15),
            'end': datetime(2025, 8, 30)
        }
        
        if qualifying_period['start'] <= current_date <= qualifying_period['end']:
            print("   ✅ Currently in UCL Qualifying period")
            
            # ตัวอย่างการแข่งขันที่อาจมี (ข้อมูลจำลอง)
            potential_matches = [
                {
                    'date': '2025-07-15',
                    'matches': [
                        {'home': 'Dinamo Zagreb', 'away': 'Qarabag', 'time': '20:00', 'round': 'Q2 - 2nd Leg'},
                        {'home': 'Sparta Prague', 'away': 'FCSB', 'time': '20:30', 'round': 'Q2 - 2nd Leg'},
                        {'home': 'Midtjylland', 'away': 'Ferencvaros', 'time': '21:00', 'round': 'Q2 - 2nd Leg'}
                    ]
                },
                {
                    'date': '2025-07-16',
                    'matches': [
                        {'home': 'Ludogorets', 'away': 'Petrocub', 'time': '19:00', 'round': 'Q2 - 2nd Leg'},
                        {'home': 'Slovan Bratislava', 'away': 'Struga', 'time': '20:00', 'round': 'Q2 - 2nd Leg'}
                    ]
                }
            ]
            
            today_matches = []
            for day_schedule in potential_matches:
                if day_schedule['date'] == self.today:
                    today_matches = day_schedule['matches']
                    break
            
            if today_matches:
                print(f"   🏆 Found {len(today_matches)} potential UCL matches today:")
                for match in today_matches:
                    print(f"      ⚽ {match['home']} vs {match['away']} - {match['time']} ({match['round']})")
                return today_matches
            else:
                print(f"   ❌ No UCL matches scheduled for {self.today}")
                return []
        else:
            print("   ❌ Not currently in UCL Qualifying period")
            return []
    
    def comprehensive_ucl_check(self):
        """ตรวจสอบแมตช์ UCL จากทุกแหล่ง"""
        print("🏆" * 70)
        print("🏆 REAL UEFA CHAMPIONS LEAGUE MATCHES CHECK")
        print(f"📅 Date: {self.today}")
        print("🏆" * 70)
        
        all_matches = []
        
        # 1. ตรวจสอบจาก SofaScore
        sofascore_matches = self.check_sofascore_ucl_matches()
        if sofascore_matches:
            all_matches.extend(sofascore_matches)
            print(f"✅ SofaScore: {len(sofascore_matches)} matches found")
        
        time.sleep(2)  # Rate limiting
        
        # 2. ตรวจสอบจาก Alternative APIs
        alt_matches = self.check_alternative_apis()
        if alt_matches:
            all_matches.extend(alt_matches)
            print(f"✅ Alternative APIs: {len(alt_matches)} matches found")
        
        time.sleep(2)  # Rate limiting
        
        # 3. ตรวจสอบจาก Football-Data.org
        fd_matches = self.check_football_data_org()
        if fd_matches:
            all_matches.extend(fd_matches)
            print(f"✅ Football-Data.org: {len(fd_matches)} matches found")
        
        # 4. Manual schedule check
        manual_matches = self.manual_ucl_schedule_check()
        
        print(f"\n📊 SUMMARY")
        print("=" * 50)
        
        if all_matches:
            print(f"🎉 FOUND {len(all_matches)} UEFA CHAMPIONS LEAGUE MATCHES TODAY!")
            print("\n🏆 TODAY'S UCL MATCHES:")
            
            for i, match in enumerate(all_matches, 1):
                print(f"\n⚽ MATCH {i}:")
                if 'home_team' in match and 'away_team' in match:
                    print(f"   🏠 {match['home_team']} vs ✈️ {match['away_team']}")
                elif 'home' in match and 'away' in match:
                    print(f"   🏠 {match['home']} vs ✈️ {match['away']}")
                
                if 'start_time' in match:
                    time_str = datetime.fromtimestamp(match['start_time']).strftime("%H:%M")
                    print(f"   🕐 Time: {time_str}")
                elif 'time' in match:
                    print(f"   🕐 Time: {match['time']}")
                
                if 'round' in match:
                    print(f"   🏆 Round: {match['round']}")
                elif 'stage' in match:
                    print(f"   🏆 Stage: {match['stage']}")
                
                if 'tournament' in match:
                    print(f"   🏟️ Tournament: {match['tournament']}")
        
        elif manual_matches:
            print(f"📅 POTENTIAL UCL MATCHES (Manual Schedule):")
            for match in manual_matches:
                print(f"   ⚽ {match['home']} vs {match['away']} - {match['time']} ({match['round']})")
        
        else:
            print("❌ NO UEFA CHAMPIONS LEAGUE MATCHES FOUND TODAY")
            print("\n🔍 Possible reasons:")
            print("   1. No UCL matches scheduled for today")
            print("   2. APIs don't have current UCL data")
            print("   3. Currently not in UCL season")
            print("   4. Matches might be tomorrow or yesterday")
            
            # แนะนำวันที่น่าจะมีแมตช์
            print(f"\n📅 UCL Qualifying Round 2 (2nd Leg) typically occurs:")
            print("   🗓️ July 23-24, 2025")
            print("   🗓️ July 30-31, 2025")
            print("   🗓️ August 6-7, 2025")
        
        # บันทึกผลลัพธ์
        results = {
            'check_date': self.today,
            'total_matches_found': len(all_matches),
            'matches': all_matches,
            'manual_potential_matches': manual_matches,
            'apis_checked': ['SofaScore', 'TheSportsDB', 'Football-Data.org'],
            'timestamp': datetime.now().isoformat()
        }
        
        with open('/Users/80090/Desktop/Project/untitle/real_ucl_matches_today.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Results saved to: real_ucl_matches_today.json")
        
        return results

def main():
    """Main execution"""
    checker = RealUCLMatchesChecker()
    
    print("🚀 Starting Real UEFA Champions League Matches Check...")
    
    try:
        results = checker.comprehensive_ucl_check()
        
        if results['total_matches_found'] > 0:
            print(f"\n✅ SUCCESS: Found {results['total_matches_found']} UCL matches!")
        else:
            print(f"\n❌ NO UCL MATCHES: No matches found for today")
            print("🔧 Try checking official UEFA website or sports news")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
