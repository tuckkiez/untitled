import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import time

class FootballDataLoader:
    def __init__(self):
        self.data_sources = {
            'csv': self.load_from_csv,
            'api': self.load_from_api,
            'json': self.load_from_json
        }
    
    def load_from_csv(self, file_path):
        """โหลดข้อมูลจากไฟล์ CSV"""
        try:
            df = pd.read_csv(file_path)
            return self.standardize_format(df)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None
    
    def load_from_json(self, file_path):
        """โหลดข้อมูลจากไฟล์ JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            return self.standardize_format(df)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return None
    
    def load_from_api(self, api_config):
        """โหลดข้อมูลจาก API (ตัวอย่าง)"""
        # ตัวอย่างสำหรับ Football-Data.org API
        headers = {
            'X-Auth-Token': api_config.get('api_key', '')
        }
        
        try:
            # ดึงข้อมูลลีก
            league_id = api_config.get('league_id', 2021)  # Premier League
            season = api_config.get('season', 2024)
            
            url = f"https://api.football-data.org/v4/competitions/{league_id}/matches"
            params = {
                'season': season,
                'status': 'FINISHED'
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                matches = []
                
                for match in data.get('matches', []):
                    if match['status'] == 'FINISHED':
                        matches.append({
                            'date': match['utcDate'][:10],
                            'home_team': match['homeTeam']['name'],
                            'away_team': match['awayTeam']['name'],
                            'home_goals': match['score']['fullTime']['home'],
                            'away_goals': match['score']['fullTime']['away']
                        })
                
                df = pd.DataFrame(matches)
                return self.standardize_format(df)
            else:
                print(f"API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error loading from API: {e}")
            return None
    
    def standardize_format(self, df):
        """มาตรฐานรูปแบบข้อมูล"""
        required_columns = ['date', 'home_team', 'away_team', 'home_goals', 'away_goals']
        
        # ตรวจสอบคอลัมน์ที่จำเป็น
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Missing columns: {missing_columns}")
            return None
        
        # แปลงประเภทข้อมูล
        df['date'] = pd.to_datetime(df['date'])
        df['home_goals'] = pd.to_numeric(df['home_goals'], errors='coerce')
        df['away_goals'] = pd.to_numeric(df['away_goals'], errors='coerce')
        
        # เรียงตามวันที่
        df = df.sort_values('date').reset_index(drop=True)
        
        # ลบข้อมูลที่ไม่สมบูรณ์
        df = df.dropna(subset=['home_goals', 'away_goals'])
        
        return df
    
    def load_data(self, source_type, source_config):
        """โหลดข้อมูลจากแหล่งที่กำหนด"""
        if source_type not in self.data_sources:
            print(f"Unsupported source type: {source_type}")
            return None
        
        return self.data_sources[source_type](source_config)

# ตัวอย่างการใช้งาน
def create_sample_csv():
    """สร้างไฟล์ CSV ตัวอย่าง"""
    import numpy as np
    
    teams = [
        'Arsenal', 'Chelsea', 'Liverpool', 'Manchester City', 'Manchester United',
        'Tottenham', 'Newcastle', 'Brighton', 'West Ham', 'Aston Villa',
        'Crystal Palace', 'Fulham', 'Brentford', 'Wolves', 'Everton',
        'Nottingham Forest', 'Bournemouth', 'Sheffield United', 'Burnley', 'Luton'
    ]
    
    matches = []
    start_date = datetime(2023, 8, 1)
    
    # สร้างตารางแข่งขันแบบ round-robin
    for round_num in range(19):  # 19 รอบ (แต่ละทีมเจอกัน 1 ครั้ง)
        round_date = start_date + timedelta(weeks=round_num)
        
        # สุ่มคู่แข่งขัน
        teams_copy = teams.copy()
        np.random.shuffle(teams_copy)
        
        for i in range(0, len(teams_copy), 2):
            if i + 1 < len(teams_copy):
                home_team = teams_copy[i]
                away_team = teams_copy[i + 1]
                
                # สร้างผลการแข่งขันแบบสมจริง
                # ทีมเหย้ามีความได้เปรียบเล็กน้อย
                home_strength = np.random.normal(1.6, 0.6)
                away_strength = np.random.normal(1.3, 0.6)
                
                home_goals = max(0, int(np.random.poisson(max(0, home_strength))))
                away_goals = max(0, int(np.random.poisson(max(0, away_strength))))
                
                matches.append({
                    'date': round_date.strftime('%Y-%m-%d'),
                    'home_team': home_team,
                    'away_team': away_team,
                    'home_goals': home_goals,
                    'away_goals': away_goals,
                    'round': round_num + 1
                })
    
    df = pd.DataFrame(matches)
    df.to_csv('/Users/80090/Desktop/Project/untitle/sample_matches.csv', index=False)
    print("สร้างไฟล์ sample_matches.csv เรียบร้อยแล้ว")
    return df

if __name__ == "__main__":
    # สร้างข้อมูลตัวอย่าง
    sample_df = create_sample_csv()
    
    # ทดสอบการโหลดข้อมูล
    loader = FootballDataLoader()
    
    # โหลดจาก CSV
    print("กำลังโหลดข้อมูลจาก CSV...")
    df = loader.load_data('csv', '/Users/80090/Desktop/Project/untitle/sample_matches.csv')
    
    if df is not None:
        print(f"โหลดข้อมูลสำเร็จ: {len(df)} เกม")
        print(f"ช่วงเวลา: {df['date'].min()} ถึง {df['date'].max()}")
        print(f"จำนวนทีม: {len(set(df['home_team'].tolist() + df['away_team'].tolist()))}")
        print("\nตัวอย่างข้อมูล:")
        print(df.head())
    else:
        print("ไม่สามารถโหลดข้อมูลได้")
