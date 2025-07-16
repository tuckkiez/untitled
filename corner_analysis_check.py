#!/usr/bin/env python3
"""
Corner Analysis Verification Script
Check consistency between expected corners and over/under probabilities
"""

import math

def calculate_corner_probability(expected_corners, threshold):
    """
    Calculate probability using Poisson distribution
    """
    # Using Poisson distribution for corner kicks
    lambda_val = expected_corners
    
    # P(X > threshold) = 1 - P(X <= threshold)
    prob_under = 0
    for k in range(int(threshold) + 1):
        prob_under += (math.exp(-lambda_val) * (lambda_val ** k)) / math.factorial(k)
    
    prob_over = 1 - prob_under
    return prob_over * 100

def analyze_corner_consistency():
    """Analyze corner predictions for all matches"""
    
    print("🚩 CORNER ANALYSIS VERIFICATION")
    print("=" * 50)
    
    matches = [
        {
            'name': 'FC Jazz vs KuPS Akatemia',
            'league': 'Finland Ykkonen',
            'expected_total': 11.9,
            'home_corners': 6.2,
            'away_corners': 5.7,
            'current_over_95': 64.7  # Current wrong value
        },
        {
            'name': 'Fredrikstad vs Bodo/Glimt', 
            'league': 'Norway Eliteserien',
            'expected_total': 12.7,
            'home_corners': 6.8,
            'away_corners': 5.9,
            'current_over_95': 68.2  # Need to check
        },
        {
            'name': 'JIPPO vs EIF',
            'league': 'Finland Ykkosliiga', 
            'expected_total': 10.4,
            'home_corners': 5.6,
            'away_corners': 4.8,
            'current_over_95': 58.3  # Need to check
        },
        {
            'name': 'Dinamo Minsk vs Ludogorets',
            'league': 'UEFA Champions League',
            'expected_total': 10.2,
            'home_corners': 4.8,
            'away_corners': 5.4,
            'current_over_95': 59.3  # Need to check
        },
        {
            'name': 'Linfield vs Shelbourne',
            'league': 'UEFA Champions League', 
            'expected_total': 8.5,
            'home_corners': 4.2,
            'away_corners': 4.3,
            'current_over_95': 45.2  # Need to check
        }
    ]
    
    for i, match in enumerate(matches, 1):
        print(f"\n🏟️  MATCH {i}: {match['name']}")
        print(f"🏆 League: {match['league']}")
        print("-" * 40)
        
        expected = match['expected_total']
        home = match['home_corners']
        away = match['away_corners']
        current_prob = match['current_over_95']
        
        # Calculate correct probability for Over 9.5
        correct_prob_95 = calculate_corner_probability(expected, 9.5)
        
        # Calculate other thresholds
        prob_85 = calculate_corner_probability(expected, 8.5)
        prob_105 = calculate_corner_probability(expected, 10.5)
        prob_115 = calculate_corner_probability(expected, 11.5)
        
        print(f"📊 Expected Total: {expected}")
        print(f"🏠 Home Corners: {home}")
        print(f"🚀 Away Corners: {away}")
        print(f"✅ Sum Check: {home + away:.1f} (should ≈ {expected})")
        
        print(f"\n🎯 PROBABILITY ANALYSIS:")
        print(f"Over 8.5: {prob_85:.1f}%")
        print(f"Over 9.5: {correct_prob_95:.1f}% (Current: {current_prob:.1f}%)")
        print(f"Over 10.5: {prob_105:.1f}%")
        print(f"Over 11.5: {prob_115:.1f}%")
        
        # Check consistency
        difference = abs(correct_prob_95 - current_prob)
        if difference > 5:
            print(f"⚠️  INCONSISTENCY DETECTED: {difference:.1f}% difference!")
            print(f"🔧 Should be: {correct_prob_95:.1f}%")
        else:
            print(f"✅ Consistent (±{difference:.1f}%)")
            
        # Recommend best threshold
        if expected >= 11:
            print(f"💡 Recommend: Over 10.5 ({prob_105:.1f}%)")
        elif expected >= 9:
            print(f"💡 Recommend: Over 9.5 ({correct_prob_95:.1f}%)")
        else:
            print(f"💡 Recommend: Over 8.5 ({prob_85:.1f}%)")
    
    print(f"\n" + "=" * 50)
    print("🔍 SUMMARY & CORRECTIONS NEEDED")
    print("=" * 50)
    
    corrections = []
    for match in matches:
        expected = match['expected_total']
        current = match['current_over_95']
        correct = calculate_corner_probability(expected, 9.5)
        
        if abs(correct - current) > 5:
            corrections.append({
                'match': match['name'],
                'current': current,
                'correct': correct,
                'expected': expected
            })
    
    if corrections:
        print("🚨 MATCHES NEEDING CORRECTION:")
        for corr in corrections:
            print(f"• {corr['match']}")
            print(f"  Expected: {corr['expected']} corners")
            print(f"  Current Over 9.5: {corr['current']:.1f}%")
            print(f"  Correct Over 9.5: {corr['correct']:.1f}%")
            print(f"  Difference: {abs(corr['correct'] - corr['current']):.1f}%")
            print()
    else:
        print("✅ All corner analyses are consistent!")
    
    return corrections

if __name__ == "__main__":
    corrections_needed = analyze_corner_consistency()
    
    if corrections_needed:
        print("🔧 ACTION REQUIRED: Update index.html with correct percentages")
    else:
        print("✅ NO ACTION NEEDED: All analyses are accurate")
