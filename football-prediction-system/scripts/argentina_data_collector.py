#!/usr/bin/env python3
"""
Argentina Primera Division Data Collector
รวบรวมข้อมูลจากหลายแหล่งสำหรับ Argentina Primera Division
"""

import requests
import json
from datetime import datetime, timedelta
import time

class ArgentinaDataCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def get_thesportsdb_data(self):
        """ดึงข้อมูลจาก TheSportsDB"""
        print("🔍 Collecting from TheSportsDB...")
        
        try:
            # ค้นหาทีมในลีกอาร์เจนติน่า
            teams_url = "https://www.thesportsdb.com/api/v1/json/3/lookup_all_teams.php"
            params = {'id': '4026'}  # Argentina Primera Division ID
            
            response = self.session.get(teams_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                teams = data.get('teams', []) or []
                
                print(f"✅ Found {len(teams)} teams")
                
                # ดึงแมทช์ของแต่ละทีม
                all_matches = []
                for i, team in enumerate(teams[:5]):  # ทดสอบ 5 ทีมแรก
                    if team:
                        team_name = team.get('strTeam', '')
                        team_id = team.get('idTeam', '')
                        
                        print(f"   📊 Getting matches for {team_name}...")
                        
                        # ดึงแมทช์ล่าสุด
                        matches_url = "https://www.thesportsdb.com/api/v1/json/3/eventslast.php"
                        match_params = {'id': team_id}
                        
                        match_response = self.session.get(matches_url, params=match_params)
                        if match_response.status_code == 200:
                            match_data = match_response.json()
                            events = match_data.get('results', []) or []
                            
                            for event in events:
                                if event and event.get('strLeague') == 'Argentinian Primera Division':
                                    all_matches.append(event)
                        
                        time.sleep(0.5)  # หน่วงเวลาไม่ให้ spam API
                
                return {
                    'teams': teams,
                    'matches': all_matches
                }
            else:
                print(f"❌ Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def get_alternative_sources(self):
        """ลองแหล่งข้อมูลอื่น"""
        print("\n🔍 Trying alternative sources...")
        
        sources = [
            {
                'name': 'Football API',
                'url': 'https://v3.football.api-sports.io/fixtures',
                'headers': {
                    'X-RapidAPI-Key': 'demo',  # ใช้ demo key
                    'X-RapidAPI-Host': 'v3.football.api-sports.io'
                },
                'params': {
                    'league': '128',  # Argentina Primera Division
                    'season': '2024'
                }
            }
        ]
        
        results = {}
        
        for source in sources:
            try:
                print(f"📡 Testing {source['name']}...")
                
                headers = source.get('headers', {})
                params = source.get('params', {})
                
                response = self.session.get(
                    source['url'], 
                    headers=headers, 
                    params=params,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results[source['name']] = data
                    print(f"✅ {source['name']}: Success")
                else:
                    print(f"❌ {source['name']}: Status {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {source['name']}: {e}")
        
        return results
    
    def create_sample_argentina_data(self):
        """สร้างข้อมูลตัวอย่างสำหรับทดสอบ"""
        print("\n🏗️ Creating sample Argentina data for testing...")
        
        # ทีมจริงใน Argentina Primera Division
        teams = [
            "River Plate", "Boca Juniors", "Racing Club", "Independiente",
            "San Lorenzo", "Estudiantes", "Gimnasia La Plata", "Lanús",
            "Banfield", "Tigre", "Vélez Sarsfield", "Huracán",
            "Argentinos Juniors", "Defensa y Justicia", "Talleres",
            "Rosario Central", "Newells Old Boys", "Godoy Cruz",
            "Platense", "Sarmiento", "Unión", "Barracas Central",
            "Instituto", "Belgrano", "Riestra", "Atlético Tucumán"
        ]
        
        # สร้างแมทช์ตัวอย่าง 20 นัด
        matches = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(20):
            match_date = base_date + timedelta(days=i*2)
            
            # สุ่มทีม
            import random
            home_team = random.choice(teams)
            away_team = random.choice([t for t in teams if t != home_team])
            
            # สร้างผลการแข่งขัน
            home_score = random.randint(0, 4)
            away_score = random.randint(0, 3)
            
            # กำหนดผลแพ้ชนะ
            if home_score > away_score:
                result = "Home Win"
            elif away_score > home_score:
                result = "Away Win"
            else:
                result = "Draw"
            
            # สร้างข้อมูลเพิ่มเติม
            total_goals = home_score + away_score
            corners_home = random.randint(2, 8)
            corners_away = random.randint(2, 8)
            total_corners = corners_home + corners_away
            
            match = {
                'id': f'ARG_{i+1}',
                'date': match_date.strftime('%Y-%m-%d'),
                'time': f"{random.randint(19, 23)}:{random.choice(['00', '30'])}",
                'home_team': home_team,
                'away_team': away_team,
                'home_score': home_score,
                'away_score': away_score,
                'result': result,
                'total_goals': total_goals,
                'corners_home': corners_home,
                'corners_away': corners_away,
                'total_corners': total_corners,
                'over_under_2_5': 'Over' if total_goals > 2.5 else 'Under',
                'corners_over_9_5': 'Over' if total_corners > 9.5 else 'Under',
                'league': 'Argentina Primera Division'
            }
            
            matches.append(match)
        
        return {
            'teams': teams,
            'matches': matches,
            'league_info': {
                'name': 'Argentina Primera Division',
                'country': 'Argentina',
                'season': '2024',
                'total_teams': len(teams)
            }
        }
    
    def save_data(self, data, filename):
        """บันทึกข้อมูล"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Data saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving data: {e}")

def main():
    print("🇦🇷 Argentina Primera Division Data Collector")
    print("=" * 60)
    
    collector = ArgentinaDataCollector()
    
    # ลองดึงข้อมูลจริง
    thesportsdb_data = collector.get_thesportsdb_data()
    alternative_data = collector.get_alternative_sources()
    
    # ถ้าไม่ได้ข้อมูลจริง ใช้ข้อมูลตัวอย่าง
    if not thesportsdb_data or not thesportsdb_data.get('matches'):
        print("\n⚠️ Real data not available, creating sample data...")
        sample_data = collector.create_sample_argentina_data()
        
        # บันทึกข้อมูลตัวอย่าง
        collector.save_data(sample_data, 'argentina_sample_data.json')
        
        print(f"\n📊 Sample Data Created:")
        print(f"   - Teams: {len(sample_data['teams'])}")
        print(f"   - Matches: {len(sample_data['matches'])}")
        print(f"   - League: {sample_data['league_info']['name']}")
        
        # แสดงตัวอย่างแมทช์
        print(f"\n🏆 Sample Matches:")
        for i, match in enumerate(sample_data['matches'][:5]):
            print(f"   {i+1}. {match['home_team']} {match['home_score']}-{match['away_score']} {match['away_team']}")
            print(f"      Date: {match['date']}, Result: {match['result']}")
            print(f"      Goals: {match['total_goals']}, Corners: {match['total_corners']}")
        
        return sample_data
    else:
        print(f"\n✅ Real data collected:")
        print(f"   - Teams: {len(thesportsdb_data['teams'])}")
        print(f"   - Matches: {len(thesportsdb_data['matches'])}")
        
        collector.save_data(thesportsdb_data, 'argentina_real_data.json')
        return thesportsdb_data

if __name__ == "__main__":
    data = main()
    
    print("\n🚀 Next Steps:")
    print("1. Use this data to create Argentina predictor")
    print("2. Run 20-match backtest with real results")
    print("3. Test predictions for tonight's matches")
    print("4. Compare with actual results")
