#!/usr/bin/env python3
"""
🚀 Check High Confidence Scores - July 17-18, 2025
ตรวจสอบการทำนายสกอร์ที่มีความมั่นใจ 80% ขึ้นไป
"""

import json

def main():
    """ฟังก์ชันหลัก"""
    print("🚀 Check High Confidence Scores - July 17-18, 2025")
    print("=" * 60)
    
    # โหลดข้อมูลผลการวิเคราะห์
    try:
        with open('uefa_competitions_real_data_analysis_with_score.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        high_confidence_scores = []
        
        for league in ['europa_league', 'conference_league']:
            for match in data[league]:
                if match['exact_score']['confidence'] >= 80:
                    high_confidence_scores.append((
                        match['home_team'],
                        match['away_team'],
                        match['exact_score']['most_likely_score'],
                        match['exact_score']['confidence']
                    ))
        
        print(f"การทำนายสกอร์ที่มีความมั่นใจ 80% ขึ้นไป: {len(high_confidence_scores)}")
        
        for i, (home, away, score, conf) in enumerate(high_confidence_scores):
            print(f"{i+1}. {home} vs {away}: {score} ({conf}%)")
        
        # ตรวจสอบการทำนายสกอร์ที่มีความมั่นใจสูงสุด 5 อันดับแรก
        all_scores = []
        
        for league in ['europa_league', 'conference_league']:
            for match in data[league]:
                all_scores.append((
                    match['home_team'],
                    match['away_team'],
                    match['exact_score']['most_likely_score'],
                    match['exact_score']['confidence']
                ))
        
        all_scores.sort(key=lambda x: x[3], reverse=True)
        
        print("\nการทำนายสกอร์ที่มีความมั่นใจสูงสุด 5 อันดับแรก:")
        
        for i, (home, away, score, conf) in enumerate(all_scores[:5]):
            print(f"{i+1}. {home} vs {away}: {score} ({conf}%)")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
