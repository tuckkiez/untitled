#!/usr/bin/env python3
"""
🇪🇸 ทดสอบ La Liga Real Predictor
ทดสอบ 20 นัดล่าสุดด้วยข้อมูลจริง
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

class LaLigaRealPredictor:
    def __init__(self):
        self.team_ratings = {}
        self.is_trained = False
        self.historical_data = None
    
    def load_real_data(self):
        """โหลดข้อมูล La Liga จริง"""
        try:
            data = pd.read_csv('laliga_real_data.csv')
            data['date'] = pd.to_datetime(data['date'])
            data = data.sort_values('date').reset_index(drop=True)
            self.historical_data = data
            return data
        except:
            return None
    
    def calculate_elo_ratings(self, matches_df):
        """คำนวณ ELO Rating"""
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
    
    def predict_simple(self, home_team, away_team):
        """ทำนายแบบง่าย (ใช้ ELO + Form)"""
        if not self.team_ratings:
            return None
        
        # ELO ratings
        home_elo = self.team_ratings.get(home_team, 1500)
        away_elo = self.team_ratings.get(away_team, 1500)
        
        # Home advantage
        home_elo += 100
        
        # คำนวณความน่าจะเป็น
        home_expected = 1 / (1 + 10**((away_elo - home_elo) / 400))
        away_expected = 1 - home_expected
        
        # ปรับด้วยฟอร์ม
        home_form = self._get_team_form(home_team)
        away_form = self._get_team_form(away_team)
        
        home_prob = home_expected * (1 + home_form * 0.1)
        away_prob = away_expected * (1 + away_form * 0.1)
        draw_prob = 0.25
        
        # Normalize
        total_prob = home_prob + away_prob + draw_prob
        home_prob /= total_prob
        away_prob /= total_prob
        draw_prob /= total_prob
        
        # ทำนายผล
        if home_prob > away_prob and home_prob > draw_prob:
            prediction = "Home Win"
            confidence = home_prob
        elif away_prob > home_prob and away_prob > draw_prob:
            prediction = "Away Win"
            confidence = away_prob
        else:
            prediction = "Draw"
            confidence = draw_prob
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'probabilities': {
                'Home Win': home_prob,
                'Draw': draw_prob,
                'Away Win': away_prob
            }
        }
    
    def _get_team_form(self, team):
        """คำนวณฟอร์มทีม"""
        if not hasattr(self, 'historical_data'):
            return 0
        
        recent_matches = self.historical_data[
            (self.historical_data['home_team'] == team) | 
            (self.historical_data['away_team'] == team)
        ].tail(5)
        
        points = 0
        for _, match in recent_matches.iterrows():
            if match['home_team'] == team:
                if match['home_goals'] > match['away_goals']:
                    points += 3
                elif match['home_goals'] == match['away_goals']:
                    points += 1
            else:
                if match['away_goals'] > match['home_goals']:
                    points += 3
                elif match['away_goals'] == match['home_goals']:
                    points += 1
        
        return (points / 15) - 0.5

def test_laliga_20_matches():
    """ทดสอบ La Liga 20 นัดล่าสุด"""
    print("🇪🇸 ทดสอบ La Liga Real Predictor")
    print("📊 ทดสอบ 20 นัดล่าสุดด้วยข้อมูลจริง")
    print("=" * 70)
    
    # สร้าง predictor
    predictor = LaLigaRealPredictor()
    
    # โหลดข้อมูล
    data = predictor.load_real_data()
    if data is None:
        print("❌ ไม่พบข้อมูล La Liga")
        return
    
    print(f"✅ โหลดข้อมูลสำเร็จ: {len(data)} เกม")
    
    # เอา 20 นัดล่าสุดมาทดสอบ
    test_matches = data.tail(20).copy()
    training_data = data.iloc[:-20].copy()
    
    print(f"📊 ข้อมูลเทรน: {len(training_data)} เกม")
    print(f"🎯 ข้อมูลทดสอบ: {len(test_matches)} เกม")
    
    # เทรนด้วยข้อมูลก่อน 20 นัดล่าสุด
    predictor.calculate_elo_ratings(training_data)
    
    # แสดง Top 5 ทีม
    print(f"\n🏆 Top 5 ทีมแข็งแกร่งที่สุด (ELO Rating):")
    sorted_teams = sorted(predictor.team_ratings.items(), key=lambda x: x[1], reverse=True)
    for i, (team, rating) in enumerate(sorted_teams[:5]):
        print(f"   {i+1}. {team}: {rating:.0f}")
    
    # ทดสอบการทำนาย
    print(f"\n🎯 ทดสอบการทำนาย 20 นัดล่าสุด:")
    print("=" * 70)
    
    correct_predictions = 0
    total_confidence = 0
    high_confidence_correct = 0
    high_confidence_total = 0
    
    results = []
    
    for idx, (_, match) in enumerate(test_matches.iterrows(), 1):
        home_team = match['home_team']
        away_team = match['away_team']
        home_goals = match['home_goals']
        away_goals = match['away_goals']
        match_date = match['date'].strftime('%Y-%m-%d')
        
        # ผลจริง
        if home_goals > away_goals:
            actual_result = "Home Win"
        elif home_goals == away_goals:
            actual_result = "Draw"
        else:
            actual_result = "Away Win"
        
        # ทำนาย
        prediction = predictor.predict_simple(home_team, away_team)
        
        if prediction:
            predicted_result = prediction['prediction']
            confidence = prediction['confidence']
            
            # ตรวจสอบความถูกต้อง
            is_correct = predicted_result == actual_result
            if is_correct:
                correct_predictions += 1
            
            total_confidence += confidence
            
            # High confidence (>60%)
            if confidence > 0.6:
                high_confidence_total += 1
                if is_correct:
                    high_confidence_correct += 1
            
            # แสดงผล
            status = "✅" if is_correct else "❌"
            print(f"{idx:2d}. {match_date} | {home_team} {home_goals}-{away_goals} {away_team}")
            print(f"    ทำนาย: {predicted_result} ({confidence:.1%}) | จริง: {actual_result} {status}")
            
            results.append({
                'match': f"{home_team} vs {away_team}",
                'predicted': predicted_result,
                'actual': actual_result,
                'confidence': confidence,
                'correct': is_correct
            })
        else:
            print(f"{idx:2d}. {match_date} | {home_team} vs {away_team} - ไม่สามารถทำนายได้")
    
    # สรุปผล
    print(f"\n📊 สรุปผลการทดสอบ:")
    print("=" * 50)
    
    if len(results) > 0:
        accuracy = correct_predictions / len(results)
        avg_confidence = total_confidence / len(results)
        
        print(f"✅ ความแม่นยำ: {correct_predictions}/{len(results)} = {accuracy:.1%}")
        print(f"📈 ความมั่นใจเฉลี่ย: {avg_confidence:.1%}")
        
        if high_confidence_total > 0:
            high_conf_accuracy = high_confidence_correct / high_confidence_total
            print(f"🔥 ความแม่นยำเมื่อมั่นใจสูง (>60%): {high_confidence_correct}/{high_confidence_total} = {high_conf_accuracy:.1%}")
        
        # วิเคราะห์ตามประเภทผล
        home_wins = sum(1 for r in results if r['predicted'] == 'Home Win')
        draws = sum(1 for r in results if r['predicted'] == 'Draw')
        away_wins = sum(1 for r in results if r['predicted'] == 'Away Win')
        
        print(f"\n📋 การทำนายตามประเภท:")
        print(f"   🏠 ทำนายเจ้าบ้านชนะ: {home_wins} คู่")
        print(f"   🤝 ทำนายเสมอ: {draws} คู่")
        print(f"   ✈️ ทำนายทีมเยือนชนะ: {away_wins} คู่")
        
        # เปรียบเทียบกับระบบเดิม
        print(f"\n🔍 เปรียบเทียบประสิทธิภาพ:")
        if accuracy >= 0.6:
            print(f"   🎉 ยอดเยี่ยม! ความแม่นยำ {accuracy:.1%} ≥ 60%")
        elif accuracy >= 0.5:
            print(f"   ✅ ดี! ความแม่นยำ {accuracy:.1%} ≥ 50%")
        else:
            print(f"   ⚠️ ต้องปรับปรุง ความแม่นยำ {accuracy:.1%} < 50%")
        
        return {
            'accuracy': accuracy,
            'avg_confidence': avg_confidence,
            'high_conf_accuracy': high_conf_accuracy if high_confidence_total > 0 else 0,
            'results': results
        }
    else:
        print("❌ ไม่สามารถทำนายได้เลย")
        return None

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 La Liga Real Data Testing")
    print("🇪🇸 ทดสอบด้วยข้อมูลจริง 380 เกม")
    print("=" * 70)
    
    # ทดสอบระบบ
    result = test_laliga_20_matches()
    
    if result:
        print(f"\n🎉 การทดสอบเสร็จสิ้น!")
        print(f"📊 ระบบ La Liga ด้วยข้อมูลจริงพร้อมใช้งาน")
        print(f"🎯 ความแม่นยำ: {result['accuracy']:.1%}")
    else:
        print(f"\n❌ การทดสอบไม่สำเร็จ")
    
    return result

if __name__ == "__main__":
    result = main()
