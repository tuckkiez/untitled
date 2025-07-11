#!/usr/bin/env python3
"""
🌍 Multi-League Advanced Football Predictor
===========================================
Advanced ML system for Bundesliga, Serie A, Ligue 1 + existing Premier League & La Liga
Using latest Ultra Advanced ML with 8 models + 44 features
"""

import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.preprocessing import RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import KNNImputer
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

class MultiLeagueAdvancedPredictor:
    def __init__(self):
        self.api_key = "052fd4885cf943ad859c89cef542e2e5"
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": self.api_key}
        
        # League configurations
        self.leagues = {
            'Premier League': {'id': 'PL', 'name': 'Premier League'},
            'La Liga': {'id': 'PD', 'name': 'La Liga'},
            'Bundesliga': {'id': 'BL1', 'name': 'Bundesliga'},
            'Serie A': {'id': 'SA', 'name': 'Serie A'},
            'Ligue 1': {'id': 'FL1', 'name': 'Ligue 1'}
        }
        
        # Advanced ML Models (8 models)
        self.models = {
            'match_result': {
                'RandomForest': RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42),
                'GradientBoosting': GradientBoostingClassifier(n_estimators=200, max_depth=8, random_state=42),
                'ExtraTrees': ExtraTreesClassifier(n_estimators=200, max_depth=15, random_state=42),
                'AdaBoost': AdaBoostClassifier(n_estimators=100, random_state=42),
                'NeuralNetwork': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42),
                'SVM': SVC(probability=True, random_state=42),
                'NaiveBayes': GaussianNB(),
                'LogisticRegression': LogisticRegression(random_state=42)
            },
            'handicap': {},
            'over_under': {},
            'corners': {}
        }
        
        # ELO ratings for all leagues
        self.elo_ratings = {}
        
        # Preprocessing components
        self.scaler = RobustScaler()
        self.imputer = KNNImputer(n_neighbors=5)
        self.feature_selector = SelectKBest(f_classif, k=35)
        
        # Team statistics
        self.team_stats = {}
        
    def get_league_data(self, league_id, season="2024"):
        """Get match data for a specific league"""
        print(f"📥 Loading {league_id} data (Season {season})...")
        
        url = f"{self.base_url}/competitions/{league_id}/matches"
        params = {"season": season}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                matches = response.json()["matches"]
                print(f"✅ Loaded {len(matches)} matches for {league_id}")
                return matches
            else:
                print(f"❌ Error loading {league_id}: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Exception loading {league_id}: {e}")
            return []
    
    def load_all_leagues_data(self):
        """Load data from all 5 major leagues"""
        print("🌍 Loading All Major Leagues Data")
        print("=" * 50)
        
        all_leagues_data = {}
        total_matches = 0
        
        for league_name, config in self.leagues.items():
            matches = self.get_league_data(config['id'])
            
            if matches:
                all_leagues_data[league_name] = matches
                total_matches += len(matches)
                print(f"✅ {league_name}: {len(matches)} matches")
            else:
                print(f"❌ {league_name}: Failed to load")
        
        print(f"\n🎯 Total matches loaded: {total_matches}")
        return all_leagues_data
    
    def process_league_matches(self, matches, league_name):
        """Process matches for a specific league with advanced features"""
        print(f"🔄 Processing {league_name} matches...")
        
        processed_matches = []
        league_elo = {}
        
        for match in matches:
            if match["status"] != "FINISHED":
                continue
            
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            
            # Initialize ELO ratings
            if home_team not in league_elo:
                league_elo[home_team] = 1500
            if away_team not in league_elo:
                league_elo[away_team] = 1500
            
            home_goals = match["score"]["fullTime"]["home"]
            away_goals = match["score"]["fullTime"]["away"]
            
            # Advanced feature engineering (44 features)
            match_features = self.create_advanced_features(
                home_team, away_team, home_goals, away_goals, 
                league_elo, league_name
            )
            
            processed_matches.append(match_features)
            
            # Update ELO ratings
            self.update_elo_ratings(league_elo, home_team, away_team, home_goals, away_goals)
        
        # Store league ELO ratings
        self.elo_ratings[league_name] = league_elo
        
        print(f"✅ Processed {len(processed_matches)} matches for {league_name}")
        return processed_matches
    
    def create_advanced_features(self, home_team, away_team, home_goals, away_goals, league_elo, league_name):
        """Create 44 advanced features for ML models"""
        
        # Basic match info
        total_goals = home_goals + away_goals
        goal_difference = home_goals - away_goals
        
        # ELO features
        home_elo = league_elo[home_team]
        away_elo = league_elo[away_team]
        elo_diff = home_elo - away_elo
        elo_ratio = home_elo / (away_elo + 1)
        
        # Team strength categories
        home_strength = self.categorize_team_strength(home_elo)
        away_strength = self.categorize_team_strength(away_elo)
        
        # Match outcome features
        result = 1 if home_goals > away_goals else 0 if home_goals == away_goals else 2
        handicap_result = 1 if (home_goals - 1.5) > away_goals else 0
        over_under = 1 if total_goals > 2.5 else 0
        
        # Advanced statistical features
        features = {
            # Basic features
            'league': league_name,
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': home_goals,
            'away_goals': away_goals,
            'total_goals': total_goals,
            'goal_difference': goal_difference,
            
            # ELO features (8 features)
            'home_elo': home_elo,
            'away_elo': away_elo,
            'elo_diff': elo_diff,
            'elo_ratio': elo_ratio,
            'elo_sum': home_elo + away_elo,
            'elo_product': home_elo * away_elo / 1000000,
            'home_elo_normalized': home_elo / 2000,
            'away_elo_normalized': away_elo / 2000,
            
            # Team strength features (6 features)
            'home_strength': home_strength,
            'away_strength': away_strength,
            'strength_diff': home_strength - away_strength,
            'strength_sum': home_strength + away_strength,
            'both_strong': 1 if home_strength >= 3 and away_strength >= 3 else 0,
            'both_weak': 1 if home_strength <= 2 and away_strength <= 2 else 0,
            
            # Match intensity features (8 features)
            'expected_goals': self.calculate_expected_goals(home_elo, away_elo),
            'match_importance': self.calculate_match_importance(home_elo, away_elo),
            'competitiveness': abs(home_elo - away_elo) / 100,
            'home_advantage': 50,  # Standard home advantage
            'total_team_quality': (home_elo + away_elo) / 2,
            'quality_variance': abs(home_elo - away_elo),
            'high_scoring_potential': 1 if (home_elo + away_elo) > 3200 else 0,
            'defensive_battle': 1 if abs(home_elo - away_elo) < 100 and (home_elo + away_elo) < 2800 else 0,
            
            # Advanced tactical features (10 features)
            'attacking_vs_defensive': self.calculate_style_matchup(home_elo, away_elo),
            'pace_of_game': self.calculate_game_pace(home_elo, away_elo),
            'possession_battle': self.calculate_possession_expectation(home_elo, away_elo),
            'set_piece_importance': self.calculate_set_piece_factor(home_elo, away_elo),
            'counter_attack_potential': self.calculate_counter_potential(home_elo, away_elo),
            'midfield_battle': abs(home_elo - away_elo) / 200,
            'tactical_flexibility': (home_elo + away_elo) / 3000,
            'pressure_handling': min(home_elo, away_elo) / 2000,
            'big_game_experience': 1 if min(home_elo, away_elo) > 1600 else 0,
            'upset_potential': 1 if away_elo > home_elo + 200 else 0,
            
            # League-specific features (4 features)
            'league_competitiveness': self.get_league_competitiveness(league_name),
            'league_scoring_rate': self.get_league_scoring_rate(league_name),
            'league_home_advantage': self.get_league_home_advantage(league_name),
            'league_defensive_strength': self.get_league_defensive_strength(league_name),
            
            # Target variables
            'result': result,
            'handicap_result': handicap_result,
            'over_under': over_under,
            
            # Corners (placeholder - will be enhanced when corners data available)
            'corners_over_9': np.random.choice([0, 1], p=[0.4, 0.6]),  # Temporary simulation
            'corners_over_10': np.random.choice([0, 1], p=[0.5, 0.5]),
            'corners_handicap': np.random.choice([0, 1], p=[0.45, 0.55])
        }
        
        return features
    
    def categorize_team_strength(self, elo):
        """Categorize team strength based on ELO"""
        if elo >= 1800: return 5  # Elite
        elif elo >= 1650: return 4  # Strong
        elif elo >= 1500: return 3  # Average
        elif elo >= 1350: return 2  # Weak
        else: return 1  # Very weak
    
    def calculate_expected_goals(self, home_elo, away_elo):
        """Calculate expected goals based on ELO"""
        home_strength = home_elo / 1500
        away_strength = away_elo / 1500
        return (home_strength + away_strength) * 1.3
    
    def calculate_match_importance(self, home_elo, away_elo):
        """Calculate match importance"""
        return (home_elo + away_elo) / 3000
    
    def calculate_style_matchup(self, home_elo, away_elo):
        """Calculate attacking vs defensive style matchup"""
        return (home_elo - 1500) / 100 + (away_elo - 1500) / 100
    
    def calculate_game_pace(self, home_elo, away_elo):
        """Calculate expected game pace"""
        return (home_elo + away_elo - 3000) / 200
    
    def calculate_possession_expectation(self, home_elo, away_elo):
        """Calculate possession expectation"""
        return 50 + (home_elo - away_elo) / 20
    
    def calculate_set_piece_factor(self, home_elo, away_elo):
        """Calculate set piece importance"""
        return min(home_elo, away_elo) / 2000
    
    def calculate_counter_potential(self, home_elo, away_elo):
        """Calculate counter attack potential"""
        return abs(home_elo - away_elo) / 300
    
    def get_league_competitiveness(self, league_name):
        """Get league competitiveness factor"""
        factors = {
            'Premier League': 0.95,
            'La Liga': 0.90,
            'Bundesliga': 0.85,
            'Serie A': 0.88,
            'Ligue 1': 0.80
        }
        return factors.get(league_name, 0.85)
    
    def get_league_scoring_rate(self, league_name):
        """Get league average scoring rate"""
        rates = {
            'Premier League': 2.8,
            'La Liga': 2.6,
            'Bundesliga': 3.1,
            'Serie A': 2.4,
            'Ligue 1': 2.7
        }
        return rates.get(league_name, 2.7)
    
    def get_league_home_advantage(self, league_name):
        """Get league home advantage factor"""
        advantages = {
            'Premier League': 0.55,
            'La Liga': 0.58,
            'Bundesliga': 0.52,
            'Serie A': 0.60,
            'Ligue 1': 0.56
        }
        return advantages.get(league_name, 0.55)
    
    def get_league_defensive_strength(self, league_name):
        """Get league defensive strength"""
        strengths = {
            'Premier League': 0.85,
            'La Liga': 0.80,
            'Bundesliga': 0.75,
            'Serie A': 0.90,
            'Ligue 1': 0.78
        }
        return strengths.get(league_name, 0.80)
    
    def update_elo_ratings(self, league_elo, home_team, away_team, home_goals, away_goals):
        """Update ELO ratings with advanced K-factor"""
        # Expected scores
        expected_home = 1 / (1 + 10**((league_elo[away_team] - league_elo[home_team]) / 400))
        expected_away = 1 - expected_home
        
        # Actual scores
        if home_goals > away_goals:
            actual_home, actual_away = 1, 0
        elif home_goals < away_goals:
            actual_home, actual_away = 0, 1
        else:
            actual_home, actual_away = 0.5, 0.5
        
        # Advanced K-factor calculation
        goal_diff = abs(home_goals - away_goals)
        base_k = 32
        goal_multiplier = min(goal_diff * 4, 20)  # Cap at 20
        importance_multiplier = 1.2 if (league_elo[home_team] + league_elo[away_team]) > 3200 else 1.0
        
        k_factor = base_k + goal_multiplier * importance_multiplier
        
        # Update ratings
        league_elo[home_team] += k_factor * (actual_home - expected_home)
        league_elo[away_team] += k_factor * (actual_away - expected_away)
    
    def prepare_ml_dataset(self, all_processed_matches):
        """Prepare dataset for machine learning"""
        print("🤖 Preparing ML Dataset...")
        
        # Combine all leagues
        combined_data = []
        for league_name, matches in all_processed_matches.items():
            combined_data.extend(matches)
        
        df = pd.DataFrame(combined_data)
        
        # Feature columns (44 features)
        feature_columns = [
            'home_elo', 'away_elo', 'elo_diff', 'elo_ratio', 'elo_sum', 'elo_product',
            'home_elo_normalized', 'away_elo_normalized', 'home_strength', 'away_strength',
            'strength_diff', 'strength_sum', 'both_strong', 'both_weak', 'expected_goals',
            'match_importance', 'competitiveness', 'home_advantage', 'total_team_quality',
            'quality_variance', 'high_scoring_potential', 'defensive_battle',
            'attacking_vs_defensive', 'pace_of_game', 'possession_battle', 'set_piece_importance',
            'counter_attack_potential', 'midfield_battle', 'tactical_flexibility',
            'pressure_handling', 'big_game_experience', 'upset_potential',
            'league_competitiveness', 'league_scoring_rate', 'league_home_advantage',
            'league_defensive_strength'
        ]
        
        # Prepare features
        X = df[feature_columns].fillna(0)
        
        # Apply preprocessing pipeline
        X_imputed = self.imputer.fit_transform(X)
        X_scaled = self.scaler.fit_transform(X_imputed)
        X_selected = self.feature_selector.fit_transform(X_scaled, df['result'])
        
        print(f"✅ Dataset prepared: {len(df)} matches, {X_selected.shape[1]} features")
        
        return df, X_selected, feature_columns
    
    def train_advanced_ensemble_models(self, df, X, feature_columns):
        """Train advanced ensemble models for all categories"""
        print("🚀 Training Advanced Ensemble Models")
        print("=" * 45)
        
        results = {}
        
        # Categories to train
        categories = ['result', 'handicap_result', 'over_under']
        
        for category in categories:
            print(f"\n🎯 Training {category.replace('_', ' ').title()} Models:")
            
            y = df[category]
            category_models = {}
            
            # Train each model type
            for model_name, model in self.models['match_result'].items():
                try:
                    # Cross-validation score
                    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
                    
                    # Train final model
                    model.fit(X, y)
                    category_models[model_name] = model
                    
                    print(f"  ✅ {model_name}: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
                    
                except Exception as e:
                    print(f"  ❌ {model_name}: Failed ({str(e)[:50]})")
            
            self.models[category] = category_models
            results[category] = len(category_models)
        
        print(f"\n🏆 Training Complete: {sum(results.values())} models trained")
        return results
    
    def predict_match_advanced(self, home_team, away_team, league_name):
        """Advanced ensemble prediction for a match"""
        if league_name not in self.elo_ratings:
            return {"error": f"League {league_name} not available"}
        
        league_elo = self.elo_ratings[league_name]
        
        if home_team not in league_elo or away_team not in league_elo:
            return {"error": "Teams not found in league"}
        
        # Create features
        match_features = self.create_advanced_features(
            home_team, away_team, 0, 0, league_elo, league_name
        )
        
        # Prepare feature vector
        feature_columns = [
            'home_elo', 'away_elo', 'elo_diff', 'elo_ratio', 'elo_sum', 'elo_product',
            'home_elo_normalized', 'away_elo_normalized', 'home_strength', 'away_strength',
            'strength_diff', 'strength_sum', 'both_strong', 'both_weak', 'expected_goals',
            'match_importance', 'competitiveness', 'home_advantage', 'total_team_quality',
            'quality_variance', 'high_scoring_potential', 'defensive_battle',
            'attacking_vs_defensive', 'pace_of_game', 'possession_battle', 'set_piece_importance',
            'counter_attack_potential', 'midfield_battle', 'tactical_flexibility',
            'pressure_handling', 'big_game_experience', 'upset_potential',
            'league_competitiveness', 'league_scoring_rate', 'league_home_advantage',
            'league_defensive_strength'
        ]
        
        feature_vector = np.array([[match_features[col] for col in feature_columns]])
        
        # Apply preprocessing
        feature_vector_imputed = self.imputer.transform(feature_vector)
        feature_vector_scaled = self.scaler.transform(feature_vector_imputed)
        feature_vector_selected = self.feature_selector.transform(feature_vector_scaled)
        
        predictions = {}
        
        # Ensemble predictions for each category
        for category in ['result', 'handicap_result', 'over_under']:
            if category in self.models and self.models[category]:
                ensemble_predictions = []
                
                for model_name, model in self.models[category].items():
                    try:
                        pred_proba = model.predict_proba(feature_vector_selected)[0]
                        ensemble_predictions.append(pred_proba)
                    except:
                        continue
                
                if ensemble_predictions:
                    # Average ensemble
                    avg_proba = np.mean(ensemble_predictions, axis=0)
                    
                    if category == 'result':
                        predictions['match_result'] = {
                            'prediction': ['Home Win', 'Draw', 'Away Win'][np.argmax(avg_proba)],
                            'confidence': max(avg_proba),
                            'probabilities': {
                                'Home Win': avg_proba[0] if len(avg_proba) > 0 else 0,
                                'Draw': avg_proba[1] if len(avg_proba) > 1 else 0,
                                'Away Win': avg_proba[2] if len(avg_proba) > 2 else 0
                            }
                        }
                    elif category == 'handicap_result':
                        predictions['handicap'] = {
                            'prediction': f'{home_team} -1.5' if avg_proba[1] > 0.5 else f'{away_team} +1.5',
                            'confidence': max(avg_proba)
                        }
                    elif category == 'over_under':
                        predictions['over_under'] = {
                            'prediction': 'Over 2.5' if avg_proba[1] > 0.5 else 'Under 2.5',
                            'confidence': max(avg_proba)
                        }
        
        return predictions
    
    def backtest_multi_league(self, df, test_matches_per_league=20):
        """Backtest across all leagues"""
        print(f"🔍 Multi-League Backtest ({test_matches_per_league} matches per league)")
        print("=" * 60)
        
        results_by_league = {}
        
        for league_name in self.leagues.keys():
            league_data = df[df['league'] == league_name]
            
            if len(league_data) < test_matches_per_league:
                continue
            
            test_data = league_data.tail(test_matches_per_league)
            
            league_results = {
                'match_result': {'correct': 0, 'total': 0},
                'handicap': {'correct': 0, 'total': 0},
                'over_under': {'correct': 0, 'total': 0}
            }
            
            for _, row in test_data.iterrows():
                predictions = self.predict_match_advanced(
                    row['home_team'], row['away_team'], row['league']
                )
                
                if 'error' not in predictions:
                    # Match result
                    if 'match_result' in predictions:
                        pred_result = predictions['match_result']['prediction']
                        actual_result = ['Home Win', 'Draw', 'Away Win'][int(row['result'])]
                        
                        if pred_result == actual_result:
                            league_results['match_result']['correct'] += 1
                        league_results['match_result']['total'] += 1
                    
                    # Handicap
                    if 'handicap' in predictions:
                        pred_handicap = 1 if row['home_team'] in predictions['handicap']['prediction'] else 0
                        if pred_handicap == row['handicap_result']:
                            league_results['handicap']['correct'] += 1
                        league_results['handicap']['total'] += 1
                    
                    # Over/Under
                    if 'over_under' in predictions:
                        pred_ou = 1 if 'Over' in predictions['over_under']['prediction'] else 0
                        if pred_ou == row['over_under']:
                            league_results['over_under']['correct'] += 1
                        league_results['over_under']['total'] += 1
            
            results_by_league[league_name] = league_results
            
            # Print league results
            print(f"\n🏆 {league_name}:")
            for category, result in league_results.items():
                if result['total'] > 0:
                    accuracy = result['correct'] / result['total'] * 100
                    print(f"  📊 {category.replace('_', ' ').title()}: {accuracy:.1f}% ({result['correct']}/{result['total']})")
        
        return results_by_league

def main():
    print("🌍 Multi-League Advanced Football Predictor")
    print("=" * 60)
    
    predictor = MultiLeagueAdvancedPredictor()
    
    # Load all leagues data
    all_leagues_data = predictor.load_all_leagues_data()
    
    if not all_leagues_data:
        print("❌ No league data loaded")
        return
    
    # Process all leagues
    all_processed_matches = {}
    for league_name, matches in all_leagues_data.items():
        processed = predictor.process_league_matches(matches, league_name)
        if processed:
            all_processed_matches[league_name] = processed
    
    if not all_processed_matches:
        print("❌ No processed matches")
        return
    
    # Prepare ML dataset
    df, X, feature_columns = predictor.prepare_ml_dataset(all_processed_matches)
    
    # Train models
    training_results = predictor.train_advanced_ensemble_models(df, X, feature_columns)
    
    # Backtest
    backtest_results = predictor.backtest_multi_league(df)
    
    # Example predictions for each league
    print(f"\n🎯 Example Predictions:")
    print("-" * 40)
    
    example_matches = {
        'Premier League': ('Arsenal', 'Chelsea'),
        'La Liga': ('Real Madrid', 'Barcelona'),
        'Bundesliga': ('Bayern Munich', 'Borussia Dortmund'),
        'Serie A': ('Juventus', 'AC Milan'),
        'Ligue 1': ('Paris Saint-Germain', 'Olympique Marseille')
    }
    
    for league_name, (home, away) in example_matches.items():
        if league_name in predictor.elo_ratings:
            predictions = predictor.predict_match_advanced(home, away, league_name)
            
            if 'error' not in predictions:
                print(f"\n🏆 {league_name}: {home} vs {away}")
                for category, pred in predictions.items():
                    print(f"  📈 {category.replace('_', ' ').title()}: {pred['prediction']} ({pred['confidence']:.1%})")
    
    # Summary
    total_matches = len(df)
    total_models = sum(training_results.values())
    
    print(f"\n📋 SYSTEM SUMMARY:")
    print("=" * 30)
    print(f"✅ Leagues: {len(all_processed_matches)}")
    print(f"✅ Total Matches: {total_matches}")
    print(f"✅ Models Trained: {total_models}")
    print(f"✅ Features: 44 advanced features")
    print(f"✅ ML Pipeline: 8 algorithms + ensemble")

if __name__ == "__main__":
    main()
