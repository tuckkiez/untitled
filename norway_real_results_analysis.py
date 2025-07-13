#!/usr/bin/env python3
"""
Norway Eliteserien Real Results Analysis
การวิเคราะห์ผลการแข่งขันจริงของ Norway Eliteserien
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

class NorwayRealResultsAnalyzer:
    def __init__(self):
        self.real_matches = [
            {
                'home_team': 'Bryne',
                'away_team': 'Vålerenga',
                'home_goals': 1,
                'away_goals': 0,
                'result': 'Home Win',
                'total_goals': 1,
                'over_under_2_5': 'Under',
                'both_teams_score': 'No'
            },
            {
                'home_team': 'FK Haugesund',
                'away_team': 'KFUM',
                'home_goals': 0,
                'away_goals': 0,
                'result': 'Draw',
                'total_goals': 0,
                'over_under_2_5': 'Under',
                'both_teams_score': 'No'
            },
            {
                'home_team': 'Kristiansund BK',
                'away_team': 'Sarpsborg 08',
                'home_goals': 0,
                'away_goals': 0,
                'result': 'Draw',
                'total_goals': 0,
                'over_under_2_5': 'Under',
                'both_teams_score': 'No'
            },
            {
                'home_team': 'Rosenborg',
                'away_team': 'Hamarkameratene',
                'home_goals': 0,
                'away_goals': 0,
                'result': 'Draw',
                'total_goals': 0,
                'over_under_2_5': 'Under',
                'both_teams_score': 'No'
            },
            {
                'home_team': 'Strømsgodset',
                'away_team': 'Tromsø',
                'home_goals': 0,
                'away_goals': 0,
                'result': 'Draw',
                'total_goals': 0,
                'over_under_2_5': 'Under',
                'both_teams_score': 'No'
            }
        ]
        
        # Our previous predictions (from the simulated analysis)
        self.our_predictions = [
            {
                'home_team': 'Brann',
                'away_team': 'Viking',
                'predicted_home_win': 58.0,
                'predicted_over_2_5': 50.4,
                'predicted_bts_yes': 54.9,
                'predicted_handicap_home': 43.0
            },
            {
                'home_team': 'Vålerenga',
                'away_team': 'Molde',
                'predicted_home_win': 24.0,
                'predicted_over_2_5': 88.8,
                'predicted_bts_yes': 75.0,
                'predicted_handicap_home': 9.0
            },
            {
                'home_team': 'Rosenborg',
                'away_team': 'Bodø/Glimt',
                'predicted_home_win': 52.0,
                'predicted_over_2_5': 92.2,
                'predicted_bts_yes': 78.1,
                'predicted_handicap_home': 13.0
            },
            {
                'home_team': 'Haugesund',
                'away_team': 'Lillestrøm',
                'predicted_home_win': 66.0,
                'predicted_over_2_5': 83.0,
                'predicted_bts_yes': 55.2,
                'predicted_handicap_home': 74.0
            },
            {
                'home_team': 'Kristiansand',
                'away_team': 'Strømsgodset',
                'predicted_home_win': 37.0,
                'predicted_over_2_5': 51.8,
                'predicted_bts_yes': 46.0,
                'predicted_handicap_home': 34.0
            },
            {
                'home_team': 'Sarpsborg 08',
                'away_team': 'Odd',
                'predicted_home_win': 35.0,
                'predicted_over_2_5': 51.8,
                'predicted_bts_yes': 38.4,
                'predicted_handicap_home': 32.0
            }
        ]
    
    def analyze_real_vs_predicted(self):
        """Analyze real results vs our predictions"""
        print("🔍 Analyzing Real Results vs Our Predictions...")
        
        # Real match statistics
        real_stats = {
            'total_matches': len(self.real_matches),
            'home_wins': sum(1 for m in self.real_matches if m['result'] == 'Home Win'),
            'draws': sum(1 for m in self.real_matches if m['result'] == 'Draw'),
            'away_wins': sum(1 for m in self.real_matches if m['result'] == 'Away Win'),
            'over_2_5': sum(1 for m in self.real_matches if m['over_under_2_5'] == 'Over'),
            'under_2_5': sum(1 for m in self.real_matches if m['over_under_2_5'] == 'Under'),
            'bts_yes': sum(1 for m in self.real_matches if m['both_teams_score'] == 'Yes'),
            'bts_no': sum(1 for m in self.real_matches if m['both_teams_score'] == 'No'),
            'total_goals': sum(m['total_goals'] for m in self.real_matches),
            'avg_goals_per_match': sum(m['total_goals'] for m in self.real_matches) / len(self.real_matches)
        }
        
        # Calculate percentages
        real_percentages = {
            'home_win_percent': (real_stats['home_wins'] / real_stats['total_matches']) * 100,
            'draw_percent': (real_stats['draws'] / real_stats['total_matches']) * 100,
            'away_win_percent': (real_stats['away_wins'] / real_stats['total_matches']) * 100,
            'over_2_5_percent': (real_stats['over_2_5'] / real_stats['total_matches']) * 100,
            'under_2_5_percent': (real_stats['under_2_5'] / real_stats['total_matches']) * 100,
            'bts_yes_percent': (real_stats['bts_yes'] / real_stats['total_matches']) * 100,
            'bts_no_percent': (real_stats['bts_no'] / real_stats['total_matches']) * 100
        }
        
        # Our predicted averages
        predicted_averages = {
            'avg_home_win': np.mean([p['predicted_home_win'] for p in self.our_predictions]),
            'avg_over_2_5': np.mean([p['predicted_over_2_5'] for p in self.our_predictions]),
            'avg_bts_yes': np.mean([p['predicted_bts_yes'] for p in self.our_predictions]),
            'avg_handicap_home': np.mean([p['predicted_handicap_home'] for p in self.our_predictions])
        }
        
        return {
            'real_results': self.real_matches,
            'real_statistics': real_stats,
            'real_percentages': real_percentages,
            'predicted_averages': predicted_averages,
            'analysis_insights': self.generate_insights(real_percentages, predicted_averages)
        }
    
    def generate_insights(self, real_percentages, predicted_averages):
        """Generate insights from comparison"""
        insights = []
        
        # Home Win Analysis
        home_win_diff = abs(real_percentages['home_win_percent'] - predicted_averages['avg_home_win'])
        if home_win_diff > 20:
            insights.append(f"🏠 Home Win: Significant difference! Real: {real_percentages['home_win_percent']:.1f}% vs Predicted: {predicted_averages['avg_home_win']:.1f}%")
        else:
            insights.append(f"🏠 Home Win: Close prediction. Real: {real_percentages['home_win_percent']:.1f}% vs Predicted: {predicted_averages['avg_home_win']:.1f}%")
        
        # Over/Under Analysis
        over_diff = abs(real_percentages['over_2_5_percent'] - predicted_averages['avg_over_2_5'])
        if over_diff > 30:
            insights.append(f"⚽ Over 2.5: Major miss! Real: {real_percentages['over_2_5_percent']:.1f}% vs Predicted: {predicted_averages['avg_over_2_5']:.1f}%")
        else:
            insights.append(f"⚽ Over 2.5: Reasonable prediction. Real: {real_percentages['over_2_5_percent']:.1f}% vs Predicted: {predicted_averages['avg_over_2_5']:.1f}%")
        
        # BTS Analysis
        bts_diff = abs(real_percentages['bts_yes_percent'] - predicted_averages['avg_bts_yes'])
        if bts_diff > 25:
            insights.append(f"🥅 BTS: Significant difference! Real: {real_percentages['bts_yes_percent']:.1f}% vs Predicted: {predicted_averages['avg_bts_yes']:.1f}%")
        else:
            insights.append(f"🥅 BTS: Good prediction. Real: {real_percentages['bts_yes_percent']:.1f}% vs Predicted: {predicted_averages['avg_bts_yes']:.1f}%")
        
        # Special observations
        if real_percentages['draw_percent'] >= 80:
            insights.append("🎯 Special Observation: Extremely high draw rate - defensive day in Norwegian football!")
        
        if real_percentages['under_2_5_percent'] == 100:
            insights.append("🛡️ Special Observation: All matches Under 2.5 goals - very defensive round!")
        
        if real_percentages['bts_no_percent'] == 100:
            insights.append("🚫 Special Observation: No match had both teams scoring - goalkeepers dominated!")
        
        return insights
    
    def create_corrected_predictions(self):
        """Create corrected predictions based on real results"""
        print("🔧 Creating corrected predictions based on real patterns...")
        
        # Based on real results, Norwegian football today was very defensive
        corrected_predictions = []
        
        for match in self.real_matches:
            # Adjust predictions based on what actually happened
            corrected_pred = {
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'actual_result': match['result'],
                'actual_goals': match['total_goals'],
                'corrected_predictions': {
                    'home_win_percent': 20.0 if match['result'] != 'Home Win' else 80.0,
                    'draw_percent': 80.0 if match['result'] == 'Draw' else 10.0,
                    'away_win_percent': 20.0 if match['result'] != 'Away Win' else 80.0,
                    'over_2_5_percent': 10.0,  # Very low based on actual results
                    'under_2_5_percent': 90.0,  # Very high based on actual results
                    'bts_yes_percent': 15.0,  # Very low based on actual results
                    'bts_no_percent': 85.0,  # Very high based on actual results
                },
                'key_4_corrected_values': {
                    'home_win': 20.0 if match['result'] != 'Home Win' else 80.0,
                    'over_2_5': 10.0,
                    'bts_yes': 15.0,
                    'handicap_home': 25.0
                }
            }
            corrected_predictions.append(corrected_pred)
        
        return corrected_predictions
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        analysis = self.analyze_real_vs_predicted()
        corrected_preds = self.create_corrected_predictions()
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'league': 'Norway Eliteserien',
            'analysis_type': 'Real Results vs ML Predictions',
            'real_match_results': analysis['real_results'],
            'real_statistics': analysis['real_statistics'],
            'real_percentages': analysis['real_percentages'],
            'our_predicted_averages': analysis['predicted_averages'],
            'corrected_predictions': corrected_preds,
            'key_insights': analysis['analysis_insights'],
            'lessons_learned': [
                "Norwegian football can be very defensive on certain days",
                "Draw rate was exceptionally high (80%)",
                "Goal scoring was much lower than predicted",
                "Both teams score rate was 0% - very unusual",
                "Our ML model overestimated attacking play"
            ],
            'model_accuracy_assessment': {
                'home_win_prediction': 'Poor - overestimated home advantage',
                'over_under_prediction': 'Very Poor - significantly overestimated goals',
                'bts_prediction': 'Poor - overestimated both teams scoring',
                'overall_assessment': 'Models need recalibration for defensive Norwegian matches'
            }
        }
        
        return report

def main():
    """Main execution"""
    print("🇳🇴 Starting Norway Eliteserien Real Results Analysis...")
    print("="*70)
    
    analyzer = NorwayRealResultsAnalyzer()
    report = analyzer.generate_comprehensive_report()
    
    # Save report
    with open('/Users/80090/Desktop/Project/untitle/norway_real_results_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("📊 REAL RESULTS SUMMARY:")
    print("-" * 40)
    for match in report['real_match_results']:
        print(f"• {match['home_team']} {match['home_goals']}-{match['away_goals']} {match['away_team']} ({match['result']})")
    
    print(f"\n📈 REAL STATISTICS:")
    stats = report['real_statistics']
    print(f"• Total Matches: {stats['total_matches']}")
    print(f"• Home Wins: {stats['home_wins']} ({report['real_percentages']['home_win_percent']:.1f}%)")
    print(f"• Draws: {stats['draws']} ({report['real_percentages']['draw_percent']:.1f}%)")
    print(f"• Away Wins: {stats['away_wins']} ({report['real_percentages']['away_win_percent']:.1f}%)")
    print(f"• Over 2.5: {stats['over_2_5']} ({report['real_percentages']['over_2_5_percent']:.1f}%)")
    print(f"• Under 2.5: {stats['under_2_5']} ({report['real_percentages']['under_2_5_percent']:.1f}%)")
    print(f"• BTS Yes: {stats['bts_yes']} ({report['real_percentages']['bts_yes_percent']:.1f}%)")
    print(f"• BTS No: {stats['bts_no']} ({report['real_percentages']['bts_no_percent']:.1f}%)")
    print(f"• Average Goals: {stats['avg_goals_per_match']:.1f}")
    
    print(f"\n🎯 OUR PREDICTIONS vs REALITY:")
    pred_avg = report['our_predicted_averages']
    real_pct = report['real_percentages']
    print(f"• Home Win: Predicted {pred_avg['avg_home_win']:.1f}% | Real {real_pct['home_win_percent']:.1f}%")
    print(f"• Over 2.5: Predicted {pred_avg['avg_over_2_5']:.1f}% | Real {real_pct['over_2_5_percent']:.1f}%")
    print(f"• BTS Yes: Predicted {pred_avg['avg_bts_yes']:.1f}% | Real {real_pct['bts_yes_percent']:.1f}%")
    
    print(f"\n🔍 KEY INSIGHTS:")
    for insight in report['key_insights']:
        print(f"• {insight}")
    
    print(f"\n📚 LESSONS LEARNED:")
    for lesson in report['lessons_learned']:
        print(f"• {lesson}")
    
    print(f"\n🎓 MODEL ACCURACY ASSESSMENT:")
    assessment = report['model_accuracy_assessment']
    for key, value in assessment.items():
        if key != 'overall_assessment':
            print(f"• {key.replace('_', ' ').title()}: {value}")
    print(f"• Overall: {assessment['overall_assessment']}")
    
    print("\n" + "="*70)
    print("💾 Analysis saved to: norway_real_results_analysis.json")
    print("🎯 Conclusion: Our ML models need recalibration for defensive Norwegian matches!")
    print("="*70)

if __name__ == "__main__":
    main()
