#!/usr/bin/env python3
"""
🚀 Update with Real API Data - อัปเดต HTML ด้วยข้อมูลจริงจาก API
ใช้ข้อมูลจริงจาก API-Sports วันที่ 13 กรกฎาคม 2025
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from real_api_data_fetcher import RealAPIDataFetcher
from multi_league_table_predictor import MultiLeagueTablePredictor
import subprocess
from datetime import datetime
import pytz
import re

class RealAPIUpdater:
    def __init__(self, api_key):
        self.api_key = api_key
        self.fetcher = RealAPIDataFetcher(api_key)
        self.predictor = MultiLeagueTablePredictor(api_key)
        self.index_path = '/Users/80090/Desktop/Project/untitle/index.html'
        
    def convert_api_data_to_predictions(self, categorized_matches):
        """แปลงข้อมูล API เป็นรูปแบบการทำนาย"""
        predictions = []
        
        for league_name, matches in categorized_matches.items():
            for match in matches:
                # สร้างข้อมูลการแข่งขัน
                match_data = {
                    'league_name': match['league_name'],
                    'league_flag': league_name.split()[0] if league_name.startswith(('🇰🇷', '🇺🇸', '🇲🇽', '🇧🇷', '🇨🇴', '🇸🇪', '🇳🇴', '🇫🇮', '🇨🇳', '🇯🇵')) else '🌍',
                    'home_team': match['home_team'],
                    'away_team': match['away_team'],
                    'venue': match['venue'],
                    'time': self.format_time(match['date']),
                    'status': match['status'],
                    'league_weight': self.get_league_weight(match['league_id'])
                }
                
                # ทำนายผล
                prediction = self.predictor.predict_match(match_data)
                
                predictions.append({
                    'match': match_data,
                    'predictions': prediction
                })
        
        return predictions
    
    def format_time(self, date_str):
        """แปลงเวลาให้อ่านง่าย"""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            # แปลงเป็น ICT (UTC+7)
            ict_time = dt.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('Asia/Bangkok'))
            return ict_time.strftime('%H:%M ICT')
        except:
            return "TBD"
    
    def get_league_weight(self, league_id):
        """กำหนดน้ำหนักลีก"""
        weights = {
            39: 1.2,   # Premier League
            140: 1.1,  # La Liga
            78: 1.1,   # Bundesliga
            135: 1.1,  # Serie A
            61: 1.0,   # Ligue 1
            293: 0.9,  # K League 2
            253: 1.0,  # MLS
            262: 1.0,  # Liga MX
            71: 1.0,   # Serie A Brazil
            239: 0.9,  # Primera A Colombia
        }
        return weights.get(league_id, 0.8)
    
    def generate_clean_html(self, predictions):
        """สร้าง HTML ใหม่ทั้งหมดด้วย Dark Theme และข้อมูลจริง"""
        
        if not predictions:
            return ""
        
        # จัดกลุ่มตามลีก
        leagues_data = {}
        for pred in predictions:
            league_name = pred['match']['league_name']
            league_flag = pred['match']['league_flag']
            
            if league_name not in leagues_data:
                leagues_data[league_name] = {
                    'flag': league_flag,
                    'matches': []
                }
            leagues_data[league_name]['matches'].append(pred)
        
        # สร้างแถวตารางสำหรับแต่ละการแข่งขัน
        table_rows = ""
        
        for league_name, league_data in leagues_data.items():
            # Header แยกลีก
            table_rows += f"""
                <tr class="league-header">
                    <td colspan="5" class="league-title">
                        {league_data['flag']} <strong>{league_name}</strong>
                    </td>
                </tr>
            """
            
            # แถวการแข่งขันในลีกนั้น (แสดงแค่ 5 นัดแรกต่อลีก)
            for pred in league_data['matches'][:5]:
                match = pred['match']
                p = pred['predictions']
                
                # สีสำหรับความมั่นใจ
                def get_confidence_class(confidence):
                    if confidence >= 75:
                        return "high-confidence"
                    elif confidence >= 65:
                        return "medium-confidence"
                    else:
                        return "low-confidence"
                
                mr_class = get_confidence_class(p['match_result']['confidence'])
                hc_class = get_confidence_class(p['handicap']['confidence'])
                ou_class = get_confidence_class(p['over_under']['confidence'])
                co_class = get_confidence_class(p['corners']['confidence'])
                
                # Status emoji
                status_emoji = "✅" if match['status'] == 'FT' else "🔴" if match['status'] in ['1H', '2H', 'HT'] else "⏰"
                
                table_rows += f"""
                    <tr class="match-row">
                        <td class="match-teams">
                            <div class="teams-info">
                                <strong>{status_emoji} {match['home_team']} vs {match['away_team']}</strong>
                                <div class="match-details">
                                    <span>⏰ {match['time']}</span>
                                    <span>📍 {match['venue']}</span>
                                </div>
                            </div>
                        </td>
                        <td class="prediction-cell {mr_class}">
                            <div class="prediction-main">{p['match_result']['prediction']}</div>
                            <div class="confidence">{p['match_result']['confidence']}%</div>
                        </td>
                        <td class="prediction-cell {hc_class}">
                            <div class="handicap-line">{p['handicap']['line']}</div>
                            <div class="handicap-rec">{p['handicap']['prediction']}</div>
                            <div class="confidence">{p['handicap']['confidence']}%</div>
                        </td>
                        <td class="prediction-cell {ou_class}">
                            <div class="prediction-main">{p['over_under']['prediction']}</div>
                            <div class="confidence">{p['over_under']['confidence']}%</div>
                        </td>
                        <td class="prediction-cell {co_class}">
                            <div class="prediction-main">{p['corners']['prediction']}</div>
                            <div class="confidence">{p['corners']['confidence']}%</div>
                        </td>
                    </tr>
                """
        
        # นับสถิติ
        total_matches = len(predictions)
        leagues_count = len(leagues_data)
        
        # สร้าง HTML ใหม่ทั้งหมด
        html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Multi-League Football Predictor - Real API Data</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 50%, #2d2d2d 100%);
            color: #ffffff;
            min-height: 100vh;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .main-header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 0;
            background: linear-gradient(135deg, #1e1e1e 0%, #3a3a3a 100%);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        .main-header h1 {{
            font-size: 3em;
            margin-bottom: 15px;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 3s ease-in-out infinite;
        }}
        
        @keyframes gradientShift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .main-header p {{
            font-size: 1.2em;
            opacity: 0.8;
            margin-bottom: 10px;
        }}
        
        .league-stats {{
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin: 30px 0;
        }}
        
        .stat-badge {{
            background: linear-gradient(135deg, #333 0%, #555 100%);
            padding: 12px 25px;
            border-radius: 25px;
            font-size: 0.95em;
            border: 1px solid #444;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}
        
        .stat-badge:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            border-color: #666;
        }}
        
        .predictions-section {{
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
            border: 1px solid #333;
        }}
        
        .section-title {{
            text-align: center;
            font-size: 2.2em;
            margin-bottom: 30px;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .predictions-table-container {{
            overflow-x: auto;
            margin: 20px 0;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}
        
        .predictions-table {{
            width: 100%;
            border-collapse: collapse;
            background: linear-gradient(135deg, #222 0%, #333 100%);
            border-radius: 15px;
            overflow: hidden;
        }}
        
        .predictions-table th {{
            background: linear-gradient(135deg, #333 0%, #444 100%);
            padding: 18px 12px;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
            border-bottom: 2px solid #555;
            color: #fff;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        
        .league-header td {{
            background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%) !important;
            padding: 15px;
            font-size: 1.3em;
            font-weight: bold;
            text-align: center;
            border-top: 2px solid #444;
            border-bottom: 1px solid #444;
        }}
        
        .league-title {{
            color: #ffd700 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        }}
        
        .match-row td {{
            padding: 16px 12px;
            text-align: center;
            border-bottom: 1px solid #333;
            transition: all 0.3s ease;
        }}
        
        .match-row:hover td {{
            background: rgba(255,255,255,0.05) !important;
        }}
        
        .match-teams {{
            text-align: left !important;
            min-width: 300px;
        }}
        
        .teams-info strong {{
            display: block;
            font-size: 1.15em;
            margin-bottom: 6px;
            color: #fff;
        }}
        
        .match-details {{
            font-size: 0.9em;
            opacity: 0.7;
            color: #ccc;
        }}
        
        .match-details span {{
            display: inline-block;
            margin-right: 15px;
        }}
        
        .prediction-cell {{
            min-width: 140px;
            transition: all 0.3s ease;
        }}
        
        .prediction-main {{
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 4px;
            color: #fff;
        }}
        
        .handicap-line {{
            font-weight: bold;
            color: #ffc107;
            margin-bottom: 4px;
            font-size: 0.95em;
        }}
        
        .handicap-rec {{
            font-size: 0.85em;
            margin-bottom: 4px;
            color: #ddd;
        }}
        
        .confidence {{
            font-size: 0.8em;
            opacity: 0.8;
            color: #bbb;
        }}
        
        /* สีตามความมั่นใจ - Dark Theme */
        .high-confidence {{
            background: linear-gradient(135deg, rgba(40, 167, 69, 0.2) 0%, rgba(40, 167, 69, 0.3) 100%) !important;
            border-left: 4px solid #28a745;
            box-shadow: inset 0 0 10px rgba(40, 167, 69, 0.1);
        }}
        
        .medium-confidence {{
            background: linear-gradient(135deg, rgba(255, 193, 7, 0.2) 0%, rgba(255, 193, 7, 0.3) 100%) !important;
            border-left: 4px solid #ffc107;
            box-shadow: inset 0 0 10px rgba(255, 193, 7, 0.1);
        }}
        
        .low-confidence {{
            background: linear-gradient(135deg, rgba(220, 53, 69, 0.2) 0%, rgba(220, 53, 69, 0.3) 100%) !important;
            border-left: 4px solid #dc3545;
            box-shadow: inset 0 0 10px rgba(220, 53, 69, 0.1);
        }}
        
        .legend {{
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #222 0%, #333 100%);
            border-radius: 15px;
            text-align: center;
            border: 1px solid #444;
        }}
        
        .legend h3 {{
            margin-bottom: 20px;
            font-size: 1.4em;
            color: #fff;
        }}
        
        .legend-items {{
            display: flex;
            justify-content: center;
            gap: 25px;
            flex-wrap: wrap;
        }}
        
        .legend-item {{
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }}
        
        .legend-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        
        .legend-item.high-confidence {{
            background: linear-gradient(135deg, rgba(40, 167, 69, 0.3) 0%, rgba(40, 167, 69, 0.4) 100%);
            border: 1px solid #28a745;
        }}
        
        .legend-item.medium-confidence {{
            background: linear-gradient(135deg, rgba(255, 193, 7, 0.3) 0%, rgba(255, 193, 7, 0.4) 100%);
            border: 1px solid #ffc107;
        }}
        
        .legend-item.low-confidence {{
            background: linear-gradient(135deg, rgba(220, 53, 69, 0.3) 0%, rgba(220, 53, 69, 0.4) 100%);
            border: 1px solid #dc3545;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 25px;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            border-radius: 15px;
            border: 1px solid #333;
        }}
        
        .footer p {{
            margin: 8px 0;
            opacity: 0.8;
            color: #ccc;
        }}
        
        .update-time {{
            color: #ffc107 !important;
            font-weight: bold;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            .main-header h1 {{
                font-size: 2.2em;
            }}
            
            .league-stats {{
                flex-direction: column;
                align-items: center;
            }}
            
            .predictions-table th,
            .predictions-table td {{
                padding: 12px 8px;
                font-size: 0.9em;
            }}
            
            .match-teams {{
                min-width: 250px;
            }}
            
            .prediction-cell {{
                min-width: 120px;
            }}
            
            .legend-items {{
                flex-direction: column;
                align-items: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="main-header">
            <h1>🚀 Multi-League Football Predictor</h1>
            <p>ระบบทำนายฟุตบอลหลายลีกขั้นสูงด้วย Advanced Machine Learning</p>
            <p>🌙 Dark Theme Edition - 📡 Real API Data</p>
        </header>
        
        <div class="league-stats">
            <span class="stat-badge">🏆 {leagues_count} Leagues</span>
            <span class="stat-badge">⚽ {total_matches} Matches</span>
            <span class="stat-badge">🤖 Advanced ML</span>
            <span class="stat-badge">📡 Real API Data</span>
            <span class="stat-badge">🌙 Dark Theme</span>
        </div>
        
        <section class="predictions-section">
            <h2 class="section-title">📊 Today's Predictions - July 13, 2025</h2>
            
            <div class="predictions-table-container">
                <table class="predictions-table">
                    <thead>
                        <tr>
                            <th>การแข่งขัน</th>
                            <th>🎯 ผลการแข่งขัน</th>
                            <th>⚖️ Handicap</th>
                            <th>⚽ Over/Under 2.5</th>
                            <th>📐 Corners</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
            
            <div class="legend">
                <h3>🔍 คำอธิบาย</h3>
                <div class="legend-items">
                    <span class="legend-item high-confidence">🟢 มั่นใจสูง (75%+)</span>
                    <span class="legend-item medium-confidence">🟡 มั่นใจปานกลาง (65-74%)</span>
                    <span class="legend-item low-confidence">🔴 มั่นใจต่ำ (<65%)</span>
                </div>
            </div>
        </section>
        
        <footer class="footer">
            <p>🤖 Powered by Advanced Machine Learning & Real API Data</p>
            <p>📊 4-Value Prediction System: Result | Handicap | Over/Under | Corners</p>
            <p>🏆 Multi-League Coverage: Real-time data from API-Sports</p>
            <p class="update-time">Last Updated: {datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%d %H:%M:%S ICT')}</p>
            <p>📡 Real API Data Integration - July 13, 2025</p>
        </footer>
    </div>
</body>
</html>"""
        
        return html_content
