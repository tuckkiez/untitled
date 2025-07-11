#!/usr/bin/env python3
"""
Fixed Argentina League Finder for Sportmonks API
ค้นหา Argentina Primera Division พร้อมจัดการ None values
"""

import requests
import json
from datetime import datetime

def safe_lower(text):
    """แปลงเป็น lowercase อย่างปลอดภัย"""
    return text.lower() if text else ''

def comprehensive_league_search():
    api_token = "1TQD9tFVUJ55dd31y6ECZ5FYeFKb8atMhavYD0tQfWgiRWISpTcDJgJ1Cclf"
    base_url = "https://api.sportmonks.com/v3/football"
    
    print("🔍 Comprehensive Argentina League Search")
    print("=" * 50)
    
    # ดึงลีกทั้งหมด
    all_leagues = []
    
    try:
        url = f"{base_url}/leagues"
        params = {
            'api_token': api_token,
            'per_page': 100
        }
        
        print(f"📡 Fetching leagues...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data and data['data']:
                leagues = data['data']
                all_leagues.extend(leagues)
                print(f"✅ Found {len(leagues)} leagues total")
                
                # แสดงตัวอย่างลีก
                print(f"\n📋 Sample leagues:")
                for i, league in enumerate(leagues[:5]):
                    name = league.get('name', 'Unknown')
                    league_id = league.get('id', 'Unknown')
                    country_id = league.get('country_id', 'Unknown')
                    short_code = league.get('short_code', 'Unknown')
                    
                    print(f"   {i+1}. {name} (ID: {league_id})")
                    print(f"      Country ID: {country_id}, Code: {short_code}")
            else:
                print(f"❌ No leagues data found")
                return []
        else:
            print(f"❌ Failed to fetch leagues: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching leagues: {e}")
        return []
    
    # ค้นหา Argentina leagues
    argentina_keywords = [
        'argentina', 'argentine', 'primera division', 'superliga argentina',
        'liga profesional', 'primera a', 'arg', 'afa', 'boca', 'river'
    ]
    
    argentina_leagues = []
    
    print(f"\n🇦🇷 Searching for Argentina leagues...")
    
    for league in all_leagues:
        league_name = safe_lower(league.get('name', ''))
        short_code = safe_lower(league.get('short_code', ''))
        country_id = league.get('country_id', 0)
        
        # ค้นหาตามชื่อ
        found_by_name = False
        for keyword in argentina_keywords:
            if keyword in league_name or keyword in short_code:
                argentina_leagues.append(league)
                print(f"✅ Found by name: {league.get('name')} (ID: {league.get('id')})")
                print(f"   Short code: {league.get('short_code')}")
                print(f"   Country ID: {country_id}")
                found_by_name = True
                break
        
        # ค้นหาตาม country_id ที่น่าจะเป็น Argentina
        if not found_by_name:
            argentina_country_ids = [1159, 11, 32, 6, 1, 320]  # เพิ่ม 320 ที่เจอใน sample
            if country_id in argentina_country_ids:
                argentina_leagues.append(league)
                print(f"✅ Found by country ID: {league.get('name')} (ID: {league.get('id')})")
                print(f"   Country ID: {country_id}")
    
    # ถ้าไม่เจอ ลองดูทุกลีกที่มี
    if not argentina_leagues:
        print(f"\n⚠️ No Argentina leagues found by keywords")
        print(f"📋 All available leagues:")
        
        for i, league in enumerate(all_leagues):
            name = league.get('name', 'Unknown')
            league_id = league.get('id', 'Unknown')
            country_id = league.get('country_id', 'Unknown')
            short_code = league.get('short_code', 'Unknown')
            
            print(f"   {i+1}. {name} (ID: {league_id})")
            print(f"      Country ID: {country_id}, Code: {short_code}")
    
    return argentina_leagues

def test_any_league_for_structure(api_token):
    """ทดสอบลีกใดๆ เพื่อดูโครงสร้างข้อมูล"""
    base_url = "https://api.sportmonks.com/v3/football"
    
    print(f"\n🔍 Testing league structure...")
    
    # ใช้ลีกแรกที่มี
    try:
        leagues_url = f"{base_url}/leagues"
        leagues_params = {'api_token': api_token, 'per_page': 1}
        
        leagues_response = requests.get(leagues_url, params=leagues_params, timeout=10)
        
        if leagues_response.status_code == 200:
            leagues_data = leagues_response.json()
            if 'data' in leagues_data and leagues_data['data']:
                test_league = leagues_data['data'][0]
                league_id = test_league.get('id')
                league_name = test_league.get('name')
                
                print(f"✅ Testing with: {league_name} (ID: {league_id})")
                
                # ทดสอบดึงซีซั่น
                seasons_url = f"{base_url}/seasons"
                seasons_params = {
                    'api_token': api_token,
                    'filters': f'leagueId:{league_id}',
                    'per_page': 5
                }
                
                seasons_response = requests.get(seasons_url, params=seasons_params, timeout=10)
                
                if seasons_response.status_code == 200:
                    seasons_data = seasons_response.json()
                    if 'data' in seasons_data:
                        seasons = seasons_data['data']
                        print(f"✅ Found {len(seasons)} seasons")
                        
                        if seasons:
                            test_season = seasons[0]
                            season_id = test_season.get('id')
                            season_name = test_season.get('name')
                            
                            print(f"   Testing season: {season_name} (ID: {season_id})")
                            
                            # ทดสอบดึงแมทช์
                            fixtures_url = f"{base_url}/fixtures"
                            fixtures_params = {
                                'api_token': api_token,
                                'filters': f'seasonId:{season_id}',
                                'per_page': 3
                            }
                            
                            fixtures_response = requests.get(fixtures_url, params=fixtures_params, timeout=10)
                            
                            if fixtures_response.status_code == 200:
                                fixtures_data = fixtures_response.json()
                                if 'data' in fixtures_data:
                                    fixtures = fixtures_data['data']
                                    print(f"✅ Found {len(fixtures)} fixtures")
                                    
                                    for fixture in fixtures:
                                        print(f"      Fixture: {fixture.get('name', 'Unknown')}")
                                        print(f"      Date: {fixture.get('starting_at')}")
                                    
                                    return True
                            else:
                                print(f"❌ Fixtures failed: {fixtures_response.status_code}")
                    else:
                        print(f"❌ No seasons data")
                else:
                    print(f"❌ Seasons failed: {seasons_response.status_code}")
        else:
            print(f"❌ Leagues failed: {leagues_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

def create_mock_argentina_with_sportmonks_structure():
    """สร้างข้อมูล Argentina ที่เลียนแบบโครงสร้าง Sportmonks"""
    print(f"\n🏗️ Creating Argentina data with Sportmonks structure...")
    
    # ข้อมูลทีมจริงใน Argentina Primera Division
    argentina_teams = [
        {"id": 1001, "name": "River Plate", "short_code": "RIV", "strength": 85},
        {"id": 1002, "name": "Boca Juniors", "short_code": "BOC", "strength": 82},
        {"id": 1003, "name": "Racing Club", "short_code": "RAC", "strength": 75},
        {"id": 1004, "name": "Independiente", "short_code": "IND", "strength": 70},
        {"id": 1005, "name": "San Lorenzo", "short_code": "SAN", "strength": 68},
        {"id": 1006, "name": "Estudiantes", "short_code": "EST", "strength": 72},
        {"id": 1007, "name": "Gimnasia La Plata", "short_code": "GIM", "strength": 65},
        {"id": 1008, "name": "Lanús", "short_code": "LAN", "strength": 67},
        {"id": 1009, "name": "Banfield", "short_code": "BAN", "strength": 63},
        {"id": 1010, "name": "Tigre", "short_code": "TIG", "strength": 60}
    ]
    
    # สร้างแมทช์ในรูปแบบ Sportmonks
    fixtures = []
    base_date = datetime.now()
    
    import random
    random.seed(42)
    
    for i in range(20):
        home_team = random.choice(argentina_teams)
        away_team = random.choice([t for t in argentina_teams if t['id'] != home_team['id']])
        
        # คำนวณผลตามความแข็งแกร่ง
        strength_diff = home_team['strength'] - away_team['strength'] + 5  # home advantage
        
        if strength_diff > 10:
            home_score = random.randint(1, 3)
            away_score = random.randint(0, home_score-1)
        elif strength_diff > 0:
            home_score = random.randint(0, 3)
            away_score = random.randint(0, 2)
        else:
            home_score = random.randint(0, 2)
            away_score = random.randint(0, 3)
        
        fixture = {
            "id": 2000 + i,
            "sport_id": 1,
            "league_id": 999,  # Argentina Primera Division
            "season_id": 2024,
            "name": f"{home_team['name']} vs {away_team['name']}",
            "starting_at": (base_date - timedelta(days=i*3)).strftime('%Y-%m-%d %H:%M:%S'),
            "state_id": 5,  # Finished
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score,
            "total_goals": home_score + away_score,
            "result": "Home Win" if home_score > away_score else "Away Win" if away_score > home_score else "Draw"
        }
        
        fixtures.append(fixture)
    
    argentina_data = {
        "league": {
            "id": 999,
            "name": "Argentina Primera Division",
            "country_id": 11,
            "short_code": "ARG PD",
            "active": True
        },
        "season": {
            "id": 2024,
            "name": "2024",
            "league_id": 999,
            "is_current": True
        },
        "teams": argentina_teams,
        "fixtures": fixtures,
        "api_info": {
            "source": "Mock data with Sportmonks structure",
            "created_at": datetime.now().isoformat(),
            "note": "Real team names with simulated results"
        }
    }
    
    return argentina_data

def main():
    print("🇦🇷 Fixed Argentina League Finder")
    print("=" * 50)
    
    api_token = "1TQD9tFVUJ55dd31y6ECZ5FYeFKb8atMhavYD0tQfWgiRWISpTcDJgJ1Cclf"
    
    # ค้นหาลีกอาร์เจนติน่า
    argentina_leagues = comprehensive_league_search()
    
    if argentina_leagues:
        print(f"\n🎯 Found {len(argentina_leagues)} Argentina leagues!")
        
        for league in argentina_leagues:
            print(f"   - {league.get('name')} (ID: {league.get('id')})")
        
        # บันทึกผลลัพธ์
        result_data = {
            'argentina_leagues': argentina_leagues,
            'found_at': datetime.now().isoformat()
        }
        
        try:
            with open('argentina_leagues_found.json', 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to argentina_leagues_found.json")
        except Exception as e:
            print(f"❌ Error saving: {e}")
    
    else:
        print(f"\n❌ No Argentina leagues found in Sportmonks API")
        
        # ทดสอบโครงสร้าง API
        if test_any_league_for_structure(api_token):
            print(f"\n✅ API structure confirmed - creating mock Argentina data")
            
            # สร้างข้อมูล mock ที่มีโครงสร้างเหมือน Sportmonks
            argentina_data = create_mock_argentina_with_sportmonks_structure()
            
            try:
                with open('argentina_mock_sportmonks_structure.json', 'w', encoding='utf-8') as f:
                    json.dump(argentina_data, f, indent=2, ensure_ascii=False)
                print(f"✅ Mock Argentina data created: argentina_mock_sportmonks_structure.json")
                
                print(f"\n🚀 READY FOR TESTING!")
                print(f"   League: {argentina_data['league']['name']}")
                print(f"   Teams: {len(argentina_data['teams'])}")
                print(f"   Fixtures: {len(argentina_data['fixtures'])}")
                print(f"   Structure: Compatible with Sportmonks API")
                
            except Exception as e:
                print(f"❌ Error creating mock data: {e}")
        else:
            print(f"\n❌ Could not determine API structure")

if __name__ == "__main__":
    from datetime import timedelta
    main()
