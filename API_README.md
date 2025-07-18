# API-Football Usage Guide

## API Endpoints

Below is the list of available API endpoints from API-Football:

- `/countries` - Get information about countries
- `/seasons` - Get available seasons
- `/leagues` - Get information about leagues
- `/teams` - Get information about teams
- `/teams/statistics` - Get team statistics
- `/venues` - Get information about venues
- `/standings` - Get league standings
- `/fixtures` - Get fixtures information
- `/fixtures/rounds` - Get rounds information
- `/fixtures/headtohead` - Get head-to-head statistics
- `/fixtures/statistics` - Get fixture statistics
- `/fixtures/events` - Get fixture events
- `/fixtures/lineups` - Get fixture lineups
- `/injuries` - Get information about injuries
- `/predictions` - Get predictions for fixtures
- `/players/seasons` - Get player seasons
- `/players` - Get information about players
- `/players/squads` - Get player squads
- `/players/topscorers` - Get top scorers
- `/players/trophies` - Get player trophies
- `/players/sidelined` - Get sidelined players
- `/trophies` - Get information about trophies
- `/coaches` - Get information about coaches
- `/transfers` - Get information about transfers
- `/odds` - Get pre-match odds
- `/odds/live` - Get live odds
- `/odds/live/bets` - Get live bets
- `/odds/mapping` - Get odds mapping
- `/odds/bookmakers` - Get information about bookmakers
- `/odds/bets` - Get information about bets
- `/timezone` - Get timezone information

## Example Usage

### Basic Request Format

```bash
curl --request GET \
  --url 'https://api-football-v1.p.rapidapi.com/v3/fixtures?date=2021-01-29' \
  --header 'x-rapidapi-host: api-football-v1.p.rapidapi.com' \
  --header 'x-rapidapi-key: f9cf9a3854mshf30572945114fb4p105c26jsnbbc82dcea9c0'
```

### Searching for Fixtures by Date

To find fixtures for a specific date:

```bash
curl --request GET \
  --url 'https://api-football-v1.p.rapidapi.com/v3/fixtures?date=2025-07-18' \
  --header 'x-rapidapi-host: api-football-v1.p.rapidapi.com' \
  --header 'x-rapidapi-key: YOUR_API_KEY'
```

### Searching for Fixtures by League

To find fixtures for a specific league:

```bash
curl --request GET \
  --url 'https://api-football-v1.p.rapidapi.com/v3/fixtures?league=39&season=2025' \
  --header 'x-rapidapi-host: api-football-v1.p.rapidapi.com' \
  --header 'x-rapidapi-key: YOUR_API_KEY'
```

### Getting League Information

To get information about leagues:

```bash
curl --request GET \
  --url 'https://api-football-v1.p.rapidapi.com/v3/leagues' \
  --header 'x-rapidapi-host: api-football-v1.p.rapidapi.com' \
  --header 'x-rapidapi-key: YOUR_API_KEY'
```

### Getting Fixtures Between Dates

To get fixtures between two dates:

```bash
curl --request GET \
  --url 'https://api-football-v1.p.rapidapi.com/v3/fixtures?from=2025-07-18&to=2025-07-19&timezone=Asia/Bangkok' \
  --header 'x-rapidapi-host: api-football-v1.p.rapidapi.com' \
  --header 'x-rapidapi-key: YOUR_API_KEY'
```

## Important Notes

1. Replace `YOUR_API_KEY` with your actual API key
2. The API has rate limits, so use requests efficiently
3. Use the timezone parameter to get results in your preferred timezone
4. Always check the API documentation for the most up-to-date information
