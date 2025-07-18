#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Fix Inconsistencies in Index HTML
แก้ไขความขัดแย้งของข้อมูลในหน้า index.html
"""

import os
import re
from bs4 import BeautifulSoup

def load_index_html():
    """Load current index.html"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup
    except:
        print("Error: Could not load index.html")
        return None

def fix_inconsistencies(soup):
    """Fix inconsistencies in predictions"""
    if not soup:
        return None
    
    # Find all table rows
    rows = soup.select('table.table tbody tr')
    
    for row in rows:
        # Get all cells in the row
        cells = row.select('td')
        
        if len(cells) < 7:  # Make sure we have enough cells
            continue
        
        # Extract data from cells
        match_result_cell = cells[2]
        over_under_cell = cells[3]
        btts_cell = cells[4]
        corners_cell = cells[5]
        exact_score_cell = cells[6]
        
        # Extract text from cells
        match_result_text = match_result_cell.get_text().strip()
        over_under_text = over_under_cell.get_text().strip()
        btts_text = btts_cell.get_text().strip()
        corners_text = corners_cell.get_text().strip()
        exact_score_text = exact_score_cell.get_text().strip()
        
        # Fix BTTS and Exact Score inconsistency
        if "YES" in btts_text:
            # Extract exact score
            exact_score_match = re.search(r'(\d+)-(\d+)', exact_score_text)
            if exact_score_match:
                home_goals = int(exact_score_match.group(1))
                away_goals = int(exact_score_match.group(2))
                
                if home_goals == 0 or away_goals == 0:
                    # Inconsistency found - fix exact score
                    if home_goals == 0:
                        home_goals = 1
                    if away_goals == 0:
                        away_goals = 1
                    
                    # Extract confidence
                    confidence_match = re.search(r'\((\d+\.?\d*)%\)', exact_score_text)
                    confidence = confidence_match.group(1) if confidence_match else "50.0"
                    
                    # Update exact score cell
                    new_exact_score = f"{home_goals}-{away_goals} ({confidence}%)"
                    exact_score_cell.string = new_exact_score
        
        elif "NO" in btts_text:
            # Extract exact score
            exact_score_match = re.search(r'(\d+)-(\d+)', exact_score_text)
            if exact_score_match:
                home_goals = int(exact_score_match.group(1))
                away_goals = int(exact_score_match.group(2))
                
                if home_goals > 0 and away_goals > 0:
                    # Inconsistency found - fix exact score
                    if "Home Win" in match_result_text:
                        away_goals = 0
                    else:
                        home_goals = 0
                    
                    # Extract confidence
                    confidence_match = re.search(r'\((\d+\.?\d*)%\)', exact_score_text)
                    confidence = confidence_match.group(1) if confidence_match else "50.0"
                    
                    # Update exact score cell
                    new_exact_score = f"{home_goals}-{away_goals} ({confidence}%)"
                    exact_score_cell.string = new_exact_score
        
        # Fix Over/Under and Exact Score inconsistency
        if "OVER" in over_under_text:
            # Extract exact score
            exact_score_match = re.search(r'(\d+)-(\d+)', exact_score_text)
            if exact_score_match:
                home_goals = int(exact_score_match.group(1))
                away_goals = int(exact_score_match.group(2))
                total_goals = home_goals + away_goals
                
                if total_goals <= 2:
                    # Inconsistency found - fix exact score
                    # Extract confidence
                    confidence_match = re.search(r'\((\d+\.?\d*)%\)', exact_score_text)
                    confidence = confidence_match.group(1) if confidence_match else "50.0"
                    
                    # Update exact score cell
                    new_exact_score = f"{home_goals+1}-{away_goals} ({confidence}%)"
                    exact_score_cell.string = new_exact_score
        
        elif "UNDER" in over_under_text:
            # Extract exact score
            exact_score_match = re.search(r'(\d+)-(\d+)', exact_score_text)
            if exact_score_match:
                home_goals = int(exact_score_match.group(1))
                away_goals = int(exact_score_match.group(2))
                total_goals = home_goals + away_goals
                
                if total_goals >= 3:
                    # Inconsistency found - fix exact score
                    # Extract confidence
                    confidence_match = re.search(r'\((\d+\.?\d*)%\)', exact_score_text)
                    confidence = confidence_match.group(1) if confidence_match else "50.0"
                    
                    # Update exact score cell
                    if "Home Win" in match_result_text:
                        new_exact_score = f"2-0 ({confidence}%)"
                    else:
                        new_exact_score = f"0-2 ({confidence}%)"
                    exact_score_cell.string = new_exact_score
        
        # Fix corners prediction to always show the higher probability option
        corners_confidence_match = re.search(r'\((\d+\.?\d*)%\)', corners_text)
        if corners_confidence_match:
            corners_confidence = float(corners_confidence_match.group(1))
            
            if "UNDER" in corners_text and corners_confidence < 50:
                # If UNDER has less than 50% confidence, it should be OVER
                over_confidence = 100 - corners_confidence
                new_corners_text = corners_text.replace("UNDER", "OVER").replace(
                    f"({corners_confidence}%)", f"({over_confidence:.1f}%)")
                corners_cell.string = new_corners_text
    
    return soup

def save_updated_index(soup, filename="index.html"):
    """Save updated index.html"""
    if not soup:
        return False
    
    # Create a backup of the original file
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open('index.html.bak2', 'w', encoding='utf-8') as f:
            f.write(original_content)
    except:
        print("Warning: Could not create backup of index.html")
    
    # Save the updated file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"Updated index.html saved successfully")
        return True
    except Exception as e:
        print(f"Error saving updated index.html: {str(e)}")
        return False

def main():
    # Load current index.html
    index_soup = load_index_html()
    
    if not index_soup:
        print("Could not load index.html. Please make sure it exists.")
        return
    
    # Fix inconsistencies
    updated_soup = fix_inconsistencies(index_soup)
    
    if not updated_soup:
        print("Failed to fix inconsistencies in index.html.")
        return
    
    # Save updated index.html
    success = save_updated_index(updated_soup)
    
    if success:
        print("Successfully fixed inconsistencies in index.html.")
    else:
        print("Failed to save updated index.html.")

if __name__ == "__main__":
    main()
