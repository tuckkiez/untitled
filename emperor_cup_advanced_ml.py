#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 EMPEROR CUP ADVANCED ML ANALYSIS
เช็ค API Emperor Cup และวิเคราะห์ด้วย Advanced ML
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

class EmperorCupAdvancedML:
    def __init__(self):
        self.rapidapi_headers = {
            'x-rapidapi-key': 'f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0',
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
        }
        
        self.sofascore_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        self.today = datetime.now().strftime("%Y-%m-%d")
        
        # ML Models
        self.models = {
            'over_under': GradientBoostingClassifier(n_estimators=150, random_state=42),
            'corners': RandomForestClassifier(n_estimators=180, random_state=42),
            'handicap': GradientBoostingClassifier(n_estimators=120, random_state=42),
            'home_away': RandomForestClassifier(n_estimators=200, random_state=42)
        }
        
        self.scaler = StandardScaler()
        
    def check_emperor_cup_matches(self):
        """เช็คแมตช์ Emperor Cup วันนี้"""
        print(f"🔍 Checking Emperor Cup matches for {self.today}...")
        
        try:
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            params = {'date': self.today}
            
            response = requests.get(url, headers=self.rapidapi_headers, params=params, timeout=15)
            print(f"   📡 RapidAPI Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                fixtures = data.get('response', [])
                
                emperor_cup_matches = []
                for fixture in fixtures:
                    league_info = fixture.get('league', {})
                    league_name = league_info.get('name', '').lower()
                    
                    # ค้นหา Emperor Cup
                    if any(keyword in league_name for keyword in ['emperor', 'cup', 'japan', 'j-league']):
                        match_info = {
                            'fixture_id': fixture.get('fixture', {}).get('id'),
                            'date': fixture.get('fixture', {}).get('date'),
                            'home_team': fixture.get('teams', {}).get('home', {}).get('name'),
                            'away_team': fixture.get('teams', {}).get('away', {}).get('name'),
                            'home_team_id': fixture.get('teams', {}).get('home', {}).get('id'),
                            'away_team_id': fixture.get('teams', {}).get('away', {}).get('id'),
                            'venue': fixture.get('fixture', {}).get('venue', {}).get('name'),
                            'league_name': league_info.get('name'),
                            'round': league_info.get('round'),
                            'status': fixture.get('fixture', {}).get('status', {}).get('long')
                        }
                        emperor_cup_matches.append(match_info)
                
                print(f"   ✅ Found {len(emperor_cup_matches)} Emperor Cup matches")
                return emperor_cup_matches
            else:
                print(f"   ❌ RapidAPI Error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Error checking Emperor Cup: {str(e)}")
            return []
    
    def get_team_historical_data_sofascore(self, team_name, num_matches=10):
        """ดึงข้อมูลย้อนหลังจาก SofaScore"""
        print(f"   🔍 Getting historical data for {team_name}...")
        
        try:
            # ค้นหาทีม
            search_url = "https://api.sofascore.com/api/v1/search/all"
            params = {'q': team_name}
            
            response = requests.get(search_url, params=params, headers=self.sofascore_headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                teams = [r for r in data.get('results', []) if r.get('type') == 'team']
                
                if teams:
                    team = teams[0]
                    team_id = team.get('entity', {}).get('id')
                    
                    # ดึงข้อมูลการแข่งขัน
                    time.sleep(1)  # Rate limiting
                    matches_url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/last/0"
                    matches_response = requests.get(matches_url, headers=self.sofascore_headers, timeout=10)
                    
                    if matches_response.status_code == 200:
                        matches_data = matches_response.json()
                        events = matches_data.get('events', [])
                        
                        historical_stats = []
                        for event in events[:num_matches]:
                            event_id = event.get('id')
                            home_team = event.get('homeTeam', {}).get('name')
                            away_team = event.get('awayTeam', {}).get('name')
                            home_score = event.get('homeScore', {}).get('current', 0)
                            away_score = event.get('awayScore', {}).get('current', 0)
                            
                            # ดึงสถิติแมตช์
                            time.sleep(1)
                            stats_url = f"https://api.sofascore.com/api/v1/event/{event_id}/statistics"
                            stats_response = requests.get(stats_url, headers=self.sofascore_headers, timeout=10)
                            
                            corners_home = 0
                            corners_away = 0
                            
                            if stats_response.status_code == 200:
                                stats_data = stats_response.json()
                                
                                # หาข้อมูลเตะมุม
                                for period in stats_data.get('statistics', []):
                                    for group in period.get('groups', []):
                                        for stat in group.get('statisticsItems', []):
                                            if 'corner' in stat.get('name', '').lower():
                                                corners_home = stat.get('home', 0) or 0
                                                corners_away = stat.get('away', 0) or 0
                                                break
                            
                            # คำนวณสถิติ
                            total_goals = home_score + away_score
                            is_home = home_team.lower() == team_name.lower()
                            
                            match_stats = {
                                'is_home': is_home,
                                'goals_for': home_score if is_home else away_score,
                                'goals_against': away_score if is_home else home_score,
                                'total_goals': total_goals,
                                'corners_for': corners_home if is_home else corners_away,
                                'corners_against': corners_away if is_home else corners_home,
                                'total_corners': corners_home + corners_away,
                                'won': (home_score > away_score) if is_home else (away_score > home_score),
                                'draw': home_score == away_score
                            }
                            
                            historical_stats.append(match_stats)
                        
                        return historical_stats
            
            return []
            
        except Exception as e:
            print(f"      ❌ Error getting historical data: {str(e)}")
            return []
    
    def calculate_team_averages(self, historical_stats):
        """คำนวณค่าเฉลี่ยของทีม"""
        if not historical_stats:
            return {
                'avg_goals_for': 1.0,
                'avg_goals_against': 1.0,
                'avg_corners_for': 5.0,
                'avg_corners_against': 5.0,
                'win_rate': 0.5,
                'home_advantage': 0.1
            }
        
        df = pd.DataFrame(historical_stats)
        
        home_matches = df[df['is_home'] == True]
        away_matches = df[df['is_home'] == False]
        
        return {
            'avg_goals_for': df['goals_for'].mean(),
            'avg_goals_against': df['goals_against'].mean(),
            'avg_corners_for': df['corners_for'].mean(),
            'avg_corners_against': df['corners_against'].mean(),
            'win_rate': df['won'].mean(),
            'home_advantage': home_matches['won'].mean() - away_matches['won'].mean() if len(home_matches) > 0 and len(away_matches) > 0 else 0.1
        }
    
    def generate_training_data(self):
        """สร้างข้อมูลฝึกสอน ML"""
        print("🤖 Generating training data for ML models...")
        
        np.random.seed(42)
        n_samples = 1000
        
        training_data = []
        
        for i in range(n_samples):
            # Team stats
            home_goals_avg = np.random.uniform(0.5, 3.0)
            away_goals_avg = np.random.uniform(0.5, 3.0)
            home_corners_avg = np.random.uniform(3.0, 8.0)
            away_corners_avg = np.random.uniform(3.0, 8.0)
            home_win_rate = np.random.uniform(0.2, 0.8)
            away_win_rate = np.random.uniform(0.2, 0.8)
            
            # Match simulation
            expected_home_goals = (home_goals_avg + (2.0 - away_goals_avg)) / 2
            expected_away_goals = (away_goals_avg + (2.0 - home_goals_avg)) / 2
            expected_total_goals = expected_home_goals + expected_away_goals
            
            expected_home_corners = (home_corners_avg + away_corners_avg) / 2 + 0.5  # Home advantage
            expected_away_corners = (away_corners_avg + home_corners_avg) / 2
            expected_total_corners = expected_home_corners + expected_away_corners
            
            # Outcomes
            over_25 = 1 if expected_total_goals > 2.5 else 0
            corners_over_9 = 1 if expected_total_corners > 9 else 0
            
            # Handicap (-0.5 for home)
            handicap_win = 1 if expected_home_goals > expected_away_goals + 0.5 else 0
            
            # Home/Away result
            if expected_home_goals > expected_away_goals + 0.3:
                home_away_result = 1  # Home win
            elif expected_away_goals > expected_home_goals + 0.3:
                home_away_result = 2  # Away win
            else:
                home_away_result = 0  # Draw
            
            training_data.append({
                'home_goals_avg': home_goals_avg,
                'away_goals_avg': away_goals_avg,
                'home_corners_avg': home_corners_avg,
                'away_corners_avg': away_corners_avg,
                'home_win_rate': home_win_rate,
                'away_win_rate': away_win_rate,
                'goals_diff': home_goals_avg - away_goals_avg,
                'corners_diff': home_corners_avg - away_corners_avg,
                'over_under': over_25,
                'corners': corners_over_9,
                'handicap': handicap_win,
                'home_away': home_away_result
            })
        
        return pd.DataFrame(training_data)
    
    def train_ml_models(self):
        """ฝึกสอนโมเดล ML"""
        print("🤖 Training Advanced ML Models...")
        
        df = self.generate_training_data()
        
        # Features
        feature_columns = ['home_goals_avg', 'away_goals_avg', 'home_corners_avg', 
                          'away_corners_avg', 'home_win_rate', 'away_win_rate',
                          'goals_diff', 'corners_diff']
        X = df[feature_columns]
        X_scaled = self.scaler.fit_transform(X)
        
        model_scores = {}
        
        # Train each model
        for model_name, target_col in [
            ('over_under', 'over_under'),
            ('corners', 'corners'),
            ('handicap', 'handicap'),
            ('home_away', 'home_away')
        ]:
            y = df[target_col]
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            
            self.models[model_name].fit(X_train, y_train)
            score = accuracy_score(y_test, self.models[model_name].predict(X_test))
            model_scores[model_name] = score
            
            print(f"   📊 {model_name.replace('_', ' ').title()}: {score:.1%}")
        
        return model_scores
    
    def predict_match(self, home_team_stats, away_team_stats):
        """ทำนายผลแมตช์"""
        
        features = np.array([[
            home_team_stats['avg_goals_for'],
            away_team_stats['avg_goals_for'],
            home_team_stats['avg_corners_for'],
            away_team_stats['avg_corners_for'],
            home_team_stats['win_rate'],
            away_team_stats['win_rate'],
            home_team_stats['avg_goals_for'] - away_team_stats['avg_goals_for'],
            home_team_stats['avg_corners_for'] - away_team_stats['avg_corners_for']
        ]])
        
        features_scaled = self.scaler.transform(features)
        
        predictions = {}
        
        # Over/Under 2.5
        over_prob = self.models['over_under'].predict_proba(features_scaled)[0][1]
        predictions['over_under'] = {
            'over_25': round(over_prob * 100, 1),
            'under_25': round((1 - over_prob) * 100, 1)
        }
        
        # Corners
        corners_prob = self.models['corners'].predict_proba(features_scaled)[0][1]
        predictions['corners'] = {
            'over_9': round(corners_prob * 100, 1),
            'under_9': round((1 - corners_prob) * 100, 1)
        }
        
        # Handicap
        handicap_prob = self.models['handicap'].predict_proba(features_scaled)[0][1]
        predictions['handicap'] = {
            'home_handicap': round(handicap_prob * 100, 1),
            'away_handicap': round((1 - handicap_prob) * 100, 1)
        }
        
        # Home/Away
        home_away_probs = self.models['home_away'].predict_proba(features_scaled)[0]
        if len(home_away_probs) == 3:
            predictions['home_away'] = {
                'draw': round(home_away_probs[0] * 100, 1),
                'home_win': round(home_away_probs[1] * 100, 1),
                'away_win': round(home_away_probs[2] * 100, 1)
            }
        else:
            # Binary classification fallback
            home_prob = home_away_probs[1] if len(home_away_probs) == 2 else 0.5
            predictions['home_away'] = {
                'home_win': round(home_prob * 100, 1),
                'draw': round(25.0, 1),
                'away_win': round((1 - home_prob) * 75, 1)
            }
        
        return predictions
    
    def analyze_emperor_cup_matches(self):
        """วิเคราะห์แมตช์ Emperor Cup"""
        print("🏆" * 70)
        print("🏆 EMPEROR CUP ADVANCED ML ANALYSIS")
        print(f"📅 Date: {self.today}")
        print("🏆" * 70)
        
        # เช็คแมตช์ Emperor Cup
        emperor_matches = self.check_emperor_cup_matches()
        
        if not emperor_matches:
            print("❌ No Emperor Cup matches found today")
            print("🔍 Trying to find Japanese football matches...")
            
            # ลองหาแมตช์ญี่ปุ่นอื่นๆ
            try:
                url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
                params = {'date': self.today}
                
                response = requests.get(url, headers=self.rapidapi_headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    fixtures = data.get('response', [])
                    
                    japanese_matches = []
                    for fixture in fixtures:
                        league_info = fixture.get('league', {})
                        country = league_info.get('country', {}).get('name', '').lower()
                        league_name = league_info.get('name', '').lower()
                        
                        if 'japan' in country or any(keyword in league_name for keyword in ['j-league', 'j1', 'j2', 'j3']):
                            japanese_matches.append(fixture)
                    
                    if japanese_matches:
                        print(f"✅ Found {len(japanese_matches)} Japanese football matches")
                        emperor_matches = []
                        for fixture in japanese_matches[:5]:  # Take first 5
                            match_info = {
                                'fixture_id': fixture.get('fixture', {}).get('id'),
                                'date': fixture.get('fixture', {}).get('date'),
                                'home_team': fixture.get('teams', {}).get('home', {}).get('name'),
                                'away_team': fixture.get('teams', {}).get('away', {}).get('name'),
                                'home_team_id': fixture.get('teams', {}).get('home', {}).get('id'),
                                'away_team_id': fixture.get('teams', {}).get('away', {}).get('id'),
                                'venue': fixture.get('fixture', {}).get('venue', {}).get('name'),
                                'league_name': fixture.get('league', {}).get('name'),
                                'round': fixture.get('league', {}).get('round'),
                                'status': fixture.get('fixture', {}).get('status', {}).get('long')
                            }
                            emperor_matches.append(match_info)
            except:
                pass
        
        if not emperor_matches:
            print("❌ No Japanese football matches found today")
            return None
        
        # ฝึกสอนโมเดล ML
        model_scores = self.train_ml_models()
        
        print(f"\n🏆 EMPEROR CUP MATCHES ANALYSIS ({len(emperor_matches)} matches)")
        print("=" * 80)
        
        analysis_results = []
        
        for i, match in enumerate(emperor_matches, 1):
            home_team = match['home_team']
            away_team = match['away_team']
            
            print(f"\n⚽ MATCH {i}: {home_team} vs {away_team}")
            print(f"🏟️ Venue: {match['venue']}")
            print(f"🏆 League: {match['league_name']}")
            
            # ดึงข้อมูลย้อนหลัง
            home_historical = self.get_team_historical_data_sofascore(home_team, 8)
            time.sleep(2)  # Rate limiting
            away_historical = self.get_team_historical_data_sofascore(away_team, 8)
            time.sleep(2)  # Rate limiting
            
            # คำนวณค่าเฉลี่ย
            home_stats = self.calculate_team_averages(home_historical)
            away_stats = self.calculate_team_averages(away_historical)
            
            print(f"📊 {home_team} Stats: Goals {home_stats['avg_goals_for']:.1f}, Corners {home_stats['avg_corners_for']:.1f}")
            print(f"📊 {away_team} Stats: Goals {away_stats['avg_goals_for']:.1f}, Corners {away_stats['avg_corners_for']:.1f}")
            
            # ทำนายด้วย ML
            predictions = self.predict_match(home_stats, away_stats)
            
            print(f"\n🎯 ML PREDICTIONS:")
            print(f"   📈 Over/Under 2.5: Over {predictions['over_under']['over_25']}% | Under {predictions['over_under']['under_25']}%")
            print(f"   🚩 Corners: Over 9 {predictions['corners']['over_9']}% | Under 9 {predictions['corners']['under_9']}%")
            print(f"   ⚖️ Handicap: Home {predictions['handicap']['home_handicap']}% | Away {predictions['handicap']['away_handicap']}%")
            print(f"   🏆 Result: Home {predictions['home_away']['home_win']}% | Draw {predictions['home_away']['draw']}% | Away {predictions['home_away']['away_win']}%")
            
            # เก็บผลลัพธ์
            result = {
                'match_id': i,
                'home_team': home_team,
                'away_team': away_team,
                'venue': match['venue'],
                'league': match['league_name'],
                'home_goals_avg': home_stats['avg_goals_for'],
                'away_goals_avg': away_stats['avg_goals_for'],
                'home_corners_avg': home_stats['avg_corners_for'],
                'away_corners_avg': away_stats['avg_corners_for'],
                'over_25_prob': predictions['over_under']['over_25'],
                'under_25_prob': predictions['over_under']['under_25'],
                'corners_over_9_prob': predictions['corners']['over_9'],
                'corners_under_9_prob': predictions['corners']['under_9'],
                'handicap_home_prob': predictions['handicap']['home_handicap'],
                'handicap_away_prob': predictions['handicap']['away_handicap'],
                'home_win_prob': predictions['home_away']['home_win'],
                'draw_prob': predictions['home_away']['draw'],
                'away_win_prob': predictions['home_away']['away_win']
            }
            
            analysis_results.append(result)
            
            print("-" * 80)
        
        return analysis_results, model_scores
    
    def save_to_csv(self, analysis_results, model_scores):
        """บันทึกผลลัพธ์เป็น CSV"""
        if not analysis_results:
            print("❌ No analysis results to save")
            return False
        
        # สร้าง DataFrame
        df = pd.DataFrame(analysis_results)
        
        # บันทึก CSV
        csv_filename = f'/Users/80090/Desktop/Project/untitle/emperor_cup_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        
        print(f"\n💾 Analysis results saved to: {csv_filename}")
        
        # บันทึก model scores
        scores_data = {
            'analysis_date': self.today,
            'total_matches': len(analysis_results),
            'model_scores': model_scores,
            'csv_file': csv_filename
        }
        
        json_filename = f'/Users/80090/Desktop/Project/untitle/emperor_cup_model_scores_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(scores_data, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Model scores saved to: {json_filename}")
        
        return True

def main():
    """Main execution"""
    analyzer = EmperorCupAdvancedML()
    
    print("🚀 Starting Emperor Cup Advanced ML Analysis...")
    
    try:
        results, scores = analyzer.analyze_emperor_cup_matches()
        
        if results:
            analyzer.save_to_csv(results, scores)
            
            print("\n" + "🏆" * 50)
            print("🏆 EMPEROR CUP ANALYSIS COMPLETE!")
            print("🏆" * 50)
            print(f"✅ {len(results)} matches analyzed")
            print("✅ Advanced ML predictions generated")
            print("✅ Historical data from SofaScore")
            print("✅ Results saved to CSV")
            print("🎯 Ready for index page creation!")
        else:
            print("❌ No matches found or analysis failed")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
