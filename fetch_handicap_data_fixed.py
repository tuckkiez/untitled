#!/usr/bin/env python3
"""
🚀 Fetch Handicap Data from API-Football (Fixed) - July 17-18, 2025
ดึงข้อมูล handicap จาก API-Football (แก้ไขแล้ว)
"""

import requests
import json
import os
import time
from datetime import datetime

class HandicapDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        self.output_dir = "api_data/handicap_data"
        
        # สร้างโฟลเดอร์สำหรับเก็บข้อมูล
        os.makedirs(self.output_dir, exist_ok=True)
    
    def fetch_odds(self, fixture_id):
        """ดึงข้อมูลอัตราต่อรองของการแข่งขัน"""
        url = f"{self.base_url}/odds"
        params = {
            'fixture': str(fixture_id),
            'bookmaker': '8',  # bet365
            'bet': '4'  # Asian Handicap
        }
        
        print(f"📊 กำลังดึงข้อมูล handicap ของการแข่งขัน {fixture_id}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/handicap_{fixture_id}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ บันทึกข้อมูลลงไฟล์: {filename}")
                return data
            else:
                print(f"❌ เกิดข้อผิดพลาด: {response.status_code}")
                print(f"ข้อความ: {response.text}")
                return None
        
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            return None
    
    def extract_handicap_data(self, odds_data):
        """แยกข้อมูล handicap จากข้อมูลอัตราต่อรอง"""
        if not odds_data or 'response' not in odds_data or not odds_data['response']:
            return {
                "handicap": {
                    "line": 0,
                    "home_prob": 50.0,
                    "away_prob": 50.0,
                    "prediction": "No Handicap",
                    "confidence": 50.0
                }
            }
        
        handicap_data = {
            "handicap": {
                "line": 0,
                "home_prob": 50.0,
                "away_prob": 50.0,
                "prediction": "No Handicap",
                "confidence": 50.0
            }
        }
        
        try:
            for bookmaker_data in odds_data['response']:
                if 'bookmakers' not in bookmaker_data:
                    continue
                
                for bookmaker in bookmaker_data['bookmakers']:
                    if bookmaker['id'] != 8:  # bet365
                        continue
                    
                    for bet in bookmaker['bets']:
                        if bet['id'] != 4:  # Asian Handicap
                            continue
                        
                        # ค้นหา handicap ที่ใกล้เคียง 0 มากที่สุด
                        best_handicap = None
                        best_handicap_value = 999
                        
                        for value in bet['values']:
                            if 'Home' in value['value']:
                                try:
                                    handicap_parts = value['value'].split(' ')
                                    if len(handicap_parts) > 1:
                                        handicap_value = float(handicap_parts[0])
                                        if abs(handicap_value) < abs(best_handicap_value):
                                            best_handicap = value
                                            best_handicap_value = handicap_value
                                except:
                                    continue
                        
                        if best_handicap:
                            handicap_value = float(best_handicap['value'].split(' ')[0])
                            home_odd = float(best_handicap['odd'])
                            
                            # หา away odd
                            away_odd = 0
                            for v in bet['values']:
                                if 'Away' in v['value'] and abs(handicap_value) in v['value']:
                                    try:
                                        away_odd = float(v['odd'])
                                        break
                                    except:
                                        continue
                            
                            if away_odd == 0:
                                away_odd = 2.0
                            
                            # คำนวณความน่าจะเป็น
                            home_prob = 1 / home_odd
                            away_prob = 1 / away_odd
                            
                            # ปรับให้ผลรวมเป็น 1
                            total = home_prob + away_prob
                            home_prob /= total
                            away_prob /= total
                            
                            # สร้างข้อมูล handicap
                            handicap_data['handicap'] = {
                                "line": handicap_value,
                                "home_prob": round(home_prob * 100, 1),
                                "away_prob": round(away_prob * 100, 1),
                                "prediction": f"Home {handicap_value}" if home_prob > away_prob else f"Away +{abs(handicap_value)}",
                                "confidence": round(max(home_prob, away_prob) * 100, 1)
                            }
                            
                            return handicap_data
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการแยกข้อมูล handicap: {e}")
        
        return handicap_data
    
    def fetch_and_extract_handicap(self, fixture_id):
        """ดึงและแยกข้อมูล handicap"""
        odds_data = self.fetch_odds(fixture_id)
        return self.extract_handicap_data(odds_data)

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Fetch Handicap Data from API-Football (Fixed) - July 17-18, 2025")
    print("=" * 60)
    
    # API key
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # สร้าง fetcher
    fetcher = HandicapDataFetcher(api_key)
    
    # โหลดข้อมูลการแข่งขัน
    try:
        with open('uefa_competitions_real_data_analysis.json', 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # ดึงข้อมูล handicap สำหรับแต่ละการแข่งขัน
        for match in analysis_data['europa_league']:
            fixture_id = match['fixture_id']
            handicap_data = fetcher.fetch_and_extract_handicap(fixture_id)
            match['handicap'] = handicap_data['handicap']
            time.sleep(1)
        
        for match in analysis_data['conference_league']:
            fixture_id = match['fixture_id']
            handicap_data = fetcher.fetch_and_extract_handicap(fixture_id)
            match['handicap'] = handicap_data['handicap']
            time.sleep(1)
        
        # บันทึกข้อมูล
        with open('uefa_competitions_real_data_analysis_with_handicap.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 บันทึกข้อมูลลงไฟล์: uefa_competitions_real_data_analysis_with_handicap.json")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
    
    print("\n✅ เสร็จสมบูรณ์!")

if __name__ == "__main__":
    main()
