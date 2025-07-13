#!/usr/bin/env python3
"""
🏗️ Multi-League Database Setup Script
สคริปต์สำหรับตั้งค่าฐานข้อมูลหลายลีกครั้งแรก
"""

import os
import time
from multi_league_database_manager import MultiLeagueDBManager

def setup_database_with_sample_data():
    """Setup database with sample data for testing"""
    
    # Initialize database manager
    db_manager = MultiLeagueDBManager(db_path="football_leagues.db")
    
    print("🏗️ Setting up Multi-League Database...")
    print("=" * 50)
    
    # Step 1: Initialize database structure
    print("1️⃣ Initializing database structure...")
    db_manager.init_database()
    db_manager.populate_leagues()
    
    # Step 2: Add sample teams for testing
    print("\n2️⃣ Adding sample teams...")
    add_sample_teams(db_manager)
    
    # Step 3: Add sample matches for testing
    print("\n3️⃣ Adding sample matches...")
    add_sample_matches(db_manager)
    
    # Step 4: Calculate statistics
    print("\n4️⃣ Calculating team statistics...")
    for league_key in db_manager.leagues.keys():
        db_manager.calculate_team_statistics(league_key, 2024)
    
    # Step 5: Show summary
    print("\n5️⃣ Database Summary:")
    summary = db_manager.get_league_summary()
    
    for league_key, info in summary.items():
        print(f"\n🏆 {info['name']}")
        print(f"   Teams: {info['teams_count']}")
        for season_data in info['matches_by_season']:
            print(f"   {season_data['season']}: {season_data['count']} matches")
    
    print("\n✅ Database setup completed!")
    return db_manager

def add_sample_teams(db_manager):
    """Add sample teams for each league"""
    import sqlite3
    
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    
    sample_teams = {
        'premier_league': [
            (1, 'Manchester City', 'England', 1880, 'Etihad Stadium', 55000),
            (2, 'Arsenal', 'England', 1886, 'Emirates Stadium', 60000),
            (3, 'Liverpool', 'England', 1892, 'Anfield', 54000),
            (4, 'Chelsea', 'England', 1905, 'Stamford Bridge', 40000),
            (5, 'Manchester United', 'England', 1878, 'Old Trafford', 74000),
        ],
        'la_liga': [
            (101, 'Real Madrid', 'Spain', 1902, 'Santiago Bernabéu', 81000),
            (102, 'Barcelona', 'Spain', 1899, 'Camp Nou', 99000),
            (103, 'Atlético Madrid', 'Spain', 1903, 'Wanda Metropolitano', 68000),
            (104, 'Sevilla', 'Spain', 1890, 'Ramón Sánchez Pizjuán', 43000),
            (105, 'Real Sociedad', 'Spain', 1909, 'Reale Arena', 40000),
        ],
        'bundesliga': [
            (201, 'Bayern Munich', 'Germany', 1900, 'Allianz Arena', 75000),
            (202, 'Borussia Dortmund', 'Germany', 1909, 'Signal Iduna Park', 81000),
            (203, 'RB Leipzig', 'Germany', 2009, 'Red Bull Arena', 47000),
            (204, 'Bayer Leverkusen', 'Germany', 1904, 'BayArena', 30000),
            (205, 'Eintracht Frankfurt', 'Germany', 1899, 'Deutsche Bank Park', 51000),
        ],
        'ligue_1': [
            (301, 'Paris Saint-Germain', 'France', 1970, 'Parc des Princes', 48000),
            (302, 'Marseille', 'France', 1899, 'Stade Vélodrome', 67000),
            (303, 'Lyon', 'France', 1950, 'Groupama Stadium', 59000),
            (304, 'Monaco', 'France', 1924, 'Stade Louis II', 18500),
            (305, 'Lille', 'France', 1944, 'Stade Pierre-Mauroy', 50000),
        ],
        'serie_a': [
            (401, 'Juventus', 'Italy', 1897, 'Allianz Stadium', 41000),
            (402, 'Inter Milan', 'Italy', 1908, 'San Siro', 80000),
            (403, 'AC Milan', 'Italy', 1899, 'San Siro', 80000),
            (404, 'Napoli', 'Italy', 1926, 'Stadio Diego Armando Maradona', 55000),
            (405, 'Roma', 'Italy', 1927, 'Stadio Olimpico', 70000),
        ],
        'jleague_2': [
            (501, 'Mito Hollyhock', 'Japan', 1990, "K's Denki Stadium", 12000),
            (502, 'Blaublitz Akita', 'Japan', 1965, 'Soyu Stadium', 20000),
            (503, 'Iwaki FC', 'Japan', 2015, 'Hawaiians Stadium Iwaki', 21000),
            (504, 'Jubilo Iwata', 'Japan', 1970, 'Yamaha Stadium', 15000),
            (505, 'Vegalta Sendai', 'Japan', 1988, 'Yurtec Stadium Sendai', 19000),
        ]
    }
    
    for league_key, teams in sample_teams.items():
        for team_data in teams:
            cursor.execute('''
                INSERT OR REPLACE INTO teams 
                (team_id, name, league_key, country, founded, venue_name, venue_capacity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (team_data[0], team_data[1], league_key, team_data[2], 
                  team_data[3], team_data[4], team_data[5]))
    
    conn.commit()
    conn.close()
    print("✅ Sample teams added")

def add_sample_matches(db_manager):
    """Add sample matches for each league"""
    import sqlite3
    import random
    from datetime import datetime, timedelta
    
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    
    # Get teams for each league
    teams_by_league = {}
    for league_key in db_manager.leagues.keys():
        cursor.execute('SELECT team_id FROM teams WHERE league_key = ?', (league_key,))
        teams_by_league[league_key] = [row[0] for row in cursor.fetchall()]
    
    match_id = 1
    
    for league_key, team_ids in teams_by_league.items():
        if len(team_ids) < 2:
            continue
            
        # Generate sample matches for 2024 season
        for i in range(20):  # 20 matches per league
            home_team = random.choice(team_ids)
            away_team = random.choice([t for t in team_ids if t != home_team])
            
            # Random match date in 2024
            start_date = datetime(2024, 1, 1)
            end_date = datetime(2024, 12, 31)
            random_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days)
            )
            
            # Random scores
            home_score = random.randint(0, 4)
            away_score = random.randint(0, 4)
            
            cursor.execute('''
                INSERT INTO matches 
                (match_id, league_key, season, match_date, home_team_id, away_team_id,
                 home_score, away_score, match_status, venue, referee)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                match_id, league_key, 2024, random_date.strftime('%Y-%m-%d'),
                home_team, away_team, home_score, away_score, 'FT',
                f'Stadium {match_id}', f'Referee {match_id}'
            ))
            
            match_id += 1
    
    conn.commit()
    conn.close()
    print("✅ Sample matches added")

