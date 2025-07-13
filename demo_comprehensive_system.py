#!/usr/bin/env python3
"""
Demo Script for Comprehensive Football Prediction System
สคริปต์สาธิตระบบทำนายฟุตบอลครบวงจร
"""

import os
import sys
import time
from datetime import datetime

def print_banner():
    """Print system banner"""
    print("🚀" + "=" * 58 + "🚀")
    print("🏆  COMPREHENSIVE FOOTBALL PREDICTION SYSTEM DEMO  🏆")
    print("🚀" + "=" * 58 + "🚀")
    print("📅 Date: July 13, 2025")
    print("🌍 Coverage: All Major Leagues Worldwide")
    print("🤖 Technology: Advanced ML + Real Odds Integration")
    print("💰 Features: Live Odds + Multi-League Predictions")
    print("=" * 62)

def check_dependencies():
    """Check if all required modules are available"""
    print("🔍 Checking system dependencies...")
    
    required_modules = [
        'requests', 'pandas', 'numpy', 'sklearn', 'sqlite3', 'json'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'sklearn':
                import sklearn
            else:
                __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Missing modules: {', '.join(missing_modules)}")
        print("📦 Install with: pip install -r requirements_comprehensive.txt")
        return False
    
    print("✅ All dependencies satisfied!")
    return True

def demo_data_collection():
    """Demo data collection phase"""
    print("\n🔄 PHASE 1: DATA COLLECTION DEMO")
    print("-" * 40)
    
    print("📊 Simulating fixture collection...")
    time.sleep(1)
    
    # Simulate league data
    leagues_demo = {
        "Premier League": 8,
        "La Liga": 6,
        "Bundesliga": 5,
        "Serie A": 7,
        "Ligue 1": 4,
        "K League 2": 3,
        "J-League": 9,
        "MLS": 12,
        "Liga MX": 8
    }
    
    total_fixtures = sum(leagues_demo.values())
    
    for league, fixtures in leagues_demo.items():
        print(f"  📈 {league}: {fixtures} fixtures")
        time.sleep(0.2)
    
    print(f"\n✅ Total: {total_fixtures} fixtures across {len(leagues_demo)} leagues")
    
    print("\n💰 Simulating odds collection...")
    time.sleep(1)
    
    odds_success_rate = 0.85
    fixtures_with_odds = int(total_fixtures * odds_success_rate)
    
    print(f"  💰 Odds collected for {fixtures_with_odds}/{total_fixtures} fixtures")
    print(f"  📊 Success rate: {odds_success_rate:.1%}")
    
    return total_fixtures, fixtures_with_odds

def demo_ml_training():
    """Demo ML training phase"""
    print("\n🤖 PHASE 2: MACHINE LEARNING DEMO")
    print("-" * 40)
    
    print("📈 Simulating feature engineering...")
    time.sleep(1)
    
    features_demo = [
        "Market odds (Home/Draw/Away)",
        "Over/Under 2.5 odds",
        "Both Teams to Score odds",
        "Implied probabilities",
        "Market margins",
        "League strength factors",
        "Historical performance"
    ]
    
    for feature in features_demo:
        print(f"  🔧 {feature}")
        time.sleep(0.3)
    
    print("\n🎯 Simulating model training...")
    time.sleep(1)
    
    models_demo = {
        "Match Result": {
            "Random Forest": 0.642,
            "Gradient Boosting": 0.658,
            "Logistic Regression": 0.635
        },
        "Over/Under 2.5": {
            "Random Forest": 0.721,
            "Gradient Boosting": 0.734,
            "Logistic Regression": 0.698
        },
        "Both Teams Score": {
            "Random Forest": 0.687,
            "Gradient Boosting": 0.695,
            "Logistic Regression": 0.672
        }
    }
    
    for prediction_type, models in models_demo.items():
        print(f"\n  📊 {prediction_type} Models:")
        for model_name, accuracy in models.items():
            print(f"    • {model_name}: {accuracy:.1%} accuracy")
            time.sleep(0.2)
    
    return models_demo

def demo_predictions():
    """Demo predictions phase"""
    print("\n🔮 PHASE 3: PREDICTIONS DEMO")
    print("-" * 40)
    
    print("🎲 Generating sample predictions...")
    time.sleep(1)
    
    sample_predictions = [
        {
            "match": "Manchester City vs Arsenal",
            "league": "Premier League",
            "prediction": "Home Win",
            "confidence": 0.78,
            "over_under": "Over 2.5",
            "btts": "Yes"
        },
        {
            "match": "Real Madrid vs Barcelona",
            "league": "La Liga", 
            "prediction": "Draw",
            "confidence": 0.65,
            "over_under": "Over 2.5",
            "btts": "Yes"
        },
        {
            "match": "Bayern Munich vs Dortmund",
            "league": "Bundesliga",
            "prediction": "Home Win",
            "confidence": 0.82,
            "over_under": "Over 2.5",
            "btts": "Yes"
        },
        {
            "match": "Incheon United vs Asan Mugunghwa",
            "league": "K League 2",
            "prediction": "Draw",
            "confidence": 0.71,
            "over_under": "Under 2.5",
            "btts": "No"
        }
    ]
    
    print("🎯 Top Confidence Predictions:")
    for i, pred in enumerate(sample_predictions, 1):
        print(f"\n  {i}. {pred['match']} ({pred['league']})")
        print(f"     🏆 Result: {pred['prediction']} ({pred['confidence']:.1%})")
        print(f"     ⚽ Goals: {pred['over_under']}")
        print(f"     🎯 BTTS: {pred['btts']}")
        time.sleep(0.5)
    
    return sample_predictions

def demo_summary():
    """Demo final summary"""
    print("\n📊 COMPREHENSIVE ANALYSIS SUMMARY")
    print("=" * 50)
    
    print("📈 DATA COLLECTION:")
    print("  • Total Leagues: 9")
    print("  • Total Fixtures: 62")
    print("  • Odds Coverage: 85.5%")
    
    print("\n🤖 MACHINE LEARNING:")
    print("  • Models Trained: 9 (3 types × 3 algorithms)")
    print("  • Best Accuracy: 73.4% (Over/Under)")
    print("  • Average Accuracy: 68.2%")
    
    print("\n🔮 PREDICTIONS:")
    print("  • Total Predictions: 62")
    print("  • High Confidence (>70%): 28")
    print("  • Leagues Covered: 9")
    
    print("\n🎯 SYSTEM CAPABILITIES:")
    capabilities = [
        "✅ Real-time odds integration",
        "✅ Multi-league coverage",
        "✅ Advanced ML algorithms",
        "✅ Ensemble predictions",
        "✅ Confidence scoring",
        "✅ Multiple bet types",
        "✅ Database persistence",
        "✅ Export capabilities"
    ]
    
    for capability in capabilities:
        print(f"  {capability}")
        time.sleep(0.2)

def main():
    """Main demo function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Demo cannot proceed without required dependencies")
        return
    
    print("\n🎬 Starting system demonstration...")
    time.sleep(2)
    
    # Demo phases
    total_fixtures, fixtures_with_odds = demo_data_collection()
    time.sleep(1)
    
    models_results = demo_ml_training()
    time.sleep(1)
    
    predictions = demo_predictions()
    time.sleep(1)
    
    demo_summary()
    
    print("\n" + "=" * 50)
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    
    print("\n🚀 To run the actual system:")
    print("   python comprehensive_prediction_system.py")
    
    print("\n📚 Available components:")
    print("   • comprehensive_odds_fetcher.py - Data collection")
    print("   • advanced_ml_with_real_odds.py - ML training")
    print("   • comprehensive_prediction_system.py - Full pipeline")
    
    print("\n💡 Features:")
    print("   🌍 Global league coverage")
    print("   💰 Real betting odds integration")
    print("   🤖 Advanced ML predictions")
    print("   📊 Comprehensive analytics")
    print("   💾 Database persistence")
    
    print("\n🎯 Ready for production use!")

if __name__ == "__main__":
    main()
