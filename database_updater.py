import sqlite3
import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseUpdater:
    """Handles all database operations for the football prediction system."""

    def __init__(self, db_path: str):
        """
        Initializes the DatabaseUpdater.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path
        self.conn = None
        self.connect()

    def connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            logger.info(f"Successfully connected to database at {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

    def _execute_query(self, query: str, params: tuple = (), fetch: str = None):
        """
        A helper function to execute SQL queries.

        Args:
            query (str): The SQL query to execute.
            params (tuple): The parameters to substitute in the query.
            fetch (str): Type of fetch ('one', 'all').

        Returns:
            The result of the fetch operation or the last inserted row id.
        """
        if not self.conn:
            self.connect()
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            if fetch == 'one':
                return cursor.fetchone()
            elif fetch == 'all':
                return cursor.fetchall()
            else:
                self.conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}\nQuery: {query}\nParams: {params}")
            self.conn.rollback()
            return None

    def add_or_get_league(self, league_id: str, league_name: str, country: str, season: str) -> str:
        """
        Adds a league if it doesn't exist, then returns its ID.

        Args:
            league_id (str): The external ID of the league.
            league_name (str): The name of the league.
            country (str): The country of the league.
            season (str): The current season.

        Returns:
            The internal league ID (which is the same as the external one in this schema).
        """
        query_select = "SELECT id FROM leagues WHERE id = ?"
        league = self._execute_query(query_select, (league_id,), fetch='one')

        if league:
            return league[0]
        else:
            query_insert = """
            INSERT INTO leagues (id, name, country, season, createdAt, updatedAt)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            now = datetime.utcnow().isoformat()
            params = (league_id, league_name, country, season, now, now)
            self._execute_query(query_insert, params)
            logger.info(f"Added new league: {league_name} ({country})")
            return league_id

    def update_matches_and_predictions(self, predictions_df: pd.DataFrame):
        """
        Updates the database with new matches and their predictions.

        Args:
            predictions_df (pd.DataFrame): DataFrame containing match and prediction data.
        """
        if predictions_df.empty:
            logger.warning("Predictions DataFrame is empty. No updates to perform.")
            return

        logger.info(f"Starting database update for {len(predictions_df)} matches...")

        for _, row in predictions_df.iterrows():
            try:
                # Step 1: Add or get league
                league_id = self.add_or_get_league(
                    str(row['league_id']),
                    row['league_name'],
                    row['league_country'],
                    str(row['league_season'])
                )

                # Step 2: Add match, if it doesn't exist based on externalId
                match_query = "SELECT id FROM matches WHERE externalId = ?"
                match = self._execute_query(match_query, (str(row['fixture_id']),), fetch='one')

                if match:
                    match_id = match[0]
                    logger.debug(f"Match {row['home_team']} vs {row['away_team']} already exists with ID: {match_id}")
                else:
                    match_date = pd.to_datetime(row['date']).isoformat()
                    match_time = pd.to_datetime(row['date']).strftime('%H:%M')

                    insert_match_query = """
                    INSERT INTO matches (externalId, leagueId, homeTeam, awayTeam, matchDate, matchTime, status, createdAt, updatedAt)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    now = datetime.utcnow().isoformat()
                    match_params = (
                        str(row['fixture_id']), league_id, row['home_team'], row['away_team'],
                        match_date, match_time, 'UPCOMING', now, now
                    )
                    match_id = self._execute_query(insert_match_query, match_params)
                    if not match_id:
                        logger.error(f"Failed to insert match for fixture ID {row['fixture_id']}")
                        continue # Skip to next match if insertion fails
                    logger.info(f"Added new match: {row['home_team']} vs {row['away_team']} (ID: {match_id})")

                # Step 3: Add predictions for the match
                predictions = self._prepare_predictions(row, match_id)
                for pred in predictions:
                    # Use INSERT OR REPLACE to handle updates gracefully
                    pred_query = """
                    INSERT OR REPLACE INTO predictions (matchId, category, prediction, confidence, createdAt, updatedAt)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """
                    now = datetime.utcnow().isoformat()
                    pred_params = (
                        pred['matchId'], pred['category'], pred['prediction'],
                        pred['confidence'], now, now
                    )
                    self._execute_query(pred_query, pred_params)
                logger.debug(f"Updated {len(predictions)} predictions for match ID {match_id}")

            except Exception as e:
                logger.error(f"Error processing row for fixture {row.get('fixture_id', 'N/A')}: {e}")

        logger.info("Database update process completed.")

    def _prepare_predictions(self, row: pd.Series, match_id: int) -> list:
        """Helper to structure prediction data from a DataFrame row."""
        predictions = []

        # Match Result
        if 'predicted_result' in row and pd.notna(row['predicted_result']):
            try:
                confidence = float(str(row.get('result_confidence', '0')).replace('%', ''))
                predictions.append({
                    'matchId': match_id,
                    'category': 'MATCH_RESULT',
                    'prediction': row['predicted_result'],
                    'confidence': confidence
                })
            except (ValueError, TypeError):
                logger.warning(f"Could not parse confidence for MATCH_RESULT on match {match_id}")


        # Over/Under
        if 'predicted_over_under' in row and pd.notna(row['predicted_over_under']):
            try:
                confidence = float(str(row.get('ou_confidence', '0')).replace('%', ''))
                predictions.append({
                    'matchId': match_id,
                    'category': 'OVER_UNDER',
                    'prediction': row['predicted_over_under'],
                    'confidence': confidence
                })
            except (ValueError, TypeError):
                logger.warning(f"Could not parse confidence for OVER_UNDER on match {match_id}")

        # Add other prediction types here if they exist in the dataframe
        # e.g., CORNERS, BTTS, etc.

        return predictions

if __name__ == '__main__':
    # Example Usage (for testing)
    print("Testing DatabaseUpdater...")

    # NOTE: Adjust this path to the correct location of your database
    db_path = 'football-prediction-system/backend/prisma/football_predictions.db'

    # Create dummy data
    dummy_data = {
        'fixture_id': [101, 102],
        'league_id': [39, 39],
        'league_name': ['Premier League', 'Premier League'],
        'league_country': ['England', 'England'],
        'league_season': [2025, 2025],
        'date': [datetime.now(), datetime.now()],
        'home_team': ['Man Utd', 'Arsenal'],
        'away_team': ['Chelsea', 'Liverpool'],
        'predicted_result': ['Home Win', 'Draw'],
        'result_confidence': ['65.5%', '51.2%'],
        'predicted_over_under': ['Over 2.5', 'Under 2.5'],
        'ou_confidence': ['72.0%', '68.8%']
    }
    dummy_df = pd.DataFrame(dummy_data)

    updater = DatabaseUpdater(db_path)
    try:
        updater.update_matches_and_predictions(dummy_df)
        print("\nTest data:")
        print(updater._execute_query("SELECT * FROM matches ORDER BY id DESC LIMIT 2", fetch='all'))
        print(updater._execute_query("SELECT * FROM predictions ORDER BY id DESC LIMIT 4", fetch='all'))
    finally:
        updater.close()

    print("\nDatabaseUpdater test finished.")
