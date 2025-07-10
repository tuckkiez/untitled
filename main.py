#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from football_predictor import FootballPredictor
from data_loader import FootballDataLoader, create_sample_csv
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import argparse

def plot_backtest_results(backtest_result):
    """แสดงกราฟผล backtest"""
    if not backtest_result or not backtest_result['results']:
        print("ไม่มีข้อมูล backtest ให้แสดง")
        return
    
    results_df = pd.DataFrame(backtest_result['results'])
    
    # กราฟความแม่นยำตามความมั่นใจ
    plt.figure(figsize=(12, 8))
    
    # กราฟที่ 1: การกระจายของความมั่นใจ
    plt.subplot(2, 2, 1)
    plt.hist(results_df['confidence'], bins=20, alpha=0.7, color='skyblue')
    plt.title('การกระจายของความมั่นใจในการทำนาย')
    plt.xlabel('ความมั่นใจ')
    plt.ylabel('จำนวน')
    
    # กราฟที่ 2: ความแม่นยำตามช่วงความมั่นใจ
    plt.subplot(2, 2, 2)
    confidence_bins = pd.cut(results_df['confidence'], bins=5)
    accuracy_by_confidence = results_df.groupby(confidence_bins)['correct'].mean()
    accuracy_by_confidence.plot(kind='bar', color='lightgreen')
    plt.title('ความแม่นยำตามช่วงความมั่นใจ')
    plt.xlabel('ช่วงความมั่นใจ')
    plt.ylabel('ความแม่นยำ')
    plt.xticks(rotation=45)
    
    # กราฟที่ 3: ผลการทำนายแต่ละประเภท
    plt.subplot(2, 2, 3)
    prediction_counts = results_df['predicted'].value_counts()
    prediction_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightcoral', 'lightyellow', 'lightblue'])
    plt.title('สัดส่วนการทำนายแต่ละประเภท')
    
    # กราฟที่ 4: ความแม่นยำของแต่ละประเภทการทำนาย
    plt.subplot(2, 2, 4)
    accuracy_by_prediction = results_df.groupby('predicted')['correct'].mean()
    accuracy_by_prediction.plot(kind='bar', color='orange')
    plt.title('ความแม่นยำของแต่ละประเภทการทำนาย')
    plt.xlabel('ประเภทการทำนาย')
    plt.ylabel('ความแม่นยำ')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('/Users/80090/Desktop/Project/untitle/backtest_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def analyze_team_performance(matches_df):
    """วิเคราะห์ผลงานของแต่ละทีม"""
    teams = list(set(matches_df['home_team'].tolist() + matches_df['away_team'].tolist()))
    team_stats = []
    
    for team in teams:
        # หาเกมของทีม
        home_games = matches_df[matches_df['home_team'] == team]
        away_games = matches_df[matches_df['away_team'] == team]
        
        # คำนวณสถิติ
        total_games = len(home_games) + len(away_games)
        
        # ผลการแข่งขัน
        home_wins = len(home_games[home_games['home_goals'] > home_games['away_goals']])
        home_draws = len(home_games[home_games['home_goals'] == home_games['away_goals']])
        home_losses = len(home_games[home_games['home_goals'] < home_games['away_goals']])
        
        away_wins = len(away_games[away_games['away_goals'] > away_games['home_goals']])
        away_draws = len(away_games[away_games['away_goals'] == away_games['home_goals']])
        away_losses = len(away_games[away_games['away_goals'] < away_games['home_goals']])
        
        total_wins = home_wins + away_wins
        total_draws = home_draws + away_draws
        total_losses = home_losses + away_losses
        
        # ประตู
        goals_for = (home_games['home_goals'].sum() + away_games['away_goals'].sum())
        goals_against = (home_games['away_goals'].sum() + away_games['home_goals'].sum())
        
        # คะแนน (3 แต้มต่อชนะ, 1 แต้มต่อเสมอ)
        points = total_wins * 3 + total_draws * 1
        
        team_stats.append({
            'team': team,
            'games': total_games,
            'wins': total_wins,
            'draws': total_draws,
            'losses': total_losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goals_for - goals_against,
            'points': points,
            'win_rate': total_wins / total_games if total_games > 0 else 0,
            'points_per_game': points / total_games if total_games > 0 else 0
        })
    
    team_stats_df = pd.DataFrame(team_stats)
    team_stats_df = team_stats_df.sort_values('points', ascending=False).reset_index(drop=True)
    
    return team_stats_df

def main():
    parser = argparse.ArgumentParser(description='ระบบทำนายผลฟุตบอล')
    parser.add_argument('--data-source', choices=['sample', 'csv', 'api'], default='sample',
                       help='แหล่งข้อมูล (sample/csv/api)')
    parser.add_argument('--data-path', type=str, help='path ของไฟล์ข้อมูล (สำหรับ csv)')
    parser.add_argument('--predict', nargs=2, metavar=('HOME_TEAM', 'AWAY_TEAM'),
                       help='ทำนายผลการแข่งขัน เช่น --predict "Arsenal" "Chelsea"')
    parser.add_argument('--backtest', action='store_true', help='ทำ backtest')
    parser.add_argument('--analyze', action='store_true', help='วิเคราะห์ผลงานทีม')
    parser.add_argument('--plot', action='store_true', help='แสดงกราฟ')
    
    args = parser.parse_args()
    
    print("=== ระบบทำนายผลฟุตบอล ===")
    print("พัฒนาโดยใช้ Machine Learning และการวิเคราะห์ทางสถิติ\n")
    
    # โหลดข้อมูล
    loader = FootballDataLoader()
    
    if args.data_source == 'sample':
        print("กำลังสร้างข้อมูลตัวอย่าง...")
        matches_df = create_sample_csv()
    elif args.data_source == 'csv':
        if not args.data_path:
            print("กรุณาระบุ path ของไฟล์ CSV ด้วย --data-path")
            return
        print(f"กำลังโหลดข้อมูลจาก {args.data_path}...")
        matches_df = loader.load_data('csv', args.data_path)
    else:
        print("API loading ยังไม่ได้ implement เต็มรูปแบบ")
        return
    
    if matches_df is None or len(matches_df) == 0:
        print("ไม่สามารถโหลดข้อมูลได้")
        return
    
    print(f"โหลดข้อมูลสำเร็จ: {len(matches_df)} เกม")
    print(f"ช่วงเวลา: {matches_df['date'].min()} ถึง {matches_df['date'].max()}")
    print(f"จำนวนทีม: {len(set(matches_df['home_team'].tolist() + matches_df['away_team'].tolist()))}")
    
    # วิเคราะห์ผลงานทีม
    if args.analyze:
        print("\n=== การวิเคราะห์ผลงานทีม ===")
        team_stats = analyze_team_performance(matches_df)
        print(team_stats.to_string(index=False))
        
        # บันทึกผลการวิเคราะห์
        team_stats.to_csv('/Users/80090/Desktop/Project/untitle/team_analysis.csv', index=False)
        print("\nบันทึกผลการวิเคราะห์ใน team_analysis.csv")
    
    # เทรนโมเดล
    print("\n=== การเทรนโมเดล ===")
    predictor = FootballPredictor()
    
    if not predictor.train(matches_df):
        print("ไม่สามารถเทรนโมเดลได้")
        return
    
    # ทำนายผลการแข่งขัน
    if args.predict:
        home_team, away_team = args.predict
        print(f"\n=== การทำนาย: {home_team} vs {away_team} ===")
        
        result = predictor.predict_match(home_team, away_team, matches_df)
        if result:
            print(f"การทำนาย: {result['prediction']}")
            print(f"ความมั่นใจ: {result['confidence']:.3f} ({result['confidence']*100:.1f}%)")
            print("\nความน่าจะเป็นของแต่ละผล:")
            for outcome, prob in result['probabilities'].items():
                print(f"  {outcome}: {prob:.3f} ({prob*100:.1f}%)")
        else:
            print("ไม่สามารถทำนายได้ (อาจเป็นเพราะไม่มีข้อมูลของทีมเหล่านี้)")
    
    # ทำ backtest
    if args.backtest:
        print("\n=== Backtest ===")
        backtest_result = predictor.backtest(matches_df, test_period_games=min(50, len(matches_df)//4))
        
        if backtest_result and args.plot:
            plot_backtest_results(backtest_result)
    
    print("\n=== สรุป ===")
    print("ระบบทำนายผลฟุตบอลพร้อมใช้งานแล้ว!")
    print("คุณสามารถ:")
    print("1. ทำนายผลการแข่งขันด้วย --predict 'ทีมเหย้า' 'ทีมเยือน'")
    print("2. ทำ backtest ด้วย --backtest")
    print("3. วิเคราะห์ผลงานทีมด้วย --analyze")
    print("4. แสดงกราฟด้วย --plot")

if __name__ == "__main__":
    main()
