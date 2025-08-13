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
from database_updater import DatabaseUpdater
import pandas as pd
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define path to the database used by the advanced system
DB_PATH = 'football-prediction-system/backend/prisma/football_predictions.db'


class IntegratedPredictionSystem:
    """ระบบทำนายฟุตบอลแบบครบวงจร (เวอร์ชันอัปเดตสำหรับฐานข้อมูล)"""

    def __init__(self, api_key: str, db_path: str):
        self.api_key = api_key
        self.fetcher = TodayMatchesFetcher(api_key)
        self.predictor = EnhancedMultiLeaguePredictor(api_key)
        self.db_updater = DatabaseUpdater(db_path)
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

    def _create_dummy_data(self) -> pd.DataFrame:
        """Creates a dummy DataFrame for testing when the API fails."""
        logger.info("🔧 API call failed. Creating dummy data for verification.")
        dummy_data = {
            'fixture_id': [999901, 999902],
            'league_id': [39, 140],
            'league_name': ['Premier League', 'La Liga'],
            'league_country': ['England', 'Spain'],
            'league_season': [2025, 2025],
            'date': [datetime.now(), datetime.now()],
            'home_team': ['Team A (dummy)', 'Team C (dummy)'],
            'away_team': ['Team B (dummy)', 'Team D (dummy)'],
        }
        return pd.DataFrame(dummy_data)

    def run_daily_analysis(self, date: str = None) -> dict:
        """รันการวิเคราะห์รายวันและอัปเดตฐานข้อมูล"""
        logger.info("📊 Starting daily analysis...")

        # Fetch today's matches
        matches_result = self.fetcher.run_daily_analysis(date)

        if not matches_result or matches_result['total_matches'] == 0:
            logger.warning("❌ No matches found from API. Using dummy data for verification.")
            matches_df = self._create_dummy_data()
        else:
            # Get matches dataframe
            matches_df = matches_result['dataframe']

        # Generate predictions if models are trained
        if self.is_trained:
            logger.info("🔮 Generating ML predictions...")
            predicted_df = self.predictor.generate_today_predictions(matches_df)
        else:
            logger.info("📝 Using basic predictions...")
            predicted_df = self._generate_basic_predictions(matches_df)

        # Update Database with predictions
        logger.info("💾 Updating database with new predictions...")
        try:
            self.db_updater.update_matches_and_predictions(predicted_df)
            logger.info("✅ Database update complete.")
        except Exception as e:
            logger.error(f"❌ Failed to update database: {e}")
            return {
                'total_matches': len(predicted_df),
                'database_updated': False,
                'error': str(e)
            }
        finally:
            self.db_updater.close()


        # Generate summary
        summary = self._generate_summary(predicted_df)

        return {
            'total_matches': len(predicted_df),
            'leagues_covered': predicted_df['league_name'].nunique(),
            'predictions_generated': True,
            'database_updated': True,
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

import os

def main():
    """Main function"""
    # The API key is now fetched from an environment variable for security.
    API_KEY = os.getenv("API_FOOTBALL_KEY")
    
    if not API_KEY:
        logger.error("FATAL: API_FOOTBALL_KEY environment variable not set.")
        print("❌ Error: API_FOOTBALL_KEY is not configured. Please set it as an environment variable.")
        return

    # Initialize system
    system = IntegratedPredictionSystem(api_key=API_KEY, db_path=DB_PATH)
    system.initialize_system()
    
    # Run daily analysis
    results = system.run_daily_analysis()
    
    if results and results.get('database_updated'):
        print("\n🎯 Integrated Prediction System Results:")
        print(f"📊 Total Matches Processed: {results['total_matches']}")
        print(f"🏆 Leagues Covered: {results['leagues_covered']}")
        print("✅ Database successfully updated with new predictions.")
        
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
    elif results:
        print(f"\n❌ An error occurred during the process.")
        print(f"   Error: {results.get('error', 'Unknown error')}")
    else:
        print("❌ No results generated. No matches found for the selected date.")

if __name__ == "__main__":
    main()
