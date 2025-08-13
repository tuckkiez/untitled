#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 Remove Duplicate Leagues from Index HTML (Direct)
ลบลีกที่ซ้ำกันในหน้า index.html (โดยตรง)
"""

import os
from bs4 import BeautifulSoup

def load_index_html():
    """Load current index.html"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            return content
    except:
        print("Error: Could not load index.html")
        return None

def save_updated_index(content, filename="index.html"):
    """Save updated index.html"""
    if not content:
        return False
    
    # Create a backup of the original file
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open('index.html.bak_direct', 'w', encoding='utf-8') as f:
            f.write(original_content)
    except:
        print("Warning: Could not create backup of index.html")
    
    # Save the updated file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated index.html saved successfully")
        return True
    except Exception as e:
        print(f"Error saving updated index.html: {str(e)}")
        return False

def main():
    # Load current index.html
    content = load_index_html()
    
    if not content:
        print("Could not load index.html. Please make sure it exists.")
        return
    
    # Create a new BeautifulSoup object
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all league sections
    cards = soup.select('div.card.mb-4')
    
    # Define leagues to keep
    leagues_to_keep = [
        "China - Super League",
        "Japan - J1 League",
        "South-Korea - K League 1",
        "South-Korea - K League 2",
        "Norway - Eliteserien",
        "Sweden - Allsvenskan",
        "Poland - Ekstraklasa",
        "Iceland - Úrvalsdeild",
        "Sweden - Superettan",
        "Denmark - 1. Division",
        "Finland - Ykkönen"
    ]
    
    # Remove cards that don't match leagues to keep
    for card in cards:
        header = card.select_one('div.card-header h2')
        if header:
            header_text = header.text.strip()
            keep_card = False
            
            for league in leagues_to_keep:
                if league in header_text:
                    keep_card = True
                    break
            
            if not keep_card:
                print(f"Removing: {header_text}")
                card.extract()
            else:
                print(f"Keeping: {header_text}")
    
    # Save updated index.html
    success = save_updated_index(str(soup))
    
    if success:
        print("Successfully removed duplicate leagues from index.html.")
    else:
        print("Failed to save updated index.html.")

if __name__ == "__main__":
    main()
