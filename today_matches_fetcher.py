#!/usr/bin/env python3
"""
📅 Today Matches Fetcher
ดึงแมตช์วันนี้จาก API-Football และสร้างตารางการแข่งขัน
วันที่ 13 กรกฎาคม หลังเที่ยง ถึง 14 กรกฎาคม ก่อนเที่ยง (เวลาไทย)
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import json
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

class TodayMatchesFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        
        # Major leagues to focus on
        self.target_leagues = {
            39: 'Premier League',
            140: 'La Liga', 
            78: 'Bundesliga',
            61: 'Ligue 1',
            135: 'Serie A',
            99: 'J-League 2',
            88: 'Eredivisie',
            94: 'Primeira Liga',
            203: 'Turkish Super League',
            144: 'Belgian Pro League'
        }
        
        print("📅 Today Matches Fetcher initialized!")
        print(f"🎯 Targeting {len(self.target_leagues)} major leagues")

    def get_today_matches(self) -> List[Dict]:
        """ดึงแมตช์วันนี้ตามเวลาไทย (13 ก.ค. หลังเที่ยง - 14 ก.ค. ก่อนเที่ยง)"""
        
        # กำหนดช่วงเวลา (เวลาไทย UTC+7)
        thailand_tz = pytz.timezone('Asia/Bangkok')
        
        # วันที่ 13 กรกฎาคม 2025 เที่ยง (12:00) เวลาไทย
        start_time = thailand_tz.localize(datetime(2025, 7, 13, 12, 0, 0))
        # วันที่ 14 กรกฎาคม 2025 เที่ยง (12:00) เวลาไทย  
        end_time = thailand_tz.localize(datetime(2025, 7, 14, 12, 0, 0))
        
        # แปลงเป็น UTC สำหรับ API
        start_utc = start_time.astimezone(pytz.UTC)
        end_utc = end_time.astimezone(pytz.UTC)
        
        print(f"🕐 ช่วงเวลาที่ค้นหา:")
        print(f"   เริ่ม: {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"   สิ้นสุด: {end_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        all_matches = []
        
        try:
            # ดึงแมตช์วันที่ 13 กรกฎาคม
            matches_13 = self._fetch_matches_by_date("2025-07-13")
            # ดึงแมตช์วันที่ 14 กรกฎาคม  
            matches_14 = self._fetch_matches_by_date("2025-07-14")
            
            # รวมแมตช์ทั้งหมด
            all_fixtures = matches_13 + matches_14
            
            # กรองตามช่วงเวลาและลีกที่ต้องการ
            for fixture in all_fixtures:
                match_time_str = fixture['fixture']['date']
                match_time_utc = datetime.fromisoformat(match_time_str.replace('Z', '+00:00'))
                match_time_utc = match_time_utc.replace(tzinfo=pytz.UTC)
                
                # ตรวจสอบว่าอยู่ในช่วงเวลาที่กำหนด
                if start_utc <= match_time_utc < end_utc:
                    league_id = fixture['league']['id']
                    
                    # ตรวจสอบว่าเป็นลีกที่เราสนใจ
                    if league_id in self.target_leagues:
                        match_data = self._extract_match_data(fixture)
                        if match_data:
                            all_matches.append(match_data)
            
            print(f"✅ พบแมตช์ทั้งหมด {len(all_matches)} แมตช์")
            return all_matches
            
        except Exception as e:
            print(f"❌ Error fetching today matches: {e}")
            return []

    def _fetch_matches_by_date(self, date: str) -> List[Dict]:
        """ดึงแมตช์ตามวันที่"""
        try:
            url = f"{self.base_url}/fixtures"
            params = {'date': date}
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data['response']
            else:
                print(f"⚠️ API Error for date {date}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching matches for {date}: {e}")
            return []

    def _extract_match_data(self, fixture: Dict) -> Dict:
        """แยกข้อมูลแมตช์ที่ต้องการ"""
        try:
            # แปลงเวลาเป็นเวลาไทย
            match_time_str = fixture['fixture']['date']
            match_time_utc = datetime.fromisoformat(match_time_str.replace('Z', '+00:00'))
            match_time_utc = match_time_utc.replace(tzinfo=pytz.UTC)
            thailand_time = match_time_utc.astimezone(pytz.timezone('Asia/Bangkok'))
            
            # ดึงราคาต่อรอง (ถ้ามี)
            odds_data = self._get_match_odds(fixture['fixture']['id'])
            
            match_data = {
                'fixture_id': fixture['fixture']['id'],
                'league': self.target_leagues.get(fixture['league']['id'], fixture['league']['name']),
                'league_id': fixture['league']['id'],
                'match_time_thai': thailand_time.strftime('%H:%M'),
                'match_date_thai': thailand_time.strftime('%Y-%m-%d'),
                'home_team': fixture['teams']['home']['name'],
                'away_team': fixture['teams']['away']['name'],
                'home_team_id': fixture['teams']['home']['id'],
                'away_team_id': fixture['teams']['away']['id'],
                'venue': fixture['fixture']['venue']['name'] if fixture['fixture']['venue'] else 'TBD',
                'status': fixture['fixture']['status']['short'],
                
                # ราคาต่อรอง
                'odds_home': odds_data.get('home', 'N/A'),
                'odds_draw': odds_data.get('draw', 'N/A'), 
                'odds_away': odds_data.get('away', 'N/A'),
                'odds_over_25': odds_data.get('over_25', 'N/A'),
                'odds_under_25': odds_data.get('under_25', 'N/A'),
                
                # ผลบอล (ถ้าแข่งเสร็จแล้ว)
                'home_score': fixture['goals']['home'] if fixture['goals']['home'] is not None else '',
                'away_score': fixture['goals']['away'] if fixture['goals']['away'] is not None else '',
                'match_result': self._get_match_result(fixture),
                
                # Prediction columns (เว้นไว้ก่อน)
                'prediction_home_away': '',
                'prediction_handicap': '',
                'prediction_over_under': '',
                'prediction_score': '',
                'prediction_corner_1st_half': '',
                'prediction_corner_full_match': '',
                
                # Additional info
                'referee': fixture['fixture']['referee'] if fixture['fixture']['referee'] else 'TBD'
            }
            
            return match_data
            
        except Exception as e:
            print(f"⚠️ Error extracting match data: {e}")
            return None

    def _get_match_odds(self, fixture_id: int) -> Dict[str, Any]:
        """ดึงราคาต่อรองของแมตช์"""
        try:
            url = f"{self.base_url}/odds"
            params = {
                'fixture': fixture_id,
                'bookmaker': 8  # Bet365
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['response']:
                    odds_data = data['response'][0]
                    bookmaker = odds_data['bookmakers'][0] if odds_data['bookmakers'] else None
                    
                    if bookmaker:
                        odds = {}
                        for bet in bookmaker['bets']:
                            if bet['name'] == 'Match Winner':
                                for value in bet['values']:
                                    if value['value'] == 'Home':
                                        odds['home'] = float(value['odd'])
                                    elif value['value'] == 'Draw':
                                        odds['draw'] = float(value['odd'])
                                    elif value['value'] == 'Away':
                                        odds['away'] = float(value['odd'])
                            
                            elif bet['name'] == 'Goals Over/Under':
                                for value in bet['values']:
                                    if '2.5' in value['value']:
                                        if 'Over' in value['value']:
                                            odds['over_25'] = float(value['odd'])
                                        elif 'Under' in value['value']:
                                            odds['under_25'] = float(value['odd'])
                        
                        return odds
            
            # Return default if no odds found
            return {}
            
        except Exception as e:
            print(f"⚠️ Error getting odds for fixture {fixture_id}: {e}")
            return {}

    def _get_match_result(self, fixture: Dict) -> str:
        """ได้ผลแมตช์ (ถ้าแข่งเสร็จแล้ว)"""
        if fixture['fixture']['status']['short'] == 'FT':
            home_score = fixture['goals']['home']
            away_score = fixture['goals']['away']
            
            if home_score > away_score:
                return 'Home Win'
            elif home_score < away_score:
                return 'Away Win'
            else:
                return 'Draw'
        return ''

    def create_matches_dataframe(self, matches: List[Dict]) -> pd.DataFrame:
        """สร้าง DataFrame จากข้อมูลแมตช์"""
        if not matches:
            return pd.DataFrame()
        
        df = pd.DataFrame(matches)
        
        # เรียงลำดับตามเวลาและลีก
        df = df.sort_values(['match_time_thai', 'league'])
        
        # จัดเรียง columns ตามที่ต้องการ
        column_order = [
            'league', 'match_time_thai', 'home_team', 'odds_home', 'odds_draw', 'odds_away',
            'away_team', 'home_score', 'away_score', 'match_result',
            'prediction_home_away', 'prediction_handicap', 'prediction_over_under',
            'prediction_score', 'prediction_corner_1st_half', 'prediction_corner_full_match',
            'venue', 'referee', 'fixture_id'
        ]
        
        # เลือกเฉพาะ columns ที่มี
        available_columns = [col for col in column_order if col in df.columns]
        df = df[available_columns]
        
        return df

    def save_to_csv(self, df: pd.DataFrame, filename: str = "today_matches.csv"):
        """บันทึกข้อมูลลง CSV"""
        try:
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"✅ บันทึกข้อมูลลง {filename} เรียบร้อย ({len(df)} แมตช์)")
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")

    def create_today_matches_website(self, df: pd.DataFrame):
        """สร้างหน้าเว็บแสดงแมตช์วันนี้"""
        
        html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚽ Today Matches - {datetime.now().strftime('%d/%m/%Y')}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .header .subtitle {{
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 15px;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .stat-item {{
            text-align: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }}

        .stat-number {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #667eea;
        }}

        .stat-label {{
            font-size: 0.9rem;
            color: #666;
        }}

        .matches-table {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 10px;
            text-align: center;
            font-weight: 600;
            font-size: 0.9rem;
        }}

        td {{
            padding: 12px 10px;
            text-align: center;
            border-bottom: 1px solid #eee;
            font-size: 0.9rem;
        }}

        tr:hover {{
            background-color: rgba(102, 126, 234, 0.05);
        }}

        .league-name {{
            font-weight: 600;
            color: #667eea;
        }}

        .team-name {{
            font-weight: 500;
            color: #333;
        }}

        .odds {{
            font-weight: 600;
            color: #28a745;
        }}

        .time {{
            font-weight: 600;
            color: #dc3545;
        }}

        .score {{
            font-weight: 700;
            color: #fd7e14;
            font-size: 1.1rem;
        }}

        .prediction-placeholder {{
            color: #999;
            font-style: italic;
        }}

        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            color: #666;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            table {{
                font-size: 0.8rem;
            }}
            
            th, td {{
                padding: 8px 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚽ Today Matches</h1>
            <div class="subtitle">การแข่งขันฟุตบอลวันนี้ - {datetime.now().strftime('%d %B %Y')}</div>
            <div class="subtitle">🕐 เวลาไทย | 💰 ราคาต่อรอง | 🔮 การทำนาย (เร็วๆ นี้)</div>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{len(df)}</div>
                    <div class="stat-label">แมตช์ทั้งหมด</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(df['league'].unique())}</div>
                    <div class="stat-label">ลีก</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(df[df['match_result'] == ''])}</div>
                    <div class="stat-label">ยังไม่แข่ง</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(df[df['match_result'] != ''])}</div>
                    <div class="stat-label">แข่งเสร็จแล้ว</div>
                </div>
            </div>
        </div>

        <div class="matches-table">
            <table>
                <thead>
                    <tr>
                        <th>ลีก</th>
                        <th>เวลา</th>
                        <th>เจ้าบ้าน</th>
                        <th>ราคาต่อรอง</th>
                        <th>ทีมเยือน</th>
                        <th>ผลบอล</th>
                        <th>Prediction<br>Home/Away</th>
                        <th>Prediction<br>Handicap</th>
                        <th>Over/Under</th>
                        <th>Score</th>
                        <th>Corner<br>1st Half</th>
                        <th>Corner<br>Full Match</th>
                    </tr>
                </thead>
                <tbody>"""
        
        # เพิ่มข้อมูลแมตช์
        for _, match in df.iterrows():
            # จัดรูปแบบราคาต่อรอง
            odds_display = f"{match.get('odds_home', 'N/A')} | {match.get('odds_draw', 'N/A')} | {match.get('odds_away', 'N/A')}"
            
            # จัดรูปแบบผลบอล
            if match.get('home_score') != '' and match.get('away_score') != '':
                score_display = f"{match['home_score']}-{match['away_score']}"
            else:
                score_display = "vs"
            
            html_content += f"""
                    <tr>
                        <td class="league-name">{match['league']}</td>
                        <td class="time">{match['match_time_thai']}</td>
                        <td class="team-name">{match['home_team']}</td>
                        <td class="odds">{odds_display}</td>
                        <td class="team-name">{match['away_team']}</td>
                        <td class="score">{score_display}</td>
                        <td class="prediction-placeholder">เร็วๆ นี้</td>
                        <td class="prediction-placeholder">เร็วๆ นี้</td>
                        <td class="prediction-placeholder">เร็วๆ นี้</td>
                        <td class="prediction-placeholder">เร็วๆ นี้</td>
                        <td class="prediction-placeholder">เร็วๆ นี้</td>
                        <td class="prediction-placeholder">เร็วๆ นี้</td>
                    </tr>"""
        
        html_content += """
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>🤖 ระบบการทำนายด้วย Advanced ML กำลังคำนวณ...</p>
            <p>📊 ข้อมูลจาก API-Football | อัปเดตล่าสุด: """ + datetime.now().strftime('%H:%M:%S') + """</p>
        </div>
    </div>
</body>
</html>"""
        
        # บันทึกไฟล์ HTML
        with open('today_matches.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ สร้างหน้าเว็บ today_matches.html เรียบร้อย")

def main():
    """ฟังก์ชันหลักสำหรับรันระบบ"""
    # ใส่ API Key ของคุณที่นี่
    API_KEY = "your_api_key_here"
    
    if API_KEY == "your_api_key_here":
        print("❌ กรุณาใส่ API Key ใน API_KEY variable")
        return
    
    print("🚀 เริ่มดึงข้อมูลแมตช์วันนี้...")
    print("=" * 50)
    
    # สร้าง fetcher
    fetcher = TodayMatchesFetcher(API_KEY)
    
    # ดึงแมตช์วันนี้
    matches = fetcher.get_today_matches()
    
    if matches:
        # สร้าง DataFrame
        df = fetcher.create_matches_dataframe(matches)
        
        # แสดงข้อมูลสรุป
        print(f"\n📊 สรุปข้อมูล:")
        print(f"   แมตช์ทั้งหมด: {len(df)}")
        print(f"   ลีกที่พบ: {', '.join(df['league'].unique())}")
        print(f"   ช่วงเวลา: {df['match_time_thai'].min()} - {df['match_time_thai'].max()}")
        
        # บันทึก CSV
        fetcher.save_to_csv(df)
        
        # สร้างหน้าเว็บ
        fetcher.create_today_matches_website(df)
        
        # แสดงตัวอย่างข้อมูล
        print(f"\n📋 ตัวอย่างข้อมูล 5 แมตช์แรก:")
        print(df[['league', 'match_time_thai', 'home_team', 'away_team', 'odds_home', 'odds_away']].head())
        
        print(f"\n🎉 เสร็จสิ้น! ไฟล์ที่สร้าง:")
        print(f"   📄 today_matches.csv - ข้อมูล CSV")
        print(f"   🌐 today_matches.html - หน้าเว็บ")
        
    else:
        print("❌ ไม่พบแมตช์ในช่วงเวลาที่กำหนด")

if __name__ == "__main__":
    main()
