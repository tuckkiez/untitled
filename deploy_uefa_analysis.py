#!/usr/bin/env python3
"""
Deploy UEFA Champions League Analysis
Automated deployment script for Champions League qualifying matches
"""

import subprocess
import os
from datetime import datetime

def deploy_uefa_analysis():
    """Deploy UEFA Champions League analysis to GitHub Pages"""
    
    print("🚀 DEPLOYING UEFA CHAMPIONS LEAGUE ANALYSIS")
    print("=" * 50)
    
    try:
        # Change to project directory
        os.chdir('/Users/80090/Desktop/Project/untitle')
        
        # Add all files
        print("📁 Adding files to git...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        commit_message = f"🏆 Add UEFA Champions League Analysis - July 16, 2025"
        print(f"💾 Committing: {commit_message}")
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to GitHub
        print("🌐 Pushing to GitHub...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("\n✅ DEPLOYMENT SUCCESSFUL!")
        print("🔗 Live at: https://tuckkiez.github.io/untitled/")
        print("📄 UEFA Report: https://tuckkiez.github.io/untitled/uefa_champions_league_report.html")
        
        # Display summary
        print(f"\n📊 DEPLOYMENT SUMMARY:")
        print(f"• UEFA Champions League analysis deployed")
        print(f"• 2 qualifying matches analyzed")
        print(f"• Kickoff: 01:45 Thai time")
        print(f"• Professional predictions included")
        print(f"• HTML report generated")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_analysis_summary():
    """Show summary of UEFA Champions League analysis"""
    
    print(f"\n🏆 UEFA CHAMPIONS LEAGUE ANALYSIS SUMMARY")
    print("=" * 50)
    print("📅 Date: July 16, 2025")
    print("🏆 Competition: UEFA Champions League")
    print("🎯 Round: 1st Qualifying Round")
    print("⏰ Kickoff: 01:45 Thai Time (18:45 UTC)")
    
    print(f"\n🔥 MATCHES:")
    print("1. 🇧🇾 Dinamo Minsk vs Ludogorets 🇧🇬")
    print("   • Venue: Városi Stadion, Mezőkövesd")
    print("   • Prediction: Ludogorets Win (55%)")
    print("   • Goals: Over 2.5 (60%)")
    
    print("2. 🇬🇧 Linfield vs Shelbourne 🇮🇪")
    print("   • Venue: Windsor Park, Belfast")
    print("   • Prediction: Linfield Win (52%)")
    print("   • Goals: Under 2.5 (65%)")
    
    print(f"\n💡 KEY INSIGHTS:")
    print("• High-stakes European qualifying matches")
    print("• Quality referees appointed")
    print("• Late night kickoff for Thai viewers")
    print("• Competitive balance expected")

if __name__ == "__main__":
    show_analysis_summary()
    
    # Ask for deployment confirmation
    deploy = input(f"\n🚀 Deploy UEFA Champions League analysis? (y/n): ").lower().strip()
    
    if deploy == 'y' or deploy == 'yes':
        success = deploy_uefa_analysis()
        if success:
            print(f"\n🎉 UEFA Champions League analysis is now live!")
        else:
            print(f"\n😞 Deployment failed. Please check the errors above.")
    else:
        print(f"\n⏸️ Deployment cancelled.")
