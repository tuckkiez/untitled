#!/usr/bin/env python3
"""
Goal5.co Match Analysis Scraper
ดึงข้อมูลและวิเคราะห์ผลงานจาก goal5.co
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

class Goal5Scraper:
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
    
    def scrape_match_analysis(self, match_id):
        """ดึงข้อมูลการวิเคราะห์แมทช์"""
        url = f"https://goal5.co/analyse/?id={match_id}"
        
        print(f"🔍 Scraping match analysis from: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ Successfully loaded page")
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # ดึงข้อมูลพื้นฐานของแมทช์
                match_info = self.extract_match_info(soup)
                
                # ดึงข้อมูลสถิติ
                statistics = self.extract_statistics(soup)
                
                # ดึงข้อมูลฟอร์ม
                form_data = self.extract_form_data(soup)
                
                # ดึงข้อมูลการทำนาย
                predictions = self.extract_predictions(soup)
                
                # ดึงข้อมูลราคาต่อรอง
                odds_data = self.extract_odds_data(soup)
                
                return {
                    'match_info': match_info,
                    'statistics': statistics,
                    'form_data': form_data,
                    'predictions': predictions,
                    'odds_data': odds_data,
                    'scraped_at': datetime.now().isoformat(),
                    'source_url': url
                }
            else:
                print(f"❌ Failed to load page: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error scraping: {e}")
            return None
    
    def extract_match_info(self, soup):
        """ดึงข้อมูลพื้นฐานของแมทช์"""
        match_info = {}
        
        try:
            # หาชื่อทีม
            team_elements = soup.find_all(['h1', 'h2', 'h3'], class_=re.compile(r'team|match'))
            if not team_elements:
                team_elements = soup.find_all('div', class_=re.compile(r'team|match'))
            
            # หาข้อความที่มี "vs" หรือ "-"
            match_title = soup.find('title')
            if match_title:
                title_text = match_title.get_text()
                match_info['page_title'] = title_text
                
                # พยายามแยกชื่อทีม
                if ' vs ' in title_text:
                    teams = title_text.split(' vs ')
                    if len(teams) >= 2:
                        match_info['home_team'] = teams[0].strip()
                        match_info['away_team'] = teams[1].split(' - ')[0].strip()
                elif ' - ' in title_text:
                    teams = title_text.split(' - ')
                    if len(teams) >= 2:
                        match_info['home_team'] = teams[0].strip()
                        match_info['away_team'] = teams[1].strip()
            
            # หาวันที่และเวลา
            date_elements = soup.find_all(text=re.compile(r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}'))
            if date_elements:
                match_info['date_found'] = [elem.strip() for elem in date_elements[:3]]
            
            # หาลีก
            league_elements = soup.find_all(text=re.compile(r'Premier|Liga|League|Division|Championship'))
            if league_elements:
                match_info['league_mentions'] = [elem.strip() for elem in league_elements[:3]]
            
        except Exception as e:
            print(f"⚠️ Error extracting match info: {e}")
        
        return match_info
    
    def extract_statistics(self, soup):
        """ดึงข้อมูลสถิติ"""
        statistics = {}
        
        try:
            # หาตารางสถิติ
            tables = soup.find_all('table')
            for i, table in enumerate(tables):
                rows = table.find_all('tr')
                table_data = []
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        row_data = [cell.get_text().strip() for cell in cells]
                        table_data.append(row_data)
                
                if table_data:
                    statistics[f'table_{i+1}'] = table_data
            
            # หาข้อมูลสถิติในรูปแบบอื่น
            stat_divs = soup.find_all('div', class_=re.compile(r'stat|score|percent'))
            stat_data = []
            
            for div in stat_divs:
                text = div.get_text().strip()
                if text and len(text) < 100:  # กรองข้อความที่สั้น
                    stat_data.append(text)
            
            if stat_data:
                statistics['stat_elements'] = stat_data[:20]  # เก็บ 20 รายการแรก
            
        except Exception as e:
            print(f"⚠️ Error extracting statistics: {e}")
        
        return statistics
    
    def extract_form_data(self, soup):
        """ดึงข้อมูลฟอร์ม"""
        form_data = {}
        
        try:
            # หาข้อมูลฟอร์มล่าสุด
            form_elements = soup.find_all(text=re.compile(r'W|L|D'))
            form_matches = []
            
            for elem in form_elements:
                text = elem.strip()
                # หาแพทเทิร์นฟอร์ม เช่น WWLDW
                if re.match(r'^[WLD]{3,10}$', text):
                    form_matches.append(text)
            
            if form_matches:
                form_data['form_patterns'] = form_matches[:10]
            
            # หาข้อมูลผลการแข่งขันล่าสุด
            score_elements = soup.find_all(text=re.compile(r'\d+-\d+'))
            scores = []
            
            for elem in score_elements:
                text = elem.strip()
                if re.match(r'^\d+-\d+$', text):
                    scores.append(text)
            
            if scores:
                form_data['recent_scores'] = scores[:10]
            
        except Exception as e:
            print(f"⚠️ Error extracting form data: {e}")
        
        return form_data
    
    def extract_predictions(self, soup):
        """ดึงข้อมูลการทำนาย"""
        predictions = {}
        
        try:
            # หาเปอร์เซ็นต์การทำนาย
            percentage_elements = soup.find_all(text=re.compile(r'\d+%'))
            percentages = []
            
            for elem in percentage_elements:
                text = elem.strip()
                if re.match(r'^\d+%$', text):
                    percentages.append(text)
            
            if percentages:
                predictions['percentages'] = percentages[:10]
            
            # หาคำทำนาย
            prediction_keywords = ['Home Win', 'Away Win', 'Draw', 'Over', 'Under', 'BTTS', 'Clean Sheet']
            prediction_elements = []
            
            for keyword in prediction_keywords:
                elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
                for elem in elements:
                    text = elem.strip()
                    if keyword.lower() in text.lower():
                        prediction_elements.append(text)
            
            if prediction_elements:
                predictions['prediction_text'] = prediction_elements[:10]
            
        except Exception as e:
            print(f"⚠️ Error extracting predictions: {e}")
        
        return predictions
    
    def extract_odds_data(self, soup):
        """ดึงข้อมูลราคาต่อรอง"""
        odds_data = {}
        
        try:
            # หาราคาต่อรองในรูปแบบทศนิยม
            decimal_odds = soup.find_all(text=re.compile(r'\d+\.\d{2}'))
            odds_values = []
            
            for elem in decimal_odds:
                text = elem.strip()
                try:
                    value = float(text)
                    if 1.0 <= value <= 50.0:  # ช่วงราคาต่อรองที่สมเหตุสมผล
                        odds_values.append(value)
                except:
                    continue
            
            if odds_values:
                odds_data['decimal_odds'] = odds_values[:15]
            
            # หาราคาต่อรองแบบเศษส่วน
            fraction_odds = soup.find_all(text=re.compile(r'\d+/\d+'))
            fractions = []
            
            for elem in fraction_odds:
                text = elem.strip()
                if re.match(r'^\d+/\d+$', text):
                    fractions.append(text)
            
            if fractions:
                odds_data['fractional_odds'] = fractions[:10]
            
        except Exception as e:
            print(f"⚠️ Error extracting odds data: {e}")
        
        return odds_data
    
    def analyze_scraped_data(self, data):
        """วิเคราะห์ข้อมูลที่ดึงมา"""
        analysis = {
            'summary': {},
            'insights': [],
            'recommendations': []
        }
        
        if not data:
            return analysis
        
        try:
            # วิเคราะห์ข้อมูลพื้นฐาน
            match_info = data.get('match_info', {})
            if 'home_team' in match_info and 'away_team' in match_info:
                analysis['summary']['match'] = f"{match_info['home_team']} vs {match_info['away_team']}"
                analysis['insights'].append(f"✅ Match identified: {analysis['summary']['match']}")
            
            # วิเคราะห์สถิติ
            statistics = data.get('statistics', {})
            if statistics:
                total_stats = sum(len(v) for v in statistics.values() if isinstance(v, list))
                analysis['summary']['statistics_found'] = total_stats
                analysis['insights'].append(f"📊 Found {total_stats} statistical data points")
            
            # วิเคราะห์ฟอร์ม
            form_data = data.get('form_data', {})
            if form_data.get('form_patterns'):
                analysis['summary']['form_patterns'] = len(form_data['form_patterns'])
                analysis['insights'].append(f"📈 Found {len(form_data['form_patterns'])} form patterns")
            
            if form_data.get('recent_scores'):
                analysis['summary']['recent_scores'] = len(form_data['recent_scores'])
                analysis['insights'].append(f"⚽ Found {len(form_data['recent_scores'])} recent scores")
            
            # วิเคราะห์การทำนาย
            predictions = data.get('predictions', {})
            if predictions.get('percentages'):
                analysis['summary']['prediction_percentages'] = len(predictions['percentages'])
                analysis['insights'].append(f"🎯 Found {len(predictions['percentages'])} prediction percentages")
            
            # วิเคราะห์ราคาต่อรอง
            odds_data = data.get('odds_data', {})
            if odds_data.get('decimal_odds'):
                analysis['summary']['odds_values'] = len(odds_data['decimal_odds'])
                analysis['insights'].append(f"💰 Found {len(odds_data['decimal_odds'])} odds values")
            
            # ให้คำแนะนำ
            if total_stats > 10:
                analysis['recommendations'].append("✅ Sufficient statistical data for analysis")
            else:
                analysis['recommendations'].append("⚠️ Limited statistical data - may need additional sources")
            
            if form_data:
                analysis['recommendations'].append("✅ Form data available for trend analysis")
            
            if predictions:
                analysis['recommendations'].append("✅ Prediction data can be used for comparison")
            
            if odds_data:
                analysis['recommendations'].append("✅ Odds data available for value betting analysis")
            
        except Exception as e:
            analysis['insights'].append(f"❌ Error in analysis: {e}")
        
        return analysis

def main():
    print("🔍 Goal5.co Match Analysis Scraper")
    print("=" * 50)
    
    match_id = "4866151"
    scraper = Goal5Scraper()
    
    # ดึงข้อมูล
    print(f"📡 Scraping match ID: {match_id}")
    scraped_data = scraper.scrape_match_analysis(match_id)
    
    if scraped_data:
        # บันทึกข้อมูลดิบ
        with open(f'goal5_match_{match_id}_raw.json', 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Raw data saved to goal5_match_{match_id}_raw.json")
        
        # วิเคราะห์ข้อมูล
        print(f"\n🧠 Analyzing scraped data...")
        analysis = scraper.analyze_scraped_data(scraped_data)
        
        # แสดงผลการวิเคราะห์
        print(f"\n📊 ANALYSIS RESULTS")
        print("=" * 50)
        
        # สรุป
        summary = analysis.get('summary', {})
        if summary:
            print(f"📋 Summary:")
            for key, value in summary.items():
                print(f"   {key}: {value}")
        
        # ข้อมูลเชิงลึก
        insights = analysis.get('insights', [])
        if insights:
            print(f"\n💡 Insights:")
            for insight in insights:
                print(f"   {insight}")
        
        # คำแนะนำ
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            print(f"\n🎯 Recommendations:")
            for rec in recommendations:
                print(f"   {rec}")
        
        # แสดงข้อมูลสำคัญ
        match_info = scraped_data.get('match_info', {})
        if match_info:
            print(f"\n🏆 MATCH INFORMATION")
            print("-" * 30)
            for key, value in match_info.items():
                if isinstance(value, list):
                    print(f"{key}: {', '.join(value[:3])}")
                else:
                    print(f"{key}: {value}")
        
        # แสดงสถิติ
        statistics = scraped_data.get('statistics', {})
        if statistics:
            print(f"\n📊 STATISTICS PREVIEW")
            print("-" * 30)
            for key, value in list(statistics.items())[:2]:
                if isinstance(value, list):
                    print(f"{key}: {len(value)} items")
                    for item in value[:3]:
                        if isinstance(item, list):
                            print(f"   {' | '.join(item)}")
                        else:
                            print(f"   {item}")
        
        # แสดงการทำนาย
        predictions = scraped_data.get('predictions', {})
        if predictions:
            print(f"\n🎯 PREDICTIONS FOUND")
            print("-" * 30)
            for key, value in predictions.items():
                if isinstance(value, list):
                    print(f"{key}: {', '.join(value[:5])}")
        
        # บันทึกการวิเคราะห์
        final_report = {
            'match_id': match_id,
            'scraped_data': scraped_data,
            'analysis': analysis,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(f'goal5_match_{match_id}_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Complete analysis saved to goal5_match_{match_id}_analysis.json")
        print(f"\n🚀 SCRAPING COMPLETED!")
        
    else:
        print(f"❌ Failed to scrape data from Goal5.co")

if __name__ == "__main__":
    main()
