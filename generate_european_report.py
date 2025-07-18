#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 European Leagues HTML Report Generator
สร้างรายงาน HTML สำหรับการวิเคราะห์ลีกยุโรป
"""

import json
import datetime
from datetime import datetime

def load_analysis_data():
    """Load analysis data from JSON file"""
    try:
        with open('european_leagues_analysis.json', 'r') as f:
            return json.load(f)
    except:
        print("Error: Could not load analysis data")
        return []

def group_matches_by_league(matches):
    """Group matches by league"""
    leagues = {}
    
    for match in matches:
        league_name = match["league"]
        if league_name not in leagues:
            leagues[league_name] = []
        
        leagues[league_name].append(match)
    
    return leagues

def find_value_bets(matches):
    """Find value bets with high confidence"""
    value_bets = []
    
    for match in matches:
        # Check for high confidence predictions (70%+)
        if match["match_result"]["confidence"] >= 70:
            value_bets.append({
                "match": match["match"],
                "league": match["league"],
                "bet": f"{match['match_result']['prediction']} @ 2.00",
                "edge": f"{round((match['match_result']['confidence'] * 2.00 / 100) - 1, 2) * 100:.1f}%",
                "confidence": f"{match['match_result']['confidence']:.1f}%"
            })
        
        if match["over_under"]["confidence"] >= 70:
            value_bets.append({
                "match": match["match"],
                "league": match["league"],
                "bet": f"{match['over_under']['prediction']} 2.5 @ 1.90",
                "edge": f"{round((match['over_under']['confidence'] * 1.90 / 100) - 1, 2) * 100:.1f}%",
                "confidence": f"{match['over_under']['confidence']:.1f}%"
            })
        
        if match["btts"]["confidence"] >= 70:
            value_bets.append({
                "match": match["match"],
                "league": match["league"],
                "bet": f"BTTS {match['btts']['prediction']} @ 1.95",
                "edge": f"{round((match['btts']['confidence'] * 1.95 / 100) - 1, 2) * 100:.1f}%",
                "confidence": f"{match['btts']['confidence']:.1f}%"
            })
        
        if match["corners"]["confidence"] >= 70:
            value_bets.append({
                "match": match["match"],
                "league": match["league"],
                "bet": f"Corners {match['corners']['prediction']} @ 2.00",
                "edge": f"{round((match['corners']['confidence'] * 2.00 / 100) - 1, 2) * 100:.1f}%",
                "confidence": f"{match['corners']['confidence']:.1f}%"
            })
    
    # Sort by confidence
    value_bets.sort(key=lambda x: float(x["confidence"].strip('%')), reverse=True)
    
    return value_bets

def calculate_league_stats(matches_by_league):
    """Calculate statistics for each league"""
    league_stats = {}
    
    for league_name, matches in matches_by_league.items():
        if not matches:
            continue
        
        # Calculate averages
        total_expected_corners = sum(match["corners"]["expected_corners"] for match in matches)
        avg_corners = total_expected_corners / len(matches)
        
        # Calculate home win percentage from predictions
        home_wins = sum(1 for match in matches if match["match_result"]["prediction"] == "Home Win")
        home_win_pct = home_wins / len(matches) * 100
        
        league_stats[league_name] = {
            "avg_corners": round(avg_corners, 1),
            "home_win_pct": round(home_win_pct, 1),
            "match_count": len(matches)
        }
    
    return league_stats

def generate_html_report(matches, value_bets, league_stats):
    """Generate HTML report"""
    # Group matches by league
    matches_by_league = group_matches_by_league(matches)
    
    # Start HTML content
    html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>🏆 European Leagues Analysis - July 18-19, 2025</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet"/>
    <style>
        :root {
            --primary-color: #ffffff;
            --secondary-color: #f8f9fa;
            --accent-color: #242233;
            --text-color: #333333;
            --text-muted: #6c757d;
            --success-color: #00b894;
            --warning-color: #fdcb6e;
            --danger-color: #e17055;
            --info-color: #0984e3;
            --highlight-color: #dfe6e9;
            --border-color: #e9ecef;
        }
        
        body {
            padding: 0;
            margin: 0;
            background-color: var(--primary-color);
            color: var(--text-color);
            font-family: monospace;
        }
        
        .container {
            max-width: 1400px;
            padding: 0;
        }
        
        .header {
            background: linear-gradient(135deg, #1e1a3d 0%, #333e60 100%);
            color: white;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .header h1 {
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 10px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .league-section {
            background-color: var(--secondary-color);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
            border: 1px solid var(--border-color);
        }
        
        .league-section h3 {
            color: var(--accent-color);
            font-weight: 600;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }
        
        .high-confidence-section {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(108, 92, 231, 0.15);
            margin-bottom: 30px;
            border: 1px solid #d6dee6;
        }
        
        .high-confidence-section h2 {
            color: var(--accent-color);
            font-weight: 700;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
        }
        
        .high-confidence-section h2 i {
            margin-right: 10px;
            font-size: 1.5em;
            color: #e30000;
        }
        
        .table {
            color: var(--text-color);
            border-collapse: separate;
            border-spacing: 0;
        }
        
        .table-dark {
            background-color: #495057;
            color: white;
        }
        
        .table-striped > tbody > tr:nth-of-type(odd) {
            background-color: rgba(0, 0, 0, 0.02);
        }
        
        .table-hover > tbody > tr:hover {
            background-color: rgba(108, 92, 231, 0.05);
        }
        
        .table-success {
            background-color: rgba(0, 184, 148, 0.1) !important;
        }
        
        .text-success {
            color: var(--success-color) !important;
        }
        
        .text-warning {
            color: var(--warning-color) !important;
        }
        
        .text-danger {
            color: var(--danger-color) !important;
        }
        
        .text-primary {
            color: var(--info-color) !important;
        }
        
        .text-muted {
            color: var(--text-muted) !important;
        }
        
        .fw-bold {
            font-weight: 700 !important;
        }
        
        .footer {
            margin-top: 30px;
            text-align: center;
            color: var(--text-muted);
            padding: 20px;
            border-top: 1px solid var(--border-color);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--primary-color);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #5549c9;
        }
        
        /* ปรับแต่งตาราง */
        .table thead th {
            background-color: #363636;
            color: white;
            border-color: #495057;
        }
        
        .table td, .table th {
            padding: 12px;
            vertical-align: middle;
        }
        
        /* ปรับแต่งแถวที่มีความเชื่อมั่นสูง */
        .high-confidence-row {
            background-color: rgb(18 251 52 / 10%) !important;
            font-weight: 500;
        }
    </style>
</head>
<body>
<div class="container py-4">
    <div class="header">
        <h1>🏆 European Leagues Analysis - July 18-19, 2025</h1>
        <p>Ultra Advanced ML Analysis with Corner Predictions at 10.0 Line</p>
    </div>
"""
    
    # Add value bets section
    if value_bets:
        html += """
    <div class="card mb-4">
        <div class="card-header bg-dark text-white">
            <h2 class="mb-0">🔥 High Confidence Value Bets</h2>
            <p class="mb-0">Selections with 70%+ confidence and positive expected value</p>
        </div>
        <div class="card-body">
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                <strong>NEW:</strong> Value bets identified using Ultra Advanced ML with Edge and Confidence metrics.
            </div>
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Match</th>
                            <th>League</th>
                            <th>Bet</th>
                            <th>Edge</th>
                            <th>Confidence</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        
        for bet in value_bets:
            html += f"""
                        <tr>
                            <td>{bet['match']}</td>
                            <td>{bet['league']}</td>
                            <td>{bet['bet']}</td>
                            <td class="text-success">{bet['edge']}</td>
                            <td>{bet['confidence']}</td>
                        </tr>
