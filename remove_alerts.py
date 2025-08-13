#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 Remove Alerts from Index HTML
ลบส่วน alert alert-info และ strong จากหน้า index.html
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

def remove_alerts(soup):
    """Remove alert alert-info and strong elements"""
    if not soup:
        return None
    
    # Find all alert elements
    alerts = soup.select('div.alert.alert-info')
    
    # Remove each alert
    for alert in alerts:
        alert.extract()
    
    return soup

def save_updated_index(soup, filename="index.html"):
    """Save updated index.html"""
    if not soup:
        return False
    
    # Create a backup of the original file
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open('index.html.bak_alerts', 'w', encoding='utf-8') as f:
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
    
    # Remove alerts
    updated_soup = remove_alerts(index_soup)
    
    if not updated_soup:
        print("Failed to remove alerts from index.html.")
        return
    
    # Save updated index.html
    success = save_updated_index(updated_soup)
    
    if success:
        print("Successfully removed alerts from index.html.")
    else:
        print("Failed to save updated index.html.")

if __name__ == "__main__":
    main()
