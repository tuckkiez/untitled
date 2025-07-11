#!/usr/bin/env python3
"""
🏆 Premier League Corners Data Test
===================================
Test API-Sports v3 with Premier League data
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta

class PremierLeagueCornersTest:
    def __init__(self):
        self.api_key = "9936a2866ebc7271a809ff2ab164b032"
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
    
    def get_premier_league_fixtures(self, season="2024", status="FT"):
        """Get Premier League fixtures"""
        print(f"📥 Getting Premier League {season} fixtures...")
        
        url = f"{self.base_url}/fixtures"
        params = {
            'league': '39',  # Premier League
            'season': season,
            'status': status
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get('response', [])
                print(f"✅ Found {len(fixtures)} fixtures")
                return fixtures
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return []
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return []
    
    def get_fixture_corners(self, fixture_id):
        """Get corners data for a specific fixture"""
        url = f"{self.base_url}/fixtures/statistics"
        params = {'fixture': fixture_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                corners_data = {}
                
                for team_stats in data.get('response', []):
                    team_name = team_stats.get('team', {}).get('name', '')
                    
                    for stat in team_stats.get('statistics', []):
                        if stat.get('type', '').lower() == 'corner kicks':
                            corners_data[team_name] = int(stat.get('value', 0))
                
                return corners_data
            else:
                return None
                
        except Exception as e:
            print(f"Error getting corners for fixture {fixture_id}: {e}")
            return None
    
    def test_corners_data_collection(self, max_fixtures=20):
        """Test collecting corners data from recent fixtures"""
        print(f"🧪 Testing Corners Data Collection (Max {max_fixtures} fixtures)")
        print("=" * 60)
        
        # Get recent fixtures
        fixtures = self.get_premier_league_fixtures()
        
        if not fixtures:
            print("❌ No fixtures found")
            return []
        
        corners_data = []
        successful_requests = 0
        
        for i, fixture in enumerate(fixtures[:max_fixtures]):
            if successful_requests >= 10:  # Limit to avoid quota issues
                print("⚠️ Stopping at 10 successful requests to preserve quota")
                break
                
            fixture_id = fixture['fixture']['id']
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            match_date = fixture['fixture']['date']
            
            print(f"\n🏈 Match {i+1}: {home_team} vs {away_team}")
            print(f"   Date: {match_date}")
            print(f"   Fixture ID: {fixture_id}")
            
            # Get corners data
            corners = self.get_fixture_corners(fixture_id)
            
            if corners:
                home_corners = corners.get(home_team, 0)
                away_corners = corners.get(away_team, 0)
                total_corners = home_corners + away_corners
                
                match_data = {
                    'fixture_id': fixture_id,
                    'date': match_date,
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_corners': home_corners,
                    'away_corners': away_corners,
                    'total_corners': total_corners,
                    'corners_over_9': 1 if total_corners > 9 else 0,
                    'corners_over_10': 1 if total_corners > 10 else 0,
                    'home_corners_advantage': 1 if home_corners > away_corners else 0
                }
                
                corners_data.append(match_data)
                successful_requests += 1
                
                print(f"   🏆 Corners: {home_team} {home_corners} - {away_corners} {away_team}")
                print(f"   📊 Total: {total_corners} corners")
                print(f"   🎯 Over 9.5: {'Yes' if total_corners > 9 else 'No'}")
                
            else:
                print(f"   ❌ No corners data available")
        
        return corners_data
    
    def analyze_corners_patterns(self, corners_data):
        """Analyze corners patterns"""
        if not corners_data:
            print("❌ No data to analyze")
            return
        
        print(f"\n📊 CORNERS DATA ANALYSIS ({len(corners_data)} matches)")
        print("=" * 50)
        
        df = pd.DataFrame(corners_data)
        
        # Basic statistics
        print(f"📈 Average total corners: {df['total_corners'].mean():.1f}")
        print(f"📈 Median total corners: {df['total_corners'].median():.1f}")
        print(f"📈 Min corners: {df['total_corners'].min()}")
        print(f"📈 Max corners: {df['total_corners'].max()}")
        
        # Over/Under analysis
        over_9_rate = df['corners_over_9'].mean() * 100
        over_10_rate = df['corners_over_10'].mean() * 100
        
        print(f"\n🎯 Over 9.5 corners: {over_9_rate:.1f}% ({df['corners_over_9'].sum()}/{len(df)})")
        print(f"🎯 Over 10.5 corners: {over_10_rate:.1f}% ({df['corners_over_10'].sum()}/{len(df)})")
        
        # Home advantage
        home_advantage_rate = df['home_corners_advantage'].mean() * 100
        print(f"🏠 Home team more corners: {home_advantage_rate:.1f}%")
        
        # Distribution
        print(f"\n📊 Corners Distribution:")
        corners_dist = df['total_corners'].value_counts().sort_index()
        for corners, count in corners_dist.items():
            percentage = count / len(df) * 100
            print(f"   {corners} corners: {count} matches ({percentage:.1f}%)")
        
        return df
    
    def save_corners_data(self, corners_data, filename="premier_league_corners.json"):
        """Save corners data to file"""
        if corners_data:
            with open(filename, 'w') as f:
                json.dump(corners_data, f, indent=2)
            print(f"💾 Saved {len(corners_data)} matches to {filename}")
        else:
            print("❌ No data to save")

def main():
    print("🏆 Premier League Corners Data Test")
    print("=" * 50)
    
    tester = PremierLeagueCornersTest()
    
    # Test corners data collection
    corners_data = tester.test_corners_data_collection(max_fixtures=15)
    
    if corners_data:
        # Analyze patterns
        df = tester.analyze_corners_patterns(corners_data)
        
        # Save data
        tester.save_corners_data(corners_data)
        
        print(f"\n🎉 SUCCESS! Collected corners data from {len(corners_data)} matches")
        print("🚀 Ready to integrate corners predictions!")
        
        # Show sample data
        print(f"\n📋 Sample Data:")
        for match in corners_data[:3]:
            print(f"   {match['home_team']} {match['home_corners']} - {match['away_corners']} {match['away_team']} (Total: {match['total_corners']})")
    
    else:
        print("❌ No corners data collected")
        print("💡 Possible issues:")
        print("   - API quota exceeded")
        print("   - No recent finished matches")
        print("   - API key limitations")

if __name__ == "__main__":
    main()
