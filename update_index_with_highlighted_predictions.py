#!/usr/bin/env python3
"""
🚀 Update Index with Highlighted Predictions - July 17-18, 2025
อัปเดตหน้า index.html โดยเน้นการทำนายที่มีความเชื่อมั่นสูง
"""

import json
import os
import re
from datetime import datetime

def update_index_with_highlighted_predictions():
    """อัปเดตหน้า index.html โดยเน้นการทำนายที่มีความเชื่อมั่นสูง"""
    print("🚀 Update Index with Highlighted Predictions - July 17-18, 2025")
    print("=" * 60)
    
    try:
        # โหลดข้อมูลการวิเคราะห์ที่สมบูรณ์
        with open('uefa_competitions_real_data_analysis_with_h2h_percentages.json', 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # โหลดไฟล์ index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # เพิ่มส่วนสรุปการทำนายที่มีความเชื่อมั่นสูง
        summary_html = generate_high_confidence_summary(analysis_data)
        
        # สร้าง HTML สำหรับตารางการวิเคราะห์
        europa_league_html = generate_league_table_html(analysis_data['europa_league'], 'UEFA Europa League')
        conference_league_html = generate_league_table_html(analysis_data['conference_league'], 'UEFA Europa Conference League')
        
        # แทนที่เนื้อหาในไฟล์ index.html
        # ค้นหาส่วนของ UEFA Europa League
        europa_pattern = r'<!-- UEFA Europa League Section Start -->.*?<!-- UEFA Europa League Section End -->'
        europa_replacement = f'<!-- UEFA Europa League Section Start -->\n{europa_league_html}\n<!-- UEFA Europa League Section End -->'
        html_content = re.sub(europa_pattern, europa_replacement, html_content, flags=re.DOTALL)
        
        # ค้นหาส่วนของ UEFA Europa Conference League
        conference_pattern = r'<!-- UEFA Conference League Section Start -->.*?<!-- UEFA Conference League Section End -->'
        conference_replacement = f'<!-- UEFA Conference League Section Start -->\n{conference_league_html}\n<!-- UEFA Conference League Section End -->'
        html_content = re.sub(conference_pattern, conference_replacement, html_content, flags=re.DOTALL)
        
        # เพิ่มส่วนสรุปการทำนายที่มีความเชื่อมั่นสูงก่อนส่วนของ UEFA Europa League
        summary_pattern = r'<!-- High Confidence Summary Start -->.*?<!-- High Confidence Summary End -->'
        if re.search(summary_pattern, html_content, re.DOTALL):
            # แทนที่ส่วนสรุปที่มีอยู่แล้ว
            summary_replacement = f'<!-- High Confidence Summary Start -->\n{summary_html}\n<!-- High Confidence Summary End -->'
            html_content = re.sub(summary_pattern, summary_replacement, html_content, flags=re.DOTALL)
        else:
            # เพิ่มส่วนสรุปใหม่ก่อนส่วนของ UEFA Europa League
            europa_section_start = '<!-- UEFA Europa League Section Start -->'
            summary_section = f'<!-- High Confidence Summary Start -->\n{summary_html}\n<!-- High Confidence Summary End -->\n\n'
            html_content = html_content.replace(europa_section_start, summary_section + europa_section_start)
        
        # บันทึกไฟล์ index.html ที่อัปเดตแล้ว
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'index_backup_{timestamp}.html'
        with open(backup_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 บันทึกไฟล์ index.html ที่อัปเดตแล้ว (สำรองไว้ที่ {backup_filename})")
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
        <h2 class="text-success mb-3">🔥 High Confidence Predictions (80%+)</h2>
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="thead-dark">
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
        confidence_class = "text-success font-weight-bold" if pred['confidence'] >= 90 else "text-success"
        html += f'''
        <tr>
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
        <h3 class="text-primary mb-3">{league_name} - July 17-18, 2025</h3>
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="thead-dark">
                    <tr>
                        <th>Match</th>
                        <th>Time (Thai)</th>
                        <th>Match Result</th>
                        <th>Over/Under 2.5</th>
                        <th>Both Teams Score</th>
                        <th>Corners</th>
                        <th>H2H Stats</th>
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
        
        # Head to Head
        h2h = match['head_to_head']
        if h2h['matches_count'] > 0:
            h2h_text = f"{h2h['matches_count']} matches<br>"
            h2h_text += f"<span class='text-success'>Home: {h2h['home_win_pct']}%</span> | "
            h2h_text += f"<span class='text-warning'>Draw: {h2h['draw_pct']}%</span> | "
            h2h_text += f"<span class='text-danger'>Away: {h2h['away_win_pct']}%</span><br>"
            h2h_text += f"Over: {h2h['over_pct']}% | Under: {h2h['under_pct']}%<br>"
            h2h_text += f"BTTS: Yes {h2h['btts_yes_pct']}% | No {h2h['btts_no_pct']}%"
        else:
            h2h_text = "No previous meetings"
        
        # Exact Score
        exact_score = match.get('exact_score', {})
        score_prediction = exact_score.get('prediction', 'N/A')
        score_confidence = exact_score.get('confidence', 0)
        score_color = get_confidence_color(score_confidence)
        
        # เพิ่มการเน้นแถวสำหรับการทำนายที่มีความเชื่อมั่นสูง
        row_class = ""
        if (match_confidence >= 80 or ou_confidence >= 80 or btts_confidence >= 80 or 
            corners_confidence >= 80 or score_confidence >= 80):
            row_class = "table-success"
        
        html += f'''
        <tr class="{row_class}">
            <td>{home_team} vs {away_team}</td>
            <td>{kickoff.split(' ')[1]}</td>
            <td class="{match_color}">{match_prediction} ({match_confidence}%)</td>
            <td class="{ou_color}">{ou_prediction} ({ou_confidence}%)</td>
            <td class="{btts_color}">{btts_prediction} ({btts_confidence}%)</td>
            <td class="{corners_color}">{corners_prediction} {corners['line']} ({corners_confidence}%)</td>
            <td>{h2h_text}</td>
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
        return "text-success font-weight-bold"  # สีเขียวเข้มและตัวหนา
    elif confidence >= 80:
        return "text-success"  # สีเขียว
    elif confidence >= 65:
        return "text-primary"  # สีน้ำเงิน
    elif confidence >= 55:
        return ""  # สีปกติ
    else:
        return "text-muted"  # สีเทา

if __name__ == "__main__":
    update_index_with_highlighted_predictions()
