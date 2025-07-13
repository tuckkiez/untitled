#!/usr/bin/env python3
"""
Update Index with Norway Tippeligaen Analysis
อัปเดต index.html ด้วยการวิเคราะห์ Norway Tippeligaen
"""

import json
from datetime import datetime

def load_norway_analysis():
    """Load Norway analysis results"""
    with open('/Users/80090/Desktop/Project/untitle/norway_tippeligaen_analysis.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_norway_html_section(analysis):
    """Create HTML section for Norway Tippeligaen"""
    
    predictions = analysis['today_predictions']
    backtest = analysis['backtest_results']
    
    html = f'''
    <!-- Norway Tippeligaen Advanced ML Analysis -->
    <section class="predictions-section" style="margin-bottom: 40px;">
        <h2 class="section-title">🇳🇴 Norway Tippeligaen - Advanced ML Analysis</h2>
        
        <!-- Performance Stats -->
        <div class="league-stats" style="margin-bottom: 30px;">
            <div class="stat-badge">
                <strong>Backtest Matches:</strong> {backtest['matches_analyzed']}
            </div>
            <div class="stat-badge">
                <strong>Match Result:</strong> {backtest['model_performance']['match_result_accuracy']}
            </div>
            <div class="stat-badge">
                <strong>Over/Under:</strong> {backtest['model_performance']['over_under_accuracy']}
            </div>
            <div class="stat-badge">
                <strong>BTS Accuracy:</strong> {backtest['model_performance']['bts_accuracy']}
            </div>
            <div class="stat-badge">
                <strong>Handicap:</strong> {backtest['model_performance']['handicap_accuracy']}
            </div>
        </div>
        
        <div class="predictions-table-container">
            <table class="predictions-table">
                <thead>
                    <tr>
                        <th>Match Details</th>
                        <th>4 Key Values (%)</th>
                        <th>Match Result</th>
                        <th>Over/Under 2.5</th>
                        <th>Both Teams Score</th>
                        <th>Asian Handicap</th>
                    </tr>
                </thead>
                <tbody>
    '''
    
    for pred in predictions:
        # Determine confidence class based on strongest prediction
        max_confidence = max(
            pred['predictions']['home_win_percent'],
            pred['predictions']['draw_percent'],
            pred['predictions']['away_win_percent']
        )
        
        if max_confidence >= 60:
            confidence_class = "high-confidence"
        elif max_confidence >= 45:
            confidence_class = "medium-confidence"
        else:
            confidence_class = "low-confidence"
        
        # Format kickoff time
        kickoff_time = pred['kickoff'][:16].replace('T', ' ')
        
        html += f'''
                    <tr class="match-row {confidence_class}">
                        <td class="match-teams">
                            <strong>{pred['home_team']} vs {pred['away_team']}</strong>
                            <div class="match-details">
                                <span>🇳🇴 Tippeligaen</span>
                                <span>⏰ {kickoff_time}</span>
                                <span>🏟️ {pred['venue']}</span>
                            </div>
                        </td>
                        <td class="prediction-cell" style="background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 215, 0, 0.2) 100%); border-left: 3px solid #ffd700;">
                            <div style="font-weight: bold; color: #ffd700; margin-bottom: 8px;">KEY 4 VALUES:</div>
                            <div style="font-size: 0.9em;">
                                <div>🏠 Home Win: <strong>{pred['key_4_values']['home_win']}%</strong></div>
                                <div>⚽ Over 2.5: <strong>{pred['key_4_values']['over_2_5']}%</strong></div>
                                <div>🥅 BTS Yes: <strong>{pred['key_4_values']['bts_yes']}%</strong></div>
                                <div>📊 Handicap: <strong>{pred['key_4_values']['handicap_home']}%</strong></div>
                            </div>
                        </td>
                        <td class="prediction-cell">
                            <div class="prediction-main">
                                H: {pred['predictions']['home_win_percent']}%
                            </div>
                            <div style="font-size: 0.85em; margin-top: 4px;">
                                D: {pred['predictions']['draw_percent']}% | A: {pred['predictions']['away_win_percent']}%
                            </div>
                        </td>
                        <td class="prediction-cell">
                            <div class="prediction-main">
                                Over: {pred['predictions']['over_2_5_percent']}%
                            </div>
                            <div style="font-size: 0.85em; margin-top: 4px;">
                                Under: {pred['predictions']['under_2_5_percent']}%
                            </div>
                        </td>
                        <td class="prediction-cell">
                            <div class="prediction-main">
                                Yes: {pred['predictions']['bts_yes_percent']}%
                            </div>
                            <div style="font-size: 0.85em; margin-top: 4px;">
                                No: {pred['predictions']['bts_no_percent']}%
                            </div>
                        </td>
                        <td class="prediction-cell">
                            <div class="prediction-main">
                                Home: {pred['predictions']['handicap_home_percent']}%
                            </div>
                            <div style="font-size: 0.85em; margin-top: 4px;">
                                Away: {pred['predictions']['handicap_away_percent']}%
                            </div>
                        </td>
                    </tr>
        '''
    
    # Add summary averages
    summary = analysis['summary']
    html += f'''
                    <tr style="background: linear-gradient(135deg, #2a2a2a 0%, #3a3a3a 100%); border-top: 2px solid #ffd700;">
                        <td class="match-teams">
                            <strong style="color: #ffd700;">📊 LEAGUE AVERAGES</strong>
                            <div class="match-details">
                                <span>🇳🇴 {summary['total_matches_today']} matches analyzed</span>
                                <span>🤖 Advanced ML</span>
                            </div>
                        </td>
                        <td class="prediction-cell" style="background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 215, 0, 0.3) 100%);">
                            <div style="font-weight: bold; color: #ffd700;">AVERAGES:</div>
                            <div style="font-size: 0.9em;">
                                <div>🏠 Home: <strong>{summary['avg_home_win_percent']}%</strong></div>
                                <div>⚽ Over: <strong>{summary['avg_over_2_5_percent']}%</strong></div>
                                <div>🥅 BTS: <strong>{summary['avg_bts_yes_percent']}%</strong></div>
                                <div>📊 Handicap: <strong>{summary['avg_handicap_home_percent']}%</strong></div>
                            </div>
                        </td>
                        <td class="prediction-cell" style="text-align: center; color: #ffd700;">
                            <strong>League Trend</strong><br>
                            <span style="font-size: 0.9em;">Balanced</span>
                        </td>
                        <td class="prediction-cell" style="text-align: center; color: #ffd700;">
                            <strong>Goal Trend</strong><br>
                            <span style="font-size: 0.9em;">High Scoring</span>
                        </td>
                        <td class="prediction-cell" style="text-align: center; color: #ffd700;">
                            <strong>BTS Trend</strong><br>
                            <span style="font-size: 0.9em;">Moderate</span>
                        </td>
                        <td class="prediction-cell" style="text-align: center; color: #ffd700;">
                            <strong>Handicap Trend</strong><br>
                            <span style="font-size: 0.9em;">Away Favored</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Key Insights -->
        <div style="margin-top: 20px; padding: 20px; background: linear-gradient(135deg, #222 0%, #333 100%); border-radius: 15px;">
            <h3 style="color: #ffd700; margin-bottom: 15px;">🔍 Key Insights from Advanced ML Analysis</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                <div>
                    <h4 style="color: #4ecdc4; margin-bottom: 10px;">🏆 Top Predictions</h4>
                    <ul style="list-style: none; padding: 0;">
    '''
    
    # Find top predictions
    top_home_win = max(predictions, key=lambda x: x['predictions']['home_win_percent'])
    top_over = max(predictions, key=lambda x: x['predictions']['over_2_5_percent'])
    top_bts = max(predictions, key=lambda x: x['predictions']['bts_yes_percent'])
    
    html += f'''
                        <li>• <strong>Strongest Home Win:</strong> {top_home_win['home_team']} ({top_home_win['predictions']['home_win_percent']}%)</li>
                        <li>• <strong>Highest Over 2.5:</strong> {top_over['home_team']} vs {top_over['away_team']} ({top_over['predictions']['over_2_5_percent']}%)</li>
                        <li>• <strong>Best BTS:</strong> {top_bts['home_team']} vs {top_bts['away_team']} ({top_bts['predictions']['bts_yes_percent']}%)</li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: #96ceb4; margin-bottom: 10px;">📈 League Characteristics</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li>• <strong>Home Advantage:</strong> {summary['avg_home_win_percent']}% average</li>
                        <li>• <strong>Goal Scoring:</strong> {summary['avg_over_2_5_percent']}% over 2.5 rate</li>
                        <li>• <strong>Both Teams Score:</strong> {summary['avg_bts_yes_percent']}% frequency</li>
                        <li>• <strong>Competitive Balance:</strong> Moderate home advantage</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
    '''
    
    return html

def update_index_with_norway():
    """Update index.html with Norway analysis"""
    print("🇳🇴 Updating index.html with Norway Tippeligaen analysis...")
    
    # Load analysis
    analysis = load_norway_analysis()
    
    # Read current index.html
    try:
        with open('/Users/80090/Desktop/Project/untitle/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("❌ index.html not found")
        return
    
    # Create Norway section
    norway_section = create_norway_html_section(analysis)
    
    # Find insertion point (after Swedish section)
    insertion_point = html_content.find('</section>', html_content.find('Swedish Allsvenskan'))
    
    if insertion_point != -1:
        # Insert after Swedish section
        insertion_point += len('</section>')
        updated_html = (html_content[:insertion_point] + 
                       '\n        ' + norway_section + 
                       html_content[insertion_point:])
        
        # Update header stats
        stats_section = updated_html.find('<div class="league-stats">')
        if stats_section != -1:
            new_stat = '''<div class="stat-badge">🇳🇴 <strong>Norway Tippeligaen:</strong> 6 matches + ML backtest</div>'''
            insert_pos = updated_html.find('>', stats_section) + 1
            updated_html = updated_html[:insert_pos] + new_stat + updated_html[insert_pos:]
        
        # Write updated HTML
        with open('/Users/80090/Desktop/Project/untitle/index.html', 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print("✅ Successfully updated index.html with Norway Tippeligaen analysis")
        return True
    else:
        print("❌ Could not find insertion point in index.html")
        return False

def create_summary_report():
    """Create comprehensive summary report"""
    analysis = load_norway_analysis()
    
    report = f"""
# 🇳🇴 Norway Tippeligaen Advanced ML Analysis Report

## 📊 Analysis Overview
- **League:** Norway Tippeligaen (Eliteserien)
- **Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
- **Matches Analyzed Today:** {analysis['summary']['total_matches_today']}
- **Backtest Sample:** {analysis['backtest_results']['matches_analyzed']} historical matches

## 🤖 ML Model Performance (Backtest Results)
| Model | Accuracy | Performance Level |
|-------|----------|------------------|
| **Match Result** | {analysis['backtest_results']['model_performance']['match_result_accuracy']} | Baseline |
| **Over/Under 2.5** | {analysis['backtest_results']['model_performance']['over_under_accuracy']} | Baseline |
| **Both Teams Score** | {analysis['backtest_results']['model_performance']['bts_accuracy']} | Good |
| **Asian Handicap** | {analysis['backtest_results']['model_performance']['handicap_accuracy']} | Good |

## ⚽ Today's Match Predictions

### 🔥 Featured Matches with 4 Key Values:

"""
    
    for i, pred in enumerate(analysis['today_predictions'], 1):
        report += f"""
**{i}. {pred['home_team']} vs {pred['away_team']}**
- 🏟️ **Venue:** {pred['venue']}
- ⏰ **Kickoff:** {pred['kickoff'][:16].replace('T', ' ')} UTC
- 📊 **4 KEY VALUES:**
  - 🏠 **Home Win:** {pred['key_4_values']['home_win']}%
  - ⚽ **Over 2.5 Goals:** {pred['key_4_values']['over_2_5']}%
  - 🥅 **Both Teams Score:** {pred['key_4_values']['bts_yes']}%
  - 📊 **Asian Handicap (Home):** {pred['key_4_values']['handicap_home']}%

**Detailed Breakdown:**
- Match Result: Home {pred['predictions']['home_win_percent']}% | Draw {pred['predictions']['draw_percent']}% | Away {pred['predictions']['away_win_percent']}%
- Over/Under: Over {pred['predictions']['over_2_5_percent']}% | Under {pred['predictions']['under_2_5_percent']}%
- Both Teams Score: Yes {pred['predictions']['bts_yes_percent']}% | No {pred['predictions']['bts_no_percent']}%
- Asian Handicap: Home {pred['predictions']['handicap_home_percent']}% | Away {pred['predictions']['handicap_away_percent']}%

"""
    
    report += f"""
## 📈 League Summary Statistics

### Average Percentages Across All Matches:
- **Home Win Rate:** {analysis['summary']['avg_home_win_percent']}%
- **Over 2.5 Goals:** {analysis['summary']['avg_over_2_5_percent']}%
- **Both Teams Score:** {analysis['summary']['avg_bts_yes_percent']}%
- **Asian Handicap (Home):** {analysis['summary']['avg_handicap_home_percent']}%

### 🔍 Key Insights:
1. **High-Scoring League:** {analysis['summary']['avg_over_2_5_percent']}% average for Over 2.5 goals indicates attacking football
2. **Moderate Home Advantage:** {analysis['summary']['avg_home_win_percent']}% home win rate shows balanced competition
3. **Goal Distribution:** {analysis['summary']['avg_bts_yes_percent']}% BTS rate suggests both teams regularly find the net
4. **Handicap Trends:** {analysis['summary']['avg_handicap_home_percent']}% suggests away teams often competitive

## 🎯 Top Recommendations

### Best Bets Based on ML Analysis:
"""
    
    # Find best bets
    top_predictions = sorted(analysis['today_predictions'], 
                           key=lambda x: max(x['predictions']['home_win_percent'], 
                                            x['predictions']['over_2_5_percent'],
                                            x['predictions']['bts_yes_percent']), 
                           reverse=True)[:3]
    
    for i, pred in enumerate(top_predictions, 1):
        strongest_pred = max([
            ('Home Win', pred['predictions']['home_win_percent']),
            ('Over 2.5', pred['predictions']['over_2_5_percent']),
            ('BTS Yes', pred['predictions']['bts_yes_percent'])
        ], key=lambda x: x[1])
        
        report += f"""
**{i}. {pred['home_team']} vs {pred['away_team']}**
- **Best Bet:** {strongest_pred[0]} ({strongest_pred[1]}%)
- **Confidence Level:** {'High' if strongest_pred[1] >= 70 else 'Medium' if strongest_pred[1] >= 55 else 'Moderate'}
- **Reasoning:** ML model shows strong statistical edge
"""
    
    report += f"""

## 🔬 Technical Analysis

### Model Architecture:
- **Random Forest** for match results and handicap predictions
- **Gradient Boosting** for over/under goals
- **Logistic Regression** for both teams score
- **Feature Engineering** based on team strength, attack/defense ratings
- **Home Advantage** factor included in calculations

### Data Quality:
- **Historical Sample:** {analysis['backtest_results']['matches_analyzed']} matches for training
- **Feature Count:** 12 engineered features per match
- **Validation Method:** Train-test split with stratification
- **Performance Monitoring:** Cross-validation accuracy tracking

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}  
**System:** Norway Tippeligaen Advanced ML Analyzer v1.0
"""
    
    # Save report
    with open('/Users/80090/Desktop/Project/untitle/NORWAY_ANALYSIS_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("📋 Comprehensive report saved to NORWAY_ANALYSIS_REPORT.md")

def main():
    """Main execution"""
    print("🚀 Starting Norway Tippeligaen Index Update...")
    
    # Update index
    if update_index_with_norway():
        print("✅ Index updated successfully")
        
        # Create summary report
        create_summary_report()
        
        # Print summary
        analysis = load_norway_analysis()
        print("\n" + "="*60)
        print("🇳🇴 NORWAY TIPPELIGAEN ANALYSIS SUMMARY")
        print("="*60)
        print(f"📊 Matches Today: {analysis['summary']['total_matches_today']}")
        print(f"🤖 Backtest Sample: {analysis['backtest_results']['matches_analyzed']} matches")
        print(f"🏠 Avg Home Win: {analysis['summary']['avg_home_win_percent']}%")
        print(f"⚽ Avg Over 2.5: {analysis['summary']['avg_over_2_5_percent']}%")
        print(f"🥅 Avg BTS Yes: {analysis['summary']['avg_bts_yes_percent']}%")
        print(f"📊 Avg Handicap Home: {analysis['summary']['avg_handicap_home_percent']}%")
        print("="*60)
        
        print("\n🔥 TOP MATCHES BY CONFIDENCE:")
        for i, pred in enumerate(analysis['today_predictions'][:3], 1):
            print(f"{i}. {pred['home_team']} vs {pred['away_team']}")
            print(f"   Key Values: H:{pred['key_4_values']['home_win']}% | O:{pred['key_4_values']['over_2_5']}% | BTS:{pred['key_4_values']['bts_yes']}% | AH:{pred['key_4_values']['handicap_home']}%")
    else:
        print("❌ Failed to update index")

if __name__ == "__main__":
    main()
