#!/usr/bin/env python3
"""
🔑 ทดสอบดึงข้อมูลจริงด้วย API Key
ทดสอบทั้ง Premier League และ La Liga
"""

import requests
import pandas as pd
import json
import time
from datetime import datetime

class RealDataTester:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {'X-Auth-Token': self.api_key}
        
    def test_api_connection(self):
        """ทดสอบการเชื่อมต่อ API"""
        print("🔑 ทดสอบการเชื่อมต่อ API...")
        print(f"API Key: {self.api_key}")
        
        try:
            # ทดสอบด้วย competitions endpoint
            url = f"{self.base_url}/competitions"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                competitions = data.get('competitions', [])
                print(f"✅ API ทำงานได้! พบ {len(competitions)} รายการแข่งขัน")
                
                # แสดงลีกที่สำคัญ
                important_leagues = ['PL', 'PD', 'BL1', 'SA', 'FL1']
                print(f"\n🏆 ลีกสำคัญที่มีข้อมูล:")
                
                for comp in competitions:
                    if comp['code'] in important_leagues:
                        print(f"   {comp['code']}: {comp['name']} ({comp['area']['name']})")
                
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return False
    
    def get_premier_league_real_data(self):
        """ดึงข้อมูล Premier League จริง"""
        print(f"\n🏴󠁧󠁢󠁥󠁮󠁧󠁿 กำลังดึงข้อมูล Premier League จริง...")
        
        try:
            url = f"{self.base_url}/competitions/PL/matches"
            params = {
                'season': 2024,
                'status': 'FINISHED'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            print(f"📊 Premier League Response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                matches = self._process_matches_data(data, 'Premier League')
                
                if matches:
                    df = pd.DataFrame(matches)
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.sort_values('date').reset_index(drop=True)
                    
                    print(f"✅ ดึงข้อมูล Premier League สำเร็จ: {len(df)} เกม")
                    
                    # บันทึกข้อมูล
                    df.to_csv('premier_league_real_data.csv', index=False)
                    print(f"💾 บันทึก: premier_league_real_data.csv")
                    
                    # แสดงตัวอย่าง
                    print(f"\n📋 ตัวอย่างข้อมูล Premier League:")
                    print(df.head())
                    
                    return df
                else:
                    print("❌ ไม่พบข้อมูลการแข่งขัน Premier League")
                    return None
            else:
                print(f"❌ Premier League API Error: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            print(f"❌ Premier League Error: {e}")
            return None
    
    def get_laliga_real_data(self):
        """ดึงข้อมูล La Liga จริง"""
        print(f"\n🇪🇸 กำลังดึงข้อมูล La Liga จริง...")
        
        try:
            url = f"{self.base_url}/competitions/PD/matches"
            params = {
                'season': 2024,
                'status': 'FINISHED'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            print(f"📊 La Liga Response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                matches = self._process_matches_data(data, 'La Liga')
                
                if matches:
                    df = pd.DataFrame(matches)
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.sort_values('date').reset_index(drop=True)
                    
                    print(f"✅ ดึงข้อมูล La Liga สำเร็จ: {len(df)} เกม")
                    
                    # บันทึกข้อมูล
                    df.to_csv('laliga_real_data.csv', index=False)
                    print(f"💾 บันทึก: laliga_real_data.csv")
                    
                    # แสดงตัวอย่าง
                    print(f"\n📋 ตัวอย่างข้อมูล La Liga:")
                    print(df.head())
                    
                    return df
                else:
                    print("❌ ไม่พบข้อมูลการแข่งขัน La Liga")
                    return None
            else:
                print(f"❌ La Liga API Error: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            print(f"❌ La Liga Error: {e}")
            return None
    
    def _process_matches_data(self, data, league_name):
        """ประมวลผลข้อมูลจาก API"""
        matches = []
        
        for match in data.get('matches', []):
            if (match['status'] == 'FINISHED' and 
                match['score']['fullTime']['home'] is not None):
                
                matches.append({
                    'date': match['utcDate'][:10],
                    'home_team': match['homeTeam']['name'],
                    'away_team': match['awayTeam']['name'],
                    'home_goals': match['score']['fullTime']['home'],
                    'away_goals': match['score']['fullTime']['away'],
                    'matchday': match.get('matchday', 0),
                    'season': match.get('season', {}).get('id', 2024),
                    'league': league_name
                })
        
        return matches
    
    def analyze_real_data(self, df, league_name):
        """วิเคราะห์ข้อมูลจริง"""
        if df is None or len(df) == 0:
            return
        
        print(f"\n📊 การวิเคราะห์ข้อมูล {league_name}:")
        print("=" * 50)
        
        print(f"📈 จำนวนเกม: {len(df)}")
        print(f"📅 ช่วงเวลา: {df['date'].min()} ถึง {df['date'].max()}")
        
        # ทีมที่มีข้อมูล
        all_teams = set(df['home_team'].unique()) | set(df['away_team'].unique())
        print(f"🏆 จำนวนทีม: {len(all_teams)}")
        
        # สถิติประตู
        total_goals = df['home_goals'].sum() + df['away_goals'].sum()
        avg_goals = total_goals / len(df)
        print(f"⚽ ประตูเฉลี่ย: {avg_goals:.2f} ต่อเกม")
        
        # ผลการแข่งขัน
        home_wins = len(df[df['home_goals'] > df['away_goals']])
        draws = len(df[df['home_goals'] == df['away_goals']])
        away_wins = len(df[df['home_goals'] < df['away_goals']])
        
        print(f"🏠 เจ้าบ้านชนะ: {home_wins} ({home_wins/len(df)*100:.1f}%)")
        print(f"🤝 เสมอ: {draws} ({draws/len(df)*100:.1f}%)")
        print(f"✈️ ทีมเยือนชนะ: {away_wins} ({away_wins/len(df)*100:.1f}%)")
        
        # แสดงทีม
        print(f"\n🏆 ทีมใน {league_name}:")
        for i, team in enumerate(sorted(all_teams), 1):
            print(f"   {i:2d}. {team}")
    
    def compare_with_mock_data(self):
        """เปรียบเทียบกับข้อมูลจำลอง"""
        print(f"\n🔍 เปรียบเทียบข้อมูลจริง vs จำลอง:")
        print("=" * 50)
        
        # ตรวจสอบไฟล์ที่มี
        import os
        
        files_check = {
            'premier_league_real_data.csv': 'Premier League (จริง)',
            'laliga_real_data.csv': 'La Liga (จริง)',
            'laliga_realistic_matches.csv': 'La Liga (จำลอง)'
        }
        
        for filename, description in files_check.items():
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                print(f"✅ {description}: {len(df)} เกม")
            else:
                print(f"❌ {description}: ไม่พบไฟล์")

def main():
    """ฟังก์ชันหลัก"""
    print("🔑 Real API Data Tester")
    print("📡 ทดสอบดึงข้อมูลจริงจาก football-data.org")
    print("=" * 70)
    
    # API Key ที่ได้รับ
    api_key = "052fd4885cf943ad859c89cef542e2e5"
    
    tester = RealDataTester(api_key)
    
    # ทดสอบการเชื่อมต่อ
    if not tester.test_api_connection():
        print("❌ ไม่สามารถเชื่อมต่อ API ได้")
        return
    
    print(f"\n" + "="*70)
    
    # ดึงข้อมูล Premier League
    pl_data = tester.get_premier_league_real_data()
    if pl_data is not None:
        tester.analyze_real_data(pl_data, "Premier League")
    
    print(f"\n" + "="*70)
    
    # รอสักครู่เพื่อไม่ให้เกิน Rate Limit
    print("⏰ รอ 2 วินาที เพื่อไม่ให้เกิน Rate Limit...")
    time.sleep(2)
    
    # ดึงข้อมูล La Liga
    laliga_data = tester.get_laliga_real_data()
    if laliga_data is not None:
        tester.analyze_real_data(laliga_data, "La Liga")
    
    # เปรียบเทียบ
    tester.compare_with_mock_data()
    
    print(f"\n" + "="*70)
    print("🎉 การทดสอบเสร็จสิ้น!")
    
    if pl_data is not None or laliga_data is not None:
        print("✅ ดึงข้อมูลจริงสำเร็จ!")
        print("🎯 พร้อมใช้งานกับ Predictor")
    else:
        print("❌ ไม่สามารถดึงข้อมูลได้")
        print("💡 ตรวจสอบ API Key หรือ Rate Limit")

if __name__ == "__main__":
    main()
