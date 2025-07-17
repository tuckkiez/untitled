#!/usr/bin/env python3
"""
🚀 API-Football Data Fetcher
สคริปต์สำหรับดึงข้อมูลจาก API-Football
"""

import requests
import json
import os
import time
from datetime import datetime

class APIFootballFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        self.output_dir = "api_data"
        
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
    
    def fetch_odds_bets_types(self):
        """ดึงข้อมูลประเภทการเดิมพัน"""
        url = f"{self.base_url}/odds/bets"
        
        print(f"📊 กำลังดึงข้อมูลประเภทการเดิมพัน...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/odds_bets_types.json"
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
    
    def fetch_odds(self, league_id, season):
        """ดึงข้อมูลอัตราต่อรอง"""
        url = f"{self.base_url}/odds"
        params = {
            'league': str(league_id),
            'season': str(season)
        }
        
        print(f"📊 กำลังดึงข้อมูลอัตราต่อรองของลีก {league_id} ฤดูกาล {season}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/odds_{league_id}_{season}.json"
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
    
    def fetch_fixtures_by_league(self, league_id, season):
        """ดึงข้อมูลการแข่งขันตามลีกและฤดูกาล"""
        url = f"{self.base_url}/fixtures"
        params = {
            'league': str(league_id),
            'season': str(season)
        }
        
        print(f"📊 กำลังดึงข้อมูลการแข่งขันของลีก {league_id} ฤดูกาล {season}...")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # บันทึกข้อมูล
                filename = f"{self.output_dir}/fixtures_league_{league_id}_{season}.json"
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

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 API-Football Data Fetcher")
    print("=" * 60)
    
    # API key
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # สร้าง fetcher
    fetcher = APIFootballFetcher(api_key)
    
    # ดึงข้อมูลสถิติของทีม
    fetcher.fetch_team_statistics(33, 39, 2020)  # Manchester United, Premier League, 2020
    
    # หน่วงเวลาเล็กน้อยเพื่อไม่ให้ API โดน rate limit
    time.sleep(1)
    
    # ดึงข้อมูลทีม
    fetcher.fetch_team_info(33)  # Manchester United
    
    # หน่วงเวลาเล็กน้อยเพื่อไม่ให้ API โดน rate limit
    time.sleep(1)
    
    # ดึงข้อมูลประเภทการเดิมพัน
    fetcher.fetch_odds_bets_types()
    
    # หน่วงเวลาเล็กน้อยเพื่อไม่ให้ API โดน rate limit
    time.sleep(1)
    
    # ดึงข้อมูลอัตราต่อรอง
    fetcher.fetch_odds(39, 2020)  # Premier League, 2020
    
    print("\n✅ เสร็จสมบูรณ์!")

if __name__ == "__main__":
    main()
