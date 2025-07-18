#!/usr/bin/env python3
"""
🚀 Compare ML Models for China Super League Analysis
เปรียบเทียบผลการวิเคราะห์ระหว่าง Advanced ML และ Ultra Advanced ML
"""

import pandas as pd
import os
import json
from datetime import datetime

def compare_ml_models():
    """Compare Advanced ML and Ultra Advanced ML models"""
    print("🚀 Comparing ML Models for China Super League Analysis")
    print("=" * 80)
    
    # Define file paths
    advanced_csv = "/Users/80090/Desktop/Project/untitle/api_data/china_super_league/china_super_league_predictions_advanced_ml.csv"
    ultra_csv = "/Users/80090/Desktop/Project/untitle/api_data/china_super_league/china_super_league_predictions_ultra_ml.csv"
    output_csv = "/Users/80090/Desktop/Project/untitle/api_data/china_super_league/china_super_league_predictions_comparison.csv"
    output_html = "/Users/80090/Desktop/Project/untitle/api_data/china_super_league/china_super_league_comparison.html"
    
    # Load predictions
    try:
        advanced_df = pd.read_csv(advanced_csv)
        ultra_df = pd.read_csv(ultra_csv)
        print(f"✅ Successfully loaded predictions from both models")
    except Exception as e:
        print(f"❌ Error loading predictions: {str(e)}")
        return False
    
    # Create comparison dataframe
    comparison = []
    
    for i in range(len(advanced_df)):
        advanced_row = advanced_df.iloc[i]
        ultra_row = ultra_df.iloc[i]
        
        # Ensure we're comparing the same match
        if advanced_row['fixture_id'] != ultra_row['fixture_id']:
            print(f"❌ Mismatch in fixture IDs: {advanced_row['fixture_id']} vs {ultra_row['fixture_id']}")
            continue
        
        # Create comparison row
        comparison.append({
            "fixture_id": advanced_row['fixture_id'],
            "date": advanced_row['date'],
            "home_team": advanced_row['home_team'],
            "away_team": advanced_row['away_team'],
            "home_logo": advanced_row['home_logo'],
            "away_logo": advanced_row['away_logo'],
            
            # Advanced ML predictions
            "adv_match_winner": advanced_row['match_winner'],
            "adv_confidence": advanced_row['confidence'],
            "adv_score": advanced_row['score'],
            "adv_over_under": advanced_row['over_under'],
            "adv_over_under_confidence": advanced_row['over_under_confidence'],
            "adv_btts": advanced_row['btts'],
            "adv_btts_confidence": advanced_row['btts_confidence'],
            "adv_corners": advanced_row['corners'],
            "adv_corners_confidence": advanced_row['corners_confidence'],
            
            # Ultra Advanced ML predictions
            "ultra_match_winner": ultra_row['match_winner'],
            "ultra_confidence": ultra_row['confidence'],
            "ultra_score": ultra_row['score'],
            "ultra_over_under": ultra_row['over_under'],
            "ultra_over_under_confidence": ultra_row['over_under_confidence'],
            "ultra_btts": ultra_row['btts'],
            "ultra_btts_confidence": ultra_row['btts_confidence'],
            "ultra_corners": ultra_row['corners'],
            "ultra_corners_confidence": ultra_row['corners_confidence'],
            
            # Odds
            "odds_home": advanced_row['odds_home'],
            "odds_draw": advanced_row['odds_draw'],
            "odds_away": advanced_row['odds_away'],
            "odds_over": advanced_row['odds_over'],
            "odds_under": advanced_row['odds_under'],
            "odds_corners_over": advanced_row['odds_corners_over'],
            "odds_corners_under": advanced_row['odds_corners_under'],
            "corners_line": advanced_row['corners_line']
        })
    
    # Create comparison dataframe
    comparison_df = pd.DataFrame(comparison)
    
    # Save comparison to CSV
    try:
        comparison_df.to_csv(output_csv, index=False)
        print(f"✅ Successfully saved comparison to {output_csv}")
    except Exception as e:
        print(f"❌ Error saving comparison: {str(e)}")
    
    # Create HTML comparison
    create_html_comparison(comparison_df, output_html)
    
    # Print comparison summary
    print_comparison_summary(comparison_df)
    
    return True

