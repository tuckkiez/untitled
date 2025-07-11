# 📊 Real Data Sources - การหาข้อมูลจริง

## 🎯 เป้าหมาย: เพิ่มความแม่นยำจาก 60% เป็น 65-70%

## 📊 1. Player Statistics APIs

### 🔥 FotMob API (แนะนำ)
```python
# URL: https://www.fotmob.com/api/
# Status: Free (with rate limits)
# Data: Player stats, team stats, match data

import requests

def get_fotmob_player_stats(player_id):
    url = f"https://www.fotmob.com/api/playerData?id={player_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# ข้อมูลที่ได้:
# - Goals, Assists, Minutes played
# - Pass accuracy, Shots, Tackles
# - Player ratings, Form
# - Expected goals (xG), Expected assists (xA)
```

### ⚽ Understat API
```python
# URL: https://understat.com/
# Status: Free scraping
# Data: Advanced metrics, xG data

import requests
from bs4 import BeautifulSoup

def get_understat_team_data(team_name, season):
    url = f"https://understat.com/team/{team_name}/{season}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract xG, xGA, shot data
    # Advanced team metrics
    return parsed_data

# ข้อมูลที่ได้:
# - Expected goals (xG) for/against
# - Shot locations and quality
# - Defensive actions
# - Team pressing statistics
```

### 📈 FBref Web Scraping
```python
# URL: https://fbref.com/
# Status: Free scraping (respect robots.txt)
# Data: Comprehensive statistics

import pandas as pd

def scrape_fbref_team_stats(team_url):
    # Read tables directly with pandas
    tables = pd.read_html(team_url)
    
    # Process different stat tables
    player_stats = tables[0]  # Player statistics
    team_stats = tables[1]    # Team statistics
    
    return {
        'player_stats': player_stats,
        'team_stats': team_stats
    }

# ข้อมูลที่ได้:
# - Detailed player statistics
# - Team tactical data
# - Historical performance data
# - Advanced metrics (xG, xA, etc.)
```

## 🏥 2. Injury Data Sources

### 🏥 Premier League Official API
```python
# URL: https://fantasy.premierleague.com/api/
# Status: Free official API
# Data: Player availability, injury status

def get_fpl_player_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    data = response.json()
    
    players = data['elements']
    
    injury_data = []
    for player in players:
        if player['status'] != 'a':  # 'a' = available
            injury_data.append({
                'name': player['web_name'],
                'team': player['team'],
                'status': player['status'],  # 'd' = doubtful, 'i' = injured, 'u' = unavailable
                'news': player['news'],
                'chance_of_playing': player['chance_of_playing_next_round']
            })
    
    return injury_data

# ข้อมูลที่ได้:
# - Current injury status
# - Chance of playing percentage
# - Injury news and updates
# - Expected return dates
```

### 📰 Sky Sports Scraping
```python
# URL: https://www.skysports.com/football/news
# Status: Web scraping
# Data: Injury news, team updates

def scrape_sky_sports_injuries():
    url = "https://www.skysports.com/football/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find injury-related articles
    injury_articles = soup.find_all('article', class_='news-list__item')
    
    injury_news = []
    for article in injury_articles:
        title = article.find('h3').text
        if any(keyword in title.lower() for keyword in ['injury', 'injured', 'doubt', 'fitness']):
            injury_news.append({
                'title': title,
                'link': article.find('a')['href'],
                'date': article.find('time')['datetime']
            })
    
    return injury_news
```

## 🌤️ 3. Weather Data APIs

### 🌦️ OpenWeatherMap API (แนะนำ)
```python
# URL: https://openweathermap.org/api
# Status: Free tier (1000 calls/day)
# Cost: $0 for basic usage

import requests
from datetime import datetime

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Stadium coordinates
        self.stadiums = {
            'Arsenal': {'lat': 51.5549, 'lon': -0.1084},  # Emirates
            'Chelsea': {'lat': 51.4816, 'lon': -0.1909},  # Stamford Bridge
            'Manchester City': {'lat': 53.4831, 'lon': -2.2004},  # Etihad
            # ... add all stadiums
        }
    
    def get_match_weather(self, home_team, match_datetime):
        coords = self.stadiums.get(home_team)
        if not coords:
            return None
            
        # Current weather
        if match_datetime <= datetime.now():
            url = f"{self.base_url}/weather"
        else:
            # Forecast (up to 5 days)
            url = f"{self.base_url}/forecast"
            
        params = {
            'lat': coords['lat'],
            'lon': coords['lon'],
            'appid': self.api_key,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params)
        return response.json()

# การใช้งาน:
weather_api = WeatherAPI('your_api_key')
weather = weather_api.get_match_weather('Arsenal', datetime(2024, 12, 15, 15, 0))

# ข้อมูลที่ได้:
# - Temperature, Humidity, Wind speed
# - Precipitation, Visibility, Pressure
# - Weather conditions (Clear, Rain, etc.)
# - 5-day forecast for upcoming matches
```

