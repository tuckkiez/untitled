#!/usr/bin/env python3
"""
Comprehensive Football Prediction System
ระบบทำนายฟุตบอลครบวงจร - ดึงข้อมูล, ดึง odds, ทำนายด้วย ML
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from comprehensive_odds_fetcher import ComprehensiveOddsFetcher
from advanced_ml_with_real_odds import AdvancedMLWithRealOdds
import pandas as pd

class ComprehensivePredictionSystem:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.odds_fetcher = ComprehensiveOddsFetcher(api_key)
        self.ml_system = AdvancedMLWithRealOdds()
        self.results = {}
        
    def run_complete_analysis(self, target_date: str = "2025-07-13"):
        """Run complete analysis pipeline"""
        print("🚀 COMPREHENSIVE FOOTBALL PREDICTION SYSTEM")
        print("=" * 60)
        print(f"📅 Target Date: {target_date}")
        print("=" * 60)
        
        # Phase 1: Data Collection
        print("\n🔄 PHASE 1: DATA COLLECTION")
        print("-" * 40)
        
        print("📊 Step 1.1: Fetching fixtures from all leagues...")
        fixtures_dict = self.odds_fetcher.fetch_fixtures_for_date(target_date)
        
        total_fixtures = sum(len(fixtures) for fixtures in fixtures_dict.values())
        print(f"✅ Found {total_fixtures} fixtures across {len(fixtures_dict)} leagues")
        
        if total_fixtures == 0:
            print("❌ No fixtures found for the target date.")
            return None
        
        print("\n💰 Step 1.2: Fetching real odds data...")
        print("⚠️  This process may take several minutes due to API rate limits...")
        
        start_time = time.time()
        all_odds = self.odds_fetcher.fetch_all_odds(fixtures_dict)
        end_time = time.time()
        
        print(f"✅ Odds collection completed in {(end_time - start_time)/60:.1f} minutes")
        print(f"💰 Collected odds for {len(all_odds)} fixtures")
        
        # Phase 2: Data Processing & ML Training
        print("\n🤖 PHASE 2: MACHINE LEARNING")
        print("-" * 40)
        
        print("📈 Step 2.1: Loading and processing data...")
        raw_data = self.ml_system.load_data_from_db()
        
        if raw_data.empty:
            print("❌ No data available for ML training")
            return None
        
        print("🔧 Step 2.2: Feature engineering...")
        odds_df = self.ml_system.extract_odds_features(raw_data)
        featured_df = self.ml_system.create_advanced_features(odds_df)
        
        # Separate completed and upcoming matches
        completed_matches = featured_df[featured_df['actual_result'].notna()].copy()
        upcoming_matches = featured_df[featured_df['actual_result'].isna()].copy()
        
        print(f"📊 Training data: {len(completed_matches)} completed matches")
        print(f"🔮 Prediction targets: {len(upcoming_matches)} upcoming matches")
        
        if len(completed_matches) >= 10:
            print("\n🎯 Step 2.3: Training ML models...")
            training_results = self.ml_system.train_models(completed_matches)
            
            # Phase 3: Predictions
            print("\n🔮 PHASE 3: PREDICTIONS")
            print("-" * 40)
            
            if len(upcoming_matches) > 0:
                print("🎲 Making predictions for upcoming matches...")
                predictions_df = self.ml_system.predict_upcoming_matches(upcoming_matches)
                
                # Save predictions
                self.save_predictions(predictions_df, target_date)
                
                # Generate summary
                summary = self.generate_comprehensive_summary(
                    fixtures_dict, all_odds, training_results, predictions_df
                )
                
                self.results = {
                    'fixtures': fixtures_dict,
                    'odds': all_odds,
                    'training_results': training_results,
                    'predictions': predictions_df,
                    'summary': summary
                }
                
                return self.results
            else:
                print("ℹ️  No upcoming matches to predict")
        else:
            print(f"⚠️  Not enough training data ({len(completed_matches)} matches)")
            print("   Need at least 10 completed matches for reliable ML training")
        
        return None
    
    def save_predictions(self, predictions_df: pd.DataFrame, target_date: str):
        """Save predictions to various formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to CSV
        csv_file = f"predictions_{target_date}_{timestamp}.csv"
        predictions_df.to_csv(csv_file, index=False)
        
        # Save to JSON
        json_file = f"predictions_{target_date}_{timestamp}.json"
        predictions_dict = predictions_df.to_dict('records')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(predictions_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Predictions saved:")
        print(f"   📄 CSV: {csv_file}")
        print(f"   📄 JSON: {json_file}")
    
    def generate_comprehensive_summary(self, fixtures_dict, all_odds, training_results, predictions_df):
        """Generate comprehensive summary"""
        summary = {
            'analysis_date': datetime.now().isoformat(),
            'data_collection': {
                'total_leagues': len(fixtures_dict),
                'total_fixtures': sum(len(fixtures) for fixtures in fixtures_dict.values()),
                'fixtures_with_odds': len(all_odds),
                'odds_coverage': len(all_odds) / sum(len(fixtures) for fixtures in fixtures_dict.values()) * 100
            },
            'machine_learning': {
                'models_trained': len(training_results),
                'model_performance': {}
            },
            'predictions': {
                'total_predictions': len(predictions_df),
                'high_confidence_predictions': len(predictions_df[predictions_df['result_confidence'] > 0.7]),
                'leagues_covered': predictions_df['league_name'].nunique() if not predictions_df.empty else 0
            }
        }
        
        # Add model performance details
        for pred_type, models in training_results.items():
            summary['machine_learning']['model_performance'][pred_type] = {
                'best_accuracy': max(model_info['cv_mean'] for model_info in models.values()),
                'average_accuracy': sum(model_info['cv_mean'] for model_info in models.values()) / len(models)
            }
        
        # Add top predictions
        if not predictions_df.empty:
            top_predictions = predictions_df.nlargest(5, 'result_confidence')[
                ['home_team', 'away_team', 'predicted_result', 'result_confidence']
            ].to_dict('records')
            summary['predictions']['top_confidence'] = top_predictions
        
        return summary
    
    def print_final_report(self):
        """Print comprehensive final report"""
        if not self.results:
            print("❌ No results available")
            return
        
        summary = self.results['summary']
        predictions_df = self.results['predictions']
        
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 60)
        
        # Data Collection Summary
        print("\n📈 DATA COLLECTION SUMMARY:")
        dc = summary['data_collection']
        print(f"  • Total Leagues Analyzed: {dc['total_leagues']}")
        print(f"  • Total Fixtures Found: {dc['total_fixtures']}")
        print(f"  • Fixtures with Odds: {dc['fixtures_with_odds']}")
        print(f"  • Odds Coverage: {dc['odds_coverage']:.1f}%")
        
        # ML Performance Summary
        print("\n🤖 MACHINE LEARNING PERFORMANCE:")
        ml = summary['machine_learning']
        for pred_type, performance in ml['model_performance'].items():
            print(f"  • {pred_type.replace('_', ' ').title()}:")
            print(f"    - Best Accuracy: {performance['best_accuracy']:.3f}")
            print(f"    - Average Accuracy: {performance['average_accuracy']:.3f}")
        
        # Predictions Summary
        print("\n🔮 PREDICTIONS SUMMARY:")
        pred = summary['predictions']
        print(f"  • Total Predictions: {pred['total_predictions']}")
        print(f"  • High Confidence (>70%): {pred['high_confidence_predictions']}")
        print(f"  • Leagues Covered: {pred['leagues_covered']}")
        
        # Top Predictions
        if 'top_confidence' in pred and pred['top_confidence']:
            print("\n🎯 TOP CONFIDENCE PREDICTIONS:")
            for i, match in enumerate(pred['top_confidence'], 1):
                print(f"  {i}. {match['home_team']} vs {match['away_team']}")
                print(f"     Prediction: {match['predicted_result']} ({match['result_confidence']:.1%})")
        
        # League Breakdown
        if not predictions_df.empty:
            print("\n🏆 PREDICTIONS BY LEAGUE:")
            league_summary = predictions_df.groupby('league_name').agg({
                'fixture_id': 'count',
                'result_confidence': 'mean'
            }).round(3)
            
            for league, stats in league_summary.iterrows():
                print(f"  • {league}: {stats['fixture_id']} matches (avg confidence: {stats['result_confidence']:.1%})")
        
        print("\n" + "=" * 60)
        print("✅ ANALYSIS COMPLETE!")
        print("📁 All data saved to database and files")
        print("🎉 Ready for betting analysis!")

def main():
    """Main execution function"""
    API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    TARGET_DATE = "2025-07-13"
    
    # Initialize system
    system = ComprehensivePredictionSystem(API_KEY)
    
    # Run complete analysis
    results = system.run_complete_analysis(TARGET_DATE)
    
    if results:
        # Print final report
        system.print_final_report()
        
        # Save comprehensive summary
        with open(f'comprehensive_summary_{TARGET_DATE}.json', 'w') as f:
            json.dump(results['summary'], f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Comprehensive summary saved to comprehensive_summary_{TARGET_DATE}.json")
    else:
        print("\n❌ Analysis could not be completed")
        print("   Please check API limits and data availability")

if __name__ == "__main__":
    main()
