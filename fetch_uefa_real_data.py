#!/usr/bin/env python3
"""
🚀 UEFA Real Data Fetcher - July 17-18, 2025
ดึงข้อมูลจริงจาก API สำหรับการแข่งขัน UEFA Europa League และ UEFA Europa Conference League
"""

import requests
import json
import os
import time
from datetime import datetime

class UEFARealDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        self.output_dir = "api_data/uefa_real_data"
        
        # สร้างโฟลเดอร์สำหรับเก็บข้อมูล
        os.makedirs(self.output_dir, exist_ok=True)
    
    def fetch_team_statistics(self, team_id, league_id, season):
        """ดึงข้อมูลสถิติของทีม"""
        url = f"{self.base_url}/teams/statistics"
        params = {
            'team': str(team_id),
            'league': str(league_id),
            'season': str(season)
        }
        
        print(f"📊 กำลังดึงข้อมูลสถิติของทีม {team_id} ในลีก {league_id} ฤดูกาล {season}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/team_statistics_{team_id}_{league_id}_{season}.json"
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
    
    def fetch_team_info(self, team_id):
        """ดึงข้อมูลทีม"""
        url = f"{self.base_url}/teams"
        params = {
            'id': str(team_id)
        }
        
        print(f"📊 กำลังดึงข้อมูลทีม {team_id}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/team_info_{team_id}.json"
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
    
    def fetch_fixtures(self, date):
        """ดึงข้อมูลการแข่งขันตามวันที่"""
        url = f"{self.base_url}/fixtures"
        params = {
            'date': date
        }
        
        print(f"📊 กำลังดึงข้อมูลการแข่งขันวันที่ {date}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/fixtures_{date}.json"
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
    
    def fetch_head_to_head(self, team1_id, team2_id):
        """ดึงข้อมูลประวัติการเจอกันของสองทีม"""
        url = f"{self.base_url}/fixtures/headtohead"
        params = {
            'h2h': f"{team1_id}-{team2_id}"
        }
        
        print(f"📊 กำลังดึงข้อมูลประวัติการเจอกันของทีม {team1_id} และ {team2_id}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/h2h_{team1_id}_{team2_id}.json"
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
    
    def fetch_team_fixtures(self, team_id, last=20):
        """ดึงข้อมูลการแข่งขันล่าสุดของทีม"""
        url = f"{self.base_url}/fixtures"
        params = {
            'team': str(team_id),
            'last': str(last)
        }
        
        print(f"📊 กำลังดึงข้อมูลการแข่งขัน {last} นัดล่าสุดของทีม {team_id}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/team_fixtures_{team_id}_last{last}.json"
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
    
    def fetch_fixture_statistics(self, fixture_id):
        """ดึงข้อมูลสถิติของการแข่งขัน"""
        url = f"{self.base_url}/fixtures/statistics"
        params = {
            'fixture': str(fixture_id)
        }
        
        print(f"📊 กำลังดึงข้อมูลสถิติของการแข่งขัน {fixture_id}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/fixture_statistics_{fixture_id}.json"
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
    
    def fetch_odds(self, fixture_id):
        """ดึงข้อมูลอัตราต่อรองของการแข่งขัน"""
        url = f"{self.base_url}/odds"
        params = {
            'fixture': str(fixture_id)
        }
        
        print(f"📊 กำลังดึงข้อมูลอัตราต่อรองของการแข่งขัน {fixture_id}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/fixture_odds_{fixture_id}.json"
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
    
    def fetch_uefa_fixtures(self):
        """ดึงข้อมูลการแข่งขัน UEFA Europa League และ UEFA Europa Conference League"""
        # ดึงข้อมูลการแข่งขันวันที่ 17-18 กรกฎาคม 2025
        fixtures_data = {}
        
        for date in ["2025-07-17", "2025-07-18"]:
            data = self.fetch_fixtures(date)
            if data and 'response' in data:
                fixtures = data['response']
                
                # กรองเฉพาะการแข่งขัน UEFA Europa League และ UEFA Europa Conference League
                uefa_fixtures = []
                for fixture in fixtures:
                    league_name = fixture['league']['name'].lower()
                    if 'europa league' in league_name or 'conference league' in league_name:
                        uefa_fixtures.append(fixture)
                
                fixtures_data[date] = uefa_fixtures
                print(f"✅ พบการแข่งขัน UEFA {len(uefa_fixtures)} รายการในวันที่ {date}")
            
            # หน่วงเวลาเล็กน้อยเพื่อไม่ให้ API โดน rate limit
            time.sleep(1)
        
        # บันทึกข้อมูล
        filename = f"{self.output_dir}/uefa_fixtures_july_17_18_2025.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(fixtures_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ บันทึกข้อมูลลงไฟล์: {filename}")
        return fixtures_data
    
    def fetch_all_data_for_uefa_fixtures(self):
        """ดึงข้อมูลทั้งหมดสำหรับการแข่งขัน UEFA"""
        # ดึงข้อมูลการแข่งขัน UEFA
        fixtures_data = self.fetch_uefa_fixtures()
        
        if not fixtures_data:
            print("❌ ไม่พบข้อมูลการแข่งขัน UEFA")
            return
        
        # รวมการแข่งขันทั้งหมด
        all_fixtures = []
        for date, fixtures in fixtures_data.items():
            all_fixtures.extend(fixtures)
        
        # ดึงข้อมูลเพิ่มเติมสำหรับแต่ละการแข่งขัน
        for fixture in all_fixtures:
            fixture_id = fixture['fixture']['id']
            home_team_id = fixture['teams']['home']['id']
            away_team_id = fixture['teams']['away']['id']
            
            # ดึงข้อมูลสถิติของการแข่งขัน
            self.fetch_fixture_statistics(fixture_id)
            time.sleep(1)
            
            # ดึงข้อมูลอัตราต่อรองของการแข่งขัน
            self.fetch_odds(fixture_id)
            time.sleep(1)
            
            # ดึงข้อมูลทีมเจ้าบ้าน
            self.fetch_team_info(home_team_id)
            time.sleep(1)
            
            # ดึงข้อมูลทีมเยือน
            self.fetch_team_info(away_team_id)
            time.sleep(1)
            
            # ดึงข้อมูลประวัติการเจอกัน
            self.fetch_head_to_head(home_team_id, away_team_id)
            time.sleep(1)
            
            # ดึงข้อมูลการแข่งขันล่าสุดของทีมเจ้าบ้าน
            self.fetch_team_fixtures(home_team_id, 10)
            time.sleep(1)
            
            # ดึงข้อมูลการแข่งขันล่าสุดของทีมเยือน
            self.fetch_team_fixtures(away_team_id, 10)
            time.sleep(1)
        
        print(f"✅ ดึงข้อมูลทั้งหมดสำเร็จ: {len(all_fixtures)} รายการ")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 UEFA Real Data Fetcher - July 17-18, 2025")
    print("=" * 60)
    
    # API key
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # สร้าง fetcher
    fetcher = UEFARealDataFetcher(api_key)
    
    # ดึงข้อมูลทั้งหมดสำหรับการแข่งขัน UEFA
    fetcher.fetch_all_data_for_uefa_fixtures()
    
    print("\n✅ เสร็จสมบูรณ์!")

if __name__ == "__main__":
    main()
