#!/usr/bin/env python3
"""
🚀 Update Index with Complete Data - July 17-18, 2025
อัปเดตหน้า index.html ด้วยข้อมูลที่สมบูรณ์ครบทั้ง 31 คู่
"""

import json
import os
import re
from datetime import datetime

def update_index_with_complete_data():
    """อัปเดตหน้า index.html ด้วยข้อมูลที่สมบูรณ์"""
    print("🚀 Update Index with Complete Data - July 17-18, 2025")
    print("=" * 60)
    
    try:
        # โหลดข้อมูลการวิเคราะห์ที่สมบูรณ์
        with open('uefa_competitions_real_data_analysis_complete.json', 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # โหลดไฟล์ index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
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
                        <th>H2H</th>
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
        h2h_text = f"{h2h['matches_count']} matches"
        if h2h['matches_count'] > 0:
            h2h_text += f": {h2h['home_wins']}-{h2h['draws']}-{h2h['away_wins']}"
            if h2h['results']:
                h2h_text += f" ({', '.join(h2h['results'])})"
        
        # Exact Score
        exact_score = match.get('exact_score', {})
        score_prediction = exact_score.get('prediction', 'N/A')
        score_confidence = exact_score.get('confidence', 0)
        score_color = get_confidence_color(score_confidence)
        
        html += f'''
        <tr>
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
    if confidence >= 80:
        return "text-success font-weight-bold"  # สีเขียว
    elif confidence >= 65:
        return "text-primary"  # สีน้ำเงิน
    elif confidence >= 55:
        return ""  # สีปกติ
    else:
        return "text-muted"  # สีเทา

if __name__ == "__main__":
    update_index_with_complete_data()
