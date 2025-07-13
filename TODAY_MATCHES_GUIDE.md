# 📅 Today Matches System Guide

## 🎯 Overview
ระบบดึงแมตช์วันนี้จาก API-Football และสร้างตารางการแข่งขันพร้อมหน้าเว็บ

### 📊 Features:
- ✅ ดึงแมตช์จาก API-Football (วันที่ 13 ก.ค. หลังเที่ยง - 14 ก.ค. ก่อนเที่ยง)
- ✅ แสดงราคาต่อรองจริง
- ✅ สร้างตารางครบถ้วน (ลีก, เวลา, ทีม, ราคา, ผล)
- ✅ เว้น Prediction columns ไว้สำหรับคำนวณทีหลัง
- ✅ Export เป็น CSV และสร้างหน้าเว็บ
- ✅ รองรับ 10 ลีกใหญ่

---

## 🚀 Quick Start

### 1. ใช้เวอร์ชันตัวอย่าง (ทดสอบ)
```bash
cd /Users/80090/Desktop/Project/untitle
python3 today_matches_demo.py
```

### 2. ใช้เวอร์ชันจริง (ต้องมี API Key)
```bash
# แก้ไข API Key ในไฟล์
nano today_matches_fetcher.py
# เปลี่ยน API_KEY = "your_api_key_here" เป็น API Key จริง

# รันระบบ
python3 today_matches_fetcher.py
```

---

## 📋 Table Structure

### Columns ที่สร้าง:
| Column | Description | Example |
|--------|-------------|---------|
| **league** | ชื่อลีก | Premier League |
| **match_time_thai** | เวลาแข่ง (เวลาไทย) | 19:30 |
| **home_team** | ทีมเจ้าบ้าน | Manchester City |
| **odds_home** | ราคาต่อรองทีมเจ้าบ้าน | 1.45 |
| **odds_draw** | ราคาต่อรองเสมอ | 4.20 |
| **odds_away** | ราคาต่อรองทีมเยือน | 6.50 |
| **away_team** | ทีมเยือน | Arsenal |
| **home_score** | ประตูทีมเจ้าบ้าน | 2 (ถ้าแข่งเสร็จ) |
| **away_score** | ประตูทีมเยือน | 1 (ถ้าแข่งเสร็จ) |
| **match_result** | ผลการแข่งขัน | Home Win |

### Prediction Columns (เว้นไว้):
| Column | Description | Status |
|--------|-------------|--------|
| **prediction_home_away** | ทำนายผลแมตช์ | 🔮 เร็วๆ นี้ |
| **prediction_handicap** | ทำนายต่อรอง | 🎯 เร็วๆ นี้ |
| **prediction_over_under** | ทำนาย Over/Under | ⚽ เร็วๆ นี้ |
| **prediction_score** | ทำนายสกอร์ | 📊 เร็วๆ นี้ |
| **prediction_corner_1st_half** | ทำนายเตะมุมครึ่งแรก | 🚩 เร็วๆ นี้ |
| **prediction_corner_full_match** | ทำนายเตะมุมเต็มเกม | 🏁 เร็วๆ นี้ |

---

## 🏆 Supported Leagues

### Target Leagues (10 ลีกใหญ่):
1. **Premier League** (England) - ID: 39
2. **La Liga** (Spain) - ID: 140
3. **Bundesliga** (Germany) - ID: 78
4. **Ligue 1** (France) - ID: 61
5. **Serie A** (Italy) - ID: 135
6. **J-League 2** (Japan) - ID: 99
7. **Eredivisie** (Netherlands) - ID: 88
8. **Primeira Liga** (Portugal) - ID: 94
9. **Turkish Super League** - ID: 203
10. **Belgian Pro League** - ID: 144

---

## 📁 Output Files

### 1. CSV File
- **Filename**: `today_matches.csv` (จริง) / `today_matches_demo.csv` (ตัวอย่าง)
- **Format**: UTF-8 with BOM
- **Usage**: สำหรับ import ข้อมูลและคำนวณ predictions

### 2. HTML Website
- **Filename**: `today_matches.html` (จริง) / `today_matches_demo.html` (ตัวอย่าง)
- **Features**: 
  - Responsive design
  - Real-time stats
  - Beautiful UI with glassmorphism
  - Mobile-friendly

