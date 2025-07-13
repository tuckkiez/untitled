#!/usr/bin/env python3
"""
🚀 Multi-League Table Predictor - ทุกลีกทุกนัดในตารางเดียว
ระบบทำนายฟุตบอลหลายลีกด้วย UI แบบตารางที่สวยงาม

Supported Leagues:
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (England)
- 🇪🇸 La Liga (Spain) 
- 🇩🇪 Bundesliga (Germany)
- 🇮🇹 Serie A (Italy)
- 🇫🇷 Ligue 1 (France)
- 🇰🇷 K League 2 (South Korea)
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
    ExtraTreesClassifier, VotingClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import time

class MultiLeagueTablePredictor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        
        # Major leagues configuration
        self.leagues = {
            39: {"name": "Premier League", "country": "England", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "weight": 1.2, "season": 2024},
            140: {"name": "La Liga", "country": "Spain", "flag": "🇪🇸", "weight": 1.1, "season": 2024},
            78: {"name": "Bundesliga", "country": "Germany", "flag": "🇩🇪", "weight": 1.1, "season": 2024},
            135: {"name": "Serie A", "country": "Italy", "flag": "🇮🇹", "weight": 1.1, "season": 2024},
            61: {"name": "Ligue 1", "country": "France", "flag": "🇫🇷", "weight": 1.0, "season": 2024},
            293: {"name": "K League 2", "country": "South Korea", "flag": "🇰🇷", "weight": 0.9, "season": 2025}
        }
        
        # Team strength database (simplified)
        self.team_strengths = {
            # Premier League
            "Manchester City": {"attack": 95, "defense": 90, "form": 92},
            "Arsenal": {"attack": 88, "defense": 85, "form": 87},
            "Liverpool": {"attack": 90, "defense": 82, "form": 86},
            "Chelsea": {"attack": 82, "defense": 78, "form": 80},
            "Manchester United": {"attack": 80, "defense": 75, "form": 78},
            "Tottenham": {"attack": 85, "defense": 72, "form": 79},
            
            # La Liga
            "Real Madrid": {"attack": 93, "defense": 88, "form": 91},
            "Barcelona": {"attack": 90, "defense": 82, "form": 86},
            "Atletico Madrid": {"attack": 82, "defense": 90, "form": 86},
            "Athletic Bilbao": {"attack": 75, "defense": 80, "form": 78},
            "Real Sociedad": {"attack": 78, "defense": 75, "form": 77},
            
            # Bundesliga
            "Bayern Munich": {"attack": 92, "defense": 85, "form": 89},
            "Borussia Dortmund": {"attack": 88, "defense": 78, "form": 83},
            "RB Leipzig": {"attack": 82, "defense": 80, "form": 81},
            "Bayer Leverkusen": {"attack": 85, "defense": 75, "form": 80},
            
            # Serie A
            "Inter": {"attack": 88, "defense": 85, "form": 87},
            "AC Milan": {"attack": 82, "defense": 80, "form": 81},
            "Juventus": {"attack": 80, "defense": 85, "form": 83},
            "Napoli": {"attack": 85, "defense": 78, "form": 82},
            "AS Roma": {"attack": 78, "defense": 75, "form": 77},
            
            # Ligue 1
            "Paris Saint Germain": {"attack": 90, "defense": 82, "form": 86},
            "AS Monaco": {"attack": 80, "defense": 75, "form": 78},
            "Marseille": {"attack": 78, "defense": 72, "form": 75},
            "Lyon": {"attack": 75, "defense": 70, "form": 73},
            
            # K League 2
            "Incheon United": {"attack": 75, "defense": 68, "form": 72},
            "Asan Mugunghwa": {"attack": 65, "defense": 70, "form": 68},
            "Bucheon FC 1995": {"attack": 78, "defense": 72, "form": 75},
            "Gimpo Citizen": {"attack": 62, "defense": 65, "form": 63},
            "Ansan Greeners": {"attack": 70, "defense": 74, "form": 72},
            "Seoul E-Land FC": {"attack": 82, "defense": 75, "form": 78}
        }
        
    def make_api_request(self, endpoint: str, params: Dict = None) -> Dict:
        """ส่งคำขอ API"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("⚠️ Rate limit reached")
                time.sleep(2)
                return {}
            else:
                print(f"❌ API Error: {response.status_code}")
                return {}
        except Exception as e:
            print(f"🚨 Request Error: {e}")
            return {}
    
    def get_today_matches(self) -> List[Dict]:
        """ดึงการแข่งขันวันนี้จากทุกลีก"""
        today = datetime.now().strftime('%Y-%m-%d')
        all_matches = []
        
        print("📥 กำลังดึงข้อมูลการแข่งขันวันนี้...")
        
        # ดึงข้อมูลจากทุกลีก
        for league_id, league_info in self.leagues.items():
            params = {
                'league': league_id,
                'season': league_info['season'],
                'date': today
            }
            
            data = self.make_api_request('fixtures', params)
            if data and 'response' in data:
                for match in data['response']:
                    if match['fixture']['status']['short'] in ['NS', 'TBD', '1H', '2H', 'HT']:
                        match_info = {
                            'league_id': league_id,
                            'league_name': league_info['name'],
                            'league_flag': league_info['flag'],
                            'league_weight': league_info['weight'],
                            'home_team': match['teams']['home']['name'],
                            'away_team': match['teams']['away']['name'],
                            'home_id': match['teams']['home']['id'],
                            'away_id': match['teams']['away']['id'],
                            'fixture_id': match['fixture']['id'],
                            'date': match['fixture']['date'],
                            'venue': match['fixture']['venue']['name'] if match['fixture']['venue'] else 'TBD',
                            'status': match['fixture']['status']['short']
                        }
                        all_matches.append(match_info)
            
            time.sleep(0.5)  # Rate limiting
        
        print(f"✅ พบการแข่งขัน {len(all_matches)} นัดจาก {len(self.leagues)} ลีก")
        return all_matches
    
    def calculate_handicap_line(self, home_team: str, away_team: str, league_weight: float) -> Tuple[float, str]:
        """คำนวณราคาต่อรอง Handicap"""
        home_rating = self.team_strengths.get(home_team, {'attack': 70, 'defense': 70, 'form': 70})
        away_rating = self.team_strengths.get(away_team, {'attack': 70, 'defense': 70, 'form': 70})
        
        # คำนวณความแข็งแกร่งรวม (รวม league weight)
        home_strength = (home_rating['attack'] + home_rating['defense'] + home_rating['form']) / 3 + 5  # Home advantage
        away_strength = (away_rating['attack'] + away_rating['defense'] + away_rating['form']) / 3
        
        # ปรับตาม league weight
        strength_diff = (home_strength - away_strength) * league_weight
        
        # กำหนดราคาต่อรอง
        if strength_diff >= 12:
            return -2.0, f"{home_team} -2.0"
        elif strength_diff >= 8:
            return -1.5, f"{home_team} -1.5"
        elif strength_diff >= 5:
            return -1.0, f"{home_team} -1.0"
        elif strength_diff >= 2:
            return -0.5, f"{home_team} -0.5"
        elif strength_diff >= -2:
            return 0.0, "Draw No Bet"
        elif strength_diff >= -5:
            return 0.5, f"{away_team} +0.5"
        elif strength_diff >= -8:
            return 1.0, f"{away_team} +1.0"
        elif strength_diff >= -12:
            return 1.5, f"{away_team} +1.5"
        else:
            return 2.0, f"{away_team} +2.0"
    
    def predict_match_result(self, home_team: str, away_team: str, league_weight: float) -> Dict:
        """ทำนายผลการแข่งขัน"""
        home_rating = self.team_strengths.get(home_team, {'attack': 70, 'defense': 70, 'form': 70})
        away_rating = self.team_strengths.get(away_team, {'attack': 70, 'defense': 70, 'form': 70})
        
        # คำนวณความแข็งแกร่งรวม
        home_strength = (home_rating['attack'] + home_rating['defense'] + home_rating['form']) / 3 + 5
        away_strength = (away_rating['attack'] + away_rating['defense'] + away_rating['form']) / 3
        
        strength_diff = (home_strength - away_strength) * league_weight
        
        # กำหนดความน่าจะเป็นและผลทำนาย
        if strength_diff >= 12:
            result, confidence = "Home Win", 85
        elif strength_diff >= 8:
            result, confidence = "Home Win", 78
        elif strength_diff >= 4:
            result, confidence = "Home Win", 68
        elif strength_diff >= 1:
            result, confidence = "Home Win", 58
        elif strength_diff >= -1:
            result, confidence = "Draw", 55
        elif strength_diff >= -4:
            result, confidence = "Away Win", 58
        elif strength_diff >= -8:
            result, confidence = "Away Win", 68
        elif strength_diff >= -12:
            result, confidence = "Away Win", 78
        else:
            result, confidence = "Away Win", 85
        
        return {'prediction': result, 'confidence': confidence}
    
    def predict_over_under(self, home_team: str, away_team: str, league_weight: float) -> Dict:
        """ทำนาย Over/Under 2.5"""
        home_rating = self.team_strengths.get(home_team, {'attack': 70, 'defense': 70, 'form': 70})
        away_rating = self.team_strengths.get(away_team, {'attack': 70, 'defense': 70, 'form': 70})
        
        # คำนวณแนวโน้มการทำประตู
        attack_power = (home_rating['attack'] + away_rating['attack']) / 2
        defense_power = (home_rating['defense'] + away_rating['defense']) / 2
        
        goal_tendency = (attack_power - defense_power + 70) * league_weight
        
        if goal_tendency >= 78:
            return {'prediction': "Over 2.5", 'confidence': 82}
        elif goal_tendency >= 72:
            return {'prediction': "Over 2.5", 'confidence': 68}
        elif goal_tendency >= 65:
            return {'prediction': "Under 2.5", 'confidence': 65}
        else:
            return {'prediction': "Under 2.5", 'confidence': 78}
    
    def predict_corners(self, home_team: str, away_team: str, league_weight: float) -> Dict:
        """ทำนาย Corners"""
        home_rating = self.team_strengths.get(home_team, {'attack': 70, 'defense': 70, 'form': 70})
        away_rating = self.team_strengths.get(away_team, {'attack': 70, 'defense': 70, 'form': 70})
        
        # คำนวณแนวโน้ม Corner
        corner_tendency = ((home_rating['attack'] + away_rating['attack']) / 2) * league_weight
        
        if corner_tendency >= 85:
            return {'prediction': "Over 10", 'confidence': 85}
        elif corner_tendency >= 75:
            return {'prediction': "Over 10", 'confidence': 72}
        else:
            return {'prediction': "Under 10", 'confidence': 75}
    
    def predict_handicap_result(self, home_team: str, away_team: str, handicap_line: float, handicap_desc: str, match_result: Dict) -> Dict:
        """ทำนายผล Handicap"""
        if "Draw No Bet" in handicap_desc:
            if match_result['prediction'] == "Draw":
                prediction = "Push (เงินคืน)"
                confidence = 85
            elif match_result['prediction'] == "Home Win":
                prediction = f"✅ {home_team} ชนะ"
                confidence = match_result['confidence']
            else:
                prediction = f"✅ {away_team} ชนะ"
                confidence = match_result['confidence']
        elif handicap_line < 0:  # Home team favored
            team_name = handicap_desc.split()[0] + " " + handicap_desc.split()[1] if len(handicap_desc.split()) > 1 else home_team
            if match_result['prediction'] == "Home Win":
                prediction = f"✅ รับ {team_name} {handicap_line}"
                confidence = match_result['confidence'] - 5
            else:
                prediction = f"❌ รับ {team_name} {handicap_line}"
                confidence = 100 - match_result['confidence']
        else:  # Away team favored
            team_name = handicap_desc.split()[0] + " " + handicap_desc.split()[1] if len(handicap_desc.split()) > 1 else away_team
            if match_result['prediction'] == "Away Win":
                prediction = f"✅ รับ {team_name} +{handicap_line}"
                confidence = match_result['confidence'] - 5
            else:
                prediction = f"❌ รับ {team_name} +{handicap_line}"
                confidence = 100 - match_result['confidence']
        
        return {'prediction': prediction, 'confidence': confidence, 'line': handicap_desc}
    
    def predict_match(self, match: Dict) -> Dict:
        """ทำนายการแข่งขันแบบครบถ้วน"""
        home_team = match['home_team']
        away_team = match['away_team']
        league_weight = match['league_weight']
        
        # ทำนายแต่ละหมวด
        match_result = self.predict_match_result(home_team, away_team, league_weight)
        over_under = self.predict_over_under(home_team, away_team, league_weight)
        corners = self.predict_corners(home_team, away_team, league_weight)
        
        # คำนวณ Handicap
        handicap_line, handicap_desc = self.calculate_handicap_line(home_team, away_team, league_weight)
        handicap_result = self.predict_handicap_result(home_team, away_team, handicap_line, handicap_desc, match_result)
        
        return {
            'match_result': match_result,
            'handicap': handicap_result,
            'over_under': over_under,
            'corners': corners
        }
    
    def get_all_predictions(self) -> List[Dict]:
        """ทำนายการแข่งขันทั้งหมด"""
        matches = self.get_today_matches()
        
        if not matches:
            print("❌ ไม่พบการแข่งขันวันนี้")
            return []
        
        predictions = []
        print(f"🤖 กำลังทำนาย {len(matches)} การแข่งขัน...")
        
        for match in matches:
            try:
                prediction = self.predict_match(match)
                predictions.append({
                    'match': match,
                    'predictions': prediction
                })
            except Exception as e:
                print(f"❌ Error predicting {match['home_team']} vs {match['away_team']}: {e}")
        
        print(f"✅ ทำนายเสร็จสิ้น {len(predictions)} การแข่งขัน")
        return predictions

if __name__ == "__main__":
    # ทดสอบระบบ
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    predictor = MultiLeagueTablePredictor(api_key)
    
    print("🚀 Multi-League Table Predictor - Testing...")
    print("=" * 60)
    
    predictions = predictor.get_all_predictions()
    
    if predictions:
        print(f"\n📊 พบการแข่งขัน {len(predictions)} นัด:")
        for i, pred in enumerate(predictions[:5], 1):  # แสดง 5 นัดแรก
            match = pred['match']
            p = pred['predictions']
            
            print(f"\n{i}. {match['league_flag']} {match['league_name']}")
            print(f"   {match['home_team']} vs {match['away_team']}")
            print(f"   🎯 Result: {p['match_result']['prediction']} ({p['match_result']['confidence']}%)")
            print(f"   ⚖️ Handicap: {p['handicap']['line']} - {p['handicap']['prediction']}")
            print(f"   ⚽ O/U: {p['over_under']['prediction']} ({p['over_under']['confidence']}%)")
            print(f"   📐 Corners: {p['corners']['prediction']} ({p['corners']['confidence']}%)")
    else:
        print("❌ ไม่พบการแข่งขันวันนี้")
