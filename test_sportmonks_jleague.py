#!/usr/bin/env python3
"""
สคริปต์ทดสอบ Sportmonks API เพื่อหาข้อมูล J-League 2
"""

import requests
import json
from typing import Dict, Any, Optional

class SportmonksAPITester:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.sportmonks.com/v3/football"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """ส่งคำขอ API และคืนค่าผลลัพธ์"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            print(f"🔍 กำลังทดสอบ endpoint: {url}")
            if params:
                print(f"📋 พารามิเตอร์: {params}")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ สำเร็จ! ได้ข้อมูลแล้ว")
                return data
            else:
                print(f"❌ เกิดข้อผิดพลาด: {response.text}")
                return {"error": response.text, "status_code": response.status_code}
                
        except requests.exceptions.RequestException as e:
            print(f"🚨 ข้อผิดพลาดในการเชื่อมต่อ: {e}")
            return {"error": str(e)}
    
    def test_basic_endpoints(self):
        """ทดสอบ endpoint พื้นฐาน"""
        print("🧪 ทดสอบการเชื่อมต่อ API พื้นฐาน...")
        
        endpoints = [
            "leagues",
            "teams", 
            "countries",
            "seasons"
        ]
        
        for endpoint in endpoints:
            print(f"\n--- ทดสอบ {endpoint} ---")
            result = self.make_request(endpoint)
            
            if "error" not in result:
                print(f"✅ {endpoint} ใช้งานได้!")
                if "data" in result:
                    print(f"📊 พบข้อมูล {len(result['data'])} รายการ")
                return True
            else:
                print(f"❌ {endpoint} ใช้งานไม่ได้")
        
        return False
    
    def search_japanese_leagues(self):
        """ค้นหาลีกญี่ปุ่น รวมถึง J-League 2"""
        print("\n🇯🇵 ค้นหาลีกญี่ปุ่น...")
        
        search_terms = ["japan", "j-league", "j league", "jleague", "j2"]
        
        for term in search_terms:
            print(f"\n--- ค้นหาด้วยคำว่า: {term} ---")
            
            result = self.make_request("leagues", {"search": term})
            
            if "error" not in result and "data" in result:
                leagues = result["data"]
                print(f"✅ พบลีก {len(leagues)} รายการที่ตรงกับ '{term}'")
                
                for league in leagues:
                    name = league.get("name", "ไม่ทราบชื่อ")
                    league_id = league.get("id", "ไม่ทราบ ID")
                    country_data = league.get("country", {})
                    country = country_data.get("name", "ไม่ทราบประเทศ") if country_data else "ไม่ทราบประเทศ"
                    
                    print(f"  🏆 {name} (ID: {league_id}) - {country}")
                    
                    # ตรวจสอบว่าเป็น J-League 2 หรือไม่
                    j2_keywords = ["j.league", "j-league", "division 2", "j2", "second"]
                    if any(keyword in name.lower() for keyword in j2_keywords):
                        print(f"    🎯 น่าจะเป็น J-League 2!")
                        return league_id
            else:
                print(f"❌ ไม่พบผลลัพธ์สำหรับ '{term}'")
        
        return None
    
    def test_original_round(self, round_id: str = "339273"):
        """ทดสอบ round ที่ระบุในคำถามเดิม"""
        print(f"\n🎯 ทดสอบ round เฉพาะ: {round_id}")
        
        # ทดสอบแบบง่ายก่อน
        result = self.make_request(f"rounds/{round_id}")
        
        if "error" not in result:
            print("✅ round endpoint พื้นฐานใช้งานได้!")
            
            # ลองใส่ include ทีละตัว
            includes_to_test = [
                "fixtures",
                "fixtures.participants", 
                "league",
                "league.country"
            ]
            
            for include in includes_to_test:
                print(f"\n--- ทดสอบกับ include: {include} ---")
                result_with_include = self.make_request(f"rounds/{round_id}", {"include": include})
                
                if "error" not in result_with_include:
                    print(f"✅ Include '{include}' ใช้งานได้!")
                else:
                    print(f"❌ Include '{include}' ใช้งานไม่ได้")
        else:
            print("❌ round endpoint พื้นฐานใช้งานไม่ได้")
    
    def find_jleague2_current_season(self):
        """หา J-League 2 ในซีซั่นปัจจุบัน"""
        print("\n🔍 ค้นหา J-League 2 ในซีซั่นปัจจุบัน...")
        
        # ค้นหาประเทศญี่ปุ่นก่อน
        countries_result = self.make_request("countries", {"search": "japan"})
        
        if "error" not in countries_result and "data" in countries_result:
            japan_countries = countries_result["data"]
            
            for country in japan_countries:
                country_id = country.get("id")
                country_name = country.get("name")
                print(f"🇯🇵 พบประเทศ: {country_name} (ID: {country_id})")
                
                # ค้นหาลีกในประเทศญี่ปุ่น
                leagues_result = self.make_request("leagues", {"countries": country_id})
                
                if "error" not in leagues_result and "data" in leagues_result:
                    leagues = leagues_result["data"]
                    print(f"📊 พบลีก {len(leagues)} รายการในญี่ปุ่น")
                    
                    for league in leagues:
                        league_name = league.get("name", "")
                        league_id = league.get("id")
                        
                        if "j2" in league_name.lower() or "division 2" in league_name.lower():
                            print(f"🎯 พบ J-League 2: {league_name} (ID: {league_id})")
                            return league_id
        
        return None

def main():
    # Token ที่ให้มา
    token = "21GtWoxlRVLIhk8mMYXLOgeigGEcmYtjq93veXNNnaV2iY287Zpz3OMd9OWd"
    
    print("🚀 ทดสอบ Sportmonks API สำหรับ J-League 2")
    print("=" * 60)
    
    tester = SportmonksAPITester(token)
    
    # รันการทดสอบ
    if tester.test_basic_endpoints():
        print("\n✅ API ใช้งานได้! ดำเนินการต่อ...")
        
        # ค้นหา J-League 2
        jleague2_id = tester.search_japanese_leagues()
        
        if not jleague2_id:
            jleague2_id = tester.find_jleague2_current_season()
        
        # ทดสอบ round เดิม
        tester.test_original_round()
        
        if jleague2_id:
            print(f"\n🎉 พบ J-League 2 แล้ว! ID: {jleague2_id}")
        else:
            print("\n😔 ไม่พบ J-League 2 ในระบบ")
    else:
        print("\n❌ API ใช้งานไม่ได้ อาจมีปัญหากับ token หรือ endpoint")
    
    print("\n" + "=" * 60)
    print("🏁 การทดสอบเสร็จสิ้น!")

if __name__ == "__main__":
    main()
