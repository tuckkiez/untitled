# 📚 Examples & Use Cases - Ultra Advanced Football Predictor

ตัวอย่างการใช้งานจริงและกรณีศึกษาต่างๆ

## 🎯 Use Case 1: การทำนายเกมสำคัญ

### Big 6 Matches Analysis

```python
from ultra_predictor_fixed import UltraAdvancedPredictor

predictor = UltraAdvancedPredictor()
data = predictor.load_premier_league_data()
predictor.train_ensemble_models(data)

# Big 6 teams
big_6 = ["Arsenal", "Chelsea", "Liverpool", "Manchester City", 
         "Manchester United", "Tottenham"]

print("🏆 การทำนาย Big 6 Matches")
print("="*60)

for i, home in enumerate(big_6):
    for away in big_6[i+1:]:
        pred = predictor.predict_match_ultra(home, away)
        
        confidence_level = "🔥" if pred['confidence'] > 0.7 else "✅" if pred['confidence'] > 0.6 else "⚖️"
        
        print(f"{confidence_level} {home} vs {away}")
        print(f"   ทำนาย: {pred['prediction']} ({pred['confidence']:.1%})")
        print(f"   โอกาส: H:{pred['probabilities']['Home Win']:.1%} "
              f"D:{pred['probabilities']['Draw']:.1%} "
              f"A:{pred['probabilities']['Away Win']:.1%}")
        print()
```

## 🎲 Use Case 2: Handicap Betting Analysis

### การวิเคราะห์ราคาต่อรอง

```python
from test_handicap_20_games import HandicapTester

class BettingAnalyzer:
    def __init__(self):
        self.handicap_tester = HandicapTester()
        
    def analyze_betting_opportunities(self, matches):
        """วิเคราะห์โอกาสการเดิมพัน"""
        print("🎲 การวิเคราะห์โอกาสการเดิมพัน")
        print("="*80)
        
        opportunities = []
        
        for home, away in matches:
            pred = self.handicap_tester.predictor.predict_match_ultra(home, away)
            
            if not pred:
                continue
                
            # คำนวณ value bet
            confidence = pred['confidence']
            home_prob = pred['probabilities']['Home Win']
            away_prob = pred['probabilities']['Away Win']
            draw_prob = pred['probabilities']['Draw']
            
            # สมมติราคาต่อรอง (odds)
            home_odds = 1 / home_prob if home_prob > 0 else 999
            away_odds = 1 / away_prob if away_prob > 0 else 999
            draw_odds = 1 / draw_prob if draw_prob > 0 else 999
            
            # หา value bets
            if confidence > 0.65:
                opportunities.append({
                    'match': f"{home} vs {away}",
                    'prediction': pred['prediction'],
                    'confidence': confidence,
                    'value': 'HIGH' if confidence > 0.75 else 'MEDIUM',
                    'recommended_bet': pred['prediction'],
                    'odds': {
                        'Home': home_odds,
                        'Draw': draw_odds, 
                        'Away': away_odds
                    }
                })
        
        # แสดงผล
        for opp in sorted(opportunities, key=lambda x: x['confidence'], reverse=True):
            print(f"🎯 {opp['match']}")
            print(f"   แนะนำ: {opp['recommended_bet']} (มั่นใจ {opp['confidence']:.1%})")
            print(f"   ระดับ: {opp['value']}")
            print(f"   ราคา: H:{opp['odds']['Home']:.2f} D:{opp['odds']['Draw']:.2f} A:{opp['odds']['Away']:.2f}")
            print()
        
        return opportunities

# ใช้งาน
analyzer = BettingAnalyzer()
matches = [
    ("Arsenal", "Chelsea"),
    ("Manchester City", "Liverpool"),
    ("Manchester United", "Tottenham"),
    ("Newcastle", "Brighton"),
    ("Aston Villa", "West Ham")
]

opportunities = analyzer.analyze_betting_opportunities(matches)
```

## 📊 Use Case 3: Season Performance Tracking

### การติดตามผลงานตลอดฤดูกาล

