#!/usr/bin/env python3
"""
🚀 Update Index with H2H Percentages - July 17-18, 2025
อัปเดตหน้า index.html โดยแสดงข้อมูล head-to-head เป็นเปอร์เซ็นต์และใช้ในการคำนวณการทำนาย
"""

import json
import os
import re
from datetime import datetime

def update_index_with_h2h_percentages():
    """อัปเดตหน้า index.html โดยแสดงข้อมูล head-to-head เป็นเปอร์เซ็นต์"""
    print("🚀 Update Index with H2H Percentages - July 17-18, 2025")
    print("=" * 60)
    
    try:
        # โหลดข้อมูลการวิเคราะห์ที่สมบูรณ์
        with open('uefa_competitions_real_data_analysis_with_exact_scores_final.json', 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # คำนวณเปอร์เซ็นต์ head-to-head และปรับปรุงการทำนาย
        for league in ['europa_league', 'conference_league']:
            for match in analysis_data[league]:
                # คำนวณเปอร์เซ็นต์ head-to-head
                calculate_h2h_percentages(match)
                
                # ปรับปรุงการทำนายโดยใช้ข้อมูล head-to-head
                update_predictions_with_h2h(match)
        
        # บันทึกข้อมูลที่อัปเดตแล้ว
        with open('uefa_competitions_real_data_analysis_with_h2h_percentages.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 บันทึกข้อมูลที่อัปเดตแล้วลงไฟล์: uefa_competitions_real_data_analysis_with_h2h_percentages.json")
        
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

def calculate_h2h_percentages(match):
    """คำนวณเปอร์เซ็นต์ head-to-head"""
    h2h = match['head_to_head']
    
    # คำนวณเปอร์เซ็นต์เฉพาะเมื่อมีข้อมูล head-to-head
    if h2h['matches_count'] > 0:
        # คำนวณเปอร์เซ็นต์การชนะ เสมอ แพ้
        h2h['home_win_pct'] = round((h2h['home_wins'] / h2h['matches_count']) * 100, 1)
        h2h['away_win_pct'] = round((h2h['away_wins'] / h2h['matches_count']) * 100, 1)
        h2h['draw_pct'] = round((h2h['draws'] / h2h['matches_count']) * 100, 1)
        
        # คำนวณเปอร์เซ็นต์ over/under
        h2h['over_pct'] = round(h2h['over_2_5_rate'] * 100, 1)
        h2h['under_pct'] = round((1 - h2h['over_2_5_rate']) * 100, 1)
        
        # คำนวณเปอร์เซ็นต์ both teams to score
        h2h['btts_yes_pct'] = round(h2h['both_teams_scored_rate'] * 100, 1)
        h2h['btts_no_pct'] = round((1 - h2h['both_teams_scored_rate']) * 100, 1)
    else:
        # กำหนดค่าเริ่มต้นเมื่อไม่มีข้อมูล head-to-head
        h2h['home_win_pct'] = 0
        h2h['away_win_pct'] = 0
        h2h['draw_pct'] = 0
        h2h['over_pct'] = 0
        h2h['under_pct'] = 0
        h2h['btts_yes_pct'] = 0
        h2h['btts_no_pct'] = 0

def update_predictions_with_h2h(match):
    """ปรับปรุงการทำนายโดยใช้ข้อมูล head-to-head"""
    h2h = match['head_to_head']
    
    # ปรับปรุงการทำนายเฉพาะเมื่อมีข้อมูล head-to-head
    if h2h['matches_count'] > 0:
        # กำหนดน้ำหนักของข้อมูล head-to-head
        h2h_weight = min(0.4, h2h['matches_count'] * 0.15)  # น้ำหนักสูงสุด 40%
        team_weight = 1 - h2h_weight
        
        # ปรับปรุงการทำนายผลการแข่งขัน
        match_result = match['match_result']
        home_win_prob = match_result['home_win'] / 100
        away_win_prob = match_result['away_win'] / 100
        draw_prob = match_result['draw'] / 100
        
        # ผสมผสานกับข้อมูล head-to-head
        h2h_home_win_prob = h2h['home_win_pct'] / 100
        h2h_away_win_prob = h2h['away_win_pct'] / 100
        h2h_draw_prob = h2h['draw_pct'] / 100
        
        # คำนวณความน่าจะเป็นใหม่
        new_home_win_prob = (home_win_prob * team_weight) + (h2h_home_win_prob * h2h_weight)
        new_away_win_prob = (away_win_prob * team_weight) + (h2h_away_win_prob * h2h_weight)
        new_draw_prob = (draw_prob * team_weight) + (h2h_draw_prob * h2h_weight)
        
        # ปรับให้ผลรวมเป็น 1
        total = new_home_win_prob + new_away_win_prob + new_draw_prob
        new_home_win_prob /= total
        new_away_win_prob /= total
        new_draw_prob /= total
        
        # อัปเดตค่าเปอร์เซ็นต์
        match_result['home_win'] = round(new_home_win_prob * 100, 1)
        match_result['away_win'] = round(new_away_win_prob * 100, 1)
        match_result['draw'] = round(new_draw_prob * 100, 1)
        
        # กำหนดผลการทำนาย
        if new_home_win_prob > max(new_draw_prob, new_away_win_prob):
            match_result['prediction'] = "Home Win"
            match_result['confidence'] = round(new_home_win_prob * 100, 1)
        elif new_draw_prob > max(new_home_win_prob, new_away_win_prob):
            match_result['prediction'] = "Draw"
            match_result['confidence'] = round(new_draw_prob * 100, 1)
        else:
            match_result['prediction'] = "Away Win"
            match_result['confidence'] = round(new_away_win_prob * 100, 1)
        
        # ปรับปรุงการทำนาย over/under
        over_under = match['over_under']
        over_prob = over_under['over_prob'] / 100
        under_prob = over_under['under_prob'] / 100
        
        # ผสมผสานกับข้อมูล head-to-head
        h2h_over_prob = h2h['over_pct'] / 100
        h2h_under_prob = h2h['under_pct'] / 100
        
        # คำนวณความน่าจะเป็นใหม่
        new_over_prob = (over_prob * team_weight) + (h2h_over_prob * h2h_weight)
        new_under_prob = (under_prob * team_weight) + (h2h_under_prob * h2h_weight)
        
        # ปรับให้ผลรวมเป็น 1
        total = new_over_prob + new_under_prob
        new_over_prob /= total
        new_under_prob /= total
        
        # อัปเดตค่าเปอร์เซ็นต์
        over_under['over_prob'] = round(new_over_prob * 100, 1)
        over_under['under_prob'] = round(new_under_prob * 100, 1)
        
        # กำหนดผลการทำนาย
        if new_over_prob > new_under_prob:
            over_under['prediction'] = "Over"
            over_under['confidence'] = round(new_over_prob * 100, 1)
        else:
            over_under['prediction'] = "Under"
            over_under['confidence'] = round(new_under_prob * 100, 1)
        
        # ปรับปรุงการทำนาย both teams to score
        btts = match['both_teams_score']
        yes_prob = btts['yes_prob'] / 100
        no_prob = btts['no_prob'] / 100
        
        # ผสมผสานกับข้อมูล head-to-head
        h2h_yes_prob = h2h['btts_yes_pct'] / 100
        h2h_no_prob = h2h['btts_no_pct'] / 100
        
        # คำนวณความน่าจะเป็นใหม่
        new_yes_prob = (yes_prob * team_weight) + (h2h_yes_prob * h2h_weight)
        new_no_prob = (no_prob * team_weight) + (h2h_no_prob * h2h_weight)
        
        # ปรับให้ผลรวมเป็น 1
        total = new_yes_prob + new_no_prob
        new_yes_prob /= total
        new_no_prob /= total
        
        # อัปเดตค่าเปอร์เซ็นต์
        btts['yes_prob'] = round(new_yes_prob * 100, 1)
        btts['no_prob'] = round(new_no_prob * 100, 1)
        
        # กำหนดผลการทำนาย
        if new_yes_prob > new_no_prob:
            btts['prediction'] = "Yes"
            btts['confidence'] = round(new_yes_prob * 100, 1)
        else:
            btts['prediction'] = "No"
            btts['confidence'] = round(new_no_prob * 100, 1)

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
    update_index_with_h2h_percentages()
