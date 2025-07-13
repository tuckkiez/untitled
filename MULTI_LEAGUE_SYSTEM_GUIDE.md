# 🏆 Multi-League Database & ML System Guide

## 📋 Overview
ระบบฐานข้อมูลและ Machine Learning หลายลีกสำหรับการทำนายผลฟุตบอลที่แม่นยำขึ้น

### 🎯 Supported Leagues:
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Premier League** (England) - Weight: 1.2
- 🇪🇸 **La Liga** (Spain) - Weight: 1.1  
- 🇩🇪 **Bundesliga** (Germany) - Weight: 1.1
- 🇫🇷 **Ligue 1** (France) - Weight: 1.0
- 🇮🇹 **Serie A** (Italy) - Weight: 1.1
- 🇯🇵 **J-League 2** (Japan) - Weight: 0.9

---

## 🏗️ Database Schema

### Tables Structure:

#### 1. **leagues** - ข้อมูลลีก
```sql
- league_key (TEXT PRIMARY KEY)
- league_id (INTEGER) 
- name (TEXT)
- country (TEXT)
- created_at (TIMESTAMP)
```

#### 2. **teams** - ข้อมูลทีม
```sql
- team_id (INTEGER PRIMARY KEY)
- name (TEXT)
- league_key (TEXT)
- country (TEXT)
- founded (INTEGER)
- venue_name (TEXT)
- venue_capacity (INTEGER)
- created_at (TIMESTAMP)
```

#### 3. **matches** - ข้อมูลการแข่งขันย้อนหลัง
```sql
- match_id (INTEGER PRIMARY KEY)
- league_key (TEXT)
- season (INTEGER)
- match_date (DATE)
- home_team_id, away_team_id (INTEGER)
- home_score, away_score (INTEGER)
- match_status (TEXT)
- home_odds, draw_odds, away_odds (REAL)
- over_25_odds, under_25_odds (REAL)
- home_corners, away_corners (INTEGER)
- home_corners_1st, away_corners_1st (INTEGER)
- home_yellow_cards, away_yellow_cards (INTEGER)
- home_red_cards, away_red_cards (INTEGER)
- referee, venue (TEXT)
```

#### 4. **team_stats** - สถิติทีม (คำนวณจาก matches)
```sql
- team_id (INTEGER)
- league_key (TEXT)
- season (INTEGER)
- matches_played, wins, draws, losses (INTEGER)
- goals_for, goals_against (INTEGER)
- home_wins, home_draws, home_losses (INTEGER)
- away_wins, away_draws, away_losses (INTEGER)
- avg_corners_for, avg_corners_against (REAL)
- elo_rating (REAL DEFAULT 1500)
- form_last_5 (TEXT)
```

#### 5. **predictions** - บันทึกการทำนาย
```sql
- match_id (INTEGER)
- prediction_date (TIMESTAMP)
- predicted_result, predicted_over_under (TEXT)
- predicted_corners_1st, predicted_corners_total (TEXT)
- confidence_result, confidence_over_under, confidence_corners (REAL)
- actual_result, actual_over_under (TEXT)
- actual_corners_1st, actual_corners_total (INTEGER)
- result_correct, over_under_correct, corners_correct (BOOLEAN)
- model_version (TEXT)
```

---

## 🚀 Quick Start

### 1. Database Setup
```bash
# Option 1: Quick setup with sample data
python3 setup_multi_league_database.py
# Choose option 1

# Option 2: Full setup with real API data
python3 setup_multi_league_database.py  
# Choose option 2, enter API key
```

### 2. Train Multi-League Model
```python
from enhanced_multi_league_predictor import EnhancedMultiLeaguePredictor

# Initialize predictor
predictor = EnhancedMultiLeaguePredictor()

# Load data from all leagues
data = predictor.load_multi_league_data()

# Engineer features
data = predictor.engineer_features(data)

# Train models
predictor.train_models(data)

# Save models
predictor.save_models()
```

### 3. Make Predictions
```python
# Example prediction
home_stats = {
    'elo': 1600,
    'win_rate': 0.6,
    'goal_avg': 2.0,
    'attack_strength': 1.2,
    'defense_strength': 0.8
}

away_stats = {
    'elo': 1500,
    'win_rate': 0.4,
    'goal_avg': 1.5,
    'attack_strength': 0.9,
    'defense_strength': 1.1
}

prediction = predictor.predict_match(home_stats, away_stats, 'premier_league')
print(f"Result: {prediction['match_result']['prediction']}")
print(f"Over/Under: {prediction['over_under']['prediction']}")
```

---

## 🔧 Advanced Features

### 1. **League Weighting System**
- Premier League: 1.2 (highest quality)
- La Liga, Bundesliga, Serie A: 1.1 (top leagues)
- Ligue 1: 1.0 (standard)
- J-League 2: 0.9 (lower division)