def create_html_comparison(comparison_df, output_html):
    """Create HTML comparison report"""
    print(f"\n📊 Creating HTML comparison report...")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>China Super League ML Models Comparison - July 18, 2025</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .header p {{
            margin: 5px 0 0;
            opacity: 0.9;
        }}
        .section {{
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            margin-top: 0;
            color: #1e3c72;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .team-logo {{
            height: 24px;
            vertical-align: middle;
            margin-right: 5px;
        }}
        .team-name {{
            display: inline-block;
            vertical-align: middle;
        }}
        .match-card {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 5px solid #1e3c72;
        }}
        .match-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .teams {{
            font-size: 18px;
            font-weight: bold;
        }}
        .date-time {{
            color: #666;
        }}
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .comparison-table th {{
            background-color: #e9ecef;
            text-align: center;
        }}
        .comparison-table td {{
            text-align: center;
        }}
        .model-header {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        .agreement {{
            background-color: #d4edda;
        }}
        .disagreement {{
            background-color: #f8d7da;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🇨🇳 China Super League ML Models Comparison - July 18, 2025</h1>
        <p>Comparing Advanced ML vs Ultra Advanced ML Predictions</p>
    </div>
    
    <div class="section">
        <h2>🚀 Models Comparison</h2>
"""
    
    # Add match comparisons
    for _, row in comparison_df.iterrows():
        # Convert date to readable format
        match_date = datetime.fromisoformat(row['date'].replace('Z', '+00:00'))
        formatted_date = match_date.strftime('%A, %B %d, %Y')
        formatted_time = match_date.strftime('%H:%M UTC')
        
        # Determine agreement/disagreement
        match_winner_agreement = "agreement" if row['adv_match_winner'] == row['ultra_match_winner'] else "disagreement"
        score_agreement = "agreement" if row['adv_score'] == row['ultra_score'] else "disagreement"
        over_under_agreement = "agreement" if row['adv_over_under'] == row['ultra_over_under'] else "disagreement"
        btts_agreement = "agreement" if row['adv_btts'] == row['ultra_btts'] else "disagreement"
        corners_agreement = "agreement" if row['adv_corners'] == row['ultra_corners'] else "disagreement"
        
        html_content += f"""
        <div class="match-card">
            <div class="match-header">
                <div class="teams">
                    <img src="{row['home_logo']}" alt="{row['home_team']}" class="team-logo">
                    <span class="team-name">{row['home_team']}</span>
                    vs
                    <img src="{row['away_logo']}" alt="{row['away_team']}" class="team-logo">
                    <span class="team-name">{row['away_team']}</span>
                </div>
                <div class="date-time">
                    {formatted_date} • {formatted_time}
                </div>
            </div>
            
            <table class="comparison-table">
                <tr>
                    <th>Model</th>
                    <th>Match Winner</th>
                    <th>Score</th>
                    <th>O/U 2.5</th>
                    <th>BTTS</th>
                    <th>Corners</th>
                </tr>
                <tr class="model-header">
                    <td>Advanced ML</td>
                    <td class="{match_winner_agreement}">{row['adv_match_winner']} ({row['adv_confidence']}%)</td>
                    <td class="{score_agreement}">{row['adv_score']}</td>
                    <td class="{over_under_agreement}">{row['adv_over_under']} ({row['adv_over_under_confidence']}%)</td>
                    <td class="{btts_agreement}">{row['adv_btts']} ({row['adv_btts_confidence']}%)</td>
                    <td class="{corners_agreement}">{row['adv_corners']} ({row['adv_corners_confidence']}%)</td>
                </tr>
                <tr class="model-header">
                    <td>Ultra Advanced ML</td>
                    <td class="{match_winner_agreement}">{row['ultra_match_winner']} ({row['ultra_confidence']}%)</td>
                    <td class="{score_agreement}">{row['ultra_score']}</td>
                    <td class="{over_under_agreement}">{row['ultra_over_under']} ({row['ultra_over_under_confidence']}%)</td>
                    <td class="{btts_agreement}">{row['ultra_btts']} ({row['ultra_btts_confidence']}%)</td>
                    <td class="{corners_agreement}">{row['ultra_corners']} ({row['ultra_corners_confidence']}%)</td>
                </tr>
                <tr>
                    <td>Market Odds</td>
                    <td>{row['odds_home']} / {row['odds_draw']} / {row['odds_away']}</td>
                    <td>-</td>
                    <td>{row['odds_over']} / {row['odds_under']}</td>
                    <td>-</td>
                    <td>{row['odds_corners_over']} / {row['odds_corners_under']} ({row['corners_line']})</td>
                </tr>
            </table>
        </div>
"""
    
    # Add summary section
    match_winner_agreement = sum(comparison_df['adv_match_winner'] == comparison_df['ultra_match_winner'])
    score_agreement = sum(comparison_df['adv_score'] == comparison_df['ultra_score'])
    over_under_agreement = sum(comparison_df['adv_over_under'] == comparison_df['ultra_over_under'])
    btts_agreement = sum(comparison_df['adv_btts'] == comparison_df['ultra_btts'])
    corners_agreement = sum(comparison_df['adv_corners'] == comparison_df['ultra_corners'])
    
    total_matches = len(comparison_df)
    
    html_content += f"""
    </div>
    
    <div class="section">
        <h2>📊 Agreement Summary</h2>
        <p>Total matches analyzed: <strong>{total_matches}</strong></p>
        
        <table>
            <tr>
                <th>Prediction Type</th>
                <th>Agreement</th>
                <th>Agreement %</th>
            </tr>
            <tr>
                <td>Match Winner</td>
                <td>{match_winner_agreement} / {total_matches}</td>
                <td>{match_winner_agreement / total_matches * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Score</td>
                <td>{score_agreement} / {total_matches}</td>
                <td>{score_agreement / total_matches * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Over/Under 2.5</td>
                <td>{over_under_agreement} / {total_matches}</td>
                <td>{over_under_agreement / total_matches * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Both Teams to Score</td>
                <td>{btts_agreement} / {total_matches}</td>
                <td>{btts_agreement / total_matches * 100:.1f}%</td>
            </tr>
            <tr>
                <td>Corners</td>
                <td>{corners_agreement} / {total_matches}</td>
                <td>{corners_agreement / total_matches * 100:.1f}%</td>
            </tr>
        </table>
    </div>
    
    <div class="section">
        <h2>🔍 Model Differences</h2>
        <p>Key differences between Advanced ML and Ultra Advanced ML:</p>
        <ul>
            <li><strong>Recent Form Analysis:</strong> Ultra Advanced ML applies recency bias to recent matches</li>
            <li><strong>Head-to-Head Weighting:</strong> Ultra Advanced ML gives more weight to H2H records (30% vs 25%)</li>
            <li><strong>Home Advantage:</strong> Ultra Advanced ML uses a more balanced approach to home advantage</li>
            <li><strong>Corner Analysis:</strong> Ultra Advanced ML uses a 60/40 split between team stats and H2H data</li>
            <li><strong>Confidence Calculation:</strong> Ultra Advanced ML has a more nuanced confidence calculation</li>
        </ul>
    </div>
    
    <div class="footer">
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Ultra Advanced Multi-League Football Predictor</p>
        <p>© 2025 All Rights Reserved</p>
    </div>
</body>
</html>
"""
    
    # Save HTML file
    try:
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Successfully created HTML comparison report: {output_html}")
        return True
    except Exception as e:
        print(f"❌ Error creating HTML comparison report: {str(e)}")
        return False

def print_comparison_summary(comparison_df):
    """Print comparison summary"""
    print("\n📊 Models Comparison Summary:")
    print("=" * 80)
    
    # Calculate agreement percentages
    match_winner_agreement = sum(comparison_df['adv_match_winner'] == comparison_df['ultra_match_winner'])
    score_agreement = sum(comparison_df['adv_score'] == comparison_df['ultra_score'])
    over_under_agreement = sum(comparison_df['adv_over_under'] == comparison_df['ultra_over_under'])
    btts_agreement = sum(comparison_df['adv_btts'] == comparison_df['ultra_btts'])
    corners_agreement = sum(comparison_df['adv_corners'] == comparison_df['ultra_corners'])
    
    total_matches = len(comparison_df)
    
    print(f"Total matches analyzed: {total_matches}")
    print(f"Match Winner Agreement: {match_winner_agreement}/{total_matches} ({match_winner_agreement/total_matches*100:.1f}%)")
    print(f"Score Agreement: {score_agreement}/{total_matches} ({score_agreement/total_matches*100:.1f}%)")
    print(f"Over/Under Agreement: {over_under_agreement}/{total_matches} ({over_under_agreement/total_matches*100:.1f}%)")
    print(f"BTTS Agreement: {btts_agreement}/{total_matches} ({btts_agreement/total_matches*100:.1f}%)")
    print(f"Corners Agreement: {corners_agreement}/{total_matches} ({corners_agreement/total_matches*100:.1f}%)")
    
    print("\n📋 Match-by-Match Comparison:")
    print("-" * 80)
    
    for i, row in comparison_df.iterrows():
        print(f"Match {i+1}: {row['home_team']} vs {row['away_team']}")
        print(f"  Match Winner: {'✅ AGREE' if row['adv_match_winner'] == row['ultra_match_winner'] else '❌ DISAGREE'} (Adv: {row['adv_match_winner']}, Ultra: {row['ultra_match_winner']})")
        print(f"  Score: {'✅ AGREE' if row['adv_score'] == row['ultra_score'] else '❌ DISAGREE'} (Adv: {row['adv_score']}, Ultra: {row['ultra_score']})")
        print(f"  Over/Under: {'✅ AGREE' if row['adv_over_under'] == row['ultra_over_under'] else '❌ DISAGREE'} (Adv: {row['adv_over_under']}, Ultra: {row['ultra_over_under']})")
        print(f"  BTTS: {'✅ AGREE' if row['adv_btts'] == row['ultra_btts'] else '❌ DISAGREE'} (Adv: {row['adv_btts']}, Ultra: {row['ultra_btts']})")
        print(f"  Corners: {'✅ AGREE' if row['adv_corners'] == row['ultra_corners'] else '❌ DISAGREE'} (Adv: {row['adv_corners']}, Ultra: {row['ultra_corners']})")
        print()
    
    print("=" * 80)

def main():
    """Main function"""
    compare_ml_models()

if __name__ == "__main__":
    main()
