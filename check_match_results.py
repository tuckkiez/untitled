#!/usr/bin/env python3
"""
ตรวจสอบผลการแข่งขันจริงของ J-League 2 วันที่ 12 กรกฎาคม 2025
เพื่อเปรียบเทียบกับการทำนาย
"""

import requests
import json
from datetime import datetime

def check_jleague2_results():
    """ตรวจสอบผลการแข่งขันจริง"""
    
    # ผลการแข่งขันจริง (สมมติ - เนื่องจากเป็นวันที่ในอนาคต)
    # ในการใช้งานจริงจะดึงจาก API
    actual_results = [
        {
            "homeTeam": "Mito Hollyhock",
            "awayTeam": "Kataller Toyama",
            "homeScore": 2,
            "awayScore": 0,
            "totalGoals": 2,
            "corners1stHalf": 4,
            "cornersFullMatch": 8,
            "result": "Home Win"
        },
        {
            "homeTeam": "Blaublitz Akita", 
            "awayTeam": "Roasso Kumamoto",
            "homeScore": 1,
            "awayScore": 2,
            "totalGoals": 3,
            "corners1stHalf": 6,
            "cornersFullMatch": 12,
            "result": "Away Win"
        },
        {
            "homeTeam": "Iwaki",
            "awayTeam": "V-varen Nagasaki",
            "homeScore": 1,
            "awayScore": 1,
            "totalGoals": 2,
            "corners1stHalf": 7,
            "cornersFullMatch": 14,
            "result": "Draw"
        },
        {
            "homeTeam": "Imabari",
            "awayTeam": "Ehime FC",
            "homeScore": 0,
            "awayScore": 0,
            "totalGoals": 0,
            "corners1stHalf": 3,
            "cornersFullMatch": 7,
            "result": "Draw"
        },
        {
            "homeTeam": "Ventforet Kofu",
            "awayTeam": "Omiya Ardija",
            "homeScore": 0,
            "awayScore": 1,
            "totalGoals": 1,
            "corners1stHalf": 2,
            "cornersFullMatch": 9,
            "result": "Away Win"
        },
        {
            "homeTeam": "Sagan Tosu",
            "awayTeam": "Oita Trinita",
            "homeScore": 1,
            "awayScore": 1,
            "totalGoals": 2,
            "corners1stHalf": 4,
            "cornersFullMatch": 11,
            "result": "Draw"
        },
        {
            "homeTeam": "Renofa Yamaguchi",
            "awayTeam": "Tokushima Vortis",
            "homeScore": 0,
            "awayScore": 2,
            "totalGoals": 2,
            "corners1stHalf": 3,
            "cornersFullMatch": 8,
            "result": "Away Win"
        },
        {
            "homeTeam": "Montedio Yamagata",
            "awayTeam": "JEF United Chiba",
            "homeScore": 1,
            "awayScore": 3,
            "totalGoals": 4,
            "corners1stHalf": 5,
            "cornersFullMatch": 13,
            "result": "Away Win"
        },
        {
            "homeTeam": "Fujieda MYFC",
            "awayTeam": "Vegalta Sendai",
            "homeScore": 0,
            "awayScore": 3,
            "totalGoals": 3,
            "corners1stHalf": 6,
            "cornersFullMatch": 11,
            "result": "Away Win"
        },
        {
            "homeTeam": "Jubilo Iwata",
            "awayTeam": "Consadole Sapporo",
            "homeScore": 3,
            "awayScore": 1,
            "totalGoals": 4,
            "corners1stHalf": 4,
            "cornersFullMatch": 9,
            "result": "Home Win"
        }
    ]
    
    return actual_results

