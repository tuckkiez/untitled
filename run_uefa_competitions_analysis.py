#!/usr/bin/env python3
"""
🚀 Run UEFA Competitions Analysis - July 17-18, 2025
รันการวิเคราะห์ UEFA Europa League และ UEFA Europa Conference League
"""

import json
import os
from datetime import datetime
import pytz
from uefa_competitions_extended_ml_analysis import UEFACompetitionsExtendedAnalyzer

def load_fixtures():
    """โหลดข้อมูลการแข่งขันจากไฟล์ (ถ้ามี) หรือสร้างข้อมูลตัวอย่าง"""
    try:
        with open('uefa_europa_competitions_extended_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        europa_league = data.get('europa_league', [])
        conference_league = data.get('conference_league', [])
        
        if not europa_league and not conference_league:
            print("❌ ไม่พบข้อมูลการแข่งขัน")
            return None
        
        return {
            'europa_league': europa_league,
            'conference_league': conference_league
        }
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ ไม่สามารถอ่านไฟล์ข้อมูลการแข่งขัน: {e}")
        return None

def analyze_fixtures():
    """วิเคราะห์การแข่งขันด้วย Advanced ML"""
    # โหลดข้อมูลการแข่งขัน
    fixtures = load_fixtures()
    if not fixtures:
        print("❌ ไม่สามารถวิเคราะห์การแข่งขันได้เนื่องจากไม่มีข้อมูล")
        return None
    
    # สร้าง analyzer
    analyzer = UEFACompetitionsExtendedAnalyzer()
    
    # วิเคราะห์ Europa League
    print("\n🏆 กำลังวิเคราะห์ UEFA Europa League...")
    europa_league_analyses = []
    for fixture in fixtures['europa_league']:
        analysis = analyzer.analyze_match(fixture)
        europa_league_analyses.append(analysis)
    print(f"✅ วิเคราะห์ UEFA Europa League สำเร็จ: {len(europa_league_analyses)} รายการ")
    
    # วิเคราะห์ Conference League
    print("\n🏆 กำลังวิเคราะห์ UEFA Europa Conference League...")
    conference_league_analyses = []
    for fixture in fixtures['conference_league']:
        analysis = analyzer.analyze_match(fixture)
        conference_league_analyses.append(analysis)
    print(f"✅ วิเคราะห์ UEFA Europa Conference League สำเร็จ: {len(conference_league_analyses)} รายการ")
    
    # บันทึกผลการวิเคราะห์
    output_data = {
        'europa_league': europa_league_analyses,
        'conference_league': conference_league_analyses,
        'analysis_time': datetime.now().isoformat()
    }
    
    with open('uefa_competitions_extended_ml_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 บันทึกผลการวิเคราะห์ลงไฟล์: uefa_competitions_extended_ml_analysis.json")
    
    return output_data

def generate_html_table(analyses, competition_name):
    """สร้างตาราง HTML สำหรับแสดงผลการวิเคราะห์"""
    if not analyses:
        return f"<div class='competition-container'><h3>{competition_name}</h3><p>No matches available</p></div>"
    
    # เรียงตามวันที่และเวลา
    analyses.sort(key=lambda x: x['kickoff_thai'])
    
    html = f"""
    <div class="competition-container">
        <h3 class="competition-title">{competition_name}</h3>
        <table class="prediction-table">
            <thead>
                <tr>
                    <th>วันที่</th>
                    <th>เวลา (ไทย)</th>
                    <th>คู่แข่งขัน</th>
                    <th>ผลการแข่งขัน</th>
                    <th>สกอร์รวม</th>
                    <th>คอร์เนอร์</th>
                    <th>คอร์เนอร์ครึ่งแรก</th>
                    <th>คอร์เนอร์ครึ่งหลัง</th>
                    <th>แฮนดิแคป</th>
                </tr>
            </thead>
            <tbody>
    """
    
    current_date = None
    
    for match in analyses:
        match_date = match['kickoff_thai'].split(' ')[0]
        match_time = match['kickoff_thai'].split(' ')[1]
        
        # แสดงวันที่เฉพาะเมื่อเปลี่ยนวัน
        date_display = match_date if match_date != current_date else ""
        current_date = match_date
        
        match_result = match['match_result']
        over_under = match['over_under']
        corners_total = match['corners']['total']
        corners_first_half = match['corners']['first_half']
        corners_second_half = match['corners']['second_half']
        handicap = match['handicap']
        
        # กำหนดสีตามความมั่นใจ
        result_class = "high-confidence" if match_result['confidence'] >= 65 else "medium-confidence" if match_result['confidence'] >= 55 else ""
        ou_class = "high-confidence" if over_under['confidence'] >= 65 else "medium-confidence" if over_under['confidence'] >= 55 else ""
        corner_class = "high-confidence" if corners_total['confidence'] >= 65 else "medium-confidence" if corners_total['confidence'] >= 55 else ""
        corner_first_class = "high-confidence" if corners_first_half['confidence'] >= 65 else "medium-confidence" if corners_first_half['confidence'] >= 55 else ""
        corner_second_class = "high-confidence" if corners_second_half['confidence'] >= 65 else "medium-confidence" if corners_second_half['confidence'] >= 55 else ""
        handicap_class = "high-confidence" if handicap['confidence'] >= 65 else "medium-confidence" if handicap['confidence'] >= 55 else ""
        
        html += f"""
            <tr>
                <td>{date_display}</td>
                <td>{match_time}</td>
                <td>{match['home_team']} vs {match['away_team']}</td>
                <td class="{result_class}">{match_result['prediction']} ({match_result['confidence']}%)</td>
                <td class="{ou_class}">{over_under['prediction']} {over_under['line']} ({over_under['confidence']}%)</td>
                <td class="{corner_class}">{corners_total['prediction']} {corners_total['line']} ({corners_total['confidence']}%)</td>
                <td class="{corner_first_class}">{corners_first_half['prediction']} {corners_first_half['line']} ({corners_first_half['confidence']}%)</td>
                <td class="{corner_second_class}">{corners_second_half['prediction']} {corners_second_half['line']} ({corners_second_half['confidence']}%)</td>
                <td class="{handicap_class}">{handicap['prediction']} ({handicap['confidence']}%)</td>
            </tr>
        """
    
    html += """
            </tbody>
        </table>
    </div>
    """
    
    return html

def generate_html_output(analysis_data):
    """สร้างไฟล์ HTML แสดงผลการวิเคราะห์"""
    if not analysis_data:
        print("❌ ไม่สามารถสร้างไฟล์ HTML ได้เนื่องจากไม่มีข้อมูลการวิเคราะห์")
        return False
    
    europa_league_html = generate_html_table(analysis_data['europa_league'], "UEFA Europa League")
    conference_league_html = generate_html_table(analysis_data['conference_league'], "UEFA Europa Conference League")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>UEFA Competitions Extended Analysis - July 17-18, 2025</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .competition-container {{
                margin-bottom: 25px;
                background-color: #fff;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .competition-title {{
                color: #1a365d;
                border-bottom: 2px solid #2a4365;
                padding-bottom: 10px;
                margin-bottom: 15px;
            }}
            .prediction-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 14px;
            }}
            .prediction-table th, .prediction-table td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #e2e8f0;
            }}
            .prediction-table th {{
                background-color: #edf2f7;
                color: #2d3748;
            }}
            .prediction-table tr:hover {{
                background-color: #f7fafc;
            }}
            .high-confidence {{
                color: #2f855a;
                font-weight: bold;
            }}
            .medium-confidence {{
                color: #d69e2e;
            }}
            .analysis-footer {{
                margin-top: 20px;
                font-size: 0.9em;
                color: #718096;
                text-align: right;
            }}
            h1, h2 {{
                color: #2a4365;
            }}
        </style>
    </head>
    <body>
        <h1>UEFA Competitions Extended Analysis - July 17-18, 2025</h1>
        <p>Advanced ML analysis for UEFA Europa League and UEFA Europa Conference League matches</p>
        
        {europa_league_html}
        
        {conference_league_html}
        
        <div class="analysis-footer">
            <p>Last updated: {datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%d %H:%M')} (Thai Time)</p>
            <p>Analysis confidence: High (based on historical team performance data)</p>
        </div>
    </body>
    </html>
    """
    
    with open('uefa_competitions_extended_tables.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"💾 บันทึก HTML ลงไฟล์: uefa_competitions_extended_tables.html")
    return True

def update_index_html(analysis_data):
    """อัปเดตหน้า index.html ด้วยผลการวิเคราะห์"""
    if not analysis_data:
        print("❌ ไม่สามารถอัปเดตหน้า index.html ได้เนื่องจากไม่มีข้อมูลการวิเคราะห์")
        return False
    
    index_path = "/Users/80090/Desktop/Project/untitle/index.html"
    
    try:
        # อ่านไฟล์ index.html
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # สร้างไฟล์สำรอง
        backup_path = f"/Users/80090/Desktop/Project/untitle/index_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ สร้างไฟล์สำรอง {backup_path} สำเร็จ")
        
        # สร้าง HTML สำหรับ UEFA Competitions
        europa_league_html = generate_html_table(analysis_data['europa_league'], "UEFA Europa League")
        conference_league_html = generate_html_table(analysis_data['conference_league'], "UEFA Europa Conference League")
        
        uefa_section = f"""
        <!-- UEFA Competitions Extended Section -->
        <div class="section-container">
            <div class="section-header">
                <h2>🇪🇺 UEFA Competitions Extended Analysis - July 17-18, 2025</h2>
                <p class="section-description">Advanced ML analysis for UEFA Europa League and UEFA Europa Conference League matches</p>
            </div>
            
            {europa_league_html}
            
            {conference_league_html}
            
            <div class="analysis-footer">
                <p>Last updated: {datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%Y-%m-%d %H:%M')} (Thai Time)</p>
                <p>Analysis confidence: High (based on historical team performance data)</p>
            </div>
        </div>
        <!-- End UEFA Competitions Extended Section -->
        """
        
        # ตรวจสอบว่ามีส่วน UEFA อยู่แล้วหรือไม่
        if "<!-- UEFA Competitions Extended Section -->" in html_content:
            # แทนที่ส่วน UEFA เดิม
            start_index = html_content.find("<!-- UEFA Competitions Extended Section -->")
            end_index = html_content.find("<!-- End UEFA Competitions Extended Section -->", start_index) + len("<!-- End UEFA Competitions Extended Section -->")
            html_content = html_content[:start_index] + uefa_section + html_content[end_index:]
        elif "<!-- UEFA Competitions Section -->" in html_content:
            # แทนที่ส่วน UEFA เดิม
            start_index = html_content.find("<!-- UEFA Competitions Section -->")
            end_index = html_content.find("<!-- End UEFA Competitions Section -->", start_index) + len("<!-- End UEFA Competitions Section -->")
            html_content = html_content[:start_index] + uefa_section + html_content[end_index:]
        else:
            # เพิ่มส่วน UEFA ใหม่ก่อน </body>
            html_content = html_content.replace("</body>", f"{uefa_section}\n</body>")
        
        # เพิ่ม CSS ถ้ายังไม่มี
        if "competition-container" not in html_content:
            css = """
            <style>
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
                font-size: 14px;
            }
            
            .prediction-table th, .prediction-table td {
                padding: 8px;
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
            </style>
            """
            html_content = html_content.replace("</head>", f"{css}\n</head>")
        
        # บันทึกไฟล์
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ อัปเดตหน้า index.html สำเร็จ")
        return True
        
    except Exception as e:
        print(f"❌ ไม่สามารถอัปเดตหน้า index.html: {e}")
        return False

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Run UEFA Competitions Analysis - July 17-18, 2025")
    print("=" * 60)
    
    # รันสคริปต์ดึงข้อมูล
    print("\n📥 กำลังรันสคริปต์ดึงข้อมูล...")
    os.system("python uefa_competitions_extended_fetcher.py")
    
    # วิเคราะห์ข้อมูล
    print("\n📊 กำลังวิเคราะห์ข้อมูล...")
    analysis_data = analyze_fixtures()
    
    if analysis_data:
        # สร้างไฟล์ HTML
        print("\n📄 กำลังสร้างไฟล์ HTML...")
        generate_html_output(analysis_data)
        
        # อัปเดตหน้า index.html
        print("\n🔄 กำลังอัปเดตหน้า index.html...")
        update_index_html(analysis_data)
    
    print("\n✅ เสร็จสมบูรณ์!")

if __name__ == "__main__":
    main()
