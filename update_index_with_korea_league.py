#!/usr/bin/env python3
"""
🚀 Update Index with Korea K League 1 Analysis - July 18, 2025
อัพเดทไฟล์ index.html ด้วยข้อมูลการวิเคราะห์ K League 1
"""

import os
import json
import pandas as pd
from datetime import datetime
import shutil

def update_index_with_korea_league():
    """Update index.html with Korea K League 1 analysis"""
    print("🚀 Updating index.html with Korea K League 1 analysis...")
    
    # Define file paths
    index_path = "/Users/80090/Desktop/Project/untitle/index.html"
    backup_path = f"/Users/80090/Desktop/Project/untitle/index_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    predictions_csv = "/Users/80090/Desktop/Project/untitle/api_data/korea_league/korea_league_predictions_ultra_ml.csv"
    
    # Create backup of index.html
    try:
        shutil.copy2(index_path, backup_path)
        print(f"✅ Created backup of index.html: {backup_path}")
    except Exception as e:
        print(f"❌ Error creating backup: {str(e)}")
        return False
    
    # Load predictions
    try:
        df = pd.read_csv(predictions_csv)
        print(f"✅ Successfully loaded {len(df)} predictions")
    except Exception as e:
        print(f"❌ Error loading predictions: {str(e)}")
        return False
    
    # Read index.html
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
        print("✅ Successfully read index.html")
    except Exception as e:
        print(f"❌ Error reading index.html: {str(e)}")
        return False
    
    # Create Korea League section HTML
    korea_section = create_korea_league_section(df)
    
    # Check if Korea League section already exists
    if "<!-- KOREA LEAGUE SECTION -->" in index_content:
        # Replace existing section
        start_marker = "<!-- KOREA LEAGUE SECTION -->"
        end_marker = "<!-- END KOREA LEAGUE SECTION -->"
        start_index = index_content.find(start_marker)
        end_index = index_content.find(end_marker) + len(end_marker)
        
        if start_index >= 0 and end_index >= len(end_marker):
            index_content = index_content[:start_index] + korea_section + index_content[end_index:]
            print("✅ Replaced existing Korea League section")
        else:
            print("❌ Could not find complete Korea League section markers")
            return False
    else:
        # Add new section before the footer
        insert_marker = '<div class="footer">'
        insert_index = index_content.rfind(insert_marker)
        
        if insert_index >= 0:
            index_content = index_content[:insert_index] + korea_section + "\n\n    " + index_content[insert_index:]
            print("✅ Added new Korea League section")
        else:
            print("❌ Could not find footer in index.html")
            return False
    
    # Update last updated timestamp
    timestamp_marker = "Last Updated:"
    timestamp_index = index_content.find(timestamp_marker)
    if timestamp_index >= 0:
        # Find the end of the timestamp line
        line_end = index_content.find("</p>", timestamp_index)
        if line_end >= 0:
            new_timestamp = f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            index_content = index_content[:timestamp_index] + new_timestamp + index_content[line_end:]
            print("✅ Updated timestamp")
    
    # Write updated index.html
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"✅ Successfully updated index.html")
        return True
    except Exception as e:
        print(f"❌ Error writing index.html: {str(e)}")
        return False

