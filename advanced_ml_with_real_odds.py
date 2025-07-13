#!/usr/bin/env python3
"""
Advanced ML System with Real Odds Integration
ระบบ ML ขั้นสูงที่ใช้ odds จริงในการทำนาย
"""

import json
import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

class AdvancedMLWithRealOdds:
    def __init__(self, db_path: str = "comprehensive_odds.db"):
        self.db_path = db_path
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_columns = []
        
    def load_data_from_db(self) -> pd.DataFrame:
        """Load comprehensive data from database"""
        conn = sqlite3.connect(self.db_path)
        
        # Main query to get fixtures with odds
        query = '''
        SELECT 
            f.id as fixture_id,
            f.league_id,
            f.league_name,
            f.home_team,
            f.away_team,
            f.status,
            f.score_home,
            f.score_away,
            f.timestamp,
            o.bookmaker,
            o.bet_name,
            o.value,
            o.odd
        FROM fixtures f
        LEFT JOIN odds o ON f.id = o.fixture_id
        WHERE f.status IN ('FT', '1H', '2H', 'LIVE')
        ORDER BY f.id, o.bookmaker, o.bet_name
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def extract_odds_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract betting odds features for ML"""
        # Pivot odds data to create features
        odds_features = []
        
        for fixture_id in df['fixture_id'].unique():
            fixture_data = df[df['fixture_id'] == fixture_id].iloc[0]
            fixture_odds = df[df['fixture_id'] == fixture_id]
            
            features = {
                'fixture_id': fixture_id,
                'league_id': fixture_data['league_id'],
                'league_name': fixture_data['league_name'],
                'home_team': fixture_data['home_team'],
                'away_team': fixture_data['away_team'],
                'score_home': fixture_data['score_home'],
                'score_away': fixture_data['score_away'],
                'timestamp': fixture_data['timestamp']
            }
            
            # Extract key odds
            match_winner_odds = fixture_odds[fixture_odds['bet_name'] == 'Match Winner']
            if not match_winner_odds.empty:
                home_odds = match_winner_odds[match_winner_odds['value'] == 'Home']['odd'].mean()
                draw_odds = match_winner_odds[match_winner_odds['value'] == 'Draw']['odd'].mean()
                away_odds = match_winner_odds[match_winner_odds['value'] == 'Away']['odd'].mean()
                
                features.update({
                    'home_odds': home_odds if not pd.isna(home_odds) else 2.0,
                    'draw_odds': draw_odds if not pd.isna(draw_odds) else 3.0,
                    'away_odds': away_odds if not pd.isna(away_odds) else 2.0
                })
            else:
                features.update({'home_odds': 2.0, 'draw_odds': 3.0, 'away_odds': 2.0})
            
            # Over/Under odds
            over_under_odds = fixture_odds[fixture_odds['bet_name'] == 'Goals Over/Under']
            over_25_odds = over_under_odds[over_under_odds['value'] == 'Over 2.5']['odd'].mean()
            under_25_odds = over_under_odds[over_under_odds['value'] == 'Under 2.5']['odd'].mean()
            
            features.update({
                'over_25_odds': over_25_odds if not pd.isna(over_25_odds) else 1.8,
                'under_25_odds': under_25_odds if not pd.isna(under_25_odds) else 1.8
            })
            
            # Both teams to score
            btts_odds = fixture_odds[fixture_odds['bet_name'] == 'Both Teams Score']
            btts_yes_odds = btts_odds[btts_odds['value'] == 'Yes']['odd'].mean()
            btts_no_odds = btts_odds[btts_odds['value'] == 'No']['odd'].mean()
            
            features.update({
                'btts_yes_odds': btts_yes_odds if not pd.isna(btts_yes_odds) else 1.8,
                'btts_no_odds': btts_no_odds if not pd.isna(btts_no_odds) else 1.8
            })
            
            odds_features.append(features)
        
        return pd.DataFrame(odds_features)
    
    def create_advanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced features from odds and match data"""
        # Implied probabilities from odds
        df['home_prob'] = 1 / df['home_odds']
        df['draw_prob'] = 1 / df['draw_odds']
        df['away_prob'] = 1 / df['away_odds']
        
        # Normalize probabilities
        total_prob = df['home_prob'] + df['draw_prob'] + df['away_prob']
        df['home_prob_norm'] = df['home_prob'] / total_prob
        df['draw_prob_norm'] = df['draw_prob'] / total_prob
        df['away_prob_norm'] = df['away_prob'] / total_prob
        
        # Market efficiency indicators
        df['market_margin'] = total_prob - 1
        df['favorite_odds'] = df[['home_odds', 'away_odds']].min(axis=1)
        df['underdog_odds'] = df[['home_odds', 'away_odds']].max(axis=1)
        df['odds_ratio'] = df['underdog_odds'] / df['favorite_odds']
        
        # Goal expectation from over/under odds
        df['goals_expectation'] = 2.5 * (df['over_25_odds'] / (df['over_25_odds'] + df['under_25_odds']))
        
        # BTTS probability
        df['btts_prob'] = 1 / df['btts_yes_odds']
        
        # League encoding
        le_league = LabelEncoder()
        df['league_encoded'] = le_league.fit_transform(df['league_name'])
        self.encoders['league'] = le_league
        
        # Create target variables
        df['actual_result'] = df.apply(self._get_match_result, axis=1)
        df['total_goals'] = df['score_home'] + df['score_away']
        df['over_25'] = (df['total_goals'] > 2.5).astype(int)
        df['btts_actual'] = ((df['score_home'] > 0) & (df['score_away'] > 0)).astype(int)
        
        return df
    
    def _get_match_result(self, row):
        """Get match result (H/D/A)"""
        if row['score_home'] > row['score_away']:
            return 'H'
        elif row['score_home'] < row['score_away']:
            return 'A'
        else:
            return 'D'
    
    def prepare_features(self, df: pd.DataFrame) -> tuple:
        """Prepare features for ML models"""
        feature_cols = [
            'league_encoded', 'home_prob_norm', 'draw_prob_norm', 'away_prob_norm',
            'market_margin', 'favorite_odds', 'underdog_odds', 'odds_ratio',
            'goals_expectation', 'btts_prob', 'home_odds', 'draw_odds', 'away_odds',
            'over_25_odds', 'under_25_odds', 'btts_yes_odds', 'btts_no_odds'
        ]
        
        X = df[feature_cols].fillna(df[feature_cols].mean())
        self.feature_columns = feature_cols
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        self.scalers['main'] = scaler
        
        return X_scaled, X
    
    def train_models(self, df: pd.DataFrame):
        """Train multiple ML models"""
        print("🤖 Training Advanced ML Models with Real Odds...")
        
        X_scaled, X_raw = self.prepare_features(df)
        
        # Encode targets
        le_result = LabelEncoder()
        y_result = le_result.fit_transform(df['actual_result'])
        self.encoders['result'] = le_result
        
        # Train models for different predictions
        models_config = {
            'match_result': {
                'target': y_result,
                'models': {
                    'rf': RandomForestClassifier(n_estimators=100, random_state=42),
                    'gb': GradientBoostingClassifier(n_estimators=100, random_state=42),
                    'lr': LogisticRegression(random_state=42, max_iter=1000)
                }
            },
            'over_under': {
                'target': df['over_25'].values,
                'models': {
                    'rf': RandomForestClassifier(n_estimators=100, random_state=42),
                    'gb': GradientBoostingClassifier(n_estimators=100, random_state=42),
                    'lr': LogisticRegression(random_state=42, max_iter=1000)
                }
            },
            'btts': {
                'target': df['btts_actual'].values,
                'models': {
                    'rf': RandomForestClassifier(n_estimators=100, random_state=42),
                    'gb': GradientBoostingClassifier(n_estimators=100, random_state=42),
                    'lr': LogisticRegression(random_state=42, max_iter=1000)
                }
            }
        }
        
        results = {}
        
        for prediction_type, config in models_config.items():
            print(f"\n📊 Training {prediction_type} models...")
            
            y = config['target']
            type_results = {}
            
            for model_name, model in config['models'].items():
                # Cross-validation
                cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
                
                # Train final model
                model.fit(X_scaled, y)
                
                type_results[model_name] = {
                    'model': model,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std()
                }
                
                print(f"  • {model_name.upper()}: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
            
            results[prediction_type] = type_results
        
        self.models = results
        return results
    
    def predict_upcoming_matches(self, upcoming_data: pd.DataFrame) -> pd.DataFrame:
        """Predict upcoming matches using trained models"""
        print("🔮 Making predictions for upcoming matches...")
        
        # Prepare features for upcoming matches
        X_scaled, X_raw = self.prepare_features(upcoming_data)
        
        predictions = []
        
        for idx, row in upcoming_data.iterrows():
            match_features = X_scaled[idx:idx+1]
            
            pred_data = {
                'fixture_id': row['fixture_id'],
                'league_name': row['league_name'],
                'home_team': row['home_team'],
                'away_team': row['away_team'],
                'timestamp': row['timestamp']
            }
            
            # Match result prediction
            if 'match_result' in self.models:
                result_probs = {}
                for model_name, model_info in self.models['match_result'].items():
                    probs = model_info['model'].predict_proba(match_features)[0]
                    result_probs[model_name] = probs
                
                # Ensemble prediction
                avg_probs = np.mean([probs for probs in result_probs.values()], axis=0)
                predicted_result = self.encoders['result'].inverse_transform([np.argmax(avg_probs)])[0]
                
                pred_data.update({
                    'predicted_result': predicted_result,
                    'result_confidence': np.max(avg_probs),
                    'home_win_prob': avg_probs[0] if len(avg_probs) > 0 else 0,
                    'draw_prob': avg_probs[1] if len(avg_probs) > 1 else 0,
                    'away_win_prob': avg_probs[2] if len(avg_probs) > 2 else 0
                })
            
            # Over/Under prediction
            if 'over_under' in self.models:
                ou_probs = []
                for model_name, model_info in self.models['over_under'].items():
                    prob = model_info['model'].predict_proba(match_features)[0][1]
                    ou_probs.append(prob)
                
                avg_ou_prob = np.mean(ou_probs)
                pred_data.update({
                    'over_25_prob': avg_ou_prob,
                    'over_25_prediction': 'Over' if avg_ou_prob > 0.5 else 'Under',
                    'ou_confidence': max(avg_ou_prob, 1 - avg_ou_prob)
                })
            
            # BTTS prediction
            if 'btts' in self.models:
                btts_probs = []
                for model_name, model_info in self.models['btts'].items():
                    prob = model_info['model'].predict_proba(match_features)[0][1]
                    btts_probs.append(prob)
                
                avg_btts_prob = np.mean(btts_probs)
                pred_data.update({
                    'btts_prob': avg_btts_prob,
                    'btts_prediction': 'Yes' if avg_btts_prob > 0.5 else 'No',
                    'btts_confidence': max(avg_btts_prob, 1 - avg_btts_prob)
                })
            
            predictions.append(pred_data)
        
        return pd.DataFrame(predictions)

def main():
    """Main execution function"""
    print("🚀 Advanced ML System with Real Odds")
    print("=" * 50)
    
    # Initialize ML system
    ml_system = AdvancedMLWithRealOdds()
    
    # Load data
    print("📊 Loading data from database...")
    raw_data = ml_system.load_data_from_db()
    
    if raw_data.empty:
        print("❌ No data found in database. Please run comprehensive_odds_fetcher.py first.")
        return
    
    print(f"✅ Loaded {len(raw_data)} records")
    
    # Extract odds features
    print("🔧 Extracting odds features...")
    odds_df = ml_system.extract_odds_features(raw_data)
    print(f"✅ Processed {len(odds_df)} fixtures")
    
    # Create advanced features
    print("⚙️ Creating advanced features...")
    featured_df = ml_system.create_advanced_features(odds_df)
    
    # Filter completed matches for training
    completed_matches = featured_df[featured_df['actual_result'].notna()].copy()
    
    if len(completed_matches) < 10:
        print("❌ Not enough completed matches for training. Need at least 10 matches.")
        return
    
    print(f"✅ Found {len(completed_matches)} completed matches for training")
    
    # Train models
    results = ml_system.train_models(completed_matches)
    
    print("\n🎯 Training Complete!")
    print("=" * 50)
    
    # Save model summary
    summary = {
        'total_matches': len(completed_matches),
        'leagues_covered': completed_matches['league_name'].nunique(),
        'model_performance': {}
    }
    
    for pred_type, models in results.items():
        summary['model_performance'][pred_type] = {
            model_name: {
                'accuracy': float(model_info['cv_mean']),
                'std': float(model_info['cv_std'])
            }
            for model_name, model_info in models.items()
        }
    
    with open('ml_model_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("📁 Model summary saved to ml_model_summary.json")
    print("🎉 Ready for predictions!")

if __name__ == "__main__":
    main()
