#!/usr/bin/env python3
"""
🚀 China Super League Corner Analysis - July 18, 2025
วิเคราะห์เตะมุมในการแข่งขัน China Super League ที่เส้น 10 ลูก
"""

import json
import os
import pandas as pd
import numpy as np
from datetime import datetime
import math

class ChinaSuperLeagueCornerAnalyzer:
    """China Super League Corner Analyzer"""
    
    def __init__(self, input_file, output_csv):
        """Initialize the analyzer"""
        self.input_file = input_file
        self.output_csv = output_csv
        self.data = None
        self.matches = None
        self.predictions = []
        
        # Corner analysis parameters
        self.team_stats_weight = 0.6
        self.h2h_weight = 0.4
        self.corner_line = 10.0  # เส้นเตะมุมที่ 10 ลูก
        
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
            expected_total_corners = (expected_total_corners * self.team_stats_weight) + (avg_h2h_corners * self.h2h_weight)
        
        # Round to nearest 0.5
        expected_total_corners = round(expected_total_corners * 2) / 2
        
        # Calculate over/under probabilities for the 10.0 line
        if expected_total_corners > self.corner_line:
            over_prob = 0.5 + min(0.4, (expected_total_corners - self.corner_line) * 0.1)
        else:
            over_prob = 0.5 - min(0.4, (self.corner_line - expected_total_corners) * 0.1)
        
        under_prob = 1 - over_prob
        
        # Determine prediction
        prediction_side = "OVER" if over_prob > under_prob else "UNDER"
        prediction_confidence = round(max(over_prob, under_prob) * 100, 1)
        
        # Create corner prediction
        corner_prediction = {
            "expected_home_corners": round(expected_home_corners, 1),
            "expected_away_corners": round(expected_away_corners, 1),
            "expected_total_corners": expected_total_corners,
            "prediction": f"{prediction_side} {self.corner_line}",
            "confidence": prediction_confidence,
            "over_prob": over_prob,
            "under_prob": under_prob
        }
        
        return corner_prediction
    
    def analyze_all_matches(self):
        """Analyze all matches and generate corner predictions"""
        print("\n🔍 Analyzing corners for all matches...")
        
        for i, match in enumerate(self.matches):
            print(f"  ⚽ Analyzing Match {i+1}: {match['home_team']['name']} vs {match['away_team']['name']}")
            
            # Generate corner prediction
            corner_prediction = self.analyze_corners(
                match['home_team'], 
                match['away_team'], 
                match.get('head_to_head', [])
            )
            
            # Update match with corner prediction
            if 'prediction' not in match:
                match['prediction'] = {}
            
            match['prediction']['corners'] = corner_prediction
            
            # Add to predictions list
            self.predictions.append({
                "fixture_id": match['fixture_id'],
                "date": match['date'],
                "home_team": match['home_team']['name'],
                "away_team": match['away_team']['name'],
                "home_logo": match['home_team']['logo'],
                "away_logo": match['away_team']['logo'],
                "corners_prediction": corner_prediction['prediction'],
                "corners_confidence": corner_prediction['confidence'],
                "expected_total_corners": corner_prediction['expected_total_corners'],
                "odds_corners_over": match['odds']['corners']['over'],
                "odds_corners_under": match['odds']['corners']['under'],
                "corners_line": match['odds']['corners']['line']
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
        output_json = self.input_file.replace('.json', '_corner_predictions.json')
        print(f"\n💾 Saving updated JSON to {output_json}...")
        
        try:
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"✅ Successfully saved updated JSON to {output_json}")
        except Exception as e:
            print(f"❌ Error saving updated JSON: {str(e)}")
    
    def print_summary(self):
        """Print summary of predictions"""
        print("\n📊 Corner Prediction Summary:")
        print("=" * 80)
        print(f"{'Home Team':<20} {'Away Team':<20} {'Prediction':<15} {'Confidence':<10} {'Expected':<10}")
        print("-" * 80)
        
        for pred in self.predictions:
            print(f"{pred['home_team']:<20} {pred['away_team']:<20} {pred['corners_prediction']:<15} {pred['corners_confidence']:.1f}% {pred['expected_total_corners']:<10}")
        
        print("=" * 80)
        
        # Calculate value bets
        value_bets = []
        for pred in self.predictions:
            # Check for value in corners market
            corners_pred = pred['corners_prediction'].split()
            corners_side = corners_pred[0]
            
            if corners_side == 'OVER' and pred['corners_confidence']/100 > (1/pred['odds_corners_over']):
                value = round((pred['corners_confidence']/100) / (1/pred['odds_corners_over']) - 1, 2) * 100
                if value >= 5:
                    value_bets.append({
                        'match': f"{pred['home_team']} vs {pred['away_team']}",
                        'bet': f"Corners Over {pred['corners_line']} @ {pred['odds_corners_over']}",
                        'edge': f"{value:.1f}%",
                        'confidence': f"{pred['corners_confidence']:.1f}%"
                    })
            
            elif corners_side == 'UNDER' and pred['corners_confidence']/100 > (1/pred['odds_corners_under']):
                value = round((pred['corners_confidence']/100) / (1/pred['odds_corners_under']) - 1, 2) * 100
                if value >= 5:
                    value_bets.append({
                        'match': f"{pred['home_team']} vs {pred['away_team']}",
                        'bet': f"Corners Under {pred['corners_line']} @ {pred['odds_corners_under']}",
                        'edge': f"{value:.1f}%",
                        'confidence': f"{pred['corners_confidence']:.1f}%"
                    })
        
        # Print value bets
        if value_bets:
            print("\n💰 Value Bets Detected:")
            print("-" * 80)
            for bet in value_bets:
                print(f"{bet['match']:<40} {bet['bet']:<25} Edge: {bet['edge']:<8} Confidence: {bet['confidence']}")
        else:
            print("\n💰 No significant value bets detected")
    
    def run(self):
        """Run the analysis pipeline"""
        print("🚀 Starting China Super League Corner Analysis")
        print("=" * 80)
        
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
    output_csv = "/Users/80090/Desktop/Project/untitle/api_data/china_super_league/china_super_league_corner_predictions.csv"
    
    analyzer = ChinaSuperLeagueCornerAnalyzer(input_file, output_csv)
    analyzer.run()

if __name__ == "__main__":
    main()
