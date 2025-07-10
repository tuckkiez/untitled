#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ตัวอย่างการใช้งานระบบทำนายฟุตบอลขั้นสูง
รวมถึงการปรับแต่งพารามิเตอร์และการวิเคราะห์เชิงลึก
"""

import pandas as pd
import numpy as np
from football_predictor import FootballPredictor
from data_loader import FootballDataLoader
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

class AdvancedFootballAnalyzer:
    def __init__(self):
        self.predictor = FootballPredictor()
        self.data_loader = FootballDataLoader()
        
    def create_realistic_data(self, num_seasons=2):
        """สร้างข้อมูลที่สมจริงมากขึ้น"""
        # ทีมพรีเมียร์ลีกพร้อมความแข็งแกร่ง
        teams_strength = {
            'Manchester City': 0.85,
            'Arsenal': 0.80,
            'Liverpool': 0.78,
            'Chelsea': 0.72,
            'Manchester United': 0.70,
            'Newcastle': 0.68,
            'Tottenham': 0.65,
            'Brighton': 0.62,
            'Aston Villa': 0.60,
            'West Ham': 0.58,
            'Crystal Palace': 0.55,
            'Fulham': 0.53,
            'Brentford': 0.50,
            'Wolves': 0.48,
            'Everton': 0.45,
            'Nottingham Forest': 0.43,
            'Bournemouth': 0.40,
            'Sheffield United': 0.35,
            'Burnley': 0.33,
            'Luton': 0.30
        }
        
        teams = list(teams_strength.keys())
        matches = []
        
        for season in range(num_seasons):
            season_start = datetime(2022 + season, 8, 1)
            
            # สร้างตารางแข่งขัน (แต่ละทีมเจอกัน 2 ครั้ง)
            for round_num in range(38):  # 38 รอบ
                round_date = season_start + timedelta(weeks=round_num)
                
                # สร้างคู่แข่งขันสำหรับรอบนี้
                teams_copy = teams.copy()
                np.random.shuffle(teams_copy)
                
                for i in range(0, len(teams_copy), 2):
                    if i + 1 < len(teams_copy):
                        home_team = teams_copy[i]
                        away_team = teams_copy[i + 1]
                        
                        # คำนวณผลการแข่งขันตามความแข็งแกร่ง
                        home_strength = teams_strength[home_team] + 0.1  # home advantage
                        away_strength = teams_strength[away_team]
                        
                        # เพิ่มความสุ่ม
                        home_performance = np.random.normal(home_strength, 0.2)
                        away_performance = np.random.normal(away_strength, 0.2)
                        
                        # คำนวณประตู
                        home_expected = max(0, home_performance * 2.5)
                        away_expected = max(0, away_performance * 2.5)
                        
                        home_goals = np.random.poisson(home_expected)
                        away_goals = np.random.poisson(away_expected)
                        
                        matches.append({
                            'date': round_date.strftime('%Y-%m-%d'),
                            'home_team': home_team,
                            'away_team': away_team,
                            'home_goals': home_goals,
                            'away_goals': away_goals,
                            'season': f"{2022 + season}-{2023 + season}",
                            'round': round_num + 1
                        })
        
        return pd.DataFrame(matches)
    
    def analyze_prediction_accuracy_by_team(self, matches_df, backtest_results):
        """วิเคราะห์ความแม่นยำการทำนายแยกตามทีม"""
        if not backtest_results or not backtest_results['results']:
            return None
        
        results_df = pd.DataFrame(backtest_results['results'])
        
        # วิเคราะห์ความแม่นยำของทีมเหย้า
        home_accuracy = results_df.groupby('home_team').agg({
            'correct': ['count', 'sum', 'mean'],
            'confidence': 'mean'
        }).round(3)
        
        home_accuracy.columns = ['total_games', 'correct_predictions', 'accuracy', 'avg_confidence']
        home_accuracy = home_accuracy.reset_index()
        home_accuracy['role'] = 'Home'
        home_accuracy = home_accuracy.rename(columns={'home_team': 'team'})
        
        # วิเคราะห์ความแม่นยำของทีมเยือน
        away_accuracy = results_df.groupby('away_team').agg({
            'correct': ['count', 'sum', 'mean'],
            'confidence': 'mean'
        }).round(3)
        
        away_accuracy.columns = ['total_games', 'correct_predictions', 'accuracy', 'avg_confidence']
        away_accuracy = away_accuracy.reset_index()
        away_accuracy['role'] = 'Away'
        away_accuracy = away_accuracy.rename(columns={'away_team': 'team'})
        
        # รวมข้อมูล
        combined_accuracy = pd.concat([home_accuracy, away_accuracy], ignore_index=True)
        team_summary = combined_accuracy.groupby('team').agg({
            'total_games': 'sum',
            'correct_predictions': 'sum',
            'avg_confidence': 'mean'
        }).round(3)
        
        team_summary['accuracy'] = (team_summary['correct_predictions'] / 
                                  team_summary['total_games']).round(3)
        
        return team_summary.sort_values('accuracy', ascending=False)
    
    def compare_prediction_methods(self, matches_df):
        """เปรียบเทียบวิธีการทำนายต่างๆ"""
        print("=== การเปรียบเทียบวิธีการทำนาย ===")
        
        # วิธีที่ 1: Random Forest (ปัจจุบัน)
        rf_predictor = FootballPredictor()
        rf_predictor.train(matches_df)
        rf_backtest = rf_predictor.backtest(matches_df, test_period_games=50)
        
        # วิธีที่ 2: Simple Win Rate
        simple_accuracy = self.simple_win_rate_prediction(matches_df)
        
        # วิธีที่ 3: Home Advantage Only
        home_accuracy = self.home_advantage_prediction(matches_df)
        
        print(f"Random Forest: {rf_backtest['accuracy']:.3f}")
        print(f"Simple Win Rate: {simple_accuracy:.3f}")
        print(f"Home Advantage Only: {home_accuracy:.3f}")
        
        return {
            'random_forest': rf_backtest['accuracy'],
            'simple_win_rate': simple_accuracy,
            'home_advantage': home_accuracy
        }
    
    def simple_win_rate_prediction(self, matches_df, test_games=50):
        """วิธีการทำนายแบบง่าย - ใช้ win rate อย่างเดียว"""
        train_data = matches_df.iloc[:-test_games]
        test_data = matches_df.iloc[-test_games:]
        
        correct = 0
        total = 0
        
        for _, match in test_data.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            
            # คำนวณ win rate ของทีมเหย้า
            home_games = train_data[
                (train_data['home_team'] == home_team) | 
                (train_data['away_team'] == home_team)
            ]
            
            home_wins = 0
            for _, game in home_games.iterrows():
                if game['home_team'] == home_team and game['home_goals'] > game['away_goals']:
                    home_wins += 1
                elif game['away_team'] == home_team and game['away_goals'] > game['home_goals']:
                    home_wins += 1
            
            home_win_rate = home_wins / len(home_games) if len(home_games) > 0 else 0.33
            
            # คำนวณ win rate ของทีมเยือน
            away_games = train_data[
                (train_data['home_team'] == away_team) | 
                (train_data['away_team'] == away_team)
            ]
            
            away_wins = 0
            for _, game in away_games.iterrows():
                if game['home_team'] == away_team and game['home_goals'] > game['away_goals']:
                    away_wins += 1
                elif game['away_team'] == away_team and game['away_goals'] > game['home_goals']:
                    away_wins += 1
            
            away_win_rate = away_wins / len(away_games) if len(away_games) > 0 else 0.33
            
            # ทำนาย (รวม home advantage)
            if home_win_rate + 0.1 > away_win_rate:
                prediction = 'Home Win'
            elif away_win_rate > home_win_rate + 0.1:
                prediction = 'Away Win'
            else:
                prediction = 'Draw'
            
            # ตรวจสอบผลจริง
            if match['home_goals'] > match['away_goals']:
                actual = 'Home Win'
            elif match['home_goals'] < match['away_goals']:
                actual = 'Away Win'
            else:
                actual = 'Draw'
            
            if prediction == actual:
                correct += 1
            total += 1
        
        return correct / total if total > 0 else 0
    
    def home_advantage_prediction(self, matches_df, test_games=50):
        """วิธีการทำนายแบบง่าย - ทีมเหย้าชนะเสมอ"""
        test_data = matches_df.iloc[-test_games:]
        
        correct = 0
        for _, match in test_data.iterrows():
            if match['home_goals'] > match['away_goals']:
                correct += 1
        
        return correct / len(test_data)
    
    def run_comprehensive_analysis(self):
        """รันการวิเคราะห์แบบครบถ้วน"""
        print("=== การวิเคราะห์ฟุตบอลขั้นสูง ===")
        
        # สร้างข้อมูลที่สมจริง
        print("กำลังสร้างข้อมูลที่สมจริง...")
        matches_df = self.create_realistic_data(num_seasons=2)
        print(f"สร้างข้อมูล {len(matches_df)} เกม")
        
        # เทรนโมเดล
        print("\nกำลังเทรนโมเดล...")
        self.predictor.train(matches_df)
        
        # ทำ backtest
        print("\nกำลังทำ backtest...")
        backtest_results = self.predictor.backtest(matches_df, test_period_games=76)  # 2 รอบสุดท้าย
        
        # วิเคราะห์ความแม่นยำตามทีม
        print("\nกำลังวิเคราะห์ความแม่นยำตามทีม...")
        team_accuracy = self.analyze_prediction_accuracy_by_team(matches_df, backtest_results)
        if team_accuracy is not None:
            print("\nความแม่นยำการทำนายแยกตามทีม:")
            print(team_accuracy.to_string())
        
        # เปรียบเทียบวิธีการทำนาย
        print("\nกำลังเปรียบเทียบวิธีการทำนาย...")
        comparison = self.compare_prediction_methods(matches_df)
        
        # ทำนายเกมตัวอย่าง
        print("\n=== ตัวอย่างการทำนาย ===")
        sample_predictions = [
            ('Manchester City', 'Arsenal'),
            ('Liverpool', 'Chelsea'),
            ('Tottenham', 'Manchester United')
        ]
        
        for home, away in sample_predictions:
            result = self.predictor.predict_match(home, away, matches_df)
            if result:
                print(f"\n{home} vs {away}")
                print(f"การทำนาย: {result['prediction']}")
                print(f"ความมั่นใจ: {result['confidence']:.3f}")
        
        return {
            'matches_data': matches_df,
            'backtest_results': backtest_results,
            'team_accuracy': team_accuracy,
            'method_comparison': comparison
        }

if __name__ == "__main__":
    analyzer = AdvancedFootballAnalyzer()
    results = analyzer.run_comprehensive_analysis()
