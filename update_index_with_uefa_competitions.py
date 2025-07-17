#!/usr/bin/env python3
"""
🚀 Update Index with UEFA Competitions Analysis - July 17, 2025
อัปเดตหน้า index.html ด้วยผลการวิเคราะห์ UEFA Europa League และ UEFA Europa Conference League
"""

import json
import os
import re
from datetime import datetime
import pytz

def read_html_file(file_path):
    """อ่านไฟล์ HTML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ไม่พบไฟล์ {file_path}")
        return None

def write_html_file(file_path, content):
    """เขียนไฟล์ HTML"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ บันทึกไฟล์ {file_path} สำเร็จ")
        return True
    except Exception as e:
        print(f"❌ ไม่สามารถบันทึกไฟล์ {file_path}: {e}")
        return False

def create_backup(file_path):
    """สร้างไฟล์สำรอง"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{file_path.rsplit('.', 1)[0]}_backup_{timestamp}.{file_path.rsplit('.', 1)[1]}"
    
    try:
        content = read_html_file(file_path)
        if content:
            write_html_file(backup_path, content)
            print(f"✅ สร้างไฟล์สำรอง {backup_path} สำเร็จ")
            return True
    except Exception as e:
        print(f"❌ ไม่สามารถสร้างไฟล์สำรอง: {e}")
    
    return False

def generate_uefa_competitions_section():
    """สร้างส่วนแสดงผลการวิเคราะห์ UEFA Competitions"""
    try:
        # อ่านผลการวิเคราะห์จากไฟล์
        with open('uefa_competitions_ml_analysis.json', 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        europa_league = analysis_data.get('europa_league', [])
        conference_league = analysis_data.get('conference_league', [])
        
        # เรียงตามเวลาแข่ง
        europa_league.sort(key=lambda x: x['kickoff_thai'])
        conference_league.sort(key=lambda x: x['kickoff_thai'])
        
        # สร้าง HTML สำหรับ Europa League
        europa_league_html = generate_competition_table(europa_league, "UEFA Europa League")
        
        # สร้าง HTML สำหรับ Conference League
        conference_league_html = generate_competition_table(conference_league, "UEFA Europa Conference League")
        
        # รวม HTML ทั้งหมด
        uefa_section = f"""
        <!-- UEFA Competitions Section -->
        <div class="section-container">
            <div class="section-header">
                <h2>🇪🇺 UEFA Competitions Analysis - July 17, 2025</h2>
                <p class="section-description">Advanced ML analysis for UEFA Europa League and UEFA Europa Conference League matches</p>
            </div>
            
            {europa_league_html}
            
            {conference_league_html}
            
            <div class="analysis-footer">
                <p>Last updated: {datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%d %H:%M')} (Thai Time)</p>
                <p>Analysis confidence: High (based on historical team performance data)</p>
            </div>
        </div>
        <!-- End UEFA Competitions Section -->
        """
        
        return uefa_section
    
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ ไม่สามารถอ่านไฟล์ผลการวิเคราะห์: {e}")
        return generate_empty_uefa_section()

def generate_competition_table(matches, competition_name):
    """สร้างตารางแสดงผลการวิเคราะห์สำหรับแต่ละการแข่งขัน"""
    if not matches:
        return f"<div class='competition-container'><h3>{competition_name}</h3><p>No matches available</p></div>"
    
    html = f"""
    <div class="competition-container">
        <h3 class="competition-title">{competition_name}</h3>
        <table class="prediction-table">
            <thead>
                <tr>
                    <th>เวลา (ไทย)</th>
                    <th>คู่แข่งขัน</th>
                    <th>ผลการแข่งขัน</th>
                    <th>สกอร์รวม</th>
                    <th>คอร์เนอร์</th>
                    <th>แฮนดิแคป</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for match in matches:
        match_result = match['match_result']
        over_under = match['over_under']
        corners = match['corners']
        handicap = match['handicap']
        
        # กำหนดสีตามความมั่นใจ
        result_class = "high-confidence" if match_result['confidence'] >= 65 else "medium-confidence" if match_result['confidence'] >= 55 else ""
        ou_class = "high-confidence" if over_under['confidence'] >= 65 else "medium-confidence" if over_under['confidence'] >= 55 else ""
        corner_class = "high-confidence" if corners['confidence'] >= 65 else "medium-confidence" if corners['confidence'] >= 55 else ""
        handicap_class = "high-confidence" if handicap['confidence'] >= 65 else "medium-confidence" if handicap['confidence'] >= 55 else ""
        
        html += f"""
            <tr>
                <td>{match['kickoff_thai'].split(' ')[1]}</td>
                <td>{match['home_team']} vs {match['away_team']}</td>
                <td class="{result_class}">{match_result['prediction']} ({match_result['confidence']}%)</td>
                <td class="{ou_class}">{over_under['prediction']} {over_under['line']} ({over_under['confidence']}%)</td>
                <td class="{corner_class}">{corners['prediction']} {corners['line']} ({corners['confidence']}%)</td>
                <td class="{handicap_class}">{handicap['prediction']} ({handicap['confidence']}%)</td>
            </tr>
        """
    
    html += """
            </tbody>
        </table>
    </div>
    """
    
    return html

def generate_empty_uefa_section():
    """สร้างส่วน UEFA ว่างเปล่า"""
    return """
    <!-- UEFA Competitions Section -->
    <div class="section-container">
        <div class="section-header">
            <h2>🇪🇺 UEFA Competitions Analysis - July 17, 2025</h2>
            <p class="section-description">Advanced ML analysis for UEFA Europa League and UEFA Europa Conference League matches</p>
        </div>
        
        <div class="competition-container">
            <h3 class="competition-title">UEFA Europa League</h3>
            <p>No matches available for today</p>
        </div>
        
        <div class="competition-container">
            <h3 class="competition-title">UEFA Europa Conference League</h3>
            <p>No matches available for today</p>
        </div>
        
        <div class="analysis-footer">
            <p>Last updated: {datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%d %H:%M')} (Thai Time)</p>
        </div>
    </div>
    <!-- End UEFA Competitions Section -->
    """

def add_uefa_styles(html_content):
    """เพิ่ม CSS สำหรับส่วน UEFA"""
    uefa_styles = """
    /* UEFA Competitions Styles */
    .competition-container {
        margin-bottom: 25px;
        background-color: #fff;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .competition-title {
        color: #1a365d;
        border-bottom: 2px solid #2a4365;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    .prediction-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    
    .prediction-table th, .prediction-table td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .prediction-table th {
        background-color: #edf2f7;
        color: #2d3748;
    }
    
    .prediction-table tr:hover {
        background-color: #f7fafc;
    }
    
    .high-confidence {
        color: #2f855a;
        font-weight: bold;
    }
    
    .medium-confidence {
        color: #d69e2e;
    }
    
    .analysis-footer {
        margin-top: 20px;
        font-size: 0.9em;
        color: #718096;
        text-align: right;
    }
    /* End UEFA Competitions Styles */
    """
    
    # ตรวจสอบว่ามี style อยู่แล้วหรือไม่
    if "</style>" in html_content:
        # แทรก CSS ก่อน </style>
        return html_content.replace("</style>", f"{uefa_styles}\n</style>")
    else:
        # เพิ่ม style ใหม่ใน head
        return html_content.replace("</head>", f"<style>\n{uefa_styles}\n</style>\n</head>")

def update_index_html():
    """อัปเดตไฟล์ index.html"""
    index_path = "/Users/80090/Desktop/Project/untitle/index.html"
    
    # อ่านไฟล์ index.html
    html_content = read_html_file(index_path)
    if not html_content:
        print("❌ ไม่สามารถอ่านไฟล์ index.html")
        return False
    
    # สร้างไฟล์สำรอง
    create_backup(index_path)
    
    # สร้างส่วน UEFA Competitions
    uefa_section = generate_uefa_competitions_section()
    
    # เพิ่ม CSS
    html_content = add_uefa_styles(html_content)
    
    # ตรวจสอบว่ามีส่วน UEFA อยู่แล้วหรือไม่
    uefa_pattern = r"<!-- UEFA Competitions Section -->.*?<!-- End UEFA Competitions Section -->"
    if re.search(uefa_pattern, html_content, re.DOTALL):
        # แทนที่ส่วน UEFA เดิม
        html_content = re.sub(uefa_pattern, uefa_section, html_content, flags=re.DOTALL)
    else:
        # เพิ่มส่วน UEFA ใหม่หลังจาก Champions League หรือส่วนอื่นๆ
        # ลองหาตำแหน่งที่เหมาะสม
        insertion_points = [
            "<!-- End UEFA Champions League Section -->",
            "</main>",
            "<footer"
        ]
        
        inserted = False
        for point in insertion_points:
            if point in html_content:
                html_content = html_content.replace(point, f"{uefa_section}\n\n{point}")
                inserted = True
                break
        
        if not inserted:
            # ถ้าไม่พบตำแหน่งที่เหมาะสม ให้เพิ่มก่อน </body>
            html_content = html_content.replace("</body>", f"{uefa_section}\n</body>")
    
    # บันทึกไฟล์
    return write_html_file(index_path, html_content)

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Update Index with UEFA Competitions Analysis - July 17, 2025")
    print("=" * 60)
    
    # รันสคริปต์วิเคราะห์ก่อน
    print("\n📊 กำลังรันสคริปต์วิเคราะห์...")
    os.system("python uefa_competitions_ml_analysis.py")
    
    # อัปเดตหน้า index.html
    print("\n🔄 กำลังอัปเดตหน้า index.html...")
    if update_index_html():
        print("✅ อัปเดตหน้า index.html สำเร็จ")
    else:
        print("❌ ไม่สามารถอัปเดตหน้า index.html")
    
    print("\n✅ เสร็จสมบูรณ์!")

if __name__ == "__main__":
    main()
