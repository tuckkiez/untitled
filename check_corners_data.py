#!/usr/bin/env python3
"""
🔍 ตรวจสอบข้อมูล Corners ที่ใช้ในการทดสอบ
"""

import pandas as pd
import numpy as np

def check_corners_data():
    """ตรวจสอบข้อมูล corners ที่ใช้"""
    print("🔍 ตรวจสอบข้อมูล Corners ที่ใช้ในการทดสอบ")
    print("=" * 60)
    
    # โหลดข้อมูล Premier League
    try:
        data = pd.read_csv('premier_league_real_data.csv')
        print(f"✅ โหลดข้อมูล Premier League: {len(data)} เกม")
        print(f"📋 Columns: {list(data.columns)}")
        
        # ตรวจสอบว่ามีข้อมูล corners หรือไม่
        if 'corners_total' in data.columns:
            print("✅ มีข้อมูล corners_total")
        else:
            print("❌ ไม่มีข้อมูล corners_total")
            
        if 'corners_first_half' in data.columns:
            print("✅ มีข้อมูล corners_first_half")
        else:
            print("❌ ไม่มีข้อมูล corners_first_half")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n🔍 ตรวจสอบการสร้างข้อมูล Corners จำลอง:")
    print("=" * 50)
    
    # จำลองการสร้างข้อมูล corners
    test_matches = [
        {'home_goals': 2, 'away_goals': 0, 'match': 'Aston Villa 2-0 Tottenham'},
        {'home_goals': 1, 'away_goals': 0, 'match': 'Chelsea 1-0 Man United'},
        {'home_goals': 2, 'away_goals': 3, 'match': 'Brentford 2-3 Fulham'},
        {'home_goals': 3, 'away_goals': 2, 'match': 'Brighton 3-2 Liverpool'},
        {'home_goals': 4, 'away_goals': 2, 'match': 'Crystal Palace 4-2 Wolves'}
    ]
    
    print("📊 ตัวอย่างการสร้างข้อมูล Corners:")
    for match in test_matches:
        home_goals = match['home_goals']
        away_goals = match['away_goals']
        total_goals = home_goals + away_goals
        
        # วิธีที่ใช้ในโค้ด
        base_corners = max(6, min(14, int(total_goals * 2.2 + np.random.normal(0, 1.5))))
        corners_total = max(4, min(16, base_corners))
        corners_first_half = max(1, min(8, int(corners_total * 0.45 + np.random.normal(0, 0.8))))
        
        corners_ou_10 = "Over" if corners_total > 10 else "Under"
        corners_fh_5 = "Over" if corners_first_half > 5 else "Under"
        
        print(f"   {match['match']}")
        print(f"     ประตู: {total_goals} -> Corners: {corners_total} ({corners_ou_10} 10)")
        print(f"     ครึ่งแรก: {corners_first_half} ({corners_fh_5} 5)")
    
    print(f"\n❌ ปัญหาที่พบ:")
    print("=" * 30)
    print("1. ข้อมูล Corners เป็นการจำลองจากจำนวนประตู")
    print("2. ใช้ random ทำให้ไม่สม่ำเสมอ")
    print("3. โมเดลเทรนด้วยข้อมูลจำลอง -> bias")
    print("4. ไม่มีข้อมูล corners จริงจาก API")
    
    print(f"\n💡 วิธีแก้ไข:")
    print("=" * 20)
    print("1. หา API ที่มีข้อมูล corners จริง")
    print("2. ใช้ข้อมูล corners จากเว็บไซต์ฟุตบอล")
    print("3. สร้างข้อมูลจำลองที่สมจริงกว่า")
    print("4. ปรับโมเดลให้ไม่ bias")

def simulate_realistic_corners():
    """สร้างข้อมูล corners ที่สมจริงกว่า"""
    print(f"\n🔧 สร้างข้อมูล Corners ที่สมจริงกว่า:")
    print("=" * 50)
    
    # ข้อมูลสถิติจริงจาก Premier League
    # เฉลี่ย corners ต่อเกม: 10-12 มุม
    # การกระจาย: 6-16 มุม
    
    realistic_corners = []
    
    for i in range(20):
        # สร้างข้อมูลที่สมจริงกว่า
        corners_total = np.random.choice([8, 9, 10, 11, 12, 13, 14], 
                                       p=[0.1, 0.15, 0.2, 0.25, 0.15, 0.1, 0.05])
        
        corners_first_half = np.random.choice([3, 4, 5, 6, 7], 
                                            p=[0.2, 0.3, 0.3, 0.15, 0.05])
        
        corners_ou_10 = "Over" if corners_total > 10 else "Under"
        corners_fh_5 = "Over" if corners_first_half > 5 else "Under"
        
        realistic_corners.append({
            'total': corners_total,
            'first_half': corners_first_half,
            'ou_10': corners_ou_10,
            'fh_5': corners_fh_5
        })
    
    # วิเคราะห์การกระจาย
    over_10_count = sum(1 for c in realistic_corners if c['ou_10'] == 'Over')
    over_5_fh_count = sum(1 for c in realistic_corners if c['fh_5'] == 'Over')
    
    print(f"📊 การกระจายที่สมจริงกว่า (20 เกม):")
    print(f"   Over 10 Total: {over_10_count}/20 = {over_10_count/20:.1%}")
    print(f"   Under 10 Total: {20-over_10_count}/20 = {(20-over_10_count)/20:.1%}")
    print(f"   Over 5 First Half: {over_5_fh_count}/20 = {over_5_fh_count/20:.1%}")
    print(f"   Under 5 First Half: {20-over_5_fh_count}/20 = {(20-over_5_fh_count)/20:.1%}")
    
    print(f"\n✅ นี่คือการกระจายที่สมจริงกว่า!")
    print("   ไม่ใช่ Under ทุกคู่")

def main():
    """ฟังก์ชันหลัก"""
    print("🔍 Corner Data Investigation")
    print("=" * 60)
    
    check_corners_data()
    simulate_realistic_corners()
    
    print(f"\n🎯 สรุป:")
    print("=" * 20)
    print("❌ ข้อมูล Corners ในการทดสอบเป็นการจำลอง")
    print("❌ โมเดล bias เพราะข้อมูลเทรนไม่จริง")
    print("❌ ทำนาย Under ทุกคู่เพราะข้อมูลจำลองส่วนใหญ่ < 10")
    print("✅ ต้องหาข้อมูล corners จริงเพื่อให้ระบบแม่นยำ")

if __name__ == "__main__":
    main()
