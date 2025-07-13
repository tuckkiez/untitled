#!/usr/bin/env python3
"""
🇰🇷 Update K League 2 Table UI Fixed - เปลี่ยน UI เป็นตารางแทนการ์ด
แก้ไข: 1) UI เป็นตาราง 2) ลบวันที่ออก 3) ดูง่ายขึ้น
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from k_league_2_fixed_predictions import KLeague2FixedPredictor
import subprocess
from datetime import datetime
import pytz
import re

class KLeague2TableUpdater:
    def __init__(self, api_key):
        self.api_key = api_key
        self.predictor = KLeague2FixedPredictor(api_key)
        self.index_path = '/Users/80090/Desktop/Project/untitle/index.html'
        
    def generate_html_section(self, predictions):
        """สร้าง HTML section แบบตารางสำหรับ K League 2"""
        
        # สร้างแถวตารางสำหรับแต่ละการแข่งขัน
        table_rows = ""
        
        for i, pred in enumerate(predictions, 1):
            match = pred['match']
            p = pred['predictions']
            
            # สีสำหรับความมั่นใจ
            def get_confidence_class(confidence):
                if confidence >= 75:
                    return "high-confidence"  # เขียว
                elif confidence >= 65:
                    return "medium-confidence"  # เหลือง
                else:
                    return "low-confidence"  # แดง
            
            # Match Result
            mr = p['match_result']
            mr_class = get_confidence_class(mr['confidence'])
            
            # Handicap
            hc = p['handicap']
            hc_class = get_confidence_class(hc['confidence'])
            
            # Over/Under
            ou = p['over_under']
            ou_class = get_confidence_class(ou['confidence'])
            
            # Corners
            co = p['corners']
            co_ft_class = get_confidence_class(co['fulltime']['confidence'])
            
            table_rows += f"""
                <tr>
                    <td class="match-teams">
                        <div class="teams-info">
                            <strong>{match['home']} vs {match['away']}</strong>
                            <div class="match-details">
                                <span>⏰ {match['time']}</span>
                                <span>📍 {match['venue']}</span>
                            </div>
                        </div>
                    </td>
                    <td class="prediction-cell {mr_class}">
                        <div class="prediction-main">{mr['prediction']}</div>
                        <div class="confidence">{mr['confidence']}%</div>
                    </td>
                    <td class="prediction-cell {hc_class}">
                        <div class="handicap-line">{hc['line']}</div>
                        <div class="handicap-rec">{hc['prediction']}</div>
                        <div class="confidence">{hc['confidence']}%</div>
                    </td>
                    <td class="prediction-cell {ou_class}">
                        <div class="prediction-main">{ou['prediction']}</div>
                        <div class="confidence">{ou['confidence']}%</div>
                    </td>
                    <td class="prediction-cell {co_ft_class}">
                        <div class="prediction-main">{co['fulltime']['prediction']}</div>
                        <div class="confidence">{co['fulltime']['confidence']}%</div>
                    </td>
                </tr>
            """
        
        # CSS styles
        css_styles = """
        <style>
        .k-league-2-section {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .section-header {
            text-align: center;
            margin-bottom: 25px;
        }
        
        .section-header h2 {
            font-size: 2.2em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .accuracy-badges {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .badge {
            background: rgba(255,255,255,0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            backdrop-filter: blur(10px);
        }
        
        .predictions-table-container {
            overflow-x: auto;
            margin: 20px 0;
        }
        
        .predictions-table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .predictions-table th {
            background: rgba(255,255,255,0.2);
            padding: 15px 10px;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }
        
        .predictions-table td {
            padding: 15px 10px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .match-column {
            min-width: 250px;
        }
        
        .match-teams {
            text-align: left !important;
        }
        
        .teams-info strong {
            display: block;
            font-size: 1.1em;
            margin-bottom: 5px;
        }
        
        .match-details {
            font-size: 0.85em;
            opacity: 0.8;
        }
        
        .match-details span {
            display: inline-block;
            margin-right: 15px;
        }
        
        .prediction-cell {
            min-width: 120px;
        }
        
        .prediction-main {
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 3px;
        }
        
        .handicap-line {
            font-weight: bold;
            color: #ffc107;
            margin-bottom: 3px;
        }
        
        .handicap-rec {
            font-size: 0.9em;
            margin-bottom: 3px;
        }
        
        .confidence {
            font-size: 0.85em;
            opacity: 0.8;
        }
        
        /* สีตามความมั่นใจ */
        .high-confidence {
            background: rgba(40, 167, 69, 0.3) !important;
            border-left: 4px solid #28a745;
        }
        
        .medium-confidence {
            background: rgba(255, 193, 7, 0.3) !important;
            border-left: 4px solid #ffc107;
        }
        
        .low-confidence {
            background: rgba(220, 53, 69, 0.3) !important;
            border-left: 4px solid #dc3545;
        }
        
        .legend {
            margin-top: 25px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            text-align: center;
        }
        
        .legend h3 {
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .legend-items {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .legend-item {
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        
        .legend-item.high-confidence {
            background: rgba(40, 167, 69, 0.3);
            border: 1px solid #28a745;
        }
        
        .legend-item.medium-confidence {
            background: rgba(255, 193, 7, 0.3);
            border: 1px solid #ffc107;
        }
        
        .legend-item.low-confidence {
            background: rgba(220, 53, 69, 0.3);
            border: 1px solid #dc3545;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .k-league-2-section {
                padding: 15px;
            }
            
            .section-header h2 {
                font-size: 1.8em;
            }
            
            .accuracy-badges {
                flex-direction: column;
                align-items: center;
            }
            
            .predictions-table th,
            .predictions-table td {
                padding: 10px 5px;
                font-size: 0.9em;
            }
            
            .match-column {
                min-width: 200px;
            }
            
            .prediction-cell {
                min-width: 100px;
            }
            
            .legend-items {
                flex-direction: column;
                align-items: center;
            }
        }
        </style>
        """
        
        # สร้าง HTML section เต็ม
        html_section = f"""
        <!-- 🇰🇷 K League 2 Advanced ML Predictions -->
        <section class="k-league-2-section">
            <div class="section-header">
                <h2>🇰🇷 K League 2 Advanced ML Predictions</h2>
                <div class="accuracy-badges">
                    <span class="badge">🎯 Overall: 58.8%</span>
                    <span class="badge">⚖️ Handicap: 35%</span>
                    <span class="badge">⚽ O/U: 65%</span>
                    <span class="badge">📐 Corners: 95%</span>
                </div>
            </div>
            
            <div class="predictions-table-container">
                <table class="predictions-table">
                    <thead>
                        <tr>
                            <th class="match-column">การแข่งขัน</th>
                            <th>🎯 ผลการแข่งขัน</th>
                            <th>⚖️ Handicap</th>
                            <th>⚽ Over/Under 2.5</th>
                            <th>📐 Corners</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
            
            <div class="legend">
                <h3>🔍 คำอธิบาย</h3>
                <div class="legend-items">
                    <span class="legend-item high-confidence">🟢 มั่นใจสูง (75%+)</span>
                    <span class="legend-item medium-confidence">🟡 มั่นใจปานกลาง (65-74%)</span>
                    <span class="legend-item low-confidence">🔴 มั่นใจต่ำ (<65%)</span>
                </div>
            </div>
        </section>
        
        {css_styles}
        """
        
        return html_section
    
    def update_index_html(self):
        """อัปเดต index.html ด้วย UI แบบตาราง"""
        try:
            # ทำนายการแข่งขัน
            print("🤖 กำลังทำนายการแข่งขัน K League 2...")
            predictions = self.predictor.get_todays_predictions()
            
            # สร้าง HTML section
            html_section = self.generate_html_section(predictions)
            
            # อ่านไฟล์ index.html
            with open(self.index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ลบ section เก่า (ถ้ามี)
            pattern = r'<!-- 🇰🇷 K League 2 Advanced ML Predictions -->.*?</style>'
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            # หาตำแหน่งที่จะแทรก (หลัง body tag)
            body_start = content.find('<body>')
            if body_start != -1:
                insert_pos = content.find('>', body_start) + 1
                content = content[:insert_pos] + '\n' + html_section + '\n' + content[insert_pos:]
            else:
                # ถ้าไม่เจอ body tag ให้แทรกที่ท้าย
                content = content + '\n' + html_section
            
            # เขียนไฟล์ใหม่
            with open(self.index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ อัปเดต index.html เป็นตารางสำเร็จ!")
            return True
            
        except Exception as e:
            print(f"❌ Error updating index.html: {e}")
            return False
    
    def push_to_github(self):
        """Push การเปลี่ยนแปลงขึ้น GitHub"""
        try:
            # เปลี่ยนไปยัง directory ของโปรเจค
            os.chdir('/Users/80090/Desktop/Project/untitle')
            
            # Git commands
            commands = [
                ['git', 'add', '.'],
                ['git', 'commit', '-m', '🇰🇷 Update K League 2 UI to Table Format - เปลี่ยน UI เป็นตารางแทนการ์ด ดูง่ายขึ้น ลบวันที่ออก'],
                ['git', 'push', 'origin', 'main']
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"❌ Git command failed: {' '.join(cmd)}")
                    print(f"Error: {result.stderr}")
                    return False
                else:
                    print(f"✅ {' '.join(cmd)} - Success")
            
            print("🚀 Push to GitHub สำเร็จ!")
            return True
            
        except Exception as e:
            print(f"❌ Error pushing to GitHub: {e}")
            return False
    
    def run_complete_update(self):
        """รันการอัปเดตแบบครบถ้วน"""
        print("🇰🇷 K League 2 Table UI Update - Starting...")
        print("=" * 60)
        
        # 1. อัปเดต HTML
        if self.update_index_html():
            print("✅ HTML Update: Success")
        else:
            print("❌ HTML Update: Failed")
            return False
        
        # 2. Push to GitHub
        if self.push_to_github():
            print("✅ GitHub Push: Success")
        else:
            print("❌ GitHub Push: Failed")
            return False
        
        print("\n🎉 K League 2 Table UI Update Complete!")
        print("🌐 View at: https://tuckkiez.github.io/untitled/")
        print("\n📊 UI Improvements:")
        print("✅ เปลี่ยนจากการ์ดเป็นตารางที่ดูง่าย")
        print("✅ ลบวันที่ยาวๆ ออก")
        print("✅ แสดงข้อมูลในตารางเดียว")
        print("✅ สีแยกตามความมั่นใจ (เขียว/เหลือง/แดง)")
        print("✅ Responsive สำหรับมือถือ")
        
        return True

if __name__ == "__main__":
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    updater = KLeague2TableUpdater(api_key)
    updater.run_complete_update()
