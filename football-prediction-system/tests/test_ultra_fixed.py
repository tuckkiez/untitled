#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ทดสอบระบบ Ultra Advanced Predictor - Fixed Version
เปรียบเทียบความแม่นยำกับระบบเดิม
"""

from ultra_predictor_fixed import UltraAdvancedPredictor
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class UltraAdvancedTester:
    def __init__(self):
        self.predictor = UltraAdvancedPredictor(
            api_key="052fd4885cf943ad859c89cef542e2e5"
        )
        
    def comprehensive_backtest(self, test_games=20):
        """ทดสอบย้อนหลังแบบครบถ้วน"""
        print("🚀 การทดสอบ Ultra Advanced Predictor - ปรับปรุงแล้ว")
        print("="*100)
        
        # โหลดข้อมูล
        print("📊 กำลังโหลดข้อมูล...")
        data = self.predictor.load_premier_league_data()
        
        if len(data) < test_games + 100:
            print(f"⚠️ ข้อมูลไม่เพียงพอ (มี {len(data)} เกม)")
            return
        
        # แบ่งข้อมูล
        train_data = data[:-test_games].copy()
        test_data = data[-test_games:].copy()
        
        print(f"🎯 เทรนด้วย {len(train_data)} เกม, ทดสอบ {len(test_data)} เกม")
        
        # เทรนโมเดล
        print(f"\n🤖 กำลังเทรนโมเดล Ultra Advanced...")
        training_results = self.predictor.train_ensemble_models(train_data)
        
        print(f"\n📋 รายละเอียดการทดสอบ {test_games} เกมล่าสุด")
        print("="*100)
        print(f"{'No.':<3} {'Date':<12} {'Match':<40} {'Score':<8} {'Actual':<10} {'Predicted':<10} {'Conf':<6} {'✓/✗':<3}")
        print("-"*100)
        
        results = []
        correct_predictions = 0
        high_confidence_correct = 0
        high_confidence_total = 0
        
        for idx, (_, match) in enumerate(test_data.iterrows(), 1):
            # ทำนาย
            prediction = self.predictor.predict_match_ultra(
                match['home_team'], 
                match['away_team'],
                match['date']
            )
            
            if not prediction:
                print(f"   ⚠️ ไม่สามารถทำนายเกม {idx} ได้")
                continue
            
            # ผลจริง
            home_goals = int(match['home_goals'])
            away_goals = int(match['away_goals'])
            score_str = f"{home_goals}-{away_goals}"
            
            if home_goals > away_goals:
                actual_result = 'Home Win'
                actual_short = 'H'
            elif home_goals == away_goals:
                actual_result = 'Draw'
                actual_short = 'D'
            else:
                actual_result = 'Away Win'
                actual_short = 'A'
            
            # เปรียบเทียบ
            predicted_result = prediction['prediction']
            pred_short = {'Home Win': 'H', 'Draw': 'D', 'Away Win': 'A'}[predicted_result]
            confidence = prediction['confidence']
            
            is_correct = predicted_result == actual_result
            if is_correct:
                correct_predictions += 1
                status = "✅"
            else:
                status = "❌"
            
            # ติดตามความแม่นยำเมื่อมั่นใจสูง
            if confidence > 0.6:
                high_confidence_total += 1
                if is_correct:
                    high_confidence_correct += 1
            
            # แสดงผล
            match_str = f"{match['home_team'][:18]} vs {match['away_team'][:18]}"
            date_str = pd.to_datetime(match['date']).strftime('%m-%d')
            
            print(f"{idx:<3} {date_str:<12} {match_str:<40} {score_str:<8} "
                  f"{actual_short:<10} {pred_short:<10} {confidence:<6.3f} {status:<3}")
            
            # เก็บข้อมูล
            results.append({
                'match_num': idx,
                'date': match['date'],
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'home_goals': home_goals,
                'away_goals': away_goals,
                'actual_result': actual_result,
                'predicted_result': predicted_result,
                'confidence': confidence,
                'is_correct': is_correct,
                'probabilities': prediction['probabilities'],
                'model_predictions': prediction['model_predictions']
            })
        
        # วิเคราะห์ผลลัพธ์
        self.analyze_ultra_results(results, correct_predictions, len(results), 
                                 high_confidence_correct, high_confidence_total)
        
        return results
    
    def analyze_ultra_results(self, results, correct_predictions, total_games, 
                            high_conf_correct, high_conf_total):
        """วิเคราะห์ผลลัพธ์ Ultra Advanced"""
        print("\n" + "="*100)
        print("📊 การวิเคราะห์ผลลัพธ์ Ultra Advanced")
        print("="*100)
        
        # ความแม่นยำโดยรวม
        overall_accuracy = correct_predictions / total_games if total_games > 0 else 0
        print(f"🎯 ความแม่นยำโดยรวม: {correct_predictions}/{total_games} = {overall_accuracy:.1%}")
        
        # ความแม่นยำเมื่อมั่นใจสูง
        if high_conf_total > 0:
            high_conf_accuracy = high_conf_correct / high_conf_total
            print(f"🔥 ความแม่นยำเมื่อมั่นใจสูง (>60%): {high_conf_correct}/{high_conf_total} = {high_conf_accuracy:.1%}")
        
        # วิเคราะห์ตามประเภทผล
        result_types = ['Home Win', 'Draw', 'Away Win']
        result_analysis = {result_type: {'correct': 0, 'total': 0, 'predicted': 0} 
                          for result_type in result_types}
        
        for result in results:
            actual = result['actual_result']
            predicted = result['predicted_result']
            
            result_analysis[actual]['total'] += 1
            result_analysis[predicted]['predicted'] += 1
            
            if actual == predicted:
                result_analysis[actual]['correct'] += 1
        
        print(f"\n📈 ความแม่นยำตามประเภทผล:")
        for result_type in result_types:
            stats = result_analysis[result_type]
            if stats['total'] > 0:
                accuracy = stats['correct'] / stats['total']
                precision = stats['correct'] / stats['predicted'] if stats['predicted'] > 0 else 0
                print(f"   {result_type:10}: {stats['correct']:2d}/{stats['total']:2d} = {accuracy:.1%} "
                      f"(Precision: {precision:.1%}, ทำนาย: {stats['predicted']} เกม)")
        
        # วิเคราะห์ตามระดับความมั่นใจ
        confidence_ranges = [(0.0, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]
        confidence_labels = ['ต่ำ', 'ปานกลาง', 'สูง', 'สูงมาก']
        
        print(f"\n🎲 ความแม่นยำตามระดับความมั่นใจ:")
        for (min_conf, max_conf), label in zip(confidence_ranges, confidence_labels):
            filtered_results = [r for r in results 
                              if min_conf <= r['confidence'] < max_conf]
            
            if filtered_results:
                correct_in_range = sum(1 for r in filtered_results if r['is_correct'])
                accuracy = correct_in_range / len(filtered_results)
                avg_conf = np.mean([r['confidence'] for r in filtered_results])
                print(f"   {label:10} ({min_conf:.1f}-{max_conf:.1f}): {correct_in_range:2d}/{len(filtered_results):2d} = {accuracy:.1%} "
                      f"(เฉลี่ย: {avg_conf:.3f})")
        
        # เปรียบเทียบโมเดลแต่ละตัว
        print(f"\n🤖 การเปรียบเทียบโมเดลแต่ละตัว:")
        if results and 'model_predictions' in results[0]:
            model_names = list(results[0]['model_predictions'].keys())
            
            for model_name in model_names:
                model_correct = 0
                model_total = 0
                
                for r in results:
                    if model_name in r['model_predictions']:
                        model_pred = r['model_predictions'][model_name]
                        model_total += 1
                        if model_pred == r['actual_result']:
                            model_correct += 1
                
                if model_total > 0:
                    model_accuracy = model_correct / model_total
                    weight = self.predictor.ensemble_weights.get(model_name, 0)
                    print(f"   {model_name:18}: {model_correct:2d}/{model_total:2d} = {model_accuracy:.1%} (น้ำหนัก: {weight:.3f})")
        
        # สถิติเพิ่มเติม
        if results:
            avg_confidence = np.mean([r['confidence'] for r in results])
            
            print(f"\n📊 สถิติเพิ่มเติม:")
            print(f"   ความมั่นใจเฉลี่ย: {avg_confidence:.3f}")
            print(f"   Features ที่ใช้: {self.predictor.selected_feature_names[:5]}... (รวม {len(self.predictor.selected_feature_names)} features)")
        
        # เปรียบเทียบกับระบบเดิม
        print(f"\n🆚 เปรียบเทียบกับระบบเดิม:")
        print(f"   ระบบเดิม (Advanced ML): ~45% ความแม่นยำ")
        print(f"   ระบบใหม่ (Ultra Advanced): {overall_accuracy:.1%} ความแม่นยำ")
        
        improvement = (overall_accuracy - 0.45) * 100
        if improvement > 0:
            print(f"   🎉 ปรับปรุงขึ้น: +{improvement:.1f} percentage points!")
        elif improvement < 0:
            print(f"   ⚠️ ลดลง: {improvement:.1f} percentage points")
        else:
            print(f"   ➡️ ความแม่นยำเท่าเดิม")
    
    def demo_ultra_predictions(self):
        """แสดงตัวอย่างการทำนาย Ultra Advanced"""
        print(f"\n🎮 ตัวอย่างการทำนาย Ultra Advanced")
        print("="*100)
        
        demo_matches = [
            ("Arsenal", "Chelsea"),
            ("Manchester City", "Liverpool"), 
            ("Manchester United", "Tottenham"),
            ("Brighton", "Newcastle"),
            ("Aston Villa", "West Ham")
        ]
        
        for home, away in demo_matches:
            pred = self.predictor.predict_match_ultra(home, away)
            
            if pred:
                print(f"\n⚽ {home} vs {away}")
                print(f"   🏆 ทำนาย: {pred['prediction']} (มั่นใจ {pred['confidence']:.1%})")
                print(f"   🤝 ความเห็นตรงกันของโมเดล: {pred['model_agreement']:.1%}")
                print(f"   📊 ความน่าจะเป็น:")
                for outcome, prob in pred['probabilities'].items():
                    print(f"      {outcome:10}: {prob:.1%}")
                print(f"   🤖 การทำนายของแต่ละโมเดล:")
                for model, prediction in pred['model_predictions'].items():
                    weight = pred['ensemble_weights'].get(model, 0)
                    print(f"      {model:3}: {prediction} (น้ำหนัก: {weight:.3f})")

# Main execution
if __name__ == "__main__":
    tester = UltraAdvancedTester()
    
    # รันการทดสอบครบถ้วน
    results = tester.comprehensive_backtest(test_games=20)
    
    # แสดงตัวอย่างการทำนาย
    tester.demo_ultra_predictions()
    
    print(f"\n🎉 การทดสอบ Ultra Advanced เสร็จสิ้น!")
    print("="*100)
