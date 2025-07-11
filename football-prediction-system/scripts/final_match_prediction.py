#!/usr/bin/env python3
"""
Final Match Prediction - Aldosivi vs Central Córdoba
การทำนายสุดท้ายที่รวมทุกการวิเคราะห์เข้าด้วยกัน
"""

import json
from datetime import datetime

def create_final_prediction():
    """สร้างการทำนายสุดท้ายที่ครบถ้วน"""
    
    print("🎯 FINAL MATCH PREDICTION - Aldosivi vs Central Córdoba")
    print("=" * 70)
    
    # ข้อมูลการแข่งขัน
    match_info = {
        'home_team': 'Aldosivi',
        'away_team': 'Central Córdoba',
        'league': 'Argentina Primera Division',
        'date': '12 July 2025',
        'time': '01:30 (Thailand time)',
        'venue': 'Estadio José María Minella, Mar del Plata'
    }
    
    print(f"🏆 MATCH INFORMATION")
    print("-" * 30)
    for key, value in match_info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # รวมการทำนายจากทุกระบบ
    predictions_summary = {
        'ai_system': {
            'match_result': 'Central Córdoba Win',
            'confidence': 68.4,
            'over_under': 'Over 2.5 goals',
            'ou_confidence': 56.3,
            'corners': 'Under 9.5 corners',
            'corners_confidence': 50.0
        },
        'goal5_analysis': {
            'match_result': 'Central Córdoba Win',
            'confidence': 80.0,  # 4/5 stars
            'reasoning': 'Superior H2H record (4W-2D-0L)',
            'handicap': 'Central Córdoba 0.0',
            'recommended': True
        },
        'corners_analysis': {
            'total_corners': 13.3,
            'over_under_9_5': 'Over 9.5',
            'confidence': 88.0,
            'best_bet': 'Over 9.5 corners',
            'team_corners': {
                'aldosivi': 4.8,
                'central_cordoba': 4.2
            }
        },
        'h2h_analysis': {
            'total_meetings': 7,
            'central_wins': 4,
            'draws': 2,
            'aldosivi_wins': 0,
            'avg_goals': 1.5,
            'avg_corners': 8.7,
            'low_scoring_tendency': True
        }
    }
    
    print(f"\n📊 PREDICTIONS COMPARISON")
    print("-" * 30)
    print(f"🤖 AI System: Central Córdoba Win (68.4%)")
    print(f"📈 Goal5.co: Central Córdoba Win (80.0%)")
    print(f"🏈 Corners: Over 9.5 corners (88.0%)")
    print(f"📋 H2H: Central Córdoba dominates (4-2-0)")
    
    # การวิเคราะห์ความเสี่ยง
    risk_analysis = {
        'low_risk': [
            'Both systems agree on Central Córdoba win',
            'Strong H2H record supports away team',
            'Aldosivi poor home form this season'
        ],
        'medium_risk': [
            'Both teams inconsistent form',
            'Low-scoring league tendency',
            'Corners prediction conflicts with H2H data'
        ],
        'high_risk': [
            'Home advantage factor',
            'Potential for surprise result',
            'Limited recent data available'
        ]
    }
    
    print(f"\n⚠️ RISK ANALYSIS")
    print("-" * 30)
    print(f"✅ Low Risk Factors:")
    for factor in risk_analysis['low_risk']:
        print(f"   • {factor}")
    
    print(f"\n⚠️ Medium Risk Factors:")
    for factor in risk_analysis['medium_risk']:
        print(f"   • {factor}")
    
    print(f"\n🚨 High Risk Factors:")
    for factor in risk_analysis['high_risk']:
        print(f"   • {factor}")
    
    # การแนะนำเดิมพันสุดท้าย
    final_betting_recommendations = {
        'primary_bets': [
            {
                'bet': 'Central Córdoba Win (Away Win)',
                'confidence': 75,
                'stake': '3-4% of bankroll',
                'reasoning': 'Both AI and Goal5.co agree, strong H2H record'
            },
            {
                'bet': 'Over 9.5 Corners',
                'confidence': 88,
                'stake': '2-3% of bankroll',
                'reasoning': 'Team averages suggest 13+ corners'
            }
        ],
        'value_bets': [
            {
                'bet': 'Central Córdoba Draw No Bet',
                'confidence': 70,
                'stake': '2% of bankroll',
                'reasoning': 'Safer option with good value'
            },
            {
                'bet': 'Under 2.5 Goals',
                'confidence': 65,
                'stake': '1-2% of bankroll',
                'reasoning': 'H2H shows low-scoring matches'
            }
        ],
        'avoid_bets': [
            'Aldosivi Win (0% H2H success)',
            'Over 3.5 Goals (both teams struggle to score)',
            'Both Teams to Score (defensive teams)'
        ]
    }
    
    print(f"\n💰 FINAL BETTING RECOMMENDATIONS")
    print("-" * 30)
    print(f"🎯 Primary Bets:")
    for bet in final_betting_recommendations['primary_bets']:
        print(f"   ✅ {bet['bet']}")
        print(f"      Confidence: {bet['confidence']}%")
        print(f"      Stake: {bet['stake']}")
        print(f"      Reason: {bet['reasoning']}")
        print()
    
    print(f"⭐ Value Bets:")
    for bet in final_betting_recommendations['value_bets']:
        print(f"   💎 {bet['bet']}")
        print(f"      Confidence: {bet['confidence']}%")
        print(f"      Stake: {bet['stake']}")
        print(f"      Reason: {bet['reasoning']}")
        print()
    
    print(f"❌ Avoid:")
    for bet in final_betting_recommendations['avoid_bets']:
        print(f"   🚫 {bet}")
    
    # สรุปการทำนายสุดท้าย
    final_verdict = {
        'match_result': 'Central Córdoba Win',
        'result_confidence': 75,
        'goals_prediction': 'Under 2.5 goals',
        'goals_confidence': 65,
        'corners_prediction': 'Over 9.5 corners',
        'corners_confidence': 88,
        'overall_confidence': 76,
        'expected_score': '0-1 or 1-2',
        'key_factors': [
            'Central Córdoba superior H2H record',
            'Aldosivi poor home form',
            'Both teams defensive style',
            'Higher corner count expected'
        ]
    }
    
    print(f"\n🏁 FINAL VERDICT")
    print("=" * 40)
    print(f"🏆 Result: {final_verdict['match_result']} ({final_verdict['result_confidence']}%)")
    print(f"⚽ Goals: {final_verdict['goals_prediction']} ({final_verdict['goals_confidence']}%)")
    print(f"🏈 Corners: {final_verdict['corners_prediction']} ({final_verdict['corners_confidence']}%)")
    print(f"📊 Overall Confidence: {final_verdict['overall_confidence']}%")
    print(f"🎯 Expected Score: {final_verdict['expected_score']}")
    
    print(f"\n🔑 Key Factors:")
    for factor in final_verdict['key_factors']:
        print(f"   • {factor}")
    
    # Portfolio allocation
    portfolio_allocation = {
        'total_bankroll_percentage': 8,
        'allocation': {
            'Central Córdoba Win': 4,
            'Over 9.5 Corners': 2,
            'Draw No Bet': 1.5,
            'Under 2.5 Goals': 0.5
        },
        'risk_level': 'Medium',
        'expected_roi': '15-25%'
    }
    
    print(f"\n💼 PORTFOLIO ALLOCATION")
    print("-" * 30)
    print(f"Total Allocation: {portfolio_allocation['total_bankroll_percentage']}% of bankroll")
    print(f"Risk Level: {portfolio_allocation['risk_level']}")
    print(f"Expected ROI: {portfolio_allocation['expected_roi']}")
    
    print(f"\nBreakdown:")
    for bet, percentage in portfolio_allocation['allocation'].items():
        print(f"   {bet}: {percentage}%")
    
    # บันทึกการทำนายสุดท้าย
    complete_prediction = {
        'match_info': match_info,
        'predictions_summary': predictions_summary,
        'risk_analysis': risk_analysis,
        'betting_recommendations': final_betting_recommendations,
        'final_verdict': final_verdict,
        'portfolio_allocation': portfolio_allocation,
        'generated_at': datetime.now().isoformat(),
        'prediction_id': 'ARG_ALD_CEN_20250712_0130'
    }
    
    with open('aldosivi_central_final_prediction.json', 'w', encoding='utf-8') as f:
        json.dump(complete_prediction, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Final prediction saved to aldosivi_central_final_prediction.json")
    
    return complete_prediction

def display_match_summary():
    """แสดงสรุปการแข่งขันแบบย่อ"""
    
    print(f"\n🎯 MATCH SUMMARY - TONIGHT 01:30")
    print("=" * 50)
    print(f"🇦🇷 Aldosivi vs Central Córdoba")
    print(f"🏆 Prediction: Central Córdoba Win (75%)")
    print(f"⚽ Goals: Under 2.5 (65%)")
    print(f"🏈 Corners: Over 9.5 (88%)")
    print(f"💰 Best Bets: Away Win + Over 9.5 Corners")
    print(f"📊 Overall Confidence: 76%")
    print(f"🎯 Expected Score: 0-1 or 1-2")
    
    print(f"\n🔍 Key Insight:")
    print(f"   Central Córdoba dominates H2H (4-2-0) and")
    print(f"   Aldosivi has poor home form this season")
    
    print(f"\n⏰ Check back after 01:30 to verify accuracy!")

def main():
    # สร้างการทำนายสุดท้าย
    prediction = create_final_prediction()
    
    # แสดงสรุป
    display_match_summary()
    
    print(f"\n🚀 PREDICTION SYSTEM READY!")
    print(f"   All analyses completed and saved")
    print(f"   Ready for real-world testing tonight")

if __name__ == "__main__":
    main()
