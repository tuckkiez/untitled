#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Corner Kicks Predictor - ระบบทำนายเตะมุม
- ทำนายจำนวนเตะมุมครึ่งแรก (เส้น 6)
- ทำนายจำนวนเตะมุมครึ่งหลัง (เส้น 6)  
- ทำนายจำนวนเตะมุมทั้งเกม (เส้น 12)
- ทำนายเตะมุมแต่ละทีม
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class CornerPredictor:
    def __init__(self):
        # โมเดลสำหรับทำนายเตะมุม
        self.models = {
            'total_corners': RandomForestRegressor(n_estimators=200, random_state=42),
            'first_half_corners': RandomForestRegressor(n_estimators=200, random_state=42),
            'second_half_corners': RandomForestRegressor(n_estimators=200, random_state=42),
            'home_corners': RandomForestRegressor(n_estimators=200, random_state=42),
            'away_corners': RandomForestRegressor(n_estimators=200, random_state=42)
        }
        
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_columns = []
        
        # สถิติเตะมุมเฉลี่ยของแต่ละทีม (จำลอง)
        self.team_corner_stats = {
            'Manchester City': {'avg_for': 6.8, 'avg_against': 3.2, 'home_boost': 1.2},
            'Arsenal': {'avg_for': 6.5, 'avg_against': 3.5, 'home_boost': 1.1},
            'Liverpool': {'avg_for': 6.9, 'avg_against': 3.8, 'home_boost': 1.3},
            'Chelsea': {'avg_for': 6.2, 'avg_against': 4.1, 'home_boost': 1.0},
            'Manchester United': {'avg_for': 5.8, 'avg_against': 4.5, 'home_boost': 0.9},
            'Tottenham': {'avg_for': 6.1, 'avg_against': 4.2, 'home_boost': 1.1},
            'Newcastle': {'avg_for': 5.5, 'avg_against': 4.8, 'home_boost': 1.0},
            'Brighton': {'avg_for': 5.9, 'avg_against': 4.6, 'home_boost': 0.8},
            'Aston Villa': {'avg_for': 5.7, 'avg_against': 4.7, 'home_boost': 0.9},
            'West Ham': {'avg_for': 5.3, 'avg_against': 5.1, 'home_boost': 0.8},
            'Crystal Palace': {'avg_for': 4.8, 'avg_against': 5.5, 'home_boost': 0.7},
            'Fulham': {'avg_for': 5.1, 'avg_against': 5.2, 'home_boost': 0.8},
            'Brentford': {'avg_for': 4.9, 'avg_against': 5.4, 'home_boost': 0.7},
            'Wolves': {'avg_for': 4.6, 'avg_against': 5.6, 'home_boost': 0.6},
            'Everton': {'avg_for': 4.4, 'avg_against': 5.8, 'home_boost': 0.6},
            'Nottingham Forest': {'avg_for': 4.2, 'avg_against': 6.1, 'home_boost': 0.5},
            'Leicester': {'avg_for': 4.5, 'avg_against': 5.9, 'home_boost': 0.6},
            'Southampton': {'avg_for': 4.1, 'avg_against': 6.3, 'home_boost': 0.5},
            'Ipswich': {'avg_for': 3.8, 'avg_against': 6.8, 'home_boost': 0.4},
            'AFC Bournemouth': {'avg_for': 4.7, 'avg_against': 5.7, 'home_boost': 0.6}
        }
    
    def generate_corner_data(self, matches_df):
        """สร้างข้อมูลเตะมุมจำลองที่สมจริง"""
        corner_data = []
        
        for _, match in matches_df.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            
            # ดึงสถิติทีม
            home_stats = self.team_corner_stats.get(home_team, {'avg_for': 5.0, 'avg_against': 5.0, 'home_boost': 0.8})
            away_stats = self.team_corner_stats.get(away_team, {'avg_for': 5.0, 'avg_against': 5.0, 'home_boost': 0.8})
            
            # คำนวณเตะมุมที่คาดหวัง
            home_expected = (home_stats['avg_for'] + away_stats['avg_against']) / 2 * home_stats['home_boost']
            away_expected = (away_stats['avg_for'] + home_stats['avg_against']) / 2 * 0.9  # away penalty
            
            # สร้างเตะมุมจำลอง
            home_corners = max(0, int(np.random.poisson(home_expected)))
            away_corners = max(0, int(np.random.poisson(away_expected)))
            total_corners = home_corners + away_corners
            
            # แบ่งครึ่งเวลา (ครึ่งแรกมักน้อยกว่า)
            first_half_ratio = np.random.uniform(0.4, 0.5)  # 40-50% ในครึ่งแรก
            first_half_corners = int(total_corners * first_half_ratio)
            second_half_corners = total_corners - first_half_corners
            
            corner_data.append({
                'home_team': home_team,
                'away_team': away_team,
                'date': match['date'],
                'home_goals': match['home_goals'],
                'away_goals': match['away_goals'],
                'home_corners': home_corners,
                'away_corners': away_corners,
                'total_corners': total_corners,
                'first_half_corners': first_half_corners,
                'second_half_corners': second_half_corners
            })
        
        return pd.DataFrame(corner_data)
    
    def create_corner_features(self, corner_data):
        """สร้าง features สำหรับทำนายเตะมุม"""
        features_list = []
        
        for idx, match in corner_data.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            
            # สถิติทีม
            home_stats = self.team_corner_stats.get(home_team, {'avg_for': 5.0, 'avg_against': 5.0, 'home_boost': 0.8})
            away_stats = self.team_corner_stats.get(away_team, {'avg_for': 5.0, 'avg_against': 5.0, 'home_boost': 0.8})
            
            # คำนวณฟอร์มล่าสุด (จำลอง)
            home_recent_corners = np.random.uniform(home_stats['avg_for'] * 0.8, home_stats['avg_for'] * 1.2)
            away_recent_corners = np.random.uniform(away_stats['avg_for'] * 0.8, away_stats['avg_for'] * 1.2)
            
            # ปัจจัยการเล่น
            match_date = pd.to_datetime(match['date'])
            is_weekend = 1 if match_date.weekday() >= 5 else 0
            month = match_date.month
            
            features = {
                # สถิติทีมเหย้า
                'home_avg_corners_for': home_stats['avg_for'],
                'home_avg_corners_against': home_stats['avg_against'],
                'home_boost': home_stats['home_boost'],
                'home_recent_form': home_recent_corners,
                
                # สถิติทีมเยือน
                'away_avg_corners_for': away_stats['avg_for'],
                'away_avg_corners_against': away_stats['avg_against'],
                'away_recent_form': away_recent_corners,
                
                # ความแตกต่าง
                'corner_strength_diff': home_stats['avg_for'] - away_stats['avg_for'],
                'defensive_diff': away_stats['avg_against'] - home_stats['avg_against'],
                
                # คาดการณ์เบื้องต้น
                'expected_home_corners': (home_stats['avg_for'] + away_stats['avg_against']) / 2,
                'expected_away_corners': (away_stats['avg_for'] + home_stats['avg_against']) / 2,
                'expected_total': ((home_stats['avg_for'] + away_stats['avg_against']) / 2) + 
                                ((away_stats['avg_for'] + home_stats['avg_against']) / 2),
                
                # ปัจจัยเวลา
                'is_weekend': is_weekend,
                'month': month,
                'is_winter': 1 if month in [12, 1, 2] else 0,
                
                # ปัจจัยการเล่น (จำลอง)
                'attacking_style_home': np.random.uniform(0.7, 1.3),
                'attacking_style_away': np.random.uniform(0.7, 1.3),
                'possession_tendency': np.random.uniform(0.8, 1.2),
                
                # Home advantage
                'home_advantage': 1.1,
            }
            
            features_list.append(features)
        
        features_df = pd.DataFrame(features_list)
        self.feature_columns = features_df.columns.tolist()
        
        return features_df
    
    def train_corner_models(self, corner_data):
        """เทรนโมเดลทำนายเตะมุม"""
        print("⚽ กำลังเทรนโมเดลทำนายเตะมุม...")
        
        # สร้าง features
        features_df = self.create_corner_features(corner_data)
        
        # เตรียมข้อมูล
        X = self.scaler.fit_transform(features_df)
        
        # เป้าหมายการทำนาย
        targets = {
            'total_corners': corner_data['total_corners'].values,
            'first_half_corners': corner_data['first_half_corners'].values,
            'second_half_corners': corner_data['second_half_corners'].values,
            'home_corners': corner_data['home_corners'].values,
            'away_corners': corner_data['away_corners'].values
        }
        
        # แบ่งข้อมูล
        X_train, X_test, _, _ = train_test_split(X, corner_data, test_size=0.2, random_state=42)
        
        model_scores = {}
        
        # เทรนแต่ละโมเดล
        for target_name, target_values in targets.items():
            y_train, y_test = train_test_split(target_values, test_size=0.2, random_state=42)
            
            # เทรนโมเดล
            model = self.models[target_name]
            model.fit(X_train, y_train)
            
            # ทดสอบ
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            model_scores[target_name] = {'mae': mae, 'rmse': rmse}
            
            print(f"   {target_name:20}: MAE={mae:.2f}, RMSE={rmse:.2f}")
        
        self.is_trained = True
        return model_scores
    
    def predict_corners(self, home_team, away_team, match_date=None):
        """ทำนายเตะมุมสำหรับการแข่งขัน"""
        if not self.is_trained:
            print("❌ โมเดลยังไม่ได้เทรน!")
            return None
        
        if not match_date:
            match_date = datetime.now()
        
        # สร้าง features
        dummy_data = pd.DataFrame([{
            'home_team': home_team,
            'away_team': away_team,
            'date': match_date,
            'home_goals': 0,
            'away_goals': 0
        }])
        
        features_df = self.create_corner_features(dummy_data)
        X = self.scaler.transform(features_df)
        
        # ทำนาย
        predictions = {}
        for target_name, model in self.models.items():
            pred_value = model.predict(X)[0]
            predictions[target_name] = max(0, round(pred_value))
        
        # คำนวณ Over/Under
        total_corners = predictions['total_corners']
        first_half = predictions['first_half_corners']
        second_half = predictions['second_half_corners']
        
        result = {
            'home_team': home_team,
            'away_team': away_team,
            'predictions': {
                'total_corners': total_corners,
                'first_half_corners': first_half,
                'second_half_corners': second_half,
                'home_corners': predictions['home_corners'],
                'away_corners': predictions['away_corners']
            },
            'over_under_analysis': {
                'total_12': 'Over' if total_corners > 12 else 'Under',
                'first_half_6': 'Over' if first_half > 6 else 'Under',
                'second_half_6': 'Over' if second_half > 6 else 'Under',
                'total_10': 'Over' if total_corners > 10 else 'Under',
                'total_8': 'Over' if total_corners > 8 else 'Under'
            },
            'confidence_scores': {
                'total_confidence': min(100, abs(total_corners - 12) * 10 + 50),
                'first_half_confidence': min(100, abs(first_half - 6) * 15 + 50),
                'second_half_confidence': min(100, abs(second_half - 6) * 15 + 50)
            }
        }
        
        return result
    
    def backtest_corners(self, corner_data, test_games=20):
        """ทดสอบการทำนายเตะมุมย้อนหลัง"""
        print("🎯 การทดสอบการทำนายเตะมุมย้อนหลัง")
        print("="*100)
        
        if len(corner_data) < test_games + 50:
            print(f"⚠️ ข้อมูลไม่เพียงพอ")
            return
        
        # แบ่งข้อมูล
        train_data = corner_data[:-test_games].copy()
        test_data = corner_data[-test_games:].copy()
        
        print(f"🎯 เทรนด้วย {len(train_data)} เกม, ทดสอบ {len(test_data)} เกม")
        
        # เทรนโมเดล
        self.train_corner_models(train_data)
        
        print(f"\n📋 รายละเอียดการทดสอบเตะมุม {test_games} เกมล่าสุด")
        print("="*100)
        print(f"{'No.':<3} {'Match':<35} {'Total':<6} {'1H':<4} {'2H':<4} {'T12':<4} {'1H6':<4} {'2H6':<4} {'Score':<6}")
        print("-"*100)
        
        results = []
        correct_total_12 = 0
        correct_first_half_6 = 0
        correct_second_half_6 = 0
        
        for idx, (_, match) in enumerate(test_data.iterrows(), 1):
            # ทำนาย
            prediction = self.predict_corners(
                match['home_team'],
                match['away_team'],
                match['date']
            )
            
            if not prediction:
                continue
            
            # ผลจริง
            actual_total = match['total_corners']
            actual_1h = match['first_half_corners']
            actual_2h = match['second_half_corners']
            
            # ผลการทำนาย
            pred_total = prediction['predictions']['total_corners']
            pred_1h = prediction['predictions']['first_half_corners']
            pred_2h = prediction['predictions']['second_half_corners']
            
            # Over/Under จริง
            actual_total_12 = 'Over' if actual_total > 12 else 'Under'
            actual_1h_6 = 'Over' if actual_1h > 6 else 'Under'
            actual_2h_6 = 'Over' if actual_2h > 6 else 'Under'
            
            # Over/Under ทำนาย
            pred_total_12 = prediction['over_under_analysis']['total_12']
            pred_1h_6 = prediction['over_under_analysis']['first_half_6']
            pred_2h_6 = prediction['over_under_analysis']['second_half_6']
            
            # ตรวจสอบความถูกต้อง
            total_12_correct = pred_total_12 == actual_total_12
            first_half_6_correct = pred_1h_6 == actual_1h_6
            second_half_6_correct = pred_2h_6 == actual_2h_6
            
            if total_12_correct:
                correct_total_12 += 1
            if first_half_6_correct:
                correct_first_half_6 += 1
            if second_half_6_correct:
                correct_second_half_6 += 1
            
            # สัญลักษณ์
            t12_symbol = "✅" if total_12_correct else "❌"
            h1_symbol = "✅" if first_half_6_correct else "❌"
            h2_symbol = "✅" if second_half_6_correct else "❌"
            
            # คะแนนรวม
            score = sum([total_12_correct, first_half_6_correct, second_half_6_correct])
            
            # แสดงผล
            match_str = f"{match['home_team'][:15]} vs {match['away_team'][:15]}"
            total_str = f"{actual_total}({pred_total})"
            h1_str = f"{actual_1h}({pred_1h})"
            h2_str = f"{actual_2h}({pred_2h})"
            
            print(f"{idx:<3} {match_str:<35} {total_str:<6} {h1_str:<4} {h2_str:<4} "
                  f"{t12_symbol:<4} {h1_symbol:<4} {h2_symbol:<4} {score}/3")
            
            # เก็บข้อมูล
            results.append({
                'match_num': idx,
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'actual_total': actual_total,
                'actual_1h': actual_1h,
                'actual_2h': actual_2h,
                'pred_total': pred_total,
                'pred_1h': pred_1h,
                'pred_2h': pred_2h,
                'total_12_correct': total_12_correct,
                'first_half_6_correct': first_half_6_correct,
                'second_half_6_correct': second_half_6_correct,
                'score': score
            })
        
        # สรุปผลลัพธ์
        self.analyze_corner_results(results, correct_total_12, correct_first_half_6, 
                                  correct_second_half_6, len(results))
        
        return results
    
    def analyze_corner_results(self, results, correct_total_12, correct_first_half_6, 
                             correct_second_half_6, total_games):
        """วิเคราะห์ผลการทำนายเตะมุม"""
        print("\n" + "="*100)
        print("📊 สรุปผลการทำนายเตะมุม")
        print("="*100)
        
        # ความแม่นยำแต่ละประเภท
        total_12_accuracy = correct_total_12 / total_games
        first_half_6_accuracy = correct_first_half_6 / total_games
        second_half_6_accuracy = correct_second_half_6 / total_games
        
        print(f"🎯 ความแม่นยำการทำนาย:")
        print(f"   เตะมุมรวม >12:        {correct_total_12}/{total_games} = {total_12_accuracy:.1%}")
        print(f"   ครึ่งแรก >6:          {correct_first_half_6}/{total_games} = {first_half_6_accuracy:.1%}")
        print(f"   ครึ่งหลัง >6:         {correct_second_half_6}/{total_games} = {second_half_6_accuracy:.1%}")
        
        # คะแนนรวม
        perfect_scores = sum(1 for r in results if r['score'] == 3)
        good_scores = sum(1 for r in results if r['score'] >= 2)
        
        print(f"\n🏆 ผลลัพธ์รวม:")
        print(f"   ถูกทั้ง 3 ค่า:        {perfect_scores}/{total_games} = {perfect_scores/total_games:.1%}")
        print(f"   ถูกอย่างน้อย 2 ค่า:   {good_scores}/{total_games} = {good_scores/total_games:.1%}")
        
        # สถิติเตะมุม
        avg_total = np.mean([r['actual_total'] for r in results])
        avg_1h = np.mean([r['actual_1h'] for r in results])
        avg_2h = np.mean([r['actual_2h'] for r in results])
        
        print(f"\n📊 สถิติเตะมุมเฉลี่ย:")
        print(f"   เตะมุมรวม: {avg_total:.1f} ครั้ง/เกม")
        print(f"   ครึ่งแรก: {avg_1h:.1f} ครั้ง/เกม")
        print(f"   ครึ่งหลัง: {avg_2h:.1f} ครั้ง/เกม")
        
        # การกระจายเตะมุม
        over_12_games = sum(1 for r in results if r['actual_total'] > 12)
        over_6_1h_games = sum(1 for r in results if r['actual_1h'] > 6)
        over_6_2h_games = sum(1 for r in results if r['actual_2h'] > 6)
        
        print(f"\n📈 การกระจายเตะมุม:")
        print(f"   เกม >12 เตะมุม: {over_12_games}/{total_games} = {over_12_games/total_games:.1%}")
        print(f"   ครึ่งแรก >6: {over_6_1h_games}/{total_games} = {over_6_1h_games/total_games:.1%}")
        print(f"   ครึ่งหลัง >6: {over_6_2h_games}/{total_games} = {over_6_2h_games/total_games:.1%}")

