#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 CORRECTED EMPEROR CUP ANALYSIS
แก้ไขการคำนวณที่ผิดพลาดและเรียงตามเวลาไทย
"""

import pandas as pd
import numpy as np
from datetime import datetime

def calculate_correct_predictions(home_stats, away_stats):
    """คำนวณการทำนายที่ถูกต้อง"""
    
    # คำนวณประตูที่คาดหวัง
    expected_home_goals = (home_stats['avg_goals_for'] + away_stats['avg_goals_against']) / 2 * 1.1
    expected_away_goals = (away_stats['avg_goals_for'] + home_stats['avg_goals_against']) / 2
    total_expected_goals = expected_home_goals + expected_away_goals
    
    # Over/Under 2.5 - สูตรที่ถูกต้อง
    if total_expected_goals >= 3.0:
        over_25_prob = min(75, int(total_expected_goals * 22))
    elif total_expected_goals >= 2.5:
        over_25_prob = min(65, int(total_expected_goals * 25))
    else:
        over_25_prob = max(20, int(total_expected_goals * 30))
    
    under_25_prob = 100 - over_25_prob
    
    # คำนวณเตะมุม
    expected_home_corners = (home_stats['avg_corners_for'] + away_stats['avg_corners_against']) / 2
    expected_away_corners = (away_stats['avg_corners_for'] + home_stats['avg_corners_against']) / 2
    total_expected_corners = expected_home_corners + expected_away_corners
    
    # Corner Over/Under 9.5 - แก้ไขให้ถูกต้อง
    if total_expected_corners >= 11.0:
        corners_over_9_prob = min(80, int(total_expected_corners * 6.5))
    elif total_expected_corners >= 9.5:
        corners_over_9_prob = min(65, int(total_expected_corners * 6.8))
    elif total_expected_corners >= 8.5:
        corners_over_9_prob = min(45, int(total_expected_corners * 5.2))
    else:
        corners_over_9_prob = max(15, int(total_expected_corners * 4.0))
    
    corners_under_9_prob = 100 - corners_over_9_prob
    
    # ผลการแข่งขัน
    home_strength = home_stats['win_rate'] * 1.15
    away_strength = away_stats['win_rate'] * 0.95
    
    home_strength += (home_stats['avg_goals_for'] - 1.2) * 0.1
    away_strength += (away_stats['avg_goals_for'] - 1.2) * 0.1
    
    total_strength = home_strength + away_strength + 0.25
    
    if total_strength > 0:
        home_win_prob = max(15, min(70, int((home_strength / total_strength) * 100)))
        away_win_prob = max(15, min(70, int((away_strength / total_strength) * 100)))
        draw_prob = max(10, 100 - home_win_prob - away_win_prob)
    else:
        home_win_prob = 40
        away_win_prob = 35
        draw_prob = 25
    
    # Handicap
    strength_diff = home_strength - away_strength
    if strength_diff > 0.1:
        handicap_home_prob = min(75, home_win_prob + 15)
    elif strength_diff < -0.1:
        handicap_home_prob = max(25, home_win_prob - 10)
    else:
        handicap_home_prob = home_win_prob + 5
    
    handicap_away_prob = 100 - handicap_home_prob
    
    return {
        'over_25_prob': over_25_prob,
        'under_25_prob': under_25_prob,
        'corners_over_9_prob': corners_over_9_prob,
        'corners_under_9_prob': corners_under_9_prob,
        'handicap_home_prob': handicap_home_prob,
        'handicap_away_prob': handicap_away_prob,
        'home_win_prob': home_win_prob,
        'draw_prob': draw_prob,
        'away_win_prob': away_win_prob,
        'expected_total_goals': round(total_expected_goals, 1),
        'expected_total_corners': round(total_expected_corners, 1)
    }

def convert_to_thai_time(utc_time_str):
    """แปลงเวลา UTC เป็นเวลาไทย"""
    time_part = utc_time_str.split('T')[1][:5]
    hour, minute = map(int, time_part.split(':'))
    thai_hour = (hour + 7) % 24
    return f'{thai_hour:02d}:{minute:02d}'

def main():
    print("🔧 Creating Corrected Emperor Cup Analysis...")
    
    # Read original data
    df = pd.read_csv('fixed_emperor_cup_analysis_20250716_124315.csv')
    
    # Team stats (from our real data analysis)
    team_stats = {
        'Cerezo Osaka': {'avg_goals_for': 1.8, 'avg_goals_against': 1.2, 'avg_corners_for': 6.3, 'avg_corners_against': 4.5, 'win_rate': 0.2},
        'Tokushima Vortis': {'avg_goals_for': 1.0, 'avg_goals_against': 1.8, 'avg_corners_for': 4.5, 'avg_corners_against': 6.3, 'win_rate': 0.6},
        'Kawasaki Frontale': {'avg_goals_for': 1.8, 'avg_goals_against': 1.8, 'avg_corners_for': 6.1, 'avg_corners_against': 6.4, 'win_rate': 0.6},
        'Sagamihara': {'avg_goals_for': 1.8, 'avg_goals_against': 1.8, 'avg_corners_for': 6.4, 'avg_corners_against': 6.1, 'win_rate': 0.4},
        'Vissel Kobe': {'avg_goals_for': 1.8, 'avg_goals_against': 1.4, 'avg_corners_for': 6.8, 'avg_corners_against': 5.6, 'win_rate': 0.4},
        'Ventforet Kofu': {'avg_goals_for': 1.4, 'avg_goals_against': 1.8, 'avg_corners_for': 5.6, 'avg_corners_against': 6.8, 'win_rate': 0.4},
        'Nagoya Grampus': {'avg_goals_for': 2.0, 'avg_goals_against': 1.8, 'avg_corners_for': 7.2, 'avg_corners_against': 6.9, 'win_rate': 0.4},
        'Roasso Kumamoto': {'avg_goals_for': 1.8, 'avg_goals_against': 2.0, 'avg_corners_for': 6.9, 'avg_corners_against': 7.2, 'win_rate': 0.4},
        'Albirex Niigata': {'avg_goals_for': 2.2, 'avg_goals_against': 2.0, 'avg_corners_for': 7.2, 'avg_corners_against': 7.1, 'win_rate': 0.4},
        'Toyo University': {'avg_goals_for': 2.0, 'avg_goals_against': 2.2, 'avg_corners_for': 7.1, 'avg_corners_against': 7.2, 'win_rate': 0.8},
        'Tokyo Verdy': {'avg_goals_for': 0.6, 'avg_goals_against': 1.8, 'avg_corners_for': 3.0, 'avg_corners_against': 6.5, 'win_rate': 0.2},
        'Sagan Tosu': {'avg_goals_for': 1.8, 'avg_goals_against': 0.6, 'avg_corners_for': 6.5, 'avg_corners_against': 3.0, 'win_rate': 0.6},
        'Gamba Osaka': {'avg_goals_for': 2.0, 'avg_goals_against': 1.8, 'avg_corners_for': 7.4, 'avg_corners_against': 6.4, 'win_rate': 0.4},
        'Montedio Yamagata': {'avg_goals_for': 1.8, 'avg_goals_against': 2.0, 'avg_corners_for': 6.4, 'avg_corners_against': 7.4, 'win_rate': 0.6},
        'FC Tokyo': {'avg_goals_for': 1.0, 'avg_goals_against': 1.6, 'avg_corners_for': 4.1, 'avg_corners_against': 5.8, 'win_rate': 0.4},
        'Oita Trinita': {'avg_goals_for': 1.6, 'avg_goals_against': 1.0, 'avg_corners_for': 5.8, 'avg_corners_against': 4.1, 'win_rate': 0.8},
        'Machida Zelvia': {'avg_goals_for': 1.4, 'avg_goals_against': 1.2, 'avg_corners_for': 5.7, 'avg_corners_against': 4.9, 'win_rate': 0.4},
        'Kataller Toyama': {'avg_goals_for': 1.2, 'avg_goals_against': 1.4, 'avg_corners_for': 4.9, 'avg_corners_against': 5.7, 'win_rate': 0.4},
        'Kashima Antlers': {'avg_goals_for': 1.8, 'avg_goals_against': 2.4, 'avg_corners_for': 6.1, 'avg_corners_against': 7.6, 'win_rate': 0.6},
        'V-varen Nagasaki': {'avg_goals_for': 2.4, 'avg_goals_against': 1.8, 'avg_corners_for': 7.6, 'avg_corners_against': 6.1, 'win_rate': 0.6},
        'Avispa Fukuoka': {'avg_goals_for': 0.8, 'avg_goals_against': 1.4, 'avg_corners_for': 4.0, 'avg_corners_against': 5.6, 'win_rate': 0.2},
        'Giravanz Kitakyushu': {'avg_goals_for': 1.4, 'avg_goals_against': 0.8, 'avg_corners_for': 5.6, 'avg_corners_against': 4.0, 'win_rate': 0.2},
        'Shonan Bellmare': {'avg_goals_for': 1.4, 'avg_goals_against': 1.2, 'avg_corners_for': 5.1, 'avg_corners_against': 5.3, 'win_rate': 0.6},
        'Shimizu S-Pulse': {'avg_goals_for': 1.2, 'avg_goals_against': 1.4, 'avg_corners_for': 5.3, 'avg_corners_against': 5.1, 'win_rate': 1.0},
        'Sanfrecce Hiroshima': {'avg_goals_for': 2.2, 'avg_goals_against': 0.4, 'avg_corners_for': 7.9, 'avg_corners_against': 3.0, 'win_rate': 0.8},
        'Fujieda MYFC': {'avg_goals_for': 0.4, 'avg_goals_against': 2.2, 'avg_corners_for': 3.0, 'avg_corners_against': 7.9, 'win_rate': 0.0},
        'Kyoto Sanga': {'avg_goals_for': 1.0, 'avg_goals_against': 0.2, 'avg_corners_for': 4.9, 'avg_corners_against': 3.0, 'win_rate': 0.2},
        'Yokohama FC': {'avg_goals_for': 0.2, 'avg_goals_against': 1.0, 'avg_corners_for': 3.0, 'avg_corners_against': 4.9, 'win_rate': 0.2},
        'Urawa Red Diamonds': {'avg_goals_for': 1.8, 'avg_goals_against': 1.4, 'avg_corners_for': 6.8, 'avg_corners_against': 5.2, 'win_rate': 0.4},
        'Consadole Sapporo': {'avg_goals_for': 1.4, 'avg_goals_against': 1.8, 'avg_corners_for': 5.2, 'avg_corners_against': 6.8, 'win_rate': 0.4}
    }
    
    # Recalculate all predictions
    corrected_results = []
    
    for i, row in df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        
        home_stats = team_stats.get(home_team, team_stats['Cerezo Osaka'])  # Default fallback
        away_stats = team_stats.get(away_team, team_stats['Tokushima Vortis'])
        
        # Recalculate predictions
        predictions = calculate_correct_predictions(home_stats, away_stats)
        
        # Convert to Thai time
        thai_time = convert_to_thai_time(row['date'])
        sort_hour = int(row['date'].split('T')[1][:2]) + 7
        
        result = {
            'match_id': i + 1,
            'thai_time': thai_time,
            'sort_hour': sort_hour,
            'date': row['date'],
            'home_team': home_team,
            'away_team': away_team,
            'venue': row['venue'],
            'league': 'Emperor Cup',
            'round': '3rd Round',
            'home_goals_avg': home_stats['avg_goals_for'],
            'away_goals_avg': away_stats['avg_goals_for'],
            'home_corners_avg': home_stats['avg_corners_for'],
            'away_corners_avg': away_stats['avg_corners_for'],
            'home_win_rate': home_stats['win_rate'],
            'away_win_rate': away_stats['win_rate'],
            'over_25_prob': predictions['over_25_prob'],
            'under_25_prob': predictions['under_25_prob'],
            'corners_over_9_prob': predictions['corners_over_9_prob'],
            'corners_under_9_prob': predictions['corners_under_9_prob'],
            'handicap_home_prob': predictions['handicap_home_prob'],
            'handicap_away_prob': predictions['handicap_away_prob'],
            'home_win_prob': predictions['home_win_prob'],
            'draw_prob': predictions['draw_prob'],
            'away_win_prob': predictions['away_win_prob']
        }
        
        corrected_results.append(result)
    
    # Create DataFrame and sort by Thai time
    corrected_df = pd.DataFrame(corrected_results)
    corrected_df = corrected_df.sort_values('sort_hour').reset_index(drop=True)
    
    # Save corrected CSV
    csv_filename = f'/Users/80090/Desktop/Project/untitle/corrected_emperor_cup_thai_time_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    corrected_df.to_csv(csv_filename, index=False, encoding='utf-8')
    
    print(f"✅ Corrected analysis saved to: {csv_filename}")
    
    # Check Kyoto Sanga vs Yokohama FC specifically
    kyoto_match = corrected_df[(corrected_df['home_team'] == 'Kyoto Sanga') & (corrected_df['away_team'] == 'Yokohama FC')]
    if not kyoto_match.empty:
        row = kyoto_match.iloc[0]
        total_corners = row['home_corners_avg'] + row['away_corners_avg']
        print(f"\n🔍 Kyoto Sanga vs Yokohama FC (CORRECTED):")
        print(f"   Total Expected Corners: {total_corners:.1f}")
        print(f"   Corner Over 9.5: {row['corners_over_9_prob']}% / {row['corners_under_9_prob']}%")
        print(f"   Thai Time: {row['thai_time']}")
    
    return csv_filename, corrected_df

if __name__ == "__main__":
    main()
