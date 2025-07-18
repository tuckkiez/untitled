# 🚀 คู่มือการใช้งานระบบวิเคราะห์ฟุตบอล Ultra Advanced ML

คู่มือนี้อธิบายวิธีการใช้งานระบบวิเคราะห์ฟุตบอล Ultra Advanced ML สำหรับ China Super League และ Korea K League 1 รวมถึงวิธีการปรับแต่งเพื่อใช้กับลีกอื่นๆ หรือวันที่อื่นๆ

## 📋 สารบัญ

1. [โครงสร้างไฟล์](#โครงสร้างไฟล์)
2. [การรันระบบ](#การรันระบบ)
3. [การปรับแต่งสำหรับลีกอื่น](#การปรับแต่งสำหรับลีกอื่น)
4. [การปรับแต่งสำหรับวันที่อื่น](#การปรับแต่งสำหรับวันที่อื่น)
5. [การปรับแต่งพารามิเตอร์การวิเคราะห์](#การปรับแต่งพารามิเตอร์การวิเคราะห์)
6. [การเชื่อมต่อกับ API จริง](#การเชื่อมต่อกับ-api-จริง)
7. [การแก้ไขปัญหาที่พบบ่อย](#การแก้ไขปัญหาที่พบบ่อย)

## 📁 โครงสร้างไฟล์

```
/Users/80090/Desktop/Project/untitle/
├── analyze_china_super_league.py    # สคริปต์วิเคราะห์ China Super League
├── analyze_korea_k_league.py        # สคริปต์วิเคราะห์ Korea K League 1
├── update_index.py                  # สคริปต์อัพเดท index.html
├── run_all_analysis.sh              # สคริปต์รันการวิเคราะห์ทั้งหมด
├── CORNER_API_GUIDE.md              # คู่มือการวิเคราะห์มุมที่เส้น 10.0
├── USAGE_GUIDE.md                   # คู่มือการใช้งานนี้
├── index.html                       # หน้าเว็บหลักที่แสดงผลการวิเคราะห์
├── data/                            # โฟลเดอร์สำหรับเก็บข้อมูล
└── output/                          # โฟลเดอร์สำหรับเก็บผลลัพธ์
    ├── china_super_league_analysis_YYYY-MM-DD.html
    └── korea_k_league_analysis_YYYY-MM-DD.html
```

## 🚀 การรันระบบ

### วิธีที่ 1: รันทั้งหมดในครั้งเดียว

```bash
cd /Users/80090/Desktop/Project/untitle
./run_all_analysis.sh
```

สคริปต์นี้จะ:
1. รันการวิเคราะห์ China Super League
2. รันการวิเคราะห์ Korea K League 1
3. อัพเดท index.html
4. เปิด index.html ในเบราว์เซอร์

### วิธีที่ 2: รันแต่ละส่วนแยกกัน

```bash
# วิเคราะห์ China Super League
python analyze_china_super_league.py

# วิเคราะห์ Korea K League 1
python analyze_korea_k_league.py

# อัพเดท index.html
python update_index.py
```

## 🌍 การปรับแต่งสำหรับลีกอื่น

หากต้องการเพิ่มการวิเคราะห์สำหรับลีกอื่น ให้ทำตามขั้นตอนดังนี้:

1. **สร้างสคริปต์วิเคราะห์ใหม่** โดยคัดลอกจากสคริปต์ที่มีอยู่:

```bash
cp analyze_china_super_league.py analyze_new_league.py
```

2. **แก้ไขสคริปต์** เพื่อปรับค่าต่างๆ:

```python
# แก้ไขชื่อคลาส
class NewLeagueAnalyzer:
    
    def __init__(self):
        # แก้ไขข้อมูลลีก
        self.league_id = 999  # รหัสลีกใหม่
        self.league_name = "New League Name"
        self.season = 2025
```

3. **แก้ไขข้อมูลทีม** ในฟังก์ชัน `load_fixtures()`, `load_team_stats()` และ `load_head_to_head()`

4. **แก้ไขชื่อไฟล์ผลลัพธ์** ในฟังก์ชัน `generate_html_report()`:

```python
output_file = os.path.join(self.output_dir, f"new_league_analysis_{datetime.now().strftime('%Y-%m-%d')}.html")
```

5. **อัพเดทสคริปต์ update_index.py** เพื่อรองรับลีกใหม่:

```python
def load_new_league_results(self):
    """Load New League analysis results"""
    print("📊 Loading New League analysis results...")
    
    # Find the latest report file
    report_files = [f for f in os.listdir(self.output_dir) if f.startswith("new_league_analysis_") and f.endswith(".html")]
    # ...
```

6. **อัพเดท index.html** เพื่อเพิ่มส่วนของลีกใหม่:

```html
<!-- New League Section -->
<div id="new-league" class="league-section">
    <h2>🏆 New League Analysis</h2>
    <p>Date: Waiting for update...</p>
    <p>No data available yet.</p>
</div>
```

7. **อัพเดทสคริปต์ run_all_analysis.sh** เพื่อรวมลีกใหม่:

```bash
# Run New League analysis
echo ""
echo "🏆 Running New League analysis..."
python "$PROJECT_DIR/analyze_new_league.py"
```

## 📅 การปรับแต่งสำหรับวันที่อื่น

หากต้องการรันการวิเคราะห์สำหรับวันที่อื่น ให้แก้ไขพารามิเตอร์ `date` ในฟังก์ชัน `load_fixtures()`:

```python
def load_fixtures(self, date="2025-07-19"):  # เปลี่ยนวันที่ตรงนี้
    """Load fixtures for the specified date"""
    print(f"📅 Loading fixtures for date: {date}...")
    # ...
```

หรือสร้างพารามิเตอร์ในฟังก์ชัน `main()` เพื่อให้สามารถกำหนดวันที่ได้จากคอมมานด์ไลน์:

```python
def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze football matches')
    parser.add_argument('--date', type=str, default='2025-07-18', help='Date in YYYY-MM-DD format')
    args = parser.parse_args()
    
    analyzer = ChinaSuperLeagueAnalyzer()
    fixtures = analyzer.load_fixtures(date=args.date)
    # ...
```

แล้วรันด้วยคำสั่ง:

```bash
python analyze_china_super_league.py --date 2025-07-19
```

## ⚙️ การปรับแต่งพารามิเตอร์การวิเคราะห์

### การปรับเส้นมุม

หากต้องการเปลี่ยนเส้นมุมจาก 10.0 เป็นค่าอื่น ให้แก้ไขในคลาสวิเคราะห์:

```python
def __init__(self):
    # ...
    # Corner analysis threshold
    self.corner_threshold = 9.5  # เปลี่ยนเป็นค่าที่ต้องการ
    # ...
```

### การปรับน้ำหนักในการคำนวณ

สามารถปรับน้ำหนักในการคำนวณได้ในฟังก์ชัน `analyze_corners()` และ `run_ultra_advanced_ml()`:

```python
# Calculate expected corners
home_corners_weight = 0.5  # เปลี่ยนจาก 0.4
away_corners_weight = 0.3  # เปลี่ยนจาก 0.4
h2h_corners_weight = 0.2   # คงเดิม
```

### การปรับเกณฑ์ Value Bet

สามารถปรับเกณฑ์ในการระบุ Value Bet ได้:

```python
# Create result
result = {
    # ...
    "value_bet": expected_value > 0.07  # เปลี่ยนจาก 0.05 เป็น 0.07 (7%)
}
```

## 🔌 การเชื่อมต่อกับ API จริง

ระบบปัจจุบันใช้ข้อมูลตัวอย่าง หากต้องการเชื่อมต่อกับ API จริง ให้แก้ไขฟังก์ชัน `load_fixtures()`, `load_team_stats()` และ `load_head_to_head()` ดังนี้:

```python
def load_fixtures(self, date="2025-07-18"):
    """Load fixtures for the specified date"""
    print(f"📅 Loading fixtures for date: {date}...")
    
    import requests
    
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"date": date, "league": self.league_id, "season": self.season}
    headers = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": "YOUR_API_KEY"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    fixtures = []
    for fixture in data.get("response", []):
        fixtures.append({
            "fixture_id": fixture["fixture"]["id"],
            "home_team": fixture["teams"]["home"]["name"],
            "away_team": fixture["teams"]["away"]["name"],
            "datetime": fixture["fixture"]["date"],
            "venue": fixture["fixture"]["venue"]["name"],
            "city": fixture["fixture"]["venue"]["city"]
        })
    
    print(f"✅ Loaded {len(fixtures)} fixtures")
    return fixtures
```

ทำในลักษณะเดียวกันสำหรับฟังก์ชันอื่นๆ

## 🔧 การแก้ไขปัญหาที่พบบ่อย

### 1. สคริปต์ไม่สามารถรันได้

ตรวจสอบว่าได้ติดตั้งไลบรารีที่จำเป็นแล้ว:

```bash
pip install requests beautifulsoup4 numpy pandas
```

### 2. ไม่พบไฟล์หรือโฟลเดอร์

ตรวจสอบว่าได้สร้างโฟลเดอร์ที่จำเป็นแล้ว:

```bash
mkdir -p /Users/80090/Desktop/Project/untitle/data
mkdir -p /Users/80090/Desktop/Project/untitle/output
```

### 3. ไม่สามารถอัพเดท index.html ได้

ตรวจสอบสิทธิ์ในการเขียนไฟล์:

```bash
chmod 644 /Users/80090/Desktop/Project/untitle/index.html
```

### 4. ไม่สามารถเปิดเบราว์เซอร์อัตโนมัติได้

เปิดไฟล์ index.html ด้วยตนเอง:

```bash
open /Users/80090/Desktop/Project/untitle/index.html
```

## 📝 สรุป

คู่มือนี้อธิบายวิธีการใช้งานและปรับแต่งระบบวิเคราะห์ฟุตบอล Ultra Advanced ML สำหรับ China Super League และ Korea K League 1 รวมถึงวิธีการปรับแต่งเพื่อใช้กับลีกอื่นๆ หรือวันที่อื่นๆ หากมีคำถามหรือปัญหาเพิ่มเติม สามารถติดต่อผู้พัฒนาได้
