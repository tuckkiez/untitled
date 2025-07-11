#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ระบบทำนายฟุตบอลแบบราคาต่อรอง
- ทำนายผลการแข่งขัน (ชนะ/แพ้/เสมอ)
- ทำนายราคาต่อรอง (Handicap) เช่น ต่อ 1.5, รอง 0.5
- ทำนายประตูสูง/ต่ำ (Over/Under)
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

class HandicapFootballPredictor:
    def __init__(self):
        # โมเดลสำหรับทำนายผลการแข่งขัน
        self.result_model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # โมเดลสำหรับทำนายผลต่างประตู (สำหรับคำนวณ handicap)
        self.goal_diff_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # โมเดลสำหรับทำนายประตูรวม
        self.total_goals_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.feature_columns = []
        self.is_trained = False
        
    def safe_divide(self, numerator, denominator, default=0.0):
        """ปลอดภัยจากการหารด้วยศูนย์"""
        if denominator == 0:
            return default
        return numerator / denominator
    
    def calculate_team_stats(self, matches_df, team_name, last_n_games=10):
        """คำนวณสถิติของทีม"""
        team_matches = matches_df[
            (matches_df['home_team'] == team_name) | 
            (matches_df['away_team'] == team_name)
        ].tail(last_n_games)
        
        if len(team_matches) == 0:
            return self._default_stats()
        
        stats = {}
        
        # สถิติพื้นฐาน
        wins = draws = losses = 0
        goals_for = goals_against = 0
        home_goals_for = away_goals_for = 0
        home_goals_against = away_goals_against = 0
        
        # สถิติราคาต่อรอง
        goal_differences = []
        total_goals_per_game = []
        big_wins = 0  # ชนะห่าง 2+ ประตู
        big_losses = 0  # แพ้ห่าง 2+ ประตู
        
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
            
            # ผลต่างประตู
            goal_diff = team_goals - opp_goals
            goal_differences.append(goal_diff)
            total_goals_per_game.append(team_goals + opp_goals)
            
            # ผลการแข่งขัน
            if team_goals > opp_goals:
                wins += 1
                if goal_diff >= 2:
                    big_wins += 1
            elif team_goals == opp_goals:
                draws += 1
            else:
                losses += 1
                if goal_diff <= -2:
                    big_losses += 1
        
        total_games = len(team_matches)
        home_games = len(team_matches[team_matches['home_team'] == team_name])
        away_games = total_games - home_games
        
        # คำนวณสถิติ
        stats['win_rate'] = self.safe_divide(wins, total_games, 0.33)
        stats['draw_rate'] = self.safe_divide(draws, total_games, 0.33)
        stats['loss_rate'] = self.safe_divide(losses, total_games, 0.34)
        
        # สถิติประตู
        stats['avg_goals_for'] = self.safe_divide(goals_for, total_games, 1.2)
        stats['avg_goals_against'] = self.safe_divide(goals_against, total_games, 1.2)
        stats['goal_difference'] = stats['avg_goals_for'] - stats['avg_goals_against']
        
        # สถิติเหย้า/เยือน
        stats['home_avg_goals_for'] = self.safe_divide(home_goals_for, home_games, 1.4)
        stats['away_avg_goals_for'] = self.safe_divide(away_goals_for, away_games, 1.0)
        stats['home_avg_goals_against'] = self.safe_divide(home_goals_against, home_games, 1.0)
        stats['away_avg_goals_against'] = self.safe_divide(away_goals_against, away_games, 1.4)
        
        # สถิติราคาต่อรอง
        stats['avg_goal_difference'] = np.mean(goal_differences) if goal_differences else 0.0
        stats['avg_total_goals'] = np.mean(total_goals_per_game) if total_goals_per_game else 2.5
        stats['big_win_rate'] = self.safe_divide(big_wins, total_games, 0.1)
        stats['big_loss_rate'] = self.safe_divide(big_losses, total_games, 0.1)
        
        # สถิติเพิ่มเติม
        stats['high_scoring_rate'] = sum(1 for g in total_goals_per_game if g >= 3) / len(total_goals_per_game) if total_goals_per_game else 0.4
        stats['low_scoring_rate'] = sum(1 for g in total_goals_per_game if g <= 1) / len(total_goals_per_game) if total_goals_per_game else 0.2
        stats['clean_sheet_rate'] = sum(1 for diff in goal_differences if (diff > 0 and is_home) or (diff < 0 and not is_home)) / len(goal_differences) if goal_differences else 0.2
        
        # ตรวจสอบ NaN
        for key, value in stats.items():
            if pd.isna(value) or np.isinf(value):
                stats[key] = self._default_stats()[key]
        
        return stats
    
    def _default_stats(self):
        """สถิติเริ่มต้น"""
        return {
            'win_rate': 0.33, 'draw_rate': 0.33, 'loss_rate': 0.34,
            'avg_goals_for': 1.2, 'avg_goals_against': 1.2, 'goal_difference': 0.0,
            'home_avg_goals_for': 1.4, 'away_avg_goals_for': 1.0,
            'home_avg_goals_against': 1.0, 'away_avg_goals_against': 1.4,
            'avg_goal_difference': 0.0, 'avg_total_goals': 2.5,
            'big_win_rate': 0.1, 'big_loss_rate': 0.1,
            'high_scoring_rate': 0.4, 'low_scoring_rate': 0.2, 'clean_sheet_rate': 0.2
        }
    
    def calculate_handicap_line(self, home_stats, away_stats):
        """คำนวณราคาต่อรองที่เหมาะสม"""
        # ความแตกต่างของทีม
        strength_diff = (home_stats['avg_goals_for'] - home_stats['avg_goals_against']) - \
                       (away_stats['avg_goals_for'] - away_stats['avg_goals_against'])
        
        # เพิ่ม home advantage
        strength_diff += 0.3
        
        # แปลงเป็นราคาต่อรอง
        if strength_diff >= 1.5:
            return 1.5  # ทีมเหย้าต่อ 1.5
        elif strength_diff >= 1.0:
            return 1.0  # ทีมเหย้าต่อ 1
        elif strength_diff >= 0.5:
            return 0.5  # ทีมเหย้าต่อ 0.5
        elif strength_diff >= -0.5:
            return 0.0  # เสมอ
        elif strength_diff >= -1.0:
            return -0.5  # ทีมเยือนต่อ 0.5
        elif strength_diff >= -1.5:
            return -1.0  # ทีมเยือนต่อ 1
        else:
            return -1.5  # ทีมเยือนต่อ 1.5
    
    def calculate_over_under_line(self, home_stats, away_stats):
        """คำนวณเส้นสูง/ต่ำที่เหมาะสม"""
        expected_goals = (home_stats['home_avg_goals_for'] + away_stats['away_avg_goals_for'] + 
                         home_stats['home_avg_goals_against'] + away_stats['away_avg_goals_against']) / 2
        
        # ปรับตามสถิติการเจอกัน
        if expected_goals >= 3.0:
            return 3.5
        elif expected_goals >= 2.5:
            return 2.5
        elif expected_goals >= 2.0:
            return 2.0
        else:
            return 1.5
    
    def prepare_features(self, matches_df):
        """เตรียม features"""
        features = []
        result_labels = []
        goal_diff_labels = []
        total_goals_labels = []
        
        print("กำลังเตรียม features สำหรับการทำนายราคาต่อรอง...")
        
        for idx, match in matches_df.iterrows():
            if idx < 15:
                continue
            
            historical_data = matches_df.iloc[:idx]
            
            # สถิติของทั้งสองทีม
            home_stats = self.calculate_team_stats(historical_data, match['home_team'])
            away_stats = self.calculate_team_stats(historical_data, match['away_team'])
            
            # สร้าง feature vector
            feature_row = []
            
            # Basic stats (12 features)
            for stat_name in ['win_rate', 'draw_rate', 'loss_rate', 'avg_goals_for', 'avg_goals_against', 'goal_difference']:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Handicap-specific stats (12 features)
            for stat_name in ['avg_goal_difference', 'big_win_rate', 'big_loss_rate', 'avg_total_goals', 'high_scoring_rate', 'low_scoring_rate']:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Relative features (6 features)
            feature_row.append(home_stats['avg_goals_for'] - away_stats['avg_goals_against'])
            feature_row.append(away_stats['avg_goals_for'] - home_stats['avg_goals_against'])
            feature_row.append(home_stats['avg_goal_difference'] - away_stats['avg_goal_difference'])
            feature_row.append(home_stats['big_win_rate'] - away_stats['big_loss_rate'])
            feature_row.append(home_stats['avg_total_goals'] - away_stats['avg_total_goals'])
            feature_row.append(1.0)  # home advantage
            
            # ตรวจสอบ NaN/Inf
            feature_row = [0.0 if pd.isna(x) or np.isinf(x) else float(x) for x in feature_row]
            features.append(feature_row)
            
            # Labels
            home_goals = int(match['home_goals']) if pd.notna(match['home_goals']) else 0
            away_goals = int(match['away_goals']) if pd.notna(match['away_goals']) else 0
            goal_diff = home_goals - away_goals
            total_goals = home_goals + away_goals
            
            # Result label
            if home_goals > away_goals:
                result_labels.append(2)  # home win
            elif home_goals < away_goals:
                result_labels.append(0)  # away win
            else:
                result_labels.append(1)  # draw
            
            goal_diff_labels.append(goal_diff)
            total_goals_labels.append(total_goals)
        
        self.feature_columns = [
            'home_win_rate', 'away_win_rate', 'home_draw_rate', 'away_draw_rate',
            'home_loss_rate', 'away_loss_rate', 'home_avg_goals_for', 'away_avg_goals_for',
            'home_avg_goals_against', 'away_avg_goals_against', 'home_goal_diff', 'away_goal_diff',
            'home_avg_goal_diff', 'away_avg_goal_diff', 'home_big_win_rate', 'away_big_win_rate',
            'home_big_loss_rate', 'away_big_loss_rate', 'home_avg_total_goals', 'away_avg_total_goals',
            'home_high_scoring_rate', 'away_high_scoring_rate', 'home_low_scoring_rate', 'away_low_scoring_rate',
            'home_attack_vs_away_defense', 'away_attack_vs_home_defense', 'goal_diff_advantage',
            'big_win_advantage', 'total_goals_diff', 'home_advantage'
        ]
        
        print(f"เตรียม features สำเร็จ: {len(features)} samples, {len(self.feature_columns)} features")
        
        return (np.array(features), np.array(result_labels), 
                np.array(goal_diff_labels), np.array(total_goals_labels))
    
    def train(self, matches_df):
        """เทรนโมเดล"""
        print("กำลังเทรนโมเดลราคาต่อรอง...")
        
        X, y_result, y_goal_diff, y_total_goals = self.prepare_features(matches_df)
        
        if len(X) < 50:
            print("ข้อมูลไม่เพียงพอสำหรับการเทรน")
            return False
        
        # ตรวจสอบและแก้ไข NaN
        X = self.imputer.fit_transform(X)
        X_scaled = self.scaler.fit_transform(X)
        
        # แบ่งข้อมูล
        X_train, X_test, y_result_train, y_result_test = train_test_split(
            X_scaled, y_result, test_size=0.2, random_state=42
        )
        
        _, _, y_diff_train, y_diff_test = train_test_split(
            X_scaled, y_goal_diff, test_size=0.2, random_state=42
        )
        
        _, _, y_total_train, y_total_test = train_test_split(
            X_scaled, y_total_goals, test_size=0.2, random_state=42
        )
        
        # เทรนโมเดล
        print("1. เทรนโมเดลทำนายผลการแข่งขัน...")
        self.result_model.fit(X_train, y_result_train)
        result_pred = self.result_model.predict(X_test)
        result_accuracy = accuracy_score(y_result_test, result_pred)
        
        print("2. เทรนโมเดลทำนายผลต่างประตู...")
        self.goal_diff_model.fit(X_train, y_diff_train)
        
        print("3. เทรนโมเดลทำนายประตูรวม...")
        self.total_goals_model.fit(X_train, y_total_train)
        
        print(f"\n📊 ผลการเทรน:")
        print(f"   ความแม่นยำผลการแข่งขัน: {result_accuracy:.3f} ({result_accuracy*100:.1f}%)")
        
        self.is_trained = True
        return True
    
    def predict_handicap(self, home_team, away_team, matches_df):
        """ทำนายราคาต่อรองครบถ้วน"""
        if not self.is_trained:
            print("โมเดลยังไม่ได้เทรน")
            return None
        
        try:
            # คำนวณสถิติ
            home_stats = self.calculate_team_stats(matches_df, home_team)
            away_stats = self.calculate_team_stats(matches_df, away_team)
            
            # สร้าง feature vector
            feature_row = []
            
            # Basic stats
            for stat_name in ['win_rate', 'draw_rate', 'loss_rate', 'avg_goals_for', 'avg_goals_against', 'goal_difference']:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Handicap-specific stats
            for stat_name in ['avg_goal_difference', 'big_win_rate', 'big_loss_rate', 'avg_total_goals', 'high_scoring_rate', 'low_scoring_rate']:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Relative features
            feature_row.extend([
                home_stats['avg_goals_for'] - away_stats['avg_goals_against'],
                away_stats['avg_goals_for'] - home_stats['avg_goals_against'],
                home_stats['avg_goal_difference'] - away_stats['avg_goal_difference'],
                home_stats['big_win_rate'] - away_stats['big_loss_rate'],
                home_stats['avg_total_goals'] - away_stats['avg_total_goals'],
                1.0
            ])
            
            # ตรวจสอบ NaN/Inf
            feature_row = [0.0 if pd.isna(x) or np.isinf(x) else float(x) for x in feature_row]
            
            # Transform features
            feature_imputed = self.imputer.transform([feature_row])
            feature_scaled = self.scaler.transform(feature_imputed)
            
            # ทำนาย
            result_pred = self.result_model.predict(feature_scaled)[0]
            result_proba = self.result_model.predict_proba(feature_scaled)[0]
            
            goal_diff_pred = self.goal_diff_model.predict(feature_scaled)[0]
            total_goals_pred = self.total_goals_model.predict(feature_scaled)[0]
            
            # แปลงผลลัพธ์
            result_map = {0: 'Away Win', 1: 'Draw', 2: 'Home Win'}
            predicted_result = result_map[result_pred]
            
            # คำนวณราคาต่อรอง
            handicap_line = self.calculate_handicap_line(home_stats, away_stats)
            over_under_line = self.calculate_over_under_line(home_stats, away_stats)
            
            # ทำนายราคาต่อรอง
            handicap_result = self.evaluate_handicap(goal_diff_pred, handicap_line)
            over_under_result = "Over" if total_goals_pred > over_under_line else "Under"
            
            return {
                'match': f"{home_team} vs {away_team}",
                'result_prediction': predicted_result,
                'result_confidence': max(result_proba),
                'result_probabilities': {
                    'Away Win': result_proba[0],
                    'Draw': result_proba[1],
                    'Home Win': result_proba[2]
                },
                'predicted_goal_difference': round(goal_diff_pred, 1),
                'predicted_total_goals': round(total_goals_pred, 1),
                'handicap_line': handicap_line,
                'handicap_prediction': handicap_result,
                'over_under_line': over_under_line,
                'over_under_prediction': over_under_result
            }
            
        except Exception as e:
            print(f"Error in handicap prediction: {e}")
            return None
    
    def evaluate_handicap(self, goal_diff, handicap_line):
        """ประเมินผลราคาต่อรอง"""
        adjusted_diff = goal_diff - handicap_line
        
        if adjusted_diff > 0:
            return "ต่อ" if handicap_line >= 0 else "รอง"
        elif adjusted_diff < 0:
            return "รอง" if handicap_line >= 0 else "ต่อ"
        else:
            return "คืนเงิน"

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    print("=== ระบบทำนายราคาต่อรองฟุตบอล ===")
    
    try:
        # โหลดข้อมูล
        matches_df = pd.read_csv('/Users/80090/Desktop/Project/untitle/sample_matches.csv')
        matches_df['date'] = pd.to_datetime(matches_df['date'])
        
        predictor = HandicapFootballPredictor()
        
        if predictor.train(matches_df):
            # ทำนายตัวอย่าง
            result = predictor.predict_handicap('Arsenal', 'Chelsea', matches_df)
            if result:
                print(f"\n=== การทำนายราคาต่อรอง ===")
                print(f"🏆 {result['match']}")
                print(f"   ผลการแข่งขัน: {result['result_prediction']} (มั่นใจ {result['result_confidence']:.3f})")
                print(f"   ราคาต่อรอง: {result['handicap_line']} → {result['handicap_prediction']}")
                print(f"   สูง/ต่ำ: {result['over_under_line']} → {result['over_under_prediction']}")
            
    except FileNotFoundError:
        print("ไม่พบไฟล์ข้อมูล")
