#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ทดสอบระบบทำนายเตะมุมด้วยข้อมูลจริงจาก API
- ดึงข้อมูลจาก FotMob API
- ดึงราคาต่อรองจาก The Odds API
- ทดสอบความแม่นยำกับข้อมูลจริง
"""

from real_corner_data import RealCornerDataFetcher
from corner_predictor import CornerPredictor
import pandas as pd
import numpy as np
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

class RealCornerTester:
    def __init__(self, odds_api_key=None):
        self.data_fetcher = RealCornerDataFetcher(odds_api_key=odds_api_key)
        self.corner_predictor = CornerPredictor()
        self.real_data = None
        
    def fetch_and_test_real_data(self, num_matches=20):
        """ดึงข้อมูลจริงและทดสอบ"""
        print("🚀 การทดสอบระบบทำนายเตะมุมด้วยข้อมูลจริง")
        print("="*100)
        
        # 1. ดึงข้อมูลจริงจาก API
        print("📡 กำลังดึงข้อมูลจริงจาก API...")
        self.real_data = self.data_fetcher.get_comprehensive_corner_data(num_matches)
        
        if not self.real_data:
            print("❌ ไม่สามารถดึงข้อมูลได้")
            return None
        
        # 2. เตรียมข้อมูลสำหรับเทรนโมเดล
        print("\n🤖 กำลังเตรียมข้อมูลและเทรนโมเดล...")
        training_data = self.prepare_training_data()
        
        # 3. เทรนโมเดล
        self.corner_predictor.train_corner_models(training_data)
        
        # 4. ทดสอบกับข้อมูลจริง
        print(f"\n🎯 กำลังทดสอบกับข้อมูลจริง {len(self.real_data)} เกม")
        results = self.test_with_real_data()
        
        return results
    
    def prepare_training_data(self):
        """เตรียมข้อมูลสำหรับเทรนโมเดล"""
        training_matches = []
        
        for match in self.real_data:
            training_matches.append({
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'date': match['date'],
                'home_goals': int(match['home_score']),
                'away_goals': int(match['away_score']),
                'home_corners': match['home_corners'],
                'away_corners': match['away_corners'],
                'total_corners': match['total_corners'],
                'first_half_corners': match['first_half_corners'],
                'second_half_corners': match['second_half_corners']
            })
        
        return pd.DataFrame(training_matches)
    
    def test_with_real_data(self):
        """ทดสอบกับข้อมูลจริง"""
        print("\n📋 รายละเอียดการทดสอบเตะมุมจริง")
        print("="*120)
        print(f"{'No.':<3} {'Match':<35} {'Score':<8} {'Total':<7} {'1H':<5} {'2H':<5} {'T12':<4} {'1H6':<4} {'2H6':<4} {'Odds':<8} {'Score':<6}")
        print("-"*120)
        
        results = []
        correct_total_12 = 0
        correct_first_half_6 = 0
        correct_second_half_6 = 0
        total_score = 0
        
        for idx, match in enumerate(self.real_data, 1):
            # ทำนาย
            prediction = self.corner_predictor.predict_corners(
                match['home_team'],
                match['away_team'],
                datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
            )
            
            if not prediction:
                continue
            
            # ข้อมูลจริง
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
            
            # คะแนนรวม
            game_score = sum([total_12_correct, first_half_6_correct, second_half_6_correct])
            total_score += game_score
            
            # สัญลักษณ์
            t12_symbol = "✅" if total_12_correct else "❌"
            h1_symbol = "✅" if first_half_6_correct else "❌"
            h2_symbol = "✅" if second_half_6_correct else "❌"
            
            # ราคาต่อรอง
            odds_12 = match['corner_odds'].get('Over_12', 'N/A')
            
            # แสดงผล
            match_str = f"{match['home_team'][:15]} vs {match['away_team'][:15]}"
            score_str = f"{match['home_score']}-{match['away_score']}"
            total_str = f"{actual_total}({pred_total})"
            h1_str = f"{actual_1h}({pred_1h})"
            h2_str = f"{actual_2h}({pred_2h})"
            odds_str = f"{odds_12}"
            
            print(f"{idx:<3} {match_str:<35} {score_str:<8} {total_str:<7} {h1_str:<5} {h2_str:<5} "
                  f"{t12_symbol:<4} {h1_symbol:<4} {h2_symbol:<4} {odds_str:<8} {game_score}/3")
            
            # เก็บข้อมูล
            results.append({
                'match_num': idx,
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'score': f"{match['home_score']}-{match['away_score']}",
                'actual_total': actual_total,
                'actual_1h': actual_1h,
                'actual_2h': actual_2h,
                'pred_total': pred_total,
                'pred_1h': pred_1h,
                'pred_2h': pred_2h,
                'total_12_correct': total_12_correct,
                'first_half_6_correct': first_half_6_correct,
                'second_half_6_correct': second_half_6_correct,
                'game_score': game_score,
                'corner_odds': match['corner_odds'],
                'data_quality': match['data_quality']
            })
        
        # วิเคราะห์ผลลัพธ์
        self.analyze_real_results(results, correct_total_12, correct_first_half_6, 
                                correct_second_half_6, total_score, len(results))
        
        return results
    
    def analyze_real_results(self, results, correct_total_12, correct_first_half_6, 
                           correct_second_half_6, total_score, total_games):
        """วิเคราะห์ผลการทดสอบจริง"""
        print("\n" + "="*120)
        print("📊 สรุปผลการทดสอบเตะมุมด้วยข้อมูลจริง")
        print("="*120)
        
        # ความแม่นยำ
        total_12_accuracy = correct_total_12 / total_games if total_games > 0 else 0
        first_half_6_accuracy = correct_first_half_6 / total_games if total_games > 0 else 0
        second_half_6_accuracy = correct_second_half_6 / total_games if total_games > 0 else 0
        overall_accuracy = total_score / (total_games * 3) if total_games > 0 else 0
        
        print(f"🎯 ความแม่นยำการทำนาย (ข้อมูลจริง):")
        print(f"   เตะมุมรวม >12:        {correct_total_12}/{total_games} = {total_12_accuracy:.1%}")
        print(f"   ครึ่งแรก >6:          {correct_first_half_6}/{total_games} = {first_half_6_accuracy:.1%}")
        print(f"   ครึ่งหลัง >6:         {correct_second_half_6}/{total_games} = {second_half_6_accuracy:.1%}")
        print(f"   ความแม่นยำรวม:        {total_score}/{total_games * 3} = {overall_accuracy:.1%}")
        
        # คุณภาพข้อมูล
        real_data_count = sum(1 for r in results if r['data_quality'] == 'real')
        simulated_data_count = sum(1 for r in results if r['data_quality'] in ['simulated', 'sample'])
        
        print(f"\n📊 คุณภาพข้อมูล:")
        print(f"   ข้อมูลจริงจาก API:    {real_data_count}/{total_games} = {real_data_count/total_games:.1%}")
        print(f"   ข้อมูลจำลอง:          {simulated_data_count}/{total_games} = {simulated_data_count/total_games:.1%}")
        
        # สถิติเตะมุมจริง
        avg_total = np.mean([r['actual_total'] for r in results])
        avg_1h = np.mean([r['actual_1h'] for r in results])
        avg_2h = np.mean([r['actual_2h'] for r in results])
        
        print(f"\n📈 สถิติเตะมุมจริงเฉลี่ย:")
        print(f"   เตะมุมรวม: {avg_total:.1f} ครั้ง/เกม")
        print(f"   ครึ่งแรก: {avg_1h:.1f} ครั้ง/เกม")
        print(f"   ครึ่งหลัง: {avg_2h:.1f} ครั้ง/เกม")
        print(f"   อัตราส่วน 1H:2H = {avg_1h/avg_2h:.2f}:1")
        
        # การกระจายเตะมุม
        over_12_games = sum(1 for r in results if r['actual_total'] > 12)
        over_6_1h_games = sum(1 for r in results if r['actual_1h'] > 6)
        over_6_2h_games = sum(1 for r in results if r['actual_2h'] > 6)
        
        print(f"\n📊 การกระจายเตะมุมจริง:")
        print(f"   เกม >12 เตะมุม: {over_12_games}/{total_games} = {over_12_games/total_games:.1%}")
        print(f"   ครึ่งแรก >6: {over_6_1h_games}/{total_games} = {over_6_1h_games/total_games:.1%}")
        print(f"   ครึ่งหลัง >6: {over_6_2h_games}/{total_games} = {over_6_2h_games/total_games:.1%}")
        
        # วิเคราะห์ราคาต่อรอง
        self.analyze_betting_value(results)
        
        # เกมที่ทำนายได้ดี
        perfect_games = [r for r in results if r['game_score'] == 3]
        if perfect_games:
            print(f"\n🏆 เกมที่ทำนายถูกทั้ง 3 ค่า ({len(perfect_games)} เกม):")
            for game in perfect_games[:5]:  # แสดง 5 เกมแรก
                odds_12 = game['corner_odds'].get('Over_12', 'N/A')
                print(f"   ✅ {game['home_team']} vs {game['away_team']} ({game['score']}) - "
                      f"Total:{game['actual_total']} 1H:{game['actual_1h']} 2H:{game['actual_2h']} "
                      f"Odds:{odds_12}")
    
    def analyze_betting_value(self, results):
        """วิเคราะห์ค่าการเดิมพัน"""
        print(f"\n💰 การวิเคราะห์ค่าการเดิมพัน:")
        
        total_bets = 0
        winning_bets = 0
        total_stake = 0
        total_return = 0
        
        for result in results:
            odds = result['corner_odds']
            
            # ทดสอบการเดิมพัน Over 12
            if 'Over_12' in odds and isinstance(odds['Over_12'], (int, float)):
                total_bets += 1
                total_stake += 100  # เดิมพัน 100 หน่วยต่อเกม
                
                # ถ้าทำนาย Over และผลจริงเป็น Over
                if result['actual_total'] > 12:
                    winning_bets += 1
                    total_return += 100 * odds['Over_12']
                
                # ถ้าทำนาย Under และผลจริงเป็น Under
                elif result['actual_total'] <= 12 and 'Under_12' in odds:
                    if isinstance(odds['Under_12'], (int, float)):
                        winning_bets += 1
                        total_return += 100 * odds['Under_12']
        
        if total_bets > 0:
            win_rate = winning_bets / total_bets
            roi = ((total_return - total_stake) / total_stake) * 100 if total_stake > 0 else 0
            
            print(f"   การเดิมพัน Over/Under 12:")
            print(f"   จำนวนเดิมพัน: {total_bets} เกม")
            print(f"   อัตราชนะ: {winning_bets}/{total_bets} = {win_rate:.1%}")
            print(f"   ROI: {roi:+.1f}%")
            
            if roi > 0:
                print(f"   🎉 กำไร: +{total_return - total_stake:.0f} หน่วย")
            else:
                print(f"   📉 ขาดทุน: {total_return - total_stake:.0f} หน่วย")
    
    def save_test_results(self, results, filename='real_corner_test_results.json'):
        """บันทึกผลการทดสอบ"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n✅ บันทึกผลการทดสอบเป็น {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")

# Main execution
if __name__ == "__main__":
    print("🚀 Real Corner Data Tester")
    print("="*60)
    
    # สร้าง tester (ใส่ Odds API key ถ้ามี)
    tester = RealCornerTester(
        odds_api_key=None  # ใส่ API key ของคุณที่นี่
    )
    
    # ทดสอบด้วยข้อมูลจริง
    results = tester.fetch_and_test_real_data(num_matches=20)
    
    if results:
        # บันทึกผลการทดสอบ
        tester.save_test_results(results)
        
        print(f"\n🎉 การทดสอบด้วยข้อมูลจริงเสร็จสิ้น!")
        print(f"📊 ทดสอบ {len(results)} เกม")
        print(f"💰 รวมการวิเคราะห์ราคาต่อรองครบถ้วน")
    else:
        print("❌ การทดสอบล้มเหลว")
