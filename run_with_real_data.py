#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
รันระบบทำนายฟุตบอลด้วยข้อมูลจริงจาก football-data.org API
"""

from real_data_example import RealDataPredictor
from football_predictor import FootballPredictor
import pandas as pd
from datetime import datetime

def main():
    # API Token ของคุณ
    API_TOKEN = "052fd4885cf943ad859c89cef542e2e5"
    
    print("=== ระบบทำนายฟุตบอลด้วยข้อมูลจริง ===")
    print("กำลังเชื่อมต่อกับ football-data.org API...")
    
    # สร้าง predictor
    predictor = RealDataPredictor(api_key=API_TOKEN)
    
    try:
        # ดึงข้อมูลพรีเมียร์ลีกฤดูกาล 2024
        print("\n1. กำลังดึงข้อมูลพรีเมียร์ลีกฤดูกาล 2024...")
        historical_data = predictor.get_premier_league_data(season=2024)
        
        if historical_data is None:
            print("❌ ไม่สามารถดึงข้อมูลได้ กรุณาตรวจสอบ API token")
            return
        
        print(f"✅ ดึงข้อมูลสำเร็จ: {len(historical_data)} เกม")
        print(f"📅 ช่วงเวลา: {historical_data['date'].min()} ถึง {historical_data['date'].max()}")
        
        # แสดงข้อมูลตัวอย่าง
        print("\n📋 ตัวอย่างข้อมูลล่าสุด:")
        print(historical_data.tail(5)[['date', 'home_team', 'away_team', 'home_goals', 'away_goals']].to_string(index=False))
        
        # ตรวจสอบว่ามีข้อมูลเพียงพอหรือไม่
        if len(historical_data) < 50:
            print(f"⚠️  ข้อมูลไม่เพียงพอสำหรับการเทรน (มี {len(historical_data)} เกม, ต้องการอย่างน้อย 50 เกม)")
            print("💡 ลองดึงข้อมูลจากฤดูกาลก่อนหน้าด้วย...")
            
            # ดึงข้อมูลฤดูกาล 2023 เพิ่มเติม
            historical_2023 = predictor.get_premier_league_data(season=2023)
            if historical_2023 is not None:
                historical_data = pd.concat([historical_2023, historical_data], ignore_index=True)
                historical_data = historical_data.sort_values('date').reset_index(drop=True)
                print(f"✅ รวมข้อมูลแล้ว: {len(historical_data)} เกม")
        
        # เทรนโมเดล
        print(f"\n2. กำลังเทรนโมเดลด้วยข้อมูลจริง...")
        football_predictor = FootballPredictor()
        
        if not football_predictor.train(historical_data):
            print("❌ ไม่สามารถเทรนโมเดลได้")
            return
        
        # วิเคราะห์ผลงานทีม
        print(f"\n3. การวิเคราะห์ผลงานทีมจากข้อมูลจริง:")
        team_stats = analyze_real_team_performance(historical_data)
        print(team_stats.head(10).to_string(index=False))
        
        # บันทึกผลการวิเคราะห์
        team_stats.to_csv('/Users/80090/Desktop/Project/untitle/real_team_analysis.csv', index=False)
        print(f"\n💾 บันทึกการวิเคราะห์ทีมใน real_team_analysis.csv")
        
        # ดึงข้อมูลการแข่งขันที่กำลังจะมาถึง
        print(f"\n4. กำลังดึงข้อมูลการแข่งขันที่กำลังจะมาถึง...")
        upcoming_matches = predictor.get_upcoming_matches(days_ahead=14)
        
        if upcoming_matches is not None and len(upcoming_matches) > 0:
            print(f"🔮 พบการแข่งขัน {len(upcoming_matches)} นัดในอีก 14 วันข้างหน้า:")
            print(upcoming_matches[['date', 'time', 'home_team', 'away_team']].to_string(index=False))
            
            # ทำนายผลการแข่งขันที่กำลังจะมาถึง
            print(f"\n5. การทำนายการแข่งขันที่กำลังจะมาถึง:")
            predictions = []
            
            for _, match in upcoming_matches.iterrows():
                result = football_predictor.predict_match(
                    match['home_team'], 
                    match['away_team'], 
                    historical_data
                )
                
                if result:
                    predictions.append({
                        'date': match['date'],
                        'time': match['time'],
                        'home_team': match['home_team'],
                        'away_team': match['away_team'],
                        'prediction': result['prediction'],
                        'confidence': result['confidence'],
                        'home_win_prob': result['probabilities']['Home Win'],
                        'draw_prob': result['probabilities']['Draw'],
                        'away_win_prob': result['probabilities']['Away Win']
                    })
                    
                    print(f"\n📅 {match['date']} {match['time']}")
                    print(f"⚽ {match['home_team']} vs {match['away_team']}")
                    print(f"🎯 การทำนาย: {result['prediction']}")
                    print(f"🎲 ความมั่นใจ: {result['confidence']:.3f} ({result['confidence']*100:.1f}%)")
                    print("📊 ความน่าจะเป็น:")
                    for outcome, prob in result['probabilities'].items():
                        print(f"   {outcome}: {prob:.3f} ({prob*100:.1f}%)")
            
            # บันทึกการทำนาย
            if predictions:
                predictions_df = pd.DataFrame(predictions)
                predictions_df.to_csv('/Users/80090/Desktop/Project/untitle/real_predictions.csv', index=False)
                print(f"\n💾 บันทึกการทำนายใน real_predictions.csv")
        else:
            print("ℹ️  ไม่มีการแข่งขันที่กำลังจะมาถึงในช่วงนี้")
        
        # ทำ backtest กับข้อมูลจริง
        print(f"\n6. การทำ Backtest กับข้อมูลจริง:")
        if len(historical_data) >= 100:
            backtest_games = min(50, len(historical_data) // 4)
            backtest_result = football_predictor.backtest(historical_data, test_period_games=backtest_games)
            
            if backtest_result:
                print(f"📈 ผล Backtest จากข้อมูลจริง:")
                print(f"   จำนวนเกมที่ทดสอบ: {backtest_result['total_games']}")
                print(f"   ทำนายถูก: {backtest_result['correct_predictions']}")
                print(f"   ความแม่นยำ: {backtest_result['accuracy']:.3f} ({backtest_result['accuracy']*100:.1f}%)")
        else:
            print("ℹ️  ข้อมูลไม่เพียงพอสำหรับ backtest")
        
        # ตัวอย่างการทำนายคู่ยอดนิยม
        print(f"\n7. ตัวอย่างการทำนายคู่ยอดนิยม:")
        popular_matches = [
            ('Arsenal', 'Chelsea'),
            ('Manchester City', 'Liverpool'),
            ('Manchester United', 'Tottenham'),
            ('Newcastle United', 'Brighton & Hove Albion')
        ]
        
        for home, away in popular_matches:
            result = football_predictor.predict_match(home, away, historical_data)
            if result:
                print(f"\n⚽ {home} vs {away}")
                print(f"🎯 การทำนาย: {result['prediction']}")
                print(f"🎲 ความมั่นใจ: {result['confidence']:.3f} ({result['confidence']*100:.1f}%)")
        
        print(f"\n✅ การวิเคราะห์เสร็จสมบูรณ์!")
        print(f"📁 ไฟล์ที่สร้างขึ้น:")
        print(f"   - real_team_analysis.csv (การวิเคราะห์ทีม)")
        print(f"   - real_predictions.csv (การทำนายการแข่งขันที่กำลังจะมาถึง)")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        print("💡 กรุณาตรวจสอบ:")
        print("   1. API token ถูกต้องหรือไม่")
        print("   2. การเชื่อมต่ออินเทอร์เน็ต")
        print("   3. API rate limit (ฟรีแพลนมีข้อจำกัด)")

def analyze_real_team_performance(matches_df):
    """วิเคราะห์ผลงานทีมจากข้อมูลจริง"""
    teams = list(set(matches_df['home_team'].tolist() + matches_df['away_team'].tolist()))
    team_stats = []
    
    for team in teams:
        # หาเกมของทีม
        home_games = matches_df[matches_df['home_team'] == team]
        away_games = matches_df[matches_df['away_team'] == team]
        
        # คำนวณสถิติ
        total_games = len(home_games) + len(away_games)
        
        if total_games == 0:
            continue
        
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
            'win_rate': round(total_wins / total_games, 3) if total_games > 0 else 0,
            'points_per_game': round(points / total_games, 3) if total_games > 0 else 0
        })
    
    team_stats_df = pd.DataFrame(team_stats)
    team_stats_df = team_stats_df.sort_values('points', ascending=False).reset_index(drop=True)
    team_stats_df.index = team_stats_df.index + 1  # เริ่มอันดับจาก 1
    
    return team_stats_df

if __name__ == "__main__":
    main()
