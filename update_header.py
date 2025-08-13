#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Update Header in Index HTML
แก้ไขหัวข้อในหน้า index.html เพื่อแสดงเฉพาะการแข่งขันวันที่ 19 กรกฎาคม 2025
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

def update_header(soup):
    """Update header to show only July 19, 2025"""
    if not soup:
        return None
    
    # Update title
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = "🏆 Asian & European Leagues Analysis - July 19, 2025"
    
    # Update header
    header_h1 = soup.select_one('div.header h1')
    if header_h1:
        header_h1.string = "🏆 July 19, 2025"
    
    # Remove any sections with July 18 in the header
    for card in soup.select('div.card.mb-4'):
        header = card.select_one('div.card-header h2')
        if header and "July 18" in header.text:
            card.extract()
    
    return soup

def save_updated_index(soup, filename="index.html"):
    """Save updated index.html"""
    if not soup:
        return False
    
    # Create a backup of the original file
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open('index.html.bak_header', 'w', encoding='utf-8') as f:
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
    
    # Update header
    updated_soup = update_header(index_soup)
    
    if not updated_soup:
        print("Failed to update header in index.html.")
        return
    
    # Save updated index.html
    success = save_updated_index(updated_soup)
    
    if success:
        print("Successfully updated header in index.html.")
    else:
        print("Failed to save updated index.html.")

if __name__ == "__main__":
    main()