def setup_with_real_api_data(api_key: str):
    """Setup database with real API data (requires API key)"""
    
    print("🌐 Setting up database with real API data...")
    print("⚠️  This will take several minutes and use API calls")
    
    # Initialize with API key
    db_manager = MultiLeagueDBManager(db_path="football_leagues.db", api_key=api_key)
    
    # Setup all leagues
    db_manager.setup_all_leagues()
    
    return db_manager

def main():
    """Main setup function"""
    print("🏗️ Multi-League Database Setup")
    print("=" * 40)
    print("Choose setup option:")
    print("1. Quick setup with sample data (for testing)")
    print("2. Full setup with real API data (requires API key)")
    print("3. Skip setup (use existing database)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 Setting up with sample data...")
        db_manager = setup_database_with_sample_data()
        
    elif choice == "2":
        api_key = input("\nEnter your API-Sports key: ").strip()
        if api_key:
            print("\n🌐 Setting up with real API data...")
            db_manager = setup_with_real_api_data(api_key)
        else:
            print("❌ API key required for real data setup")
            return
            
    elif choice == "3":
        print("\n⏭️ Skipping database setup")
        db_manager = MultiLeagueDBManager(db_path="football_leagues.db")
        
    else:
        print("❌ Invalid choice")
        return
    
    # Test the enhanced predictor
    print("\n🤖 Testing Enhanced Multi-League Predictor...")
    from enhanced_multi_league_predictor import EnhancedMultiLeaguePredictor
    
    predictor = EnhancedMultiLeaguePredictor()
    data = predictor.load_multi_league_data()
    
    if not data.empty:
        print(f"✅ Loaded {len(data)} matches for ML training")
        
        # Quick training test
        data = predictor.engineer_features(data)
        predictor.train_models(data)
        
        print("\n🎉 Setup completed successfully!")
        print("📊 You can now use the enhanced multi-league predictor")
        
    else:
        print("⚠️ No data found. You may need to run the full API setup")

if __name__ == "__main__":
    main()
