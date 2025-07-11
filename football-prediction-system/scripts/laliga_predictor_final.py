#!/usr/bin/env python3
"""
🇪🇸 La Liga Predictor - Final Methods
ส่วนสุดท้ายของระบบทำนาย La Liga
"""

# Helper methods สำหรับ LaLigaPredictor (ต่อจาก laliga_predictor_complete.py)

def create_laliga_features(self, matches_df):
    """สร้าง Features สำหรับ La Liga"""
    print("🔧 กำลังสร้าง La Liga Advanced Features...")
    
    features = []
    
    for idx, match in matches_df.iterrows():
        home_team = match['home_team']
        away_team = match['away_team']
        match_date = pd.to_datetime(match['date'])
        
        # ข้อมูลก่อนหน้า
        prev_matches = matches_df[matches_df['date'] < match_date]
        
        if len(prev_matches) < 10:
            continue
        
        # คำนวณ features
        feature_dict = {}
        
        # ELO Ratings
        if hasattr(self, 'team_ratings'):
            feature_dict['home_elo'] = self.team_ratings.get(home_team, 1500)
            feature_dict['away_elo'] = self.team_ratings.get(away_team, 1500)
            feature_dict['elo_diff'] = feature_dict['home_elo'] - feature_dict['away_elo']
        
        # Recent Form
        home_recent = self._get_recent_form(prev_matches, home_team, 5)
        away_recent = self._get_recent_form(prev_matches, away_team, 5)
        
        feature_dict['home_recent_points'] = home_recent['points']
        feature_dict['away_recent_points'] = away_recent['points']
        feature_dict['home_recent_goals_for'] = home_recent['goals_for']
        feature_dict['away_recent_goals_for'] = away_recent['goals_for']
        feature_dict['home_recent_goals_against'] = home_recent['goals_against']
        feature_dict['away_recent_goals_against'] = away_recent['goals_against']
        
        # Season Form
        home_season = self._get_season_form(prev_matches, home_team)
        away_season = self._get_season_form(prev_matches, away_team)
        
        feature_dict['home_season_points_per_game'] = home_season['ppg']
        feature_dict['away_season_points_per_game'] = away_season['ppg']
        feature_dict['home_season_goals_per_game'] = home_season['gpg']
        feature_dict['away_season_goals_per_game'] = away_season['gpg']
        
        # Head to Head
        h2h = self._get_head_to_head(prev_matches, home_team, away_team)
        feature_dict['h2h_home_wins'] = h2h['home_wins']
        feature_dict['h2h_away_wins'] = h2h['away_wins']
        feature_dict['h2h_draws'] = h2h['draws']
        
        # Home/Away Performance
        home_home_form = self._get_home_away_form(prev_matches, home_team, 'home')
        away_away_form = self._get_home_away_form(prev_matches, away_team, 'away')
        
        feature_dict['home_home_ppg'] = home_home_form['ppg']
        feature_dict['away_away_ppg'] = away_away_form['ppg']
        
        # Momentum
        feature_dict['home_momentum'] = self._calculate_momentum(prev_matches, home_team)
        feature_dict['away_momentum'] = self._calculate_momentum(prev_matches, away_team)
        
        # Goals Statistics
        feature_dict['home_avg_goals_scored'] = home_season['goals_for'] / max(1, home_season['games'])
        feature_dict['away_avg_goals_scored'] = away_season['goals_for'] / max(1, away_season['games'])
        feature_dict['home_avg_goals_conceded'] = home_season['goals_against'] / max(1, home_season['games'])
        feature_dict['away_avg_goals_conceded'] = away_season['goals_against'] / max(1, away_season['games'])
        
        # Strength
        feature_dict['home_attack_strength'] = feature_dict['home_avg_goals_scored'] / 1.5
        feature_dict['away_attack_strength'] = feature_dict['away_avg_goals_scored'] / 1.5
        feature_dict['home_defense_strength'] = 1.5 / max(0.1, feature_dict['home_avg_goals_conceded'])
        feature_dict['away_defense_strength'] = 1.5 / max(0.1, feature_dict['away_avg_goals_conceded'])
        
        # Match Context
        feature_dict['days_since_last_match_home'] = self._days_since_last_match(prev_matches, home_team, match_date)
        feature_dict['days_since_last_match_away'] = self._days_since_last_match(prev_matches, away_team, match_date)
        
        # League Position
        feature_dict['home_league_position'] = self._get_league_position(prev_matches, home_team)
        feature_dict['away_league_position'] = self._get_league_position(prev_matches, away_team)
        
        # Target
        if match['home_goals'] > match['away_goals']:
            target = 'Home Win'
        elif match['home_goals'] == match['away_goals']:
            target = 'Draw'
        else:
            target = 'Away Win'
        
        feature_dict['target'] = target
        features.append(feature_dict)
    
    features_df = pd.DataFrame(features)
    print(f"✅ สร้าง {len(features_df.columns)-1} La Liga Features สำเร็จ")
    
    return features_df

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

# Helper methods
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
        'gpg': goals_for / max(1, games), 'goals_for': goals_for, 'goals_against': goals_against
    }

