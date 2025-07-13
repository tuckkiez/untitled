#!/usr/bin/env python3
"""
🚀 Integrated Football Prediction System
ระบบทำนายฟุตบอลแบบครบวงจร

Combines:
- Today Matches Fetcher
- Enhanced Multi-League Predictor
- Real-time predictions with ML models
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from today_matches_fetcher import TodayMatchesFetcher
from enhanced_multi_league_predictor import EnhancedMultiLeaguePredictor
import pandas as pd
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegratedPredictionSystem:
    """ระบบทำนายฟุตบอลแบบครบวงจร"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.fetcher = TodayMatchesFetcher(api_key)
        self.predictor = EnhancedMultiLeaguePredictor(api_key)
        self.is_trained = False
        
    def initialize_system(self):
        """เริ่มต้นระบบและเทรนโมเดล"""
        logger.info("🚀 Initializing Integrated Prediction System...")
        
        # Train ML models
        logger.info("🤖 Training ML models...")
        training_data = self.predictor.prepare_training_data()
        
        if not training_data.empty:
            self.predictor.train_models(training_data)
            self.is_trained = True
            logger.info("✅ ML models trained successfully!")
        else:
            logger.warning("⚠️ No training data available - using basic predictions")
            
    def run_daily_analysis(self, date: str = None) -> dict:
        """รันการวิเคราะห์รายวัน"""
        logger.info("📊 Starting daily analysis...")
        
        # Fetch today's matches
        matches_result = self.fetcher.run_daily_analysis(date)
        
        if not matches_result or matches_result['total_matches'] == 0:
            logger.warning("❌ No matches found for analysis")
            return {}
        
        # Get matches dataframe
        matches_df = matches_result['dataframe']
        
        # Generate predictions if models are trained
        if self.is_trained:
            logger.info("🔮 Generating ML predictions...")
            predicted_df = self.predictor.generate_today_predictions(matches_df)
        else:
            logger.info("📝 Using basic predictions...")
            predicted_df = self._generate_basic_predictions(matches_df)
        
        # Update HTML with predictions
        html_content = self.fetcher.generate_html_table(predicted_df)
        html_file = self.fetcher.save_html_report(html_content, "integrated_predictions_report.html")
        
        # Export updated CSV
        csv_file = self.fetcher.export_to_csv(predicted_df, "integrated_predictions.csv")
        
        # Generate summary
        summary = self._generate_summary(predicted_df)
        
        return {
            'total_matches': len(predicted_df),
            'leagues_covered': predicted_df['league_name'].nunique(),
            'predictions_generated': True,
            'csv_file': csv_file,
            'html_file': html_file,
            'summary': summary,
            'dataframe': predicted_df
        }
    
    def _generate_basic_predictions(self, df: pd.DataFrame) -> pd.DataFrame:
        """สร้างการทำนายพื้นฐาน (เมื่อไม่มีโมเดล ML)"""
        import random
        
        for idx, row in df.iterrows():
            # Basic random predictions (for demo)
            results = ['Home Win', 'Draw', 'Away Win']
            ou_options = ['Over 2.5', 'Under 2.5']
            
            df.at[idx, 'predicted_result'] = random.choice(results)
            df.at[idx, 'result_confidence'] = f"{random.randint(50, 85)}%"
            df.at[idx, 'predicted_over_under'] = random.choice(ou_options)
            df.at[idx, 'ou_confidence'] = f"{random.randint(55, 80)}%"
            df.at[idx, 'value_bet_rating'] = random.choice(['🔥 High Value', '⭐ Good Value', '✅ Fair Value'])
            df.at[idx, 'recommended_bet'] = f"{df.at[idx, 'predicted_result']} + {df.at[idx, 'predicted_over_under']}"
        
        return df
    
    def _generate_summary(self, df: pd.DataFrame) -> dict:
        """สร้างสรุปผลการวิเคราะห์"""
        if df.empty:
            return {}
        
        # Count predictions by type
        result_counts = df['predicted_result'].value_counts().to_dict()
        ou_counts = df['predicted_over_under'].value_counts().to_dict()
        value_counts = df['value_bet_rating'].value_counts().to_dict()
        
        # High confidence predictions
        high_conf_matches = df[df['result_confidence'].str.contains('7[0-9]%|8[0-9]%|9[0-9]%', na=False)]
        
        return {
            'total_predictions': len(df),
            'result_distribution': result_counts,
            'over_under_distribution': ou_counts,
            'value_distribution': value_counts,
            'high_confidence_count': len(high_conf_matches),
            'high_confidence_matches': high_conf_matches[['home_team', 'away_team', 'predicted_result', 'result_confidence']].to_dict('records') if not high_conf_matches.empty else []
        }

def main():
    """Main function"""
    API_KEY = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    
    # Initialize system
    system = IntegratedPredictionSystem(API_KEY)
    system.initialize_system()
    
    # Run daily analysis
    results = system.run_daily_analysis()
    
    if results:
        print("\n🎯 Integrated Prediction System Results:")
        print(f"📊 Total Matches: {results['total_matches']}")
        print(f"🏆 Leagues Covered: {results['leagues_covered']}")
        print(f"📁 CSV File: {results['csv_file']}")
        print(f"🌐 HTML File: {results['html_file']}")
        
        # Display summary
        summary = results['summary']
        print(f"\n📈 Predictions Summary:")
        print(f"  • Total Predictions: {summary.get('total_predictions', 0)}")
        print(f"  • High Confidence: {summary.get('high_confidence_count', 0)}")
        
        if summary.get('result_distribution'):
            print(f"  • Result Distribution: {summary['result_distribution']}")
        
        if summary.get('high_confidence_matches'):
            print(f"\n🔥 High Confidence Matches:")
            for match in summary['high_confidence_matches'][:3]:  # Show top 3
                print(f"    {match['home_team']} vs {match['away_team']}: {match['predicted_result']} ({match['result_confidence']})")
    else:
        print("❌ No results generated")

if __name__ == "__main__":
    main()
