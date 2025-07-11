#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ทดสอบย้อนหลัง 20 เกมล่าสุด - Advanced ML
แสดงผลการทำนาย vs ผลจริงแบบละเอียด
"""

from advanced_ml_predictor import AdvancedFootballPredictor
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class BacktestAnalyzer:
    def __init__(self):
        self.predictor = AdvancedFootballPredictor(
            api_key="052fd4885cf943ad859c89cef542e2e5"
        )
        
    def detailed_backtest(self, num_games=20):
        """ทดสอบย้อนหลังแบบละเอียด"""
        print("🔍 การทดสอบย้อนหลัง 20 เกมล่าสุด - Advanced ML")
        print("="*100)
        
        # โหลดข้อมูล
        print("📊 กำลังโหลดข้อมูลจาก Premier League API...")
        data = self.predictor.load_premier_league_data()
        
        if len(data) < num_games + 50:
            print(f"⚠️ ข้อมูลไม่เพียงพอ (มี {len(data)} เกม)")
            return
        
        # แบ่งข้อมูล
        train_data = data[:-num_games].copy()
        test_data = data[-num_games:].copy()
        
        print(f"🎯 เทรนด้วย {len(train_data)} เกม")
        print(f"🧪 ทดสอบ {len(test_data)} เกม")
        
        # เทรนโมเดล
        print(f"\n🤖 กำลังเทรนโมเดล Advanced ML...")
        training_results = self.predictor.train_models(train_data)
        
        print(f"\n📋 รายละเอียดการทดสอบ 20 เกมล่าสุด")
        print("="*100)
        print(f"{'No.':<3} {'Date':<12} {'Match':<40} {'Score':<8} {'Actual':<10} {'Predicted':<10} {'Conf':<6} {'✓/✗':<3}")
        print("-"*100)
        
        results = []
        correct_predictions = 0
        
        for idx, (_, match) in enumerate(test_data.iterrows(), 1):
            # ทำนาย
            prediction = self.predictor.predict_match_advanced(
                match['home_team'], 
                match['away_team'],
                match['date']
            )
            
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
            
            # แสดงผล
            match_str = f"{match['home_team'][:18]} vs {match['away_team'][:18]}"
            date_str = pd.to_datetime(match['date']).strftime('%Y-%m-%d')
            
            print(f"{idx:<3} {date_str:<12} {match_str:<40} {score_str:<8} "
                  f"{actual_short:<10} {pred_short:<10} {confidence:<6.3f} {status:<3}")
            
            # เก็บข้อมูลสำหรับการวิเคราะห์
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
        
        # สรุปผลลัพธ์
        self.analyze_detailed_results(results, correct_predictions, num_games)
        
        return results
    
    def analyze_detailed_results(self, results, correct_predictions, total_games):
        """วิเคราะห์ผลลัพธ์แบบละเอียด"""
        print("\n" + "="*100)
        print("📊 การวิเคราะห์ผลลัพธ์แบบละเอียด")
        print("="*100)
        
        # ความแม่นยำโดยรวม
        overall_accuracy = correct_predictions / total_games
        print(f"🎯 ความแม่นยำโดยรวม: {correct_predictions}/{total_games} = {overall_accuracy:.1%}")
        
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
        
        # เกมที่ทำนายผิดแต่มั่นใจสูง
        high_conf_wrong = [r for r in results 
                          if not r['is_correct'] and r['confidence'] > 0.6]
        
        if high_conf_wrong:
            print(f"\n⚠️ เกมที่ทำนายผิดแต่มั่นใจสูง ({len(high_conf_wrong)} เกม):")
            for r in high_conf_wrong:
                print(f"   {r['home_team'][:15]} vs {r['away_team'][:15]} | "
                      f"จริง: {r['actual_result'][:4]} | ทำนาย: {r['predicted_result'][:4]} | "
                      f"มั่นใจ: {r['confidence']:.3f}")
        
        # เกมที่ทำนายถูกและมั่นใจสูง
        high_conf_correct = [r for r in results 
                           if r['is_correct'] and r['confidence'] > 0.6]
        
        if high_conf_correct:
            print(f"\n✅ เกมที่ทำนายถูกและมั่นใจสูง ({len(high_conf_correct)} เกม):")
            for r in high_conf_correct:
                print(f"   {r['home_team'][:15]} vs {r['away_team'][:15]} | "
                      f"ผล: {r['actual_result'][:4]} | มั่นใจ: {r['confidence']:.3f}")
        
        # วิเคราะห์โมเดลแต่ละตัว
        print(f"\n🤖 การเปรียบเทียบโมเดลแต่ละตัว:")
        model_names = ['Random Forest', 'Gradient Boosting']
        
        for model_name in model_names:
            model_correct = 0
            model_total = 0
            
            for r in results:
                if model_name in r['model_predictions']:
                    model_pred = r['model_predictions'][model_name]
                    if model_pred != 'N/A':
                        model_total += 1
                        if model_pred == r['actual_result']:
                            model_correct += 1
            
            if model_total > 0:
                model_accuracy = model_correct / model_total
                print(f"   {model_name:18}: {model_correct:2d}/{model_total:2d} = {model_accuracy:.1%}")
        
        # สถิติประตู
        total_goals = sum(r['home_goals'] + r['away_goals'] for r in results)
        avg_goals = total_goals / len(results)
        
        high_scoring = sum(1 for r in results if r['home_goals'] + r['away_goals'] > 2.5)
        low_scoring = len(results) - high_scoring
        
        print(f"\n⚽ สถิติประตู:")
        print(f"   ประตูรวมเฉลี่ย: {avg_goals:.1f} ประตู/เกม")
        print(f"   เกมประตูสูง (>2.5): {high_scoring}/{len(results)} = {high_scoring/len(results):.1%}")
        print(f"   เกมประตูต่ำ (≤2.5): {low_scoring}/{len(results)} = {low_scoring/len(results):.1%}")
        
        # ทีมที่ปรากฏบ่อย
        team_appearances = {}
        team_results = {}
        
        for r in results:
            for team in [r['home_team'], r['away_team']]:
                team_appearances[team] = team_appearances.get(team, 0) + 1
                if team not in team_results:
                    team_results[team] = {'wins': 0, 'draws': 0, 'losses': 0}
                
                if team == r['home_team']:
                    if r['home_goals'] > r['away_goals']:
                        team_results[team]['wins'] += 1
                    elif r['home_goals'] == r['away_goals']:
                        team_results[team]['draws'] += 1
                    else:
                        team_results[team]['losses'] += 1
                else:  # away team
                    if r['away_goals'] > r['home_goals']:
                        team_results[team]['wins'] += 1
                    elif r['away_goals'] == r['home_goals']:
                        team_results[team]['draws'] += 1
                    else:
                        team_results[team]['losses'] += 1
        
        print(f"\n🏆 ทีมที่ปรากฏบ่อยใน 20 เกมล่าสุด:")
        sorted_teams = sorted(team_appearances.items(), key=lambda x: x[1], reverse=True)
        
        for team, count in sorted_teams[:10]:  # แสดง 10 ทีมแรก
            stats = team_results[team]
            total_games = stats['wins'] + stats['draws'] + stats['losses']
            win_rate = stats['wins'] / total_games if total_games > 0 else 0
            
            print(f"   {team[:20]:20}: {count} เกม | "
                  f"W:{stats['wins']} D:{stats['draws']} L:{stats['losses']} | "
                  f"อัตราชนะ: {win_rate:.1%}")

# Main execution
if __name__ == "__main__":
    analyzer = BacktestAnalyzer()
    results = analyzer.detailed_backtest(num_games=20)
    
    print(f"\n🎉 การทดสอบย้อนหลัง 20 เกมเสร็จสิ้น!")
    print("="*100)