def _get_head_to_head(self, matches_df, home_team, away_team):
    """Head to Head"""
    h2h_matches = matches_df[
        ((matches_df['home_team'] == home_team) & (matches_df['away_team'] == away_team)) |
        ((matches_df['home_team'] == away_team) & (matches_df['away_team'] == home_team))
    ]
    
    home_wins = away_wins = draws = 0
    
    for _, match in h2h_matches.iterrows():
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
    
    return {'home_wins': home_wins, 'away_wins': away_wins, 'draws': draws}

def _get_home_away_form(self, matches_df, team, venue):
    """Home/Away form"""
    if venue == 'home':
        team_matches = matches_df[matches_df['home_team'] == team]
    else:
        team_matches = matches_df[matches_df['away_team'] == team]
    
    points = games = 0
    
    for _, match in team_matches.iterrows():
        games += 1
        if venue == 'home':
            if match['home_goals'] > match['away_goals']:
                points += 3
            elif match['home_goals'] == match['away_goals']:
                points += 1
        else:
            if match['away_goals'] > match['home_goals']:
                points += 3
            elif match['away_goals'] == match['home_goals']:
                points += 1
    
    return {'ppg': points / max(1, games)}

def _calculate_momentum(self, matches_df, team):
    """Momentum calculation"""
    recent_matches = matches_df[
        (matches_df['home_team'] == team) | (matches_df['away_team'] == team)
    ].tail(3)
    
    momentum = 0
    weight = 3
    
    for _, match in recent_matches.iterrows():
        if match['home_team'] == team:
            if match['home_goals'] > match['away_goals']:
                momentum += weight * 3
            elif match['home_goals'] == match['away_goals']:
                momentum += weight * 1
        else:
            if match['away_goals'] > match['home_goals']:
                momentum += weight * 3
            elif match['away_goals'] == match['home_goals']:
                momentum += weight * 1
        weight -= 1
    
    return momentum

def _days_since_last_match(self, matches_df, team, current_date):
    """Days since last match"""
    team_matches = matches_df[
        (matches_df['home_team'] == team) | (matches_df['away_team'] == team)
    ]
    
    if len(team_matches) == 0:
        return 7
    
    last_match_date = team_matches['date'].max()
    return (current_date - last_match_date).days

def _get_league_position(self, matches_df, team):
    """League position"""
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

# รวม methods ทั้งหมดเข้าไปใน class
def create_complete_laliga_predictor():
    """สร้าง La Liga Predictor ฉบับสมบูรณ์"""
    
    # อ่านไฟล์หลัก
    with open('laliga_predictor_complete.py', 'r', encoding='utf-8') as f:
        main_code = f.read()
    
    # เพิ่ม methods
    additional_methods = '''
    # เพิ่ม methods เหล่านี้เข้าไปใน LaLigaPredictor class
    def create_laliga_features(self, matches_df):
        return create_laliga_features(self, matches_df)
    
    def _ensemble_predict(self, X):
        return _ensemble_predict(self, X)
    
    def _ensemble_predict_proba(self, X_sample):
        return _ensemble_predict_proba(self, X_sample)
    
    def _get_recent_form(self, matches_df, team, n_games):
        return _get_recent_form(self, matches_df, team, n_games)
    
    def _get_season_form(self, matches_df, team):
        return _get_season_form(self, matches_df, team)
    
    def _get_head_to_head(self, matches_df, home_team, away_team):
        return _get_head_to_head(self, matches_df, home_team, away_team)
    
    def _get_home_away_form(self, matches_df, team, venue):
        return _get_home_away_form(self, matches_df, team, venue)
    
    def _calculate_momentum(self, matches_df, team):
        return _calculate_momentum(self, matches_df, team)
    
    def _days_since_last_match(self, matches_df, team, current_date):
        return _days_since_last_match(self, matches_df, team, current_date)
    
    def _get_league_position(self, matches_df, team):
        return _get_league_position(self, matches_df, team)

# Test function
def main():
    """ทดสอบระบบ La Liga Predictor"""
    print("🇪🇸 La Liga Advanced Predictor - Test")
    print("=" * 50)
    
    # สร้าง predictor
    predictor = LaLigaPredictor()
    
    # โหลดข้อมูล
    data = predictor.load_laliga_data()
    
    # เทรนโมเดล
    success = predictor.train_ensemble_models(data)
    
    if success:
        print("\\n🎯 ทดสอบการทำนาย:")
        
        # ทดสอบการทำนาย
        test_matches = [
            ('Real Madrid', 'FC Barcelona'),
            ('Atletico Madrid', 'Real Sociedad'),
            ('Sevilla FC', 'Valencia CF')
        ]
        
        for home, away in test_matches:
            result = predictor.predict_match_laliga(home, away)
            if result:
                print(f"   {home} vs {away}: {result['prediction']} ({result['confidence']:.1%})")
        
        print("\\n✅ ระบบ La Liga Predictor พร้อมใช้งาน!")
    else:
        print("❌ การเทรนไม่สำเร็จ")

if __name__ == "__main__":
    main()
'''
    
    # รวมโค้ด
    complete_code = main_code + additional_methods
    
    # บันทึกไฟล์สมบูรณ์
    with open('laliga_predictor_complete_final.py', 'w', encoding='utf-8') as f:
        f.write(complete_code)
    
    print("✅ สร้าง La Liga Predictor ฉบับสมบูรณ์เรียบร้อย")

if __name__ == "__main__":
    create_complete_laliga_predictor()
