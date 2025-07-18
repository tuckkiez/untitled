#!/usr/bin/env python3
"""
🚀 Fetch Data from API-Football - July 18, 2025
ดึงข้อมูลจาก API-Football สำหรับการวิเคราะห์ฟุตบอล
"""

import requests
import json
import os
from datetime import datetime

class APIFootballFetcher:
    """API-Football Data Fetcher"""
    
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
        
        print("🚀 Initializing API-Football Fetcher")
    
    def fetch_fixtures(self, date="2025-07-18", league=None, season=None):
        """Fetch fixtures for the specified date"""
        print(f"📅 Fetching fixtures for date: {date}...")
        
        url = f"{self.base_url}/fixtures"
        params = {"date": date}
        
        if league:
            params["league"] = league
        
        if season:
            params["season"] = season
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            filename = f"fixtures_{date}"
            if league:
                filename += f"_league{league}"
            if season:
                filename += f"_season{season}"
            filename += ".json"
            
            output_file = os.path.join(self.data_dir, filename)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched fixtures: {data.get('results', 0)} matches")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching fixtures: {str(e)}")
            return None
    
    def fetch_odds(self, fixture_id=None, date=None, league=None, season=None, bookmaker=None, bet=None):
        """Fetch odds for fixtures"""
        print(f"💰 Fetching odds...")
        
        url = f"{self.base_url}/odds"
        params = {}
        
        if fixture_id:
            params["fixture"] = fixture_id
        
        if date:
            params["date"] = date
        
        if league:
            params["league"] = league
        
        if season:
            params["season"] = season
        
        if bookmaker:
            params["bookmaker"] = bookmaker
        
        if bet:
            params["bet"] = bet
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            filename = "odds"
            if fixture_id:
                filename += f"_fixture{fixture_id}"
            if date:
                filename += f"_{date}"
            if league:
                filename += f"_league{league}"
            filename += ".json"
            
            output_file = os.path.join(self.data_dir, filename)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched odds for {data.get('results', 0)} fixtures")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching odds: {str(e)}")
            return None
    
    def fetch_team_statistics(self, team_id, league_id, season):
        """Fetch team statistics"""
        print(f"📊 Fetching statistics for team {team_id} in league {league_id} season {season}...")
        
        url = f"{self.base_url}/teams/statistics"
        params = {
            "team": team_id,
            "league": league_id,
            "season": season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.data_dir, f"team_stats_{team_id}_league{league_id}_season{season}.json")
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
            output_file = os.path.join(self.data_dir, f"h2h_{team1_id}_vs_{team2_id}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched head to head statistics: {data.get('results', 0)} matches")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching head to head statistics: {str(e)}")
            return None
    
    def fetch_leagues(self, country=None, season=None, team=None):
        """Fetch leagues"""
        print(f"🏆 Fetching leagues...")
        
        url = f"{self.base_url}/leagues"
        params = {}
        
        if country:
            params["country"] = country
        
        if season:
            params["season"] = season
        
        if team:
            params["team"] = team
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            filename = "leagues"
            if country:
                filename += f"_{country}"
            if season:
                filename += f"_season{season}"
            if team:
                filename += f"_team{team}"
            filename += ".json"
            
            output_file = os.path.join(self.data_dir, filename)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched {data.get('results', 0)} leagues")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching leagues: {str(e)}")
            return None
    
    def fetch_standings(self, league_id, season):
        """Fetch standings"""
        print(f"📊 Fetching standings for league {league_id} season {season}...")
        
        url = f"{self.base_url}/standings"
        params = {
            "league": league_id,
            "season": season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save data
            output_file = os.path.join(self.data_dir, f"standings_league{league_id}_season{season}.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully fetched standings")
            print(f"✅ Data saved to: {output_file}")
            
            return data
        except Exception as e:
            print(f"❌ Error fetching standings: {str(e)}")
            return None
    
    def fetch_korea_k_league_data(self, date="2025-07-18", season=2025):
        """Fetch all relevant data for Korea K League 1"""
        print(f"🇰🇷 Fetching all data for Korea K League 1...")
        
        # League ID for Korea K League 1 is 292
        league_id = 292
        
        # 1. Fetch fixtures
        fixtures_data = self.fetch_fixtures(date=date, league=league_id, season=season)
        
        if not fixtures_data or fixtures_data.get("results", 0) == 0:
            print("❌ No fixtures found for Korea K League 1")
            return None
        
        # 2. Fetch odds for these fixtures
        odds_data = self.fetch_odds(date=date, league=league_id, season=season)
        
        # 3. Fetch standings
        standings_data = self.fetch_standings(league_id=league_id, season=season)
        
        # 4. For each fixture, fetch team statistics and head to head
        fixtures = fixtures_data.get("response", [])
        for fixture in fixtures:
            fixture_id = fixture.get("fixture", {}).get("id")
            home_team_id = fixture.get("teams", {}).get("home", {}).get("id")
            away_team_id = fixture.get("teams", {}).get("away", {}).get("id")
            home_team_name = fixture.get("teams", {}).get("home", {}).get("name")
            away_team_name = fixture.get("teams", {}).get("away", {}).get("name")
            
            print(f"📋 Processing fixture {fixture_id}: {home_team_name} vs {away_team_name}")
            
            # Fetch team statistics
            self.fetch_team_statistics(team_id=home_team_id, league_id=league_id, season=season)
            self.fetch_team_statistics(team_id=away_team_id, league_id=league_id, season=season)
            
            # Fetch head to head
            self.fetch_head_to_head(team1_id=home_team_id, team2_id=away_team_id)
        
        print(f"✅ Successfully fetched all data for Korea K League 1")
        return {
            "fixtures": fixtures_data,
            "odds": odds_data,
            "standings": standings_data
        }
    
    def fetch_china_super_league_data(self, date="2025-07-18", season=2025):
        """Fetch all relevant data for China Super League"""
        print(f"🇨🇳 Fetching all data for China Super League...")
        
        # League ID for China Super League is 169
        league_id = 169
        
        # 1. Fetch fixtures
        fixtures_data = self.fetch_fixtures(date=date, league=league_id, season=season)
        
        if not fixtures_data or fixtures_data.get("results", 0) == 0:
            print("❌ No fixtures found for China Super League")
            return None
        
        # 2. Fetch odds for these fixtures
        odds_data = self.fetch_odds(date=date, league=league_id, season=season)
        
        # 3. Fetch standings
        standings_data = self.fetch_standings(league_id=league_id, season=season)
        
        # 4. For each fixture, fetch team statistics and head to head
        fixtures = fixtures_data.get("response", [])
        for fixture in fixtures:
            fixture_id = fixture.get("fixture", {}).get("id")
            home_team_id = fixture.get("teams", {}).get("home", {}).get("id")
            away_team_id = fixture.get("teams", {}).get("away", {}).get("id")
            home_team_name = fixture.get("teams", {}).get("home", {}).get("name")
            away_team_name = fixture.get("teams", {}).get("away", {}).get("name")
            
            print(f"📋 Processing fixture {fixture_id}: {home_team_name} vs {away_team_name}")
            
            # Fetch team statistics
            self.fetch_team_statistics(team_id=home_team_id, league_id=league_id, season=season)
            self.fetch_team_statistics(team_id=away_team_id, league_id=league_id, season=season)
            
            # Fetch head to head
            self.fetch_head_to_head(team1_id=home_team_id, team2_id=away_team_id)
        
        print(f"✅ Successfully fetched all data for China Super League")
        return {
            "fixtures": fixtures_data,
            "odds": odds_data,
            "standings": standings_data
        }

def main():
    """Main function"""
    fetcher = APIFootballFetcher()
    
    # Fetch data for Korea K League 1
    korea_data = fetcher.fetch_korea_k_league_data()
    
    # Fetch data for China Super League
    china_data = fetcher.fetch_china_super_league_data()
    
    print("\n✅ Data fetching complete!")

if __name__ == "__main__":
    main()
