#!/usr/bin/env python3
"""
🚀 UEFA Real Data Analyzer - July 17-18, 2025
วิเคราะห์ข้อมูลจริงและทำนายผลการแข่งขัน UEFA Europa League และ UEFA Europa Conference League
"""

import json
import os
import numpy as np
import pandas as pd
from datetime import datetime
import pytz
from typing import Dict, List, Any
import glob

class UEFARealDataAnalyzer:
    def __init__(self):
        self.thai_tz = pytz.timezone('Asia/Bangkok')
        self.data_dir = "api_data/uefa_real_data"
        self.team_data_cache = {}
        self.h2h_data_cache = {}
        self.fixtures_data_cache = {}
        self.odds_data_cache = {}
        
        # โหลดข้อมูลจาก API
        self.load_data_from_api()
    
    def load_data_from_api(self):
        """โหลดข้อมูลจาก API"""
        print("📥 กำลังโหลดข้อมูลจาก API...")
        
        # โหลดข้อมูลทีม
        team_files = glob.glob(f"{self.data_dir}/team_info_*.json")
        for file in team_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'response' in data and len(data['response']) > 0:
                        team_id = data['response'][0]['team']['id']
                        self.team_data_cache[team_id] = data['response'][0]
            except Exception as e:
                print(f"❌ ไม่สามารถโหลดข้อมูลทีมจากไฟล์ {file}: {e}")
        
        print(f"✅ โหลดข้อมูลทีม {len(self.team_data_cache)} ทีม")
        
        # โหลดข้อมูลประวัติการเจอกัน
        h2h_files = glob.glob(f"{self.data_dir}/h2h_*.json")
        for file in h2h_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'response' in data:
                        # ดึง team_id จากชื่อไฟล์
                        filename = os.path.basename(file)
                        team_ids = filename.replace('h2h_', '').replace('.json', '').split('_')
                        if len(team_ids) == 2:
                            key = f"{team_ids[0]}_{team_ids[1]}"
                            self.h2h_data_cache[key] = data['response']
            except Exception as e:
                print(f"❌ ไม่สามารถโหลดข้อมูลประวัติการเจอกันจากไฟล์ {file}: {e}")
        
        print(f"✅ โหลดข้อมูลประวัติการเจอกัน {len(self.h2h_data_cache)} คู่")
        
        # โหลดข้อมูลการแข่งขันของทีม
        fixtures_files = glob.glob(f"{self.data_dir}/team_fixtures_*.json")
        for file in fixtures_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'response' in data:
                        # ดึง team_id จากชื่อไฟล์
                        filename = os.path.basename(file)
                        team_id = filename.replace('team_fixtures_', '').split('_')[0]
                        self.fixtures_data_cache[team_id] = data['response']
            except Exception as e:
                print(f"❌ ไม่สามารถโหลดข้อมูลการแข่งขันของทีมจากไฟล์ {file}: {e}")
        
        print(f"✅ โหลดข้อมูลการแข่งขันของทีม {len(self.fixtures_data_cache)} ทีม")
        
        # โหลดข้อมูลอัตราต่อรอง
        odds_files = glob.glob(f"{self.data_dir}/fixture_odds_*.json")
        for file in odds_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'response' in data and len(data['response']) > 0:
                        # ดึง fixture_id จากชื่อไฟล์
                        filename = os.path.basename(file)
                        fixture_id = filename.replace('fixture_odds_', '').replace('.json', '')
                        self.odds_data_cache[fixture_id] = data['response']
            except Exception as e:
                print(f"❌ ไม่สามารถโหลดข้อมูลอัตราต่อรองจากไฟล์ {file}: {e}")
        
        print(f"✅ โหลดข้อมูลอัตราต่อรอง {len(self.odds_data_cache)} รายการ")
    
    def get_team_form(self, team_id):
        """ดึงข้อมูลฟอร์มของทีม"""
        if str(team_id) not in self.fixtures_data_cache:
            return {
                "form": "UNKNOWN",
                "win_rate": 0.5,
                "draw_rate": 0.25,
                "lose_rate": 0.25,
                "goals_scored_avg": 1.5,
                "goals_conceded_avg": 1.5,
                "clean_sheets_rate": 0.2,
                "both_teams_scored_rate": 0.5,
                "over_2_5_rate": 0.5,
                "corners_avg": 10.0,
                "corners_for_avg": 5.0,
                "corners_against_avg": 5.0,
                "corners_first_half_avg": 4.0,
                "corners_second_half_avg": 6.0
            }
        
        fixtures = self.fixtures_data_cache[str(team_id)]
        
        # กรองเฉพาะการแข่งขันที่จบแล้ว
        completed_fixtures = [f for f in fixtures if f['fixture']['status']['short'] == 'FT']
        
        if not completed_fixtures:
            return {
                "form": "UNKNOWN",
                "win_rate": 0.5,
                "draw_rate": 0.25,
                "lose_rate": 0.25,
                "goals_scored_avg": 1.5,
                "goals_conceded_avg": 1.5,
                "clean_sheets_rate": 0.2,
                "both_teams_scored_rate": 0.5,
                "over_2_5_rate": 0.5,
                "corners_avg": 10.0,
                "corners_for_avg": 5.0,
                "corners_against_avg": 5.0,
                "corners_first_half_avg": 4.0,
                "corners_second_half_avg": 6.0
            }
        
        # คำนวณฟอร์ม
        form = ""
        wins = 0
        draws = 0
        loses = 0
        goals_scored = 0
        goals_conceded = 0
        clean_sheets = 0
        both_teams_scored = 0
        over_2_5 = 0
        
        for fixture in completed_fixtures:
            is_home = fixture['teams']['home']['id'] == int(team_id)
            team_goals = fixture['goals']['home'] if is_home else fixture['goals']['away']
            opponent_goals = fixture['goals']['away'] if is_home else fixture['goals']['home']
            
            # บันทึกผลการแข่งขัน
            if team_goals > opponent_goals:
                form += "W"
                wins += 1
            elif team_goals == opponent_goals:
                form += "D"
                draws += 1
            else:
                form += "L"
                loses += 1
            
            # บันทึกประตู
            goals_scored += team_goals
            goals_conceded += opponent_goals
            
            # บันทึก clean sheet
            if opponent_goals == 0:
                clean_sheets += 1
            
            # บันทึก both teams scored
            if team_goals > 0 and opponent_goals > 0:
                both_teams_scored += 1
            
            # บันทึก over 2.5
            if team_goals + opponent_goals > 2.5:
                over_2_5 += 1
        
        # คำนวณค่าเฉลี่ย
        num_fixtures = len(completed_fixtures)
        win_rate = wins / num_fixtures
        draw_rate = draws / num_fixtures
        lose_rate = loses / num_fixtures
        goals_scored_avg = goals_scored / num_fixtures
        goals_conceded_avg = goals_conceded / num_fixtures
        clean_sheets_rate = clean_sheets / num_fixtures
        both_teams_scored_rate = both_teams_scored / num_fixtures
        over_2_5_rate = over_2_5 / num_fixtures
        
        # คำนวณค่าเฉลี่ยคอร์เนอร์ (ใช้ค่าเฉลี่ยทั่วไปเนื่องจากข้อมูลอาจไม่มี)
        corners_avg = 10.0
        corners_for_avg = 5.0
        corners_against_avg = 5.0
        corners_first_half_avg = 4.0
        corners_second_half_avg = 6.0
        
        return {
            "form": form[:5],  # เอาแค่ 5 นัดล่าสุด
            "win_rate": win_rate,
            "draw_rate": draw_rate,
            "lose_rate": lose_rate,
            "goals_scored_avg": goals_scored_avg,
            "goals_conceded_avg": goals_conceded_avg,
            "clean_sheets_rate": clean_sheets_rate,
            "both_teams_scored_rate": both_teams_scored_rate,
            "over_2_5_rate": over_2_5_rate,
            "corners_avg": corners_avg,
            "corners_for_avg": corners_for_avg,
            "corners_against_avg": corners_against_avg,
            "corners_first_half_avg": corners_first_half_avg,
            "corners_second_half_avg": corners_second_half_avg
        }
    
    def get_head_to_head_stats(self, home_team_id, away_team_id):
        """ดึงข้อมูลสถิติการเจอกันของสองทีม"""
        key1 = f"{home_team_id}_{away_team_id}"
        key2 = f"{away_team_id}_{home_team_id}"
        
        if key1 not in self.h2h_data_cache and key2 not in self.h2h_data_cache:
            return {
                "matches_count": 0,
                "home_wins": 0,
                "away_wins": 0,
                "draws": 0,
                "goals_scored_avg": 0,
                "goals_conceded_avg": 0,
                "both_teams_scored_rate": 0,
                "over_2_5_rate": 0,
                "corners_avg": 0
            }
        
        h2h_data = self.h2h_data_cache.get(key1, self.h2h_data_cache.get(key2, []))
        
        # กรองเฉพาะการแข่งขันที่จบแล้ว
        completed_fixtures = [f for f in h2h_data if f['fixture']['status']['short'] == 'FT']
        
        if not completed_fixtures:
            return {
                "matches_count": 0,
                "home_wins": 0,
                "away_wins": 0,
                "draws": 0,
                "goals_scored_avg": 0,
                "goals_conceded_avg": 0,
                "both_teams_scored_rate": 0,
                "over_2_5_rate": 0,
                "corners_avg": 0
            }
        
        # คำนวณสถิติ
        home_wins = 0
        away_wins = 0
        draws = 0
        total_goals = 0
        both_teams_scored = 0
        over_2_5 = 0
        
        for fixture in completed_fixtures:
            home_goals = fixture['goals']['home']
            away_goals = fixture['goals']['away']
            
            # บันทึกผลการแข่งขัน
            if home_goals > away_goals:
                if fixture['teams']['home']['id'] == int(home_team_id):
                    home_wins += 1
                else:
                    away_wins += 1
            elif home_goals < away_goals:
                if fixture['teams']['home']['id'] == int(home_team_id):
                    away_wins += 1
                else:
                    home_wins += 1
            else:
                draws += 1
            
            # บันทึกประตู
            total_goals += home_goals + away_goals
            
            # บันทึก both teams scored
            if home_goals > 0 and away_goals > 0:
                both_teams_scored += 1
            
            # บันทึก over 2.5
            if home_goals + away_goals > 2.5:
                over_2_5 += 1
        
        # คำนวณค่าเฉลี่ย
        num_fixtures = len(completed_fixtures)
        goals_avg = total_goals / num_fixtures
        both_teams_scored_rate = both_teams_scored / num_fixtures
        over_2_5_rate = over_2_5 / num_fixtures
        
        return {
            "matches_count": num_fixtures,
            "home_wins": home_wins,
            "away_wins": away_wins,
            "draws": draws,
            "goals_avg": goals_avg,
            "both_teams_scored_rate": both_teams_scored_rate,
            "over_2_5_rate": over_2_5_rate,
            "corners_avg": 10.0  # ใช้ค่าเฉลี่ยทั่วไปเนื่องจากข้อมูลอาจไม่มี
        }
    
    def get_odds(self, fixture_id):
        """ดึงข้อมูลอัตราต่อรอง"""
        if str(fixture_id) not in self.odds_data_cache:
            return {
                "match_winner": {"home": 2.0, "draw": 3.5, "away": 3.0},
                "over_under_2_5": {"over": 1.9, "under": 1.9},
                "both_teams_score": {"yes": 1.8, "no": 2.0},
                "handicap": {"home": 1.9, "away": 1.9},
                "asian_handicap": {"value": 0, "home": 1.9, "away": 1.9}
            }
        
        odds_data = self.odds_data_cache[str(fixture_id)]
        
        # ค่าเริ่มต้น
        result = {
            "match_winner": {"home": 2.0, "draw": 3.5, "away": 3.0},
            "over_under_2_5": {"over": 1.9, "under": 1.9},
            "both_teams_score": {"yes": 1.8, "no": 2.0},
            "handicap": {"home": 1.9, "away": 1.9},
            "asian_handicap": {"value": 0, "home": 1.9, "away": 1.9}
        }
        
        # ดึงข้อมูลอัตราต่อรอง
        try:
            for bookmaker in odds_data:
                if 'bookmaker' not in bookmaker:
                    continue
                    
                for bet in bookmaker['bookmaker']['bets']:
                    # Match Winner (1X2)
                    if bet['id'] == 1:
                        for value in bet['values']:
                            if value['value'] == 'Home':
                                result['match_winner']['home'] = float(value['odd'])
                            elif value['value'] == 'Draw':
                                result['match_winner']['draw'] = float(value['odd'])
                            elif value['value'] == 'Away':
                                result['match_winner']['away'] = float(value['odd'])
                    
                    # Over/Under 2.5
                    elif bet['id'] == 5:
                        for value in bet['values']:
                            if value['value'] == 'Over 2.5':
                                result['over_under_2_5']['over'] = float(value['odd'])
                            elif value['value'] == 'Under 2.5':
                                result['over_under_2_5']['under'] = float(value['odd'])
                    
                    # Both Teams Score
                    elif bet['id'] == 8:
                        for value in bet['values']:
                            if value['value'] == 'Yes':
                                result['both_teams_score']['yes'] = float(value['odd'])
                            elif value['value'] == 'No':
                                result['both_teams_score']['no'] = float(value['odd'])
                    
                    # Asian Handicap
                    elif bet['id'] == 4:
                        for value in bet['values']:
                            if '-' in value['value'] and 'Home' in value['value']:
                                handicap_value = float(value['value'].split(' ')[0])
                                result['asian_handicap']['value'] = handicap_value
                                result['asian_handicap']['home'] = float(value['odd'])
                            elif '+' in value['value'] and 'Away' in value['value']:
                                result['asian_handicap']['away'] = float(value['odd'])
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการดึงข้อมูลอัตราต่อรอง: {e}")
        
        return result
    
    def analyze_match(self, fixture):
        """วิเคราะห์การแข่งขัน"""
        fixture_id = fixture['fixture']['id']
        home_team_id = fixture['teams']['home']['id']
        away_team_id = fixture['teams']['away']['id']
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        
        # ดึงข้อมูลฟอร์มของทีม
        home_form = self.get_team_form(home_team_id)
        away_form = self.get_team_form(away_team_id)
        
        # ดึงข้อมูลประวัติการเจอกัน
        h2h_stats = self.get_head_to_head_stats(home_team_id, away_team_id)
        
        # ดึงข้อมูลอัตราต่อรอง
        odds = self.get_odds(fixture_id)
        
        # คำนวณความน่าจะเป็นจากอัตราต่อรอง
        match_winner_probs = self.odds_to_probabilities(odds['match_winner'])
        over_under_probs = self.odds_to_probabilities(odds['over_under_2_5'])
        btts_probs = self.odds_to_probabilities(odds['both_teams_score'])
        
        # ปรับความน่าจะเป็นตามฟอร์มของทีม
        home_win_prob = match_winner_probs['home'] * 0.7 + home_form['win_rate'] * 0.3
        draw_prob = match_winner_probs['draw']
        away_win_prob = match_winner_probs['away'] * 0.7 + away_form['win_rate'] * 0.3
        
        # ปรับให้ผลรวมเป็น 1
        total = home_win_prob + draw_prob + away_win_prob
        home_win_prob /= total
        draw_prob /= total
        away_win_prob /= total
        
        # คำนวณความน่าจะเป็นของ Over/Under
        over_prob = over_under_probs['over'] * 0.7 + (home_form['over_2_5_rate'] + away_form['over_2_5_rate']) / 2 * 0.3
        under_prob = 1 - over_prob
        
        # คำนวณความน่าจะเป็นของ Both Teams to Score
        btts_yes_prob = btts_probs['yes'] * 0.7 + (home_form['both_teams_scored_rate'] + away_form['both_teams_scored_rate']) / 2 * 0.3
        btts_no_prob = 1 - btts_yes_prob
        
        # คำนวณ Expected Goals
        expected_goals_home = home_form['goals_scored_avg'] * 0.6 + away_form['goals_conceded_avg'] * 0.4
        expected_goals_away = away_form['goals_scored_avg'] * 0.6 + home_form['goals_conceded_avg'] * 0.4
        expected_goals = expected_goals_home + expected_goals_away
        
        # คำนวณ Handicap
        handicap_value = odds['asian_handicap']['value']
        home_handicap_prob = 0.5
        away_handicap_prob = 0.5
        
        if handicap_value != 0:
            # ปรับความน่าจะเป็นตามค่า handicap
            if handicap_value < 0:  # เจ้าบ้านเป็นต่อ
                home_handicap_prob = home_win_prob * 0.8
                away_handicap_prob = 1 - home_handicap_prob
            else:  # ทีมเยือนเป็นต่อ
                away_handicap_prob = away_win_prob * 0.8
                home_handicap_prob = 1 - away_handicap_prob
        
        # คำนวณ Corners
        # ใช้ข้อมูลจาก corner_utility.py
        from corner_utility import get_corner_stats, get_head_to_head_corners
        
        home_corners = get_corner_stats(home_team)
        away_corners = get_corner_stats(away_team)
        h2h_corners = get_head_to_head_corners(home_team, away_team)
        
        # คำนวณความน่าจะเป็นของ Corners
        expected_corners_total = (home_corners['corners_for_avg'] + away_corners['corners_for_avg']) * 0.9
        expected_corners_first_half = (home_corners['first_half_corners_avg'] + away_corners['first_half_corners_avg']) * 0.5
        expected_corners_second_half = (home_corners['second_half_corners_avg'] + away_corners['second_half_corners_avg']) * 0.5
        
        # ปรับตามประวัติการเจอกัน
        if h2h_corners['matches_count'] > 0:
            h2h_weight = min(0.3, h2h_corners['matches_count'] * 0.05)  # น้ำหนักสูงสุด 30%
            team_weight = 1 - h2h_weight
            
            expected_corners_total = (expected_corners_total * team_weight) + (h2h_corners['avg_total_corners'] * h2h_weight)
            expected_corners_first_half = (expected_corners_first_half * team_weight) + (h2h_corners['avg_first_half_corners'] * h2h_weight)
            expected_corners_second_half = (expected_corners_second_half * team_weight) + (h2h_corners['avg_second_half_corners'] * h2h_weight)
        
        # คำนวณความน่าจะเป็นของ Over/Under Corners
        over_9_5_corners_prob = home_corners['over_9_5_rate'] * 0.5 + away_corners['over_9_5_rate'] * 0.5
        if h2h_corners['matches_count'] > 0:
            over_9_5_corners_prob = over_9_5_corners_prob * 0.7 + h2h_corners['over_9_5_rate'] * 0.3
        
        # ปรับตามค่าคาดการณ์
        if expected_corners_total > 10.5:
            over_9_5_corners_prob += 0.15
        elif expected_corners_total < 8.5:
            over_9_5_corners_prob -= 0.15
        
        over_9_5_corners_prob = max(0.05, min(0.95, over_9_5_corners_prob))
        under_9_5_corners_prob = 1 - over_9_5_corners_prob
        
        # คำนวณความน่าจะเป็นของ Over/Under Corners ครึ่งแรก
        over_4_5_first_half_corners_prob = home_corners['over_4_5_first_half_rate'] * 0.5 + away_corners['over_4_5_first_half_rate'] * 0.5
        if h2h_corners['matches_count'] > 0:
            over_4_5_first_half_corners_prob = over_4_5_first_half_corners_prob * 0.7 + h2h_corners['over_4_5_first_half_rate'] * 0.3
        
        # ปรับตามค่าคาดการณ์
        if expected_corners_first_half > 5:
            over_4_5_first_half_corners_prob += 0.15
        elif expected_corners_first_half < 3.5:
            over_4_5_first_half_corners_prob -= 0.15
        
        over_4_5_first_half_corners_prob = max(0.05, min(0.95, over_4_5_first_half_corners_prob))
        under_4_5_first_half_corners_prob = 1 - over_4_5_first_half_corners_prob
        
        # คำนวณความน่าจะเป็นของ Over/Under Corners ครึ่งหลัง
        over_5_5_second_half_corners_prob = home_corners['over_5_5_second_half_rate'] * 0.5 + away_corners['over_5_5_second_half_rate'] * 0.5
        if h2h_corners['matches_count'] > 0:
            over_5_5_second_half_corners_prob = over_5_5_second_half_corners_prob * 0.7 + h2h_corners['over_5_5_second_half_rate'] * 0.3
        
        # ปรับตามค่าคาดการณ์
        if expected_corners_second_half > 6:
            over_5_5_second_half_corners_prob += 0.15
        elif expected_corners_second_half < 4.5:
            over_5_5_second_half_corners_prob -= 0.15
        
        over_5_5_second_half_corners_prob = max(0.05, min(0.95, over_5_5_second_half_corners_prob))
        under_5_5_second_half_corners_prob = 1 - over_5_5_second_half_corners_prob
        
        # สร้างผลการวิเคราะห์
        analysis = {
            'fixture_id': fixture_id,
            'home_team': home_team,
            'away_team': away_team,
            'kickoff_thai': self.convert_to_thai_time(fixture['fixture']['date']),
            'competition': fixture['league']['name'],
            'match_result': {
                'home_win': round(home_win_prob * 100, 1),
                'draw': round(draw_prob * 100, 1),
                'away_win': round(away_win_prob * 100, 1),
                'prediction': 'Home Win' if home_win_prob > max(draw_prob, away_win_prob) else 
                             'Draw' if draw_prob > max(home_win_prob, away_win_prob) else 'Away Win',
                'confidence': round(max(home_win_prob, draw_prob, away_win_prob) * 100, 1)
            },
            'over_under': {
                'line': 2.5,
                'over_prob': round(over_prob * 100, 1),
                'under_prob': round(under_prob * 100, 1),
                'prediction': 'Over' if over_prob > under_prob else 'Under',
                'confidence': round(max(over_prob, under_prob) * 100, 1),
                'expected_goals': round(expected_goals, 1)
            },
            'both_teams_score': {
                'yes_prob': round(btts_yes_prob * 100, 1),
                'no_prob': round(btts_no_prob * 100, 1),
                'prediction': 'Yes' if btts_yes_prob > btts_no_prob else 'No',
                'confidence': round(max(btts_yes_prob, btts_no_prob) * 100, 1)
            },
            'corners': {
                'total': {
                    'line': 9.5,
                    'over_prob': round(over_9_5_corners_prob * 100, 1),
                    'under_prob': round(under_9_5_corners_prob * 100, 1),
                    'prediction': 'Over' if over_9_5_corners_prob > under_9_5_corners_prob else 'Under',
                    'confidence': round(max(over_9_5_corners_prob, under_9_5_corners_prob) * 100, 1),
                    'expected_corners': round(expected_corners_total, 1)
                },
                'first_half': {
                    'line': 4.5,
                    'over_prob': round(over_4_5_first_half_corners_prob * 100, 1),
                    'under_prob': round(under_4_5_first_half_corners_prob * 100, 1),
                    'prediction': 'Over' if over_4_5_first_half_corners_prob > under_4_5_first_half_corners_prob else 'Under',
                    'confidence': round(max(over_4_5_first_half_corners_prob, under_4_5_first_half_corners_prob) * 100, 1),
                    'expected_corners': round(expected_corners_first_half, 1)
                },
                'second_half': {
                    'line': 5.5,
                    'over_prob': round(over_5_5_second_half_corners_prob * 100, 1),
                    'under_prob': round(under_5_5_second_half_corners_prob * 100, 1),
                    'prediction': 'Over' if over_5_5_second_half_corners_prob > under_5_5_second_half_corners_prob else 'Under',
                    'confidence': round(max(over_5_5_second_half_corners_prob, under_5_5_second_half_corners_prob) * 100, 1),
                    'expected_corners': round(expected_corners_second_half, 1)
                }
            },
            'handicap': {
                'line': handicap_value,
                'home_prob': round(home_handicap_prob * 100, 1),
                'away_prob': round(away_handicap_prob * 100, 1),
                'prediction': f"{home_team} {handicap_value}" if home_handicap_prob > away_handicap_prob else f"{away_team} +{abs(handicap_value)}",
                'confidence': round(max(home_handicap_prob, away_handicap_prob) * 100, 1)
            },
            'team_stats': {
                'home': {
                    'win_rate_home': f"{round(home_form['win_rate'] * 100)}%",
                    'goals_scored': home_form['goals_scored_avg'],
                    'goals_conceded': home_form['goals_conceded_avg'],
                    'form': home_form['form']
                },
                'away': {
                    'win_rate_away': f"{round(away_form['win_rate'] * 100)}%",
                    'goals_scored': away_form['goals_scored_avg'],
                    'goals_conceded': away_form['goals_conceded_avg'],
                    'form': away_form['form']
                }
            },
            'head_to_head': {
                'matches_count': h2h_stats['matches_count'],
                'home_wins': h2h_stats['home_wins'],
                'away_wins': h2h_stats['away_wins'],
                'draws': h2h_stats['draws'],
                'goals_avg': h2h_stats['goals_avg'] if 'goals_avg' in h2h_stats else 0,
                'both_teams_scored_rate': h2h_stats['both_teams_scored_rate'],
                'over_2_5_rate': h2h_stats['over_2_5_rate']
            }
        }
        
        return analysis
    
    def odds_to_probabilities(self, odds):
        """แปลงอัตราต่อรองเป็นความน่าจะเป็น"""
        probabilities = {}
        total_probability = 0
        
        for key, value in odds.items():
            probabilities[key] = 1 / value
            total_probability += probabilities[key]
        
        # ปรับให้ผลรวมเป็น 1
        for key in probabilities:
            probabilities[key] /= total_probability
        
        return probabilities
    
    def convert_to_thai_time(self, utc_time):
        """แปลงเวลา UTC เป็นเวลาไทย"""
        try:
            utc_dt = datetime.fromisoformat(utc_time.replace('Z', '+00:00'))
            thai_dt = utc_dt.astimezone(self.thai_tz)
            return thai_dt.strftime('%Y-%m-%d %H:%M')
        except:
            return utc_time
    
    def analyze_uefa_fixtures(self):
        """วิเคราะห์การแข่งขัน UEFA Europa League และ UEFA Europa Conference League"""
        # โหลดข้อมูลการแข่งขัน UEFA
        try:
            with open(f"{self.data_dir}/uefa_fixtures_july_17_18_2025.json", 'r', encoding='utf-8') as f:
                fixtures_data = json.load(f)
        except Exception as e:
            print(f"❌ ไม่สามารถโหลดข้อมูลการแข่งขัน UEFA: {e}")
            return None
        
        # รวมการแข่งขันทั้งหมด
        all_fixtures = []
        for date, fixtures in fixtures_data.items():
            all_fixtures.extend(fixtures)
        
        # แยกการแข่งขันตามประเภท
        europa_league_fixtures = []
        conference_league_fixtures = []
        
        for fixture in all_fixtures:
            league_name = fixture['league']['name'].lower()
            if 'europa league' in league_name:
                europa_league_fixtures.append(fixture)
            elif 'conference league' in league_name:
                conference_league_fixtures.append(fixture)
        
        # วิเคราะห์การแข่งขัน
        europa_league_analyses = []
        conference_league_analyses = []
        
        print(f"📊 กำลังวิเคราะห์การแข่งขัน UEFA Europa League ({len(europa_league_fixtures)} รายการ)...")
        for fixture in europa_league_fixtures:
            analysis = self.analyze_match(fixture)
            europa_league_analyses.append(analysis)
        
        print(f"📊 กำลังวิเคราะห์การแข่งขัน UEFA Europa Conference League ({len(conference_league_fixtures)} รายการ)...")
        for fixture in conference_league_fixtures:
            analysis = self.analyze_match(fixture)
            conference_league_analyses.append(analysis)
        
        # สร้างผลการวิเคราะห์
        result = {
            'europa_league': europa_league_analyses,
            'conference_league': conference_league_analyses,
            'analysis_time': datetime.now().isoformat()
        }
        
        # บันทึกผลการวิเคราะห์
        with open('uefa_competitions_real_data_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ บันทึกผลการวิเคราะห์ลงไฟล์: uefa_competitions_real_data_analysis.json")
        
        return result

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 UEFA Real Data Analyzer - July 17-18, 2025")
    print("=" * 60)
    
    # สร้าง analyzer
    analyzer = UEFARealDataAnalyzer()
    
    # วิเคราะห์การแข่งขัน UEFA
    analyzer.analyze_uefa_fixtures()
    
    print("\n✅ เสร็จสมบูรณ์!")

if __name__ == "__main__":
    main()
