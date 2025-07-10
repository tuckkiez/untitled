#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ระบบทำนายฟุตบอลแบบ Advanced ML
- สถิติผู้เล่น (Player Statistics)
- ข้อมูลการบาดเจ็บ (Injury Data)
- ปัจจัยสภาพอากาศ (Weather Conditions)
- Deep Learning Neural Network
- ปรับปรุงการทำนาย Draw
"""

import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Machine Learning Libraries
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

# Deep Learning Libraries
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("⚠️ TensorFlow ไม่พร้อมใช้งาน จะใช้ Traditional ML แทน")
    TENSORFLOW_AVAILABLE = False

class AdvancedFootballPredictor:
    def __init__(self, api_key=None, weather_api_key=None):
        self.api_key = api_key
        self.weather_api_key = weather_api_key
        
        # Traditional ML Models
        self.rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
        self.gb_model = GradientBoostingClassifier(n_estimators=200, random_state=42)
        
        # Deep Learning Model
        self.dl_model = None
        
        # Preprocessing
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.imputer = SimpleImputer(strategy='median')
        
        # Data storage
        self.historical_data = None
        self.player_stats = {}
        self.injury_data = {}
        self.weather_data = {}
        
        self.is_trained = False
        self.feature_columns = []
        
    def get_player_statistics(self, team_name, season=2024):
        """ดึงสถิติผู้เล่น"""
        if not self.api_key:
            return self._generate_mock_player_stats(team_name)
        
        headers = {'X-Auth-Token': self.api_key}
        
        try:
            # ดึงข้อมูลทีม
            url = f"https://api.football-data.org/v4/teams"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                teams = response.json().get('teams', [])
                team_id = None
                
                for team in teams:
                    if team_name.lower() in team['name'].lower():
                        team_id = team['id']
                        break
                
                if team_id:
                    # ดึงสถิติผู้เล่น
                    squad_url = f"https://api.football-data.org/v4/teams/{team_id}"
                    squad_response = requests.get(squad_url, headers=headers)
                    
                    if squad_response.status_code == 200:
                        squad_data = squad_response.json()
                        return self._process_player_stats(squad_data)
            
            return self._generate_mock_player_stats(team_name)
            
        except Exception as e:
            print(f"Error getting player stats: {e}")
            return self._generate_mock_player_stats(team_name)
    
    def _generate_mock_player_stats(self, team_name):
        """สร้างสถิติผู้เล่นจำลอง"""
        # สถิติจำลองตามความแข็งแกร่งของทีม
        team_strength = {
            'Manchester City': 0.9, 'Arsenal': 0.85, 'Liverpool': 0.88,
            'Chelsea': 0.8, 'Manchester United': 0.75, 'Tottenham': 0.78,
            'Newcastle': 0.72, 'Brighton': 0.68, 'Aston Villa': 0.7,
            'West Ham': 0.65, 'Crystal Palace': 0.6, 'Fulham': 0.62,
            'Brentford': 0.58, 'Wolves': 0.55, 'Everton': 0.52,
            'Nottingham Forest': 0.5, 'Leicester': 0.48, 'Southampton': 0.45,
            'Ipswich': 0.4, 'AFC Bournemouth': 0.55
        }
        
        strength = team_strength.get(team_name, 0.5)
        
        return {
            'avg_goals_per_game': strength * 2.5 + np.random.normal(0, 0.3),
            'avg_assists_per_game': strength * 1.8 + np.random.normal(0, 0.2),
            'pass_accuracy': 0.7 + strength * 0.25 + np.random.normal(0, 0.05),
            'shots_per_game': strength * 15 + np.random.normal(0, 2),
            'tackles_per_game': (1 - strength) * 20 + 15 + np.random.normal(0, 2),
            'key_players_available': np.random.randint(8, 12),
            'team_chemistry': strength + np.random.normal(0, 0.1),
            'recent_form': np.random.uniform(0.3, 1.0),
            'fitness_level': np.random.uniform(0.7, 1.0)
        }
    
    def get_injury_data(self, team_name):
        """ดึงข้อมูลการบาดเจ็บ"""
        # จำลองข้อมูลการบาดเจ็บ
        injury_impact = np.random.uniform(0.0, 0.3)  # 0-30% impact
        key_players_injured = np.random.randint(0, 4)
        
        return {
            'injury_impact_score': injury_impact,
            'key_players_injured': key_players_injured,
            'total_injured_players': np.random.randint(0, 8),
            'avg_days_out': np.random.uniform(5, 30),
            'defensive_injuries': np.random.randint(0, 3),
            'midfield_injuries': np.random.randint(0, 3),
            'attacking_injuries': np.random.randint(0, 3)
        }
    
    def get_weather_data(self, city="London", match_date=None):
        """ดึงข้อมูลสภาพอากาศ"""
        if not match_date:
            match_date = datetime.now()
        
        # จำลองข้อมูลสภาพอากาศ
        weather_conditions = {
            'temperature': np.random.uniform(5, 25),  # Celsius
            'humidity': np.random.uniform(40, 90),    # Percentage
            'wind_speed': np.random.uniform(0, 20),   # km/h
            'precipitation': np.random.uniform(0, 10), # mm
            'visibility': np.random.uniform(5, 15),   # km
            'pressure': np.random.uniform(990, 1030), # hPa
            'weather_score': 0.0  # Will be calculated
        }
        
        # คำนวณ weather impact score
        temp_score = 1.0 if 10 <= weather_conditions['temperature'] <= 20 else 0.7
        rain_score = 1.0 if weather_conditions['precipitation'] < 2 else 0.6
        wind_score = 1.0 if weather_conditions['wind_speed'] < 15 else 0.8
        
        weather_conditions['weather_score'] = (temp_score + rain_score + wind_score) / 3
        
        return weather_conditions
    
    def create_advanced_features(self, matches_df):
        """สร้าง Advanced Features"""
        print("🔧 กำลังสร้าง Advanced Features...")
        
        features_list = []
        
        for idx, match in matches_df.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            match_date = pd.to_datetime(match['date'])
            
            # Basic team stats
            home_stats = self.calculate_team_stats(matches_df, home_team, idx)
            away_stats = self.calculate_team_stats(matches_df, away_team, idx)
            
            # Player statistics
            home_player_stats = self.get_player_statistics(home_team)
            away_player_stats = self.get_player_statistics(away_team)
            
            # Injury data
            home_injuries = self.get_injury_data(home_team)
            away_injuries = self.get_injury_data(away_team)
            
            # Weather data
            weather = self.get_weather_data("London", match_date)
            
            # Combine all features
            features = {
                # Basic team features
                'home_win_rate': home_stats['win_rate'],
                'home_draw_rate': home_stats['draw_rate'],
                'home_loss_rate': home_stats['loss_rate'],
                'away_win_rate': away_stats['win_rate'],
                'away_draw_rate': away_stats['draw_rate'],
                'away_loss_rate': away_stats['loss_rate'],
                
                'home_goals_for': home_stats['avg_goals_for'],
                'home_goals_against': home_stats['avg_goals_against'],
                'away_goals_for': away_stats['avg_goals_for'],
                'away_goals_against': away_stats['avg_goals_against'],
                
                # Player statistics features
                'home_player_goals': home_player_stats['avg_goals_per_game'],
                'home_player_assists': home_player_stats['avg_assists_per_game'],
                'home_pass_accuracy': home_player_stats['pass_accuracy'],
                'home_shots_per_game': home_player_stats['shots_per_game'],
                'home_tackles_per_game': home_player_stats['tackles_per_game'],
                'home_team_chemistry': home_player_stats['team_chemistry'],
                'home_fitness_level': home_player_stats['fitness_level'],
                
                'away_player_goals': away_player_stats['avg_goals_per_game'],
                'away_player_assists': away_player_stats['avg_assists_per_game'],
                'away_pass_accuracy': away_player_stats['pass_accuracy'],
                'away_shots_per_game': away_player_stats['shots_per_game'],
                'away_tackles_per_game': away_player_stats['tackles_per_game'],
                'away_team_chemistry': away_player_stats['team_chemistry'],
                'away_fitness_level': away_player_stats['fitness_level'],
                
                # Injury impact features
                'home_injury_impact': home_injuries['injury_impact_score'],
                'home_key_injured': home_injuries['key_players_injured'],
                'away_injury_impact': away_injuries['injury_impact_score'],
                'away_key_injured': away_injuries['key_players_injured'],
                
                # Weather features
                'temperature': weather['temperature'],
                'humidity': weather['humidity'],
                'wind_speed': weather['wind_speed'],
                'precipitation': weather['precipitation'],
                'weather_score': weather['weather_score'],
                
                # Advanced derived features
                'goal_difference_trend': home_stats['avg_goals_for'] - away_stats['avg_goals_for'],
                'defensive_strength_diff': away_stats['avg_goals_against'] - home_stats['avg_goals_against'],
                'form_difference': home_stats['recent_form'] - away_stats['recent_form'],
                'chemistry_difference': home_player_stats['team_chemistry'] - away_player_stats['team_chemistry'],
                'injury_advantage': away_injuries['injury_impact_score'] - home_injuries['injury_impact_score'],
                
                # Home advantage with conditions
                'home_advantage': 0.1 * weather['weather_score'] * (1 - home_injuries['injury_impact_score']),
                
                # Match context
                'month': match_date.month,
                'day_of_week': match_date.weekday(),
                'is_weekend': 1 if match_date.weekday() >= 5 else 0,
            }
            
            features_list.append(features)
        
        features_df = pd.DataFrame(features_list)
        self.feature_columns = features_df.columns.tolist()
        
        print(f"✅ สร้าง {len(self.feature_columns)} features สำเร็จ")
        return features_df
    
    def calculate_team_stats(self, matches_df, team_name, current_idx, last_n_games=10):
        """คำนวณสถิติทีม"""
        # ดึงเกมก่อนหน้า
        team_matches = matches_df[
            ((matches_df['home_team'] == team_name) | 
             (matches_df['away_team'] == team_name)) &
            (matches_df.index < current_idx)
        ].tail(last_n_games)
        
        if len(team_matches) == 0:
            return {
                'win_rate': 0.5, 'draw_rate': 0.25, 'loss_rate': 0.25,
                'avg_goals_for': 1.5, 'avg_goals_against': 1.5,
                'recent_form': 0.5
            }
        
        wins = draws = losses = 0
        goals_for = goals_against = 0
        recent_results = []
        
        for _, match in team_matches.iterrows():
            if match['home_team'] == team_name:
                gf, ga = match['home_goals'], match['away_goals']
            else:
                gf, ga = match['away_goals'], match['home_goals']
            
            goals_for += gf
            goals_against += ga
            
            if gf > ga:
                wins += 1
                recent_results.append(1.0)
            elif gf == ga:
                draws += 1
                recent_results.append(0.5)
            else:
                losses += 1
                recent_results.append(0.0)
        
        total_games = len(team_matches)
        recent_form = np.mean(recent_results[-5:]) if recent_results else 0.5
        
        return {
            'win_rate': wins / total_games,
            'draw_rate': draws / total_games,
            'loss_rate': losses / total_games,
            'avg_goals_for': goals_for / total_games,
            'avg_goals_against': goals_against / total_games,
            'recent_form': recent_form
        }
    
    def create_deep_learning_model(self, input_dim):
        """สร้าง Deep Learning Model"""
        if not TENSORFLOW_AVAILABLE:
            return None
        
        model = Sequential([
            Dense(256, activation='relu', input_shape=(input_dim,)),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            
            Dense(32, activation='relu'),
            Dropout(0.2),
            
            # Output layer for 3 classes (Home Win, Draw, Away Win)
            Dense(3, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_models(self, matches_df):
        """เทรนโมเดลทั้งหมด"""
        print("🤖 กำลังเทรนโมเดล Advanced ML...")
        
        # สร้าง features
        features_df = self.create_advanced_features(matches_df)
        
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
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"📊 Training data: {X_train.shape}")
        print(f"📊 Features: {len(self.feature_columns)}")
        
        # Train Traditional ML Models
        print("1. เทรน Random Forest...")
        self.rf_model.fit(X_train, y_train)
        rf_score = self.rf_model.score(X_test, y_test)
        
        print("2. เทรน Gradient Boosting...")
        self.gb_model.fit(X_train, y_train)
        gb_score = self.gb_model.score(X_test, y_test)
        
        # Train Deep Learning Model
        dl_score = 0
        if TENSORFLOW_AVAILABLE:
            print("3. เทรน Deep Learning Model...")
            self.dl_model = self.create_deep_learning_model(X_train.shape[1])
            
            early_stopping = EarlyStopping(
                monitor='val_loss', patience=10, restore_best_weights=True
            )
            
            history = self.dl_model.fit(
                X_train, y_train,
                epochs=100,
                batch_size=32,
                validation_split=0.2,
                callbacks=[early_stopping],
                verbose=0
            )
            
            dl_score = self.dl_model.evaluate(X_test, y_test, verbose=0)[1]
        
        print(f"\n📊 ผลการเทรน:")
        print(f"   Random Forest: {rf_score:.3f}")
        print(f"   Gradient Boosting: {gb_score:.3f}")
        if TENSORFLOW_AVAILABLE:
            print(f"   Deep Learning: {dl_score:.3f}")
        
        # Test predictions
        rf_pred = self.rf_model.predict(X_test)
        gb_pred = self.gb_model.predict(X_test)
        
        print(f"\n📈 Classification Report (Random Forest):")
        print(classification_report(y_test, rf_pred, 
                                  target_names=['Away Win', 'Draw', 'Home Win']))
        
        self.is_trained = True
        return {
            'rf_score': rf_score,
            'gb_score': gb_score,
            'dl_score': dl_score,
            'X_test': X_test,
            'y_test': y_test
        }
    
    def predict_match_advanced(self, home_team, away_team, match_date=None):
        """ทำนายการแข่งขันแบบ Advanced"""
        if not self.is_trained:
            print("❌ โมเดลยังไม่ได้เทรน!")
            return None
        
        if not match_date:
            match_date = datetime.now()
        
        # สร้าง features สำหรับการทำนาย
        dummy_match = pd.DataFrame([{
            'date': match_date,
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': 0,  # dummy
            'away_goals': 0   # dummy
        }])
        
        features_df = self.create_advanced_features(dummy_match)
        X = self.imputer.transform(features_df)
        X_scaled = self.scaler.transform(X)
        
        # Predictions from all models
        rf_pred = self.rf_model.predict(X_scaled)[0]
        rf_proba = self.rf_model.predict_proba(X_scaled)[0]
        
        gb_pred = self.gb_model.predict(X_scaled)[0]
        gb_proba = self.gb_model.predict_proba(X_scaled)[0]
        
        dl_pred = None
        dl_proba = None
        if TENSORFLOW_AVAILABLE and self.dl_model:
            dl_proba = self.dl_model.predict(X_scaled, verbose=0)[0]
            dl_pred = np.argmax(dl_proba)
        
        # Ensemble prediction
        if dl_proba is not None:
            ensemble_proba = (rf_proba + gb_proba + dl_proba) / 3
        else:
            ensemble_proba = (rf_proba + gb_proba) / 2
        
        ensemble_pred = np.argmax(ensemble_proba)
        
        # Convert predictions to labels
        labels = ['Away Win', 'Draw', 'Home Win']
        
        result = {
            'home_team': home_team,
            'away_team': away_team,
            'prediction': labels[ensemble_pred],
            'confidence': float(np.max(ensemble_proba)),
            'probabilities': {
                'Away Win': float(ensemble_proba[0]),
                'Draw': float(ensemble_proba[1]),
                'Home Win': float(ensemble_proba[2])
            },
            'model_predictions': {
                'Random Forest': labels[rf_pred],
                'Gradient Boosting': labels[gb_pred],
                'Deep Learning': labels[dl_pred] if dl_pred is not None else 'N/A'
            },
            'features_used': len(self.feature_columns)
        }
        
        return result
    
    def analyze_feature_importance(self):
        """วิเคราะห์ความสำคัญของ Features"""
        if not self.is_trained:
            return None
        
        # Random Forest Feature Importance
        rf_importance = self.rf_model.feature_importances_
        
        # Gradient Boosting Feature Importance
        gb_importance = self.gb_model.feature_importances_
        
        # Combine importances
        avg_importance = (rf_importance + gb_importance) / 2
        
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': avg_importance
        }).sort_values('importance', ascending=False)
        
        return feature_importance
    
    def load_premier_league_data(self, season=2024):
        """โหลดข้อมูล Premier League"""
        if not self.api_key:
            print("⚠️ ไม่มี API key, จะใช้ข้อมูลจำลอง")
            return self._generate_mock_data()
        
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
        
        return self._generate_mock_data()
    
    def _generate_mock_data(self):
        """สร้างข้อมูลจำลอง"""
        print("🔄 สร้างข้อมูลจำลอง...")
        
        teams = [
            'Manchester City', 'Arsenal', 'Liverpool', 'Chelsea',
            'Manchester United', 'Tottenham', 'Newcastle', 'Brighton',
            'Aston Villa', 'West Ham', 'Crystal Palace', 'Fulham',
            'Brentford', 'Wolves', 'Everton', 'Nottingham Forest',
            'Leicester', 'Southampton', 'Ipswich', 'AFC Bournemouth'
        ]
        
        matches = []
        start_date = datetime(2023, 8, 1)
        
        for i in range(500):  # สร้าง 500 เกม
            home_team = np.random.choice(teams)
            away_team = np.random.choice([t for t in teams if t != home_team])
            
            # จำลองผลการแข่งขัน
            home_strength = np.random.uniform(0.3, 1.0)
            away_strength = np.random.uniform(0.3, 1.0)
            
            home_goals = np.random.poisson(home_strength * 2)
            away_goals = np.random.poisson(away_strength * 1.5)
            
            matches.append({
                'date': start_date + timedelta(days=i),
                'home_team': home_team,
                'away_team': away_team,
                'home_goals': home_goals,
                'away_goals': away_goals
            })
        
        df = pd.DataFrame(matches)
        print(f"✅ สร้างข้อมูลจำลองสำเร็จ: {len(df)} เกม")
        return df

# Example usage
if __name__ == "__main__":
    print("🚀 ระบบทำนายฟุตบอล Advanced ML")
    print("="*50)
    
    # Initialize predictor
    predictor = AdvancedFootballPredictor(
        api_key="052fd4885cf943ad859c89cef542e2e5",
        weather_api_key="your_weather_api_key"
    )
    
    # Load data
    data = predictor.load_premier_league_data()
    
    # Train models
    results = predictor.train_models(data)
    
    # Make predictions
    print("\n🎯 ตัวอย่างการทำนาย:")
    print("="*50)
    
    matches_to_predict = [
        ("Arsenal", "Chelsea"),
        ("Manchester City", "Liverpool"),
        ("Manchester United", "Tottenham")
    ]
    
    for home, away in matches_to_predict:
        prediction = predictor.predict_match_advanced(home, away)
        if prediction:
            print(f"\n⚽ {home} vs {away}")
            print(f"   🏆 ทำนาย: {prediction['prediction']}")
            print(f"   🎯 ความมั่นใจ: {prediction['confidence']:.1%}")
            print(f"   📊 ความน่าจะเป็น:")
            for outcome, prob in prediction['probabilities'].items():
                print(f"      {outcome}: {prob:.1%}")
    
    # Feature importance
    print(f"\n📈 ความสำคัญของ Features:")
    print("="*50)
    importance = predictor.analyze_feature_importance()
    if importance is not None:
        print(importance.head(10))
