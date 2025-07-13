#!/usr/bin/env python3
"""
🚀 Enhanced Multi-League ML Predictor
ใช้ข้อมูลจากฐานข้อมูลหลายลีกเพื่อทำนายที่แม่นยำขึ้น
Premier League, La Liga, Bundesliga, Ligue 1, Serie A, J-League 2
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Advanced ML Models
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier, 
    ExtraTreesClassifier, VotingClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

class EnhancedMultiLeaguePredictor:
    def __init__(self, db_path: str = "football_leagues.db"):
        self.db_path = db_path
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.feature_columns = []
        
        # League configurations
        self.leagues = {
            'premier_league': {'name': 'Premier League', 'weight': 1.2},
            'la_liga': {'name': 'La Liga', 'weight': 1.1},
            'bundesliga': {'name': 'Bundesliga', 'weight': 1.1},
            'ligue_1': {'name': 'Ligue 1', 'weight': 1.0},
            'serie_a': {'name': 'Serie A', 'weight': 1.1},
            'jleague_2': {'name': 'J-League 2', 'weight': 0.9}
        }
        
        print("🚀 Enhanced Multi-League ML Predictor initialized!")
        print(f"📊 Supporting {len(self.leagues)} leagues")

    def load_multi_league_data(self, seasons: List[int] = [2023, 2024]) -> pd.DataFrame:
        """Load and combine data from multiple leagues"""
        conn = sqlite3.connect(self.db_path)
        
        all_data = []
        
        for league_key, config in self.leagues.items():
            for season in seasons:
                query = '''
                    SELECT 
                        m.*,
                        ht.name as home_team_name,
                        at.name as away_team_name,
                        hts.wins as home_wins,
                        hts.draws as home_draws,
                        hts.losses as home_losses,
                        hts.goals_for as home_goals_for,
                        hts.goals_against as home_goals_against,
                        hts.elo_rating as home_elo,
                        ats.wins as away_wins,
                        ats.draws as away_draws,
                        ats.losses as away_losses,
                        ats.goals_for as away_goals_for,
                        ats.goals_against as away_goals_against,
                        ats.elo_rating as away_elo
                    FROM matches m
                    JOIN teams ht ON m.home_team_id = ht.team_id
                    JOIN teams at ON m.away_team_id = at.team_id
                    LEFT JOIN team_stats hts ON m.home_team_id = hts.team_id AND m.season = hts.season
                    LEFT JOIN team_stats ats ON m.away_team_id = ats.team_id AND m.season = ats.season
                    WHERE m.league_key = ? AND m.season = ? AND m.match_status = 'FT'
                    ORDER BY m.match_date
                '''
                
                league_data = pd.read_sql_query(query, conn, params=(league_key, season))
                if not league_data.empty:
                    league_data['league_weight'] = config['weight']
                    league_data['league_name'] = config['name']
                    all_data.append(league_data)
        
        conn.close()
        
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            print(f"✅ Loaded {len(combined_data)} matches from {len(all_data)} league-seasons")
            return combined_data
        else:
            print("❌ No data found in database")
            return pd.DataFrame()

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced features from multi-league data"""
        print("🔧 Engineering advanced features...")
        
        # Basic features
        df['total_goals'] = df['home_score'] + df['away_score']
        df['goal_difference'] = df['home_score'] - df['away_score']
        df['match_result'] = df.apply(self._get_match_result, axis=1)
        df['over_under_25'] = (df['total_goals'] > 2.5).astype(int)
        
        # ELO difference
        df['elo_difference'] = df['home_elo'].fillna(1500) - df['away_elo'].fillna(1500)
        
        # Team form features
        df['home_win_rate'] = df['home_wins'] / (df['home_wins'] + df['home_draws'] + df['home_losses']).replace(0, 1)
        df['away_win_rate'] = df['away_wins'] / (df['away_wins'] + df['away_draws'] + df['away_losses']).replace(0, 1)
        df['home_goal_avg'] = df['home_goals_for'] / (df['home_wins'] + df['home_draws'] + df['home_losses']).replace(0, 1)
        df['away_goal_avg'] = df['away_goals_for'] / (df['away_wins'] + df['away_draws'] + df['away_losses']).replace(0, 1)
        
        # Attack vs Defense
        df['home_attack_strength'] = df['home_goals_for'] / df['home_goals_for'].mean()
        df['home_defense_strength'] = df['home_goals_against'] / df['home_goals_against'].mean()
        df['away_attack_strength'] = df['away_goals_for'] / df['away_goals_for'].mean()
        df['away_defense_strength'] = df['away_goals_against'] / df['away_goals_against'].mean()
        
        # League-specific features
        df['is_top_league'] = df['league_weight'].apply(lambda x: 1 if x >= 1.1 else 0)
        
        # Encode categorical features
        le_league = LabelEncoder()
        df['league_encoded'] = le_league.fit_transform(df['league_key'])
        self.label_encoders['league'] = le_league
        
        # Select feature columns
        self.feature_columns = [
            'elo_difference', 'home_win_rate', 'away_win_rate',
            'home_goal_avg', 'away_goal_avg', 'home_attack_strength',
            'home_defense_strength', 'away_attack_strength', 'away_defense_strength',
            'league_weight', 'is_top_league', 'league_encoded'
        ]
        
        # Fill missing values
        for col in self.feature_columns:
            df[col] = df[col].fillna(df[col].median())
        
        print(f"✅ Created {len(self.feature_columns)} features")
        return df

    def _get_match_result(self, row):
        """Get match result (0=Home Win, 1=Draw, 2=Away Win)"""
        if row['home_score'] > row['away_score']:
            return 0  # Home Win
        elif row['home_score'] == row['away_score']:
            return 1  # Draw
        else:
            return 2  # Away Win

    def train_models(self, df: pd.DataFrame):
        """Train ML models on multi-league data"""
        print("🤖 Training advanced ML models...")
        
        # Prepare features and targets
        X = df[self.feature_columns].values
        y_result = df['match_result'].values
        y_over_under = df['over_under_25'].values
        
        # Apply league weights to samples
        sample_weights = df['league_weight'].values
        
        # Split data
        X_train, X_test, y_result_train, y_result_test = train_test_split(
            X, y_result, test_size=0.2, random_state=42, stratify=y_result
        )
        _, _, y_ou_train, y_ou_test = train_test_split(
            X, y_over_under, test_size=0.2, random_state=42, stratify=y_over_under
        )
        
        # Scale features
        self.scalers['match_result'] = StandardScaler()
        self.scalers['over_under'] = StandardScaler()
        
        X_train_scaled = self.scalers['match_result'].fit_transform(X_train)
        X_test_scaled = self.scalers['match_result'].transform(X_test)
        
        # Train Match Result Model
        print("🎯 Training Match Result model...")
        rf_result = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
        gb_result = GradientBoostingClassifier(n_estimators=150, max_depth=8, random_state=42)
        et_result = ExtraTreesClassifier(n_estimators=200, max_depth=15, random_state=42)
        lr_result = LogisticRegression(random_state=42, max_iter=1000)
        
        self.models['match_result'] = VotingClassifier(
            estimators=[
                ('rf', rf_result), ('gb', gb_result), 
                ('et', et_result), ('lr', lr_result)
            ],
            voting='soft'
        )
        
        self.models['match_result'].fit(X_train_scaled, y_result_train)
        
        # Evaluate Match Result Model
        result_pred = self.models['match_result'].predict(X_test_scaled)
        result_accuracy = accuracy_score(y_result_test, result_pred)
        print(f"✅ Match Result Accuracy: {result_accuracy:.3f}")
        
        # Train Over/Under Model
        print("🎯 Training Over/Under model...")
        rf_ou = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
        gb_ou = GradientBoostingClassifier(n_estimators=150, max_depth=8, random_state=42)
        et_ou = ExtraTreesClassifier(n_estimators=200, max_depth=15, random_state=42)
        lr_ou = LogisticRegression(random_state=42, max_iter=1000)
        
        self.models['over_under'] = VotingClassifier(
            estimators=[
                ('rf', rf_ou), ('gb', gb_ou), 
                ('et', et_ou), ('lr', lr_ou)
            ],
            voting='soft'
        )
        
        X_train_ou_scaled = self.scalers['over_under'].fit_transform(X_train)
        X_test_ou_scaled = self.scalers['over_under'].transform(X_test)
        
        self.models['over_under'].fit(X_train_ou_scaled, y_ou_train)
        
        # Evaluate Over/Under Model
        ou_pred = self.models['over_under'].predict(X_test_ou_scaled)
        ou_accuracy = accuracy_score(y_ou_test, ou_pred)
        print(f"✅ Over/Under Accuracy: {ou_accuracy:.3f}")
        
        # Feature importance
        self._analyze_feature_importance(df)
        
        print("🎉 Model training completed!")

    def _analyze_feature_importance(self, df: pd.DataFrame):
        """Analyze feature importance across leagues"""
        print("\n📊 Feature Importance Analysis:")
        
        # Get feature importance from Random Forest
        rf_model = self.models['match_result'].named_estimators_['rf']
        importances = rf_model.feature_importances_
        
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        print(feature_importance.head(10))

    def predict_match(self, home_team_stats: Dict, away_team_stats: Dict, 
                     league_key: str) -> Dict[str, Any]:
        """Predict match outcome using trained models"""
        
        # Create feature vector
        league_weight = self.leagues.get(league_key, {}).get('weight', 1.0)
        league_encoded = self.label_encoders['league'].transform([league_key])[0]
        
        features = np.array([[
            home_team_stats.get('elo', 1500) - away_team_stats.get('elo', 1500),  # elo_difference
            home_team_stats.get('win_rate', 0.5),  # home_win_rate
            away_team_stats.get('win_rate', 0.5),  # away_win_rate
            home_team_stats.get('goal_avg', 1.5),  # home_goal_avg
            away_team_stats.get('goal_avg', 1.5),  # away_goal_avg
            home_team_stats.get('attack_strength', 1.0),  # home_attack_strength
            home_team_stats.get('defense_strength', 1.0),  # home_defense_strength
            away_team_stats.get('attack_strength', 1.0),  # away_attack_strength
            away_team_stats.get('defense_strength', 1.0),  # away_defense_strength
            league_weight,  # league_weight
            1 if league_weight >= 1.1 else 0,  # is_top_league
            league_encoded  # league_encoded
        ]])
        
        # Scale features
        features_scaled_result = self.scalers['match_result'].transform(features)
        features_scaled_ou = self.scalers['over_under'].transform(features)
        
        # Make predictions
        result_proba = self.models['match_result'].predict_proba(features_scaled_result)[0]
        result_pred = self.models['match_result'].predict(features_scaled_result)[0]
        
        ou_proba = self.models['over_under'].predict_proba(features_scaled_ou)[0]
        ou_pred = self.models['over_under'].predict(features_scaled_ou)[0]
        
        # Format results
        result_labels = ['Home Win', 'Draw', 'Away Win']
        ou_labels = ['Under 2.5', 'Over 2.5']
        
        return {
            'match_result': {
                'prediction': result_labels[result_pred],
                'probabilities': {
                    'home': result_proba[0] * 100,
                    'draw': result_proba[1] * 100,
                    'away': result_proba[2] * 100
                },
                'confidence': max(result_proba) * 100
            },
            'over_under': {
                'prediction': ou_labels[ou_pred],
                'probabilities': {
                    'under': ou_proba[0] * 100,
                    'over': ou_proba[1] * 100
                },
                'confidence': max(ou_proba) * 100
            },
            'league_info': {
                'league': league_key,
                'weight': league_weight,
                'is_top_league': league_weight >= 1.1
            }
        }

    def save_models(self, model_dir: str = "models"):
        """Save trained models and scalers"""
        import os
        os.makedirs(model_dir, exist_ok=True)
        
        # Save models
        for model_name, model in self.models.items():
            joblib.dump(model, f"{model_dir}/{model_name}_model.pkl")
        
        # Save scalers
        for scaler_name, scaler in self.scalers.items():
            joblib.dump(scaler, f"{model_dir}/{scaler_name}_scaler.pkl")
        
        # Save label encoders
        for encoder_name, encoder in self.label_encoders.items():
            joblib.dump(encoder, f"{model_dir}/{encoder_name}_encoder.pkl")
        
        # Save feature columns
        joblib.dump(self.feature_columns, f"{model_dir}/feature_columns.pkl")
        
        print(f"✅ Models saved to {model_dir}/")

    def load_models(self, model_dir: str = "models"):
        """Load trained models and scalers"""
        try:
            # Load models
            for model_name in ['match_result', 'over_under']:
                self.models[model_name] = joblib.load(f"{model_dir}/{model_name}_model.pkl")
            
            # Load scalers
            for scaler_name in ['match_result', 'over_under']:
                self.scalers[scaler_name] = joblib.load(f"{model_dir}/{scaler_name}_scaler.pkl")
            
            # Load label encoders
            self.label_encoders['league'] = joblib.load(f"{model_dir}/league_encoder.pkl")
            
            # Load feature columns
            self.feature_columns = joblib.load(f"{model_dir}/feature_columns.pkl")
            
            print(f"✅ Models loaded from {model_dir}/")
            return True
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False

    def backtest_performance(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """Backtest model performance on historical data"""
        print("🔍 Backtesting model performance...")
        
        correct_results = 0
        correct_ou = 0
        total_predictions = 0
        
        for _, match in test_data.iterrows():
            # Create dummy team stats for backtesting
            home_stats = {
                'elo': match.get('home_elo', 1500),
                'win_rate': match.get('home_win_rate', 0.5),
                'goal_avg': match.get('home_goal_avg', 1.5),
                'attack_strength': match.get('home_attack_strength', 1.0),
                'defense_strength': match.get('home_defense_strength', 1.0)
            }
            
            away_stats = {
                'elo': match.get('away_elo', 1500),
                'win_rate': match.get('away_win_rate', 0.5),
                'goal_avg': match.get('away_goal_avg', 1.5),
                'attack_strength': match.get('away_attack_strength', 1.0),
                'defense_strength': match.get('away_defense_strength', 1.0)
            }
            
            prediction = self.predict_match(home_stats, away_stats, match['league_key'])
            
            # Check match result
            actual_result = self._get_match_result(match)
            predicted_result_idx = ['Home Win', 'Draw', 'Away Win'].index(prediction['match_result']['prediction'])
            
            if actual_result == predicted_result_idx:
                correct_results += 1
            
            # Check over/under
            actual_ou = 1 if match['total_goals'] > 2.5 else 0
            predicted_ou = 1 if prediction['over_under']['prediction'] == 'Over 2.5' else 0
            
            if actual_ou == predicted_ou:
                correct_ou += 1
            
            total_predictions += 1
        
        result_accuracy = correct_results / total_predictions
        ou_accuracy = correct_ou / total_predictions
        overall_accuracy = (correct_results + correct_ou) / (total_predictions * 2)
        
        performance = {
            'match_result_accuracy': result_accuracy,
            'over_under_accuracy': ou_accuracy,
            'overall_accuracy': overall_accuracy,
            'total_matches': total_predictions
        }
        
        print(f"📊 Backtest Results:")
        print(f"   Match Result: {result_accuracy:.3f}")
        print(f"   Over/Under: {ou_accuracy:.3f}")
        print(f"   Overall: {overall_accuracy:.3f}")
        print(f"   Total Matches: {total_predictions}")
        
        return performance

def main():
    """Main function to demonstrate usage"""
    predictor = EnhancedMultiLeaguePredictor()
    
    # Load multi-league data
    data = predictor.load_multi_league_data()
    
    if not data.empty:
        # Engineer features
        data = predictor.engineer_features(data)
        
        # Train models
        predictor.train_models(data)
        
        # Save models
        predictor.save_models()
        
        # Backtest performance
        test_data = data.sample(n=min(100, len(data)), random_state=42)
        performance = predictor.backtest_performance(test_data)
        
        # Example prediction
        print("\n🔮 Example Prediction:")
        home_stats = {'elo': 1600, 'win_rate': 0.6, 'goal_avg': 2.0, 'attack_strength': 1.2, 'defense_strength': 0.8}
        away_stats = {'elo': 1500, 'win_rate': 0.4, 'goal_avg': 1.5, 'attack_strength': 0.9, 'defense_strength': 1.1}
        
        prediction = predictor.predict_match(home_stats, away_stats, 'premier_league')
        print(f"Match Result: {prediction['match_result']['prediction']} ({prediction['match_result']['confidence']:.1f}%)")
        print(f"Over/Under: {prediction['over_under']['prediction']} ({prediction['over_under']['confidence']:.1f}%)")
    
    else:
        print("❌ No data available. Please run database setup first.")

if __name__ == "__main__":
    main()
