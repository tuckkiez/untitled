#!/usr/bin/env python3
"""
🚀 J-League 2 Advanced ML Predictor
ระบบทำนายขั้นสูงด้วย Machine Learning สำหรับ J-League 2
ทำนาย 5 ค่า: ผลการแข่งขัน, Handicap, Over/Under, Corner ครึ่งแรก, Corner ครึ่งหลัง
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Advanced ML Models
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier, 
    ExtraTreesClassifier, AdaBoostClassifier, VotingClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score
from sklearn.impute import KNNImputer

class JLeague2AdvancedML:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        self.league_id = 99  # J2 League
        self.season = 2025
        
        # Advanced ML Models
        self.models = {
            'match_result': self._create_ensemble_model(),
            'handicap': self._create_ensemble_model(),
            'over_under': self._create_ensemble_model(),
            'corner_1st_half': self._create_ensemble_model(),
            'corner_2nd_half': self._create_ensemble_model()
        }
        
        # Scalers
        self.scalers = {
            'match_result': StandardScaler(),
            'handicap': StandardScaler(),
            'over_under': StandardScaler(),
            'corner_1st_half': StandardScaler(),
            'corner_2nd_half': StandardScaler()
        }
        
        # Data storage
        self.fixtures_data = []
        self.team_stats = {}
        self.feature_columns = []
        self.is_trained = False
        
    def _create_ensemble_model(self):
        """สร้าง Ensemble Model ขั้นสูง"""
        base_models = [
            ('rf', RandomForestClassifier(n_estimators=300, max_depth=15, random_state=42, n_jobs=-1)),
            ('gb', GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=8, random_state=42)),
            ('et', ExtraTreesClassifier(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1)),
            ('mlp', MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)),
            ('svm', SVC(C=1.0, kernel='rbf', probability=True, random_state=42))
        ]
        
        return VotingClassifier(
            estimators=base_models,
            voting='soft',
            n_jobs=-1
        )
    
    def make_api_request(self, endpoint: str, params: Dict = None) -> Dict:
        """ส่งคำขอ API"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ API Error: {response.status_code}")
                return {}
        except Exception as e:
            print(f"🚨 Request Error: {e}")
            return {}
    
    def load_fixtures_data(self) -> Tuple[List[Dict], List[Dict]]:
        """ดึงข้อมูลการแข่งขันทั้งหมด"""
        print("📥 กำลังดึงข้อมูลการแข่งขัน J-League 2...")
        
        params = {
            'league': self.league_id,
            'season': self.season
        }
        
        data = self.make_api_request('fixtures', params)
        
        if 'response' in data:
            fixtures = data['response']
            print(f"✅ ดึงข้อมูลได้ {len(fixtures)} การแข่งขัน")
            
            # แยกนัดที่จบแล้วและยังไม่แข่ง
            finished_fixtures = []
            upcoming_fixtures = []
            
            for fixture in fixtures:
                if fixture['fixture']['status']['short'] == 'FT':
                    finished_fixtures.append(fixture)
                elif fixture['fixture']['status']['short'] in ['NS', 'TBD']:
                    upcoming_fixtures.append(fixture)
            
            print(f"🏁 นัดที่จบแล้ว: {len(finished_fixtures)} นัด")
            print(f"⏳ นัดที่ยังไม่แข่ง: {len(upcoming_fixtures)} นัด")
            
            self.fixtures_data = fixtures
            return finished_fixtures, upcoming_fixtures
        
        return [], []
    
    def calculate_team_statistics(self, fixtures: List[Dict]) -> Dict:
        """คำนวณสถิติทีมขั้นสูง"""
        print("📊 กำลังคำนวณสถิติทีมขั้นสูง...")
        
        team_stats = {}
        
        for fixture in fixtures:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_goals = fixture['goals']['home'] or 0
            away_goals = fixture['goals']['away'] or 0
            
            # เริ่มต้นสถิติทีม
            for team in [home_team, away_team]:
                if team not in team_stats:
                    team_stats[team] = {
                        'matches_played': 0,
                        'wins': 0, 'draws': 0, 'losses': 0,
                        'goals_for': 0, 'goals_against': 0,
                        'home_wins': 0, 'home_draws': 0, 'home_losses': 0,
                        'away_wins': 0, 'away_draws': 0, 'away_losses': 0,
                        'home_goals_for': 0, 'home_goals_against': 0,
                        'away_goals_for': 0, 'away_goals_against': 0,
                        'recent_form': [],  # 5 นัดล่าสุด
                        'corners_for': 0, 'corners_against': 0,  # จำลองข้อมูล corner
                        'corner_1st_half': 0, 'corner_2nd_half': 0,
                        'elo_rating': 1500
                    }
            
            # อัปเดตสถิติ
            team_stats[home_team]['matches_played'] += 1
            team_stats[away_team]['matches_played'] += 1
            
            team_stats[home_team]['goals_for'] += home_goals
            team_stats[home_team]['goals_against'] += away_goals
            team_stats[home_team]['home_goals_for'] += home_goals
            team_stats[home_team]['home_goals_against'] += away_goals
            
            team_stats[away_team]['goals_for'] += away_goals
            team_stats[away_team]['goals_against'] += home_goals
            team_stats[away_team]['away_goals_for'] += away_goals
            team_stats[away_team]['away_goals_against'] += home_goals
            
            # ผลการแข่งขัน
            if home_goals > away_goals:
                team_stats[home_team]['wins'] += 1
                team_stats[home_team]['home_wins'] += 1
                team_stats[away_team]['losses'] += 1
                team_stats[away_team]['away_losses'] += 1
                
                # Form
                team_stats[home_team]['recent_form'].append('W')
                team_stats[away_team]['recent_form'].append('L')
                
            elif home_goals < away_goals:
                team_stats[away_team]['wins'] += 1
                team_stats[away_team]['away_wins'] += 1
                team_stats[home_team]['losses'] += 1
                team_stats[home_team]['home_losses'] += 1
                
                # Form
                team_stats[home_team]['recent_form'].append('L')
                team_stats[away_team]['recent_form'].append('W')
                
            else:
                team_stats[home_team]['draws'] += 1
                team_stats[home_team]['home_draws'] += 1
                team_stats[away_team]['draws'] += 1
                team_stats[away_team]['away_draws'] += 1
                
                # Form
                team_stats[home_team]['recent_form'].append('D')
                team_stats[away_team]['recent_form'].append('D')
            
            # จำลองข้อมูล Corner (ใช้สูตรจากสถิติจริง)
            total_goals = home_goals + away_goals
            estimated_corners = max(8, min(16, 10 + total_goals * 1.2 + np.random.normal(0, 2)))
            
            home_corners = int(estimated_corners * 0.6) if home_goals >= away_goals else int(estimated_corners * 0.4)
            away_corners = int(estimated_corners - home_corners)
            
            team_stats[home_team]['corners_for'] += home_corners
            team_stats[home_team]['corners_against'] += away_corners
            team_stats[away_team]['corners_for'] += away_corners
            team_stats[away_team]['corners_against'] += home_corners
            
            # Corner แยกครึ่ง (จำลอง)
            corner_1st = int(estimated_corners * 0.45)
            corner_2nd = int(estimated_corners * 0.55)
            
            team_stats[home_team]['corner_1st_half'] += corner_1st * 0.6
            team_stats[home_team]['corner_2nd_half'] += corner_2nd * 0.6
            team_stats[away_team]['corner_1st_half'] += corner_1st * 0.4
            team_stats[away_team]['corner_2nd_half'] += corner_2nd * 0.4
            
            # เก็บ Form เฉพาะ 5 นัดล่าสุด
            for team in [home_team, away_team]:
                if len(team_stats[team]['recent_form']) > 5:
                    team_stats[team]['recent_form'] = team_stats[team]['recent_form'][-5:]
        
        # คำนวณ ELO Rating
        self._calculate_elo_ratings(fixtures, team_stats)
        
        self.team_stats = team_stats
        return team_stats
    
    def _calculate_elo_ratings(self, fixtures: List[Dict], team_stats: Dict):
        """คำนวณ ELO Rating"""
        for fixture in fixtures:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_goals = fixture['goals']['home'] or 0
            away_goals = fixture['goals']['away'] or 0
            
            # ผลการแข่งขัน
            if home_goals > away_goals:
                home_result, away_result = 1.0, 0.0
            elif home_goals < away_goals:
                home_result, away_result = 0.0, 1.0
            else:
                home_result, away_result = 0.5, 0.5
            
            # คำนวณ Expected Score
            home_rating = team_stats[home_team]['elo_rating']
            away_rating = team_stats[away_team]['elo_rating']
            
            home_expected = 1 / (1 + 10**((away_rating - home_rating - 100) / 400))
            away_expected = 1 - home_expected
            
            # อัปเดต ELO
            K = 32
            team_stats[home_team]['elo_rating'] += K * (home_result - home_expected)
            team_stats[away_team]['elo_rating'] += K * (away_result - away_expected)
