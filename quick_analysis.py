#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Quick Analysis Script
Run this for instant Value Bet analysis with current data
"""

import os
import sys
from datetime import datetime

def print_header():
    print("🚀 Ultra Advanced Football Predictor - Quick Analysis")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_files():
    """Check if required files exist"""
    required_files = [
        'corrected_value_bet_analyzer.py',
        'simple_value_bet_analyzer.py',
        'index.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def run_analysis():
    """Run the main analysis"""
    print("\n🔥 Running Value Bet Analysis...")
    print("-" * 40)
    
    try:
        # Import and run the corrected analyzer
        import subprocess
        result = subprocess.run([sys.executable, 'corrected_value_bet_analyzer.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Analysis completed successfully!")
            print("\n📊 Results:")
            print(result.stdout)
        else:
            print("❌ Analysis failed!")
            print(f"Error: {result.stderr}")
            
            # Try simple analyzer as fallback
            print("\n🔄 Trying simple analyzer...")
            result = subprocess.run([sys.executable, 'simple_value_bet_analyzer.py'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Simple analysis completed!")
                print(result.stdout)
            else:
                print("❌ Both analyzers failed!")
                
    except Exception as e:
        print(f"❌ Error running analysis: {e}")

def show_quick_commands():
    """Show quick commands for reference"""
    print("\n" + "=" * 60)
    print("⚡ Quick Commands")
    print("=" * 60)
    
    commands = [
        ("🔍 Run Analysis", "python corrected_value_bet_analyzer.py"),
        ("🌐 Open Website", "open https://tuckkiez.github.io/untitled/"),
        ("📊 Check Actions", "open https://github.com/tuckkiez/untitled/actions"),
        ("🚀 Quick Deploy", "./quick_deploy.sh"),
        ("📝 Git Status", "git status"),
        ("💾 Quick Commit", "git add . && git commit -m 'Update' && git push origin main")
    ]
    
    for desc, cmd in commands:
        print(f"{desc:20} | {cmd}")

def main():
    print_header()
    
    # Check current directory
    if not os.path.exists('index.html'):
        print("❌ Not in project directory!")
        print("💡 Please run: cd /Users/80090/Desktop/Project/untitle")
        return
    
    print("✅ In correct project directory")
    
    # Check files
    if not check_files():
        return
    
    # Run analysis
    run_analysis()
    
    # Show commands
    show_quick_commands()
    
    print("\n🎉 Quick analysis complete!")
    print("💡 Use the commands above for common tasks")

if __name__ == "__main__":
    main()
