#!/usr/bin/env python3
"""
🎯 Improved Corners Data Collection Strategy
===========================================
Strategies to get more complete corners data
"""

import requests
import json
import time
from datetime import datetime, timedelta

class ImprovedCornersCollector:
    def __init__(self):
        self.api_key = "9936a2866ebc7271a809ff2ab164b032"
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        self.request_count = 0
        self.daily_limit = 100
    
    def check_quota_status(self):
        """Check remaining API quota"""
        url = f"{self.base_url}/status"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                quota = data.get('response', {})
                current = quota.get('requests', {}).get('current', 0)
                limit = quota.get('requests', {}).get('limit_day', 100)
                
                print(f"📊 API Quota: {current}/{limit} requests used")
                return limit - current
            else:
                print(f"❌ Quota check failed: {response.status_code}")
                return 0
        except Exception as e:
            print(f"❌ Quota check error: {e}")
            return 0
    
    def get_fixtures_by_date_range(self, league_id="39", season="2023", 
                                  start_date=None, end_date=None):
        """Get fixtures by specific date range"""
        print(f"📅 Getting fixtures by date range...")
        
        url = f"{self.base_url}/fixtures"
        params = {
            'league': league_id,
            'season': season,
            'status': 'FT'
        }
        
        if start_date:
            params['from'] = start_date
        if end_date:
            params['to'] = end_date
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            self.request_count += 1
            
            if response.status_code == 200:
                fixtures = response.json().get('response', [])
                print(f"✅ Found {len(fixtures)} fixtures in date range")
                return fixtures
            else:
                print(f"❌ Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Exception: {e}")
            return []
    
    def get_fixtures_by_round(self, league_id="39", season="2023", round_number="Regular Season - 1"):
        """Get fixtures by specific round"""
        print(f"🏆 Getting fixtures for round: {round_number}")
        
        url = f"{self.base_url}/fixtures"
        params = {
            'league': league_id,
            'season': season,
            'round': round_number,
            'status': 'FT'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            self.request_count += 1
            
            if response.status_code == 200:
                fixtures = response.json().get('response', [])
                print(f"✅ Found {len(fixtures)} fixtures in round")
                return fixtures
            else:
                print(f"❌ Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Exception: {e}")
            return []
    
    def collect_corners_systematically(self, league_id="39", season="2023", 
                                     max_requests=80):
        """Systematic corners collection with quota management"""
        print(f"🎯 Systematic Corners Collection")
        print("=" * 40)
        
        remaining_quota = self.check_quota_status()
        if remaining_quota < 20:
            print(f"⚠️ Low quota remaining: {remaining_quota}")
            print("💡 Consider running tomorrow or upgrading API plan")
            return []
        
        # Strategy 1: Recent matches first (more likely to have data)
        print("\n📅 Strategy 1: Recent matches")
        recent_fixtures = self.get_fixtures_by_date_range(
            league_id, season, 
            start_date="2023-05-01",  # End of season
            end_date="2023-05-31"
        )
        
        corners_data = []
        successful_corners = 0
        
        for fixture in recent_fixtures[:min(30, max_requests//2)]:
            if self.request_count >= max_requests:
                break
                
            corners = self.get_fixture_corners_detailed(fixture)
            if corners:
                corners_data.append(corners)
                successful_corners += 1
                print(f"✅ {corners['home_team']} vs {corners['away_team']}: {corners['total_corners']} corners")
            else:
                print(f"❌ No corners: {fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}")
            
            # Rate limiting
            time.sleep(0.5)
        
        print(f"\n📊 Recent matches: {successful_corners} successful")
        
        # Strategy 2: Popular teams (more likely to have complete data)
        if self.request_count < max_requests:
            print(f"\n🌟 Strategy 2: Popular teams")
            popular_teams = ["Arsenal", "Manchester City", "Liverpool", "Chelsea", "Manchester United", "Tottenham"]
            
            for team in popular_teams:
                if self.request_count >= max_requests:
                    break
                    
                team_fixtures = self.get_team_fixtures(league_id, season, team)
                
                for fixture in team_fixtures[:5]:  # 5 matches per team
                    if self.request_count >= max_requests:
                        break
                        
                    corners = self.get_fixture_corners_detailed(fixture)
                    if corners and not any(c['fixture_id'] == corners['fixture_id'] for c in corners_data):
                        corners_data.append(corners)
                        successful_corners += 1
                        print(f"✅ {corners['home_team']} vs {corners['away_team']}: {corners['total_corners']} corners")
                    
                    time.sleep(0.5)
        
        print(f"\n🎯 Total corners data collected: {len(corners_data)}")
        return corners_data
    
    def get_team_fixtures(self, league_id, season, team_name):
        """Get fixtures for a specific team"""
        url = f"{self.base_url}/fixtures"
        params = {
            'league': league_id,
            'season': season,
            'team': self.get_team_id(team_name),
            'status': 'FT'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            self.request_count += 1
            
            if response.status_code == 200:
                return response.json().get('response', [])
            else:
                return []
        except Exception as e:
            return []
    
    def get_team_id(self, team_name):
        """Get team ID for API calls"""
        team_ids = {
            "Arsenal": 42,
            "Manchester City": 50,
            "Liverpool": 40,
            "Chelsea": 49,
            "Manchester United": 33,
            "Tottenham": 47
        }
        return team_ids.get(team_name, 42)  # Default to Arsenal
    
    def get_fixture_corners_detailed(self, fixture):
        """Get detailed corners data for a fixture"""
        fixture_id = fixture['fixture']['id']
        
        url = f"{self.base_url}/fixtures/statistics"
        params = {'fixture': fixture_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            self.request_count += 1
            
            if response.status_code == 200:
                stats_data = response.json()
                
                home_corners = 0
                away_corners = 0
                home_team = fixture['teams']['home']['name']
                away_team = fixture['teams']['away']['name']
                
                for team_stats in stats_data.get('response', []):
                    for stat in team_stats.get('statistics', []):
                        if stat.get('type', '').lower() == 'corner kicks':
                            if team_stats['team']['name'] == home_team:
                                home_corners = int(stat.get('value', 0))
                            else:
                                away_corners = int(stat.get('value', 0))
                
                if home_corners > 0 or away_corners > 0:
                    return {
                        'fixture_id': fixture_id,
                        'date': fixture['fixture']['date'],
                        'home_team': home_team,
                        'away_team': away_team,
                        'home_corners': home_corners,
                        'away_corners': away_corners,
                        'total_corners': home_corners + away_corners,
                        'corners_over_9': 1 if (home_corners + away_corners) > 9 else 0,
                        'corners_over_10': 1 if (home_corners + away_corners) > 10 else 0,
                        'corners_handicap': 1 if home_corners > (away_corners + 2.5) else 0
                    }
                else:
                    return None
            else:
                return None
        except Exception as e:
            return None
    
    def save_corners_data(self, corners_data, filename="improved_corners_data.json"):
        """Save corners data with metadata"""
        data_with_metadata = {
            'collection_date': datetime.now().isoformat(),
            'total_matches': len(corners_data),
            'api_requests_used': self.request_count,
            'matches': corners_data
        }
        
        with open(filename, 'w') as f:
            json.dump(data_with_metadata, f, indent=2)
        
        print(f"💾 Saved {len(corners_data)} matches to {filename}")
    
    def analyze_collection_efficiency(self, corners_data):
        """Analyze data collection efficiency"""
        print(f"\n📊 Collection Efficiency Analysis")
        print("=" * 35)
        
        if not corners_data:
            print("❌ No data to analyze")
            return
        
        total_corners = [match['total_corners'] for match in corners_data]
        
        print(f"📈 Matches collected: {len(corners_data)}")
        print(f"📈 API requests used: {self.request_count}")
        print(f"📈 Success rate: {len(corners_data)/self.request_count*100:.1f}%")
        print(f"📈 Average corners: {sum(total_corners)/len(total_corners):.1f}")
        print(f"📈 Corners range: {min(total_corners)}-{max(total_corners)}")
        
        # Over/Under analysis
        over_9 = sum(1 for match in corners_data if match['corners_over_9'])
        over_10 = sum(1 for match in corners_data if match['corners_over_10'])
        
        print(f"📈 Over 9.5 corners: {over_9}/{len(corners_data)} ({over_9/len(corners_data)*100:.1f}%)")
        print(f"📈 Over 10.5 corners: {over_10}/{len(corners_data)} ({over_10/len(corners_data)*100:.1f}%)")

def main():
    print("🎯 Improved Corners Data Collection")
    print("=" * 50)
    
    collector = ImprovedCornersCollector()
    
    # Check quota first
    remaining = collector.check_quota_status()
    
    if remaining < 10:
        print("⚠️ Insufficient quota for meaningful collection")
        print("💡 Try again tomorrow or upgrade API plan")
        return
    
    # Collect corners data systematically
    corners_data = collector.collect_corners_systematically(
        league_id="39", 
        season="2023", 
        max_requests=min(80, remaining-5)  # Leave 5 requests buffer
    )
    
    if corners_data:
        # Save data
        collector.save_corners_data(corners_data)
        
        # Analyze efficiency
        collector.analyze_collection_efficiency(corners_data)
        
        print(f"\n🎉 SUCCESS! Collected {len(corners_data)} matches with corners data")
        print("💡 This is a significant improvement over the previous 19 matches")
    else:
        print("❌ No corners data collected")
        print("💡 Check API quota and try different strategies")

if __name__ == "__main__":
    main()
