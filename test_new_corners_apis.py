#!/usr/bin/env python3
"""
🎯 Test New Corners APIs
========================
Testing both RapidAPI and API-Sports for corners data
"""

import requests
import json
from datetime import datetime, timedelta

class CornersAPITester:
    def __init__(self):
        self.api_key = "9936a2866ebc7271a809ff2ab164b032"
        
        # API configurations
        self.rapidapi_config = {
            'base_url': 'https://api-football-v1.p.rapidapi.com',
            'headers': {
                'X-RapidAPI-Key': self.api_key,
                'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
            }
        }
        
        self.apisports_config = {
            'base_url': 'https://v3.football.api-sports.io',
            'headers': {
                'x-rapidapi-key': self.api_key,
                'x-rapidapi-host': 'v3.football.api-sports.io'
            }
        }
    
    def test_rapidapi_v2_statistics(self):
        """Test RapidAPI v2 statistics endpoint"""
        print("🧪 Testing RapidAPI v2 Statistics")
        print("=" * 40)
        
        # First, get recent fixtures to test
        fixtures_url = f"{self.rapidapi_config['base_url']}/v3/fixtures"
        params = {
            'league': '39',  # Premier League
            'season': '2024',
            'last': '5'
        }
        
        try:
            response = requests.get(fixtures_url, headers=self.rapidapi_config['headers'], params=params)
            print(f"Fixtures Status: {response.status_code}")
            
            if response.status_code == 200:
                fixtures_data = response.json()
                if 'response' in fixtures_data and len(fixtures_data['response']) > 0:
                    fixture_id = fixtures_data['response'][0]['fixture']['id']
                    print(f"✅ Got fixture ID: {fixture_id}")
                    
                    # Test v2 statistics endpoint
                    stats_url = f"{self.rapidapi_config['base_url']}/v2/statistics/fixture/{fixture_id}"
                    stats_response = requests.get(stats_url, headers=self.rapidapi_config['headers'])
                    
                    print(f"Statistics Status: {stats_response.status_code}")
                    
                    if stats_response.status_code == 200:
                        stats_data = stats_response.json()
                        print("✅ RapidAPI v2 Statistics working!")
                        print(f"📊 Sample data keys: {list(stats_data.keys())}")
                        
                        # Look for corners data
                        if 'api' in stats_data and 'statistics' in stats_data['api']:
                            for team_stats in stats_data['api']['statistics']:
                                print(f"📈 Team: {team_stats.get('team_name', 'Unknown')}")
                                for stat in team_stats.get('statistics', []):
                                    if 'corner' in stat.get('type', '').lower():
                                        print(f"🏆 CORNERS FOUND: {stat}")
                        
                        return True, stats_data
                    else:
                        print(f"❌ Statistics failed: {stats_response.status_code}")
                        print(f"Response: {stats_response.text[:200]}")
                        return False, None
                else:
                    print("❌ No fixtures found")
                    return False, None
            else:
                print(f"❌ Fixtures failed: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False, None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False, None
    
    def test_apisports_v3_statistics(self):
        """Test API-Sports v3 statistics endpoint"""
        print("\n🧪 Testing API-Sports v3 Statistics")
        print("=" * 40)
        
        # Test with the example fixture ID
        fixture_id = "215662"
        stats_url = f"{self.apisports_config['base_url']}/fixtures/statistics"
        params = {'fixture': fixture_id}
        
        try:
            response = requests.get(stats_url, headers=self.apisports_config['headers'], params=params)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                stats_data = response.json()
                print("✅ API-Sports v3 Statistics working!")
                print(f"📊 Response keys: {list(stats_data.keys())}")
                
                if 'response' in stats_data:
                    for team_stats in stats_data['response']:
                        team_name = team_stats.get('team', {}).get('name', 'Unknown')
                        print(f"\n📈 Team: {team_name}")
                        
                        for stat in team_stats.get('statistics', []):
                            stat_type = stat.get('type', '')
                            stat_value = stat.get('value', '')
                            
                            # Look for corners
                            if 'corner' in stat_type.lower():
                                print(f"🏆 CORNERS: {stat_type} = {stat_value}")
                            
                            # Show all available stats
                            print(f"   {stat_type}: {stat_value}")
                
                return True, stats_data
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False, None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False, None
    
    def test_recent_premier_league_fixtures(self):
        """Test with recent Premier League fixtures"""
        print("\n🧪 Testing Recent Premier League Fixtures")
        print("=" * 45)
        
        # Get recent finished fixtures
        fixtures_url = f"{self.apisports_config['base_url']}/fixtures"
        params = {
            'league': '39',  # Premier League
            'season': '2024',
            'status': 'FT',  # Finished
            'last': '10'
        }
        
        try:
            response = requests.get(fixtures_url, headers=self.apisports_config['headers'], params=params)
            print(f"Fixtures Status: {response.status_code}")
            
            if response.status_code == 200:
                fixtures_data = response.json()
                
                if 'response' in fixtures_data and len(fixtures_data['response']) > 0:
                    print(f"✅ Found {len(fixtures_data['response'])} finished matches")
                    
                    corners_data = []
                    
                    # Test first 3 fixtures for corners data
                    for i, fixture in enumerate(fixtures_data['response'][:3]):
                        fixture_id = fixture['fixture']['id']
                        home_team = fixture['teams']['home']['name']
                        away_team = fixture['teams']['away']['name']
                        
                        print(f"\n🏈 Match {i+1}: {home_team} vs {away_team}")
                        print(f"   Fixture ID: {fixture_id}")
                        
                        # Get statistics for this fixture
                        stats_url = f"{self.apisports_config['base_url']}/fixtures/statistics"
                        stats_params = {'fixture': fixture_id}
                        
                        stats_response = requests.get(stats_url, headers=self.apisports_config['headers'], params=stats_params)
                        
                        if stats_response.status_code == 200:
                            stats_data = stats_response.json()
                            
                            match_corners = {'fixture_id': fixture_id, 'home_team': home_team, 'away_team': away_team}
                            
                            for team_stats in stats_data.get('response', []):
                                team_name = team_stats.get('team', {}).get('name', '')
                                
                                for stat in team_stats.get('statistics', []):
                                    if 'corner' in stat.get('type', '').lower():
                                        corners_value = stat.get('value', 0)
                                        if team_name == home_team:
                                            match_corners['home_corners'] = corners_value
                                        else:
                                            match_corners['away_corners'] = corners_value
                                        
                                        print(f"   🏆 {team_name} Corners: {corners_value}")
                            
                            if 'home_corners' in match_corners and 'away_corners' in match_corners:
                                total_corners = int(match_corners['home_corners']) + int(match_corners['away_corners'])
                                match_corners['total_corners'] = total_corners
                                print(f"   📊 Total Corners: {total_corners}")
                                corners_data.append(match_corners)
                        else:
                            print(f"   ❌ Stats failed: {stats_response.status_code}")
                    
                    return corners_data
                else:
                    print("❌ No finished fixtures found")
                    return []
            else:
                print(f"❌ Fixtures failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def test_api_limits(self):
        """Test API rate limits and quotas"""
        print("\n🔍 Testing API Limits")
        print("=" * 25)
        
        # Make multiple requests to test limits
        for i in range(5):
            url = f"{self.apisports_config['base_url']}/status"
            response = requests.get(url, headers=self.apisports_config['headers'])
            
            print(f"Request {i+1}: Status {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data:
                    quota = data['response']
                    print(f"   📊 Requests today: {quota.get('requests', {}).get('current', 'N/A')}")
                    print(f"   📊 Limit per day: {quota.get('requests', {}).get('limit_day', 'N/A')}")
            elif response.status_code == 429:
                print("   ⚠️ Rate limit hit!")
                break
            else:
                print(f"   ❌ Error: {response.text[:100]}")

def main():
    print("🎯 Comprehensive Corners API Testing")
    print("=" * 50)
    
    tester = CornersAPITester()
    
    # Test API limits first
    tester.test_api_limits()
    
    # Test RapidAPI v2
    rapidapi_success, rapidapi_data = tester.test_rapidapi_v2_statistics()
    
    # Test API-Sports v3
    apisports_success, apisports_data = tester.test_apisports_v3_statistics()
    
    # Test recent fixtures
    corners_data = tester.test_recent_premier_league_fixtures()
    
    # Summary
    print("\n🏆 TESTING SUMMARY")
    print("=" * 30)
    print(f"RapidAPI v2: {'✅ Working' if rapidapi_success else '❌ Failed'}")
    print(f"API-Sports v3: {'✅ Working' if apisports_success else '❌ Failed'}")
    print(f"Corners Data Found: {len(corners_data)} matches")
    
    if corners_data:
        print("\n📊 Sample Corners Data:")
        for match in corners_data[:2]:
            print(f"   {match['home_team']} {match.get('home_corners', 'N/A')} - {match.get('away_corners', 'N/A')} {match['away_team']}")
            print(f"   Total: {match.get('total_corners', 'N/A')} corners")
    
    # Recommendation
    print("\n💡 RECOMMENDATION:")
    if len(corners_data) >= 2:
        print("✅ API-Sports v3 is working and has corners data!")
        print("🚀 Ready to integrate corners predictions!")
    elif apisports_success or rapidapi_success:
        print("⚠️ API working but corners data limited")
        print("🔍 Need to test with more recent fixtures")
    else:
        print("❌ Both APIs failed - check API key or quotas")

if __name__ == "__main__":
    main()
