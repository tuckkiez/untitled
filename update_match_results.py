import os
import requests
import sqlite3
import logging
from datetime import datetime, timedelta

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
DB_PATH = 'football-prediction-system/backend/prisma/football_predictions.db'
API_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = "api-football-v1.p.rapidapi.com"
API_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

class ResultUpdater:
    def __init__(self, db_path, api_key):
        if not api_key:
            raise ValueError("API key is missing. Please set the API_FOOTBALL_KEY environment variable.")
        self.db_path = db_path
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": API_HOST
        }
        self.conn = None

    def _connect_db(self):
        """Establish database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            logging.info("Successfully connected to the database.")
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            raise

    def _close_db(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")

    def _execute_query(self, query, params=(), fetch=None):
        """Execute a SQL query."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            if fetch == 'one':
                return cursor.fetchone()
            if fetch == 'all':
                return cursor.fetchall()
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}\nQuery: {query}")
            return None

    def get_pending_matches(self):
        """
        Get matches that are 'UPCOMING' and have a match date in the past
        (within the last 24 hours).
        """
        yesterday = (datetime.utcnow() - timedelta(days=1)).isoformat()
        query = """
        SELECT id, externalId, homeTeam, awayTeam FROM matches
        WHERE status = 'UPCOMING' AND matchDate < ?
        """
        # The query parameter should be a string for ISO format comparison
        return self._execute_query(query, (datetime.utcnow().isoformat(),), fetch='all')


    def fetch_results_from_api(self, fixture_ids):
        """Fetch results for given fixture IDs from the API."""
        if not fixture_ids:
            return None

        params = {"ids": "-".join(fixture_ids)}
        try:
            response = requests.get(API_URL, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json().get('response', [])
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            return None

    def update_database_with_results(self, matches_to_update):
        """Update match status, scores, and evaluate predictions."""
        if not matches_to_update:
            logging.info("No pending matches to update.")
            return

        fixture_ids = [match['externalId'] for match in matches_to_update if match['externalId']]

        if not fixture_ids:
            logging.info("No pending matches with external IDs to update.")
            return

        api_results = self.fetch_results_from_api(fixture_ids)

        if not api_results:
            logging.warning("Could not fetch results from API. Aborting update.")
            return

        updated_count = 0
        for result in api_results:
            fixture = result.get('fixture', {})
            fixture_id = str(fixture.get('id'))
            status = fixture.get('status', {}).get('short')

            # We only care about finished matches
            if status not in ['FT', 'AET', 'PEN']:
                logging.info(f"Match {fixture_id} is not finished yet (Status: {status}). Skipping.")
                continue

            goals = result.get('goals', {})
            home_score = goals.get('home')
            away_score = goals.get('away')

            if home_score is None or away_score is None:
                logging.warning(f"Scores for match {fixture_id} are null. Skipping.")
                continue

            # Update match table
            update_query = """
            UPDATE matches
            SET status = 'FINISHED', homeScore = ?, awayScore = ?, updatedAt = ?
            WHERE externalId = ?
            """
            now = datetime.utcnow().isoformat()
            self._execute_query(update_query, (home_score, away_score, now, fixture_id))
            logging.info(f"Updated match {fixture_id} to FINISHED with score {home_score}-{away_score}.")
            updated_count += 1

        logging.info(f"Successfully updated {updated_count} matches.")


    def run(self):
        """Main execution flow."""
        logging.info("🚀 Starting match result update process...")
        self._connect_db()
        try:
            pending_matches = self.get_pending_matches()
            if not pending_matches:
                logging.info("No matches found that need a result update.")
                return

            logging.info(f"Found {len(pending_matches)} matches to check for results.")
            self.update_database_with_results(pending_matches)

        finally:
            self._close_db()
        logging.info("✅ Match result update process finished.")


def main():
    """Entry point."""
    try:
        updater = ResultUpdater(db_path=DB_PATH, api_key=API_KEY)
        updater.run()
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
