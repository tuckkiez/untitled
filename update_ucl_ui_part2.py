#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 UEFA CHAMPIONS LEAGUE UI UPDATER - PART 2
สร้าง Match Cards สำหรับแมตช์ UCL จริง
"""

from datetime import datetime
import json

class UCLMatchCardsGenerator:
    def __init__(self):
        self.ucl_matches_data = [
            {
                "match_num": 1,
                "home_team": "Kairat Almaty",
                "away_team": "Olimpija Ljubljana",
                "home_country": "Kazakhstan",
                "away_country": "Slovenia",
                "date": "2025-07-15T15:00:00+00:00",
                "venue": "Ortalyq stadion",
                "home_strength": 2.9,
                "away_strength": 2.9,
                "predictions": {
                    "match_result": {"home_win": 80.5, "draw": 12.0, "away_win": 7.5},
                    "over_under_25": {"over": 18.9, "under": 81.1},
                    "both_teams_score": {"yes": 16.1, "no": 83.9},
                    "corners": {"over_8": 26.5, "under_8": 73.5}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Kairat Almaty Win", "confidence": 80.5},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 81.1},
                    {"rank": "🥉 TERTIARY", "bet": "Both Teams Score - No", "confidence": 83.9}
                ]
            },
            {
                "match_num": 2,
                "home_team": "Lincoln Red Imps FC",
                "away_team": "Vikingur Gota",
                "home_country": "Gibraltar",
                "away_country": "Faroe Islands",
                "date": "2025-07-15T15:30:00+00:00",
                "venue": "Europa Point Stadium",
                "home_strength": 2.8,
                "away_strength": 2.2,
                "predictions": {
                    "match_result": {"home_win": 75.5, "draw": 21.5, "away_win": 3.0},
                    "over_under_25": {"over": 26.3, "under": 73.7},
                    "both_teams_score": {"yes": 42.8, "no": 57.2},
                    "corners": {"over_8": 10.0, "under_8": 90.0}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Lincoln Red Imps Win", "confidence": 75.5},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 73.7}
                ]
            },
            {
                "match_num": 3,
                "home_team": "Milsami Orhei",
                "away_team": "KuPS",
                "home_country": "Moldova",
                "away_country": "Finland",
                "date": "2025-07-15T17:00:00+00:00",
                "venue": "Complexul Sportiv Raional",
                "home_strength": 2.4,
                "away_strength": 3.9,
                "predictions": {
                    "match_result": {"home_win": 55.0, "draw": 15.5, "away_win": 29.5},
                    "over_under_25": {"over": 27.1, "under": 72.9},
                    "both_teams_score": {"yes": 23.3, "no": 76.7},
                    "corners": {"over_8": 14.6, "under_8": 85.4}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Milsami Orhei Win", "confidence": 55.0},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 72.9},
                    {"rank": "🥉 TERTIARY", "bet": "Both Teams Score - No", "confidence": 76.7}
                ]
            },
            {
                "match_num": 4,
                "home_team": "Hamrun Spartans",
                "away_team": "FK Zalgiris Vilnius",
                "home_country": "Malta",
                "away_country": "Lithuania",
                "date": "2025-07-15T17:00:00+00:00",
                "venue": "Ta'Qali National Stadium",
                "home_strength": 2.7,
                "away_strength": 3.6,
                "predictions": {
                    "match_result": {"home_win": 55.5, "draw": 17.5, "away_win": 27.0},
                    "over_under_25": {"over": 29.5, "under": 70.5},
                    "both_teams_score": {"yes": 11.1, "no": 88.9},
                    "corners": {"over_8": 43.8, "under_8": 56.2}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Hamrun Spartans Win", "confidence": 55.5},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 70.5},
                    {"rank": "🥉 TERTIARY", "bet": "Both Teams Score - No", "confidence": 88.9}
                ]
            },
            {
                "match_num": 5,
                "home_team": "Malmo FF",
                "away_team": "Saburtalo",
                "home_country": "Sweden",
                "away_country": "Georgia",
                "date": "2025-07-15T17:00:00+00:00",
                "venue": "Eleda Stadion",
                "home_strength": 4.8,
                "away_strength": 3.7,
                "predictions": {
                    "match_result": {"home_win": 52.0, "draw": 42.5, "away_win": 5.5},
                    "over_under_25": {"over": 33.0, "under": 67.0},
                    "both_teams_score": {"yes": 58.3, "no": 41.7},
                    "corners": {"over_8": 34.0, "under_8": 66.0}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Malmo FF Win", "confidence": 52.0},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 67.0}
                ]
            },
            {
                "match_num": 6,
                "home_team": "Rīgas FS",
                "away_team": "FC Levadia Tallinn",
                "home_country": "Latvia",
                "away_country": "Estonia",
                "date": "2025-07-15T17:00:00+00:00",
                "venue": "LNK Sporta Parks",
                "home_strength": 3.2,
                "away_strength": 2.9,
                "predictions": {
                    "match_result": {"home_win": 76.5, "draw": 17.0, "away_win": 6.5},
                    "over_under_25": {"over": 16.7, "under": 83.3},
                    "both_teams_score": {"yes": 30.0, "no": 70.0},
                    "corners": {"over_8": 33.4, "under_8": 66.6}
                },
                "betting_recommendations": [
                    {"rank": "🥇 PRIMARY", "bet": "Rīgas FS Win", "confidence": 76.5},
                    {"rank": "🥈 SECONDARY", "bet": "Under 2.5 Goals", "confidence": 83.3},
                    {"rank": "🥉 TERTIARY", "bet": "Both Teams Score - No", "confidence": 70.0}
                ]
            }
        ]
    
    def format_time(self, iso_time):
        """แปลงเวลาเป็นรูปแบบที่อ่านง่าย"""
        try:
            dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
            # Convert to Bangkok time (UTC+7)
            bangkok_time = dt.replace(tzinfo=None)
            return bangkok_time.strftime("%H:%M")
        except:
            return "TBD"
    
    def generate_match_card(self, match_data):
        """สร้าง HTML สำหรับ match card"""
        
        # Determine if high confidence
        max_confidence = max([rec["confidence"] for rec in match_data["betting_recommendations"]])
        high_confidence_class = "high-confidence" if max_confidence > 70 else ""
        
        time_str = self.format_time(match_data["date"])
        
        html = f"""
        <div class="match-card {high_confidence_class}">
            <div class="match-header">
                <div class="match-title">⚽ MATCH {match_data['match_num']}</div>
                <div class="match-time">{time_str}</div>
            </div>
            
            <div class="venue-info">
                🏟️ {match_data['venue']} | 📍 1st Qualifying Round
            </div>
            
            <div class="teams-section">
                <div class="team">
                    <div class="team-name">🏠 {match_data['home_team']}</div>
                    <div class="team-country">({match_data['home_country']})</div>
                    <div class="team-strength">{match_data['home_strength']}/10</div>
                </div>
                <div class="vs">VS</div>
                <div class="team">
                    <div class="team-name">✈️ {match_data['away_team']}</div>
                    <div class="team-country">({match_data['away_country']})</div>
                    <div class="team-strength">{match_data['away_strength']}/10</div>
                </div>
            </div>
            
            <div class="predictions-section">
                <div class="prediction-category">
                    <div class="category-title">🏆 Match Result</div>
                    <div class="prediction-bars">
                        <div class="prediction-bar">
                            <div class="prediction-fill" style="width: {match_data['predictions']['match_result']['home_win']}%">
                                {match_data['predictions']['match_result']['home_win']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill draw" style="width: {match_data['predictions']['match_result']['draw']}%">
                                {match_data['predictions']['match_result']['draw']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill away" style="width: {match_data['predictions']['match_result']['away_win']}%">
                                {match_data['predictions']['match_result']['away_win']}%
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
                            <div class="prediction-fill over" style="width: {match_data['predictions']['over_under_25']['over']}%">
                                {match_data['predictions']['over_under_25']['over']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill under" style="width: {match_data['predictions']['over_under_25']['under']}%">
                                {match_data['predictions']['over_under_25']['under']}%
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
                            <div class="prediction-fill over" style="width: {match_data['predictions']['both_teams_score']['yes']}%">
                                {match_data['predictions']['both_teams_score']['yes']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill under" style="width: {match_data['predictions']['both_teams_score']['no']}%">
                                {match_data['predictions']['both_teams_score']['no']}%
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
                            <div class="prediction-fill over" style="width: {match_data['predictions']['corners']['over_8']}%">
                                {match_data['predictions']['corners']['over_8']}%
                            </div>
                        </div>
                        <div class="prediction-bar">
                            <div class="prediction-fill under" style="width: {match_data['predictions']['corners']['under_8']}%">
                                {match_data['predictions']['corners']['under_8']}%
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
        
        # Add betting recommendations
        for rec in match_data["betting_recommendations"]:
            html += f"""
                <div class="bet-item">
                    <div>
                        <span class="bet-rank">{rec['rank']}</span>
                        {rec['bet']}
                    </div>
                    <div class="bet-confidence">{rec['confidence']}%</div>
                </div>"""
        
        html += """
            </div>
        </div>"""
        
        return html
    
    def generate_all_match_cards(self):
        """สร้าง HTML สำหรับ match cards ทั้งหมด"""
        
        cards_html = '<div class="matches-grid">\n'
        
        for match in self.ucl_matches_data:
            cards_html += self.generate_match_card(match)
            cards_html += '\n'
        
        cards_html += '</div>\n'
        
        return cards_html
    
    def save_match_cards(self):
        """บันทึก match cards HTML"""
        cards_html = self.generate_all_match_cards()
        
        with open('/Users/80090/Desktop/Project/untitle/ucl_match_cards.html', 'w', encoding='utf-8') as f:
            f.write(cards_html)
        
        print("✅ UCL Match Cards created successfully!")
        return cards_html

def main():
    """Main execution"""
    generator = UCLMatchCardsGenerator()
    
    print("🚀 Creating UEFA Champions League Match Cards...")
    
    try:
        generator.save_match_cards()
        print("✅ Part 2 completed - Match cards ready!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
