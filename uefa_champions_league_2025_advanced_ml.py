#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 UEFA CHAMPIONS LEAGUE 2025-2026 ADVANCED ML ANALYSIS
ระบบวิเคราะห์แชมเปี้ยนส์ลีกด้วย Machine Learning ขั้นสูง
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import requests
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

class UEFAChampionsLeagueAdvancedML:
    def __init__(self):
        self.analysis_date = datetime.now().strftime("%Y-%m-%d")
        self.season = "2025-2026"
        self.competition = "UEFA Champions League"
        
        # Advanced ML Models
        self.models = {
            'match_result': RandomForestClassifier(n_estimators=200, random_state=42),
            'over_under': GradientBoostingClassifier(n_estimators=150, random_state=42),
            'both_teams_score': RandomForestClassifier(n_estimators=180, random_state=42),
            'corners': GradientBoostingClassifier(n_estimators=120, random_state=42)
        }
        
        self.scaler = StandardScaler()
        
        # Champions League specific factors
        self.ucl_factors = {
            'home_advantage': 0.15,  # ลดลงใน UCL
            'experience_weight': 0.25,  # ประสบการณ์ UCL สำคัญ
            'form_weight': 0.20,
            'head_to_head_weight': 0.15,
            'squad_depth_weight': 0.25  # ความลึกของทีมสำคัญใน UCL
        }
        
    def get_ucl_teams_data(self):
        """ข้อมูลทีมที่เข้าร่วม UEFA Champions League 2025-26"""
        ucl_teams = {
            # Pot 1 - Champions + Top Coefficient
            "pot_1": [
                {"name": "Real Madrid", "country": "Spain", "coefficient": 136.0, "ucl_titles": 15},
                {"name": "Manchester City", "country": "England", "coefficient": 125.0, "ucl_titles": 1},
                {"name": "Bayern Munich", "country": "Germany", "coefficient": 122.0, "ucl_titles": 6},
                {"name": "Paris Saint-Germain", "country": "France", "coefficient": 118.0, "ucl_titles": 0},
                {"name": "Liverpool", "country": "England", "coefficient": 115.0, "ucl_titles": 6},
                {"name": "Inter Milan", "country": "Italy", "coefficient": 112.0, "ucl_titles": 3},
                {"name": "Borussia Dortmund", "country": "Germany", "coefficient": 110.0, "ucl_titles": 1},
                {"name": "RB Leipzig", "country": "Germany", "coefficient": 108.0, "ucl_titles": 0}
            ],
            # Pot 2 - Strong European Teams
            "pot_2": [
                {"name": "Arsenal", "country": "England", "coefficient": 105.0, "ucl_titles": 0},
                {"name": "Atletico Madrid", "country": "Spain", "coefficient": 102.0, "ucl_titles": 0},
                {"name": "Atalanta", "country": "Italy", "coefficient": 98.0, "ucl_titles": 0},
                {"name": "Juventus", "country": "Italy", "coefficient": 95.0, "ucl_titles": 2},
                {"name": "Benfica", "country": "Portugal", "coefficient": 92.0, "ucl_titles": 2},
                {"name": "AC Milan", "country": "Italy", "coefficient": 90.0, "ucl_titles": 7},
                {"name": "Barcelona", "country": "Spain", "coefficient": 88.0, "ucl_titles": 5},
                {"name": "Bayer Leverkusen", "country": "Germany", "coefficient": 85.0, "ucl_titles": 0}
            ],
            # Pot 3 - Emerging Powers
            "pot_3": [
                {"name": "Feyenoord", "country": "Netherlands", "coefficient": 82.0, "ucl_titles": 1},
                {"name": "Sporting CP", "country": "Portugal", "coefficient": 80.0, "ucl_titles": 0},
                {"name": "PSV Eindhoven", "country": "Netherlands", "coefficient": 78.0, "ucl_titles": 1},
                {"name": "Dinamo Zagreb", "country": "Croatia", "coefficient": 75.0, "ucl_titles": 0},
                {"name": "Red Bull Salzburg", "country": "Austria", "coefficient": 72.0, "ucl_titles": 0},
                {"name": "Lille", "country": "France", "coefficient": 70.0, "ucl_titles": 0},
                {"name": "Celtic", "country": "Scotland", "coefficient": 68.0, "ucl_titles": 1},
                {"name": "Club Brugge", "country": "Belgium", "coefficient": 65.0, "ucl_titles": 0}
            ],
            # Pot 4 - Qualifiers & Smaller Nations
            "pot_4": [
                {"name": "Monaco", "country": "France", "coefficient": 62.0, "ucl_titles": 0},
                {"name": "Aston Villa", "country": "England", "coefficient": 60.0, "ucl_titles": 1},
                {"name": "Bologna", "country": "Italy", "coefficient": 58.0, "ucl_titles": 0},
                {"name": "Girona", "country": "Spain", "coefficient": 55.0, "ucl_titles": 0},
                {"name": "Stuttgart", "country": "Germany", "coefficient": 52.0, "ucl_titles": 0},
                {"name": "Sturm Graz", "country": "Austria", "coefficient": 50.0, "ucl_titles": 0},
                {"name": "Brest", "country": "France", "coefficient": 48.0, "ucl_titles": 0},
                {"name": "Slovan Bratislava", "country": "Slovakia", "coefficient": 45.0, "ucl_titles": 0}
            ]
        }
        
        return ucl_teams
    
    def generate_ucl_fixtures(self):
        """สร้างการแข่งขันจำลองสำหรับ UCL 2025-26"""
        teams_data = self.get_ucl_teams_data()
        all_teams = []
        
        for pot in teams_data.values():
            all_teams.extend(pot)
        
        # สร้างการแข่งขันแบบ League Phase (36 teams, 8 matches each)
        fixtures = []
        today = datetime.now()
        
        # สร้างการแข่งขัน 8 นัดสำหรับแต่ละทีม
        for i, team in enumerate(all_teams[:16]):  # วิเคราะห์ 16 ทีมแรก
            # สร้าง 4 นัดในช่วงนี้
            for match_day in range(1, 5):
                opponent_idx = (i + match_day * 3) % len(all_teams)
                if opponent_idx != i:
                    opponent = all_teams[opponent_idx]
                    
                    match_date = today + timedelta(days=match_day * 14)  # ทุก 2 สัปดาห์
                    
                    fixture = {
                        'match_id': f"UCL_{i}_{match_day}",
                        'date': match_date.strftime("%Y-%m-%d"),
                        'time': "21:00",
                        'home_team': team['name'],
                        'away_team': opponent['name'],
                        'home_coefficient': team['coefficient'],
                        'away_coefficient': opponent['coefficient'],
                        'home_ucl_titles': team['ucl_titles'],
                        'away_ucl_titles': opponent['ucl_titles'],
                        'home_country': team['country'],
                        'away_country': opponent['country'],
                        'matchday': match_day,
                        'competition_phase': 'League Phase'
                    }
                    
                    fixtures.append(fixture)
        
        return fixtures[:20]  # Return 20 matches for analysis
    
    def calculate_team_strength(self, team_data, opponent_data):
        """คำนวณความแข็งแกร่งของทีมใน UCL"""
        
        # Base strength from coefficient
        team_strength = team_data['coefficient'] / 10
        opponent_strength = opponent_data['coefficient'] / 10
        
        # UCL Experience Factor
        ucl_experience_team = min(team_data['ucl_titles'] * 2, 10)
        ucl_experience_opponent = min(opponent_data['ucl_titles'] * 2, 10)
        
        # Country League Strength
        league_strength = {
            'England': 1.2, 'Spain': 1.15, 'Germany': 1.1, 'Italy': 1.05,
            'France': 1.0, 'Portugal': 0.95, 'Netherlands': 0.9, 'Austria': 0.85,
            'Belgium': 0.8, 'Scotland': 0.75, 'Croatia': 0.7, 'Slovakia': 0.65
        }
        
        team_league_bonus = league_strength.get(team_data['country'], 0.7)
        opponent_league_bonus = league_strength.get(opponent_data['country'], 0.7)
        
        # Final Strength Calculation
        final_team_strength = (
            team_strength * 0.5 +
            ucl_experience_team * 0.3 +
            team_league_bonus * 5 * 0.2
        )
        
        final_opponent_strength = (
            opponent_strength * 0.5 +
            ucl_experience_opponent * 0.3 +
            opponent_league_bonus * 5 * 0.2
        )
        
        return final_team_strength, final_opponent_strength
    
    def generate_training_data(self):
        """สร้างข้อมูลฝึกสอนจากประวัติศาสตร์ UCL"""
        
        # Historical UCL data simulation
        np.random.seed(42)
        n_samples = 1000
        
        training_data = []
        
        for i in range(n_samples):
            # Team strengths
            home_coeff = np.random.uniform(45, 140)
            away_coeff = np.random.uniform(45, 140)
            
            home_titles = np.random.choice([0, 1, 2, 3, 5, 6, 7, 15], p=[0.4, 0.2, 0.15, 0.1, 0.05, 0.04, 0.03, 0.03])
            away_titles = np.random.choice([0, 1, 2, 3, 5, 6, 7, 15], p=[0.4, 0.2, 0.15, 0.1, 0.05, 0.04, 0.03, 0.03])
            
            # Features
            coeff_diff = home_coeff - away_coeff
            titles_diff = home_titles - away_titles
            home_advantage = 1
            
            # Outcomes based on realistic UCL patterns
            win_prob = 0.4 + (coeff_diff / 200) + (titles_diff / 20) + 0.1  # Home advantage
            win_prob = max(0.1, min(0.8, win_prob))
            
            if np.random.random() < win_prob:
                result = 1  # Home win
                goals_home = np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1])
                goals_away = np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1])
            elif np.random.random() < 0.3:
                result = 0  # Draw
                goals_home = np.random.choice([0, 1, 2], p=[0.2, 0.6, 0.2])
                goals_away = goals_home
            else:
                result = 2  # Away win
                goals_away = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
                goals_home = np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1])
            
            total_goals = goals_home + goals_away
            over_25 = 1 if total_goals > 2.5 else 0
            bts = 1 if goals_home > 0 and goals_away > 0 else 0
            
            # Corner simulation
            corners_home = max(2, int(np.random.normal(6 + coeff_diff/20, 2)))
            corners_away = max(2, int(np.random.normal(6 - coeff_diff/20, 2)))
            total_corners = corners_home + corners_away
            
            training_data.append({
                'home_coefficient': home_coeff,
                'away_coefficient': away_coeff,
                'coefficient_diff': coeff_diff,
                'home_titles': home_titles,
                'away_titles': away_titles,
                'titles_diff': titles_diff,
                'home_advantage': home_advantage,
                'result': result,
                'over_25': over_25,
                'bts': bts,
                'total_corners': total_corners,
                'corners_over_10': 1 if total_corners > 10 else 0
            })
        
        return pd.DataFrame(training_data)
    
    def train_models(self):
        """ฝึกสอนโมเดล ML"""
        print("🤖 Training Advanced ML Models for UEFA Champions League...")
        
        # Generate training data
        df = self.generate_training_data()
        
        # Features
        feature_columns = ['home_coefficient', 'away_coefficient', 'coefficient_diff', 
                          'home_titles', 'away_titles', 'titles_diff', 'home_advantage']
        X = df[feature_columns]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train models
        model_scores = {}
        
        # Match Result Model
        y_result = df['result']
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_result, test_size=0.2, random_state=42)
        self.models['match_result'].fit(X_train, y_train)
        result_score = accuracy_score(y_test, self.models['match_result'].predict(X_test))
        model_scores['match_result'] = result_score
        
        # Over/Under Model
        y_over = df['over_25']
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_over, test_size=0.2, random_state=42)
        self.models['over_under'].fit(X_train, y_train)
        over_score = accuracy_score(y_test, self.models['over_under'].predict(X_test))
        model_scores['over_under'] = over_score
        
        # Both Teams Score Model
        y_bts = df['bts']
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_bts, test_size=0.2, random_state=42)
        self.models['both_teams_score'].fit(X_train, y_train)
        bts_score = accuracy_score(y_test, self.models['both_teams_score'].predict(X_test))
        model_scores['both_teams_score'] = bts_score
        
        # Corners Model
        y_corners = df['corners_over_10']
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_corners, test_size=0.2, random_state=42)
        self.models['corners'].fit(X_train, y_train)
        corners_score = accuracy_score(y_test, self.models['corners'].predict(X_test))
        model_scores['corners'] = corners_score
        
        print("✅ Model Training Complete!")
        return model_scores
    
    def predict_match(self, fixture):
        """ทำนายผลการแข่งขัน"""
        
        # Prepare features
        features = np.array([[
            fixture['home_coefficient'],
            fixture['away_coefficient'],
            fixture['home_coefficient'] - fixture['away_coefficient'],
            fixture['home_ucl_titles'],
            fixture['away_ucl_titles'],
            fixture['home_ucl_titles'] - fixture['away_ucl_titles'],
            1  # home_advantage
        ]])
        
        features_scaled = self.scaler.transform(features)
        
        # Predictions
        result_probs = self.models['match_result'].predict_proba(features_scaled)[0]
        over_prob = self.models['over_under'].predict_proba(features_scaled)[0][1]
        bts_prob = self.models['both_teams_score'].predict_proba(features_scaled)[0][1]
        corners_over_prob = self.models['corners'].predict_proba(features_scaled)[0][1]
        
        # Map result probabilities
        if len(result_probs) == 3:
            home_win_prob, draw_prob, away_win_prob = result_probs
        else:
            # Handle binary classification
            home_win_prob = result_probs[1] if len(result_probs) == 2 else 0.4
            away_win_prob = 1 - home_win_prob if len(result_probs) == 2 else 0.3
            draw_prob = 1 - home_win_prob - away_win_prob
        
        return {
            'match_result': {
                'home_win': round(home_win_prob * 100, 1),
                'draw': round(draw_prob * 100, 1),
                'away_win': round(away_win_prob * 100, 1)
            },
            'over_under_25': {
                'over': round(over_prob * 100, 1),
                'under': round((1 - over_prob) * 100, 1)
            },
            'both_teams_score': {
                'yes': round(bts_prob * 100, 1),
                'no': round((1 - bts_prob) * 100, 1)
            },
            'corners': {
                'over_10': round(corners_over_prob * 100, 1),
                'under_10': round((1 - corners_over_prob) * 100, 1)
            }
        }
    
    def analyze_ucl_matches(self):
        """วิเคราะห์การแข่งขัน UCL วันนี้"""
        
        print("🏆" * 70)
        print("🏆 UEFA CHAMPIONS LEAGUE 2025-2026 ADVANCED ML ANALYSIS")
        print(f"📅 Analysis Date: {self.analysis_date}")
        print("🏆" * 70)
        
        # Train models
        model_scores = self.train_models()
        
        print(f"\n🤖 MODEL PERFORMANCE")
        print("=" * 50)
        for model_name, score in model_scores.items():
            print(f"📊 {model_name.replace('_', ' ').title()}: {score:.1%}")
        
        # Generate fixtures
        fixtures = self.generate_ucl_fixtures()
        
        print(f"\n🏆 TODAY'S UCL MATCHES ANALYSIS")
        print("=" * 70)
        
        predictions = []
        
        for i, fixture in enumerate(fixtures[:10], 1):  # Analyze top 10 matches
            print(f"\n⚽ MATCH {i}: {fixture['home_team']} vs {fixture['away_team']}")
            print(f"📅 Date: {fixture['date']} {fixture['time']}")
            print(f"🏟️ Phase: {fixture['competition_phase']} - Matchday {fixture['matchday']}")
            print(f"📊 Coefficients: {fixture['home_coefficient']:.1f} vs {fixture['away_coefficient']:.1f}")
            print(f"🏆 UCL Titles: {fixture['home_ucl_titles']} vs {fixture['away_ucl_titles']}")
            
            # Get prediction
            prediction = self.predict_match(fixture)
            
            print(f"\n🎯 PREDICTIONS:")
            print(f"   🏆 Match Result:")
            print(f"      🏠 {fixture['home_team']}: {prediction['match_result']['home_win']}%")
            print(f"      🤝 Draw: {prediction['match_result']['draw']}%")
            print(f"      ✈️ {fixture['away_team']}: {prediction['match_result']['away_win']}%")
            
            print(f"   ⚽ Over/Under 2.5:")
            print(f"      📈 Over 2.5: {prediction['over_under_25']['over']}%")
            print(f"      📉 Under 2.5: {prediction['over_under_25']['under']}%")
            
            print(f"   🎯 Both Teams Score:")
            print(f"      ✅ Yes: {prediction['both_teams_score']['yes']}%")
            print(f"      ❌ No: {prediction['both_teams_score']['no']}%")
            
            print(f"   🚩 Corners:")
            print(f"      📈 Over 10: {prediction['corners']['over_10']}%")
            print(f"      📉 Under 10: {prediction['corners']['under_10']}%")
            
            # Betting recommendations
            max_prob = max(prediction['match_result'].values())
            if max_prob == prediction['match_result']['home_win']:
                main_bet = f"{fixture['home_team']} Win"
            elif max_prob == prediction['match_result']['away_win']:
                main_bet = f"{fixture['away_team']} Win"
            else:
                main_bet = "Draw"
            
            print(f"\n💰 BETTING RECOMMENDATIONS:")
            print(f"   🥇 PRIMARY: {main_bet} ({max_prob}%)")
            
            if prediction['over_under_25']['over'] > 60:
                print(f"   🥈 SECONDARY: Over 2.5 Goals ({prediction['over_under_25']['over']}%)")
            elif prediction['over_under_25']['under'] > 60:
                print(f"   🥈 SECONDARY: Under 2.5 Goals ({prediction['over_under_25']['under']}%)")
            
            if prediction['both_teams_score']['yes'] > 60:
                print(f"   🥉 TERTIARY: Both Teams Score - Yes ({prediction['both_teams_score']['yes']}%)")
            
            predictions.append({
                'fixture': fixture,
                'prediction': prediction,
                'main_bet': main_bet
            })
            
            print("-" * 70)
        
        # Summary
        print(f"\n📊 ANALYSIS SUMMARY")
        print("=" * 50)
        print(f"🏆 Competition: {self.competition} {self.season}")
        print(f"📅 Analysis Date: {self.analysis_date}")
        print(f"🔢 Matches Analyzed: {len(predictions)}")
        print(f"🤖 ML Models Used: {len(self.models)}")
        
        # Save results
        results = {
            'competition': f"{self.competition} {self.season}",
            'analysis_date': self.analysis_date,
            'model_scores': model_scores,
            'predictions': predictions,
            'summary': {
                'total_matches': len(predictions),
                'high_confidence_predictions': len([p for p in predictions if max(p['prediction']['match_result'].values()) > 60])
            }
        }
        
        with open('/Users/80090/Desktop/Project/untitle/ucl_2025_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n💾 Results saved to: ucl_2025_analysis.json")
        
        print("\n🏆" * 30)
        print("🏆 UEFA CHAMPIONS LEAGUE ANALYSIS COMPLETE!")
        print("🏆" * 30)
        
        return results

def main():
    """Main execution function"""
    analyzer = UEFAChampionsLeagueAdvancedML()
    
    print("🚀 Starting UEFA Champions League 2025-2026 Advanced ML Analysis...")
    
    try:
        results = analyzer.analyze_ucl_matches()
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📊 {results['summary']['total_matches']} matches analyzed")
        print(f"🎯 {results['summary']['high_confidence_predictions']} high-confidence predictions")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        print("🔧 Please check the system and try again")

if __name__ == "__main__":
    main()
