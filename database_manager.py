#!/usr/bin/env python3
"""
🗄️ Database Manager for Football Prediction System
ระบบจัดการฐานข้อมูลสำหรับการทำนายฟุตบอล

Features:
- SQLite database for storing predictions and results
- Multi-league support
- Performance tracking
- Historical data analysis
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional, Tuple
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """ระบบจัดการฐานข้อมูล"""
    
    def __init__(self, db_path: str = "football_predictions.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """สร้างฐานข้อมูลและตาราง"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Leagues table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leagues (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    country TEXT NOT NULL,
                    weight REAL DEFAULT 1.0,
                    season INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Teams table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    league_id INTEGER,
                    elo_rating REAL DEFAULT 1500,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (league_id) REFERENCES leagues (id)
                )
            """)
            
            # Matches table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    fixture_id INTEGER PRIMARY KEY,
                    league_id INTEGER,
                    home_team_id INTEGER,
                    away_team_id INTEGER,
                    match_date TIMESTAMP,
                    home_goals INTEGER,
                    away_goals INTEGER,
                    total_goals INTEGER,
                    result TEXT, -- 'Home', 'Draw', 'Away'
                    status TEXT,
                    venue TEXT,
                    city TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (league_id) REFERENCES leagues (id),
                    FOREIGN KEY (home_team_id) REFERENCES teams (id),
                    FOREIGN KEY (away_team_id) REFERENCES teams (id)
                )
            """)
            
            # Team statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS team_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team_id INTEGER,
                    league_id INTEGER,
                    season INTEGER,
                    games_played INTEGER DEFAULT 0,
                    wins INTEGER DEFAULT 0,
                    draws INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    goals_for INTEGER DEFAULT 0,
                    goals_against INTEGER DEFAULT 0,
                    home_wins INTEGER DEFAULT 0,
                    away_wins INTEGER DEFAULT 0,
                    form TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (team_id) REFERENCES teams (id),
                    FOREIGN KEY (league_id) REFERENCES leagues (id)
                )
            """)
            
            # Predictions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fixture_id INTEGER,
                    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    predicted_result TEXT,
                    result_confidence REAL,
                    predicted_handicap TEXT,
                    handicap_confidence REAL,
                    predicted_over_under TEXT,
                    ou_confidence REAL,
                    predicted_corners_1h TEXT,
                    corners_1h_confidence REAL,
                    predicted_corners_2h TEXT,
                    corners_2h_confidence REAL,
                    value_bet_rating TEXT,
                    recommended_bet TEXT,
                    model_version TEXT DEFAULT 'v1.0',
                    actual_result TEXT,
                    actual_total_goals INTEGER,
                    prediction_correct BOOLEAN,
                    FOREIGN KEY (fixture_id) REFERENCES matches (fixture_id)
                )
            """)
            
            conn.commit()
            logger.info("✅ Database initialized successfully")
    
    def insert_league(self, league_id: int, name: str, country: str, weight: float = 1.0, season: int = 2025):
        """เพิ่มข้อมูลลีก"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO leagues (id, name, country, weight, season)
                VALUES (?, ?, ?, ?, ?)
            """, (league_id, name, country, weight, season))
            conn.commit()
    
    def insert_team(self, team_id: int, name: str, league_id: int, elo_rating: float = 1500):
        """เพิ่มข้อมูลทีม"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO teams (id, name, league_id, elo_rating, last_updated)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (team_id, name, league_id, elo_rating))
            conn.commit()
    
    def insert_match(self, match_data: Dict):
        """เพิ่มข้อมูลการแข่งขัน"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO matches 
                (fixture_id, league_id, home_team_id, away_team_id, match_date, 
                 home_goals, away_goals, total_goals, result, status, venue, city)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                match_data['fixture_id'],
                match_data['league_id'],
                match_data['home_team_id'],
                match_data['away_team_id'],
                match_data['match_date'],
                match_data.get('home_goals'),
                match_data.get('away_goals'),
                match_data.get('total_goals'),
                match_data.get('result'),
                match_data['status'],
                match_data.get('venue'),
                match_data.get('city')
            ))
            conn.commit()
    
    def insert_prediction(self, prediction_data: Dict):
        """เพิ่มข้อมูลการทำนาย"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO predictions 
                (fixture_id, predicted_result, result_confidence, predicted_handicap, 
                 handicap_confidence, predicted_over_under, ou_confidence, 
                 predicted_corners_1h, corners_1h_confidence, predicted_corners_2h, 
                 corners_2h_confidence, value_bet_rating, recommended_bet, model_version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prediction_data['fixture_id'],
                prediction_data.get('predicted_result'),
                prediction_data.get('result_confidence'),
                prediction_data.get('predicted_handicap'),
                prediction_data.get('handicap_confidence'),
                prediction_data.get('predicted_over_under'),
                prediction_data.get('ou_confidence'),
                prediction_data.get('predicted_corners_1h'),
                prediction_data.get('corners_1h_confidence'),
                prediction_data.get('predicted_corners_2h'),
                prediction_data.get('corners_2h_confidence'),
                prediction_data.get('value_bet_rating'),
                prediction_data.get('recommended_bet'),
                prediction_data.get('model_version', 'v1.0')
            ))
            conn.commit()
    
    def update_prediction_result(self, fixture_id: int, actual_result: str, actual_total_goals: int):
        """อัปเดตผลการแข่งขันจริง"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get prediction
            cursor.execute("""
                SELECT predicted_result, predicted_over_under 
                FROM predictions 
                WHERE fixture_id = ? 
                ORDER BY prediction_date DESC 
                LIMIT 1
            """, (fixture_id,))
            
            prediction = cursor.fetchone()
            if prediction:
                predicted_result, predicted_ou = prediction
                
                # Check if result prediction is correct
                result_correct = (predicted_result == actual_result)
                
                # Check if over/under prediction is correct
                ou_correct = False
                if predicted_ou:
                    if "Over" in predicted_ou and actual_total_goals > 2.5:
                        ou_correct = True
                    elif "Under" in predicted_ou and actual_total_goals <= 2.5:
                        ou_correct = True
                
                overall_correct = result_correct or ou_correct
                
                # Update prediction
                cursor.execute("""
                    UPDATE predictions 
                    SET actual_result = ?, actual_total_goals = ?, prediction_correct = ?
                    WHERE fixture_id = ?
                """, (actual_result, actual_total_goals, overall_correct, fixture_id))
                
                conn.commit()
    
    def get_prediction_accuracy(self, days: int = 30) -> Dict:
        """คำนวณความแม่นยำของการทำนาย"""
        with sqlite3.connect(self.db_path) as conn:
            # Overall accuracy
            query = """
                SELECT 
                    COUNT(*) as total_predictions,
                    SUM(CASE WHEN prediction_correct = 1 THEN 1 ELSE 0 END) as correct_predictions,
                    AVG(CASE WHEN prediction_correct = 1 THEN 1.0 ELSE 0.0 END) as accuracy
                FROM predictions 
                WHERE prediction_date >= datetime('now', '-{} days')
                AND actual_result IS NOT NULL
            """.format(days)
            
            df_overall = pd.read_sql_query(query, conn)
            
            # Accuracy by prediction type
            query_by_type = """
                SELECT 
                    predicted_result,
                    COUNT(*) as total,
                    SUM(CASE WHEN actual_result = predicted_result THEN 1 ELSE 0 END) as correct,
                    AVG(CASE WHEN actual_result = predicted_result THEN 1.0 ELSE 0.0 END) as accuracy
                FROM predictions 
                WHERE prediction_date >= datetime('now', '-{} days')
                AND actual_result IS NOT NULL
                GROUP BY predicted_result
            """.format(days)
            
            df_by_type = pd.read_sql_query(query_by_type, conn)
            
            return {
                'overall': df_overall.to_dict('records')[0] if not df_overall.empty else {},
                'by_type': df_by_type.to_dict('records') if not df_by_type.empty else []
            }
    
    def get_team_stats(self, team_id: int) -> Dict:
        """ดึงสถิติทีม"""
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT t.name, ts.*, l.name as league_name
                FROM teams t
                LEFT JOIN team_stats ts ON t.id = ts.team_id
                LEFT JOIN leagues l ON ts.league_id = l.id
                WHERE t.id = ?
                ORDER BY ts.last_updated DESC
                LIMIT 1
            """
            
            df = pd.read_sql_query(query, conn, params=(team_id,))
            return df.to_dict('records')[0] if not df.empty else {}
    
    def get_head_to_head(self, team1_id: int, team2_id: int, limit: int = 10) -> pd.DataFrame:
        """ดึงข้อมูลการเจอกันในอดีต"""
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT m.*, 
                       h.name as home_team_name, 
                       a.name as away_team_name,
                       l.name as league_name
                FROM matches m
                JOIN teams h ON m.home_team_id = h.id
                JOIN teams a ON m.away_team_id = a.id
                JOIN leagues l ON m.league_id = l.id
                WHERE (m.home_team_id = ? AND m.away_team_id = ?)
                   OR (m.home_team_id = ? AND m.away_team_id = ?)
                ORDER BY m.match_date DESC
                LIMIT ?
            """
            
            return pd.read_sql_query(query, conn, params=(team1_id, team2_id, team2_id, team1_id, limit))
    
    def export_predictions_report(self, days: int = 7) -> str:
        """สร้างรายงานการทำนาย"""
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT p.*, m.match_date, 
                       h.name as home_team, a.name as away_team,
                       l.name as league_name
                FROM predictions p
                JOIN matches m ON p.fixture_id = m.fixture_id
                JOIN teams h ON m.home_team_id = h.id
                JOIN teams a ON m.away_team_id = a.id
                JOIN leagues l ON m.league_id = l.id
                WHERE p.prediction_date >= datetime('now', '-{} days')
                ORDER BY p.prediction_date DESC
            """.format(days)
            
            df = pd.read_sql_query(query, conn)
            
            if not df.empty:
                filename = f"predictions_report_{datetime.now().strftime('%Y%m%d')}.csv"
                df.to_csv(filename, index=False)
                logger.info(f"📊 Predictions report exported to: {filename}")
                return filename
            
            return ""
    
    def cleanup_old_data(self, days: int = 90):
        """ลบข้อมูลเก่า"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Delete old predictions
            cursor.execute("""
                DELETE FROM predictions 
                WHERE prediction_date < datetime('now', '-{} days')
            """.format(days))
            
            deleted_predictions = cursor.rowcount
            
            # Delete old matches
            cursor.execute("""
                DELETE FROM matches 
                WHERE match_date < datetime('now', '-{} days')
                AND fixture_id NOT IN (SELECT fixture_id FROM predictions)
            """.format(days))
            
            deleted_matches = cursor.rowcount
            
            conn.commit()
            
            logger.info(f"🗑️ Cleaned up {deleted_predictions} old predictions and {deleted_matches} old matches")

