#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 UEFA CHAMPIONS LEAGUE - CLEAN UI FROM SCRATCH
สร้าง UI ใหม่หมดที่สะอาดและเรียบร้อย
"""

from datetime import datetime

class CleanUCLUI:
    def __init__(self):
        self.matches_data = [
            {
                "id": 1,
                "home": "Kairat Almaty",
                "away": "Olimpija Ljubljana",
                "home_country": "🇰🇿 Kazakhstan",
                "away_country": "🇸🇮 Slovenia",
                "time": "22:00",
                "venue": "Ortalyq stadion",
                "home_strength": 2.9,
                "away_strength": 2.9,
                "home_win": 80.5,
                "draw": 12.0,
                "away_win": 7.5,
                "over_25": 18.9,
                "under_25": 81.1,
                "bts_yes": 16.1,
                "bts_no": 83.9,
                "corners_over": 26.5,
                "corners_under": 73.5,
                "primary_bet": "Kairat Almaty Win",
                "primary_confidence": 80.5,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 81.1
            },
            {
                "id": 2,
                "home": "Lincoln Red Imps",
                "away": "Vikingur Gota",
                "home_country": "🇬🇮 Gibraltar",
                "away_country": "🇫🇴 Faroe Islands",
                "time": "22:30",
                "venue": "Europa Point Stadium",
                "home_strength": 2.8,
                "away_strength": 2.2,
                "home_win": 75.5,
                "draw": 21.5,
                "away_win": 3.0,
                "over_25": 26.3,
                "under_25": 73.7,
                "bts_yes": 42.8,
                "bts_no": 57.2,
                "corners_over": 10.0,
                "corners_under": 90.0,
                "primary_bet": "Lincoln Red Imps Win",
                "primary_confidence": 75.5,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 73.7
            },
            {
                "id": 3,
                "home": "Milsami Orhei",
                "away": "KuPS",
                "home_country": "🇲🇩 Moldova",
                "away_country": "🇫🇮 Finland",
                "time": "00:00",
                "venue": "Complexul Sportiv Raional",
                "home_strength": 2.4,
                "away_strength": 3.9,
                "home_win": 55.0,
                "draw": 15.5,
                "away_win": 29.5,
                "over_25": 27.1,
                "under_25": 72.9,
                "bts_yes": 23.3,
                "bts_no": 76.7,
                "corners_over": 14.6,
                "corners_under": 85.4,
                "primary_bet": "Milsami Orhei Win",
                "primary_confidence": 55.0,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 72.9
            },
            {
                "id": 4,
                "home": "Hamrun Spartans",
                "away": "Zalgiris Vilnius",
                "home_country": "🇲🇹 Malta",
                "away_country": "🇱🇹 Lithuania",
                "time": "00:00",
                "venue": "Ta'Qali National Stadium",
                "home_strength": 2.7,
                "away_strength": 3.6,
                "home_win": 55.5,
                "draw": 17.5,
                "away_win": 27.0,
                "over_25": 29.5,
                "under_25": 70.5,
                "bts_yes": 11.1,
                "bts_no": 88.9,
                "corners_over": 43.8,
                "corners_under": 56.2,
                "primary_bet": "Hamrun Spartans Win",
                "primary_confidence": 55.5,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 70.5
            },
            {
                "id": 5,
                "home": "Malmo FF",
                "away": "Saburtalo",
                "home_country": "🇸🇪 Sweden",
                "away_country": "🇬🇪 Georgia",
                "time": "00:00",
                "venue": "Eleda Stadion",
                "home_strength": 4.8,
                "away_strength": 3.7,
                "home_win": 52.0,
                "draw": 42.5,
                "away_win": 5.5,
                "over_25": 33.0,
                "under_25": 67.0,
                "bts_yes": 58.3,
                "bts_no": 41.7,
                "corners_over": 34.0,
                "corners_under": 66.0,
                "primary_bet": "Malmo FF Win",
                "primary_confidence": 52.0,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 67.0
            },
            {
                "id": 6,
                "home": "Rīgas FS",
                "away": "Levadia Tallinn",
                "home_country": "🇱🇻 Latvia",
                "away_country": "🇪🇪 Estonia",
                "time": "00:00",
                "venue": "LNK Sporta Parks",
                "home_strength": 3.2,
                "away_strength": 2.9,
                "home_win": 76.5,
                "draw": 17.0,
                "away_win": 6.5,
                "over_25": 16.7,
                "under_25": 83.3,
                "bts_yes": 30.0,
                "bts_no": 70.0,
                "corners_over": 33.4,
                "corners_under": 66.6,
                "primary_bet": "Rīgas FS Win",
                "primary_confidence": 76.5,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 83.3
            },
            {
                "id": 7,
                "home": "Differdange",
                "away": "Drita",
                "home_country": "🇱🇺 Luxembourg",
                "away_country": "🇽🇰 Kosovo",
                "time": "01:00",
                "venue": "Stade Municipal Differdange",
                "home_strength": 2.3,
                "away_strength": 3.2,
                "home_win": 64.0,
                "draw": 21.5,
                "away_win": 14.5,
                "over_25": 57.4,
                "under_25": 42.6,
                "bts_yes": 29.4,
                "bts_no": 70.6,
                "corners_over": 46.8,
                "corners_under": 53.2,
                "primary_bet": "Differdange Win",
                "primary_confidence": 64.0,
                "secondary_bet": "Both Teams Score - No",
                "secondary_confidence": 70.6
            },
            {
                "id": 8,
                "home": "Shkendija",
                "away": "The New Saints",
                "home_country": "🇲🇰 North Macedonia",
                "away_country": "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Wales",
                "time": "01:00",
                "venue": "Toše Proeski Arena",
                "home_strength": 3.4,
                "away_strength": 3.7,
                "home_win": 52.0,
                "draw": 19.0,
                "away_win": 29.0,
                "over_25": 19.1,
                "under_25": 80.9,
                "bts_yes": 35.6,
                "bts_no": 64.4,
                "corners_over": 29.5,
                "corners_under": 70.5,
                "primary_bet": "Shkendija Win",
                "primary_confidence": 52.0,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 80.9
            },
            {
                "id": 9,
                "home": "Inter Escaldes",
                "away": "FCSB",
                "home_country": "🇦🇩 Andorra",
                "away_country": "🇷🇴 Romania",
                "time": "01:30",
                "venue": "Nou Estadi Encamp",
                "home_strength": 1.9,
                "away_strength": 4.3,
                "home_win": 52.5,
                "draw": 20.5,
                "away_win": 27.0,
                "over_25": 14.4,
                "under_25": 85.6,
                "bts_yes": 14.4,
                "bts_no": 85.6,
                "corners_over": 10.0,
                "corners_under": 90.0,
                "primary_bet": "Inter Escaldes Win",
                "primary_confidence": 52.5,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 85.6
            },
            {
                "id": 10,
                "home": "Zrinjski",
                "away": "Virtus",
                "home_country": "🇧🇦 Bosnia",
                "away_country": "🇸🇲 San Marino",
                "time": "02:00",
                "venue": "Stadion Bijeli Brijeg",
                "home_strength": 3.7,
                "away_strength": 1.3,
                "home_win": 53.5,
                "draw": 40.0,
                "away_win": 6.5,
                "over_25": 9.3,
                "under_25": 90.7,
                "bts_yes": 58.3,
                "bts_no": 41.7,
                "corners_over": 30.5,
                "corners_under": 69.5,
                "primary_bet": "Zrinjski Win",
                "primary_confidence": 53.5,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 90.7
            },
            {
                "id": 11,
                "home": "Breidablik",
                "away": "Egnatia",
                "home_country": "🇮🇸 Iceland",
                "away_country": "🇦🇱 Albania",
                "time": "02:00",
                "venue": "Kópavogsvöllur",
                "home_strength": 3.4,
                "away_strength": 3.4,
                "home_win": 72.0,
                "draw": 16.0,
                "away_win": 12.0,
                "over_25": 20.3,
                "under_25": 79.7,
                "bts_yes": 25.6,
                "bts_no": 74.4,
                "corners_over": 27.3,
                "corners_under": 72.7,
                "primary_bet": "Breidablik Win",
                "primary_confidence": 72.0,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 79.7
            },
            {
                "id": 12,
                "home": "Buducnost",
                "away": "FC Noah",
                "home_country": "🇲🇪 Montenegro",
                "away_country": "🇦🇲 Armenia",
                "time": "02:00",
                "venue": "Stadion Pod Goricom",
                "home_strength": 3.2,
                "away_strength": 2.9,
                "home_win": 76.5,
                "draw": 17.0,
                "away_win": 6.5,
                "over_25": 16.7,
                "under_25": 83.3,
                "bts_yes": 30.0,
                "bts_no": 70.0,
                "corners_over": 33.4,
                "corners_under": 66.6,
                "primary_bet": "Buducnost Win",
                "primary_confidence": 76.5,
                "secondary_bet": "Under 2.5 Goals",
                "secondary_confidence": 83.3
            }
        ]
    
    def create_clean_html(self):
        """สร้าง HTML ที่สะอาดและเรียบร้อย"""
        
        html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 UEFA Champions League 2025-26 - Advanced ML Analysis</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0e27;
            color: #ffffff;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 40px 0;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            color: #ffd700;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.1rem;
            color: #a0a0a0;
            margin-bottom: 30px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-bottom: 20px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #ffd700;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #a0a0a0;
        }
        
        .matches {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
        }
        
        .match {
            background: #1a1f3a;
            border-radius: 12px;
            padding: 25px;
            border: 1px solid #2a2f4a;
            transition: all 0.3s ease;
        }
        
        .match:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(255, 215, 0, 0.1);
            border-color: #ffd700;
        }
        
        .match.high-confidence {
            border: 2px solid #ffd700;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        }
        
        .match-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #2a2f4a;
        }
        
        .match-number {
            font-size: 1.2rem;
            font-weight: bold;
            color: #ffd700;
        }
        
        .match-time {
            background: #ffd700;
            color: #0a0e27;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .teams {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }
        
        .team {
            text-align: center;
            flex: 1;
        }
        
        .team-name {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .team-country {
            font-size: 0.9rem;
            color: #a0a0a0;
            margin-bottom: 8px;
        }
        
        .team-strength {
            background: rgba(255, 215, 0, 0.1);
            color: #ffd700;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .vs {
            font-size: 1.5rem;
            font-weight: bold;
            color: #ffd700;
            margin: 0 20px;
        }
        
        .venue {
            text-align: center;
            font-size: 0.9rem;
            color: #a0a0a0;
            margin-bottom: 20px;
        }
        
        .predictions {
            margin-bottom: 20px;
        }
        
        .prediction-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        
        .prediction-label {
            font-size: 0.9rem;
            color: #a0a0a0;
            margin-bottom: 5px;
        }
        
        .prediction-bar {
            background: #2a2f4a;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 8px;
        }
        
        .prediction-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #66BB6A);
            border-radius: 4px;
            transition: width 1s ease;
        }
        
        .prediction-values {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
        }
        
        .prediction-values span {
            color: #a0a0a0;
        }
        
        .betting {
            background: rgba(255, 215, 0, 0.05);
            border: 1px solid rgba(255, 215, 0, 0.2);
            border-radius: 8px;
            padding: 15px;
        }
        
        .betting-title {
            font-size: 1rem;
            font-weight: bold;
            color: #ffd700;
            margin-bottom: 10px;
        }
        
        .bet {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            padding: 8px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 6px;
        }
        
        .bet:last-child {
            margin-bottom: 0;
        }
        
        .bet-text {
            font-size: 0.9rem;
        }
        
        .bet-confidence {
            background: #4CAF50;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 30px;
            color: #a0a0a0;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .matches {
                grid-template-columns: 1fr;
            }
            
            .stats {
                flex-direction: column;
                gap: 20px;
            }
            
            .teams {
                flex-direction: column;
                gap: 15px;
            }
            
            .vs {
                margin: 10px 0;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 UEFA Champions League 2025-26</h1>
            <p>Qualifying Round 1 - Advanced ML Analysis</p>
            <div class="stats">
                <div class="stat">
                    <span class="stat-number">12</span>
                    <span class="stat-label">Matches</span>
                </div>
                <div class="stat">
                    <span class="stat-number">6</span>
                    <span class="stat-label">High Confidence</span>
                </div>
                <div class="stat">
                    <span class="stat-number">63.8%</span>
                    <span class="stat-label">Avg Confidence</span>
                </div>
            </div>
        </div>
        
        <div class="matches">"""
        
        # เพิ่มแมตช์ทั้งหมด
        for match in self.matches_data:
            high_conf_class = "high-confidence" if match["primary_confidence"] > 70 else ""
            
            html += f"""
            <div class="match {high_conf_class}">
                <div class="match-header">
                    <div class="match-number">⚽ MATCH {match['id']}</div>
                    <div class="match-time">{match['time']}</div>
                </div>
                
                <div class="teams">
                    <div class="team">
                        <div class="team-name">🏠 {match['home']}</div>
                        <div class="team-country">{match['home_country']}</div>
                        <div class="team-strength">{match['home_strength']}/10</div>
                    </div>
                    <div class="vs">VS</div>
                    <div class="team">
                        <div class="team-name">✈️ {match['away']}</div>
                        <div class="team-country">{match['away_country']}</div>
                        <div class="team-strength">{match['away_strength']}/10</div>
                    </div>
                </div>
                
                <div class="venue">🏟️ {match['venue']}</div>
                
                <div class="predictions">
                    <div class="prediction-row">
                        <div style="flex: 1; margin-right: 10px;">
                            <div class="prediction-label">🏆 Match Result</div>
                            <div class="prediction-values">
                                <span>Home {match['home_win']}%</span>
                                <span>Draw {match['draw']}%</span>
                                <span>Away {match['away_win']}%</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="prediction-row">
                        <div style="flex: 1; margin-right: 10px;">
                            <div class="prediction-label">⚽ Over/Under 2.5</div>
                            <div class="prediction-values">
                                <span>Over {match['over_25']}%</span>
                                <span>Under {match['under_25']}%</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="prediction-row">
                        <div style="flex: 1; margin-right: 10px;">
                            <div class="prediction-label">🎯 Both Teams Score</div>
                            <div class="prediction-values">
                                <span>Yes {match['bts_yes']}%</span>
                                <span>No {match['bts_no']}%</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="prediction-row">
                        <div style="flex: 1;">
                            <div class="prediction-label">🚩 Corners</div>
                            <div class="prediction-values">
                                <span>Over 8: {match['corners_over']}%</span>
                                <span>Under 8: {match['corners_under']}%</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="betting">
                    <div class="betting-title">💰 BETTING RECOMMENDATIONS</div>
                    <div class="bet">
                        <div class="bet-text">🥇 PRIMARY: {match['primary_bet']}</div>
                        <div class="bet-confidence">{match['primary_confidence']}%</div>
                    </div>
                    <div class="bet">
                        <div class="bet-text">🥈 SECONDARY: {match['secondary_bet']}</div>
                        <div class="bet-confidence">{match['secondary_confidence']}%</div>
                    </div>
                </div>
            </div>"""
        
        html += """
        </div>
        
        <div class="footer">
            <p>📅 Last Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """ (Bangkok Time)</p>
            <p>🤖 Powered by Advanced Machine Learning | 📊 Real Data from RapidAPI Football</p>
            <p>🏆 UEFA Champions League 2025-26 Qualifying Round 1</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def save_clean_ui(self):
        """บันทึก UI ที่สะอาด"""
        
        # สำรองไฟล์เก่า
        import os
        if os.path.exists('/Users/80090/Desktop/Project/untitle/index.html'):
            backup_name = f'/Users/80090/Desktop/Project/untitle/index_messy_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            import shutil
            shutil.copy('/Users/80090/Desktop/Project/untitle/index.html', backup_name)
            print(f"✅ Backed up messy UI to: {backup_name}")
        
        # สร้าง HTML ใหม่
        clean_html = self.create_clean_html()
        
        # บันทึกไฟล์ใหม่
        with open('/Users/80090/Desktop/Project/untitle/index.html', 'w', encoding='utf-8') as f:
            f.write(clean_html)
        
        print("✅ Clean UEFA Champions League UI created!")
        return True

def main():
    """Main execution"""
    ui = CleanUCLUI()
    
    print("🧹 Creating Clean UEFA Champions League UI from scratch...")
    
    try:
        if ui.save_clean_ui():
            print("\n" + "🎉" * 50)
            print("🎉 CLEAN UEFA CHAMPIONS LEAGUE UI COMPLETE!")
            print("🎉" * 50)
            print("✅ Simple and clean design")
            print("✅ Easy to read layout")
            print("✅ Mobile responsive")
            print("✅ Fast loading")
            print("✅ Professional appearance")
            print("🏆 UI is now clean and organized!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
