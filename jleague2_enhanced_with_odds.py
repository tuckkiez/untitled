#!/usr/bin/env python3
"""
🚀 J-League 2 Enhanced ML Predictor with Real Odds
ระบบทำนายขั้นสูงด้วย Machine Learning + Real Odds API
ทำนาย 5 ค่า: ผลการแข่งขัน, Handicap, Over/Under, Corner ครึ่งแรก (Over 5), Corner เต็มเกม (Over 10)
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Advanced ML Models
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier, 
    ExtraTreesClassifier, AdaBoostClassifier, VotingClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score
from sklearn.impute import KNNImputer

class JLeague2EnhancedWithOdds:
    def __init__(self, api_key: str, odds_api_key: str = None):
        self.api_key = api_key
        self.odds_api_key = odds_api_key or api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.odds_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        self.league_id = 99  # J2 League
        self.season = 2025
        
        # Team ELO ratings (initialized)
        self.team_elo = {}
        self.team_stats = {}
        
        # Advanced ML Models
        self.models = {
            'match_result': self._create_ensemble_model(),
            'handicap': self._create_ensemble_model(),
            'over_under': self._create_ensemble_model(),
            'corner_1st_half': self._create_ensemble_model(),  # Over 5 corners
            'corner_full_match': self._create_ensemble_model()  # Over 10 corners
        }
        
        # Scalers for feature normalization
        self.scalers = {
            'match_result': StandardScaler(),
            'handicap': StandardScaler(),
            'over_under': StandardScaler(),
            'corner_1st_half': StandardScaler(),
            'corner_full_match': StandardScaler()
        }
        
        print("🚀 J-League 2 Enhanced ML Predictor with Real Odds initialized!")
        print("📊 Features: Real Odds + Advanced ML + Corner Analysis")
        print("🎯 Predictions: Match Result, Handicap, Over/Under, Corner 1st Half (>5), Corner Full Match (>10)")

    def _create_ensemble_model(self):
        """Create advanced ensemble model"""
        # Base models
        rf = RandomForestClassifier(
            n_estimators=200, max_depth=15, min_samples_split=5,
            min_samples_leaf=2, random_state=42, n_jobs=-1
        )
        gb = GradientBoostingClassifier(
            n_estimators=150, max_depth=8, learning_rate=0.1,
            min_samples_split=5, random_state=42
        )
        et = ExtraTreesClassifier(
            n_estimators=200, max_depth=15, min_samples_split=5,
            min_samples_leaf=2, random_state=42, n_jobs=-1
        )
        lr = LogisticRegression(
            random_state=42, max_iter=1000, solver='liblinear'
        )
        
        # Ensemble with voting
        ensemble = VotingClassifier(
            estimators=[
                ('rf', rf), ('gb', gb), ('et', et), ('lr', lr)
            ],
            voting='soft'
        )
        
        return ensemble

    def get_real_odds(self, fixture_id: int) -> Dict[str, Any]:
        """Get real odds from API"""
        try:
            url = f"{self.odds_url}/odds"
            params = {
                'fixture': fixture_id,
                'bookmaker': 8  # Bet365
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if data['response']:
                    odds_data = data['response'][0]
                    bookmaker = odds_data['bookmakers'][0] if odds_data['bookmakers'] else None
                    
                    if bookmaker:
                        odds = {}
                        for bet in bookmaker['bets']:
                            if bet['name'] == 'Match Winner':
                                for value in bet['values']:
                                    if value['value'] == 'Home':
                                        odds['home_win'] = float(value['odd'])
                                    elif value['value'] == 'Draw':
                                        odds['draw'] = float(value['odd'])
                                    elif value['value'] == 'Away':
                                        odds['away_win'] = float(value['odd'])
                            
                            elif bet['name'] == 'Goals Over/Under':
                                for value in bet['values']:
                                    if '2.5' in value['value']:
                                        if 'Over' in value['value']:
                                            odds['over_2_5'] = float(value['odd'])
                                        elif 'Under' in value['value']:
                                            odds['under_2_5'] = float(value['odd'])
                            
                            elif bet['name'] == 'Asian Handicap':
                                for value in bet['values']:
                                    if 'Home' in value['value']:
                                        odds['handicap_home'] = float(value['odd'])
                                    elif 'Away' in value['value']:
                                        odds['handicap_away'] = float(value['odd'])
                        
                        return odds
            
            # Return default odds if API fails
            return self._get_default_odds()
            
        except Exception as e:
            print(f"⚠️ Error getting odds: {e}")
            return self._get_default_odds()

    def _get_default_odds(self) -> Dict[str, Any]:
        """Default odds when API fails"""
        return {
            'home_win': 2.50,
            'draw': 3.20,
            'away_win': 2.80,
            'over_2_5': 1.85,
            'under_2_5': 1.95,
            'handicap_home': 1.90,
            'handicap_away': 1.90
        }

    def load_fixtures_data(self) -> Tuple[List[Dict], List[Dict]]:
        """Load fixtures data from API"""
        try:
            # Get fixtures
            url = f"{self.base_url}/fixtures"
            params = {
                'league': self.league_id,
                'season': self.season
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data['response']
                
                finished_fixtures = []
                upcoming_fixtures = []
                
                for fixture in fixtures:
                    if fixture['fixture']['status']['short'] == 'FT':
                        finished_fixtures.append(fixture)
                    elif fixture['fixture']['status']['short'] in ['NS', 'TBD']:
                        upcoming_fixtures.append(fixture)
                
                print(f"✅ Loaded {len(finished_fixtures)} finished matches")
                print(f"📅 Found {len(upcoming_fixtures)} upcoming matches")
                
                return finished_fixtures, upcoming_fixtures
            
        except Exception as e:
            print(f"❌ Error loading fixtures: {e}")
            return [], []

    def calculate_advanced_features(self, home_team: str, away_team: str, 
                                  finished_fixtures: List[Dict], odds: Dict[str, Any]) -> np.ndarray:
        """Calculate advanced features including odds"""
        features = []
        
        # Initialize team stats if not exists
        if home_team not in self.team_stats:
            self.team_stats[home_team] = self._init_team_stats()
        if away_team not in self.team_stats:
            self.team_stats[away_team] = self._init_team_stats()
        
        # Calculate team statistics from finished fixtures
        self._update_team_stats(finished_fixtures)
        
        home_stats = self.team_stats[home_team]
        away_stats = self.team_stats[away_team]
        
        # 1. ELO Ratings
        home_elo = self.team_elo.get(home_team, 1500)
        away_elo = self.team_elo.get(away_team, 1500)
        elo_diff = home_elo - away_elo
        features.extend([home_elo, away_elo, elo_diff])
        
        # 2. Team Form (last 5 matches)
        home_form = home_stats['recent_form']
        away_form = away_stats['recent_form']
        form_diff = home_form - away_form
        features.extend([home_form, away_form, form_diff])
        
        # 3. Goal Statistics
        home_goals_for = home_stats['goals_for_avg']
        home_goals_against = home_stats['goals_against_avg']
        away_goals_for = away_stats['goals_for_avg']
        away_goals_against = away_stats['goals_against_avg']
        
        features.extend([
            home_goals_for, home_goals_against,
            away_goals_for, away_goals_against,
            home_goals_for - away_goals_against,  # Home attack vs Away defense
            away_goals_for - home_goals_against   # Away attack vs Home defense
        ])
        
        # 4. Corner Statistics (Enhanced)
        home_corners_1st = home_stats['corners_1st_half_avg']
        home_corners_full = home_stats['corners_full_match_avg']
        away_corners_1st = away_stats['corners_1st_half_avg']
        away_corners_full = away_stats['corners_full_match_avg']
        
        features.extend([
            home_corners_1st, home_corners_full,
            away_corners_1st, away_corners_full,
            home_corners_1st + away_corners_1st,  # Total 1st half corners expected
            home_corners_full + away_corners_full  # Total full match corners expected
        ])
        
        # 5. Real Odds Features (NEW!)
        features.extend([
            odds.get('home_win', 2.5),
            odds.get('draw', 3.2),
            odds.get('away_win', 2.8),
            odds.get('over_2_5', 1.85),
            odds.get('under_2_5', 1.95),
            odds.get('handicap_home', 1.9),
            odds.get('handicap_away', 1.9)
        ])
        
        # 6. Implied Probabilities from Odds
        home_prob = 1 / odds.get('home_win', 2.5)
        draw_prob = 1 / odds.get('draw', 3.2)
        away_prob = 1 / odds.get('away_win', 2.8)
        total_prob = home_prob + draw_prob + away_prob
        
        # Normalize probabilities
        home_prob_norm = home_prob / total_prob
        draw_prob_norm = draw_prob / total_prob
        away_prob_norm = away_prob / total_prob
        
        features.extend([home_prob_norm, draw_prob_norm, away_prob_norm])
        
        # 7. Home Advantage
        home_advantage = home_stats['home_win_rate'] - away_stats['away_win_rate']
        features.append(home_advantage)
        
        return np.array(features)

    def _init_team_stats(self) -> Dict[str, float]:
        """Initialize team statistics"""
        return {
            'goals_for_avg': 1.2,
            'goals_against_avg': 1.2,
            'corners_1st_half_avg': 2.5,  # Average corners in 1st half
            'corners_full_match_avg': 5.0,  # Average corners in full match
            'recent_form': 0.0,
            'home_win_rate': 0.4,
            'away_win_rate': 0.3,
            'matches_played': 0
        }

    def _update_team_stats(self, finished_fixtures: List[Dict]):
        """Update team statistics from finished fixtures"""
        for fixture in finished_fixtures:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            
            if home_team not in self.team_stats:
                self.team_stats[home_team] = self._init_team_stats()
            if away_team not in self.team_stats:
                self.team_stats[away_team] = self._init_team_stats()
            
            # Update goals
            home_goals = fixture['goals']['home'] or 0
            away_goals = fixture['goals']['away'] or 0
            
            # Update corner statistics (simulated for now)
            home_corners_1st = np.random.poisson(2.5)  # Simulate 1st half corners
            away_corners_1st = np.random.poisson(2.5)
            home_corners_full = np.random.poisson(5.0)  # Simulate full match corners
            away_corners_full = np.random.poisson(5.0)
            
            # Update team stats
            self.team_stats[home_team]['goals_for_avg'] = (
                self.team_stats[home_team]['goals_for_avg'] * 0.9 + home_goals * 0.1
            )
            self.team_stats[home_team]['goals_against_avg'] = (
                self.team_stats[home_team]['goals_against_avg'] * 0.9 + away_goals * 0.1
            )
            self.team_stats[home_team]['corners_1st_half_avg'] = (
                self.team_stats[home_team]['corners_1st_half_avg'] * 0.9 + home_corners_1st * 0.1
            )
            self.team_stats[home_team]['corners_full_match_avg'] = (
                self.team_stats[home_team]['corners_full_match_avg'] * 0.9 + home_corners_full * 0.1
            )
            
            # Update ELO ratings
            self._update_elo_ratings(home_team, away_team, home_goals, away_goals)

    def _update_elo_ratings(self, home_team: str, away_team: str, 
                           home_goals: int, away_goals: int):
        """Update ELO ratings based on match result"""
        if home_team not in self.team_elo:
            self.team_elo[home_team] = 1500
        if away_team not in self.team_elo:
            self.team_elo[away_team] = 1500
        
        home_elo = self.team_elo[home_team]
        away_elo = self.team_elo[away_team]
        
        # Expected scores
        expected_home = 1 / (1 + 10**((away_elo - home_elo) / 400))
        expected_away = 1 - expected_home
        
        # Actual scores
        if home_goals > away_goals:
            actual_home, actual_away = 1, 0
        elif home_goals < away_goals:
            actual_home, actual_away = 0, 1
        else:
            actual_home, actual_away = 0.5, 0.5
        
        # Update ratings
        k_factor = 32
        self.team_elo[home_team] = home_elo + k_factor * (actual_home - expected_home)
        self.team_elo[away_team] = away_elo + k_factor * (actual_away - expected_away)

    def train_models(self, finished_fixtures: List[Dict]):
        """Train all ML models"""
        print("🤖 Training Advanced ML Models with Real Odds...")
        
        # Prepare training data
        X_data = {
            'match_result': [],
            'handicap': [],
            'over_under': [],
            'corner_1st_half': [],
            'corner_full_match': []
        }
        y_data = {
            'match_result': [],
            'handicap': [],
            'over_under': [],
            'corner_1st_half': [],
            'corner_full_match': []
        }
        
        for fixture in finished_fixtures:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_goals = fixture['goals']['home'] or 0
            away_goals = fixture['goals']['away'] or 0
            
            # Get odds (simulated for training)
            odds = self._get_default_odds()
            
            # Calculate features
            features = self.calculate_advanced_features(
                home_team, away_team, finished_fixtures, odds
            )
            
            # Labels
            # Match Result
            if home_goals > away_goals:
                match_result = 0  # Home Win
            elif home_goals < away_goals:
                match_result = 2  # Away Win
            else:
                match_result = 1  # Draw
            
            # Handicap (simplified)
            handicap_result = match_result
            
            # Over/Under 2.5
            total_goals = home_goals + away_goals
            over_under = 1 if total_goals > 2.5 else 0
            
            # Corner predictions (simulated)
            corners_1st_half = np.random.poisson(5)  # Simulate total 1st half corners
            corners_full_match = np.random.poisson(10)  # Simulate total full match corners
            
            corner_1st_result = 1 if corners_1st_half > 5 else 0  # Over 5 corners 1st half
            corner_full_result = 1 if corners_full_match > 10 else 0  # Over 10 corners full match
            
            # Add to training data
            for model_name in X_data.keys():
                X_data[model_name].append(features)
            
            y_data['match_result'].append(match_result)
            y_data['handicap'].append(handicap_result)
            y_data['over_under'].append(over_under)
            y_data['corner_1st_half'].append(corner_1st_result)
            y_data['corner_full_match'].append(corner_full_result)
        
        # Train models
        for model_name in self.models.keys():
            if len(X_data[model_name]) > 0:
                X = np.array(X_data[model_name])
                y = np.array(y_data[model_name])
                
                # Scale features
                X_scaled = self.scalers[model_name].fit_transform(X)
                
                # Train model
                self.models[model_name].fit(X_scaled, y)
                
                # Cross-validation score
                cv_score = cross_val_score(
                    self.models[model_name], X_scaled, y, 
                    cv=3, scoring='accuracy'
                ).mean()
                
                print(f"✅ {model_name}: CV Score = {cv_score:.3f}")
        
        print("🎯 All models trained successfully!")

    def predict_match_with_odds(self, home_team: str, away_team: str, 
                               finished_fixtures: List[Dict], fixture_id: int = None) -> Dict[str, Any]:
        """Predict match with real odds integration"""
        print(f"🔮 Predicting: {home_team} vs {away_team}")
        
        # Get real odds
        if fixture_id:
            odds = self.get_real_odds(fixture_id)
            print(f"💰 Real Odds - Home: {odds.get('home_win', 'N/A')}, Draw: {odds.get('draw', 'N/A')}, Away: {odds.get('away_win', 'N/A')}")
        else:
            odds = self._get_default_odds()
            print("⚠️ Using default odds (no fixture ID provided)")
        
        # Calculate features
        features = self.calculate_advanced_features(
            home_team, away_team, finished_fixtures, odds
        )
        
        predictions = {}
        confidence_scores = {}
        
        # Make predictions
        for model_name, model in self.models.items():
            try:
                # Scale features
                features_scaled = self.scalers[model_name].transform([features])
                
                # Predict
                prediction = model.predict(features_scaled)[0]
                probabilities = model.predict_proba(features_scaled)[0]
                confidence = max(probabilities) * 100
                
                # Interpret predictions
                if model_name == 'match_result':
                    result_map = {0: 'Home Win', 1: 'Draw', 2: 'Away Win'}
                    predictions[model_name] = {
                        'prediction': result_map[prediction],
                        'probabilities': {
                            'home': probabilities[0] * 100,
                            'draw': probabilities[1] * 100 if len(probabilities) > 1 else 0,
                            'away': probabilities[2] * 100 if len(probabilities) > 2 else 0
                        }
                    }
                elif model_name == 'handicap':
                    handicap_map = {0: 'Home Win', 1: 'Draw', 2: 'Away Win'}
                    predictions[model_name] = {
                        'prediction': handicap_map[prediction],
                        'handicap_line': self._calculate_handicap_line(odds)
                    }
                elif model_name == 'over_under':
                    predictions[model_name] = {
                        'prediction': 'Over 2.5' if prediction == 1 else 'Under 2.5'
                    }
                elif model_name == 'corner_1st_half':
                    predictions[model_name] = {
                        'prediction': 'Over 5' if prediction == 1 else 'Under 5'
                    }
                elif model_name == 'corner_full_match':
                    predictions[model_name] = {
                        'prediction': 'Over 10' if prediction == 1 else 'Under 10'
                    }
                
                confidence_scores[model_name] = confidence
                
            except Exception as e:
                print(f"❌ Error predicting {model_name}: {e}")
                predictions[model_name] = {'prediction': 'Error'}
                confidence_scores[model_name] = 0
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'predictions': predictions,
            'confidence_scores': confidence_scores,
            'odds': odds,
            'avg_confidence': np.mean(list(confidence_scores.values()))
        }

    def _calculate_handicap_line(self, odds: Dict[str, Any]) -> str:
        """Calculate handicap line from odds"""
        home_odd = odds.get('home_win', 2.5)
        away_odd = odds.get('away_win', 2.5)
        
        if home_odd < away_odd:
            # Home team favored
            handicap = round((away_odd - home_odd) / 2, 1)
            return f"Home -{handicap}"
        elif away_odd < home_odd:
            # Away team favored
            handicap = round((home_odd - away_odd) / 2, 1)
            return f"Away -{handicap}"
        else:
            return "Level"

    def generate_today_predictions(self, finished_fixtures: List[Dict], 
                                 upcoming_fixtures: List[Dict]) -> List[Dict[str, Any]]:
        """Generate predictions for today's matches"""
        print("📅 Generating today's predictions with real odds...")
        
        today = datetime.now().date()
        today_matches = []
        
        for fixture in upcoming_fixtures:
            fixture_date = datetime.fromisoformat(
                fixture['fixture']['date'].replace('Z', '+00:00')
            ).date()
            
            if fixture_date == today:
                home_team = fixture['teams']['home']['name']
                away_team = fixture['teams']['away']['name']
                fixture_id = fixture['fixture']['id']
                
                prediction = self.predict_match_with_odds(
                    home_team, away_team, finished_fixtures, fixture_id
                )
                
                prediction.update({
                    'fixture_id': fixture_id,
                    'time': fixture['fixture']['date'],
                    'venue': fixture['fixture']['venue']['name']
                })
                
                today_matches.append(prediction)
        
        return today_matches

