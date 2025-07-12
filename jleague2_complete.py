#!/usr/bin/env python3
"""
🚀 J-League 2 Advanced ML Predictor - Final Version
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
            ('rf', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)),
            ('gb', GradientBoostingClassifier(n_estimators=50, learning_rate=0.1, max_depth=6, random_state=42)),
            ('et', ExtraTreesClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)),
            ('lr', LogisticRegression(C=1.0, max_iter=1000, random_state=42))
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
                        'corners_for': 0, 'corners_against': 0,
                        'corner_1st_half': 0, 'corner_2nd_half': 0,
                        'elo_rating': 1500
                    }
            
            # อัปเดตสถิติ
            team_stats[home_team]['matches_played'] += 1
            team_stats[away_team]['matches_played'] += 1
            
            team_stats[home_team]['goals_for'] += home_goals
            team_stats[home_team]['goals_against'] += away_goals
            team_stats[away_team]['goals_for'] += away_goals
            team_stats[away_team]['goals_against'] += home_goals
            
            # ผลการแข่งขัน
            if home_goals > away_goals:
                team_stats[home_team]['wins'] += 1
                team_stats[away_team]['losses'] += 1
                team_stats[home_team]['recent_form'].append('W')
                team_stats[away_team]['recent_form'].append('L')
            elif home_goals < away_goals:
                team_stats[away_team]['wins'] += 1
                team_stats[home_team]['losses'] += 1
                team_stats[home_team]['recent_form'].append('L')
                team_stats[away_team]['recent_form'].append('W')
            else:
                team_stats[home_team]['draws'] += 1
                team_stats[away_team]['draws'] += 1
                team_stats[home_team]['recent_form'].append('D')
                team_stats[away_team]['recent_form'].append('D')
            
            # จำลองข้อมูล Corner
            total_goals = home_goals + away_goals
            estimated_corners = max(8, min(16, 10 + total_goals * 1.2 + np.random.normal(0, 2)))
            
            home_corners = int(estimated_corners * 0.6) if home_goals >= away_goals else int(estimated_corners * 0.4)
            away_corners = int(estimated_corners - home_corners)
            
            team_stats[home_team]['corners_for'] += home_corners
            team_stats[home_team]['corners_against'] += away_corners
            team_stats[away_team]['corners_for'] += away_corners
            team_stats[away_team]['corners_against'] += home_corners
            
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
    def create_advanced_features(self, home_team: str, away_team: str) -> np.ndarray:
        """สร้าง Features ขั้นสูงสำหรับการทำนาย"""
        if home_team not in self.team_stats or away_team not in self.team_stats:
            return np.array([0.5] * 20)  # ลดจำนวน features
        
        home_stats = self.team_stats[home_team]
        away_stats = self.team_stats[away_team]
        
        features = []
        
        # 1. ELO Rating Features
        features.extend([
            home_stats['elo_rating'] / 2000,
            away_stats['elo_rating'] / 2000,
            (home_stats['elo_rating'] - away_stats['elo_rating']) / 400
        ])
        
        # 2. Goal Statistics
        home_matches = max(1, home_stats['matches_played'])
        away_matches = max(1, away_stats['matches_played'])
        
        features.extend([
            home_stats['goals_for'] / home_matches,
            home_stats['goals_against'] / home_matches,
            away_stats['goals_for'] / away_matches,
            away_stats['goals_against'] / away_matches,
            (home_stats['goals_for'] - home_stats['goals_against']) / home_matches,
            (away_stats['goals_for'] - away_stats['goals_against']) / away_matches
        ])
        
        # 3. Win/Draw/Loss Ratios
        features.extend([
            home_stats['wins'] / home_matches,
            home_stats['draws'] / home_matches,
            away_stats['wins'] / away_matches,
            away_stats['draws'] / away_matches
        ])
        
        # 4. Recent Form
        home_form_points = sum([3 if x=='W' else 1 if x=='D' else 0 for x in home_stats['recent_form'][-5:]])
        away_form_points = sum([3 if x=='W' else 1 if x=='D' else 0 for x in away_stats['recent_form'][-5:]])
        
        features.extend([
            home_form_points / 15,
            away_form_points / 15
        ])
        
        # 5. Corner Statistics
        features.extend([
            home_stats['corners_for'] / home_matches,
            home_stats['corners_against'] / home_matches,
            away_stats['corners_for'] / away_matches,
            away_stats['corners_against'] / away_matches
        ])
        
        return np.array(features)
    
    def prepare_training_data(self, fixtures: List[Dict]) -> Tuple[np.ndarray, Dict]:
        """เตรียมข้อมูลสำหรับการเทรน"""
        print("🔧 กำลังเตรียมข้อมูลสำหรับการเทรน...")
        
        X = []
        y = {
            'match_result': [],
            'handicap': [],
            'over_under': [],
            'corner_1st_half': [],
            'corner_2nd_half': []
        }
        
        # เรียงตามวันที่
        sorted_fixtures = sorted(fixtures, key=lambda x: x['fixture']['date'])
        
        # ใช้ข้อมูลทั้งหมดในการคำนวณสถิติ
        self.calculate_team_statistics(sorted_fixtures)
        
        for fixture in sorted_fixtures:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_goals = fixture['goals']['home'] or 0
            away_goals = fixture['goals']['away'] or 0
            
            # สร้าง features
            features = self.create_advanced_features(home_team, away_team)
            X.append(features)
            
            # Labels
            # 1. Match Result
            if home_goals > away_goals:
                y['match_result'].append(2)  # Home Win
            elif home_goals < away_goals:
                y['match_result'].append(0)  # Away Win
            else:
                y['match_result'].append(1)  # Draw
            
            # 2. Handicap
            y['handicap'].append(y['match_result'][-1])
            
            # 3. Over/Under 2.5
            total_goals = home_goals + away_goals
            y['over_under'].append(1 if total_goals > 2.5 else 0)
            
            # 4. Corner 1st Half (จำลอง)
            estimated_corners_1st = max(2, min(8, 3 + total_goals * 0.8 + np.random.normal(0, 1)))
            y['corner_1st_half'].append(1 if estimated_corners_1st > 5 else 0)
            
            # 5. Corner 2nd Half (จำลอง)
            estimated_corners_2nd = max(2, min(10, 4 + total_goals * 1.0 + np.random.normal(0, 1)))
            y['corner_2nd_half'].append(1 if estimated_corners_2nd > 5 else 0)
        
        return np.array(X), y
    
    def train_models(self, fixtures: List[Dict]):
        """เทรนโมเดล ML ทั้งหมด"""
        print("🤖 กำลังเทรนโมเดล Advanced ML...")
        
        # เตรียมข้อมูลเทรน
        X, y = self.prepare_training_data(fixtures)
        
        if len(X) == 0:
            print("❌ ไม่มีข้อมูลสำหรับการเทรน")
            return
        
        print(f"📊 ข้อมูลเทรน: {len(X)} samples, {len(X[0])} features")
        
        # เทรนแต่ละโมเดล
        for target_name, target_values in y.items():
            print(f"🔧 กำลังเทรนโมเดล {target_name}...")
            
            try:
                # Scale features
                X_scaled = self.scalers[target_name].fit_transform(X)
                
                # เทรนโมเดล
                self.models[target_name].fit(X_scaled, target_values)
                
                # Cross-validation score
                cv_scores = cross_val_score(
                    self.models[target_name], X_scaled, target_values, 
                    cv=3, scoring='accuracy'
                )
                
                print(f"   ✅ {target_name}: CV Score = {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
            except Exception as e:
                print(f"   ❌ {target_name}: Error = {e}")
        
        self.is_trained = True
        print("🎉 การเทรนเสร็จสิ้น!")
    
    def predict_match(self, home_team: str, away_team: str) -> Dict:
        """ทำนายการแข่งขัน 5 ค่า"""
        if not self.is_trained:
            print("❌ โมเดลยังไม่ได้เทรน")
            return {}
        
        # สร้าง features
        features = self.create_advanced_features(home_team, away_team).reshape(1, -1)
        
        predictions = {}
        
        for target_name, model in self.models.items():
            try:
                # Scale features
                features_scaled = self.scalers[target_name].transform(features)
                
                # ทำนาย
                pred_class = model.predict(features_scaled)[0]
                pred_proba = model.predict_proba(features_scaled)[0]
                
                predictions[target_name] = {
                    'prediction': pred_class,
                    'probabilities': pred_proba,
                    'confidence': max(pred_proba)
                }
            except Exception as e:
                print(f"❌ Error predicting {target_name}: {e}")
                predictions[target_name] = {
                    'prediction': 1,
                    'probabilities': [0.33, 0.34, 0.33],
                    'confidence': 0.34
                }
        
        # แปลงผลลัพธ์
        result = {
            'home_team': home_team,
            'away_team': away_team,
            'match_result': self._interpret_match_result(predictions['match_result']),
            'handicap': self._interpret_handicap(predictions['handicap']),
            'over_under': self._interpret_over_under(predictions['over_under']),
            'corner_1st_half': self._interpret_corner(predictions['corner_1st_half'], '1st Half'),
            'corner_2nd_half': self._interpret_corner(predictions['corner_2nd_half'], '2nd Half'),
            'confidence_scores': {
                'match_result': predictions['match_result']['confidence'],
                'handicap': predictions['handicap']['confidence'],
                'over_under': predictions['over_under']['confidence'],
                'corner_1st_half': predictions['corner_1st_half']['confidence'],
                'corner_2nd_half': predictions['corner_2nd_half']['confidence']
            }
        }
        
        return result
    
    def _interpret_match_result(self, pred_data: Dict) -> Dict:
        """แปลผลการทำนายผลการแข่งขัน"""
        class_names = ['Away Win', 'Draw', 'Home Win']
        pred_class = pred_data['prediction']
        probabilities = pred_data['probabilities']
        
        return {
            'prediction': class_names[pred_class],
            'home_win_prob': probabilities[2] if len(probabilities) > 2 else 0.33,
            'draw_prob': probabilities[1] if len(probabilities) > 1 else 0.34,
            'away_win_prob': probabilities[0] if len(probabilities) > 0 else 0.33,
            'confidence': pred_data['confidence']
        }
    
    def _interpret_handicap(self, pred_data: Dict) -> Dict:
        """แปลผลการทำนาย Handicap"""
        class_names = ['Away Win', 'Draw', 'Home Win']
        pred_class = pred_data['prediction']
        
        return {
            'prediction': class_names[pred_class],
            'confidence': pred_data['confidence']
        }
    
    def _interpret_over_under(self, pred_data: Dict) -> Dict:
        """แปลผลการทำนาย Over/Under"""
        pred_class = pred_data['prediction']
        probabilities = pred_data['probabilities']
        
        return {
            'prediction': 'Over 2.5' if pred_class == 1 else 'Under 2.5',
            'over_prob': probabilities[1] if len(probabilities) > 1 else 0.5,
            'under_prob': probabilities[0] if len(probabilities) > 1 else 0.5,
            'confidence': pred_data['confidence']
        }
    
    def _interpret_corner(self, pred_data: Dict, half: str) -> Dict:
        """แปลผลการทำนาย Corner"""
        pred_class = pred_data['prediction']
        probabilities = pred_data['probabilities']
        
        return {
            'prediction': f'Over 5 ({half})' if pred_class == 1 else f'Under 5 ({half})',
            'over_prob': probabilities[1] if len(probabilities) > 1 else 0.5,
            'under_prob': probabilities[0] if len(probabilities) > 1 else 0.5,
            'confidence': pred_data['confidence']
        }
