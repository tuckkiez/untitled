#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Clean Index HTML
ลบส่วน League Statistics และ Value Bets จากหน้า index.html โดยตรง
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

def clean_index_html(soup):
    """Remove League Statistics and Value Bets sections"""
    if not soup:
        return None
    
    # Find all card bodies
    card_bodies = soup.select('div.card-body')
    
    for card_body in card_bodies:
        # Find and remove row sections that contain League Statistics and Value Bets
        rows = card_body.select('div.row.mb-4')
        for row in rows:
            row.extract()
    
    # Fix any inconsistencies in corners predictions
    for td in soup.select('td'):
        text = td.get_text().strip()
        if "UNDER" in text and "%" in text:
            # Extract the confidence value
            confidence_text = text.split('(')[1].split('%')[0] if '(' in text else "0"
            try:
                confidence = float(confidence_text)
                if confidence < 50:
                    # Replace UNDER with OVER and update confidence
                    new_text = text.replace("UNDER", "OVER").replace(
                        f"({confidence}%)", f"({100-confidence}%)")
                    td.string = new_text
            except ValueError:
                pass
    
    return soup

def save_updated_index(soup, filename="index.html"):
    """Save updated index.html"""
    if not soup:
        return False
    
    # Create a backup of the original file
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open('index.html.bak', 'w', encoding='utf-8') as f:
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
    
    # Clean index.html
    updated_soup = clean_index_html(index_soup)
    
    if not updated_soup:
        print("Failed to clean index.html.")
        return
    
    # Save updated index.html
    success = save_updated_index(updated_soup)
    
    if success:
        print("Successfully cleaned index.html.")
    else:
        print("Failed to save updated index.html.")

if __name__ == "__main__":
    main()