```python
import pandas as pd
from datetime import datetime, timedelta

class SeasonTracker:
    def __init__(self):
        self.predictor = UltraAdvancedPredictor()
        self.predictions_log = []
        
    def track_season_predictions(self, start_date, end_date):
        """ติดตามการทำนายตลอดฤดูกาล"""
        
        # โหลดข้อมูลและเทรน
        data = self.predictor.load_premier_league_data()
        self.predictor.train_ensemble_models(data)
        
        # กรองเกมในช่วงเวลาที่กำหนด
        season_matches = data[
            (pd.to_datetime(data['date']) >= start_date) &
            (pd.to_datetime(data['date']) <= end_date)
        ]
        
        print(f"📅 การติดตามฤดูกาล {start_date.strftime('%Y-%m-%d')} ถึง {end_date.strftime('%Y-%m-%d')}")
        print(f"📊 จำนวนเกม: {len(season_matches)} เกม")
        print("="*80)
        
        correct_predictions = 0
        high_confidence_correct = 0
        high_confidence_total = 0
        
        monthly_stats = {}
        
        for _, match in season_matches.iterrows():
            # ทำนาย
            pred = self.predictor.predict_match_ultra(
                match['home_team'], 
                match['away_team'],
                match['date']
            )
            
            if not pred:
                continue
            
            # ผลจริง
            actual = self.get_actual_result(match)
            is_correct = pred['prediction'] == actual
            
            if is_correct:
                correct_predictions += 1
                
            if pred['confidence'] > 0.6:
                high_confidence_total += 1
                if is_correct:
                    high_confidence_correct += 1
            
            # สถิติรายเดือน
            month = pd.to_datetime(match['date']).strftime('%Y-%m')
            if month not in monthly_stats:
                monthly_stats[month] = {'correct': 0, 'total': 0}
            
            monthly_stats[month]['total'] += 1
            if is_correct:
                monthly_stats[month]['correct'] += 1
            
            # บันทึก
            self.predictions_log.append({
                'date': match['date'],
                'match': f"{match['home_team']} vs {match['away_team']}",
                'prediction': pred['prediction'],
                'actual': actual,
                'confidence': pred['confidence'],
                'correct': is_correct
            })
        
        # สรุปผล
        total_games = len(season_matches)
        overall_accuracy = correct_predictions / total_games if total_games > 0 else 0
        high_conf_accuracy = high_confidence_correct / high_confidence_total if high_confidence_total > 0 else 0
        
        print(f"🎯 สรุปผลการทำนายฤดูกาล:")
        print(f"   ความแม่นยำโดยรวม: {correct_predictions}/{total_games} = {overall_accuracy:.1%}")
        print(f"   ความแม่นยำเมื่อมั่นใจสูง: {high_confidence_correct}/{high_confidence_total} = {high_conf_accuracy:.1%}")
        
        print(f"\n📈 สถิติรายเดือน:")
        for month, stats in sorted(monthly_stats.items()):
            accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
            print(f"   {month}: {stats['correct']:2d}/{stats['total']:2d} = {accuracy:.1%}")
        
        return self.predictions_log
    
    def get_actual_result(self, match):
        """แปลงผลจริงเป็น label"""
        if match['home_goals'] > match['away_goals']:
            return 'Home Win'
        elif match['home_goals'] == match['away_goals']:
            return 'Draw'
        else:
            return 'Away Win'

# ใช้งาน
tracker = SeasonTracker()
start_date = datetime(2024, 8, 1)
end_date = datetime(2024, 12, 31)

season_log = tracker.track_season_predictions(start_date, end_date)
```

## 🏆 Use Case 4: Tournament Bracket Prediction

### การทำนายแบรกเก็ตทัวร์นาเมนต์

```python
class TournamentPredictor:
    def __init__(self):
        self.predictor = UltraAdvancedPredictor()
        
    def predict_knockout_stage(self, teams, rounds=['Round of 16', 'Quarter Finals', 'Semi Finals', 'Final']):
        """ทำนายระยะน็อคเอาท์"""
        
        # เทรนโมเดล
        data = self.predictor.load_premier_league_data()
        self.predictor.train_ensemble_models(data)
        
        current_teams = teams.copy()
        
        for round_name in rounds:
            print(f"🏆 {round_name}")
            print("="*50)
            
            next_round_teams = []
            
            # จับคู่ทีม
            for i in range(0, len(current_teams), 2):
                if i + 1 < len(current_teams):
                    team1 = current_teams[i]
                    team2 = current_teams[i + 1]
                    
                    # ทำนาย (สมมติเป็นสนามกลาง)
                    pred1 = self.predictor.predict_match_ultra(team1, team2)
                    pred2 = self.predictor.predict_match_ultra(team2, team1)
                    
                    if pred1 and pred2:
                        # เฉลี่ยความน่าจะเป็น
                        team1_prob = (pred1['probabilities']['Home Win'] + pred2['probabilities']['Away Win']) / 2
                        team2_prob = (pred1['probabilities']['Away Win'] + pred2['probabilities']['Home Win']) / 2
                        
                        winner = team1 if team1_prob > team2_prob else team2
                        confidence = max(team1_prob, team2_prob)
                        
                        print(f"   {team1} vs {team2}")
                        print(f"   ผู้ชนะ: {winner} ({confidence:.1%})")
                        print(f"   โอกาส: {team1} {team1_prob:.1%} - {team2} {team2_prob:.1%}")
                        print()
                        
                        next_round_teams.append(winner)
            
            current_teams = next_round_teams
            
            if len(current_teams) <= 1:
                break
        
        if current_teams:
            print(f"🏆 แชมป์ที่คาดการณ์: {current_teams[0]}")
        
        return current_teams

# ใช้งาน
tournament = TournamentPredictor()

# Top 16 Premier League teams
top_16_teams = [
    "Manchester City", "Arsenal", "Liverpool", "Chelsea",
    "Manchester United", "Tottenham", "Newcastle", "Brighton",
    "Aston Villa", "West Ham", "Crystal Palace", "Fulham",
    "Brentford", "Wolves", "Everton", "Nottingham Forest"
]

champion = tournament.predict_knockout_stage(top_16_teams)
```

