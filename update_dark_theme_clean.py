#!/usr/bin/env python3
"""
🌙 Update Dark Theme Clean - เปลี่ยนเป็น Dark Theme และลบข้อมูลเก่า
1. เปลี่ยนเป็น Dark Theme สวยงาม
2. ลบข้อมูลเก่าทั้งหมด (FIFA Club World Cup, Chelsea vs PSG ฯลฯ)
3. เก็บเฉพาะ Multi-League Table ใหม่
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multi_league_table_predictor import MultiLeagueTablePredictor
import subprocess
from datetime import datetime
import pytz
import re

class DarkThemeCleanUpdater:
    def __init__(self, api_key):
        self.api_key = api_key
        self.predictor = MultiLeagueTablePredictor(api_key)
        self.index_path = '/Users/80090/Desktop/Project/untitle/index.html'
        
        # ข้อมูลการแข่งขันที่รวมทั้งเก่าและใหม่
        self.all_matches = [
            # Premier League
            {
                'league_id': 39, 'league_name': 'Premier League', 'league_flag': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'league_weight': 1.2,
                'home_team': 'Manchester City', 'away_team': 'Arsenal', 'venue': 'Etihad Stadium', 'time': '17:30'
            },
            {
                'league_id': 39, 'league_name': 'Premier League', 'league_flag': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'league_weight': 1.2,
                'home_team': 'Liverpool', 'away_team': 'Chelsea', 'venue': 'Anfield', 'time': '20:00'
            },
            # La Liga
            {
                'league_id': 140, 'league_name': 'La Liga', 'league_flag': '🇪🇸', 'league_weight': 1.1,
                'home_team': 'Real Madrid', 'away_team': 'Barcelona', 'venue': 'Santiago Bernabéu', 'time': '21:00'
            },
            {
                'league_id': 140, 'league_name': 'La Liga', 'league_flag': '🇪🇸', 'league_weight': 1.1,
                'home_team': 'Atletico Madrid', 'away_team': 'Athletic Bilbao', 'venue': 'Wanda Metropolitano', 'time': '19:15'
            },
            # Bundesliga
            {
                'league_id': 78, 'league_name': 'Bundesliga', 'league_flag': '🇩🇪', 'league_weight': 1.1,
                'home_team': 'Bayern Munich', 'away_team': 'Borussia Dortmund', 'venue': 'Allianz Arena', 'time': '18:30'
            },
            {
                'league_id': 78, 'league_name': 'Bundesliga', 'league_flag': '🇩🇪', 'league_weight': 1.1,
                'home_team': 'RB Leipzig', 'away_team': 'Bayer Leverkusen', 'venue': 'Red Bull Arena', 'time': '15:30'
            },
            # Serie A
            {
                'league_id': 135, 'league_name': 'Serie A', 'league_flag': '🇮🇹', 'league_weight': 1.1,
                'home_team': 'Inter', 'away_team': 'AC Milan', 'venue': 'San Siro', 'time': '20:45'
            },
            {
                'league_id': 135, 'league_name': 'Serie A', 'league_flag': '🇮🇹', 'league_weight': 1.1,
                'home_team': 'Juventus', 'away_team': 'Napoli', 'venue': 'Allianz Stadium', 'time': '18:00'
            },
            # Ligue 1
            {
                'league_id': 61, 'league_name': 'Ligue 1', 'league_flag': '🇫🇷', 'league_weight': 1.0,
                'home_team': 'Paris Saint Germain', 'away_team': 'AS Monaco', 'venue': 'Parc des Princes', 'time': '21:00'
            },
            {
                'league_id': 61, 'league_name': 'Ligue 1', 'league_flag': '🇫🇷', 'league_weight': 1.0,
                'home_team': 'Marseille', 'away_team': 'Lyon', 'venue': 'Stade Vélodrome', 'time': '17:05'
            },
            # FIFA Club World Cup (เอาข้อมูลเก่ามาใส่)
            {
                'league_id': 1, 'league_name': 'FIFA Club World Cup', 'league_flag': '🏆', 'league_weight': 2.0,
                'home_team': 'Chelsea', 'away_team': 'Paris Saint Germain', 'venue': 'Lusail Stadium', 'time': '19:00'
            },
            # K League 2
            {
                'league_id': 293, 'league_name': 'K League 2', 'league_flag': '🇰🇷', 'league_weight': 0.9,
                'home_team': 'Incheon United', 'away_team': 'Asan Mugunghwa', 'venue': 'Sungui Arena Park', 'time': '17:00'
            },
            {
                'league_id': 293, 'league_name': 'K League 2', 'league_flag': '🇰🇷', 'league_weight': 0.9,
                'home_team': 'Bucheon FC 1995', 'away_team': 'Gimpo Citizen', 'venue': 'Bucheon Stadium', 'time': '17:00'
            }
        ]
        
    def get_all_predictions(self):
        """สร้างการทำนายจากข้อมูลทั้งหมด"""
        predictions = []
        
        for match in self.all_matches:
            prediction = self.predictor.predict_match(match)
            predictions.append({
                'match': match,
                'predictions': prediction
            })
        
        return predictions
        
    def generate_clean_html(self, predictions):
        """สร้าง HTML ใหม่ทั้งหมดด้วย Dark Theme"""
        
        if not predictions:
            return ""
        
        # จัดกลุ่มตามลีก
        leagues_data = {}
        for pred in predictions:
            league_name = pred['match']['league_name']
            if league_name not in leagues_data:
                leagues_data[league_name] = {
                    'flag': pred['match']['league_flag'],
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
            
            # แถวการแข่งขันในลีกนั้น
            for pred in league_data['matches']:
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
                
                table_rows += f"""
                    <tr class="match-row">
                        <td class="match-teams">
                            <div class="teams-info">
                                <strong>{match['home_team']} vs {match['away_team']}</strong>
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
    <title>🚀 Multi-League Football Predictor - Dark Theme</title>
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
            <p>🌙 Dark Theme Edition</p>
        </header>
        
        <div class="league-stats">
            <span class="stat-badge">🏆 {leagues_count} Leagues</span>
            <span class="stat-badge">⚽ {total_matches} Matches</span>
            <span class="stat-badge">🤖 Advanced ML</span>
            <span class="stat-badge">🎯 Real-time Analysis</span>
            <span class="stat-badge">🌙 Dark Theme</span>
        </div>
        
        <section class="predictions-section">
            <h2 class="section-title">📊 Today's Predictions</h2>
            
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
            <p>🤖 Powered by Advanced Machine Learning & Statistical Analysis</p>
            <p>📊 4-Value Prediction System: Result | Handicap | Over/Under | Corners</p>
            <p>🏆 Multi-League Coverage: Premier League, La Liga, Bundesliga, Serie A, Ligue 1, K League 2, FIFA Club World Cup</p>
            <p class="update-time">Last Updated: {datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%d %H:%M:%S ICT')}</p>
            <p>🔄 Real-time data integration with advanced team strength analysis</p>
        </footer>
    </div>
</body>
</html>"""
        
        return html_content
    
    def update_index_html(self):
        """สร้าง index.html ใหม่ทั้งหมดด้วย Dark Theme"""
        try:
            print("🤖 กำลังสร้างการทำนายทั้งหมด...")
            predictions = self.get_all_predictions()
            
            if not predictions:
                print("❌ ไม่มีข้อมูลการแข่งขัน")
                return False
            
            print("🌙 กำลังสร้าง Dark Theme HTML...")
            html_content = self.generate_clean_html(predictions)
            
            # เขียนไฟล์ใหม่ทั้งหมด
            with open(self.index_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print("✅ สร้าง index.html ใหม่ด้วย Dark Theme สำเร็จ!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating new index.html: {e}")
            return False
    
    def push_to_github(self):
        """Push การเปลี่ยนแปลงขึ้น GitHub"""
        try:
            os.chdir('/Users/80090/Desktop/Project/untitle')
            
            commands = [
                ['git', 'add', '.'],
                ['git', 'commit', '-m', '🌙 Dark Theme Multi-League Predictor - ลบข้อมูลเก่า เปลี่ยนเป็น Dark Theme สวยงาม รวมทุกลีกในตารางเดียว'],
                ['git', 'push', 'origin', 'main']
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"❌ Git command failed: {' '.join(cmd)}")
                    print(f"Error: {result.stderr}")
                    return False
                else:
                    print(f"✅ {' '.join(cmd)} - Success")
            
            print("🚀 Push to GitHub สำเร็จ!")
            return True
            
        except Exception as e:
            print(f"❌ Error pushing to GitHub: {e}")
            return False
    
    def run_complete_update(self):
        """รันการอัปเดตแบบครบถ้วน"""
        print("🌙 Dark Theme Clean Update - Starting...")
        print("=" * 60)
        
        if self.update_index_html():
            print("✅ HTML Update: Success")
        else:
            print("❌ HTML Update: Failed")
            return False
        
        if self.push_to_github():
            print("✅ GitHub Push: Success")
        else:
            print("❌ GitHub Push: Failed")
            return False
        
        print("\n🎉 Dark Theme Clean Update Complete!")
        print("🌐 View at: https://tuckkiez.github.io/untitled/")
        print("\n🌙 Dark Theme Features:")
        print("✅ สีดำสวยงาม พร้อม Gradient Effects")
        print("✅ ลบข้อมูลเก่าทั้งหมด (FIFA Club World Cup, Chelsea vs PSG)")
        print("✅ รวมข้อมูลเก่าเข้าในตารางใหม่")
        print("✅ Animation และ Hover Effects")
        print("✅ Responsive Design สำหรับทุกอุปกรณ์")
        print("\n🏆 Leagues: Premier League, La Liga, Bundesliga, Serie A, Ligue 1, K League 2, FIFA Club World Cup")
        
        return True

if __name__ == "__main__":
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    updater = DarkThemeCleanUpdater(api_key)
    updater.run_complete_update()
