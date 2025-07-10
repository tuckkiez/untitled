#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ตรวจสอบผลลัพธ์จริงจาก 100 เกมล่าสุด
การทดสอบที่ครอบคลุมและน่าเชื่อถือมากขึ้น
"""

from enhanced_predictor_fixed import EnhancedFootballPredictorFixed
from football_predictor import FootballPredictor
from real_data_example import RealDataPredictor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class Comprehensive100MatchTest:
    def __init__(self):
        self.api_token = "052fd4885cf943ad859c89cef542e2e5"
        self.enhanced_predictor = None
        self.basic_predictor = None
        self.historical_data = None
        
    def load_data(self):
        """โหลดข้อมูลครบถ้วน"""
        print("🔄 กำลังโหลดข้อมูลครบถ้วนสำหรับการทดสอบ 100 เกม...")
        
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
        
        # เรียงและทำความสะอาด
        self.historical_data = self.historical_data.sort_values('date').reset_index(drop=True)
        self.historical_data = self.historical_data.dropna(subset=['home_goals', 'away_goals'])
        
        print(f"📅 ช่วงเวลา: {self.historical_data['date'].min()} ถึง {self.historical_data['date'].max()}")
        
        return True
    
    def train_models(self, train_data):
        """เทรนทั้งสองโมเดล"""
        print("🤖 กำลังเทรนโมเดลสำหรับการทดสอบ 100 เกม...")
        
        # Enhanced Model
        print("1. เทรน Enhanced Model...")
        self.enhanced_predictor = EnhancedFootballPredictorFixed()
        enhanced_success = self.enhanced_predictor.train(train_data)
        
        # Basic Model
        print("2. เทรน Basic Model...")
        self.basic_predictor = FootballPredictor()
        basic_success = self.basic_predictor.train(train_data)
        
        return enhanced_success and basic_success
    
    def test_100_matches(self):
        """ทดสอบ 100 เกมล่าสุด"""
        print("\n🔍 กำลังทดสอบ 100 เกมล่าสุด...")
        print("="*100)
        
        if len(self.historical_data) < 200:
            print("❌ ข้อมูลไม่เพียงพอสำหรับการทดสอบ 100 เกม")
            return None
        
        # แบ่งข้อมูล
        test_matches = self.historical_data.tail(100)
        train_data = self.historical_data.iloc[:-100]
        
        # เทรนโมเดล
        if not self.train_models(train_data):
            print("❌ ไม่สามารถเทรนโมเดลได้")
            return None
        
        # ทดสอบ
        enhanced_results = []
        basic_results = []
        
        print(f"{'No.':<4} {'Date':<12} {'Match':<40} {'Result':<10} {'Enhanced':<12} {'Basic':<12} {'E-Conf':<8} {'B-Conf':<8}")
        print("-" * 100)
        
        for idx, (_, match) in enumerate(test_matches.iterrows(), 1):
            # ผลจริง
            home_goals = int(match['home_goals'])
            away_goals = int(match['away_goals'])
            
            if home_goals > away_goals:
                actual = 'Home Win'
                actual_short = 'H'
            elif home_goals < away_goals:
                actual = 'Away Win'
                actual_short = 'A'
            else:
                actual = 'Draw'
                actual_short = 'D'
            
            # ทำนายด้วย Enhanced Model
            enhanced_pred = self.enhanced_predictor.predict_match(
                match['home_team'], match['away_team'], train_data
            )
            
            # ทำนายด้วย Basic Model
            basic_pred = self.basic_predictor.predict_match(
                match['home_team'], match['away_team'], train_data
            )
            
            if enhanced_pred and basic_pred:
                # Enhanced results
                enhanced_correct = (enhanced_pred['prediction'] == actual)
                enhanced_results.append({
                    'match': f"{match['home_team']} vs {match['away_team']}",
                    'date': match['date'],
                    'actual': actual,
                    'predicted': enhanced_pred['prediction'],
                    'confidence': enhanced_pred['confidence'],
                    'correct': enhanced_correct
                })
                
                # Basic results
                basic_correct = (basic_pred['prediction'] == actual)
                basic_results.append({
                    'match': f"{match['home_team']} vs {match['away_team']}",
                    'date': match['date'],
                    'actual': actual,
                    'predicted': basic_pred['prediction'],
                    'confidence': basic_pred['confidence'],
                    'correct': basic_correct
                })
                
                # แสดงผล
                home_short = match['home_team'].replace(' FC', '').replace(' United', ' Utd')[:18]
                away_short = match['away_team'].replace(' FC', '').replace(' United', ' Utd')[:18]
                match_str = f"{home_short} vs {away_short}"
                
                result_str = f"{home_goals}-{away_goals} ({actual_short})"
                enhanced_short = enhanced_pred['prediction'][0] if enhanced_pred['prediction'] != 'Draw' else 'D'
                basic_short = basic_pred['prediction'][0] if basic_pred['prediction'] != 'Draw' else 'D'
                
                enhanced_status = "✅" if enhanced_correct else "❌"
                basic_status = "✅" if basic_correct else "❌"
                
                print(f"{idx:<4} {match['date'].strftime('%Y-%m-%d'):<12} {match_str:<40} {result_str:<10} "
                      f"{enhanced_short}{enhanced_status:<11} {basic_short}{basic_status:<11} "
                      f"{enhanced_pred['confidence']:.3f}    {basic_pred['confidence']:.3f}")
        
        return self.analyze_results(enhanced_results, basic_results)
    
    def analyze_results(self, enhanced_results, basic_results):
        """วิเคราะห์ผลลัพธ์"""
        print("\n" + "="*100)
        print("📊 การวิเคราะห์ผลลัพธ์ 100 เกม")
        print("="*100)
        
        # คำนวณสถิติพื้นฐาน
        enhanced_correct = sum(r['correct'] for r in enhanced_results)
        basic_correct = sum(r['correct'] for r in basic_results)
        
        enhanced_accuracy = enhanced_correct / len(enhanced_results)
        basic_accuracy = basic_correct / len(basic_results)
        
        enhanced_avg_conf = np.mean([r['confidence'] for r in enhanced_results])
        basic_avg_conf = np.mean([r['confidence'] for r in basic_results])
        
        print(f"🏆 สรุปผลลัพธ์:")
        print(f"   Enhanced Model: {enhanced_correct}/100 = {enhanced_accuracy:.3f} ({enhanced_accuracy*100:.1f}%)")
        print(f"   Basic Model:    {basic_correct}/100 = {basic_accuracy:.3f} ({basic_accuracy*100:.1f}%)")
        print(f"   การปรับปรุง:    +{(enhanced_accuracy - basic_accuracy):.3f} ({(enhanced_accuracy - basic_accuracy)*100:.1f} percentage points)")
        
        print(f"\n📊 ความมั่นใจเฉลี่ย:")
        print(f"   Enhanced Model: {enhanced_avg_conf:.3f}")
        print(f"   Basic Model:    {basic_avg_conf:.3f}")
        
        # วิเคราะห์ตามระดับความมั่นใจ
        self.analyze_by_confidence(enhanced_results, basic_results)
        
        # วิเคราะห์ตามประเภทผลลัพธ์
        self.analyze_by_outcome_type(enhanced_results, basic_results)
        
        # วิเคราะห์ช่วงเวลา
        self.analyze_by_time_period(enhanced_results, basic_results)
        
        # สร้างกราฟ
        self.create_analysis_charts(enhanced_results, basic_results)
        
        return {
            'enhanced': {
                'accuracy': enhanced_accuracy,
                'correct': enhanced_correct,
                'avg_confidence': enhanced_avg_conf,
                'results': enhanced_results
            },
            'basic': {
                'accuracy': basic_accuracy,
                'correct': basic_correct,
                'avg_confidence': basic_avg_conf,
                'results': basic_results
            }
        }
    
    def analyze_by_confidence(self, enhanced_results, basic_results):
        """วิเคราะห์ตามระดับความมั่นใจ"""
        print(f"\n🎯 วิเคราะห์ตามระดับความมั่นใจ:")
        
        confidence_levels = [0.5, 0.6, 0.7, 0.8]
        
        for level in confidence_levels:
            # Enhanced Model
            enhanced_high_conf = [r for r in enhanced_results if r['confidence'] > level]
            enhanced_high_conf_correct = sum(r['correct'] for r in enhanced_high_conf)
            enhanced_high_conf_acc = enhanced_high_conf_correct / len(enhanced_high_conf) if enhanced_high_conf else 0
            
            # Basic Model
            basic_high_conf = [r for r in basic_results if r['confidence'] > level]
            basic_high_conf_correct = sum(r['correct'] for r in basic_high_conf)
            basic_high_conf_acc = basic_high_conf_correct / len(basic_high_conf) if basic_high_conf else 0
            
            print(f"   ความมั่นใจ > {level:.1f}:")
            print(f"     Enhanced: {enhanced_high_conf_correct}/{len(enhanced_high_conf)} = {enhanced_high_conf_acc:.3f} ({enhanced_high_conf_acc*100:.1f}%)")
            print(f"     Basic:    {basic_high_conf_correct}/{len(basic_high_conf)} = {basic_high_conf_acc:.3f} ({basic_high_conf_acc*100:.1f}%)")
    
    def analyze_by_outcome_type(self, enhanced_results, basic_results):
        """วิเคราะห์ตามประเภทผลลัพธ์"""
        print(f"\n⚽ วิเคราะห์ตามประเภทผลลัพธ์:")
        
        outcome_types = ['Home Win', 'Away Win', 'Draw']
        
        for outcome in outcome_types:
            # ผลจริง
            actual_outcomes = [r for r in enhanced_results if r['actual'] == outcome]
            
            # Enhanced Model
            enhanced_correct_outcomes = [r for r in actual_outcomes if r['predicted'] == outcome]
            enhanced_acc = len(enhanced_correct_outcomes) / len(actual_outcomes) if actual_outcomes else 0
            
            # Basic Model
            basic_outcomes = [r for r in basic_results if r['actual'] == outcome]
            basic_correct_outcomes = [r for r in basic_outcomes if r['predicted'] == outcome]
            basic_acc = len(basic_correct_outcomes) / len(basic_outcomes) if basic_outcomes else 0
            
            print(f"   {outcome}: (จริง {len(actual_outcomes)} เกม)")
            print(f"     Enhanced: {len(enhanced_correct_outcomes)}/{len(actual_outcomes)} = {enhanced_acc:.3f} ({enhanced_acc*100:.1f}%)")
            print(f"     Basic:    {len(basic_correct_outcomes)}/{len(basic_outcomes)} = {basic_acc:.3f} ({basic_acc*100:.1f}%)")
    
    def analyze_by_time_period(self, enhanced_results, basic_results):
        """วิเคราะห์ตามช่วงเวลา"""
        print(f"\n📅 วิเคราะห์ตามช่วงเวลา (แบ่งเป็น 4 ช่วง):")
        
        # แบ่งเป็น 4 ช่วงๆ ละ 25 เกม
        for i in range(4):
            start_idx = i * 25
            end_idx = (i + 1) * 25
            
            enhanced_period = enhanced_results[start_idx:end_idx]
            basic_period = basic_results[start_idx:end_idx]
            
            enhanced_correct = sum(r['correct'] for r in enhanced_period)
            basic_correct = sum(r['correct'] for r in basic_period)
            
            enhanced_acc = enhanced_correct / len(enhanced_period)
            basic_acc = basic_correct / len(basic_period)
            
            print(f"   ช่วงที่ {i+1} (เกม {start_idx+1}-{end_idx}):")
            print(f"     Enhanced: {enhanced_correct}/25 = {enhanced_acc:.3f} ({enhanced_acc*100:.1f}%)")
            print(f"     Basic:    {basic_correct}/25 = {basic_acc:.3f} ({basic_acc*100:.1f}%)")
    
    def create_analysis_charts(self, enhanced_results, basic_results):
        """สร้างกราฟวิเคราะห์"""
        print(f"\n📈 กำลังสร้างกราฟวิเคราะห์...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # กราฟที่ 1: เปรียบเทียบความแม่นยำ
        models = ['Enhanced Model', 'Basic Model']
        accuracies = [
            sum(r['correct'] for r in enhanced_results) / len(enhanced_results),
            sum(r['correct'] for r in basic_results) / len(basic_results)
        ]
        
        bars1 = ax1.bar(models, accuracies, color=['#2E8B57', '#4682B4'])
        ax1.set_title('เปรียบเทียบความแม่นยำ (100 เกม)', fontsize=14, pad=20)
        ax1.set_ylabel('ความแม่นยำ')
        ax1.set_ylim(0, 1)
        
        # เพิ่มค่าบนแท่ง
        for bar, acc in zip(bars1, accuracies):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{acc:.3f}\n({acc*100:.1f}%)', ha='center', va='bottom')
        
        # กราฟที่ 2: การกระจายความมั่นใจ
        ax2.hist([r['confidence'] for r in enhanced_results], bins=20, alpha=0.7, 
                label='Enhanced', color='#2E8B57')
        ax2.hist([r['confidence'] for r in basic_results], bins=20, alpha=0.7, 
                label='Basic', color='#4682B4')
        ax2.set_title('การกระจายความมั่นใจ')
        ax2.set_xlabel('ความมั่นใจ')
        ax2.set_ylabel('จำนวน')
        ax2.legend()
        
        # กราฟที่ 3: ความแม่นยำตามประเภทผลลัพธ์
        outcome_types = ['Home Win', 'Away Win', 'Draw']
        enhanced_by_outcome = []
        basic_by_outcome = []
        
        for outcome in outcome_types:
            enhanced_actual = [r for r in enhanced_results if r['actual'] == outcome]
            enhanced_correct = [r for r in enhanced_actual if r['predicted'] == outcome]
            enhanced_acc = len(enhanced_correct) / len(enhanced_actual) if enhanced_actual else 0
            enhanced_by_outcome.append(enhanced_acc)
            
            basic_actual = [r for r in basic_results if r['actual'] == outcome]
            basic_correct = [r for r in basic_actual if r['predicted'] == outcome]
            basic_acc = len(basic_correct) / len(basic_actual) if basic_actual else 0
            basic_by_outcome.append(basic_acc)
        
        x = np.arange(len(outcome_types))
        width = 0.35
        
        ax3.bar(x - width/2, enhanced_by_outcome, width, label='Enhanced', color='#2E8B57')
        ax3.bar(x + width/2, basic_by_outcome, width, label='Basic', color='#4682B4')
        ax3.set_title('ความแม่นยำตามประเภทผลลัพธ์')
        ax3.set_xlabel('ประเภทผลลัพธ์')
        ax3.set_ylabel('ความแม่นยำ')
        ax3.set_xticks(x)
        ax3.set_xticklabels(outcome_types)
        ax3.legend()
        
        # กราฟที่ 4: ความแม่นยำตามช่วงเวลา
        periods = ['ช่วง 1', 'ช่วง 2', 'ช่วง 3', 'ช่วง 4']
        enhanced_by_period = []
        basic_by_period = []
        
        for i in range(4):
            start_idx = i * 25
            end_idx = (i + 1) * 25
            
            enhanced_period = enhanced_results[start_idx:end_idx]
            basic_period = basic_results[start_idx:end_idx]
            
            enhanced_acc = sum(r['correct'] for r in enhanced_period) / len(enhanced_period)
            basic_acc = sum(r['correct'] for r in basic_period) / len(basic_period)
            
            enhanced_by_period.append(enhanced_acc)
            basic_by_period.append(basic_acc)
        
        x = np.arange(len(periods))
        ax4.bar(x - width/2, enhanced_by_period, width, label='Enhanced', color='#2E8B57')
        ax4.bar(x + width/2, basic_by_period, width, label='Basic', color='#4682B4')
        ax4.set_title('ความแม่นยำตามช่วงเวลา')
        ax4.set_xlabel('ช่วงเวลา (25 เกม/ช่วง)')
        ax4.set_ylabel('ความแม่นยำ')
        ax4.set_xticks(x)
        ax4.set_xticklabels(periods)
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig('/Users/80090/Desktop/Project/untitle/100_matches_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ บันทึกกราฟใน 100_matches_analysis.png")
    
    def run_comprehensive_test(self):
        """รันการทดสอบครบถ้วน 100 เกม"""
        print("🏆 การทดสอบครบถ้วน 100 เกมล่าสุด")
        print("🔬 เปรียบเทียบ Enhanced Model vs Basic Model")
        print("="*100)
        
        # โหลดข้อมูล
        if not self.load_data():
            return
        
        # ทดสอบ 100 เกม
        results = self.test_100_matches()
        
        if results:
            print(f"\n🏆 สรุปการทดสอบ 100 เกม:")
            print(f"✅ Enhanced Model: {results['enhanced']['accuracy']*100:.1f}% accuracy")
            print(f"📊 Basic Model: {results['basic']['accuracy']*100:.1f}% accuracy")
            print(f"🚀 การปรับปรุง: +{(results['enhanced']['accuracy'] - results['basic']['accuracy'])*100:.1f} percentage points")
            
            if results['enhanced']['accuracy'] > 0.55:
                print(f"\n🎉 ยอดเยี่ยม! Enhanced Model ให้ความแม่นยำสูงกว่า 55%")
            elif results['enhanced']['accuracy'] > 0.50:
                print(f"\n✅ ดี! Enhanced Model ให้ความแม่นยำสูงกว่า 50%")
            elif results['enhanced']['accuracy'] > results['basic']['accuracy']:
                print(f"\n📈 Enhanced Model ดีกว่า Basic Model")
            else:
                print(f"\n📝 ผลการทดสอบใกล้เคียงกัน")
        
        return results

def main():
    tester = Comprehensive100MatchTest()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
