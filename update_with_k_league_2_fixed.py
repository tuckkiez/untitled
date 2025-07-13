#!/usr/bin/env python3
"""
🇰🇷 Update Index with K League 2 (Fixed)
อัปเดท index.html โดยเพิ่ม K League 2 เข้าไปโดยไม่แก้ UI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from k_league_2_predictor import KLeague2Predictor
import subprocess
from datetime import datetime
import pytz
import re

class IndexUpdater:
    def __init__(self, api_key):
        self.api_key = api_key
        self.predictor = KLeague2Predictor(api_key)
        self.index_path = '/Users/80090/Desktop/Project/untitle/index.html'

    def format_time(self, utc_time):
        """แปลงเวลา UTC เป็นเวลาไทย"""
        try:
            dt = datetime.fromisoformat(utc_time.replace('Z', '+00:00'))
            thai_tz = pytz.timezone('Asia/Bangkok')
            thai_time = dt.astimezone(thai_tz)
            return thai_time.strftime('%H:%M')
        except:
            return "17:00"

    def get_confidence_color(self, confidence):
        """กำหนดสีตามระดับความมั่นใจ"""
        if confidence >= 80:
            return "#4CAF50"  # เขียว
        elif confidence >= 70:
            return "#FF9800"  # ส้ม
        elif confidence >= 60:
            return "#2196F3"  # น้ำเงิน
        else:
            return "#9E9E9E"  # เทา

    def generate_k_league_match_card(self, match):
        """สร้าง HTML สำหรับ K League 2 match card"""
        predictions = match.get('real_predictions', {})
        time = self.format_time(match['fixture']['date'])
        
        venue = match['fixture']['venue']['name'] if match['fixture']['venue']['name'] else 'TBD'
        city = match['fixture']['venue']['city'] if match['fixture']['venue']['city'] else 'TBD'
        
        # สร้าง HTML สำหรับการทำนาย
        result_color = self.get_confidence_color(predictions.get('result_confidence', 65))
        handicap_color = self.get_confidence_color(predictions.get('handicap_confidence', 60))
        ou_color = self.get_confidence_color(predictions.get('ou_confidence', 65))
        corner_ht_color = self.get_confidence_color(predictions.get('corner_ht_confidence', 65))
        corner_ft_color = self.get_confidence_color(predictions.get('corner_ft_confidence', 70))
        
        return f"""
                    <div class="match-card priority-medium">
                        <div class="match-header">
                            <div class="match-status">🔴 Not Started</div>
                            <div class="match-time">{time} ICT</div>
                        </div>
                        <div class="match-teams">
                            <div class="team-name">{match['teams']['home']['name']}</div>
                            <div class="vs">VS</div>
                            <div class="team-name">{match['teams']['away']['name']}</div>
                        </div>
                        <div class="match-venue">{venue}, {city}</div>
                        
                        <div class="predictions-advanced">
                            <div class="pred-section">
                                <h4>🎯 Match Result</h4>
                                <div class="pred-row">
                                    <span class="pred-label">Prediction:</span>
                                    <span class="pred-value" style="color: {result_color}">{predictions.get('result', 'Draw')}</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {predictions.get('result_confidence', 65)}%; background-color: {result_color}"></div>
                                </div>
                                <div class="confidence-text">{predictions.get('result_confidence', 65)}% Confidence</div>
                            </div>
                            
                            <div class="pred-section">
                                <h4>⚖️ Handicap</h4>
                                <div class="pred-row">
                                    <span class="pred-label">Line:</span>
                                    <span class="pred-value" style="color: {handicap_color}">{predictions.get('handicap', '0')}</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {predictions.get('handicap_confidence', 60)}%; background-color: {handicap_color}"></div>
                                </div>
                                <div class="confidence-text">{predictions.get('handicap_confidence', 60)}% Confidence</div>
                            </div>
                            
                            <div class="pred-section">
                                <h4>⚽ Over/Under</h4>
                                <div class="pred-row">
                                    <span class="pred-label">2.5 Goals:</span>
                                    <span class="pred-value" style="color: {ou_color}">{predictions.get('over_under', 'Over 2.5')}</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {predictions.get('ou_confidence', 65)}%; background-color: {ou_color}"></div>
                                </div>
                                <div class="confidence-text">{predictions.get('ou_confidence', 65)}% Confidence</div>
                            </div>
                            
                            <div class="pred-section">
                                <h4>🚩 Corners</h4>
                                <div class="pred-row">
                                    <span class="pred-label">Half-time:</span>
                                    <span class="pred-value" style="color: {corner_ht_color}">{predictions.get('corner_ht', 'Under 4.5')}</span>
                                </div>
                                <div class="pred-row">
                                    <span class="pred-label">Full-time:</span>
                                    <span class="pred-value" style="color: {corner_ft_color}">{predictions.get('corner_ft', 'Over 9.5')}</span>
                                </div>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {(predictions.get('corner_ht_confidence', 65) + predictions.get('corner_ft_confidence', 70)) / 2}%; background-color: {corner_ft_color}"></div>
                                </div>
                                <div class="confidence-text">Avg {int((predictions.get('corner_ht_confidence', 65) + predictions.get('corner_ft_confidence', 70)) / 2)}% Confidence</div>
                            </div>
                        </div>
                    </div>"""

    def update_index_html(self, k_league_matches):
        """อัปเดท index.html โดยเพิ่ม K League 2"""
        
        # อ่านไฟล์ index.html ปัจจุบัน
        with open(self.index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # สร้าง K League 2 section
        k_league_section = f"""
            <div class="league-section">
                <div class="league-header">
                    <div class="league-title">🇰🇷 K League 2 (South Korea)</div>
                    <div class="league-weight">Weight: 0.9</div>
                </div>
                <div class="matches-grid">"""
        
        # เพิ่ม match cards
        for match in k_league_matches:
            k_league_section += self.generate_k_league_match_card(match)
        
        k_league_section += """
                </div>
            </div>"""
        
        # หาตำแหน่งที่จะแทรก K League 2 (ก่อน footer)
        footer_position = html_content.find('<div class="footer">')
        if footer_position != -1:
            # แทรกก่อน footer
            html_content = html_content[:footer_position] + k_league_section + "\n        " + html_content[footer_position:]
        else:
            # ถ้าหา footer ไม่เจอ ให้แทรกก่อน </div> สุดท้าย
            last_div_position = html_content.rfind('</div>\n    </div>\n</body>')
            if last_div_position != -1:
                html_content = html_content[:last_div_position] + k_league_section + "\n        " + html_content[last_div_position:]
        
        # อัปเดตสถิติ
        # อัปเดต Total Matches
        current_matches = re.search(r'<div class="stat-number">(\d+)</div>\s*<div class="stat-label">Total Matches</div>', html_content)
        if current_matches:
            current_count = int(current_matches.group(1))
            new_count = current_count + len(k_league_matches)
            html_content = html_content.replace(
                f'<div class="stat-number">{current_count}</div>',
                f'<div class="stat-number">{new_count}</div>',
                1  # แทนที่แค่ครั้งแรก (Total Matches)
            )
        
        # อัปเดต Leagues Covered
        leagues_pattern = r'(<div class="stat-number">)(\d+)(</div>\s*<div class="stat-label">Leagues Covered</div>)'
        leagues_match = re.search(leagues_pattern, html_content)
        if leagues_match:
            current_count = int(leagues_match.group(2))
            new_count = current_count + 1  # เพิ่ม K League 2
            html_content = re.sub(leagues_pattern, f'\\g<1>{new_count}\\g<3>', html_content)
        
        # อัปเดต Last Updated time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S ICT')
        html_content = re.sub(
            r'Last Updated: [^<]+',
            f'Last Updated: {current_time}',
            html_content
        )
        
        # บันทึกไฟล์
        with open(self.index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Updated index.html with {len(k_league_matches)} K League 2 matches")

    def run_update(self):
        """รันการอัปเดตทั้งหมด"""
        print("🇰🇷 Starting K League 2 Update Process...")
        
        # Step 1: ดึงข้อมูลและทำนาย K League 2
        k_league_matches = self.predictor.run_k_league_analysis()
        
        if not k_league_matches:
            print("❌ No K League 2 matches to update!")
            return
        
        # Step 2: อัปเดท index.html
        print("📝 Updating index.html...")
        self.update_index_html(k_league_matches)
        
        # Step 3: Git operations
        print("📤 Pushing to GitHub...")
        try:
            os.chdir('/Users/80090/Desktop/Project/untitle')
            
            subprocess.run(['git', 'add', '.'], check=True)
            
            commit_message = f"""🇰🇷 Add K League 2 Predictions (17:00 ICT)

