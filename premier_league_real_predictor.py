#!/usr/bin/env python3
"""
🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League Real Data Predictor
ระบบทำนาย Premier League ด้วยข้อมูลจริง 380 เกม
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import RobustScaler
from sklearn.impute import KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

class PremierLeagueRealPredictor:
    def __init__(self):
        # ML Models (เดียวกับ Ultra Advanced)
        self.models = {
            'rf': RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1),
            'gb': GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, max_depth=6, random_state=42),
            'et': ExtraTreesClassifier(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1),
            'lr': LogisticRegression(C=1.0, max_iter=1000, random_state=42),
            'svm': SVC(C=1.0, kernel='rbf', probability=True, random_state=42)
        }
        
        # Preprocessing
        self.scaler = RobustScaler()
        self.imputer = KNNImputer(n_neighbors=5)
        self.feature_selector = SelectKBest(f_classif, k=30)
        
        # Storage
        self.trained_models = {}
        self.ensemble_weights = {}
        self.team_ratings = {}
        
        self.is_trained = False
        self.feature_columns = []
        self.selected_feature_names = []
        self.historical_data = None
        
    def load_real_premier_league_data(self):
        """โหลดข้อมูล Premier League จริง"""
        print("🏴󠁧󠁢󠁥󠁮󠁧󠁿 กำลังโหลดข้อมูล Premier League จริง...")
        
        try:
            data = pd.read_csv('premier_league_real_data.csv')
            data['date'] = pd.to_datetime(data['date'])
            data = data.sort_values('date').reset_index(drop=True)
            
            print(f"✅ โหลดข้อมูล Premier League จริงสำเร็จ: {len(data)} เกม")
            print(f"📅 ช่วงเวลา: {data['date'].min().strftime('%Y-%m-%d')} ถึง {data['date'].max().strftime('%Y-%m-%d')}")
            
            # แสดงทีม
            teams = sorted(set(data['home_team'].unique()) | set(data['away_team'].unique()))
            print(f"🏆 ทีมใน Premier League: {len(teams)} ทีม")
            
            self.historical_data = data
            return data
            
        except FileNotFoundError:
            print("❌ ไม่พบไฟล์ premier_league_real_data.csv")
            print("💡 รัน test_real_api_data.py ก่อน")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def calculate_elo_ratings(self, matches_df):
        """คำนวณ ELO Rating"""
        print("🏆 กำลังคำนวณ ELO Ratings...")
        
        teams = set(matches_df['home_team'].unique()) | set(matches_df['away_team'].unique())
        elo_ratings = {team: 1500 for team in teams}
        
        K = 32
        
        for _, match in matches_df.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            home_goals = match['home_goals']
            away_goals = match['away_goals']
            
            if home_goals > away_goals:
                home_result, away_result = 1.0, 0.0
            elif home_goals == away_goals:
                home_result, away_result = 0.5, 0.5
            else:
                home_result, away_result = 0.0, 1.0
            
            home_expected = 1 / (1 + 10**((elo_ratings[away_team] - elo_ratings[home_team]) / 400))
            away_expected = 1 - home_expected
            
            elo_ratings[home_team] += K * (home_result - home_expected)
            elo_ratings[away_team] += K * (away_result - away_expected)
        
        self.team_ratings = elo_ratings
        return elo_ratings
    
    def create_ultra_features(self, matches_df):
        """สร้าง Ultra Advanced Features"""
        print("🔧 กำลังสร้าง Ultra Advanced Features...")
        
        features = []
        
        for idx, match in matches_df.iterrows():
            if idx < 20:  # ต้องมีข้อมูลพอ
                continue
                
            home_team = match['home_team']
            away_team = match['away_team']
            match_date = pd.to_datetime(match['date'])
            
            # ข้อมูลก่อนหน้า
            prev_matches = matches_df[matches_df['date'] < match_date]
            
            feature_dict = {}
            
            # 1. ELO Ratings
            feature_dict['home_elo'] = self.team_ratings.get(home_team, 1500)
            feature_dict['away_elo'] = self.team_ratings.get(away_team, 1500)
            feature_dict['elo_diff'] = feature_dict['home_elo'] - feature_dict['away_elo']
            
            # 2. Recent Form (5 เกมล่าสุด)
            home_recent = self._get_recent_form(prev_matches, home_team, 5)
            away_recent = self._get_recent_form(prev_matches, away_team, 5)
            
            feature_dict['home_recent_points'] = home_recent['points']
            feature_dict['away_recent_points'] = away_recent['points']
            feature_dict['home_recent_goals_for'] = home_recent['goals_for']
            feature_dict['away_recent_goals_for'] = away_recent['goals_for']
            feature_dict['home_recent_goals_against'] = home_recent['goals_against']
            feature_dict['away_recent_goals_against'] = away_recent['goals_against']
            
            # 3. Season Form
            home_season = self._get_season_form(prev_matches, home_team)
            away_season = self._get_season_form(prev_matches, away_team)
            
            feature_dict['home_season_ppg'] = home_season['ppg']
            feature_dict['away_season_ppg'] = away_season['ppg']
            feature_dict['home_goals_per_game'] = home_season['goals_for'] / max(1, home_season['games'])
            feature_dict['away_goals_per_game'] = away_season['goals_for'] / max(1, away_season['games'])
            
            # 4. Head to Head
            h2h = self._get_head_to_head(prev_matches, home_team, away_team)
            feature_dict['h2h_home_wins'] = h2h['home_wins']
            feature_dict['h2h_away_wins'] = h2h['away_wins']
            feature_dict['h2h_draws'] = h2h['draws']
            
            # 5. Home/Away Performance
            home_home_form = self._get_home_away_form(prev_matches, home_team, 'home')
            away_away_form = self._get_home_away_form(prev_matches, away_team, 'away')
            
            feature_dict['home_home_ppg'] = home_home_form['ppg']
            feature_dict['away_away_ppg'] = away_away_form['ppg']
            
            # 6. Momentum
            feature_dict['home_momentum'] = self._calculate_momentum(prev_matches, home_team)
            feature_dict['away_momentum'] = self._calculate_momentum(prev_matches, away_team)
            
            # 7. Goals Statistics
            feature_dict['home_avg_goals_scored'] = home_season['goals_for'] / max(1, home_season['games'])
            feature_dict['away_avg_goals_scored'] = away_season['goals_for'] / max(1, away_season['games'])
            feature_dict['home_avg_goals_conceded'] = home_season['goals_against'] / max(1, home_season['games'])
            feature_dict['away_avg_goals_conceded'] = away_season['goals_against'] / max(1, away_season['games'])
            
            # 8. Strength
            feature_dict['home_attack_strength'] = feature_dict['home_avg_goals_scored'] / 1.5
            feature_dict['away_attack_strength'] = feature_dict['away_avg_goals_scored'] / 1.5
            feature_dict['home_defense_strength'] = 1.5 / max(0.1, feature_dict['home_avg_goals_conceded'])
            feature_dict['away_defense_strength'] = 1.5 / max(0.1, feature_dict['away_avg_goals_conceded'])
            
            # 9. Match Context
            feature_dict['days_since_last_match_home'] = self._days_since_last_match(prev_matches, home_team, match_date)
            feature_dict['days_since_last_match_away'] = self._days_since_last_match(prev_matches, away_team, match_date)
            
            # 10. League Position
            feature_dict['home_league_position'] = self._get_league_position(prev_matches, home_team)
            feature_dict['away_league_position'] = self._get_league_position(prev_matches, away_team)
            
            # Target
            if match['home_goals'] > match['away_goals']:
                target = 'Home Win'
            elif match['home_goals'] == match['away_goals']:
                target = 'Draw'
            else:
                target = 'Away Win'
            
            feature_dict['target'] = target
            features.append(feature_dict)
        
        features_df = pd.DataFrame(features)
        print(f"✅ สร้าง {len(features_df.columns)-1} Ultra Features สำเร็จ")
        
        return features_df
    
    def train_ensemble_models(self, data):
        """เทรนโมเดล Ensemble"""
        print("🤖 กำลังเทรนโมเดล Premier League Ultra Advanced Ensemble...")
        
        # คำนวณ ELO ratings
        self.calculate_elo_ratings(data)
        
        # สร้าง features
        features_df = self.create_ultra_features(data)
        
        if len(features_df) < 50:
            print("❌ ข้อมูลไม่เพียงพอสำหรับการเทรน")
            return False
        
        # แยก features และ target
        X = features_df.drop('target', axis=1)
        y = features_df['target']
        
        # Preprocessing
        X_processed = self.imputer.fit_transform(X)
        X_processed = self.scaler.fit_transform(X_processed)
        
        # Feature selection
        X_selected = self.feature_selector.fit_transform(X_processed, y)
        
        self.feature_columns = X.columns.tolist()
        selected_indices = self.feature_selector.get_support(indices=True)
        self.selected_feature_names = [self.feature_columns[i] for i in selected_indices]
        
        print(f"📊 Selected {len(self.selected_feature_names)} best features")
        
        # Split data
        split_idx = int(len(X_selected) * 0.8)
        X_train, X_test = X_selected[:split_idx], X_selected[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        print(f"📊 Training data: {X_train.shape}")
        
        # Train models
        model_scores = {}
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        for name, model in self.models.items():
            print(f"   เทรน {name}...")
            
            # Cross validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')
            
            # Train on full training set
            model.fit(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            model_scores[name] = test_score
            self.trained_models[name] = model
            
            print(f"   {name}: CV={cv_scores.mean():.3f}±{cv_scores.std():.3f}, Test={test_score:.3f}")
        
        # Calculate ensemble weights
        total_score = sum(model_scores.values())
        if total_score > 0:
            raw_weights = {name: score/total_score for name, score in model_scores.items()}
            # Apply softmax for better distribution
            exp_weights = {name: np.exp(weight*5) for name, weight in raw_weights.items()}
            total_exp = sum(exp_weights.values())
            self.ensemble_weights = {name: weight/total_exp for name, weight in exp_weights.items()}
        else:
            self.ensemble_weights = {name: 1/len(self.models) for name in self.models.keys()}
        
        print(f"🎯 Ensemble weights: {self.ensemble_weights}")
        
        # Ensemble performance
        ensemble_pred = self._ensemble_predict(X_test)
        ensemble_accuracy = np.mean(ensemble_pred == y_test)
        
        print(f"\n📊 ผลการเทรน:")
        for name, score in model_scores.items():
            print(f"   {name:<15}: {score:.3f}")
        print(f"   {'Ensemble':<15}: {ensemble_accuracy:.3f}")
        
        # Classification report
        print(f"\n📈 Classification Report (Ensemble):")
        print(classification_report(y_test, ensemble_pred))
        
        self.is_trained = True
        return True
    
    def predict_match_premier_league(self, home_team, away_team):
        """ทำนายการแข่งขัน Premier League"""
        if not self.is_trained:
            print("❌ โมเดลยังไม่ได้เทรน!")
            return None
        
        print(f"🔧 กำลังสร้าง Features สำหรับ {home_team} vs {away_team}...")
        
        # สร้าง features สำหรับการทำนาย
        feature_dict = self._create_prediction_features(home_team, away_team)
        
        if not feature_dict:
            return {'prediction': 'Draw', 'confidence': 0.33, 'probabilities': {'Home Win': 0.33, 'Draw': 0.34, 'Away Win': 0.33}}
        
        # แปลงเป็น DataFrame
        X_pred = pd.DataFrame([feature_dict])
        
        # Preprocessing
        X_processed = self.imputer.transform(X_pred)
        X_processed = self.scaler.transform(X_processed)
        X_selected = self.feature_selector.transform(X_processed)
        
        # Ensemble prediction
        probabilities = self._ensemble_predict_proba(X_selected[0])
        
        # Find prediction
        classes = ['Away Win', 'Draw', 'Home Win']
        max_prob_idx = np.argmax(probabilities)
        prediction = classes[max_prob_idx]
        confidence = probabilities[max_prob_idx]
        
        prob_dict = {
            'Home Win': probabilities[2],
            'Draw': probabilities[1], 
            'Away Win': probabilities[0]
        }
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'probabilities': prob_dict
        }
