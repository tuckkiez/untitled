#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 Remove Duplicate Leagues from Index HTML (Fixed)
ลบลีกที่ซ้ำกันในหน้า index.html (แก้ไขแล้ว)
"""

import os
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

def remove_duplicate_leagues(soup):
    """Remove duplicate leagues"""
    if not soup:
        return None
    
    # Define league mappings (equivalent leagues)
    league_mappings = {
        "Norway - Tippeligaen": "Norway - Eliteserien",
        "Iceland - Premier League": "Iceland - Úrvalsdeild",
        "Denmark - Division 1": "Denmark - 1. Division",
        "Finland - Ykkonen": "Finland - Ykkönen"
    }
    
    # Find all league sections (cards)
    league_cards = soup.select('div.card.mb-4')
    
    # Keep track of leagues we've seen
    seen_leagues = {}
    
    # Check each league section
    for card in league_cards:
        header = card.select_one('div.card-header h2')
        if header:
            header_text = header.text.strip()
            
            # Extract league name (remove date)
            league_name = header_text.split(" - July")[0] if " - July" in header_text else header_text
            
            # Check if this league has an equivalent name
            normalized_league_name = league_mappings.get(league_name, league_name)
            
            # Check if we've seen this league before
            if normalized_league_name in seen_leagues:
                # Remove this duplicate
                print(f"Removing duplicate: {league_name}")
                card.extract()
            else:
                # Mark this league as seen
                seen_leagues[normalized_league_name] = True
                print(f"Keeping: {league_name}")
    
    return soup

def save_updated_index(soup, filename="index.html"):
    """Save updated index.html"""
    if not soup:
        return False
    
    # Create a backup of the original file
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open('index.html.bak_duplicates', 'w', encoding='utf-8') as f:
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
    
    # Remove duplicate leagues
    updated_soup = remove_duplicate_leagues(index_soup)
    
    if not updated_soup:
        print("Failed to remove duplicate leagues from index.html.")
        return
    
    # Save updated index.html
    success = save_updated_index(updated_soup)
    
    if success:
        print("Successfully removed duplicate leagues from index.html.")
    else:
        print("Failed to save updated index.html.")

if __name__ == "__main__":
    main()
