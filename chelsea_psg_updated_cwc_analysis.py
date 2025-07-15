#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 CHELSEA vs PSG - UPDATED FIFA CWC ANALYSIS
Updated with latest FIFA Club World Cup results (July 2025)
Advanced ML Analysis with Real Performance Data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

class UpdatedChelsePSGAnalyzer:
    def __init__(self):
        self.analysis_date = "2025-07-13"
        self.match_info = {
            "teams": "Chelsea vs Paris Saint-Germain",
            "competition": "International Friendly / Pre-season",
            "analysis_type": "Updated FIFA CWC Performance Analysis"
        }
        
    def analyze_psg_cwc_performance(self):
        """วิเคราะห์ผลงาน PSG ใน FIFA CWC 2025"""
        psg_matches = [
            {"date": "2025-07-10", "opponent": "Real Madrid", "result": "4-0", "venue": "N", "handicap": "-0/0.5", "ou": "O", "ht": "3-0"},
            {"date": "2025-07-05", "opponent": "Bayern Munich", "result": "2-0", "venue": "N", "handicap": "-0", "ou": "U", "ht": "0-0"},
            {"date": "2025-06-29", "opponent": "Inter Miami", "result": "4-0", "venue": "N", "handicap": "-2.5", "ou": "O", "ht": "4-0"},
            {"date": "2025-06-24", "opponent": "Seattle Sounders", "result": "2-0", "venue": "A", "handicap": "-2/2.5", "ou": "U", "ht": "0-1"},
            {"date": "2025-06-20", "opponent": "Botafogo", "result": "0-1", "venue": "N", "handicap": "-1.5", "ou": "U", "ht": "0-1"},
            {"date": "2025-06-16", "opponent": "Atletico Madrid", "result": "4-0", "venue": "N", "handicap": "-0.5", "ou": "O", "ht": "2-0"}
        ]
        
        # คำนวณสถิติ PSG
        total_matches = len(psg_matches)
        wins = sum(1 for m in psg_matches if m["result"].split("-")[0] > m["result"].split("-")[1])
        losses = sum(1 for m in psg_matches if m["result"].split("-")[0] < m["result"].split("-")[1])
        
        goals_for = sum(int(m["result"].split("-")[0]) for m in psg_matches)
        goals_against = sum(int(m["result"].split("-")[1]) for m in psg_matches)
        
        over_25 = sum(1 for m in psg_matches if m["ou"] == "O")
        clean_sheets = sum(1 for m in psg_matches if int(m["result"].split("-")[1]) == 0)
        
        psg_stats = {
            "matches_played": total_matches,
            "wins": wins,
            "losses": losses,
            "win_rate": wins / total_matches * 100,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goals_per_match": goals_for / total_matches,
            "goals_conceded_per_match": goals_against / total_matches,
            "over_25_rate": over_25 / total_matches * 100,
            "clean_sheet_rate": clean_sheets / total_matches * 100,
            "form": "WWWWLW"  # ล่าสุด 6 นัด
        }
        
        return psg_stats
    
    def analyze_chelsea_cwc_performance(self):
        """วิเคราะห์ผลงาน Chelsea ใน FIFA CWC 2025"""
        chelsea_matches = [
            {"date": "2025-07-09", "opponent": "Fluminense", "result": "2-0", "venue": "A", "handicap": "-1", "ou": "U", "ht": "0-1"},
            {"date": "2025-07-05", "opponent": "Palmeiras", "result": "2-1", "venue": "A", "handicap": "-0.5", "ou": "O", "ht": "0-1"},
            {"date": "2025-06-29", "opponent": "Benfica", "result": "1-1", "venue": "N", "handicap": "-0.5", "ou": "U", "ht": "0-0", "note": "90min[1-1], 120min[1-4]"},
            {"date": "2025-06-25", "opponent": "Esperance Tunis", "result": "3-0", "venue": "A", "handicap": "-1.5", "ou": "O", "ht": "0-2"},
            {"date": "2025-06-21", "opponent": "Flamengo", "result": "1-3", "venue": "A", "handicap": "-0/0.5", "ou": "O", "ht": "0-1"},
            {"date": "2025-06-17", "opponent": "Los Angeles", "result": "2-0", "venue": "N", "handicap": "-1.5", "ou": "U", "ht": "1-0"}
        ]
        
        # คำนวณสถิติ Chelsea
        total_matches = len(chelsea_matches)
        wins = sum(1 for m in chelsea_matches if m["result"].split("-")[0] > m["result"].split("-")[1])
        draws = sum(1 for m in chelsea_matches if m["result"].split("-")[0] == m["result"].split("-")[1])
        losses = sum(1 for m in chelsea_matches if m["result"].split("-")[0] < m["result"].split("-")[1])
        
        goals_for = sum(int(m["result"].split("-")[0]) for m in chelsea_matches)
        goals_against = sum(int(m["result"].split("-")[1]) for m in chelsea_matches)
        
        over_25 = sum(1 for m in chelsea_matches if m["ou"] == "O")
        clean_sheets = sum(1 for m in chelsea_matches if int(m["result"].split("-")[1]) == 0)
        
        chelsea_stats = {
            "matches_played": total_matches,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "win_rate": wins / total_matches * 100,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goals_per_match": goals_for / total_matches,
            "goals_conceded_per_match": goals_against / total_matches,
            "over_25_rate": over_25 / total_matches * 100,
            "clean_sheet_rate": clean_sheets / total_matches * 100,
            "form": "WWDWLW"  # ล่าสุด 6 นัด
        }
        
        return chelsea_stats
    
    def calculate_updated_predictions(self, psg_stats, chelsea_stats):
        """คำนวณการทำนายใหม่ตามผลงาน FIFA CWC"""
        
        # Team Strength Calculation (0-100)
        psg_strength = (
            psg_stats["win_rate"] * 0.3 +
            psg_stats["goals_per_match"] * 10 * 0.25 +
            (100 - psg_stats["goals_conceded_per_match"] * 20) * 0.25 +
            psg_stats["clean_sheet_rate"] * 0.2
        )
        
        chelsea_strength = (
            chelsea_stats["win_rate"] * 0.3 +
            chelsea_stats["goals_per_match"] * 10 * 0.25 +
            (100 - chelsea_stats["goals_conceded_per_match"] * 20) * 0.25 +
            chelsea_stats["clean_sheet_rate"] * 0.2
        )
        
        # Form Factor (recent 6 matches)
        psg_form_score = 5 * 0.8  # 5W, 1L = 83.3%
        chelsea_form_score = 4 * 0.7  # 4W, 1D, 1L = 66.7%
        
        # Adjusted Strength
        psg_adjusted = psg_strength + psg_form_score
        chelsea_adjusted = chelsea_strength + chelsea_form_score
        
        total_strength = psg_adjusted + chelsea_adjusted
        
        # Match Result Predictions
        psg_win_prob = psg_adjusted / total_strength
        chelsea_win_prob = chelsea_adjusted / total_strength
        draw_prob = 0.25  # Base draw probability
        
        # Normalize
        total_prob = psg_win_prob + chelsea_win_prob + draw_prob
        psg_win_prob = psg_win_prob / total_prob
        chelsea_win_prob = chelsea_win_prob / total_prob
        draw_prob = draw_prob / total_prob
        
        # Goals Prediction
        expected_psg_goals = psg_stats["goals_per_match"] * 0.7 + chelsea_stats["goals_conceded_per_match"] * 0.3
        expected_chelsea_goals = chelsea_stats["goals_per_match"] * 0.7 + psg_stats["goals_conceded_per_match"] * 0.3
        
        total_goals = expected_psg_goals + expected_chelsea_goals
        
        # Over/Under 2.5
        over_25_prob = min(85, max(15, (total_goals - 2.0) * 30 + 50))
        under_25_prob = 100 - over_25_prob
        
        # Both Teams Score
        psg_score_prob = min(90, max(10, expected_psg_goals * 35 + 20))
        chelsea_score_prob = min(90, max(10, expected_chelsea_goals * 35 + 20))
        bts_yes_prob = (psg_score_prob * chelsea_score_prob) / 100
        bts_no_prob = 100 - bts_yes_prob
        
        return {
            "team_strength": {
                "psg": round(psg_adjusted, 1),
                "chelsea": round(chelsea_adjusted, 1)
            },
            "match_result": {
                "psg_win": round(psg_win_prob * 100, 1),
                "draw": round(draw_prob * 100, 1),
                "chelsea_win": round(chelsea_win_prob * 100, 1)
            },
            "goals": {
                "expected_psg": round(expected_psg_goals, 2),
                "expected_chelsea": round(expected_chelsea_goals, 2),
                "total_expected": round(total_goals, 2)
            },
            "over_under": {
                "over_25": round(over_25_prob, 1),
                "under_25": round(under_25_prob, 1)
            },
            "both_teams_score": {
                "yes": round(bts_yes_prob, 1),
                "no": round(bts_no_prob, 1)
            }
        }
    
    def generate_analysis_report(self):
        """สร้างรายงานการวิเคราะห์แบบครบถ้วน"""
        
        print("🔥" * 50)
        print("🏆 CHELSEA vs PSG - UPDATED FIFA CWC ANALYSIS")
        print("📅 Analysis Date:", self.analysis_date)
        print("🔥" * 50)
        
        # วิเคราะห์ผลงาน
        psg_stats = self.analyze_psg_cwc_performance()
        chelsea_stats = self.analyze_chelsea_cwc_performance()
        
        print("\n🇫🇷 PARIS SAINT-GERMAIN - FIFA CWC 2025 PERFORMANCE")
        print("=" * 60)
        print(f"📊 Matches Played: {psg_stats['matches_played']}")
        print(f"🏆 Wins: {psg_stats['wins']} ({psg_stats['win_rate']:.1f}%)")
        print(f"❌ Losses: {psg_stats['losses']}")
        print(f"⚽ Goals For: {psg_stats['goals_for']} ({psg_stats['goals_per_match']:.2f} per match)")
        print(f"🥅 Goals Against: {psg_stats['goals_against']} ({psg_stats['goals_conceded_per_match']:.2f} per match)")
        print(f"📈 Over 2.5 Rate: {psg_stats['over_25_rate']:.1f}%")
        print(f"🛡️ Clean Sheets: {psg_stats['clean_sheet_rate']:.1f}%")
        print(f"📋 Recent Form: {psg_stats['form']}")
        
        print("\n🏴󠁧󠁢󠁥󠁮󠁧󠁿 CHELSEA - FIFA CWC 2025 PERFORMANCE")
        print("=" * 60)
        print(f"📊 Matches Played: {chelsea_stats['matches_played']}")
        print(f"🏆 Wins: {chelsea_stats['wins']} ({chelsea_stats['win_rate']:.1f}%)")
        print(f"🤝 Draws: {chelsea_stats['draws']}")
        print(f"❌ Losses: {chelsea_stats['losses']}")
        print(f"⚽ Goals For: {chelsea_stats['goals_for']} ({chelsea_stats['goals_per_match']:.2f} per match)")
        print(f"🥅 Goals Against: {chelsea_stats['goals_against']} ({chelsea_stats['goals_conceded_per_match']:.2f} per match)")
        print(f"📈 Over 2.5 Rate: {chelsea_stats['over_25_rate']:.1f}%")
        print(f"🛡️ Clean Sheets: {chelsea_stats['clean_sheet_rate']:.1f}%")
        print(f"📋 Recent Form: {chelsea_stats['form']}")
        
        # คำนวณการทำนาย
        predictions = self.calculate_updated_predictions(psg_stats, chelsea_stats)
        
        print("\n🎯 UPDATED PREDICTIONS")
        print("=" * 60)
        print(f"💪 Team Strength:")
        print(f"   🇫🇷 PSG: {predictions['team_strength']['psg']}")
        print(f"   🏴󠁧󠁢󠁥󠁮󠁧󠁿 Chelsea: {predictions['team_strength']['chelsea']}")
        
        print(f"\n🏆 Match Result:")
        print(f"   🇫🇷 PSG Win: {predictions['match_result']['psg_win']}%")
        print(f"   🤝 Draw: {predictions['match_result']['draw']}%")
        print(f"   🏴󠁧󠁢󠁥󠁮󠁧󠁿 Chelsea Win: {predictions['match_result']['chelsea_win']}%")
        
        print(f"\n⚽ Goals Prediction:")
        print(f"   🇫🇷 PSG Expected: {predictions['goals']['expected_psg']}")
        print(f"   🏴󠁧󠁢󠁥󠁮󠁧󠁿 Chelsea Expected: {predictions['goals']['expected_chelsea']}")
        print(f"   📊 Total Expected: {predictions['goals']['total_expected']}")
        
        print(f"\n📊 Over/Under 2.5:")
        print(f"   📈 Over 2.5: {predictions['over_under']['over_25']}%")
        print(f"   📉 Under 2.5: {predictions['over_under']['under_25']}%")
        
        print(f"\n🎯 Both Teams Score:")
        print(f"   ✅ Yes: {predictions['both_teams_score']['yes']}%")
        print(f"   ❌ No: {predictions['both_teams_score']['no']}%")
        
        # Key Insights
        print("\n🔍 KEY INSIGHTS")
        print("=" * 60)
        
        if psg_stats['win_rate'] > chelsea_stats['win_rate']:
            print("🔥 PSG มีฟอร์มที่ดีกว่าใน FIFA CWC 2025")
        else:
            print("🔥 Chelsea มีฟอร์มที่ดีกว่าใน FIFA CWC 2025")
            
        if psg_stats['goals_per_match'] > 2.5:
            print("⚽ PSG มีพลังโจมตีสูงมาก (>2.5 goals/match)")
        
        if chelsea_stats['clean_sheet_rate'] > 50:
            print("🛡️ Chelsea มีการป้องกันที่แข็งแกร่ง")
            
        if predictions['goals']['total_expected'] > 2.5:
            print("📈 คาดว่าจะเป็นเกมที่มีประตูเยอะ")
        else:
            print("📉 คาดว่าจะเป็นเกมที่มีประตูน้อย")
        
        print("\n🎯 BETTING RECOMMENDATIONS")
        print("=" * 60)
        
        # หาค่าที่แนะนำ
        max_prob = max(predictions['match_result'].values())
        if max_prob == predictions['match_result']['psg_win']:
            print("🥇 PRIMARY: PSG Win")
        elif max_prob == predictions['match_result']['chelsea_win']:
            print("🥇 PRIMARY: Chelsea Win")
        else:
            print("🥇 PRIMARY: Draw")
            
        if predictions['over_under']['over_25'] > 60:
            print("🥈 SECONDARY: Over 2.5 Goals")
        elif predictions['over_under']['under_25'] > 60:
            print("🥈 SECONDARY: Under 2.5 Goals")
            
        if predictions['both_teams_score']['yes'] > 60:
            print("🥉 TERTIARY: Both Teams Score - Yes")
        elif predictions['both_teams_score']['no'] > 60:
            print("🥉 TERTIARY: Both Teams Score - No")
        
        print("\n" + "🔥" * 50)
        print("✅ ANALYSIS COMPLETE - UPDATED WITH FIFA CWC 2025 DATA")
        print("🔥" * 50)
        
        return {
            "psg_stats": psg_stats,
            "chelsea_stats": chelsea_stats,
            "predictions": predictions,
            "analysis_date": self.analysis_date
        }

def main():
    """Main execution function"""
    analyzer = UpdatedChelsePSGAnalyzer()
    results = analyzer.generate_analysis_report()
    
    # Save results to JSON
    with open('/Users/80090/Desktop/Project/untitle/chelsea_psg_updated_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to: chelsea_psg_updated_analysis.json")

if __name__ == "__main__":
    main()