# Example usage
if __name__ == "__main__":
    from ultra_predictor_fixed import UltraAdvancedPredictor
    
    print("⚽ ระบบทำนายเตะมุม - Corner Kicks Predictor")
    print("="*60)
    
    # โหลดข้อมูลการแข่งขัน
    predictor = UltraAdvancedPredictor()
    match_data = predictor.load_premier_league_data()
    
    # สร้างระบบทำนายเตะมุม
    corner_predictor = CornerPredictor()
    
    # สร้างข้อมูลเตะมุม
    corner_data = corner_predictor.generate_corner_data(match_data)
    
    # ทดสอบย้อนหลัง
    results = corner_predictor.backtest_corners(corner_data, test_games=20)
    
    # ตัวอย่างการทำนาย
    print(f"\n🎮 ตัวอย่างการทำนายเตะมุม:")
    print("="*60)
    
    demo_matches = [
        ("Arsenal", "Chelsea"),
        ("Manchester City", "Liverpool"),
        ("Manchester United", "Tottenham")
    ]
    
    for home, away in demo_matches:
        prediction = corner_predictor.predict_corners(home, away)
        if prediction:
            print(f"\n⚽ {home} vs {away}")
            print(f"   🎯 เตะมุมรวม: {prediction['predictions']['total_corners']} ({prediction['over_under_analysis']['total_12']} 12)")
            print(f"   🕐 ครึ่งแรก: {prediction['predictions']['first_half_corners']} ({prediction['over_under_analysis']['first_half_6']} 6)")
            print(f"   🕕 ครึ่งหลัง: {prediction['predictions']['second_half_corners']} ({prediction['over_under_analysis']['second_half_6']} 6)")
            print(f"   🏠 ทีมเหย้า: {prediction['predictions']['home_corners']} เตะมุม")
            print(f"   ✈️ ทีมเยือน: {prediction['predictions']['away_corners']} เตะมุม")
    
    print(f"\n✅ ระบบทำนายเตะมุมพร้อมใช้งาน!")
