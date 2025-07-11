#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ระบบทำนายฟุตบอลแบบครบถ้วน
- ทำนายทีมชนะ/แพ้/เสมอ
- ทำนายจำนวนประตูรวม (สูง/ต่ำ)
- ทำนายสกอร์ที่แน่นอน
- ทำนายผลต่างประตู
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

class ComprehensiveFootballPredictor:
    def __init__(self):
        # โมเดลสำหรับทำนายผลการแข่งขัน
        self.result_model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # โมเดลสำหรับทำนายประตูทีมเหย้า
        self.home_goals_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # โมเดลสำหรับทำนายประตูทีมเยือน
        self.away_goals_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
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
        
        # สถิติประตู
        goals_per_game = []
        goals_conceded_per_game = []
        total_goals_per_game = []
        
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
            
            # เก็บสถิติประตูแต่ละเกม
            goals_per_game.append(team_goals)
            goals_conceded_per_game.append(opp_goals)
            total_goals_per_game.append(team_goals + opp_goals)
            
            # ผลการแข่งขัน
            if team_goals > opp_goals:
                wins += 1
            elif team_goals == opp_goals:
                draws += 1
            else:
                losses += 1
        
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
        
        # สถิติประตูเหย้า/เยือน
        stats['home_avg_goals_for'] = self.safe_divide(home_goals_for, home_games, 1.4)
        stats['away_avg_goals_for'] = self.safe_divide(away_goals_for, away_games, 1.0)
        stats['home_avg_goals_against'] = self.safe_divide(home_goals_against, home_games, 1.0)
        stats['away_avg_goals_against'] = self.safe_divide(away_goals_against, away_games, 1.4)
        
        # สถิติประตูรวม
        stats['avg_total_goals'] = np.mean(total_goals_per_game) if total_goals_per_game else 2.5
        stats['goals_variance'] = np.var(goals_per_game) if len(goals_per_game) > 1 else 1.0
        
        # สถิติเพิ่มเติม
        stats['high_scoring_rate'] = sum(1 for g in total_goals_per_game if g >= 3) / len(total_goals_per_game) if total_goals_per_game else 0.4
        stats['low_scoring_rate'] = sum(1 for g in total_goals_per_game if g <= 1) / len(total_goals_per_game) if total_goals_per_game else 0.2
        stats['clean_sheet_rate'] = sum(1 for g in goals_conceded_per_game if g == 0) / len(goals_conceded_per_game) if goals_conceded_per_game else 0.2
        
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
            'avg_total_goals': 2.5, 'goals_variance': 1.0,
            'high_scoring_rate': 0.4, 'low_scoring_rate': 0.2, 'clean_sheet_rate': 0.2
        }
    
    def prepare_features(self, matches_df):
        """เตรียม features สำหรับการเทรน"""
        features = []
        result_labels = []
        home_goals_labels = []
        away_goals_labels = []
        total_goals_labels = []
        
        print("กำลังเตรียม features สำหรับการทำนายครบถ้วน...")
        
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
            
            # Goal-specific stats (14 features)
            for stat_name in ['home_avg_goals_for', 'away_avg_goals_for', 'avg_total_goals', 
                            'goals_variance', 'high_scoring_rate', 'low_scoring_rate', 'clean_sheet_rate']:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Relative features (6 features)
            feature_row.append(home_stats['avg_goals_for'] - away_stats['avg_goals_against'])
            feature_row.append(away_stats['avg_goals_for'] - home_stats['avg_goals_against'])
            feature_row.append(home_stats['avg_total_goals'] - away_stats['avg_total_goals'])
            feature_row.append(home_stats['high_scoring_rate'] - away_stats['high_scoring_rate'])
            feature_row.append(home_stats['clean_sheet_rate'] - away_stats['clean_sheet_rate'])
            feature_row.append(1.0)  # home advantage
            
            # ตรวจสอบ NaN/Inf
            feature_row = [0.0 if pd.isna(x) or np.isinf(x) else float(x) for x in feature_row]
            features.append(feature_row)
            
            # Labels
            home_goals = int(match['home_goals']) if pd.notna(match['home_goals']) else 0
            away_goals = int(match['away_goals']) if pd.notna(match['away_goals']) else 0
            total_goals = home_goals + away_goals
            
            # Result label
            if home_goals > away_goals:
                result_labels.append(2)  # home win
            elif home_goals < away_goals:
                result_labels.append(0)  # away win
            else:
                result_labels.append(1)  # draw
            
            home_goals_labels.append(home_goals)
            away_goals_labels.append(away_goals)
            total_goals_labels.append(total_goals)
        
        self.feature_columns = [
            'home_win_rate', 'away_win_rate', 'home_draw_rate', 'away_draw_rate',
            'home_loss_rate', 'away_loss_rate', 'home_avg_goals_for', 'away_avg_goals_for',
            'home_avg_goals_against', 'away_avg_goals_against', 'home_goal_diff', 'away_goal_diff',
            'home_home_goals_for', 'away_home_goals_for', 'home_away_goals_for', 'away_away_goals_for',
            'home_avg_total_goals', 'away_avg_total_goals', 'home_goals_variance', 'away_goals_variance',
            'home_high_scoring_rate', 'away_high_scoring_rate', 'home_low_scoring_rate', 'away_low_scoring_rate',
            'home_clean_sheet_rate', 'away_clean_sheet_rate',
            'home_attack_vs_away_defense', 'away_attack_vs_home_defense', 'total_goals_diff',
            'high_scoring_diff', 'clean_sheet_diff', 'home_advantage'
        ]
        
        print(f"เตรียม features สำเร็จ: {len(features)} samples, {len(self.feature_columns)} features")
        
        return (np.array(features), np.array(result_labels), 
                np.array(home_goals_labels), np.array(away_goals_labels), 
                np.array(total_goals_labels))
    
    def train(self, matches_df):
        """เทรนโมเดลทั้งหมด"""
        print("กำลังเทรนโมเดลครบถ้วน...")
        
        X, y_result, y_home_goals, y_away_goals, y_total_goals = self.prepare_features(matches_df)
        
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
        
        _, _, y_home_train, y_home_test = train_test_split(
            X_scaled, y_home_goals, test_size=0.2, random_state=42
        )
        
        _, _, y_away_train, y_away_test = train_test_split(
            X_scaled, y_away_goals, test_size=0.2, random_state=42
        )
        
        _, _, y_total_train, y_total_test = train_test_split(
            X_scaled, y_total_goals, test_size=0.2, random_state=42
        )
        
        # เทรนโมเดลผลการแข่งขัน
        print("1. เทรนโมเดลทำนายผลการแข่งขัน...")
        self.result_model.fit(X_train, y_result_train)
        result_pred = self.result_model.predict(X_test)
        result_accuracy = accuracy_score(y_result_test, result_pred)
        
        # เทรนโมเดลประตูทีมเหย้า
        print("2. เทรนโมเดลทำนายประตูทีมเหย้า...")
        self.home_goals_model.fit(X_train, y_home_train)
        home_pred = self.home_goals_model.predict(X_test)
        home_mae = mean_absolute_error(y_home_test, home_pred)
        
        # เทรนโมเดลประตูทีมเยือน
        print("3. เทรนโมเดลทำนายประตูทีมเยือน...")
        self.away_goals_model.fit(X_train, y_away_train)
        away_pred = self.away_goals_model.predict(X_test)
        away_mae = mean_absolute_error(y_away_test, away_pred)
        
        # เทรนโมเดลประตูรวม
        print("4. เทรนโมเดลทำนายประตูรวม...")
        self.total_goals_model.fit(X_train, y_total_train)
        total_pred = self.total_goals_model.predict(X_test)
        total_mae = mean_absolute_error(y_total_test, total_pred)
        
        print(f"\n📊 ผลการเทรน:")
        print(f"   ความแม่นยำผลการแข่งขัน: {result_accuracy:.3f} ({result_accuracy*100:.1f}%)")
        print(f"   MAE ประตูทีมเหย้า: {home_mae:.3f}")
        print(f"   MAE ประตูทีมเยือน: {away_mae:.3f}")
        print(f"   MAE ประตูรวม: {total_mae:.3f}")
        
        self.is_trained = True
        return True
    
    def predict_comprehensive(self, home_team, away_team, matches_df):
        """ทำนายครบถ้วน"""
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
            
            # Goal-specific stats
            for stat_name in ['home_avg_goals_for', 'away_avg_goals_for', 'avg_total_goals', 
                            'goals_variance', 'high_scoring_rate', 'low_scoring_rate', 'clean_sheet_rate']:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # Relative features
            feature_row.extend([
                home_stats['avg_goals_for'] - away_stats['avg_goals_against'],
                away_stats['avg_goals_for'] - home_stats['avg_goals_against'],
                home_stats['avg_total_goals'] - away_stats['avg_total_goals'],
                home_stats['high_scoring_rate'] - away_stats['high_scoring_rate'],
                home_stats['clean_sheet_rate'] - away_stats['clean_sheet_rate'],
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
            
            home_goals_pred = max(0, round(self.home_goals_model.predict(feature_scaled)[0]))
            away_goals_pred = max(0, round(self.away_goals_model.predict(feature_scaled)[0]))
            total_goals_pred = self.total_goals_model.predict(feature_scaled)[0]
            
            # แปลงผลลัพธ์
            result_map = {0: 'Away Win', 1: 'Draw', 2: 'Home Win'}
            predicted_result = result_map[result_pred]
            
            # คำนวณผลต่างประตู
            goal_difference = home_goals_pred - away_goals_pred
            
            # ทำนายสูง/ต่ำ (เกณฑ์ 2.5 ประตู)
            over_under_threshold = 2.5
            over_under = "Over" if total_goals_pred > over_under_threshold else "Under"
            
            return {
                'match': f"{home_team} vs {away_team}",
                'result_prediction': predicted_result,
                'result_confidence': max(result_proba),
                'result_probabilities': {
                    'Away Win': result_proba[0],
                    'Draw': result_proba[1],
                    'Home Win': result_proba[2]
                },
                'predicted_score': f"{home_goals_pred}-{away_goals_pred}",
                'home_goals': home_goals_pred,
                'away_goals': away_goals_pred,
                'goal_difference': goal_difference,
                'total_goals': round(total_goals_pred, 1),
                'over_under_2_5': over_under,
                'over_under_confidence': abs(total_goals_pred - over_under_threshold)
            }
            
        except Exception as e:
            print(f"Error in comprehensive prediction: {e}")
            return None
    
    def evaluate_comprehensive_predictions(self, matches_df, test_games=50):
        """ประเมินการทำนายครบถ้วน"""
        print(f"\n🔍 การประเมินการทำนายครบถ้วน ({test_games} เกม)")
        print("="*80)
        
        if len(matches_df) < test_games + 100:
            print("ข้อมูลไม่เพียงพอ")
            return None
        
        # แบ่งข้อมูล
        train_data = matches_df.iloc[:-test_games]
        test_data = matches_df.iloc[-test_games:]
        
        # เทรนโมเดลใหม่
        temp_predictor = ComprehensiveFootballPredictor()
        if not temp_predictor.train(train_data):
            return None
        
        # ทดสอบ
        results = []
        result_correct = score_correct = over_under_correct = goal_diff_correct = 0
        
        print(f"{'No.':<3} {'Match':<35} {'Actual':<8} {'Pred':<8} {'Score':<8} {'O/U':<5} {'R':<2} {'S':<2} {'O':<2} {'G':<2}")
        print("-" * 80)
        
        for idx, (_, match) in enumerate(test_data.iterrows(), 1):
            # ผลจริง
            actual_home = int(match['home_goals'])
            actual_away = int(match['away_goals'])
            actual_total = actual_home + actual_away
            actual_diff = actual_home - actual_away
            
            if actual_home > actual_away:
                actual_result = 'Home Win'
            elif actual_home < actual_away:
                actual_result = 'Away Win'
            else:
                actual_result = 'Draw'
            
            actual_over_under = "Over" if actual_total > 2.5 else "Under"
            
            # ทำนาย
            prediction = temp_predictor.predict_comprehensive(
                match['home_team'], match['away_team'], train_data
            )
            
            if prediction:
                # ตรวจสอบความถูกต้อง
                result_match = prediction['result_prediction'] == actual_result
                score_match = (prediction['home_goals'] == actual_home and 
                             prediction['away_goals'] == actual_away)
                over_under_match = prediction['over_under_2_5'] == actual_over_under
                goal_diff_match = abs(prediction['goal_difference'] - actual_diff) <= 1
                
                if result_match: result_correct += 1
                if score_match: score_correct += 1
                if over_under_match: over_under_correct += 1
                if goal_diff_match: goal_diff_correct += 1
                
                # แสดงผล
                home_short = match['home_team'].replace(' FC', '')[:15]
                away_short = match['away_team'].replace(' FC', '')[:15]
                match_str = f"{home_short} vs {away_short}"
                
                actual_score = f"{actual_home}-{actual_away}"
                pred_result_short = prediction['result_prediction'][0] if prediction['result_prediction'] != 'Draw' else 'D'
                
                r_status = "✅" if result_match else "❌"
                s_status = "✅" if score_match else "❌"
                o_status = "✅" if over_under_match else "❌"
                g_status = "✅" if goal_diff_match else "❌"
                
                print(f"{idx:<3} {match_str:<35} {actual_score:<8} {pred_result_short:<8} "
                      f"{prediction['predicted_score']:<8} {prediction['over_under_2_5']:<5} "
                      f"{r_status:<2} {s_status:<2} {o_status:<2} {g_status:<2}")
                
                results.append({
                    'result_correct': result_match,
                    'score_correct': score_match,
                    'over_under_correct': over_under_match,
                    'goal_diff_correct': goal_diff_match
                })
        
        # สรุปผล
        total_tests = len(results)
        result_accuracy = result_correct / total_tests
        score_accuracy = score_correct / total_tests
        over_under_accuracy = over_under_correct / total_tests
        goal_diff_accuracy = goal_diff_correct / total_tests
        
        print("\n" + "="*80)
        print(f"📊 สรุปผลการประเมิน ({total_tests} เกม):")
        print(f"   🎯 ทำนายผลการแข่งขัน: {result_correct}/{total_tests} = {result_accuracy:.3f} ({result_accuracy*100:.1f}%)")
        print(f"   ⚽ ทำนายสกอร์แน่นอน: {score_correct}/{total_tests} = {score_accuracy:.3f} ({score_accuracy*100:.1f}%)")
        print(f"   📈 ทำนายสูง/ต่ำ 2.5: {over_under_correct}/{total_tests} = {over_under_accuracy:.3f} ({over_under_accuracy*100:.1f}%)")
        print(f"   📊 ทำนายผลต่างประตู: {goal_diff_correct}/{total_tests} = {goal_diff_accuracy:.3f} ({goal_diff_accuracy*100:.1f}%)")
        
        return {
            'result_accuracy': result_accuracy,
            'score_accuracy': score_accuracy,
            'over_under_accuracy': over_under_accuracy,
            'goal_diff_accuracy': goal_diff_accuracy,
            'total_tests': total_tests,
            'results': results
        }

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    print("=== ระบบทำนายฟุตบอลครบถ้วน ===")
    
    try:
        # โหลดข้อมูล
        matches_df = pd.read_csv('/Users/80090/Desktop/Project/untitle/sample_matches.csv')
        matches_df['date'] = pd.to_datetime(matches_df['date'])
        
        predictor = ComprehensiveFootballPredictor()
        
        if predictor.train(matches_df):
            # ทำนายตัวอย่าง
            result = predictor.predict_comprehensive('Arsenal', 'Chelsea', matches_df)
            if result:
                print(f"\n=== การทำนายครบถ้วน ===")
                print(f"🏆 {result['match']}")
                print(f"   ผลการแข่งขัน: {result['result_prediction']} (มั่นใจ {result['result_confidence']:.3f})")
                print(f"   สกอร์ที่คาด: {result['predicted_score']}")
                print(f"   ประตูรวม: {result['total_goals']} ({result['over_under_2_5']})")
                print(f"   ผลต่างประตู: {result['goal_difference']}")
            
            # ประเมินผล
            evaluation = predictor.evaluate_comprehensive_predictions(matches_df, test_games=30)
            
    except FileNotFoundError:
        print("ไม่พบไฟล์ข้อมูล")
