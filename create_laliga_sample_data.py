#!/usr/bin/env python3
"""
🇪🇸 สร้างข้อมูล La Liga สำเร็จรูปคุณภาพสูง
ใกล้เคียงข้อมูลจริงมากที่สุด (จนกว่าจะได้ API Key)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_realistic_laliga_data():
    """สร้างข้อมูล La Liga ที่ใกล้เคียงความจริง"""
    print("🇪🇸 กำลังสร้างข้อมูล La Liga คุณภาพสูง...")
    
    # ทีมใน La Liga 2024-25 (จริง)
    teams_data = {
        'Real Madrid': {'strength': 2.3, 'home_bonus': 0.4, 'form': 0.9},
        'FC Barcelona': {'strength': 2.2, 'home_bonus': 0.4, 'form': 0.8},
        'Atletico Madrid': {'strength': 1.9, 'home_bonus': 0.3, 'form': 0.85},
        'Athletic Bilbao': {'strength': 1.6, 'home_bonus': 0.5, 'form': 0.75},
        'Real Sociedad': {'strength': 1.5, 'home_bonus': 0.3, 'form': 0.7},
        'Real Betis': {'strength': 1.4, 'home_bonus': 0.3, 'form': 0.72},
        'Villarreal CF': {'strength': 1.4, 'home_bonus': 0.2, 'form': 0.68},
        'Valencia CF': {'strength': 1.2, 'home_bonus': 0.3, 'form': 0.6},
        'Sevilla FC': {'strength': 1.3, 'home_bonus': 0.2, 'form': 0.65},
        'RC Celta': {'strength': 1.1, 'home_bonus': 0.2, 'form': 0.6},
        'CA Osasuna': {'strength': 1.0, 'home_bonus': 0.4, 'form': 0.7},
        'Getafe CF': {'strength': 0.9, 'home_bonus': 0.3, 'form': 0.55},
        'UD Las Palmas': {'strength': 0.9, 'home_bonus': 0.2, 'form': 0.5},
        'Girona FC': {'strength': 1.2, 'home_bonus': 0.2, 'form': 0.75},
        'Rayo Vallecano': {'strength': 1.0, 'home_bonus': 0.3, 'form': 0.6},
        'RCD Espanyol': {'strength': 0.8, 'home_bonus': 0.2, 'form': 0.45},
        'Deportivo Alaves': {'strength': 0.8, 'home_bonus': 0.2, 'form': 0.5},
        'Real Valladolid': {'strength': 0.7, 'home_bonus': 0.2, 'form': 0.4},
        'CD Leganes': {'strength': 0.7, 'home_bonus': 0.2, 'form': 0.45},
        'RCD Mallorca': {'strength': 0.9, 'home_bonus': 0.2, 'form': 0.55}
    }
    
    teams = list(teams_data.keys())
    matches = []
    
    # สร้างข้อมูล 300 เกม (ใกล้เคียงจริง)
    print("⚽ กำลังสร้างการแข่งขัน...")
    
    for i in range(300):
        # เลือกทีม
        home_team = random.choice(teams)
        away_team = random.choice([t for t in teams if t != home_team])
        
        # ข้อมูลทีม
        home_data = teams_data[home_team]
        away_data = teams_data[away_team]
        
        # คำนวณความแข็งแกร่ง
        home_strength = home_data['strength'] + home_data['home_bonus']
        away_strength = away_data['strength']
        
        # ปรับตามฟอร์ม
        home_strength *= home_data['form']
        away_strength *= away_data['form']
        
        # เพิ่มความสุ่ม
        home_strength += random.uniform(-0.3, 0.3)
        away_strength += random.uniform(-0.3, 0.3)
        
        # คำนวณประตู
        home_goals = max(0, int(np.random.poisson(home_strength)))
        away_goals = max(0, int(np.random.poisson(away_strength)))
        
        # ปรับให้เหมือนจริง (ลดเกมประตูเยอะ)
        if home_goals + away_goals > 5:
            if random.random() < 0.7:  # 70% ลดประตู
                home_goals = min(home_goals, 3)
                away_goals = min(away_goals, 2)
        
        # สร้างวันที่ (ย้อนหลัง 4 เดือน)
        days_ago = random.randint(1, 120)
        match_date = datetime.now() - timedelta(days=days_ago)
        
        # เพิ่มข้อมูลเพิ่มเติม
        matchday = random.randint(1, 38)
        
        matches.append({
            'date': match_date.strftime('%Y-%m-%d'),
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': home_goals,
            'away_goals': away_goals,
            'matchday': matchday,
            'season': 2024
        })
    
    # สร้าง DataFrame
    df = pd.DataFrame(matches)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"✅ สร้างข้อมูล La Liga สำเร็จ: {len(df)} เกม")
    
    return df

def analyze_realistic_data(df):
    """วิเคราะห์ข้อมูลที่สร้างขึ้น"""
    print(f"\n📊 การวิเคราะห์ข้อมูล La Liga:")
    print("=" * 40)
    
    print(f"📈 จำนวนเกม: {len(df)}")
    print(f"📅 ช่วงเวลา: {df['date'].min().strftime('%Y-%m-%d')} ถึง {df['date'].max().strftime('%Y-%m-%d')}")
    
    # ทีมที่มีข้อมูล
    all_teams = set(df['home_team'].unique()) | set(df['away_team'].unique())
    print(f"🏆 จำนวนทีม: {len(all_teams)}")
    
    # สถิติประตู
    total_goals = df['home_goals'].sum() + df['away_goals'].sum()
    avg_goals = total_goals / len(df)
    print(f"⚽ ประตูเฉลี่ย: {avg_goals:.2f} ต่อเกม")
    
    # ผลการแข่งขัน
    home_wins = len(df[df['home_goals'] > df['away_goals']])
    draws = len(df[df['home_goals'] == df['away_goals']])
    away_wins = len(df[df['home_goals'] < df['away_goals']])
    
    print(f"🏠 เจ้าบ้านชนะ: {home_wins} ({home_wins/len(df)*100:.1f}%)")
    print(f"🤝 เสมอ: {draws} ({draws/len(df)*100:.1f}%)")
    print(f"✈️ ทีมเยือนชนะ: {away_wins} ({away_wins/len(df)*100:.1f}%)")
    
    # สถิติทีม
    team_stats = {}
    for _, row in df.iterrows():
        # Home team
        if row['home_team'] not in team_stats:
            team_stats[row['home_team']] = {'games': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
        
        team_stats[row['home_team']]['games'] += 1
        team_stats[row['home_team']]['goals_for'] += row['home_goals']
        team_stats[row['home_team']]['goals_against'] += row['away_goals']
        
        if row['home_goals'] > row['away_goals']:
            team_stats[row['home_team']]['wins'] += 1
        elif row['home_goals'] == row['away_goals']:
            team_stats[row['home_team']]['draws'] += 1
        else:
            team_stats[row['home_team']]['losses'] += 1
        
        # Away team
        if row['away_team'] not in team_stats:
            team_stats[row['away_team']] = {'games': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
        
        team_stats[row['away_team']]['games'] += 1
        team_stats[row['away_team']]['goals_for'] += row['away_goals']
        team_stats[row['away_team']]['goals_against'] += row['home_goals']
        
        if row['away_goals'] > row['home_goals']:
            team_stats[row['away_team']]['wins'] += 1
        elif row['away_goals'] == row['home_goals']:
            team_stats[row['away_team']]['draws'] += 1
        else:
            team_stats[row['away_team']]['losses'] += 1
    
    # คำนวณคะแนน
    for team in team_stats:
        team_stats[team]['points'] = (team_stats[team]['wins'] * 3 + team_stats[team]['draws'])
        team_stats[team]['ppg'] = team_stats[team]['points'] / max(1, team_stats[team]['games'])
    
    # Top 5 ทีม
    top_teams = sorted(team_stats.items(), key=lambda x: x[1]['points'], reverse=True)[:5]
    print(f"\n🏆 Top 5 ทีม (คะแนน):")
    for i, (team, stats) in enumerate(top_teams, 1):
        print(f"   {i}. {team}: {stats['points']} คะแนน ({stats['games']} เกม)")

def create_teams_info():
    """สร้างข้อมูลทีม"""
    teams_info = [
        {'name': 'Real Madrid', 'short_name': 'RMA', 'founded': 1902, 'venue': 'Santiago Bernabéu'},
        {'name': 'FC Barcelona', 'short_name': 'BAR', 'founded': 1899, 'venue': 'Camp Nou'},
        {'name': 'Atletico Madrid', 'short_name': 'ATM', 'founded': 1903, 'venue': 'Wanda Metropolitano'},
        {'name': 'Athletic Bilbao', 'short_name': 'ATH', 'founded': 1898, 'venue': 'San Mamés'},
        {'name': 'Real Sociedad', 'short_name': 'RSO', 'founded': 1909, 'venue': 'Reale Arena'},
        {'name': 'Real Betis', 'short_name': 'BET', 'founded': 1907, 'venue': 'Benito Villamarín'},
        {'name': 'Villarreal CF', 'short_name': 'VIL', 'founded': 1923, 'venue': 'Estadio de la Cerámica'},
        {'name': 'Valencia CF', 'short_name': 'VAL', 'founded': 1919, 'venue': 'Mestalla'},
        {'name': 'Sevilla FC', 'short_name': 'SEV', 'founded': 1890, 'venue': 'Ramón Sánchez Pizjuán'},
        {'name': 'RC Celta', 'short_name': 'CEL', 'founded': 1923, 'venue': 'Balaídos'},
        {'name': 'CA Osasuna', 'short_name': 'OSA', 'founded': 1920, 'venue': 'El Sadar'},
        {'name': 'Getafe CF', 'short_name': 'GET', 'founded': 1946, 'venue': 'Coliseum Alfonso Pérez'},
        {'name': 'UD Las Palmas', 'short_name': 'LPA', 'founded': 1949, 'venue': 'Estadio Gran Canaria'},
        {'name': 'Girona FC', 'short_name': 'GIR', 'founded': 1930, 'venue': 'Estadi Montilivi'},
        {'name': 'Rayo Vallecano', 'short_name': 'RAY', 'founded': 1924, 'venue': 'Campo de Fútbol de Vallecas'},
        {'name': 'RCD Espanyol', 'short_name': 'ESP', 'founded': 1900, 'venue': 'RCDE Stadium'},
        {'name': 'Deportivo Alaves', 'short_name': 'ALA', 'founded': 1921, 'venue': 'Mendizorrotza'},
        {'name': 'Real Valladolid', 'short_name': 'VLL', 'founded': 1928, 'venue': 'José Zorrilla'},
        {'name': 'CD Leganes', 'short_name': 'LEG', 'founded': 1928, 'venue': 'Butarque'},
        {'name': 'RCD Mallorca', 'short_name': 'MLL', 'founded': 1916, 'venue': 'Visit Mallorca Estadi'}
    ]
    
    return pd.DataFrame(teams_info)

def main():
    """ฟังก์ชันหลัก"""
    print("🇪🇸 La Liga Sample Data Creator")
    print("📊 สร้างข้อมูลคุณภาพสูงใกล้เคียงความจริง")
    print("=" * 60)
    
    # สร้างข้อมูลการแข่งขัน
    matches_df = create_realistic_laliga_data()
    
    # วิเคราะห์ข้อมูล
    analyze_realistic_data(matches_df)
    
    # สร้างข้อมูลทีม
    teams_df = create_teams_info()
    
    # บันทึกไฟล์
    matches_df.to_csv('laliga_realistic_matches.csv', index=False)
    teams_df.to_csv('laliga_teams_info.csv', index=False)
    
    print(f"\n💾 บันทึกไฟล์สำเร็จ:")
    print(f"   📁 laliga_realistic_matches.csv ({len(matches_df)} เกม)")
    print(f"   📁 laliga_teams_info.csv ({len(teams_df)} ทีม)")
    
    print(f"\n✅ ข้อมูล La Liga คุณภาพสูงพร้อมใช้งาน!")
    print(f"🎯 สามารถนำไปใช้กับ La Liga Predictor ได้ทันที")
    print(f"📝 ข้อมูลนี้ใกล้เคียงความจริงมากที่สุด")
    
    return matches_df, teams_df

if __name__ == "__main__":
    matches, teams = main()
