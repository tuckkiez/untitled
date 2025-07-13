#!/usr/bin/env python3
"""
🚀 Advanced Real Football Predictions System
ระบบทำนายฟุตบอลแบบจริงจังด้วยข้อมูลสถิติจริง

4 ค่าการทำนาย:
1. Home/Away/Draw
2. Handicap
3. Over/Under 2.5
4. Corner (Half-time & Full-time)
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import time
from collections import defaultdict
import math

class AdvancedRealPredictor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        
        # League mappings for real data
        self.league_mappings = {
            "FIFA Club World Cup": {"id": 1, "season": 2025},
            "Premier League": {"id": 39, "season": 2024},  # England
            "La Liga": {"id": 140, "season": 2024},        # Spain
            "Bundesliga": {"id": 78, "season": 2024},      # Germany
            "Serie A": {"id": 135, "season": 2024},        # Italy
            "Ligue 1": {"id": 61, "season": 2024},         # France
            "Allsvenskan": {"id": 113, "season": 2025},    # Sweden
            "Veikkausliiga": {"id": 244, "season": 2025},  # Finland
            "Serie A": {"id": 71, "season": 2025},         # Brazil
            "Liga MX": {"id": 262, "season": 2025},        # Mexico
            "Primera A": {"id": 239, "season": 2025},      # Colombia
            "K League 2": {"id": 293, "season": 2025}      # South Korea
        }
        
        # Team league mappings for FIFA Club World Cup
        self.team_leagues = {
            "Chelsea": {"league_id": 39, "season": 2024, "country": "England"},
            "Paris Saint Germain": {"league_id": 61, "season": 2024, "country": "France"},
            "Real Madrid": {"league_id": 140, "season": 2024, "country": "Spain"},
            "Manchester City": {"league_id": 39, "season": 2024, "country": "England"},
            "Bayern Munich": {"league_id": 78, "season": 2024, "country": "Germany"},
            "Inter": {"league_id": 135, "season": 2024, "country": "Italy"},
            "Juventus": {"league_id": 135, "season": 2024, "country": "Italy"},
            "AC Milan": {"league_id": 135, "season": 2024, "country": "Italy"}
        }

    def make_api_request(self, endpoint, params=None):
        """ทำ API request พร้อม error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(0.5)  # Rate limiting
            return response.json()
        except Exception as e:
            print(f"❌ API Error: {e}")
            return None

    def get_team_statistics(self, team_id, league_id, season):
        """ดึงสถิติทีมจากลีก"""
        params = {
            'team': team_id,
            'league': league_id,
            'season': season
        }
        
        data = self.make_api_request('teams/statistics', params)
        if not data or not data.get('response'):
            return None
            
        stats = data['response']
        
        # คำนวณสถิติสำคัญ
        fixtures = stats.get('fixtures', {})
        goals = stats.get('goals', {})
        
        total_games = fixtures.get('played', {}).get('total', 0)
        if total_games == 0:
            return None
            
        return {
            'games_played': total_games,
            'wins_home': fixtures.get('wins', {}).get('home', 0),
            'wins_away': fixtures.get('wins', {}).get('away', 0),
            'draws_home': fixtures.get('draws', {}).get('home', 0),
            'draws_away': fixtures.get('draws', {}).get('away', 0),
            'losses_home': fixtures.get('loses', {}).get('home', 0),
            'losses_away': fixtures.get('loses', {}).get('away', 0),
            'goals_for_home': goals.get('for', {}).get('total', {}).get('home', 0),
            'goals_for_away': goals.get('for', {}).get('total', {}).get('away', 0),
            'goals_against_home': goals.get('against', {}).get('total', {}).get('home', 0),
            'goals_against_away': goals.get('against', {}).get('total', {}).get('away', 0),
            'avg_goals_for': goals.get('for', {}).get('average', {}).get('total', '0'),
            'avg_goals_against': goals.get('against', {}).get('average', {}).get('total', '0')
        }

    def get_head_to_head(self, team1_id, team2_id):
        """ดึงข้อมูลการเจอกันในอดีต"""
        params = {
            'h2h': f"{team1_id}-{team2_id}",
            'last': 10
        }
        
        data = self.make_api_request('fixtures/headtohead', params)
        if not data or not data.get('response'):
            return []
            
        return data['response']

    def get_recent_form(self, team_id, league_id, season, last_games=5):
        """ดึงฟอร์มล่าสุดของทีม"""
        params = {
            'team': team_id,
            'league': league_id,
            'season': season,
            'last': last_games
        }
        
        data = self.make_api_request('fixtures', params)
        if not data or not data.get('response'):
            return []
            
        return data['response']

    def calculate_elo_rating(self, team_stats, opponent_stats):
        """คำนวณ ELO rating แบบง่าย"""
        if not team_stats or not opponent_stats:
            return 1500  # Default ELO
            
        # คำนวณจากสถิติพื้นฐาน
        team_points = (team_stats['wins_home'] + team_stats['wins_away']) * 3 + \
                     (team_stats['draws_home'] + team_stats['draws_away'])
        
        opponent_points = (opponent_stats['wins_home'] + opponent_stats['wins_away']) * 3 + \
                         (opponent_stats['draws_home'] + opponent_stats['draws_away'])
        
        team_games = team_stats['games_played']
        opponent_games = opponent_stats['games_played']
        
        if team_games == 0 or opponent_games == 0:
            return 1500
            
        team_avg = team_points / team_games
        opponent_avg = opponent_points / opponent_games
        
        # แปลงเป็น ELO (1200-1800 range)
        base_elo = 1500
        elo_diff = (team_avg - opponent_avg) * 100
        
        return max(1200, min(1800, base_elo + elo_diff))

    def predict_match_result(self, home_stats, away_stats, h2h_data, home_form, away_form):
        """ทำนายผลการแข่งขัน (Home/Draw/Away)"""
        if not home_stats or not away_stats:
            return {"prediction": "Draw", "confidence": 50, "probabilities": [33, 34, 33]}
        
        # คำนวณความแข็งแกร่งของทีม
        home_strength = self.calculate_team_strength(home_stats, True)
        away_strength = self.calculate_team_strength(away_stats, False)
        
        # ปรับตามฟอร์มล่าสุด
        home_form_factor = self.calculate_form_factor(home_form, True)
        away_form_factor = self.calculate_form_factor(away_form, False)
        
        # ปรับตาม H2H
        h2h_factor = self.calculate_h2h_factor(h2h_data)
        
        # คำนวณความน่าจะเป็น
        home_prob = (home_strength + home_form_factor + h2h_factor['home']) / 3
        away_prob = (away_strength + away_form_factor + h2h_factor['away']) / 3
        draw_prob = 100 - home_prob - away_prob
        
        # ปรับให้รวมเป็น 100%
        total = home_prob + draw_prob + away_prob
        if total > 0:
            home_prob = (home_prob / total) * 100
            draw_prob = (draw_prob / total) * 100
            away_prob = (away_prob / total) * 100
        
        # หาผลทำนาย
        max_prob = max(home_prob, draw_prob, away_prob)
        if max_prob == home_prob:
            prediction = "Home Win"
        elif max_prob == away_prob:
            prediction = "Away Win"
        else:
            prediction = "Draw"
        
        confidence = min(95, max(55, int(max_prob)))
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": [round(home_prob, 1), round(draw_prob, 1), round(away_prob, 1)]
        }

    def predict_handicap(self, home_stats, away_stats):
        """ทำนาย Handicap"""
        if not home_stats or not away_stats:
            return {"handicap": "0", "confidence": 50}
        
        # คำนวณความแตกต่างของทีม
        home_avg_goals = float(home_stats.get('avg_goals_for', '0') or '0')
        away_avg_goals = float(away_stats.get('avg_goals_for', '0') or '0')
        
        home_avg_concede = float(home_stats.get('avg_goals_against', '0') or '0')
        away_avg_concede = float(away_stats.get('avg_goals_against', '0') or '0')
        
        # คำนวณ goal difference
        home_gd = home_avg_goals - home_avg_concede
        away_gd = away_avg_goals - away_avg_concede
        
        difference = home_gd - away_gd
        
        # กำหนด handicap
        if difference > 1.0:
            handicap = "-1.5"
            confidence = min(85, 60 + int(difference * 10))
        elif difference > 0.5:
            handicap = "-1"
            confidence = min(80, 55 + int(difference * 15))
        elif difference > 0.2:
            handicap = "-0.5"
            confidence = min(75, 50 + int(difference * 20))
        elif difference < -1.0:
            handicap = "+1.5"
            confidence = min(85, 60 + int(abs(difference) * 10))
        elif difference < -0.5:
            handicap = "+1"
            confidence = min(80, 55 + int(abs(difference) * 15))
        elif difference < -0.2:
            handicap = "+0.5"
            confidence = min(75, 50 + int(abs(difference) * 20))
        else:
            handicap = "0"
            confidence = 60
        
        return {"handicap": handicap, "confidence": confidence}

    def predict_over_under(self, home_stats, away_stats, h2h_data):
        """ทำนาย Over/Under 2.5"""
        if not home_stats or not away_stats:
            return {"prediction": "Under 2.5", "confidence": 55}
        
        # คำนวณเฉลี่ยประตูรวม
        home_avg_for = float(home_stats.get('avg_goals_for', '0') or '0')
        home_avg_against = float(home_stats.get('avg_goals_against', '0') or '0')
        away_avg_for = float(away_stats.get('avg_goals_for', '0') or '0')
        away_avg_against = float(away_stats.get('avg_goals_against', '0') or '0')
        
        # คำนวณประตูที่คาดว่าจะเกิดขึ้น
        expected_home_goals = (home_avg_for + away_avg_against) / 2
        expected_away_goals = (away_avg_for + home_avg_against) / 2
        total_expected = expected_home_goals + expected_away_goals
        
        # ปรับตาม H2H
        if h2h_data:
            h2h_avg = sum(match['goals']['home'] + match['goals']['away'] 
                         for match in h2h_data if match.get('goals')) / len(h2h_data)
            total_expected = (total_expected + h2h_avg) / 2
        
        # ทำนาย
        if total_expected > 2.7:
            prediction = "Over 2.5"
            confidence = min(85, 60 + int((total_expected - 2.5) * 15))
        elif total_expected < 2.3:
            prediction = "Under 2.5"
            confidence = min(85, 60 + int((2.5 - total_expected) * 15))
        else:
            prediction = "Over 2.5" if total_expected >= 2.5 else "Under 2.5"
            confidence = 55
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "expected_goals": round(total_expected, 2)
        }

    def predict_corners(self, home_stats, away_stats):
        """ทำนาย Corner (Half-time & Full-time)"""
        # ใช้สถิติพื้นฐานในการประมาณ
        if not home_stats or not away_stats:
            return {
                "halftime": {"prediction": "Under 5", "confidence": 60},
                "fulltime": {"prediction": "Over 9", "confidence": 65}
            }
        
        # ประมาณจากการเล่นรุกของทีม
        home_attack = float(home_stats.get('avg_goals_for', '0') or '0')
        away_attack = float(away_stats.get('avg_goals_for', '0') or '0')
        
        # คำนวณ corner ที่คาดหวัง
        expected_corners = (home_attack + away_attack) * 4  # ประมาณ 4 corner ต่อ 1 goal
        
        # Half-time (ประมาณ 40% ของ full-time)
        ht_corners = expected_corners * 0.4
        ft_corners = expected_corners
        
        # ทำนาย Half-time
        if ht_corners > 5.5:
            ht_pred = "Over 5"
            ht_conf = min(80, 60 + int((ht_corners - 5) * 5))
        else:
            ht_pred = "Under 5"
            ht_conf = min(80, 60 + int((5 - ht_corners) * 5))
        
        # ทำนาย Full-time
        if ft_corners > 9.5:
            ft_pred = "Over 9"
            ft_conf = min(80, 60 + int((ft_corners - 9) * 3))
        else:
            ft_pred = "Under 9"
            ft_conf = min(80, 60 + int((9 - ft_corners) * 3))
        
        return {
            "halftime": {"prediction": ht_pred, "confidence": ht_conf},
            "fulltime": {"prediction": ft_pred, "confidence": ft_conf},
            "expected_corners": round(ft_corners, 1)
        }

    def calculate_team_strength(self, stats, is_home):
        """คำนวณความแข็งแกร่งของทีม"""
        if not stats:
            return 50
        
        total_games = stats['games_played']
        if total_games == 0:
            return 50
        
        if is_home:
            wins = stats['wins_home']
            draws = stats['draws_home']
            losses = stats['losses_home']
            home_games = wins + draws + losses
            if home_games == 0:
                return 50
            strength = ((wins * 3 + draws) / (home_games * 3)) * 100
        else:
            wins = stats['wins_away']
            draws = stats['draws_away']
            losses = stats['losses_away']
            away_games = wins + draws + losses
            if away_games == 0:
                return 50
            strength = ((wins * 3 + draws) / (away_games * 3)) * 100
        
        return max(20, min(80, strength))

    def calculate_form_factor(self, form_data, is_home):
        """คำนวณฟอร์มล่าสุด"""
        if not form_data:
            return 50
        
        points = 0
        games = 0
        
        for match in form_data[-5:]:  # 5 เกมล่าสุด
            if not match.get('teams') or not match.get('goals'):
                continue
                
            home_team = match['teams']['home']['id']
            away_team = match['teams']['away']['id']
            home_goals = match['goals']['home']
            away_goals = match['goals']['away']
            
            games += 1
            
            # ตรวจสอบว่าทีมเล่นเป็นเจ้าบ้านหรือทีมเยือน
            if (is_home and match.get('fixture', {}).get('venue', {}).get('name')) or \
               (not is_home and not match.get('fixture', {}).get('venue', {}).get('name')):
                if home_goals > away_goals:
                    points += 3
                elif home_goals == away_goals:
                    points += 1
            else:
                if away_goals > home_goals:
                    points += 3
                elif home_goals == away_goals:
                    points += 1
        
        if games == 0:
            return 50
            
        form_percentage = (points / (games * 3)) * 100
        return max(20, min(80, form_percentage))

    def calculate_h2h_factor(self, h2h_data):
        """คำนวณปัจจัยจากการเจอกันในอดีต"""
        if not h2h_data:
            return {"home": 50, "away": 50}
        
        home_wins = 0
        away_wins = 0
        draws = 0
        
        for match in h2h_data[-5:]:  # 5 เกมล่าสุด
            if not match.get('goals'):
                continue
                
            home_goals = match['goals']['home']
            away_goals = match['goals']['away']
            
            if home_goals > away_goals:
                home_wins += 1
            elif away_goals > home_goals:
                away_wins += 1
            else:
                draws += 1
        
        total = home_wins + away_wins + draws
        if total == 0:
            return {"home": 50, "away": 50}
        
        home_factor = (home_wins / total) * 100
        away_factor = (away_wins / total) * 100
        
        return {"home": home_factor, "away": away_factor}

    def get_fifa_club_world_cup_prediction(self, home_team, away_team):
        """ทำนายพิเศษสำหรับ FIFA Club World Cup"""
        print(f"🏆 Analyzing FIFA Club World Cup: {home_team} vs {away_team}")
        
        # ดึงข้อมูลทีมจากลีกต้นสังกัด
        home_league_info = self.team_leagues.get(home_team)
        away_league_info = self.team_leagues.get(away_team)
        
        if not home_league_info or not away_league_info:
            print(f"⚠️ Team league info not found, using default prediction")
            return self.get_default_prediction()
        
        # ค้นหา team ID
        home_team_id = self.find_team_id(home_team, home_league_info['league_id'])
        away_team_id = self.find_team_id(away_team, away_league_info['league_id'])
        
        if not home_team_id or not away_team_id:
            print(f"⚠️ Team IDs not found, using default prediction")
            return self.get_default_prediction()
        
        # ดึงสถิติจากลีกต้นสังกัด
        home_stats = self.get_team_statistics(home_team_id, home_league_info['league_id'], home_league_info['season'])
        away_stats = self.get_team_statistics(away_team_id, away_league_info['league_id'], away_league_info['season'])
        
        # ดึงข้อมูล H2H และฟอร์ม
        h2h_data = self.get_head_to_head(home_team_id, away_team_id)
        home_form = self.get_recent_form(home_team_id, home_league_info['league_id'], home_league_info['season'])
        away_form = self.get_recent_form(away_team_id, away_league_info['league_id'], away_league_info['season'])
        
        # ปรับค่าสำหรับการแข่งขันระดับโลก (เพิ่มความไม่แน่นอน)
        predictions = self.generate_full_prediction(home_stats, away_stats, h2h_data, home_form, away_form)
        
        # ปรับความมั่นใจลงเนื่องจากเป็นการแข่งขันพิเศษ
        for key in predictions:
            if isinstance(predictions[key], dict) and 'confidence' in predictions[key]:
                predictions[key]['confidence'] = max(60, predictions[key]['confidence'] - 10)
        
        return predictions

    def find_team_id(self, team_name, league_id):
        """ค้นหา team ID จากชื่อทีม"""
        params = {'league': league_id, 'season': 2024}
        data = self.make_api_request('teams', params)
        
        if not data or not data.get('response'):
            return None
        
        for team in data['response']:
            if team['team']['name'].lower() == team_name.lower():
                return team['team']['id']
        
        return None

    def generate_full_prediction(self, home_stats, away_stats, h2h_data, home_form, away_form):
        """สร้างการทำนายครบทั้ง 4 ค่า"""
        result_pred = self.predict_match_result(home_stats, away_stats, h2h_data, home_form, away_form)
        handicap_pred = self.predict_handicap(home_stats, away_stats)
        ou_pred = self.predict_over_under(home_stats, away_stats, h2h_data)
        corner_pred = self.predict_corners(home_stats, away_stats)
        
        return {
            "match_result": result_pred,
            "handicap": handicap_pred,
            "over_under": ou_pred,
            "corners": corner_pred
        }

    def get_default_prediction(self):
        """การทำนายเริ่มต้นเมื่อไม่มีข้อมูล"""
        return {
            "match_result": {"prediction": "Draw", "confidence": 55, "probabilities": [30, 40, 30]},
            "handicap": {"handicap": "0", "confidence": 50},
            "over_under": {"prediction": "Over 2.5", "confidence": 60, "expected_goals": 2.8},
            "corners": {
                "halftime": {"prediction": "Under 5", "confidence": 60},
                "fulltime": {"prediction": "Over 9", "confidence": 65},
                "expected_corners": 10.5
            }
        }

if __name__ == "__main__":
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    predictor = AdvancedRealPredictor(api_key)
    
    # ทดสอบการทำนาย FIFA Club World Cup
    fifa_prediction = predictor.get_fifa_club_world_cup_prediction("Chelsea", "Paris Saint Germain")
    print(json.dumps(fifa_prediction, indent=2))
