#!/usr/bin/env python3
"""
🇪🇸 Simple La Liga Predictor
ระบบทำนายลีกสเปนแยกต่างหาก (ใช้โครงสร้างเดียวกับ Ultra Advanced)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Copy โครงสร้างจาก Ultra Advanced Predictor
class SimpleLaLigaPredictor:
    def __init__(self):
        self.team_ratings = {}
        self.historical_data = None
        
    def load_laliga_data(self):
        """โหลดข้อมูล La Liga (จำลอง)"""
        print("🇪🇸 กำลังโหลดข้อมูล La Liga...")
        
        # ทีมใน La Liga
        teams = [
            'Real Madrid', 'FC Barcelona', 'Atletico Madrid', 'Athletic Bilbao',
            'Real Sociedad', 'Real Betis', 'Villarreal CF', 'Valencia CF',
            'Sevilla FC', 'RC Celta', 'CA Osasuna', 'Getafe CF',
            'UD Las Palmas', 'Girona FC', 'Rayo Vallecano', 'RCD Espanyol',
            'Deportivo Alaves', 'Real Valladolid', 'CD Leganes', 'RCD Mallorca'
        ]
        
        matches = []
        
        # สร้างข้อมูลจำลอง 200 เกม
        for i in range(200):
            home_team = np.random.choice(teams)
            away_team = np.random.choice([t for t in teams if t != home_team])
            
            # ความแข็งแกร่งของทีม
            home_strength = self._get_team_strength(home_team)
            away_strength = self._get_team_strength(away_team)
            
            # Home advantage
            home_strength += 0.3
            
            # คำนวณประตู
            home_goals = max(0, int(np.random.poisson(home_strength)))
            away_goals = max(0, int(np.random.poisson(away_strength)))
            
            # สร้างวันที่
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
        
        self.historical_data = data
        return data
    
    def _get_team_strength(self, team):
        """ความแข็งแกร่งของทีม La Liga"""
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
        """คำนวณ ELO Rating สำหรับ La Liga"""
        print("🏆 กำลังคำนวณ ELO Ratings สำหรับ La Liga...")
        
        teams = set(matches_df['home_team'].unique()) | set(matches_df['away_team'].unique())
        elo_ratings = {team: 1500 for team in teams}
        
        K = 32
        
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
    
    def predict_match_laliga(self, home_team, away_team):
        """ทำนายการแข่งขัน La Liga (แบบง่าย)"""
        print(f"🔧 กำลังทำนาย {home_team} vs {away_team}...")
        
        if not self.team_ratings:
            print("❌ ยังไม่ได้คำนวณ ELO Ratings")
            return None
        
        # ดึง ELO ratings
        home_elo = self.team_ratings.get(home_team, 1500)
        away_elo = self.team_ratings.get(away_team, 1500)
        
        # Home advantage
        home_elo += 100
        
        # คำนวณความน่าจะเป็น
        home_expected = 1 / (1 + 10**((away_elo - home_elo) / 400))
        away_expected = 1 - home_expected
        draw_prob = 0.25  # โอกาสเสมอ
        
        # ปรับให้รวมเป็น 1
        total_prob = home_expected + away_expected + draw_prob
        home_prob = home_expected / total_prob
        away_prob = away_expected / total_prob
        draw_prob = draw_prob / total_prob
        
        # ทำนายผล
        if home_prob > away_prob and home_prob > draw_prob:
            prediction = "Home Win"
            confidence = home_prob
        elif away_prob > home_prob and away_prob > draw_prob:
            prediction = "Away Win"
            confidence = away_prob
        else:
            prediction = "Draw"
            confidence = draw_prob
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'probabilities': {
                'Home Win': home_prob,
                'Draw': draw_prob,
                'Away Win': away_prob
            }
        }

def test_simple_laliga():
    """ทดสอบระบบ La Liga แบบง่าย"""
    print("🇪🇸 ทดสอบ Simple La Liga Predictor")
    print("=" * 50)
    
    # สร้าง predictor
    predictor = SimpleLaLigaPredictor()
    
    # โหลดข้อมูล
    data = predictor.load_laliga_data()
    
    # คำนวณ ELO
    predictor.calculate_elo_ratings(data)
    
    # แสดง Top 5 ทีม
    print(f"\n🏆 Top 5 ทีมแข็งแกร่งที่สุด (ELO Rating):")
    sorted_teams = sorted(predictor.team_ratings.items(), key=lambda x: x[1], reverse=True)
    for i, (team, rating) in enumerate(sorted_teams[:5]):
        print(f"   {i+1}. {team}: {rating:.0f}")
    
    # ทดสอบการทำนาย
    print(f"\n🎯 ทดสอบการทำนาย:")
    test_matches = [
        ('Real Madrid', 'FC Barcelona'),
        ('Atletico Madrid', 'Real Sociedad'),
        ('Sevilla FC', 'Valencia CF'),
        ('Athletic Bilbao', 'Real Betis')
    ]
    
    results = []
    
    for home, away in test_matches:
        result = predictor.predict_match_laliga(home, away)
        if result:
            results.append(result)
            print(f"\n⚽ {home} vs {away}")
            print(f"   🎯 ทำนาย: {result['prediction']} ({result['confidence']:.1%})")
            
            probs = result['probabilities']
            print(f"   📊 {home}: {probs['Home Win']:.1%} | เสมอ: {probs['Draw']:.1%} | {away}: {probs['Away Win']:.1%}")
    
    # สรุป
    if results:
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        print(f"\n📊 สรุป:")
        print(f"   ✅ ทำนายสำเร็จ: {len(results)} คู่")
        print(f"   📈 ความมั่นใจเฉลี่ย: {avg_confidence:.1%}")
        
        if avg_confidence > 0.4:
            print(f"   🎉 ระบบ La Liga ทำงานได้ดี!")
        else:
            print(f"   ⚠️ ต้องปรับปรุงเพิ่มเติม")
    
    return predictor

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Simple La Liga Predictor")
    print("🇪🇸 ระบบทำนายลีกสเปนแยกต่างหาก")
    print("=" * 60)
    
    # ทดสอบระบบ
    predictor = test_simple_laliga()
    
    print(f"\n✅ ระบบ La Liga Predictor พร้อมใช้งาน!")
    print(f"📝 ระบบนี้แยกต่างหากจาก Premier League")
    print(f"🔧 ใช้โครงสร้างเดียวกัน แต่ข้อมูลต่างกัน")
    
    return predictor

if __name__ == "__main__":
    predictor = main()
