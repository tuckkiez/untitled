#!/usr/bin/env python3
"""
TheStatsDontLie.com Corners Data Scraper
ดึงข้อมูลเตะมุมจาก Argentina Primera Division
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

class CornersDataScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def scrape_corners_data(self, url):
        """ดึงข้อมูลเตะมุม"""
        print(f"🔍 Scraping corners data from: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ Successfully loaded corners page")
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # ดึงข้อมูลตาราง
                corners_data = self.extract_corners_table(soup)
                
                # ดึงข้อมูลสถิติ
                corners_stats = self.extract_corners_statistics(soup)
                
                # ดึงข้อมูลทีม
                team_corners = self.extract_team_corners_data(soup)
                
                return {
                    'corners_data': corners_data,
                    'corners_stats': corners_stats,
                    'team_corners': team_corners,
                    'scraped_at': datetime.now().isoformat(),
                    'source_url': url
                }
            else:
                print(f"❌ Failed to load page: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error scraping: {e}")
            return None
    
    def extract_corners_table(self, soup):
        """ดึงข้อมูลตารางเตะมุม"""
        corners_data = []
        
        try:
            # หาตารางข้อมูล
            tables = soup.find_all('table')
            
            for table in tables:
                # ตรวจสอบว่าเป็นตารางเตะมุมหรือไม่
                headers = table.find_all('th')
                if headers:
                    header_text = ' '.join([th.get_text().strip().lower() for th in headers])
                    
                    if 'corner' in header_text or 'team' in header_text:
                        rows = table.find_all('tr')
                        
                        for row in rows[1:]:  # ข้าม header
                            cells = row.find_all(['td', 'th'])
                            if len(cells) >= 3:
                                row_data = [cell.get_text().strip() for cell in cells]
                                corners_data.append(row_data)
            
            print(f"✅ Found {len(corners_data)} corners data rows")
            
        except Exception as e:
            print(f"⚠️ Error extracting corners table: {e}")
        
        return corners_data
    
    def extract_corners_statistics(self, soup):
        """ดึงสถิติเตะมุม"""
        stats = {}
        
        try:
            # หาข้อมูลสถิติ
            stat_elements = soup.find_all(['div', 'span', 'p'], class_=re.compile(r'stat|average|total'))
            
            for element in stat_elements:
                text = element.get_text().strip()
                
                # หาตัวเลขที่เกี่ยวข้องกับเตะมุม
                if re.search(r'\d+\.?\d*', text) and ('corner' in text.lower() or 'avg' in text.lower()):
                    stats[text] = re.findall(r'\d+\.?\d*', text)
            
            # หาข้อมูลเปอร์เซ็นต์
            percentage_elements = soup.find_all(string=re.compile(r'\d+%'))
            for elem in percentage_elements:
                parent = elem.parent
                if parent and 'corner' in parent.get_text().lower():
                    stats[f'percentage_{len(stats)}'] = elem.strip()
            
        except Exception as e:
            print(f"⚠️ Error extracting corners statistics: {e}")
        
        return stats
    
    def extract_team_corners_data(self, soup):
        """ดึงข้อมูลเตะมุมของแต่ละทีม"""
        team_data = {}
        
        try:
            # หาชื่อทีม Argentina
            argentina_teams = [
                'River Plate', 'Boca Juniors', 'Racing Club', 'Independiente',
                'San Lorenzo', 'Estudiantes', 'Aldosivi', 'Central Cordoba',
                'Gimnasia', 'Lanus', 'Banfield', 'Tigre', 'Velez', 'Huracan',
                'Argentinos Juniors', 'Defensa', 'Talleres', 'Rosario',
                'Newells', 'Godoy Cruz', 'Platense', 'Sarmiento'
            ]
            
            # ค้นหาข้อมูลทีม
            for team in argentina_teams:
                team_elements = soup.find_all(string=re.compile(team, re.IGNORECASE))
                
                for elem in team_elements:
                    parent = elem.parent
                    if parent:
                        # หาตัวเลขใกล้ๆ ชื่อทีม
                        parent_text = parent.get_text()
                        numbers = re.findall(r'\d+\.?\d*', parent_text)
                        
                        if numbers:
                            team_data[team] = {
                                'text': parent_text.strip(),
                                'numbers': numbers
                            }
        
        except Exception as e:
            print(f"⚠️ Error extracting team corners data: {e}")
        
        return team_data
    
    def analyze_corners_data(self, data):
        """วิเคราะห์ข้อมูลเตะมุม"""
        analysis = {
            'summary': {},
            'insights': [],
            'team_analysis': {},
            'predictions': {}
        }
        
        if not data:
            return analysis
        
        try:
            corners_data = data.get('corners_data', [])
            corners_stats = data.get('corners_stats', {})
            team_corners = data.get('team_corners', {})
            
            # วิเคราะห์ข้อมูลพื้นฐาน
            analysis['summary'] = {
                'total_data_rows': len(corners_data),
                'statistics_found': len(corners_stats),
                'teams_analyzed': len(team_corners)
            }
            
            # วิเคราะห์สถิติ
            if corners_stats:
                analysis['insights'].append(f"📊 Found {len(corners_stats)} corner statistics")
                
                # หาค่าเฉลี่ย
                averages = []
                for stat, values in corners_stats.items():
                    if isinstance(values, list) and values:
                        try:
                            avg = sum(float(v) for v in values) / len(values)
                            averages.append(avg)
                        except:
                            continue
                
                if averages:
                    overall_avg = sum(averages) / len(averages)
                    analysis['summary']['average_corners'] = round(overall_avg, 1)
                    analysis['insights'].append(f"⚽ Average corners per match: {overall_avg:.1f}")
            
            # วิเคราะห์ทีม
            if team_corners:
                analysis['insights'].append(f"🏆 Found data for {len(team_corners)} teams")
                
                # หาทีมที่เตะมุมมากที่สุด/น้อยที่สุด
                team_corner_counts = {}
                
                for team, info in team_corners.items():
                    numbers = info.get('numbers', [])
                    if numbers:
                        try:
                            # ใช้ตัวเลขแรกเป็นจำนวนเตะมุม
                            corners = float(numbers[0])
                            team_corner_counts[team] = corners
                        except:
                            continue
                
                if team_corner_counts:
                    max_team = max(team_corner_counts, key=team_corner_counts.get)
                    min_team = min(team_corner_counts, key=team_corner_counts.get)
                    
                    analysis['team_analysis'] = {
                        'highest_corners': {
                            'team': max_team,
                            'value': team_corner_counts[max_team]
                        },
                        'lowest_corners': {
                            'team': min_team,
                            'value': team_corner_counts[min_team]
                        }
                    }
                    
                    analysis['insights'].append(f"🔝 Highest corners: {max_team} ({team_corner_counts[max_team]})")
                    analysis['insights'].append(f"🔻 Lowest corners: {min_team} ({team_corner_counts[min_team]})")
            
            # การทำนายสำหรับ Aldosivi vs Central Cordoba
            aldosivi_data = team_corners.get('Aldosivi', {})
            central_data = team_corners.get('Central Cordoba', {})
            
            if aldosivi_data or central_data:
                analysis['predictions']['match_corners'] = self.predict_match_corners(
                    aldosivi_data, central_data, analysis.get('summary', {}).get('average_corners', 10)
                )
            
        except Exception as e:
            analysis['insights'].append(f"❌ Error in analysis: {e}")
        
        return analysis
    
    def predict_match_corners(self, home_data, away_data, league_avg):
        """ทำนายเตะมุมสำหรับแมทช์"""
        prediction = {
            'total_corners_prediction': 'Unknown',
            'over_under_9_5': 'Unknown',
            'confidence': 'Low',
            'reasoning': []
        }
        
        try:
            home_corners = 0
            away_corners = 0
            
            # ดึงข้อมูลเตะมุมของทีมเหย้า
            if home_data and home_data.get('numbers'):
                try:
                    home_corners = float(home_data['numbers'][0])
                    prediction['reasoning'].append(f"Aldosivi avg: {home_corners} corners")
                except:
                    pass
            
            # ดึงข้อมูลเตะมุมของทีมเยือน
            if away_data and away_data.get('numbers'):
                try:
                    away_corners = float(away_data['numbers'][0])
                    prediction['reasoning'].append(f"Central Cordoba avg: {away_corners} corners")
                except:
                    pass
            
            # คำนวณการทำนาย
            if home_corners > 0 and away_corners > 0:
                total_predicted = (home_corners + away_corners) / 2
                prediction['total_corners_prediction'] = f"{total_predicted:.1f}"
                
                if total_predicted > 9.5:
                    prediction['over_under_9_5'] = 'Over 9.5'
                    prediction['confidence'] = 'Medium'
                else:
                    prediction['over_under_9_5'] = 'Under 9.5'
                    prediction['confidence'] = 'Medium'
                
                prediction['reasoning'].append(f"Predicted total: {total_predicted:.1f} corners")
                
            elif league_avg:
                prediction['total_corners_prediction'] = f"{league_avg:.1f}"
                prediction['over_under_9_5'] = 'Over 9.5' if league_avg > 9.5 else 'Under 9.5'
                prediction['confidence'] = 'Low'
                prediction['reasoning'].append(f"Using league average: {league_avg:.1f}")
            
        except Exception as e:
            prediction['reasoning'].append(f"Error in prediction: {e}")
        
        return prediction

def main():
    print("🏈 TheStatsDontLie.com Corners Data Scraper")
    print("=" * 60)
    
    url = "https://www.thestatsdontlie.com/football/n-s-america/argentina/primera-division/corners/"
    scraper = CornersDataScraper()
    
    # ดึงข้อมูล
    print(f"📡 Scraping corners data...")
    scraped_data = scraper.scrape_corners_data(url)
    
    if scraped_data:
        # บันทึกข้อมูลดิบ
        with open('argentina_corners_raw_data.json', 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Raw corners data saved")
        
        # วิเคราะห์ข้อมูล
        print(f"\n🧠 Analyzing corners data...")
        analysis = scraper.analyze_corners_data(scraped_data)
        
        # แสดงผลการวิเคราะห์
        print(f"\n📊 CORNERS DATA ANALYSIS")
        print("=" * 50)
        
        # สรุป
        summary = analysis.get('summary', {})
        if summary:
            print(f"📋 Summary:")
            for key, value in summary.items():
                print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # ข้อมูลเชิงลึก
        insights = analysis.get('insights', [])
        if insights:
            print(f"\n💡 Insights:")
            for insight in insights:
                print(f"   {insight}")
        
        # การวิเคราะห์ทีม
        team_analysis = analysis.get('team_analysis', {})
        if team_analysis:
            print(f"\n🏆 TEAM ANALYSIS")
            print("-" * 30)
            for key, value in team_analysis.items():
                if isinstance(value, dict):
                    print(f"{key.replace('_', ' ').title()}: {value.get('team')} ({value.get('value')})")
        
        # การทำนายแมทช์
        predictions = analysis.get('predictions', {})
        if predictions:
            match_corners = predictions.get('match_corners', {})
            if match_corners:
                print(f"\n🎯 MATCH CORNERS PREDICTION")
                print("-" * 30)
                print(f"Aldosivi vs Central Córdoba:")
                print(f"   Total Corners: {match_corners.get('total_corners_prediction', 'Unknown')}")
                print(f"   Over/Under 9.5: {match_corners.get('over_under_9_5', 'Unknown')}")
                print(f"   Confidence: {match_corners.get('confidence', 'Unknown')}")
                
                reasoning = match_corners.get('reasoning', [])
                if reasoning:
                    print(f"   Reasoning:")
                    for reason in reasoning:
                        print(f"      - {reason}")
        
        # บันทึกการวิเคราะห์
        final_report = {
            'scraped_data': scraped_data,
            'analysis': analysis,
            'generated_at': datetime.now().isoformat()
        }
        
        with open('argentina_corners_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Complete corners analysis saved to argentina_corners_analysis.json")
        print(f"\n🚀 CORNERS DATA SCRAPING COMPLETED!")
        
        return analysis
        
    else:
        print(f"❌ Failed to scrape corners data")
        return None

if __name__ == "__main__":
    main()
