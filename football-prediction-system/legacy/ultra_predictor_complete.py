#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ultra Advanced Football Predictor - Complete Version
ระบบทำนายฟุตบอลที่แม่นยำที่สุด
- Ensemble of 5 ML models
- ELO rating system
- Advanced feature engineering
- Momentum and form analysis
- Head-to-head statistics
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, log_loss
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
        self.trained_models = {}
        self.ensemble_weights = {}
        
        self.is_trained = False
        self.feature_columns = []
        self.selected_feature_names = []
        
    def calculate_elo_ratings(self, matches_df):
        """คำนวณ ELO Rating สำหรับแต่ละทีม"""
        print("🏆 กำลังคำนวณ ELO Ratings...")
        
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
                home_result, away_result = 1.0, 0.0
            elif home_goals == away_goals:
                home_result, away_result = 0.5, 0.5
            else:
                home_result, away_result = 0.0, 1.0
            
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
        
        points = goals_for = goals_against = 0
        
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
        ].tail(10)
        
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
            else:
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
            scoring_trend = defensive_trend = 0.0
        
        return {
            'momentum': momentum,
            'scoring_trend': scoring_trend,
            'defensive_trend': defensive_trend
        }
    
    def create_ultra_features(self, matches_df):
        """สร้าง Ultra Advanced Features"""
        print("🔧 กำลังสร้าง Ultra Advanced Features...")
        
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
            season_progress = (match_date.month - 8) % 12 / 12
            
            # Advanced features
            features = {
                'home_elo': home_elo,
                'away_elo': away_elo,
                'elo_difference': home_elo - away_elo,
                'elo_ratio': home_elo / away_elo if away_elo > 0 else 1.0,
                
                'home_form_points': home_form['form_points'],
                'home_form_goals': home_form['form_goals'],
                'home_form_conceded': home_form['form_conceded'],
                'away_form_points': away_form['form_points'],
                'away_form_goals': away_form['form_goals'],
                'away_form_conceded': away_form['form_conceded'],
                
                'form_points_diff': home_form['form_points'] - away_form['form_points'],
                'form_attack_diff': home_form['form_goals'] - away_form['form_goals'],
                'form_defense_diff': away_form['form_conceded'] - home_form['form_conceded'],
                
                'h2h_home_advantage': h2h['h2h_home_wins'],
                'h2h_draw_tendency': h2h['h2h_draws'],
                'h2h_away_advantage': h2h['h2h_away_wins'],
                
                'home_momentum': home_momentum['momentum'],
                'away_momentum': away_momentum['momentum'],
                'momentum_difference': home_momentum['momentum'] - away_momentum['momentum'],
                'home_scoring_trend': home_momentum['scoring_trend'],
                'away_scoring_trend': away_momentum['scoring_trend'],
                'home_defensive_trend': home_momentum['defensive_trend'],
                'away_defensive_trend': away_momentum['defensive_trend'],
                
                'days_since_epoch': days_since_epoch,
                'season_progress': season_progress,
                'is_early_season': 1 if season_progress < 0.3 else 0,
                'is_mid_season': 1 if 0.3 <= season_progress < 0.7 else 0,
                'is_late_season': 1 if season_progress >= 0.7 else 0,
                
                'month': match_date.month,
                'day_of_week': match_date.weekday(),
                'is_weekend': 1 if match_date.weekday() >= 5 else 0,
                'is_midweek': 1 if match_date.weekday() in [1, 2, 3] else 0,
                
                'overall_strength_home': (home_elo / 1500) * home_momentum['momentum'],
                'overall_strength_away': (away_elo / 1500) * away_momentum['momentum'],
                'strength_ratio': ((home_elo / 1500) * home_momentum['momentum']) / 
                                ((away_elo / 1500) * away_momentum['momentum']) if away_momentum['momentum'] > 0 else 1.0,
                
                'adjusted_home_advantage': 0.1 * (home_form['form_points'] / 3.0),
                'attack_vs_defense': home_form['form_goals'] - away_form['form_conceded'],
                'defense_vs_attack': home_form['form_conceded'] - away_form['form_goals'],
            }
            
            features_list.append(features)
        
        features_df = pd.DataFrame(features_list)
        self.feature_columns = features_df.columns.tolist()
        
        print(f"✅ สร้าง {len(self.feature_columns)} Ultra Features สำเร็จ")
        return features_df
    
    def train_ensemble_models(self, matches_df):
        """เทรนโมเดล Ensemble"""
        print("🤖 กำลังเทรนโมเดล Ultra Advanced Ensemble...")
        
        features_df = self.create_ultra_features(matches_df)
        
        # สร้าง target labels
        y = []
        for _, match in matches_df.iterrows():
            home_goals = match['home_goals']
            away_goals = match['away_goals']
            
            if home_goals > away_goals:
                y.append(2)  # Home Win
            elif home_goals == away_goals:
                y.append(1)  # Draw
            else:
                y.append(0)  # Away Win
        
        y = np.array(y)
        
        # Preprocessing
        X = self.imputer.fit_transform(features_df)
        X_scaled = self.scaler.fit_transform(X)
        X_selected = self.feature_selector.fit_transform(X_scaled, y)
        
        selected_features = self.feature_selector.get_support()
        self.selected_feature_names = [name for name, selected in 
                                     zip(self.feature_columns, selected_features) if selected]
        
        print(f"📊 Selected {len(self.selected_feature_names)} best features")
        
        # Split data with stratification
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"📊 Training data: {X_train.shape}")
        
        # Train individual models
        model_scores = {}
        self.trained_models = {}
        
        for name, model in self.models.items():
            print(f"   เทรน {name}...")
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            
            # Train on full training set
            model.fit(X_train, y_train)
            test_score = model.score(X_test, y_test)
            
            model_scores[name] = {
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'test_score': test_score
            }
            
            self.trained_models[name] = model
            print(f"   {name}: CV={cv_scores.mean():.3f}±{cv_scores.std():.3f}, Test={test_score:.3f}")
        
        # Calculate ensemble weights
        self.ensemble_weights = self.calculate_ensemble_weights(model_scores)
        
        # Test ensemble
        ensemble_pred = self.predict_ensemble(X_test)
        ensemble_accuracy = accuracy_score(y_test, ensemble_pred)
        
        print(f"\n📊 ผลการเทรน:")
        for name, scores in model_scores.items():
            print(f"   {name:15}: {scores['test_score']:.3f}")
        print(f"   {'Ensemble':15}: {ensemble_accuracy:.3f}")
        
        print(f"\n📈 Classification Report (Ensemble):")
        print(classification_report(y_test, ensemble_pred, 
                                  target_names=['Away Win', 'Draw', 'Home Win']))
        
        self.is_trained = True
        return {
            'model_scores': model_scores,
            'ensemble_accuracy': ensemble_accuracy,
            'X_test': X_test,
            'y_test': y_test
        }
    
    def calculate_ensemble_weights(self, model_scores):
        """คำนวณน้ำหนักสำหรับ ensemble"""
        scores = [scores['test_score'] for scores in model_scores.values()]
        exp_scores = np.exp(np.array(scores) * 5)
        weights = exp_scores / np.sum(exp_scores)
        
        weight_dict = {}
        for i, name in enumerate(model_scores.keys()):
            weight_dict[name] = weights[i]
        
        print(f"🎯 Ensemble weights: {weight_dict}")
        return weight_dict
    
    def predict_ensemble(self, X):
        """ทำนายด้วย Ensemble"""
        if not self.is_trained:
            raise ValueError("Models not trained yet!")
        
        ensemble_proba = np.zeros((X.shape[0], 3))
        
        for name, model in self.trained_models.items():
            proba = model.predict_proba(X)
            weight = self.ensemble_weights[name]
            ensemble_proba += weight * proba
        
        return np.argmax(ensemble_proba, axis=1)
    
    def predict_match_ultra(self, home_team, away_team, match_date=None):
        """ทำนายการแข่งขันแบบ Ultra Advanced"""
        if not self.is_trained:
            print("❌ โมเดลยังไม่ได้เทรน!")
            return None
        
        if not match_date:
            match_date = datetime.now()
        
        # สร้าง dummy match
        dummy_match = pd.DataFrame([{
            'date': match_date,
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': 0,
            'away_goals': 0
        }])
        
        # สร้าง features
        features_df = self.create_ultra_features(dummy_match)
        
        # Preprocessing
        X = self.imputer.transform(features_df)
        X_scaled = self.scaler.transform(X)
        X_selected = self.feature_selector.transform(X_scaled)
        
        # Get predictions
        model_predictions = {}
        model_probabilities = {}
        
        for name, model in self.trained_models.items():
            pred = model.predict(X_selected)[0]
            proba = model.predict_proba(X_selected)[0]
            
            model_predictions[name] = ['Away Win', 'Draw', 'Home Win'][pred]
            model_probabilities[name] = proba
        
        # Ensemble prediction
        ensemble_proba = np.zeros(3)
        for name, proba in model_probabilities.items():
            weight = self.ensemble_weights[name]
            ensemble_proba += weight * proba
        
        ensemble_pred = np.argmax(ensemble_proba)
        ensemble_confidence = np.max(ensemble_proba)
        
        # Confidence adjustment based on model agreement
        pred_variance = np.var([np.argmax(proba) for proba in model_probabilities.values()])
        confidence_adjustment = max(0.7, 1.0 - pred_variance * 0.3)
        adjusted_confidence = ensemble_confidence * confidence_adjustment
        
        labels = ['Away Win', 'Draw', 'Home Win']
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'prediction': labels[ensemble_pred],
            'confidence': float(adjusted_confidence),
            'raw_confidence': float(ensemble_confidence),
            'probabilities': {
                'Away Win': float(ensemble_proba[0]),
                'Draw': float(ensemble_proba[1]),
                'Home Win': float(ensemble_proba[2])
            },
            'model_predictions': model_predictions,
            'model_agreement': 1.0 - pred_variance,
            'features_used': len(self.selected_feature_names),
            'ensemble_weights': self.ensemble_weights
        }
    
    def load_premier_league_data(self, season=2024):
        """โหลดข้อมูล Premier League"""
        if not self.api_key:
            return self._generate_enhanced_mock_data()
        
        headers = {'X-Auth-Token': self.api_key}
        
        try:
            url = "https://api.football-data.org/v4/competitions/PL/matches"
            params = {'season': season, 'status': 'FINISHED'}
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                matches = []
                
                for match in data.get('matches', []):
                    if match['status'] == 'FINISHED' and match['score']['fullTime']['home'] is not None:
                        matches.append({
                            'date': match['utcDate'][:10],
                            'home_team': match['homeTeam']['name'],
                            'away_team': match['awayTeam']['name'],
                            'home_goals': match['score']['fullTime']['home'],
                            'away_goals': match['score']['fullTime']['away']
                        })
                
                df = pd.DataFrame(matches)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                
                print(f"✅ โหลดข้อมูลจริงสำเร็จ: {len(df)} เกม")
                return df
            
        except Exception as e:
            print(f"Error loading data: {e}")
        
        return self._generate_enhanced_mock_data()
    
    def _generate_enhanced_mock_data(self):
        """สร้างข้อมูลจำลองที่สมจริง"""
        print("🔄 สร้างข้อมูลจำลองแบบ Enhanced...")
        
        teams = [
            'Manchester City', 'Arsenal', 'Liverpool', 'Chelsea',
            'Manchester United', 'Tottenham', 'Newcastle', 'Brighton',
            'Aston Villa', 'West Ham', 'Crystal Palace', 'Fulham',
            'Brentford', 'Wolves', 'Everton', 'Nottingham Forest',
            'Leicester', 'Southampton', 'Ipswich', 'AFC Bournemouth'
        ]
        
        team_strengths = {
            'Manchester City': 0.95, 'Arsenal': 0.88, 'Liverpool': 0.90,
            'Chelsea': 0.82, 'Manchester United': 0.78, 'Tottenham': 0.80,
            'Newcastle': 0.75, 'Brighton': 0.70, 'Aston Villa': 0.73,
            'West Ham': 0.68, 'Crystal Palace': 0.62, 'Fulham': 0.65,
            'Brentford': 0.60, 'Wolves': 0.58, 'Everton': 0.55,
            'Nottingham Forest': 0.52, 'Leicester': 0.50, 'Southampton': 0.48,
            'Ipswich': 0.42, 'AFC Bournemouth': 0.57
        }
        
        matches = []
        start_date = datetime(2023, 8, 1)
        
        for i in range(600):
            home_team = np.random.choice(teams)
            away_team = np.random.choice([t for t in teams if t != home_team])
            
            home_strength = team_strengths[home_team] + 0.1
            away_strength = team_strengths[away_team]
            
            total_strength = home_strength + away_strength
            home_expected = home_strength * 3.5 / total_strength
            away_expected = away_strength * 3.5 / total_strength
            
            home_goals = max(0, int(np.random.poisson(home_expected)))
            away_goals = max(0, int(np.random.poisson(away_expected)))
            
            matches.append({
                'date': start_date + timedelta(days=i//3),
                'home_team': home_team,
                'away_team': away_team,
                'home_goals': home_goals,
                'away_goals': away_goals
            })
        
        df = pd.DataFrame(matches)
        df = df.sort_values('date').reset_index(drop=True)
        print(f"✅ สร้างข้อมูลจำลองสำเร็จ: {len(df)} เกม")
        return df

# Example usage
if __name__ == "__main__":
    print("🚀 Ultra Advanced Football Predictor")
    print("="*50)
    
    predictor = UltraAdvancedPredictor(api_key="052fd4885cf943ad859c89cef542e2e5")
    
    # Load data
    data = predictor.load_premier_league_data()
    
    # Train models
    results = predictor.train_ensemble_models(data)
    
    # Make predictions
    print("\n🎯 ตัวอย่างการทำนาย Ultra Advanced:")
    print("="*50)
    
    matches_to_predict = [
        ("Arsenal", "Chelsea"),
        ("Manchester City", "Liverpool"),
        ("Manchester United", "Tottenham")
    ]
    
    for home, away in matches_to_predict:
        prediction = predictor.predict_match_ultra(home, away)
        if prediction:
            print(f"\n⚽ {home} vs {away}")
            print(f"   🏆 ทำนาย: {prediction['prediction']}")
            print(f"   🎯 ความมั่นใจ: {prediction['confidence']:.1%}")
            print(f"   🤝 ความเห็นตรงกันของโมเดล: {prediction['model_agreement']:.1%}")
            print(f"   📊 ความน่าจะเป็น:")
            for outcome, prob in prediction['probabilities'].items():
                print(f"      {outcome}: {prob:.1%}")
    
    print(f"\n✅ Ultra Advanced Predictor พร้อมใช้งาน!")
