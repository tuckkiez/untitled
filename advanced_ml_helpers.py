#!/usr/bin/env python3
"""
Helper methods สำหรับ Advanced ML Predictor
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Helper methods สำหรับ Advanced ML Predictor
def _get_recent_form(self, matches_df, team, n_games):
    """คำนวณฟอร์มล่าสุด"""
    team_matches = matches_df[
        (matches_df['home_team'] == team) | (matches_df['away_team'] == team)
    ].tail(n_games)
    
    points = goals_for = goals_against = 0
    
    for _, match in team_matches.iterrows():
        if match['home_team'] == team:
            goals_for += match['home_goals']
            goals_against += match['away_goals']
            if match['home_goals'] > match['away_goals']:
                points += 3
            elif match['home_goals'] == match['away_goals']:
                points += 1
        else:
            goals_for += match['away_goals']
            goals_against += match['home_goals']
            if match['away_goals'] > match['home_goals']:
                points += 3
            elif match['away_goals'] == match['home_goals']:
                points += 1
    
    return {'points': points, 'goals_for': goals_for, 'goals_against': goals_against}

def _get_season_form(self, matches_df, team):
    """คำนวณฟอร์มทั้งฤดูกาล"""
    team_matches = matches_df[
        (matches_df['home_team'] == team) | (matches_df['away_team'] == team)
    ]
    
    points = goals_for = goals_against = games = 0
    
    for _, match in team_matches.iterrows():
        games += 1
        if match['home_team'] == team:
            goals_for += match['home_goals']
            goals_against += match['away_goals']
            if match['home_goals'] > match['away_goals']:
                points += 3
            elif match['home_goals'] == match['away_goals']:
                points += 1
        else:
            goals_for += match['away_goals']
            goals_against += match['home_goals']
            if match['away_goals'] > match['home_goals']:
                points += 3
            elif match['away_goals'] == match['home_goals']:
                points += 1
    
    return {
        'points': points, 'games': games, 'ppg': points / max(1, games),
        'goals_for': goals_for, 'goals_against': goals_against
    }

def _get_clean_sheets(self, matches_df, team, venue):
    """คำนวณ Clean Sheets"""
    if venue == 'home':
        team_matches = matches_df[matches_df['home_team'] == team]
        clean_sheets = len(team_matches[team_matches['away_goals'] == 0])
    else:
        team_matches = matches_df[matches_df['away_team'] == team]
        clean_sheets = len(team_matches[team_matches['home_goals'] == 0])
    
    return clean_sheets

def _get_head_to_head_extended(self, matches_df, home_team, away_team):
    """Head to Head แบบขยาย"""
    h2h_matches = matches_df[
        ((matches_df['home_team'] == home_team) & (matches_df['away_team'] == away_team)) |
        ((matches_df['home_team'] == away_team) & (matches_df['away_team'] == home_team))
    ]
    
    home_wins = away_wins = draws = total_goals = 0
    
    for _, match in h2h_matches.iterrows():
        total_goals += match['home_goals'] + match['away_goals']
        
        if match['home_team'] == home_team:
            if match['home_goals'] > match['away_goals']:
                home_wins += 1
            elif match['home_goals'] == match['away_goals']:
                draws += 1
            else:
                away_wins += 1
        else:
            if match['away_goals'] > match['home_goals']:
                home_wins += 1
            elif match['away_goals'] == match['home_goals']:
                draws += 1
            else:
                away_wins += 1
    
    avg_goals = total_goals / max(1, len(h2h_matches))
    
    return {
        'home_wins': home_wins, 'away_wins': away_wins, 'draws': draws,
        'avg_goals': avg_goals
    }

def _calculate_advanced_momentum(self, matches_df, team):
    """คำนวณ Advanced Momentum"""
    recent_matches = matches_df[
        (matches_df['home_team'] == team) | (matches_df['away_team'] == team)
    ].tail(5)
    
    momentum = 0
    weight = 5
    
    for _, match in recent_matches.iterrows():
        points = 0
        if match['home_team'] == team:
            if match['home_goals'] > match['away_goals']:
                points = 3
            elif match['home_goals'] == match['away_goals']:
                points = 1
        else:
            if match['away_goals'] > match['home_goals']:
                points = 3
            elif match['away_goals'] == match['home_goals']:
                points = 1
        
        momentum += weight * points
        weight -= 1
    
    return momentum / 45  # Normalize

def _calculate_trend(self, matches_df, team):
    """คำนวณแนวโน้ม (Trend)"""
    team_matches = matches_df[
        (matches_df['home_team'] == team) | (matches_df['away_team'] == team)
    ].tail(10)
    
    if len(team_matches) < 5:
        return 0
    
    # แบ่งเป็น 2 ช่วง
    first_half = team_matches.iloc[:5]
    second_half = team_matches.iloc[5:]
    
    def get_points(matches, team):
        points = 0
        for _, match in matches.iterrows():
            if match['home_team'] == team:
                if match['home_goals'] > match['away_goals']:
                    points += 3
                elif match['home_goals'] == match['away_goals']:
                    points += 1
            else:
                if match['away_goals'] > match['home_goals']:
                    points += 3
                elif match['away_goals'] == match['home_goals']:
                    points += 1
        return points
    
    first_points = get_points(first_half, team)
    second_points = get_points(second_half, team)
    
    return (second_points - first_points) / 15  # Normalize

def _days_since_last_match(self, matches_df, team, current_date):
    """วันที่ผ่านมาตั้งแต่เกมล่าสุด"""
    team_matches = matches_df[
        (matches_df['home_team'] == team) | (matches_df['away_team'] == team)
    ]
    
    if len(team_matches) == 0:
        return 7
    
    last_match_date = team_matches['date'].max()
    return (current_date - last_match_date).days

def _get_league_position(self, matches_df, team):
    """ตำแหน่งในลีก"""
    teams = set(matches_df['home_team'].unique()) | set(matches_df['away_team'].unique())
    table = {}
    
    for t in teams:
        season_form = self._get_season_form(matches_df, t)
        table[t] = season_form['points']
    
    sorted_teams = sorted(table.items(), key=lambda x: x[1], reverse=True)
    
    for pos, (t, points) in enumerate(sorted_teams, 1):
        if t == team:
            return pos
    
    return 10

def _ensemble_predict(self, X):
    """Ensemble prediction"""
    predictions = []
    
    for sample in X:
        sample_preds = []
        for name, model in self.trained_models.items():
            pred = model.predict([sample])[0]
            weight = self.ensemble_weights[name]
            sample_preds.append((pred, weight))
        
        # Weighted voting
        vote_counts = {}
        for pred, weight in sample_preds:
            vote_counts[pred] = vote_counts.get(pred, 0) + weight
        
        final_pred = max(vote_counts.items(), key=lambda x: x[1])[0]
        predictions.append(final_pred)
    
    return np.array(predictions)

def _ensemble_predict_proba(self, X_sample):
    """Ensemble probability prediction"""
    class_probs = {'Away Win': 0, 'Draw': 0, 'Home Win': 0}
    
    for name, model in self.trained_models.items():
        proba = model.predict_proba([X_sample])[0]
        weight = self.ensemble_weights[name]
        
        classes = model.classes_
        for i, class_name in enumerate(classes):
            class_probs[class_name] += proba[i] * weight
    
    # Normalize
    total = sum(class_probs.values())
    if total > 0:
        for key in class_probs:
            class_probs[key] /= total
    
    return [class_probs['Away Win'], class_probs['Draw'], class_probs['Home Win']]

def predict_comprehensive(self, home_team, away_team):
    """ทำนายครบถ้วน: ผลการแข่งขัน + Handicap + Over/Under + Corners"""
    if not self.is_trained:
        print("❌ โมเดลยังไม่ได้เทรน!")
        return None
    
    print(f"🔧 กำลังทำนายครบถ้วน {home_team} vs {away_team}...")
    
    # สร้าง features สำหรับการทำนาย
    feature_dict = self._create_prediction_features(home_team, away_team)
    
    if not feature_dict:
        return None
    
    # แปลงเป็น DataFrame
    X_pred = pd.DataFrame([feature_dict])
    
    # Preprocessing
    X_processed = self.imputer.transform(X_pred)
    X_processed = self.scaler.transform(X_processed)
    X_selected = self.feature_selector.transform(X_processed)
    
    # ทำนายผลการแข่งขัน
    match_probabilities = self._ensemble_predict_proba(X_selected[0])
    classes = ['Away Win', 'Draw', 'Home Win']
    max_prob_idx = np.argmax(match_probabilities)
    match_prediction = classes[max_prob_idx]
    match_confidence = match_probabilities[max_prob_idx]
    
    # ทำนาย Handicap
    if 'rf' in self.handicap_models:
        handicap_pred = self.handicap_models['rf'].predict(X_selected)[0]
        handicap_proba = self.handicap_models['rf'].predict_proba(X_selected)[0]
        handicap_confidence = max(handicap_proba)
    else:
        handicap_pred = "Home Win"
        handicap_confidence = 0.5
    
    # ทำนาย Over/Under
    if 'gb' in self.ou_models:
        ou_pred = self.ou_models['gb'].predict(X_selected)[0]
        ou_proba = self.ou_models['gb'].predict_proba(X_selected)[0]
        ou_confidence = max(ou_proba)
    else:
        ou_pred = "Under"
        ou_confidence = 0.5
    
    # ทำนาย Corners
    corners_total_pred = "Under"
    corners_fh_pred = "Under"
    corners_confidence = 0.5
    
    if 'total' in self.corners_models and 'first_half' in self.corners_models:
        corners_total_pred = self.corners_models['total'].predict(X_selected)[0]
        corners_fh_pred = self.corners_models['first_half'].predict(X_selected)[0]
        
        total_proba = self.corners_models['total'].predict_proba(X_selected)[0]
        fh_proba = self.corners_models['first_half'].predict_proba(X_selected)[0]
        corners_confidence = (max(total_proba) + max(fh_proba)) / 2
    
    return {
        'match_result': {
            'prediction': match_prediction,
            'confidence': match_confidence,
            'probabilities': {
                'Home Win': match_probabilities[2],
                'Draw': match_probabilities[1],
                'Away Win': match_probabilities[0]
            }
        },
        'handicap': {
            'prediction': handicap_pred,
            'confidence': handicap_confidence
        },
        'over_under': {
            'prediction': ou_pred,
            'confidence': ou_confidence
        },
        'corners': {
            'total_prediction': corners_total_pred,
            'first_half_prediction': corners_fh_pred,
            'confidence': corners_confidence
        }
    }

def _create_prediction_features(self, home_team, away_team):
    """สร้าง features สำหรับการทำนาย"""
    if not hasattr(self, 'historical_data'):
        return {}
    
    matches_df = self.historical_data
    current_date = datetime.now()
    
    feature_dict = {}
    
    # ELO Ratings
    feature_dict['home_elo'] = self.team_ratings.get(home_team, 1500)
    feature_dict['away_elo'] = self.team_ratings.get(away_team, 1500)
    feature_dict['elo_diff'] = feature_dict['home_elo'] - feature_dict['away_elo']
    feature_dict['elo_ratio'] = feature_dict['home_elo'] / max(1, feature_dict['away_elo'])
    
    # Recent Form (Multiple periods)
    for period in [3, 5, 10]:
        home_recent = self._get_recent_form(matches_df, home_team, period)
        away_recent = self._get_recent_form(matches_df, away_team, period)
        
        feature_dict[f'home_recent_{period}_points'] = home_recent['points']
        feature_dict[f'away_recent_{period}_points'] = away_recent['points']
        feature_dict[f'home_recent_{period}_goals_for'] = home_recent['goals_for']
        feature_dict[f'away_recent_{period}_goals_for'] = away_recent['goals_for']
        feature_dict[f'home_recent_{period}_goals_against'] = home_recent['goals_against']
        feature_dict[f'away_recent_{period}_goals_against'] = away_recent['goals_against']
    
    # Season Form
    home_season = self._get_season_form(matches_df, home_team)
    away_season = self._get_season_form(matches_df, away_team)
    
    feature_dict['home_season_ppg'] = home_season['ppg']
    feature_dict['away_season_ppg'] = away_season['ppg']
    feature_dict['home_goals_per_game'] = home_season['goals_for'] / max(1, home_season['games'])
    feature_dict['away_goals_per_game'] = away_season['goals_for'] / max(1, away_season['games'])
    feature_dict['home_goals_against_per_game'] = home_season['goals_against'] / max(1, home_season['games'])
    feature_dict['away_goals_against_per_game'] = away_season['goals_against'] / max(1, away_season['games'])
    
    # Advanced Statistics
    feature_dict['home_goal_difference'] = home_season['goals_for'] - home_season['goals_against']
    feature_dict['away_goal_difference'] = away_season['goals_for'] - away_season['goals_against']
    feature_dict['home_clean_sheets'] = self._get_clean_sheets(matches_df, home_team, 'home')
    feature_dict['away_clean_sheets'] = self._get_clean_sheets(matches_df, away_team, 'away')
    
    # Head to Head
    h2h = self._get_head_to_head_extended(matches_df, home_team, away_team)
    feature_dict['h2h_home_wins'] = h2h['home_wins']
    feature_dict['h2h_away_wins'] = h2h['away_wins']
    feature_dict['h2h_draws'] = h2h['draws']
    feature_dict['h2h_avg_goals'] = h2h['avg_goals']
    
    # Momentum & Trends
    feature_dict['home_momentum'] = self._calculate_advanced_momentum(matches_df, home_team)
    feature_dict['away_momentum'] = self._calculate_advanced_momentum(matches_df, away_team)
    feature_dict['home_trend'] = self._calculate_trend(matches_df, home_team)
    feature_dict['away_trend'] = self._calculate_trend(matches_df, away_team)
    
    # Match Context
    feature_dict['days_since_last_match_home'] = self._days_since_last_match(matches_df, home_team, current_date)
    feature_dict['days_since_last_match_away'] = self._days_since_last_match(matches_df, away_team, current_date)
    feature_dict['home_league_position'] = self._get_league_position(matches_df, home_team)
    feature_dict['away_league_position'] = self._get_league_position(matches_df, away_team)
    
    return feature_dict

# เพิ่ม methods เข้าไปใน AdvancedMLPredictor class
def add_helper_methods():
    """เพิ่ม helper methods เข้าไปใน AdvancedMLPredictor"""
    from advanced_ml_predictor import AdvancedMLPredictor
    
    AdvancedMLPredictor._get_recent_form = _get_recent_form
    AdvancedMLPredictor._get_season_form = _get_season_form
    AdvancedMLPredictor._get_clean_sheets = _get_clean_sheets
    AdvancedMLPredictor._get_head_to_head_extended = _get_head_to_head_extended
    AdvancedMLPredictor._calculate_advanced_momentum = _calculate_advanced_momentum
    AdvancedMLPredictor._calculate_trend = _calculate_trend
    AdvancedMLPredictor._days_since_last_match = _days_since_last_match
    AdvancedMLPredictor._get_league_position = _get_league_position
    AdvancedMLPredictor._ensemble_predict = _ensemble_predict
    AdvancedMLPredictor._ensemble_predict_proba = _ensemble_predict_proba
    AdvancedMLPredictor.predict_comprehensive = predict_comprehensive
    AdvancedMLPredictor._create_prediction_features = _create_prediction_features

if __name__ == "__main__":
    add_helper_methods()
    print("✅ เพิ่ม helper methods สำหรับ Advanced ML Predictor สำเร็จ")