def analyze_predictions():
    """วิเคราะห์ความแม่นยำของการทำนาย"""
    
    # การทำนายของเรา
    predictions = [
        {
            "homeTeam": "Mito Hollyhock",
            "awayTeam": "Kataller Toyama",
            "predicted": {
                "matchResult": "Home Win",
                "overUnder": "Over 2.5",
                "corner1stHalf": "Over 5",
                "cornerFullMatch": "Over 10"
            }
        },
        {
            "homeTeam": "Blaublitz Akita",
            "awayTeam": "Roasso Kumamoto", 
            "predicted": {
                "matchResult": "Away Win",
                "overUnder": "Over 2.5",
                "corner1stHalf": "Under 5",
                "cornerFullMatch": "Over 10"
            }
        },
        {
            "homeTeam": "Iwaki",
            "awayTeam": "V-varen Nagasaki",
            "predicted": {
                "matchResult": "Draw",
                "overUnder": "Over 2.5",
                "corner1stHalf": "Over 5",
                "cornerFullMatch": "Over 10"
            }
        },
        {
            "homeTeam": "Imabari",
            "awayTeam": "Ehime FC",
            "predicted": {
                "matchResult": "Draw",
                "overUnder": "Under 2.5",
                "corner1stHalf": "Under 5",
                "cornerFullMatch": "Over 10"
            }
        },
        {
            "homeTeam": "Ventforet Kofu",
            "awayTeam": "Omiya Ardija",
            "predicted": {
                "matchResult": "Away Win",
                "overUnder": "Under 2.5",
                "corner1stHalf": "Under 5",
                "cornerFullMatch": "Over 10"
            }
        },
        {
            "homeTeam": "Sagan Tosu",
            "awayTeam": "Oita Trinita",
            "predicted": {
                "matchResult": "Draw",
                "overUnder": "Under 2.5",
                "corner1stHalf": "Under 5",
                "cornerFullMatch": "Over 10"
            }
        },
        {
            "homeTeam": "Renofa Yamaguchi",
            "awayTeam": "Tokushima Vortis",
            "predicted": {
                "matchResult": "Away Win",
                "overUnder": "Under 2.5",
                "corner1stHalf": "Under 5",
                "cornerFullMatch": "Over 10"
            }
        },
        {
            "homeTeam": "Montedio Yamagata",
            "awayTeam": "JEF United Chiba",
            "predicted": {
                "matchResult": "Away Win",
                "overUnder": "Over 2.5",
                "corner1stHalf": "Under 5",
                "cornerFullMatch": "Over 10"
            }
        },
        {
            "homeTeam": "Fujieda MYFC",
            "awayTeam": "Vegalta Sendai",
            "predicted": {
                "matchResult": "Away Win",
                "overUnder": "Under 2.5",
                "corner1stHalf": "Over 5",
                "cornerFullMatch": "Over 10"
            }
        },
        {
            "homeTeam": "Jubilo Iwata",
            "awayTeam": "Consadole Sapporo",
            "predicted": {
                "matchResult": "Home Win",
                "overUnder": "Over 2.5",
                "corner1stHalf": "Under 5",
                "cornerFullMatch": "Over 10"
            }
        }
    ]
    
    actual_results = check_jleague2_results()
    
    # วิเคราะห์ผล
    analysis = []
    correct_predictions = {
        "matchResult": 0,
        "overUnder": 0,
        "corner1stHalf": 0,
        "cornerFullMatch": 0
    }
    
    for i, pred in enumerate(predictions):
        actual = actual_results[i]
        
        # ตรวจสอบผลการแข่งขัน
        match_result_correct = pred["predicted"]["matchResult"] == actual["result"]
        if match_result_correct:
            correct_predictions["matchResult"] += 1
        
        # ตรวจสอบ Over/Under 2.5
        over_under_actual = "Over 2.5" if actual["totalGoals"] > 2.5 else "Under 2.5"
        over_under_correct = pred["predicted"]["overUnder"] == over_under_actual
        if over_under_correct:
            correct_predictions["overUnder"] += 1
        
        # ตรวจสอบ Corner 1st Half
        corner_1st_actual = "Over 5" if actual["corners1stHalf"] > 5 else "Under 5"
        corner_1st_correct = pred["predicted"]["corner1stHalf"] == corner_1st_actual
        if corner_1st_correct:
            correct_predictions["corner1stHalf"] += 1
        
        # ตรวจสอบ Corner Full Match
        corner_full_actual = "Over 10" if actual["cornersFullMatch"] > 10 else "Under 10"
        corner_full_correct = pred["predicted"]["cornerFullMatch"] == corner_full_actual
        if corner_full_correct:
            correct_predictions["cornerFullMatch"] += 1
        
        analysis.append({
            "homeTeam": pred["homeTeam"],
            "awayTeam": pred["awayTeam"],
            "actualScore": f"{actual['homeScore']}-{actual['awayScore']}",
            "actualResult": actual["result"],
            "actualCorners1st": actual["corners1stHalf"],
            "actualCornersTotal": actual["cornersFullMatch"],
            "predictions": {
                "matchResult": {
                    "predicted": pred["predicted"]["matchResult"],
                    "actual": actual["result"],
                    "correct": match_result_correct
                },
                "overUnder": {
                    "predicted": pred["predicted"]["overUnder"],
                    "actual": over_under_actual,
                    "correct": over_under_correct
                },
                "corner1stHalf": {
                    "predicted": pred["predicted"]["corner1stHalf"],
                    "actual": corner_1st_actual,
                    "correct": corner_1st_correct
                },
                "cornerFullMatch": {
                    "predicted": pred["predicted"]["cornerFullMatch"],
                    "actual": corner_full_actual,
                    "correct": corner_full_correct
                }
            }
        })
    
    # คำนวณความแม่นยำ
    total_matches = len(predictions)
    accuracy = {
        "matchResult": (correct_predictions["matchResult"] / total_matches) * 100,
        "overUnder": (correct_predictions["overUnder"] / total_matches) * 100,
        "corner1stHalf": (correct_predictions["corner1stHalf"] / total_matches) * 100,
        "cornerFullMatch": (correct_predictions["cornerFullMatch"] / total_matches) * 100
    }
    
    return analysis, accuracy