## 📱 Use Case 5: Real-time Match Monitoring

### การติดตามเกมแบบ Real-time

```python
import time
from datetime import datetime

class RealTimeMonitor:
    def __init__(self):
        self.predictor = UltraAdvancedPredictor()
        self.active_predictions = {}
        
    def setup_monitoring(self):
        """ตั้งค่าการติดตาม"""
        data = self.predictor.load_premier_league_data()
        self.predictor.train_ensemble_models(data)
        print("✅ ระบบติดตามพร้อมใช้งาน")
        
    def add_match_to_monitor(self, home_team, away_team, match_time):
        """เพิ่มเกมที่ต้องการติดตาม"""
        match_id = f"{home_team}_vs_{away_team}_{match_time}"
        
        prediction = self.predictor.predict_match_ultra(home_team, away_team)
        
        if prediction:
            self.active_predictions[match_id] = {
                'home_team': home_team,
                'away_team': away_team,
                'match_time': match_time,
                'prediction': prediction,
                'status': 'SCHEDULED'
            }
            
            print(f"📅 เพิ่มการติดตาม: {home_team} vs {away_team}")
            print(f"   ทำนาย: {prediction['prediction']} ({prediction['confidence']:.1%})")
            
    def monitor_matches(self):
        """ติดตามเกมที่กำลังแข่ง"""
        print("🔴 เริ่มการติดตามแบบ Real-time")
        print("="*60)
        
        while self.active_predictions:
            current_time = datetime.now()
            
            for match_id, match_info in list(self.active_predictions.items()):
                match_time = datetime.strptime(match_info['match_time'], '%Y-%m-%d %H:%M')
                
                # ตรวจสอบสถานะเกม
                if current_time >= match_time and match_info['status'] == 'SCHEDULED':
                    print(f"⚽ เกมเริ่มแล้ว: {match_info['home_team']} vs {match_info['away_team']}")
                    print(f"   การทำนายของเรา: {match_info['prediction']['prediction']}")
                    print(f"   ความมั่นใจ: {match_info['prediction']['confidence']:.1%}")
                    
                    match_info['status'] = 'LIVE'
                    
                elif current_time >= match_time + timedelta(hours=2) and match_info['status'] == 'LIVE':
                    print(f"🏁 เกมจบแล้ว: {match_info['home_team']} vs {match_info['away_team']}")
                    print("   รอผลการแข่งขันจริง...")
                    
                    match_info['status'] = 'FINISHED'
                    # ในการใช้งานจริง จะดึงผลจาก API
                    
            time.sleep(60)  # ตรวจสอบทุกนาที
            
    def update_match_result(self, match_id, home_goals, away_goals):
        """อัปเดตผลการแข่งขันจริง"""
        if match_id in self.active_predictions:
            match_info = self.active_predictions[match_id]
            
            # ผลจริง
            if home_goals > away_goals:
                actual_result = 'Home Win'
            elif home_goals == away_goals:
                actual_result = 'Draw'
            else:
                actual_result = 'Away Win'
            
            predicted_result = match_info['prediction']['prediction']
            is_correct = predicted_result == actual_result
            
            print(f"📊 ผลการแข่งขัน: {match_info['home_team']} {home_goals}-{away_goals} {match_info['away_team']}")
            print(f"   ทำนาย: {predicted_result}")
            print(f"   ผลจริง: {actual_result}")
            print(f"   ผลลัพธ์: {'✅ ถูก' if is_correct else '❌ ผิด'}")
            print()
            
            # ลบออกจากการติดตาม
            del self.active_predictions[match_id]

# ใช้งาน
monitor = RealTimeMonitor()
monitor.setup_monitoring()

# เพิ่มเกมที่ต้องการติดตาม
monitor.add_match_to_monitor("Arsenal", "Chelsea", "2024-12-15 15:00")
monitor.add_match_to_monitor("Manchester City", "Liverpool", "2024-12-15 17:30")

# เริ่มการติดตาม
# monitor.monitor_matches()  # รันในลูปจริง
```

