#!/usr/bin/env python3
"""
🚀 Create Light Theme Index HTML - July 17-18, 2025
สร้างไฟล์ index.html ใหม่ด้วยธีมสีขาว ตัวหนังสือสีเข้ม และไฮไลท์ด้วยสีที่ตัดกันแต่ไม่เข้มมากเกินไป
"""

import json
import os
from datetime import datetime

def create_light_theme_index():
    """สร้างไฟล์ index.html ใหม่ด้วยธีมสีขาว"""
    print("🚀 Create Light Theme Index HTML - July 17-18, 2025")
    print("=" * 60)
    
    try:
        # โหลดข้อมูลการวิเคราะห์ที่สมบูรณ์
        with open('uefa_competitions_real_data_analysis_with_h2h_percentages.json', 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # สร้าง HTML สำหรับส่วนสรุปการทำนายที่มีความเชื่อมั่นสูง
        summary_html = generate_high_confidence_summary(analysis_data)
        
        # สร้าง HTML สำหรับตารางการวิเคราะห์
        europa_league_html = generate_league_table_html(analysis_data['europa_league'], 'UEFA Europa League')
        conference_league_html = generate_league_table_html(analysis_data['conference_league'], 'UEFA Europa Conference League')
        
        # สร้าง HTML ทั้งหมด
        html_content = f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 UEFA Europa League & Conference League Analysis - July 17-18, 2025</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        :root {{
            --primary-color: #ffffff;
            --secondary-color: #f8f9fa;
            --accent-color: #6c5ce7;
            --text-color: #333333;
            --text-muted: #6c757d;
            --success-color: #00b894;
            --warning-color: #fdcb6e;
            --danger-color: #e17055;
            --info-color: #0984e3;
            --highlight-color: #dfe6e9;
            --border-color: #e9ecef;
        }}
        
        body {{
            padding: 0;
            margin: 0;
            background-color: var(--primary-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        .container {{
            max-width: 1400px;
            padding: 0;
        }}
        
        .header {{
            background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
            color: white;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .header h1 {{
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 10px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .league-section {{
            background-color: var(--secondary-color);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
            border: 1px solid var(--border-color);
        }}
        
        .league-section h3 {{
            color: var(--accent-color);
            font-weight: 600;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }}
        
        .high-confidence-section {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(108, 92, 231, 0.15);
            margin-bottom: 30px;
            border: 1px solid #d6dee6;
        }}
        
        .high-confidence-section h2 {{
            color: var(--accent-color);
            font-weight: 700;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
        }}
        
        .high-confidence-section h2 i {{
            margin-right: 10px;
            font-size: 1.5em;
            color: #e84393;
        }}
        
        .table {{
            color: var(--text-color);
            border-collapse: separate;
            border-spacing: 0;
        }}
        
        .table-dark {{
            background-color: #495057;
            color: white;
        }}
        
        .table-striped > tbody > tr:nth-of-type(odd) {{
            background-color: rgba(0, 0, 0, 0.02);
        }}
        
        .table-hover > tbody > tr:hover {{
            background-color: rgba(108, 92, 231, 0.05);
        }}
        
        .table-success {{
            background-color: rgba(0, 184, 148, 0.1) !important;
        }}
        
        .text-success {{
            color: var(--success-color) !important;
        }}
        
        .text-warning {{
            color: var(--warning-color) !important;
        }}
        
        .text-danger {{
            color: var(--danger-color) !important;
        }}
        
        .text-primary {{
            color: var(--info-color) !important;
        }}
        
        .text-muted {{
            color: var(--text-muted) !important;
        }}
        
        .fw-bold {{
            font-weight: 700 !important;
        }}
        
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: var(--text-muted);
            padding: 20px;
            border-top: 1px solid var(--border-color);
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--primary-color);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--accent-color);
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #5549c9;
        }}
        
        /* ปรับแต่งตาราง */
        .table thead th {{
            background-color: #495057;
            color: white;
            border-color: #495057;
        }}
        
        .table td, .table th {{
            padding: 12px;
            vertical-align: middle;
        }}
        
        /* ปรับแต่งแถวที่มีความเชื่อมั่นสูง */
        .high-confidence-row {{
            background-color: rgba(0, 184, 148, 0.1) !important;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="container py-4">
        <div class="header">
            <h1>🏆 UEFA EUROPA LEAGUE & CONFERENCE LEAGUE ANALYSIS</h1>
            <p>July 17-18, 2025 | Advanced ML Predictions with Head-to-Head Data</p>
        </div>
        
        <!-- High Confidence Summary Start -->
        {summary_html}
        <!-- High Confidence Summary End -->
        
        <!-- UEFA Europa League Section Start -->
        {europa_league_html}
        <!-- UEFA Europa League Section End -->
        
        <!-- UEFA Conference League Section Start -->
        {conference_league_html}
        <!-- UEFA Conference League Section End -->
        
        <div class="footer">
            <p>© 2025 Ultra Advanced Multi-League Football Predictor | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''
        
        # บันทึกไฟล์ index.html ที่สร้างใหม่
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'index_backup_{timestamp}.html'
        with open(backup_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 สร้างไฟล์ index.html ใหม่เรียบร้อยแล้ว (สำรองไว้ที่ {backup_filename})")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

def generate_high_confidence_summary(analysis_data):
    """สร้าง HTML สำหรับส่วนสรุปการทำนายที่มีความเชื่อมั่นสูง"""
    # รวบรวมการทำนายที่มีความเชื่อมั่นสูง (80%+)
    high_confidence_predictions = []
    for league in ['europa_league', 'conference_league']:
        for match in analysis_data[league]:
            # ตรวจสอบการทำนายผลการแข่งขัน
            if match['match_result']['confidence'] >= 80:
                high_confidence_predictions.append({
                    'match': f"{match['home_team']} vs {match['away_team']}",
                    'type': 'Match Result',
                    'prediction': match['match_result']['prediction'],
                    'confidence': match['match_result']['confidence'],
                    'kickoff': match['kickoff_thai']
                })
            
            # ตรวจสอบการทำนาย over/under
            if match['over_under']['confidence'] >= 80:
                high_confidence_predictions.append({
                    'match': f"{match['home_team']} vs {match['away_team']}",
                    'type': 'Over/Under',
                    'prediction': match['over_under']['prediction'],
                    'confidence': match['over_under']['confidence'],
                    'kickoff': match['kickoff_thai']
                })
            
            # ตรวจสอบการทำนาย both teams to score
            if match['both_teams_score']['confidence'] >= 80:
                high_confidence_predictions.append({
                    'match': f"{match['home_team']} vs {match['away_team']}",
                    'type': 'Both Teams Score',
                    'prediction': match['both_teams_score']['prediction'],
                    'confidence': match['both_teams_score']['confidence'],
                    'kickoff': match['kickoff_thai']
                })
            
            # ตรวจสอบการทำนาย corners
            if match['corners']['total']['confidence'] >= 80:
                high_confidence_predictions.append({
                    'match': f"{match['home_team']} vs {match['away_team']}",
                    'type': 'Corners',
                    'prediction': f"{match['corners']['total']['prediction']} {match['corners']['total']['line']}",
                    'confidence': match['corners']['total']['confidence'],
                    'kickoff': match['kickoff_thai']
                })
            
            # ตรวจสอบการทำนาย exact score
            if 'exact_score' in match and match['exact_score']['confidence'] >= 80:
                high_confidence_predictions.append({
                    'match': f"{match['home_team']} vs {match['away_team']}",
                    'type': 'Exact Score',
                    'prediction': match['exact_score']['prediction'],
                    'confidence': match['exact_score']['confidence'],
                    'kickoff': match['kickoff_thai']
                })
    
    # เรียงลำดับตามความเชื่อมั่น
    high_confidence_predictions.sort(key=lambda x: x['confidence'], reverse=True)
    
    # สร้าง HTML สำหรับส่วนสรุป
    html = '''
    <div class="high-confidence-section mb-5">
        <h2><i class="fas fa-fire"></i> HIGH CONFIDENCE PREDICTIONS (80%+)</h2>
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Match</th>
                        <th>Time (Thai)</th>
                        <th>Prediction Type</th>
                        <th>Prediction</th>
                        <th>Confidence</th>
                    </tr>
                </thead>
                <tbody>
    '''
    
    for pred in high_confidence_predictions:
        confidence_class = "text-success fw-bold" if pred['confidence'] >= 90 else "text-success"
        html += f'''
        <tr class="high-confidence-row">
            <td>{pred['match']}</td>
            <td>{pred['kickoff'].split(' ')[1]}</td>
            <td>{pred['type']}</td>
            <td>{pred['prediction']}</td>
            <td class="{confidence_class}">{pred['confidence']}%</td>
        </tr>
        '''
    
    html += '''
                </tbody>
            </table>
        </div>
    </div>
    '''
    
    return html

def generate_league_table_html(matches, league_name):
    """สร้าง HTML สำหรับตารางการวิเคราะห์"""
    html = f'''
    <div class="league-section mb-5">
        <h3>{league_name} - July 17-18, 2025</h3>
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Match</th>
                        <th>Time (Thai)</th>
                        <th>Match Result</th>
                        <th>Over/Under 2.5</th>
                        <th>Both Teams Score</th>
                        <th>Corners</th>
                        <th>Exact Score</th>
                    </tr>
                </thead>
                <tbody>
    '''
    
    # เรียงลำดับตามเวลาแข่งขัน
    matches = sorted(matches, key=lambda x: x['kickoff_thai'])
    
    for match in matches:
        home_team = match['home_team']
        away_team = match['away_team']
        kickoff = match['kickoff_thai']
        
        # Match Result
        match_result = match['match_result']
        match_prediction = match_result['prediction']
        match_confidence = match_result['confidence']
        match_color = get_confidence_color(match_confidence)
        
        # Over/Under
        over_under = match['over_under']
        ou_prediction = over_under['prediction']
        ou_confidence = over_under['confidence']
        ou_color = get_confidence_color(ou_confidence)
        
        # Both Teams Score
        btts = match['both_teams_score']
        btts_prediction = btts['prediction']
        btts_confidence = btts['confidence']
        btts_color = get_confidence_color(btts_confidence)
        
        # Corners
        corners = match['corners']['total']
        corners_prediction = corners['prediction']
        corners_confidence = corners['confidence']
        corners_color = get_confidence_color(corners_confidence)
        
        # Exact Score
        exact_score = match.get('exact_score', {})
        score_prediction = exact_score.get('prediction', 'N/A')
        score_confidence = exact_score.get('confidence', 0)
        score_color = get_confidence_color(score_confidence)
        
        # เพิ่มการเน้นแถวสำหรับการทำนายที่มีความเชื่อมั่นสูง
        row_class = ""
        if (match_confidence >= 80 or ou_confidence >= 80 or btts_confidence >= 80 or 
            corners_confidence >= 80 or score_confidence >= 80):
            row_class = "high-confidence-row"
        
        html += f'''
        <tr class="{row_class}">
            <td>{home_team} vs {away_team}</td>
            <td>{kickoff.split(' ')[1]}</td>
            <td class="{match_color}">{match_prediction} ({match_confidence}%)</td>
            <td class="{ou_color}">{ou_prediction} ({ou_confidence}%)</td>
            <td class="{btts_color}">{btts_prediction} ({btts_confidence}%)</td>
            <td class="{corners_color}">{corners_prediction} {corners['line']} ({corners_confidence}%)</td>
            <td class="{score_color}">{score_prediction} ({score_confidence}%)</td>
        </tr>
        '''
    
    html += '''
                </tbody>
            </table>
        </div>
    </div>
    '''
    
    return html

def get_confidence_color(confidence):
    """กำหนดสีตามค่าความเชื่อมั่น"""
    if confidence >= 90:
        return "text-success fw-bold"  # สีเขียวเข้มและตัวหนา
    elif confidence >= 80:
        return "text-success"  # สีเขียว
    elif confidence >= 65:
        return "text-primary"  # สีน้ำเงิน
    elif confidence >= 55:
        return ""  # สีปกติ
    else:
        return "text-muted"  # สีเทา

if __name__ == "__main__":
    create_light_theme_index()
