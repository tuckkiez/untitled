#!/usr/bin/env python3
"""
Argentina Primera Division Predictor
ระบบทำนายสำหรับ Argentina Primera Division พร้อม Backtest 20 นัด
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class ArgentinaPredictor:
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.team_stats = {}
        self.league_name = "Argentina Primera Division"
        
    def load_data(self, filename='argentina_sample_data.json'):
        """โหลดข้อมูล Argentina"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ Loaded {len(data['matches'])} matches from {filename}")
            return data
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def calculate_team_stats(self, matches):
        """คำนวณสถิติทีม"""
        stats = {}
        
        for match in matches:
            home_team = match['home_team']
            away_team = match['away_team']
            
            # Initialize team stats
            for team in [home_team, away_team]:
                if team not in stats:
                    stats[team] = {
                        'matches': 0,
                        'wins': 0,
                        'draws': 0,
                        'losses': 0,
                        'goals_for': 0,
                        'goals_against': 0,
                        'corners_for': 0,
                        'corners_against': 0,
                        'home_matches': 0,
                        'away_matches': 0,
                        'home_wins': 0,
                        'away_wins': 0
                    }
            
            # Update stats
            home_score = match['home_score']
            away_score = match['away_score']
            result = match['result']
            
            # Home team stats
            stats[home_team]['matches'] += 1
            stats[home_team]['home_matches'] += 1
            stats[home_team]['goals_for'] += home_score
            stats[home_team]['goals_against'] += away_score
            stats[home_team]['corners_for'] += match['corners_home']
            stats[home_team]['corners_against'] += match['corners_away']
            
            if result == 'Home Win':
                stats[home_team]['wins'] += 1
                stats[home_team]['home_wins'] += 1
                stats[away_team]['losses'] += 1
            elif result == 'Away Win':
                stats[home_team]['losses'] += 1
                stats[away_team]['wins'] += 1
                stats[away_team]['away_wins'] += 1
            else:
                stats[home_team]['draws'] += 1
                stats[away_team]['draws'] += 1
            
            # Away team stats
            stats[away_team]['matches'] += 1
            stats[away_team]['away_matches'] += 1
            stats[away_team]['goals_for'] += away_score
            stats[away_team]['goals_against'] += home_score
            stats[away_team]['corners_for'] += match['corners_away']
            stats[away_team]['corners_against'] += match['corners_home']
        
        # Calculate derived stats
        for team in stats:
            s = stats[team]
            if s['matches'] > 0:
                s['win_rate'] = s['wins'] / s['matches']
                s['goals_per_match'] = s['goals_for'] / s['matches']
                s['goals_conceded_per_match'] = s['goals_against'] / s['matches']
                s['corners_per_match'] = s['corners_for'] / s['matches']
                s['goal_difference'] = s['goals_for'] - s['goals_against']
                
                if s['home_matches'] > 0:
                    s['home_win_rate'] = s['home_wins'] / s['home_matches']
                else:
                    s['home_win_rate'] = 0
                    
                if s['away_matches'] > 0:
                    s['away_win_rate'] = s['away_wins'] / s['away_matches']
                else:
                    s['away_win_rate'] = 0
        
        return stats
    
    def create_features(self, home_team, away_team, stats):
        """สร้าง features สำหรับการทำนาย"""
        home_stats = stats.get(home_team, {})
        away_stats = stats.get(away_team, {})
        
        features = {
            # Home team features
            'home_win_rate': home_stats.get('win_rate', 0.5),
            'home_goals_per_match': home_stats.get('goals_per_match', 1.0),
            'home_goals_conceded': home_stats.get('goals_conceded_per_match', 1.0),
            'home_corners_per_match': home_stats.get('corners_per_match', 5.0),
            'home_goal_difference': home_stats.get('goal_difference', 0),
            'home_advantage': home_stats.get('home_win_rate', 0.5),
            
            # Away team features
            'away_win_rate': away_stats.get('win_rate', 0.5),
            'away_goals_per_match': away_stats.get('goals_per_match', 1.0),
            'away_goals_conceded': away_stats.get('goals_conceded_per_match', 1.0),
            'away_corners_per_match': away_stats.get('corners_per_match', 5.0),
            'away_goal_difference': away_stats.get('goal_difference', 0),
            'away_form': away_stats.get('away_win_rate', 0.3),
            
            # Head-to-head features
            'win_rate_diff': home_stats.get('win_rate', 0.5) - away_stats.get('win_rate', 0.5),
            'goals_diff': home_stats.get('goals_per_match', 1.0) - away_stats.get('goals_per_match', 1.0),
            'defense_diff': away_stats.get('goals_conceded_per_match', 1.0) - home_stats.get('goals_conceded_per_match', 1.0),
            
            # Combined features
            'total_goals_expected': home_stats.get('goals_per_match', 1.0) + away_stats.get('goals_per_match', 1.0),
            'total_corners_expected': home_stats.get('corners_per_match', 5.0) + away_stats.get('corners_per_match', 5.0),
        }
        
        return features
    
    def prepare_training_data(self, matches, stats):
        """เตรียมข้อมูลสำหรับเทรน"""
        X = []
        y_result = []
        y_over_under = []
        y_corners = []
        
        for match in matches:
            features = self.create_features(match['home_team'], match['away_team'], stats)
            X.append(list(features.values()))
            
            # Labels
            if match['result'] == 'Home Win':
                y_result.append(0)
            elif match['result'] == 'Draw':
                y_result.append(1)
            else:
                y_result.append(2)
            
            y_over_under.append(1 if match['total_goals'] > 2.5 else 0)
            y_corners.append(1 if match['total_corners'] > 9.5 else 0)
        
        return np.array(X), np.array(y_result), np.array(y_over_under), np.array(y_corners)
    
    def train_models(self, X, y_result, y_over_under, y_corners):
        """เทรนโมเดล"""
        print("🧠 Training models...")
        
        # Result prediction models
        self.models['result_rf'] = RandomForestClassifier(n_estimators=100, random_state=42)
        self.models['result_gb'] = GradientBoostingClassifier(random_state=42)
        self.models['result_lr'] = LogisticRegression(random_state=42, max_iter=1000)
        
        # Over/Under models
        self.models['over_under_rf'] = RandomForestClassifier(n_estimators=100, random_state=42)
        self.models['over_under_gb'] = GradientBoostingClassifier(random_state=42)
        
        # Corners models
        self.models['corners_rf'] = RandomForestClassifier(n_estimators=100, random_state=42)
        self.models['corners_gb'] = GradientBoostingClassifier(random_state=42)
        
        # Train all models
        for name, model in self.models.items():
            if 'result' in name:
                model.fit(X, y_result)
            elif 'over_under' in name:
                model.fit(X, y_over_under)
            elif 'corners' in name:
                model.fit(X, y_corners)
        
        print("✅ Models trained successfully")
    
    def predict_match(self, home_team, away_team, stats):
        """ทำนายการแข่งขัน"""
        features = self.create_features(home_team, away_team, stats)
        X = np.array([list(features.values())])
        
        # Result prediction (ensemble)
        result_probs = []
        for model_name in ['result_rf', 'result_gb', 'result_lr']:
            probs = self.models[model_name].predict_proba(X)[0]
            result_probs.append(probs)
        
        avg_result_probs = np.mean(result_probs, axis=0)
        result_pred = np.argmax(avg_result_probs)
        result_confidence = np.max(avg_result_probs) * 100
        
        # Over/Under prediction
        over_under_probs = []
        for model_name in ['over_under_rf', 'over_under_gb']:
            prob = self.models[model_name].predict_proba(X)[0][1]
            over_under_probs.append(prob)
        
        over_under_prob = np.mean(over_under_probs)
        over_under_pred = 'Over 2.5' if over_under_prob > 0.5 else 'Under 2.5'
        over_under_confidence = max(over_under_prob, 1 - over_under_prob) * 100
        
        # Corners prediction
        corners_probs = []
        for model_name in ['corners_rf', 'corners_gb']:
            prob = self.models[model_name].predict_proba(X)[0][1]
            corners_probs.append(prob)
        
        corners_prob = np.mean(corners_probs)
        corners_pred = 'Over 9.5' if corners_prob > 0.5 else 'Under 9.5'
        corners_confidence = max(corners_prob, 1 - corners_prob) * 100
        
        # Result mapping
        result_map = {0: 'Home Win', 1: 'Draw', 2: 'Away Win'}
        
        return {
            'match_result': {
                'prediction': result_map[result_pred],
                'confidence': result_confidence
            },
            'over_under': {
                'prediction': over_under_pred,
                'confidence': over_under_confidence
            },
            'corners': {
                'prediction': corners_pred,
                'confidence': corners_confidence
            },
            'expected_goals': features['total_goals_expected'],
            'expected_corners': features['total_corners_expected']
        }
    
    def backtest_20_matches(self, data):
        """ทดสอบย้อนหลัง 20 นัด"""
        print(f"\n🧪 Running 20-match backtest for {self.league_name}")
        print("=" * 60)
        
        matches = data['matches']
        
        # แบ่งข้อมูล: ใช้ 15 นัดแรกเทรน, 5 นัดหลังทดสอบ
        train_matches = matches[:15]
        test_matches = matches[15:20]
        
        # คำนวณสถิติจากข้อมูลเทรน
        stats = self.calculate_team_stats(train_matches)
        
        # เตรียมข้อมูลเทรน
        X_train, y_result_train, y_over_under_train, y_corners_train = self.prepare_training_data(train_matches, stats)
        
        # เทรนโมเดล
        self.train_models(X_train, y_result_train, y_over_under_train, y_corners_train)
        
        # ทดสอบ
        results = []
        correct_results = 0
        correct_over_under = 0
        correct_corners = 0
        
        print(f"📊 Backtest Results:")
        print("-" * 60)
        
        for i, match in enumerate(test_matches):
            prediction = self.predict_match(match['home_team'], match['away_team'], stats)
            
            # ตรวจสอบความถูกต้อง
            result_correct = prediction['match_result']['prediction'] == match['result']
            over_under_correct = (
                (prediction['over_under']['prediction'] == 'Over 2.5' and match['total_goals'] > 2.5) or
                (prediction['over_under']['prediction'] == 'Under 2.5' and match['total_goals'] <= 2.5)
            )
            corners_correct = (
                (prediction['corners']['prediction'] == 'Over 9.5' and match['total_corners'] > 9.5) or
                (prediction['corners']['prediction'] == 'Under 9.5' and match['total_corners'] <= 9.5)
            )
            
            if result_correct:
                correct_results += 1
            if over_under_correct:
                correct_over_under += 1
            if corners_correct:
                correct_corners += 1
            
            # แสดงผล
            print(f"{i+1}. {match['home_team']} vs {match['away_team']}")
            print(f"   Actual: {match['result']} ({match['home_score']}-{match['away_score']}, Goals: {match['total_goals']}, Corners: {match['total_corners']})")
            print(f"   Predicted: {prediction['match_result']['prediction']} ({prediction['match_result']['confidence']:.1f}%)")
            print(f"   Over/Under: {prediction['over_under']['prediction']} ({prediction['over_under']['confidence']:.1f}%) {'✅' if over_under_correct else '❌'}")
            print(f"   Corners: {prediction['corners']['prediction']} ({prediction['corners']['confidence']:.1f}%) {'✅' if corners_correct else '❌'}")
            print(f"   Result: {'✅ CORRECT' if result_correct else '❌ WRONG'}")
            print()
            
            results.append({
                'match': f"{match['home_team']} vs {match['away_team']}",
                'actual_result': match['result'],
                'predicted_result': prediction['match_result']['prediction'],
                'result_correct': result_correct,
                'result_confidence': prediction['match_result']['confidence'],
                'over_under_correct': over_under_correct,
                'corners_correct': corners_correct
            })
        
        # สรุปผล
        total_matches = len(test_matches)
        result_accuracy = (correct_results / total_matches) * 100
        over_under_accuracy = (correct_over_under / total_matches) * 100
        corners_accuracy = (correct_corners / total_matches) * 100
        
        print("📈 BACKTEST SUMMARY")
        print("=" * 60)
        print(f"🎯 Match Result Accuracy: {correct_results}/{total_matches} ({result_accuracy:.1f}%)")
        print(f"⚽ Over/Under Accuracy: {correct_over_under}/{total_matches} ({over_under_accuracy:.1f}%)")
        print(f"🚩 Corners Accuracy: {correct_corners}/{total_matches} ({corners_accuracy:.1f}%)")
        print(f"📊 Overall Performance: {(result_accuracy + over_under_accuracy + corners_accuracy)/3:.1f}%")
        
        return {
            'results': results,
            'accuracy': {
                'match_result': result_accuracy,
                'over_under': over_under_accuracy,
                'corners': corners_accuracy,
                'overall': (result_accuracy + over_under_accuracy + corners_accuracy) / 3
            }
        }
    
    def predict_todays_matches(self, data):
        """ทำนายแมทช์วันนี้"""
        print(f"\n🔮 Today's Predictions for {self.league_name}")
        print("=" * 60)
        
        # ใช้ข้อมูลทั้งหมดเพื่อคำนวณสถิติ
        stats = self.calculate_team_stats(data['matches'])
        X, y_result, y_over_under, y_corners = self.prepare_training_data(data['matches'], stats)
        self.train_models(X, y_result, y_over_under, y_corners)
        
        # แมทช์ตัวอย่างสำหรับวันนี้
        todays_matches = [
            {'home_team': 'River Plate', 'away_team': 'Boca Juniors', 'time': '01:30'},
            {'home_team': 'Racing Club', 'away_team': 'Independiente', 'time': '06:00'}
        ]
        
        predictions = []
        
        for i, match in enumerate(todays_matches):
            prediction = self.predict_match(match['home_team'], match['away_team'], stats)
            
            print(f"{i+1}. {match['home_team']} vs {match['away_team']} ({match['time']})")
            print(f"   🏆 Result: {prediction['match_result']['prediction']} ({prediction['match_result']['confidence']:.1f}%)")
            print(f"   ⚽ Goals: {prediction['over_under']['prediction']} ({prediction['over_under']['confidence']:.1f}%)")
            print(f"   🚩 Corners: {prediction['corners']['prediction']} ({prediction['corners']['confidence']:.1f}%)")
            print(f"   📊 Expected: {prediction['expected_goals']:.1f} goals, {prediction['expected_corners']:.1f} corners")
            
            # แสดงระดับความมั่นใจ
            avg_confidence = (prediction['match_result']['confidence'] + 
                            prediction['over_under']['confidence'] + 
                            prediction['corners']['confidence']) / 3
            
            if avg_confidence >= 75:
                confidence_level = "🔥 HIGH CONFIDENCE"
            elif avg_confidence >= 60:
                confidence_level = "⭐ GOOD CONFIDENCE"
            else:
                confidence_level = "⚠️ LOW CONFIDENCE"
            
            print(f"   {confidence_level} (Avg: {avg_confidence:.1f}%)")
            print()
            
            predictions.append({
                'match': f"{match['home_team']} vs {match['away_team']}",
                'time': match['time'],
                'predictions': prediction,
                'confidence_level': confidence_level,
                'avg_confidence': avg_confidence
            })
        
        return predictions

def main():
    print("🇦🇷 Argentina Primera Division Predictor")
    print("=" * 60)
    
    predictor = ArgentinaPredictor()
    
    # โหลดข้อมูล
    data = predictor.load_data('argentina_sample_data.json')
    if not data:
        print("❌ No data available")
        return
    
    # รัน backtest 20 นัด
    backtest_results = predictor.backtest_20_matches(data)
    
    # ทำนายแมทช์วันนี้
    todays_predictions = predictor.predict_todays_matches(data)
    
    print("\n🎯 FINAL SUMMARY")
    print("=" * 60)
    print(f"✅ Backtest completed with {backtest_results['accuracy']['overall']:.1f}% overall accuracy")
    print(f"🔮 {len(todays_predictions)} predictions made for tonight's matches")
    print(f"📊 System ready for real-time testing!")

if __name__ == "__main__":
    main()