"""
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
    </div>
"""
    
    # Add league sections
    for league_name, league_matches in matches_by_league.items():
        if not league_matches:
            continue
        
        # Get league flag emoji
        flag_emoji = "🇪🇺"  # Default
        if "Norway" in league_name:
            flag_emoji = "🇳🇴"
        elif "Danish" in league_name or "Denmark" in league_name:
            flag_emoji = "🇩🇰"
        elif "Ireland" in league_name:
            flag_emoji = "🇮🇪"
        elif "Finnish" in league_name or "Finland" in league_name:
            flag_emoji = "🇫🇮"
        elif "Russian" in league_name or "Russia" in league_name:
            flag_emoji = "🇷🇺"
        elif "Romania" in league_name:
            flag_emoji = "🇷🇴"
        elif "Poland" in league_name:
            flag_emoji = "🇵🇱"
        elif "Iceland" in league_name:
            flag_emoji = "🇮🇸"
        
        stats = league_stats.get(league_name, {"avg_corners": 10.0, "home_win_pct": 45.0, "match_count": len(league_matches)})
        
        html += f"""
    <div class="card mb-4">
        <div class="card-header bg-dark text-white">
            <h2 class="mb-0">{flag_emoji} {league_name} - July 18-19, 2025</h2>
            <p class="mb-0">Ultra Advanced ML Analysis with Corner Predictions at 10.0 Line</p>
        </div>
        <div class="card-body">
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                <strong>NEW:</strong> {league_name} analysis with Ultra Advanced ML and corner predictions at 10.0 line for {stats['match_count']} matches.
            </div>
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">League Statistics</h5>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    Average Corners
                                    <span class="badge bg-primary rounded-pill">{stats['avg_corners']}</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    Home Win %
                                    <span class="badge bg-primary rounded-pill">{stats['home_win_pct']}%</span>
                                </li>
                                <li class="list-group-item d-flex justify-content-between align-items-center">
                                    Matches Analyzed
                                    <span class="badge bg-primary rounded-pill">{stats['match_count']}</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">League Value Bets</h5>
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
"""
        
        # Add league-specific value bets
        league_value_bets = [bet for bet in value_bets if bet["league"] == league_name]
        if league_value_bets:
            for bet in league_value_bets[:3]:  # Show top 3
                html += f"""
                                        <tr>
                                            <td>{bet['match']}</td>
                                            <td>{bet['bet']}</td>
                                            <td class="text-success">{bet['edge']}</td>
                                            <td>{bet['confidence']}</td>
                                        </tr>
"""
        else:
            html += """
                                        <tr>
                                            <td colspan="4" class="text-center">No high confidence value bets found</td>
                                        </tr>
"""
        
        html += """
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
"""
        
        # Add matches
        for match in league_matches:
            # Determine if this is a high confidence row
            high_confidence = match["high_confidence"]
            row_class = "high-confidence-row" if high_confidence else ""
            
            # Format match result
            match_result = match["match_result"]["prediction"]
            match_confidence = match["match_result"]["confidence"]
            match_result_class = "text-success fw-bold" if match_confidence >= 70 else ""
            
            # Format over/under
            over_under = match["over_under"]["prediction"]
            over_under_confidence = match["over_under"]["confidence"]
            over_under_class = "text-success fw-bold" if over_under_confidence >= 70 else ""
            
            # Format BTTS
            btts = match["btts"]["prediction"]
            btts_confidence = match["btts"]["confidence"]
            btts_class = "text-success fw-bold" if btts_confidence >= 70 else ""
            
            # Format corners
            corners = match["corners"]["prediction"]
            corners_confidence = match["corners"]["confidence"]
            corners_class = "text-success fw-bold" if corners_confidence >= 70 else ""
            
            # Format exact score
            exact_score = match["exact_score"]["prediction"]
            exact_score_confidence = match["exact_score"]["confidence"]
            
            html += f"""
                    <tr class="{row_class}">
                        <td>{match['time']}</td>
                        <td>{match['match']}</td>
                        <td class="{match_result_class}">{match_result} ({match_confidence}%)</td>
                        <td class="{over_under_class}">{over_under} ({over_under_confidence}%)</td>
                        <td class="{btts_class}">{btts} ({btts_confidence}%)</td>
                        <td class="{corners_class}">{corners} ({corners_confidence}%)</td>
                        <td class="text-muted">{exact_score} ({exact_score_confidence}%)</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
    </div>
"""
    
    # Add footer
    now = datetime.now()
    html += f"""
    <div class="footer">
        <p>Last updated: {now.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>© 2025 Ultra Advanced Multi-League Football Predictor</p>
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    
    return html

def save_html_report(html_content, filename="european_leagues_report.html"):
    """Save HTML report to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML report saved to {filename}")

def main():
    # Load analysis data
    matches = load_analysis_data()
    
    if not matches:
        print("No analysis data found. Please run analyze_european_leagues.py first.")
        return
    
    # Group matches by league
    matches_by_league = group_matches_by_league(matches)
    
    # Find value bets
    value_bets = find_value_bets(matches)
    
    # Calculate league stats
    league_stats = calculate_league_stats(matches_by_league)
    
    # Generate HTML report
    html_content = generate_html_report(matches, value_bets, league_stats)
    
    # Save HTML report
    save_html_report(html_content)

if __name__ == "__main__":
    main()
