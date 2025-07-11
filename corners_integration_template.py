#!/usr/bin/env python3
"""
🏆 Corners Data Integration Template
===================================
Ready-to-use template for when corners data becomes available
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import requests
from datetime import datetime

class CornersDataIntegrator:
    def __init__(self):
        self.corners_sources = {
            'rapidapi': {
                'url': 'https://api-football-v1.p.rapidapi.com',
                'headers': {'X-RapidAPI-Key': 'YOUR_KEY_HERE'},
                'status': 'paid'
            },
            'thesportsdb': {
                'url': 'https://www.thesportsdb.com/api/v1/json',
                'headers': {},
                'status': 'limited'
            },
            'web_scraping': {
                'sources': ['ESPN', 'BBC Sport', 'Flashscore'],
                'status': 'manual'
            }
        }
    
    def test_rapidapi_corners(self, api_key):
        """Test RapidAPI for corners data"""
        print("🧪 Testing RapidAPI for Corners...")
        
        headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
        }
        
        # Test endpoint
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {
            'league': '39',  # Premier League
            'season': '2024',
            'last': '10'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data and len(data['response']) > 0:
                    match = data['response'][0]
                    
                    # Check for corners data
                    if 'statistics' in match:
                        print("✅ Statistics available")
                        return True
                    else:
                        print("❌ No statistics in response")
                        return False
                else:
                    print("❌ No matches in response")
                    return False
            else:
                print(f"❌ API Error: {response.status_code}")
                if response.status_code == 403:
                    print("💡 Need to upgrade RapidAPI plan")
                elif response.status_code == 429:
                    print("💡 Rate limit exceeded")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def scrape_espn_corners(self, match_url):
        """Template for ESPN corners scraping"""
        print("🕷️ ESPN Corners Scraping Template")
        print("⚠️  Requires: pip install beautifulsoup4 selenium")
        
        scraping_code = '''
        from bs4 import BeautifulSoup
        import requests
        
        def get_espn_corners(match_url):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            try:
                response = requests.get(match_url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find corners statistics
                stats_section = soup.find('section', class_='Statistics')
                if stats_section:
                    corners_row = stats_section.find('tr', string=lambda text: 'Corner' in text if text else False)
                    if corners_row:
                        corners_data = corners_row.find_all('td')
                        home_corners = int(corners_data[0].text)
                        away_corners = int(corners_data[2].text)
                        return home_corners, away_corners
                
                return None, None
                
            except Exception as e:
                print(f"Scraping error: {e}")
                return None, None
        '''
        
        print("📋 Code template ready for implementation")
        return scraping_code
    
    def integrate_corners_data(self, matches_data, corners_source='manual'):
        """Integrate corners data into existing match data"""
        print(f"🔗 Integrating corners data from: {corners_source}")
        
        enhanced_data = matches_data.copy()
        
        if corners_source == 'manual':
            # Manual data entry template
            print("📝 Manual corners data entry:")
            print("Format: match_id,home_corners,away_corners")
            
            # Example manual data
            manual_corners = {
                'match_1': {'home': 6, 'away': 4},
                'match_2': {'home': 8, 'away': 3},
                'match_3': {'home': 5, 'away': 7}
            }
            
            # Add corners features
            enhanced_data['home_corners'] = 0
            enhanced_data['away_corners'] = 0
            enhanced_data['total_corners'] = 0
            enhanced_data['corners_over_9'] = 0
            enhanced_data['corners_handicap'] = 0  # Home -2.5 corners
            
            print("✅ Corners columns added to dataset")
            
        elif corners_source == 'api':
            # API integration template
            print("🔌 API corners integration template ready")
            
        elif corners_source == 'scraping':
            # Web scraping integration
            print("🕷️ Web scraping integration template ready")
        
        return enhanced_data
    
    def train_corners_model(self, data_with_corners):
        """Train corners prediction model"""
        print("🤖 Training Corners Prediction Model...")
        
        # Features for corners prediction
        corners_features = [
            'home_elo', 'away_elo', 'elo_diff',
            'home_attack_strength', 'away_attack_strength',
            'home_recent_corners_avg', 'away_recent_corners_avg'
        ]
        
        # Prepare data
        X = data_with_corners[corners_features].fillna(0)
        
        # Multiple corners targets
        models = {}
        
        # Over/Under 9.5 corners
        if 'corners_over_9' in data_with_corners.columns:
            y_corners_ou = data_with_corners['corners_over_9'].dropna()
            X_corners = X.loc[y_corners_ou.index]
            
            models['corners_over_under'] = RandomForestClassifier(n_estimators=100, random_state=42)
            models['corners_over_under'].fit(X_corners, y_corners_ou)
            print("✅ Corners Over/Under model trained")
        
        # Corners handicap (Home -2.5)
        if 'corners_handicap' in data_with_corners.columns:
            y_corners_hcp = data_with_corners['corners_handicap'].dropna()
            X_corners_hcp = X.loc[y_corners_hcp.index]
            
            models['corners_handicap'] = RandomForestClassifier(n_estimators=100, random_state=42)
            models['corners_handicap'].fit(X_corners_hcp, y_corners_hcp)
            print("✅ Corners Handicap model trained")
        
        return models
    
    def predict_corners(self, models, home_team, away_team, team_stats):
        """Predict corners for a match"""
        if not models:
            return {
                'corners_over_under': 'Data not available',
                'corners_handicap': 'Data not available',
                'confidence': 0.0
            }
        
        # Prepare features
        features = np.array([[
            team_stats.get(home_team, {}).get('elo', 1500),
            team_stats.get(away_team, {}).get('elo', 1500),
            team_stats.get(home_team, {}).get('elo', 1500) - team_stats.get(away_team, {}).get('elo', 1500),
            team_stats.get(home_team, {}).get('attack_strength', 1.0),
            team_stats.get(away_team, {}).get('attack_strength', 1.0),
            team_stats.get(home_team, {}).get('avg_corners', 5.0),
            team_stats.get(away_team, {}).get('avg_corners', 5.0)
        ]])
        
        predictions = {}
        
        # Over/Under 9.5 corners
        if 'corners_over_under' in models:
            ou_proba = models['corners_over_under'].predict_proba(features)[0]
            predictions['corners_over_under'] = {
                'prediction': 'Over 9.5' if ou_proba[1] > 0.5 else 'Under 9.5',
                'confidence': max(ou_proba)
            }
        
        # Corners handicap
        if 'corners_handicap' in models:
            hcp_proba = models['corners_handicap'].predict_proba(features)[0]
            predictions['corners_handicap'] = {
                'prediction': f'{home_team} -2.5' if hcp_proba[1] > 0.5 else f'{away_team} +2.5',
                'confidence': max(hcp_proba)
            }
        
        return predictions
    
    def generate_corners_data_plan(self):
        """Generate action plan for corners data acquisition"""
        plan = """
        🎯 Corners Data Acquisition Plan
        ================================
        
        📋 Priority Options:
        
        1. 💰 RapidAPI Football (Recommended)
           - Cost: $10-50/month
           - Reliability: High
           - Data Quality: Excellent
           - Implementation: 1-2 days
        
        2. 🕷️ Web Scraping
           - Cost: Free
           - Reliability: Medium
           - Data Quality: Good
           - Implementation: 1-2 weeks
           - Risk: Site changes
        
        3. 📊 Manual Collection
           - Cost: Time
           - Reliability: High
           - Data Quality: Perfect
           - Implementation: Ongoing
           - Scalability: Limited
        
        4. 🤝 Data Partnership
           - Cost: Variable
           - Reliability: High
           - Data Quality: Excellent
           - Implementation: 2-4 weeks
        
        📈 Implementation Steps:
        
        Phase 1: Test & Validate
        - [ ] Test RapidAPI with trial
        - [ ] Validate data quality
        - [ ] Check historical coverage
        
        Phase 2: Integration
        - [ ] Modify data pipeline
        - [ ] Add corners features
        - [ ] Retrain models
        
        Phase 3: Backtesting
        - [ ] Test on historical data
        - [ ] Validate accuracy
        - [ ] Compare with current system
        
        Phase 4: Production
        - [ ] Deploy corners predictions
        - [ ] Monitor performance
        - [ ] Continuous improvement
        """
        
        return plan

def main():
    print("🏆 Corners Data Integration System")
    print("=" * 50)
    
    integrator = CornersDataIntegrator()
    
    # Show current status
    print("📊 Current Corners Data Status:")
    for source, info in integrator.corners_sources.items():
        print(f"   {source}: {info['status']}")
    
    print("\n" + integrator.generate_corners_data_plan())
    
    # Test RapidAPI if key provided
    print("\n🧪 API Testing:")
    print("To test RapidAPI: integrator.test_rapidapi_corners('YOUR_API_KEY')")
    
    # Show scraping template
    scraping_code = integrator.scrape_espn_corners("example_url")
    
    print("\n✅ Integration templates ready!")
    print("💡 Run this script when corners data source is available")

if __name__ == "__main__":
    main()
