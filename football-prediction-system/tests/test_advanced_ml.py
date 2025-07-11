#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ทดสอบระบบทำนายฟุตบอล Advanced ML
- ทดสอบทุกฟีเจอร์ใหม่
- เปรียบเทียบโมเดลต่างๆ
- วิเคราะห์ผลลัพธ์เชิงลึก
"""

from advanced_ml_predictor import AdvancedFootballPredictor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AdvancedMLTester:
    def __init__(self):
        self.predictor = AdvancedFootballPredictor(
            api_key="052fd4885cf943ad859c89cef542e2e5"
        )
        self.test_results = {}
        
    def comprehensive_test(self, test_games=50):
        """ทดสอบครบถ้วน"""
        print("🚀 การทดสอบระบบ Advanced ML")
        print("="*80)
        
        # โหลดข้อมูล
        print("📊 กำลังโหลดข้อมูล...")
        data = self.predictor.load_premier_league_data()
        
        if len(data) < test_games + 100:
            print(f"⚠️ ข้อมูลไม่เพียงพอ (มี {len(data)} เกม)")
            return
        
        # แบ่งข้อมูลสำหรับการทดสอบ
        train_data = data[:-test_games].copy()
        test_data = data[-test_games:].copy()
        
        print(f"🎯 เทรนด้วย {len(train_data)} เกม, ทดสอบ {len(test_data)} เกม")
        
        # เทรนโมเดล
        print("\n🤖 กำลังเทรนโมเดล Advanced ML...")
        training_results = self.predictor.train_models(train_data)
        
        # ทดสอบการทำนาย
        print(f"\n🎯 กำลังทดสอบการทำนาย {test_games} เกม...")
        predictions = []
        actual_results = []
        
        for idx, match in test_data.iterrows():
            # ทำนาย
            pred = self.predictor.predict_match_advanced(
                match['home_team'], 
                match['away_team'],
                match['date']
            )
            
            # ผลจริง
            if match['home_goals'] > match['away_goals']:
                actual = 'Home Win'
            elif match['home_goals'] == match['away_goals']:
                actual = 'Draw'
            else:
                actual = 'Away Win'
            
            predictions.append(pred)
            actual_results.append(actual)
            
            # แสดงผล
            correct = "✅" if pred['prediction'] == actual else "❌"
            print(f"{idx-len(train_data)+1:2d}. {match['home_team'][:15]:15} vs {match['away_team'][:15]:15} | "
                  f"จริง: {actual:8} | ทำนาย: {pred['prediction']:8} | "
                  f"มั่นใจ: {pred['confidence']:.3f} {correct}")
        
        # วิเคราะห์ผลลัพธ์
        self.analyze_results(predictions, actual_results, test_data)
        
        # วิเคราะห์ Feature Importance
        self.analyze_features()
        
        # สร้างกราฟ
        self.create_visualizations(predictions, actual_results)
        
        return predictions, actual_results
    
    def analyze_results(self, predictions, actual_results, test_data):
        """วิเคราะห์ผลลัพธ์"""
        print(f"\n📊 การวิเคราะห์ผลลัพธ์")
        print("="*80)
        
        # ความแม่นยำโดยรวม
        correct_predictions = sum(1 for pred, actual in zip(predictions, actual_results) 
                                if pred['prediction'] == actual)
        total_predictions = len(predictions)
        overall_accuracy = correct_predictions / total_predictions
        
        print(f"🎯 ความแม่นยำโดยรวม: {correct_predictions}/{total_predictions} = {overall_accuracy:.1%}")
        
        # วิเคราะห์ตามประเภทผล
        result_analysis = {'Home Win': [], 'Draw': [], 'Away Win': []}
        
        for pred, actual in zip(predictions, actual_results):
            result_analysis[actual].append(pred['prediction'] == actual)
        
        print(f"\n📈 ความแม่นยำตามประเภทผล:")
        for result_type, correct_list in result_analysis.items():
            if correct_list:
                accuracy = sum(correct_list) / len(correct_list)
                print(f"   {result_type:10}: {sum(correct_list):2d}/{len(correct_list):2d} = {accuracy:.1%}")
        
        # วิเคราะห์ตามระดับความมั่นใจ
        confidence_ranges = [
            (0.0, 0.4, "ต่ำ"),
            (0.4, 0.6, "ปานกลาง"),
            (0.6, 0.8, "สูง"),
            (0.8, 1.0, "สูงมาก")
        ]
        
        print(f"\n🎲 ความแม่นยำตามระดับความมั่นใจ:")
        for min_conf, max_conf, label in confidence_ranges:
            filtered_results = [
                (pred['prediction'] == actual) 
                for pred, actual in zip(predictions, actual_results)
                if min_conf <= pred['confidence'] < max_conf
            ]
            
            if filtered_results:
                accuracy = sum(filtered_results) / len(filtered_results)
                print(f"   {label:10} ({min_conf:.1f}-{max_conf:.1f}): {sum(filtered_results):2d}/{len(filtered_results):2d} = {accuracy:.1%}")
        
        # วิเคราะห์การทำนาย Draw
        draw_predictions = [pred for pred in predictions if pred['prediction'] == 'Draw']
        actual_draws = [actual for actual in actual_results if actual == 'Draw']
        correct_draws = sum(1 for pred, actual in zip(predictions, actual_results) 
                          if pred['prediction'] == 'Draw' and actual == 'Draw')
        
        print(f"\n🤝 การวิเคราะห์ Draw:")
        print(f"   ทำนาย Draw: {len(draw_predictions)} เกม")
        print(f"   Draw จริง: {len(actual_draws)} เกม")
        print(f"   ทำนาย Draw ถูก: {correct_draws} เกม")
        
        if len(draw_predictions) > 0:
            draw_precision = correct_draws / len(draw_predictions)
            print(f"   Precision (Draw): {draw_precision:.1%}")
        
        if len(actual_draws) > 0:
            draw_recall = correct_draws / len(actual_draws)
            print(f"   Recall (Draw): {draw_recall:.1%}")
        
        # เปรียบเทียบโมเดล
        print(f"\n🤖 การเปรียบเทียบโมเดล:")
        model_accuracies = {'Random Forest': [], 'Gradient Boosting': [], 'Deep Learning': []}
        
        for pred, actual in zip(predictions, actual_results):
            for model_name in model_accuracies.keys():
                if model_name in pred['model_predictions']:
                    model_pred = pred['model_predictions'][model_name]
                    if model_pred != 'N/A':
                        model_accuracies[model_name].append(model_pred == actual)
        
        for model_name, correct_list in model_accuracies.items():
            if correct_list:
                accuracy = sum(correct_list) / len(correct_list)
                print(f"   {model_name:18}: {accuracy:.1%}")
    
    def analyze_features(self):
        """วิเคราะห์ความสำคัญของ Features"""
        print(f"\n🔍 การวิเคราะห์ Feature Importance")
        print("="*80)
        
        importance_df = self.predictor.analyze_feature_importance()
        
        if importance_df is not None:
            print("🏆 Top 15 Features ที่สำคัญที่สุด:")
            for idx, row in importance_df.head(15).iterrows():
                print(f"   {idx+1:2d}. {row['feature']:25} : {row['importance']:.4f}")
            
            # จัดกลุ่ม features
            feature_categories = {
                'Player Stats': ['player', 'chemistry', 'fitness', 'pass_accuracy', 'shots', 'tackles'],
                'Injury Impact': ['injury', 'injured'],
                'Weather': ['temperature', 'humidity', 'wind', 'precipitation', 'weather'],
                'Team Performance': ['win_rate', 'goals_for', 'goals_against', 'form'],
                'Match Context': ['month', 'day_of_week', 'weekend', 'home_advantage']
            }
            
            print(f"\n📊 ความสำคัญตามหมวดหมู่:")
            for category, keywords in feature_categories.items():
                category_importance = importance_df[
                    importance_df['feature'].str.contains('|'.join(keywords), case=False)
                ]['importance'].sum()
                print(f"   {category:18}: {category_importance:.4f}")
    
    def create_visualizations(self, predictions, actual_results):
        """สร้างกราฟวิเคราะห์"""
        print(f"\n📈 กำลังสร้างกราฟวิเคราะห์...")
        
        # สร้างกราฟ
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Advanced ML Football Prediction Analysis', fontsize=16, fontweight='bold')
        
        # 1. Confusion Matrix
        from sklearn.metrics import confusion_matrix
        import seaborn as sns
        
        labels = ['Away Win', 'Draw', 'Home Win']
        pred_labels = [pred['prediction'] for pred in predictions]
        
        cm = confusion_matrix(actual_results, pred_labels, labels=labels)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=labels, yticklabels=labels, ax=axes[0,0])
        axes[0,0].set_title('Confusion Matrix')
        axes[0,0].set_xlabel('Predicted')
        axes[0,0].set_ylabel('Actual')
        
        # 2. Confidence Distribution
        confidences = [pred['confidence'] for pred in predictions]
        axes[0,1].hist(confidences, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0,1].set_title('Confidence Score Distribution')
        axes[0,1].set_xlabel('Confidence Score')
        axes[0,1].set_ylabel('Frequency')
        axes[0,1].axvline(np.mean(confidences), color='red', linestyle='--', 
                         label=f'Mean: {np.mean(confidences):.3f}')
        axes[0,1].legend()
        
        # 3. Accuracy by Confidence Range
        conf_ranges = np.arange(0, 1.1, 0.1)
        accuracies = []
        
        for i in range(len(conf_ranges)-1):
            min_conf, max_conf = conf_ranges[i], conf_ranges[i+1]
            range_results = [
                pred['prediction'] == actual
                for pred, actual in zip(predictions, actual_results)
                if min_conf <= pred['confidence'] < max_conf
            ]
            
            if range_results:
                accuracies.append(sum(range_results) / len(range_results))
            else:
                accuracies.append(0)
        
        axes[1,0].bar(range(len(accuracies)), accuracies, alpha=0.7, color='lightgreen')
        axes[1,0].set_title('Accuracy by Confidence Range')
        axes[1,0].set_xlabel('Confidence Range')
        axes[1,0].set_ylabel('Accuracy')
        axes[1,0].set_xticks(range(len(accuracies)))
        axes[1,0].set_xticklabels([f'{conf_ranges[i]:.1f}-{conf_ranges[i+1]:.1f}' 
                                  for i in range(len(accuracies))], rotation=45)
        
        # 4. Model Comparison
        model_names = ['Random Forest', 'Gradient Boosting', 'Deep Learning', 'Ensemble']
        model_scores = []
        
        for model_name in model_names[:-1]:  # ไม่รวม Ensemble
            model_correct = sum(1 for pred, actual in zip(predictions, actual_results)
                              if pred['model_predictions'].get(model_name, 'N/A') == actual
                              and pred['model_predictions'].get(model_name, 'N/A') != 'N/A')
            model_total = sum(1 for pred in predictions 
                            if pred['model_predictions'].get(model_name, 'N/A') != 'N/A')
            
            if model_total > 0:
                model_scores.append(model_correct / model_total)
            else:
                model_scores.append(0)
        
        # Ensemble score
        ensemble_correct = sum(1 for pred, actual in zip(predictions, actual_results)
                             if pred['prediction'] == actual)
        model_scores.append(ensemble_correct / len(predictions))
        
        colors = ['lightcoral', 'lightsalmon', 'lightblue', 'gold']
        bars = axes[1,1].bar(model_names, model_scores, color=colors, alpha=0.8)
        axes[1,1].set_title('Model Performance Comparison')
        axes[1,1].set_ylabel('Accuracy')
        axes[1,1].set_ylim(0, 1)
        
        # เพิ่มค่าบนแท่งกราฟ
        for bar, score in zip(bars, model_scores):
            axes[1,1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                          f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('/Users/80090/Desktop/Project/untitle/advanced_ml_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ บันทึกกราฟเป็น 'advanced_ml_analysis.png'")
    
    def demo_predictions(self):
        """แสดงตัวอย่างการทำนาย"""
        print(f"\n🎮 ตัวอย่างการทำนายแบบ Advanced ML")
        print("="*80)
        
        demo_matches = [
            ("Arsenal", "Chelsea"),
            ("Manchester City", "Liverpool"),
            ("Manchester United", "Tottenham"),
            ("Brighton", "Newcastle"),
            ("Aston Villa", "West Ham")
        ]
        
        for home, away in demo_matches:
            pred = self.predictor.predict_match_advanced(home, away)
            
            if pred:
                print(f"\n⚽ {home} vs {away}")
                print(f"   🏆 ทำนาย: {pred['prediction']} (มั่นใจ {pred['confidence']:.1%})")
                print(f"   📊 ความน่าจะเป็น:")
                for outcome, prob in pred['probabilities'].items():
                    print(f"      {outcome:10}: {prob:.1%}")
                print(f"   🤖 โมเดลต่างๆ:")
                for model, prediction in pred['model_predictions'].items():
                    print(f"      {model:18}: {prediction}")
                print(f"   🔧 Features ที่ใช้: {pred['features_used']}")

# Main execution
if __name__ == "__main__":
    tester = AdvancedMLTester()
    
    # รันการทดสอบครบถ้วน
    predictions, actual_results = tester.comprehensive_test(test_games=30)
    
    # แสดงตัวอย่างการทำนาย
    tester.demo_predictions()
    
    print(f"\n🎉 การทดสอบ Advanced ML เสร็จสิ้น!")
    print("="*80)
