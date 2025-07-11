import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class FootballPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.feature_columns = []
        self.is_trained = False
        
    def calculate_team_stats(self, matches_df, team_name, last_n_games=10):
        """คำนวณสถิติของทีมจากเกมล่าสุด"""
        # กรองเกมของทีม
        team_matches = matches_df[
            (matches_df['home_team'] == team_name) | 
            (matches_df['away_team'] == team_name)
        ].tail(last_n_games)
        
        if len(team_matches) == 0:
            return self._default_stats()
            
        stats = {}
        
        # คำนวณสถิติพื้นฐาน
        wins = 0
        draws = 0
        losses = 0
        goals_for = 0
        goals_against = 0
        
        for _, match in team_matches.iterrows():
            if match['home_team'] == team_name:
                goals_for += match['home_goals']
                goals_against += match['away_goals']
                if match['home_goals'] > match['away_goals']:
                    wins += 1
                elif match['home_goals'] == match['away_goals']:
                    draws += 1
                else:
                    losses += 1
            else:
                goals_for += match['away_goals']
                goals_against += match['home_goals']
                if match['away_goals'] > match['home_goals']:
                    wins += 1
                elif match['away_goals'] == match['home_goals']:
                    draws += 1
                else:
                    losses += 1
        
        total_games = len(team_matches)
        stats['win_rate'] = wins / total_games if total_games > 0 else 0
        stats['draw_rate'] = draws / total_games if total_games > 0 else 0
        stats['loss_rate'] = losses / total_games if total_games > 0 else 0
        stats['avg_goals_for'] = goals_for / total_games if total_games > 0 else 0
        stats['avg_goals_against'] = goals_against / total_games if total_games > 0 else 0
        stats['goal_difference'] = stats['avg_goals_for'] - stats['avg_goals_against']
        
        return stats
    
    def _default_stats(self):
        """สถิติเริ่มต้นสำหรับทีมใหม่"""
        return {
            'win_rate': 0.33,
            'draw_rate': 0.33,
            'loss_rate': 0.34,
            'avg_goals_for': 1.0,
            'avg_goals_against': 1.0,
            'goal_difference': 0.0
        }
    
    def prepare_features(self, matches_df):
        """เตรียมข้อมูล features สำหรับการเทรน"""
        features = []
        labels = []
        
        for idx, match in matches_df.iterrows():
            # คำนวณสถิติของทั้งสองทีม
            home_stats = self.calculate_team_stats(
                matches_df.iloc[:idx], match['home_team']
            )
            away_stats = self.calculate_team_stats(
                matches_df.iloc[:idx], match['away_team']
            )
            
            # สร้าง feature vector
            feature_row = []
            for stat_name in ['win_rate', 'draw_rate', 'loss_rate', 
                            'avg_goals_for', 'avg_goals_against', 'goal_difference']:
                feature_row.append(home_stats[stat_name])
                feature_row.append(away_stats[stat_name])
            
            # เพิ่ม relative features
            feature_row.append(home_stats['win_rate'] - away_stats['win_rate'])
            feature_row.append(home_stats['goal_difference'] - away_stats['goal_difference'])
            feature_row.append(1)  # home advantage
            
            features.append(feature_row)
            
            # กำหนด label (0=away win, 1=draw, 2=home win)
            if match['home_goals'] > match['away_goals']:
                labels.append(2)  # home win
            elif match['home_goals'] < match['away_goals']:
                labels.append(0)  # away win
            else:
                labels.append(1)  # draw
        
        self.feature_columns = [
            'home_win_rate', 'away_win_rate',
            'home_draw_rate', 'away_draw_rate',
            'home_loss_rate', 'away_loss_rate',
            'home_avg_goals_for', 'away_avg_goals_for',
            'home_avg_goals_against', 'away_avg_goals_against',
            'home_goal_diff', 'away_goal_diff',
            'win_rate_diff', 'goal_diff_diff', 'home_advantage'
        ]
        
        return np.array(features), np.array(labels)
    
    def train(self, matches_df):
        """เทรนโมเดล"""
        print("กำลังเตรียมข้อมูลสำหรับการเทรน...")
        X, y = self.prepare_features(matches_df)
        
        if len(X) < 50:
            print("ข้อมูลไม่เพียงพอสำหรับการเทรน (ต้องการอย่างน้อย 50 เกม)")
            return False
        
        print(f"จำนวนเกมที่ใช้เทรน: {len(X)}")
        
        # แบ่งข้อมูลสำหรับ validation
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # เทรนโมเดล
        self.model.fit(X_train, y_train)
        
        # ทดสอบความแม่นยำ
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"ความแม่นยำของโมเดล: {accuracy:.3f}")
        print("\nรายงานผลการทำนาย:")
        print(classification_report(y_test, y_pred, 
                                  target_names=['Away Win', 'Draw', 'Home Win']))
        
        self.is_trained = True
        return True
    
    def predict_match(self, home_team, away_team, matches_df):
        """ทำนายผลการแข่งขัน"""
        if not self.is_trained:
            print("โมเดลยังไม่ได้เทรน กรุณาเทรนโมเดลก่อน")
            return None
        
        # คำนวณสถิติปัจจุบันของทั้งสองทีม
        home_stats = self.calculate_team_stats(matches_df, home_team)
        away_stats = self.calculate_team_stats(matches_df, away_team)
        
        # สร้าง feature vector
        feature_row = []
        for stat_name in ['win_rate', 'draw_rate', 'loss_rate', 
                        'avg_goals_for', 'avg_goals_against', 'goal_difference']:
            feature_row.append(home_stats[stat_name])
            feature_row.append(away_stats[stat_name])
        
        feature_row.append(home_stats['win_rate'] - away_stats['win_rate'])
        feature_row.append(home_stats['goal_difference'] - away_stats['goal_difference'])
        feature_row.append(1)  # home advantage
        
        # ทำนาย
        prediction = self.model.predict([feature_row])[0]
        probabilities = self.model.predict_proba([feature_row])[0]
        
        result_map = {0: 'Away Win', 1: 'Draw', 2: 'Home Win'}
        
        return {
            'prediction': result_map[prediction],
            'probabilities': {
                'Away Win': probabilities[0],
                'Draw': probabilities[1],
                'Home Win': probabilities[2]
            },
            'confidence': max(probabilities)
        }
    
    def backtest(self, matches_df, test_period_games=50):
        """ทดสอบย้อนหลังความแม่นยำของโมเดล"""
        if len(matches_df) < test_period_games + 100:
            print("ข้อมูลไม่เพียงพอสำหรับ backtest")
            return None
        
        # แบ่งข้อมูลสำหรับ backtest
        train_data = matches_df.iloc[:-test_period_games]
        test_data = matches_df.iloc[-test_period_games:]
        
        # เทรนโมเดลด้วยข้อมูลเก่า
        print("กำลังเทรนโมเดลสำหรับ backtest...")
        temp_model = FootballPredictor()
        temp_model.train(train_data)
        
        # ทดสอบกับข้อมูลใหม่
        correct_predictions = 0
        total_predictions = 0
        results = []
        
        print("กำลังทำ backtest...")
        for idx, match in test_data.iterrows():
            prediction_result = temp_model.predict_match(
                match['home_team'], match['away_team'], train_data
            )
            
            if prediction_result:
                # กำหนดผลจริง
                if match['home_goals'] > match['away_goals']:
                    actual = 'Home Win'
                elif match['home_goals'] < match['away_goals']:
                    actual = 'Away Win'
                else:
                    actual = 'Draw'
                
                predicted = prediction_result['prediction']
                is_correct = (predicted == actual)
                
                if is_correct:
                    correct_predictions += 1
                total_predictions += 1
                
                results.append({
                    'home_team': match['home_team'],
                    'away_team': match['away_team'],
                    'actual': actual,
                    'predicted': predicted,
                    'correct': is_correct,
                    'confidence': prediction_result['confidence']
                })
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        
        print(f"\nผล Backtest:")
        print(f"จำนวนเกมที่ทดสอบ: {total_predictions}")
        print(f"ทำนายถูก: {correct_predictions}")
        print(f"ความแม่นยำ: {accuracy:.3f} ({accuracy*100:.1f}%)")
        
        return {
            'accuracy': accuracy,
            'total_games': total_predictions,
            'correct_predictions': correct_predictions,
            'results': results
        }

