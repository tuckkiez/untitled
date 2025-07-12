#!/usr/bin/env python3
"""
🏆 J-League 2 Ultra Advanced Predictor & Backtest System
ระบบทำนายและทดสอบย้อนหลังสำหรับ J-League 2 ด้วย API-Sports
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class JLeague2Predictor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        self.league_id = 99  # J2 League
        self.season = 2025
        self.team_ratings = {}
        self.fixtures_data = []
        
    def make_api_request(self, endpoint: str, params: Dict = None) -> Dict:
        """ส่งคำขอ API"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ API Error: {response.status_code}")
                return {}
        except Exception as e:
            print(f"🚨 Request Error: {e}")
            return {}
    
    def load_fixtures_data(self) -> List[Dict]:
        """ดึงข้อมูลการแข่งขันทั้งหมด"""
        print("📥 กำลังดึงข้อมูลการแข่งขัน J-League 2...")
        
        params = {
            'league': self.league_id,
            'season': self.season
        }
        
        data = self.make_api_request('fixtures', params)
        
        if 'response' in data:
            fixtures = data['response']
            print(f"✅ ดึงข้อมูลได้ {len(fixtures)} การแข่งขัน")
            
            # กรองเฉพาะนัดที่จบแล้ว
            finished_fixtures = []
            upcoming_fixtures = []
            
            for fixture in fixtures:
                if fixture['fixture']['status']['short'] == 'FT':
                    finished_fixtures.append(fixture)
                elif fixture['fixture']['status']['short'] in ['NS', 'TBD']:
                    upcoming_fixtures.append(fixture)
            
            print(f"🏁 นัดที่จบแล้ว: {len(finished_fixtures)} นัด")
            print(f"⏳ นัดที่ยังไม่แข่ง: {len(upcoming_fixtures)} นัด")
            
            self.fixtures_data = fixtures
            return finished_fixtures, upcoming_fixtures
        
        return [], []
    
    def calculate_team_ratings(self, fixtures: List[Dict]) -> Dict:
        """คำนวณ ELO Rating สำหรับแต่ละทีม"""
        print("🧮 กำลังคำนวณ ELO Rating...")
        
        # เริ่มต้น ELO ที่ 1500 สำหรับทุกทีม
        ratings = {}
        
        for fixture in fixtures:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            
            if home_team not in ratings:
                ratings[home_team] = 1500
            if away_team not in ratings:
                ratings[away_team] = 1500
        
        # คำนวณ ELO จากผลการแข่งขัน
        for fixture in fixtures:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_goals = fixture['goals']['home'] or 0
            away_goals = fixture['goals']['away'] or 0
            
            # คำนวณผลการแข่งขัน
            if home_goals > away_goals:
                home_result = 1.0  # ชนะ
                away_result = 0.0  # แพ้
            elif home_goals < away_goals:
                home_result = 0.0  # แพ้
                away_result = 1.0  # ชนะ
            else:
                home_result = 0.5  # เสมอ
                away_result = 0.5  # เสมอ
            
            # คำนวณ Expected Score
            home_expected = 1 / (1 + 10**((ratings[away_team] - ratings[home_team] - 100) / 400))
            away_expected = 1 / (1 + 10**((ratings[home_team] - ratings[away_team] + 100) / 400))
            
            # อัปเดต ELO (K-factor = 32)
            K = 32
            ratings[home_team] += K * (home_result - home_expected)
            ratings[away_team] += K * (away_result - away_expected)
        
        self.team_ratings = ratings
        
        # แสดงอันดับทีม
        sorted_teams = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
        print("\n🏆 อันดับทีมตาม ELO Rating:")
        for i, (team, rating) in enumerate(sorted_teams[:10], 1):
            print(f"  {i:2d}. {team:<25} {rating:.0f}")
        
        return ratings
    
    def predict_match(self, home_team: str, away_team: str) -> Dict:
        """ทำนายผลการแข่งขัน"""
        if home_team not in self.team_ratings or away_team not in self.team_ratings:
            return {
                'home_win_prob': 0.33,
                'draw_prob': 0.34,
                'away_win_prob': 0.33,
                'prediction': 'Draw',
                'confidence': 0.34,
                'home_handicap': 'Draw',
                'over_under': 'Under 2.5'
            }
        
        home_rating = self.team_ratings[home_team]
        away_rating = self.team_ratings[away_team]
        
        # คำนวณความน่าจะเป็น (รวม Home Advantage +100)
        home_expected = 1 / (1 + 10**((away_rating - home_rating - 100) / 400))
        away_expected = 1 - home_expected
        
        # ปรับความน่าจะเป็นให้รวมการเสมอ
        draw_prob = 0.25  # ความน่าจะเป็นเสมอพื้นฐาน
        home_win_prob = home_expected * (1 - draw_prob)
        away_win_prob = away_expected * (1 - draw_prob)
        
        # ทำนายผลลัพธ์
        if home_win_prob > away_win_prob and home_win_prob > draw_prob:
            prediction = 'Home Win'
            confidence = home_win_prob
        elif away_win_prob > home_win_prob and away_win_prob > draw_prob:
            prediction = 'Away Win'
            confidence = away_win_prob
        else:
            prediction = 'Draw'
            confidence = draw_prob
        
        # ทำนาย Handicap
        rating_diff = home_rating - away_rating + 100  # รวม home advantage
        if rating_diff > 100:
            handicap_pred = 'Home Win'
        elif rating_diff < -100:
            handicap_pred = 'Away Win'
        else:
            handicap_pred = 'Draw'
        
        # ทำนาย Over/Under (ใช้ rating เฉลี่ยเป็นตัวชี้วัด)
        avg_rating = (home_rating + away_rating) / 2
        if avg_rating > 1550:
            over_under = 'Over 2.5'
        else:
            over_under = 'Under 2.5'
        
        return {
            'home_win_prob': home_win_prob,
            'draw_prob': draw_prob,
            'away_win_prob': away_win_prob,
            'prediction': prediction,
            'confidence': confidence,
            'home_handicap': handicap_pred,
            'over_under': over_under,
            'home_rating': home_rating,
            'away_rating': away_rating
        }
    
    def backtest_last_matches(self, finished_fixtures: List[Dict], num_matches: int = 20) -> Dict:
        """ทดสอบย้อนหลัง N นัดล่าสุด"""
        print(f"\n🔬 เริ่มการทดสอบย้อนหลัง {num_matches} นัดล่าสุด...")
        
        # เรียงตามวันที่
        sorted_fixtures = sorted(finished_fixtures, key=lambda x: x['fixture']['date'])
        
        # แบ่งข้อมูลสำหรับเทรนและทดสอบ
        train_fixtures = sorted_fixtures[:-num_matches]
        test_fixtures = sorted_fixtures[-num_matches:]
        
        print(f"📚 ใช้ข้อมูลเทรน: {len(train_fixtures)} นัด")
        print(f"🧪 ใช้ข้อมูลทดสอบ: {len(test_fixtures)} นัด")
        
        # คำนวณ ELO จากข้อมูลเทรน
        self.calculate_team_ratings(train_fixtures)
        
        # ทดสอบการทำนาย
        results = {
            'match_result': {'correct': 0, 'total': 0},
            'handicap': {'correct': 0, 'total': 0},
            'over_under': {'correct': 0, 'total': 0},
            'high_confidence': {'correct': 0, 'total': 0},
            'predictions': []
        }
        
        print(f"\n📊 ผลการทดสอบ {num_matches} นัดล่าสุด:")
        print("=" * 80)
        
        for i, fixture in enumerate(test_fixtures, 1):
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_goals = fixture['goals']['home'] or 0
            away_goals = fixture['goals']['away'] or 0
            
            # ทำนาย
            prediction = self.predict_match(home_team, away_team)
            
            # ผลจริง
            if home_goals > away_goals:
                actual_result = 'Home Win'
                actual_handicap = 'Home Win'
            elif home_goals < away_goals:
                actual_result = 'Away Win'
                actual_handicap = 'Away Win'
            else:
                actual_result = 'Draw'
                actual_handicap = 'Draw'
            
            total_goals = home_goals + away_goals
            actual_over_under = 'Over 2.5' if total_goals > 2.5 else 'Under 2.5'
            
            # ตรวจสอบความถูกต้อง
            match_correct = prediction['prediction'] == actual_result
            handicap_correct = prediction['home_handicap'] == actual_handicap
            over_under_correct = prediction['over_under'] == actual_over_under
            
            results['match_result']['correct'] += match_correct
            results['match_result']['total'] += 1
            results['handicap']['correct'] += handicap_correct
            results['handicap']['total'] += 1
            results['over_under']['correct'] += over_under_correct
            results['over_under']['total'] += 1
            
            # High confidence (>60%)
            if prediction['confidence'] > 0.6:
                results['high_confidence']['correct'] += match_correct
                results['high_confidence']['total'] += 1
            
            # แสดงผล
            status_match = "✅" if match_correct else "❌"
            status_handicap = "✅" if handicap_correct else "❌"
            status_over_under = "✅" if over_under_correct else "❌"
            
            print(f"{i:2d}. {home_team:<20} {home_goals}-{away_goals} {away_team:<20}")
            print(f"    ทำนาย: {prediction['prediction']:<8} {status_match} | "
                  f"Handicap: {prediction['home_handicap']:<8} {status_handicap} | "
                  f"O/U: {prediction['over_under']:<8} {status_over_under} | "
                  f"มั่นใจ: {prediction['confidence']:.1%}")
            
            results['predictions'].append({
                'home_team': home_team,
                'away_team': away_team,
                'home_goals': home_goals,
                'away_goals': away_goals,
                'prediction': prediction,
                'actual_result': actual_result,
                'match_correct': match_correct,
                'handicap_correct': handicap_correct,
                'over_under_correct': over_under_correct
            })
        
        return results
    
    def print_backtest_summary(self, results: Dict):
        """แสดงสรุปผลการทดสอบ"""
        print("\n" + "=" * 60)
        print("🏆 สรุปผลการทดสอบย้อนหลัง J-League 2")
        print("=" * 60)
        
        # คำนวณเปอร์เซ็นต์
        match_accuracy = (results['match_result']['correct'] / results['match_result']['total']) * 100
        handicap_accuracy = (results['handicap']['correct'] / results['handicap']['total']) * 100
        over_under_accuracy = (results['over_under']['correct'] / results['over_under']['total']) * 100
        
        print(f"📊 **ผลการแข่งขัน**: {results['match_result']['correct']}/{results['match_result']['total']} = {match_accuracy:.1f}%")
        print(f"🎯 **Handicap**: {results['handicap']['correct']}/{results['handicap']['total']} = {handicap_accuracy:.1f}%")
        print(f"⚽ **Over/Under**: {results['over_under']['correct']}/{results['over_under']['total']} = {over_under_accuracy:.1f}%")
        
        if results['high_confidence']['total'] > 0:
            high_conf_accuracy = (results['high_confidence']['correct'] / results['high_confidence']['total']) * 100
            print(f"🔥 **เมื่อมั่นใจสูง (>60%)**: {results['high_confidence']['correct']}/{results['high_confidence']['total']} = {high_conf_accuracy:.1f}%")
        
        # เปรียบเทียบกับระบบเดิม
        print(f"\n📈 **เปรียบเทียบกับระบบเดิม**:")
        print(f"   ระบบเดิม: 60.0% | ระบบใหม่: {match_accuracy:.1f}% | ผลต่าง: {match_accuracy-60:.1f}%")
        
        # ระดับประสิทธิภาพ
        if match_accuracy >= 65:
            level = "🥇 ยอดเยี่ยม"
        elif match_accuracy >= 60:
            level = "🥈 ดีมาก"
        elif match_accuracy >= 55:
            level = "🥉 ดี"
        else:
            level = "📈 ต้องปรับปรุง"
        
        print(f"🏆 **ระดับประสิทธิภาพ**: {level}")
    
    def get_today_matches(self) -> List[Dict]:
        """ดึงการแข่งขันวันนี้"""
        print(f"\n📅 ค้นหาการแข่งขันวันนี้ ({datetime.now().strftime('%Y-%m-%d')})...")
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        params = {
            'league': self.league_id,
            'season': self.season,
            'date': today
        }
        
        data = self.make_api_request('fixtures', params)
        
        if 'response' in data and data['response']:
            matches = data['response']
            print(f"⚽ พบการแข่งขันวันนี้ {len(matches)} นัด")
            return matches
        else:
            print("😔 ไม่มีการแข่งขันวันนี้")
            
            # ลองหาการแข่งขันที่ใกล้ที่สุด
            print("🔍 ค้นหาการแข่งขันที่ใกล้ที่สุด...")
            
            for i in range(1, 8):  # ค้นหา 7 วันข้างหน้า
                future_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
                params['date'] = future_date
                
                data = self.make_api_request('fixtures', params)
                if 'response' in data and data['response']:
                    matches = data['response']
                    print(f"⚽ พบการแข่งขันวันที่ {future_date}: {len(matches)} นัด")
                    return matches
            
            return []
    
    def predict_today_matches(self, matches: List[Dict]):
        """ทำนายการแข่งขันวันนี้"""
        if not matches:
            print("❌ ไม่มีการแข่งขันให้ทำนาย")
            return
        
        print(f"\n🔮 การทำนายการแข่งขัน J-League 2")
        print("=" * 80)
        
        for i, match in enumerate(matches, 1):
            home_team = match['teams']['home']['name']
            away_team = match['teams']['away']['name']
            match_date = match['fixture']['date']
            venue = match['fixture']['venue']['name'] if match['fixture']['venue'] else "ไม่ระบุ"
            
            # ทำนาย
            prediction = self.predict_match(home_team, away_team)
            
            print(f"\n🏟️  **นัดที่ {i}**: {home_team} vs {away_team}")
            print(f"📅 **วันเวลา**: {match_date}")
            print(f"🏟️  **สนาม**: {venue}")
            print(f"⭐ **ELO Rating**: {home_team} ({prediction['home_rating']:.0f}) vs {away_team} ({prediction['away_rating']:.0f})")
            
            print(f"\n🎯 **การทำนาย 4 ค่า**:")
            print(f"   1️⃣ **ผลการแข่งขัน**: {prediction['prediction']} ({prediction['confidence']:.1%})")
            print(f"   2️⃣ **Handicap**: {prediction['home_handicap']}")
            print(f"   3️⃣ **Over/Under**: {prediction['over_under']}")
            
            # คำนวณ Value Bet (สมมติ)
            if prediction['confidence'] > 0.6:
                value_status = "🔥 **High Value**"
            elif prediction['confidence'] > 0.5:
                value_status = "✅ **Good Value**"
            else:
                value_status = "⚠️  **Low Value**"
            
            print(f"   4️⃣ **Value Bet**: {value_status}")
            
            print(f"\n📊 **ความน่าจะเป็น**:")
            print(f"   🏠 {home_team} ชนะ: {prediction['home_win_prob']:.1%}")
            print(f"   🤝 เสมอ: {prediction['draw_prob']:.1%}")
            print(f"   ✈️  {away_team} ชนะ: {prediction['away_win_prob']:.1%}")
            
            if prediction['confidence'] > 0.6:
                print(f"\n💡 **คำแนะนำ**: การทำนายนี้มีความมั่นใจสูง แนะนำให้พิจารณาลงเดิมพัน")
            
            print("-" * 80)

def main():
    # API Key
    API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    print("🚀 J-League 2 Ultra Advanced Predictor")
    print("=" * 50)
    
    # สร้าง predictor
    predictor = JLeague2Predictor(API_KEY)
    
    # ดึงข้อมูลการแข่งขัน
    finished_fixtures, upcoming_fixtures = predictor.load_fixtures_data()
    
    if not finished_fixtures:
        print("❌ ไม่สามารถดึงข้อมูลได้")
        return
    
    # ทำ backtest
    results = predictor.backtest_last_matches(finished_fixtures, 20)
    predictor.print_backtest_summary(results)
    
    # ทำนายการแข่งขันวันนี้
    today_matches = predictor.get_today_matches()
    predictor.predict_today_matches(today_matches)
    
    print(f"\n🎉 การวิเคราะห์เสร็จสิ้น!")
    print(f"📊 ระบบใช้ข้อมูล {len(finished_fixtures)} นัดในการคำนวณ ELO Rating")
    print(f"🔬 ทดสอบย้อนหลัง 20 นัดล่าสุด")
    print(f"🔮 ทำนายการแข่งขันที่จะมาถึง")

if __name__ == "__main__":
    main()
