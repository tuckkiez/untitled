#!/usr/bin/env python3
"""
🎨 HTML Generator for Real Predictions
สร้าง HTML สำหรับการทำนายจริง
"""

from datetime import datetime
import pytz

class HTMLGenerator:
    def __init__(self):
        self.league_weights = {
            "FIFA Club World Cup": 2.0,
            "Serie A": 1.3,
            "Liga MX": 1.2,
            "Allsvenskan": 1.1,
            "Primera A": 1.1,
            "Veikkausliiga": 1.0,
            "Primera Nacional": 1.0,
            "Serie B": 0.9,
            "Super Cup": 1.5,
            "Premier League": 1.2,
            "Eliteserien": 1.0
        }

    def get_league_priority(self, league_name):
        """กำหนดลำดับความสำคัญของลีก"""
        priority_map = {
            "FIFA Club World Cup": 1,
            "Serie A": 2,
            "Liga MX": 3,
            "Allsvenskan": 4,
            "Primera A": 5,
            "Super Cup": 6,
            "Veikkausliiga": 7,
            "Premier League": 8,
            "Primera Nacional": 9,
            "Serie B": 10,
            "Eliteserien": 11
        }
        
        for key, priority in priority_map.items():
            if key in league_name:
                return priority
        return 99

    def format_time(self, utc_time):
        """แปลงเวลา UTC เป็นเวลาไทย"""
        try:
            dt = datetime.fromisoformat(utc_time.replace('Z', '+00:00'))
            thai_tz = pytz.timezone('Asia/Bangkok')
            thai_time = dt.astimezone(thai_tz)
            return thai_time.strftime('%H:%M')
        except:
            return "TBD"

    def get_status_emoji(self, status):
        """แปลงสถานะเป็น emoji"""
        status_map = {
            'NS': '🔴 Not Started',
            'LIVE': '🟢 LIVE',
            'HT': '🟡 Half Time',
            'FT': '⚪ Finished',
            'PST': '🟠 Postponed',
            'CANC': '❌ Cancelled'
        }
        return status_map.get(status, f'🔵 {status}')

    def get_confidence_color(self, confidence):
        """กำหนดสีตามระดับความมั่นใจ"""
        if confidence >= 80:
            return "#4CAF50"  # เขียว
        elif confidence >= 70:
            return "#FF9800"  # ส้m
        elif confidence >= 60:
            return "#2196F3"  # น้ำเงิน
        else:
            return "#9E9E9E"  # เทา

    def generate_match_card_html(self, match):
        """สร้าง HTML สำหรับ match card"""
        predictions = match.get('real_predictions', {})
        status = self.get_status_emoji(match['fixture']['status']['short'])
        time = self.format_time(match['fixture']['date'])
        
        # กำหนด priority class
        league_name = match['league']['name']
        weight = self.league_weights.get(league_name, 1.0)
        priority_class = "priority-high" if weight >= 1.5 else "priority-medium" if weight >= 1.0 else "priority-low"
        
        # ตรวจสอบว่าเป็นการแข่งขันสดหรือไม่
        live_indicator = '<div class="live-indicator"></div>' if match['fixture']['status']['short'] in ['LIVE', '1H', '2H'] else ''
        
        venue = match['fixture']['venue']['name'] if match['fixture']['venue']['name'] else 'TBD'
        city = match['fixture']['venue']['city'] if match['fixture']['venue']['city'] else 'TBD'
        
        # สร้าง HTML สำหรับการทำนาย
        result_color = self.get_confidence_color(predictions.get('result_confidence', 55))
        handicap_color = self.get_confidence_color(predictions.get('handicap_confidence', 50))
        ou_color = self.get_confidence_color(predictions.get('ou_confidence', 60))
        corner_ht_color = self.get_confidence_color(predictions.get('corner_ht_confidence', 60))
        corner_ft_color = self.get_confidence_color(predictions.get('corner_ft_confidence', 65))
        
        return f"""
                    <div class="match-card {priority_class}">
                        {live_indicator}
                        <div class="match-header">
                            <div class="match-status">{status}</div>
                            <div class="match-time">{time} ICT</div>
                        </div>
                        <div class="match-teams">
                            <div class="team-name">{match['teams']['home']['name']}</div>
                            <div class="vs">VS</div>
                            <div class="team-name">{match['teams']['away']['name']}</div>
                        </div>
                        <div class="match-venue">{venue}, {city}</div>
                        
                        <div class="predictions-advanced">
                            <div class="pred-section">
                                <h4>🎯 Match Result</h4>
                                <div class="pred-row">
                                    <span class="pred-label">Prediction:</span>
                                    <span class="pred-value" style="color: {result_color}">{predictions.get('result', 'Draw')}</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {predictions.get('result_confidence', 55)}%; background-color: {result_color}"></div>
                                </div>
                                <div class="confidence-text">{predictions.get('result_confidence', 55)}% Confidence</div>
                            </div>
                            
                            <div class="pred-section">
                                <h4>⚖️ Handicap</h4>
                                <div class="pred-row">
                                    <span class="pred-label">Line:</span>
                                    <span class="pred-value" style="color: {handicap_color}">{predictions.get('handicap', '0')}</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {predictions.get('handicap_confidence', 50)}%; background-color: {handicap_color}"></div>
                                </div>
                                <div class="confidence-text">{predictions.get('handicap_confidence', 50)}% Confidence</div>
                            </div>
                            
                            <div class="pred-section">
                                <h4>⚽ Over/Under</h4>
                                <div class="pred-row">
                                    <span class="pred-label">2.5 Goals:</span>
                                    <span class="pred-value" style="color: {ou_color}">{predictions.get('over_under', 'Over 2.5')}</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {predictions.get('ou_confidence', 60)}%; background-color: {ou_color}"></div>
                                </div>
                                <div class="confidence-text">{predictions.get('ou_confidence', 60)}% Confidence</div>
                            </div>
                            
                            <div class="pred-section">
                                <h4>🚩 Corners</h4>
                                <div class="pred-row">
                                    <span class="pred-label">Half-time:</span>
                                    <span class="pred-value" style="color: {corner_ht_color}">{predictions.get('corner_ht', 'Under 5')}</span>
                                </div>
                                <div class="pred-row">
                                    <span class="pred-label">Full-time:</span>
                                    <span class="pred-value" style="color: {corner_ft_color}">{predictions.get('corner_ft', 'Over 9')}</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {(predictions.get('corner_ht_confidence', 60) + predictions.get('corner_ft_confidence', 65)) / 2}%; background-color: {corner_ft_color}"></div>
                                </div>
                                <div class="confidence-text">Avg {int((predictions.get('corner_ht_confidence', 60) + predictions.get('corner_ft_confidence', 65)) / 2)}% Confidence</div>
                            </div>
                        </div>
                    </div>"""

    def generate_full_html(self, matches_by_date):
        """สร้าง HTML เต็มรูปแบบ"""
        # คำนวณสถิติ
        total_matches = sum(len(matches) for matches in matches_by_date.values())
        total_leagues = len(set(match['league']['name'] for matches in matches_by_date.values() for match in matches))
        live_matches = sum(1 for matches in matches_by_date.values() for match in matches if match['fixture']['status']['short'] in ['LIVE', '1H', '2H', 'HT'])
        
        # เริ่มต้น HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Advanced Football Predictions | Real Data Analysis</title>
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
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
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
            margin-bottom: 40px;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
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

        .header p {{
            font-size: 1.1rem;
            opacity: 0.8;
            margin-bottom: 20px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .stat-number {{
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
        }}

        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.7;
            margin-top: 5px;
        }}

        .date-section {{
            margin-bottom: 40px;
        }}

        .date-header {{
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 20px;
            padding: 15px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            text-align: center;
        }}

        .league-section {{
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .league-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .league-title {{
            font-size: 1.3rem;
            font-weight: 600;
        }}

        .league-weight {{
            background: rgba(102, 126, 234, 0.2);
            color: #667eea;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }}

        .matches-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 20px;
        }}

        .match-card {{
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .match-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            border-color: rgba(102, 126, 234, 0.5);
        }}

        .match-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .match-status {{
            font-size: 0.9rem;
            font-weight: 500;
        }}

        .match-time {{
            font-size: 0.9rem;
            opacity: 0.7;
        }}

        .match-teams {{
            text-align: center;
            margin-bottom: 15px;
        }}

        .team-name {{
            font-size: 1.1rem;
            font-weight: 600;
            margin: 5px 0;
        }}

        .vs {{
            font-size: 0.9rem;
            opacity: 0.6;
            margin: 10px 0;
        }}

        .match-venue {{
            font-size: 0.8rem;
            opacity: 0.6;
            text-align: center;
            margin-bottom: 15px;
        }}

        .predictions-advanced {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }}

        .pred-section {{
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .pred-section:last-child {{
            margin-bottom: 0;
            border-bottom: none;
        }}

        .pred-section h4 {{
            font-size: 0.9rem;
            margin-bottom: 8px;
            opacity: 0.9;
        }}

        .pred-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }}

        .pred-label {{
            font-size: 0.85rem;
            opacity: 0.8;
        }}

        .pred-value {{
            font-weight: 600;
            font-size: 0.85rem;
        }}

        .confidence-bar {{
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            margin: 5px 0;
            overflow: hidden;
        }}

        .confidence-fill {{
            height: 100%;
            border-radius: 2px;
            transition: width 0.3s ease;
        }}

        .confidence-text {{
            font-size: 0.75rem;
            opacity: 0.7;
            text-align: center;
        }}

        .priority-high {{
            border-left: 4px solid #ff6b6b;
        }}

        .priority-medium {{
            border-left: 4px solid #feca57;
        }}

        .priority-low {{
            border-left: 4px solid #48dbfb;
        }}

        .live-indicator {{
            position: absolute;
            top: 10px;
            right: 10px;
            width: 10px;
            height: 10px;
            background: #ff6b6b;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}

        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .footer p {{
            opacity: 0.7;
            margin-bottom: 10px;
        }}

        .update-time {{
            color: #667eea;
            font-weight: 500;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            .matches-grid {{
                grid-template-columns: 1fr;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Advanced Football Predictions</h1>
            <p>Real Data Analysis with Machine Learning & Statistical Models</p>
            <p>4-Value Predictions: Match Result | Handicap | Over/Under | Corners</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{total_matches}</div>
                    <div class="stat-label">Total Matches</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_leagues}</div>
                    <div class="stat-label">Leagues Covered</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{live_matches}</div>
                    <div class="stat-label">Live Matches</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">4</div>
                    <div class="stat-label">Prediction Types</div>
                </div>
            </div>
        </div>
"""

        # สร้างเนื้อหาสำหรับแต่ละวัน
        for date, matches in matches_by_date.items():
            if not matches:
                continue
                
            # แปลงวันที่
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%B %d, %Y')
            except:
                formatted_date = date
                
            html += f"""
        <div class="date-section">
            <div class="date-header">📅 {formatted_date}</div>
"""

            # จัดกลุ่มตามลีก
            leagues = {}
            for match in matches:
                league_name = match['league']['name']
                if league_name not in leagues:
                    leagues[league_name] = []
                leagues[league_name].append(match)

            # เรียงลำดับลีกตามความสำคัญ
            sorted_leagues = sorted(leagues.items(), key=lambda x: self.get_league_priority(x[0]))

            for league_name, league_matches in sorted_leagues:
                weight = self.league_weights.get(league_name, 1.0)
                country = league_matches[0]['league']['country']
                
                html += f"""
            <div class="league-section">
                <div class="league-header">
                    <div class="league-title">🏆 {league_name} ({country})</div>
                    <div class="league-weight">Weight: {weight}</div>
                </div>
                <div class="matches-grid">
"""

                for match in league_matches:
                    html += self.generate_match_card_html(match)

                html += """
                </div>
            </div>
"""

            html += """
        </div>
"""

        # Footer
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S ICT')
        html += f"""
        <div class="footer">
            <p>🤖 Powered by Advanced Statistical Analysis & Real Team Data</p>
            <p>📊 4-Value Prediction System: Result | Handicap | Over/Under | Corners</p>
            <p>🏆 Special FIFA Club World Cup Analysis with Cross-League Data</p>
            <p class="update-time">Last Updated: {current_time}</p>
            <p>🔄 Real-time data integration with API-Sports</p>
        </div>
    </div>

    <script>
        // Auto-refresh every 30 minutes for real predictions
        setTimeout(function() {{
            location.reload();
        }}, 1800000);
        
        // Add loading animation for match cards
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.match-card');
            cards.forEach((card, index) => {{
                setTimeout(() => {{
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    card.style.transition = 'all 0.5s ease';
                    setTimeout(() => {{
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }}, 50);
                }}, index * 100);
            }});
        }});
    </script>
</body>
</html>"""

        return html
