#!/usr/bin/env python3
"""
🚀 Fetch Korea K League 1 Data from API-Football - July 18, 2025
ดึงข้อมูล Korea K League 1 จาก API-Football สำหรับการวิเคราะห์ฟุตบอล
"""

import requests
import json
import os
from datetime import datetime

class KoreaKLeagueDataFetcher:
    """Korea K League 1 Data Fetcher using API-Football"""
    
    def __init__(self):
        """Initialize the fetcher"""
        self.api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
        self.api_host = "api-football-v1.p.rapidapi.com"
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            "x-rapidapi-host": self.api_host,
            "x-rapidapi-key": self.api_key
        }
        self.data_dir = "/Users/80090/Desktop/Project/untitle/data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # League info
        self.league_id = 292  # Korea K League 1
        self.league_name = "Korea K League 1"
        self.season = 2025
        
        print(f"🚀 Initializing {self.league_name} Data Fetcher")
    
    def fetch_fixtures(self, date="2025-07-18"):
        """Fetch fixtures for the specified date"""
        print(f"📅 Fetching fixtures for date: {date}...")
        
        url = f"{self.base_url}/fixtures"
        params = {
            "date": date,
            "league": self.league_id,
            "season": self.season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.data_dir, f"korea_fixtures_{date}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched fixtures: {data.get('results', 0)} matches")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching fixtures: {str(e)}")
            return None
    
    def fetch_odds(self, date="2025-07-18"):
        """Fetch odds for fixtures"""
        print(f"💰 Fetching odds for date: {date}...")
        
        url = f"{self.base_url}/odds"
        params = {
            "date": date,
            "league": self.league_id,
            "season": self.season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.data_dir, f"korea_odds_{date}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched odds for {data.get('results', 0)} fixtures")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching odds: {str(e)}")
            return None
    
    def fetch_standings(self):
        """Fetch standings"""
        print(f"📊 Fetching standings...")
        
        url = f"{self.base_url}/standings"
        params = {
            "league": self.league_id,
            "season": self.season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.data_dir, f"korea_standings_{self.season}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched standings")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching standings: {str(e)}")
            return None
    
    def fetch_team_statistics(self, team_id):
        """Fetch team statistics"""
        print(f"📊 Fetching statistics for team {team_id}...")
        
        url = f"{self.base_url}/teams/statistics"
        params = {
            "team": team_id,
            "league": self.league_id,
            "season": self.season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.data_dir, f"korea_team_stats_{team_id}_{self.season}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched team statistics")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching team statistics: {str(e)}")
            return None
    
    def fetch_head_to_head(self, team1_id, team2_id):
        """Fetch head to head statistics"""
        print(f"🆚 Fetching head to head statistics for teams {team1_id} vs {team2_id}...")
        
        url = f"{self.base_url}/fixtures/headtohead"
        params = {
            "h2h": f"{team1_id}-{team2_id}"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.data_dir, f"korea_h2h_{team1_id}_vs_{team2_id}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched head to head statistics: {data.get('results', 0)} matches")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching head to head statistics: {str(e)}")
            return None
    
    def process_fixtures_data(self, fixtures_data):
        """Process fixtures data"""
        print("🔄 Processing fixtures data...")
        
        fixtures = []
        
        for fixture in fixtures_data.get("response", []):
            fixture_id = fixture.get("fixture", {}).get("id")
            home_team = fixture.get("teams", {}).get("home", {})
            away_team = fixture.get("teams", {}).get("away", {})
            
            fixtures.append({
                "fixture_id": fixture_id,
                "home_team": home_team.get("name"),
                "home_team_id": home_team.get("id"),
                "away_team": away_team.get("name"),
                "away_team_id": away_team.get("id"),
                "datetime": fixture.get("fixture", {}).get("date"),
                "venue": fixture.get("fixture", {}).get("venue", {}).get("name"),
                "city": fixture.get("fixture", {}).get("venue", {}).get("city")
            })
        
        print(f"✅ Processed {len(fixtures)} fixtures")
        return fixtures
    
    def fetch_all_data(self, date="2025-07-18"):
        """Fetch all relevant data for Korea K League 1"""
        print(f"🇰🇷 Fetching all data for {self.league_name} on {date}...")
        
        # 1. Fetch fixtures
        fixtures_data = self.fetch_fixtures(date=date)
        
        if not fixtures_data or fixtures_data.get("results", 0) == 0:
            print(f"❌ No fixtures found for {self.league_name} on {date}")
            return None
        
        # 2. Fetch odds for these fixtures
        odds_data = self.fetch_odds(date=date)
        
        # 3. Fetch standings
        standings_data = self.fetch_standings()
        
        # 4. Process fixtures data
        fixtures = self.process_fixtures_data(fixtures_data)
        
        # 5. For each fixture, fetch team statistics and head to head
        for fixture in fixtures:
            home_team_id = fixture["home_team_id"]
            away_team_id = fixture["away_team_id"]
            
            print(f"📋 Processing fixture: {fixture['home_team']} vs {fixture['away_team']}")
            
            # Fetch team statistics
            self.fetch_team_statistics(team_id=home_team_id)
            self.fetch_team_statistics(team_id=away_team_id)
            
            # Fetch head to head
            self.fetch_head_to_head(team1_id=home_team_id, team2_id=away_team_id)
        
        print(f"✅ Successfully fetched all data for {self.league_name}")
        
        # 6. Return all data
        return {
            "fixtures": fixtures,
            "fixtures_data": fixtures_data,
            "odds_data": odds_data,
            "standings_data": standings_data
        }

def main():
    """Main function"""
    fetcher = KoreaKLeagueDataFetcher()
    
    # Fetch all data for Korea K League 1
    data = fetcher.fetch_all_data()
    
    if data:
        # Save processed data
        output_file = os.path.join(fetcher.data_dir, f"korea_k_league_processed_data_{datetime.now().strftime('%Y-%m-%d')}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data["fixtures"], f, ensure_ascii=False, indent=2)
        
        print(f"✅ Processed data saved to: {output_file}")
        print(f"✅ Total fixtures: {len(data['fixtures'])}")
    
    print("\n✅ Data fetching complete!")

if __name__ == "__main__":
    main()