# ฟังก์ชันสำหรับโหลดข้อมูลตัวอย่าง
def create_sample_data():
    """สร้างข้อมูลตัวอย่างสำหรับทดสอบ"""
    teams = ['Arsenal', 'Chelsea', 'Liverpool', 'Man City', 'Man United', 
             'Tottenham', 'Newcastle', 'Brighton', 'West Ham', 'Aston Villa']
    
    matches = []
    for i in range(200):  # สร้าง 200 เกม
        home_team = np.random.choice(teams)
        away_team = np.random.choice([t for t in teams if t != home_team])
        
        # สร้างผลการแข่งขันแบบสมจริง
        home_strength = np.random.normal(1.5, 0.5)
        away_strength = np.random.normal(1.2, 0.5)
        
        home_goals = max(0, int(np.random.poisson(home_strength)))
        away_goals = max(0, int(np.random.poisson(away_strength)))
        
        matches.append({
            'date': f"2024-{(i//30)+1:02d}-{(i%30)+1:02d}",
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': home_goals,
            'away_goals': away_goals
        })
    
    return pd.DataFrame(matches)

if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    print("=== ระบบทำนายผลฟุตบอล ===")
    
    # สร้างข้อมูลตัวอย่าง
    print("กำลังสร้างข้อมูลตัวอย่าง...")
    matches_df = create_sample_data()
    
    # สร้างและเทรนโมเดล
    predictor = FootballPredictor()
    predictor.train(matches_df)
    
    # ทำนายเกมใหม่
    print("\n=== การทำนาย ===")
    result = predictor.predict_match('Arsenal', 'Chelsea', matches_df)
    if result:
        print(f"Arsenal vs Chelsea")
        print(f"การทำนาย: {result['prediction']}")
        print(f"ความมั่นใจ: {result['confidence']:.3f}")
        print("ความน่าจะเป็น:")
        for outcome, prob in result['probabilities'].items():
            print(f"  {outcome}: {prob:.3f} ({prob*100:.1f}%)")
    
    # ทำ backtest
    print("\n=== Backtest ===")
    backtest_result = predictor.backtest(matches_df, test_period_games=30)
