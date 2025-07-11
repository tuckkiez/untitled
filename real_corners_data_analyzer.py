#!/usr/bin/env python3
"""
Real Corners Data Analyzer
วิเคราะห์ข้อมูล corners จริงจาก thestatsdontlie.com
"""

import pandas as pd
import numpy as np
from datetime import datetime

class RealCornersAnalyzer:
    def __init__(self):
        self.real_data = {
            'Aldosivi': {
                'team_corners_home': 5.2,
                'team_corners_away': 5.2,
                'team_corners_avg': 5.2,
                'match_corners_avg': 10.2,
                'over_9_5_pct': 60,
                'over_10_5_pct': 40
            },
            'Central Córdoba': {
                'team_corners_home': 4.8,
                'team_corners_away': 4.8,
                'team_corners_avg': 4.8,
                'match_corners_avg': 9.8,
                'over_9_5_pct': 40,
                'over_10_5_pct': 20
            }
        }
    
    def analyze_match_prediction(self, home_team, away_team):
        """วิเคราะห์การทำนาย corners สำหรับแมตช์"""
        
        if home_team not in self.real_data or away_team not in self.real_data:
            return None
            
        home_data = self.real_data[home_team]
        away_data = self.real_data[away_team]
        
        # คำนวณการทำนาย corners
        predicted_corners = (
            home_data['team_corners_home'] + 
            away_data['team_corners_away']
        )
        
        # คำนวณ Over/Under probabilities
        avg_over_9_5 = (home_data['over_9_5_pct'] + away_data['over_9_5_pct']) / 2
        avg_over_10_5 = (home_data['over_10_5_pct'] + away_data['over_10_5_pct']) / 2
        
        # เปรียบเทียบกับข้อมูลเฉลี่ยของแต่ละทีม
        match_avg = (home_data['match_corners_avg'] + away_data['match_corners_avg']) / 2
        
        analysis = {
            'predicted_corners': predicted_corners,
            'match_average': match_avg,
            'over_9_5_probability': avg_over_9_5,
            'over_10_5_probability': avg_over_10_5,
            'recommendation': self._get_recommendation(predicted_corners, avg_over_9_5, avg_over_10_5),
            'confidence_level': self._calculate_confidence(home_data, away_data)
        }
        
        return analysis
    
    def _get_recommendation(self, predicted, over_9_5_pct, over_10_5_pct):
        """ให้คำแนะนำการเดิมพัน"""
        recommendations = []
        
        if over_9_5_pct >= 50:
            recommendations.append(f"Over 9.5 corners ({over_9_5_pct}% probability)")
        else:
            recommendations.append(f"Under 9.5 corners ({100-over_9_5_pct}% probability)")
            
        if over_10_5_pct >= 40:
            recommendations.append(f"Consider Over 10.5 corners ({over_10_5_pct}% probability)")
        
        return recommendations
    
    def _calculate_confidence(self, home_data, away_data):
        """คำนวณระดับความมั่นใจ"""
        # ยิ่งข้อมูลสอดคล้องกัน ยิ่งมั่นใจ
        home_consistency = abs(home_data['team_corners_home'] - home_data['team_corners_away'])
        away_consistency = abs(away_data['team_corners_home'] - away_data['team_corners_away'])
        
        # ความแตกต่างน้อย = ความมั่นใจสูง
        avg_consistency = (home_consistency + away_consistency) / 2
        confidence = max(60, 90 - (avg_consistency * 10))
        
        return min(confidence, 95)
    
    def compare_with_previous_prediction(self, home_team, away_team, previous_prediction):
        """เปรียบเทียบกับการทำนายก่อนหน้า"""
        
        real_analysis = self.analyze_match_prediction(home_team, away_team)
        if not real_analysis:
            return None
            
        comparison = {
            'previous_prediction': previous_prediction,
            'real_data_analysis': real_analysis,
            'accuracy_assessment': self._assess_accuracy(previous_prediction, real_analysis),
            'updated_recommendation': self._get_updated_recommendation(real_analysis)
        }
        
        return comparison
    
    def _assess_accuracy(self, previous, real):
        """ประเมินความแม่นยำของการทำนายก่อนหน้า"""
        
        prev_corners = previous.get('predicted_corners', 0)
        real_corners = real['predicted_corners']
        
        difference = abs(prev_corners - real_corners)
        
        if difference <= 1:
            accuracy = "Very High"
        elif difference <= 2:
            accuracy = "High"
        elif difference <= 3:
            accuracy = "Medium"
        else:
            accuracy = "Low"
            
        return {
            'accuracy_level': accuracy,
            'difference': difference,
            'previous_corners': prev_corners,
            'real_data_corners': real_corners
        }
    
    def _get_updated_recommendation(self, analysis):
        """ให้คำแนะนำที่อัพเดทแล้ว"""
        
        corners = analysis['predicted_corners']
        over_9_5 = analysis['over_9_5_probability']
        confidence = analysis['confidence_level']
        
        if corners >= 10 and over_9_5 >= 50:
            return {
                'primary': f"Over 9.5 corners",
                'confidence': f"{over_9_5}%",
                'secondary': f"Total corners: ~{corners:.1f}",
                'risk_level': "Medium" if confidence >= 70 else "High"
            }
        else:
            return {
                'primary': f"Under 10.5 corners",
                'confidence': f"{100-analysis['over_10_5_probability']}%",
                'secondary': f"Total corners: ~{corners:.1f}",
                'risk_level': "Low" if confidence >= 80 else "Medium"
            }

def main():
    """ทดสอบการวิเคราะห์"""
    
    analyzer = RealCornersAnalyzer()
    
    # วิเคราะห์แมตช์ Aldosivi vs Central Córdoba
    print("🏆 Real Corners Data Analysis")
    print("=" * 50)
    
    analysis = analyzer.analyze_match_prediction("Aldosivi", "Central Córdoba")
    
    if analysis:
        print(f"📊 Match: Aldosivi vs Central Córdoba")
        print(f"🎯 Predicted Corners: {analysis['predicted_corners']:.1f}")
        print(f"📈 Match Average: {analysis['match_average']:.1f}")
        print(f"🔥 Over 9.5 Probability: {analysis['over_9_5_probability']}%")
        print(f"⚡ Over 10.5 Probability: {analysis['over_10_5_probability']}%")
        print(f"💪 Confidence Level: {analysis['confidence_level']:.1f}%")
        print("\n🎲 Recommendations:")
        for rec in analysis['recommendation']:
            print(f"   • {rec}")
    
    # เปรียบเทียบกับการทำนายก่อนหน้า
    print("\n" + "=" * 50)
    print("🔄 Comparison with Previous Prediction")
    
    previous_pred = {
        'predicted_corners': 13.3,
        'confidence': 88,
        'recommendation': 'Over 9.5 corners'
    }
    
    comparison = analyzer.compare_with_previous_prediction(
        "Aldosivi", "Central Córdoba", previous_pred
    )
    
    if comparison:
        acc = comparison['accuracy_assessment']
        print(f"📊 Previous Prediction: {acc['previous_corners']} corners")
        print(f"📈 Real Data Prediction: {acc['real_data_corners']:.1f} corners")
        print(f"🎯 Accuracy Level: {acc['accuracy_level']}")
        print(f"📉 Difference: {acc['difference']:.1f} corners")
        
        updated = comparison['updated_recommendation']
        print(f"\n🔥 Updated Recommendation:")
        print(f"   Primary: {updated['primary']} ({updated['confidence']})")
        print(f"   Secondary: {updated['secondary']}")
        print(f"   Risk Level: {updated['risk_level']}")

if __name__ == "__main__":
    main()
