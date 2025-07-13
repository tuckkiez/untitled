#!/usr/bin/env python3
"""
🏆 Multi-League Database Manager
ระบบจัดการฐานข้อมูลการแข่งขันหลายลีก
Premier League, La Liga, Bundesliga, Ligue 1, Serie A, J-League 2
"""

import sqlite3
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class MultiLeagueDBManager:
    def __init__(self, db_path: str = "football_leagues.db", api_key: str = None):
        self.db_path = db_path
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        } if api_key else {}
        
        # League configurations
        self.leagues = {
            'premier_league': {
                'id': 39,
                'name': 'Premier League',
                'country': 'England',
                'seasons': [2023, 2024, 2025]
            },
            'la_liga': {
                'id': 140,
                'name': 'La Liga',
                'country': 'Spain', 
                'seasons': [2023, 2024, 2025]
            },
            'bundesliga': {
                'id': 78,
                'name': 'Bundesliga',
                'country': 'Germany',
                'seasons': [2023, 2024, 2025]
            },
            'ligue_1': {
                'id': 61,
                'name': 'Ligue 1',
                'country': 'France',
                'seasons': [2023, 2024, 2025]
            },
            'serie_a': {
                'id': 135,
                'name': 'Serie A',
                'country': 'Italy',
                'seasons': [2023, 2024, 2025]
            },
            'jleague_2': {
                'id': 99,
                'name': 'J-League 2',
                'country': 'Japan',
                'seasons': [2023, 2024, 2025]
            }
        }
        
        self.init_database()
        print("🚀 Multi-League Database Manager initialized!")
        print(f"📊 Managing {len(self.leagues)} leagues")

    def init_database(self):
        """Initialize database with all necessary tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Leagues table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leagues (
                league_key TEXT PRIMARY KEY,
                league_id INTEGER,
                name TEXT,
                country TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                team_id INTEGER PRIMARY KEY,
                name TEXT,
                league_key TEXT,
                country TEXT,
                founded INTEGER,
                venue_name TEXT,
                venue_capacity INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (league_key) REFERENCES leagues (league_key)
            )
        ''')
        
        # Matches table (main historical data)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY,
                league_key TEXT,
                season INTEGER,
                match_date DATE,
                home_team_id INTEGER,
                away_team_id INTEGER,
                home_score INTEGER,
                away_score INTEGER,
                match_status TEXT,
                home_odds REAL,
                draw_odds REAL,
                away_odds REAL,
                over_25_odds REAL,
                under_25_odds REAL,
                home_corners INTEGER,
                away_corners INTEGER,
                home_corners_1st INTEGER,
                away_corners_1st INTEGER,
                home_yellow_cards INTEGER,
                away_yellow_cards INTEGER,
                home_red_cards INTEGER,
                away_red_cards INTEGER,
                referee TEXT,
                venue TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (league_key) REFERENCES leagues (league_key),
                FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
                FOREIGN KEY (away_team_id) REFERENCES teams (team_id)
            )
        ''')
        
        # Team statistics table (calculated from matches)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER,
                league_key TEXT,
                season INTEGER,
                matches_played INTEGER,
                wins INTEGER,
                draws INTEGER,
                losses INTEGER,
                goals_for INTEGER,
                goals_against INTEGER,
                home_wins INTEGER,
                home_draws INTEGER,
                home_losses INTEGER,
                away_wins INTEGER,
                away_draws INTEGER,
                away_losses INTEGER,
                avg_corners_for REAL,
                avg_corners_against REAL,
                elo_rating REAL DEFAULT 1500,
                form_last_5 TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams (team_id),
                FOREIGN KEY (league_key) REFERENCES leagues (league_key)
            )
        ''')
        
        # Predictions table (for tracking our ML predictions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER,
                prediction_date TIMESTAMP,
                predicted_result TEXT,
                predicted_over_under TEXT,
                predicted_corners_1st TEXT,
                predicted_corners_total TEXT,
                confidence_result REAL,
                confidence_over_under REAL,
                confidence_corners REAL,
                actual_result TEXT,
                actual_over_under TEXT,
                actual_corners_1st INTEGER,
                actual_corners_total INTEGER,
                result_correct BOOLEAN,
                over_under_correct BOOLEAN,
                corners_correct BOOLEAN,
                model_version TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (match_id) REFERENCES matches (match_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database tables initialized")

    def populate_leagues(self):
        """Populate leagues table with configuration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for league_key, config in self.leagues.items():
            cursor.execute('''
                INSERT OR REPLACE INTO leagues (league_key, league_id, name, country)
                VALUES (?, ?, ?, ?)
            ''', (league_key, config['id'], config['name'], config['country']))
        
        conn.commit()
        conn.close()
        print("✅ Leagues populated")

    def fetch_and_store_teams(self, league_key: str):
        """Fetch teams from API and store in database"""
        if not self.api_key:
            print("❌ API key required for fetching data")
            return
        
        league_config = self.leagues[league_key]
        league_id = league_config['id']
        
        try:
            url = f"{self.base_url}/teams"
            params = {'league': league_id, 'season': 2024}
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                teams = data['response']
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                for team_data in teams:
                    team = team_data['team']
                    venue = team_data['venue']
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO teams 
                        (team_id, name, league_key, country, founded, venue_name, venue_capacity)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        team['id'], team['name'], league_key, team['country'],
                        team['founded'], venue['name'], venue['capacity']
                    ))
                
                conn.commit()
                conn.close()
                print(f"✅ {len(teams)} teams stored for {league_config['name']}")
            
        except Exception as e:
            print(f"❌ Error fetching teams for {league_key}: {e}")

    def fetch_and_store_matches(self, league_key: str, season: int):
        """Fetch historical matches and store in database"""
        if not self.api_key:
            print("❌ API key required for fetching data")
            return
        
        league_config = self.leagues[league_key]
        league_id = league_config['id']
        
        try:
            url = f"{self.base_url}/fixtures"
            params = {'league': league_id, 'season': season}
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data['response']
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                stored_count = 0
                for fixture in fixtures:
                    if fixture['fixture']['status']['short'] == 'FT':  # Only finished matches
                        match_data = self._extract_match_data(fixture, league_key, season)
                        if match_data:
                            cursor.execute('''
                                INSERT OR REPLACE INTO matches 
                                (match_id, league_key, season, match_date, home_team_id, away_team_id,
                                 home_score, away_score, match_status, venue, referee)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', match_data)
                            stored_count += 1
                
                conn.commit()
                conn.close()
                print(f"✅ {stored_count} matches stored for {league_config['name']} {season}")
            
        except Exception as e:
            print(f"❌ Error fetching matches for {league_key} {season}: {e}")

    def _extract_match_data(self, fixture: Dict, league_key: str, season: int) -> Tuple:
        """Extract match data from API response"""
        try:
            match_id = fixture['fixture']['id']
            match_date = fixture['fixture']['date'][:10]  # YYYY-MM-DD
            home_team_id = fixture['teams']['home']['id']
            away_team_id = fixture['teams']['away']['id']
            home_score = fixture['goals']['home']
            away_score = fixture['goals']['away']
            match_status = fixture['fixture']['status']['short']
            venue = fixture['fixture']['venue']['name']
            referee = fixture['fixture']['referee']
            
            return (
                match_id, league_key, season, match_date, home_team_id, away_team_id,
                home_score, away_score, match_status, venue, referee
            )
        except Exception as e:
            print(f"⚠️ Error extracting match data: {e}")
            return None

    def calculate_team_statistics(self, league_key: str, season: int):
        """Calculate team statistics from stored matches"""
        conn = sqlite3.connect(self.db_path)
        
        # Get all teams in the league
        teams_df = pd.read_sql_query('''
            SELECT team_id, name FROM teams WHERE league_key = ?
        ''', conn, params=(league_key,))
        
        # Get all matches for the season
        matches_df = pd.read_sql_query('''
            SELECT * FROM matches 
            WHERE league_key = ? AND season = ? AND match_status = 'FT'
        ''', conn, params=(league_key, season))
        
        cursor = conn.cursor()
        
        for _, team in teams_df.iterrows():
            team_id = team['team_id']
            
            # Home matches
            home_matches = matches_df[matches_df['home_team_id'] == team_id]
            # Away matches  
            away_matches = matches_df[matches_df['away_team_id'] == team_id]
            
            # Calculate statistics
            total_matches = len(home_matches) + len(away_matches)
            
            # Home stats
            home_wins = len(home_matches[home_matches['home_score'] > home_matches['away_score']])
            home_draws = len(home_matches[home_matches['home_score'] == home_matches['away_score']])
            home_losses = len(home_matches[home_matches['home_score'] < home_matches['away_score']])
            
            # Away stats
            away_wins = len(away_matches[away_matches['away_score'] > away_matches['home_score']])
            away_draws = len(away_matches[away_matches['away_score'] == away_matches['home_score']])
            away_losses = len(away_matches[away_matches['away_score'] < away_matches['home_score']])
            
            # Total stats
            total_wins = home_wins + away_wins
            total_draws = home_draws + away_draws
            total_losses = home_losses + away_losses
            
            # Goals
            goals_for = (home_matches['home_score'].sum() + away_matches['away_score'].sum())
            goals_against = (home_matches['away_score'].sum() + away_matches['home_score'].sum())
            
            # Store statistics
            cursor.execute('''
                INSERT OR REPLACE INTO team_stats 
                (team_id, league_key, season, matches_played, wins, draws, losses,
                 goals_for, goals_against, home_wins, home_draws, home_losses,
                 away_wins, away_draws, away_losses)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                team_id, league_key, season, total_matches, total_wins, total_draws, total_losses,
                goals_for, goals_against, home_wins, home_draws, home_losses,
                away_wins, away_draws, away_losses
            ))
        
        conn.commit()
        conn.close()
        print(f"✅ Team statistics calculated for {league_key} {season}")

    def get_league_summary(self) -> Dict:
        """Get summary of all leagues in database"""
        conn = sqlite3.connect(self.db_path)
        
        summary = {}
        for league_key in self.leagues.keys():
            # Count teams
            teams_count = pd.read_sql_query('''
                SELECT COUNT(*) as count FROM teams WHERE league_key = ?
            ''', conn, params=(league_key,)).iloc[0]['count']
            
            # Count matches by season
            matches_by_season = pd.read_sql_query('''
                SELECT season, COUNT(*) as count FROM matches 
                WHERE league_key = ? GROUP BY season
            ''', conn, params=(league_key,))
            
            summary[league_key] = {
                'name': self.leagues[league_key]['name'],
                'teams_count': teams_count,
                'matches_by_season': matches_by_season.to_dict('records')
            }
        
        conn.close()
        return summary

    def export_league_data(self, league_key: str, season: int, output_file: str):
        """Export league data to CSV for ML training"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                m.*,
                ht.name as home_team_name,
                at.name as away_team_name,
                hts.elo_rating as home_elo,
                ats.elo_rating as away_elo,
                hts.form_last_5 as home_form,
                ats.form_last_5 as away_form
            FROM matches m
            JOIN teams ht ON m.home_team_id = ht.team_id
            JOIN teams at ON m.away_team_id = at.team_id
            LEFT JOIN team_stats hts ON m.home_team_id = hts.team_id AND m.season = hts.season
            LEFT JOIN team_stats ats ON m.away_team_id = ats.team_id AND m.season = ats.season
            WHERE m.league_key = ? AND m.season = ? AND m.match_status = 'FT'
            ORDER BY m.match_date
        '''
        
        df = pd.read_sql_query(query, conn, params=(league_key, season))
        df.to_csv(output_file, index=False)
        
        conn.close()
        print(f"✅ {len(df)} matches exported to {output_file}")
        return df

    def setup_all_leagues(self):
        """Setup all leagues with teams and recent matches"""
        print("🚀 Setting up all leagues...")
        
        # Populate leagues
        self.populate_leagues()
        
        # For each league, fetch teams and matches
        for league_key in self.leagues.keys():
            print(f"\n📊 Processing {self.leagues[league_key]['name']}...")
            
            # Fetch teams
            self.fetch_and_store_teams(league_key)
            
            # Fetch matches for recent seasons
            for season in [2023, 2024]:
                self.fetch_and_store_matches(league_key, season)
                self.calculate_team_statistics(league_key, season)
        
        print("\n🎉 All leagues setup completed!")

def main():
    """Main function to demonstrate usage"""
    # Initialize with your API key
    API_KEY = "your_api_key_here"
    
    db_manager = MultiLeagueDBManager(api_key=API_KEY)
    
    # Setup all leagues (run once)
    # db_manager.setup_all_leagues()
    
    # Get summary
    summary = db_manager.get_league_summary()
    
    print("\n📊 DATABASE SUMMARY:")
    print("=" * 50)
    for league_key, info in summary.items():
        print(f"\n🏆 {info['name']}")
        print(f"   Teams: {info['teams_count']}")
        print(f"   Matches by season:")
        for season_data in info['matches_by_season']:
            print(f"     {season_data['season']}: {season_data['count']} matches")
    
    # Export data for ML training
    print("\n📤 Exporting data for ML training...")
    for league_key in ['premier_league', 'la_liga', 'jleague_2']:
        output_file = f"{league_key}_2024_data.csv"
        db_manager.export_league_data(league_key, 2024, output_file)

if __name__ == "__main__":
    main()
