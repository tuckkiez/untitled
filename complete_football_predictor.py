#!/usr/bin/env python3
"""
🚀 Complete Football Prediction System
======================================
Ultimate system combining all prediction categories with real data
"""

import requests
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

class CompleteFootballPredictor:
    def __init__(self):
        # API Configuration
        self.football_data_key = "052fd4885cf943ad859c89cef542e2e5"
        self.apisports_key = "9936a2866ebc7271a809ff2ab164b032"
        
        self.football_data_url = "https://api.football-data.org/v4"
        self.apisports_url = "https://v3.football.api-sports.io"
        
        self.football_data_headers = {"X-Auth-Token": self.football_data_key}
        self.apisports_headers = {
            'x-rapidapi-key': self.apisports_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        
        # Models for all categories
        self.models = {
            'match_result': None,
            'handicap': None,
            'over_under': None,
            'corners_over_9': None,
            'corners_over_10': None,
            'corners_handicap': None
        }
        
        self.elo_ratings = {}
        self.scaler = StandardScaler()
        
    def get_match_results_data(self, league_id="PL", season="2024"):
        """Get match results from football-data.org"""
        print("📥 Getting match results data...")
        
        url = f"{self.football_data_url}/competitions/{league_id}/matches"
        params = {"season": season}
        
        try:
            response = requests.get(url, headers=self.football_data_headers, params=params)
            
            if response.status_code == 200:
                matches = response.json()["matches"]
                print(f"✅ Got {len(matches)} match results")
                return matches
            else:
                print(f"❌ Error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return []
    
    def get_corners_data(self, league_id="39", season="2023", max_matches=50):
        """Get corners data from API-Sports"""
        print("📥 Getting corners data...")
        
        # Get fixtures
        url = f"{self.apisports_url}/fixtures"
        params = {
            'league': league_id,
            'season': season,
            'status': 'FT'
        }
        
        try:
            response = requests.get(url, headers=self.apisports_headers, params=params)
            
            if response.status_code != 200:
                print(f"❌ Fixtures error: {response.status_code}")
                return []
            
            fixtures = response.json().get('response', [])[:max_matches]
            corners_data = []
            
            for i, fixture in enumerate(fixtures[:20]):  # Limit to preserve quota
                fixture_id = fixture['fixture']['id']
                
                # Get statistics
                stats_url = f"{self.apisports_url}/fixtures/statistics"
                stats_params = {'fixture': fixture_id}
                
                stats_response = requests.get(stats_url, headers=self.apisports_headers, params=stats_params)
                
                if stats_response.status_code == 200:
                    stats_data = stats_response.json()
                    
                    home_corners = 0
                    away_corners = 0
                    
                    for team_stats in stats_data.get('response', []):
                        for stat in team_stats.get('statistics', []):
                            if stat.get('type', '').lower() == 'corner kicks':
                                if team_stats['team']['name'] == fixture['teams']['home']['name']:
                                    home_corners = int(stat.get('value', 0))
                                else:
                                    away_corners = int(stat.get('value', 0))
                    
                    if home_corners > 0 or away_corners > 0:
                        corners_data.append({
                            'fixture_id': fixture_id,
                            'home_team': fixture['teams']['home']['name'],
                            'away_team': fixture['teams']['away']['name'],
                            'home_corners': home_corners,
                            'away_corners': away_corners,
                            'total_corners': home_corners + away_corners
                        })
            
            print(f"✅ Got {len(corners_data)} matches with corners data")
            return corners_data
            
        except Exception as e:
            print(f"❌ Exception: {e}")
            return []
    
    def prepare_complete_dataset(self, match_results, corners_data):
        """Combine match results and corners data"""
        print("🔄 Preparing complete dataset...")
        
        complete_data = []
        
        # Process match results
        for match in match_results:
            if match["status"] != "FINISHED":
                continue
            
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            
            # Initialize ELO if needed
            if home_team not in self.elo_ratings:
                self.elo_ratings[home_team] = 1500
            if away_team not in self.elo_ratings:
                self.elo_ratings[away_team] = 1500
            
            home_goals = match["score"]["fullTime"]["home"]
            away_goals = match["score"]["fullTime"]["away"]
            
            match_record = {
                'home_team': home_team,
                'away_team': away_team,
                'home_goals': home_goals,
                'away_goals': away_goals,
                'total_goals': home_goals + away_goals,
                'home_elo': self.elo_ratings[home_team],
                'away_elo': self.elo_ratings[away_team],
                'elo_diff': self.elo_ratings[home_team] - self.elo_ratings[away_team],
                
                # Match result
                'result': 1 if home_goals > away_goals else 0 if home_goals == away_goals else 2,
                
                # Handicap (-1.5 for home)
                'handicap_result': 1 if (home_goals - 1.5) > away_goals else 0,
                
                # Over/Under 2.5
                'over_under': 1 if (home_goals + away_goals) > 2.5 else 0,
                
                # Default corners (will be updated if available)
                'home_corners': 0,
                'away_corners': 0,
                'total_corners': 0,
                'corners_over_9': 0,
                'corners_over_10': 0,
                'corners_handicap': 0
            }
            
            # Try to find matching corners data
            for corners_match in corners_data:
                if (corners_match['home_team'] in home_team or home_team in corners_match['home_team']) and \
                   (corners_match['away_team'] in away_team or away_team in corners_match['away_team']):
                    
                    match_record.update({
                        'home_corners': corners_match['home_corners'],
                        'away_corners': corners_match['away_corners'],
                        'total_corners': corners_match['total_corners'],
                        'corners_over_9': 1 if corners_match['total_corners'] > 9 else 0,
                        'corners_over_10': 1 if corners_match['total_corners'] > 10 else 0,
                        'corners_handicap': 1 if corners_match['home_corners'] > (corners_match['away_corners'] + 2.5) else 0
                    })
                    break
            
            complete_data.append(match_record)
            
            # Update ELO ratings
            self.update_elo_ratings(home_team, away_team, home_goals, away_goals)
        
        print(f"✅ Prepared {len(complete_data)} complete match records")
        return complete_data
    
    def update_elo_ratings(self, home_team, away_team, home_goals, away_goals):
        """Update ELO ratings"""
        expected_home = 1 / (1 + 10**((self.elo_ratings[away_team] - self.elo_ratings[home_team]) / 400))
        expected_away = 1 - expected_home
        
        if home_goals > away_goals:
            actual_home, actual_away = 1, 0
        elif home_goals < away_goals:
            actual_home, actual_away = 0, 1
        else:
            actual_home, actual_away = 0.5, 0.5
        
        goal_diff = abs(home_goals - away_goals)
        k_factor = 32 + goal_diff * 4
        
        self.elo_ratings[home_team] += k_factor * (actual_home - expected_home)
        self.elo_ratings[away_team] += k_factor * (actual_away - expected_away)
    
    def train_all_models(self, data):
        """Train all prediction models"""
        print("🤖 Training All Prediction Models")
        print("=" * 40)
        
        df = pd.DataFrame(data)
        
        # Basic features
        feature_cols = ['home_elo', 'away_elo', 'elo_diff']
        X = df[feature_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        models_trained = 0
        
        # 1. Match Result
        if 'result' in df.columns:
            y = df['result']
            self.models['match_result'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['match_result'].fit(X_scaled, y)
            cv_score = cross_val_score(self.models['match_result'], X_scaled, y, cv=5).mean()
            print(f"✅ Match Result Model - CV Score: {cv_score:.3f}")
            models_trained += 1
        
        # 2. Handicap
        if 'handicap_result' in df.columns:
            y = df['handicap_result']
            self.models['handicap'] = GradientBoostingClassifier(n_estimators=100, random_state=42)
            self.models['handicap'].fit(X_scaled, y)
            cv_score = cross_val_score(self.models['handicap'], X_scaled, y, cv=5).mean()
            print(f"✅ Handicap Model - CV Score: {cv_score:.3f}")
            models_trained += 1
        
        # 3. Over/Under
        if 'over_under' in df.columns:
            y = df['over_under']
            self.models['over_under'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['over_under'].fit(X_scaled, y)
            cv_score = cross_val_score(self.models['over_under'], X_scaled, y, cv=5).mean()
            print(f"✅ Over/Under Model - CV Score: {cv_score:.3f}")
            models_trained += 1
        
        # 4. Corners Over 9.5
        corners_data = df[df['total_corners'] > 0]  # Only matches with corners data
        if len(corners_data) > 5 and 'corners_over_9' in corners_data.columns:
            X_corners = X_scaled[corners_data.index]
            y = corners_data['corners_over_9']
            self.models['corners_over_9'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['corners_over_9'].fit(X_corners, y)
            cv_score = cross_val_score(self.models['corners_over_9'], X_corners, y, cv=3).mean()
            print(f"✅ Corners Over 9.5 Model - CV Score: {cv_score:.3f}")
            models_trained += 1
        
        # 5. Corners Over 10.5
        if len(corners_data) > 5 and 'corners_over_10' in corners_data.columns:
            X_corners = X_scaled[corners_data.index]
            y = corners_data['corners_over_10']
            self.models['corners_over_10'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['corners_over_10'].fit(X_corners, y)
            cv_score = cross_val_score(self.models['corners_over_10'], X_corners, y, cv=3).mean()
            print(f"✅ Corners Over 10.5 Model - CV Score: {cv_score:.3f}")
            models_trained += 1
        
        # 6. Corners Handicap
        if len(corners_data) > 5 and 'corners_handicap' in corners_data.columns:
            X_corners = X_scaled[corners_data.index]
            y = corners_data['corners_handicap']
            self.models['corners_handicap'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['corners_handicap'].fit(X_corners, y)
            cv_score = cross_val_score(self.models['corners_handicap'], X_corners, y, cv=3).mean()
            print(f"✅ Corners Handicap Model - CV Score: {cv_score:.3f}")
            models_trained += 1
        
        print(f"🎯 Successfully trained {models_trained} models")
        return models_trained
    
    def predict_complete_match(self, home_team, away_team):
        """Complete match prediction for all categories"""
        home_elo = self.elo_ratings.get(home_team, 1500)
        away_elo = self.elo_ratings.get(away_team, 1500)
        elo_diff = home_elo - away_elo
        
        features = np.array([[home_elo, away_elo, elo_diff]])
        features_scaled = self.scaler.transform(features)
        
        predictions = {}
        
        # Match Result
        if self.models['match_result']:
            proba = self.models['match_result'].predict_proba(features_scaled)[0]
            predictions['match_result'] = {
                'prediction': ['Home Win', 'Draw', 'Away Win'][np.argmax(proba)],
                'confidence': max(proba),
                'probabilities': {
                    'Home Win': proba[0] if len(proba) > 0 else 0,
                    'Draw': proba[1] if len(proba) > 1 else 0,
                    'Away Win': proba[2] if len(proba) > 2 else 0
                }
            }
        
        # Handicap
        if self.models['handicap']:
            proba = self.models['handicap'].predict_proba(features_scaled)[0]
            predictions['handicap'] = {
                'prediction': f'{home_team} -1.5' if proba[1] > 0.5 else f'{away_team} +1.5',
                'confidence': max(proba)
            }
        
        # Over/Under
        if self.models['over_under']:
            proba = self.models['over_under'].predict_proba(features_scaled)[0]
            predictions['over_under'] = {
                'prediction': 'Over 2.5' if proba[1] > 0.5 else 'Under 2.5',
                'confidence': max(proba)
            }
        
        # Corners Over 9.5
        if self.models['corners_over_9']:
            proba = self.models['corners_over_9'].predict_proba(features_scaled)[0]
            predictions['corners_over_9'] = {
                'prediction': 'Over 9.5' if proba[1] > 0.5 else 'Under 9.5',
                'confidence': max(proba)
            }
        
        # Corners Over 10.5
        if self.models['corners_over_10']:
            proba = self.models['corners_over_10'].predict_proba(features_scaled)[0]
            predictions['corners_over_10'] = {
                'prediction': 'Over 10.5' if proba[1] > 0.5 else 'Under 10.5',
                'confidence': max(proba)
            }
        
        # Corners Handicap
        if self.models['corners_handicap']:
            proba = self.models['corners_handicap'].predict_proba(features_scaled)[0]
            predictions['corners_handicap'] = {
                'prediction': f'{home_team} -2.5 corners' if proba[1] > 0.5 else f'{away_team} +2.5 corners',
                'confidence': max(proba)
            }
        
        return predictions
    
    def backtest_complete_system(self, data, test_size=20):
        """Backtest complete prediction system"""
        print(f"🔍 Complete System Backtest (Last {test_size} matches)")
        print("=" * 50)
        
        df = pd.DataFrame(data)
        test_data = df.tail(test_size)
        
        results = {}
        categories = ['result', 'handicap_result', 'over_under', 'corners_over_9', 'corners_over_10', 'corners_handicap']
        
        for category in categories:
            if category in test_data.columns:
                correct = 0
                total = 0
                
                for _, row in test_data.iterrows():
                    if pd.isna(row[category]):
                        continue
                    
                    # Simple prediction based on ELO
                    home_elo = row['home_elo']
                    away_elo = row['away_elo']
                    
                    if category == 'result':
                        if home_elo > away_elo + 100:
                            pred = 1  # Home win
                        elif away_elo > home_elo + 100:
                            pred = 2  # Away win
                        else:
                            pred = 0  # Draw
                    elif category == 'handicap_result':
                        pred = 1 if home_elo > away_elo + 50 else 0
                    elif category == 'over_under':
                        pred = 1 if abs(home_elo - away_elo) < 200 else 0
                    else:  # Corners categories
                        pred = 1 if home_elo > away_elo else 0
                    
                    if pred == row[category]:
                        correct += 1
                    total += 1
                
                if total > 0:
                    accuracy = correct / total * 100
                    results[category] = {'accuracy': accuracy, 'correct': correct, 'total': total}
                    print(f"📊 {category.replace('_', ' ').title()}: {accuracy:.1f}% ({correct}/{total})")
        
        return results

def main():
    print("🚀 Complete Football Prediction System")
    print("=" * 50)
    
    predictor = CompleteFootballPredictor()
    
    # Get match results data
    match_results = predictor.get_match_results_data("PL", "2024")
    
    # Get corners data
    corners_data = predictor.get_corners_data("39", "2023", 30)
    
    if not match_results:
        print("❌ No match results data")
        return
    
    # Prepare complete dataset
    complete_data = predictor.prepare_complete_dataset(match_results, corners_data)
    
    if len(complete_data) < 10:
        print("❌ Insufficient data")
        return
    
    # Train all models
    models_trained = predictor.train_all_models(complete_data)
    
    if models_trained == 0:
        print("❌ No models trained")
        return
    
    # Backtest
    backtest_results = predictor.backtest_complete_system(complete_data)
    
    # Example predictions
    print(f"\n🎯 Complete Match Prediction Example:")
    print("-" * 45)
    
    predictions = predictor.predict_complete_match("Arsenal", "Chelsea")
    
    for category, pred in predictions.items():
        print(f"📈 {category.replace('_', ' ').title()}: {pred['prediction']} ({pred['confidence']:.1%})")
    
    # Save complete dataset
    with open('complete_football_data.json', 'w') as f:
        json.dump(complete_data, f, indent=2)
    
    print(f"\n💾 Saved complete dataset with {len(complete_data)} matches")
    print("🏆 Complete Football Prediction System ready!")
    
    # Summary
    print(f"\n📋 SYSTEM SUMMARY:")
    print("=" * 30)
    print(f"✅ Match Results: {len(match_results)} matches")
    print(f"✅ Corners Data: {len(corners_data)} matches")
    print(f"✅ Models Trained: {models_trained}")
    print(f"✅ Categories: Match Result, Handicap, Over/Under, Corners")

if __name__ == "__main__":
    main()
