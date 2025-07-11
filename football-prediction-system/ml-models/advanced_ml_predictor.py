#!/usr/bin/env python3
"""
🚀 Advanced ML Football Predictor
ใช้ Advanced ML Models + ข้อมูลจริง + Handicap + Over/Under + Corners
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import RobustScaler, StandardScaler
from sklearn.impute import KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.model_selection import cross_val_score, StratifiedKFold, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
import warnings
warnings.filterwarnings('ignore')

class AdvancedMLPredictor:
    def __init__(self, league_name):
        self.league_name = league_name
        
        # Advanced ML Models
        self.models = {
            # Traditional Models
            'rf': RandomForestClassifier(n_estimators=300, max_depth=15, random_state=42, n_jobs=-1),
            'gb': GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=8, random_state=42),
            'et': ExtraTreesClassifier(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1),
            'ada': AdaBoostClassifier(n_estimators=100, learning_rate=1.0, random_state=42),
            
            # Neural Networks
            'mlp': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42),
            
            # Support Vector Machine
            'svm': SVC(C=1.0, kernel='rbf', probability=True, random_state=42),
            
            # Naive Bayes
            'nb': GaussianNB(),
            
            # Logistic Regression
            'lr': LogisticRegression(C=1.0, max_iter=1000, random_state=42)
        }
        
        # Preprocessing
        self.scaler = RobustScaler()
        self.imputer = KNNImputer(n_neighbors=5)
        self.feature_selector = SelectKBest(f_classif, k=35)  # เพิ่มจาก 30 เป็น 35
        
        # Storage
        self.trained_models = {}
        self.ensemble_weights = {}
        self.team_ratings = {}
        
        self.is_trained = False
        self.feature_columns = []
        self.selected_feature_names = []
        self.historical_data = None
        
        # Separate models for different predictions
        self.handicap_models = {}
        self.ou_models = {}
        self.corners_models = {}
        
    def load_real_data(self):
        """โหลดข้อมูลจริง"""
        try:
            if self.league_name.lower() == 'premier league':
                data = pd.read_csv('premier_league_real_data.csv')
            elif self.league_name.lower() == 'la liga':
                data = pd.read_csv('laliga_real_data.csv')
            else:
                print(f"❌ ไม่รองรับลีก {self.league_name}")
                return None
            
            data['date'] = pd.to_datetime(data['date'])
            data = data.sort_values('date').reset_index(drop=True)
            
            # เพิ่มข้อมูล Handicap, Over/Under, Corners
            data = self._add_betting_data(data)
            
            print(f"✅ โหลดข้อมูล {self.league_name} สำเร็จ: {len(data)} เกม")
            
            self.historical_data = data
            return data
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def _add_betting_data(self, df):
        """เพิ่มข้อมูล Handicap, Over/Under, Corners"""
        print("🔧 กำลังเพิ่มข้อมูล Handicap, Over/Under และ Corners...")
        
        betting_data = []
        
        for _, match in df.iterrows():
            home_goals = match['home_goals']
            away_goals = match['away_goals']
            total_goals = home_goals + away_goals
            goal_diff = home_goals - away_goals
            
            # คำนวณ Handicap (จำลองจากผลจริง)
            if abs(goal_diff) >= 3:
                handicap_line = -2.0 if goal_diff > 0 else 2.0
            elif abs(goal_diff) == 2:
                handicap_line = -1.5 if goal_diff > 0 else 1.5
            elif abs(goal_diff) == 1:
                handicap_line = -0.5 if goal_diff > 0 else 0.5
            else:
                handicap_line = 0
            
            # ผล Handicap
            if handicap_line < 0:  # Home favored
                handicap_result = home_goals + handicap_line - away_goals
            else:  # Away favored
                handicap_result = home_goals - (away_goals + abs(handicap_line))
            
            if handicap_result > 0:
                handicap_outcome = "Home Win"
            elif handicap_result == 0:
                handicap_outcome = "Push"
            else:
                handicap_outcome = "Away Win"
            
            # Over/Under 2.5
            ou_outcome = "Over" if total_goals > 2.5 else "Under"
            
            # จำลองเตะมุม (ใกล้เคียงความจริง)
            base_corners = max(6, min(14, int(total_goals * 2.2 + np.random.normal(0, 1.5))))
            corners_total = max(4, min(16, base_corners))
            corners_first_half = max(1, min(8, int(corners_total * 0.45 + np.random.normal(0, 0.8))))
            corners_second_half = corners_total - corners_first_half
            
            # ผลเตะมุม
            corners_ou_10 = "Over" if corners_total > 10 else "Under"
            corners_fh_5 = "Over" if corners_first_half > 5 else "Under"
            
            betting_data.append({
                'handicap_line': handicap_line,
                'handicap_result': handicap_outcome,
                'total_goals': total_goals,
                'ou_result': ou_outcome,
                'corners_total': corners_total,
                'corners_first_half': corners_first_half,
                'corners_second_half': corners_second_half,
                'corners_ou_10': corners_ou_10,
                'corners_fh_5': corners_fh_5
            })
        
        # เพิ่มข้อมูลเข้า DataFrame
        betting_df = pd.DataFrame(betting_data)
        result_df = pd.concat([df, betting_df], axis=1)
        
        print(f"✅ เพิ่มข้อมูลการเดิมพันสำเร็จ")
        return result_df
    
    def calculate_elo_ratings(self, matches_df):
        """คำนวณ ELO Rating แบบ Advanced"""
        print("🏆 กำลังคำนวณ Advanced ELO Ratings...")
        
        teams = set(matches_df['home_team'].unique()) | set(matches_df['away_team'].unique())
        elo_ratings = {team: 1500 for team in teams}
        
        # Dynamic K-factor
        for _, match in matches_df.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            home_goals = match['home_goals']
            away_goals = match['away_goals']
            
            # Goal difference affects K-factor
            goal_diff = abs(home_goals - away_goals)
            K = 32 + (goal_diff * 4)  # Bigger wins = bigger rating changes
            
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
    
    def create_advanced_features(self, matches_df):
        """สร้าง Advanced Features"""
        print("🔧 กำลังสร้าง Advanced Features...")
        
        features = []
        
        for idx, match in matches_df.iterrows():
            if idx < 30:  # ต้องมีข้อมูลพอ
                continue
                
            home_team = match['home_team']
            away_team = match['away_team']
            match_date = pd.to_datetime(match['date'])
            
            # ข้อมูลก่อนหน้า
            prev_matches = matches_df[matches_df['date'] < match_date]
            
            feature_dict = {}
            
            # 1. ELO Ratings (Advanced)
            feature_dict['home_elo'] = self.team_ratings.get(home_team, 1500)
            feature_dict['away_elo'] = self.team_ratings.get(away_team, 1500)
            feature_dict['elo_diff'] = feature_dict['home_elo'] - feature_dict['away_elo']
            feature_dict['elo_ratio'] = feature_dict['home_elo'] / max(1, feature_dict['away_elo'])
            
            # 2. Recent Form (Multiple periods)
            for period in [3, 5, 10]:
                home_recent = self._get_recent_form(prev_matches, home_team, period)
                away_recent = self._get_recent_form(prev_matches, away_team, period)
                
                feature_dict[f'home_recent_{period}_points'] = home_recent['points']
                feature_dict[f'away_recent_{period}_points'] = away_recent['points']
                feature_dict[f'home_recent_{period}_goals_for'] = home_recent['goals_for']
                feature_dict[f'away_recent_{period}_goals_for'] = away_recent['goals_for']
                feature_dict[f'home_recent_{period}_goals_against'] = home_recent['goals_against']
                feature_dict[f'away_recent_{period}_goals_against'] = away_recent['goals_against']
            
            # 3. Season Form
            home_season = self._get_season_form(prev_matches, home_team)
            away_season = self._get_season_form(prev_matches, away_team)
            
            feature_dict['home_season_ppg'] = home_season['ppg']
            feature_dict['away_season_ppg'] = away_season['ppg']
            feature_dict['home_goals_per_game'] = home_season['goals_for'] / max(1, home_season['games'])
            feature_dict['away_goals_per_game'] = away_season['goals_for'] / max(1, away_season['games'])
            feature_dict['home_goals_against_per_game'] = home_season['goals_against'] / max(1, home_season['games'])
            feature_dict['away_goals_against_per_game'] = away_season['goals_against'] / max(1, away_season['games'])
            
            # 4. Advanced Statistics
            feature_dict['home_goal_difference'] = home_season['goals_for'] - home_season['goals_against']
            feature_dict['away_goal_difference'] = away_season['goals_for'] - away_season['goals_against']
            feature_dict['home_clean_sheets'] = self._get_clean_sheets(prev_matches, home_team, 'home')
            feature_dict['away_clean_sheets'] = self._get_clean_sheets(prev_matches, away_team, 'away')
            
            # 5. Head to Head (Extended)
            h2h = self._get_head_to_head_extended(prev_matches, home_team, away_team)
            feature_dict['h2h_home_wins'] = h2h['home_wins']
            feature_dict['h2h_away_wins'] = h2h['away_wins']
            feature_dict['h2h_draws'] = h2h['draws']
            feature_dict['h2h_avg_goals'] = h2h['avg_goals']
            
            # 6. Momentum & Trends
            feature_dict['home_momentum'] = self._calculate_advanced_momentum(prev_matches, home_team)
            feature_dict['away_momentum'] = self._calculate_advanced_momentum(prev_matches, away_team)
            feature_dict['home_trend'] = self._calculate_trend(prev_matches, home_team)
            feature_dict['away_trend'] = self._calculate_trend(prev_matches, away_team)
            
            # 7. Match Context
            feature_dict['days_since_last_match_home'] = self._days_since_last_match(prev_matches, home_team, match_date)
            feature_dict['days_since_last_match_away'] = self._days_since_last_match(prev_matches, away_team, match_date)
            feature_dict['home_league_position'] = self._get_league_position(prev_matches, home_team)
            feature_dict['away_league_position'] = self._get_league_position(prev_matches, away_team)
            
            # Targets
            if match['home_goals'] > match['away_goals']:
                match_result = 'Home Win'
            elif match['home_goals'] == match['away_goals']:
                match_result = 'Draw'
            else:
                match_result = 'Away Win'
            
            feature_dict['match_result'] = match_result
            feature_dict['handicap_result'] = match['handicap_result']
            feature_dict['ou_result'] = match['ou_result']
            feature_dict['corners_ou_10'] = match['corners_ou_10']
            feature_dict['corners_fh_5'] = match['corners_fh_5']
            
            features.append(feature_dict)
        
        features_df = pd.DataFrame(features)
        print(f"✅ สร้าง {len(features_df.columns)-5} Advanced Features สำเร็จ")
        
        return features_df
    
    def train_advanced_models(self, data):
        """เทรน Advanced ML Models"""
        print(f"🤖 กำลังเทรน Advanced ML Models สำหรับ {self.league_name}...")
        
        # คำนวณ ELO ratings
        self.calculate_elo_ratings(data)
        
        # สร้าง features
        features_df = self.create_advanced_features(data)
        
        if len(features_df) < 100:
            print("❌ ข้อมูลไม่เพียงพอสำหรับการเทรน Advanced Models")
            return False
        
        # เทรนโมเดลแยกตามประเภท
        self._train_match_result_models(features_df)
        self._train_handicap_models(features_df)
        self._train_ou_models(features_df)
        self._train_corners_models(features_df)
        
        self.is_trained = True
        return True
    
    def _train_match_result_models(self, features_df):
        """เทรนโมเดลทำนายผลการแข่งขัน"""
        print("🎯 เทรนโมเดลทำนายผลการแข่งขัน...")
        
        # แยก features และ target
        target_cols = ['match_result', 'handicap_result', 'ou_result', 'corners_ou_10', 'corners_fh_5']
        X = features_df.drop(target_cols, axis=1)
        y = features_df['match_result']
        
        # Preprocessing
        X_processed = self.imputer.fit_transform(X)
        X_processed = self.scaler.fit_transform(X_processed)
        X_selected = self.feature_selector.fit_transform(X_processed, y)
        
        self.feature_columns = X.columns.tolist()
        selected_indices = self.feature_selector.get_support(indices=True)
        self.selected_feature_names = [self.feature_columns[i] for i in selected_indices]
        
        print(f"📊 Selected {len(self.selected_feature_names)} best features")
        
        # Split data
        split_idx = int(len(X_selected) * 0.8)
        X_train, X_test = X_selected[:split_idx], X_selected[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train models with hyperparameter tuning
        model_scores = {}
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        for name, model in self.models.items():
            print(f"   เทรน {name}...")
            
            # Hyperparameter tuning for key models
            if name == 'rf':
                param_grid = {'n_estimators': [200, 300], 'max_depth': [12, 15]}
                grid_search = GridSearchCV(model, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
                grid_search.fit(X_train, y_train)
                model = grid_search.best_estimator_
            
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
        
        print(f"\n📊 ผลการเทรนโมเดลผลการแข่งขัน:")
        for name, score in model_scores.items():
            print(f"   {name:<15}: {score:.3f}")
        print(f"   {'Ensemble':<15}: {ensemble_accuracy:.3f}")
    
    def _train_handicap_models(self, features_df):
        """เทรนโมเดล Handicap"""
        print("🎲 เทรนโมเดล Handicap...")
        
        target_cols = ['match_result', 'handicap_result', 'ou_result', 'corners_ou_10', 'corners_fh_5']
        X = features_df.drop(target_cols, axis=1)
        y = features_df['handicap_result']
        
        # ใช้ preprocessing เดียวกัน
        X_processed = self.imputer.transform(X)
        X_processed = self.scaler.transform(X_processed)
        X_selected = self.feature_selector.transform(X_processed)
        
        # เทรนโมเดลง่ายๆ
        handicap_model = RandomForestClassifier(n_estimators=200, random_state=42)
        handicap_model.fit(X_selected, y)
        
        self.handicap_models['rf'] = handicap_model
        
        # ทดสอบ
        accuracy = handicap_model.score(X_selected, y)
        print(f"   Handicap Model Accuracy: {accuracy:.3f}")
    
    def _train_ou_models(self, features_df):
        """เทรนโมเดล Over/Under"""
        print("⚽ เทรนโมเดล Over/Under...")
        
        target_cols = ['match_result', 'handicap_result', 'ou_result', 'corners_ou_10', 'corners_fh_5']
        X = features_df.drop(target_cols, axis=1)
        y = features_df['ou_result']
        
        X_processed = self.imputer.transform(X)
        X_processed = self.scaler.transform(X_processed)
        X_selected = self.feature_selector.transform(X_processed)
        
        ou_model = GradientBoostingClassifier(n_estimators=150, random_state=42)
        ou_model.fit(X_selected, y)
        
        self.ou_models['gb'] = ou_model
        
        accuracy = ou_model.score(X_selected, y)
        print(f"   Over/Under Model Accuracy: {accuracy:.3f}")
    
    def _train_corners_models(self, features_df):
        """เทรนโมเดล Corners"""
        print("🥅 เทรนโมเดล Corners...")
        
        target_cols = ['match_result', 'handicap_result', 'ou_result', 'corners_ou_10', 'corners_fh_5']
        X = features_df.drop(target_cols, axis=1)
        
        # Total Corners
        y_total = features_df['corners_ou_10']
        corners_total_model = ExtraTreesClassifier(n_estimators=200, random_state=42)
        
        X_processed = self.imputer.transform(X)
        X_processed = self.scaler.transform(X_processed)
        X_selected = self.feature_selector.transform(X_processed)
        
        corners_total_model.fit(X_selected, y_total)
        self.corners_models['total'] = corners_total_model
        
        # First Half Corners
        y_fh = features_df['corners_fh_5']
        corners_fh_model = ExtraTreesClassifier(n_estimators=200, random_state=42)
        corners_fh_model.fit(X_selected, y_fh)
        self.corners_models['first_half'] = corners_fh_model
        
        total_accuracy = corners_total_model.score(X_selected, y_total)
        fh_accuracy = corners_fh_model.score(X_selected, y_fh)
        
        print(f"   Corners Total Model Accuracy: {total_accuracy:.3f}")
        print(f"   Corners First Half Model Accuracy: {fh_accuracy:.3f}")
