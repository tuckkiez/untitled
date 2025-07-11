#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ทดสอบระบบทำนายราคาต่อรองกับข้อมูลจริง
- ทำนายผลการแข่งขัน (ชนะ/แพ้/เสมอ)
- ทำนายราคาต่อรอง (ต่อ/รอง)
- ทำนายประตูสูง/ต่ำ
สรุปผล 3 ค่า: ผลการแข่งขัน, ราคาต่อรอง, สูง/ต่ำ
"""

from handicap_predictor import HandicapFootballPredictor
from real_data_example import RealDataPredictor
import pandas as pd
import numpy as np

class HandicapRealTest:
    def __init__(self):
        self.api_token = "052fd4885cf943ad859c89cef542e2e5"
        self.predictor = None
        self.historical_data = None
        
    def load_data(self):
        """โหลดข้อมูลจริง"""
        print("🔄 กำลังโหลดข้อมูลจริงสำหรับการทดสอบราคาต่อรอง...")
        
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
    
    def calculate_actual_handicap_result(self, home_goals, away_goals, handicap_line):
        """คำนวณผลราคาต่อรองจริง"""
        actual_diff = home_goals - away_goals
        adjusted_diff = actual_diff - handicap_line
        
        if handicap_line >= 0:  # ทีมเหย้าต่อ
            if adjusted_diff > 0:
                return "ต่อ"
            elif adjusted_diff < 0:
                return "รอง"
            else:
                return "คืนเงิน"
        else:  # ทีมเยือนต่อ
            if adjusted_diff < 0:
                return "ต่อ"
            elif adjusted_diff > 0:
                return "รอง"
            else:
                return "คืนเงิน"
    
    def test_handicap_predictions(self, test_games=50):
        """ทดสอบการทำนายราคาต่อรอง"""
        print(f"\n🎯 การทดสอบการทำนายราคาต่อรอง ({test_games} เกม)")
        print("="*100)
        
        if len(self.historical_data) < test_games + 100:
            print("ข้อมูลไม่เพียงพอ")
            return None
        
        # แบ่งข้อมูล
        train_data = self.historical_data.iloc[:-test_games]
        test_data = self.historical_data.iloc[-test_games:]
        
        # เทรนโมเดล
        print("🤖 กำลังเทรนโมเดลราคาต่อรอง...")
        self.predictor = HandicapFootballPredictor()
        if not self.predictor.train(train_data):
            return None
        
        # ทดสอบ
        results = []
        
        # ตัวนับความถูกต้อง
        result_correct = 0  # ทำนายผลการแข่งขัน
        handicap_correct = 0  # ทำนายราคาต่อรอง
        over_under_correct = 0  # ทำนายสูง/ต่ำ
        triple_correct = 0  # ทำนายถูกทั้ง 3 ค่า
        
        print(f"{'No.':<3} {'Date':<12} {'Match':<35} {'Score':<8} {'Result':<6} {'H-Cap':<8} {'O/U':<6} {'R':<2} {'H':<2} {'O':<2}")
        print("-" * 100)
        
        for idx, (_, match) in enumerate(test_data.iterrows(), 1):
            # ผลจริง
            actual_home = int(match['home_goals'])
            actual_away = int(match['away_goals'])
            actual_total = actual_home + actual_away
            
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
            
            # ทำนาย
            prediction = self.predictor.predict_handicap(
                match['home_team'], match['away_team'], train_data
            )
            
            if prediction:
                # คำนวณผลจริงของราคาต่อรอง
                actual_handicap = self.calculate_actual_handicap_result(
                    actual_home, actual_away, prediction['handicap_line']
                )
                
                # สูง/ต่ำจริง
                actual_over_under = "Over" if actual_total > prediction['over_under_line'] else "Under"
                
                # ตรวจสอบความถูกต้อง
                
                # 1. ผลการแข่งขัน
                result_match = prediction['result_prediction'] == actual_result
                if result_match:
                    result_correct += 1
                
                # 2. ราคาต่อรอง
                handicap_match = prediction['handicap_prediction'] == actual_handicap
                if handicap_match:
                    handicap_correct += 1
                
                # 3. สูง/ต่ำ
                over_under_match = prediction['over_under_prediction'] == actual_over_under
                if over_under_match:
                    over_under_correct += 1
                
                # 4. ทั้ง 3 ค่า
                if result_match and handicap_match and over_under_match:
                    triple_correct += 1
                
                # แสดงผล
                home_short = match['home_team'].replace(' FC', '').replace(' United', ' Utd')[:15]
                away_short = match['away_team'].replace(' FC', '').replace(' United', ' Utd')[:15]
                match_str = f"{home_short} vs {away_short}"
                
                score_str = f"{actual_home}-{actual_away}"
                
                # ราคาต่อรอง
                handicap_str = f"{prediction['handicap_line']:+.1f}"
                if prediction['handicap_line'] >= 0:
                    handicap_display = f"H{handicap_str}"
                else:
                    handicap_display = f"A{abs(prediction['handicap_line']):.1f}"
                
                # สูง/ต่ำ
                ou_str = f"{prediction['over_under_line']:.1f}"
                
                # สถานะ
                r_status = "✅" if result_match else "❌"
                h_status = "✅" if handicap_match else "❌"
                o_status = "✅" if over_under_match else "❌"
                
                print(f"{idx:<3} {match['date'].strftime('%Y-%m-%d'):<12} {match_str:<35} "
                      f"{score_str:<8} {actual_result_short:<6} {handicap_display:<8} {ou_str:<6} "
                      f"{r_status:<2} {h_status:<2} {o_status:<2}")
                
                results.append({
                    'match': match_str,
                    'date': match['date'],
                    'actual_result': actual_result,
                    'predicted_result': prediction['result_prediction'],
                    'actual_score': f"{actual_home}-{actual_away}",
                    'handicap_line': prediction['handicap_line'],
                    'actual_handicap': actual_handicap,
                    'predicted_handicap': prediction['handicap_prediction'],
                    'over_under_line': prediction['over_under_line'],
                    'actual_over_under': actual_over_under,
                    'predicted_over_under': prediction['over_under_prediction'],
                    'result_correct': result_match,
                    'handicap_correct': handicap_match,
                    'over_under_correct': over_under_match,
                    'triple_correct': result_match and handicap_match and over_under_match,
                    'confidence': prediction['result_confidence']
                })
        
        # สรุปผล
        total_tests = len(results)
        
        result_accuracy = result_correct / total_tests
        handicap_accuracy = handicap_correct / total_tests
        over_under_accuracy = over_under_correct / total_tests
        triple_accuracy = triple_correct / total_tests
        
        print("\n" + "="*100)
        print(f"🏆 สรุปผลการทดสอบราคาต่อรอง ({total_tests} เกม):")
        print(f"="*60)
        print(f"1️⃣  ทำนายผลการแข่งขัน (ชนะ/แพ้/เสมอ):")
        print(f"    ถูก: {result_correct}/{total_tests} = {result_accuracy:.3f} ({result_accuracy*100:.1f}%)")
        
        print(f"\n2️⃣  ทำนายราคาต่อรอง (ต่อ/รอง):")
        print(f"    ถูก: {handicap_correct}/{total_tests} = {handicap_accuracy:.3f} ({handicap_accuracy*100:.1f}%)")
        
        print(f"\n3️⃣  ทำนายประตูสูง/ต่ำ:")
        print(f"    ถูก: {over_under_correct}/{total_tests} = {over_under_accuracy:.3f} ({over_under_accuracy*100:.1f}%)")
        
        print(f"\n🎯 ทำนายถูกทั้ง 3 ค่า:")
        print(f"    ถูก: {triple_correct}/{total_tests} = {triple_accuracy:.3f} ({triple_accuracy*100:.1f}%)")
        
        # วิเคราะห์เพิ่มเติม
        self.analyze_handicap_results(results)
        
        return {
            'result_accuracy': result_accuracy,
            'handicap_accuracy': handicap_accuracy,
            'over_under_accuracy': over_under_accuracy,
            'triple_accuracy': triple_accuracy,
            'total_tests': total_tests,
            'results': results
        }
    
    def analyze_handicap_results(self, results):
        """วิเคราะห์ผลลัพธ์ราคาต่อรอง"""
        print(f"\n🔍 การวิเคราะห์ราคาต่อรองเชิงลึก:")
        print("="*50)
        
        # วิเคราะห์ตามระดับความมั่นใจ
        high_conf_results = [r for r in results if r['confidence'] > 0.6]
        if high_conf_results:
            high_conf_result_acc = sum(r['result_correct'] for r in high_conf_results) / len(high_conf_results)
            high_conf_handicap_acc = sum(r['handicap_correct'] for r in high_conf_results) / len(high_conf_results)
            print(f"📈 เมื่อมั่นใจสูง (>60%) - {len(high_conf_results)} เกม:")
            print(f"   ผลการแข่งขัน: {high_conf_result_acc:.3f} ({high_conf_result_acc*100:.1f}%)")
            print(f"   ราคาต่อรอง: {high_conf_handicap_acc:.3f} ({high_conf_handicap_acc*100:.1f}%)")
        
        # วิเคราะห์ตามประเภทราคาต่อรอง
        home_handicap = [r for r in results if r['handicap_line'] > 0]
        away_handicap = [r for r in results if r['handicap_line'] < 0]
        even_handicap = [r for r in results if r['handicap_line'] == 0]
        
        if home_handicap:
            home_h_acc = sum(r['handicap_correct'] for r in home_handicap) / len(home_handicap)
            print(f"🏠 ทีมเหย้าต่อ: {home_h_acc:.3f} ({len(home_handicap)} เกม)")
        
        if away_handicap:
            away_h_acc = sum(r['handicap_correct'] for r in away_handicap) / len(away_handicap)
            print(f"✈️  ทีมเยือนต่อ: {away_h_acc:.3f} ({len(away_handicap)} เกม)")
        
        if even_handicap:
            even_h_acc = sum(r['handicap_correct'] for r in even_handicap) / len(even_handicap)
            print(f"⚖️  เสมอ: {even_h_acc:.3f} ({len(even_handicap)} เกม)")
        
        # วิเคราะห์ตามเส้นสูง/ต่ำ
        over_25_games = [r for r in results if r['over_under_line'] == 2.5]
        over_35_games = [r for r in results if r['over_under_line'] == 3.5]
        
        if over_25_games:
            over_25_acc = sum(r['over_under_correct'] for r in over_25_games) / len(over_25_games)
            print(f"📊 เส้น 2.5: {over_25_acc:.3f} ({len(over_25_games)} เกม)")
        
        if over_35_games:
            over_35_acc = sum(r['over_under_correct'] for r in over_35_games) / len(over_35_games)
            print(f"📊 เส้น 3.5: {over_35_acc:.3f} ({len(over_35_games)} เกม)")
        
        # เกมที่ทำนายถูกทั้ง 3 ค่า
        triple_correct = [r for r in results if r['triple_correct']]
        if triple_correct:
            print(f"\n🏆 เกมที่ทำนายถูกทั้ง 3 ค่า ({len(triple_correct)} เกม):")
            for r in triple_correct[:5]:  # แสดง 5 เกมแรก
                handicap_desc = f"ต่อ {r['handicap_line']}" if r['handicap_line'] > 0 else f"รอง {abs(r['handicap_line'])}" if r['handicap_line'] < 0 else "เสมอ"
                print(f"   ✅ {r['match']}: {r['actual_score']} - {r['actual_result']} - {handicap_desc} - {r['actual_over_under']}")
    
    def predict_sample_matches(self):
        """ทำนายเกมตัวอย่าง"""
        if not self.predictor:
            return
        
        print(f"\n🎮 ตัวอย่างการทำนายราคาต่อรอง:")
        print("="*80)
        
        sample_matches = [
            ('Arsenal FC', 'Chelsea FC'),
            ('Manchester City FC', 'Liverpool FC'),
            ('Manchester United FC', 'Tottenham Hotspur FC')
        ]
        
        for home, away in sample_matches:
            result = self.predictor.predict_handicap(home, away, self.historical_data)
            if result:
                print(f"\n⚽ {result['match']}")
                print(f"   🏆 ผลการแข่งขัน: {result['result_prediction']} (มั่นใจ {result['result_confidence']:.3f})")
                
                # แสดงราคาต่อรอง
                handicap_line = result['handicap_line']
                if handicap_line > 0:
                    handicap_desc = f"ทีมเหย้าต่อ {handicap_line}"
                elif handicap_line < 0:
                    handicap_desc = f"ทีมเยือนต่อ {abs(handicap_line)}"
                else:
                    handicap_desc = "เสมอ"
                
                print(f"   🎯 ราคาต่อรอง: {handicap_desc} → {result['handicap_prediction']}")
                print(f"   📊 สูง/ต่ำ: {result['over_under_line']} → {result['over_under_prediction']}")
                print(f"   📈 คาดการณ์: ผลต่าง {result['predicted_goal_difference']:+.1f}, รวม {result['predicted_total_goals']:.1f} ประตู")
                
                print(f"   🎲 ความน่าจะเป็น:")
                for outcome, prob in result['result_probabilities'].items():
                    print(f"      {outcome}: {prob:.3f} ({prob*100:.1f}%)")
    
    def run_handicap_test(self):
        """รันการทดสอบราคาต่อรอง"""
        print("🏆 ระบบทดสอบการทำนายราคาต่อรองฟุตบอล")
        print("🎯 ทำนาย 3 ค่า: ผลการแข่งขัน + ราคาต่อรอง + สูง/ต่ำ")
        print("="*80)
        
        # โหลดข้อมูล
        if not self.load_data():
            return
        
        # ทดสอบการทำนายราคาต่อรอง
        results = self.test_handicap_predictions(test_games=50)
        
        if results:
            # ทำนายตัวอย่าง
            self.predict_sample_matches()
            
            # สรุปสุดท้าย
            print(f"\n🏆 สรุปการทดสอบราคาต่อรอง:")
            print(f"✅ ทำนายผลการแข่งขัน: {results['result_accuracy']*100:.1f}%")
            print(f"🎯 ทำนายราคาต่อรอง: {results['handicap_accuracy']*100:.1f}%")
            print(f"📈 ทำนายสูง/ต่ำ: {results['over_under_accuracy']*100:.1f}%")
            print(f"🏆 ทำนายถูกทั้ง 3 ค่า: {results['triple_accuracy']*100:.1f}%")
            
            if results['handicap_accuracy'] > 0.5:
                print(f"\n🎉 ยอดเยี่ยม! ระบบทำนายราคาต่อรองได้ดี")
            
            if results['triple_accuracy'] > 0.15:
                print(f"🔥 ระบบทำนายถูกทั้ง 3 ค่าได้ดีมาก!")
        
        return results

def main():
    tester = HandicapRealTest()
    tester.run_handicap_test()

if __name__ == "__main__":
    main()
