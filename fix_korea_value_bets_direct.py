#!/usr/bin/env python3
"""
🚀 Fix Korea K League 1 Value Bets Direct - July 18, 2025
แก้ไขข้อมูล Value Bets ของ K League 1 ให้ตรงกับทีมที่แข่งขันจริงโดยตรง
"""

import os
import re
from datetime import datetime

def fix_korea_value_bets_direct():
    """Fix Korea K League 1 Value Bets Direct"""
    print("🚀 Fixing Korea K League 1 Value Bets Direct...")
    
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
    
    # Find the Korea K League Value Bets table
    korea_value_bets_pattern = r'<div class="card-body">\s*<h5 class="card-title">Value Bets Detected</h5>\s*<div class="table-responsive">\s*<table class="table table-sm">\s*<thead>\s*<tr>\s*<th>Match</th>\s*<th>Bet</th>\s*<th>Edge</th>\s*<th>Confidence</th>\s*</tr>\s*</thead>\s*<tbody>\s*<tr>\s*<td>Gangwon FC vs Pohang Steelers</td>'
    
    # New Value Bets HTML
    new_value_bets_html = '''<div class="card-body">
<h5 class="card-title">Value Bets Detected</h5>
<div class="table-responsive">
<table class="table table-sm">
<thead>
<tr>
<th>Match</th>
<th>Bet</th>
<th>Edge</th>
<th>Confidence</th>
</tr>
</thead>
<tbody>
<tr>
<td>Daegu FC vs Gimcheon Sangmu FC</td>
<td>BTTS NO @ 1.75</td>
<td class="text-success">19.0%</td>
<td>71.8%</td>
</tr>
<tr>
<td>Suwon FC vs Gwangju FC</td>
<td>Away Win @ 2.30</td>
<td class="text-success">15.0%</td>
<td>70.5%</td>
</tr>
</tbody>
</table>
</div>
</div>'''
    
    # Replace the old Value Bets table with the new one
    updated_html = re.sub(korea_value_bets_pattern, new_value_bets_html, html_content, flags=re.DOTALL)
    
    # Update last updated time
    updated_html = re.sub(r'<p>Last updated: .*?</p>', f'<p>Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>', updated_html)
    
    # Save updated index.html
    try:
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(updated_html)
        
        print("✅ Successfully fixed Korea K League 1 Value Bets Direct")
        return True
    except Exception as e:
        print(f"❌ Error saving index.html: {str(e)}")
        return False

if __name__ == "__main__":
    fix_korea_value_bets_direct()
