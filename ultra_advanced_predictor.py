#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ultra Advanced Football Predictor
- Ensemble of 5+ ML models
- Advanced feature engineering
- Time series analysis
- Market odds integration
- Player form tracking
- Tactical analysis
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.impute import KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif
import warnings
warnings.filterwarnings('ignore')

class UltraAdvancedPredictor:
    def __init__(self, api_key=None):
        self.api_key = api_key
        
        # Multiple ML Models with optimized parameters
        self.models = {
            'rf': RandomForestClassifier(
                n_estimators=300, max_depth=15, min_samples_split=5,
                min_samples_leaf=2, random_state=42, n_jobs=-1
            ),
            'gb': GradientBoostingClassifier(
                n_estimators=200, learning_rate=0.1, max_depth=8,
                min_samples_split=10, random_state=42
            ),
            'et': ExtraTreesClassifier(
                n_estimators=250, max_depth=12, min_samples_split=8,
                random_state=42, n_jobs=-1
            ),
            'lr': LogisticRegression(
                C=1.0, max_iter=1000, random_state=42
            ),
            'svm': SVC(
                C=1.0, kernel='rbf', probability=True, random_state=42
            )
        }
        
        # Advanced preprocessing
        self.scaler = RobustScaler()
        self.imputer = KNNImputer(n_neighbors=5)
        self.feature_selector = SelectKBest(f_classif, k=35)
        
        # Data storage
        self.historical_data = None
        self.team_ratings = {}
        self.player_form = {}
        self.head_to_head = {}
        
        self.is_trained = False
        self.feature_columns = []
        
    def calculate_elo_ratings(self, matches_df):
        """คำนวณ ELO Rating สำหรับแต่ละทีม"""
        print("🏆 กำลังคำนวณ ELO Ratings...")
        
        # เริ่มต้น ELO ที่ 1500 สำหรับทุกทีม
        teams = set(matches_df['home_team'].unique()) | set(matches_df['away_team'].unique())
        elo_ratings = {team: 1500 for team in teams}
        
        K = 32  # K-factor
        
        for _, match in matches_df.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            home_goals = match['home_goals']
            away_goals = match['away_goals']
            
            # คำนวณผลลัพธ์
            if home_goals > away_goals:
                home_result = 1.0
                away_result = 0.0
            elif home_goals == away_goals:
                home_result = 0.5
                away_result = 0.5
            else:
                home_result = 0.0
                away_result = 1.0
            
            # คำนวณ Expected Score
            home_expected = 1 / (1 + 10**((elo_ratings[away_team] - elo_ratings[home_team]) / 400))
            away_expected = 1 - home_expected
            
            # อัปเดต ELO
            elo_ratings[home_team] += K * (home_result - home_expected)
            elo_ratings[away_team] += K * (away_result - away_expected)
        
        self.team_ratings = elo_ratings
        return elo_ratings
    
    def calculate_recent_form(self, matches_df, team_name, current_idx, games=5):
        """คำนวณฟอร์มล่าสุดของทีม"""
        team_matches = matches_df[
            ((matches_df['home_team'] == team_name) | 
             (matches_df['away_team'] == team_name)) &
            (matches_df.index < current_idx)
        ].tail(games)
        
        if len(team_matches) == 0:
            return {'form_points': 1.5, 'form_goals': 1.5, 'form_conceded': 1.5}
        
        points = 0
        goals_for = 0
        goals_against = 0
        
        for _, match in team_matches.iterrows():
            if match['home_team'] == team_name:
                gf, ga = match['home_goals'], match['away_goals']
            else:
                gf, ga = match['away_goals'], match['home_goals']
            
            goals_for += gf
            goals_against += ga
            
            if gf > ga:
                points += 3
            elif gf == ga:
                points += 1
        
        return {
            'form_points': points / len(team_matches),
            'form_goals': goals_for / len(team_matches),
            'form_conceded': goals_against / len(team_matches)
        }
    
    def calculate_head_to_head(self, matches_df, home_team, away_team, current_idx):
        """คำนวณสถิติการเจอกันในอดีต"""
        h2h_matches = matches_df[
            (((matches_df['home_team'] == home_team) & (matches_df['away_team'] == away_team)) |
             ((matches_df['home_team'] == away_team) & (matches_df['away_team'] == home_team))) &
            (matches_df.index < current_idx)
        ].tail(10)  # 10 เกมล่าสุด
        
        if len(h2h_matches) == 0:
            return {'h2h_home_wins': 0.33, 'h2h_draws': 0.33, 'h2h_away_wins': 0.33}
        
        home_wins = draws = away_wins = 0
        
        for _, match in h2h_matches.iterrows():
            if match['home_team'] == home_team:
                if match['home_goals'] > match['away_goals']:
                    home_wins += 1
                elif match['home_goals'] == match['away_goals']:
                    draws += 1
                else:
                    away_wins += 1
            else:  # away_team is home in this match
                if match['home_goals'] > match['away_goals']:
                    away_wins += 1
                elif match['home_goals'] == match['away_goals']:
                    draws += 1
                else:
                    home_wins += 1
        
        total = len(h2h_matches)
        return {
            'h2h_home_wins': home_wins / total,
            'h2h_draws': draws / total,
            'h2h_away_wins': away_wins / total
        }
    
    def calculate_momentum(self, matches_df, team_name, current_idx):
        """คำนวณ momentum ของทีม"""
        recent_matches = matches_df[
            ((matches_df['home_team'] == team_name) | 
             (matches_df['away_team'] == team_name)) &
            (matches_df.index < current_idx)
        ].tail(10)
        
        if len(recent_matches) == 0:
            return {'momentum': 0.5, 'scoring_trend': 0.0, 'defensive_trend': 0.0}
        
        # คำนวณ momentum จากผลลัพธ์
        results = []
        goals_for = []
        goals_against = []
        
        for _, match in recent_matches.iterrows():
            if match['home_team'] == team_name:
                gf, ga = match['home_goals'], match['away_goals']
            else:
                gf, ga = match['away_goals'], match['home_goals']
            
            goals_for.append(gf)
            goals_against.append(ga)
            
            if gf > ga:
                results.append(1.0)
            elif gf == ga:
                results.append(0.5)
            else:
                results.append(0.0)
        
        # ให้น้ำหนักมากขึ้นกับเกมล่าสุด
        weights = np.linspace(0.5, 1.0, len(results))
        momentum = np.average(results, weights=weights)
        
        # คำนวณ trend
        if len(goals_for) >= 5:
            scoring_trend = np.polyfit(range(len(goals_for)), goals_for, 1)[0]
            defensive_trend = -np.polyfit(range(len(goals_against)), goals_against, 1)[0]
        else:
            scoring_trend = 0.0
            defensive_trend = 0.0
        
        return {
            'momentum': momentum,
            'scoring_trend': scoring_trend,
            'defensive_trend': defensive_trend
        }
    
    def create_ultra_features(self, matches_df):
        """สร้าง Ultra Advanced Features"""
        print("🔧 กำลังสร้าง Ultra Advanced Features...")
        
        # คำนวณ ELO ratings
        elo_ratings = self.calculate_elo_ratings(matches_df)
        
        features_list = []
        
        for idx, match in matches_df.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            match_date = pd.to_datetime(match['date'])
            
            # Basic team stats
            home_form = self.calculate_recent_form(matches_df, home_team, idx)
            away_form = self.calculate_recent_form(matches_df, away_team, idx)
            
            # Head-to-head
            h2h = self.calculate_head_to_head(matches_df, home_team, away_team, idx)
            
            # Momentum
            home_momentum = self.calculate_momentum(matches_df, home_team, idx)
            away_momentum = self.calculate_momentum(matches_df, away_team, idx)
            
            # ELO ratings
            home_elo = elo_ratings.get(home_team, 1500)
            away_elo = elo_ratings.get(away_team, 1500)
            
            # Time-based features
            days_since_epoch = (match_date - datetime(2020, 1, 1)).days
            season_progress = (match_date.month - 8) % 12 / 12  # August = start of season
            
            # Advanced features
            features = {
                # ELO features
                'home_elo': home_elo,
                'away_elo': away_elo,
                'elo_difference': home_elo - away_elo,
                'elo_ratio': home_elo / away_elo if away_elo > 0 else 1.0,
                
                # Form features
                'home_form_points': home_form['form_points'],
                'home_form_goals': home_form['form_goals'],
                'home_form_conceded': home_form['form_conceded'],
                'away_form_points': away_form['form_points'],
                'away_form_goals': away_form['form_goals'],
                'away_form_conceded': away_form['form_conceded'],
                
                # Form differences
                'form_points_diff': home_form['form_points'] - away_form['form_points'],
                'form_attack_diff': home_form['form_goals'] - away_form['form_goals'],
                'form_defense_diff': away_form['form_conceded'] - home_form['form_conceded'],
                
                # Head-to-head
                'h2h_home_advantage': h2h['h2h_home_wins'],
                'h2h_draw_tendency': h2h['h2h_draws'],
                'h2h_away_advantage': h2h['h2h_away_wins'],
                
                # Momentum
                'home_momentum': home_momentum['momentum'],
                'away_momentum': away_momentum['momentum'],
                'momentum_difference': home_momentum['momentum'] - away_momentum['momentum'],
                'home_scoring_trend': home_momentum['scoring_trend'],
                'away_scoring_trend': away_momentum['scoring_trend'],
                'home_defensive_trend': home_momentum['defensive_trend'],
                'away_defensive_trend': away_momentum['defensive_trend'],
                
                # Time features
                'days_since_epoch': days_since_epoch,
                'season_progress': season_progress,
                'is_early_season': 1 if season_progress < 0.3 else 0,
                'is_mid_season': 1 if 0.3 <= season_progress < 0.7 else 0,
                'is_late_season': 1 if season_progress >= 0.7 else 0,
                
                # Match context
                'month': match_date.month,
                'day_of_week': match_date.weekday(),
                'is_weekend': 1 if match_date.weekday() >= 5 else 0,
                'is_midweek': 1 if match_date.weekday() in [1, 2, 3] else 0,
                
                # Combined features
                'overall_strength_home': (home_elo / 1500) * home_momentum['momentum'],
                'overall_strength_away': (away_elo / 1500) * away_momentum['momentum'],
                'strength_ratio': ((home_elo / 1500) * home_momentum['momentum']) / 
                                ((away_elo / 1500) * away_momentum['momentum']) if away_momentum['momentum'] > 0 else 1.0,
                
                # Home advantage adjusted by form
                'adjusted_home_advantage': 0.1 * (home_form['form_points'] / 3.0),
                
                # Defensive vs Offensive matchup
                'attack_vs_defense': home_form['form_goals'] - away_form['form_conceded'],
                'defense_vs_attack': home_form['form_conceded'] - away_form['form_goals'],
            }
            
            features_list.append(features)
        
        features_df = pd.DataFrame(features_list)
        self.feature_columns = features_df.columns.tolist()
        
        print(f"✅ สร้าง {len(self.feature_columns)} Ultra Features สำเร็จ")
        return features_df
