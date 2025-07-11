#!/usr/bin/env python3
"""
📊 เปรียบเทียบประสิทธิภาพ
Single League (Premier League) vs Multi League (PL + La Liga)
"""

import pandas as pd
import numpy as np
from ultra_predictor_fixed import UltraAdvancedPredictor

def test_single_league():
    """ทดสอบระบบด้วย Premier League เท่านั้น"""
    print("🏴󠁧󠁢󠁥󠁮󠁧󠁿 ทดสอบระบบ Single League (Premier League)")
    print("=" * 50)
    
    predictor = UltraAdvancedPredictor()
    data = predictor.load_premier_league_data()
    predictor.train_ensemble_models(data)
    
    # ทดสอบการทำนาย
    test_matches = [
        ('Arsenal', 'Chelsea'),
        ('Manchester City', 'Liverpool'),
        ('Manchester United', 'Tottenham'),
        ('Newcastle United', 'Brighton'),
        ('Aston Villa', 'West Ham United')
    ]
    
    results = []
    total_confidence = 0
    
    print("\n🎯 ผลการทำนาย:")
    for home, away in test_matches:
        result = predictor.predict_match_ultra(home, away)
        results.append(result)
        total_confidence += result['confidence']
        print(f"   {home} vs {away}: {result['prediction']} ({result['confidence']:.1%})")
    
    avg_confidence = total_confidence / len(test_matches)
    
    return {
        'type': 'Single League',
        'data_size': len(data),
        'avg_confidence': avg_confidence,
        'results': results,
        'model_accuracy': getattr(predictor, 'last_ensemble_score', 0.51)
    }

def test_multi_league():
    """ทดสอบระบบด้วย Premier League + La Liga"""
    print("\n🌍 ทดสอบระบบ Multi League (PL + La Liga)")
    print("=" * 50)
    
    # โหลดข้อมูลรวม
    try:
        combined_data = pd.read_csv('combined_pl_laliga_data.csv')
        print(f"✅ โหลดข้อมูลรวมสำเร็จ: {len(combined_data)} เกม")
    except:
        print("❌ ไม่พบไฟล์ข้อมูลรวม กำลังสร้างใหม่...")
        from add_laliga_data import combine_premier_league_and_laliga
        combined_data = combine_premier_league_and_laliga()
    
    predictor = UltraAdvancedPredictor()
    predictor.train_ensemble_models(combined_data)
    
    # ทดสอบการทำนายเดียวกัน
    test_matches = [
        ('Arsenal', 'Chelsea'),
        ('Manchester City', 'Liverpool'),
        ('Manchester United', 'Tottenham'),
        ('Newcastle United', 'Brighton'),
        ('Aston Villa', 'West Ham United')
    ]
    
    results = []
    total_confidence = 0
    
    print("\n🎯 ผลการทำนาย:")
    for home, away in test_matches:
        result = predictor.predict_match_ultra(home, away)
        results.append(result)
        total_confidence += result['confidence']
        print(f"   {home} vs {away}: {result['prediction']} ({result['confidence']:.1%})")
    
    avg_confidence = total_confidence / len(test_matches)
    
    # ทดสอบ La Liga teams
    print("\n🇪🇸 ทดสอบทีม La Liga:")
    laliga_matches = [
        ('Real Madrid', 'FC Barcelona'),
        ('Atletico Madrid', 'Real Sociedad')
    ]
    
    for home, away in laliga_matches:
        result = predictor.predict_match_ultra(home, away)
        print(f"   {home} vs {away}: {result['prediction']} ({result['confidence']:.1%})")
    
    return {
        'type': 'Multi League',
        'data_size': len(combined_data),
        'avg_confidence': avg_confidence,
        'results': results,
        'model_accuracy': getattr(predictor, 'last_ensemble_score', 0.51)
    }

def compare_performance(single_result, multi_result):
    """เปรียบเทียบประสิทธิภาพ"""
    print(f"\n📊 การเปรียบเทียบประสิทธิภาพ")
    print("=" * 60)
    
    print(f"📈 ข้อมูลการเทรน:")
    print(f"   Single League: {single_result['data_size']} เกม")
    print(f"   Multi League:  {multi_result['data_size']} เกม")
    print(f"   เพิ่มขึ้น: +{multi_result['data_size'] - single_result['data_size']} เกม ({((multi_result['data_size'] / single_result['data_size']) - 1) * 100:.1f}%)")
    
    print(f"\n🎯 ความมั่นใจเฉลี่ย:")
    print(f"   Single League: {single_result['avg_confidence']:.1%}")
    print(f"   Multi League:  {multi_result['avg_confidence']:.1%}")
    
    confidence_diff = multi_result['avg_confidence'] - single_result['avg_confidence']
    if confidence_diff > 0:
        print(f"   ✅ ปรับปรุง: +{confidence_diff:.1%}")
    else:
        print(f"   ❌ ลดลง: {confidence_diff:.1%}")
    
    print(f"\n🤖 ประสิทธิภาพโมเดล:")
    print(f"   Single League: {single_result['model_accuracy']:.1%}")
    print(f"   Multi League:  {multi_result['model_accuracy']:.1%}")
    
    accuracy_diff = multi_result['model_accuracy'] - single_result['model_accuracy']
    if accuracy_diff > 0:
        print(f"   ✅ ปรับปรุง: +{accuracy_diff:.1%}")
    else:
        print(f"   ❌ ลดลง: {accuracy_diff:.1%}")
    
    # เปรียบเทียบการทำนายแต่ละคู่
    print(f"\n🔍 เปรียบเทียบการทำนายแต่ละคู่:")
    matches = ['Arsenal vs Chelsea', 'Man City vs Liverpool', 'Man Utd vs Tottenham', 
               'Newcastle vs Brighton', 'Aston Villa vs West Ham']
    
    for i, match in enumerate(matches):
        single_pred = single_result['results'][i]
        multi_pred = multi_result['results'][i]
        
        print(f"   {match}:")
        print(f"     Single: {single_pred['prediction']} ({single_pred['confidence']:.1%})")
        print(f"     Multi:  {multi_pred['prediction']} ({multi_pred['confidence']:.1%})")
        
        if single_pred['prediction'] != multi_pred['prediction']:
            print(f"     🔄 การทำนายเปลี่ยน!")
        
        conf_diff = multi_pred['confidence'] - single_pred['confidence']
        if abs(conf_diff) > 0.05:
            if conf_diff > 0:
                print(f"     📈 ความมั่นใจเพิ่ม: +{conf_diff:.1%}")
            else:
                print(f"     📉 ความมั่นใจลด: {conf_diff:.1%}")

