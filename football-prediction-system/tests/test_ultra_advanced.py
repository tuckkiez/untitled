#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ทดสอบระบบ Ultra Advanced Predictor
เปรียบเทียบกับระบบเดิมและแสดงการปรับปรุง
"""

from ultra_predictor_complete import UltraAdvancedPredictor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
        print("🚀 การทดสอบ Ultra Advanced Predictor")
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
        print(f"{'No.':<3} {'Date':<12} {'Match':<40} {'Score':<8} {'Actual':<10} {'Predicted':<10} {'Conf':<6} {'Agr':<5} {'✓/✗':<3}")
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
            agreement = prediction['model_agreement']
            
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
                  f"{actual_short:<10} {pred_short:<10} {confidence:<6.3f} {agreement:<5.3f} {status:<3}")
            
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
                'model_agreement': agreement,
                'is_correct': is_correct,
                'probabilities': prediction['probabilities'],
                'model_predictions': prediction['model_predictions']
            })
        
        # วิเคราะห์ผลลัพธ์
        self.analyze_ultra_results(results, correct_predictions, test_games, 
                                 high_confidence_correct, high_confidence_total)
        
        # สร้างกราฟ
        self.create_ultra_visualizations(results)
        
        return results
    
    def analyze_ultra_results(self, results, correct_predictions, total_games, 
                            high_conf_correct, high_conf_total):
        """วิเคราะห์ผลลัพธ์ Ultra Advanced"""
        print("\n" + "="*100)
        print("📊 การวิเคราะห์ผลลัพธ์ Ultra Advanced")
        print("="*100)
        
        # ความแม่นยำโดยรวม
        overall_accuracy = correct_predictions / total_games
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
        
        # วิเคราะห์ Model Agreement
        high_agreement = [r for r in results if r['model_agreement'] > 0.8]
        low_agreement = [r for r in results if r['model_agreement'] < 0.6]
        
        if high_agreement:
            high_agr_correct = sum(1 for r in high_agreement if r['is_correct'])
            high_agr_accuracy = high_agr_correct / len(high_agreement)
            print(f"\n🤝 เมื่อโมเดลเห็นตรงกันสูง (>80%): {high_agr_correct}/{len(high_agreement)} = {high_agr_accuracy:.1%}")
        
        if low_agreement:
            low_agr_correct = sum(1 for r in low_agreement if r['is_correct'])
            low_agr_accuracy = low_agr_correct / len(low_agreement)
            print(f"🤔 เมื่อโมเดลเห็นไม่ตรงกัน (<60%): {low_agr_correct}/{len(low_agreement)} = {low_agr_accuracy:.1%}")
        
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
                avg_agr = np.mean([r['model_agreement'] for r in filtered_results])
                print(f"   {label:10} ({min_conf:.1f}-{max_conf:.1f}): {correct_in_range:2d}/{len(filtered_results):2d} = {accuracy:.1%} "
                      f"(เฉลี่ย: Conf={avg_conf:.3f}, Agr={avg_agr:.3f})")
        
        # เปรียบเทียบโมเดลแต่ละตัว
        print(f"\n🤖 การเปรียบเทียบโมเดลแต่ละตัว:")
        model_names = ['rf', 'gb', 'et', 'lr', 'svm']
        model_full_names = {
            'rf': 'Random Forest',
            'gb': 'Gradient Boosting', 
            'et': 'Extra Trees',
            'lr': 'Logistic Regression',
            'svm': 'SVM'
        }
        
        for model_name in model_names:
            model_correct = 0
            model_total = 0
            
            for r in results:
                if model_name in self.predictor.ensemble_weights:
                    model_total += 1
                    # ใช้ ensemble prediction เป็นตัวแทน
                    if r['is_correct']:
                        model_correct += 1
            
            if model_total > 0:
                weight = self.predictor.ensemble_weights.get(model_name, 0)
                print(f"   {model_full_names[model_name]:18}: น้ำหนัก {weight:.3f}")
        
        # สถิติเพิ่มเติม
        avg_confidence = np.mean([r['confidence'] for r in results])
        avg_agreement = np.mean([r['model_agreement'] for r in results])
        
        print(f"\n📊 สถิติเพิ่มเติม:")
        print(f"   ความมั่นใจเฉลี่ย: {avg_confidence:.3f}")
        print(f"   ความเห็นตรงกันเฉลี่ย: {avg_agreement:.3f}")
        print(f"   Features ที่ใช้: {results[0]['probabilities'] if results else 'N/A'}")
    
    def create_ultra_visualizations(self, results):
        """สร้างกราฟวิเคราะห์ Ultra Advanced"""
        print(f"\n📈 กำลังสร้างกราฟวิเคราะห์ Ultra Advanced...")
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Ultra Advanced Football Prediction Analysis', fontsize=16, fontweight='bold')
        
        # 1. Accuracy vs Confidence
        confidences = [r['confidence'] for r in results]
        accuracies = [1 if r['is_correct'] else 0 for r in results]
        
        # Bin the data
        conf_bins = np.linspace(0, 1, 11)
        bin_accuracies = []
        bin_centers = []
        
        for i in range(len(conf_bins)-1):
            mask = (np.array(confidences) >= conf_bins[i]) & (np.array(confidences) < conf_bins[i+1])
            if np.sum(mask) > 0:
                bin_accuracies.append(np.mean(np.array(accuracies)[mask]))
                bin_centers.append((conf_bins[i] + conf_bins[i+1]) / 2)
        
        axes[0,0].plot(bin_centers, bin_accuracies, 'o-', linewidth=2, markersize=8)
        axes[0,0].set_title('Accuracy vs Confidence')
        axes[0,0].set_xlabel('Confidence')
        axes[0,0].set_ylabel('Accuracy')
        axes[0,0].grid(True, alpha=0.3)
        axes[0,0].set_ylim(0, 1)
        
        # 2. Model Agreement vs Accuracy
        agreements = [r['model_agreement'] for r in results]
        
        # Bin by agreement
        agr_bins = np.linspace(0, 1, 11)
        agr_accuracies = []
        agr_centers = []
        
        for i in range(len(agr_bins)-1):
            mask = (np.array(agreements) >= agr_bins[i]) & (np.array(agreements) < agr_bins[i+1])
            if np.sum(mask) > 0:
                agr_accuracies.append(np.mean(np.array(accuracies)[mask]))
                agr_centers.append((agr_bins[i] + agr_bins[i+1]) / 2)
        
        axes[0,1].plot(agr_centers, agr_accuracies, 's-', color='orange', linewidth=2, markersize=8)
        axes[0,1].set_title('Accuracy vs Model Agreement')
        axes[0,1].set_xlabel('Model Agreement')
        axes[0,1].set_ylabel('Accuracy')
        axes[0,1].grid(True, alpha=0.3)
        axes[0,1].set_ylim(0, 1)
        
        # 3. Confidence Distribution
        axes[0,2].hist(confidences, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0,2].axvline(np.mean(confidences), color='red', linestyle='--', 
                         label=f'Mean: {np.mean(confidences):.3f}')
        axes[0,2].set_title('Confidence Distribution')
        axes[0,2].set_xlabel('Confidence')
        axes[0,2].set_ylabel('Frequency')
        axes[0,2].legend()
        
        # 4. Model Agreement Distribution
        axes[1,0].hist(agreements, bins=15, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[1,0].axvline(np.mean(agreements), color='red', linestyle='--',
                         label=f'Mean: {np.mean(agreements):.3f}')
        axes[1,0].set_title('Model Agreement Distribution')
        axes[1,0].set_xlabel('Model Agreement')
        axes[1,0].set_ylabel('Frequency')
        axes[1,0].legend()
        
        # 5. Prediction Distribution
        pred_counts = {}
        for r in results:
            pred = r['predicted_result']
            pred_counts[pred] = pred_counts.get(pred, 0) + 1
        
        pred_labels = list(pred_counts.keys())
        pred_values = list(pred_counts.values())
        colors = ['lightcoral', 'lightyellow', 'lightblue']
        
        axes[1,1].pie(pred_values, labels=pred_labels, autopct='%1.1f%%', 
                     colors=colors[:len(pred_labels)], startangle=90)
        axes[1,1].set_title('Prediction Distribution')
        
        # 6. Confidence vs Agreement Scatter
        correct_mask = np.array(accuracies) == 1
        incorrect_mask = np.array(accuracies) == 0
        
        axes[1,2].scatter(np.array(confidences)[correct_mask], np.array(agreements)[correct_mask], 
                         c='green', alpha=0.7, label='Correct', s=50)
        axes[1,2].scatter(np.array(confidences)[incorrect_mask], np.array(agreements)[incorrect_mask], 
                         c='red', alpha=0.7, label='Incorrect', s=50)
        axes[1,2].set_title('Confidence vs Agreement')
        axes[1,2].set_xlabel('Confidence')
        axes[1,2].set_ylabel('Model Agreement')
        axes[1,2].legend()
        axes[1,2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/Users/80090/Desktop/Project/untitle/ultra_advanced_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ บันทึกกราฟเป็น 'ultra_advanced_analysis.png'")
    
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
                    print(f"      {model:18}: {prediction} (น้ำหนัก: {weight:.3f})")

# Main execution
if __name__ == "__main__":
    tester = UltraAdvancedTester()
    
    # รันการทดสอบครบถ้วน
    results = tester.comprehensive_backtest(test_games=20)
    
    # แสดงตัวอย่างการทำนาย
    tester.demo_ultra_predictions()
    
    print(f"\n🎉 การทดสอบ Ultra Advanced เสร็จสิ้น!")
    print("="*100)
