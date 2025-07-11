#!/usr/bin/env python3
"""
🔍 หา API อื่นสำหรับข้อมูล corners
"""

import requests
import json

def test_free_football_apis():
    """ทดสอบ Free Football APIs"""
    print("🆓 ทดสอบ Free Football APIs")
    print("=" * 40)
    
    # 1. Football-data.org (ที่เราใช้อยู่)
    print("1. 📊 Football-data.org:")
    print("   ✅ มีข้อมูลผลการแข่งขัน")
    print("   ❌ ไม่มีข้อมูล corners")
    print("   🔑 API Key: 052fd4885cf943ad859c89cef542e2e5")
    
    # 2. ลอง FotMob API (unofficial)
    print("\n2. 📱 FotMob API (unofficial):")
    try:
        url = "https://www.fotmob.com/api/matches"
        params = {"date": "20250710"}
        
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ API ทำงานได้")
            print(f"   📊 Keys: {list(data.keys())[:5]}")
        else:
            print("   ❌ API ไม่ทำงาน")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. ลอง API-Sports (RapidAPI อื่น)
    print("\n3. ⚽ API-Sports alternatives:")
    print("   - TheSportsDB API (free)")
    print("   - SportRadar API (paid)")
    print("   - ESPN API (unofficial)")
    
    # 4. ลอง TheSportsDB
    print("\n4. 🏆 TheSportsDB API:")
    try:
        url = "https://www.thesportsdb.com/api/v1/json/3/eventslast.php"
        params = {"id": "133604"}  # Premier League ID
        
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ API ทำงานได้")
            
            if 'results' in data and data['results']:
                event = data['results'][0]
                print(f"   📋 Sample Event Keys: {list(event.keys())[:10]}")
                
                # ตรวจสอบว่ามีข้อมูล corners หรือไม่
                corner_fields = [k for k in event.keys() if 'corner' in k.lower()]
                if corner_fields:
                    print(f"   🥅 Corner Fields: {corner_fields}")
                else:
                    print("   ❌ ไม่มีข้อมูล corners")
            else:
                print("   ❌ ไม่มีข้อมูล results")
        else:
            print("   ❌ API ไม่ทำงาน")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def suggest_corners_data_sources():
    """แนะนำแหล่งข้อมูล corners"""
    print(f"\n💡 แนะนำแหล่งข้อมูล Corners:")
    print("=" * 40)
    
    print("🎯 ตัวเลือกที่มี:")
    print("\n1. 💰 Paid APIs:")
    print("   - RapidAPI Football (ต้องอัปเกรด plan)")
    print("   - SportRadar API ($$$)")
    print("   - Opta Sports Data ($$$)")
    
    print("\n2. 🆓 Free/Alternative:")
    print("   - Web Scraping จาก ESPN/BBC Sport")
    print("   - FotMob unofficial API")
    print("   - Flashscore scraping")
    
    print("\n3. 📊 Manual Data Collection:")
    print("   - รวบรวมข้อมูลจากเว็บไซต์ฟุตบอล")
    print("   - สร้าง database เอง")
    print("   - ใช้ข้อมูลจาก betting sites")
    
    print("\n4. 🔄 Hybrid Approach:")
    print("   - ใช้ข้อมูลจริงที่มี (ผลการแข่งขัน)")
    print("   - เพิ่ม corners เมื่อหาข้อมูลได้")
    print("   - เน้นที่ Handicap/Over-Under ก่อน")

def create_corners_data_plan():
    """สร้างแผนการหาข้อมูล corners"""
    print(f"\n📋 แผนการหาข้อมูล Corners:")
    print("=" * 40)
    
    print("🎯 Phase 1: ทันที (ไม่มี corners)")
    print("   ✅ เน้นที่ Match Result, Handicap, Over/Under")
    print("   ✅ ใช้ข้อมูลจริงที่มีอยู่")
    print("   ✅ ปรับปรุงความแม่นยำของ 3 ประเภทนี้")
    
    print("\n🎯 Phase 2: ระยะสั้น (1-2 สัปดาห์)")
    print("   🔍 หา free API ที่มีข้อมูล corners")
    print("   🔍 ทดสอบ web scraping")
    print("   🔍 รวบรวมข้อมูล corners manual")
    
    print("\n🎯 Phase 3: ระยะยาว (1 เดือน)")
    print("   💰 พิจารณาซื้อ paid API")
    print("   🤖 สร้างระบบ scraping อัตโนมัติ")
    print("   📊 สร้าง corners database")
    
    print("\n✅ ข้อเสนอแนะ:")
    print("   1. เริ่มจาก 3 ประเภทที่มีข้อมูลจริง")
    print("   2. ปรับปรุงความแม่นยำให้ดีที่สุด")
    print("   3. เพิ่ม corners ทีหลังเมื่อมีข้อมูล")

def main():
    """ฟังก์ชันหลัก"""
    print("🔍 Corners Data Source Finder")
    print("=" * 50)
    
    # ทดสอบ APIs
    test_free_football_apis()
    
    # แนะนำแหล่งข้อมูล
    suggest_corners_data_sources()
    
    # สร้างแผน
    create_corners_data_plan()
    
    print(f"\n🎯 สรุป:")
    print("=" * 20)
    print("❌ RapidAPI ที่ให้มาใช้ไม่ได้ (403/429)")
    print("🔍 ต้องหาแหล่งข้อมูล corners อื่น")
    print("✅ เน้นที่ 3 ประเภทที่มีข้อมูลจริงก่อน")
    print("📈 ปรับปรุงความแม่นยำของระบบที่มี")

if __name__ == "__main__":
    main()
