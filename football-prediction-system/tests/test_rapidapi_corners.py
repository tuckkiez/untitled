#!/usr/bin/env python3
"""
🔍 ทดสอบ RapidAPI Football API สำหรับข้อมูล corners
"""

import requests
import json

def test_rapidapi_corners():
    """ทดสอบ RapidAPI Football API"""
    print("🔍 ทดสอบ RapidAPI Football API")
    print("=" * 50)
    
    # API Configuration
    url = 'https://api-football-v1.p.rapidapi.com/v2/odds/league/865927/bookmaker/5?page=2'
    headers = {
        'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
        'x-rapidapi-key': 'f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0'
    }
    
    print(f"📡 URL: {url}")
    print(f"🔑 API Key: {headers['x-rapidapi-key'][:20]}...")
    
    try:
        print(f"\n🚀 กำลังเรียก API...")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ API ทำงานได้!")
                print(f"📊 Response Type: {type(data)}")
                
                if isinstance(data, dict):
                    print(f"🔑 Keys: {list(data.keys())}")
                    
                    # แสดงข้อมูลตัวอย่าง
                    print(f"\n📋 ตัวอย่างข้อมูล:")
                    print(json.dumps(data, indent=2, ensure_ascii=False)[:1000] + "...")
                    
                elif isinstance(data, list):
                    print(f"📊 จำนวนรายการ: {len(data)}")
                    if len(data) > 0:
                        print(f"📋 ตัวอย่างรายการแรก:")
                        print(json.dumps(data[0], indent=2, ensure_ascii=False)[:500] + "...")
                
                return data
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON Decode Error: {e}")
                print(f"📄 Raw Response: {response.text[:500]}")
                return None
                
        elif response.status_code == 401:
            print(f"❌ Unauthorized - API Key ไม่ถูกต้องหรือหมดอายุ")
            return None
            
        elif response.status_code == 403:
            print(f"❌ Forbidden - ไม่มีสิทธิ์เข้าถึง endpoint นี้")
            return None
            
        elif response.status_code == 429:
            print(f"❌ Rate Limit Exceeded - เกินจำนวนการเรียกที่อนุญาต")
            return None
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"📄 Response: {response.text[:500]}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout - API ใช้เวลานานเกินไป")
        return None
        
    except requests.exceptions.ConnectionError:
        print(f"🌐 Connection Error - ไม่สามารถเชื่อมต่อได้")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None

def explore_api_endpoints():
    """สำรวจ endpoints อื่นๆ ที่อาจมีข้อมูล corners"""
    print(f"\n🔍 สำรวจ API Endpoints อื่นๆ")
    print("=" * 40)
    
    base_url = 'https://api-football-v1.p.rapidapi.com'
    headers = {
        'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
        'x-rapidapi-key': 'f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0'
    }
    
    # ลอง endpoints ที่อาจมีข้อมูล corners
    test_endpoints = [
        '/v2/fixtures/league/39',  # Premier League fixtures
        '/v2/statistics/fixture/592872',  # Match statistics
        '/v2/leagues',  # Available leagues
        '/v3/fixtures',  # V3 fixtures
    ]
    
    for endpoint in test_endpoints:
        print(f"\n📡 ทดสอบ: {endpoint}")
        try:
            url = base_url + endpoint
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        print(f"   Keys: {list(data.keys())[:5]}")
                    elif isinstance(data, list):
                        print(f"   Items: {len(data)}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"   Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   Exception: {e}")

def check_api_documentation():
    """แสดงข้อมูลเกี่ยวกับ API"""
    print(f"\n📚 ข้อมูล RapidAPI Football API")
    print("=" * 40)
    
    print(f"🔗 API: api-football-v1.p.rapidapi.com")
    print(f"📋 Features ที่น่าสนใจ:")
    print(f"   - Match fixtures และผลการแข่งขัน")
    print(f"   - Team และ player statistics")
    print(f"   - Live scores")
    print(f"   - Odds และ betting data")
    print(f"   - Match events (goals, cards, corners)")
    
    print(f"\n🎯 สำหรับข้อมูล Corners ควรหา:")
    print(f"   - Match statistics endpoint")
    print(f"   - Match events endpoint")
    print(f"   - Live match data")

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 RapidAPI Football API Tester")
    print("🥅 ทดสอบการดึงข้อมูล Corners")
    print("=" * 60)
    
    # ทดสอบ API ที่ให้มา
    data = test_rapidapi_corners()
    
    # สำรวจ endpoints อื่น
    explore_api_endpoints()
    
    # แสดงข้อมูล API
    check_api_documentation()
    
    print(f"\n🎯 สรุป:")
    print("=" * 20)
    
    if data is not None:
        print("✅ API Key ใช้งานได้")
        print("✅ สามารถเชื่อมต่อ RapidAPI ได้")
        print("🔍 ต้องหา endpoint ที่มีข้อมูล corners")
    else:
        print("❌ ไม่สามารถดึงข้อมูลได้")
        print("🔧 ต้องตรวจสอบ API Key หรือ endpoint")
    
    return data

if __name__ == "__main__":
    result = main()
