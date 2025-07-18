#!/usr/bin/env python3
"""
🚀 Fix Value Bets and Highlighting in index.html - July 18, 2025
แก้ไขข้อมูล Value Bets และการไฮไลท์ให้ถูกต้อง
"""

import os
import json
from datetime import datetime
from bs4 import BeautifulSoup

def fix_value_bets_highlight():
    """Fix Value Bets and Highlighting in index.html"""
    print("🚀 Fixing Value Bets and Highlighting in index.html...")
    
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
                
                # Add only high confidence value bets (70%+ confidence)
                tr1 = soup.new_tag("tr")
                
                td1_1 = soup.new_tag("td")
                td1_1.string = "Changchun Yatai vs Shanghai SIPG"
                tr1.append(td1_1)
                
                td1_2 = soup.new_tag("td")
                td1_2.string = "Corners OVER 10.0 @ 2.0"
                tr1.append(td1_2)
                
                td1_3 = soup.new_tag("td", attrs={"class": "text-success"})
                td1_3.string = "26.0%"
                tr1.append(td1_3)
                
                td1_4 = soup.new_tag("td")
                td1_4.string = "76.0%"
                tr1.append(td1_4)
                
                tbody.append(tr1)
                
                tr2 = soup.new_tag("tr")
                
                td2_1 = soup.new_tag("td")
                td2_1.string = "Zhejiang vs Yunnan Yukun"
                tr2.append(td2_1)
                
                td2_2 = soup.new_tag("td")
                td2_2.string = "Home Win @ 1.85"
                tr2.append(td2_2)
                
                td2_3 = soup.new_tag("td", attrs={"class": "text-success"})
                td2_3.string = "29.8%"
                tr2.append(td2_3)
                
                td2_4 = soup.new_tag("td")
                td2_4.string = "72.5%"
                tr2.append(td2_4)
                
                tbody.append(tr2)
        
        # Update China Super League main table
        main_table = None
        tables = china_section.find_all("table", class_="table")
        if len(tables) >= 2:
            main_table = tables[-1]  # Last table should be the main table
        
        if main_table:
            rows = main_table.find("tbody").find_all("tr")
            
            # Fix highlighting in main table
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 7:
                    # Remove high-confidence-row class from all rows
                    if "high-confidence-row" in row.get("class", []):
                        row["class"].remove("high-confidence-row")
                    
                    # Remove text-success fw-bold class from cells with low confidence
                    for cell in cells:
                        if "text-success" in cell.get("class", []) and "fw-bold" in cell.get("class", []):
                            confidence_text = cell.text
                            confidence_value = 0
                            try:
                                confidence_value = float(confidence_text.split("(")[1].split("%")[0])
                            except:
                                pass
                            
                            if confidence_value < 70:
                                if "text-success" in cell.get("class", []):
                                    cell["class"].remove("text-success")
                                if "fw-bold" in cell.get("class", []):
                                    cell["class"].remove("fw-bold")
                    
                    # Add high-confidence-row class to rows with high confidence predictions
                    for cell in cells:
                        if cell.text and "(" in cell.text and ")" in cell.text:
                            try:
                                confidence_text = cell.text
                                confidence_value = float(confidence_text.split("(")[1].split("%")[0])
                                if confidence_value >= 70:
                                    if "high-confidence-row" not in row.get("class", []):
                                        if row.get("class") is None:
                                            row["class"] = ["high-confidence-row"]
                                        else:
                                            row["class"].append("high-confidence-row")
                                    
                                    # Add text-success fw-bold to high confidence cells
                                    if "text-success" not in cell.get("class", []):
                                        if cell.get("class") is None:
                                            cell["class"] = ["text-success", "fw-bold"]
                                        else:
                                            cell["class"].extend(["text-success", "fw-bold"])
                            except:
                                pass
    
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
                
                # Add only high confidence value bets (70%+ confidence)
                tr1 = soup.new_tag("tr")
                
                td1_1 = soup.new_tag("td")
                td1_1.string = "Daegu FC vs Gimcheon Sangmu FC"
                tr1.append(td1_1)
                
                td1_2 = soup.new_tag("td")
                td1_2.string = "BTTS NO @ 1.75"
                tr1.append(td1_2)
                
                td1_3 = soup.new_tag("td", attrs={"class": "text-success"})
                td1_3.string = "19.0%"
                tr1.append(td1_3)
                
                td1_4 = soup.new_tag("td")
                td1_4.string = "71.8%"
                tr1.append(td1_4)
                
                tbody.append(tr1)
        
        # Update Korea K League main table
        main_table = None
        tables = korea_section.find_all("table", class_="table")
        if len(tables) >= 2:
            main_table = tables[-1]  # Last table should be the main table
        
        if main_table:
            rows = main_table.find("tbody").find_all("tr")
            
            # Fix highlighting in main table
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 7:
                    # Remove high-confidence-row class from all rows
                    if "high-confidence-row" in row.get("class", []):
                        row["class"].remove("high-confidence-row")
                    
                    # Remove text-success fw-bold class from cells with low confidence
                    for cell in cells:
                        if "text-success" in cell.get("class", []) and "fw-bold" in cell.get("class", []):
                            confidence_text = cell.text
                            confidence_value = 0
                            try:
                                confidence_value = float(confidence_text.split("(")[1].split("%")[0])
                            except:
                                pass
                            
                            if confidence_value < 70:
                                if "text-success" in cell.get("class", []):
                                    cell["class"].remove("text-success")
                                if "fw-bold" in cell.get("class", []):
                                    cell["class"].remove("fw-bold")
                    
                    # Add high-confidence-row class to rows with high confidence predictions
                    for cell in cells:
                        if cell.text and "(" in cell.text and ")" in cell.text:
                            try:
                                confidence_text = cell.text
                                confidence_value = float(confidence_text.split("(")[1].split("%")[0])
                                if confidence_value >= 70:
                                    if "high-confidence-row" not in row.get("class", []):
                                        if row.get("class") is None:
                                            row["class"] = ["high-confidence-row"]
                                        else:
                                            row["class"].append("high-confidence-row")
                                    
                                    # Add text-success fw-bold to high confidence cells
                                    if "text-success" not in cell.get("class", []):
                                        if cell.get("class") is None:
                                            cell["class"] = ["text-success", "fw-bold"]
                                        else:
                                            cell["class"].extend(["text-success", "fw-bold"])
                            except:
                                pass
    
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
        
        print("✅ Successfully fixed Value Bets and Highlighting in index.html")
        return True
    except Exception as e:
        print(f"❌ Error saving index.html: {str(e)}")
        return False

if __name__ == "__main__":
    fix_value_bets_highlight()
