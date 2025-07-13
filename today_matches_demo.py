#!/usr/bin/env python3
"""
📅 Today Matches Demo (ตัวอย่างข้อมูล)
สร้างตัวอย่างตารางการแข่งขันวันนี้เพื่อทดสอบระบบ
"""

import pandas as pd
from datetime import datetime
import random

def create_sample_matches():
    """สร้างข้อมูลตัวอย่างแมตช์วันนี้"""
    
    sample_matches = [
        {
            'league': 'Premier League',
            'match_time_thai': '19:30',
            'home_team': 'Manchester City',
            'odds_home': 1.45,
            'odds_draw': 4.20,
            'odds_away': 6.50,
            'away_team': 'Arsenal',
            'home_score': '',
            'away_score': '',
            'match_result': '',
            'prediction_home_away': '',
            'prediction_handicap': '',
            'prediction_over_under': '',
            'prediction_score': '',
            'prediction_corner_1st_half': '',
            'prediction_corner_full_match': '',
            'venue': 'Etihad Stadium',
            'fixture_id': 1001
        },
        {
            'league': 'La Liga',
            'match_time_thai': '21:00',
            'home_team': 'Real Madrid',
            'odds_home': 1.65,
            'odds_draw': 3.80,
            'odds_away': 4.50,
            'away_team': 'Barcelona',
            'home_score': '',
            'away_score': '',
            'match_result': '',
            'prediction_home_away': '',
            'prediction_handicap': '',
            'prediction_over_under': '',
            'prediction_score': '',
            'prediction_corner_1st_half': '',
            'prediction_corner_full_match': '',
            'venue': 'Santiago Bernabéu',
            'fixture_id': 1002
        },
        {
            'league': 'Bundesliga',
            'match_time_thai': '20:30',
            'home_team': 'Bayern Munich',
            'odds_home': 1.35,
            'odds_draw': 5.00,
            'odds_away': 8.00,
            'away_team': 'Borussia Dortmund',
            'home_score': '',
            'away_score': '',
            'match_result': '',
            'prediction_home_away': '',
            'prediction_handicap': '',
            'prediction_over_under': '',
            'prediction_score': '',
            'prediction_corner_1st_half': '',
            'prediction_corner_full_match': '',
            'venue': 'Allianz Arena',
            'fixture_id': 1003
        },
        {
            'league': 'Serie A',
            'match_time_thai': '22:45',
            'home_team': 'Juventus',
            'odds_home': 2.10,
            'odds_draw': 3.40,
            'odds_away': 3.20,
            'away_team': 'Inter Milan',
            'home_score': '',
            'away_score': '',
            'match_result': '',
            'prediction_home_away': '',
            'prediction_handicap': '',
            'prediction_over_under': '',
            'prediction_score': '',
            'prediction_corner_1st_half': '',
            'prediction_corner_full_match': '',
            'venue': 'Allianz Stadium',
            'fixture_id': 1004
        },
        {
            'league': 'Ligue 1',
            'match_time_thai': '23:00',
            'home_team': 'Paris Saint-Germain',
            'odds_home': 1.25,
            'odds_draw': 5.50,
            'odds_away': 10.00,
            'away_team': 'Marseille',
            'home_score': '',
            'away_score': '',
            'match_result': '',
            'prediction_home_away': '',
            'prediction_handicap': '',
            'prediction_over_under': '',
            'prediction_score': '',
            'prediction_corner_1st_half': '',
            'prediction_corner_full_match': '',
            'venue': 'Parc des Princes',
            'fixture_id': 1005
        },
        {
            'league': 'J-League 2',
            'match_time_thai': '18:00',
            'home_team': 'Mito Hollyhock',
            'odds_home': 2.80,
            'odds_draw': 3.20,
            'odds_away': 2.40,
            'away_team': 'Vegalta Sendai',
            'home_score': '2',
            'away_score': '1',
            'match_result': 'Home Win',
            'prediction_home_away': '',
            'prediction_handicap': '',
            'prediction_over_under': '',
            'prediction_score': '',
            'prediction_corner_1st_half': '',
            'prediction_corner_full_match': '',
            'venue': "K's Denki Stadium",
            'fixture_id': 1006
        }
    ]
    
    return sample_matches