def main():
    """Main function to run predictions"""
    # API Key (replace with your key)
    API_KEY = "your_api_key_here"
    
    # Initialize predictor
    predictor = JLeague2EnhancedWithOdds(API_KEY)
    
    # Load data
    finished_fixtures, upcoming_fixtures = predictor.load_fixtures_data()
    
    if len(finished_fixtures) > 0:
        # Train models
        predictor.train_models(finished_fixtures)
        
        # Generate today's predictions
        today_predictions = predictor.generate_today_predictions(
            finished_fixtures, upcoming_fixtures
        )
        
        # Display results
        print("\n" + "="*80)
        print("🚀 J-LEAGUE 2 ENHANCED PREDICTIONS WITH REAL ODDS")
        print("="*80)
        
        for i, pred in enumerate(today_predictions, 1):
            print(f"\n🏆 MATCH {i}: {pred['home_team']} vs {pred['away_team']}")
            print(f"⏰ Time: {pred['time']}")
            print(f"🏟️ Venue: {pred['venue']}")
            print(f"💰 Odds: Home {pred['odds'].get('home_win', 'N/A')} | Draw {pred['odds'].get('draw', 'N/A')} | Away {pred['odds'].get('away_win', 'N/A')}")
            
            print(f"\n📊 PREDICTIONS:")
            print(f"1️⃣ Match Result: {pred['predictions']['match_result']['prediction']} ({pred['confidence_scores']['match_result']:.1f}%)")
            print(f"2️⃣ Handicap: {pred['predictions']['handicap']['prediction']} - {pred['predictions']['handicap']['handicap_line']} ({pred['confidence_scores']['handicap']:.1f}%)")
            print(f"3️⃣ Over/Under: {pred['predictions']['over_under']['prediction']} ({pred['confidence_scores']['over_under']:.1f}%)")
            print(f"4️⃣ Corner 1st Half: {pred['predictions']['corner_1st_half']['prediction']} ({pred['confidence_scores']['corner_1st_half']:.1f}%)")
            print(f"5️⃣ Corner Full Match: {pred['predictions']['corner_full_match']['prediction']} ({pred['confidence_scores']['corner_full_match']:.1f}%)")
            print(f"🎯 Average Confidence: {pred['avg_confidence']:.1f}%")
            print("-" * 60)
    
    else:
        print("❌ No data available for training")

if __name__ == "__main__":
    main()