## 🎯 Use Case 6: Custom Strategy Development

### การพัฒนากลยุทธ์เฉพาะ

```python
class CustomStrategy:
    def __init__(self):
        self.predictor = UltraAdvancedPredictor()
        self.strategy_results = []
        
    def conservative_strategy(self, matches):
        """กลยุทธ์อนุรักษ์นิยม - เลือกเฉพาะเกมที่มั่นใจสูง"""
        print("🛡️ กลยุทธ์อนุรักษ์นิยม")
        print("="*50)
        
        data = self.predictor.load_premier_league_data()
        self.predictor.train_ensemble_models(data)
        
        selected_matches = []
        
        for home, away in matches:
            pred = self.predictor.predict_match_ultra(home, away)
            
            if pred and pred['confidence'] > 0.7 and pred['model_agreement'] > 0.8:
                selected_matches.append({
                    'match': f"{home} vs {away}",
                    'prediction': pred['prediction'],
                    'confidence': pred['confidence'],
                    'agreement': pred['model_agreement']
                })
        
        print(f"📊 เลือกได้ {len(selected_matches)} เกมจาก {len(matches)} เกม")
        
        for match in selected_matches:
            print(f"✅ {match['match']}")
            print(f"   ทำนาย: {match['prediction']}")
            print(f"   ความมั่นใจ: {match['confidence']:.1%}")
            print(f"   ความเห็นตรงกัน: {match['agreement']:.1%}")
            print()
        
        return selected_matches
    
    def aggressive_strategy(self, matches):
        """กลยุทธ์ก้าวร้าว - รวมทุกเกมที่มีโอกาส"""
        print("⚡ กลยุทธ์ก้าวร้าว")
        print("="*50)
        
        data = self.predictor.load_premier_league_data()
        self.predictor.train_ensemble_models(data)
        
        all_predictions = []
        
        for home, away in matches:
            pred = self.predictor.predict_match_ultra(home, away)
            
            if pred and pred['confidence'] > 0.5:
                risk_level = "สูง" if pred['confidence'] < 0.6 else "ปานกลาง" if pred['confidence'] < 0.7 else "ต่ำ"
                
                all_predictions.append({
                    'match': f"{home} vs {away}",
                    'prediction': pred['prediction'],
                    'confidence': pred['confidence'],
                    'risk': risk_level
                })
        
        # เรียงตามความมั่นใจ
        all_predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        print(f"📊 รวม {len(all_predictions)} เกมทั้งหมด")
        
        for pred in all_predictions:
            risk_emoji = "🔥" if pred['risk'] == "ต่ำ" else "⚖️" if pred['risk'] == "ปานกลาง" else "⚠️"
            print(f"{risk_emoji} {pred['match']}")
            print(f"   ทำนาย: {pred['prediction']} ({pred['confidence']:.1%})")
            print(f"   ความเสี่ยง: {pred['risk']}")
            print()
        
        return all_predictions

# ใช้งาน
strategy = CustomStrategy()

upcoming_matches = [
    ("Arsenal", "Chelsea"),
    ("Manchester City", "Liverpool"),
    ("Manchester United", "Tottenham"),
    ("Newcastle", "Brighton"),
    ("Aston Villa", "West Ham"),
    ("Crystal Palace", "Fulham"),
    ("Brentford", "Wolves"),
    ("Everton", "Southampton")
]

# ทดสอบกลยุทธ์ต่างๆ
conservative_picks = strategy.conservative_strategy(upcoming_matches)
aggressive_picks = strategy.aggressive_strategy(upcoming_matches)
```

---

**🎯 ตัวอย่างเหล่านี้แสดงให้เห็นความยืดหยุ่นและประสิทธิภาพของระบบ Ultra Advanced Football Predictor ในการใช้งานจริง!** ⚽🚀
