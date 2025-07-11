#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
โมเดลทำนายฟุตบอลที่ปรับปรุงแล้ว
เพิ่มความแม่นยำด้วย Advanced Features และ Ensemble Methods
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class EnhancedFootballPredictor:
    def __init__(self):
        self.ensemble_model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.is_trained = False
        
    def calculate_advanced_team_stats(self, matches_df, team_name, last_n_games=15):
        """คำนวณสถิติขั้นสูงของทีม"""
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
        recent_form = []  # ฟอร์ม 5 เกมล่าสุด
        goal_times = []  # เวลาที่ทำประตู
        clean_sheets = 0
        big_wins = 0  # ชนะห่าง 3+ ประตู
        comeback_wins = 0  # ชนะหลังตาม
        
        for _, match in team_matches.iterrows():
            is_home = match['home_team'] == team_name
            
            if is_home:
                team_goals = match['home_goals']
                opp_goals = match['away_goals']
                home_goals_for += team_goals
                home_goals_against += opp_goals
            else:
                team_goals = match['away_goals']
                opp_goals = match['home_goals']
                away_goals_for += team_goals
                away_goals_against += opp_goals
            
            goals_for += team_goals
            goals_against += opp_goals
            
            # ผลการแข่งขัน
            if team_goals > opp_goals:
                wins += 1
                recent_form.append(3)  # 3 คะแนน
                if is_home:
                    home_wins += 1
                else:
                    away_wins += 1
                    
                # Big win
                if team_goals - opp_goals >= 3:
                    big_wins += 1
                    
            elif team_goals == opp_goals:
                draws += 1
                recent_form.append(1)  # 1 คะแนน
            else:
                losses += 1
                recent_form.append(0)  # 0 คะแนน
            
            # Clean sheet
            if opp_goals == 0:
                clean_sheets += 1
        
        total_games = len(team_matches)
        home_games = len(team_matches[team_matches['home_team'] == team_name])
        away_games = total_games - home_games
        
        # คำนวณสถิติ
        stats['win_rate'] = wins / total_games if total_games > 0 else 0
        stats['draw_rate'] = draws / total_games if total_games > 0 else 0
        stats['loss_rate'] = losses / total_games if total_games > 0 else 0
        stats['avg_goals_for'] = goals_for / total_games if total_games > 0 else 0
        stats['avg_goals_against'] = goals_against / total_games if total_games > 0 else 0
        stats['goal_difference'] = stats['avg_goals_for'] - stats['avg_goals_against']
        
        # สถิติขั้นสูง
        stats['home_win_rate'] = home_wins / home_games if home_games > 0 else 0
        stats['away_win_rate'] = away_wins / away_games if away_games > 0 else 0
        stats['home_avg_goals_for'] = home_goals_for / home_games if home_games > 0 else 0
        stats['away_avg_goals_for'] = away_goals_for / away_games if away_games > 0 else 0
        stats['home_avg_goals_against'] = home_goals_against / home_games if home_games > 0 else 0
        stats['away_avg_goals_against'] = away_goals_against / away_games if away_games > 0 else 0
        
        # ฟอร์มล่าสุด (5 เกม)
        recent_5 = recent_form[-5:] if len(recent_form) >= 5 else recent_form
        stats['recent_form'] = sum(recent_5) / len(recent_5) if recent_5 else 1.0
        
        # สถิติเพิ่มเติม
        stats['clean_sheet_rate'] = clean_sheets / total_games if total_games > 0 else 0
        stats['big_win_rate'] = big_wins / total_games if total_games > 0 else 0
        stats['scoring_consistency'] = 1 - (np.std([g for g in [home_goals_for, away_goals_for] if g > 0]) / max(1, stats['avg_goals_for']))
        
        # Momentum (ถ่วงน้ำหนักเกมล่าสุด)
        weights = np.exp(np.linspace(-1, 0, len(recent_form)))
        stats['momentum'] = np.average(recent_form, weights=weights) if recent_form else 1.0
        
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
            'scoring_consistency': 0.5, 'momentum': 1.0
        }
    
    def calculate_head_to_head_stats(self, matches_df, home_team, away_team, last_n=10):
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
            total_goals += match['home_goals'] + match['away_goals']
            
            if match['home_team'] == home_team:
                if match['home_goals'] > match['away_goals']:
                    home_wins += 1
            else:
                if match['away_goals'] > match['home_goals']:
                    home_wins += 1
        
        return {
            'h2h_home_advantage': 0.2 if home_wins > len(h2h_matches) / 2 else 0.0,
            'h2h_avg_goals': total_goals / len(h2h_matches),
            'h2h_home_win_rate': home_wins / len(h2h_matches)
        }
    
    def prepare_enhanced_features(self, matches_df):
        """เตรียมข้อมูล features ขั้นสูง"""
        features = []
        labels = []
        
        print("กำลังสร้าง enhanced features...")
        
        for idx, match in matches_df.iterrows():
            if idx < 20:  # ข้าม 20 เกมแรกเพื่อให้มีข้อมูลเพียงพอ
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
            for stat_name in ['win_rate', 'draw_rate', 'loss_rate', 'avg_goals_for', 'avg_goals_against', 'goal_difference']:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Advanced stats (16 features)
            for stat_name in ['home_win_rate', 'away_win_rate', 'recent_form', 'clean_sheet_rate', 
                            'big_win_rate', 'scoring_consistency', 'momentum', 'home_avg_goals_for']:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Relative features (8 features)
            feature_row.append(home_stats['win_rate'] - away_stats['win_rate'])
            feature_row.append(home_stats['goal_difference'] - away_stats['goal_difference'])
            feature_row.append(home_stats['recent_form'] - away_stats['recent_form'])
            feature_row.append(home_stats['momentum'] - away_stats['momentum'])
            feature_row.append(home_stats['home_win_rate'] - away_stats['away_win_rate'])
            feature_row.append(home_stats['scoring_consistency'] - away_stats['scoring_consistency'])
            feature_row.append(home_stats['clean_sheet_rate'] - away_stats['clean_sheet_rate'])
            feature_row.append(home_stats['big_win_rate'] - away_stats['big_win_rate'])
            
            # Head-to-head features (3 features)
            feature_row.append(h2h_stats['h2h_home_advantage'])
            feature_row.append(h2h_stats['h2h_avg_goals'])
            feature_row.append(h2h_stats['h2h_home_win_rate'])
            
            # Home advantage (1 feature)
            feature_row.append(1.0)  # home advantage constant
            
            features.append(feature_row)
            
            # Label
            if match['home_goals'] > match['away_goals']:
                labels.append(2)  # home win
            elif match['home_goals'] < match['away_goals']:
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
            'home_big_win_rate', 'away_big_win_rate', 'home_scoring_consistency', 'away_scoring_consistency',
            'home_momentum', 'away_momentum', 'home_home_avg_goals_for', 'away_home_avg_goals_for',
            'win_rate_diff', 'goal_diff_diff', 'recent_form_diff', 'momentum_diff',
            'home_away_advantage', 'scoring_consistency_diff', 'clean_sheet_diff', 'big_win_diff',
            'h2h_home_advantage', 'h2h_avg_goals', 'h2h_home_win_rate', 'home_advantage'
        ]
        
        print(f"สร้าง features สำเร็จ: {len(features)} samples, {len(self.feature_columns)} features")
        
        return np.array(features), np.array(labels)
    
    def create_ensemble_model(self):
        """สร้าง ensemble model"""
        # Random Forest with optimized parameters
        rf = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
        
        # Gradient Boosting
        gb = GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=8,
            random_state=42
        )
        
        # Logistic Regression
        lr = LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced'
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
        
        if len(X) < 100:
            print("ข้อมูลไม่เพียงพอสำหรับการเทรนขั้นสูง (ต้องการอย่างน้อย 100 เกม)")
            return False
        
        print(f"จำนวนเกมที่ใช้เทรน: {len(X)}")
        print(f"จำนวน features: {len(self.feature_columns)}")
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # แบ่งข้อมูล
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.25, random_state=42, stratify=y
        )
        
        # สร้างและเทรน ensemble model
        print("กำลังเทรน ensemble model...")
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
        cv_scores = cross_val_score(self.ensemble_model, X_scaled, y, cv=5)
        print(f"Cross Validation Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        self.is_trained = True
        return True
    
    def predict_match(self, home_team, away_team, matches_df):
        """ทำนายผลการแข่งขันด้วยโมเดลขั้นสูง"""
        if not self.is_trained:
            print("โมเดลยังไม่ได้เทรน")
            return None
        
        # คำนวณสถิติปัจจุบัน
        home_stats = self.calculate_advanced_team_stats(matches_df, home_team)
        away_stats = self.calculate_advanced_team_stats(matches_df, away_team)
        h2h_stats = self.calculate_head_to_head_stats(matches_df, home_team, away_team)
        
        # สร้าง feature vector
        feature_row = []
        
        # Basic stats
        for stat_name in ['win_rate', 'draw_rate', 'loss_rate', 'avg_goals_for', 'avg_goals_against', 'goal_difference']:
            feature_row.append(home_stats[stat_name])
            feature_row.append(away_stats[stat_name])
        
        # Advanced stats
        for stat_name in ['home_win_rate', 'away_win_rate', 'recent_form', 'clean_sheet_rate', 
                        'big_win_rate', 'scoring_consistency', 'momentum', 'home_avg_goals_for']:
            feature_row.append(home_stats[stat_name])
            feature_row.append(away_stats[stat_name])
        
        # Relative features
        feature_row.extend([
            home_stats['win_rate'] - away_stats['win_rate'],
            home_stats['goal_difference'] - away_stats['goal_difference'],
            home_stats['recent_form'] - away_stats['recent_form'],
            home_stats['momentum'] - away_stats['momentum'],
            home_stats['home_win_rate'] - away_stats['away_win_rate'],
            home_stats['scoring_consistency'] - away_stats['scoring_consistency'],
            home_stats['clean_sheet_rate'] - away_stats['clean_sheet_rate'],
            home_stats['big_win_rate'] - away_stats['big_win_rate']
        ])
        
        # Head-to-head features
        feature_row.extend([
            h2h_stats['h2h_home_advantage'],
            h2h_stats['h2h_avg_goals'],
            h2h_stats['h2h_home_win_rate']
        ])
        
        # Home advantage
        feature_row.append(1.0)
        
        # Normalize
        feature_scaled = self.scaler.transform([feature_row])
        
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
            'model_type': 'Enhanced Ensemble'
        }
    
    def backtest(self, matches_df, test_period_games=50):
        """Backtest ขั้นสูง"""
        if len(matches_df) < test_period_games + 150:
            print("ข้อมูลไม่เพียงพอสำหรับ enhanced backtest")
            return None
        
        # แบ่งข้อมูล
        train_data = matches_df.iloc[:-test_period_games]
        test_data = matches_df.iloc[-test_period_games:]
        
        # เทรนโมเดลใหม่
        print("กำลังเทรน Enhanced Model สำหรับ backtest...")
        temp_model = EnhancedFootballPredictor()
        if not temp_model.train(train_data):
            return None
        
        # ทดสอบ
        correct_predictions = 0
        total_predictions = 0
        results = []
        confidence_levels = []
        
        print("กำลังทำ Enhanced Backtest...")
        for idx, match in test_data.iterrows():
            prediction_result = temp_model.predict_match(
                match['home_team'], match['away_team'], train_data
            )
            
            if prediction_result:
                # ผลจริง
                if match['home_goals'] > match['away_goals']:
                    actual = 'Home Win'
                elif match['home_goals'] < match['away_goals']:
                    actual = 'Away Win'
                else:
                    actual = 'Draw'
                
                predicted = prediction_result['prediction']
                is_correct = (predicted == actual)
                confidence = prediction_result['confidence']
                
                if is_correct:
                    correct_predictions += 1
                total_predictions += 1
                
                confidence_levels.append(confidence)
                results.append({
                    'home_team': match['home_team'],
                    'away_team': match['away_team'],
                    'actual': actual,
                    'predicted': predicted,
                    'correct': is_correct,
                    'confidence': confidence
                })
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        avg_confidence = np.mean(confidence_levels) if confidence_levels else 0
        
        print(f"\nผล Enhanced Backtest:")
        print(f"จำนวนเกมที่ทดสอบ: {total_predictions}")
        print(f"ทำนายถูก: {correct_predictions}")
        print(f"ความแม่นยำ: {accuracy:.3f} ({accuracy*100:.1f}%)")
        print(f"ความมั่นใจเฉลี่ย: {avg_confidence:.3f} ({avg_confidence*100:.1f}%)")
        
        # วิเคราะห์ความแม่นยำตามระดับความมั่นใจ
        high_confidence_results = [r for r in results if r['confidence'] > 0.6]
        if high_confidence_results:
            high_conf_accuracy = sum(r['correct'] for r in high_confidence_results) / len(high_confidence_results)
            print(f"ความแม่นยำเมื่อความมั่นใจ > 60%: {high_conf_accuracy:.3f} ({high_conf_accuracy*100:.1f}%)")
            print(f"จำนวนการทำนายที่มั่นใจสูง: {len(high_confidence_results)}/{total_predictions}")
        
        return {
            'accuracy': accuracy,
            'total_games': total_predictions,
            'correct_predictions': correct_predictions,
            'avg_confidence': avg_confidence,
            'results': results
        }

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    print("=== Enhanced Football Prediction System ===")
    
    # โหลดข้อมูลจริง (ต้องมีไฟล์ sample_matches.csv)
    try:
        matches_df = pd.read_csv('/Users/80090/Desktop/Project/untitle/sample_matches.csv')
        matches_df['date'] = pd.to_datetime(matches_df['date'])
        
        predictor = EnhancedFootballPredictor()
        
        if predictor.train(matches_df):
            # ทำนายตัวอย่าง
            result = predictor.predict_match('Arsenal', 'Chelsea', matches_df)
            if result:
                print(f"\n=== Enhanced Prediction ===")
                print(f"Arsenal vs Chelsea")
                print(f"การทำนาย: {result['prediction']}")
                print(f"ความมั่นใจ: {result['confidence']:.3f}")
                print(f"โมเดล: {result['model_type']}")
            
            # Backtest
            backtest_result = predictor.backtest(matches_df, test_period_games=30)
            
    except FileNotFoundError:
        print("ไม่พบไฟล์ข้อมูล กรุณารันโปรแกรมหลักก่อน")