✨ Added K League 2 Coverage:
- {len(k_league_matches)} matches at 17:00 ICT
- Advanced 4-value predictions for each match
- Team-specific analysis with ratings
- Real-time Korean football data

🎯 Matches Added:"""
            
            for match in k_league_matches:
                home = match['teams']['home']['name']
                away = match['teams']['away']['name']
                result = match['real_predictions']['result']
                confidence = match['real_predictions']['result_confidence']
                commit_message += f"\n- {home} vs {away}: {result} ({confidence}%)"
            
            commit_message += f"""

📊 Updated Stats:
- Total matches increased by {len(k_league_matches)}
- Added K League 2 to leagues coverage
- Enhanced Korean football predictions
- Maintained existing UI/UX design"""
            
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            
            print("✅ Successfully pushed to GitHub!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            return
        
        # Step 4: สรุปผล
        print("\n" + "=" * 60)
        print("🎉 K LEAGUE 2 UPDATE COMPLETED!")
        print("=" * 60)
        
        print(f"🇰🇷 K League 2 Matches Added: {len(k_league_matches)}")
        print(f"⏰ Match Time: 17:00 ICT (10:00 UTC)")
        print(f"🎯 Prediction Types: 4 (Result, Handicap, O/U, Corners)")
        print(f"🌐 Website: https://tuckkiez.github.io/untitled/")
        
        print("\n🏆 K League 2 Matches:")
        for match in k_league_matches:
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            predictions = match['real_predictions']
            print(f"  • {home} vs {away}")
            print(f"    Result: {predictions['result']} ({predictions['result_confidence']}%)")
            print(f"    Handicap: {predictions['handicap']} ({predictions['handicap_confidence']}%)")
            print(f"    O/U: {predictions['over_under']} ({predictions['ou_confidence']}%)")
            print(f"    Corners: {predictions['corner_ft']} ({predictions['corner_ft_confidence']}%)")
        
        print("\n✅ K League 2 successfully integrated into existing system!")

if __name__ == "__main__":
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    updater = IndexUpdater(api_key)
    updater.run_update()
