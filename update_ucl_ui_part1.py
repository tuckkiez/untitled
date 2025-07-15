#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏆 UEFA CHAMPIONS LEAGUE UI UPDATER - PART 1
อัพเดต UI ด้วยข้อมูลแมตช์ UCL จริงและลบข้อมูลเก่า
"""

import json
from datetime import datetime

class UCLUIUpdater:
    def __init__(self):
        self.analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def generate_ucl_html_header(self):
        """สร้าง HTML header สำหรับ UCL"""
        return """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 UEFA Champions League 2025-26 - Advanced ML Analysis</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            min-width: 120px;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #FFD700;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .matches-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .match-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .match-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .match-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .match-title {
            font-size: 1.4em;
            font-weight: bold;
        }
        
        .match-time {
            background: #FFD700;
            color: #1e3c72;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .teams-section {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .team {
            text-align: center;
            flex: 1;
        }
        
        .team-name {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .team-country {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .team-strength {
            font-size: 1.1em;
            color: #FFD700;
            margin-top: 5px;
        }
        
        .vs {
            font-size: 1.5em;
            font-weight: bold;
            color: #FFD700;
            margin: 0 20px;
        }
        
        .predictions-section {
            margin-bottom: 20px;
        }
        
        .prediction-category {
            margin-bottom: 15px;
        }
        
        .category-title {
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 8px;
            color: #FFD700;
        }
        
        .prediction-bars {
            display: flex;
            gap: 10px;
            margin-bottom: 5px;
        }
        
        .prediction-bar {
            flex: 1;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            overflow: hidden;
            position: relative;
            height: 30px;
        }
        
        .prediction-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            transition: width 0.8s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .prediction-fill.draw {
            background: linear-gradient(90deg, #FF9800, #FFC107);
        }
        
        .prediction-fill.away {
            background: linear-gradient(90deg, #f44336, #FF5722);
        }
        
        .prediction-fill.over {
            background: linear-gradient(90deg, #2196F3, #03A9F4);
        }
        
        .prediction-fill.under {
            background: linear-gradient(90deg, #9C27B0, #E91E63);
        }
        
        .prediction-labels {
            display: flex;
            justify-content: space-between;
            font-size: 0.8em;
            margin-top: 3px;
            opacity: 0.8;
        }
        
        .betting-recommendations {
            background: rgba(255, 215, 0, 0.1);
            border: 1px solid #FFD700;
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }
        
        .betting-title {
            font-size: 1.1em;
            font-weight: bold;
            color: #FFD700;
            margin-bottom: 10px;
        }
        
        .bet-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            padding: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
        }
        
        .bet-rank {
            font-weight: bold;
            margin-right: 10px;
        }
        
        .bet-confidence {
            background: #4CAF50;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .venue-info {
            font-size: 0.9em;
            opacity: 0.8;
            text-align: center;
            margin-bottom: 15px;
        }
        
        .high-confidence {
            border: 2px solid #FFD700;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .update-time {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 10px;
        }
        
        .ml-info {
            font-size: 1em;
            margin-bottom: 15px;
        }
        
        .confidence-legend {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
        }
        
        .legend-high { background: #FFD700; }
        .legend-medium { background: #4CAF50; }
        .legend-low { background: #FF9800; }
        
        @media (max-width: 768px) {
            .matches-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .stats-bar {
                flex-direction: column;
                gap: 15px;
            }
            
            .teams-section {
                flex-direction: column;
                gap: 15px;
            }
            
            .vs {
                margin: 10px 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 UEFA Champions League 2025-26</h1>
            <div class="subtitle">Qualifying Round 1 - Advanced ML Analysis</div>
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-number">12</div>
                    <div class="stat-label">Matches</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">6</div>
                    <div class="stat-label">High Confidence</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">63.8%</div>
                    <div class="stat-label">Avg Confidence</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">4</div>
                    <div class="stat-label">ML Models</div>
                </div>
            </div>
        </div>
"""
    
    def save_html_header(self):
        """บันทึก HTML header"""
        header_html = self.generate_ucl_html_header()
        
        with open('/Users/80090/Desktop/Project/untitle/ucl_ui_header.html', 'w', encoding='utf-8') as f:
            f.write(header_html)
        
        print("✅ UCL UI Header created successfully!")
        return header_html

def main():
    """Main execution"""
    updater = UCLUIUpdater()
    
    print("🚀 Creating UEFA Champions League UI Header...")
    
    try:
        updater.save_html_header()
        print("✅ Part 1 completed - HTML header ready!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
