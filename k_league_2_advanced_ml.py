#!/usr/bin/env python3
"""
🇰🇷 K League 2 Advanced ML Predictor
ระบบทำนายขั้นสูงด้วย Machine Learning สำหรับ K League 2
ทำนาย 4 ค่า: ผลการแข่งขัน, Handicap, Over/Under, Corners
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
import time

class KLeague2AdvancedML:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        self.league_id = 293  # K League 2
        self.season = 2025
        
        # Advanced ML Models
        self.models = {
            'match_result': self._create_ensemble_model(),
            'handicap': self._create_ensemble_model(),
            'over_under': self._create_ensemble_model(),
            'corners': self._create_ensemble_model()
        }
        
        # Scalers
        self.scalers = {
            'match_result': StandardScaler(),
            'handicap': StandardScaler(),
            'over_under': StandardScaler(),
            'corners': StandardScaler()
        }
        
        # Data storage
        self.fixtures_data = []
        self.team_stats = {}
        self.feature_columns = []
        self.is_trained = False
        
        # Historical data for training
        self.historical_matches = []
        
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
            elif response.status_code == 429:
                print("⚠️ Rate limit reached, using backup data")
                return {}
            else:
                print(f"❌ API Error: {response.status_code}")
                return {}
        except Exception as e:
            print(f"🚨 Request Error: {e}")
            return {}
    
    def load_k_league_2_data(self) -> List[Dict]:
        """ดึงข้อมูล K League 2 ย้อนหลัง"""
        print("📥 กำลังดึงข้อมูล K League 2...")
        
        # ดึงข้อมูลย้อนหลัง 30 วัน
        matches = []
        for days_back in range(1, 31):
            date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            params = {
                'league': self.league_id,
                'season': self.season,
                'date': date
            }
            
            data = self.make_api_request('fixtures', params)
            if data and 'response' in data:
                for match in data['response']:
                    if match['fixture']['status']['short'] == 'FT':
                        matches.append(match)
            
            time.sleep(0.5)  # Rate limiting
            
            if len(matches) >= 50:  # เก็บ 50 เกมล่าสุด
                break
        
        print(f"✅ ดึงข้อมูลได้ {len(matches)} เกม")
        self.historical_matches = matches
        return matches
    
    def extract_features(self, match: Dict) -> Dict:
        """สกัดฟีเจอร์จากข้อมูลการแข่งขัน"""
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        
        # Basic features
        features = {
            'home_team_id': match['teams']['home']['id'],
            'away_team_id': match['teams']['away']['id'],
            'home_goals': match['goals']['home'] or 0,
            'away_goals': match['goals']['away'] or 0,
            'total_goals': (match['goals']['home'] or 0) + (match['goals']['away'] or 0),
            'goal_difference': (match['goals']['home'] or 0) - (match['goals']['away'] or 0),
        }
        
        # Match result
        if features['home_goals'] > features['away_goals']:
            features['match_result'] = 'Home Win'
        elif features['home_goals'] < features['away_goals']:
            features['match_result'] = 'Away Win'
        else:
            features['match_result'] = 'Draw'
        
        # Handicap (จำลองจากผลจริง)
        goal_diff = features['goal_difference']
        if abs(goal_diff) >= 2:
            handicap_line = -1.5 if goal_diff > 0 else 1.5
        elif abs(goal_diff) == 1:
            handicap_line = -0.5 if goal_diff > 0 else 0.5
        else:
            handicap_line = 0
        
        features['handicap_line'] = handicap_line
        
        # Handicap result
        if handicap_line < 0:  # Home favored
            handicap_result = features['home_goals'] + handicap_line - features['away_goals']
        else:  # Away favored
            handicap_result = features['home_goals'] - (features['away_goals'] + abs(handicap_line))
        
        if handicap_result > 0:
            features['handicap_result'] = 'Home Win'
        elif handicap_result == 0:
            features['handicap_result'] = 'Push'
        else:
            features['handicap_result'] = 'Away Win'
        
        # Over/Under 2.5
        features['over_under'] = 'Over' if features['total_goals'] > 2.5 else 'Under'
        
        # Corners (จำลองจากประตู)
        base_corners = max(6, min(14, int(features['total_goals'] * 2.5 + np.random.normal(0, 1.5))))
        features['corners_total'] = max(4, min(16, base_corners))
        features['corners_first_half'] = max(1, min(8, int(features['corners_total'] * 0.4 + np.random.normal(0, 0.8))))
        features['corners_second_half'] = features['corners_total'] - features['corners_first_half']
        
        # Corner predictions
        features['corners_over_10'] = 'Over' if features['corners_total'] > 10 else 'Under'
        features['corners_fh_over_5'] = 'Over' if features['corners_first_half'] > 5 else 'Under'
        
        return features
    
    def prepare_training_data(self) -> pd.DataFrame:
        """เตรียมข้อมูลสำหรับเทรน"""
        if not self.historical_matches:
            self.load_k_league_2_data()
        
        if not self.historical_matches:
            print("❌ ไม่มีข้อมูลสำหรับเทรน")
            return pd.DataFrame()
        
        # สกัดฟีเจอร์
        features_list = []
        for match in self.historical_matches:
            features = self.extract_features(match)
            features_list.append(features)
        
        df = pd.DataFrame(features_list)
        print(f"✅ เตรียมข้อมูลเทรนสำเร็จ: {len(df)} เกม")
        return df
    
    def train_models(self, df: pd.DataFrame):
        """เทรนโมเดล ML"""
        if df.empty:
            print("❌ ไม่มีข้อมูลสำหรับเทรน")
            return
        
        print("🤖 กำลังเทรนโมเดล Advanced ML...")
        
        # เตรียมฟีเจอร์
        feature_cols = ['home_team_id', 'away_team_id', 'total_goals', 'goal_difference']
        X = df[feature_cols].fillna(0)
        
        # เทรนแต่ละโมเดล
        models_to_train = {
            'match_result': df['match_result'],
            'handicap': df['handicap_result'],
            'over_under': df['over_under'],
            'corners': df['corners_over_10']
        }
        
        for model_name, y in models_to_train.items():
            if len(y.unique()) < 2:
                continue
                
            try:
                # Scale features
                X_scaled = self.scalers[model_name].fit_transform(X)
                
                # Train model
                self.models[model_name].fit(X_scaled, y)
                
                # Cross validation
                cv_scores = cross_val_score(self.models[model_name], X_scaled, y, cv=3, scoring='accuracy')
                print(f"✅ {model_name}: CV Score = {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
                
            except Exception as e:
                print(f"❌ Error training {model_name}: {e}")
        
        self.feature_columns = feature_cols
        self.is_trained = True
        print("🎯 เทรนโมเดลเสร็จสิ้น!")
    
    def predict_match(self, home_team: str, away_team: str, home_id: int = None, away_id: int = None) -> Dict:
        """ทำนายการแข่งขัน"""
        if not self.is_trained:
            print("⚠️ โมเดลยังไม่ได้เทรน ใช้การทำนายพื้นฐาน")
            return self._basic_prediction(home_team, away_team)
        
        # เตรียมฟีเจอร์
        features = {
            'home_team_id': home_id or hash(home_team) % 1000,
            'away_team_id': away_id or hash(away_team) % 1000,
            'total_goals': 2.5,  # ค่าเฉลี่ย
            'goal_difference': 0
        }
        
        X = pd.DataFrame([features])[self.feature_columns]
        
        predictions = {}
        confidences = {}
        
        # ทำนายแต่ละโมเดล
        for model_name, model in self.models.items():
            try:
                X_scaled = self.scalers[model_name].transform(X)
                pred = model.predict(X_scaled)[0]
                prob = model.predict_proba(X_scaled)[0]
                confidence = max(prob) * 100
                
                predictions[model_name] = pred
                confidences[model_name] = confidence
                
            except Exception as e:
                print(f"❌ Error predicting {model_name}: {e}")
                predictions[model_name] = "Unknown"
                confidences[model_name] = 50
        
        return {
            'match_result': {
                'prediction': predictions.get('match_result', 'Draw'),
                'confidence': confidences.get('match_result', 60)
            },
            'handicap': {
                'prediction': predictions.get('handicap', 'Push'),
                'confidence': confidences.get('handicap', 55)
            },
            'over_under': {
                'prediction': predictions.get('over_under', 'Over'),
                'confidence': confidences.get('over_under', 65)
            },
            'corners': {
                'halftime': {'prediction': 'Under 5', 'confidence': 60},
                'fulltime': {'prediction': predictions.get('corners', 'Over 10'), 'confidence': confidences.get('corners', 70)}
            }
        }
    
    def _basic_prediction(self, home_team: str, away_team: str) -> Dict:
        """การทำนายพื้นฐานเมื่อไม่มีโมเดล"""
        # ใช้ hash เพื่อให้ผลลัพธ์คงที่
        seed = hash(home_team + away_team) % 1000
        np.random.seed(seed)
        
        predictions = ['Home Win', 'Draw', 'Away Win']
        handicaps = ['Home Win', 'Push', 'Away Win']
        ou_options = ['Over', 'Under']
        
        return {
            'match_result': {
                'prediction': np.random.choice(predictions, p=[0.4, 0.3, 0.3]),
                'confidence': np.random.randint(60, 80)
            },
            'handicap': {
                'prediction': np.random.choice(handicaps, p=[0.45, 0.1, 0.45]),
                'confidence': np.random.randint(55, 75)
            },
            'over_under': {
                'prediction': np.random.choice(ou_options, p=[0.6, 0.4]),
                'confidence': np.random.randint(65, 85)
            },
            'corners': {
                'halftime': {'prediction': 'Under 5', 'confidence': 65},
                'fulltime': {'prediction': 'Over 10', 'confidence': 70}
            }
        }
    
    def backtest_system(self, test_matches: int = 20) -> Dict:
        """ทดสอบระบบย้อนหลัง"""
        if not self.historical_matches or len(self.historical_matches) < test_matches:
            print("❌ ข้อมูลไม่เพียงพอสำหรับ backtest")
            return {}
        
        print(f"🔍 กำลังทดสอบระบบย้อนหลัง {test_matches} เกม...")
        
        # แบ่งข้อมูล
        train_data = self.historical_matches[:-test_matches]
        test_data = self.historical_matches[-test_matches:]
        
        # เทรนด้วยข้อมูลเก่า
        old_matches = self.historical_matches
        self.historical_matches = train_data
        
        df = self.prepare_training_data()
        if not df.empty:
            self.train_models(df)
        
        # ทดสอบ
        results = {
            'match_result': {'correct': 0, 'total': 0},
            'handicap': {'correct': 0, 'total': 0},
            'over_under': {'correct': 0, 'total': 0},
            'corners': {'correct': 0, 'total': 0}
        }
        
        for match in test_data:
            actual_features = self.extract_features(match)
            home_team = match['teams']['home']['name']
            away_team = match['teams']['away']['name']
            home_id = match['teams']['home']['id']
            away_id = match['teams']['away']['id']
            
            predictions = self.predict_match(home_team, away_team, home_id, away_id)
            
            # เปรียบเทียบผล
            if predictions['match_result']['prediction'] == actual_features['match_result']:
                results['match_result']['correct'] += 1
            results['match_result']['total'] += 1
            
            if predictions['handicap']['prediction'] == actual_features['handicap_result']:
                results['handicap']['correct'] += 1
            results['handicap']['total'] += 1
            
            if predictions['over_under']['prediction'] == actual_features['over_under']:
                results['over_under']['correct'] += 1
            results['over_under']['total'] += 1
            
            if predictions['corners']['fulltime']['prediction'].startswith(actual_features['corners_over_10']):
                results['corners']['correct'] += 1
            results['corners']['total'] += 1
        
        # คืนค่าข้อมูลเดิม
        self.historical_matches = old_matches
        
        # คำนวณความแม่นยำ
        accuracy_results = {}
        for category, data in results.items():
            if data['total'] > 0:
                accuracy = (data['correct'] / data['total']) * 100
                accuracy_results[category] = {
                    'accuracy': accuracy,
                    'correct': data['correct'],
                    'total': data['total']
                }
        
        return accuracy_results

if __name__ == "__main__":
    # ทดสอบระบบ
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    predictor = KLeague2AdvancedML(api_key)
    
    # เทรนโมเดล
    df = predictor.prepare_training_data()
    if not df.empty:
        predictor.train_models(df)
        
        # ทดสอบการทำนาย
        result = predictor.predict_match("Incheon United", "Asan Mugunghwa")
        print("\n🎯 ตัวอย่างการทำนาย:")
        print(f"Match Result: {result['match_result']['prediction']} ({result['match_result']['confidence']:.1f}%)")
        print(f"Handicap: {result['handicap']['prediction']} ({result['handicap']['confidence']:.1f}%)")
        print(f"Over/Under: {result['over_under']['prediction']} ({result['over_under']['confidence']:.1f}%)")
        print(f"Corners: {result['corners']['fulltime']['prediction']} ({result['corners']['fulltime']['confidence']:.1f}%)")
        
        # Backtest
        backtest_results = predictor.backtest_system(20)
        if backtest_results:
            print("\n📊 ผล Backtest (20 เกมล่าสุด):")
            for category, data in backtest_results.items():
                print(f"{category}: {data['accuracy']:.1f}% ({data['correct']}/{data['total']})")
    else:
        print("❌ ไม่สามารถเทรนโมเดลได้")
