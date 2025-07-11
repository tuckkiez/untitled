#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Weather API Integration สำหรับการทำนายฟุตบอล
- ดึงข้อมูลสภาพอากาศจริง
- วิเคราะห์ผลกระทบต่อการเล่น
- รวมเข้ากับโมเดลทำนาย
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class WeatherPredictor:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Stadium locations (lat, lon)
        self.stadium_locations = {
            'Arsenal': (51.5549, -0.1084),  # Emirates Stadium
            'Chelsea': (51.4816, -0.1909),  # Stamford Bridge
            'Manchester City': (53.4831, -2.2004),  # Etihad Stadium
            'Manchester United': (53.4631, -2.2913),  # Old Trafford
            'Liverpool': (53.4308, -2.9608),  # Anfield
            'Tottenham': (51.6042, -0.0665),  # Tottenham Hotspur Stadium
            'Newcastle': (54.9756, -1.6217),  # St. James' Park
            'Brighton': (50.8611, -0.0831),  # Amex Stadium
            'Aston Villa': (52.5097, -1.8849),  # Villa Park
            'West Ham': (51.5386, -0.0166),  # London Stadium
            'Crystal Palace': (51.3983, -0.0855),  # Selhurst Park
            'Fulham': (51.4749, -0.2217),  # Craven Cottage
            'Brentford': (51.4907, -0.2889),  # Brentford Community Stadium
            'Wolves': (52.5901, -2.1306),  # Molineux Stadium
            'Everton': (53.4387, -2.9663),  # Goodison Park
            'Nottingham Forest': (52.9400, -1.1327),  # City Ground
            'Leicester': (52.6204, -1.1420),  # King Power Stadium
            'Southampton': (50.9058, -1.3914),  # St. Mary's Stadium
            'Ipswich': (52.0550, 1.1447),  # Portman Road
            'AFC Bournemouth': (50.7352, -1.8384)  # Vitality Stadium
        }
        
        # Weather impact factors
        self.weather_factors = {
            'temperature': {'optimal': (15, 22), 'weight': 0.2},
            'humidity': {'optimal': (40, 70), 'weight': 0.15},
            'wind_speed': {'optimal': (0, 10), 'weight': 0.25},
            'precipitation': {'optimal': (0, 1), 'weight': 0.3},
            'visibility': {'optimal': (10, 50), 'weight': 0.1}
        }
    
    def get_current_weather(self, team_name):
        """ดึงข้อมูลสภาพอากาศปัจจุบัน"""
        if not self.api_key:
            return self._generate_mock_weather()
        
        if team_name not in self.stadium_locations:
            return self._generate_mock_weather()
        
        lat, lon = self.stadium_locations[team_name]
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._process_weather_data(data)
            else:
                print(f"Weather API Error: {response.status_code}")
                return self._generate_mock_weather()
                
        except Exception as e:
            print(f"Error getting weather data: {e}")
            return self._generate_mock_weather()
    
    def get_forecast_weather(self, team_name, match_date):
        """ดึงข้อมูลพยากรณ์อากาศ"""
        if not self.api_key:
            return self._generate_mock_weather()
        
        if team_name not in self.stadium_locations:
            return self._generate_mock_weather()
        
        lat, lon = self.stadium_locations[team_name]
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._find_closest_forecast(data, match_date)
            else:
                return self._generate_mock_weather()
                
        except Exception as e:
            print(f"Error getting forecast data: {e}")
            return self._generate_mock_weather()
    
    def _process_weather_data(self, data):
        """ประมวลผลข้อมูลสภาพอากาศ"""
        weather_info = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data.get('wind', {}).get('speed', 0) * 3.6,  # m/s to km/h
            'wind_direction': data.get('wind', {}).get('deg', 0),
            'precipitation': data.get('rain', {}).get('1h', 0) + data.get('snow', {}).get('1h', 0),
            'visibility': data.get('visibility', 10000) / 1000,  # meters to km
            'cloud_cover': data['clouds']['all'],
            'weather_main': data['weather'][0]['main'],
            'weather_description': data['weather'][0]['description'],
            'datetime': datetime.fromtimestamp(data['dt'])
        }
        
        # คำนวณ weather impact score
        weather_info['impact_score'] = self._calculate_weather_impact(weather_info)
        
        return weather_info
    
    def _find_closest_forecast(self, forecast_data, target_date):
        """หาพยากรณ์อากาศที่ใกล้เคียงกับวันแข่งขัน"""
        target_timestamp = target_date.timestamp()
        closest_forecast = None
        min_time_diff = float('inf')
        
        for forecast in forecast_data['list']:
            forecast_time = forecast['dt']
            time_diff = abs(forecast_time - target_timestamp)
            
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_forecast = forecast
        
        if closest_forecast:
            return self._process_weather_data({
                'main': closest_forecast['main'],
                'weather': closest_forecast['weather'],
                'clouds': closest_forecast['clouds'],
                'wind': closest_forecast.get('wind', {}),
                'rain': closest_forecast.get('rain', {}),
                'snow': closest_forecast.get('snow', {}),
                'visibility': closest_forecast.get('visibility', 10000),
                'dt': closest_forecast['dt']
            })
        
        return self._generate_mock_weather()
    
    def _calculate_weather_impact(self, weather_info):
        """คำนวณผลกระทบของสภาพอากาศต่อการเล่น"""
        total_score = 0
        total_weight = 0
        
        for factor, config in self.weather_factors.items():
            if factor in weather_info:
                value = weather_info[factor]
                optimal_min, optimal_max = config['optimal']
                weight = config['weight']
                
                # คำนวณคะแนนสำหรับแต่ละปัจจัย
                if optimal_min <= value <= optimal_max:
                    factor_score = 1.0  # เหมาะสมที่สุด
                elif value < optimal_min:
                    factor_score = max(0, 1 - (optimal_min - value) / optimal_min)
                else:
                    factor_score = max(0, 1 - (value - optimal_max) / optimal_max)
                
                total_score += factor_score * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.5
    
    def _generate_mock_weather(self):
        """สร้างข้อมูลสภาพอากาศจำลอง"""
        # สร้างข้อมูลจำลองที่สมจริง
        season_month = datetime.now().month
        
        # ปรับอุณหภูมิตามฤดูกาล
        if season_month in [12, 1, 2]:  # ฤดูหนาว
            temp_base = 8
        elif season_month in [3, 4, 5]:  # ฤดูใบไม้ผลิ
            temp_base = 15
        elif season_month in [6, 7, 8]:  # ฤดูร้อน
            temp_base = 22
        else:  # ฤดูใบไม้ร่วง
            temp_base = 12
        
        weather_info = {
            'temperature': temp_base + np.random.normal(0, 5),
            'humidity': np.random.uniform(40, 85),
            'pressure': np.random.uniform(995, 1025),
            'wind_speed': np.random.exponential(8),  # ส่วนใหญ่ลมแรงน้อย
            'wind_direction': np.random.uniform(0, 360),
            'precipitation': np.random.exponential(1),  # ส่วนใหญ่ไม่มีฝน
            'visibility': np.random.uniform(8, 15),
            'cloud_cover': np.random.uniform(0, 100),
            'weather_main': np.random.choice(['Clear', 'Clouds', 'Rain', 'Drizzle'], 
                                           p=[0.4, 0.4, 0.15, 0.05]),
            'weather_description': 'simulated weather',
            'datetime': datetime.now()
        }
        
        weather_info['impact_score'] = self._calculate_weather_impact(weather_info)
        
        return weather_info
    
    def get_weather_features(self, home_team, away_team, match_date=None):
        """ดึง weather features สำหรับโมเดล ML"""
        if not match_date:
            match_date = datetime.now()
        
        # ใช้สนามของทีมเหย้า
        if match_date > datetime.now():
            weather = self.get_forecast_weather(home_team, match_date)
        else:
            weather = self.get_current_weather(home_team)
        
        # สร้าง features สำหรับ ML
        features = {
            'weather_temperature': weather['temperature'],
            'weather_humidity': weather['humidity'],
            'weather_wind_speed': weather['wind_speed'],
            'weather_precipitation': weather['precipitation'],
            'weather_visibility': weather['visibility'],
            'weather_impact_score': weather['impact_score'],
            'weather_cloud_cover': weather['cloud_cover'],
            'weather_pressure': weather['pressure'],
            
            # Categorical weather features (one-hot encoded)
            'weather_clear': 1 if weather['weather_main'] == 'Clear' else 0,
            'weather_clouds': 1 if weather['weather_main'] == 'Clouds' else 0,
            'weather_rain': 1 if weather['weather_main'] == 'Rain' else 0,
            'weather_drizzle': 1 if weather['weather_main'] == 'Drizzle' else 0,
            
            # Derived features
            'weather_is_good': 1 if weather['impact_score'] > 0.7 else 0,
            'weather_is_bad': 1 if weather['impact_score'] < 0.4 else 0,
            'weather_temp_optimal': 1 if 15 <= weather['temperature'] <= 22 else 0,
            'weather_high_wind': 1 if weather['wind_speed'] > 15 else 0,
            'weather_heavy_rain': 1 if weather['precipitation'] > 5 else 0,
        }
        
        return features, weather
    
    def analyze_weather_impact(self, matches_df):
        """วิเคราะห์ผลกระทบของสภาพอากาศต่อผลการแข่งขัน"""
        print("🌤️ กำลังวิเคราะห์ผลกระทบของสภาพอากาศ...")
        
        weather_analysis = []
        
        for idx, match in matches_df.iterrows():
            features, weather = self.get_weather_features(
                match['home_team'], 
                match['away_team'], 
                pd.to_datetime(match['date'])
            )
            
            # ผลการแข่งขัน
            if match['home_goals'] > match['away_goals']:
                result = 'Home Win'
            elif match['home_goals'] == match['away_goals']:
                result = 'Draw'
            else:
                result = 'Away Win'
            
            weather_analysis.append({
                'match': f"{match['home_team']} vs {match['away_team']}",
                'result': result,
                'total_goals': match['home_goals'] + match['away_goals'],
                'weather_score': weather['impact_score'],
                'temperature': weather['temperature'],
                'precipitation': weather['precipitation'],
                'wind_speed': weather['wind_speed'],
                'weather_main': weather['weather_main']
            })
        
        analysis_df = pd.DataFrame(weather_analysis)
        
        # วิเคราะห์ความสัมพันธ์
        print(f"\n📊 สถิติสภาพอากาศ:")
        print(f"   อุณหภูมิเฉลี่ย: {analysis_df['temperature'].mean():.1f}°C")
        print(f"   ฝนเฉลี่ย: {analysis_df['precipitation'].mean():.1f}mm")
        print(f"   ลมเฉลี่ย: {analysis_df['wind_speed'].mean():.1f}km/h")
        print(f"   คะแนนสภาพอากาศเฉลี่ย: {analysis_df['weather_score'].mean():.3f}")
        
        # วิเคราะห์ตามสภาพอากาศ
        weather_groups = analysis_df.groupby('weather_main')
        print(f"\n🌦️ ผลการแข่งขันตามสภาพอากาศ:")
        for weather_type, group in weather_groups:
            avg_goals = group['total_goals'].mean()
            home_wins = (group['result'] == 'Home Win').sum()
            draws = (group['result'] == 'Draw').sum()
            away_wins = (group['result'] == 'Away Win').sum()
            total = len(group)
            
            print(f"   {weather_type:10}: {total:2d} เกม | "
                  f"ประตูเฉลี่ย: {avg_goals:.1f} | "
                  f"H:{home_wins} D:{draws} A:{away_wins}")
        
        return analysis_df

