#!/usr/bin/env python3
"""
🏆 Test Corners Data with 2023 Season
=====================================
Test with completed 2022-2023 Premier League season
"""

import requests
import json
import pandas as pd

class CornersTest2023:
    def __init__(self):
        self.api_key = "9936a2866ebc7271a809ff2ab164b032"
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
    
    def test_multiple_seasons(self):
        """Test multiple seasons to find available data"""
        print("🔍 Testing Multiple Seasons")
        print("=" * 30)
        
        seasons = ['2023', '2022', '2021']
        
        for season in seasons:
            print(f"\n📅 Testing Season {season}:")
            
            url = f"{self.base_url}/fixtures"
            params = {
                'league': '39',  # Premier League
                'season': season,
                'status': 'FT'
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    fixtures = data.get('response', [])
                    print(f"   ✅ Found {len(fixtures)} finished matches")
                    
                    if len(fixtures) > 0:
                        return season, fixtures[:10]  # Return first 10 matches
                else:
                    print(f"   ❌ Error: {response.text[:100]}")
                    
            except Exception as e:
                print(f"   ❌ Exception: {e}")
        
        return None, []
    
    def test_specific_fixture(self, fixture_id="867946"):
        """Test with a specific known fixture ID"""
        print(f"\n🧪 Testing Specific Fixture: {fixture_id}")
        print("=" * 40)
        
        url = f"{self.base_url}/fixtures/statistics"
        params = {'fixture': fixture_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Statistics API working!")
                
                corners_found = False
                
                for team_stats in data.get('response', []):
                    team_name = team_stats.get('team', {}).get('name', 'Unknown')
                    print(f"\n📈 Team: {team_name}")
                    
                    for stat in team_stats.get('statistics', []):
                        stat_type = stat.get('type', '')
                        stat_value = stat.get('value', '')
                        
                        if 'corner' in stat_type.lower():
                            print(f"🏆 CORNERS: {stat_type} = {stat_value}")
                            corners_found = True
                        
                        # Show first few stats
                        print(f"   {stat_type}: {stat_value}")
                
                return corners_found, data
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False, None
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False, None
    
    def test_leagues_with_corners(self):
        """Test different leagues to find corners data"""
        print("\n🌍 Testing Different Leagues")
        print("=" * 35)
        
        leagues = {
            '39': 'Premier League',
            '140': 'La Liga', 
            '78': 'Bundesliga',
            '135': 'Serie A',
            '61': 'Ligue 1'
        }
        
        for league_id, league_name in leagues.items():
            print(f"\n🏆 Testing {league_name} (ID: {league_id}):")
            
            # Get recent fixtures
            url = f"{self.base_url}/fixtures"
            params = {
                'league': league_id,
                'season': '2023',
                'status': 'FT',
                'last': '5'
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    fixtures = data.get('response', [])
                    print(f"   📊 Found {len(fixtures)} matches")
                    
                    if fixtures:
                        # Test first fixture for corners
                        fixture_id = fixtures[0]['fixture']['id']
                        home_team = fixtures[0]['teams']['home']['name']
                        away_team = fixtures[0]['teams']['away']['name']
                        
                        print(f"   🏈 Testing: {home_team} vs {away_team}")
                        
                        corners_found, _ = self.test_fixture_corners(fixture_id)
                        if corners_found:
                            print(f"   ✅ {league_name} has corners data!")
                            return league_id, league_name
                        else:
                            print(f"   ❌ No corners data in {league_name}")
                else:
                    print(f"   ❌ API Error: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Exception: {e}")
        
        return None, None
    
    def test_fixture_corners(self, fixture_id):
        """Test corners for a specific fixture"""
        url = f"{self.base_url}/fixtures/statistics"
        params = {'fixture': fixture_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                for team_stats in data.get('response', []):
                    for stat in team_stats.get('statistics', []):
                        if 'corner' in stat.get('type', '').lower():
                            return True
                
                return False
            else:
                return False
                
        except Exception as e:
            return False
    
    def check_api_status(self):
        """Check API status and quotas"""
        print("🔍 Checking API Status")
        print("=" * 25)
        
        url = f"{self.base_url}/status"
        
        try:
            response = requests.get(url, headers=self.headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if 'response' in data:
                    quota = data['response']
                    print(f"✅ API Status: Active")
                    print(f"📊 Requests today: {quota.get('requests', {}).get('current', 'N/A')}")
                    print(f"📊 Daily limit: {quota.get('requests', {}).get('limit_day', 'N/A')}")
                    print(f"📊 Account type: {quota.get('account', {}).get('plan', 'N/A')}")
                    
                    return True
                else:
                    print("❌ Invalid response format")
                    return False
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False

def main():
    print("🏆 Comprehensive Corners API Test")
    print("=" * 50)
    
    tester = CornersTest2023()
    
    # Check API status first
    api_working = tester.check_api_status()
    
    if not api_working:
        print("❌ API not working properly")
        return
    
    # Test specific fixture
    corners_found, data = tester.test_specific_fixture()
    
    if corners_found:
        print("\n🎉 SUCCESS! Corners data found!")
    else:
        print("\n⚠️ No corners in test fixture, trying other approaches...")
        
        # Test multiple seasons
        season, fixtures = tester.test_multiple_seasons()
        
        if fixtures:
            print(f"\n✅ Found data in season {season}")
            
            # Test first fixture for corners
            fixture_id = fixtures[0]['fixture']['id']
            corners_found, _ = tester.test_fixture_corners(fixture_id)
            
            if corners_found:
                print("🏆 Corners data confirmed!")
            else:
                print("❌ Still no corners data")
        else:
            # Test different leagues
            league_id, league_name = tester.test_leagues_with_corners()
            
            if league_id:
                print(f"\n🎯 Found corners data in {league_name}!")
            else:
                print("\n❌ No corners data found in any league")
    
    print("\n📋 SUMMARY:")
    print("=" * 20)
    if corners_found:
        print("✅ API-Sports v3 has corners data")
        print("🚀 Ready to integrate corners predictions")
        print("💡 Use fixture statistics endpoint")
    else:
        print("❌ Corners data not accessible")
        print("💡 May need different API plan or endpoints")

if __name__ == "__main__":
    main()
