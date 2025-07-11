#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
โมเดลทำนายฟุตบอลที่ปรับปรุงแล้ว (แก้ไข NaN issues)
เพิ่มความแม่นยำด้วย Advanced Features และ Ensemble Methods
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

class EnhancedFootballPredictorFixed:
    def __init__(self):
        self.ensemble_model = None
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.feature_columns = []
        self.is_trained = False
        
    def safe_divide(self, numerator, denominator, default=0.0):
        """ปลอดภัยจากการหารด้วยศูนย์"""
        if denominator == 0:
            return default
        return numerator / denominator
    
    def calculate_advanced_team_stats(self, matches_df, team_name, last_n_games=12):
        """คำนวณสถิติขั้นสูงของทีม (แก้ไข NaN)"""
        # กรองเกมของทีม
        team_matches = matches_df[
            (matches_df['home_team'] == team_name) | 
            (matches_df['away_team'] == team_name)
        ].tail(last_n_games)
        
        if len(team_matches) == 0:
            return self._default_advanced_stats()
        
        stats = {}
        
        # สถิติพื้นฐาน
        wins = draws = losses = 0
        goals_for = goals_against = 0
        home_wins = away_wins = 0
        home_goals_for = away_goals_for = 0
        home_goals_against = away_goals_against = 0
        
        # สถิติขั้นสูง
        recent_form = []
        clean_sheets = 0
        big_wins = 0
        
        for _, match in team_matches.iterrows():
            is_home = match['home_team'] == team_name
            
            if is_home:
                team_goals = int(match['home_goals']) if pd.notna(match['home_goals']) else 0
                opp_goals = int(match['away_goals']) if pd.notna(match['away_goals']) else 0
                home_goals_for += team_goals
                home_goals_against += opp_goals
            else:
                team_goals = int(match['away_goals']) if pd.notna(match['away_goals']) else 0
                opp_goals = int(match['home_goals']) if pd.notna(match['home_goals']) else 0
                away_goals_for += team_goals
                away_goals_against += opp_goals
            
            goals_for += team_goals
            goals_against += opp_goals
            
            # ผลการแข่งขัน
            if team_goals > opp_goals:
                wins += 1
                recent_form.append(3)
                if is_home:
                    home_wins += 1
                else:
                    away_wins += 1
                if team_goals - opp_goals >= 3:
                    big_wins += 1
            elif team_goals == opp_goals:
                draws += 1
                recent_form.append(1)
            else:
                losses += 1
                recent_form.append(0)
            
            if opp_goals == 0:
                clean_sheets += 1
        
        total_games = len(team_matches)
        home_games = len(team_matches[team_matches['home_team'] == team_name])
        away_games = total_games - home_games
        
        # คำนวณสถิติ (ป้องกัน division by zero)
        stats['win_rate'] = self.safe_divide(wins, total_games, 0.33)
        stats['draw_rate'] = self.safe_divide(draws, total_games, 0.33)
        stats['loss_rate'] = self.safe_divide(losses, total_games, 0.34)
        stats['avg_goals_for'] = self.safe_divide(goals_for, total_games, 1.0)
        stats['avg_goals_against'] = self.safe_divide(goals_against, total_games, 1.0)
        stats['goal_difference'] = stats['avg_goals_for'] - stats['avg_goals_against']
        
        # สถิติขั้นสูง
        stats['home_win_rate'] = self.safe_divide(home_wins, home_games, 0.4)
        stats['away_win_rate'] = self.safe_divide(away_wins, away_games, 0.25)
        stats['home_avg_goals_for'] = self.safe_divide(home_goals_for, home_games, 1.2)
        stats['away_avg_goals_for'] = self.safe_divide(away_goals_for, away_games, 0.8)
        stats['home_avg_goals_against'] = self.safe_divide(home_goals_against, home_games, 0.8)
        stats['away_avg_goals_against'] = self.safe_divide(away_goals_against, away_games, 1.2)
        
        # ฟอร์มล่าสุด
        recent_5 = recent_form[-5:] if len(recent_form) >= 5 else recent_form
        stats['recent_form'] = self.safe_divide(sum(recent_5), len(recent_5), 1.0) if recent_5 else 1.0
        
        # สถิติเพิ่มเติม
        stats['clean_sheet_rate'] = self.safe_divide(clean_sheets, total_games, 0.3)
        stats['big_win_rate'] = self.safe_divide(big_wins, total_games, 0.1)
        
        # Momentum (ถ่วงน้ำหนักเกมล่าสุด)
        if recent_form:
            weights = np.exp(np.linspace(-0.5, 0, len(recent_form)))
            stats['momentum'] = np.average(recent_form, weights=weights)
        else:
            stats['momentum'] = 1.0
        
        # ตรวจสอบ NaN และแทนที่
        for key, value in stats.items():
            if pd.isna(value) or np.isinf(value):
                stats[key] = self._default_advanced_stats()[key]
        
        return stats
    
    def _default_advanced_stats(self):
        """สถิติเริ่มต้นสำหรับทีมใหม่"""
        return {
            'win_rate': 0.33, 'draw_rate': 0.33, 'loss_rate': 0.34,
            'avg_goals_for': 1.2, 'avg_goals_against': 1.2, 'goal_difference': 0.0,
            'home_win_rate': 0.4, 'away_win_rate': 0.25,
            'home_avg_goals_for': 1.4, 'away_avg_goals_for': 1.0,
            'home_avg_goals_against': 1.0, 'away_avg_goals_against': 1.4,
            'recent_form': 1.0, 'clean_sheet_rate': 0.3, 'big_win_rate': 0.1,
            'momentum': 1.0
        }
    
    def calculate_head_to_head_stats(self, matches_df, home_team, away_team, last_n=8):
        """คำนวณสถิติการเจอกันโดยตรง"""
        h2h_matches = matches_df[
            ((matches_df['home_team'] == home_team) & (matches_df['away_team'] == away_team)) |
            ((matches_df['home_team'] == away_team) & (matches_df['away_team'] == home_team))
        ].tail(last_n)
        
        if len(h2h_matches) == 0:
            return {'h2h_home_advantage': 0.1, 'h2h_avg_goals': 2.5, 'h2h_home_win_rate': 0.4}
        
        home_wins = 0
        total_goals = 0
        
        for _, match in h2h_matches.iterrows():
            home_goals = int(match['home_goals']) if pd.notna(match['home_goals']) else 0
            away_goals = int(match['away_goals']) if pd.notna(match['away_goals']) else 0
            total_goals += home_goals + away_goals
            
            if match['home_team'] == home_team:
                if home_goals > away_goals:
                    home_wins += 1
            else:
                if away_goals > home_goals:
                    home_wins += 1
        
        return {
            'h2h_home_advantage': 0.15 if home_wins > len(h2h_matches) / 2 else 0.05,
            'h2h_avg_goals': self.safe_divide(total_goals, len(h2h_matches), 2.5),
            'h2h_home_win_rate': self.safe_divide(home_wins, len(h2h_matches), 0.4)
        }
    
    def prepare_enhanced_features(self, matches_df):
        """เตรียมข้อมูล features ขั้นสูง (แก้ไข NaN)"""
        features = []
        labels = []
        
        print("กำลังสร้าง enhanced features...")
        
        for idx, match in matches_df.iterrows():
            if idx < 15:  # ข้าม 15 เกมแรก
                continue
                
            # ใช้ข้อมูลก่อนหน้าเท่านั้น
            historical_data = matches_df.iloc[:idx]
            
            # สถิติของทั้งสองทีม
            home_stats = self.calculate_advanced_team_stats(historical_data, match['home_team'])
            away_stats = self.calculate_advanced_team_stats(historical_data, match['away_team'])
            
            # สถิติการเจอกันโดยตรง
            h2h_stats = self.calculate_head_to_head_stats(historical_data, match['home_team'], match['away_team'])
            
            # สร้าง feature vector
            feature_row = []
            
            # Basic stats (12 features)
            basic_stats = ['win_rate', 'draw_rate', 'loss_rate', 'avg_goals_for', 'avg_goals_against', 'goal_difference']
            for stat_name in basic_stats:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Advanced stats (12 features)
            advanced_stats = ['home_win_rate', 'away_win_rate', 'recent_form', 'clean_sheet_rate', 'big_win_rate', 'momentum']
            for stat_name in advanced_stats:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Relative features (6 features)
            feature_row.append(home_stats['win_rate'] - away_stats['win_rate'])
            feature_row.append(home_stats['goal_difference'] - away_stats['goal_difference'])
            feature_row.append(home_stats['recent_form'] - away_stats['recent_form'])
            feature_row.append(home_stats['momentum'] - away_stats['momentum'])
            feature_row.append(home_stats['home_win_rate'] - away_stats['away_win_rate'])
            feature_row.append(home_stats['clean_sheet_rate'] - away_stats['clean_sheet_rate'])
            
            # Head-to-head features (3 features)
            feature_row.append(h2h_stats['h2h_home_advantage'])
            feature_row.append(h2h_stats['h2h_avg_goals'])
            feature_row.append(h2h_stats['h2h_home_win_rate'])
            
            # Home advantage (1 feature)
            feature_row.append(1.0)
            
            # ตรวจสอบและแทนที่ NaN/Inf
            feature_row = [0.0 if pd.isna(x) or np.isinf(x) else float(x) for x in feature_row]
            
            features.append(feature_row)
            
            # Label
            home_goals = int(match['home_goals']) if pd.notna(match['home_goals']) else 0
            away_goals = int(match['away_goals']) if pd.notna(match['away_goals']) else 0
            
            if home_goals > away_goals:
                labels.append(2)  # home win
            elif home_goals < away_goals:
                labels.append(0)  # away win
            else:
                labels.append(1)  # draw
        
        # สร้างชื่อ features
        self.feature_columns = [
            'home_win_rate', 'away_win_rate', 'home_draw_rate', 'away_draw_rate',
            'home_loss_rate', 'away_loss_rate', 'home_avg_goals_for', 'away_avg_goals_for',
            'home_avg_goals_against', 'away_avg_goals_against', 'home_goal_diff', 'away_goal_diff',
            'home_home_win_rate', 'away_home_win_rate', 'home_away_win_rate', 'away_away_win_rate',
            'home_recent_form', 'away_recent_form', 'home_clean_sheet_rate', 'away_clean_sheet_rate',
            'home_big_win_rate', 'away_big_win_rate', 'home_momentum', 'away_momentum',
            'win_rate_diff', 'goal_diff_diff', 'recent_form_diff', 'momentum_diff',
            'home_away_advantage', 'clean_sheet_diff', 'h2h_home_advantage', 'h2h_avg_goals', 
            'h2h_home_win_rate', 'home_advantage'
        ]
        
        print(f"สร้าง features สำเร็จ: {len(features)} samples, {len(self.feature_columns)} features")
        
        return np.array(features), np.array(labels)
    
    def create_ensemble_model(self):
        """สร้าง ensemble model ที่ปรับปรุงแล้ว"""
        # Random Forest with optimized parameters
        rf = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            min_samples_split=8,
            min_samples_leaf=4,
            random_state=42,
            class_weight='balanced'
        )
        
        # Gradient Boosting (ใช้ HistGradientBoosting แทน)
        from sklearn.ensemble import HistGradientBoostingClassifier
        gb = HistGradientBoostingClassifier(
            max_iter=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        # Logistic Regression
        lr = LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced',
            C=0.1
        )
        
        # Ensemble
        ensemble = VotingClassifier(
            estimators=[
                ('rf', rf),
                ('gb', gb),
                ('lr', lr)
            ],
            voting='soft'
        )
        
        return ensemble
    
    def train(self, matches_df):
        """เทรนโมเดลขั้นสูง"""
        print("กำลังเตรียมข้อมูลสำหรับการเทรนขั้นสูง...")
        X, y = self.prepare_enhanced_features(matches_df)
        
        if len(X) < 80:
            print("ข้อมูลไม่เพียงพอสำหรับการเทรนขั้นสูง (ต้องการอย่างน้อย 80 เกม)")
            return False
        
        print(f"จำนวนเกมที่ใช้เทรน: {len(X)}")
        print(f"จำนวน features: {len(self.feature_columns)}")
        
        # ตรวจสอบและแก้ไข NaN
        X = self.imputer.fit_transform(X)
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # แบ่งข้อมูล
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # สร้างและเทรน ensemble model
        print("กำลังเทรน enhanced ensemble model...")
        self.ensemble_model = self.create_ensemble_model()
        self.ensemble_model.fit(X_train, y_train)
        
        # ทดสอบ
        y_pred = self.ensemble_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"ความแม่นยำของ Enhanced Model: {accuracy:.3f} ({accuracy*100:.1f}%)")
        print("\nรายงานผลการทำนายขั้นสูง:")
        print(classification_report(y_test, y_pred, 
                                  target_names=['Away Win', 'Draw', 'Home Win']))
        
        # Cross validation
        try:
            cv_scores = cross_val_score(self.ensemble_model, X_scaled, y, cv=3)
            print(f"Cross Validation Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        except:
            print("Cross validation ไม่สามารถทำได้")
        
        self.is_trained = True
        return True
    
    def predict_match(self, home_team, away_team, matches_df):
        """ทำนายผลการแข่งขันด้วยโมเดลขั้นสูง"""
        if not self.is_trained:
            print("โมเดลยังไม่ได้เทรน")
            return None
        
        try:
            # คำนวณสถิติปัจจุบัน
            home_stats = self.calculate_advanced_team_stats(matches_df, home_team)
            away_stats = self.calculate_advanced_team_stats(matches_df, away_team)
            h2h_stats = self.calculate_head_to_head_stats(matches_df, home_team, away_team)
            
            # สร้าง feature vector
            feature_row = []
            
            # Basic stats
            basic_stats = ['win_rate', 'draw_rate', 'loss_rate', 'avg_goals_for', 'avg_goals_against', 'goal_difference']
            for stat_name in basic_stats:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Advanced stats
            advanced_stats = ['home_win_rate', 'away_win_rate', 'recent_form', 'clean_sheet_rate', 'big_win_rate', 'momentum']
            for stat_name in advanced_stats:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Relative features
            feature_row.extend([
                home_stats['win_rate'] - away_stats['win_rate'],
                home_stats['goal_difference'] - away_stats['goal_difference'],
                home_stats['recent_form'] - away_stats['recent_form'],
                home_stats['momentum'] - away_stats['momentum'],
                home_stats['home_win_rate'] - away_stats['away_win_rate'],
                home_stats['clean_sheet_rate'] - away_stats['clean_sheet_rate']
            ])
            
            # Head-to-head features
            feature_row.extend([
                h2h_stats['h2h_home_advantage'],
                h2h_stats['h2h_avg_goals'],
                h2h_stats['h2h_home_win_rate']
            ])
            
            # Home advantage
            feature_row.append(1.0)
            
            # ตรวจสอบและแทนที่ NaN/Inf
            feature_row = [0.0 if pd.isna(x) or np.isinf(x) else float(x) for x in feature_row]
            
            # Transform features
            feature_imputed = self.imputer.transform([feature_row])
            feature_scaled = self.scaler.transform(feature_imputed)
            
            # ทำนาย
            prediction = self.ensemble_model.predict(feature_scaled)[0]
            probabilities = self.ensemble_model.predict_proba(feature_scaled)[0]
            
            result_map = {0: 'Away Win', 1: 'Draw', 2: 'Home Win'}
            
            return {
                'prediction': result_map[prediction],
                'probabilities': {
                    'Away Win': probabilities[0],
                    'Draw': probabilities[1],
                    'Home Win': probabilities[2]
                },
                'confidence': max(probabilities),
                'model_type': 'Enhanced Ensemble (Fixed)'
            }
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    print("=== Enhanced Football Prediction System (Fixed) ===")
    
    try:
        # โหลดข้อมูลจริง
        matches_df = pd.read_csv('/Users/80090/Desktop/Project/untitle/sample_matches.csv')
        matches_df['date'] = pd.to_datetime(matches_df['date'])
        
        predictor = EnhancedFootballPredictorFixed()
        
        if predictor.train(matches_df):
            # ทำนายตัวอย่าง
            result = predictor.predict_match('Arsenal', 'Chelsea', matches_df)
            if result:
                print(f"\n=== Enhanced Prediction (Fixed) ===")
                print(f"Arsenal vs Chelsea")
                print(f"การทำนาย: {result['prediction']}")
                print(f"ความมั่นใจ: {result['confidence']:.3f}")
                print(f"โมเดล: {result['model_type']}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("กรุณาตรวจสอบไฟล์ข้อมูล")
