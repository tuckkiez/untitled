#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Corrected Value Bet Analyzer - ราคาที่ถูกต้องจากภาพ
ระบบวิเคราะห์ Value Bet ด้วยราคาจริงที่อ่านถูกต้อง
"""

import json
from datetime import datetime
import math

class CorrectedValueBetAnalyzer:
    def __init__(self):
        self.real_odds_data = {}
        self.predictions = {}
        
    def calculate_implied_probability(self, odds: float) -> float:
        """คำนวณความน่าจะเป็นจากราคา"""
        return 1 / odds if odds > 0 else 0
        
    def calculate_value_bet(self, our_prob: float, bookmaker_odds: float) -> dict:
        """คำนวณ Value Bet"""
        implied_prob = self.calculate_implied_probability(bookmaker_odds)
        edge = our_prob - implied_prob
        expected_value = (our_prob * bookmaker_odds) - 1
        
        # Kelly Criterion
        kelly_fraction = max(0, edge / (bookmaker_odds - 1)) if bookmaker_odds > 1 else 0
        
        return {
            'our_probability': our_prob,
            'implied_probability': implied_prob,
            'edge': edge,
            'expected_value': expected_value,
            'is_value_bet': edge > 0.05,  # Edge มากกว่า 5%
            'confidence_level': 'HIGH' if edge > 0.1 else 'MEDIUM' if edge > 0.05 else 'LOW',
            'kelly_fraction': kelly_fraction
        }
    
    def analyze_match_corrected(self, home_team: str, away_team: str, 
                               our_predictions: dict, real_odds: dict) -> dict:
        """วิเคราะห์การแข่งขันด้วยราคาที่ถูกต้อง"""
        
        analysis = {
            'match': f"{home_team} vs {away_team}",
            'our_predictions': our_predictions,
            'real_odds': real_odds,
            'value_analysis': {},
            'value_bets': [],
            'recommendations': []
        }
        
        # วิเคราะห์ 1X2 (ราคาที่ถูกต้อง)
        if 'win_probabilities' in our_predictions and 'odds_1x2' in real_odds:
            home_prob = our_predictions['win_probabilities']['home']
            draw_prob = our_predictions['win_probabilities']['draw']
            away_prob = our_predictions['win_probabilities']['away']
            
            home_value = self.calculate_value_bet(home_prob, real_odds['odds_1x2']['home'])
            draw_value = self.calculate_value_bet(draw_prob, real_odds['odds_1x2']['draw'])
            away_value = self.calculate_value_bet(away_prob, real_odds['odds_1x2']['away'])
            
            analysis['value_analysis']['1x2'] = {
                'home': home_value,
                'draw': draw_value,
                'away': away_value
            }
            
            # เก็บ Value Bets
            for outcome, value_data, odds in [
                ('HOME_WIN', home_value, real_odds['odds_1x2']['home']),
                ('DRAW', draw_value, real_odds['odds_1x2']['draw']),
                ('AWAY_WIN', away_value, real_odds['odds_1x2']['away'])
            ]:
                if value_data['is_value_bet']:
                    analysis['value_bets'].append({
                        'type': '1X2',
                        'outcome': outcome,
                        'odds': odds,
                        'our_probability': value_data['our_probability'],
                        'edge': value_data['edge'],
                        'expected_value': value_data['expected_value'],
                        'confidence': value_data['confidence_level'],
                        'kelly_fraction': value_data['kelly_fraction']
                    })
        
        # วิเคราะห์ Handicap (ราคาที่ถูกต้อง)
        if 'handicap_prediction' in our_predictions and 'handicap_odds' in real_odds:
            home_handicap_prob = our_predictions['handicap_prediction']['home_probability']
            away_handicap_prob = our_predictions['handicap_prediction']['away_probability']
            
            home_handicap_value = self.calculate_value_bet(home_handicap_prob, real_odds['handicap_odds']['home'])
            away_handicap_value = self.calculate_value_bet(away_handicap_prob, real_odds['handicap_odds']['away'])
            
            analysis['value_analysis']['handicap'] = {
                'home': home_handicap_value,
                'away': away_handicap_value
            }
            
            for outcome, value_data, odds in [
                ('HOME_HANDICAP', home_handicap_value, real_odds['handicap_odds']['home']),
                ('AWAY_HANDICAP', away_handicap_value, real_odds['handicap_odds']['away'])
            ]:
                if value_data['is_value_bet']:
                    analysis['value_bets'].append({
                        'type': 'HANDICAP',
                        'outcome': f"{outcome} (0)",
                        'odds': odds,
                        'our_probability': value_data['our_probability'],
                        'edge': value_data['edge'],
                        'expected_value': value_data['expected_value'],
                        'confidence': value_data['confidence_level'],
                        'kelly_fraction': value_data['kelly_fraction']
                    })
        
        # วิเคราะห์ Over/Under (ราคาที่ถูกต้อง)
        if 'over_under_prediction' in our_predictions and 'over_under_odds' in real_odds:
            over_prob = our_predictions['over_under_prediction']['over_probability']
            under_prob = our_predictions['over_under_prediction']['under_probability']
            
            over_value = self.calculate_value_bet(over_prob, real_odds['over_under_odds']['over'])
            under_value = self.calculate_value_bet(under_prob, real_odds['over_under_odds']['under'])
            
            analysis['value_analysis']['over_under'] = {
                'over': over_value,
                'under': under_value
            }
            
            for outcome, value_data, odds in [
                ('OVER', over_value, real_odds['over_under_odds']['over']),
                ('UNDER', under_value, real_odds['over_under_odds']['under'])
            ]:
                if value_data['is_value_bet']:
                    line = real_odds['over_under_odds'].get('line', '1.5/2')
                    analysis['value_bets'].append({
                        'type': 'OVER/UNDER',
                        'outcome': f"{outcome} {line}",
                        'odds': odds,
                        'our_probability': value_data['our_probability'],
                        'edge': value_data['edge'],
                        'expected_value': value_data['expected_value'],
                        'confidence': value_data['confidence_level'],
                        'kelly_fraction': value_data['kelly_fraction']
                    })
        
        # วิเคราะห์เตะมุม
        if 'corner_prediction' in our_predictions and 'corner_odds' in real_odds:
            corner_over_prob = our_predictions['corner_prediction']['over_probability']
            corner_under_prob = our_predictions['corner_prediction']['under_probability']
            
            corner_over_value = self.calculate_value_bet(corner_over_prob, real_odds['corner_odds']['over'])
            corner_under_value = self.calculate_value_bet(corner_under_prob, real_odds['corner_odds']['under'])
            
            analysis['value_analysis']['corners'] = {
                'over': corner_over_value,
                'under': corner_under_value
            }
            
            for outcome, value_data, odds in [
                ('CORNER_OVER', corner_over_value, real_odds['corner_odds']['over']),
                ('CORNER_UNDER', corner_under_value, real_odds['corner_odds']['under'])
            ]:
                if value_data['is_value_bet']:
                    line = real_odds['corner_odds'].get('line', '9')
                    analysis['value_bets'].append({
                        'type': 'CORNERS',
                        'outcome': f"{outcome} {line}",
                        'odds': odds,
                        'our_probability': value_data['our_probability'],
                        'edge': value_data['edge'],
                        'expected_value': value_data['expected_value'],
                        'confidence': value_data['confidence_level'],
                        'kelly_fraction': value_data['kelly_fraction']
                    })
        
        # สร้างคำแนะนำ
        analysis['recommendations'] = self._generate_recommendations(analysis['value_bets'])
        
        return analysis
    
    def _generate_recommendations(self, value_bets: list) -> dict:
        """สร้างคำแนะนำการเดิมพัน"""
        if not value_bets:
            return {
                'action': 'PASS',
                'reason': 'No value bets found',
                'confidence': 'N/A'
            }
        
        high_confidence_bets = [bet for bet in value_bets if bet['confidence'] == 'HIGH']
        medium_confidence_bets = [bet for bet in value_bets if bet['confidence'] == 'MEDIUM']
        
        if high_confidence_bets:
            best_bet = max(high_confidence_bets, key=lambda x: x['edge'])
            return {
                'action': 'BET',
                'recommended_bet': best_bet,
                'total_value_bets': len(value_bets),
                'high_confidence_bets': len(high_confidence_bets),
                'confidence': 'HIGH'
            }
        elif medium_confidence_bets:
            best_bet = max(medium_confidence_bets, key=lambda x: x['edge'])
            return {
                'action': 'CONSIDER',
                'recommended_bet': best_bet,
                'total_value_bets': len(value_bets),
                'confidence': 'MEDIUM',
                'warning': 'Proceed with caution'
            }
        else:
            return {
                'action': 'PASS',
                'reason': 'Low confidence value bets only',
                'confidence': 'LOW'
            }

def main():
    """ฟังก์ชันหลักด้วยราคาที่ถูกต้อง"""
    
    print("🚀 Corrected Value Bet Analyzer - ราคาที่ถูกต้อง")
    print("=" * 65)
    
    # สร้าง analyzer
    analyzer = CorrectedValueBetAnalyzer()
    
    # ราคาที่ถูกต้องจากภาพ
    real_odds = {
        'odds_1x2': {
            'home': 3.00,    # 1 = 3.00 (ซีเอ อัลไดรี่ ชนะ)
            'draw': 2.84,    # X = 2.84 (เสมอ)
            'away': 2.53     # 2 = 2.53 (เซ็นทรัล คอร์โดบา ชนะ)
        },
        'handicap_odds': {
            'line': '0',
            'home': 2.13,    # เจ้าบ้าน 0 = 2.13
            'away': 1.78     # เยือน 0 = 1.78
        },
        'over_under_odds': {
            'line': '1.5/2',
            'over': 1.80,    # สูง 1.5/2 = 1.80
            'under': 2.09    # ต่ำ 1.5/2 = 2.09
        },
        'corner_odds': {
            'line': '9',
            'over': 2.05,    # เตะมุมสูง 9 = 2.05
            'under': 1.77    # เตะมุมต่ำ 9 = 1.77
        }
    }
    
    # การทำนายของเรา (ปรับตามผลที่เคยคำนวณ)
    our_predictions = {
        'prediction': 'AWAY_WIN',  # เปลี่ยนเป็นทีมเยือนชนะ
        'confidence': 0.65,
        'win_probabilities': {
            'home': 0.30,    # ซีเอ อัลไดรี่ ชนะ 30%
            'draw': 0.25,    # เสมอ 25%
            'away': 0.45     # เซ็นทรัล คอร์โดบา ชนะ 45%
        },
        'handicap_prediction': {
            'home_probability': 0.40,  # เจ้าบ้าน +0
            'away_probability': 0.60   # เยือน +0
        },
        'over_under_prediction': {
            'prediction': 'UNDER',
            'over_probability': 0.35,   # Over 1.5/2 = 35%
            'under_probability': 0.65   # Under 1.5/2 = 65%
        },
        'corner_prediction': {
            'over_probability': 0.45,   # Corner Over 9 = 45%
            'under_probability': 0.55   # Corner Under 9 = 55%
        },
        'expected_score': {
            'home': 1.2,
            'away': 1.8
        }
    }
    
    # วิเคราะห์การแข่งขัน
    analysis = analyzer.analyze_match_corrected(
        'ซีเอ อัลไดรี่',
        'เซ็นทรัล คอร์โดบา เอสดีอี',
        our_predictions,
        real_odds
    )
    
    # แสดงผลการวิเคราะห์
    print(f"\n🏆 การแข่งขัน: {analysis['match']}")
    print(f"⏰ เวลา: 12 ก.ค. 01:30")
    print("-" * 65)
    
    print("\n📊 การทำนายของเรา:")
    pred = analysis['our_predictions']
    print(f"   ผลทำนาย: {pred['prediction']} (มั่นใจ {pred['confidence']:.1%})")
    print(f"   ความน่าจะเป็น: เจ้าบ้าน {pred['win_probabilities']['home']:.1%} | "
          f"เสมอ {pred['win_probabilities']['draw']:.1%} | "
          f"ทีมเยือน {pred['win_probabilities']['away']:.1%}")
    print(f"   คะแนนคาด: {pred['expected_score']['home']:.1f} - {pred['expected_score']['away']:.1f}")
    
    print("\n💰 ราคาจริงจากเว็บพนัน (แก้ไขแล้ว):")
    odds = analysis['real_odds']
    print(f"   1X2: เจ้าบ้าน {odds['odds_1x2']['home']:.2f} | "
          f"เสมอ {odds['odds_1x2']['draw']:.2f} | "
          f"ทีมเยือน {odds['odds_1x2']['away']:.2f}")
    print(f"   Handicap (0): เจ้าบ้าน {odds['handicap_odds']['home']:.2f} | "
          f"ทีมเยือน {odds['handicap_odds']['away']:.2f}")
    print(f"   Over/Under (1.5/2): Over {odds['over_under_odds']['over']:.2f} | "
          f"Under {odds['over_under_odds']['under']:.2f}")
    print(f"   เตะมุม (9): Over {odds['corner_odds']['over']:.2f} | "
          f"Under {odds['corner_odds']['under']:.2f}")
    
    print("\n🎯 Value Bet Analysis:")
    
    # วิเคราะห์ 1X2
    if '1x2' in analysis['value_analysis']:
        print("   1X2 Value Analysis:")
        outcomes = ['home', 'draw', 'away']
        labels = ['เจ้าบ้าน', 'เสมอ', 'ทีมเยือน']
        for outcome, label in zip(outcomes, labels):
            data = analysis['value_analysis']['1x2'][outcome]
            edge_pct = data['edge'] * 100
            print(f"     {label}: Edge {edge_pct:+.1f}% | "
                  f"EV {data['expected_value']:+.3f} | "
                  f"{'✅ VALUE BET' if data['is_value_bet'] else '❌ No Value'}")
    
    # วิเคราะห์ Handicap
    if 'handicap' in analysis['value_analysis']:
        print("   Handicap Value Analysis:")
        for side, data in analysis['value_analysis']['handicap'].items():
            edge_pct = data['edge'] * 100
            label = 'เจ้าบ้าน' if side == 'home' else 'ทีมเยือน'
            print(f"     {label}: Edge {edge_pct:+.1f}% | "
                  f"EV {data['expected_value']:+.3f} | "
                  f"{'✅ VALUE BET' if data['is_value_bet'] else '❌ No Value'}")
    
    # วิเคราะห์ Over/Under
    if 'over_under' in analysis['value_analysis']:
        print("   Over/Under (1.5/2) Value Analysis:")
        for bet_type, data in analysis['value_analysis']['over_under'].items():
            edge_pct = data['edge'] * 100
            print(f"     {bet_type.upper()}: Edge {edge_pct:+.1f}% | "
                  f"EV {data['expected_value']:+.3f} | "
                  f"{'✅ VALUE BET' if data['is_value_bet'] else '❌ No Value'}")
    
    # วิเคราะห์เตะมุม
    if 'corners' in analysis['value_analysis']:
        print("   เตะมุม (9) Value Analysis:")
        for bet_type, data in analysis['value_analysis']['corners'].items():
            edge_pct = data['edge'] * 100
            print(f"     {bet_type.upper()}: Edge {edge_pct:+.1f}% | "
                  f"EV {data['expected_value']:+.3f} | "
                  f"{'✅ VALUE BET' if data['is_value_bet'] else '❌ No Value'}")
    
    print("\n🔥 Value Bets ที่พบ:")
    if analysis['value_bets']:
        for i, bet in enumerate(analysis['value_bets'], 1):
            print(f"   {i}. {bet['type']}: {bet['outcome']}")
            print(f"      💰 ราคา: {bet['odds']:.2f}")
            print(f"      📊 ความน่าจะเป็นของเรา: {bet['our_probability']:.1%}")
            print(f"      📈 Edge: {bet['edge']:+.1%}")
            print(f"      💡 Expected Value: {bet['expected_value']:+.1%}")
            print(f"      🎯 ความมั่นใจ: {bet['confidence']}")
            print(f"      🎲 Kelly Fraction: {bet['kelly_fraction']:.3f}")
            print()
    else:
        print("   ❌ ไม่พบ Value Bet ที่น่าสนใจ")
    
    print("💡 คำแนะนำการเดิมพัน:")
    rec = analysis['recommendations']
    print(f"   การกระทำ: {rec['action']}")
    
    if rec['action'] == 'BET':
        print(f"   ✅ แนะนำเดิมพัน: {rec['recommended_bet']['outcome']}")
        print(f"   💰 ราคา: {rec['recommended_bet']['odds']:.2f}")
        print(f"   📈 Edge: {rec['recommended_bet']['edge']:+.1%}")
        print(f"   🎯 ความมั่นใจ: {rec['confidence']}")
    elif rec['action'] == 'CONSIDER':
        print(f"   ⚠️  พิจารณา: {rec['recommended_bet']['outcome']}")
        print(f"   💰 ราคา: {rec['recommended_bet']['odds']:.2f}")
        print(f"   ⚠️  {rec.get('warning', '')}")
    else:
        print(f"   ❌ เหตุผล: {rec.get('reason', 'No value found')}")
    
    print("\n📈 สรุปการวิเคราะห์:")
    total_value_bets = len(analysis['value_bets'])
    high_confidence_bets = len([b for b in analysis['value_bets'] if b['confidence'] == 'HIGH'])
    
    print(f"   📊 Value Bets ทั้งหมด: {total_value_bets}")
    print(f"   🔥 ความมั่นใจสูง: {high_confidence_bets}")
    
    if total_value_bets > 0:
        avg_edge = sum([b['edge'] for b in analysis['value_bets']]) / total_value_bets
        print(f"   📈 Edge เฉลี่ย: {avg_edge:+.1%}")
        
        if high_confidence_bets > 0:
            print("   ✅ แนะนำให้พิจารณาเดิมพัน")
        else:
            print("   ⚠️  ระมัดระวัง - Edge ไม่สูงมาก")
    else:
        print("   ❌ ไม่แนะนำให้เดิมพันในเกมนี้")
    
    print("\n" + "=" * 65)
    print("🚀 Corrected Value Bet Analyzer")
    print("💡 ระบบวิเคราะห์ Value Bet ด้วยราคาที่ถูกต้อง")
    print("⚽ แก้ไขข้อผิดพลาดการอ่านราคาแล้ว")

if __name__ == "__main__":
    main()
