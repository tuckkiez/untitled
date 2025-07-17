#!/usr/bin/env python3
"""
🚀 Fix All Head to Head Data - July 17-18, 2025
แก้ไขข้อมูล head to head ของทุกคู่และคำนวณค่าเปอร์เซ็นต์ใหม่
"""

import json
import os
import numpy as np
import math
from datetime import datetime

def fix_head_to_head_data():
    """แก้ไขข้อมูล head to head ของทุกคู่"""
    print("🚀 Fix All Head to Head Data - July 17-18, 2025")
    print("=" * 60)
    
    # โหลดข้อมูลผลการวิเคราะห์
    try:
        with open('uefa_competitions_real_data_analysis_with_score_correct.json', 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # โหลดข้อมูล head to head ทั้งหมด
        with open('all_head_to_head_data.json', 'r', encoding='utf-8') as f:
            all_h2h_data = json.load(f)
        
        # แก้ไขข้อมูล head to head สำหรับทุกคู่
        for league in ['europa_league', 'conference_league']:
            for match in analysis_data[league]:
                home_team = match['home_team']
                away_team = match['away_team']
                key = f"{home_team} vs {away_team}"
                
                # ตรวจสอบว่ามีข้อมูล head to head หรือไม่
                if key in all_h2h_data:
                    h2h_data = all_h2h_data[key]
                    results = h2h_data['results']
                    
                    if results:
                        print(f"กำลังแก้ไขข้อมูล head to head ของคู่ {key}...")
                        print(f"  ก่อนแก้ไข: {match['head_to_head']}")
                        
                        # นับจำนวนการชนะ เสมอ แพ้
                        home_wins = 0
                        away_wins = 0
                        draws = 0
                        total_goals = 0
                        both_teams_scored = 0
                        over_2_5 = 0
                        
                        # สร้างข้อความสำหรับแสดงผลการแข่งขัน
                        h2h_results_text = []
                        
                        for result in results:
                            if result['home_team'] == home_team:
                                if result['home_goals'] > result['away_goals']:
                                    home_wins += 1
                                elif result['home_goals'] < result['away_goals']:
                                    away_wins += 1
                                else:
                                    draws += 1
                                
                                h2h_results_text.append(f"{result['home_goals']}-{result['away_goals']}")
                            elif result['away_team'] == home_team:
                                if result['away_goals'] > result['home_goals']:
                                    home_wins += 1
                                elif result['away_goals'] < result['home_goals']:
                                    away_wins += 1
                                else:
                                    draws += 1
                                
                                h2h_results_text.append(f"{result['away_goals']}-{result['home_goals']}")
                            
                            # คำนวณจำนวนประตูรวม
                            total_goals += result['home_goals'] + result['away_goals']
                            
                            # ตรวจสอบว่าทั้งสองทีมทำประตูหรือไม่
                            if result['home_goals'] > 0 and result['away_goals'] > 0:
                                both_teams_scored += 1
                            
                            # ตรวจสอบว่าประตูรวมมากกว่า 2.5 หรือไม่
                            if result['home_goals'] + result['away_goals'] > 2.5:
                                over_2_5 += 1
                        
                        # คำนวณค่าเฉลี่ย
                        matches_count = len(results)
                        goals_avg = total_goals / matches_count if matches_count > 0 else 0
                        both_teams_scored_rate = both_teams_scored / matches_count if matches_count > 0 else 0
                        over_2_5_rate = over_2_5 / matches_count if matches_count > 0 else 0
                        
                        # แก้ไขข้อมูล head to head
                        match['head_to_head'] = {
                            'matches_count': matches_count,
                            'home_wins': home_wins,
                            'away_wins': away_wins,
                            'draws': draws,
                            'goals_avg': goals_avg,
                            'both_teams_scored_rate': both_teams_scored_rate,
                            'over_2_5_rate': over_2_5_rate,
                            'results': h2h_results_text
                        }
                        
                        print(f"  หลังแก้ไข: {match['head_to_head']}")
                        
                        # คำนวณค่าเปอร์เซ็นต์ใหม่
                        recalculate_percentages(match)
        
        # บันทึกข้อมูลที่แก้ไขแล้ว
        with open('uefa_competitions_real_data_analysis_final.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 บันทึกข้อมูลที่แก้ไขแล้วลงไฟล์: uefa_competitions_real_data_analysis_final.json")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

def recalculate_percentages(match):
    """คำนวณค่าเปอร์เซ็นต์ใหม่"""
    # ดึงข้อมูลทีม
    home_team_stats = match['team_stats']['home']
    away_team_stats = match['team_stats']['away']
    h2h = match['head_to_head']
    
    # คำนวณค่าเปอร์เซ็นต์ใหม่สำหรับผลการแข่งขัน
    home_win_prob = float(home_team_stats['win_rate_home'].replace('%', '')) / 100
    away_win_prob = float(away_team_stats['win_rate_away'].replace('%', '')) / 100
    
    # ปรับตาม head to head
    if h2h['matches_count'] > 0:
        h2h_weight = min(0.3, h2h['matches_count'] * 0.1)  # น้ำหนักสูงสุด 30%
        team_weight = 1 - h2h_weight
        
        h2h_home_win_prob = h2h['home_wins'] / h2h['matches_count'] if h2h['matches_count'] > 0 else 0
        h2h_away_win_prob = h2h['away_wins'] / h2h['matches_count'] if h2h['matches_count'] > 0 else 0
        h2h_draw_prob = h2h['draws'] / h2h['matches_count'] if h2h['matches_count'] > 0 else 0
        
        home_win_prob = (home_win_prob * team_weight) + (h2h_home_win_prob * h2h_weight)
        away_win_prob = (away_win_prob * team_weight) + (h2h_away_win_prob * h2h_weight)
        draw_prob = 1 - home_win_prob - away_win_prob
        
        # ปรับให้ผลรวมเป็น 1
        total = home_win_prob + away_win_prob + draw_prob
        home_win_prob /= total
        away_win_prob /= total
        draw_prob /= total
    else:
        draw_prob = 1 - home_win_prob - away_win_prob
    
    # ปรับค่าให้อยู่ในช่วง 0-1
    home_win_prob = max(0, min(1, home_win_prob))
    away_win_prob = max(0, min(1, away_win_prob))
    draw_prob = max(0, min(1, draw_prob))
    
    # ปรับให้ผลรวมเป็น 1
    total = home_win_prob + away_win_prob + draw_prob
    home_win_prob /= total
    away_win_prob /= total
    draw_prob /= total
    
    # อัปเดตค่าเปอร์เซ็นต์
    match['match_result']['home_win'] = round(home_win_prob * 100, 1)
    match['match_result']['away_win'] = round(away_win_prob * 100, 1)
    match['match_result']['draw'] = round(draw_prob * 100, 1)
    
    # กำหนดผลการทำนาย
    if home_win_prob > max(draw_prob, away_win_prob):
        match['match_result']['prediction'] = "Home Win"
        match['match_result']['confidence'] = round(home_win_prob * 100, 1)
    elif draw_prob > max(home_win_prob, away_win_prob):
        match['match_result']['prediction'] = "Draw"
        match['match_result']['confidence'] = round(draw_prob * 100, 1)
    else:
        match['match_result']['prediction'] = "Away Win"
        match['match_result']['confidence'] = round(away_win_prob * 100, 1)
    
    # คำนวณค่าเปอร์เซ็นต์ใหม่สำหรับ over/under
    over_prob = 0.5  # ค่าเริ่มต้น
    
    # ปรับตาม head to head
    if h2h['matches_count'] > 0:
        h2h_weight = min(0.3, h2h['matches_count'] * 0.1)  # น้ำหนักสูงสุด 30%
        team_weight = 1 - h2h_weight
        
        over_prob = (over_prob * team_weight) + (h2h['over_2_5_rate'] * h2h_weight)
    
    # ปรับค่าให้อยู่ในช่วง 0-1
    over_prob = max(0.05, min(0.95, over_prob))
    under_prob = 1 - over_prob
    
    # อัปเดตค่าเปอร์เซ็นต์
    match['over_under']['over_prob'] = round(over_prob * 100, 1)
    match['over_under']['under_prob'] = round(under_prob * 100, 1)
    
    # กำหนดผลการทำนาย
    if over_prob > under_prob:
        match['over_under']['prediction'] = "Over"
        match['over_under']['confidence'] = round(over_prob * 100, 1)
    else:
        match['over_under']['prediction'] = "Under"
        match['over_under']['confidence'] = round(under_prob * 100, 1)
    
    # คำนวณค่าเปอร์เซ็นต์ใหม่สำหรับ both teams to score
    btts_yes_prob = 0.5  # ค่าเริ่มต้น
    
    # ปรับตาม head to head
    if h2h['matches_count'] > 0:
        h2h_weight = min(0.3, h2h['matches_count'] * 0.1)  # น้ำหนักสูงสุด 30%
        team_weight = 1 - h2h_weight
        
        btts_yes_prob = (btts_yes_prob * team_weight) + (h2h['both_teams_scored_rate'] * h2h_weight)
    
    # ปรับค่าให้อยู่ในช่วง 0-1
    btts_yes_prob = max(0.05, min(0.95, btts_yes_prob))
    btts_no_prob = 1 - btts_yes_prob
    
    # อัปเดตค่าเปอร์เซ็นต์
    match['both_teams_score']['yes_prob'] = round(btts_yes_prob * 100, 1)
    match['both_teams_score']['no_prob'] = round(btts_no_prob * 100, 1)
    
    # กำหนดผลการทำนาย
    if btts_yes_prob > btts_no_prob:
        match['both_teams_score']['prediction'] = "Yes"
        match['both_teams_score']['confidence'] = round(btts_yes_prob * 100, 1)
    else:
        match['both_teams_score']['prediction'] = "No"
        match['both_teams_score']['confidence'] = round(btts_no_prob * 100, 1)

if __name__ == "__main__":
    fix_head_to_head_data()