def main():
    """Test database functionality"""
    db = DatabaseManager("test_football.db")
    
    # Insert sample data
    db.insert_league(293, "K League 2", "South Korea", 0.9, 2025)
    db.insert_team(2763, "Incheon United", 293)
    db.insert_team(2753, "Asan Mugunghwa", 293)
    
    # Insert sample match
    match_data = {
        'fixture_id': 1337689,
        'league_id': 293,
        'home_team_id': 2763,
        'away_team_id': 2753,
        'match_date': '2025-07-13 10:00:00',
        'status': 'Not Started',
        'venue': 'Sungui Arena Park',
        'city': 'Incheon'
    }
    db.insert_match(match_data)
    
    # Insert sample prediction
    prediction_data = {
        'fixture_id': 1337689,
        'predicted_result': 'Draw',
        'result_confidence': 0.76,
        'predicted_over_under': 'Over 2.5',
        'ou_confidence': 0.77,
        'value_bet_rating': '⭐ Good Value',
        'recommended_bet': 'Draw + Over 2.5'
    }
    db.insert_prediction(prediction_data)
    
    print("✅ Database test completed successfully!")
    
    # Clean up test database
    if os.path.exists("test_football.db"):
        os.remove("test_football.db")

if __name__ == "__main__":
    main()
