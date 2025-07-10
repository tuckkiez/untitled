# คู่มือการใช้งานระบบทำนายผลฟุตบอล

## ภาพรวมระบบ

ระบบนี้ประกอบด้วย 5 ไฟล์หลัก:

1. **`football_predictor.py`** - โมเดล Machine Learning สำหรับทำนาย
2. **`data_loader.py`** - โหลดข้อมูลจากแหล่งต่างๆ
3. **`main.py`** - ไฟล์หลักสำหรับรันระบบ
4. **`advanced_example.py`** - ตัวอย่างการวิเคราะห์ขั้นสูง
5. **`real_data_example.py`** - การใช้งานกับข้อมูลจริงจาก API

## การติดตั้งและเตรียมพร้อม

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. ตรวจสอบการติดตั้ง
```bash
python main.py --help
```

## วิธีการใช้งาน

### 1. การใช้งานพื้นฐาน

#### ทำนายผลการแข่งขัน
```bash
python main.py --predict "Arsenal" "Chelsea"
```

#### วิเคราะห์ผลงานทีม
```bash
python main.py --analyze
```

#### ทำ Backtest
```bash
python main.py --backtest
```

#### แสดงกราฟผล Backtest
```bash
python main.py --backtest --plot
```

#### รันทุกฟีเจอร์พร้อมกัน
```bash
python main.py --analyze --backtest --plot --predict "Liverpool" "Manchester City"
```

### 2. การใช้งานกับข้อมูลของคุณเอง

#### เตรียมไฟล์ CSV
สร้างไฟล์ CSV ที่มีคอลัมน์:
- `date`: วันที่ (YYYY-MM-DD)
- `home_team`: ทีมเหย้า
- `away_team`: ทีมเยือน
- `home_goals`: ประตูทีมเหย้า
- `away_goals`: ประตูทีมเยือน

ตัวอย่าง:
```csv
date,home_team,away_team,home_goals,away_goals
2024-01-15,Arsenal,Chelsea,2,1
2024-01-22,Liverpool,Manchester City,1,1
2024-01-29,Tottenham,Manchester United,3,0
```

#### ใช้งานกับไฟล์ CSV
```bash
python main.py --data-source csv --data-path "your_data.csv" --predict "Team1" "Team2"
```

### 3. การวิเคราะห์ขั้นสูง

#### รันการวิเคราะห์แบบครบถ้วน
```bash
python advanced_example.py
```

การวิเคราะห์ขั้นสูงจะให้:
- ข้อมูลที่สมจริงมากขึ้น (2 ฤดูกาล)
- การเปรียบเทียบวิธีการทำนายต่างๆ
- ความแม่นยำแยกตามทีม
- การทำนายตัวอย่างหลายคู่

### 4. การใช้งานกับข้อมูลจริงจาก API

#### สมัคร API Key
1. ไปที่ https://www.football-data.org/client/register
2. สมัครสมาชิกฟรี
3. รับ API key

#### ใช้งานกับข้อมูลจริง
```python
from real_data_example import RealDataPredictor

predictor = RealDataPredictor()
api_key = "YOUR_API_KEY_HERE"

results = predictor.run_real_prediction(api_key, season=2024)
```

## ผลลัพธ์ที่ได้

### 1. การทำนาย
```
=== การทำนาย: Arsenal vs Chelsea ===
การทำนาย: Home Win
ความมั่นใจ: 0.654 (65.4%)

ความน่าจะเป็นของแต่ละผล:
  Away Win: 0.234 (23.4%)
  Draw: 0.112 (11.2%)
  Home Win: 0.654 (65.4%)
```

### 2. การวิเคราะห์ทีม
```
             team  games  wins  draws  losses  points  win_rate
        Arsenal     19     8      9       2      33     0.421
        Chelsea     19     4      3      12      15     0.211
```

### 3. Backtest
```
=== Backtest ===
จำนวนเกมที่ทดสอบ: 50
ทำนายถูก: 32
ความแม่นยำ: 0.640 (64.0%)
```

### 4. ไฟล์ที่สร้างขึ้น
- `sample_matches.csv` - ข้อมูลตัวอย่าง
- `team_analysis.csv` - ผลการวิเคราะห์ทีม
- `backtest_analysis.png` - กราฟผล backtest
- `real_predictions.csv` - การทำนายจากข้อมูลจริง

## อัลกอริทึมและ Features

