#!/usr/bin/env python3
"""
🚀 Update Value Bets with Correct Team Data - July 18, 2025
แก้ไขข้อมูล Value Bets ให้สอดคล้องกับทีมที่แข่งขันจริง
"""

import os
import json
from datetime import datetime
from bs4 import BeautifulSoup

def update_value_bets_correct():
    """Update Value Bets with Correct Team Data"""
    print("🚀 Updating Value Bets with Correct Team Data...")
    
    # Paths
    project_dir = "/Users/80090/Desktop/Project/untitle"
    index_file = os.path.join(project_dir, "index.html")
    
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
    
    # Find China Super League section
    china_section = None
    cards = soup.find_all("div", class_="card")
    
    for card in cards:
        header = card.find("div", class_="card-header")
        if header and "China Super League" in header.text:
            china_section = card
            break
    
    if not china_section:
        print("❌ Could not find China Super League section in index.html")
    else:
        print(f"✅ Found China Super League section")
        
        # Update China Super League Value Bets
        value_bets_table = None
        for table in china_section.find_all("table", class_="table"):
            if "Value Bets" in str(table.previous_element):
                value_bets_table = table
                break
        
        if value_bets_table:
            tbody = value_bets_table.find("tbody")
            if tbody:
                tbody.clear()
                
                # Add correct value bets for China Super League
                tr1 = soup.new_tag("tr")
                
                td1_1 = soup.new_tag("td")
                td1_1.string = "Changchun Yatai vs Shanghai SIPG"
                tr1.append(td1_1)
                
                td1_2 = soup.new_tag("td")
                td1_2.string = "Away Win @ 3.0"
                tr1.append(td1_2)
                
                td1_3 = soup.new_tag("td", attrs={"class": "text-success"})
                td1_3.string = "34.7%"
                tr1.append(td1_3)
                
                td1_4 = soup.new_tag("td")
                td1_4.string = "44.9%"
                tr1.append(td1_4)
                
                tbody.append(tr1)
                
                tr2 = soup.new_tag("tr")
                
                td2_1 = soup.new_tag("td")
                td2_1.string = "Hangzhou Greentown vs Yunnan Yukun"
                tr2.append(td2_1)
                
                td2_2 = soup.new_tag("td")
                td2_2.string = "Home Win @ 2.2"
                tr2.append(td2_2)
                
                td2_3 = soup.new_tag("td", attrs={"class": "text-success"})
                td2_3.string = "18.7%"
                tr2.append(td2_3)
                
                td2_4 = soup.new_tag("td")
                td2_4.string = "54.0%"
                tr2.append(td2_4)
                
                tbody.append(tr2)
                
                tr3 = soup.new_tag("tr")
                
                td3_1 = soup.new_tag("td")
                td3_1.string = "Wuhan Three Towns vs Qingdao Youth Island"
                tr3.append(td3_1)
                
                td3_2 = soup.new_tag("td")
                td3_2.string = "Home Win @ 2.2"
                tr3.append(td3_2)
                
                td3_3 = soup.new_tag("td", attrs={"class": "text-success"})
                td3_3.string = "10.0%"
                tr3.append(td3_3)
                
                td3_4 = soup.new_tag("td")
                td3_4.string = "55.0%"
                tr3.append(td3_4)
                
                tbody.append(tr3)
    
    # Find Korea K League section
    korea_section = None
    
    for card in cards:
        header = card.find("div", class_="card-header")
        if header and "Korea K League" in header.text:
            korea_section = card
            break
    
    if not korea_section:
        print("❌ Could not find Korea K League section in index.html")
    else:
        print(f"✅ Found Korea K League section")
        
        # Update Korea K League Value Bets
        value_bets_table = None
        for table in korea_section.find_all("table", class_="table"):
            if "Value Bets" in str(table.previous_element):
                value_bets_table = table
                break
        
        if value_bets_table:
            tbody = value_bets_table.find("tbody")
            if tbody:
                tbody.clear()
                
                # Add correct value bets for Korea K League
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
                td1_4.string = "28.5%"
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
        
        print("✅ Successfully updated Value Bets with Correct Team Data")
        return True
    except Exception as e:
        print(f"❌ Error saving index.html: {str(e)}")
        return False

if __name__ == "__main__":
    update_value_bets_correct()
