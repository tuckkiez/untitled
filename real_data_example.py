#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ตัวอย่างการใช้งานกับข้อมูลจริงจาก API
สำหรับใช้งานจริงกับข้อมูลฟุตบอลจาก football-data.org
"""

import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from football_predictor import FootballPredictor
from data_loader import FootballDataLoader

class RealDataPredictor:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.predictor = FootballPredictor()
        self.data_loader = FootballDataLoader()
        
    def get_premier_league_data(self, season=2024):
        """ดึงข้อมูลพรีเมียร์ลีกจาก API"""
        if not self.api_key:
            print("ต้องการ API key จาก football-data.org")
            print("สมัครได้ที่: https://www.football-data.org/client/register")
            return None
        
        headers = {'X-Auth-Token': self.api_key}
        
        try:
            # ดึงข้อมูลการแข่งขันที่จบแล้ว
            url = "https://api.football-data.org/v4/competitions/PL/matches"
            params = {
                'season': season,
                'status': 'FINISHED'
            }
            
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
                            'away_goals': match['score']['fullTime']['away'],
                            'matchday': match['matchday']
                        })
                
                df = pd.DataFrame(matches)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                
                print(f"ดึงข้อมูลสำเร็จ: {len(df)} เกม")
                return df
                
            elif response.status_code == 429:
                print("API rate limit exceeded. กรุณารอสักครู่แล้วลองใหม่")
                return None
            else:
                print(f"API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_upcoming_matches(self, days_ahead=7):
        """ดึงข้อมูลการแข่งขันที่กำลังจะมาถึง"""
        if not self.api_key:
            return None
        
        headers = {'X-Auth-Token': self.api_key}
        
        try:
            url = "https://api.football-data.org/v4/competitions/PL/matches"
            params = {
                'status': 'SCHEDULED',
                'dateFrom': datetime.now().strftime('%Y-%m-%d'),
                'dateTo': (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                upcoming = []
                
                for match in data.get('matches', []):
                    upcoming.append({
                        'date': match['utcDate'][:10],
                        'time': match['utcDate'][11:16],
                        'home_team': match['homeTeam']['name'],
                        'away_team': match['awayTeam']['name'],
                        'matchday': match['matchday']
                    })
                
                return pd.DataFrame(upcoming)
            else:
                print(f"API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def predict_upcoming_matches(self, historical_data, upcoming_matches):
        """ทำนายผลการแข่งขันที่กำลังจะมาถึง"""
        if historical_data is None or upcoming_matches is None:
            return None
        
        # เทรนโมเดล
        print("กำลังเทรนโมเดลด้วยข้อมูลจริง...")
        if not self.predictor.train(historical_data):
            return None
        
        predictions = []
        
        print("\n=== การทำนายการแข่งขันที่กำลังจะมาถึง ===")
        for _, match in upcoming_matches.iterrows():
            result = self.predictor.predict_match(
                match['home_team'], 
                match['away_team'], 
                historical_data
            )
            
            if result:
                predictions.append({
                    'date': match['date'],
                    'time': match['time'],
                    'home_team': match['home_team'],
                    'away_team': match['away_team'],
                    'prediction': result['prediction'],
                    'confidence': result['confidence'],
                    'home_win_prob': result['probabilities']['Home Win'],
                    'draw_prob': result['probabilities']['Draw'],
                    'away_win_prob': result['probabilities']['Away Win']
                })
                
                print(f"\n{match['date']} {match['time']}")
                print(f"{match['home_team']} vs {match['away_team']}")
                print(f"การทำนาย: {result['prediction']}")
                print(f"ความมั่นใจ: {result['confidence']:.3f}")
                print("ความน่าจะเป็น:")
                for outcome, prob in result['probabilities'].items():
                    print(f"  {outcome}: {prob:.3f} ({prob*100:.1f}%)")
        
        return pd.DataFrame(predictions)
    
    def save_predictions_to_csv(self, predictions, filename="predictions.csv"):
        """บันทึกการทำนายลงไฟล์ CSV"""
        if predictions is not None and len(predictions) > 0:
            predictions.to_csv(filename, index=False)
            print(f"\nบันทึกการทำนายใน {filename}")
    
    def run_real_prediction(self, api_key, season=2024):
        """รันการทำนายด้วยข้อมูลจริง"""
        self.api_key = api_key
        
        print("=== ระบบทำนายฟุตบอลด้วยข้อมูลจริง ===")
        
        # ดึงข้อมูลประวัติการแข่งขัน
        print("กำลังดึงข้อมูลประวัติการแข่งขัน...")
        historical_data = self.get_premier_league_data(season)
        
        if historical_data is None:
            print("ไม่สามารถดึงข้อมูลได้")
            return None
        
        # ดึงข้อมูลการแข่งขันที่กำลังจะมาถึง
        print("กำลังดึงข้อมูลการแข่งขันที่กำลังจะมาถึง...")
        upcoming_matches = self.get_upcoming_matches(days_ahead=14)
        
        if upcoming_matches is None or len(upcoming_matches) == 0:
            print("ไม่มีการแข่งขันที่กำลังจะมาถึง")
            return None
        
        print(f"พบการแข่งขัน {len(upcoming_matches)} นัดในอีก 14 วันข้างหน้า")
        
        # ทำนายผล
        predictions = self.predict_upcoming_matches(historical_data, upcoming_matches)
        
        # บันทึกผล
        if predictions is not None:
            self.save_predictions_to_csv(predictions, "real_predictions.csv")
        
        return {
            'historical_data': historical_data,
            'upcoming_matches': upcoming_matches,
            'predictions': predictions
        }

def demo_with_sample_api_key():
    """ตัวอย่างการใช้งาน (ต้องใส่ API key จริง)"""
    print("=== ตัวอย่างการใช้งานกับข้อมูลจริง ===")
    print("หมายเหตุ: ต้องมี API key จาก football-data.org")
    print("สมัครได้ที่: https://www.football-data.org/client/register")
    print()
    
    # ตัวอย่างโค้ดสำหรับใช้งานจริง
    sample_code = '''
# วิธีใช้งานจริง:
predictor = RealDataPredictor()
api_key = "YOUR_API_KEY_HERE"  # ใส่ API key ของคุณ

results = predictor.run_real_prediction(api_key, season=2024)

if results:
    print("การทำนายเสร็จสิ้น!")
    print(f"ข้อมูลประวัติ: {len(results['historical_data'])} เกม")
    print(f"การแข่งขันที่กำลังจะมาถึง: {len(results['upcoming_matches'])} นัด")
    if results['predictions'] is not None:
        print(f"การทำนาย: {len(results['predictions'])} นัด")
'''
    
    print(sample_code)

if __name__ == "__main__":
    demo_with_sample_api_key()