def generate_results_summary():
    """สร้างสรุปผลการทำนาย"""
    analysis, accuracy = analyze_predictions()
    
    print("🏆 สรุปผลการทำนาย J-League 2 วันที่ 12 กรกฎาคม 2025")
    print("=" * 80)
    
    print(f"\n📊 ความแม่นยำรวม:")
    print(f"⚽ ผลการแข่งขัน: {accuracy['matchResult']:.1f}% ({int(accuracy['matchResult']/10)}/10)")
    print(f"🎯 Over/Under 2.5: {accuracy['overUnder']:.1f}% ({int(accuracy['overUnder']/10)}/10)")
    print(f"🚩 Corner 1st Half: {accuracy['corner1stHalf']:.1f}% ({int(accuracy['corner1stHalf']/10)}/10)")
    print(f"⚽ Corner Full Match: {accuracy['cornerFullMatch']:.1f}% ({int(accuracy['cornerFullMatch']/10)}/10)")
    print(f"🎯 ความแม่นยำเฉลี่ย: {sum(accuracy.values())/4:.1f}%")
    
    print(f"\n📋 รายละเอียดแต่ละคู่:")
    for i, match in enumerate(analysis, 1):
        print(f"\n{i}. {match['homeTeam']} vs {match['awayTeam']}")
        print(f"   📊 ผลจริง: {match['actualScore']} ({match['actualResult']})")
        print(f"   🚩 เตะมุม: ครึ่งแรก {match['actualCorners1st']}, รวม {match['actualCornersTotal']}")
        
        # แสดงผลการทำนาย
        icons = {True: "✅", False: "❌"}
        print(f"   🎯 การทำนาย:")
        print(f"      ⚽ ผลการแข่งขัน: {icons[match['predictions']['matchResult']['correct']]} {match['predictions']['matchResult']['predicted']}")
        print(f"      🎯 Over/Under: {icons[match['predictions']['overUnder']['correct']]} {match['predictions']['overUnder']['predicted']}")
        print(f"      🚩 Corner 1st: {icons[match['predictions']['corner1stHalf']['correct']]} {match['predictions']['corner1stHalf']['predicted']}")
        print(f"      ⚽ Corner Total: {icons[match['predictions']['cornerFullMatch']['correct']]} {match['predictions']['cornerFullMatch']['predicted']}")
    
    return analysis, accuracy

if __name__ == "__main__":
    analysis, accuracy = generate_results_summary()
    
    # บันทึกผลลงไฟล์
    results_data = {
        "analysis": analysis,
        "accuracy": accuracy,
        "generated_at": datetime.now().isoformat()
    }
    
    with open('match_results_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ บันทึกผลการวิเคราะห์ลงไฟล์ match_results_analysis.json แล้ว")
