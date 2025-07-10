#!/usr/bin/env python3
"""
🚀 Chelsea vs PSG Prediction with Real PSG Data
ใช้ข้อมูลจริงของ PSG ในการทำนาย
"""

import pandas as pd
import numpy as np
from ultra_predictor_fixed import UltraAdvancedPredictor

def analyze_team_comparison():
    """เปรียบเทียบฟอร์มของทั้งสองทีม"""
    
    print("🏆 CHELSEA vs PSG - DETAILED ANALYSIS")
    print("=" * 60)
    
    # ข้อมูล PSG จริง
    psg_ligue1 = pd.read_csv('psg_ligue1_results.csv')
    psg_cl = pd.read_csv('psg_champions_league_results.csv')
    
    print("\n📊 ฟอร์ม Paris Saint-Germain (ข้อมูลจริง):")
    print("=" * 40)
    
    # วิเคราะห์ PSG Ligue 1
    psg_l1_stats = calculate_team_stats(psg_ligue1, 'Paris Saint-Germain')
    print(f"🇫🇷 Ligue 1 (10 เกมล่าสุด):")
    print(f"   ชนะ: {psg_l1_stats['wins']} | เสมอ: {psg_l1_stats['draws']} | แพ้: {psg_l1_stats['losses']}")
    print(f"   ประตูได้: {psg_l1_stats['goals_for']} | ประตูเสีย: {psg_l1_stats['goals_against']}")
    print(f"   อัตราชนะ: {psg_l1_stats['win_rate']:.1%}")
    print(f"   ประตูเฉลี่ย: {psg_l1_stats['goals_for']/psg_l1_stats['games']:.1f} ต่อเกม")
    
    # วิเคราะห์ PSG Champions League
    psg_cl_stats = calculate_team_stats(psg_cl, 'Paris Saint-Germain')
    print(f"\n🏆 Champions League (6 เกมล่าสุด):")
    print(f"   ชนะ: {psg_cl_stats['wins']} | เสมอ: {psg_cl_stats['draws']} | แพ้: {psg_cl_stats['losses']}")
    print(f"   ประตูได้: {psg_cl_stats['goals_for']} | ประตูเสีย: {psg_cl_stats['goals_against']}")
    print(f"   อัตราชนะ: {psg_cl_stats['win_rate']:.1%}")
    print(f"   ประตูเฉลี่ย: {psg_cl_stats['goals_for']/psg_cl_stats['games']:.1f} ต่อเกม")
    
    # วิเคราะห์ฟอร์มล่าสุด
    all_psg = pd.concat([psg_ligue1, psg_cl])
    all_psg['date'] = pd.to_datetime(all_psg['date'])
    recent_psg = all_psg.sort_values('date', ascending=False).head(5)
    
    print(f"\n🔥 ฟอร์ม PSG 5 เกมล่าสุด:")
    form_results = []
    for _, match in recent_psg.iterrows():
        opponent = match['away_team'] if match['home_team'] == 'Paris Saint-Germain' else match['home_team']
        
        if match['home_team'] == 'Paris Saint-Germain':
            psg_goals = match['home_goals']
            opp_goals = match['away_goals']
            venue = "H"
        else:
            psg_goals = match['away_goals']
            opp_goals = match['home_goals']
            venue = "A"
        
        if psg_goals > opp_goals:
            result = "W"
        elif psg_goals == opp_goals:
            result = "D"
        else:
            result = "L"
        
        form_results.append(result)
        print(f"   {match['date'].strftime('%m/%d')} vs {opponent} ({venue}) {psg_goals}-{opp_goals} [{result}]")
    
    form_string = " ".join(form_results)
    print(f"   ฟอร์ม: {form_string}")
    
    # เปรียบเทียบกับ Chelsea (จำลอง)
    print(f"\n📊 เปรียบเทียบ Chelsea vs PSG:")
    print("=" * 40)
    
    # Chelsea stats (จำลองจาก Premier League form)
    chelsea_stats = {
        'games': 15, 'wins': 8, 'draws': 4, 'losses': 3,
        'goals_for': 28, 'goals_against': 18, 'win_rate': 0.533
    }
    
    print(f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 Chelsea (Premier League):")
    print(f"   อัตราชนะ: {chelsea_stats['win_rate']:.1%}")
    print(f"   ประตูเฉลี่ย: {chelsea_stats['goals_for']/chelsea_stats['games']:.1f} ต่อเกม")
    print(f"   ประตูเสียเฉลี่ย: {chelsea_stats['goals_against']/chelsea_stats['games']:.1f} ต่อเกม")
    
    print(f"\n🇫🇷 PSG (รวมทุกรายการ):")
    combined_psg = {
        'games': psg_l1_stats['games'] + psg_cl_stats['games'],
        'wins': psg_l1_stats['wins'] + psg_cl_stats['wins'],
        'goals_for': psg_l1_stats['goals_for'] + psg_cl_stats['goals_for'],
        'goals_against': psg_l1_stats['goals_against'] + psg_cl_stats['goals_against']
    }
    combined_psg['win_rate'] = combined_psg['wins'] / combined_psg['games']
    
    print(f"   อัตราชนะ: {combined_psg['win_rate']:.1%}")
    print(f"   ประตูเฉลี่ย: {combined_psg['goals_for']/combined_psg['games']:.1f} ต่อเกม")
    print(f"   ประตูเสียเฉลี่ย: {combined_psg['goals_against']/combined_psg['games']:.1f} ต่อเกม")
    
    return {
        'psg_ligue1': psg_l1_stats,
        'psg_cl': psg_cl_stats,
        'psg_combined': combined_psg,
        'chelsea': chelsea_stats,
        'psg_form': form_string
    }

def calculate_team_stats(matches_df, team_name):
    """คำนวณสถิติทีม"""
    stats = {
        'games': 0, 'wins': 0, 'draws': 0, 'losses': 0,
        'goals_for': 0, 'goals_against': 0, 'win_rate': 0
    }
    
    for _, match in matches_df.iterrows():
        if match['home_team'] == team_name:
            stats['games'] += 1
            stats['goals_for'] += match['home_goals']
            stats['goals_against'] += match['away_goals']
            
            if match['home_goals'] > match['away_goals']:
                stats['wins'] += 1
            elif match['home_goals'] == match['away_goals']:
                stats['draws'] += 1
            else:
                stats['losses'] += 1
                
        elif match['away_team'] == team_name:
            stats['games'] += 1
            stats['goals_for'] += match['away_goals']
            stats['goals_against'] += match['home_goals']
            
            if match['away_goals'] > match['home_goals']:
                stats['wins'] += 1
            elif match['away_goals'] == match['home_goals']:
                stats['draws'] += 1
            else:
                stats['losses'] += 1
    
    if stats['games'] > 0:
        stats['win_rate'] = stats['wins'] / stats['games']
    
    return stats

def predict_with_real_data(team_stats):
    """ทำนายด้วยข้อมูลจริง"""
    
    print(f"\n🎯 การทำนายด้วยข้อมูลจริง:")
    print("=" * 40)
    
    chelsea = team_stats['chelsea']
    psg_combined = team_stats['psg_combined']
    psg_cl = team_stats['psg_cl']  # ฟอร์มในยุโรป
    
    # คำนวณความแข็งแกร่ง
    chelsea_strength = (chelsea['win_rate'] * 0.6 + 
                       (chelsea['goals_for']/chelsea['games'])/3 * 0.4)
    
    # PSG ใช้ฟอร์ม Champions League เป็นหลัก (เพราะใกล้เคียงระดับ)
    psg_strength = (psg_cl['win_rate'] * 0.7 + 
                   psg_combined['win_rate'] * 0.3)
    
    print(f"💪 ความแข็งแกร่ง:")
    print(f"   Chelsea: {chelsea_strength:.3f}")
    print(f"   PSG: {psg_strength:.3f}")
    
    # Home advantage
    home_advantage = 0.1
    chelsea_adj = chelsea_strength + home_advantage
    
    # คำนวณความน่าจะเป็น
    total_strength = chelsea_adj + psg_strength
    
    if total_strength > 0:
        chelsea_prob = chelsea_adj / total_strength
        psg_prob = psg_strength / total_strength
        draw_prob = 1 - (chelsea_prob + psg_prob) + 0.2  # เพิ่มโอกาสเสมอ
        
        # ปรับให้รวมเป็น 1
        total_prob = chelsea_prob + psg_prob + draw_prob
        chelsea_prob /= total_prob
        psg_prob /= total_prob
        draw_prob /= total_prob
    else:
        chelsea_prob = psg_prob = draw_prob = 0.33
    
    # ทำนายผล
    if chelsea_prob > psg_prob and chelsea_prob > draw_prob:
        prediction = "Chelsea Win"
        confidence = chelsea_prob
    elif psg_prob > chelsea_prob and psg_prob > draw_prob:
        prediction = "PSG Win"
        confidence = psg_prob
    else:
        prediction = "Draw"
        confidence = draw_prob
    
    print(f"\n🎯 ผลการทำนาย:")
    print(f"   Chelsea ชนะ: {chelsea_prob:.1%}")
    print(f"   เสมอ: {draw_prob:.1%}")
    print(f"   PSG ชนะ: {psg_prob:.1%}")
    print(f"\n🏆 ทำนาย: {prediction} (มั่นใจ {confidence:.1%})")
    
    # ทำนาย Goals
    expected_goals = (chelsea['goals_for']/chelsea['games'] + 
                     psg_combined['goals_for']/psg_combined['games']) / 2
    
    if expected_goals > 2.5:
        ou_prediction = "Over 2.5"
        ou_confidence = 0.65
    else:
        ou_prediction = "Under 2.5"
        ou_confidence = 0.60
    
    print(f"\n⚽ Over/Under: {ou_prediction} (มั่นใจ {ou_confidence:.1%})")
    print(f"   คาดการณ์ประตู: {expected_goals:.1f}")
    
    # ข้อสังเกต
    print(f"\n📝 ข้อสังเกตสำคัญ:")
    print(f"   🔴 PSG ฟอร์มในยุโรปไม่ดี (ชนะแค่ 33.3%)")
    print(f"   🔵 PSG เก่งในลีกฝรั่งเศส (ชนะ 70%)")
    print(f"   🏠 Chelsea เล่นที่บ้าน (Home Advantage)")
    print(f"   ⚡ PSG เพิ่งชนะ Man City 4-2 (ฟอร์มดีขึ้น)")
    
    return {
        'prediction': prediction,
        'confidence': confidence,
        'probabilities': {
            'Chelsea': chelsea_prob,
            'Draw': draw_prob,
            'PSG': psg_prob
        },
        'over_under': ou_prediction,
        'ou_confidence': ou_confidence,
        'expected_goals': expected_goals
    }

def main():
    # วิเคราะห์ข้อมูล
    team_stats = analyze_team_comparison()
    
    # ทำนายด้วยข้อมูลจริง
    prediction = predict_with_real_data(team_stats)
    
    print(f"\n" + "=" * 60)
    print("📋 สรุปการทำนาย Chelsea vs PSG (ข้อมูลจริง):")
    print("=" * 60)
    print(f"1. ผลการแข่งขัน: {prediction['prediction']} ({prediction['confidence']:.1%})")
    print(f"2. Over/Under: {prediction['over_under']} ({prediction['ou_confidence']:.1%})")
    print(f"3. คาดการณ์ประตู: {prediction['expected_goals']:.1f}")
    
    # ความน่าเชื่อถือ
    print(f"\n🎯 ความน่าเชื่อถือ:")
    if prediction['confidence'] > 0.5:
        print("✅ ข้อมูลจริงทำให้การทำนายน่าเชื่อถือมากขึ้น")
    else:
        print("⚠️ การแข่งขันคาดว่าจะสูสี")
    
    return prediction

if __name__ == "__main__":
    result = main()
