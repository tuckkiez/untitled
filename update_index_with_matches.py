#!/usr/bin/env python3
"""
🌐 Index Page Updater with Extended League Matches
อัปเดทหน้า index.html ด้วยข้อมูลการแข่งขันจากลีกเพิ่มเติม
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
import os
from typing import Dict, List, Optional

class IndexPageUpdater:
    """ระบบอัปเดทหน้า index"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        
        # Extended leagues with correct IDs
        self.leagues = {
            # Top Priority - Major Tournaments
            1: {"name": "FIFA Club World Cup", "country": "World", "priority": 1, "flag": "🌍"},
            
            # High Priority - Major South American
            71: {"name": "Serie A", "country": "Brazil", "priority": 1, "flag": "🇧🇷"},
            72: {"name": "Serie B", "country": "Brazil", "priority": 2, "flag": "🇧🇷"},
            128: {"name": "Primera División", "country": "Argentina", "priority": 1, "flag": "🇦🇷"},
            129: {"name": "Primera B Nacional", "country": "Argentina", "priority": 2, "flag": "🇦🇷"},
            239: {"name": "Primera A", "country": "Colombia", "priority": 2, "flag": "🇨🇴"},
            262: {"name": "Liga MX", "country": "Mexico", "priority": 2, "flag": "🇲🇽"},
            
            # Medium Priority - European
            103: {"name": "Eliteserien", "country": "Norway", "priority": 2, "flag": "🇳🇴"},
            113: {"name": "Allsvenskan", "country": "Sweden", "priority": 2, "flag": "🇸🇪"},
            244: {"name": "Veikkausliiga", "country": "Finland", "priority": 3, "flag": "🇫🇮"},
            283: {"name": "Liga I", "country": "Romania", "priority": 3, "flag": "🇷🇴"},
            106: {"name": "Ekstraklasa", "country": "Poland", "priority": 3, "flag": "🇵🇱"},
            
            # Lower Priority - Others
            383: {"name": "Ligat ha'Al", "country": "Israel", "priority": 4, "flag": "🇮🇱"},
            165: {"name": "Úrvalsdeild", "country": "Iceland", "priority": 4, "flag": "🇮🇸"},
            1087: {"name": "Ykkösliiga", "country": "Finland", "priority": 4, "flag": "🇫🇮"},
            294: {"name": "K League 2", "country": "South Korea", "priority": 3, "flag": "🇰🇷"},
        }
    
    def get_recent_fixtures(self, days_back: int = 1, days_forward: int = 2) -> Dict:
        """ดึงข้อมูลการแข่งขันย้อนหลังและข้างหน้า"""
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=days_forward)).strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/fixtures"
        params = {
            'from': start_date,
            'to': end_date
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching fixtures: {e}")
            return {}
    
    def process_fixtures(self, fixtures_data: Dict) -> pd.DataFrame:
        """ประมวลผลข้อมูลการแข่งขัน"""
        if not fixtures_data.get('response'):
            return pd.DataFrame()
        
        processed_data = []
        
        for fixture in fixtures_data['response']:
            league_id = fixture['league']['id']
            
            # Skip if not in our target leagues
            if league_id not in self.leagues:
                continue
            
            league_info = self.leagues[league_id]
            match_time = datetime.fromtimestamp(fixture['fixture']['timestamp'], tz=pytz.UTC)
            local_time = match_time.astimezone()
            
            match_data = {
                'fixture_id': fixture['fixture']['id'],
                'league_id': league_id,
                'league_name': fixture['league']['name'],
                'league_country': fixture['league']['country'],
                'league_flag': league_info['flag'],
                'priority': league_info['priority'],
                'home_team': fixture['teams']['home']['name'],
                'away_team': fixture['teams']['away']['name'],
                'status': fixture['fixture']['status']['long'],
                'status_short': fixture['fixture']['status']['short'],
                'venue': fixture['fixture']['venue']['name'] if fixture['fixture']['venue'] else 'TBD',
                'city': fixture['fixture']['venue']['city'] if fixture['fixture']['venue'] else 'TBD',
                'round': fixture['league']['round'],
                'match_time_local': local_time.strftime('%m/%d %H:%M'),
                'match_date': local_time.strftime('%Y-%m-%d'),
                'is_today': local_time.date() == datetime.now().date(),
                'is_live': fixture['fixture']['status']['short'] in ['1H', '2H', 'HT', 'ET', 'P'],
                'is_finished': fixture['fixture']['status']['short'] == 'FT'
            }
            
            # Add scores if available
            if fixture['goals']['home'] is not None:
                match_data['home_goals'] = fixture['goals']['home']
                match_data['away_goals'] = fixture['goals']['away']
                match_data['score'] = f"{fixture['goals']['home']}-{fixture['goals']['away']}"
            else:
                match_data['home_goals'] = None
                match_data['away_goals'] = None
                match_data['score'] = 'vs'
            
            processed_data.append(match_data)
        
        return pd.DataFrame(processed_data)
    
    def generate_matches_html(self, df: pd.DataFrame) -> str:
        """สร้าง HTML สำหรับแสดงการแข่งขัน"""
        if df.empty:
            return """
            <div class="no-matches">
                <h3>🔍 No Extended League Matches Found</h3>
                <p>ไม่พบการแข่งขันจากลีกเพิ่มเติมในช่วงเวลานี้</p>
            </div>
            """
        
        # Sort by priority and time
        df_sorted = df.sort_values(['priority', 'fixture_id'])
        
        html = f"""
        <div class="extended-matches-section">
            <div class="section-header">
                <h2>🌍 Extended League Matches</h2>
                <div class="matches-stats">
                    <span class="stat">📊 {len(df)} matches</span>
                    <span class="stat">🏆 {df['league_name'].nunique()} leagues</span>
                    <span class="stat">🌍 {df['league_country'].nunique()} countries</span>
                </div>
            </div>
            
            <div class="matches-container">
        """
        
        # Group by priority
        priority_groups = df_sorted.groupby('priority')
        
        for priority, group_df in priority_groups:
            priority_names = {
                1: "🔥 Top Priority",
                2: "⭐ High Priority",
                3: "✅ Medium Priority", 
                4: "📋 Standard Priority"
            }
            
            html += f"""
            <div class="priority-group priority-{priority}">
                <h3>{priority_names.get(priority, '📋 Other')}</h3>
                <div class="matches-grid">
            """
            
            # Group by league
            league_groups = group_df.groupby(['league_name', 'league_country', 'league_flag'])
            
            for (league_name, country, flag), league_df in league_groups:
                html += f"""
                <div class="league-block">
                    <div class="league-title">
                        <span class="flag">{flag}</span>
                        <span class="name">{league_name}</span>
                        <span class="country">({country})</span>
                    </div>
                    <div class="league-matches">
                """
                
                for _, match in league_df.iterrows():
                    # Status styling
                    if match['is_live']:
                        status_class = 'live'
                        status_icon = '🔴'
                    elif match['is_finished']:
                        status_class = 'finished'
                        status_icon = '✅'
                    else:
                        status_class = 'upcoming'
                        status_icon = '⏰'
                    
                    html += f"""
                    <div class="match-item {status_class}">
                        <div class="match-status">
                            <span class="icon">{status_icon}</span>
                            <span class="time">{match['match_time_local']}</span>
                        </div>
                        <div class="match-teams">
                            <span class="home">{match['home_team']}</span>
                            <span class="score">{match['score']}</span>
                            <span class="away">{match['away_team']}</span>
                        </div>
                        <div class="match-details">
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
        </div>
        
        <style>
        .extended-matches-section {
            margin: 30px 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            color: white;
        }
        
        .section-header {
            text-align: center;
            margin-bottom: 25px;
        }
        
        .section-header h2 {
            margin: 0 0 10px 0;
            font-size: 1.8em;
        }
        
        .matches-stats {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .stat {
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .priority-group {
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
        }
        
        .priority-group h3 {
            margin: 0 0 15px 0;
            font-size: 1.2em;
        }
        
        .matches-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 15px;
        }
        
        .league-block {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 15px;
            color: #333;
        }
        
        .league-title {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            font-weight: bold;
            border-bottom: 2px solid #eee;
            padding-bottom: 8px;
        }
        
        .flag {
            font-size: 1.2em;
        }
        
        .name {
            flex: 1;
        }
        
        .country {
            font-size: 0.85em;
            color: #666;
        }
        
        .league-matches {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .match-item {
            padding: 10px;
            border-radius: 6px;
            border-left: 4px solid #ddd;
        }
        
        .match-item.live {
            background: #fff3cd;
            border-left-color: #ffc107;
            animation: pulse 2s infinite;
        }
        
        .match-item.finished {
            background: #d4edda;
            border-left-color: #28a745;
        }
        
        .match-item.upcoming {
            background: #f8f9fa;
            border-left-color: #6c757d;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.8; }
            100% { opacity: 1; }
        }
        
        .match-status {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
            font-size: 0.85em;
            color: #666;
        }
        
        .match-teams {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .score {
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        .match-details {
            text-align: center;
            color: #666;
            font-size: 0.8em;
        }
        
        @media (max-width: 768px) {
            .matches-grid {
                grid-template-columns: 1fr;
            }
            
            .matches-stats {
                flex-direction: column;
                gap: 10px;
            }
        }
        </style>
        """
        
        return html
    
    def update_index_page(self, matches_html: str, csv_data: pd.DataFrame):
        """อัปเดทหน้า index.html"""
        index_path = "index.html"
        
        # Save CSV
        csv_filename = f"extended_matches_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        csv_data.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f"📁 CSV saved: {csv_filename}")
        
        # Check if index.html exists
        if not os.path.exists(index_path):
            # Create new index.html
            html_content = f"""
            <!DOCTYPE html>
            <html lang="th">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>🚀 Ultra Advanced Football Predictor</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    .header {{
                        text-align: center;
                        color: white;
                        margin-bottom: 30px;
                    }}
                    .header h1 {{
                        font-size: 2.5em;
                        margin: 0;
                    }}
                    .last-updated {{
                        text-align: center;
                        color: white;
                        margin-top: 30px;
                        opacity: 0.8;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🚀 Ultra Advanced Football Predictor</h1>
                        <p>ระบบทำนายฟุตบอลขั้นสูงพร้อมข้อมูลแบบเรียลไทม์</p>
                    </div>
                    
                    {matches_html}
                    
                    <div class="last-updated">
                        <p>📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p>📊 Data from API-Sports | 🔄 Auto-refresh every hour</p>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            # Read existing index.html
            with open(index_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Replace or insert matches section
            if '<!-- EXTENDED_MATCHES_SECTION -->' in html_content:
                # Replace existing section
                start_marker = '<!-- EXTENDED_MATCHES_SECTION -->'
                end_marker = '<!-- /EXTENDED_MATCHES_SECTION -->'
                
                start_idx = html_content.find(start_marker)
                end_idx = html_content.find(end_marker)
                
                if start_idx != -1 and end_idx != -1:
                    html_content = (
                        html_content[:start_idx] +
                        f'{start_marker}\n{matches_html}\n{end_marker}' +
                        html_content[end_idx + len(end_marker):]
                    )
            else:
                # Insert before closing body tag
                insert_content = f"""
                <!-- EXTENDED_MATCHES_SECTION -->
                {matches_html}
                <!-- /EXTENDED_MATCHES_SECTION -->
                """
                
                html_content = html_content.replace('</body>', f'{insert_content}\n</body>')
        
        # Write updated HTML
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🌐 Index page updated: {index_path}")
    
    def run_update(self):
        """รันการอัปเดท"""
        print("🌍 Starting Extended League Matches Update...")
        
        # Fetch fixtures
        fixtures_data = self.get_recent_fixtures(days_back=1, days_forward=3)
        
        if not fixtures_data:
            print("❌ Failed to fetch fixtures data")
            return
        
        print(f"📊 Total fixtures found: {fixtures_data.get('results', 0)}")
        
        # Process fixtures
        df = self.process_fixtures(fixtures_data)
        
        if df.empty:
            print("⚠️ No matches found from target leagues")
            # Still create HTML with no matches message
            matches_html = self.generate_matches_html(df)
            self.update_index_page(matches_html, df)
            return
        
        print(f"🏆 Target league matches: {len(df)}")
        print(f"📈 Leagues: {df['league_name'].nunique()}")
        print(f"🌍 Countries: {df['league_country'].nunique()}")
        
        # Generate HTML
        matches_html = self.generate_matches_html(df)
        
        # Update index page
        self.update_index_page(matches_html, df)
        
        # Show summary
        print("\n📋 League Summary:")
        league_summary = df.groupby(['league_name', 'league_country']).size()
        for (league, country), count in league_summary.items():
            print(f"  • {league} ({country}): {count} matches")
        
        print("\n✅ Update completed successfully!")

def main():
    """Main function"""
    API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    updater = IndexPageUpdater(API_KEY)
    updater.run_update()

if __name__ == "__main__":
    main()
