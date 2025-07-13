#!/usr/bin/env python3
"""
Comprehensive Odds Fetcher for All Leagues
ดึง odds จริงสำหรับทุกลีกในวันที่กำหนด
"""

import requests
import json
import time
from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List, Any, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveOddsFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        
        # All leagues from our existing system
        self.leagues = {
            # Major European Leagues
            39: {"name": "Premier League", "country": "England", "weight": 1.2},
            140: {"name": "La Liga", "country": "Spain", "weight": 1.1},
            78: {"name": "Bundesliga", "country": "Germany", "weight": 1.1},
            135: {"name": "Serie A", "country": "Italy", "weight": 1.1},
            61: {"name": "Ligue 1", "country": "France", "weight": 1.0},
            
            # Asian Leagues
            292: {"name": "K League 2", "country": "South Korea", "weight": 0.9},
            98: {"name": "J-League", "country": "Japan", "weight": 0.9},
            169: {"name": "Super League", "country": "China", "weight": 0.8},
            
            # American Leagues
            253: {"name": "MLS", "country": "USA", "weight": 0.9},
            262: {"name": "Liga MX", "country": "Mexico", "weight": 0.9},
            
            # Other Major Leagues
            88: {"name": "Eredivisie", "country": "Netherlands", "weight": 0.9},
            94: {"name": "Primeira Liga", "country": "Portugal", "weight": 0.9},
            203: {"name": "Süper Lig", "country": "Turkey", "weight": 0.8},
            71: {"name": "Serie A", "country": "Brazil", "weight": 0.8},
            128: {"name": "Liga Profesional", "country": "Argentina", "weight": 0.8},
        }
        
        self.db_path = "comprehensive_odds.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Fixtures table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fixtures (
                id INTEGER PRIMARY KEY,
                league_id INTEGER,
                league_name TEXT,
                date TEXT,
                timestamp INTEGER,
                home_team TEXT,
                away_team TEXT,
                status TEXT,
                score_home INTEGER,
                score_away INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Odds table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS odds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fixture_id INTEGER,
                bookmaker TEXT,
                bet_type TEXT,
                bet_name TEXT,
                value TEXT,
                odd REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fixture_id) REFERENCES fixtures (id)
            )
        ''')
        
        # League stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS league_stats (
                league_id INTEGER PRIMARY KEY,
                league_name TEXT,
                total_fixtures INTEGER,
                fixtures_with_odds INTEGER,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def fetch_fixtures_for_date(self, date: str = "2025-07-13") -> Dict[int, List[Dict]]:
        """Fetch all fixtures for all leagues on specific date"""
        all_fixtures = {}
        
        for league_id, league_info in self.leagues.items():
            logger.info(f"Fetching fixtures for {league_info['name']} (ID: {league_id})")
            
            url = f"{self.base_url}/fixtures"
            params = {
                'league': league_id,
                'date': date,
                'season': 2025
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data['results'] > 0:
                    fixtures = data['response']
                    all_fixtures[league_id] = fixtures
                    logger.info(f"Found {len(fixtures)} fixtures for {league_info['name']}")
                    
                    # Save to database
                    self.save_fixtures_to_db(league_id, league_info['name'], fixtures)
                else:
                    logger.info(f"No fixtures found for {league_info['name']}")
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error fetching fixtures for {league_info['name']}: {e}")
                continue
        
        return all_fixtures
    
    def save_fixtures_to_db(self, league_id: int, league_name: str, fixtures: List[Dict]):
        """Save fixtures to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for fixture in fixtures:
            fixture_data = fixture['fixture']
            teams = fixture['teams']
            goals = fixture['goals']
            
            cursor.execute('''
                INSERT OR REPLACE INTO fixtures 
                (id, league_id, league_name, date, timestamp, home_team, away_team, status, score_home, score_away)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                fixture_data['id'],
                league_id,
                league_name,
                fixture_data['date'],
                fixture_data['timestamp'],
                teams['home']['name'],
                teams['away']['name'],
                fixture_data['status']['short'],
                goals['home'] if goals['home'] is not None else 0,
                goals['away'] if goals['away'] is not None else 0
            ))
        
        conn.commit()
        conn.close()
    
    def fetch_odds_for_fixture(self, fixture_id: int) -> Optional[Dict]:
        """Fetch odds for specific fixture"""
        url = f"{self.base_url}/odds"
        params = {
            'fixture': fixture_id
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['results'] > 0:
                return data['response'][0]  # Return first odds data
            return None
            
        except Exception as e:
            logger.error(f"Error fetching odds for fixture {fixture_id}: {e}")
            return None
    
    def fetch_all_odds(self, fixtures_dict: Dict[int, List[Dict]]) -> Dict[int, Dict]:
        """Fetch odds for all fixtures"""
        all_odds = {}
        total_fixtures = sum(len(fixtures) for fixtures in fixtures_dict.values())
        processed = 0
        
        logger.info(f"Starting to fetch odds for {total_fixtures} fixtures")
        
        for league_id, fixtures in fixtures_dict.items():
            league_name = self.leagues[league_id]['name']
            logger.info(f"Processing odds for {league_name}")
            
            for fixture in fixtures:
                fixture_id = fixture['fixture']['id']
                
                # Fetch odds
                odds_data = self.fetch_odds_for_fixture(fixture_id)
                
                if odds_data:
                    all_odds[fixture_id] = odds_data
                    self.save_odds_to_db(fixture_id, odds_data)
                    logger.info(f"✅ Odds saved for fixture {fixture_id}")
                else:
                    logger.warning(f"❌ No odds found for fixture {fixture_id}")
                
                processed += 1
                logger.info(f"Progress: {processed}/{total_fixtures} ({processed/total_fixtures*100:.1f}%)")
                
                # Rate limiting - important for API limits
                time.sleep(1)
        
        return all_odds
    
    def save_odds_to_db(self, fixture_id: int, odds_data: Dict):
        """Save odds data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing odds for this fixture
        cursor.execute('DELETE FROM odds WHERE fixture_id = ?', (fixture_id,))
        
        # Save new odds
        if 'bookmakers' in odds_data:
            for bookmaker in odds_data['bookmakers']:
                bookmaker_name = bookmaker['name']
                
                for bet in bookmaker['bets']:
                    bet_name = bet['name']
                    
                    for value in bet['values']:
                        cursor.execute('''
                            INSERT INTO odds (fixture_id, bookmaker, bet_type, bet_name, value, odd)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            fixture_id,
                            bookmaker_name,
                            'match_winner',  # We'll categorize later
                            bet_name,
                            value['value'],
                            float(value['odd'])
                        ))
        
        conn.commit()
        conn.close()
    
    def get_comprehensive_summary(self) -> Dict:
        """Get comprehensive summary of fetched data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get fixtures summary
        cursor.execute('''
            SELECT league_name, COUNT(*) as fixture_count
            FROM fixtures
            GROUP BY league_name
            ORDER BY fixture_count DESC
        ''')
        fixtures_summary = cursor.fetchall()
        
        # Get odds summary
        cursor.execute('''
            SELECT f.league_name, COUNT(DISTINCT o.fixture_id) as fixtures_with_odds
            FROM fixtures f
            LEFT JOIN odds o ON f.id = o.fixture_id
            WHERE o.fixture_id IS NOT NULL
            GROUP BY f.league_name
            ORDER BY fixtures_with_odds DESC
        ''')
        odds_summary = cursor.fetchall()
        
        # Get total stats
        cursor.execute('SELECT COUNT(*) FROM fixtures')
        total_fixtures = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT fixture_id) FROM odds')
        fixtures_with_odds = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM odds')
        total_odds_records = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_fixtures': total_fixtures,
            'fixtures_with_odds': fixtures_with_odds,
            'total_odds_records': total_odds_records,
            'fixtures_by_league': dict(fixtures_summary),
            'odds_by_league': dict(odds_summary),
            'coverage_percentage': (fixtures_with_odds / total_fixtures * 100) if total_fixtures > 0 else 0
        }
    
    def export_data_for_ml(self, output_file: str = "comprehensive_data_for_ml.json"):
        """Export data in format suitable for ML processing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all fixtures with their odds
        cursor.execute('''
            SELECT 
                f.id, f.league_id, f.league_name, f.date, f.timestamp,
                f.home_team, f.away_team, f.status, f.score_home, f.score_away
            FROM fixtures f
            ORDER BY f.league_id, f.timestamp
        ''')
        
        fixtures = cursor.fetchall()
        ml_data = []
        
        for fixture in fixtures:
            fixture_id = fixture[0]
            
            # Get odds for this fixture
            cursor.execute('''
                SELECT bookmaker, bet_name, value, odd
                FROM odds
                WHERE fixture_id = ?
            ''', (fixture_id,))
            
            odds_data = cursor.fetchall()
            
            # Structure data for ML
            fixture_data = {
                'fixture_id': fixture[0],
                'league_id': fixture[1],
                'league_name': fixture[2],
                'date': fixture[3],
                'timestamp': fixture[4],
                'home_team': fixture[5],
                'away_team': fixture[6],
                'status': fixture[7],
                'score_home': fixture[8],
                'score_away': fixture[9],
                'odds': {}
            }
            
            # Organize odds by bet type
            for bookmaker, bet_name, value, odd in odds_data:
                if bet_name not in fixture_data['odds']:
                    fixture_data['odds'][bet_name] = {}
                if bookmaker not in fixture_data['odds'][bet_name]:
                    fixture_data['odds'][bet_name][bookmaker] = {}
                
                fixture_data['odds'][bet_name][bookmaker][value] = odd
            
            ml_data.append(fixture_data)
        
        conn.close()
        
        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ml_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"ML data exported to {output_file}")
        return ml_data

def main():
    """Main execution function"""
    API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # Initialize fetcher
    fetcher = ComprehensiveOddsFetcher(API_KEY)
    
    print("🚀 Starting Comprehensive Odds Fetching System")
    print("=" * 60)
    
    # Step 1: Fetch all fixtures
    print("📅 Step 1: Fetching fixtures for all leagues...")
    fixtures_dict = fetcher.fetch_fixtures_for_date("2025-07-13")
    
    total_fixtures = sum(len(fixtures) for fixtures in fixtures_dict.values())
    print(f"✅ Found {total_fixtures} fixtures across {len(fixtures_dict)} leagues")
    
    # Step 2: Fetch odds for all fixtures
    print("\n💰 Step 2: Fetching odds for all fixtures...")
    print("⚠️  This may take a while due to API rate limits...")
    
    all_odds = fetcher.fetch_all_odds(fixtures_dict)
    
    # Step 3: Generate summary
    print("\n📊 Step 3: Generating comprehensive summary...")
    summary = fetcher.get_comprehensive_summary()
    
    print("\n" + "=" * 60)
    print("📈 COMPREHENSIVE SUMMARY")
    print("=" * 60)
    print(f"Total Fixtures: {summary['total_fixtures']}")
    print(f"Fixtures with Odds: {summary['fixtures_with_odds']}")
    print(f"Total Odds Records: {summary['total_odds_records']}")
    print(f"Coverage: {summary['coverage_percentage']:.1f}%")
    
    print("\n📋 Fixtures by League:")
    for league, count in summary['fixtures_by_league'].items():
        print(f"  • {league}: {count} fixtures")
    
    print("\n💰 Odds Coverage by League:")
    for league, count in summary['odds_by_league'].items():
        print(f"  • {league}: {count} fixtures with odds")
    
    # Step 4: Export for ML
    print("\n🤖 Step 4: Exporting data for ML processing...")
    ml_data = fetcher.export_data_for_ml()
    
    print(f"✅ Data exported successfully!")
    print(f"📁 Database: {fetcher.db_path}")
    print(f"📁 ML Data: comprehensive_data_for_ml.json")
    
    print("\n🎯 Ready for Advanced ML Processing!")

if __name__ == "__main__":
    main()
