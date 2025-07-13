#!/usr/bin/env python3
"""
🚀 Today Matches Fetcher System
ระบบดึงข้อมูลการแข่งขันวันนี้แบบเรียลไทม์

Features:
- ดึงข้อมูลการแข่งขันจาก API-Sports
- กรองลีกสำคัญ (Premier League, La Liga, Bundesliga, Serie A, Ligue 1, J-League 2)
- สร้างตารางสำหรับการทำนาย
- Export เป็น CSV และ HTML
- รองรับ Multi-league analysis
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional, Tuple
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TodayMatchesFetcher:
    """ระบบดึงข้อมูลการแข่งขันวันนี้"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        
        # Major leagues configuration
        self.major_leagues = {
            39: {"name": "Premier League", "country": "England", "weight": 1.2},
            140: {"name": "La Liga", "country": "Spain", "weight": 1.1},
            78: {"name": "Bundesliga", "country": "Germany", "weight": 1.1},
            135: {"name": "Serie A", "country": "Italy", "weight": 1.1},
            61: {"name": "Ligue 1", "country": "France", "weight": 1.0},
            293: {"name": "K League 2", "country": "South Korea", "weight": 0.9}  # J-League 2 equivalent
        }
        
    def get_today_fixtures(self, date: Optional[str] = None) -> Dict:
        """ดึงข้อมูลการแข่งขันวันนี้"""
        if not date:
            # Get today's date in UTC
            today = datetime.now(pytz.UTC).strftime('%Y-%m-%d')
        else:
            today = date
            
        url = f"{self.base_url}/fixtures"
        params = {'date': today}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching fixtures: {e}")
            return {}
    
    def filter_major_leagues(self, fixtures_data: Dict) -> List[Dict]:
        """กรองเฉพาะลีกสำคัญ"""
        if not fixtures_data.get('response'):
            return []
        
        major_fixtures = []
        for fixture in fixtures_data['response']:
            league_id = fixture['league']['id']
            if league_id in self.major_leagues:
                # Add league weight and info
                fixture['league_weight'] = self.major_leagues[league_id]['weight']
                fixture['league_info'] = self.major_leagues[league_id]
                major_fixtures.append(fixture)
        
        return major_fixtures
    
    def process_fixtures_for_prediction(self, fixtures: List[Dict]) -> pd.DataFrame:
        """แปลงข้อมูลเป็น DataFrame สำหรับการทำนาย"""
        processed_data = []
        
        for fixture in fixtures:
            # Extract basic info
            match_data = {
                'fixture_id': fixture['fixture']['id'],
                'date': fixture['fixture']['date'],
                'timestamp': fixture['fixture']['timestamp'],
                'league_id': fixture['league']['id'],
                'league_name': fixture['league']['name'],
                'league_country': fixture['league']['country'],
                'league_weight': fixture.get('league_weight', 1.0),
                'season': fixture['league']['season'],
                'round': fixture['league']['round'],
                'home_team_id': fixture['teams']['home']['id'],
                'home_team': fixture['teams']['home']['name'],
                'away_team_id': fixture['teams']['away']['id'],
                'away_team': fixture['teams']['away']['name'],
                'venue': fixture['fixture']['venue']['name'] if fixture['fixture']['venue'] else 'TBD',
                'city': fixture['fixture']['venue']['city'] if fixture['fixture']['venue'] else 'TBD',
                'status': fixture['fixture']['status']['long'],
                'status_short': fixture['fixture']['status']['short']
            }
            
            # Add goals if match is finished
            if fixture['goals']['home'] is not None:
                match_data.update({
                    'home_goals': fixture['goals']['home'],
                    'away_goals': fixture['goals']['away'],
                    'total_goals': fixture['goals']['home'] + fixture['goals']['away']
                })
            else:
                match_data.update({
                    'home_goals': None,
                    'away_goals': None,
                    'total_goals': None
                })
            
            # Convert timestamp to readable time
            match_time = datetime.fromtimestamp(fixture['fixture']['timestamp'], tz=pytz.UTC)
            match_data['match_time_utc'] = match_time.strftime('%H:%M UTC')
            match_data['match_time_local'] = match_time.astimezone().strftime('%H:%M %Z')
            
            processed_data.append(match_data)
        
        return pd.DataFrame(processed_data)
    
    def generate_prediction_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """สร้างตารางสำหรับการทำนาย"""
        if df.empty:
            return pd.DataFrame()
        
        # Sort by league weight (descending) and match time
        df_sorted = df.sort_values(['league_weight', 'timestamp'], ascending=[False, True])
        
        # Create prediction table
        prediction_table = df_sorted[[
            'fixture_id', 'league_name', 'league_country', 'league_weight',
            'home_team', 'away_team', 'match_time_utc', 'match_time_local',
            'venue', 'city', 'status', 'round'
        ]].copy()
        
        # Add prediction columns (to be filled by ML models)
        prediction_columns = [
            'predicted_result',  # Home/Draw/Away
            'result_confidence',
            'predicted_handicap',
            'handicap_confidence', 
            'predicted_over_under',
            'ou_confidence',
            'predicted_corners_1h',
            'corners_1h_confidence',
            'predicted_corners_2h',
            'corners_2h_confidence',
            'value_bet_rating',
            'recommended_bet'
        ]
        
        for col in prediction_columns:
            prediction_table[col] = 'TBD'
        
        return prediction_table
    
    def export_to_csv(self, df: pd.DataFrame, filename: str = None) -> str:
        """Export ข้อมูลเป็น CSV"""
        if filename is None:
            today = datetime.now().strftime('%Y%m%d')
            filename = f"today_matches_{today}.csv"
        
        filepath = os.path.join(os.getcwd(), filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"Data exported to: {filepath}")
        return filepath
    
    def generate_html_table(self, df: pd.DataFrame) -> str:
        """สร้างตาราง HTML สำหรับแสดงผล"""
        if df.empty:
            return "<p>No matches found for today.</p>"
        
        html = """
        <div class="matches-container">
            <h2>🔥 Today's Major League Matches</h2>
            <div class="matches-grid">
        """
        
        # Group by league
        for league_name in df['league_name'].unique():
            league_matches = df[df['league_name'] == league_name]
            league_weight = league_matches.iloc[0]['league_weight']
            league_country = league_matches.iloc[0]['league_country']
            
            html += f"""
            <div class="league-section">
                <h3>🏆 {league_name} ({league_country}) - Weight: {league_weight}</h3>
                <div class="matches-list">
            """
            
            for _, match in league_matches.iterrows():
                status_icon = "🔴" if match['status'] == 'Not Started' else "⚽"
                html += f"""
                <div class="match-card">
                    <div class="match-header">
                        <span class="status">{status_icon} {match['status']}</span>
                        <span class="time">{match['match_time_local']}</span>
                    </div>
                    <div class="match-teams">
                        <div class="home-team">{match['home_team']}</div>
                        <div class="vs">VS</div>
                        <div class="away-team">{match['away_team']}</div>
                    </div>
                    <div class="match-info">
                        <small>{match['venue']}, {match['city']}</small>
                    </div>
                    <div class="predictions">
                        <div class="pred-item">Result: <span class="pred-value">{match.get('predicted_result', 'TBD')}</span></div>
                        <div class="pred-item">O/U: <span class="pred-value">{match.get('predicted_over_under', 'TBD')}</span></div>
                        <div class="pred-item">Value: <span class="pred-value">{match.get('value_bet_rating', 'TBD')}</span></div>
                    </div>
                </div>
                """
            
            html += """
                </div>
            </div>
            """
        
        html += """
            </div>
        </div>
        
        <style>
        .matches-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .league-section {
            margin-bottom: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 20px;
            color: white;
        }
        
        .league-section h3 {
            margin: 0 0 15px 0;
            font-size: 1.2em;
        }
        
        .matches-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        
        .match-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .match-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 0.9em;
        }
        
        .match-teams {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 15px 0;
            font-weight: bold;
        }
        
        .vs {
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
        }
        
        .match-info {
            text-align: center;
            margin: 10px 0;
            opacity: 0.8;
        }
        
        .predictions {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            font-size: 0.85em;
        }
        
        .pred-item {
            text-align: center;
        }
        
        .pred-value {
            display: block;
            font-weight: bold;
            color: #FFD700;
        }
        </style>
        """
        
        return html
    
    def save_html_report(self, html_content: str, filename: str = None) -> str:
        """บันทึกรายงาน HTML"""
        if filename is None:
            today = datetime.now().strftime('%Y%m%d')
            filename = f"today_matches_report_{today}.html"
        
        filepath = os.path.join(os.getcwd(), filename)
        
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Today's Football Matches - {datetime.now().strftime('%Y-%m-%d')}</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        logger.info(f"HTML report saved to: {filepath}")
        return filepath
    
    def run_daily_analysis(self, date: Optional[str] = None) -> Dict:
        """รันการวิเคราะห์รายวัน"""
        logger.info("🚀 Starting Today Matches Analysis...")
        
        # Fetch today's fixtures
        fixtures_data = self.get_today_fixtures(date)
        if not fixtures_data:
            logger.error("Failed to fetch fixtures data")
            return {}
        
        logger.info(f"📊 Total fixtures found: {fixtures_data.get('results', 0)}")
        
        # Filter major leagues
        major_fixtures = self.filter_major_leagues(fixtures_data)
        logger.info(f"🏆 Major league fixtures: {len(major_fixtures)}")
        
        if not major_fixtures:
            logger.warning("No major league fixtures found for today")
            return {}
        
        # Process fixtures
        df = self.process_fixtures_for_prediction(major_fixtures)
        prediction_table = self.generate_prediction_table(df)
        
        # Export data
        csv_file = self.export_to_csv(prediction_table)
        html_content = self.generate_html_table(prediction_table)
        html_file = self.save_html_report(html_content)
        
        # Summary statistics
        league_summary = df.groupby(['league_name', 'league_country']).size().to_dict()
        
        results = {
            'total_matches': len(df),
            'leagues_covered': len(df['league_name'].unique()),
            'league_breakdown': league_summary,
            'csv_file': csv_file,
            'html_file': html_file,
            'dataframe': prediction_table,
            'raw_data': major_fixtures
        }
        
        logger.info("✅ Analysis completed successfully!")
        return results

def main():
    """Main function for testing"""
    # API key (replace with your actual key)
    API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # Initialize fetcher
    fetcher = TodayMatchesFetcher(API_KEY)
    
    # Run analysis
    results = fetcher.run_daily_analysis()
    
    if results:
        print("\n🎯 Today's Matches Analysis Summary:")
        print(f"📊 Total Matches: {results['total_matches']}")
        print(f"🏆 Leagues Covered: {results['leagues_covered']}")
        print(f"📁 CSV File: {results['csv_file']}")
        print(f"🌐 HTML File: {results['html_file']}")
        
        print("\n📈 League Breakdown:")
        for league_info, count in results['league_breakdown'].items():
            print(f"  • {league_info}: {count} matches")
        
        # Display first few matches
        if not results['dataframe'].empty:
            print("\n🔥 Sample Matches:")
            sample_df = results['dataframe'][['league_name', 'home_team', 'away_team', 'match_time_local']].head()
            print(sample_df.to_string(index=False))
    else:
        print("❌ No matches found or error occurred")

if __name__ == "__main__":
    main()
