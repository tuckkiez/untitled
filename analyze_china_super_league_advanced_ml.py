#!/usr/bin/env python3
"""
🚀 Advanced ML Analysis for China Super League - July 18, 2025
วิเคราะห์การแข่งขัน China Super League ด้วย Advanced ML
"""

import json
import os
import pandas as pd
import numpy as np
from datetime import datetime
import math

class AdvancedMLAnalyzer:
    """Advanced ML Analyzer for China Super League"""
    
    def __init__(self, input_file, output_csv):
        """Initialize the analyzer"""
        self.input_file = input_file
        self.output_csv = output_csv
        self.data = None
        self.matches = None
        self.predictions = []
        
        # ML parameters
        self.form_weight = 0.30
        self.h2h_weight = 0.25
        self.stats_weight = 0.30
        self.home_advantage = 0.15
        
        # Confidence thresholds
        self.high_confidence = 65.0
        self.medium_confidence = 55.0
        
    def load_data(self):
        """Load data from input file"""
        print(f"📂 Loading data from {self.input_file}...")
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                self.matches = self.data.get('matches', [])
                print(f"✅ Successfully loaded {len(self.matches)} matches")
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return False
        return True
    
    def analyze_form(self, team_data):
        """Analyze team form based on last 5 matches"""
        form = team_data.get('form', '')
        form_score = 0
        
        # Calculate form score
        for result in form:
            if result == 'W':
                form_score += 3
            elif result == 'D':
                form_score += 1
        
        # Calculate weighted form score (max 15 points)
        return form_score / 15
    
    def analyze_h2h(self, h2h_data, home_team_name):
        """Analyze head-to-head records"""
        home_wins = 0
        away_wins = 0
        draws = 0
        
        for match in h2h_data:
            home_team = match.get('home_team')
            score = match.get('score', '0-0')
            
            try:
                home_goals, away_goals = map(int, score.split('-'))
                
                if home_team == home_team_name:
                    if home_goals > away_goals:
                        home_wins += 1
                    elif home_goals < away_goals:
                        away_wins += 1
                    else:
                        draws += 1
                else:
                    if home_goals < away_goals:
                        home_wins += 1
                    elif home_goals > away_goals:
                        away_wins += 1
                    else:
                        draws += 1
            except:
                continue
        
        total_matches = home_wins + away_wins + draws
        if total_matches == 0:
            return 0.5  # Neutral if no H2H data
        
        # Calculate H2H advantage for home team
        home_advantage = (home_wins + 0.5 * draws) / total_matches
        return home_advantage
    
    def analyze_stats(self, home_team, away_team):
        """Analyze team statistics"""
        home_stats = home_team.get('stats', {})
        away_stats = away_team.get('stats', {})
        
        # Calculate attack strength
        home_attack = home_stats.get('goals_scored', 0) / 10  # Normalize to 0-1 range
        away_attack = away_stats.get('goals_scored', 0) / 10
        
        # Calculate defense strength (inverse of goals conceded)
        home_defense = 1 - (home_stats.get('goals_conceded', 0) / 20)  # Normalize to 0-1 range
        away_defense = 1 - (away_stats.get('goals_conceded', 0) / 20)
        
        # Calculate home advantage
        home_advantage = home_stats.get('home_wins', 0) / (home_stats.get('home_wins', 0) + 
                                                          home_stats.get('home_draws', 0) + 
                                                          home_stats.get('home_losses', 0) + 0.001)
        
        # Calculate away performance
        away_performance = away_stats.get('away_wins', 0) / (away_stats.get('away_wins', 0) + 
                                                            away_stats.get('away_draws', 0) + 
                                                            away_stats.get('away_losses', 0) + 0.001)
        
        # Calculate overall stats advantage for home team
        home_overall = (home_attack + home_defense + home_advantage) / 3
        away_overall = (away_attack + away_defense + away_performance) / 3
        
        # Calculate stats advantage
        stats_advantage = (home_overall / (home_overall + away_overall))
        return min(max(stats_advantage, 0), 1)  # Ensure between 0 and 1
    
    def analyze_corners(self, home_team, away_team, h2h_data):
        """Analyze corner statistics and predict corner outcomes"""
        home_stats = home_team.get('stats', {})
        away_stats = away_team.get('stats', {})
        
        # Get corner stats
        home_corners_for = home_stats.get('corners_for', 5.0)
        home_corners_against = home_stats.get('corners_against', 5.0)
        away_corners_for = away_stats.get('corners_for', 5.0)
        away_corners_against = away_stats.get('corners_against', 5.0)
        
        # Calculate expected corners
        expected_home_corners = (home_corners_for + away_corners_against) / 2
        expected_away_corners = (away_corners_for + home_corners_against) / 2
        expected_total_corners = expected_home_corners + expected_away_corners
        
        # Analyze H2H corner data
        h2h_corners = []
        for match in h2h_data:
            if 'corners' in match:
                try:
                    home_corners, away_corners = map(int, match['corners'].split('-'))
                    h2h_corners.append(home_corners + away_corners)
                except:
                    pass
        
        # Adjust based on H2H data if available
        if h2h_corners:
            avg_h2h_corners = sum(h2h_corners) / len(h2h_corners)
            expected_total_corners = (expected_total_corners * 0.7) + (avg_h2h_corners * 0.3)
        
        # Round to nearest 0.5
        expected_total_corners = round(expected_total_corners * 2) / 2
        
        # Calculate over/under probabilities for common lines
        over_under_probs = {}
        for line in [8.5, 9.5, 10.5, 11.5]:
            if expected_total_corners > line:
                over_prob = 0.5 + min(0.4, (expected_total_corners - line) * 0.1)
            else:
                over_prob = 0.5 - min(0.4, (line - expected_total_corners) * 0.1)
            
            over_under_probs[f"over_{line}"] = over_prob
            over_under_probs[f"under_{line}"] = 1 - over_prob
        
        # Determine most confident prediction
        line_with_highest_confidence = max(
            ["over_8.5", "over_9.5", "over_10.5", "over_11.5", "under_8.5", "under_9.5", "under_10.5", "under_11.5"],
            key=lambda x: abs(over_under_probs[x] - 0.5)
        )
        
        prediction_side = "OVER" if line_with_highest_confidence.startswith("over") else "UNDER"
        prediction_line = line_with_highest_confidence.split("_")[1]
        prediction_confidence = round(over_under_probs[line_with_highest_confidence] * 100, 1)
        
        # Create corner prediction
        corner_prediction = {
            "expected_home_corners": round(expected_home_corners, 1),
            "expected_away_corners": round(expected_away_corners, 1),
            "expected_total_corners": expected_total_corners,
            "prediction": f"{prediction_side} {prediction_line}",
            "confidence": prediction_confidence,
            "over_under_probs": over_under_probs
        }
        
        return corner_prediction
    
    def predict_match_result(self, match):
        """Predict match result using Advanced ML"""
        home_team = match.get('home_team', {})
        away_team = match.get('away_team', {})
        h2h_data = match.get('head_to_head', [])
        
        # Calculate form advantage
        home_form = self.analyze_form(home_team)
        away_form = self.analyze_form(away_team)
        form_advantage = home_form / (home_form + away_form) if (home_form + away_form) > 0 else 0.5
        
        # Calculate H2H advantage
        h2h_advantage = self.analyze_h2h(h2h_data, home_team.get('name'))
        
        # Calculate stats advantage
        stats_advantage = self.analyze_stats(home_team, away_team)
        
        # Calculate overall home win probability
        home_win_prob = (
            form_advantage * self.form_weight +
            h2h_advantage * self.h2h_weight +
            stats_advantage * self.stats_weight +
            self.home_advantage
        )
        
        # Normalize to ensure it's between 0 and 1
        home_win_prob = min(max(home_win_prob, 0), 1)
        
        # Calculate draw and away win probabilities
        draw_factor = 0.15 + (0.1 * (1 - abs(2 * home_win_prob - 1)))  # Higher for balanced matches
        draw_prob = min(draw_factor, 0.3)  # Cap draw probability at 30%
        
        away_win_prob = 1 - home_win_prob - draw_prob
        away_win_prob = max(away_win_prob, 0)  # Ensure non-negative
        
        # Normalize probabilities to sum to 1
        total_prob = home_win_prob + draw_prob + away_win_prob
        home_win_prob /= total_prob
        draw_prob /= total_prob
        away_win_prob /= total_prob
        
        # Determine match winner prediction
        if home_win_prob > draw_prob and home_win_prob > away_win_prob:
            match_winner = "HOME"
            confidence = home_win_prob * 100
        elif away_win_prob > home_win_prob and away_win_prob > draw_prob:
            match_winner = "AWAY"
            confidence = away_win_prob * 100
        else:
            match_winner = "DRAW"
            confidence = draw_prob * 100
        
        # Predict score
        home_goals_exp = (home_team.get('stats', {}).get('goals_scored', 15) / 8) * (away_team.get('stats', {}).get('goals_conceded', 15) / 15)
        away_goals_exp = (away_team.get('stats', {}).get('goals_scored', 15) / 8) * (home_team.get('stats', {}).get('goals_conceded', 15) / 15)
        
        # Adjust for match winner prediction
        if match_winner == "HOME":
            home_goals_exp *= 1.2
            away_goals_exp *= 0.9
        elif match_winner == "AWAY":
            home_goals_exp *= 0.9
            away_goals_exp *= 1.2
        
        # Round to nearest likely score
        home_goals = round(home_goals_exp)
        away_goals = round(away_goals_exp)
        
        # Ensure score reflects match winner
        if match_winner == "HOME" and home_goals <= away_goals:
            if away_goals == 0:
                home_goals = 1
            else:
                home_goals = away_goals + 1
        elif match_winner == "AWAY" and away_goals <= home_goals:
            if home_goals == 0:
                away_goals = 1
            else:
                away_goals = home_goals + 1
        elif match_winner == "DRAW" and home_goals != away_goals:
            # Set most likely draw score
            if (home_goals + away_goals) / 2 < 1.5:
                home_goals = away_goals = 0
            elif (home_goals + away_goals) / 2 < 2.5:
                home_goals = away_goals = 1
            else:
                home_goals = away_goals = 2
        
        # Predict over/under 2.5 goals
        total_goals = home_goals + away_goals
        over_under = "OVER" if total_goals > 2.5 else "UNDER"
        
        # Calculate over/under confidence
        over_under_confidence = 0
        if total_goals > 2.5:
            over_under_confidence = 50 + min(15, (total_goals - 2.5) * 10)
        else:
            over_under_confidence = 50 + min(15, (2.5 - total_goals) * 10)
        
        # Predict both teams to score
        btts = "YES" if home_goals > 0 and away_goals > 0 else "NO"
        
        # Calculate BTTS confidence
        btts_confidence = 0
        if btts == "YES":
            btts_confidence = 50 + min(20, home_goals * 5 + away_goals * 5)
        else:
            btts_confidence = 50 + min(20, (2 - home_goals - away_goals) * 10)
        
        # Predict corners
        corner_prediction = self.analyze_corners(home_team, away_team, h2h_data)
        
        # Create prediction object
        prediction = {
            "match_winner": match_winner,
            "home_win_prob": round(home_win_prob * 100, 1),
            "draw_prob": round(draw_prob * 100, 1),
            "away_win_prob": round(away_win_prob * 100, 1),
            "score": f"{home_goals}-{away_goals}",
            "over_under": over_under,
            "over_under_confidence": round(over_under_confidence, 1),
            "btts": btts,
            "btts_confidence": round(btts_confidence, 1),
            "corners": corner_prediction["prediction"],
            "corners_confidence": corner_prediction["confidence"],
            "expected_total_corners": corner_prediction["expected_total_corners"],
            "confidence": round(confidence, 1),
            "confidence_level": "HIGH" if confidence >= self.high_confidence else "MEDIUM" if confidence >= self.medium_confidence else "LOW",
            "model": "Advanced ML"
        }
        
        return prediction
    
    def analyze_all_matches(self):
        """Analyze all matches and generate predictions"""
        print("\n🔍 Analyzing matches with Advanced ML...")
        
        for i, match in enumerate(self.matches):
            print(f"  ⚽ Analyzing Match {i+1}: {match['home_team']['name']} vs {match['away_team']['name']}")
            
            # Generate prediction
            prediction = self.predict_match_result(match)
            
            # Update match with prediction
            match['prediction'] = prediction
            
            # Add to predictions list
            self.predictions.append({
                "fixture_id": match['fixture_id'],
                "date": match['date'],
                "home_team": match['home_team']['name'],
                "away_team": match['away_team']['name'],
                "home_logo": match['home_team']['logo'],
                "away_logo": match['away_team']['logo'],
                "match_winner": prediction['match_winner'],
                "confidence": prediction['confidence'],
                "confidence_level": prediction['confidence_level'],
                "score": prediction['score'],
                "over_under": prediction['over_under'],
                "over_under_confidence": prediction['over_under_confidence'],
                "btts": prediction['btts'],
                "btts_confidence": prediction['btts_confidence'],
                "corners": prediction['corners'],
                "corners_confidence": prediction['corners_confidence'],
                "expected_total_corners": prediction['expected_total_corners'],
                "home_win_prob": prediction['home_win_prob'],
                "draw_prob": prediction['draw_prob'],
                "away_win_prob": prediction['away_win_prob'],
                "odds_home": match['odds']['home_win'],
                "odds_draw": match['odds']['draw'],
                "odds_away": match['odds']['away_win'],
                "odds_over": match['odds']['over_under']['over'],
                "odds_under": match['odds']['over_under']['under'],
                "odds_corners_over": match['odds']['corners']['over'],
                "odds_corners_under": match['odds']['corners']['under'],
                "corners_line": match['odds']['corners']['line'],
                "model": "Advanced ML"
            })
    
    def save_predictions_csv(self):
        """Save predictions to CSV file"""
        print(f"\n💾 Saving predictions to {self.output_csv}...")
        
        try:
            df = pd.DataFrame(self.predictions)
            df.to_csv(self.output_csv, index=False)
            print(f"✅ Successfully saved predictions to {self.output_csv}")
        except Exception as e:
            print(f"❌ Error saving predictions: {str(e)}")
    
    def save_updated_json(self):
        """Save updated JSON with predictions"""
        output_json = self.input_file.replace('.json', '_advanced_ml_predictions.json')
        print(f"\n💾 Saving updated JSON to {output_json}...")
        
        try:
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"✅ Successfully saved updated JSON to {output_json}")
        except Exception as e:
            print(f"❌ Error saving updated JSON: {str(e)}")
    
    def print_summary(self):
        """Print summary of predictions"""
        print("\n📊 Advanced ML Prediction Summary:")
        print("=" * 100)
        print(f"{'Home Team':<20} {'Away Team':<20} {'Prediction':<10} {'Score':<8} {'Confidence':<10} {'O/U':<5} {'BTTS':<5} {'Corners':<10}")
        print("-" * 100)
        
        for pred in self.predictions:
            print(f"{pred['home_team']:<20} {pred['away_team']:<20} {pred['match_winner']:<10} {pred['score']:<8} {pred['confidence']:.1f}% {pred['over_under']:<5} {pred['btts']:<5} {pred['corners']:<10}")
        
        print("=" * 100)
    
    def run(self):
        """Run the analysis pipeline"""
        print("🚀 Starting Advanced ML Analysis for China Super League")
        print("=" * 100)
        
        # Load data
        if not self.load_data():
            return False
        
        # Analyze matches
        self.analyze_all_matches()
        
        # Save predictions to CSV
        self.save_predictions_csv()
        
        # Save updated JSON
        self.save_updated_json()
        
        # Print summary
        self.print_summary()
        
        print("\n✅ Analysis complete!")
        return True

def main():
    """Main function"""
    input_file = "/Users/80090/Desktop/Project/untitle/api_data/china_super_league/china_super_league_20250718_updated.json"
    output_csv = "/Users/80090/Desktop/Project/untitle/api_data/china_super_league/china_super_league_predictions_advanced_ml.csv"
    
    analyzer = AdvancedMLAnalyzer(input_file, output_csv)
    analyzer.run()

if __name__ == "__main__":
    main()
