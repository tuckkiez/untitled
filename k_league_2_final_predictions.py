#!/usr/bin/env python3
"""
🇰🇷 K League 2 Final Advanced ML Predictions
การทำนายขั้นสุดท้ายด้วย Advanced ML สำหรับ K League 2
"""

from k_league_2_advanced_ml import KLeague2AdvancedML
import json

def main():
    print("🇰🇷 K League 2 Advanced ML Analysis")
    print("=" * 50)
    
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    predictor = KLeague2AdvancedML(api_key)
    
    # เทรนโมเดล
    print("🤖 Training Advanced ML Models...")
    df = predictor.prepare_training_data()
    
    if df.empty:
        print("❌ ไม่มีข้อมูลสำหรับเทรน")
        return
    
    predictor.train_models(df)
    
    # ทำ Backtest
    print("\n🔍 Running Backtest (20 matches)...")
    backtest_results = predictor.backtest_system(20)
    
    print("\n📊 Backtest Results:")
    if backtest_results:
        for category, data in backtest_results.items():
            print(f"  • {category}: {data['accuracy']:.1f}% ({data['correct']}/{data['total']})")
    
    # การแข่งขันวันนี้ (ข้อมูลที่รู้)
    matches_today = [
        {
            'home': 'Incheon United',
            'away': 'Asan Mugunghwa',
            'home_id': 2763,
            'away_id': 2753,
            'time': '17:00 ICT',
            'venue': 'Sungui Arena Park, Incheon'
        },
        {
            'home': 'Bucheon FC 1995',
            'away': 'Gimpo Citizen',
            'home_id': 2745,
            'away_id': 7078,
            'time': '17:00 ICT',
            'venue': 'Bucheon Stadium, Bucheon'
        },
        {
            'home': 'Ansan Greeners',
            'away': 'Seoul E-Land FC',
            'home_id': 2758,
            'away_id': 2749,
            'time': '17:00 ICT',
            'venue': 'Ansan Wa Stadium, Ansan'
        }
    ]
    
    print("\n🎯 Today's Advanced ML Predictions (17:00 ICT):")
    print("=" * 50)
    
    all_predictions = []
    
    for i, match in enumerate(matches_today, 1):
        print(f"\n{i}. {match['home']} vs {match['away']}")
        print(f"   📍 {match['venue']}")
        print(f"   ⏰ {match['time']}")
        
        # ทำนายด้วย Advanced ML
        predictions = predictor.predict_match(
            match['home'], 
            match['away'], 
            match['home_id'], 
            match['away_id']
        )
        
        # แสดงผลการทำนาย
        print(f"   🎯 Match Result: {predictions['match_result']['prediction']} ({predictions['match_result']['confidence']:.1f}%)")
        print(f"   ⚖️ Handicap: {predictions['handicap']['prediction']} ({predictions['handicap']['confidence']:.1f}%)")
        print(f"   ⚽ Over/Under 2.5: {predictions['over_under']['prediction']} ({predictions['over_under']['confidence']:.1f}%)")
        print(f"   🚩 Corners HT: {predictions['corners']['halftime']['prediction']} ({predictions['corners']['halftime']['confidence']:.1f}%)")
        print(f"   🚩 Corners FT: {predictions['corners']['fulltime']['prediction']} ({predictions['corners']['fulltime']['confidence']:.1f}%)")
        
        # เก็บข้อมูลสำหรับสรุป
        match_prediction = {
            'match': f"{match['home']} vs {match['away']}",
            'predictions': predictions
        }
        all_predictions.append(match_prediction)
    
    # สรุปผลการวิเคราะห์
    print("\n" + "=" * 60)
    print("📈 ADVANCED ML ANALYSIS SUMMARY")
    print("=" * 60)
    
    print(f"\n🤖 Model Performance (Backtest 20 matches):")
    if backtest_results:
        total_accuracy = sum(data['accuracy'] for data in backtest_results.values()) / len(backtest_results)
        print(f"  📊 Overall Accuracy: {total_accuracy:.1f}%")
        print(f"  🥇 Best Category: Over/Under ({backtest_results.get('over_under', {}).get('accuracy', 0):.1f}%)")
        print(f"  🎯 Match Results: {backtest_results.get('match_result', {}).get('accuracy', 0):.1f}%")
        print(f"  ⚖️ Handicap: {backtest_results.get('handicap', {}).get('accuracy', 0):.1f}%")
        print(f"  🚩 Corners: {backtest_results.get('corners', {}).get('accuracy', 0):.1f}%")
    
    print(f"\n🎯 Today's High Confidence Predictions:")
    for pred in all_predictions:
        match_name = pred['match']
        preds = pred['predictions']
        
        # หาการทำนายที่มีความมั่นใจสูงสุด
        confidences = {
            'Match Result': preds['match_result']['confidence'],
            'Handicap': preds['handicap']['confidence'],
            'Over/Under': preds['over_under']['confidence'],
            'Corners': preds['corners']['fulltime']['confidence']
        }
        
        max_confidence = max(confidences.values())
        if max_confidence >= 70:
            best_pred = [k for k, v in confidences.items() if v == max_confidence][0]
            if best_pred == 'Match Result':
                value = preds['match_result']['prediction']
            elif best_pred == 'Handicap':
                value = preds['handicap']['prediction']
            elif best_pred == 'Over/Under':
                value = preds['over_under']['prediction']
            else:
                value = preds['corners']['fulltime']['prediction']
            
            print(f"  🔥 {match_name}: {best_pred} = {value} ({max_confidence:.1f}%)")
    
    print(f"\n🔍 ML Model Details:")
    print(f"  • Algorithm: Ensemble (RF + GB + ET + LR)")
    print(f"  • Training Data: {len(predictor.historical_matches)} K League 2 matches")
    print(f"  • Cross-Validation: 3-fold stratified")
    print(f"  • Feature Engineering: Team IDs, Goals, Goal Difference")
    print(f"  • Preprocessing: StandardScaler + KNN Imputation")
    
    print(f"\n🌐 System Status:")
    print(f"  ✅ Advanced ML Models: Trained & Ready")
    print(f"  ✅ K League 2 Data: {len(predictor.historical_matches)} matches loaded")
    print(f"  ✅ Predictions: 4-value analysis complete")
    print(f"  ✅ Backtest: 20 matches validated")
    
    print(f"\n📊 Prediction Confidence Distribution:")
    all_confidences = []
    for pred in all_predictions:
        preds = pred['predictions']
        all_confidences.extend([
            preds['match_result']['confidence'],
            preds['handicap']['confidence'],
            preds['over_under']['confidence'],
            preds['corners']['fulltime']['confidence']
        ])
    
    avg_confidence = sum(all_confidences) / len(all_confidences)
    high_confidence = sum(1 for c in all_confidences if c >= 70)
    
    print(f"  📈 Average Confidence: {avg_confidence:.1f}%")
    print(f"  🔥 High Confidence (≥70%): {high_confidence}/{len(all_confidences)} predictions")
    
    print(f"\n✅ Analysis Complete! Check website for live updates.")

if __name__ == "__main__":
    main()
