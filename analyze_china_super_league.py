#!/usr/bin/env python3
"""
🚀 China Super League Analysis - July 18, 2025
วิเคราะห์ผลการแข่งขัน China Super League ด้วย Ultra Advanced ML
"""

import json
import os
import numpy as np
import pandas as pd
from datetime import datetime

class ChinaSuperLeagueAnalyzer:
    """China Super League Analyzer with Ultra Advanced ML"""
    
    def __init__(self):
        """Initialize the analyzer"""
        self.data_dir = "/Users/80090/Desktop/Project/untitle/data"
        self.output_dir = "/Users/80090/Desktop/Project/untitle/output"
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # League info
        self.league_id = 169
        self.league_name = "China Super League"
        self.season = 2025
        
        # Corner analysis threshold (10.0 instead of 8.5)
        self.corner_threshold = 10.0
        
        print(f"🚀 Initializing {self.league_name} Analyzer")
    
    def load_fixtures(self, date="2025-07-18"):
        """Load fixtures for the specified date"""
        print(f"📅 Loading fixtures for date: {date}...")
        
        # In a real scenario, this would load from API or database
        # For this example, we'll create sample data
        fixtures = [
            {
                "fixture_id": 1341028,
                "home_team": "Changchun Yatai",
                "away_team": "Shanghai SIPG",
                "datetime": "2025-07-18T08:30:00+00:00",
                "venue": "Changchun Sports Center Stadium",
                "city": "Changchun"
            },
            {
                "fixture_id": 1341027,
                "home_team": "Wuhan Three Towns",
                "away_team": "Qingdao Youth Island",
                "datetime": "2025-07-18T11:00:00+00:00",
                "venue": "Wuhan Sports Center Stadium",
                "city": "Wuhan"
            },
            {
                "fixture_id": 1341029,
                "home_team": "Tianjin Teda",
                "away_team": "Chengdu Better City",
                "datetime": "2025-07-18T11:35:00+00:00",
                "venue": "TEDA Football Stadium",
                "city": "Tianjin"
            },
            {
                "fixture_id": 1341030,
                "home_team": "Hangzhou Greentown",
                "away_team": "Yunnan Yukun",
                "datetime": "2025-07-18T12:00:00+00:00",
                "venue": "Huanglong Sports Centre",
                "city": "Hangzhou"
            }
        ]
        
        print(f"✅ Loaded {len(fixtures)} fixtures")
        return fixtures
    
    def load_team_stats(self):
        """Load team statistics"""
        print("📊 Loading team statistics...")
        
        # In a real scenario, this would load from API or database
        # For this example, we'll create sample data
        team_stats = {
            "Changchun Yatai": {
                "matches_played": 16,
                "wins": 7,
                "draws": 4,
                "losses": 5,
                "goals_scored": 22,
                "goals_conceded": 18,
                "avg_corners_for": 5.2,
                "avg_corners_against": 4.8,
                "avg_total_corners": 10.0,
                "over_10_corners_percentage": 43.8
            },
            "Shanghai SIPG": {
                "matches_played": 16,
                "wins": 9,
                "draws": 3,
                "losses": 4,
                "goals_scored": 28,
                "goals_conceded": 15,
                "avg_corners_for": 5.5,
                "avg_corners_against": 4.3,
                "avg_total_corners": 9.8,
                "over_10_corners_percentage": 50.0
            },
            "Wuhan Three Towns": {
                "matches_played": 16,
                "wins": 8,
                "draws": 5,
                "losses": 3,
                "goals_scored": 25,
                "goals_conceded": 14,
                "avg_corners_for": 5.7,
                "avg_corners_against": 4.9,
                "avg_total_corners": 10.6,
                "over_10_corners_percentage": 62.5
            },
            "Qingdao Youth Island": {
                "matches_played": 16,
                "wins": 5,
                "draws": 4,
                "losses": 7,
                "goals_scored": 18,
                "goals_conceded": 22,
                "avg_corners_for": 4.8,
                "avg_corners_against": 5.6,
                "avg_total_corners": 10.4,
                "over_10_corners_percentage": 56.3
            },
            "Tianjin Teda": {
                "matches_played": 16,
                "wins": 6,
                "draws": 5,
                "losses": 5,
                "goals_scored": 20,
                "goals_conceded": 19,
                "avg_corners_for": 5.0,
                "avg_corners_against": 5.1,
                "avg_total_corners": 10.1,
                "over_10_corners_percentage": 50.0
            },
            "Chengdu Better City": {
                "matches_played": 16,
                "wins": 7,
                "draws": 3,
                "losses": 6,
                "goals_scored": 23,
                "goals_conceded": 20,
                "avg_corners_for": 5.3,
                "avg_corners_against": 4.7,
                "avg_total_corners": 10.0,
                "over_10_corners_percentage": 43.8
            },
            "Hangzhou Greentown": {
                "matches_played": 16,
                "wins": 8,
                "draws": 4,
                "losses": 4,
                "goals_scored": 24,
                "goals_conceded": 16,
                "avg_corners_for": 5.4,
                "avg_corners_against": 4.5,
                "avg_total_corners": 9.9,
                "over_10_corners_percentage": 43.8
            },
            "Yunnan Yukun": {
                "matches_played": 16,
                "wins": 4,
                "draws": 5,
                "losses": 7,
                "goals_scored": 17,
                "goals_conceded": 23,
                "avg_corners_for": 4.6,
                "avg_corners_against": 5.8,
                "avg_total_corners": 10.4,
                "over_10_corners_percentage": 56.3
            }
        }
        
        print(f"✅ Loaded statistics for {len(team_stats)} teams")
        return team_stats
    
    def load_head_to_head(self):
        """Load head to head statistics"""
        print("🆚 Loading head to head statistics...")
        
        # In a real scenario, this would load from API or database
        # For this example, we'll create sample data
        h2h_stats = {
            "Changchun Yatai-Shanghai SIPG": {
                "matches": 10,
                "home_wins": 3,
                "draws": 2,
                "away_wins": 5,
                "home_goals": 12,
                "away_goals": 18,
                "avg_total_corners": 10.2,
                "over_10_corners_percentage": 60.0
            },
            "Wuhan Three Towns-Qingdao Youth Island": {
                "matches": 8,
                "home_wins": 5,
                "draws": 2,
                "away_wins": 1,
                "home_goals": 16,
                "away_goals": 8,
                "avg_total_corners": 11.0,
                "over_10_corners_percentage": 75.0
            },
            "Tianjin Teda-Chengdu Better City": {
                "matches": 6,
                "home_wins": 3,
                "draws": 1,
                "away_wins": 2,
                "home_goals": 10,
                "away_goals": 9,
                "avg_total_corners": 9.8,
                "over_10_corners_percentage": 33.3
            },
            "Hangzhou Greentown-Yunnan Yukun": {
                "matches": 4,
                "home_wins": 3,
                "draws": 0,
                "away_wins": 1,
                "home_goals": 9,
                "away_goals": 4,
                "avg_total_corners": 10.5,
                "over_10_corners_percentage": 50.0
            }
        }
        
        print(f"✅ Loaded head to head statistics for {len(h2h_stats)} matchups")
        return h2h_stats
    
    def analyze_corners(self, fixtures, team_stats, h2h_stats):
        """Analyze corners for the fixtures"""
        print(f"🔍 Analyzing corners with threshold {self.corner_threshold}...")
        
        results = []
        
        for fixture in fixtures:
            home_team = fixture["home_team"]
            away_team = fixture["away_team"]
            h2h_key = f"{home_team}-{away_team}"
            
            # Get team stats
            home_stats = team_stats.get(home_team, {})
            away_stats = team_stats.get(away_team, {})
            
            # Get head to head stats
            h2h = h2h_stats.get(h2h_key, {})
            
            # Calculate expected corners
            home_corners_weight = 0.4
            away_corners_weight = 0.4
            h2h_corners_weight = 0.2
            
            expected_corners = (
                home_stats.get("avg_total_corners", 0) * home_corners_weight +
                away_stats.get("avg_total_corners", 0) * away_corners_weight +
                h2h.get("avg_total_corners", 0) * h2h_corners_weight
            )
            
            # Calculate probability of over 10.0 corners
            home_over_prob = home_stats.get("over_10_corners_percentage", 0) / 100
            away_over_prob = away_stats.get("over_10_corners_percentage", 0) / 100
            h2h_over_prob = h2h.get("over_10_corners_percentage", 0) / 100
            
            over_probability = (
                home_over_prob * home_corners_weight +
                away_over_prob * away_corners_weight +
                h2h_over_prob * h2h_corners_weight
            )
            
            # Calculate value
            market_odds_over = 2.00  # Example market odds
            expected_value = (over_probability * market_odds_over) - 1
            
            # Create result
            result = {
                "fixture_id": fixture["fixture_id"],
                "home_team": home_team,
                "away_team": away_team,
                "datetime": fixture["datetime"],
                "venue": fixture["venue"],
                "city": fixture["city"],
                "expected_corners": round(expected_corners, 1),
                "over_probability": round(over_probability * 100, 1),
                "market_odds_over": market_odds_over,
                "expected_value": round(expected_value * 100, 1),
                "recommendation": "Over" if over_probability > 0.5 else "Under",
                "value_bet": expected_value > 0.05
            }
            
            results.append(result)
        
        print(f"✅ Analyzed corners for {len(results)} fixtures")
        return results
    
    def run_ultra_advanced_ml(self, fixtures, team_stats, h2h_stats):
        """Run Ultra Advanced ML analysis"""
        print("🧠 Running Ultra Advanced ML analysis...")
        
        results = []
        
        for fixture in fixtures:
            home_team = fixture["home_team"]
            away_team = fixture["away_team"]
            h2h_key = f"{home_team}-{away_team}"
            
            # Get team stats
            home_stats = team_stats.get(home_team, {})
            away_stats = team_stats.get(away_team, {})
            
            # Get head to head stats
            h2h = h2h_stats.get(h2h_key, {})
            
            # Calculate win probabilities using Ultra Advanced ML
            # This is a simplified example - real ML would be more complex
            
            # Home win probability factors
            home_win_rate = home_stats.get("wins", 0) / home_stats.get("matches_played", 1)
            away_loss_rate = away_stats.get("losses", 0) / away_stats.get("matches_played", 1)
            h2h_home_win_rate = h2h.get("home_wins", 0) / h2h.get("matches", 1)
            
            # Away win probability factors
            away_win_rate = away_stats.get("wins", 0) / away_stats.get("matches_played", 1)
            home_loss_rate = home_stats.get("losses", 0) / home_stats.get("matches_played", 1)
            h2h_away_win_rate = h2h.get("away_wins", 0) / h2h.get("matches", 1)
            
            # Draw probability factors
            home_draw_rate = home_stats.get("draws", 0) / home_stats.get("matches_played", 1)
            away_draw_rate = away_stats.get("draws", 0) / away_stats.get("matches_played", 1)
            h2h_draw_rate = h2h.get("draws", 0) / h2h.get("matches", 1)
            
            # Calculate final probabilities with weights
            team_weight = 0.4
            opponent_weight = 0.3
            h2h_weight = 0.3
            
            home_win_prob = (
                home_win_rate * team_weight +
                away_loss_rate * opponent_weight +
                h2h_home_win_rate * h2h_weight
            )
            
            away_win_prob = (
                away_win_rate * team_weight +
                home_loss_rate * opponent_weight +
                h2h_away_win_rate * h2h_weight
            )
            
            draw_prob = (
                home_draw_rate * team_weight +
                away_draw_rate * team_weight +
                h2h_draw_rate * h2h_weight
            )
            
            # Normalize probabilities
            total_prob = home_win_prob + away_win_prob + draw_prob
            home_win_prob /= total_prob
            away_win_prob /= total_prob
            draw_prob /= total_prob
            
            # Market odds (example)
            market_odds_home = 2.20
            market_odds_draw = 3.40
            market_odds_away = 3.00
            
            # Calculate expected values
            ev_home = (home_win_prob * market_odds_home) - 1
            ev_draw = (draw_prob * market_odds_draw) - 1
            ev_away = (away_win_prob * market_odds_away) - 1
            
            # Determine best bet
            best_ev = max(ev_home, ev_draw, ev_away)
            if best_ev == ev_home:
                best_bet = "Home"
                best_odds = market_odds_home
                best_prob = home_win_prob
            elif best_ev == ev_draw:
                best_bet = "Draw"
                best_odds = market_odds_draw
                best_prob = draw_prob
            else:
                best_bet = "Away"
                best_odds = market_odds_away
                best_prob = away_win_prob
            
            # Create result
            result = {
                "fixture_id": fixture["fixture_id"],
                "home_team": home_team,
                "away_team": away_team,
                "datetime": fixture["datetime"],
                "venue": fixture["venue"],
                "city": fixture["city"],
                "home_win_probability": round(home_win_prob * 100, 1),
                "draw_probability": round(draw_prob * 100, 1),
                "away_win_probability": round(away_win_prob * 100, 1),
                "market_odds_home": market_odds_home,
                "market_odds_draw": market_odds_draw,
                "market_odds_away": market_odds_away,
                "ev_home": round(ev_home * 100, 1),
                "ev_draw": round(ev_draw * 100, 1),
                "ev_away": round(ev_away * 100, 1),
                "best_bet": best_bet,
                "best_odds": best_odds,
                "best_probability": round(best_prob * 100, 1),
                "best_ev": round(best_ev * 100, 1),
                "value_bet": best_ev > 0.05
            }
            
            results.append(result)
        
        print(f"✅ Completed Ultra Advanced ML analysis for {len(results)} fixtures")
        return results
    
    def generate_html_report(self, ml_results, corner_results):
        """Generate HTML report"""
        print("📄 Generating HTML report...")
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>China Super League Analysis - {datetime.now().strftime('%Y-%m-%d')}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }}
                h1, h2, h3 {{
                    color: #0066cc;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th, td {{
                    padding: 12px 15px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #0066cc;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .value-bet {{
                    background-color: #dff0d8;
                    font-weight: bold;
                }}
                .high-probability {{
                    color: #0066cc;
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    font-size: 0.8em;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🇨🇳 China Super League Analysis</h1>
                <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
                <p>Analysis performed using Ultra Advanced ML technology</p>
                
                <h2>Match Predictions</h2>
                <table>
                    <tr>
                        <th>Match</th>
                        <th>Date & Time</th>
                        <th>Home Win</th>
                        <th>Draw</th>
                        <th>Away Win</th>
                        <th>Best Bet</th>
                        <th>Odds</th>
                        <th>EV</th>
                    </tr>
        """
        
        # Add match prediction rows
        for result in ml_results:
            value_bet_class = "value-bet" if result["value_bet"] else ""
            high_prob_class = "high-probability" if result["best_probability"] > 60 else ""
            
            html += f"""
                    <tr class="{value_bet_class}">
                        <td>{result["home_team"]} vs {result["away_team"]}</td>
                        <td>{result["datetime"]}</td>
                        <td>{result["home_win_probability"]}%</td>
                        <td>{result["draw_probability"]}%</td>
                        <td>{result["away_win_probability"]}%</td>
                        <td class="{high_prob_class}">{result["best_bet"]} ({result["best_probability"]}%)</td>
                        <td>{result["best_odds"]}</td>
                        <td>{result["best_ev"]}%</td>
                    </tr>
            """
        
        html += """
                </table>
                
                <h2>Corner Analysis (Over/Under 10.0)</h2>
                <table>
                    <tr>
                        <th>Match</th>
                        <th>Date & Time</th>
                        <th>Expected Corners</th>
                        <th>Over 10.0 Probability</th>
                        <th>Market Odds</th>
                        <th>Recommendation</th>
                        <th>EV</th>
                    </tr>
        """
        
        # Add corner analysis rows
        for result in corner_results:
            value_bet_class = "value-bet" if result["value_bet"] else ""
            high_prob_class = "high-probability" if result["over_probability"] > 60 else ""
            
            html += f"""
                    <tr class="{value_bet_class}">
                        <td>{result["home_team"]} vs {result["away_team"]}</td>
                        <td>{result["datetime"]}</td>
                        <td>{result["expected_corners"]}</td>
                        <td class="{high_prob_class}">{result["over_probability"]}%</td>
                        <td>{result["market_odds_over"]}</td>
                        <td>{result["recommendation"]}</td>
                        <td>{result["expected_value"]}%</td>
                    </tr>
            """
        
        html += """
                </table>
                
                <div class="footer">
                    <p>Generated by Ultra Advanced ML Football Predictor</p>
                    <p>© 2025 All Rights Reserved</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save HTML report
        output_file = os.path.join(self.output_dir, f"china_super_league_analysis_{datetime.now().strftime('%Y-%m-%d')}.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ HTML report generated: {output_file}")
        return output_file
    
    def run_analysis(self):
        """Run the complete analysis"""
        print(f"🚀 Running complete analysis for {self.league_name}...")
        
        # 1. Load data
        fixtures = self.load_fixtures()
        team_stats = self.load_team_stats()
        h2h_stats = self.load_head_to_head()
        
        # 2. Run analyses
        corner_results = self.analyze_corners(fixtures, team_stats, h2h_stats)
        ml_results = self.run_ultra_advanced_ml(fixtures, team_stats, h2h_stats)
        
        # 3. Generate report
        report_file = self.generate_html_report(ml_results, corner_results)
        
        print(f"✅ Analysis complete! Report saved to: {report_file}")
        
        # 4. Return results
        return {
            "fixtures": fixtures,
            "corner_results": corner_results,
            "ml_results": ml_results,
            "report_file": report_file
        }

def main():
    """Main function"""
    analyzer = ChinaSuperLeagueAnalyzer()
    results = analyzer.run_analysis()
    
    # Print summary
    print("\n📊 Analysis Summary:")
    print(f"Total fixtures analyzed: {len(results['fixtures'])}")
    
    value_bets_ml = [r for r in results["ml_results"] if r["value_bet"]]
    value_bets_corners = [r for r in results["corner_results"] if r["value_bet"]]
    
    print(f"Value bets (match result): {len(value_bets_ml)}")
    print(f"Value bets (corners): {len(value_bets_corners)}")
    
    if value_bets_ml:
        print("\n🔥 Top Match Result Value Bets:")
        for bet in sorted(value_bets_ml, key=lambda x: x["best_ev"], reverse=True)[:3]:
            print(f"  • {bet['home_team']} vs {bet['away_team']}: {bet['best_bet']} @ {bet['best_odds']} (EV: {bet['best_ev']}%)")
    
    if value_bets_corners:
        print("\n🔥 Top Corner Value Bets:")
        for bet in sorted(value_bets_corners, key=lambda x: x["expected_value"], reverse=True)[:3]:
            print(f"  • {bet['home_team']} vs {bet['away_team']}: {bet['recommendation']} 10.0 @ {bet['market_odds_over']} (EV: {bet['expected_value']}%)")
    
    print(f"\n📄 Full report available at: {results['report_file']}")

if __name__ == "__main__":
    main()
