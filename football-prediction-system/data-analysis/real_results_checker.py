#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ตรวจสอบผลลัพธ์จริงจาก 20 นัดล่าสุด
เปรียบเทียบการทำนายกับผลจริงที่เกิดขึ้น
"""

from final_enhanced_predictor import FinalEnhancedPredictor
from real_data_example import RealDataPredictor
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class RealResultsChecker:
    def __init__(self):
        self.api_token = "052fd4885cf943ad859c89cef542e2e5"
        self.predictor = None
        self.historical_data = None
        
    def load_latest_data(self):
        """โหลดข้อมูลล่าสุดรวมถึงผลที่เพิ่งจบ"""
        print("🔄 กำลังโหลดข้อมูลล่าสุด...")
        
        real_predictor = RealDataPredictor(api_key=self.api_token)
        
        # ดึงข้อมูลล่าสุด
        data_2024 = real_predictor.get_premier_league_data(season=2024)
        data_2023 = real_predictor.get_premier_league_data(season=2023)
        
        if data_2024 is None:
            print("❌ ไม่สามารถโหลดข้อมูลได้")
            return False
        
        # รวมข้อมูล
        if data_2023 is not None:
            self.historical_data = pd.concat([data_2023, data_2024], ignore_index=True)
        else:
            self.historical_data = data_2024
        
        # เรียงตามวันที่
        self.historical_data = self.historical_data.sort_values('date').reset_index(drop=True)
        self.historical_data = self.historical_data.dropna(subset=['home_goals', 'away_goals'])
        
        print(f"✅ โหลดข้อมูลสำเร็จ: {len(self.historical_data)} เกม")
        print(f"📅 ข้อมูลล่าสุด: {self.historical_data['date'].max()}")
        
        return True
    
    def setup_predictor(self):
        """ตั้งค่า predictor"""
        print("\n🤖 กำลังเตรียม Enhanced Predictor...")
        
        self.predictor = FinalEnhancedPredictor()
        self.predictor.api_token = self.api_token
        self.predictor.historical_data = self.historical_data
        
        # เทรนโมเดลด้วยข้อมูลทั้งหมดยกเว้น 20 เกมล่าสุด
        train_data = self.historical_data.iloc[:-20]
        
        if not self.predictor.train_both_models():
            # ถ้าไม่สำเร็จ ให้เทรนแบบง่าย
            from enhanced_predictor_fixed import EnhancedFootballPredictorFixed
            self.predictor.enhanced_predictor = EnhancedFootballPredictorFixed()
            self.predictor.enhanced_predictor.train(train_data)
            
        print("✅ เตรียม Predictor สำเร็จ")
        return True
    
    def check_last_20_matches(self):
        """ตรวจสอบผลลัพธ์ 20 นัดล่าสุด"""
        print("\n🔍 กำลังตรวจสอบผลลัพธ์ 20 นัดล่าสุด...")
        print("="*80)
        
        # เอา 20 เกมล่าสุด
        last_20_matches = self.historical_data.tail(20)
        train_data = self.historical_data.iloc[:-20]
        
        results = []
        correct_predictions = 0
        high_confidence_correct = 0
        high_confidence_total = 0
        
        print(f"{'No.':<3} {'Date':<12} {'Match':<35} {'Result':<8} {'Predicted':<10} {'Confidence':<10} {'Status':<8}")
        print("-" * 80)
        
        for idx, (_, match) in enumerate(last_20_matches.iterrows(), 1):
            # ผลจริง
            home_goals = int(match['home_goals'])
            away_goals = int(match['away_goals'])
            
            if home_goals > away_goals:
                actual_result = 'Home Win'
                actual_short = 'H'
            elif home_goals < away_goals:
                actual_result = 'Away Win'
                actual_short = 'A'
            else:
                actual_result = 'Draw'
                actual_short = 'D'
            
            # ทำนายด้วยข้อมูลก่อนหน้า
            try:
                if hasattr(self.predictor, 'enhanced_predictor') and self.predictor.enhanced_predictor:
                    prediction = self.predictor.enhanced_predictor.predict_match(
                        match['home_team'], match['away_team'], train_data
                    )
                else:
                    # ใช้ basic predictor
                    from football_predictor import FootballPredictor
                    basic_predictor = FootballPredictor()
                    basic_predictor.train(train_data)
                    prediction = basic_predictor.predict_match(
                        match['home_team'], match['away_team'], train_data
                    )
            except:
                prediction = None
            
            if prediction:
                predicted_result = prediction['prediction']
                confidence = prediction['confidence']
                
                # ตรวจสอบความถูกต้อง
                is_correct = (predicted_result == actual_result)
                if is_correct:
                    correct_predictions += 1
                    status = "✅"
                else:
                    status = "❌"
                
                # ตรวจสอบ high confidence
                if confidence > 0.6:
                    high_confidence_total += 1
                    if is_correct:
                        high_confidence_correct += 1
                
                # แสดงผล
                home_team_short = match['home_team'].replace(' FC', '').replace(' United', ' Utd')[:15]
                away_team_short = match['away_team'].replace(' FC', '').replace(' United', ' Utd')[:15]
                match_str = f"{home_team_short} vs {away_team_short}"
                
                predicted_short = predicted_result[0] if predicted_result != 'Draw' else 'D'
                result_str = f"{home_goals}-{away_goals} ({actual_short})"
                
                print(f"{idx:<3} {match['date'].strftime('%Y-%m-%d'):<12} {match_str:<35} {result_str:<8} "
                      f"{predicted_short:<10} {confidence:.3f}     {status:<8}")
                
                results.append({
                    'match': f"{match['home_team']} vs {match['away_team']}",
                    'date': match['date'],
                    'actual': actual_result,
                    'predicted': predicted_result,
                    'confidence': confidence,
                    'correct': is_correct,
                    'home_goals': home_goals,
                    'away_goals': away_goals
                })
            else:
                print(f"{idx:<3} {match['date'].strftime('%Y-%m-%d'):<12} {match_str:<35} {result_str:<8} "
                      f"{'N/A':<10} {'N/A':<10} {'⚠️':<8}")
        
        # สรุปผล
        total_predictions = len([r for r in results if r is not None])
        overall_accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        high_conf_accuracy = high_confidence_correct / high_confidence_total if high_confidence_total > 0 else 0
        
        print("\n" + "="*80)
        print("📊 สรุปผลการตรวจสอบ 20 นัดล่าสุด:")
        print(f"🎯 ความแม่นยำทั้งหมด: {correct_predictions}/{total_predictions} = {overall_accuracy:.3f} ({overall_accuracy*100:.1f}%)")
        print(f"🔥 ความแม่นยำเมื่อมั่นใจ > 60%: {high_confidence_correct}/{high_confidence_total} = {high_conf_accuracy:.3f} ({high_conf_accuracy*100:.1f}%)")
        print(f"📈 จำนวนการทำนายที่มั่นใจสูง: {high_confidence_total}/20 ({high_confidence_total/20*100:.1f}%)")
        
        # วิเคราะห์ประเภทการทำนาย
        home_wins_actual = len([r for r in results if r['actual'] == 'Home Win'])
        away_wins_actual = len([r for r in results if r['actual'] == 'Away Win'])
        draws_actual = len([r for r in results if r['actual'] == 'Draw'])
        
        home_wins_predicted = len([r for r in results if r['predicted'] == 'Home Win'])
        away_wins_predicted = len([r for r in results if r['predicted'] == 'Away Win'])
        draws_predicted = len([r for r in results if r['predicted'] == 'Draw'])
        
        print(f"\n📋 การกระจายผลลัพธ์:")
        print(f"   Home Win: จริง {home_wins_actual}, ทำนาย {home_wins_predicted}")
        print(f"   Away Win: จริง {away_wins_actual}, ทำนาย {away_wins_predicted}")
        print(f"   Draw: จริง {draws_actual}, ทำนาย {draws_predicted}")
        
        # ความแม่นยำแต่ละประเภท
        home_win_correct = len([r for r in results if r['actual'] == 'Home Win' and r['predicted'] == 'Home Win'])
        away_win_correct = len([r for r in results if r['actual'] == 'Away Win' and r['predicted'] == 'Away Win'])
        draw_correct = len([r for r in results if r['actual'] == 'Draw' and r['predicted'] == 'Draw'])
        
        print(f"\n🎯 ความแม่นยำแต่ละประเภท:")
        if home_wins_actual > 0:
            print(f"   Home Win: {home_win_correct}/{home_wins_actual} = {home_win_correct/home_wins_actual:.3f}")
        if away_wins_actual > 0:
            print(f"   Away Win: {away_win_correct}/{away_wins_actual} = {away_win_correct/away_wins_actual:.3f}")
        if draws_actual > 0:
            print(f"   Draw: {draw_correct}/{draws_actual} = {draw_correct/draws_actual:.3f}")
        
        return {
            'results': results,
            'overall_accuracy': overall_accuracy,
            'high_confidence_accuracy': high_conf_accuracy,
            'high_confidence_count': high_confidence_total,
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions
        }
    
    def show_detailed_analysis(self, results_data):
        """แสดงการวิเคราะห์เชิงลึก"""
        results = results_data['results']
        
        print(f"\n🔬 การวิเคราะห์เชิงลึก:")
        print("="*60)
        
        # การทำนายที่ถูกต้องและมีความมั่นใจสูง
        high_conf_correct = [r for r in results if r['confidence'] > 0.6 and r['correct']]
        if high_conf_correct:
            print(f"🎉 การทำนายที่ถูกและมั่นใจสูง ({len(high_conf_correct)} เกม):")
            for r in high_conf_correct:
                print(f"   ✅ {r['match']}: {r['predicted']} (มั่นใจ {r['confidence']:.3f})")
        
        # การทำนายที่ผิดแต่มีความมั่นใจสูง
        high_conf_wrong = [r for r in results if r['confidence'] > 0.6 and not r['correct']]
        if high_conf_wrong:
            print(f"\n⚠️  การทำนายที่ผิดแต่มั่นใจสูง ({len(high_conf_wrong)} เกม):")
            for r in high_conf_wrong:
                print(f"   ❌ {r['match']}: ทำนาย {r['predicted']}, จริง {r['actual']} (มั่นใจ {r['confidence']:.3f})")
        
        # เกมที่ยากต่อการทำนาย (ความมั่นใจต่ำ)
        low_conf = [r for r in results if r['confidence'] < 0.5]
        if low_conf:
            print(f"\n🤔 เกมที่ยากต่อการทำนาย ({len(low_conf)} เกม):")
            for r in low_conf:
                status = "✅" if r['correct'] else "❌"
                print(f"   {status} {r['match']}: มั่นใจ {r['confidence']:.3f}")
        
        # ค่าเฉลี่ยความมั่นใจ
        avg_confidence = np.mean([r['confidence'] for r in results])
        print(f"\n📊 ค่าเฉลี่ยความมั่นใจ: {avg_confidence:.3f}")
        
        # เปรียบเทียบกับ backtest
        print(f"\n📈 เปรียบเทียบกับ Backtest:")
        print(f"   Backtest (100 เกม): 51.0% accuracy")
        print(f"   Real Check (20 เกม): {results_data['overall_accuracy']*100:.1f}% accuracy")
        
        if results_data['overall_accuracy'] > 0.51:
            print(f"   🎉 ผลจริงดีกว่า Backtest!")
        elif results_data['overall_accuracy'] > 0.45:
            print(f"   ✅ ผลจริงใกล้เคียง Backtest")
        else:
            print(f"   ⚠️  ผลจริงต่ำกว่า Backtest (อาจเป็นเพราะข้อมูลน้อย)")
    
    def run_real_check(self):
        """รันการตรวจสอบผลจริง"""
        print("🏆 ระบบตรวจสอบผลลัพธ์จริง - 20 นัดล่าสุด")
        print("🔍 เปรียบเทียบการทำนายกับผลที่เกิดขึ้นจริง")
        print("="*80)
        
        # โหลดข้อมูล
        if not self.load_latest_data():
            return
        
        # ตั้งค่า predictor
        if not self.setup_predictor():
            return
        
        # ตรวจสอบ 20 นัดล่าสุด
        results_data = self.check_last_20_matches()
        
        # วิเคราะห์เชิงลึก
        self.show_detailed_analysis(results_data)
        
        # สรุปสุดท้าย
        print(f"\n🏆 สรุปการตรวจสอบ:")
        print(f"✅ ความแม่นยำจริง: {results_data['overall_accuracy']*100:.1f}%")
        print(f"🔥 ความแม่นยำเมื่อมั่นใจสูง: {results_data['high_confidence_accuracy']*100:.1f}%")
        print(f"📊 จำนวนการทำนายที่มั่นใจสูง: {results_data['high_confidence_count']}/20")
        
        if results_data['overall_accuracy'] >= 0.5:
            print(f"\n🎉 ยอดเยี่ยม! ระบบให้ความแม่นยำ ≥ 50% ในการทดสอบจริง")
        elif results_data['overall_accuracy'] >= 0.45:
            print(f"\n✅ ดี! ระบบให้ความแม่นยำใกล้เคียงกับ backtest")
        else:
            print(f"\n📝 หมายเหตุ: ข้อมูล 20 เกมอาจไม่เพียงพอสำหรับการประเมิน")
        
        return results_data

def main():
    checker = RealResultsChecker()
    checker.run_real_check()

if __name__ == "__main__":
    main()
