#!/usr/bin/env python3
"""
🚀 Fetch Real Football Data from API-Football - July 18, 2025
ดึงข้อมูลจริงจาก API-Football
"""

import requests
import json
import os
from datetime import datetime

class FootballDataFetcher:
    """Football Data Fetcher using API-Football"""
    
    def __init__(self, api_key):
        """Initialize the fetcher"""
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
            "x-rapidapi-key": api_key
        }
        self.output_dir = "/Users/80090/Desktop/Project/untitle/api_data/real_football_data"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def fetch_fixtures_by_date(self, date):
        """Fetch fixtures by date"""
        print(f"📅 Fetching fixtures for date: {date}...")
        
        url = f"{self.base_url}/fixtures"
        params = {"date": date}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.output_dir, f"fixtures_{date}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully saved fixtures to {output_file}")
            print(f"📊 Found {data.get('results', 0)} fixtures")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching fixtures: {str(e)}")
            return None
    
    def fetch_head_to_head(self, team1_id, team2_id):
        """Fetch head to head between two teams"""
        print(f"🆚 Fetching head to head for teams: {team1_id} vs {team2_id}...")
        
        url = f"{self.base_url}/fixtures/headtohead"
        params = {"h2h": f"{team1_id}-{team2_id}"}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.output_dir, f"h2h_{team1_id}_{team2_id}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully saved head to head to {output_file}")
            print(f"📊 Found {data.get('results', 0)} matches")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching head to head: {str(e)}")
            return None
    
    def fetch_team_statistics(self, league_id, season, team_id):
        """Fetch team statistics"""
        print(f"📊 Fetching statistics for team {team_id} in league {league_id} season {season}...")
        
        url = f"{self.base_url}/teams/statistics"
        params = {
            "league": league_id,
            "season": season,
            "team": team_id
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.output_dir, f"stats_league{league_id}_team{team_id}_season{season}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully saved team statistics to {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching team statistics: {str(e)}")
            return None
    
    def fetch_scoremer_data(self, league_id):
        """Fetch data from scoremer.com"""
        print(f"🌐 Fetching data from scoremer.com for league {league_id}...")
        print("⚠️ Note: This would require web scraping which is not implemented in this script.")
        print("⚠️ You would need to use a library like BeautifulSoup or Selenium to scrape the website.")
        
        # Example URL: https://www.scoremer.com/league/85
        url = f"https://www.scoremer.com/league/{league_id}"
        
        print(f"📋 URL to scrape: {url}")
        
        return None
    
    def fetch_and_process_league_data(self, league_id, season, date):
        """Fetch and process data for a specific league"""
        print(f"🏆 Fetching data for league {league_id}, season {season}, date {date}...")
        
        # 1. Fetch fixtures for the date
        fixtures_data = self.fetch_fixtures_by_date(date)
        
        if not fixtures_data or fixtures_data.get('results', 0) == 0:
            print(f"❌ No fixtures found for date {date}")
            return None
        
        # Filter fixtures for the specified league
        league_fixtures = []
        for fixture in fixtures_data.get('response', []):
            if fixture.get('league', {}).get('id') == league_id:
                league_fixtures.append(fixture)
        
        if not league_fixtures:
            print(f"❌ No fixtures found for league {league_id} on date {date}")
            return None
        
        print(f"✅ Found {len(league_fixtures)} fixtures for league {league_id}")
        
        # 2. Process each fixture
        processed_fixtures = []
        for fixture in league_fixtures:
            fixture_id = fixture.get('fixture', {}).get('id')
            home_team_id = fixture.get('teams', {}).get('home', {}).get('id')
            away_team_id = fixture.get('teams', {}).get('away', {}).get('id')
            
            print(f"📋 Processing fixture {fixture_id}: {fixture.get('teams', {}).get('home', {}).get('name')} vs {fixture.get('teams', {}).get('away', {}).get('name')}")
            
            # 3. Fetch head to head
            h2h_data = self.fetch_head_to_head(home_team_id, away_team_id)
            
            # 4. Fetch team statistics
            home_stats = self.fetch_team_statistics(league_id, season, home_team_id)
            away_stats = self.fetch_team_statistics(league_id, season, away_team_id)
            
            # 5. Create processed fixture
            processed_fixture = {
                "fixture": fixture,
                "head_to_head": h2h_data.get('response', []) if h2h_data else [],
                "home_team_stats": home_stats.get('response', {}) if home_stats else {},
                "away_team_stats": away_stats.get('response', {}) if away_stats else {}
            }
            
            processed_fixtures.append(processed_fixture)
        
        # 6. Save processed data
        output_data = {
            "league_id": league_id,
            "season": season,
            "date": date,
            "fixtures": processed_fixtures,
            "fetch_time": datetime.now().isoformat()
        }
        
        output_file = os.path.join(self.output_dir, f"league{league_id}_fixtures_{date}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Successfully saved processed data to {output_file}")
        
        return output_data

def main():
    """Main function"""
    # API key
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # Create fetcher
    fetcher = FootballDataFetcher(api_key)
    
    # Parameters
    date = "2025-07-18"  # Today's date
    
    # Fetch fixtures for today
    fixtures_data = fetcher.fetch_fixtures_by_date(date)
    
    # Example: Fetch head to head for Manchester United vs Manchester City
    # fetcher.fetch_head_to_head(33, 34)
    
    # Example: Fetch team statistics for Manchester United in Premier League
    # fetcher.fetch_team_statistics(39, 2024, 33)
    
    # Example: Fetch and process data for K League 1
    # Korean K League 1 ID is 292
    # fetcher.fetch_and_process_league_data(292, 2025, date)
    
    print("\n✅ Data fetching complete!")

if __name__ == "__main__":
    main()
