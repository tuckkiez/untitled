#!/usr/bin/env python3
"""
🚀 Improve Colors in Index HTML - July 17-18, 2025
ปรับปรุงสีในไฟล์ index.html ให้อ่านง่ายขึ้น โดยเฉพาะส่วนที่ไม่ได้ highlight
"""

import os
from datetime import datetime
import re

def improve_colors():
    """ปรับปรุงสีในไฟล์ index.html ให้อ่านง่ายขึ้น"""
    print("🚀 Improve Colors in Index HTML - July 17-18, 2025")
    print("=" * 60)
    
    try:
        # โหลดไฟล์ index.html
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # ปรับปรุงสีใน CSS
        css_updates = """
        :root {
            --primary-color: #121212;
            --secondary-color: #1e1e1e;
            --accent-color: #bb86fc;
            --text-color: #ffffff;
            --text-muted: #cccccc;
            --success-color: #00e676;
            --warning-color: #ffab00;
            --danger-color: #ff5252;
            --info-color: #40c4ff;
            --neutral-color: #e0e0e0;
        }
        
        body {
            padding: 0;
            margin: 0;
            background-color: var(--primary-color);
            color: var(--text-color);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .text-success {
            color: var(--success-color) !important;
        }
        
        .text-warning {
            color: var(--warning-color) !important;
        }
        
        .text-danger {
            color: var(--danger-color) !important;
        }
        
        .text-primary {
            color: var(--info-color) !important;
        }
        
        .text-muted {
            color: var(--text-muted) !important;
        }
        
        .table {
            color: var(--text-color);
            border-collapse: separate;
            border-spacing: 0;
        }
        
        .table-dark {
            background-color: var(--secondary-color);
            color: var(--text-color);
        }
        
        .table-striped > tbody > tr:nth-of-type(odd) {
            background-color: rgba(255, 255, 255, 0.05);
        }
        
        .table-hover > tbody > tr:hover {
            background-color: rgba(187, 134, 252, 0.1);
        }
        
        .table-success {
            background-color: rgba(0, 230, 118, 0.15) !important;
        }
        
        /* ปรับปรุงสีสำหรับข้อความที่ไม่ได้ highlight */
        .table td {
            color: var(--neutral-color);
        }
        """
        
        # แทนที่ CSS เดิม
        css_pattern = r':root\s*{[^}]*}.*?\.table-success\s*{[^}]*}'
        html_content = re.sub(css_pattern, css_updates, html_content, flags=re.DOTALL)
        
        # บันทึกไฟล์ index.html ที่ปรับปรุงแล้ว
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'index_backup_{timestamp}.html'
        with open(backup_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 ปรับปรุงสีในไฟล์ index.html เรียบร้อยแล้ว (สำรองไว้ที่ {backup_filename})")
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    improve_colors()
