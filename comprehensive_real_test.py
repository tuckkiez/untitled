#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ทดสอบระบบทำนายครบถ้วนกับข้อมูลจริง
- ทำนายทีมชนะ/แพ้/เสมอ
- ทำนายสกอร์แน่นอน
- ทำนายประตูสูง/ต่ำ
- สรุปผล 3 ค่า: ผลการแข่งขัน, ผลต่างประตู, ประตูสูง/ต่ำ
"""

from enhanced_score_predictor import ComprehensiveFootballPredictor
from real_data_example import RealDataPredictor
import pandas as pd
import numpy as np

class ComprehensiveRealTest:
    def __init__(self):
        self.api_token = "052fd4885cf943ad859c89cef542e2e5"
        self.predictor = None
        self.historical_data = None
        
    def load_data(self):
        """โหลดข้อมูลจริง"""
        print("🔄 กำลังโหลดข้อมูลจริงสำหรับการทดสอบครบถ้วน...")
        
        real_predictor = RealDataPredictor(api_key=self.api_token)
        data_2024 = real_predictor.get_premier_league_data(season=2024)
        data_2023 = real_predictor.get_premier_league_data(season=2023)
        
        if data_2024 is None:
            return False
        
        if data_2023 is not None:
            self.historical_data = pd.concat([data_2023, data_2024], ignore_index=True)
        else:
            self.historical_data = data_2024
        
        self.historical_data = self.historical_data.sort_values('date').reset_index(drop=True)
        self.historical_data = self.historical_data.dropna(subset=['home_goals', 'away_goals'])
        
        print(f"✅ โหลดข้อมูลสำเร็จ: {len(self.historical_data)} เกม")
        return True
    
    def test_comprehensive_predictions(self, test_games=50):
        """ทดสอบการทำนายครบถ้วน"""
        print(f"\n🎯 การทดสอบการทำนายครบถ้วน ({test_games} เกม)")
        print("="*100)
        
        if len(self.historical_data) < test_games + 100:
            print("ข้อมูลไม่เพียงพอ")
            return None
        
        # แบ่งข้อมูล
        train_data = self.historical_data.iloc[:-test_games]
        test_data = self.historical_data.iloc[-test_games:]
        
        # เทรนโมเดล
        print("🤖 กำลังเทรนโมเดลครบถ้วน...")
        self.predictor = ComprehensiveFootballPredictor()
        if not self.predictor.train(train_data):
            return None
        
        # ทดสอบ
        results = []
        
        # ตัวนับความถูกต้อง
        result_correct = 0  # ทำนายผลการแข่งขัน
        score_exact_correct = 0  # ทำนายสกอร์แน่นอน
        over_under_correct = 0  # ทำนายสูง/ต่ำ
        goal_diff_correct = 0  # ทำนายผลต่างประตู (ใกล้เคียง ±1)
        
        print(f"{'No.':<3} {'Date':<12} {'Match':<35} {'Actual':<10} {'Pred':<10} {'Score':<10} {'O/U':<6} {'R':<2} {'S':<2} {'O':<2} {'D':<2}")
        print("-" * 100)
        
        for idx, (_, match) in enumerate(test_data.iterrows(), 1):
            # ผลจริง
            actual_home = int(match['home_goals'])
            actual_away = int(match['away_goals'])
            actual_total = actual_home + actual_away
            actual_diff = actual_home - actual_away
            
            # ผลการแข่งขันจริง
            if actual_home > actual_away:
                actual_result = 'Home Win'
                actual_result_short = 'H'
            elif actual_home < actual_away:
                actual_result = 'Away Win'
                actual_result_short = 'A'
            else:
                actual_result = 'Draw'
                actual_result_short = 'D'
            
            # สูง/ต่ำจริง
            actual_over_under = "Over" if actual_total > 2.5 else "Under"
            actual_ou_short = "O" if actual_total > 2.5 else "U"
            
            # ทำนาย
            prediction = self.predictor.predict_comprehensive(
                match['home_team'], match['away_team'], train_data
            )
            
            if prediction:
                # ตรวจสอบความถูกต้อง
                
                # 1. ผลการแข่งขัน
                result_match = prediction['result_prediction'] == actual_result
                if result_match:
                    result_correct += 1
                
                # 2. สกอร์แน่นอน
                score_exact_match = (prediction['home_goals'] == actual_home and 
                                   prediction['away_goals'] == actual_away)
                if score_exact_match:
                    score_exact_correct += 1
                
                # 3. สูง/ต่ำ 2.5 ประตู
                over_under_match = prediction['over_under_2_5'] == actual_over_under
                if over_under_match:
                    over_under_correct += 1
                
                # 4. ผลต่างประตู (ใกล้เคียง ±1)
                pred_diff = prediction['goal_difference']
                goal_diff_match = abs(pred_diff - actual_diff) <= 1
                if goal_diff_match:
                    goal_diff_correct += 1
                
                # แสดงผล
                home_short = match['home_team'].replace(' FC', '').replace(' United', ' Utd')[:15]
                away_short = match['away_team'].replace(' FC', '').replace(' United', ' Utd')[:15]
                match_str = f"{home_short} vs {away_short}"
                
                actual_score_str = f"{actual_home}-{actual_away} ({actual_result_short})"
                pred_result_short = prediction['result_prediction'][0] if prediction['result_prediction'] != 'Draw' else 'D'
                pred_score_str = f"{prediction['predicted_score']} ({pred_result_short})"
                pred_ou_short = "O" if prediction['over_under_2_5'] == "Over" else "U"
                
                # สถานะ
                r_status = "✅" if result_match else "❌"
                s_status = "✅" if score_exact_match else "❌"
                o_status = "✅" if over_under_match else "❌"
                d_status = "✅" if goal_diff_match else "❌"
                
                print(f"{idx:<3} {match['date'].strftime('%Y-%m-%d'):<12} {match_str:<35} "
                      f"{actual_score_str:<10} {pred_score_str:<10} "
                      f"{actual_ou_short}/{pred_ou_short}({actual_total:.1f})<6 "
                      f"{r_status:<2} {s_status:<2} {o_status:<2} {d_status:<2}")
                
                results.append({
                    'match': match_str,
                    'date': match['date'],
                    'actual_result': actual_result,
                    'predicted_result': prediction['result_prediction'],
                    'actual_score': f"{actual_home}-{actual_away}",
                    'predicted_score': prediction['predicted_score'],
                    'actual_total': actual_total,
                    'predicted_total': prediction['total_goals'],
                    'actual_over_under': actual_over_under,
                    'predicted_over_under': prediction['over_under_2_5'],
                    'actual_diff': actual_diff,
                    'predicted_diff': pred_diff,
                    'result_correct': result_match,
                    'score_exact_correct': score_exact_match,
                    'over_under_correct': over_under_match,
                    'goal_diff_correct': goal_diff_match,
                    'confidence': prediction['result_confidence']
                })
        
        # สรุปผล
        total_tests = len(results)
        
        result_accuracy = result_correct / total_tests
        score_accuracy = score_exact_correct / total_tests
        over_under_accuracy = over_under_correct / total_tests
        goal_diff_accuracy = goal_diff_correct / total_tests
        
        print("\n" + "="*100)
        print(f"🏆 สรุปผลการทดสอบครบถ้วน ({total_tests} เกม):")
        print(f"="*60)
        print(f"1️⃣  ทำนายผลการแข่งขัน (ชนะ/แพ้/เสมอ):")
        print(f"    ถูก: {result_correct}/{total_tests} = {result_accuracy:.3f} ({result_accuracy*100:.1f}%)")
        
        print(f"\n2️⃣  ทำนายสกอร์แน่นอน:")
        print(f"    ถูก: {score_exact_correct}/{total_tests} = {score_accuracy:.3f} ({score_accuracy*100:.1f}%)")
        
        print(f"\n3️⃣  ทำนายประตูสูง/ต่ำ (2.5):")
        print(f"    ถูก: {over_under_correct}/{total_tests} = {over_under_accuracy:.3f} ({over_under_accuracy*100:.1f}%)")
        
        print(f"\n4️⃣  ทำนายผลต่างประตู (±1):")
        print(f"    ถูก: {goal_diff_correct}/{total_tests} = {goal_diff_accuracy:.3f} ({goal_diff_accuracy*100:.1f}%)")
        
        # วิเคราะห์เพิ่มเติม
        self.analyze_detailed_results(results)
        
        return {
            'result_accuracy': result_accuracy,
            'score_accuracy': score_accuracy,
            'over_under_accuracy': over_under_accuracy,
            'goal_diff_accuracy': goal_diff_accuracy,
            'total_tests': total_tests,
            'results': results
        }
    
    def analyze_detailed_results(self, results):
        """วิเคราะห์ผลลัพธ์เชิงลึก"""
        print(f"\n🔍 การวิเคราะห์เชิงลึก:")
        print("="*50)
        
        # วิเคราะห์ตามระดับความมั่นใจ
        high_conf_results = [r for r in results if r['confidence'] > 0.6]
        if high_conf_results:
            high_conf_result_acc = sum(r['result_correct'] for r in high_conf_results) / len(high_conf_results)
            print(f"📈 ความแม่นยำเมื่อมั่นใจสูง (>60%): {high_conf_result_acc:.3f} ({len(high_conf_results)} เกม)")
        
        # วิเคราะห์ตามประเภทผลลัพธ์
        home_wins = [r for r in results if r['actual_result'] == 'Home Win']
        away_wins = [r for r in results if r['actual_result'] == 'Away Win']
        draws = [r for r in results if r['actual_result'] == 'Draw']
        
        if home_wins:
            home_acc = sum(r['result_correct'] for r in home_wins) / len(home_wins)
            print(f"🏠 ความแม่นยำ Home Win: {home_acc:.3f} ({len(home_wins)} เกม)")
        
        if away_wins:
            away_acc = sum(r['result_correct'] for r in away_wins) / len(away_wins)
            print(f"✈️  ความแม่นยำ Away Win: {away_acc:.3f} ({len(away_wins)} เกม)")
        
        if draws:
            draw_acc = sum(r['result_correct'] for r in draws) / len(draws)
            print(f"🤝 ความแม่นยำ Draw: {draw_acc:.3f} ({len(draws)} เกม)")
        
        # วิเคราะห์ประตูรวม
        over_games = [r for r in results if r['actual_over_under'] == 'Over']
        under_games = [r for r in results if r['actual_over_under'] == 'Under']
        
        if over_games:
            over_acc = sum(r['over_under_correct'] for r in over_games) / len(over_games)
            print(f"📈 ความแม่นยำ Over 2.5: {over_acc:.3f} ({len(over_games)} เกม)")
        
        if under_games:
            under_acc = sum(r['over_under_correct'] for r in under_games) / len(under_games)
            print(f"📉 ความแม่นยำ Under 2.5: {under_acc:.3f} ({len(under_games)} เกม)")
        
        # เกมที่ทำนายถูกทั้ง 3 ค่า
        triple_correct = [r for r in results if r['result_correct'] and r['over_under_correct'] and r['goal_diff_correct']]
        triple_accuracy = len(triple_correct) / len(results)
        print(f"\n🎯 ทำนายถูกทั้ง 3 ค่า: {len(triple_correct)}/{len(results)} = {triple_accuracy:.3f} ({triple_accuracy*100:.1f}%)")
        
        if triple_correct:
            print(f"🏆 เกมที่ทำนายถูกทั้ง 3 ค่า:")
            for r in triple_correct[:5]:  # แสดง 5 เกมแรก
                print(f"   ✅ {r['match']}: {r['actual_score']} ({r['actual_result']}) - {r['actual_over_under']}")
    
    def predict_sample_matches(self):
        """ทำนายเกมตัวอย่าง"""
        if not self.predictor:
            return
        
        print(f"\n🎮 ตัวอย่างการทำนายครบถ้วน:")
        print("="*80)
        
        sample_matches = [
            ('Arsenal FC', 'Chelsea FC'),
            ('Manchester City FC', 'Liverpool FC'),
            ('Manchester United FC', 'Tottenham Hotspur FC')
        ]
        
        for home, away in sample_matches:
            result = self.predictor.predict_comprehensive(home, away, self.historical_data)
            if result:
                print(f"\n⚽ {result['match']}")
                print(f"   🏆 ผลการแข่งขัน: {result['result_prediction']} (มั่นใจ {result['result_confidence']:.3f})")
                print(f"   📊 สกอร์ที่คาด: {result['predicted_score']}")
                print(f"   📈 ประตูรวม: {result['total_goals']} ({result['over_under_2_5']})")
                print(f"   📏 ผลต่างประตู: {result['goal_difference']:+d}")
                
                print(f"   🎲 ความน่าจะเป็น:")
                for outcome, prob in result['result_probabilities'].items():
                    print(f"      {outcome}: {prob:.3f} ({prob*100:.1f}%)")
    
    def run_comprehensive_test(self):
        """รันการทดสอบครบถ้วน"""
        print("🏆 ระบบทดสอบการทำนายฟุตบอลครบถ้วน")
        print("🎯 ทำนาย 3 ค่า: ผลการแข่งขัน + สกอร์ + ประตูสูง/ต่ำ")
        print("="*80)
        
        # โหลดข้อมูล
        if not self.load_data():
            return
        
        # ทดสอบการทำนายครบถ้วน
        results = self.test_comprehensive_predictions(test_games=50)
        
        if results:
            # ทำนายตัวอย่าง
            self.predict_sample_matches()
            
            # สรุปสุดท้าย
            print(f"\n🏆 สรุปการทดสอบครบถ้วน:")
            print(f"✅ ทำนายผลการแข่งขัน: {results['result_accuracy']*100:.1f}%")
            print(f"⚽ ทำนายสกอร์แน่นอน: {results['score_accuracy']*100:.1f}%")
            print(f"📈 ทำนายสูง/ต่ำ: {results['over_under_accuracy']*100:.1f}%")
            print(f"📊 ทำนายผลต่างประตู: {results['goal_diff_accuracy']*100:.1f}%")
            
            if results['result_accuracy'] > 0.5:
                print(f"\n🎉 ยอดเยี่ยม! ระบบให้ความแม่นยำสูงในการทำนายผลการแข่งขัน")
            
            if results['over_under_accuracy'] > 0.55:
                print(f"🔥 ระบบทำนายประตูสูง/ต่ำได้ดีมาก!")
        
        return results

def main():
    tester = ComprehensiveRealTest()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
