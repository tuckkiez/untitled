#!/usr/bin/env python3
"""
🇪🇸 La Liga Real Data Collector
ดึงข้อมูล La Liga จริงจาก football-data.org API
"""

import requests
import pandas as pd
import json
from datetime import datetime
import time

class LaLigaRealDataCollector:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {'X-Auth-Token': self.api_key} if api_key else {}
        
    def get_laliga_matches(self, season=2024):
        """ดึงข้อมูลการแข่งขัน La Liga จริง"""
        print("🇪🇸 กำลังดึงข้อมูล La Liga จาก football-data.org...")
        
        if not self.api_key:
            print("⚠️ ไม่มี API Key - ลองใช้ Free API")
            return self._try_free_api()
        
        try:
            # La Liga competition code: PD (Primera División)
            url = f"{self.base_url}/competitions/PD/matches"
            params = {
                'season': season,
                'status': 'FINISHED'
            }
            
            print(f"📡 กำลังเรียก API: {url}")
            print(f"🔑 Headers: {self.headers}")
            print(f"📋 Parameters: {params}")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                matches = self._process_matches_data(data)
                
                if matches:
                    df = pd.DataFrame(matches)
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.sort_values('date').reset_index(drop=True)
                    
                    print(f"✅ ดึงข้อมูล La Liga สำเร็จ: {len(df)} เกม")
                    
                    # บันทึกข้อมูล
                    df.to_csv('laliga_real_matches.csv', index=False)
                    print(f"💾 บันทึกไฟล์: laliga_real_matches.csv")
                    
                    return df
                else:
                    print("❌ ไม่พบข้อมูลการแข่งขัน")
                    return None
                    
            elif response.status_code == 403:
                print("❌ API Key ไม่ถูกต้องหรือหมดอายุ")
                print("💡 ลองใช้ Free API แทน...")
                return self._try_free_api()
                
            elif response.status_code == 429:
                print("⏰ เกิน Rate Limit - รอ 60 วินาที...")
                time.sleep(60)
                return self.get_laliga_matches(season)
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"📄 Response: {response.text[:500]}")
                return self._try_free_api()
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout - ลองใหม่...")
            return self._try_free_api()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._try_free_api()
    
    def _try_free_api(self):
        """ลองใช้ Free API (v2)"""
        print("🆓 ลองใช้ Free API (v2)...")
        
        try:
            # ใช้ v2 API ที่เป็น free
            url = "https://api.football-data.org/v2/competitions/PD/matches"
            params = {
                'season': 2024,
                'status': 'FINISHED'
            }
            
            # ไม่ใส่ API key สำหรับ free tier
            response = requests.get(url, params=params, timeout=30)
            
            print(f"📊 Free API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                matches = self._process_matches_data_v2(data)
                
                if matches:
                    df = pd.DataFrame(matches)
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.sort_values('date').reset_index(drop=True)
                    
                    print(f"✅ ดึงข้อมูล La Liga (Free API) สำเร็จ: {len(df)} เกม")
                    
                    # บันทึกข้อมูล
                    df.to_csv('laliga_real_matches.csv', index=False)
                    print(f"💾 บันทึกไฟล์: laliga_real_matches.csv")
                    
                    return df
                else:
                    print("❌ ไม่พบข้อมูลการแข่งขัน (Free API)")
                    return None
            else:
                print(f"❌ Free API Error: {response.status_code}")
                print(f"📄 Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            print(f"❌ Free API Error: {e}")
            return None
    
    def _process_matches_data(self, data):
        """ประมวลผลข้อมูลจาก API v4"""
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
                    'season': match.get('season', {}).get('id', 2024)
                })
        
        return matches
    
    def _process_matches_data_v2(self, data):
        """ประมวลผลข้อมูลจาก API v2"""
        matches = []
        
        for match in data.get('matches', []):
            if (match['status'] == 'FINISHED' and 
                match['score']['fullTime']['homeTeam'] is not None):
                
                matches.append({
                    'date': match['utcDate'][:10],
                    'home_team': match['homeTeam']['name'],
                    'away_team': match['awayTeam']['name'],
                    'home_goals': match['score']['fullTime']['homeTeam'],
                    'away_goals': match['score']['fullTime']['awayTeam'],
                    'matchday': match.get('matchday', 0),
                    'season': 2024
                })
        
        return matches
    
    def get_laliga_teams(self):
        """ดึงรายชื่อทีมใน La Liga"""
        print("🏆 กำลังดึงรายชื่อทีม La Liga...")
        
        try:
            url = f"{self.base_url}/competitions/PD/teams"
            
            if self.api_key:
                response = requests.get(url, headers=self.headers, timeout=30)
            else:
                # ลอง v2 API
                url = "https://api.football-data.org/v2/competitions/PD/teams"
                response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                teams = []
                
                for team in data.get('teams', []):
                    teams.append({
                        'name': team['name'],
                        'short_name': team.get('shortName', team['name']),
                        'founded': team.get('founded', 0),
                        'venue': team.get('venue', 'Unknown')
                    })
                
                df = pd.DataFrame(teams)
                print(f"✅ ดึงข้อมูลทีม La Liga สำเร็จ: {len(df)} ทีม")
                
                # บันทึกข้อมูล
                df.to_csv('laliga_teams.csv', index=False)
                print(f"💾 บันทึกไฟล์: laliga_teams.csv")
                
                return df
            else:
                print(f"❌ ไม่สามารถดึงข้อมูลทีมได้: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting teams: {e}")
            return None
    
    def analyze_data_quality(self, df):
        """วิเคราะห์คุณภาพข้อมูล"""
        if df is None or len(df) == 0:
            print("❌ ไม่มีข้อมูลให้วิเคราะห์")
            return
        
        print(f"\n📊 การวิเคราะห์ข้อมูล La Liga:")
        print("=" * 40)
        
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
        
        # ทีมที่เล่นมากที่สุด
        team_games = {}
        for _, row in df.iterrows():
            team_games[row['home_team']] = team_games.get(row['home_team'], 0) + 1
            team_games[row['away_team']] = team_games.get(row['away_team'], 0) + 1
        
        top_teams = sorted(team_games.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"\n🔥 ทีมที่มีข้อมูลมากที่สุด:")
        for i, (team, games) in enumerate(top_teams, 1):
            print(f"   {i}. {team}: {games} เกม")

