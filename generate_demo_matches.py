#!/usr/bin/env python3
"""
🎯 Demo Matches Generator
สร้างข้อมูลการแข่งขันตัวอย่างสำหรับแสดงผลในหน้า index
"""

import pandas as pd
from datetime import datetime, timedelta
import random
import json

def generate_demo_matches():
    """สร้างข้อมูลการแข่งขันตัวอย่าง"""
    
    # Demo leagues data
    leagues_data = [
        # Top Priority
        {"id": 1, "name": "FIFA Club World Cup 2025", "country": "USA", "flag": "🌍", "priority": 1},
        {"id": 71, "name": "Serie A", "country": "Brazil", "flag": "🇧🇷", "priority": 1},
        {"id": 128, "name": "Primera División", "country": "Argentina", "flag": "🇦🇷", "priority": 1},
        
        # High Priority
        {"id": 262, "name": "Liga MX", "country": "Mexico", "flag": "🇲🇽", "priority": 2},
        {"id": 239, "name": "Primera A", "country": "Colombia", "flag": "🇨🇴", "priority": 2},
        {"id": 103, "name": "Eliteserien", "country": "Norway", "flag": "🇳🇴", "priority": 2},
        {"id": 113, "name": "Allsvenskan", "country": "Sweden", "flag": "🇸🇪", "priority": 2},
        
        # Medium Priority
        {"id": 244, "name": "Veikkausliiga", "country": "Finland", "flag": "🇫🇮", "priority": 3},
        {"id": 283, "name": "Liga I", "country": "Romania", "flag": "🇷🇴", "priority": 3},
        {"id": 106, "name": "Ekstraklasa", "country": "Poland", "flag": "🇵🇱", "priority": 3},
        {"id": 294, "name": "K League 2", "country": "South Korea", "flag": "🇰🇷", "priority": 3},
        
        # Standard Priority
        {"id": 383, "name": "Ligat ha'Al", "country": "Israel", "flag": "🇮🇱", "priority": 4},
        {"id": 165, "name": "Úrvalsdeild", "country": "Iceland", "flag": "🇮🇸", "priority": 4},
        {"id": 1087, "name": "Ykkösliiga", "country": "Finland", "flag": "🇫🇮", "priority": 4},
    ]
    
    # Demo teams for each league
    teams_data = {
        1: [("Real Madrid", "Manchester City"), ("Bayern Munich", "Flamengo"), ("Al Hilal", "Chelsea")],
        71: [("Flamengo", "Palmeiras"), ("São Paulo", "Corinthians"), ("Atlético-MG", "Internacional")],
        128: [("River Plate", "Boca Juniors"), ("Racing", "Independiente"), ("San Lorenzo", "Estudiantes")],
        262: [("América", "Chivas"), ("Cruz Azul", "Pumas"), ("Tigres", "Monterrey")],
        239: [("Millonarios", "Nacional"), ("Junior", "Santa Fe"), ("Medellín", "Cali")],
        103: [("Molde", "Bodø/Glimt"), ("Rosenborg", "Brann"), ("Viking", "Lillestrøm")],
        113: [("Malmö FF", "AIK"), ("Hammarby", "Djurgården"), ("IFK Göteborg", "Elfsborg")],
        244: [("HJK Helsinki", "KuPS"), ("SJK", "Inter Turku"), ("Ilves", "VPS")],
        283: [("CFR Cluj", "FCSB"), ("Universitatea Craiova", "Rapid București"), ("Sepsi", "UTA Arad")],
        106: [("Legia Warsaw", "Lech Poznań"), ("Cracovia", "Wisła Kraków"), ("Jagiellonia", "Pogoń Szczecin")],
        294: [("Incheon United", "Asan Mugunghwa"), ("Bucheon FC", "Gimpo Citizen"), ("Ansan Greeners", "Seoul E-Land")],
        383: [("Maccabi Tel Aviv", "Hapoel Be'er Sheva"), ("Maccabi Haifa", "Hapoel Tel Aviv"), ("Beitar Jerusalem", "Bnei Sakhnin")],
        165: [("KR Reykjavik", "Valur"), ("FH Hafnarfjörður", "Breiðablik"), ("Víkingur Reykjavík", "Stjarnan")],
        1087: [("AC Oulu", "KTP"), ("HIFK", "PK-35 Vantaa"), ("Ekenas IF", "FC Jazz")]
    }
    
    # Generate matches
    matches = []
    base_time = datetime.now()
    
    for league in leagues_data:
        league_id = league["id"]
        if league_id not in teams_data:
            continue
            
        # Generate 2-4 matches per league
        num_matches = random.randint(2, 4)
        league_teams = teams_data[league_id]
        
        for i in range(min(num_matches, len(league_teams))):
            home_team, away_team = league_teams[i]
            
            # Random time within next 24 hours
            match_time = base_time + timedelta(
                hours=random.randint(0, 24),
                minutes=random.choice([0, 15, 30, 45])
            )
            
            # Random status
            status_options = [
                ("Not Started", "NS", "upcoming"),
                ("First Half", "1H", "live"),
                ("Half Time", "HT", "live"),
                ("Second Half", "2H", "live"),
                ("Match Finished", "FT", "finished")
            ]
            
            status_long, status_short, match_type = random.choice(status_options)
            
            # Generate score if finished or live
            if match_type in ["live", "finished"]:
                home_goals = random.randint(0, 4)
                away_goals = random.randint(0, 4)
                score = f"{home_goals}-{away_goals}"
            else:
                home_goals = None
                away_goals = None
                score = "vs"
            
            match = {
                'fixture_id': 1000000 + len(matches),
                'league_id': league_id,
                'league_name': league["name"],
                'league_country': league["country"],
                'league_flag': league["flag"],
                'priority': league["priority"],
                'home_team': home_team,
                'away_team': away_team,
                'status': status_long,
                'status_short': status_short,
                'venue': f"{home_team} Stadium",
                'city': f"{league['country']} City",
                'round': f"Round {random.randint(1, 30)}",
                'match_time_local': match_time.strftime('%m/%d %H:%M'),
                'match_date': match_time.strftime('%Y-%m-%d'),
                'is_today': match_time.date() == datetime.now().date(),
                'is_live': match_type == "live",
                'is_finished': match_type == "finished",
                'home_goals': home_goals,
                'away_goals': away_goals,
                'score': score
            }
            
            matches.append(match)
    
    return pd.DataFrame(matches)

