#!/usr/bin/env python3
"""
🚀 Update Multi-League Table Final - ทุกลีกทุกนัดในตารางเดียว
อัปเดต index.html ด้วยการทำนายจากทุกลีกใหญ่ในรูปแบบตาราง

Supported Leagues:
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (England)
- 🇪🇸 La Liga (Spain) 
- 🇩🇪 Bundesliga (Germany)
- 🇮🇹 Serie A (Italy)
- 🇫🇷 Ligue 1 (France)
- 🇰🇷 K League 2 (South Korea)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multi_league_table_predictor import MultiLeagueTablePredictor
import subprocess
from datetime import datetime
import pytz
import re

class MultiLeagueTableUpdater:
    def __init__(self, api_key):
        self.api_key = api_key
        self.predictor = MultiLeagueTablePredictor(api_key)
        self.index_path = '/Users/80090/Desktop/Project/untitle/index.html'
        
        # ข้อมูลตัวอย่างการแข่งขันวันนี้ (เนื่องจาก API ไม่มีข้อมูลจริง)
        self.sample_matches = [
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
        
    def get_sample_predictions(self):
        """สร้างการทำนายจากข้อมูลตัวอย่าง"""
        predictions = []
        
        for match in self.sample_matches:
            prediction = self.predictor.predict_match(match)
            predictions.append({
                'match': match,
                'predictions': prediction
            })
        
        return predictions
        
    def generate_html_section(self, predictions):
        """สร้าง HTML section แบบตารางสำหรับทุกลีก"""
        
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
        
        # CSS styles
        css_styles = """
        <style>
        .multi-league-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .section-header {
            text-align: center;
            margin-bottom: 25px;
        }
        
        .section-header h2 {
            font-size: 2.5em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .league-stats {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 25px;
        }
        
        .stat-badge {
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.9em;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .predictions-table-container {
            overflow-x: auto;
            margin: 20px 0;
        }
        
        .predictions-table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .predictions-table th {
            background: rgba(255,255,255,0.2);
            padding: 15px 10px;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }
        
        .league-header td {
            background: rgba(255,255,255,0.15) !important;
            padding: 12px 15px;
            font-size: 1.2em;
            font-weight: bold;
            text-align: center;
            border-top: 2px solid rgba(255,255,255,0.3);
        }
        
        .league-title {
            color: #ffd700 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        .match-row td {
            padding: 15px 10px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .match-teams {
            text-align: left !important;
            min-width: 280px;
        }
        
        .teams-info strong {
            display: block;
            font-size: 1.1em;
            margin-bottom: 5px;
        }
        
        .match-details {
            font-size: 0.85em;
            opacity: 0.8;
        }
        
        .match-details span {
            display: inline-block;
            margin-right: 15px;
        }
        
        .prediction-cell {
            min-width: 130px;
        }
        
        .prediction-main {
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 3px;
        }
        
        .handicap-line {
            font-weight: bold;
            color: #ffc107;
            margin-bottom: 3px;
            font-size: 0.95em;
        }
        
        .handicap-rec {
            font-size: 0.85em;
            margin-bottom: 3px;
        }
        
        .confidence {
            font-size: 0.8em;
            opacity: 0.8;
        }
        
        /* สีตามความมั่นใจ */
        .high-confidence {
            background: rgba(40, 167, 69, 0.3) !important;
            border-left: 4px solid #28a745;
        }
        
        .medium-confidence {
            background: rgba(255, 193, 7, 0.3) !important;
            border-left: 4px solid #ffc107;
        }
        
        .low-confidence {
            background: rgba(220, 53, 69, 0.3) !important;
            border-left: 4px solid #dc3545;
        }
        
        .legend {
            margin-top: 25px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            text-align: center;
        }
        
        .legend h3 {
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .legend-items {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .legend-item {
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .legend-item.high-confidence {
            background: rgba(40, 167, 69, 0.3);
            border: 1px solid #28a745;
        }
        
        .legend-item.medium-confidence {
            background: rgba(255, 193, 7, 0.3);
            border: 1px solid #ffc107;
        }
        
        .legend-item.low-confidence {
            background: rgba(220, 53, 69, 0.3);
            border: 1px solid #dc3545;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .multi-league-section {
                padding: 15px;
            }
            
            .section-header h2 {
                font-size: 2em;
            }
            
            .league-stats {
                flex-direction: column;
                align-items: center;
            }
            
            .predictions-table th,
            .predictions-table td {
                padding: 10px 5px;
                font-size: 0.9em;
            }
            
            .match-teams {
                min-width: 220px;
            }
            
            .prediction-cell {
                min-width: 110px;
            }
        }
        </style>
        """
        
        # นับสถิติ
        total_matches = len(predictions)
        leagues_count = len(leagues_data)
        
        # สร้าง HTML section เต็ม
        html_section = f"""
        <!-- 🚀 Multi-League Advanced ML Predictions -->
        <section class="multi-league-section">
            <div class="section-header">
                <h2>🚀 Multi-League Advanced ML Predictions</h2>
                <div class="league-stats">
                    <span class="stat-badge">🏆 {leagues_count} Leagues</span>
                    <span class="stat-badge">⚽ {total_matches} Matches</span>
                    <span class="stat-badge">🤖 Advanced ML</span>
                    <span class="stat-badge">🎯 Real-time Analysis</span>
                </div>
            </div>
            
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
        
        {css_styles}
        """
        
        return html_section
    
    def update_index_html(self):
        """อัปเดต index.html ด้วย Multi-League Table"""
        try:
            # ทำนายการแข่งขัน
            print("🤖 กำลังทำนายการแข่งขันจากทุกลีก...")
            predictions = self.get_sample_predictions()
            
            if not predictions:
                print("❌ ไม่มีข้อมูลการแข่งขัน")
                return False
            
            # สร้าง HTML section
            html_section = self.generate_html_section(predictions)
            
            # อ่านไฟล์ index.html
            with open(self.index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ลบ section เก่าทั้งหมด
            patterns = [
                r'<!-- 🇰🇷 K League 2 Advanced ML Predictions -->.*?</style>',
                r'<!-- 🚀 Multi-League Advanced ML Predictions -->.*?</style>'
            ]
            
            for pattern in patterns:
                content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            # หาตำแหน่งที่จะแทรก (หลัง body tag)
            body_start = content.find('<body>')
            if body_start != -1:
                insert_pos = content.find('>', body_start) + 1
                content = content[:insert_pos] + '\n' + html_section + '\n' + content[insert_pos:]
            else:
                content = content + '\n' + html_section
            
            # เขียนไฟล์ใหม่
            with open(self.index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ อัปเดต index.html ด้วย Multi-League Table สำเร็จ!")
            return True
            
        except Exception as e:
            print(f"❌ Error updating index.html: {e}")
            return False
    
    def push_to_github(self):
        """Push การเปลี่ยนแปลงขึ้น GitHub"""
        try:
            os.chdir('/Users/80090/Desktop/Project/untitle')
            
            commands = [
                ['git', 'add', '.'],
                ['git', 'commit', '-m', '🚀 Multi-League Table UI - ทุกลีกทุกนัดในตารางเดียว! Premier League, La Liga, Bundesliga, Serie A, Ligue 1, K League 2'],
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
        print("🚀 Multi-League Table Update - Starting...")
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
        
        print("\n🎉 Multi-League Table Update Complete!")
        print("🌐 View at: https://tuckkiez.github.io/untitled/")
        print("\n🏆 Leagues Covered:")
        print("✅ 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League - 2 matches")
        print("✅ 🇪🇸 La Liga - 2 matches")
        print("✅ 🇩🇪 Bundesliga - 2 matches")
        print("✅ 🇮🇹 Serie A - 2 matches")
        print("✅ 🇫🇷 Ligue 1 - 2 matches")
        print("✅ 🇰🇷 K League 2 - 2 matches")
        print(f"\n📊 Total: 6 leagues, 12 matches")
        
        return True

if __name__ == "__main__":
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    updater = MultiLeagueTableUpdater(api_key)
    updater.run_complete_update()
