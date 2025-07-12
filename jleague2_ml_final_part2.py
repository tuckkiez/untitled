    def create_advanced_features(self, home_team: str, away_team: str) -> np.ndarray:
        """สร้าง Features ขั้นสูงสำหรับการทำนาย"""
        if home_team not in self.team_stats or away_team not in self.team_stats:
            return np.array([0.5] * 20)  # ลดจำนวน features
        
        home_stats = self.team_stats[home_team]
        away_stats = self.team_stats[away_team]
        
        features = []
        
        # 1. ELO Rating Features
        features.extend([
            home_stats['elo_rating'] / 2000,
            away_stats['elo_rating'] / 2000,
            (home_stats['elo_rating'] - away_stats['elo_rating']) / 400
        ])
        
        # 2. Goal Statistics
        home_matches = max(1, home_stats['matches_played'])
        away_matches = max(1, away_stats['matches_played'])
        
        features.extend([
            home_stats['goals_for'] / home_matches,
            home_stats['goals_against'] / home_matches,
            away_stats['goals_for'] / away_matches,
            away_stats['goals_against'] / away_matches,
            (home_stats['goals_for'] - home_stats['goals_against']) / home_matches,
            (away_stats['goals_for'] - away_stats['goals_against']) / away_matches
        ])
        
        # 3. Win/Draw/Loss Ratios
        features.extend([
            home_stats['wins'] / home_matches,
            home_stats['draws'] / home_matches,
            away_stats['wins'] / away_matches,
            away_stats['draws'] / away_matches
        ])
        
        # 4. Recent Form
        home_form_points = sum([3 if x=='W' else 1 if x=='D' else 0 for x in home_stats['recent_form'][-5:]])
        away_form_points = sum([3 if x=='W' else 1 if x=='D' else 0 for x in away_stats['recent_form'][-5:]])
        
        features.extend([
            home_form_points / 15,
            away_form_points / 15
        ])
        
        # 5. Corner Statistics
        features.extend([
            home_stats['corners_for'] / home_matches,
            home_stats['corners_against'] / home_matches,
            away_stats['corners_for'] / away_matches,
            away_stats['corners_against'] / away_matches
        ])
        
        return np.array(features)
    
    def prepare_training_data(self, fixtures: List[Dict]) -> Tuple[np.ndarray, Dict]:
        """เตรียมข้อมูลสำหรับการเทรน"""
        print("🔧 กำลังเตรียมข้อมูลสำหรับการเทรน...")
        
        X = []
        y = {
            'match_result': [],
            'handicap': [],
            'over_under': [],
            'corner_1st_half': [],
            'corner_2nd_half': []
        }
        
        # เรียงตามวันที่
        sorted_fixtures = sorted(fixtures, key=lambda x: x['fixture']['date'])
        
        # ใช้ข้อมูลทั้งหมดในการคำนวณสถิติ
        self.calculate_team_statistics(sorted_fixtures)
        
        for fixture in sorted_fixtures:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_goals = fixture['goals']['home'] or 0
            away_goals = fixture['goals']['away'] or 0
            
            # สร้าง features
            features = self.create_advanced_features(home_team, away_team)
            X.append(features)
            
            # Labels
            # 1. Match Result
            if home_goals > away_goals:
                y['match_result'].append(2)  # Home Win
            elif home_goals < away_goals:
                y['match_result'].append(0)  # Away Win
            else:
                y['match_result'].append(1)  # Draw
            
            # 2. Handicap
            y['handicap'].append(y['match_result'][-1])
            
            # 3. Over/Under 2.5
            total_goals = home_goals + away_goals
            y['over_under'].append(1 if total_goals > 2.5 else 0)
            
            # 4. Corner 1st Half (จำลอง)
            estimated_corners_1st = max(2, min(8, 3 + total_goals * 0.8 + np.random.normal(0, 1)))
            y['corner_1st_half'].append(1 if estimated_corners_1st > 5 else 0)
            
            # 5. Corner 2nd Half (จำลอง)
            estimated_corners_2nd = max(2, min(10, 4 + total_goals * 1.0 + np.random.normal(0, 1)))
            y['corner_2nd_half'].append(1 if estimated_corners_2nd > 5 else 0)
        
        return np.array(X), y
    
    def train_models(self, fixtures: List[Dict]):
        """เทรนโมเดล ML ทั้งหมด"""
        print("🤖 กำลังเทรนโมเดล Advanced ML...")
        
        # เตรียมข้อมูลเทรน
        X, y = self.prepare_training_data(fixtures)
        
        if len(X) == 0:
            print("❌ ไม่มีข้อมูลสำหรับการเทรน")
            return
        
        print(f"📊 ข้อมูลเทรน: {len(X)} samples, {len(X[0])} features")
        
        # เทรนแต่ละโมเดล
        for target_name, target_values in y.items():
            print(f"🔧 กำลังเทรนโมเดล {target_name}...")
            
            try:
                # Scale features
                X_scaled = self.scalers[target_name].fit_transform(X)
                
                # เทรนโมเดล
                self.models[target_name].fit(X_scaled, target_values)
                
                # Cross-validation score
                cv_scores = cross_val_score(
                    self.models[target_name], X_scaled, target_values, 
                    cv=3, scoring='accuracy'
                )
                
                print(f"   ✅ {target_name}: CV Score = {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
            except Exception as e:
                print(f"   ❌ {target_name}: Error = {e}")
        
        self.is_trained = True
        print("🎉 การเทรนเสร็จสิ้น!")
    
    def predict_match(self, home_team: str, away_team: str) -> Dict:
        """ทำนายการแข่งขัน 5 ค่า"""
        if not self.is_trained:
            print("❌ โมเดลยังไม่ได้เทรน")
            return {}
        
        # สร้าง features
        features = self.create_advanced_features(home_team, away_team).reshape(1, -1)
        
        predictions = {}
        
        for target_name, model in self.models.items():
            try:
                # Scale features
                features_scaled = self.scalers[target_name].transform(features)
                
                # ทำนาย
                pred_class = model.predict(features_scaled)[0]
                pred_proba = model.predict_proba(features_scaled)[0]
                
                predictions[target_name] = {
                    'prediction': pred_class,
                    'probabilities': pred_proba,
                    'confidence': max(pred_proba)
                }
            except Exception as e:
                print(f"❌ Error predicting {target_name}: {e}")
                predictions[target_name] = {
                    'prediction': 1,
                    'probabilities': [0.33, 0.34, 0.33],
                    'confidence': 0.34
                }
        
        # แปลงผลลัพธ์
        result = {
            'home_team': home_team,
            'away_team': away_team,
            'match_result': self._interpret_match_result(predictions['match_result']),
            'handicap': self._interpret_handicap(predictions['handicap']),
            'over_under': self._interpret_over_under(predictions['over_under']),
            'corner_1st_half': self._interpret_corner(predictions['corner_1st_half'], '1st Half'),
            'corner_2nd_half': self._interpret_corner(predictions['corner_2nd_half'], '2nd Half'),
            'confidence_scores': {
                'match_result': predictions['match_result']['confidence'],
                'handicap': predictions['handicap']['confidence'],
                'over_under': predictions['over_under']['confidence'],
                'corner_1st_half': predictions['corner_1st_half']['confidence'],
                'corner_2nd_half': predictions['corner_2nd_half']['confidence']
            }
        }
        
        return result
    
    def _interpret_match_result(self, pred_data: Dict) -> Dict:
        """แปลผลการทำนายผลการแข่งขัน"""
        class_names = ['Away Win', 'Draw', 'Home Win']
        pred_class = pred_data['prediction']
        probabilities = pred_data['probabilities']
        
        return {
            'prediction': class_names[pred_class],
            'home_win_prob': probabilities[2] if len(probabilities) > 2 else 0.33,
            'draw_prob': probabilities[1] if len(probabilities) > 1 else 0.34,
            'away_win_prob': probabilities[0] if len(probabilities) > 0 else 0.33,
            'confidence': pred_data['confidence']
        }
    
    def _interpret_handicap(self, pred_data: Dict) -> Dict:
        """แปลผลการทำนาย Handicap"""
        class_names = ['Away Win', 'Draw', 'Home Win']
        pred_class = pred_data['prediction']
        
        return {
            'prediction': class_names[pred_class],
            'confidence': pred_data['confidence']
        }
    
    def _interpret_over_under(self, pred_data: Dict) -> Dict:
        """แปลผลการทำนาย Over/Under"""
        pred_class = pred_data['prediction']
        probabilities = pred_data['probabilities']
        
        return {
            'prediction': 'Over 2.5' if pred_class == 1 else 'Under 2.5',
            'over_prob': probabilities[1] if len(probabilities) > 1 else 0.5,
            'under_prob': probabilities[0] if len(probabilities) > 1 else 0.5,
            'confidence': pred_data['confidence']
        }
    
    def _interpret_corner(self, pred_data: Dict, half: str) -> Dict:
        """แปลผลการทำนาย Corner"""
        pred_class = pred_data['prediction']
        probabilities = pred_data['probabilities']
        
        return {
            'prediction': f'Over 5 ({half})' if pred_class == 1 else f'Under 5 ({half})',
            'over_prob': probabilities[1] if len(probabilities) > 1 else 0.5,
            'under_prob': probabilities[0] if len(probabilities) > 1 else 0.5,
            'confidence': pred_data['confidence']
        }
