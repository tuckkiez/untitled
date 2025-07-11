#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ระบบทำนายฟุตบอลแบบ Interactive
ใช้ข้อมูลจริงจาก API และให้ผู้ใช้เลือกทีมเพื่อทำนาย
"""

from real_data_example import RealDataPredictor
from football_predictor import FootballPredictor
import pandas as pd

class InteractiveFootballPredictor:
    def __init__(self):
        self.api_token = "052fd4885cf943ad859c89cef542e2e5"
        self.predictor = None
        self.historical_data = None
        self.teams = []
        
    def load_data(self):
        """โหลดข้อมูลจาก API"""
        print("🔄 กำลังโหลดข้อมูลจาก football-data.org...")
        
        real_predictor = RealDataPredictor(api_key=self.api_token)
        
        # ดึงข้อมูลฤดูกาล 2024
        self.historical_data = real_predictor.get_premier_league_data(season=2024)
        
        if self.historical_data is None:
            print("❌ ไม่สามารถโหลดข้อมูลได้")
            return False
        
        # ดึงรายชื่อทีม
        self.teams = sorted(list(set(
            self.historical_data['home_team'].tolist() + 
            self.historical_data['away_team'].tolist()
        )))
        
        print(f"✅ โหลดข้อมูลสำเร็จ: {len(self.historical_data)} เกม")
        print(f"📊 จำนวนทีม: {len(self.teams)} ทีม")
        
        return True
    
    def train_model(self):
        """เทรนโมเดล"""
        print("\n🤖 กำลังเทรนโมเดล...")
        self.predictor = FootballPredictor()
        
        if not self.predictor.train(self.historical_data):
            print("❌ ไม่สามารถเทรนโมเดลได้")
            return False
        
        print("✅ เทรนโมเดลสำเร็จ")
        return True
    
    def show_teams(self):
        """แสดงรายชื่อทีมทั้งหมด"""
        print("\n📋 รายชื่อทีมในพรีเมียร์ลีก:")
        print("=" * 50)
        
        for i, team in enumerate(self.teams, 1):
            # ลบ "FC" ออกเพื่อให้อ่านง่าย
            display_name = team.replace(" FC", "").replace(" United FC", " United")
            print(f"{i:2d}. {display_name}")
    
    def get_team_choice(self, prompt):
        """ให้ผู้ใช้เลือกทีม"""
        while True:
            try:
                print(f"\n{prompt}")
                choice = input("กรุณาใส่หมายเลขทีม (หรือพิมพ์ 'list' เพื่อดูรายชื่อ): ").strip()
                
                if choice.lower() == 'list':
                    self.show_teams()
                    continue
                
                team_index = int(choice) - 1
                
                if 0 <= team_index < len(self.teams):
                    return self.teams[team_index]
                else:
                    print(f"❌ กรุณาใส่หมายเลข 1-{len(self.teams)}")
                    
            except ValueError:
                print("❌ กรุณาใส่หมายเลขที่ถูกต้อง")
    
    def predict_match(self, home_team, away_team):
        """ทำนายผลการแข่งขัน"""
        result = self.predictor.predict_match(home_team, away_team, self.historical_data)
        
        if not result:
            print("❌ ไม่สามารถทำนายได้")
            return
        
        # แสดงผลการทำนาย
        print("\n" + "="*60)
        print(f"⚽ การทำนาย: {home_team.replace(' FC', '')} vs {away_team.replace(' FC', '')}")
        print("="*60)
        
        # แสดงการทำนาย
        prediction_emoji = {
            'Home Win': '🏠',
            'Away Win': '✈️',
            'Draw': '🤝'
        }
        
        print(f"\n🎯 การทำนาย: {prediction_emoji.get(result['prediction'], '⚽')} {result['prediction']}")
        print(f"🎲 ความมั่นใจ: {result['confidence']:.3f} ({result['confidence']*100:.1f}%)")
        
        # แสดงความน่าจะเป็น
        print(f"\n📊 ความน่าจะเป็นของแต่ละผล:")
        for outcome, prob in result['probabilities'].items():
            emoji = prediction_emoji.get(outcome, '⚽')
            bar_length = int(prob * 20)  # สร้าง progress bar
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"   {emoji} {outcome:10s}: {bar} {prob:.3f} ({prob*100:.1f}%)")
        
        # แสดงสถิติทีม
        self.show_team_stats(home_team, away_team)
    
    def show_team_stats(self, home_team, away_team):
        """แสดงสถิติของทั้งสองทีม"""
        print(f"\n📈 สถิติการเจอกันล่าสุด:")
        
        # หาเกมที่ทั้งสองทีมเจอกัน
        head_to_head = self.historical_data[
            ((self.historical_data['home_team'] == home_team) & 
             (self.historical_data['away_team'] == away_team)) |
            ((self.historical_data['home_team'] == away_team) & 
             (self.historical_data['away_team'] == home_team))
        ].tail(5)
        
        if len(head_to_head) > 0:
            print(f"   เกมล่าสุด {len(head_to_head)} นัด:")
            for _, match in head_to_head.iterrows():
                date = match['date'].strftime('%Y-%m-%d')
                home = match['home_team'].replace(' FC', '')
                away = match['away_team'].replace(' FC', '')
                score = f"{match['home_goals']}-{match['away_goals']}"
                print(f"   📅 {date}: {home} {score} {away}")
        else:
            print("   ไม่มีข้อมูลการเจอกันในฤดูกาลนี้")
    
    def run_interactive_session(self):
        """รันเซสชันแบบ interactive"""
        print("🏆 ยินดีต้อนรับสู่ระบบทำนายผลฟุตบอลพรีเมียร์ลีก!")
        print("📊 ใช้ข้อมูลจริงจาก football-data.org")
        
        # โหลดข้อมูลและเทรนโมเดล
        if not self.load_data():
            return
        
        if not self.train_model():
            return
        
        # แสดงรายชื่อทีม
        self.show_teams()
        
        while True:
            try:
                print("\n" + "="*60)
                print("🎮 เลือกการทำนาย")
                print("="*60)
                
                # เลือกทีมเหย้า
                home_team = self.get_team_choice("🏠 เลือกทีมเหย้า:")
                
                # เลือกทีมเยือน
                while True:
                    away_team = self.get_team_choice("✈️  เลือกทีมเยือน:")
                    if away_team != home_team:
                        break
                    print("❌ ไม่สามารถเลือกทีมเดียวกันได้")
                
                # ทำนาย
                self.predict_match(home_team, away_team)
                
                # ถามว่าต้องการทำนายต่อหรือไม่
                print("\n" + "="*60)
                continue_choice = input("🔄 ต้องการทำนายเกมอื่นหรือไม่? (y/n): ").strip().lower()
                
                if continue_choice not in ['y', 'yes', 'ใช่']:
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 ขอบคุณที่ใช้บริการ!")
                break
            except Exception as e:
                print(f"\n❌ เกิดข้อผิดพลาด: {e}")
                continue
        
        print("\n🏆 ขอบคุณที่ใช้ระบบทำนายผลฟุตบอล!")
        print("📊 ความแม่นยำของระบบอยู่ที่ประมาณ 46% จากการ backtest")
        print("⚠️  หมายเหตุ: ใช้เพื่อความบันเทิงเท่านั้น")

def main():
    predictor = InteractiveFootballPredictor()
    predictor.run_interactive_session()

if __name__ == "__main__":
    main()
