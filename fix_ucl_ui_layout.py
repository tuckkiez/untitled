#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 UEFA CHAMPIONS LEAGUE UI LAYOUT FIX
แก้ไข layout และ CSS ที่เละๆ ให้ดูดีขึ้น
"""

import os
import shutil
from datetime import datetime

class UCLUILayoutFixer:
    def __init__(self):
        self.analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def generate_fixed_css(self):
        """สร้าง CSS ที่แก้ไขแล้ว"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            min-height: 100vh;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header Styles */
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 15px;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
        }
        
        .header .subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 25px;
            color: #e0e0e0;
        }
        
        .stats-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 20px;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .stat-item {
            text-align: center;
            padding: 20px 15px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-item:hover {
            transform: translateY(-3px);
            background: rgba(255, 255, 255, 0.12);
        }
        
        .stat-number {
            font-size: 1.8rem;
            font-weight: bold;
            color: #FFD700;
            display: block;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.85rem;
            opacity: 0.8;
            color: #e0e0e0;
        }
        
        /* Matches Grid */
        .matches-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        
        .match-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .match-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #FFD700, #FFA500);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .match-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 215, 0, 0.3);
        }
        
        .match-card:hover::before {
            opacity: 1;
        }
        
        .high-confidence {
            border: 2px solid #FFD700;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.2);
        }
        
        .high-confidence::before {
            opacity: 1;
        }
        
        /* Match Header */
        .match-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.15);
        }
        
        .match-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #FFD700;
        }
        
        .match-time {
            background: linear-gradient(45deg, #FFD700, #FFA500);
            color: #1a1a2e;
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.9rem;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        }
        
        .venue-info {
            font-size: 0.9rem;
            opacity: 0.8;
            text-align: center;
            margin-bottom: 20px;
            color: #b0b0b0;
        }
        
        /* Teams Section */
        .teams-section {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 20px;
            align-items: center;
            margin-bottom: 25px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 15px;
        }
        
        .team {
            text-align: center;
        }
        
        .team-name {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: #ffffff;
        }
        
        .team-country {
            font-size: 0.85rem;
            opacity: 0.7;
            margin-bottom: 8px;
            color: #b0b0b0;
        }
        
        .team-strength {
            font-size: 1rem;
            color: #FFD700;
            font-weight: 600;
            background: rgba(255, 215, 0, 0.1);
            padding: 4px 12px;
            border-radius: 20px;
            display: inline-block;
        }
        
        .vs {
            font-size: 1.5rem;
            font-weight: bold;
            color: #FFD700;
            text-align: center;
            background: rgba(255, 215, 0, 0.1);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
        }
        
        /* Predictions Section */
        .predictions-section {
            margin-bottom: 25px;
        }
        
        .prediction-category {
            margin-bottom: 20px;
        }
        
        .category-title {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 12px;
            color: #FFD700;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .prediction-bars {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 8px;
            margin-bottom: 8px;
        }
        
        .prediction-bar {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            overflow: hidden;
            position: relative;
            height: 35px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .prediction-fill {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 0.85rem;
            transition: width 1s ease;
            position: relative;
            overflow: hidden;
        }
        
        .prediction-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .prediction-fill.home {
            background: linear-gradient(135deg, #4CAF50, #66BB6A);
        }
        
        .prediction-fill.draw {
            background: linear-gradient(135deg, #FF9800, #FFB74D);
        }
        
        .prediction-fill.away {
            background: linear-gradient(135deg, #f44336, #EF5350);
        }
        
        .prediction-fill.over {
            background: linear-gradient(135deg, #2196F3, #42A5F5);
        }
        
        .prediction-fill.under {
            background: linear-gradient(135deg, #9C27B0, #BA68C8);
        }
        
        .prediction-labels {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 8px;
            font-size: 0.75rem;
            margin-top: 5px;
            opacity: 0.8;
            text-align: center;
        }
        
        /* Betting Recommendations */
        .betting-recommendations {
            background: rgba(255, 215, 0, 0.05);
            border: 1px solid rgba(255, 215, 0, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .betting-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #FFD700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .bet-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding: 12px 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .bet-item:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(5px);
        }
        
        .bet-item:last-child {
            margin-bottom: 0;
        }
        
        .bet-rank {
            font-weight: 600;
            margin-right: 10px;
            font-size: 0.9rem;
        }
        
        .bet-confidence {
            background: linear-gradient(45deg, #4CAF50, #66BB6A);
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 60px;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .update-time {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 15px;
            color: #b0b0b0;
        }
        
        .ml-info {
            font-size: 1rem;
            margin-bottom: 20px;
            color: #e0e0e0;
        }
        
        .confidence-legend {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 25px;
            flex-wrap: wrap;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }
        
        .legend-high { 
            background: linear-gradient(45deg, #FFD700, #FFA500);
        }
        .legend-medium { 
            background: linear-gradient(45deg, #4CAF50, #66BB6A);
        }
        .legend-low { 
            background: linear-gradient(45deg, #FF9800, #FFB74D);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .matches-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .stats-bar {
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }
            
            .teams-section {
                grid-template-columns: 1fr;
                gap: 15px;
                text-align: center;
            }
            
            .vs {
                order: 2;
                margin: 10px auto;
            }
            
            .prediction-bars {
                grid-template-columns: 1fr;
                gap: 6px;
            }
            
            .prediction-labels {
                grid-template-columns: 1fr;
                gap: 6px;
            }
            
            .confidence-legend {
                flex-direction: column;
                gap: 15px;
                align-items: center;
            }
            
            .bet-item {
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }
        }
        
        @media (max-width: 480px) {
            .header {
                padding: 25px 15px;
            }
            
            .header h1 {
                font-size: 1.8rem;
            }
            
            .match-card {
                padding: 20px;
            }
            
            .stats-bar {
                grid-template-columns: 1fr;
            }
        }
        
        /* Loading Animation */
        .match-card {
            animation: fadeInUp 0.6s ease forwards;
            opacity: 0;
            transform: translateY(30px);
        }
        
        .match-card:nth-child(1) { animation-delay: 0.1s; }
        .match-card:nth-child(2) { animation-delay: 0.2s; }
        .match-card:nth-child(3) { animation-delay: 0.3s; }
        .match-card:nth-child(4) { animation-delay: 0.4s; }
        .match-card:nth-child(5) { animation-delay: 0.5s; }
        .match-card:nth-child(6) { animation-delay: 0.6s; }
        
        @keyframes fadeInUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(45deg, #FFD700, #FFA500);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(45deg, #FFA500, #FFD700);
        }
        """
    
    def fix_html_structure(self):
        """แก้ไขโครงสร้าง HTML"""
        
        # อ่านไฟล์ index.html ปัจจุบัน
        try:
            with open('/Users/80090/Desktop/Project/untitle/index.html', 'r', encoding='utf-8') as f:
                current_html = f.read()
        except FileNotFoundError:
            print("❌ index.html not found!")
            return False
        
        # สำรองไฟล์เก่า
        backup_name = f'/Users/80090/Desktop/Project/untitle/index_before_fix_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        with open(backup_name, 'w', encoding='utf-8') as f:
            f.write(current_html)
        print(f"✅ Backed up current index.html to: {backup_name}")
        
        # แทนที่ CSS ใหม่
        fixed_css = self.generate_fixed_css()
        
        # หา CSS section และแทนที่
        import re
        
        # Pattern เพื่อหา CSS ระหว่าง <style> tags
        css_pattern = r'<style>(.*?)</style>'
        
        if re.search(css_pattern, current_html, re.DOTALL):
            # แทนที่ CSS เก่าด้วย CSS ใหม่
            fixed_html = re.sub(css_pattern, f'<style>{fixed_css}</style>', current_html, flags=re.DOTALL)
        else:
            # ถ้าไม่เจอ CSS ให้เพิ่มใน head
            head_pattern = r'</head>'
            fixed_html = re.sub(head_pattern, f'<style>{fixed_css}</style>\n</head>', current_html)
        
        # แก้ไข class names ที่อาจจะผิด
        fixes = [
            # แก้ prediction-fill classes
            ('class="prediction-fill"', 'class="prediction-fill home"'),
            ('class="prediction-fill draw"', 'class="prediction-fill draw"'),
            ('class="prediction-fill away"', 'class="prediction-fill away"'),
            ('class="prediction-fill over"', 'class="prediction-fill over"'),
            ('class="prediction-fill under"', 'class="prediction-fill under"'),
        ]
        
        for old, new in fixes:
            if old in fixed_html and old != new:
                # แทนที่เฉพาะครั้งแรกเพื่อไม่ให้ซ้ำ
                fixed_html = fixed_html.replace(old, new, 1)
        
        # บันทึกไฟล์ที่แก้ไขแล้ว
        with open('/Users/80090/Desktop/Project/untitle/index.html', 'w', encoding='utf-8') as f:
            f.write(fixed_html)
        
        return True
    
    def add_javascript_enhancements(self):
        """เพิ่ม JavaScript เพื่อปรับปรุง UX"""
        
        js_code = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Animate prediction bars
            const predictionFills = document.querySelectorAll('.prediction-fill');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const fill = entry.target;
                        const width = fill.style.width;
                        fill.style.width = '0%';
                        setTimeout(() => {
                            fill.style.width = width;
                        }, 100);
                    }
                });
            }, { threshold: 0.5 });
            
            predictionFills.forEach(fill => {
                observer.observe(fill);
            });
            
            // Add click effects to bet items
            const betItems = document.querySelectorAll('.bet-item');
            betItems.forEach(item => {
                item.addEventListener('click', function() {
                    this.style.transform = 'scale(0.98)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 150);
                });
            });
            
            // Smooth scroll for better UX
            document.documentElement.style.scrollBehavior = 'smooth';
            
            // Add loading effect
            const matchCards = document.querySelectorAll('.match-card');
            matchCards.forEach((card, index) => {
                card.style.animationDelay = `${index * 0.1}s`;
            });
        });
        </script>
        """
        
        # อ่านไฟล์ปัจจุบัน
        with open('/Users/80090/Desktop/Project/untitle/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # เพิ่ม JavaScript ก่อน </body>
        if '</body>' in html_content:
            html_content = html_content.replace('</body>', f'{js_code}\n</body>')
        
        # บันทึกไฟล์
        with open('/Users/80090/Desktop/Project/untitle/index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True

def main():
    """Main execution"""
    fixer = UCLUILayoutFixer()
    
    print("🔧 Starting UEFA Champions League UI Layout Fix...")
    
    try:
        # แก้ไข HTML structure และ CSS
        if fixer.fix_html_structure():
            print("✅ HTML structure and CSS fixed!")
            
            # เพิ่ม JavaScript enhancements
            if fixer.add_javascript_enhancements():
                print("✅ JavaScript enhancements added!")
            
            print("\n" + "🎉" * 50)
            print("🎉 UEFA CHAMPIONS LEAGUE UI LAYOUT FIX COMPLETE!")
            print("🎉" * 50)
            print("✅ Fixed CSS grid and column layouts")
            print("✅ Improved responsive design")
            print("✅ Enhanced visual styling")
            print("✅ Added smooth animations")
            print("✅ Better mobile compatibility")
            print("🏆 UI is now clean and professional!")
            
        else:
            print("❌ Failed to fix HTML structure")
        
    except Exception as e:
        print(f"❌ Error during fix: {str(e)}")

if __name__ == "__main__":
    main()
