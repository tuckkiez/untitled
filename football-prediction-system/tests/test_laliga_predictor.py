#!/usr/bin/env python3
"""
🇪🇸 ทดสอบระบบ La Liga Predictor
แยกต่างหากจาก Premier League
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import ระบบ La Liga ที่สร้างขึ้น
from laliga_predictor_complete import LaLigaPredictor
import pandas as pd
import numpy as np

def test_laliga_system():
    """ทดสอบระบบ La Liga แยกต่างหาก"""
    print("🇪🇸 ทดสอบระบบ La Liga Advanced Predictor")
    print("=" * 60)
    print("📝 หมายเหตุ: ระบบนี้แยกต่างหากจาก Premier League")
    print("=" * 60)
    
    # สร้าง La Liga Predictor
    predictor = LaLigaPredictor()
    
    # โหลดข้อมูล La Liga
    print("\n📊 กำลังโหลดข้อมูล La Liga...")
    data = predictor.load_laliga_data()
    
    print(f"✅ โหลดข้อมูลสำเร็จ: {len(data)} เกม")
    
    # แสดงตัวอย่างข้อมูล
    print(f"\n📋 ตัวอย่างข้อมูล La Liga:")
    print(data.head())
    
    # แสดงทีมใน La Liga
    teams = sorted(set(data['home_team'].unique()) | set(data['away_team'].unique()))
    print(f"\n🏆 ทีมใน La Liga ({len(teams)} ทีม):")
    for i, team in enumerate(teams, 1):
        print(f"   {i:2d}. {team}")
    
    # เทรนโมเดล
    print(f"\n🤖 กำลังเทรนโมเดล La Liga...")
    success = predictor.train_ensemble_models(data)
    
    if not success:
        print("❌ การเทรนไม่สำเร็จ")
        return False
    
    # ทดสอบการทำนาย
    print(f"\n🎯 ทดสอบการทำนาย La Liga:")
    print("-" * 40)
    
    test_matches = [
        ('Real Madrid', 'FC Barcelona'),
        ('Atletico Madrid', 'Real Sociedad'),
        ('Sevilla FC', 'Valencia CF'),
        ('Athletic Bilbao', 'Real Betis'),
        ('Villarreal CF', 'RC Celta')
    ]
    
    results = []
    
    for home, away in test_matches:
        print(f"\n⚽ {home} vs {away}")
        result = predictor.predict_match_laliga(home, away)
        
        if result:
            results.append(result)
            print(f"   🎯 ทำนาย: {result['prediction']}")
            print(f"   💪 ความมั่นใจ: {result['confidence']:.1%}")
            
            probs = result['probabilities']
            print(f"   📊 {home} ชนะ: {probs['Home Win']:.1%}")
            print(f"   📊 เสมอ: {probs['Draw']:.1%}")
            print(f"   📊 {away} ชนะ: {probs['Away Win']:.1%}")
        else:
            print("   ❌ ไม่สามารถทำนายได้")
    
    # สรุปผลการทดสอบ
    print(f"\n📊 สรุปผลการทดสอบ:")
    print("=" * 40)
    
    if results:
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        print(f"✅ ทำนายสำเร็จ: {len(results)}/{len(test_matches)} คู่")
        print(f"📈 ความมั่นใจเฉลี่ย: {avg_confidence:.1%}")
        
        # นับการทำนาย
        predictions = [r['prediction'] for r in results]
        home_wins = predictions.count('Home Win')
        draws = predictions.count('Draw')
        away_wins = predictions.count('Away Win')
        
        print(f"🏠 ทำนายเจ้าบ้านชนะ: {home_wins} คู่")
        print(f"🤝 ทำนายเสมอ: {draws} คู่")
        print(f"✈️ ทำนายทีมเยือนชนะ: {away_wins} คู่")
        
        if avg_confidence > 0.5:
            print(f"\n✅ ระบบ La Liga Predictor ทำงานได้ดี!")
            print(f"🎯 ความมั่นใจสูงกว่า 50%")
        else:
            print(f"\n⚠️ ระบบต้องปรับปรุงเพิ่มเติม")
    else:
        print("❌ ไม่สามารถทำนายได้เลย")
    
    return True

def compare_with_premier_league():
    """เปรียบเทียบกับระบบ Premier League"""
    print(f"\n🔍 เปรียบเทียบกับระบบ Premier League:")
    print("-" * 40)
    
    try:
        from ultra_predictor_fixed import UltraAdvancedPredictor
        
        # ทดสอบ Premier League
        print("🏴󠁧󠁢󠁥󠁮󠁧󠁿 ทดสอบ Premier League:")
        pl_predictor = UltraAdvancedPredictor()
        pl_data = pl_predictor.load_premier_league_data()
        pl_predictor.train_ensemble_models(pl_data)
        
        pl_result = pl_predictor.predict_match_ultra('Arsenal', 'Chelsea')
        print(f"   Arsenal vs Chelsea: {pl_result['prediction']} ({pl_result['confidence']:.1%})")
        
        # ทดสอบ La Liga
        print("🇪🇸 ทดสอบ La Liga:")
        laliga_predictor = LaLigaPredictor()
        laliga_data = laliga_predictor.load_laliga_data()
        laliga_predictor.train_ensemble_models(laliga_data)
        
        laliga_result = laliga_predictor.predict_match_laliga('Real Madrid', 'FC Barcelona')
        print(f"   Real Madrid vs Barcelona: {laliga_result['prediction']} ({laliga_result['confidence']:.1%})")
        
        print(f"\n📊 เปรียบเทียบ:")
        print(f"   Premier League ข้อมูล: {len(pl_data)} เกม")
        print(f"   La Liga ข้อมูล: {len(laliga_data)} เกม")
        print(f"   Premier League ความมั่นใจ: {pl_result['confidence']:.1%}")
        print(f"   La Liga ความมั่นใจ: {laliga_result['confidence']:.1%}")
        
    except Exception as e:
        print(f"❌ Error comparing systems: {e}")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 La Liga Advanced Predictor - Independent System")
    print("🇪🇸 ระบบทำนายลีกสเปนแยกต่างหาก")
    print("=" * 70)
    
    # ทดสอบระบบ La Liga
    success = test_laliga_system()
    
    if success:
        # เปรียบเทียบกับ Premier League
        compare_with_premier_league()
        
        print(f"\n🎉 การทดสอบเสร็จสิ้น!")
        print(f"✅ ระบบ La Liga Predictor พร้อมใช้งาน")
        print(f"📝 ระบบนี้แยกต่างหากจาก Premier League")
        print(f"🔧 สามารถใช้งานได้อิสระ")
    else:
        print(f"\n❌ การทดสอบไม่สำเร็จ")
        print(f"🔧 ต้องแก้ไขปัญหาก่อนใช้งาน")

if __name__ == "__main__":
    main()
