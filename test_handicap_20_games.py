#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ทดสอบระบบ Handicap เฉพาะ 20 นัดล่าสุด
- ทำนายทีมต่อรอง (Handicap)
- ทำนายสูง/ต่ำ (Over/Under)
- ทำนายผลการแข่งขัน
"""

from ultra_predictor_fixed import UltraAdvancedPredictor
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class HandicapTester:
    def __init__(self):
        self.predictor = UltraAdvancedPredictor(
            api_key="052fd4885cf943ad859c89cef542e2e5"
        )
        
    def calculate_handicap_line(self, home_elo, away_elo, home_form, away_form):
        """คำนวณเส้น Handicap"""
        # คำนวณความแตกต่างความแข็งแกร่ง
        elo_diff = home_elo - away_elo
        form_diff = home_form - away_form
        
        # รวมปัจจัย
        total_diff = (elo_diff / 100) + (form_diff * 2) + 0.3  # home advantage
        
        # แปลงเป็นเส้น handicap
        if total_diff >= 1.5:
            return "H-1.5"  # ทีมเหย้าต่อ 1.5
        elif total_diff >= 1.0:
            return "H-1.0"  # ทีมเหย้าต่อ 1.0
        elif total_diff >= 0.5:
            return "H-0.5"  # ทีมเหย้าต่อ 0.5
        elif total_diff >= -0.5:
            return "H+0.0"  # เสมอ
        elif total_diff >= -1.0:
            return "A-0.5"  # ทีมเยือนต่อ 0.5
        elif total_diff >= -1.5:
            return "A-1.0"  # ทีมเยือนต่อ 1.0
        else:
            return "A-1.5"  # ทีมเยือนต่อ 1.5
    
    def calculate_over_under_line(self, home_goals_avg, away_goals_avg, home_concede_avg, away_concede_avg):
        """คำนวณเส้น Over/Under"""
        expected_goals = (home_goals_avg + away_concede_avg + away_goals_avg + home_concede_avg) / 2
        
        if expected_goals >= 3.5:
            return "3.5"
        elif expected_goals >= 2.5:
            return "2.5"
        else:
            return "2.0"
    
    def check_handicap_result(self, handicap_line, home_goals, away_goals):
        """ตรวจสอบผล Handicap"""
        goal_diff = home_goals - away_goals
        
        if handicap_line == "H-1.5":
            return "ต่อ" if goal_diff >= 2 else "รอง"
        elif handicap_line == "H-1.0":
            return "ต่อ" if goal_diff >= 2 else ("ครึ่งรอง" if goal_diff == 1 else "รอง")
        elif handicap_line == "H-0.5":
            return "ต่อ" if goal_diff >= 1 else "รอง"
        elif handicap_line == "H+0.0":
            return "ต่อ" if goal_diff >= 1 else ("เสมอ" if goal_diff == 0 else "รอง")
        elif handicap_line == "A-0.5":
            return "รอง" if goal_diff <= -1 else "ต่อ"
        elif handicap_line == "A-1.0":
            return "รอง" if goal_diff <= -2 else ("ครึ่งต่อ" if goal_diff == -1 else "ต่อ")
        elif handicap_line == "A-1.5":
            return "รอง" if goal_diff <= -2 else "ต่อ"
        
        return "เสมอ"
    
    def check_over_under_result(self, ou_line, total_goals):
        """ตรวจสอบผล Over/Under"""
        line_value = float(ou_line)
        
        if total_goals > line_value:
            return "Over"
        elif total_goals < line_value:
            return "Under"
        else:
            return "เสมอ"
    
    def handicap_backtest(self, test_games=20):
        """ทดสอบ Handicap ย้อนหลัง"""
        print("🎲 การทดสอบ Handicap 20 นัดล่าสุด")
        print("="*120)
        
        # โหลดข้อมูล
        data = self.predictor.load_premier_league_data()
        
        if len(data) < test_games + 100:
            print(f"⚠️ ข้อมูลไม่เพียงพอ")
            return
        
        # แบ่งข้อมูล
        train_data = data[:-test_games].copy()
        test_data = data[-test_games:].copy()
        
        print(f"🎯 เทรนด้วย {len(train_data)} เกม, ทดสอบ {len(test_data)} เกม")
        
        # เทรนโมเดล
        print(f"\n🤖 กำลังเทรนโมเดลสำหรับ Handicap...")
        training_results = self.predictor.train_ensemble_models(train_data)
        
        print(f"\n📋 รายละเอียดการทดสอบ Handicap 20 เกมล่าสุด")
        print("="*120)
        print(f"{'No.':<3} {'Date':<10} {'Match':<35} {'Score':<8} {'Result':<6} {'H-Cap':<8} {'O/U':<6} {'R':<2} {'H':<2} {'O':<2}")
        print("-"*120)
        
        results = []
        correct_results = 0
        correct_handicaps = 0
        correct_over_unders = 0
        correct_all_three = 0
        
        for idx, (_, match) in enumerate(test_data.iterrows(), 1):
            # ทำนายผลการแข่งขัน
            prediction = self.predictor.predict_match_ultra(
                match['home_team'], 
                match['away_team'],
                match['date']
            )
            
            if not prediction:
                continue
            
            # ข้อมูลจริง
            home_goals = int(match['home_goals'])
            away_goals = int(match['away_goals'])
            total_goals = home_goals + away_goals
            score_str = f"{home_goals}-{away_goals}"
            
            # ผลจริง
            if home_goals > away_goals:
                actual_result = 'H'
            elif home_goals == away_goals:
                actual_result = 'D'
            else:
                actual_result = 'A'
            
            # ทำนายผล
            predicted_result = prediction['prediction']
            pred_result = {'Home Win': 'H', 'Draw': 'D', 'Away Win': 'A'}[predicted_result]
            
            # คำนวณ Handicap และ O/U
            # ใช้ข้อมูลจาก ELO และ form (สมมติ)
            home_elo = 1500 + np.random.normal(0, 100)  # จำลอง
            away_elo = 1500 + np.random.normal(0, 100)
            home_form = np.random.uniform(0, 3)
            away_form = np.random.uniform(0, 3)
            
            # คำนวณเส้น
            handicap_line = self.calculate_handicap_line(home_elo, away_elo, home_form, away_form)
            ou_line = self.calculate_over_under_line(1.5, 1.2, 1.3, 1.4)  # จำลอง
            
            # ผล Handicap และ O/U จริง
            handicap_result = self.check_handicap_result(handicap_line, home_goals, away_goals)
            ou_result = self.check_over_under_result(ou_line, total_goals)
            
            # ทำนาย Handicap (จำลอง)
            if "H-" in handicap_line:
                predicted_handicap = "ต่อ" if prediction['probabilities']['Home Win'] > 0.5 else "รอง"
            elif "A-" in handicap_line:
                predicted_handicap = "รอง" if prediction['probabilities']['Away Win'] > 0.5 else "ต่อ"
            else:
                predicted_handicap = "ต่อ" if prediction['probabilities']['Home Win'] > prediction['probabilities']['Away Win'] else "รอง"
            
            # ทำนาย O/U (จำลอง)
            expected_total = 2.5 + (prediction['confidence'] - 0.5)  # จำลอง
            predicted_ou = "Over" if expected_total > float(ou_line) else "Under"
            
            # ตรวจสอบความถูกต้อง
            result_correct = pred_result == actual_result
            handicap_correct = predicted_handicap == handicap_result
            ou_correct = predicted_ou == ou_result
            
            if result_correct:
                correct_results += 1
            if handicap_correct:
                correct_handicaps += 1
            if ou_correct:
                correct_over_unders += 1
            if result_correct and handicap_correct and ou_correct:
                correct_all_three += 1
            
            # สัญลักษณ์
            r_symbol = "✅" if result_correct else "❌"
            h_symbol = "✅" if handicap_correct else "❌"
            o_symbol = "✅" if ou_correct else "❌"
            
            # แสดงผล
            match_str = f"{match['home_team'][:15]} vs {match['away_team'][:15]}"
            date_str = pd.to_datetime(match['date']).strftime('%m-%d')
            
            print(f"{idx:<3} {date_str:<10} {match_str:<35} {score_str:<8} {actual_result:<6} "
                  f"{handicap_line:<8} {ou_line:<6} {r_symbol:<2} {h_symbol:<2} {o_symbol:<2}")
            
            # เก็บข้อมูล
            results.append({
                'match_num': idx,
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'home_goals': home_goals,
                'away_goals': away_goals,
                'actual_result': actual_result,
                'predicted_result': pred_result,
                'handicap_line': handicap_line,
                'handicap_result': handicap_result,
                'predicted_handicap': predicted_handicap,
                'ou_line': ou_line,
                'ou_result': ou_result,
                'predicted_ou': predicted_ou,
                'result_correct': result_correct,
                'handicap_correct': handicap_correct,
                'ou_correct': ou_correct
            })
        
        # สรุปผลลัพธ์
        self.analyze_handicap_results(results, correct_results, correct_handicaps, 
                                    correct_over_unders, correct_all_three, len(results))
        
        return results
    
    def analyze_handicap_results(self, results, correct_results, correct_handicaps, 
                               correct_over_unders, correct_all_three, total_games):
        """วิเคราะห์ผล Handicap"""
        print("\n" + "="*120)
        print("📊 สรุปผลการทดสอบ Handicap")
        print("="*120)
        
        # ความแม่นยำแต่ละประเภท
        result_accuracy = correct_results / total_games
        handicap_accuracy = correct_handicaps / total_games
        ou_accuracy = correct_over_unders / total_games
        all_three_accuracy = correct_all_three / total_games
        
        print(f"🎯 ความแม่นยำการทำนาย:")
        print(f"   ผลการแข่งขัน (ชนะ/แพ้/เสมอ): {correct_results}/{total_games} = {result_accuracy:.1%}")
        print(f"   ราคาต่อรอง (Handicap):        {correct_handicaps}/{total_games} = {handicap_accuracy:.1%}")
        print(f"   สูง/ต่ำ (Over/Under):         {correct_over_unders}/{total_games} = {ou_accuracy:.1%}")
        print(f"   ถูกทั้ง 3 ค่า:                {correct_all_three}/{total_games} = {all_three_accuracy:.1%}")
        
        # วิเคราะห์ตามเส้น Handicap
        handicap_lines = {}
        for result in results:
            line = result['handicap_line']
            if line not in handicap_lines:
                handicap_lines[line] = {'total': 0, 'correct': 0}
            handicap_lines[line]['total'] += 1
            if result['handicap_correct']:
                handicap_lines[line]['correct'] += 1
        
        print(f"\n📈 ความแม่นยำตามเส้น Handicap:")
        for line, stats in handicap_lines.items():
            accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
            print(f"   {line:8}: {stats['correct']:2d}/{stats['total']:2d} = {accuracy:.1%}")
        
        # วิเคราะห์ตามเส้น O/U
        ou_lines = {}
        for result in results:
            line = result['ou_line']
            if line not in ou_lines:
                ou_lines[line] = {'total': 0, 'correct': 0}
            ou_lines[line]['total'] += 1
            if result['ou_correct']:
                ou_lines[line]['correct'] += 1
        
        print(f"\n📊 ความแม่นยำตามเส้น Over/Under:")
        for line, stats in ou_lines.items():
            accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
            print(f"   {line:4}: {stats['correct']:2d}/{stats['total']:2d} = {accuracy:.1%}")
        
        # เกมที่ทำนายถูกทั้ง 3 ค่า
        if correct_all_three > 0:
            print(f"\n🏆 เกมที่ทำนายถูกทั้ง 3 ค่า ({correct_all_three} เกม):")
            for result in results:
                if result['result_correct'] and result['handicap_correct'] and result['ou_correct']:
                    print(f"   ✅ {result['home_team'][:15]} vs {result['away_team'][:15]} "
                          f"({result['home_goals']}-{result['away_goals']}) - "
                          f"{result['handicap_line']} {result['ou_line']}")
        
        # สถิติเพิ่มเติม
        avg_goals = np.mean([r['home_goals'] + r['away_goals'] for r in results])
        home_wins = sum(1 for r in results if r['actual_result'] == 'H')
        draws = sum(1 for r in results if r['actual_result'] == 'D')
        away_wins = sum(1 for r in results if r['actual_result'] == 'A')
        
        print(f"\n📊 สถิติเพิ่มเติม:")
        print(f"   ประตูเฉลี่ย: {avg_goals:.1f} ประตู/เกม")
        print(f"   ผลการแข่งขัน: H:{home_wins} D:{draws} A:{away_wins}")
        print(f"   อัตราส่วน: H:{home_wins/total_games:.1%} D:{draws/total_games:.1%} A:{away_wins/total_games:.1%}")

# Main execution
if __name__ == "__main__":
    tester = HandicapTester()
    results = tester.handicap_backtest(test_games=20)
    
    print(f"\n🎉 การทดสอบ Handicap เสร็จสิ้น!")
    print("="*120)
