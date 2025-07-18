#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Update Index with European Leagues Analysis (Fixed Version)
อัพเดทหน้า index.html ด้วยการวิเคราะห์ลีกยุโรป (เวอร์ชันที่แก้ไขแล้ว)
"""

import os
import json
import datetime
from bs4 import BeautifulSoup

def load_european_html():
    """Load European leagues HTML report"""
    try:
        with open('european_leagues_report.html', 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup
    except:
        print("Error: Could not load European leagues HTML report")
        return None

def load_index_html():
    """Load current index.html"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup
    except:
        print("Error: Could not load index.html")
        return None

def extract_league_sections(european_soup):
    """Extract league sections from European leagues HTML report"""
    if not european_soup:
        return []
    
    # Find all league sections (cards)
    league_cards = european_soup.select('div.card.mb-4')
    
    # Filter out the value bets section
    league_sections = []
    for card in league_cards:
        header = card.select_one('div.card-header h2')
        if header and not "High Confidence Value Bets" in header.text:
            # Remove League Statistics and Value Bets sections
            card_body = card.select_one('div.card-body')
            if card_body:
                # Keep only the alert and table
                alert = card_body.select_one('div.alert')
                table = card_body.select_one('table.table')
                
                # Clear the card body and add back only what we want
                for child in list(card_body.children):
                    child.extract()
                
                if alert:
                    card_body.append(alert)
                if table:
                    card_body.append(table)
            
            league_sections.append(card)
    
    return league_sections

def update_index_html(index_soup, league_sections):
    """Update index.html with European leagues analysis"""
    if not index_soup or not league_sections:
        return None
    
    # Find the container where we'll add our content
    container = index_soup.select_one('div.container.py-4')
    if not container:
        print("Error: Could not find container in index.html")
        return None
    
    # Find the footer
    footer = index_soup.select_one('div.footer')
    if not footer:
        print("Error: Could not find footer in index.html")
        return None
    
    # Remove any existing European league sections
    for card in container.select('div.card.mb-4'):
        header = card.select_one('div.card-header h2')
        if header:
            header_text = header.text.strip()
            for league_name in ["Norway", "Danish", "Ireland", "Finnish", "Russian", "Romania", "Poland", "Denmark", "Finland", "Iceland"]:
                if league_name in header_text and "China" not in header_text and "Korea" not in header_text:
                    card.extract()
    
    # Add each league section before the footer
    for section in league_sections:
        footer.insert_before(section)
    
    # Update the last updated time in the footer
    now = datetime.datetime.now()
    updated_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Find all p tags in the footer
    p_tags = footer.find_all('p')
    if p_tags:
        # Update the first p tag
        p_tags[0].string = f"Last updated: {updated_time}"
    
    return index_soup

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
    # Load European leagues HTML report
    european_soup = load_european_html()
    
    if not european_soup:
        print("No European leagues HTML report found. Please run generate_european_report_fixed.py first.")
        return
    
    # Extract league sections from European leagues HTML report
    league_sections = extract_league_sections(european_soup)
    
    if not league_sections:
        print("No league sections found in European leagues HTML report.")
        return
    
    print(f"Found {len(league_sections)} league sections to add to index.html")
    
    # Load current index.html
    index_soup = load_index_html()
    
    if not index_soup:
        print("Could not load index.html. Please make sure it exists.")
        return
    
    # Update index.html with European leagues analysis
    updated_soup = update_index_html(index_soup, league_sections)
    
    if not updated_soup:
        print("Failed to update index.html.")
        return
    
    # Save updated index.html
    success = save_updated_index(updated_soup)
    
    if success:
        print("Successfully updated index.html with European leagues analysis.")
    else:
        print("Failed to save updated index.html.")

if __name__ == "__main__":
    main()
