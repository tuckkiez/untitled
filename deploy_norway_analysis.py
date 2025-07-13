#!/usr/bin/env python3
"""
Deploy Norway Tippeligaen Analysis
Deploy การวิเคราะห์ Norway Tippeligaen พร้อม push code
"""

import subprocess
import json
from datetime import datetime

def run_git_command(command, description):
    """Run git command"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, 
                              cwd='/Users/80090/Desktop/Project/untitle')
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def create_deployment_summary():
    """Create deployment summary"""
    
    # Load Norway analysis results
    with open('/Users/80090/Desktop/Project/untitle/norway_tippeligaen_analysis.json', 'r') as f:
        norway_data = json.load(f)
    
    summary = {
        "deployment_info": {
            "timestamp": datetime.now().isoformat(),
            "version": "Norway Tippeligaen Advanced ML v1.0",
            "league": "Norway Tippeligaen (Eliteserien)",
            "features_added": [
                "Advanced ML analysis with 4 key prediction values",
                "100-match backtest validation",
                "6 today's matches with detailed predictions",
                "Comprehensive statistical analysis",
                "Live HTML dashboard integration"
            ],
            "files_created": [
                "norway_tippeligaen_advanced_ml.py",
                "update_norway_analysis.py", 
                "deploy_norway_analysis.py",
                "NORWAY_ANALYSIS_REPORT.md",
                "norway_tippeligaen_analysis.json"
            ],
            "analysis_results": {
                "total_matches_today": norway_data['summary']['total_matches_today'],
                "backtest_sample_size": norway_data['backtest_results']['matches_analyzed'],
                "avg_home_win_percent": norway_data['summary']['avg_home_win_percent'],
                "avg_over_2_5_percent": norway_data['summary']['avg_over_2_5_percent'],
                "avg_bts_yes_percent": norway_data['summary']['avg_bts_yes_percent'],
                "avg_handicap_home_percent": norway_data['summary']['avg_handicap_home_percent']
            },
            "model_performance": norway_data['backtest_results']['model_performance'],
            "top_predictions": [
                {
                    "match": f"{pred['home_team']} vs {pred['away_team']}",
                    "key_4_values": pred['key_4_values']
                } for pred in norway_data['today_predictions'][:3]
            ]
        }
    }
    
    with open('/Users/80090/Desktop/Project/untitle/norway_deployment_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    return summary

def main():
    """Main deployment function"""
    print("🚀 Starting Norway Tippeligaen Analysis Deployment...")
    print("="*70)
    
    # Create deployment summary
    summary = create_deployment_summary()
    print("📋 Deployment summary created")
    
    # Git operations
    print("\n📦 Git Operations:")
    
    if run_git_command("git add .", "Adding all files"):
        commit_msg = f"feat: Add Norway Tippeligaen advanced ML analysis - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        if run_git_command(f'git commit -m "{commit_msg}"', "Committing changes"):
            if run_git_command("git push origin main", "Pushing to GitHub"):
                print("✅ Successfully deployed to GitHub!")
            else:
                print("⚠️ Push failed, but commit successful")
    
    # Display comprehensive summary
    print("\n" + "="*70)
    print("🇳🇴 NORWAY TIPPELIGAEN DEPLOYMENT COMPLETE")
    print("="*70)
    
    analysis = summary['deployment_info']['analysis_results']
    
    print("✅ Features Deployed:")
    for feature in summary['deployment_info']['features_added']:
        print(f"   • {feature}")
    
    print(f"\n📊 Analysis Summary:")
    print(f"   • League: {summary['deployment_info']['league']}")
    print(f"   • Matches Today: {analysis['total_matches_today']}")
    print(f"   • Backtest Sample: {analysis['backtest_sample_size']} matches")
    print(f"   • Average Home Win: {analysis['avg_home_win_percent']}%")
    print(f"   • Average Over 2.5: {analysis['avg_over_2_5_percent']}%")
    print(f"   • Average BTS Yes: {analysis['avg_bts_yes_percent']}%")
    print(f"   • Average Handicap Home: {analysis['avg_handicap_home_percent']}%")
    
    print(f"\n🔥 Top 3 Matches with 4 Key Values:")
    for i, pred in enumerate(summary['deployment_info']['top_predictions'], 1):
        values = pred['key_4_values']
        print(f"   {i}. {pred['match']}")
        print(f"      H:{values['home_win']}% | O:{values['over_2_5']}% | BTS:{values['bts_yes']}% | AH:{values['handicap_home']}%")
    
    print(f"\n🤖 Model Performance (Backtest):")
    perf = summary['deployment_info']['model_performance']
    print(f"   • Match Result: {perf['match_result_accuracy']}")
    print(f"   • Over/Under: {perf['over_under_accuracy']}")
    print(f"   • Both Teams Score: {perf['bts_accuracy']}")
    print(f"   • Asian Handicap: {perf['handicap_accuracy']}")
    
    print(f"\n🌐 Access Points:")
    print(f"   • Live Demo: https://tuckkiez.github.io/untitled/")
    print(f"   • GitHub: https://github.com/tuckkiez/untitled")
    print(f"   • Analysis Report: NORWAY_ANALYSIS_REPORT.md")
    
    print("="*70)
    print("🎯 Norway Tippeligaen Advanced ML Analysis Successfully Deployed!")
    print("="*70)

if __name__ == "__main__":
    main()
