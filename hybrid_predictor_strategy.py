#!/usr/bin/env python3
"""
🔄 Hybrid Football Prediction Strategy
=====================================
Focus on real data we have while preparing for corners integration
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import requests
import json
from datetime import datetime, timedelta

class HybridFootballPredictor:
    def __init__(self):
        self.api_key = "052fd4885cf943ad859c89cef542e2e5"
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": self.api_key}
        
        # Focus on categories with real data
        self.models = {
            'match_result': None,
            'handicap': None,
            'over_under': None,
            'corners': None  # Placeholder for future
        }
        
        self.elo_ratings = {}
        
    def get_real_matches(self, league_id, season="2024"):
        """Get real match data from football-data.org"""
        url = f"{self.base_url}/competitions/{league_id}/matches"
        params = {"season": season}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()["matches"]
            else:
                print(f"❌ API Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def prepare_features_without_corners(self, matches):
        """Prepare features focusing on available real data"""
        features = []
        
        for match in matches:
            if match["status"] != "FINISHED":
                continue
                
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            
            # Initialize ELO if needed
            if home_team not in self.elo_ratings:
                self.elo_ratings[home_team] = 1500
            if away_team not in self.elo_ratings:
                self.elo_ratings[away_team] = 1500
            
            # Core features from real data
            feature_row = {
                'home_elo': self.elo_ratings[home_team],
                'away_elo': self.elo_ratings[away_team],
                'elo_diff': self.elo_ratings[home_team] - self.elo_ratings[away_team],
                'home_goals': match["score"]["fullTime"]["home"],
                'away_goals': match["score"]["fullTime"]["away"],
                'total_goals': match["score"]["fullTime"]["home"] + match["score"]["fullTime"]["away"],
                'goal_diff': match["score"]["fullTime"]["home"] - match["score"]["fullTime"]["away"],
                
                # Match result
                'result': 1 if match["score"]["fullTime"]["home"] > match["score"]["fullTime"]["away"] else 
                         0 if match["score"]["fullTime"]["home"] == match["score"]["fullTime"]["away"] else 2,
                
                # Handicap (-1.5 for home team)
                'handicap_result': 1 if (match["score"]["fullTime"]["home"] - 1.5) > match["score"]["fullTime"]["away"] else 0,
                
                # Over/Under 2.5
                'over_under': 1 if (match["score"]["fullTime"]["home"] + match["score"]["fullTime"]["away"]) > 2.5 else 0,
                
                # Placeholder for corners (when available)
                'corners_over_9': None,  # Will be filled when data available
                'corners_total': None
            }
            
            features.append(feature_row)
            
            # Update ELO ratings
            self.update_elo_ratings(home_team, away_team, 
                                  match["score"]["fullTime"]["home"], 
                                  match["score"]["fullTime"]["away"])
        
        return pd.DataFrame(features)
    
    def update_elo_ratings(self, home_team, away_team, home_goals, away_goals):
        """Update ELO ratings based on match result"""
        # Expected scores
        expected_home = 1 / (1 + 10**((self.elo_ratings[away_team] - self.elo_ratings[home_team]) / 400))
        expected_away = 1 - expected_home
        
        # Actual scores
        if home_goals > away_goals:
            actual_home, actual_away = 1, 0
        elif home_goals < away_goals:
            actual_home, actual_away = 0, 1
        else:
            actual_home, actual_away = 0.5, 0.5
        
        # K-factor (higher for bigger wins)
        goal_diff = abs(home_goals - away_goals)
        k_factor = 32 + goal_diff * 4
        
        # Update ratings
        self.elo_ratings[home_team] += k_factor * (actual_home - expected_home)
        self.elo_ratings[away_team] += k_factor * (actual_away - expected_away)
    
    def train_hybrid_models(self, data):
        """Train models on available real data"""
        print("🤖 Training Hybrid Models...")
        
        # Prepare features (excluding corners for now)
        feature_cols = ['home_elo', 'away_elo', 'elo_diff']
        X = data[feature_cols].fillna(0)
        
        # Train match result model
        y_result = data['result'].dropna()
        X_result = X.loc[y_result.index]
        if len(X_result) > 0:
            self.models['match_result'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['match_result'].fit(X_result, y_result)
            print("✅ Match Result model trained")
        
        # Train handicap model
        y_handicap = data['handicap_result'].dropna()
        X_handicap = X.loc[y_handicap.index]
        if len(X_handicap) > 0:
            self.models['handicap'] = GradientBoostingClassifier(n_estimators=100, random_state=42)
            self.models['handicap'].fit(X_handicap, y_handicap)
            print("✅ Handicap model trained")
        
        # Train over/under model
        y_ou = data['over_under'].dropna()
        X_ou = X.loc[y_ou.index]
        if len(X_ou) > 0:
            self.models['over_under'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['over_under'].fit(X_ou, y_ou)
            print("✅ Over/Under model trained")
        
        print("🎯 Corners model: Waiting for data source...")
    
    def predict_match_hybrid(self, home_team, away_team):
        """Make predictions using hybrid approach"""
        # Get current ELO ratings
        home_elo = self.elo_ratings.get(home_team, 1500)
        away_elo = self.elo_ratings.get(away_team, 1500)
        elo_diff = home_elo - away_elo
        
        features = np.array([[home_elo, away_elo, elo_diff]])
        
        predictions = {}
        
        # Match Result
        if self.models['match_result']:
            result_proba = self.models['match_result'].predict_proba(features)[0]
            predictions['match_result'] = {
                'prediction': ['Home Win', 'Draw', 'Away Win'][np.argmax(result_proba)],
                'confidence': max(result_proba),
                'probabilities': {
                    'Home Win': result_proba[0] if len(result_proba) > 0 else 0,
                    'Draw': result_proba[1] if len(result_proba) > 1 else 0,
                    'Away Win': result_proba[2] if len(result_proba) > 2 else 0
                }
            }
        
        # Handicap
        if self.models['handicap']:
            handicap_proba = self.models['handicap'].predict_proba(features)[0]
            predictions['handicap'] = {
                'prediction': 'Home -1.5' if handicap_proba[1] > 0.5 else 'Away +1.5',
                'confidence': max(handicap_proba)
            }
        
        # Over/Under
        if self.models['over_under']:
            ou_proba = self.models['over_under'].predict_proba(features)[0]
            predictions['over_under'] = {
                'prediction': 'Over 2.5' if ou_proba[1] > 0.5 else 'Under 2.5',
                'confidence': max(ou_proba)
            }
        
        # Corners (placeholder)
        predictions['corners'] = {
            'prediction': 'Data not available',
            'confidence': 0.0,
            'note': 'Waiting for corners data source'
        }
        
        return predictions
    
    def backtest_hybrid(self, data, test_size=20):
        """Backtest hybrid predictions"""
        print(f"🔍 Hybrid Backtest (Last {test_size} matches)")
        print("=" * 50)
        
        # Use last matches for testing
        test_data = data.tail(test_size).copy()
        train_data = data.head(len(data) - test_size).copy()
        
        # Retrain on training data
        self.train_hybrid_models(train_data)
        
        results = {
            'match_result': {'correct': 0, 'total': 0},
            'handicap': {'correct': 0, 'total': 0},
            'over_under': {'correct': 0, 'total': 0}
        }
        
        for idx, row in test_data.iterrows():
            # Make prediction (simplified for backtest)
            home_elo = row['home_elo']
            away_elo = row['away_elo']
            
            # Match result prediction
            if home_elo > away_elo + 100:
                pred_result = 1  # Home win
            elif away_elo > home_elo + 100:
                pred_result = 2  # Away win
            else:
                pred_result = 0  # Draw
            
            if pred_result == row['result']:
                results['match_result']['correct'] += 1
            results['match_result']['total'] += 1
            
            # Handicap prediction
            pred_handicap = 1 if home_elo > away_elo + 50 else 0
            if pred_handicap == row['handicap_result']:
                results['handicap']['correct'] += 1
            results['handicap']['total'] += 1
            
            # Over/Under prediction
            pred_ou = 1 if abs(home_elo - away_elo) < 200 else 0  # Close games = more goals
            if pred_ou == row['over_under']:
                results['over_under']['correct'] += 1
            results['over_under']['total'] += 1
        
        # Print results
        for category, result in results.items():
            if result['total'] > 0:
                accuracy = result['correct'] / result['total'] * 100
                print(f"📊 {category.replace('_', ' ').title()}: {accuracy:.1f}% ({result['correct']}/{result['total']})")
        
        return results

def main():
    print("🔄 Hybrid Football Predictor")
    print("=" * 50)
    
    predictor = HybridFootballPredictor()
    
    # Get Premier League data
    print("📥 Loading Premier League data...")
    matches = predictor.get_real_matches("PL")  # Premier League
    
    if matches:
        print(f"✅ Loaded {len(matches)} matches")
        
        # Prepare features
        data = predictor.prepare_features_without_corners(matches)
        print(f"📊 Prepared {len(data)} match features")
        
        # Train models
        predictor.train_hybrid_models(data)
        
        # Backtest
        predictor.backtest_hybrid(data)
        
        # Example prediction
        print("\n🎯 Example Prediction:")
        print("-" * 30)
        prediction = predictor.predict_match_hybrid("Arsenal", "Chelsea")
        
        for category, pred in prediction.items():
            print(f"📈 {category.replace('_', ' ').title()}: {pred['prediction']} ({pred['confidence']:.1%})")
    
    else:
        print("❌ No data loaded")

if __name__ == "__main__":
    main()