### 🌡️ WeatherAPI.com
```python
# URL: https://www.weatherapi.com/
# Status: Free tier (1M calls/month)
# Cost: $0 for basic usage

def get_weather_api_data(api_key, location, date):
    url = f"http://api.weatherapi.com/v1/history.json"
    params = {
        'key': api_key,
        'q': location,
        'dt': date.strftime('%Y-%m-%d')
    }
    
    response = requests.get(url, params=params)
    return response.json()

# ข้อมูลที่ได้:
# - More detailed weather data
# - Historical weather (for backtesting)
# - Weather alerts and warnings
# - Air quality data
```

## 💰 4. Market Odds APIs

### 🎲 The Odds API
```python
# URL: https://the-odds-api.com/
# Status: Free tier (500 requests/month)
# Cost: $0.001 per request after free tier

def get_betting_odds(api_key, sport='soccer_epl'):
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        'api_key': api_key,
        'regions': 'uk',
        'markets': 'h2h,spreads,totals',
        'oddsFormat': 'decimal'
    }
    
    response = requests.get(url, params=params)
    return response.json()

# ข้อมูลที่ได้:
# - Match winner odds (1X2)
# - Handicap odds (spreads)
# - Over/Under odds (totals)
# - Multiple bookmaker odds
```

### 📊 Betfair API
```python
# URL: https://docs.developer.betfair.com/
# Status: Free for developers
# Cost: Commission on winnings only

# Requires application approval
# More complex setup but richer data
# Exchange odds vs bookmaker odds
```

## 🔧 5. Implementation Plan

### Phase 1: Quick Wins (1-2 weeks)
```python
# 1. OpenWeatherMap integration
weather_api = WeatherAPI('your_key')

# 2. FPL injury data
injury_data = get_fpl_player_data()

# 3. Basic FotMob scraping
player_stats = get_fotmob_player_stats(player_id)
```

### Phase 2: Advanced Integration (2-4 weeks)
```python
# 1. Understat xG data
xg_data = get_understat_team_data('Arsenal', 2024)

# 2. FBref comprehensive stats
fbref_data = scrape_fbref_team_stats(team_url)

# 3. Odds API integration
odds_data = get_betting_odds(api_key)
```

### Phase 3: Real-time System (1-2 months)
```python
# 1. Automated data collection
# 2. Real-time injury updates
# 3. Live weather monitoring
# 4. Odds movement tracking
```

## 💡 6. Expected Impact

### Current vs Expected Accuracy
| Data Source | Current | With Real Data | Improvement |
|-------------|---------|----------------|-------------|
| **Player Stats** | Mock (Random) | Real API | **+5-8%** |
| **Injury Data** | Mock (Random) | Real Status | **+3-5%** |
| **Weather** | Mock (Seasonal) | Real Conditions | **+2-3%** |
| **Market Odds** | None | Real Odds | **+3-5%** |
| **Total** | **60%** | **68-76%** | **+8-16%** |

### Conservative Estimate
- **Current**: 60% accuracy
- **With Real Data**: **65-70%** accuracy
- **Target**: Beat 65% professional tipster level

## 🚀 7. Getting Started

### Step 1: Get API Keys
```bash
# OpenWeatherMap (Free)
# 1. Go to https://openweathermap.org/api
# 2. Sign up for free account
# 3. Get API key (1000 calls/day free)

# The Odds API (Free tier)
# 1. Go to https://the-odds-api.com/
# 2. Sign up for free account  
# 3. Get API key (500 requests/month free)
```

### Step 2: Test Integration
```python
# Test weather API
weather = WeatherAPI('your_key')
result = weather.get_match_weather('Arsenal', datetime.now())
print(result)

# Test injury data
injuries = get_fpl_player_data()
print(f"Found {len(injuries)} injured players")
```

### Step 3: Integrate with Predictor
```python
# Modify ultra_predictor_fixed.py
# Replace mock data functions with real API calls
# Test accuracy improvement
```

## 📈 8. Cost Analysis

### Free Tier Usage
- **OpenWeatherMap**: 1000 calls/day = ~30,000/month (FREE)
- **The Odds API**: 500 calls/month (FREE)
- **FPL API**: Unlimited (FREE)
- **Web Scraping**: Free (respect rate limits)

### Paid Tier (if needed)
- **OpenWeatherMap**: $40/month for 100,000 calls
- **The Odds API**: $50/month for 50,000 calls
- **WeatherAPI**: $4/month for 1M calls

**Total Monthly Cost: $0-100 depending on usage**

---

**🎯 Priority: Start with free APIs (Weather + Injury) for immediate 5-8% accuracy boost!** 🚀
