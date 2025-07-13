#!/usr/bin/env python3
"""
🚀 Real Predictions Index Updater
อัปเดตหน้า index.html ด้วยการทำนายจริงจากข้อมูลสถิติ
"""

import requests
import json
from datetime import datetime, timedelta
import time
from advanced_real_predictions import AdvancedRealPredictor

class RealPredictionsUpdater:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        self.predictor = AdvancedRealPredictor(api_key)
        
        # ลีกที่สนใจ
        self.target_leagues = [
            "FIFA Club World Cup",
            "Allsvenskan",
            "Veikkausliiga", 
            "Super Cup",
            "Serie A",
            "Serie B",
            "Primera Nacional",
            "Primera A",
            "Primera División",
            "2. Division",
            "3. Division",
            "Eliteserien",
            "Premier League",
            "Liga MX"
        ]

    def fetch_matches(self, date):
        """ดึงข้อมูลการแข่งขันจาก API"""
        url = f"{self.base_url}/fixtures"
        params = {"date": date}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('response', [])
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return []

    def filter_target_matches(self, matches):
        """กรองเฉพาะลีกที่สนใจ"""
        filtered = []
        for match in matches:
            league_name = match['league']['name']
            if any(target in league_name for target in self.target_leagues):
                filtered.append(match)
        return filtered

    def get_real_predictions(self, match):
        """ดึงการทำนายจริงสำหรับแต่ละแมตช์"""
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        league_name = match['league']['name']
        
        print(f"🔮 Predicting: {home_team} vs {away_team} ({league_name})")
        
        try:
            if "FIFA Club World Cup" in league_name:
                # ใช้การทำนายพิเศษสำหรับ FIFA Club World Cup
                predictions = self.predictor.get_fifa_club_world_cup_prediction(home_team, away_team)
            else:
                # ใช้การทำนายปกติสำหรับลีกอื่นๆ
                predictions = self.get_league_predictions(match)
            
            return predictions
            
        except Exception as e:
            print(f"❌ Prediction error for {home_team} vs {away_team}: {e}")
            return self.predictor.get_default_prediction()

    def get_league_predictions(self, match):
        """ดึงการทำนายสำหรับลีกปกติ"""
        # ค้นหาข้อมูลทีมและสถิติ
        home_team_id = match['teams']['home']['id']
        away_team_id = match['teams']['away']['id']
        league_id = match['league']['id']
        season = match['league']['season'] if 'season' in match['league'] else 2025
        
        # ดึงสถิติทีม
        home_stats = self.predictor.get_team_statistics(home_team_id, league_id, season)
        away_stats = self.predictor.get_team_statistics(away_team_id, league_id, season)
        
        # ดึงข้อมูล H2H และฟอร์ม
        h2h_data = self.predictor.get_head_to_head(home_team_id, away_team_id)
        home_form = self.predictor.get_recent_form(home_team_id, league_id, season)
        away_form = self.predictor.get_recent_form(away_team_id, league_id, season)
        
        # สร้างการทำนาย
        return self.predictor.generate_full_prediction(home_stats, away_stats, h2h_data, home_form, away_form)

    def format_predictions_for_display(self, predictions):
        """จัดรูปแบบการทำนายสำหรับแสดงผล"""
        if not predictions:
            return {
                'result': 'Draw',
                'result_confidence': 55,
                'handicap': '0',
                'handicap_confidence': 50,
                'over_under': 'Over 2.5',
                'ou_confidence': 60,
                'corner_ht': 'Under 5',
                'corner_ht_confidence': 60,
                'corner_ft': 'Over 9',
                'corner_ft_confidence': 65
            }
        
        return {
            'result': predictions.get('match_result', {}).get('prediction', 'Draw'),
            'result_confidence': predictions.get('match_result', {}).get('confidence', 55),
            'handicap': predictions.get('handicap', {}).get('handicap', '0'),
            'handicap_confidence': predictions.get('handicap', {}).get('confidence', 50),
            'over_under': predictions.get('over_under', {}).get('prediction', 'Over 2.5'),
            'ou_confidence': predictions.get('over_under', {}).get('confidence', 60),
            'corner_ht': predictions.get('corners', {}).get('halftime', {}).get('prediction', 'Under 5'),
            'corner_ht_confidence': predictions.get('corners', {}).get('halftime', {}).get('confidence', 60),
            'corner_ft': predictions.get('corners', {}).get('fulltime', {}).get('prediction', 'Over 9'),
            'corner_ft_confidence': predictions.get('corners', {}).get('fulltime', {}).get('confidence', 65)
        }

    def run_predictions(self):
        """รันการทำนายสำหรับวันนี้และพรุ่งนี้"""
        print("🚀 Starting Real Predictions Analysis...")
        
        # ดึงข้อมูล 2 วัน
        today = datetime.now().strftime('%Y-%m-%d')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        all_matches_with_predictions = {}
        
        for date in [today, tomorrow]:
            print(f"📊 Processing matches for {date}...")
            matches = self.fetch_matches(date)
            filtered_matches = self.filter_target_matches(matches)
            
            if not filtered_matches:
                print(f"❌ No target matches found for {date}")
                continue
            
            matches_with_predictions = []
            
            for i, match in enumerate(filtered_matches):
                print(f"🔮 Processing match {i+1}/{len(filtered_matches)}")
                
                # ดึงการทำนายจริง
                predictions = self.get_real_predictions(match)
                formatted_predictions = self.format_predictions_for_display(predictions)
                
                # เพิ่มการทำนายเข้าไปในข้อมูลแมตช์
                match['real_predictions'] = formatted_predictions
                matches_with_predictions.append(match)
                
                # หน่วงเวลาเพื่อไม่ให้ API rate limit
                time.sleep(1)
            
            all_matches_with_predictions[date] = matches_with_predictions
            print(f"✅ Completed {len(matches_with_predictions)} matches for {date}")
        
        return all_matches_with_predictions

if __name__ == "__main__":
    api_key = "f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0"
    updater = RealPredictionsUpdater(api_key)
    
    # ทดสอบการทำงาน
    results = updater.run_predictions()
    print(f"📊 Total processed: {sum(len(matches) for matches in results.values())} matches")
