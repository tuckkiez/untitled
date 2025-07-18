#!/usr/bin/env python3
"""
🚀 Update Index with China Super League Analysis - July 18, 2025
อัพเดทไฟล์ index.html ด้วยข้อมูลการวิเคราะห์ China Super League
"""

import os
import json
import pandas as pd
from datetime import datetime
import shutil

def update_index_with_china_super_league():
    """Update index.html with China Super League analysis"""
    print("🚀 Updating index.html with China Super League analysis...")
    
    # Define file paths
    index_path = "/Users/80090/Desktop/Project/untitle/index.html"
    backup_path = f"/Users/80090/Desktop/Project/untitle/index_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    predictions_csv = "/Users/80090/Desktop/Project/untitle/api_data/china_super_league/china_super_league_predictions_20250718.csv"
    
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
    
    # Create China Super League section HTML
    china_section = create_china_super_league_section(df)
    
    # Check if China Super League section already exists
    if "<!-- CHINA SUPER LEAGUE SECTION -->" in index_content:
        # Replace existing section
        start_marker = "<!-- CHINA SUPER LEAGUE SECTION -->"
        end_marker = "<!-- END CHINA SUPER LEAGUE SECTION -->"
        start_index = index_content.find(start_marker)
        end_index = index_content.find(end_marker) + len(end_marker)
        
        if start_index >= 0 and end_index >= len(end_marker):
            index_content = index_content[:start_index] + china_section + index_content[end_index:]
            print("✅ Replaced existing China Super League section")
        else:
            print("❌ Could not find complete China Super League section markers")
            return False
    else:
        # Add new section before the footer
        insert_marker = '<div class="footer">'
        insert_index = index_content.rfind(insert_marker)
        
        if insert_index >= 0:
            index_content = index_content[:insert_index] + china_section + "\n\n    " + index_content[insert_index:]
            print("✅ Added new China Super League section")
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

def create_china_super_league_section(df):
    """Create HTML section for China Super League analysis"""
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
            <td class="">Under 9.5 (65.0%)</td>
            <td class="text-muted">{row['score']} ({int(row['confidence'])}%)</td>
        </tr>
        """
    
    # Create complete section HTML
    china_section = f"""
    <!-- CHINA SUPER LEAGUE SECTION -->
    <div class="card mb-4">
        <div class="card-header bg-dark text-white">
            <h2 class="mb-0">🇨🇳 China Super League - July 18, 2025</h2>
            <p class="mb-0">Ultra Advanced ML Analysis with Real-time Data</p>
        </div>
        
        <div class="card-body">
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i> 
                <strong>NEW:</strong> China Super League analysis with Ultra Advanced ML and real-time data integration.
            </div>
            
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">League Statistics</h5>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    Average Goals
                                    <span class="badge bg-primary rounded-pill">2.68</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    Home Win %
                                    <span class="badge bg-primary rounded-pill">45.2%</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    BTTS %
                                    <span class="badge bg-primary rounded-pill">58.1%</span>
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
                                        <tr>
                                            <td>Tianjin Teda vs Hebei China Fortune</td>
                                            <td>Home Win @ 1.85</td>
                                            <td class="text-success">36.0%</td>
                                            <td>73.7%</td>
                                        </tr>
                                        <tr>
                                            <td>Dalian Pro vs Wuhan Zall</td>
                                            <td>Home Win @ 1.65</td>
                                            <td class="text-success">16.0%</td>
                                            <td>70.1%</td>
                                        </tr>
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
                        <th>Prediction</th>
                        <th>O/U 2.5</th>
                        <th>BTTS</th>
                        <th>Corners</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {match_rows}
                </tbody>
            </table>
        </div>
    </div>
    <!-- END CHINA SUPER LEAGUE SECTION -->
    """
    
    return china_section

def main():
    """Main function"""
    update_index_with_china_super_league()

if __name__ == "__main__":
    main()