---

## 🔧 Technical Details

### Time Zone Handling:
```python
# เวลาไทย (UTC+7)
thailand_tz = pytz.timezone('Asia/Bangkok')
start_time = thailand_tz.localize(datetime(2025, 7, 13, 12, 0, 0))
end_time = thailand_tz.localize(datetime(2025, 7, 14, 12, 0, 0))
```

### API Endpoints Used:
```python
# Fixtures
GET /v3/fixtures?date=2025-07-13

# Odds  
GET /v3/odds?fixture={fixture_id}&bookmaker=8
```

### Error Handling:
- API rate limiting
- Missing odds data
- Network timeouts
- Invalid responses

---

## 🔄 Workflow Integration

### Current Workflow:
1. **Fetch Matches** → `today_matches_fetcher.py`
2. **Create Table** → CSV + HTML files
3. **Manual Predictions** → (เร็วๆ นี้)
4. **Update Files** → เพิ่ม predictions ลง CSV
5. **Display Results** → หน้าเว็บอัปเดตอัตโนมัติ

### Future Integration:
```python
# Step 1: Fetch matches
fetcher = TodayMatchesFetcher(API_KEY)
matches = fetcher.get_today_matches()
df = fetcher.create_matches_dataframe(matches)

# Step 2: Add predictions (เร็วๆ นี้)
predictor = EnhancedMultiLeaguePredictor()
df = predictor.add_predictions_to_dataframe(df)

# Step 3: Update files
fetcher.save_to_csv(df, "today_matches_with_predictions.csv")
fetcher.create_today_matches_website(df)
```

---

## 📊 Sample Output

### CSV Structure:
```csv
league,match_time_thai,home_team,odds_home,odds_draw,odds_away,away_team,home_score,away_score,match_result,prediction_home_away,prediction_handicap,prediction_over_under,prediction_score,prediction_corner_1st_half,prediction_corner_full_match,venue,fixture_id
Premier League,19:30,Manchester City,1.45,4.2,6.5,Arsenal,,,,,,,,,Etihad Stadium,1001
La Liga,21:00,Real Madrid,1.65,3.8,4.5,Barcelona,,,,,,,,,Santiago Bernabéu,1002
```

### Website Features:
- 📊 **Live Stats**: Total matches, leagues, completed/upcoming
- 🎨 **Modern UI**: Glassmorphism design with gradients
- 📱 **Responsive**: Works on all devices
- 🔮 **Prediction Ready**: Columns ready for ML predictions

---

## 🛠️ Customization

### Add New Leagues:
```python
self.target_leagues = {
    39: 'Premier League',
    140: 'La Liga',
    # Add new league
    2: 'Championship',
    3: 'League One'
}
```

### Modify Time Range:
```python
# Change date range
start_time = thailand_tz.localize(datetime(2025, 7, 14, 12, 0, 0))
end_time = thailand_tz.localize(datetime(2025, 7, 15, 12, 0, 0))
```

### Custom Columns:
```python
# Add new prediction columns
'prediction_cards': '',
'prediction_referee_bias': '',
'prediction_weather_impact': ''
```

---

## 🚨 Important Notes

### API Limitations:
- **Rate Limit**: 100 requests/day (free tier)
- **Odds Data**: May not be available for all matches
- **Real-time**: Data updated every 15 minutes

### File Management:
- CSV files overwrite existing data
- HTML files auto-refresh with new data
- Backup important prediction data

### Next Steps:
1. ✅ **Current**: Basic match fetching and display
2. 🔄 **Next**: Integrate ML predictions
3. 🚀 **Future**: Real-time updates and live predictions

---

## 📞 Usage Examples

### Basic Usage:
```bash
# Demo version (no API key needed)
python3 today_matches_demo.py

# Real version (API key required)
python3 today_matches_fetcher.py
```

### Integration with ML:
```python
# Load today's matches
df = pd.read_csv('today_matches.csv')

# Add predictions (coming soon)
# df = add_ml_predictions(df)

# Save updated file
df.to_csv('today_matches_with_predictions.csv', index=False)
```

---

**🎉 Ready to fetch today's matches and create beautiful match tables!**
