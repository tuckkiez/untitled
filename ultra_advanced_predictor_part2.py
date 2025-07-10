#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ultra Advanced Predictor - Part 2: Training and Prediction Methods
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, log_loss
import warnings
warnings.filterwarnings('ignore')

class UltraAdvancedPredictorMethods:
    """Methods to be added to UltraAdvancedPredictor class"""
    
    def optimize_models(self, X_train, y_train):
        """ปรับแต่งพารามิเตอร์ของโมเดล"""
        print("🔧 กำลังปรับแต่งพารามิเตอร์โมเดล...")
        
        # Grid search parameters (simplified for speed)
        param_grids = {
            'rf': {
                'n_estimators': [200, 300],
                'max_depth': [12, 15],
                'min_samples_split': [5, 10]
            },
            'gb': {
                'n_estimators': [150, 200],
                'learning_rate': [0.1, 0.15],
                'max_depth': [6, 8]
            }
        }
        
        optimized_models = {}
        
        for model_name, model in self.models.items():
            if model_name in param_grids:
                print(f"   ปรับแต่ง {model_name}...")
                grid_search = GridSearchCV(
                    model, param_grids[model_name], 
                    cv=3, scoring='accuracy', n_jobs=-1
                )
                grid_search.fit(X_train, y_train)
                optimized_models[model_name] = grid_search.best_estimator_
                print(f"   {model_name} best score: {grid_search.best_score_:.3f}")
            else:
                optimized_models[model_name] = model
        
        self.models = optimized_models
    
    def train_ensemble_models(self, matches_df):
        """เทรนโมเดล Ensemble"""
        print("🤖 กำลังเทรนโมเดล Ultra Advanced Ensemble...")
        
        # สร้าง features
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
        
        # Feature selection
        X_selected = self.feature_selector.fit_transform(X_scaled, y)
        selected_features = self.feature_selector.get_support()
        self.selected_feature_names = [name for name, selected in 
                                     zip(self.feature_columns, selected_features) if selected]
        
        print(f"📊 Selected {len(self.selected_feature_names)} best features")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"📊 Training data: {X_train.shape}")
        
        # Optimize models (optional, can be slow)
        # self.optimize_models(X_train, y_train)
        
        # Train individual models
        model_scores = {}
        self.trained_models = {}
        
        for name, model in self.models.items():
            print(f"   เทรน {name}...")
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            
            # Train on full training set
            model.fit(X_train, y_train)
            
            # Test score
            test_score = model.score(X_test, y_test)
            
            model_scores[name] = {
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'test_score': test_score
            }
            
            self.trained_models[name] = model
            
            print(f"   {name}: CV={cv_scores.mean():.3f}±{cv_scores.std():.3f}, Test={test_score:.3f}")
        
        # Calculate ensemble weights based on performance
        self.ensemble_weights = self.calculate_ensemble_weights(model_scores)
        
        # Test ensemble
        ensemble_pred = self.predict_ensemble(X_test)
        ensemble_accuracy = accuracy_score(y_test, ensemble_pred)
        
        print(f"\n📊 ผลการเทรน:")
        for name, scores in model_scores.items():
            print(f"   {name:15}: {scores['test_score']:.3f}")
        print(f"   {'Ensemble':15}: {ensemble_accuracy:.3f}")
        
        # Classification report
        from sklearn.metrics import classification_report
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
        # ใช้ test score เป็นฐานในการคำนวณน้ำหนัก
        scores = [scores['test_score'] for scores in model_scores.values()]
        
        # Softmax transformation
        exp_scores = np.exp(np.array(scores) * 5)  # Scale up differences
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
        
        # Get predictions from all models
        predictions = {}
        probabilities = {}
        
        for name, model in self.trained_models.items():
            pred = model.predict(X)
            proba = model.predict_proba(X)
            
            predictions[name] = pred
            probabilities[name] = proba
        
        # Weighted ensemble of probabilities
        ensemble_proba = np.zeros_like(probabilities[list(probabilities.keys())[0]])
        
        for name, proba in probabilities.items():
            weight = self.ensemble_weights[name]
            ensemble_proba += weight * proba
        
        # Final prediction
        ensemble_pred = np.argmax(ensemble_proba, axis=1)
        
        return ensemble_pred
    
    def predict_match_ultra(self, home_team, away_team, match_date=None):
        """ทำนายการแข่งขันแบบ Ultra Advanced"""
        if not self.is_trained:
            print("❌ โมเดลยังไม่ได้เทรน!")
            return None
        
        if not match_date:
            match_date = datetime.now()
        
        # สร้าง dummy match สำหรับการทำนาย
        dummy_match = pd.DataFrame([{
            'date': match_date,
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': 0,  # dummy
            'away_goals': 0   # dummy
        }])
        
        # สร้าง features
        features_df = self.create_ultra_features(dummy_match)
        
        # Preprocessing
        X = self.imputer.transform(features_df)
        X_scaled = self.scaler.transform(X)
        X_selected = self.feature_selector.transform(X_scaled)
        
        # Get predictions from all models
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
        
        # Calculate prediction confidence adjustment
        # If models disagree significantly, reduce confidence
        pred_variance = np.var([np.argmax(proba) for proba in model_probabilities.values()])
        confidence_adjustment = max(0.7, 1.0 - pred_variance * 0.3)
        adjusted_confidence = ensemble_confidence * confidence_adjustment
        
        labels = ['Away Win', 'Draw', 'Home Win']
        
        result = {
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
        
        return result
    
    def analyze_feature_importance_ultra(self):
        """วิเคราะห์ความสำคัญของ Features แบบ Ultra"""
        if not self.is_trained:
            return None
        
        # รวม feature importance จากทุกโมเดล
        importance_dict = {}
        
        for name, model in self.trained_models.items():
            if hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_
                weight = self.ensemble_weights[name]
                
                for i, feature_name in enumerate(self.selected_feature_names):
                    if feature_name not in importance_dict:
                        importance_dict[feature_name] = 0
                    importance_dict[feature_name] += weight * importance[i]
        
        # สร้าง DataFrame
        feature_importance = pd.DataFrame([
            {'feature': feature, 'importance': importance}
            for feature, importance in importance_dict.items()
        ]).sort_values('importance', ascending=False)
        
        return feature_importance
    
    def load_premier_league_data(self, season=2024):
        """โหลดข้อมูล Premier League"""
        if not self.api_key:
            print("⚠️ ไม่มี API key, จะใช้ข้อมูลจำลอง")
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
        """สร้างข้อมูลจำลองที่สมจริงมากขึ้น"""
        print("🔄 สร้างข้อมูลจำลองแบบ Enhanced...")
        
        teams = [
            'Manchester City', 'Arsenal', 'Liverpool', 'Chelsea',
            'Manchester United', 'Tottenham', 'Newcastle', 'Brighton',
            'Aston Villa', 'West Ham', 'Crystal Palace', 'Fulham',
            'Brentford', 'Wolves', 'Everton', 'Nottingham Forest',
            'Leicester', 'Southampton', 'Ipswich', 'AFC Bournemouth'
        ]
        
        # Team strengths (more realistic)
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
        
        for i in range(600):  # สร้าง 600 เกม
            home_team = np.random.choice(teams)
            away_team = np.random.choice([t for t in teams if t != home_team])
            
            # คำนวณความน่าจะเป็นตามความแข็งแกร่ง
            home_strength = team_strengths[home_team] + 0.1  # home advantage
            away_strength = team_strengths[away_team]
            
            # สร้างผลการแข่งขันที่สมจริง
            total_strength = home_strength + away_strength
            home_expected = home_strength * 3.5 / total_strength
            away_expected = away_strength * 3.5 / total_strength
            
            home_goals = max(0, int(np.random.poisson(home_expected)))
            away_goals = max(0, int(np.random.poisson(away_expected)))
            
            matches.append({
                'date': start_date + timedelta(days=i//3),  # 3 matches per day average
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
    print("🚀 Ultra Advanced Football Predictor - Part 2")
    print("="*50)
    print("This file contains methods to be integrated with the main predictor class.")