def generate_demo_html(df: pd.DataFrame) -> str:
    """สร้าง HTML สำหรับข้อมูล demo"""
    if df.empty:
        return """
        <div class="no-matches">
            <h3>🔍 No Extended League Matches Found</h3>
            <p>ไม่พบการแข่งขันจากลีกเพิ่มเติมในช่วงเวลานี้</p>
        </div>
        """
    
    # Sort by priority and time
    df_sorted = df.sort_values(['priority', 'fixture_id'])
    
    html = f"""
    <div class="extended-matches-section">
        <div class="section-header">
            <h2>🌍 Extended League Matches (Demo Data)</h2>
            <div class="matches-stats">
                <span class="stat">📊 {len(df)} matches</span>
                <span class="stat">🏆 {df['league_name'].nunique()} leagues</span>
                <span class="stat">🌍 {df['league_country'].nunique()} countries</span>
            </div>
        </div>
        
        <div class="matches-container">
    """
    
    # Group by priority
    priority_groups = df_sorted.groupby('priority')
    
    for priority, group_df in priority_groups:
        priority_names = {
            1: "🔥 Top Priority",
            2: "⭐ High Priority",
            3: "✅ Medium Priority", 
            4: "📋 Standard Priority"
        }
        
        html += f"""
        <div class="priority-group priority-{priority}">
            <h3>{priority_names.get(priority, '📋 Other')}</h3>
            <div class="matches-grid">
        """
        
        # Group by league
        league_groups = group_df.groupby(['league_name', 'league_country', 'league_flag'])
        
        for (league_name, country, flag), league_df in league_groups:
            html += f"""
            <div class="league-block">
                <div class="league-title">
                    <span class="flag">{flag}</span>
                    <span class="name">{league_name}</span>
                    <span class="country">({country})</span>
                </div>
                <div class="league-matches">
            """
            
            for _, match in league_df.iterrows():
                # Status styling
                if match['is_live']:
                    status_class = 'live'
                    status_icon = '🔴'
                elif match['is_finished']:
                    status_class = 'finished'
                    status_icon = '✅'
                else:
                    status_class = 'upcoming'
                    status_icon = '⏰'
                
                html += f"""
                <div class="match-item {status_class}">
                    <div class="match-status">
                        <span class="icon">{status_icon}</span>
                        <span class="time">{match['match_time_local']}</span>
                    </div>
                    <div class="match-teams">
                        <span class="home">{match['home_team']}</span>
                        <span class="score">{match['score']}</span>
                        <span class="away">{match['away_team']}</span>
                    </div>
                    <div class="match-details">
                        <small>{match['round']}</small>
                    </div>
                </div>
                """
            
            html += """
                </div>
            </div>
            """
        
        html += """
            </div>
        </div>
        """
    
    html += """
        </div>
    </div>
    
    <style>
    .extended-matches-section {
        margin: 30px 0;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
    }
    
    .section-header {
        text-align: center;
        margin-bottom: 25px;
    }
    
    .section-header h2 {
        margin: 0 0 10px 0;
        font-size: 1.8em;
    }
    
    .matches-stats {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .stat {
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9em;
    }
    
    .priority-group {
        margin-bottom: 30px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
    }
    
    .priority-group h3 {
        margin: 0 0 15px 0;
        font-size: 1.2em;
    }
    
    .matches-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 15px;
    }
    
    .league-block {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 15px;
        color: #333;
    }
    
    .league-title {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
        font-weight: bold;
        border-bottom: 2px solid #eee;
        padding-bottom: 8px;
    }
    
    .flag {
        font-size: 1.2em;
    }
    
    .name {
        flex: 1;
    }
    
    .country {
        font-size: 0.85em;
        color: #666;
    }
    
    .league-matches {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .match-item {
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid #ddd;
    }
    
    .match-item.live {
        background: #fff3cd;
        border-left-color: #ffc107;
        animation: pulse 2s infinite;
    }
    
    .match-item.finished {
        background: #d4edda;
        border-left-color: #28a745;
    }
    
    .match-item.upcoming {
        background: #f8f9fa;
        border-left-color: #6c757d;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .match-status {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
        font-size: 0.85em;
        color: #666;
    }
    
    .match-teams {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .score {
        background: #e9ecef;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.9em;
    }
    
    .match-details {
        text-align: center;
        color: #666;
        font-size: 0.8em;
    }
    
    @media (max-width: 768px) {
        .matches-grid {
            grid-template-columns: 1fr;
        }
        
        .matches-stats {
            flex-direction: column;
            gap: 10px;
        }
    }
    </style>
    """
    
    return html

