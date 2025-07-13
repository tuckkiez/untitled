#!/usr/bin/env python3
"""
Swedish Allsvenskan Advanced ML Analysis Update
อัปเดตการวิเคราะห์ Swedish Allsvenskan ด้วย Advanced ML และ Real Odds
"""

import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import requests
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

class SwedishAllsvenskanMLAnalyzer:
    def __init__(self):
        self.api_key = "YOUR_API_KEY"  # Replace with actual API key
        self.models = {}
        self.scalers = {}
        self.results = {}
        
    def fetch_swedish_allsvenskan_data(self):
        """Fetch Swedish Allsvenskan fixtures and odds"""
        print("🇸🇪 Fetching Swedish Allsvenskan data...")
        
        # API endpoints
        fixtures_url = "https://v3.football.api-sports.io/fixtures"
        odds_url = "https://v3.football.api-sports.io/odds"
        
        headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'v3.football.api-sports.io'
        }
        
        # Get today's fixtures for Swedish Allsvenskan (League ID: 113)
        fixtures_params = {
            'league': 113,
            'season': 2025,
            'date': '2025-07-13'
        }
        
        try:
            fixtures_response = requests.get(fixtures_url, headers=headers, params=fixtures_params)
            fixtures_data = fixtures_response.json()
            
            if fixtures_data.get('results', 0) > 0:
                fixtures = fixtures_data['response']
                print(f"✅ Found {len(fixtures)} Swedish Allsvenskan fixtures")
                
                # Process each fixture
                processed_fixtures = []
                for fixture in fixtures:
                    fixture_data = self.process_fixture_with_odds(fixture, headers)
                    if fixture_data:
                        processed_fixtures.append(fixture_data)
                
                return processed_fixtures
            else:
                print("❌ No Swedish Allsvenskan fixtures found for today")
                return []
                
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return []
    
    def process_fixture_with_odds(self, fixture, headers):
        """Process individual fixture with odds data"""
        fixture_id = fixture['fixture']['id']
        
        # Get odds for this fixture
        odds_params = {'fixture': fixture_id}
        odds_url = "https://v3.football.api-sports.io/odds"
        
        try:
            odds_response = requests.get(odds_url, headers=headers, params=odds_params)
            odds_data = odds_response.json()
            
            if odds_data.get('results', 0) > 0:
                odds_info = odds_data['response'][0]
                
                # Extract key odds
                match_winner_odds = self.extract_match_winner_odds(odds_info)
                over_under_odds = self.extract_over_under_odds(odds_info)
                both_teams_score_odds = self.extract_both_teams_score_odds(odds_info)
                
                return {
                    'fixture_id': fixture_id,
                    'home_team': fixture['teams']['home']['name'],
                    'away_team': fixture['teams']['away']['name'],
                    'date': fixture['fixture']['date'],
                    'status': fixture['fixture']['status']['short'],
                    'league': 'Swedish Allsvenskan',
                    'match_winner_odds': match_winner_odds,
                    'over_under_odds': over_under_odds,
                    'both_teams_score_odds': both_teams_score_odds,
                    'venue': fixture['fixture']['venue']['name'],
                    'referee': fixture['fixture']['referee']
                }
        except Exception as e:
            print(f"⚠️ Error processing fixture {fixture_id}: {e}")
            
        return None
    
    def extract_match_winner_odds(self, odds_info):
        """Extract match winner odds"""
        for bookmaker in odds_info.get('bookmakers', []):
            for bet in bookmaker.get('bets', []):
                if bet['name'] == 'Match Winner':
                    values = bet['values']
                    return {
                        'home': float(values[0]['odd']) if len(values) > 0 else None,
                        'draw': float(values[1]['odd']) if len(values) > 1 else None,
                        'away': float(values[2]['odd']) if len(values) > 2 else None,
                        'bookmaker': bookmaker['name']
                    }
        return None
    
    def extract_over_under_odds(self, odds_info):
        """Extract Over/Under 2.5 goals odds"""
        for bookmaker in odds_info.get('bookmakers', []):
            for bet in bookmaker.get('bets', []):
                if bet['name'] == 'Goals Over/Under':
                    for value in bet['values']:
                        if 'Over 2.5' in value['value']:
                            over_odd = float(value['odd'])
                        elif 'Under 2.5' in value['value']:
                            under_odd = float(value['odd'])
                    
                    return {
                        'over_2_5': over_odd if 'over_odd' in locals() else None,
                        'under_2_5': under_odd if 'under_odd' in locals() else None,
                        'bookmaker': bookmaker['name']
                    }
        return None
    
    def extract_both_teams_score_odds(self, odds_info):
        """Extract Both Teams to Score odds"""
        for bookmaker in odds_info.get('bookmakers', []):
            for bet in bookmaker.get('bets', []):
                if bet['name'] == 'Both Teams Score':
                    values = bet['values']
                    return {
                        'yes': float(values[0]['odd']) if len(values) > 0 else None,
                        'no': float(values[1]['odd']) if len(values) > 1 else None,
                        'bookmaker': bookmaker['name']
                    }
        return None
    
    def create_ml_features(self, fixtures_data):
        """Create ML features from fixtures and odds data"""
        features = []
        
        for fixture in fixtures_data:
            if not fixture['match_winner_odds']:
                continue
                
            # Basic odds features
            home_odd = fixture['match_winner_odds']['home']
            draw_odd = fixture['match_winner_odds']['draw'] 
            away_odd = fixture['match_winner_odds']['away']
            
            # Implied probabilities
            total_prob = (1/home_odd + 1/draw_odd + 1/away_odd)
            home_prob = (1/home_odd) / total_prob
            draw_prob = (1/draw_odd) / total_prob
            away_prob = (1/away_odd) / total_prob
            
            # Market margin
            margin = total_prob - 1
            
            # Over/Under features
            ou_features = {}
            if fixture['over_under_odds']:
                over_odd = fixture['over_under_odds'].get('over_2_5')
                under_odd = fixture['over_under_odds'].get('under_2_5')
                if over_odd and under_odd:
                    ou_total = 1/over_odd + 1/under_odd
                    ou_features = {
                        'over_prob': (1/over_odd) / ou_total,
                        'under_prob': (1/under_odd) / ou_total,
                        'goal_expectation': 2.5 * ((1/under_odd) / ou_total) + 3.5 * ((1/over_odd) / ou_total)
                    }
            
            # Both Teams Score features
            bts_features = {}
            if fixture['both_teams_score_odds']:
                yes_odd = fixture['both_teams_score_odds'].get('yes')
                no_odd = fixture['both_teams_score_odds'].get('no')
                if yes_odd and no_odd:
                    bts_total = 1/yes_odd + 1/no_odd
                    bts_features = {
                        'bts_yes_prob': (1/yes_odd) / bts_total,
                        'bts_no_prob': (1/no_odd) / bts_total
                    }
            
            feature_row = {
                'fixture_id': fixture['fixture_id'],
                'home_team': fixture['home_team'],
                'away_team': fixture['away_team'],
                'home_odd': home_odd,
                'draw_odd': draw_odd,
                'away_odd': away_odd,
                'home_prob': home_prob,
                'draw_prob': draw_prob,
                'away_prob': away_prob,
                'margin': margin,
                'favorite_odd': min(home_odd, away_odd),
                'underdog_odd': max(home_odd, away_odd),
                'odds_ratio': max(home_odd, away_odd) / min(home_odd, away_odd),
                **ou_features,
                **bts_features
            }
            
            features.append(feature_row)
        
        return pd.DataFrame(features)
    
    def run_advanced_ml_analysis(self, features_df):
        """Run advanced ML analysis on Swedish Allsvenskan data"""
        print("🤖 Running Advanced ML Analysis...")
        
        # Simulate historical data for training (in real implementation, use actual historical data)
        historical_features = self.generate_historical_features()
        
        # Prepare features for ML
        feature_cols = ['home_prob', 'draw_prob', 'away_prob', 'margin', 'favorite_odd', 
                       'underdog_odd', 'odds_ratio']
        
        # Add O/U and BTS features if available
        if 'over_prob' in features_df.columns:
            feature_cols.extend(['over_prob', 'under_prob', 'goal_expectation'])
        if 'bts_yes_prob' in features_df.columns:
            feature_cols.extend(['bts_yes_prob', 'bts_no_prob'])
        
        X = historical_features[feature_cols].fillna(0)
        
        # Create target variables (simulated)
        y_match = historical_features['actual_result']  # 0=Home, 1=Draw, 2=Away
        y_over_under = historical_features['actual_over_under']  # 0=Under, 1=Over
        y_bts = historical_features['actual_bts']  # 0=No, 1=Yes
        
        # Train models
        models = {
            'match_result': RandomForestClassifier(n_estimators=100, random_state=42),
            'over_under': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'both_teams_score': LogisticRegression(random_state=42)
        }
        
        results = {}
        
        # Match Result Model
        X_train, X_test, y_train, y_test = train_test_split(X, y_match, test_size=0.3, random_state=42)
        models['match_result'].fit(X_train, y_train)
        y_pred = models['match_result'].predict(X_test)
        results['match_result_accuracy'] = accuracy_score(y_test, y_pred)
        
        # Over/Under Model
        models['over_under'].fit(X_train, y_over_under)
        y_pred_ou = models['over_under'].predict(X_test)
        results['over_under_accuracy'] = accuracy_score(y_over_under[X_test.index], y_pred_ou)
        
        # Both Teams Score Model
        models['both_teams_score'].fit(X_train, y_bts)
        y_pred_bts = models['both_teams_score'].predict(X_test)
        results['bts_accuracy'] = accuracy_score(y_bts[X_test.index], y_pred_bts)
        
        # Make predictions for today's matches
        today_features = features_df[feature_cols].fillna(0)
        
        predictions = []
        for idx, row in features_df.iterrows():
            feature_vector = today_features.iloc[idx:idx+1]
            
            # Match result prediction
            match_pred = models['match_result'].predict(feature_vector)[0]
            match_proba = models['match_result'].predict_proba(feature_vector)[0]
            
            # Over/Under prediction
            ou_pred = models['over_under'].predict(feature_vector)[0]
            ou_proba = models['over_under'].predict_proba(feature_vector)[0]
            
            # Both Teams Score prediction
            bts_pred = models['both_teams_score'].predict(feature_vector)[0]
            bts_proba = models['both_teams_score'].predict_proba(feature_vector)[0]
            
            prediction = {
                'fixture_id': row['fixture_id'],
                'home_team': row['home_team'],
                'away_team': row['away_team'],
                'match_result': {
                    'prediction': ['Home Win', 'Draw', 'Away Win'][match_pred],
                    'confidence': max(match_proba) * 100
                },
                'over_under': {
                    'prediction': 'Over 2.5' if ou_pred == 1 else 'Under 2.5',
                    'confidence': max(ou_proba) * 100
                },
                'both_teams_score': {
                    'prediction': 'Yes' if bts_pred == 1 else 'No',
                    'confidence': max(bts_proba) * 100
                },
                'odds_analysis': {
                    'home_odd': row['home_odd'],
                    'draw_odd': row['draw_odd'],
                    'away_odd': row['away_odd'],
                    'value_bet': self.detect_value_bet(row, match_proba)
                }
            }
            
            predictions.append(prediction)
        
        return {
            'predictions': predictions,
            'model_performance': results,
            'analysis_time': datetime.now(timezone.utc).isoformat()
        }
    
    def generate_historical_features(self):
        """Generate simulated historical features for training"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate realistic odds-based features
        home_odds = np.random.uniform(1.5, 4.0, n_samples)
        away_odds = np.random.uniform(1.5, 4.0, n_samples)
        draw_odds = np.random.uniform(2.8, 4.5, n_samples)
        
        # Calculate probabilities
        total_probs = 1/home_odds + 1/draw_odds + 1/away_odds
        home_probs = (1/home_odds) / total_probs
        draw_probs = (1/draw_odds) / total_probs
        away_probs = (1/away_odds) / total_probs
        
        margins = total_probs - 1
        favorite_odds = np.minimum(home_odds, away_odds)
        underdog_odds = np.maximum(home_odds, away_odds)
        odds_ratios = underdog_odds / favorite_odds
        
        # Generate O/U and BTS features
        over_probs = np.random.uniform(0.3, 0.7, n_samples)
        under_probs = 1 - over_probs
        goal_expectations = 2.5 + np.random.normal(0, 0.5, n_samples)
        
        bts_yes_probs = np.random.uniform(0.4, 0.8, n_samples)
        bts_no_probs = 1 - bts_yes_probs
        
        # Generate realistic outcomes based on probabilities
        actual_results = []
        actual_over_under = []
        actual_bts = []
        
        for i in range(n_samples):
            # Match result based on probabilities
            rand = np.random.random()
            if rand < home_probs[i]:
                actual_results.append(0)  # Home win
            elif rand < home_probs[i] + draw_probs[i]:
                actual_results.append(1)  # Draw
            else:
                actual_results.append(2)  # Away win
            
            # Over/Under based on goal expectation
            actual_over_under.append(1 if np.random.random() < over_probs[i] else 0)
            
            # Both Teams Score
            actual_bts.append(1 if np.random.random() < bts_yes_probs[i] else 0)
        
        return pd.DataFrame({
            'home_prob': home_probs,
            'draw_prob': draw_probs,
            'away_prob': away_probs,
            'margin': margins,
            'favorite_odd': favorite_odds,
            'underdog_odd': underdog_odds,
            'odds_ratio': odds_ratios,
            'over_prob': over_probs,
            'under_prob': under_probs,
            'goal_expectation': goal_expectations,
            'bts_yes_prob': bts_yes_probs,
            'bts_no_prob': bts_no_probs,
            'actual_result': actual_results,
            'actual_over_under': actual_over_under,
            'actual_bts': actual_bts
        })
    
    def detect_value_bet(self, row, match_proba):
        """Detect value betting opportunities"""
        home_prob_model = match_proba[0]
        draw_prob_model = match_proba[1]
        away_prob_model = match_proba[2]
        
        home_implied = 1 / row['home_odd']
        draw_implied = 1 / row['draw_odd']
        away_implied = 1 / row['away_odd']
        
        value_bets = []
        
        # Check for value bets (model probability > implied probability)
        if home_prob_model > home_implied * 1.05:  # 5% edge threshold
            value_bets.append({
                'type': 'Home Win',
                'model_prob': home_prob_model,
                'implied_prob': home_implied,
                'edge': (home_prob_model - home_implied) * 100,
                'odd': row['home_odd']
            })
        
        if draw_prob_model > draw_implied * 1.05:
            value_bets.append({
                'type': 'Draw',
                'model_prob': draw_prob_model,
                'implied_prob': draw_implied,
                'edge': (draw_prob_model - draw_implied) * 100,
                'odd': row['draw_odd']
            })
        
        if away_prob_model > away_implied * 1.05:
            value_bets.append({
                'type': 'Away Win',
                'model_prob': away_prob_model,
                'implied_prob': away_implied,
                'edge': (away_prob_model - away_implied) * 100,
                'odd': row['away_odd']
            })
        
        return value_bets
    
    def update_index_html(self, analysis_results):
        """Update index.html with Swedish Allsvenskan analysis"""
        print("📝 Updating index.html with Swedish Allsvenskan analysis...")
        
        # Read current index.html
        try:
            with open('/Users/80090/Desktop/Project/untitle/index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            print("❌ index.html not found")
            return
        
        # Create Swedish Allsvenskan section
        swedish_section = self.create_swedish_section_html(analysis_results)
        
        # Find insertion point (after main header, before existing predictions)
        insertion_point = html_content.find('<div class="predictions-section">')
        
        if insertion_point != -1:
            # Insert Swedish section
            updated_html = (html_content[:insertion_point] + 
                          swedish_section + 
                          html_content[insertion_point:])
            
            # Update stats in header
            updated_html = self.update_header_stats(updated_html, analysis_results)
            
            # Write updated HTML
            with open('/Users/80090/Desktop/Project/untitle/index.html', 'w', encoding='utf-8') as f:
                f.write(updated_html)
            
            print("✅ Successfully updated index.html with Swedish Allsvenskan analysis")
        else:
            print("❌ Could not find insertion point in index.html")
    
    def create_swedish_section_html(self, analysis_results):
        """Create HTML section for Swedish Allsvenskan"""
        predictions = analysis_results['predictions']
        performance = analysis_results['model_performance']
        
        html = f'''
        <!-- Swedish Allsvenskan Advanced ML Analysis -->
        <div class="predictions-section" style="margin-bottom: 40px;">
            <h2 class="section-title">🇸🇪 Swedish Allsvenskan - Advanced ML Analysis</h2>
            
            <!-- Performance Stats -->
            <div class="league-stats" style="margin-bottom: 30px;">
                <div class="stat-badge">
                    <strong>Match Result Accuracy:</strong> {performance.get('match_result_accuracy', 0)*100:.1f}%
                </div>
                <div class="stat-badge">
                    <strong>Over/Under Accuracy:</strong> {performance.get('over_under_accuracy', 0)*100:.1f}%
                </div>
                <div class="stat-badge">
                    <strong>Both Teams Score:</strong> {performance.get('bts_accuracy', 0)*100:.1f}%
                </div>
                <div class="stat-badge">
                    <strong>Analysis Time:</strong> {datetime.now().strftime('%H:%M UTC')}
                </div>
            </div>
            
            <div class="predictions-table-container">
                <table class="predictions-table">
                    <thead>
                        <tr>
                            <th>Match</th>
                            <th>Match Result</th>
                            <th>Over/Under 2.5</th>
                            <th>Both Teams Score</th>
                            <th>Value Bets</th>
                            <th>Odds Analysis</th>
                        </tr>
                    </thead>
                    <tbody>
        '''
        
        for pred in predictions:
            # Determine confidence class
            avg_confidence = (pred['match_result']['confidence'] + 
                            pred['over_under']['confidence'] + 
                            pred['both_teams_score']['confidence']) / 3
            
            if avg_confidence >= 75:
                confidence_class = "high-confidence"
            elif avg_confidence >= 60:
                confidence_class = "medium-confidence"
            else:
                confidence_class = "low-confidence"
            
            # Value bets display
            value_bets_html = ""
            if pred['odds_analysis']['value_bet']:
                for vb in pred['odds_analysis']['value_bet']:
                    value_bets_html += f"<div style='color: #28a745; font-weight: bold;'>{vb['type']}: +{vb['edge']:.1f}% edge</div>"
            else:
                value_bets_html = "<span style='opacity: 0.6;'>No value detected</span>"
            
            html += f'''
                        <tr class="match-row {confidence_class}">
                            <td class="match-teams">
                                <strong>{pred['home_team']} vs {pred['away_team']}</strong>
                                <div class="match-details">
                                    <span>🇸🇪 Swedish Allsvenskan</span>
                                    <span>📊 Advanced ML</span>
                                </div>
                            </td>
                            <td class="prediction-cell">
                                <div class="prediction-main">{pred['match_result']['prediction']}</div>
                                <div class="confidence">Confidence: {pred['match_result']['confidence']:.1f}%</div>
                            </td>
                            <td class="prediction-cell">
                                <div class="prediction-main">{pred['over_under']['prediction']}</div>
                                <div class="confidence">Confidence: {pred['over_under']['confidence']:.1f}%</div>
                            </td>
                            <td class="prediction-cell">
                                <div class="prediction-main">{pred['both_teams_score']['prediction']}</div>
                                <div class="confidence">Confidence: {pred['both_teams_score']['confidence']:.1f}%</div>
                            </td>
                            <td class="prediction-cell">
                                {value_bets_html}
                            </td>
                            <td class="prediction-cell">
                                <div style="font-size: 0.85em;">
                                    <div>Home: {pred['odds_analysis']['home_odd']:.2f}</div>
                                    <div>Draw: {pred['odds_analysis']['draw_odd']:.2f}</div>
                                    <div>Away: {pred['odds_analysis']['away_odd']:.2f}</div>
                                </div>
                            </td>
                        </tr>
            '''
        
        html += '''
                    </tbody>
                </table>
            </div>
        </div>
        '''
        
        return html
    
    def update_header_stats(self, html_content, analysis_results):
        """Update header statistics"""
        # Find and update league stats
        stats_section = html_content.find('<div class="league-stats">')
        if stats_section != -1:
            # Add Swedish Allsvenskan to stats
            new_stat = f'''<div class="stat-badge">🇸🇪 Swedish Allsvenskan: {len(analysis_results['predictions'])} matches analyzed</div>'''
            
            # Insert after opening div
            insert_pos = html_content.find('>', stats_section) + 1
            html_content = html_content[:insert_pos] + new_stat + html_content[insert_pos:]
        
        return html_content
    
    def save_analysis_results(self, analysis_results):
        """Save analysis results to JSON file"""
        filename = f"swedish_allsvenskan_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        filepath = f"/Users/80090/Desktop/Project/untitle/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Analysis results saved to {filename}")
        return filepath

def main():
    """Main execution function"""
    print("🚀 Starting Swedish Allsvenskan Advanced ML Analysis...")
    
    analyzer = SwedishAllsvenskanMLAnalyzer()
    
    # Step 1: Fetch data
    fixtures_data = analyzer.fetch_swedish_allsvenskan_data()
    
    if not fixtures_data:
        print("❌ No data available for analysis")
        return
    
    # Step 2: Create ML features
    features_df = analyzer.create_ml_features(fixtures_data)
    print(f"📊 Created features for {len(features_df)} matches")
    
    # Step 3: Run ML analysis
    analysis_results = analyzer.run_advanced_ml_analysis(features_df)
    
    # Step 4: Update index.html
    analyzer.update_index_html(analysis_results)
    
    # Step 5: Save results
    analyzer.save_analysis_results(analysis_results)
    
    # Step 6: Print summary
    print("\n" + "="*60)
    print("🇸🇪 SWEDISH ALLSVENSKAN ADVANCED ML ANALYSIS COMPLETE")
    print("="*60)
    print(f"📊 Matches Analyzed: {len(analysis_results['predictions'])}")
    print(f"🎯 Match Result Accuracy: {analysis_results['model_performance']['match_result_accuracy']*100:.1f}%")
    print(f"⚽ Over/Under Accuracy: {analysis_results['model_performance']['over_under_accuracy']*100:.1f}%")
    print(f"🥅 Both Teams Score Accuracy: {analysis_results['model_performance']['bts_accuracy']*100:.1f}%")
    print(f"⏰ Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("="*60)
    
    # Print top predictions
    print("\n🔥 TOP PREDICTIONS:")
    for i, pred in enumerate(analysis_results['predictions'][:3], 1):
        avg_conf = (pred['match_result']['confidence'] + 
                   pred['over_under']['confidence'] + 
                   pred['both_teams_score']['confidence']) / 3
        print(f"{i}. {pred['home_team']} vs {pred['away_team']}")
        print(f"   Result: {pred['match_result']['prediction']} ({pred['match_result']['confidence']:.1f}%)")
        print(f"   O/U: {pred['over_under']['prediction']} ({pred['over_under']['confidence']:.1f}%)")
        print(f"   BTS: {pred['both_teams_score']['prediction']} ({pred['both_teams_score']['confidence']:.1f}%)")
        print(f"   Average Confidence: {avg_conf:.1f}%")
        if pred['odds_analysis']['value_bet']:
            print(f"   💰 Value Bets: {len(pred['odds_analysis']['value_bet'])} detected")
        print()

if __name__ == "__main__":
    main()