### 2. **Advanced Feature Engineering**
```python
# ELO-based features
- elo_difference: Home ELO - Away ELO

# Team form features  
- home_win_rate, away_win_rate
- home_goal_avg, away_goal_avg

# Attack/Defense strength
- home_attack_strength, home_defense_strength
- away_attack_strength, away_defense_strength

# League-specific features
- league_weight, is_top_league, league_encoded
```

### 3. **Ensemble ML Models**
```python
# Match Result Prediction
- RandomForestClassifier
- GradientBoostingClassifier  
- ExtraTreesClassifier
- LogisticRegression
- VotingClassifier (soft voting)

# Over/Under Prediction
- Same ensemble approach
- Separate model for better specialization
```

---

## 📊 Performance Expectations

### Expected Accuracy by League:
- **Premier League**: 60-65% (high quality data)
- **La Liga**: 58-63% (tactical league)
- **Bundesliga**: 57-62% (high-scoring)
- **Serie A**: 55-60% (defensive)
- **Ligue 1**: 54-59% (PSG dominance)
- **J-League 2**: 50-55% (lower division)

### Overall System Performance:
- **Match Result**: 55-60% (improved from single league)
- **Over/Under**: 65-70% (strong with more data)
- **Combined Accuracy**: 60-65%

---

## 🔄 Data Management Workflow

### 1. **Initial Setup**
```bash
# Create database structure
python3 multi_league_database_manager.py

# Populate with historical data
db_manager.setup_all_leagues()
```

### 2. **Regular Updates**
```python
# Update with new matches (weekly)
for league_key in leagues:
    db_manager.fetch_and_store_matches(league_key, current_season)
    db_manager.calculate_team_statistics(league_key, current_season)
```

### 3. **Model Retraining**
```python
# Retrain models (monthly)
predictor = EnhancedMultiLeaguePredictor()
data = predictor.load_multi_league_data()
data = predictor.engineer_features(data)
predictor.train_models(data)
predictor.save_models()
```

---

## 📈 Benefits of Multi-League System

### 1. **Increased Data Volume**
- More training samples → Better model performance
- Cross-league patterns → Improved generalization
- Seasonal variations → Robust predictions

### 2. **League-Specific Insights**
- Different playing styles and patterns
- Varying levels of competitiveness
- Cultural and tactical differences

### 3. **Enhanced Feature Engineering**
- League quality weighting
- Cross-league team comparisons
- Meta-features from multiple competitions

### 4. **Better Accuracy**
- Expected 5-10% improvement over single league
- More reliable Over/Under predictions
- Reduced overfitting to specific league patterns

---

## 🛠️ Maintenance & Monitoring

### 1. **Database Maintenance**
```sql
-- Check data quality
SELECT league_key, COUNT(*) as matches, 
       MIN(match_date) as earliest, MAX(match_date) as latest
FROM matches GROUP BY league_key;

-- Monitor prediction accuracy
SELECT model_version, 
       AVG(CASE WHEN result_correct THEN 1.0 ELSE 0.0 END) as accuracy
FROM predictions GROUP BY model_version;
```

### 2. **Performance Monitoring**
```python
# Regular backtesting
performance = predictor.backtest_performance(recent_data)
print(f"Current accuracy: {performance['overall_accuracy']:.3f}")

# Feature importance analysis
predictor._analyze_feature_importance(data)
```

### 3. **Model Updates**
- Retrain monthly with new data
- A/B test new features
- Monitor for concept drift
- Update league weights based on performance

---

## 🎯 Next Steps

### 1. **Immediate Improvements**
- Add corner predictions (1st half, full match)
- Include card predictions (yellow/red)
- Add referee influence analysis

### 2. **Advanced Features**
- Player injury data integration
- Weather condition analysis
- Head-to-head historical records
- Market odds integration

### 3. **System Expansion**
- Add more leagues (Championship, Eredivisie, etc.)
- Include cup competitions
- Real-time prediction updates
- Web dashboard for monitoring

---

## 📞 Usage Examples

### Database Manager
```python
from multi_league_database_manager import MultiLeagueDBManager

# Initialize
db_manager = MultiLeagueDBManager(api_key="your_key")

# Get summary
summary = db_manager.get_league_summary()

# Export data
df = db_manager.export_league_data('premier_league', 2024, 'pl_data.csv')
```

### Enhanced Predictor
```python
from enhanced_multi_league_predictor import EnhancedMultiLeaguePredictor

# Initialize and train
predictor = EnhancedMultiLeaguePredictor()
data = predictor.load_multi_league_data()
data = predictor.engineer_features(data)
predictor.train_models(data)

# Make prediction
prediction = predictor.predict_match(home_stats, away_stats, 'la_liga')
```

---

**🚀 Ready to build the ultimate multi-league football prediction system!**