def analyze_data_quality():
    """วิเคราะห์คุณภาพข้อมูล"""
    print(f"\n🔬 วิเคราะห์คุณภาพข้อมูล")
    print("=" * 40)
    
    try:
        combined_data = pd.read_csv('combined_pl_laliga_data.csv')
        
        # แยกตามลีก
        pl_data = combined_data[combined_data['league'] == 'Premier League']
        laliga_data = combined_data[combined_data['league'] == 'La Liga']
        
        print(f"📊 การกระจายข้อมูล:")
        print(f"   Premier League: {len(pl_data)} เกม ({len(pl_data)/len(combined_data)*100:.1f}%)")
        print(f"   La Liga: {len(laliga_data)} เกม ({len(laliga_data)/len(combined_data)*100:.1f}%)")
        
        # วิเคราะห์ประตู
        print(f"\n⚽ สถิติประตู:")
        print(f"   Premier League เฉลี่ย: {(pl_data['home_goals'] + pl_data['away_goals']).mean():.2f} ประตู/เกม")
        print(f"   La Liga เฉลี่ย: {(laliga_data['home_goals'] + laliga_data['away_goals']).mean():.2f} ประตู/เกม")
        
        # วิเคราะห์ผลการแข่งขัน
        def analyze_results(data, league_name):
            home_wins = len(data[data['home_goals'] > data['away_goals']])
            draws = len(data[data['home_goals'] == data['away_goals']])
            away_wins = len(data[data['home_goals'] < data['away_goals']])
            total = len(data)
            
            print(f"   {league_name}:")
            print(f"     เจ้าบ้านชนะ: {home_wins/total*100:.1f}%")
            print(f"     เสมอ: {draws/total*100:.1f}%")
            print(f"     ทีมเยือนชนะ: {away_wins/total*100:.1f}%")
        
        print(f"\n🏆 ผลการแข่งขัน:")
        analyze_results(pl_data, "Premier League")
        analyze_results(laliga_data, "La Liga")
        
    except Exception as e:
        print(f"❌ Error analyzing data: {e}")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 การเปรียบเทียบประสิทธิภาพ Single vs Multi League")
    print("=" * 70)
    
    # ทดสอบทั้งสองระบบ
    single_result = test_single_league()
    multi_result = test_multi_league()
    
    # เปรียบเทียบ
    compare_performance(single_result, multi_result)
    
    # วิเคราะห์ข้อมูล
    analyze_data_quality()
    
    # สรุปผล
    print(f"\n🎯 สรุปผลการทดสอบ:")
    print("=" * 40)
    
    if multi_result['avg_confidence'] > single_result['avg_confidence']:
        print("✅ การเพิ่ม La Liga ช่วยปรับปรุงความมั่นใจในการทำนาย")
    else:
        print("⚠️ การเพิ่ม La Liga ไม่ได้ปรับปรุงความมั่นใจ")
    
    if multi_result['model_accuracy'] > single_result['model_accuracy']:
        print("✅ การเพิ่ม La Liga ช่วยปรับปรุงประสิทธิภาพโมเดล")
    else:
        print("⚠️ การเพิ่ม La Liga ไม่ได้ปรับปรุงประสิทธิภาพโมเดล")
    
    print(f"\n💡 คำแนะนำ:")
    if (multi_result['avg_confidence'] > single_result['avg_confidence'] and 
        multi_result['model_accuracy'] >= single_result['model_accuracy']):
        print("🟢 แนะนำให้ใช้ระบบ Multi League")
        print("   - ข้อมูลมากขึ้นช่วยปรับปรุงการทำนาย")
        print("   - พร้อมเพิ่มลีกอื่นๆ ต่อไป")
    else:
        print("🟡 ควรปรับแต่งเพิ่มเติมก่อนเพิ่มลีกอื่น")
        print("   - อาจต้องปรับ feature engineering")
        print("   - หรือปรับสัดส่วนข้อมูลระหว่างลีก")
    
    return single_result, multi_result

if __name__ == "__main__":
    single, multi = main()
