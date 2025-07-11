#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ระบบทำนายฟุตบอลขั้นสูงสุดท้าย - เพิ่มความแม่นยำสูงสุด
ใช้ Enhanced Model ที่แก้ไขแล้วกับข้อมูลจริง
"""

from enhanced_predictor_fixed import EnhancedFootballPredictorFixed
from real_data_example import RealDataPredictor
from football_predictor import FootballPredictor
import pandas as pd
import numpy as np

class FinalEnhancedPredictor:
    def __init__(self):
        self.api_token = "052fd4885cf943ad859c89cef542e2e5"
        self.enhanced_predictor = None
        self.basic_predictor = None
        self.historical_data = None
        self.teams = []
        
    def load_comprehensive_data(self):
        """โหลดข้อมูลแบบครบถ้วน"""
        print("🔄 กำลังโหลดข้อมูลครบถ้วนจาก football-data.org...")
        
        real_predictor = RealDataPredictor(api_key=self.api_token)
        
        # ดึงข้อมูลหลายฤดูกาล
        data_2024 = real_predictor.get_premier_league_data(season=2024)
        data_2023 = real_predictor.get_premier_league_data(season=2023)
        
        if data_2024 is None:
            print("❌ ไม่สามารถโหลดข้อมูลได้")
            return False
        
        # รวมข้อมูล
        if data_2023 is not None:
            self.historical_data = pd.concat([data_2023, data_2024], ignore_index=True)
            print(f"✅ รวมข้อมูล 2 ฤดูกาล: {len(self.historical_data)} เกม")
        else:
            self.historical_data = data_2024
            print(f"✅ ใช้ข้อมูลฤดูกาล 2024: {len(self.historical_data)} เกม")
        
        # เรียงตามวันที่และทำความสะอาดข้อมูล
        self.historical_data = self.historical_data.sort_values('date').reset_index(drop=True)
        
        # ลบข้อมูลที่ไม่สมบูรณ์
        self.historical_data = self.historical_data.dropna(subset=['home_goals', 'away_goals'])
        
        # ดึงรายชื่อทีม
        self.teams = sorted(list(set(
            self.historical_data['home_team'].tolist() + 
            self.historical_data['away_team'].tolist()
        )))
        
        print(f"📊 จำนวนทีม: {len(self.teams)} ทีม")
        print(f"📅 ช่วงเวลา: {self.historical_data['date'].min()} ถึง {self.historical_data['date'].max()}")
        
        return True
    
    def train_both_models(self):
        """เทรนทั้ง Enhanced และ Basic Model"""
        print("\n🤖 กำลังเทรนโมเดลทั้งสอง...")
        
        # Enhanced Model
        print("1. กำลังเทรน Enhanced Model...")
        self.enhanced_predictor = EnhancedFootballPredictorFixed()
        enhanced_success = self.enhanced_predictor.train(self.historical_data)
        
        # Basic Model
        print("\n2. กำลังเทรน Basic Model...")
        self.basic_predictor = FootballPredictor()
        basic_success = self.basic_predictor.train(self.historical_data)
        
        if enhanced_success and basic_success:
            print("✅ เทรนโมเดลทั้งสองสำเร็จ")
            return True
        else:
            print("❌ เทรนโมเดลไม่สำเร็จ")
            return False
    
    def comprehensive_backtest(self, test_games=80):
        """ทำ backtest แบบครบถ้วน"""
        print(f"\n📊 กำลังทำ Comprehensive Backtest ({test_games} เกม)...")
        
        if len(self.historical_data) < test_games + 100:
            print("ข้อมูลไม่เพียงพอสำหรับ backtest")
            return None, None
        
        # แบ่งข้อมูล
        train_data = self.historical_data.iloc[:-test_games]
        test_data = self.historical_data.iloc[-test_games:]
        
        # เทรนโมเดลใหม่สำหรับ backtest
        print("กำลังเทรนโมเดลสำหรับ backtest...")
        
        # Enhanced Model
        enhanced_temp = EnhancedFootballPredictorFixed()
        enhanced_trained = enhanced_temp.train(train_data)
        
        # Basic Model
        basic_temp = FootballPredictor()
        basic_trained = basic_temp.train(train_data)
        
        if not (enhanced_trained and basic_trained):
            print("ไม่สามารถเทรนโมเดลสำหรับ backtest ได้")
            return None, None
        
        # ทดสอบทั้งสองโมเดล
        enhanced_results = []
        basic_results = []
        
        print("กำลังทำการทดสอบ...")
        for idx, match in test_data.iterrows():
            # ผลจริง
            if match['home_goals'] > match['away_goals']:
                actual = 'Home Win'
            elif match['home_goals'] < match['away_goals']:
                actual = 'Away Win'
            else:
                actual = 'Draw'
            
            # Enhanced Model
            enhanced_pred = enhanced_temp.predict_match(
                match['home_team'], match['away_team'], train_data
            )
            if enhanced_pred:
                enhanced_results.append({
                    'actual': actual,
                    'predicted': enhanced_pred['prediction'],
                    'correct': enhanced_pred['prediction'] == actual,
                    'confidence': enhanced_pred['confidence']
                })
            
            # Basic Model
            basic_pred = basic_temp.predict_match(
                match['home_team'], match['away_team'], train_data
            )
            if basic_pred:
                basic_results.append({
                    'actual': actual,
                    'predicted': basic_pred['prediction'],
                    'correct': basic_pred['prediction'] == actual,
                    'confidence': basic_pred['confidence']
                })
        
        # คำนวณผลลัพธ์
        enhanced_accuracy = sum(r['correct'] for r in enhanced_results) / len(enhanced_results) if enhanced_results else 0
        basic_accuracy = sum(r['correct'] for r in basic_results) / len(basic_results) if basic_results else 0
        
        enhanced_avg_conf = np.mean([r['confidence'] for r in enhanced_results]) if enhanced_results else 0
        basic_avg_conf = np.mean([r['confidence'] for r in basic_results]) if basic_results else 0
        
        # วิเคราะห์ความแม่นยำตามระดับความมั่นใจ
        enhanced_high_conf = [r for r in enhanced_results if r['confidence'] > 0.6]
        enhanced_high_conf_acc = sum(r['correct'] for r in enhanced_high_conf) / len(enhanced_high_conf) if enhanced_high_conf else 0
        
        basic_high_conf = [r for r in basic_results if r['confidence'] > 0.6]
        basic_high_conf_acc = sum(r['correct'] for r in basic_high_conf) / len(basic_high_conf) if basic_high_conf else 0
        
        print(f"\n🏆 ผล Comprehensive Backtest:")
        print(f"{'='*60}")
        print(f"📈 Enhanced Model:")
        print(f"   ความแม่นยำทั้งหมด: {enhanced_accuracy:.3f} ({enhanced_accuracy*100:.1f}%)")
        print(f"   ความมั่นใจเฉลี่ย: {enhanced_avg_conf:.3f}")
        print(f"   ความแม่นยำเมื่อมั่นใจ > 60%: {enhanced_high_conf_acc:.3f} ({len(enhanced_high_conf)} เกม)")
        
        print(f"\n📊 Basic Model:")
        print(f"   ความแม่นยำทั้งหมด: {basic_accuracy:.3f} ({basic_accuracy*100:.1f}%)")
        print(f"   ความมั่นใจเฉลี่ย: {basic_avg_conf:.3f}")
        print(f"   ความแม่นยำเมื่อมั่นใจ > 60%: {basic_high_conf_acc:.3f} ({len(basic_high_conf)} เกม)")
        
        improvement = enhanced_accuracy - basic_accuracy
        print(f"\n🚀 การปรับปรุง: +{improvement:.3f} ({improvement*100:.1f} percentage points)")
        
        return {
            'enhanced': {
                'accuracy': enhanced_accuracy,
                'avg_confidence': enhanced_avg_conf,
                'high_conf_accuracy': enhanced_high_conf_acc,
                'high_conf_games': len(enhanced_high_conf),
                'results': enhanced_results
            },
            'basic': {
                'accuracy': basic_accuracy,
                'avg_confidence': basic_avg_conf,
                'high_conf_accuracy': basic_high_conf_acc,
                'high_conf_games': len(basic_high_conf),
                'results': basic_results
            }
        }, improvement
    
    def smart_predict(self, home_team, away_team):
        """ทำนายอัจฉริยะ - ใช้ทั้งสองโมเดลและเลือกที่ดีที่สุด"""
        print(f"\n🧠 Smart Prediction: {home_team.replace(' FC', '')} vs {away_team.replace(' FC', '')}")
        print("="*70)
        
        # ทำนายด้วยทั้งสองโมเดล
        enhanced_result = self.enhanced_predictor.predict_match(home_team, away_team, self.historical_data)
        basic_result = self.basic_predictor.predict_match(home_team, away_team, self.historical_data)
        
        if not enhanced_result or not basic_result:
            print("❌ ไม่สามารถทำนายได้")
            return None
        
        print(f"🤖 Enhanced Model:")
        print(f"   การทำนาย: {enhanced_result['prediction']}")
        print(f"   ความมั่นใจ: {enhanced_result['confidence']:.3f} ({enhanced_result['confidence']*100:.1f}%)")
        
        print(f"\n📊 Basic Model:")
        print(f"   การทำนาย: {basic_result['prediction']}")
        print(f"   ความมั่นใจ: {basic_result['confidence']:.3f} ({basic_result['confidence']*100:.1f}%)")
        
        # เลือกโมเดลที่ดีที่สุด
        if enhanced_result['confidence'] > basic_result['confidence']:
            final_result = enhanced_result
            chosen_model = "Enhanced Model"
        else:
            final_result = basic_result
            chosen_model = "Basic Model"
        
        print(f"\n🎯 Final Smart Prediction (ใช้ {chosen_model}):")
        print(f"   การทำนาย: {final_result['prediction']}")
        print(f"   ความมั่นใจ: {final_result['confidence']:.3f} ({final_result['confidence']*100:.1f}%)")
        
        # แสดงความน่าจะเป็น
        print(f"\n📊 ความน่าจะเป็นของแต่ละผล:")
        prediction_emoji = {'Home Win': '🏠', 'Away Win': '✈️', 'Draw': '🤝'}
        for outcome, prob in final_result['probabilities'].items():
            emoji = prediction_emoji.get(outcome, '⚽')
            bar_length = int(prob * 25)
            bar = "█" * bar_length + "░" * (25 - bar_length)
            print(f"   {emoji} {outcome:10s}: {bar} {prob:.3f} ({prob*100:.1f}%)")
        
        # การวิเคราะห์ความน่าเชื่อถือ
        if final_result['confidence'] > 0.7:
            reliability = "สูงมาก 🔥"
        elif final_result['confidence'] > 0.6:
            reliability = "สูง ✅"
        elif final_result['confidence'] > 0.5:
            reliability = "ปานกลาง ⚡"
        else:
            reliability = "ต่ำ ⚠️"
        
        print(f"\n🔍 ความน่าเชื่อถือ: {reliability}")
        
        return final_result
    
    def run_final_analysis(self):
        """รันการวิเคราะห์สุดท้าย"""
        print("🏆 ระบบทำนายฟุตบอลขั้นสูงสุดท้าย")
        print("🚀 Enhanced Model + Smart Prediction")
        print("="*60)
        
        # โหลดข้อมูล
        if not self.load_comprehensive_data():
            return
        
        # เทรนโมเดล
        if not self.train_both_models():
            return
        
        # ทำ backtest
        backtest_results, improvement = self.comprehensive_backtest(test_games=100)
        
        if backtest_results is None:
            return
        
        # ทำนายตัวอย่าง
        print(f"\n🎮 ตัวอย่าง Smart Predictions:")
        sample_matches = [
            ('Arsenal FC', 'Chelsea FC'),
            ('Manchester City FC', 'Liverpool FC'),
            ('Manchester United FC', 'Tottenham Hotspur FC'),
            ('Newcastle United FC', 'Brighton & Hove Albion FC')
        ]
        
        for home, away in sample_matches:
            self.smart_predict(home, away)
            print("\n" + "-"*70)
        
        # สรุปผลสุดท้าย
        enhanced_acc = backtest_results['enhanced']['accuracy']
        basic_acc = backtest_results['basic']['accuracy']
        
        print(f"\n🏆 สรุปผลการพัฒนา:")
        print(f"✅ Enhanced Model: {enhanced_acc*100:.1f}% accuracy")
        print(f"📊 Basic Model: {basic_acc*100:.1f}% accuracy")
        print(f"🚀 การปรับปรุง: +{improvement*100:.1f} percentage points")
        
        if enhanced_acc > 0.55:
            print(f"\n🎉 ความสำเร็จ: Enhanced Model ให้ความแม่นยำสูงกว่า 55%!")
        elif enhanced_acc > 0.50:
            print(f"\n✅ ผลดี: Enhanced Model ให้ความแม่นยำสูงกว่า 50%")
        else:
            print(f"\n📝 หมายเหตุ: ฟุตบอลมีความไม่แน่นอนสูง ผลลัพธ์นี้ยังคงมีประโยชน์")
        
        print(f"\n💡 คำแนะนำการใช้งาน:")
        print(f"   - ใช้ Smart Prediction เพื่อผลลัพธ์ที่ดีที่สุด")
        print(f"   - เชื่อถือการทำนายที่มีความมั่นใจ > 60%")
        print(f"   - ใช้เป็นข้อมูลอ้างอิงเท่านั้น ไม่ใช่เพื่อการเดิมพัน")
        
        return backtest_results

def main():
    predictor = FinalEnhancedPredictor()
    predictor.run_final_analysis()

if __name__ == "__main__":
    main()
