#!/usr/bin/env python3
"""
🏆 Ultimate Corners Predictor
=============================
Complete corners prediction system with real API data
"""

import requests
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class UltimateCornersPredictor:
    def __init__(self):
        self.api_key = "9936a2866ebc7271a809ff2ab164b032"
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        
        self.models = {
            'corners_over_9': None,
            'corners_over_10': None,
            'corners_handicap': None,  # Home -2.5 corners
            'total_corners_range': None
        }
        
        self.team_stats = {}
        self.scaler = StandardScaler()
        
    def collect_historical_data(self, league_id="39", season="2023", max_matches=100):
        """Collect historical corners data"""
        print(f"📥 Collecting Historical Data (League: {league_id}, Season: {season})")
        print("=" * 60)
        
        # Get fixtures
        fixtures_url = f"{self.base_url}/fixtures"
        params = {
            'league': league_id,
            'season': season,
            'status': 'FT'
        }
        
        try:
            response = requests.get(fixtures_url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"❌ Fixtures API Error: {response.status_code}")
                return []
            
            fixtures_data = response.json()
            fixtures = fixtures_data.get('response', [])[:max_matches]
            
            print(f"✅ Found {len(fixtures)} finished matches")
            
            corners_dataset = []
            successful_requests = 0
            
            for i, fixture in enumerate(fixtures):
                if successful_requests >= 50:  # Limit to preserve quota
                    print(f"⚠️ Stopping at {successful_requests} matches to preserve API quota")
                    break
                
                fixture_id = fixture['fixture']['id']
                home_team = fixture['teams']['home']['name']
                away_team = fixture['teams']['away']['name']
                match_date = fixture['fixture']['date']
                
                print(f"🏈 Match {i+1}: {home_team} vs {away_team}", end=" ")
                
                # Get match statistics
                stats_data = self.get_match_statistics(fixture_id)
                
                if stats_data:
                    match_record = self.process_match_data(fixture, stats_data)
                    if match_record:
                        corners_dataset.append(match_record)
                        successful_requests += 1
                        print(f"✅ (Corners: {match_record['total_corners']})")
                    else:
                        print("❌ No corners data")
                else:
                    print("❌ No stats")
            
            print(f"\n📊 Successfully collected {len(corners_dataset)} matches with corners data")
            return corners_dataset
            
        except Exception as e:
            print(f"❌ Error collecting data: {e}")
            return []
    
    def get_match_statistics(self, fixture_id):
        """Get detailed match statistics"""
        url = f"{self.base_url}/fixtures/statistics"
        params = {'fixture': fixture_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            return None
    
    def process_match_data(self, fixture, stats_data):
        """Process match data into features"""
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        
        # Initialize match record
        match_record = {
            'fixture_id': fixture['fixture']['id'],
            'date': fixture['fixture']['date'],
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': fixture['goals']['home'] or 0,
            'away_goals': fixture['goals']['away'] or 0
        }
        
        # Process team statistics
        team_stats = {}
        
        for team_data in stats_data.get('response', []):
            team_name = team_data.get('team', {}).get('name', '')
            stats = {}
            
            for stat in team_data.get('statistics', []):
                stat_type = stat.get('type', '').lower()
                stat_value = stat.get('value', 0)
                
                # Convert percentage strings to numbers
                if isinstance(stat_value, str) and '%' in stat_value:
                    stat_value = float(stat_value.replace('%', ''))
                elif stat_value == 'None' or stat_value is None:
                    stat_value = 0
                else:
                    try:
                        stat_value = float(stat_value)
                    except:
                        stat_value = 0
                
                stats[stat_type] = stat_value
            
            team_stats[team_name] = stats
        
        # Extract corners data
        home_corners = team_stats.get(home_team, {}).get('corner kicks', 0)
        away_corners = team_stats.get(away_team, {}).get('corner kicks', 0)
        
        if home_corners == 0 and away_corners == 0:
            return None  # No corners data available
        
        # Add corners features
        match_record.update({
            'home_corners': int(home_corners),
            'away_corners': int(away_corners),
            'total_corners': int(home_corners + away_corners),
            'corners_over_9': 1 if (home_corners + away_corners) > 9 else 0,
            'corners_over_10': 1 if (home_corners + away_corners) > 10 else 0,
            'corners_handicap': 1 if home_corners > (away_corners + 2.5) else 0,
            'home_corners_advantage': 1 if home_corners > away_corners else 0
        })
        
        # Add other match features
        home_stats = team_stats.get(home_team, {})
        away_stats = team_stats.get(away_team, {})
        
        match_record.update({
            'home_shots': home_stats.get('total shots', 0),
            'away_shots': away_stats.get('total shots', 0),
            'home_shots_on_target': home_stats.get('shots on goal', 0),
            'away_shots_on_target': away_stats.get('shots on goal', 0),
            'home_possession': home_stats.get('ball possession', 50),
            'away_possession': away_stats.get('ball possession', 50),
            'home_fouls': home_stats.get('fouls', 0),
            'away_fouls': away_stats.get('fouls', 0),
            'home_offsides': home_stats.get('offsides', 0),
            'away_offsides': away_stats.get('offsides', 0)
        })
        
        return match_record
    
    def prepare_features(self, data):
        """Prepare features for machine learning"""
        df = pd.DataFrame(data)
        
        # Create advanced features
        df['total_shots'] = df['home_shots'] + df['away_shots']
        df['shots_difference'] = df['home_shots'] - df['away_shots']
        df['possession_difference'] = df['home_possession'] - df['away_possession']
        df['total_fouls'] = df['home_fouls'] + df['away_fouls']
        df['attacking_intensity'] = (df['home_shots'] + df['away_shots'] + df['home_corners'] + df['away_corners']) / 4
        df['home_attacking_ratio'] = df['home_shots'] / (df['home_shots'] + df['away_shots'] + 1)
        df['away_attacking_ratio'] = df['away_shots'] / (df['home_shots'] + df['away_shots'] + 1)
        
        # Feature columns for prediction
        feature_cols = [
            'home_shots', 'away_shots', 'total_shots', 'shots_difference',
            'home_shots_on_target', 'away_shots_on_target',
            'home_possession', 'away_possession', 'possession_difference',
            'home_fouls', 'away_fouls', 'total_fouls',
            'attacking_intensity', 'home_attacking_ratio', 'away_attacking_ratio'
        ]
        
        return df, feature_cols
    
    def train_corners_models(self, data):
        """Train corners prediction models"""
        print("🤖 Training Corners Prediction Models")
        print("=" * 40)
        
        df, feature_cols = self.prepare_features(data)
        
        # Prepare features
        X = df[feature_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Train multiple models
        models_trained = 0
        
        # 1. Over 9.5 corners
        if 'corners_over_9' in df.columns:
            y = df['corners_over_9']
            self.models['corners_over_9'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['corners_over_9'].fit(X_scaled, y)
            
            # Cross-validation score
            cv_score = cross_val_score(self.models['corners_over_9'], X_scaled, y, cv=5).mean()
            print(f"✅ Over 9.5 Corners Model - CV Score: {cv_score:.3f}")
            models_trained += 1
        
        # 2. Over 10.5 corners
        if 'corners_over_10' in df.columns:
            y = df['corners_over_10']
            self.models['corners_over_10'] = GradientBoostingClassifier(n_estimators=100, random_state=42)
            self.models['corners_over_10'].fit(X_scaled, y)
            
            cv_score = cross_val_score(self.models['corners_over_10'], X_scaled, y, cv=5).mean()
            print(f"✅ Over 10.5 Corners Model - CV Score: {cv_score:.3f}")
            models_trained += 1
        
        # 3. Corners handicap (Home -2.5)
        if 'corners_handicap' in df.columns:
            y = df['corners_handicap']
            self.models['corners_handicap'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models['corners_handicap'].fit(X_scaled, y)
            
            cv_score = cross_val_score(self.models['corners_handicap'], X_scaled, y, cv=5).mean()
            print(f"✅ Corners Handicap Model - CV Score: {cv_score:.3f}")
            models_trained += 1
        
        print(f"🎯 Successfully trained {models_trained} corners models")
        return models_trained > 0
    
    def predict_corners(self, home_team, away_team, match_features=None):
        """Predict corners for a match"""
        if not any(self.models.values()):
            return {"error": "No models trained"}
        
        # Use default features if not provided
        if match_features is None:
            match_features = {
                'home_shots': 12, 'away_shots': 10,
                'home_shots_on_target': 4, 'away_shots_on_target': 3,
                'home_possession': 55, 'away_possession': 45,
                'home_fouls': 12, 'away_fouls': 14,
                'attacking_intensity': 8, 'home_attacking_ratio': 0.55, 'away_attacking_ratio': 0.45
            }
        
        # Prepare features
        feature_data = {
            'home_shots': match_features.get('home_shots', 12),
            'away_shots': match_features.get('away_shots', 10),
            'total_shots': match_features.get('home_shots', 12) + match_features.get('away_shots', 10),
            'shots_difference': match_features.get('home_shots', 12) - match_features.get('away_shots', 10),
            'home_shots_on_target': match_features.get('home_shots_on_target', 4),
            'away_shots_on_target': match_features.get('away_shots_on_target', 3),
            'home_possession': match_features.get('home_possession', 55),
            'away_possession': match_features.get('away_possession', 45),
            'possession_difference': match_features.get('home_possession', 55) - match_features.get('away_possession', 45),
            'home_fouls': match_features.get('home_fouls', 12),
            'away_fouls': match_features.get('away_fouls', 14),
            'total_fouls': match_features.get('home_fouls', 12) + match_features.get('away_fouls', 14),
            'attacking_intensity': match_features.get('attacking_intensity', 8),
            'home_attacking_ratio': match_features.get('home_attacking_ratio', 0.55),
            'away_attacking_ratio': match_features.get('away_attacking_ratio', 0.45)
        }
        
        # Convert to array
        feature_array = np.array([[
            feature_data['home_shots'], feature_data['away_shots'], feature_data['total_shots'],
            feature_data['shots_difference'], feature_data['home_shots_on_target'], 
            feature_data['away_shots_on_target'], feature_data['home_possession'],
            feature_data['away_possession'], feature_data['possession_difference'],
            feature_data['home_fouls'], feature_data['away_fouls'], feature_data['total_fouls'],
            feature_data['attacking_intensity'], feature_data['home_attacking_ratio'],
            feature_data['away_attacking_ratio']
        ]])
        
        # Scale features
        feature_array_scaled = self.scaler.transform(feature_array)
        
        predictions = {}
        
        # Over 9.5 corners
        if self.models['corners_over_9']:
            proba = self.models['corners_over_9'].predict_proba(feature_array_scaled)[0]
            predictions['over_9_corners'] = {
                'prediction': 'Over 9.5' if proba[1] > 0.5 else 'Under 9.5',
                'confidence': max(proba),
                'probability_over': proba[1]
            }
        
        # Over 10.5 corners
        if self.models['corners_over_10']:
            proba = self.models['corners_over_10'].predict_proba(feature_array_scaled)[0]
            predictions['over_10_corners'] = {
                'prediction': 'Over 10.5' if proba[1] > 0.5 else 'Under 10.5',
                'confidence': max(proba),
                'probability_over': proba[1]
            }
        
        # Corners handicap
        if self.models['corners_handicap']:
            proba = self.models['corners_handicap'].predict_proba(feature_array_scaled)[0]
            predictions['corners_handicap'] = {
                'prediction': f'{home_team} -2.5' if proba[1] > 0.5 else f'{away_team} +2.5',
                'confidence': max(proba),
                'probability_home': proba[1]
            }
        
        return predictions
    
    def backtest_corners_predictions(self, data, test_size=0.2):
        """Backtest corners predictions"""
        print(f"🔍 Backtesting Corners Predictions")
        print("=" * 40)
        
        df, feature_cols = self.prepare_features(data)
        
        # Split data
        X = df[feature_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Test each model
        results = {}
        
        for model_name, model in self.models.items():
            if model and model_name in df.columns:
                y = df[model_name]
                X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=test_size, random_state=42)
                
                # Train and predict
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                
                accuracy = accuracy_score(y_test, y_pred)
                results[model_name] = {
                    'accuracy': accuracy,
                    'correct': sum(y_pred == y_test),
                    'total': len(y_test)
                }
                
                print(f"📊 {model_name.replace('_', ' ').title()}: {accuracy:.1%} ({results[model_name]['correct']}/{results[model_name]['total']})")
        
        return results

def main():
    print("🏆 Ultimate Corners Predictor")
    print("=" * 50)
    
    predictor = UltimateCornersPredictor()
    
    # Collect historical data
    print("📥 Collecting historical corners data...")
    historical_data = predictor.collect_historical_data(league_id="39", season="2023", max_matches=80)
    
    if len(historical_data) < 10:
        print("❌ Insufficient data collected")
        return
    
    print(f"✅ Collected {len(historical_data)} matches with corners data")
    
    # Train models
    models_trained = predictor.train_corners_models(historical_data)
    
    if not models_trained:
        print("❌ Failed to train models")
        return
    
    # Backtest
    backtest_results = predictor.backtest_corners_predictions(historical_data)
    
    # Example predictions
    print(f"\n🎯 Example Corners Predictions:")
    print("-" * 40)
    
    # Arsenal vs Chelsea example
    predictions = predictor.predict_corners("Arsenal", "Chelsea")
    
    for category, pred in predictions.items():
        print(f"📈 {category.replace('_', ' ').title()}: {pred['prediction']} ({pred['confidence']:.1%})")
    
    # Save data
    with open('corners_historical_data.json', 'w') as f:
        json.dump(historical_data, f, indent=2)
    
    print(f"\n💾 Saved {len(historical_data)} matches to corners_historical_data.json")
    print("🚀 Ultimate Corners Predictor ready!")

if __name__ == "__main__":
    main()