def create_korea_league_section(df):
    """Create HTML section for Korea K League 1 analysis"""
    # Create table rows for matches
    match_rows = ""
    for _, row in df.iterrows():
        # Convert date to readable format
        match_date = datetime.fromisoformat(row['date'].replace('Z', '+00:00'))
        formatted_time = match_date.strftime('%H:%M')
        
        # Determine confidence class
        confidence_class = "text-success fw-bold" if row['confidence_level'] == "HIGH" else "text-primary" if row['confidence_level'] == "MEDIUM" else ""
        row_class = "high-confidence-row" if row['confidence_level'] == "HIGH" else ""
        
        # Format prediction text
        prediction_text = ""
        if row['match_winner'] == "HOME":
            prediction_text = "Home Win"
        elif row['match_winner'] == "AWAY":
            prediction_text = "Away Win"
        else:
            prediction_text = "Draw"
        
        # Add match row
        match_rows += f"""
        <tr class="{row_class}">
            <td>{formatted_time}</td>
            <td>{row['home_team']} vs {row['away_team']}</td>
            <td class="{confidence_class}">{prediction_text} ({row['confidence']}%)</td>
            <td class="">{row['over_under']} ({row['over_under_confidence']}%)</td>
            <td class="">{row['btts']} ({row['btts_confidence']}%)</td>
            <td class="">{row['corners']} ({row['corners_confidence']}%)</td>
            <td class="text-muted">{row['score']} ({int(row['confidence'])}%)</td>
        </tr>
        """
    
    # Calculate value bets
    value_bets = []
    for _, row in df.iterrows():
        # Check for value in match winner market
        if row['match_winner'] == 'HOME' and (1/row['odds_home']) < (row['home_win_prob']/100):
            value = round((row['home_win_prob']/100) / (1/row['odds_home']) - 1, 2) * 100
            if value >= 5:  # At least 5% edge
                value_bets.append({
                    'match': f"{row['home_team']} vs {row['away_team']}",
                    'bet': f"Home Win @ {row['odds_home']}",
                    'edge': f"{value:.1f}%",
                    'confidence': f"{row['confidence']:.1f}%"
                })
        
        elif row['match_winner'] == 'DRAW' and (1/row['odds_draw']) < (row['draw_prob']/100):
            value = round((row['draw_prob']/100) / (1/row['odds_draw']) - 1, 2) * 100
            if value >= 5:
                value_bets.append({
                    'match': f"{row['home_team']} vs {row['away_team']}",
                    'bet': f"Draw @ {row['odds_draw']}",
                    'edge': f"{value:.1f}%",
                    'confidence': f"{row['confidence']:.1f}%"
                })
        
        elif row['match_winner'] == 'AWAY' and (1/row['odds_away']) < (row['away_win_prob']/100):
            value = round((row['away_win_prob']/100) / (1/row['odds_away']) - 1, 2) * 100
            if value >= 5:
                value_bets.append({
                    'match': f"{row['home_team']} vs {row['away_team']}",
                    'bet': f"Away Win @ {row['odds_away']}",
                    'edge': f"{value:.1f}%",
                    'confidence': f"{row['confidence']:.1f}%"
                })
        
        # Check for value in corners market
        corners_pred = row['corners'].split()
        corners_side = corners_pred[0]
        
        if corners_side == 'OVER' and row['corners_confidence']/100 > (1/row['odds_corners_over']):
            value = round((row['corners_confidence']/100) / (1/row['odds_corners_over']) - 1, 2) * 100
            if value >= 5:
                value_bets.append({
                    'match': f"{row['home_team']} vs {row['away_team']}",
                    'bet': f"Corners {corners_side} {row['corners_line']} @ {row['odds_corners_over']}",
                    'edge': f"{value:.1f}%",
                    'confidence': f"{row['corners_confidence']:.1f}%"
                })
        
        elif corners_side == 'UNDER' and row['corners_confidence']/100 > (1/row['odds_corners_under']):
            value = round((row['corners_confidence']/100) / (1/row['odds_corners_under']) - 1, 2) * 100
            if value >= 5:
                value_bets.append({
                    'match': f"{row['home_team']} vs {row['away_team']}",
                    'bet': f"Corners {corners_side} {row['corners_line']} @ {row['odds_corners_under']}",
                    'edge': f"{value:.1f}%",
                    'confidence': f"{row['corners_confidence']:.1f}%"
                })
    
    # Sort value bets by edge
    value_bets = sorted(value_bets, key=lambda x: float(x['edge'].strip('%')), reverse=True)
    
    # Create value bets HTML
    value_bets_html = ""
    for bet in value_bets[:3]:  # Show top 3 value bets
        value_bets_html += f"""
                                        <tr>
                                            <td>{bet['match']}</td>
                                            <td>{bet['bet']}</td>
                                            <td class="text-success">{bet['edge']}</td>
                                            <td>{bet['confidence']}</td>
                                        </tr>
        """
    
    # If no value bets found
    if not value_bets_html:
        value_bets_html = """
                                        <tr>
                                            <td colspan="4" class="text-center">No significant value bets detected</td>
                                        </tr>
        """
    
    # Create complete section HTML
    korea_section = f"""
    <!-- KOREA LEAGUE SECTION -->
    <div class="card mb-4">
        <div class="card-header bg-dark text-white">
            <h2 class="mb-0">🇰🇷 Korea K League 1 - July 18, 2025</h2>
            <p class="mb-0">Ultra Advanced ML Analysis with Corner Predictions</p>
        </div>
        
        <div class="card-body">
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i> 
                <strong>NEW:</strong> Korea K League 1 analysis with Ultra Advanced ML and corner predictions at 10.0 line.
            </div>
            
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">League Statistics</h5>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    Average Goals
                                    <span class="badge bg-primary rounded-pill">2.75</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    Home Win %
                                    <span class="badge bg-primary rounded-pill">46.5%</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    Avg. Corners
                                    <span class="badge bg-primary rounded-pill">10.4</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Value Bets Detected</h5>
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Match</th>
                                            <th>Bet</th>
                                            <th>Edge</th>
                                            <th>Confidence</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {value_bets_html}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Time</th>
                        <th>Match</th>
                        <th>Match Result</th>
                        <th>O/U 2.5</th>
                        <th>Both Teams Score</th>
                        <th>Corners</th>
                        <th>Exact Score</th>
                    </tr>
                </thead>
                <tbody>
                    {match_rows}
                </tbody>
            </table>
        </div>
    </div>
    <!-- END KOREA LEAGUE SECTION -->
    """
    
    return korea_section

def main():
    """Main function"""
    update_index_with_korea_league()

if __name__ == "__main__":
    main()
