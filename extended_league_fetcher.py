#!/usr/bin/env python3
"""
🌍 Extended League Matches Fetcher
ระบบดึงข้อมูลการแข่งขันจากลีกเพิ่มเติมตามที่ร้องขอ

Leagues:
- FIFA Club World Cup 2025
- Norway Tippeligaen
- Sweden Allsvenskan  
- Finland Veikkausliiga
- Romania Super League
- Israeli Super Cup
- Iceland Premier League
- Poland Super Cup
- Finland Ykkonen
- Korea Division 2
- Brazil Serie A & B
- Argentina Primera Division & B Nacional
- Colombia Primera Division
- Mexico Primera Division
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtendedLeagueFetcher:
    """ระบบดึงข้อมูลลีกเพิ่มเติม"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        
        # Extended leagues configuration
        self.extended_leagues = {
            # FIFA Club World Cup
            1: {"name": "FIFA Club World Cup", "country": "World", "weight": 1.5, "priority": 1},
            
            # European Leagues
            103: {"name": "Eliteserien", "country": "Norway", "weight": 1.0, "priority": 2},
            113: {"name": "Allsvenskan", "country": "Sweden", "weight": 1.0, "priority": 2},
            244: {"name": "Veikkausliiga", "country": "Finland", "weight": 0.9, "priority": 3},
            283: {"name": "Liga I", "country": "Romania", "weight": 0.8, "priority": 3},
            383: {"name": "Ligat ha'Al", "country": "Israel", "weight": 0.7, "priority": 4},
            165: {"name": "Úrvalsdeild", "country": "Iceland", "weight": 0.6, "priority": 4},
            106: {"name": "Ekstraklasa", "country": "Poland", "weight": 0.9, "priority": 3},
            1087: {"name": "Ykkösliiga", "country": "Finland", "weight": 0.7, "priority": 4},
            
            # Asian Leagues
            294: {"name": "K League 2", "country": "South Korea", "weight": 0.8, "priority": 3},
            
            # South American Leagues
            71: {"name": "Serie A", "country": "Brazil", "weight": 1.3, "priority": 1},
            72: {"name": "Serie B", "country": "Brazil", "weight": 1.1, "priority": 2},
            128: {"name": "Primera División", "country": "Argentina", "weight": 1.2, "priority": 1},
            129: {"name": "Primera B Nacional", "country": "Argentina", "weight": 0.9, "priority": 3},
            239: {"name": "Primera A", "country": "Colombia", "weight": 1.0, "priority": 2},
            262: {"name": "Liga MX", "country": "Mexico", "weight": 1.1, "priority": 2}
        }
    
    def get_fixtures_by_date_range(self, start_date: str, end_date: str) -> Dict:
        """ดึงข้อมูลการแข่งขันตามช่วงวันที่"""
        url = f"{self.base_url}/fixtures"
        params = {
            'from': start_date,
            'to': end_date
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching fixtures: {e}")
            return {}
    
    def filter_extended_leagues(self, fixtures_data: Dict) -> List[Dict]:
        """กรองเฉพาะลีกที่ต้องการ"""
        if not fixtures_data.get('response'):
            return []
        
        extended_fixtures = []
        for fixture in fixtures_data['response']:
            league_id = fixture['league']['id']
            if league_id in self.extended_leagues:
                # Add league info
                league_info = self.extended_leagues[league_id]
                fixture['league_weight'] = league_info['weight']
                fixture['league_priority'] = league_info['priority']
                fixture['league_info'] = league_info
                extended_fixtures.append(fixture)
        
        return extended_fixtures
    
    def process_extended_fixtures(self, fixtures: List[Dict]) -> pd.DataFrame:
        """แปลงข้อมูลเป็น DataFrame"""
        processed_data = []
        
        for fixture in fixtures:
            # Convert timestamp to local time
            match_time = datetime.fromtimestamp(fixture['fixture']['timestamp'], tz=pytz.UTC)
            local_time = match_time.astimezone()
            
            match_data = {
                'fixture_id': fixture['fixture']['id'],
                'date': fixture['fixture']['date'],
                'timestamp': fixture['fixture']['timestamp'],
                'league_id': fixture['league']['id'],
                'league_name': fixture['league']['name'],
                'league_country': fixture['league']['country'],
                'league_weight': fixture.get('league_weight', 1.0),
                'league_priority': fixture.get('league_priority', 5),
                'season': fixture['league']['season'],
                'round': fixture['league']['round'],
                'home_team_id': fixture['teams']['home']['id'],
                'home_team': fixture['teams']['home']['name'],
                'away_team_id': fixture['teams']['away']['id'],
                'away_team': fixture['teams']['away']['name'],
                'venue': fixture['fixture']['venue']['name'] if fixture['fixture']['venue'] else 'TBD',
                'city': fixture['fixture']['venue']['city'] if fixture['fixture']['venue'] else 'TBD',
                'status': fixture['fixture']['status']['long'],
                'status_short': fixture['fixture']['status']['short'],
                'match_time_utc': match_time.strftime('%H:%M UTC'),
                'match_time_local': local_time.strftime('%H:%M %Z'),
                'match_date_local': local_time.strftime('%Y-%m-%d'),
                'is_today': local_time.date() == datetime.now().date(),
                'is_tomorrow': local_time.date() == (datetime.now() + timedelta(days=1)).date()
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
            
            processed_data.append(match_data)
        
        return pd.DataFrame(processed_data)
    
    def generate_extended_html(self, df: pd.DataFrame) -> str:
        """สร้าง HTML สำหรับแสดงผลในหน้า index"""
        if df.empty:
            return "<p>No matches found for the specified period.</p>"
        
        # Sort by priority and time
        df_sorted = df.sort_values(['league_priority', 'timestamp'])
        
        html = """
        <div class="extended-matches-container">
            <h2>🌍 Extended League Matches (Today - Tomorrow 12:00)</h2>
            <div class="matches-summary">
                <div class="summary-stats">
                    <span class="stat-item">📊 Total: {total_matches}</span>
                    <span class="stat-item">🏆 Leagues: {total_leagues}</span>
                    <span class="stat-item">🌍 Countries: {total_countries}</span>
                </div>
            </div>
        """.format(
            total_matches=len(df),
            total_leagues=df['league_name'].nunique(),
            total_countries=df['league_country'].nunique()
        )
        
        # Group by priority and league
        priority_groups = df_sorted.groupby('league_priority')
        
        for priority, priority_df in priority_groups:
            priority_name = {
                1: "🔥 Top Priority",
                2: "⭐ High Priority", 
                3: "✅ Medium Priority",
                4: "📋 Standard Priority",
                5: "📝 Low Priority"
            }.get(priority, "📋 Other")
            
            html += f"""
            <div class="priority-section priority-{priority}">
                <h3>{priority_name}</h3>
                <div class="leagues-grid">
            """
            
            # Group by league within priority
            league_groups = priority_df.groupby(['league_name', 'league_country'])
            
            for (league_name, country), league_df in league_groups:
                league_weight = league_df.iloc[0]['league_weight']
                
                html += f"""
                <div class="league-section">
                    <div class="league-header">
                        <h4>🏆 {league_name}</h4>
                        <span class="league-info">
                            <span class="country">{country}</span>
                            <span class="weight">Weight: {league_weight}</span>
                        </span>
                    </div>
                    <div class="matches-list">
                """
                
                for _, match in league_df.iterrows():
                    # Status styling
                    if match['status_short'] == 'NS':
                        status_class = 'not-started'
                        status_icon = '🔴'
                    elif match['status_short'] == 'FT':
                        status_class = 'finished'
                        status_icon = '✅'
                    elif match['status_short'] in ['1H', '2H', 'HT']:
                        status_class = 'live'
                        status_icon = '🔴'
                    else:
                        status_class = 'other'
                        status_icon = '⚪'
                    
                    # Time display
                    time_display = match['match_time_local']
                    if match['is_tomorrow']:
                        time_display = f"Tomorrow {time_display}"
                    
                    html += f"""
                    <div class="match-card {status_class}">
                        <div class="match-header">
                            <span class="status">{status_icon} {match['status']}</span>
                            <span class="time">{time_display}</span>
                        </div>
                        <div class="match-teams">
                            <div class="home-team">{match['home_team']}</div>
                            <div class="vs">VS</div>
                            <div class="away-team">{match['away_team']}</div>
                        </div>
                        <div class="match-info">
                            <small>{match['venue']}, {match['city']}</small>
                        </div>
                        <div class="match-round">
                            <small>{match['round']}</small>
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
            """
        
        html += """
        </div>
        
        <style>
        .extended-matches-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .matches-summary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            color: white;
            text-align: center;
        }
        
        .summary-stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
        }
        
        .priority-section {
            margin-bottom: 40px;
            border-radius: 15px;
            padding: 20px;
        }
        
        .priority-1 { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }
        .priority-2 { background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); }
        .priority-3 { background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%); }
        .priority-4 { background: linear-gradient(135deg, #1dd1a1 0%, #10ac84 100%); }
        .priority-5 { background: linear-gradient(135deg, #a4b0be 0%, #747d8c 100%); }
        
        .priority-section h3 {
            color: white;
            margin: 0 0 20px 0;
            font-size: 1.3em;
        }
        
        .leagues-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }
        
        .league-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .league-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            color: white;
        }
        
        .league-header h4 {
            margin: 0;
            font-size: 1.1em;
        }
        
        .league-info {
            display: flex;
            gap: 10px;
            font-size: 0.85em;
        }
        
        .country, .weight {
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 8px;
            border-radius: 12px;
        }
        
        .matches-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .match-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 12px;
            border-left: 4px solid #ddd;
        }
        
        .match-card.not-started {
            border-left-color: #e74c3c;
        }
        
        .match-card.live {
            border-left-color: #f39c12;
            animation: pulse 2s infinite;
        }
        
        .match-card.finished {
            border-left-color: #27ae60;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        
        .match-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.85em;
            color: #666;
        }
        
        .match-teams {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 10px 0;
            font-weight: bold;
            color: #333;
        }
        
        .vs {
            background: #f8f9fa;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.8em;
            color: #666;
        }
        
        .match-info, .match-round {
            text-align: center;
            color: #666;
            font-size: 0.8em;
        }
        
        .match-round {
            margin-top: 5px;
            font-style: italic;
        }
        
        @media (max-width: 768px) {
            .leagues-grid {
                grid-template-columns: 1fr;
            }
            
            .summary-stats {
                flex-direction: column;
                gap: 10px;
            }
        }
        </style>
        """
        
        return html
    
    def run_extended_analysis(self, days_ahead: int = 1) -> Dict:
        """รันการวิเคราะห์ลีกเพิ่มเติม"""
        logger.info("🌍 Starting Extended League Analysis...")
        
        # Calculate date range (today to tomorrow 12:00)
        today = datetime.now().strftime('%Y-%m-%d')
        tomorrow_noon = (datetime.now() + timedelta(days=days_ahead)).replace(hour=12, minute=0, second=0)
        end_date = tomorrow_noon.strftime('%Y-%m-%d')
        
        logger.info(f"📅 Date range: {today} to {end_date}")
        
        # Fetch fixtures
        fixtures_data = self.get_fixtures_by_date_range(today, end_date)
        if not fixtures_data:
            logger.error("Failed to fetch fixtures data")
            return {}
        
        logger.info(f"📊 Total fixtures found: {fixtures_data.get('results', 0)}")
        
        # Filter extended leagues
        extended_fixtures = self.filter_extended_leagues(fixtures_data)
        logger.info(f"🏆 Extended league fixtures: {len(extended_fixtures)}")
        
        if not extended_fixtures:
            logger.warning("No extended league fixtures found")
            return {}
        
        # Process fixtures
        df = self.process_extended_fixtures(extended_fixtures)
        
        # Filter for matches until tomorrow 12:00
        tomorrow_noon_ts = tomorrow_noon.timestamp()
        df_filtered = df[df['timestamp'] <= tomorrow_noon_ts]
        
        logger.info(f"⏰ Matches until tomorrow 12:00: {len(df_filtered)}")
        
        # Generate HTML
        html_content = self.generate_extended_html(df_filtered)
        
        # Save files
        csv_file = f"extended_matches_{datetime.now().strftime('%Y%m%d')}.csv"
        html_file = f"extended_matches_report_{datetime.now().strftime('%Y%m%d')}.html"
        
        df_filtered.to_csv(csv_file, index=False, encoding='utf-8')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Extended League Matches - {datetime.now().strftime('%Y-%m-%d')}</title>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """)
        
        # Generate summary
        league_summary = df_filtered.groupby(['league_name', 'league_country']).size().to_dict()
        priority_summary = df_filtered.groupby('league_priority').size().to_dict()
        
        results = {
            'total_matches': len(df_filtered),
            'leagues_covered': df_filtered['league_name'].nunique(),
            'countries_covered': df_filtered['league_country'].nunique(),
            'league_breakdown': league_summary,
            'priority_breakdown': priority_summary,
            'csv_file': csv_file,
            'html_file': html_file,
            'html_content': html_content,
            'dataframe': df_filtered
        }
        
        logger.info("✅ Extended analysis completed successfully!")
        return results

def main():
    """Main function for testing"""
    API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # Initialize fetcher
    fetcher = ExtendedLeagueFetcher(API_KEY)
    
    # Run analysis
    results = fetcher.run_extended_analysis()
    
    if results:
        print("\n🌍 Extended League Analysis Summary:")
        print(f"📊 Total Matches: {results['total_matches']}")
        print(f"🏆 Leagues Covered: {results['leagues_covered']}")
        print(f"🌍 Countries: {results['countries_covered']}")
        print(f"📁 CSV File: {results['csv_file']}")
        print(f"🌐 HTML File: {results['html_file']}")
        
        print("\n📈 League Breakdown:")
        for league_info, count in list(results['league_breakdown'].items())[:10]:
            print(f"  • {league_info}: {count} matches")
        
        print("\n🎯 Priority Breakdown:")
        for priority, count in results['priority_breakdown'].items():
            priority_name = {
                1: "Top Priority",
                2: "High Priority", 
                3: "Medium Priority",
                4: "Standard Priority",
                5: "Low Priority"
            }.get(priority, "Other")
            print(f"  • {priority_name}: {count} matches")
    else:
        print("❌ No matches found or error occurred")

if __name__ == "__main__":
    main()