def create_today_matches_website_demo(df: pd.DataFrame):
    """สร้างหน้าเว็บแสดงแมตช์วันนี้ (เวอร์ชันตัวอย่าง)"""
    
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
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 1200px;
        }}

        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 8px;
            text-align: center;
            font-weight: 600;
            font-size: 0.85rem;
            white-space: nowrap;
        }}

        td {{
            padding: 12px 8px;
            text-align: center;
            border-bottom: 1px solid #eee;
            font-size: 0.85rem;
        }}

        tr:hover {{
            background-color: rgba(102, 126, 234, 0.05);
        }}

        .league-name {{
            font-weight: 600;
            color: #667eea;
            white-space: nowrap;
        }}

        .team-name {{
            font-weight: 500;
            color: #333;
            max-width: 120px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .odds {{
            font-weight: 600;
            color: #28a745;
            font-size: 0.8rem;
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

        .result-win {{
            background-color: #d4edda;
            color: #155724;
            font-weight: 600;
        }}

        .prediction-placeholder {{
            color: #999;
            font-style: italic;
            font-size: 0.8rem;
        }}

        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            color: #666;
        }}

        .demo-badge {{
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 15px;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            .matches-table {{
                margin: 0 -20px;
                border-radius: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="demo-badge">🧪 DEMO VERSION</div>
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
                        <th>ราคาต่อรอง<br>(H|D|A)</th>
                        <th>ทีมเยือน</th>
                        <th>ผลบอล</th>
                        <th>Prediction<br>Home/Away</th>
                        <th>Prediction<br>Handicap</th>
                        <th>Over/Under<br>2.5</th>
                        <th>Score<br>Prediction</th>
                        <th>Corner<br>1st Half</th>
                        <th>Corner<br>Full Match</th>
                    </tr>
                </thead>
                <tbody>"""
    
    # เพิ่มข้อมูลแมตช์
    for _, match in df.iterrows():
        # จัดรูปแบบราคาต่อรอง
        odds_display = f"{match.get('odds_home', 'N/A')}<br>{match.get('odds_draw', 'N/A')}<br>{match.get('odds_away', 'N/A')}"
        
        # จัดรูปแบบผลบอล
        if match.get('home_score') != '' and match.get('away_score') != '':
            score_display = f"{match['home_score']}-{match['away_score']}"
            result_class = "result-win" if match.get('match_result') else ""
        else:
            score_display = "vs"
            result_class = ""
        
        html_content += f"""
                    <tr>
                        <td class="league-name">{match['league']}</td>
                        <td class="time">{match['match_time_thai']}</td>
                        <td class="team-name">{match['home_team']}</td>
                        <td class="odds">{odds_display}</td>
                        <td class="team-name">{match['away_team']}</td>
                        <td class="score {result_class}">{score_display}</td>
                        <td class="prediction-placeholder">🔮 เร็วๆ นี้</td>
                        <td class="prediction-placeholder">🎯 เร็วๆ นี้</td>
                        <td class="prediction-placeholder">⚽ เร็วๆ นี้</td>
                        <td class="prediction-placeholder">📊 เร็วๆ นี้</td>
                        <td class="prediction-placeholder">🚩 เร็วๆ นี้</td>
                        <td class="prediction-placeholder">🏁 เร็วๆ นี้</td>
                    </tr>"""
    
    html_content += """
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>🤖 <strong>ระบบการทำนายด้วย Advanced ML กำลังคำนวณ...</strong></p>
            <p>📊 ข้อมูลจาก API-Football | 🧪 นี่คือเวอร์ชันตัวอย่าง</p>
            <p>⚡ เร็วๆ นี้จะมีการทำนายแบบเรียลไทม์!</p>
            <p>อัปเดตล่าสุด: """ + datetime.now().strftime('%H:%M:%S') + """</p>
        </div>
    </div>
</body>
</html>"""
    
    # บันทึกไฟล์ HTML
    with open('today_matches_demo.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ สร้างหน้าเว็บ today_matches_demo.html เรียบร้อย")

def main():
    """ฟังก์ชันหลักสำหรับสร้างตัวอย่าง"""
    print("🧪 สร้างตัวอย่างตารางการแข่งขันวันนี้...")
    print("=" * 50)
    
    # สร้างข้อมูลตัวอย่าง
    sample_matches = create_sample_matches()
    df = pd.DataFrame(sample_matches)
    
    # เรียงลำดับตามเวลา
    df = df.sort_values('match_time_thai')
    
    # แสดงข้อมูลสรุป
    print(f"\n📊 สรุปข้อมูลตัวอย่าง:")
    print(f"   แมตช์ทั้งหมด: {len(df)}")
    print(f"   ลีกที่มี: {', '.join(df['league'].unique())}")
    print(f"   ช่วงเวลา: {df['match_time_thai'].min()} - {df['match_time_thai'].max()}")
    
    # บันทึก CSV
    df.to_csv('today_matches_demo.csv', index=False, encoding='utf-8-sig')
    print("✅ บันทึกข้อมูลลง today_matches_demo.csv เรียบร้อย")
    
    # สร้างหน้าเว็บ
    create_today_matches_website_demo(df)
    
    # แสดงตัวอย่างข้อมูล
    print(f"\n📋 ตัวอย่างข้อมูล:")
    print(df[['league', 'match_time_thai', 'home_team', 'away_team', 'odds_home', 'odds_away']].to_string(index=False))
    
    print(f"\n🎉 เสร็จสิ้น! ไฟล์ที่สร้าง:")
    print(f"   📄 today_matches_demo.csv - ข้อมูล CSV ตัวอย่าง")
    print(f"   🌐 today_matches_demo.html - หน้าเว็บตัวอย่าง")
    print(f"\n💡 เปิดไฟล์ today_matches_demo.html ในเบราว์เซอร์เพื่อดูผลลัพธ์")

if __name__ == "__main__":
    main()