def main():
    """ฟังก์ชันหลัก"""
    print("🇪🇸 La Liga Real Data Collector")
    print("📡 ดึงข้อมูลจริงจาก football-data.org")
    print("=" * 60)
    
    # ลองใช้ API key ถ้ามี (ใส่ API key ของคุณที่นี่)
    api_key = None  # ใส่ API key ที่นี่ถ้ามี
    
    collector = LaLigaRealDataCollector(api_key)
    
    # ดึงข้อมูลทีม
    teams_df = collector.get_laliga_teams()
    if teams_df is not None:
        print(f"\n🏆 ทีมใน La Liga:")
        for i, team in enumerate(teams_df['name'], 1):
            print(f"   {i:2d}. {team}")
    
    # ดึงข้อมูลการแข่งขัน
    matches_df = collector.get_laliga_matches()
    
    if matches_df is not None:
        # วิเคราะห์ข้อมูล
        collector.analyze_data_quality(matches_df)
        
        print(f"\n✅ สำเร็จ! ข้อมูล La Liga พร้อมใช้งาน")
        print(f"📁 ไฟล์: laliga_real_matches.csv")
        print(f"🎯 พร้อมนำไปใช้กับ La Liga Predictor")
        
        return matches_df
    else:
        print(f"\n❌ ไม่สามารถดึงข้อมูลได้")
        print(f"💡 ตรวจสอบ:")
        print(f"   - การเชื่อมต่ออินเทอร์เน็ต")
        print(f"   - API Key (ถ้ามี)")
        print(f"   - Rate Limit ของ API")
        
        return None

if __name__ == "__main__":
    data = main()