# Example usage
if __name__ == "__main__":
    # ใช้ API key จริงหรือ None สำหรับข้อมูลจำลอง
    weather_predictor = WeatherPredictor(api_key=None)  # ใส่ API key ของคุณที่นี่
    
    print("🌤️ ระบบวิเคราะห์สภาพอากาศสำหรับฟุตบอล")
    print("="*50)
    
    # ทดสอบดึงข้อมูลสภาพอากาศ
    teams_to_test = ['Arsenal', 'Manchester City', 'Liverpool']
    
    for team in teams_to_test:
        print(f"\n⚽ {team}:")
        weather = weather_predictor.get_current_weather(team)
        
        print(f"   🌡️  อุณหภูมิ: {weather['temperature']:.1f}°C")
        print(f"   💧 ความชื้น: {weather['humidity']:.0f}%")
        print(f"   💨 ลม: {weather['wind_speed']:.1f} km/h")
        print(f"   🌧️  ฝน: {weather['precipitation']:.1f} mm")
        print(f"   👁️  ทัศนวิสัย: {weather['visibility']:.1f} km")
        print(f"   📊 คะแนนผลกระทบ: {weather['impact_score']:.3f}")
        print(f"   🌤️  สภาพอากาศ: {weather['weather_main']}")
    
    # ทดสอบ weather features
    print(f"\n🔧 ตัวอย่าง Weather Features:")
    features, weather_detail = weather_predictor.get_weather_features('Arsenal', 'Chelsea')
    
    print(f"Features สำหรับ ML:")
    for key, value in list(features.items())[:10]:  # แสดง 10 features แรก
        print(f"   {key:25}: {value}")
    
    print(f"\n✅ ระบบ Weather Integration พร้อมใช้งาน!")