### Features ที่ใช้ (15 features):
1. **อัตราชนะ** ทีมเหย้า/เยือน
2. **อัตราเสมอ** ทีมเหย้า/เยือน
3. **อัตราแพ้** ทีมเหย้า/เยือน
4. **ประตูเฉลี่ยที่ทำได้** ทีมเหย้า/เยือน
5. **ประตูเฉลี่ยที่เสีย** ทีมเหย้า/เยือน
6. **ผลต่างประตู** ทีมเหย้า/เยือน
7. **ความแตกต่างอัตราชนะ** ระหว่างทีม
8. **ความแตกต่างผลต่างประตู** ระหว่างทีม
9. **ความได้เปรียบเหย้า** (Home Advantage)

### โมเดล Machine Learning:
- **Random Forest Classifier** (100 trees)
- **Cross Validation** เพื่อป้องกัน overfitting
- **Stratified Split** เพื่อความสมดุลของข้อมูล

## ข้อจำกัดและข้อแนะนำ

### ข้อจำกัด:
1. **ข้อมูลขั้นต่ำ**: ต้องมีอย่างน้อย 50 เกม
2. **ทีมใหม่**: ใช้สถิติเริ่มต้นสำหรับทีมที่ไม่มีประวัติ
3. **ปัจจัยภายนอก**: ไม่รวมการบาดเจ็บ, สภาพอากาศ, etc.

### ข้อแนะนำ:
1. **ข้อมูลมากขึ้น**: ยิ่งมีข้อมูลมาก ความแม่นยำยิ่งสูง
2. **อัปเดตสม่ำเสมอ**: เพิ่มข้อมูลใหม่เป็นประจำ
3. **ตรวจสอบชื่อทีม**: ให้ตรงกับข้อมูลที่มี

## การแก้ไขปัญหาที่พบบ่อย

### 1. ข้อผิดพลาด "ไม่สามารถเทรนโมเดลได้"
**สาเหตุ**: ข้อมูลไม่เพียงพอ (น้อยกว่า 50 เกม)
**แก้ไข**: เพิ่มข้อมูลหรือใช้ข้อมูลตัวอย่าง

### 2. ข้อผิดพลาด "ไม่สามารถทำนายได้"
**สาเหตุ**: ชื่อทีมไม่ตรงกับข้อมูล
**แก้ไข**: ตรวจสอบชื่อทีมในไฟล์ข้อมูล

### 3. ความแม่นยำต่ำ
**สาเหตุ**: ข้อมูลไม่เพียงพอหรือไม่มีคุณภาพ
**แก้ไข**: เพิ่มข้อมูลหรือปรับปรุงคุณภาพข้อมูล

### 4. API Error
**สาเหตุ**: API key ไม่ถูกต้องหรือเกิน rate limit
**แก้ไข**: ตรวจสอบ API key หรือรอสักครู่

## ตัวอย่างการใช้งานจริง

### สคริปต์สำหรับการทำนายประจำสัปดาห์:
```bash
#!/bin/bash
# weekly_prediction.sh

echo "=== การทำนายประจำสัปดาห์ ==="
python main.py --data-source csv --data-path "current_season.csv" \
    --predict "Arsenal" "Chelsea" \
    --predict "Liverpool" "Manchester City" \
    --predict "Tottenham" "Manchester United" \
    --backtest --analyze
```

### การใช้งานใน Python Script:
```python
from football_predictor import FootballPredictor
import pandas as pd

# โหลดข้อมูล
df = pd.read_csv('your_data.csv')

# สร้างและเทรนโมเดล
predictor = FootballPredictor()
predictor.train(df)

# ทำนาย
result = predictor.predict_match('Arsenal', 'Chelsea', df)
print(f"การทำนาย: {result['prediction']}")
print(f"ความมั่นใจ: {result['confidence']:.3f}")
```

## การพัฒนาต่อ

### ฟีเจอร์ที่สามารถเพิ่มได้:
1. **ข้อมูลผู้เล่น**: สถิติและการบาดเจ็บ
2. **ข้อมูลการเดิมพัน**: Odds จากเว็บเดิมพัน
3. **ปัจจัยสภาพอากาศ**: อุณหภูมิ, ฝน
4. **Deep Learning**: ใช้ Neural Networks
5. **การทำนายสกอร์**: ทำนายผลที่แน่นอน

### การปรับปรุงโมเดล:
1. **Feature Engineering**: สร้าง features ใหม่
2. **Hyperparameter Tuning**: ปรับค่าพารามิเตอร์
3. **Ensemble Methods**: รวมหลายโมเดล
4. **Time Series**: ใช้ข้อมูลเวลาในการทำนาย

---

**หมายเหตุ**: ระบบนี้เป็นเครื่องมือสำหรับการศึกษาและความบันเทิง ไม่ควรใช้สำหรับการเดิมพันจริง
