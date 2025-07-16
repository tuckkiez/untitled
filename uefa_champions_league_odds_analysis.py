#!/usr/bin/env python3
"""
UEFA Champions League Odds Analysis
Dinamo Minsk vs Ludogorets - July 16, 2025
Professional betting analysis with real odds from 14+ bookmakers
"""

import json
from datetime import datetime
import statistics

def analyze_uefa_champions_league_odds():
    """Analyze real odds data for UEFA Champions League qualifying match"""
    
    print("🏆 UEFA CHAMPIONS LEAGUE QUALIFYING ROUND ANALYSIS")
    print("=" * 60)
    print("📅 Match Date: July 16, 2025 - 18:45 UTC (01:45 Thai Time)")
    print("🏟️  Fixture: Dinamo Minsk vs Ludogorets")
    print("🆔 Fixture ID: 1383449")
    print("🔄 Last Update: 2025-07-16T12:34:15+00:00")
    print()
    
    # Match Winner Odds Analysis
    print("⚽ MATCH WINNER ODDS ANALYSIS")
    print("-" * 40)
    
    # Collected odds from major bookmakers
    match_winner_odds = {
        'Bwin': {'Home': 5.00, 'Draw': 3.80, 'Away': 1.65},
        '10Bet': {'Home': 4.75, 'Draw': 3.70, 'Away': 1.65},
        'William Hill': {'Home': 4.80, 'Draw': 3.70, 'Away': 1.65},
        'Bet365': {'Home': 4.33, 'Draw': 3.90, 'Away': 1.65},
        'Marathonbet': {'Home': 5.20, 'Draw': 3.84, 'Away': 1.66},
        'Unibet': {'Home': 5.00, 'Draw': 3.95, 'Away': 1.62},
        'Betfair': {'Home': 4.75, 'Draw': 3.60, 'Away': 1.62},
        '188Bet': {'Home': 4.20, 'Draw': 3.60, 'Away': 1.66},
        'Fonbet': {'Home': 4.70, 'Draw': 4.00, 'Away': 1.70},
        'Pinnacle': {'Home': 4.64, 'Draw': 3.84, 'Away': 1.66},
        'SBO': {'Home': 4.15, 'Draw': 3.29, 'Away': 1.66},
        '1xBet': {'Home': 5.26, 'Draw': 3.89, 'Away': 1.68},
        'Betano': {'Home': 4.75, 'Draw': 3.75, 'Away': 1.65},
        'Superbet': {'Home': 4.65, 'Draw': 3.90, 'Away': 1.67}
    }
    
    # Calculate average odds
    home_odds = [odds['Home'] for odds in match_winner_odds.values()]
    draw_odds = [odds['Draw'] for odds in match_winner_odds.values()]
    away_odds = [odds['Away'] for odds in match_winner_odds.values()]
    
    avg_home = statistics.mean(home_odds)
    avg_draw = statistics.mean(draw_odds)
    avg_away = statistics.mean(away_odds)
    
    print(f"🏠 Dinamo Minsk (Home): {avg_home:.2f} average odds")
    print(f"🤝 Draw: {avg_draw:.2f} average odds")
    print(f"🚀 Ludogorets (Away): {avg_away:.2f} average odds")
    print()
    
    # Convert to implied probabilities
    home_prob = (1/avg_home) * 100
    draw_prob = (1/avg_draw) * 100
    away_prob = (1/avg_away) * 100
    
    print("📊 IMPLIED PROBABILITIES")
    print("-" * 30)
    print(f"🏠 Dinamo Minsk Win: {home_prob:.1f}%")
    print(f"🤝 Draw: {draw_prob:.1f}%")
    print(f"🚀 Ludogorets Win: {away_prob:.1f}%")
    print()
    
    # Goals Over/Under Analysis
    print("⚽ GOALS OVER/UNDER ANALYSIS")
    print("-" * 35)
    
    # Over/Under 2.5 Goals from multiple bookmakers
    over_under_25 = {
        'Bwin': {'Over': 1.85, 'Under': 1.85},
        '10Bet': {'Over': 1.95, 'Under': 1.80},
        'Bet365': {'Over': 2.00, 'Under': 1.80},
        'Marathonbet': {'Over': 1.97, 'Under': 1.83},
        'Unibet': {'Over': 1.84, 'Under': 1.92},
        'Betfair': {'Over': 1.91, 'Under': 1.80},
        '188Bet': {'Over': 1.86, 'Under': 1.96},
        'Fonbet': {'Over': 1.95, 'Under': 1.85},
        'Pinnacle': {'Over': 1.99, 'Under': 1.82},
        'SBO': {'Over': 1.95, 'Under': 1.83},
        '1xBet': {'Over': 1.99, 'Under': 1.85},
        'Betano': {'Over': 1.95, 'Under': 1.78},
        'Superbet': {'Over': 1.85, 'Under': 1.87}
    }
    
    over_25_odds = [odds['Over'] for odds in over_under_25.values()]
    under_25_odds = [odds['Under'] for odds in over_under_25.values()]
    
    avg_over_25 = statistics.mean(over_25_odds)
    avg_under_25 = statistics.mean(under_25_odds)
    
    over_25_prob = (1/avg_over_25) * 100
    under_25_prob = (1/avg_under_25) * 100
    
    print(f"📈 Over 2.5 Goals: {avg_over_25:.2f} odds ({over_25_prob:.1f}% probability)")
    print(f"📉 Under 2.5 Goals: {avg_under_25:.2f} odds ({under_25_prob:.1f}% probability)")
    print()
    
    # Both Teams to Score Analysis
    print("🎯 BOTH TEAMS TO SCORE ANALYSIS")
    print("-" * 35)
    
    btts_odds = {
        'Bwin': {'Yes': 1.87, 'No': 1.80},
        '10Bet': {'Yes': 1.85, 'No': 1.80},
        'William Hill': {'Yes': 1.85, 'No': 1.85},
        'Bet365': {'Yes': 2.00, 'No': 1.73},
        'Marathonbet': {'Yes': 1.92, 'No': 1.79},
        'Unibet': {'Yes': 1.83, 'No': 1.89},
        'Betfair': {'Yes': 1.95, 'No': 1.80},
        '188Bet': {'Yes': 1.86, 'No': 1.91},
        'Fonbet': {'Yes': 1.88, 'No': 1.92},
        'Pinnacle': {'Yes': 1.93, 'No': 1.84},
        '1xBet': {'Yes': 1.92, 'No': 1.84},
        'Betano': {'Yes': 1.93, 'No': 1.78},
        'Superbet': {'Yes': 1.85, 'No': 1.87}
    }
    
    btts_yes_odds = [odds['Yes'] for odds in btts_odds.values()]
    btts_no_odds = [odds['No'] for odds in btts_odds.values()]
    
    avg_btts_yes = statistics.mean(btts_yes_odds)
    avg_btts_no = statistics.mean(btts_no_odds)
    
    btts_yes_prob = (1/avg_btts_yes) * 100
    btts_no_prob = (1/avg_btts_no) * 100
    
    print(f"✅ Both Teams Score: {avg_btts_yes:.2f} odds ({btts_yes_prob:.1f}% probability)")
    print(f"❌ Both Teams Don't Score: {avg_btts_no:.2f} odds ({btts_no_prob:.1f}% probability)")
    print()
    
    # Corners Analysis
    print("🚩 CORNERS ANALYSIS")
    print("-" * 20)
    
    # Over/Under 8.5 Corners from available bookmakers
    corners_85 = {
        'Bwin': {'Over': 1.66, 'Under': 2.05},
        '10Bet': {'Over': 1.70, 'Under': 2.05},
        'Bet365': {'Over': 1.67, 'Under': 2.10},
        'Marathonbet': {'Over': 1.72, 'Under': 2.00},
        'Unibet': {'Over': 1.67, 'Under': 2.07},
        'Fonbet': {'Over': 1.67, 'Under': 2.07},
        'Pinnacle': {'Over': 1.75, 'Under': 1.97},
        '1xBet': {'Over': 1.70, 'Under': 2.08},
        'Betano': {'Over': 1.65, 'Under': 2.10},
        'Superbet': {'Over': 1.66, 'Under': 2.10}
    }
    
    corners_over_odds = [odds['Over'] for odds in corners_85.values()]
    corners_under_odds = [odds['Under'] for odds in corners_85.values()]
    
    avg_corners_over = statistics.mean(corners_over_odds)
    avg_corners_under = statistics.mean(corners_under_odds)
    
    corners_over_prob = (1/avg_corners_over) * 100
    corners_under_prob = (1/avg_corners_under) * 100
    
    print(f"📈 Over 8.5 Corners: {avg_corners_over:.2f} odds ({corners_over_prob:.1f}% probability)")
    print(f"📉 Under 8.5 Corners: {avg_corners_under:.2f} odds ({corners_under_prob:.1f}% probability)")
    print()
    
    # Professional Predictions
    print("🎯 PROFESSIONAL PREDICTIONS")
    print("=" * 40)
    print()
    
    print("🏆 MATCH RESULT PREDICTION")
    print(f"🥇 Primary: Ludogorets Win ({away_prob:.1f}% confidence)")
    print(f"🥈 Secondary: Draw ({draw_prob:.1f}% confidence)")
    print(f"🥉 Unlikely: Dinamo Minsk Win ({home_prob:.1f}% confidence)")
    print()
    
    print("⚽ GOALS PREDICTION")
    if over_25_prob > under_25_prob:
        print(f"🎯 Over 2.5 Goals ({over_25_prob:.1f}% confidence)")
        print("📊 Expected: 3+ goals in this match")
    else:
        print(f"🎯 Under 2.5 Goals ({under_25_prob:.1f}% confidence)")
        print("📊 Expected: 0-2 goals in this match")
    print()
    
    print("🎯 BOTH TEAMS TO SCORE")
    if btts_yes_prob > btts_no_prob:
        print(f"✅ Yes ({btts_yes_prob:.1f}% confidence)")
        print("📊 Both teams likely to score")
    else:
        print(f"❌ No ({btts_no_prob:.1f}% confidence)")
        print("📊 At least one team likely to keep clean sheet")
    print()
    
    print("🚩 CORNERS PREDICTION")
    if corners_over_prob > corners_under_prob:
        print(f"📈 Over 8.5 Corners ({corners_over_prob:.1f}% confidence)")
        print("📊 Expected: 9+ corners in this match")
    else:
        print(f"📉 Under 8.5 Corners ({corners_under_prob:.1f}% confidence)")
        print("📊 Expected: 0-8 corners in this match")
    print()
    
    # Market Analysis
    print("📈 MARKET ANALYSIS")
    print("=" * 25)
    
    # Calculate market margins
    total_prob = home_prob + draw_prob + away_prob
    market_margin = total_prob - 100
    
    print(f"📊 Market Efficiency: {100-market_margin:.1f}%")
    print(f"📈 Bookmaker Margin: {market_margin:.1f}%")
    
    if market_margin < 5:
        print("✅ Efficient market - competitive odds")
    elif market_margin < 8:
        print("⚠️  Moderate market - acceptable odds")
    else:
        print("❌ High margin market - less favorable odds")
    print()
    
    # Value Betting Opportunities
    print("💰 VALUE BETTING ANALYSIS")
    print("-" * 30)
    
    # Find best odds for each outcome
    best_home = max(home_odds)
    best_draw = max(draw_odds)
    best_away = max(away_odds)
    
    print(f"🏠 Best Home Odds: {best_home:.2f}")
    print(f"🤝 Best Draw Odds: {best_draw:.2f}")
    print(f"🚀 Best Away Odds: {best_away:.2f}")
    print()
    
    # Calculate value
    home_value = (best_home * home_prob/100) - 1
    draw_value = (best_draw * draw_prob/100) - 1
    away_value = (best_away * away_prob/100) - 1
    
    print("📊 VALUE ASSESSMENT:")
    if home_value > 0:
        print(f"🏠 Home Win: +{home_value:.1%} value")
    if draw_value > 0:
        print(f"🤝 Draw: +{draw_value:.1%} value")
    if away_value > 0:
        print(f"🚀 Away Win: +{away_value:.1%} value")
    
    if max(home_value, draw_value, away_value) <= 0:
        print("⚠️  No significant value bets identified")
    print()
    
    print("🔍 FINAL RECOMMENDATION")
    print("=" * 30)
    print("🎯 Recommended Bet: Ludogorets Win")
    print(f"📊 Confidence Level: {away_prob:.1f}%")
    print(f"💰 Best Odds: {best_away:.2f}")
    print("📈 Reasoning: Strong away team in qualifying round")
    print("⚠️  Risk Level: Medium (Champions League qualifying)")
    print()
    
    print("📝 ADDITIONAL NOTES")
    print("-" * 20)
    print("• UEFA Champions League 1st Qualifying Round")
    print("• Ludogorets has European experience advantage")
    print("• Away goals rule may apply in qualifying")
    print("• Consider live betting for better value")
    print("• Monitor team news before kickoff")
    
    return {
        'match_winner': {'home': avg_home, 'draw': avg_draw, 'away': avg_away},
        'probabilities': {'home': home_prob, 'draw': draw_prob, 'away': away_prob},
        'goals': {'over_25': avg_over_25, 'under_25': avg_under_25},
        'btts': {'yes': avg_btts_yes, 'no': avg_btts_no},
        'corners': {'over_85': avg_corners_over, 'under_85': avg_corners_under},
        'recommendation': 'Ludogorets Win',
        'confidence': away_prob
    }

if __name__ == "__main__":
    analysis = analyze_uefa_champions_league_odds()
    
    print("\n" + "="*60)
    print("🏆 UEFA CHAMPIONS LEAGUE ANALYSIS COMPLETE")
    print("📅 Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*60)