def update_index_with_demo():
    """อัปเดทหน้า index ด้วยข้อมูล demo"""
    # Generate demo data
    df = generate_demo_matches()
    
    # Save CSV
    csv_filename = f"demo_extended_matches_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f"📁 Demo CSV saved: {csv_filename}")
    
    # Generate HTML
    matches_html = generate_demo_html(df)
    
    # Update index.html
    index_path = "index.html"
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Replace extended matches section
        start_marker = '<!-- EXTENDED_MATCHES_SECTION -->'
        end_marker = '<!-- /EXTENDED_MATCHES_SECTION -->'
        
        start_idx = html_content.find(start_marker)
        end_idx = html_content.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            html_content = (
                html_content[:start_idx] +
                f'{start_marker}\n{matches_html}\n{end_marker}' +
                html_content[end_idx + len(end_marker):]
            )
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"🌐 Index page updated with demo data: {index_path}")
            
            # Show summary
            print(f"\n📊 Demo Data Summary:")
            print(f"  • Total Matches: {len(df)}")
            print(f"  • Leagues: {df['league_name'].nunique()}")
            print(f"  • Countries: {df['league_country'].nunique()}")
            
            print(f"\n📋 League Breakdown:")
            league_summary = df.groupby(['league_name', 'league_country']).size()
            for (league, country), count in league_summary.items():
                print(f"  • {league} ({country}): {count} matches")
            
            print(f"\n🎯 Status Breakdown:")
            status_summary = df.groupby('status').size()
            for status, count in status_summary.items():
                print(f"  • {status}: {count} matches")
                
        else:
            print("❌ Could not find extended matches section markers in index.html")
            
    except FileNotFoundError:
        print("❌ index.html not found")
    except Exception as e:
        print(f"❌ Error updating index.html: {e}")

def main():
    """Main function"""
    print("🎯 Generating Demo Extended League Matches...")
    update_index_with_demo()
    print("✅ Demo generation completed!")

if __name__ == "__main__":
    main()
