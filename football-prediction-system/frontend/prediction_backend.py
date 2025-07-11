#!/usr/bin/env python3
"""
🏆 Football Prediction Backend
==============================
Backend system for managing prediction results and website updates
"""

import json
import requests
from datetime import datetime, timedelta
import os

class PredictionBackend:
    def __init__(self):
        self.data_file = 'prediction_data.js'
        self.api_key = "052fd4885cf943ad859c89cef542e2e5"
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": self.api_key}
        
        # League ID mapping
        self.league_mapping = {
            'premier-league': 'PL',
            'la-liga': 'PD',
            'bundesliga': 'BL1',
            'serie-a': 'SA',
            'ligue-1': 'FL1'
        }
        
    def load_prediction_data(self):
        """Load prediction data from JavaScript file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract JSON data from JavaScript file
            start = content.find('const predictionData = ') + len('const predictionData = ')
            end = content.rfind('};') + 1
            json_str = content[start:end]
            
            return json.loads(json_str)
        except Exception as e:
            print(f"❌ Error loading prediction data: {e}")
            return None
    
    def save_prediction_data(self, data):
        """Save prediction data back to JavaScript file"""
        try:
            js_content = f"""// Football Prediction Data
const predictionData = {json.dumps(data, indent=4, ensure_ascii=False)};"""
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                f.write(js_content)
            
            print("✅ Prediction data saved successfully")
            return True
        except Exception as e:
            print(f"❌ Error saving prediction data: {e}")
            return False
    
    def get_real_match_results(self, league_id, days_back=7):
        """Get real match results from API"""
        print(f"📥 Fetching real results for {league_id}...")
        
        api_league_id = self.league_mapping.get(league_id)
        if not api_league_id:
            print(f"❌ Unknown league: {league_id}")
            return []
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        url = f"{self.base_url}/competitions/{api_league_id}/matches"
        params = {
            "status": "FINISHED",
            "dateFrom": start_date.strftime("%Y-%m-%d"),
            "dateTo": end_date.strftime("%Y-%m-%d")
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                matches = response.json()["matches"]
                print(f"✅ Found {len(matches)} finished matches")
                return matches
            else:
                print(f"❌ API Error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            return []
    
    def update_match_result(self, match_id, category, is_correct):
        """Update a specific match result"""
        data = self.load_prediction_data()
        if not data:
            return False
        
        # Find and update the match
        for league_id, league_data in data.items():
            for match in league_data['matches']:
                if match['id'] == match_id:
                    if category in match['predictions']:
                        match['predictions'][category]['result'] = 'correct' if is_correct else 'incorrect'
                        
                        # Save updated data
                        if self.save_prediction_data(data):
                            print(f"✅ Updated match {match_id}, category {category}: {'correct' if is_correct else 'incorrect'}")
                            return True
                    else:
                        print(f"❌ Category {category} not found in match {match_id}")
                        return False
        
        print(f"❌ Match {match_id} not found")
        return False
    
    def bulk_update_results(self, updates):
        """Bulk update multiple results"""
        print(f"🔄 Bulk updating {len(updates)} results...")
        
        data = self.load_prediction_data()
        if not data:
            return False
        
        updated_count = 0
        
        for update in updates:
            match_id = update['match_id']
            category = update['category']
            is_correct = update['is_correct']
            
            # Find and update the match
            for league_id, league_data in data.items():
                for match in league_data['matches']:
                    if match['id'] == match_id:
                        if category in match['predictions']:
                            match['predictions'][category]['result'] = 'correct' if is_correct else 'incorrect'
                            updated_count += 1
                            break
        
        if updated_count > 0:
            if self.save_prediction_data(data):
                print(f"✅ Successfully updated {updated_count} results")
                return True
        
        print(f"❌ Failed to update results")
        return False
    
    def auto_update_from_api(self, league_id):
        """Automatically update results from API"""
        print(f"🤖 Auto-updating {league_id} from API...")
        
        # Get prediction data
        data = self.load_prediction_data()
        if not data:
            return False
        
        # Get real match results
        real_matches = self.get_real_match_results(league_id)
        if not real_matches:
            return False
        
        # Match predictions with real results
        updates = []
        
        for real_match in real_matches:
            home_team = real_match["homeTeam"]["name"]
            away_team = real_match["awayTeam"]["name"]
            home_goals = real_match["score"]["fullTime"]["home"]
            away_goals = real_match["score"]["fullTime"]["away"]
            
            # Find corresponding prediction
            for match in data[league_id]['matches']:
                if (match['homeTeam'] in home_team or home_team in match['homeTeam']) and \
                   (match['awayTeam'] in away_team or away_team in match['awayTeam']):
                    
                    # Check match result
                    if home_goals > away_goals:
                        actual_result = 'Home Win'
                    elif away_goals > home_goals:
                        actual_result = 'Away Win'
                    else:
                        actual_result = 'Draw'
                    
                    predicted_result = match['predictions']['matchResult']['prediction']
                    is_correct = (predicted_result == actual_result)
                    
                    updates.append({
                        'match_id': match['id'],
                        'category': 'matchResult',
                        'is_correct': is_correct
                    })
                    
                    # Check handicap (-1.5 for home team)
                    handicap_result = (home_goals - 1.5) > away_goals
                    predicted_handicap = 'Home' in match['predictions']['handicap']['prediction']
                    
                    updates.append({
                        'match_id': match['id'],
                        'category': 'handicap',
                        'is_correct': handicap_result == predicted_handicap
                    })
                    
                    # Check over/under 2.5
                    total_goals = home_goals + away_goals
                    over_under_result = total_goals > 2.5
                    predicted_over = 'Over' in match['predictions']['overUnder']['prediction']
                    
                    updates.append({
                        'match_id': match['id'],
                        'category': 'overUnder',
                        'is_correct': over_under_result == predicted_over
                    })
                    
                    break
        
        # Apply updates
        if updates:
            return self.bulk_update_results(updates)
        else:
            print("❌ No matching predictions found")
            return False
    
    def generate_accuracy_report(self):
        """Generate accuracy report for all leagues"""
        print("📊 Generating Accuracy Report")
        print("=" * 50)
        
        data = self.load_prediction_data()
        if not data:
            return
        
        overall_stats = {
            'total_predictions': 0,
            'correct_predictions': 0,
            'categories': {
                'matchResult': {'correct': 0, 'total': 0},
                'handicap': {'correct': 0, 'total': 0},
                'overUnder': {'correct': 0, 'total': 0},
                'corners': {'correct': 0, 'total': 0}
            }
        }
        
        for league_id, league_data in data.items():
            print(f"\n🏆 {league_data['name']}:")
            
            league_stats = {
                'matchResult': {'correct': 0, 'total': 0},
                'handicap': {'correct': 0, 'total': 0},
                'overUnder': {'correct': 0, 'total': 0},
                'corners': {'correct': 0, 'total': 0}
            }
            
            for match in league_data['matches']:
                for category, prediction in match['predictions'].items():
                    if prediction['result'] != 'pending':
                        league_stats[category]['total'] += 1
                        overall_stats['categories'][category]['total'] += 1
                        overall_stats['total_predictions'] += 1
                        
                        if prediction['result'] == 'correct':
                            league_stats[category]['correct'] += 1
                            overall_stats['categories'][category]['correct'] += 1
                            overall_stats['correct_predictions'] += 1
            
            # Print league statistics
            for category, stats in league_stats.items():
                if stats['total'] > 0:
                    accuracy = (stats['correct'] / stats['total']) * 100
                    print(f"  📈 {category.replace('_', ' ').title()}: {accuracy:.1f}% ({stats['correct']}/{stats['total']})")
        
        # Print overall statistics
        print(f"\n🎯 OVERALL STATISTICS:")
        print("=" * 30)
        
        if overall_stats['total_predictions'] > 0:
            overall_accuracy = (overall_stats['correct_predictions'] / overall_stats['total_predictions']) * 100
            print(f"📊 Overall Accuracy: {overall_accuracy:.1f}% ({overall_stats['correct_predictions']}/{overall_stats['total_predictions']})")
        
        for category, stats in overall_stats['categories'].items():
            if stats['total'] > 0:
                accuracy = (stats['correct'] / stats['total']) * 100
                print(f"📈 {category.replace('_', ' ').title()}: {accuracy:.1f}% ({stats['correct']}/{stats['total']})")
    
    def create_admin_interface(self):
        """Create simple admin interface"""
        print("🔧 Football Prediction Admin Interface")
        print("=" * 50)
        
        while True:
            print("\n📋 Available Commands:")
            print("1. Update single match result")
            print("2. Bulk update results")
            print("3. Auto-update from API")
            print("4. Generate accuracy report")
            print("5. View prediction data")
            print("6. Exit")
            
            choice = input("\n👉 Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.admin_single_update()
            elif choice == '2':
                self.admin_bulk_update()
            elif choice == '3':
                self.admin_auto_update()
            elif choice == '4':
                self.generate_accuracy_report()
            elif choice == '5':
                self.admin_view_data()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def admin_single_update(self):
        """Admin interface for single update"""
        try:
            match_id = int(input("Match ID: "))
            category = input("Category (matchResult/handicap/overUnder/corners): ").strip()
            is_correct = input("Correct? (y/n): ").strip().lower() == 'y'
            
            self.update_match_result(match_id, category, is_correct)
        except ValueError:
            print("❌ Invalid input")
    
    def admin_bulk_update(self):
        """Admin interface for bulk update"""
        print("📝 Enter updates (format: match_id,category,correct)")
        print("Example: 1,matchResult,y")
        print("Type 'done' when finished:")
        
        updates = []
        while True:
            line = input("Update: ").strip()
            if line.lower() == 'done':
                break
            
            try:
                parts = line.split(',')
                if len(parts) == 3:
                    updates.append({
                        'match_id': int(parts[0]),
                        'category': parts[1].strip(),
                        'is_correct': parts[2].strip().lower() == 'y'
                    })
                else:
                    print("❌ Invalid format")
            except ValueError:
                print("❌ Invalid input")
        
        if updates:
            self.bulk_update_results(updates)
    
    def admin_auto_update(self):
        """Admin interface for auto update"""
        print("Available leagues:")
        for league_id in self.league_mapping.keys():
            print(f"- {league_id}")
        
        league_id = input("League ID: ").strip()
        if league_id in self.league_mapping:
            self.auto_update_from_api(league_id)
        else:
            print("❌ Invalid league ID")
    
    def admin_view_data(self):
        """Admin interface for viewing data"""
        data = self.load_prediction_data()
        if data:
            for league_id, league_data in data.items():
                print(f"\n🏆 {league_data['name']} ({len(league_data['matches'])} matches)")
                for match in league_data['matches'][:3]:  # Show first 3 matches
                    print(f"  {match['id']}: {match['homeTeam']} vs {match['awayTeam']}")

def main():
    print("🏆 Football Prediction Backend")
    print("=" * 50)
    
    backend = PredictionBackend()
    
    # Check if data file exists
    if not os.path.exists(backend.data_file):
        print(f"❌ Data file {backend.data_file} not found")
        print("💡 Make sure the website files are in the same directory")
        return
    
    # Start admin interface
    backend.create_admin_interface()

if __name__ == "__main__":
    main()
