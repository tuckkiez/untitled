#!/usr/bin/env python3
"""
🇪🇸 La Liga Advanced Predictor
ระบบทำนายผลฟุตบอลลีกสเปน (แยกต่างหากจาก Premier League)
ใช้โครงสร้างเดียวกับ Ultra Advanced Predictor
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import RobustScaler
from sklearn.impute import KNNImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

class LaLigaPredictor:
    def __init__(self, api_key=None):
        self.api_key = api_key
        
        # ML Models (เดียวกับ Ultra Advanced)
        self.models = {
            'rf': RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1),
            'gb': GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, max_depth=6, random_state=42),
            'et': ExtraTreesClassifier(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1),
            'lr': LogisticRegression(C=1.0, max_iter=1000, random_state=42),
            'svm': SVC(C=1.0, kernel='rbf', probability=True, random_state=42)
        }
        
        # Preprocessing
        self.scaler = RobustScaler()
        self.imputer = KNNImputer(n_neighbors=5)
        self.feature_selector = SelectKBest(f_classif, k=30)
        
        # Storage
        self.trained_models = {}
        self.ensemble_weights = {}
        self.team_ratings = {}
        
        self.is_trained = False
        self.feature_columns = []
        self.selected_feature_names = []
        
    def load_laliga_data(self, season=2024):
        """โหลดข้อมูล La Liga จาก API หรือสร้างจำลอง"""
        print("🇪🇸 กำลังโหลดข้อมูล La Liga...")
        
        if not self.api_key:
            return self._generate_laliga_mock_data()
        
        try:
            # ลองใช้ Football-data.org API
            url = "https://api.football-data.org/v4/competitions/PD/matches"
            headers = {'X-Auth-Token': self.api_key}
            params = {'season': season, 'status': 'FINISHED'}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data_json = response.json()
                matches = []
                
                for match in data_json.get('matches', []):
                    if match['status'] == 'FINISHED' and match['score']['fullTime']['home'] is not None:
                        matches.append({
                            'date': match['utcDate'][:10],
                            'home_team': match['homeTeam']['name'],
                            'away_team': match['awayTeam']['name'],
                            'home_goals': match['score']['fullTime']['home'],
                            'away_goals': match['score']['fullTime']['away']
                        })
                
                data = pd.DataFrame(matches)
                data['date'] = pd.to_datetime(data['date'])
                data = data.sort_values('date').reset_index(drop=True)
                
                print(f"✅ โหลดข้อมูล La Liga จริงสำเร็จ: {len(data)} เกม")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                data = self._generate_laliga_mock_data()
                
        except Exception as e:
            print(f"❌ Error loading La Liga data: {e}")
            data = self._generate_laliga_mock_data()
        
        self.historical_data = data
        return data
    
    def _generate_laliga_mock_data(self):
        """สร้างข้อมูลจำลอง La Liga (ใกล้เคียงความจริง)"""
        print("🔄 สร้างข้อมูลจำลอง La Liga...")
        
        # ทีมใน La Liga 2024-25
        teams = [
            'Real Madrid', 'FC Barcelona', 'Atletico Madrid', 'Athletic Bilbao',
            'Real Sociedad', 'Real Betis', 'Villarreal CF', 'Valencia CF',
            'Sevilla FC', 'RC Celta', 'CA Osasuna', 'Getafe CF',
            'UD Las Palmas', 'Girona FC', 'Rayo Vallecano', 'RCD Espanyol',
            'Deportivo Alaves', 'Real Valladolid', 'CD Leganes', 'RCD Mallorca'
        ]
        
        matches = []
        
        # สร้างข้อมูลจำลอง 380 เกม (19 ทีม x 2 รอบ)
        for i in range(380):
            home_team = np.random.choice(teams)
            away_team = np.random.choice([t for t in teams if t != home_team])
            
            # ความแข็งแกร่งของทีม (จำลองจากความจริง)
            home_strength = self._get_team_strength(home_team)
            away_strength = self._get_team_strength(away_team)
            
            # Home advantage
            home_strength += 0.3
            
            # คำนวณประตู
            home_goals = max(0, int(np.random.poisson(home_strength)))
            away_goals = max(0, int(np.random.poisson(away_strength)))
            
            # สร้างวันที่ (ย้อนหลัง 120 วัน)
            days_ago = np.random.randint(1, 120)
            match_date = datetime.now() - timedelta(days=days_ago)
            
            matches.append({
                'date': match_date.strftime('%Y-%m-%d'),
                'home_team': home_team,
                'away_team': away_team,
                'home_goals': home_goals,
                'away_goals': away_goals
            })
        
        data = pd.DataFrame(matches)
        data['date'] = pd.to_datetime(data['date'])
        data = data.sort_values('date').reset_index(drop=True)
        
        print(f"✅ สร้างข้อมูลจำลอง La Liga สำเร็จ: {len(data)} เกม")
        return data
    
    def _get_team_strength(self, team):
        """กำหนดความแข็งแกร่งของทีม La Liga (จำลองจากความจริง)"""
        strength_map = {
            'Real Madrid': 2.3, 'FC Barcelona': 2.2, 'Atletico Madrid': 1.9,
            'Athletic Bilbao': 1.6, 'Real Sociedad': 1.5, 'Real Betis': 1.4,
            'Villarreal CF': 1.4, 'Valencia CF': 1.2, 'Sevilla FC': 1.3,
            'RC Celta': 1.1, 'CA Osasuna': 1.0, 'Getafe CF': 0.9,
            'UD Las Palmas': 0.9, 'Girona FC': 1.2, 'Rayo Vallecano': 1.0,
            'RCD Espanyol': 0.8, 'Deportivo Alaves': 0.8, 'Real Valladolid': 0.7,
            'CD Leganes': 0.7, 'RCD Mallorca': 0.9
        }
        return strength_map.get(team, 1.0)
    
    def calculate_elo_ratings(self, matches_df):
        """คำนวณ ELO Rating สำหรับทีม La Liga"""
        print("🏆 กำลังคำนวณ ELO Ratings สำหรับ La Liga...")
        
        teams = set(matches_df['home_team'].unique()) | set(matches_df['away_team'].unique())
        elo_ratings = {team: 1500 for team in teams}
        
        K = 32  # K-factor เดียวกับระบบเดิม
        
        for _, match in matches_df.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            home_goals = match['home_goals']
            away_goals = match['away_goals']
            
            if home_goals > away_goals:
                home_result, away_result = 1.0, 0.0
            elif home_goals == away_goals:
                home_result, away_result = 0.5, 0.5
            else:
                home_result, away_result = 0.0, 1.0
            
            home_expected = 1 / (1 + 10**((elo_ratings[away_team] - elo_ratings[home_team]) / 400))
            away_expected = 1 - home_expected
            
            elo_ratings[home_team] += K * (home_result - home_expected)
            elo_ratings[away_team] += K * (away_result - away_expected)
        
        self.team_ratings = elo_ratings
        return elo_ratings
