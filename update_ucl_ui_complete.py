#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 UEFA CHAMPIONS LEAGUE UI UPDATER - COMPLETE
รวมทุกส่วนและสร้าง UI สมบูรณ์ พร้อมลบข้อมูลเก่า
"""

import os
import shutil
from datetime import datetime

class UCLCompleteUIUpdater:
    def __init__(self):
        self.analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # ข้อมูลแมตช์ที่เหลือ (7-12)
        self.remaining_matches = [
            {
                "match_num": 7,
                "home_team": "FC Differdange 03",
                "away_team": "Drita",
                "home_country": "Luxembourg",
                "away_country": "Kosovo",
                "date": "2025-07-15T18:00:00+00:00",
                "venue": "Stade Municipal Differdange Terrain 2 Synthetique",
                "home_strength": 2.3,
                "away_strength": 3.2,
                "predictions": {
                    "match_result": {"home_win": 64.0, "draw": 21.5, "away_win": 14.5},
                    "over_under_25": {"over": 57.4, "under": 42.6},
                    "both_teams_score": {"yes": 29.4, "no": 70.6},
                    "corners": {"over_8": 46.8, "under_8": 53.2}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "FC Differdange Win", "confidence": 64.0},
                    {"rank": "🥉 TERTIARY", "bet": "Both Teams Score - No", "confidence": 70.6}
                ]
            },
            {
                "match_num": 8,
                "home_team": "Shkendija",
                "away_team": "The New Saints",
                "home_country": "North Macedonia",
                "away_country": "Wales",
                "date": "2025-07-15T18:00:00+00:00",
                "venue": "Toše Proeski Arena",
                "home_strength": 3.4,
                "away_strength": 3.7,
                "predictions": {
                    "match_result": {"home_win": 52.0, "draw": 19.0, "away_win": 29.0},
                    "over_under_25": {"over": 19.1, "under": 80.9},
                    "both_teams_score": {"yes": 35.6, "no": 64.4},
                    "corners": {"over_8": 29.5, "under_8": 70.5}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Shkendija Win", "confidence": 52.0},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 80.9},
                    {"rank": "🥉 TERTIARY", "bet": "Both Teams Score - No", "confidence": 64.4}
                ]
            },
            {
                "match_num": 9,
                "home_team": "Inter Club d'Escaldes",
                "away_team": "FCSB",
                "home_country": "Andorra",
                "away_country": "Romania",
                "date": "2025-07-15T18:30:00+00:00",
                "venue": "Nou Estadi Encamp",
                "home_strength": 1.9,
                "away_strength": 4.3,
                "predictions": {
                    "match_result": {"home_win": 52.5, "draw": 20.5, "away_win": 27.0},
                    "over_under_25": {"over": 14.4, "under": 85.6},
                    "both_teams_score": {"yes": 14.4, "no": 85.6},
                    "corners": {"over_8": 10.0, "under_8": 90.0}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Inter Escaldes Win", "confidence": 52.5},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 85.6},
                    {"rank": "🥉 TERTIARY", "bet": "Both Teams Score - No", "confidence": 85.6}
                ]
            },
            {
                "match_num": 10,
                "home_team": "Zrinjski",
                "away_team": "Virtus",
                "home_country": "Bosnia and Herzegovina",
                "away_country": "San Marino",
                "date": "2025-07-15T19:00:00+00:00",
                "venue": "Stadion Bijeli Brijeg",
                "home_strength": 3.7,
                "away_strength": 1.3,
                "predictions": {
                    "match_result": {"home_win": 53.5, "draw": 40.0, "away_win": 6.5},
                    "over_under_25": {"over": 9.3, "under": 90.7},
                    "both_teams_score": {"yes": 58.3, "no": 41.7},
                    "corners": {"over_8": 30.5, "under_8": 69.5}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Zrinjski Win", "confidence": 53.5},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 90.7}
                ]
            },
            {
                "match_num": 11,
                "home_team": "Breidablik",
                "away_team": "Egnatia Rrogozhinë",
                "home_country": "Iceland",
                "away_country": "Albania",
                "date": "2025-07-15T19:00:00+00:00",
                "venue": "Kópavogsvöllur",
                "home_strength": 3.4,
                "away_strength": 3.4,
                "predictions": {
                    "match_result": {"home_win": 72.0, "draw": 16.0, "away_win": 12.0},
                    "over_under_25": {"over": 20.3, "under": 79.7},
                    "both_teams_score": {"yes": 25.6, "no": 74.4},
                    "corners": {"over_8": 27.3, "under_8": 72.7}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Breidablik Win", "confidence": 72.0},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 79.7},
                    {"rank": "🥉 TERTIARY", "bet": "Both Teams Score - No", "confidence": 74.4}
                ]
            },
            {
                "match_num": 12,
                "home_team": "Buducnost Podgorica",
                "away_team": "FC Noah",
                "home_country": "Montenegro",
                "away_country": "Armenia",
                "date": "2025-07-15T19:00:00+00:00",
                "venue": "Stadion Pod Goricom",
                "home_strength": 3.2,
                "away_strength": 2.9,
                "predictions": {
                    "match_result": {"home_win": 76.5, "draw": 17.0, "away_win": 6.5},
                    "over_under_25": {"over": 16.7, "under": 83.3},
                    "both_teams_score": {"yes": 30.0, "no": 70.0},
                    "corners": {"over_8": 33.4, "under_8": 66.6}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Buducnost Win", "confidence": 76.5},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 83.3},
                    {"rank": "🥉 TERTIARY", "bet": "Both Teams Score - No", "confidence": 70.0}
                ]
            }
        ]
    
    def format_time(self, iso_time):
        """แปลงเวลาเป็นรูปแบบที่อ่านง่าย"""
        try:
            dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
            return dt.strftime("%H:%M")
        except:
            return "TBD"
    
    def generate_remaining_match_cards(self):
        """สร้าง match cards สำหรับแมตช์ที่เหลือ"""
        cards_html = ""
        
        for match in self.remaining_matches:
            max_confidence = max([rec["confidence"] for rec in match["betting_recommendations"]])
            high_confidence_class = "high-confidence" if max_confidence > 70 else ""
            time_str = self.format_time(match["date"])
            
            cards_html += f"""
        <div class="match-card {high_confidence_class}">
            <div class="match-header">
                <div class="match-title">⚽ MATCH {match['match_num']}</div>
                <div class="match-time">{time_str}</div>
            </div>
            
            <div class="venue-info">
                🏟️ {match['venue']} | 📍 1st Qualifying Round
            </div>
            
            <div class="teams-section">
                <div class="team">
                    <div class="team-name">🏠 {match['home_team']}</div>
                    <div class="team-country">({match['home_country']})</div>
                    <div class="team-strength">{match['home_strength']}/10</div>
                </div>
                <div class="vs">VS</div>
                <div class="team">
                    <div class="team-name">✈️ {match['away_team']}</div>
                    <div class="team-country">({match['away_country']})</div>
                    <div class="team-strength">{match['away_strength']}/10</div>
                </div>
            </div>
            
            <div class="predictions-section">
                <div class="prediction-category">
                    <div class="category-title">🏆 Match Result</div>
                    <div class="prediction-bars">
                        <div class="prediction-bar">
                            <div class="prediction-fill" style="width: {match['predictions']['match_result']['home_win']}%">
                                {match['predictions']['match_result']['home_win']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill draw" style="width: {match['predictions']['match_result']['draw']}%">
                                {match['predictions']['match_result']['draw']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill away" style="width: {match['predictions']['match_result']['away_win']}%">
                                {match['predictions']['match_result']['away_win']}%
                            </div>
                        </div>
                    </div>
                    <div class="prediction-labels">
                        <span>Home Win</span>
                        <span>Draw</span>
                        <span>Away Win</span>
                    </div>
                </div>
                
                <div class="prediction-category">
                    <div class="category-title">⚽ Over/Under 2.5</div>
                    <div class="prediction-bars">
                        <div class="prediction-bar">
                            <div class="prediction-fill over" style="width: {match['predictions']['over_under_25']['over']}%">
                                {match['predictions']['over_under_25']['over']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill under" style="width: {match['predictions']['over_under_25']['under']}%">
                                {match['predictions']['over_under_25']['under']}%
                            </div>
                        </div>
                    </div>
                    <div class="prediction-labels">
                        <span>Over 2.5</span>
                        <span>Under 2.5</span>
                    </div>
                </div>
                
                <div class="prediction-category">
                    <div class="category-title">🎯 Both Teams Score</div>
                    <div class="prediction-bars">
                        <div class="prediction-bar">
                            <div class="prediction-fill over" style="width: {match['predictions']['both_teams_score']['yes']}%">
                                {match['predictions']['both_teams_score']['yes']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill under" style="width: {match['predictions']['both_teams_score']['no']}%">
                                {match['predictions']['both_teams_score']['no']}%
                            </div>
                        </div>
                    </div>
                    <div class="prediction-labels">
                        <span>Yes</span>
                        <span>No</span>
                    </div>
                </div>
                
                <div class="prediction-category">
                    <div class="category-title">🚩 Corners</div>
                    <div class="prediction-bars">
                        <div class="prediction-bar">
                            <div class="prediction-fill over" style="width: {match['predictions']['corners']['over_8']}%">
                                {match['predictions']['corners']['over_8']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill under" style="width: {match['predictions']['corners']['under_8']}%">
                                {match['predictions']['corners']['under_8']}%
                            </div>
                        </div>
                    </div>
                    <div class="prediction-labels">
                        <span>Over 8</span>
                        <span>Under 8</span>
                    </div>
                </div>
            </div>
            
            <div class="betting-recommendations">
                <div class="betting-title">💰 BETTING RECOMMENDATIONS</div>"""
            
            for rec in match["betting_recommendations"]:
                cards_html += f"""
                <div class="bet-item">
                    <div>
                        <span class="bet-rank">{rec['rank']}</span>
                        {rec['bet']}
                    </div>
                    <div class="bet-confidence">{rec['confidence']}%</div>
                </div>"""
            
            cards_html += """
            </div>
        </div>"""
        
        return cards_html
    
    def generate_footer(self):
        """สร้าง footer"""
        return f"""
        <div class="footer">
            <div class="update-time">
                📅 Last Updated: {self.analysis_date} (Bangkok Time)
            </div>
            <div class="ml-info">
                🤖 Powered by Advanced Machine Learning | 📊 Real Data from RapidAPI Football
            </div>
            <div class="confidence-legend">
                <div class="legend-item">
                    <div class="legend-color legend-high"></div>
                    <span>High Confidence (70%+)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color legend-medium"></div>
                    <span>Medium Confidence (50-70%)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color legend-low"></div>
                    <span>Low Confidence (<50%)</span>
                </div>
            </div>
            <div style="margin-top: 20px; font-size: 0.9em; opacity: 0.8;">
                🏆 UEFA Champions League 2025-26 Qualifying Round 1<br>
                Advanced ML Analysis with 63.8% Average Confidence
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def backup_old_index(self):
        """สำรองไฟล์ index.html เก่า"""
        try:
            if os.path.exists('/Users/80090/Desktop/Project/untitle/index.html'):
                backup_name = f'/Users/80090/Desktop/Project/untitle/index_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
                shutil.copy('/Users/80090/Desktop/Project/untitle/index.html', backup_name)
                print(f"✅ Old index.html backed up to: {backup_name}")
        except Exception as e:
            print(f"⚠️ Could not backup old index.html: {str(e)}")
    
    def create_complete_ucl_ui(self):
        """สร้าง UI สมบูรณ์"""
        print("🚀 Creating Complete UEFA Champions League UI...")
        
        # สำรองไฟล์เก่า
        self.backup_old_index()
        
        # อ่าน header
        try:
            with open('/Users/80090/Desktop/Project/untitle/ucl_ui_header.html', 'r', encoding='utf-8') as f:
                header_html = f.read()
        except FileNotFoundError:
            print("❌ Header file not found. Please run part 1 first.")
            return False
        
        # อ่าน match cards แรก
        try:
            with open('/Users/80090/Desktop/Project/untitle/ucl_match_cards.html', 'r', encoding='utf-8') as f:
                first_cards_html = f.read()
        except FileNotFoundError:
            print("❌ Match cards file not found. Please run part 2 first.")
            return False
        
        # สร้าง match cards ที่เหลือ
        remaining_cards_html = self.generate_remaining_match_cards()
        
        # รวม match cards ทั้งหมด
        all_cards_html = first_cards_html.replace('</div>', remaining_cards_html + '</div>')
        
        # สร้าง footer
        footer_html = self.generate_footer()
        
        # รวมทุกส่วน
        complete_html = header_html + all_cards_html + footer_html
        
        # บันทึกเป็น index.html ใหม่
        with open('/Users/80090/Desktop/Project/untitle/index.html', 'w', encoding='utf-8') as f:
            f.write(complete_html)
        
        print("✅ Complete UEFA Champions League UI created!")
        print("🏆 New index.html with real UCL matches is ready!")
        
        # ลบไฟล์ชั่วคราว
        try:
            os.remove('/Users/80090/Desktop/Project/untitle/ucl_ui_header.html')
            os.remove('/Users/80090/Desktop/Project/untitle/ucl_match_cards.html')
            print("🧹 Temporary files cleaned up")
        except:
            pass
        
        return True

def main():
    """Main execution"""
    updater = UCLCompleteUIUpdater()
    
    print("🏆 Starting Complete UEFA Champions League UI Update...")
    
    try:
        success = updater.create_complete_ucl_ui()
        
        if success:
            print("\n" + "🏆" * 50)
            print("🏆 UEFA CHAMPIONS LEAGUE UI UPDATE COMPLETE!")
            print("🏆" * 50)
            print("✅ Old data removed and replaced with real UCL matches")
            print("✅ 12 real matches with Advanced ML analysis")
            print("✅ High confidence predictions highlighted")
            print("✅ Ready for viewing at index.html")
        else:
            print("❌ UI update failed")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
