#!/usr/bin/env python3
"""
🚀 Update K League 1 Section in index.html - July 18, 2025
อัพเดทส่วนของ K League 1 ในหน้า index.html
"""

import os
import json
from datetime import datetime
from bs4 import BeautifulSoup

def update_k_league_section():
    """Update K League 1 section in index.html"""
    print("🚀 Updating K League 1 section in index.html...")
    
    # Paths
    project_dir = "/Users/80090/Desktop/Project/untitle"
    index_file = os.path.join(project_dir, "index.html")
    output_dir = os.path.join(project_dir, "output")
    
    # Load index.html
    try:
        with open(index_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        print("✅ Successfully loaded index.html")
    except Exception as e:
        print(f"❌ Error loading index.html: {str(e)}")
        return False
    
    # Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find K League section
    k_league_section = None
    cards = soup.find_all("div", class_="card")
    
    for card in cards:
        header = card.find("div", class_="card-header")
        if header and "Korea K League" in header.text:
            k_league_section = card
            break
    
    if not k_league_section and len(cards) >= 2:
        k_league_section = cards[1]  # Assuming it's the second card
    
    if not k_league_section:
        print("❌ Could not find K League section in index.html")
        return False
    
    print(f"✅ Found K League section: {k_league_section.find('h2').text if k_league_section.find('h2') else 'No title found'}")
    
    # Update K League section with correct data
    header = k_league_section.find("div", class_="card-header")
    if header:
        h2 = header.find("h2")
        if h2:
            h2.string = "🇰🇷 Korea K League 1 - July 18, 2025"
        
        p = header.find("p")
        if p:
            p.string = "Ultra Advanced ML Analysis with Corner Predictions at 10.0 Line"
    
    # Update alert
    alert = k_league_section.find("div", class_="alert")
    if alert:
        alert.clear()
        i_tag = soup.new_tag("i", attrs={"class": "fas fa-info-circle"})
        alert.append(i_tag)
        alert.append(" ")
        strong = soup.new_tag("strong")
        strong.string = "NEW:"
        alert.append(strong)
        alert.append(" Korea K League 1 analysis with Ultra Advanced ML and corner predictions at 10.0 line for 2 matches.")
    
    # Update league statistics
    stats_list = k_league_section.find("ul", class_="list-group")
    if stats_list:
        stats_items = stats_list.find_all("li", class_="list-group-item")
        if len(stats_items) >= 3:
            avg_goals_span = stats_items[0].find("span", class_="badge")
            if avg_goals_span:
                avg_goals_span.string = "2.50"
            
            home_win_span = stats_items[1].find("span", class_="badge")
            if home_win_span:
                home_win_span.string = "42.5%"
            
            avg_corners_span = stats_items[2].find("span", class_="badge")
            if avg_corners_span:
                avg_corners_span.string = "10.3"
    
    # Update value bets
    value_bets_table = None
    for table in k_league_section.find_all("table", class_="table"):
        if "Value Bets" in str(table.previous_element):
            value_bets_table = table
            break
    
    if value_bets_table:
        tbody = value_bets_table.find("tbody")
        if tbody:
            tbody.clear()
            
            # Add new value bets
            tr1 = soup.new_tag("tr")
            
            td1_1 = soup.new_tag("td")
            td1_1.string = "Daegu FC vs Gimcheon Sangmu FC"
            tr1.append(td1_1)
            
            td1_2 = soup.new_tag("td")
            td1_2.string = "Home Win @ 3.75"
            tr1.append(td1_2)
            
            td1_3 = soup.new_tag("td", attrs={"class": "text-success"})
            td1_3.string = "6.8%"
            tr1.append(td1_3)
            
            td1_4 = soup.new_tag("td")
            td1_4.string = "28.2%"
            tr1.append(td1_4)
            
            tbody.append(tr1)
            
            tr2 = soup.new_tag("tr")
            
            td2_1 = soup.new_tag("td")
            td2_1.string = "Suwon FC vs Gwangju FC"
            tr2.append(td2_1)
            
            td2_2 = soup.new_tag("td")
            td2_2.string = "Away Win @ 2.30"
            tr2.append(td2_2)
            
            td2_3 = soup.new_tag("td", attrs={"class": "text-success"})
            td2_3.string = "5.0%"
            tr2.append(td2_3)
            
            td2_4 = soup.new_tag("td")
            td2_4.string = "45.7%"
            tr2.append(td2_4)
            
            tbody.append(tr2)
    
    # Update main table
    main_table = None
    tables = k_league_section.find_all("table", class_="table")
    if len(tables) >= 2:
        main_table = tables[-1]  # Last table should be the main table
    
    if main_table:
        tbody = main_table.find("tbody")
        if tbody:
            tbody.clear()
            
            # Add new matches
            tr1 = soup.new_tag("tr", attrs={"class": "high-confidence-row"})
            
            td1_1 = soup.new_tag("td")
            td1_1.string = "17:30"
            tr1.append(td1_1)
            
            td1_2 = soup.new_tag("td")
            td1_2.string = "Daegu FC [12] vs Gimcheon Sangmu FC [3]"
            tr1.append(td1_2)
            
            td1_3 = soup.new_tag("td", attrs={"class": "text-success fw-bold"})
            td1_3.string = "Home Win (28.2%)"
            tr1.append(td1_3)
            
            td1_4 = soup.new_tag("td")
            td1_4.string = "UNDER (65%)"
            tr1.append(td1_4)
            
            td1_5 = soup.new_tag("td")
            td1_5.string = "NO (70%)"
            tr1.append(td1_5)
            
            td1_6 = soup.new_tag("td")
            td1_6.string = "UNDER 9.0 (55.0%)"
            tr1.append(td1_6)
            
            td1_7 = soup.new_tag("td", attrs={"class": "text-muted"})
            td1_7.string = "1-0 (28%)"
            tr1.append(td1_7)
            
            tbody.append(tr1)
            
            tr2 = soup.new_tag("tr")
            
            td2_1 = soup.new_tag("td")
            td2_1.string = "17:30"
            tr2.append(td2_1)
            
            td2_2 = soup.new_tag("td")
            td2_2.string = "Suwon FC [11] vs Gwangju FC [5]"
            tr2.append(td2_2)
            
            td2_3 = soup.new_tag("td")
            td2_3.string = "Away Win (45.7%)"
            tr2.append(td2_3)
            
            td2_4 = soup.new_tag("td")
            td2_4.string = "UNDER (65%)"
            tr2.append(td2_4)
            
            td2_5 = soup.new_tag("td")
            td2_5.string = "NO (70%)"
            tr2.append(td2_5)
            
            td2_6 = soup.new_tag("td")
            td2_6.string = "UNDER 8.5 (60.0%)"
            tr2.append(td2_6)
            
            td2_7 = soup.new_tag("td", attrs={"class": "text-muted"})
            td2_7.string = "0-1 (45%)"
            tr2.append(td2_7)
            
            tbody.append(tr2)
    
    # Update last updated time
    footer = soup.find("div", class_="footer")
    if footer:
        p_tags = footer.find_all("p")
        if p_tags and len(p_tags) > 0:
            p_tags[0].string = f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Save updated index.html
    try:
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(str(soup))
        
        print("✅ Successfully updated K League section in index.html")
        return True
    except Exception as e:
        print(f"❌ Error saving index.html: {str(e)}")
        return False

if __name__ == "__main__":
    update_k_league_section()
