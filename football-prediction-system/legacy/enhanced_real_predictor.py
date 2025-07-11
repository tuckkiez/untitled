#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ระบบทำนายฟุตบอลขั้นสูงด้วยข้อมูลจริง
ใช้ Enhanced Model เพื่อเพิ่มความแม่นยำ
"""

from enhanced_predictor import EnhancedFootballPredictor
from real_data_example import RealDataPredictor
import pandas as pd
import numpy as np

class EnhancedRealPredictor:
    def __init__(self):
        self.api_token = "052fd4885cf943ad859c89cef542e2e5"
        self.enhanced_predictor = None
        self.historical_data = None
        self.teams = []
        
    def load_and_prepare_data(self):
        """โหลดและเตรียมข้อมูลจาก API"""
        print("🔄 กำลังโหลดข้อมูลจาก football-data.org...")
        
        real_predictor = RealDataPredictor(api_key=self.api_token)
        
        # ดึงข้อมูลหลายฤดูกาลเพื่อเพิ่มความแม่นยำ
        data_2024 = real_predictor.get_premier_league_data(season=2024)
        data_2023 = real_predictor.get_premier_league_data(season=2023)
        
        if data_2024 is None:
            print("❌ ไม่สามารถโหลดข้อมูลได้")
            return False
        
        # รวมข้อมูลหลายฤดูกาล
        if data_2023 is not None:
            self.historical_data = pd.concat([data_2023, data_2024], ignore_index=True)
            print(f"✅ รวมข้อมูล 2 ฤดูกาล: {len(self.historical_data)} เกม")
        else:
            self.historical_data = data_2024
            print(f"✅ ใช้ข้อมูลฤดูกาล 2024: {len(self.historical_data)} เกม")
        
        # เรียงตามวันที่
        self.historical_data = self.historical_data.sort_values('date').reset_index(drop=True)
        
        # ดึงรายชื่อทีม
        self.teams = sorted(list(set(
            self.historical_data['home_team'].tolist() + 
            self.historical_data['away_team'].tolist()
        )))
        
        print(f"📊 จำนวนทีม: {len(self.teams)} ทีม")
        print(f"📅 ช่วงเวลา: {self.historical_data['date'].min()} ถึง {self.historical_data['date'].max()}")
        
        return True
    
    def train_enhanced_model(self):
        """เทรน Enhanced Model"""
        print("\n🤖 กำลังเทรน Enhanced Model...")
        self.enhanced_predictor = EnhancedFootballPredictor()
        
        if not self.enhanced_predictor.train(self.historical_data):
            print("❌ ไม่สามารถเทรน Enhanced Model ได้")
            return False
        
        print("✅ เทรน Enhanced Model สำเร็จ")
        return True
    
    def compare_models(self):
        """เปรียบเทียบ Enhanced Model กับ Basic Model"""
        print("\n📊 กำลังเปรียบเทียบโมเดล...")
        
        # Enhanced Model Backtest
        enhanced_result = self.enhanced_predictor.backtest(self.historical_data, test_period_games=60)
        
        # Basic Model Backtest (สำหรับเปรียบเทียบ)
        from football_predictor import FootballPredictor
        basic_predictor = FootballPredictor()
        basic_predictor.train(self.historical_data.iloc[:-60])
        
        # Manual backtest for basic model
        test_data = self.historical_data.iloc[-60:]
        basic_correct = 0
        basic_total = 0
        
        for _, match in test_data.iterrows():
            result = basic_predictor.predict_match(
                match['home_team'], match['away_team'], 
                self.historical_data.iloc[:-60]
            )
            if result:
                actual = 'Home Win' if match['home_goals'] > match['away_goals'] else \
                        'Away Win' if match['home_goals'] < match['away_goals'] else 'Draw'
                if result['prediction'] == actual:
                    basic_correct += 1
                basic_total += 1
        
        basic_accuracy = basic_correct / basic_total if basic_total > 0 else 0
        
        print(f"\n🏆 การเปรียบเทียบโมเดล:")
        print(f"{'='*50}")
        print(f"📈 Enhanced Model:")
        print(f"   ความแม่นยำ: {enhanced_result['accuracy']:.3f} ({enhanced_result['accuracy']*100:.1f}%)")
        print(f"   ความมั่นใจเฉลี่ย: {enhanced_result['avg_confidence']:.3f}")
        print(f"   จำนวน Features: 40")
        print(f"   โมเดล: Ensemble (RF + GB + LR)")
        
        print(f"\n📊 Basic Model:")
        print(f"   ความแม่นยำ: {basic_accuracy:.3f} ({basic_accuracy*100:.1f}%)")
        print(f"   จำนวน Features: 15")
        print(f"   โมเดล: Random Forest")
        
        improvement = enhanced_result['accuracy'] - basic_accuracy
        print(f"\n🚀 การปรับปรุง: +{improvement:.3f} ({improvement*100:.1f} percentage points)")
        
        return enhanced_result, basic_accuracy
    
    def predict_with_analysis(self, home_team, away_team):
        """ทำนายพร้อมการวิเคราะห์เชิงลึก"""
        result = self.enhanced_predictor.predict_match(home_team, away_team, self.historical_data)
        
        if not result:
            print("❌ ไม่สามารถทำนายได้")
            return None
        
        # แสดงผลการทำนาย
        print("\n" + "="*70)
        print(f"⚽ Enhanced Prediction: {home_team.replace(' FC', '')} vs {away_team.replace(' FC', '')}")
        print("="*70)
        
        # การทำนาย
        prediction_emoji = {'Home Win': '🏠', 'Away Win': '✈️', 'Draw': '🤝'}
        print(f"\n🎯 การทำนาย: {prediction_emoji.get(result['prediction'], '⚽')} {result['prediction']}")
        print(f"🎲 ความมั่นใจ: {result['confidence']:.3f} ({result['confidence']*100:.1f}%)")
        print(f"🤖 โมเดล: {result['model_type']}")
        
        # ความน่าจะเป็น
        print(f"\n📊 ความน่าจะเป็นของแต่ละผล:")
        for outcome, prob in result['probabilities'].items():
            emoji = prediction_emoji.get(outcome, '⚽')
            bar_length = int(prob * 25)
            bar = "█" * bar_length + "░" * (25 - bar_length)
            print(f"   {emoji} {outcome:10s}: {bar} {prob:.3f} ({prob*100:.1f}%)")
        
        # การวิเคราะห์ความน่าเชื่อถือ
        confidence_level = "สูงมาก" if result['confidence'] > 0.7 else \
                          "สูง" if result['confidence'] > 0.6 else \
                          "ปานกลาง" if result['confidence'] > 0.5 else "ต่ำ"
        
        print(f"\n🔍 การวิเคราะห์:")
        print(f"   ระดับความน่าเชื่อถือ: {confidence_level}")
        
        if result['confidence'] > 0.65:
            print(f"   💡 แนะนำ: การทำนายนี้มีความน่าเชื่อถือสูง")
        elif result['confidence'] < 0.45:
            print(f"   ⚠️  คำเตือน: การทำนายนี้มีความไม่แน่นอนสูง")
        
        # สถิติทีม
        self.show_team_comparison(home_team, away_team)
        
        return result
    
    def show_team_comparison(self, home_team, away_team):
        """แสดงการเปรียบเทียบทีม"""
        print(f"\n📈 การเปรียบเทียบทีม:")
        
        # คำนวณสถิติขั้นสูง
        home_stats = self.enhanced_predictor.calculate_advanced_team_stats(self.historical_data, home_team)
        away_stats = self.enhanced_predictor.calculate_advanced_team_stats(self.historical_data, away_team)
        
        stats_to_show = [
            ('Win Rate', 'win_rate'),
            ('Recent Form', 'recent_form'),
            ('Goals/Game', 'avg_goals_for'),
            ('Clean Sheets', 'clean_sheet_rate'),
            ('Home Win Rate', 'home_win_rate'),
            ('Momentum', 'momentum')
        ]
        
        print(f"   {'Stat':<15} {'Home':<15} {'Away':<15} {'Advantage':<10}")
        print(f"   {'-'*55}")
        
        for stat_name, stat_key in stats_to_show:
            home_val = home_stats[stat_key]
            away_val = away_stats[stat_key]
            
            if home_val > away_val:
                advantage = "🏠 Home"
            elif away_val > home_val:
                advantage = "✈️ Away"
            else:
                advantage = "🤝 Equal"
            
            print(f"   {stat_name:<15} {home_val:<15.3f} {away_val:<15.3f} {advantage:<10}")
    
    def run_enhanced_analysis(self):
        """รันการวิเคราะห์ขั้นสูงแบบครบถ้วน"""
        print("🏆 ระบบทำนายฟุตบอลขั้นสูง - Enhanced Model")
        print("📊 ใช้ Ensemble Learning และ Advanced Features")
        
        # โหลดข้อมูล
        if not self.load_and_prepare_data():
            return
        
        # เทรนโมเดล
        if not self.train_enhanced_model():
            return
        
        # เปรียบเทียบโมเดล
        enhanced_result, basic_accuracy = self.compare_models()
        
        # ทำนายตัวอย่าง
        print(f"\n🎮 ตัวอย่างการทำนายขั้นสูง:")
        sample_matches = [
            ('Arsenal FC', 'Chelsea FC'),
            ('Manchester City FC', 'Liverpool FC'),
            ('Manchester United FC', 'Tottenham Hotspur FC')
        ]
        
        for home, away in sample_matches:
            self.predict_with_analysis(home, away)
            print("\n" + "-"*70)
        
        # สรุปผล
        print(f"\n🏆 สรุปผลการปรับปรุง:")
        print(f"✅ Enhanced Model ให้ความแม่นยำ {enhanced_result['accuracy']*100:.1f}%")
        print(f"📈 ปรับปรุงจาก Basic Model {(enhanced_result['accuracy'] - basic_accuracy)*100:.1f} percentage points")
        print(f"🎯 ความมั่นใจเฉลี่ย {enhanced_result['avg_confidence']*100:.1f}%")
        
        # คำแนะนำการใช้งาน
        if enhanced_result['accuracy'] > 0.55:
            print(f"\n💡 คำแนะนำ: โมเดลมีประสิทธิภาพดี เหมาะสำหรับการวิเคราะห์")
        else:
            print(f"\n⚠️  หมายเหตุ: ฟุตบอลมีความไม่แน่นอนสูง ใช้เป็นข้อมูลอ้างอิงเท่านั้น")
        
        return enhanced_result

def main():
    predictor = EnhancedRealPredictor()
    predictor.run_enhanced_analysis()

if __name__ == "__main__":
    main()
