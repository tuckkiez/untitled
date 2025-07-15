#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 CORNER STATISTICS UTILITY
Quick utility to fetch corner data for any team
"""

import requests
import json
import time

def get_team_corner_stats(team_name, num_matches=10):
    """
    ดึงสถิติเตะมุมของทีม
    
    Args:
        team_name (str): ชื่อทีม
        num_matches (int): จำนวนแมตช์ที่ต้องการดู
    
    Returns:
        list: รายการสถิติเตะมุม
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        # ค้นหาทีม
        search_url = "https://api.sofascore.com/api/v1/search/all"
        params = {'q': team_name}
        
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            teams = [r for r in data.get('results', []) if r.get('type') == 'team']
            
            if teams:
                team = teams[0]
                team_id = team.get('entity', {}).get('id')
                
                # ดึงข้อมูลการแข่งขัน
                time.sleep(1)
                matches_url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/last/0"
                matches_response = requests.get(matches_url, headers=headers, timeout=10)
                
                if matches_response.status_code == 200:
                    matches_data = matches_response.json()
                    events = matches_data.get('events', [])
                    
                    corner_stats = []
                    for event in events[:num_matches]:
                        event_id = event.get('id')
                        home_team = event.get('homeTeam', {}).get('name')
                        away_team = event.get('awayTeam', {}).get('name')
                        
                        # ดึงสถิติ
                        time.sleep(1)
                        stats_url = f"https://api.sofascore.com/api/v1/event/{event_id}/statistics"
                        stats_response = requests.get(stats_url, headers=headers, timeout=10)
                        
                        if stats_response.status_code == 200:
                            stats_data = stats_response.json()
                            
                            # หาข้อมูลเตะมุม
                            for period in stats_data.get('statistics', []):
                                for group in period.get('groups', []):
                                    for stat in group.get('statisticsItems', []):
                                        if 'corner' in stat.get('name', '').lower():
                                            corner_stats.append({
                                                'match': f"{home_team} vs {away_team}",
                                                'stat_name': stat['name'],
                                                'home_corners': stat.get('home'),
                                                'away_corners': stat.get('away')
                                            })
                    
                    return corner_stats
        
        return []
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

# Example usage:
if __name__ == "__main__":
    # ดึงข้อมูลเตะมุม Chelsea
    chelsea_corners = get_team_corner_stats("Chelsea", 5)
    
    if chelsea_corners:
        print("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Chelsea Corner Statistics:")
        for stat in chelsea_corners:
            print(f"   {stat['match']}: {stat['stat_name']} = {stat['home_corners']}-{stat['away_corners']}")
    else:
        print("❌ No corner data found")
