# ==========================================
# AGRISENSE AFRICA - PROFESSIONAL AGRICULTURAL INTELLIGENCE PLATFORM
# Version 2.0 - High Performance Agricultural Recommendation System
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# GLOBAL CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AgriSense Africa | Smart Agricultural Platform",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "AgriSense Africa - Smart Platform for Sustainable Agriculture"
    }
)

class Config:
    """Global application configurations"""
    APP_NAME = "AgriSense Africa"
    APP_VERSION = "2.0.0"
    COMPANY = "AgriSense Intelligence"
    
    CLIMATE_FILE = "Dados_clima_2018_2023.csv"
    NDVI_FOLDER = "ndvi"
    HEADER_IMAGE = "WhatsApp Image 2026-02-17 at 11.37.47.jpeg"
    
    TEMP_MIN = -10
    TEMP_MAX = 50
    PRECIP_MAX = 500
    SOIL_MOISTURE_MAX = 0.6
    
    PRIMARY_COLOR = "#1A4D3E"
    SECONDARY_COLOR = "#D9B48B"
    ACCENT_COLOR = "#E67E22"
    DANGER_COLOR = "#C44536"
    SUCCESS_COLOR = "#2C7A47"
    WARNING_COLOR = "#E67E22"
    INFO_COLOR = "#3498DB"
    BACKGROUND_LIGHT = "#FDF8F0"
    BACKGROUND_DARK = "#2C3E2F"
    TEXT_DARK = "#2C3E2F"
    TEXT_LIGHT = "#FDF8F0"
    
    GRADIENT_HEADER = f"linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SUCCESS_COLOR} 100%)"
    GRADIENT_CARD = "linear-gradient(135deg, #FFFFFF 0%, #FDF8F0 100%)"
    GRADIENT_SOIL = f"linear-gradient(135deg, {PRIMARY_COLOR} 0%, {BACKGROUND_DARK} 100%)"
    
    CACHE_TTL = 3600

def inject_custom_css():
    """Inject custom CSS styles"""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{
            font-family: 'Inter', sans-serif;
        }}
        
        .stApp {{
            background-color: {Config.BACKGROUND_LIGHT};
        }}
        
        .main-header {{
            background: {Config.GRADIENT_HEADER};
            padding: 1.5rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            gap: 2rem;
        }}
        
        .header-logo {{
            width: 80px;
            height: 80px;
            border-radius: 16px;
            object-fit: cover;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .header-content {{
            flex: 1;
        }}
        
        .header-content h1 {{
            color: white;
            margin: 0;
            font-size: 2rem;
            font-weight: 600;
            letter-spacing: -0.02em;
        }}
        
        .header-content p {{
            color: rgba(255,255,255,0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
        }}
        
        .header-tagline {{
            color: {Config.SECONDARY_COLOR};
            font-weight: 500;
            margin-top: 0.25rem;
        }}
        
        .metric-card {{
            background: {Config.GRADIENT_CARD};
            padding: 1.2rem;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.3s ease;
            border: 1px solid rgba(217, 180, 139, 0.2);
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(26, 77, 62, 0.1);
        }}
        
        .recommendation-card {{
            background: white;
            padding: 1.2rem;
            border-radius: 16px;
            margin: 0.8rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.3s ease;
            border-top: 3px solid;
            border: 1px solid rgba(217, 180, 139, 0.2);
            border-top-width: 3px;
        }}
        
        .recommendation-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(26, 77, 62, 0.12);
        }}
        
        .crop-high {{ border-top-color: {Config.SUCCESS_COLOR}; }}
        .crop-moderate {{ border-top-color: {Config.WARNING_COLOR}; }}
        .crop-low {{ border-top-color: {Config.DANGER_COLOR}; }}
        
        .progress-container {{
            background: rgba(217, 180, 139, 0.2);
            border-radius: 8px;
            height: 6px;
            margin: 12px 0;
            overflow: hidden;
        }}
        
        .progress-bar {{
            height: 100%;
            border-radius: 8px;
            transition: width 0.4s ease;
            background: linear-gradient(90deg, {Config.SUCCESS_COLOR}, {Config.PRIMARY_COLOR});
        }}
        
        .soil-card {{
            background: {Config.GRADIENT_SOIL};
            padding: 1rem;
            border-radius: 16px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem;
            background: {Config.GRADIENT_CARD};
            border-radius: 16px;
            margin-top: 2rem;
            font-size: 0.85rem;
            border: 1px solid rgba(217, 180, 139, 0.2);
            color: {Config.TEXT_DARK};
        }}
        
        h1, h2, h3, h4 {{
            color: {Config.PRIMARY_COLOR};
            font-weight: 600;
        }}
        
        .big-metric {{
            font-size: 2.2rem;
            font-weight: 700;
            color: {Config.SECONDARY_COLOR};
            margin: 0;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: {Config.TEXT_LIGHT};
            border-right: 1px solid rgba(217, 180, 139, 0.2);
        }}
        
        .stButton > button {{
            background: {Config.GRADIENT_HEADER};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1.2rem;
            font-weight: 500;
            transition: all 0.3s;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(26, 77, 62, 0.3);
        }}
        
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {Config.SECONDARY_COLOR};
            border-radius: 4px;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px;
            padding: 6px 16px;
            font-weight: 500;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {Config.PRIMARY_COLOR};
            color: white;
        }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
def load_climate_data() -> Optional[pd.DataFrame]:
    """Load and process climate data"""
    try:
        if not os.path.exists(Config.CLIMATE_FILE):
            st.error(f"File {Config.CLIMATE_FILE} not found")
            return None
        
        df = pd.read_csv(Config.CLIMATE_FILE)
        
        required_cols = ['valid_time', 't2m', 'tp', 'u10', 'v10', 'ssrd', 'swvl1', 'swvl2']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing columns: {missing_cols}")
            return None
        
        df['valid_time'] = pd.to_datetime(df['valid_time'])
        df['year'] = df['valid_time'].dt.year
        df['month'] = df['valid_time'].dt.month
        df['day'] = df['valid_time'].dt.day
        df['month_name'] = df['month'].apply(lambda x: calendar.month_abbr[x])
        
        df['temp_c'] = df['t2m'] - 273.15
        df['precip_mm'] = df['tp'] * 1000
        df['wind_speed'] = np.sqrt(df['u10']**2 + df['v10']**2)
        df['solar_mj'] = df['ssrd'] / 1e6
        
        df['temp_c'] = df['temp_c'].clip(Config.TEMP_MIN, Config.TEMP_MAX)
        df['precip_mm'] = df['precip_mm'].clip(0, Config.PRECIP_MAX)
        df['swvl1'] = df['swvl1'].clip(0, Config.SOIL_MOISTURE_MAX)
        df['swvl2'] = df['swvl2'].clip(0, Config.SOIL_MOISTURE_MAX)
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

@st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
def load_ndvi_data(year: int, month: int) -> Optional[Dict[str, Any]]:
    """Load NDVI data"""
    extensions = ['.tif', '.tiff', '.TIFF']
    name_formats = [f"NDVI_{year}_{month:02d}", f"ndvi_{year}_{month:02d}"]
    
    ndvi_path = None
    for name_format in name_formats:
        for ext in extensions:
            test_path = os.path.join(Config.NDVI_FOLDER, f"{name_format}{ext}")
            if os.path.exists(test_path):
                ndvi_path = test_path
                break
        if ndvi_path:
            break
    
    if ndvi_path is None:
        return None
    
    try:
        with rasterio.open(ndvi_path) as src:
            ndvi = src.read(1)
            ndvi = np.where(ndvi < -1000, np.nan, ndvi)
            ndvi = np.clip(ndvi, -1, 1)
            
            valid_data = ndvi[~np.isnan(ndvi)]
            
            return {
                'data': ndvi,
                'mean': float(np.mean(valid_data)) if len(valid_data) > 0 else 0,
                'std': float(np.std(valid_data)) if len(valid_data) > 0 else 0,
                'min': float(np.min(valid_data)) if len(valid_data) > 0 else 0,
                'max': float(np.max(valid_data)) if len(valid_data) > 0 else 0,
                'shape': ndvi.shape,
                'valid_pixels': len(valid_data),
                'total_pixels': ndvi.size
            }
    except Exception as e:
        st.warning(f"Error reading NDVI: {str(e)}")
        return None

class CropRecommender:
    """Crop recommendation system"""
    
    CROPS_DATABASE = {
        'Corn': {
            'icon': '🌽',
            'temp_range': (20, 30),
            'precip_range': (80, 150),
            'soil_range': (0.20, 0.35),
            'optimal_months': [10, 11, 12],
            'description': 'High nutritional value cereal, good for consumption and commercialization.',
            'planting_depth': '3-5 cm',
            'spacing': '80 x 40 cm',
            'cycle': '90-120 days',
            'expected_yield': '3-5 ton/ha',
            'water_requirement': 'Moderate',
            'market_value': 'High'
        },
        'Rice': {
            'icon': '🌾',
            'temp_range': (22, 32),
            'precip_range': (150, 250),
            'soil_range': (0.30, 0.45),
            'optimal_months': [11, 12, 1, 2],
            'description': 'Staple cereal, high market demand.',
            'planting_depth': '2-3 cm',
            'spacing': '25 x 25 cm',
            'cycle': '120-150 days',
            'expected_yield': '4-6 ton/ha',
            'water_requirement': 'High',
            'market_value': 'Very High'
        },
        'Cowpea': {
            'icon': '🫘',
            'temp_range': (20, 35),
            'precip_range': (60, 120),
            'soil_range': (0.15, 0.30),
            'optimal_months': [11, 12, 1],
            'description': 'Protein-rich legume, fixes nitrogen in the soil.',
            'planting_depth': '3-4 cm',
            'spacing': '50 x 20 cm',
            'cycle': '70-90 days',
            'expected_yield': '1-2 ton/ha',
            'water_requirement': 'Low',
            'market_value': 'High'
        },
        'Cassava': {
            'icon': '🌿',
            'temp_range': (18, 35),
            'precip_range': (100, 200),
            'soil_range': (0.15, 0.35),
            'optimal_months': [10, 11, 12, 1, 2],
            'description': 'Drought-resistant root, food security crop.',
            'planting_depth': '5-8 cm',
            'spacing': '100 x 80 cm',
            'cycle': '240-360 days',
            'expected_yield': '15-25 ton/ha',
            'water_requirement': 'Low',
            'market_value': 'Medium'
        },
        'Cotton': {
            'icon': '🧶',
            'temp_range': (20, 35),
            'precip_range': (70, 130),
            'soil_range': (0.20, 0.35),
            'optimal_months': [10, 11, 12],
            'description': 'Commercial crop with high profitability.',
            'planting_depth': '2-3 cm',
            'spacing': '80 x 40 cm',
            'cycle': '140-180 days',
            'expected_yield': '2-3 ton/ha',
            'water_requirement': 'Moderate',
            'market_value': 'Very High'
        },
        'Peanut': {
            'icon': '🥜',
            'temp_range': (22, 32),
            'precip_range': (80, 150),
            'soil_range': (0.15, 0.30),
            'optimal_months': [11, 12, 1],
            'description': 'Oilseed legume, good for crop rotation.',
            'planting_depth': '3-5 cm',
            'spacing': '60 x 20 cm',
            'cycle': '100-120 days',
            'expected_yield': '1.5-2.5 ton/ha',
            'water_requirement': 'Low',
            'market_value': 'High'
        },
        'Sweet Potato': {
            'icon': '🍠',
            'temp_range': (18, 30),
            'precip_range': (70, 150),
            'soil_range': (0.15, 0.35),
            'optimal_months': [11, 12, 1, 2],
            'description': 'Nutritious root, good for consumption and commercialization.',
            'planting_depth': '3-5 cm',
            'spacing': '80 x 30 cm',
            'cycle': '90-120 days',
            'expected_yield': '10-15 ton/ha',
            'water_requirement': 'Moderate',
            'market_value': 'Medium'
        },
        'Tomato': {
            'icon': '🍅',
            'temp_range': (18, 28),
            'precip_range': (80, 120),
            'soil_range': (0.25, 0.40),
            'optimal_months': [4, 5, 6, 7],
            'description': 'High demand vegetable, good profitability.',
            'planting_depth': '1-2 cm',
            'spacing': '100 x 50 cm',
            'cycle': '90-120 days',
            'expected_yield': '40-60 ton/ha',
            'water_requirement': 'High',
            'market_value': 'Very High'
        },
        'Onion': {
            'icon': '🧅',
            'temp_range': (15, 28),
            'precip_range': (60, 100),
            'soil_range': (0.20, 0.35),
            'optimal_months': [5, 6, 7, 8],
            'description': 'High commercial value vegetable.',
            'planting_depth': '1-2 cm',
            'spacing': '30 x 10 cm',
            'cycle': '120-150 days',
            'expected_yield': '20-30 ton/ha',
            'water_requirement': 'Moderate',
            'market_value': 'High'
        }
    }
    
    def __init__(self, temperature: float, precipitation: float, soil_moisture: float,
                 solar_radiation: float, ndvi: Optional[float], month: int):
        self.conditions = {
            'temp': temperature,
            'precip': precipitation,
            'soil': soil_moisture,
            'solar': solar_radiation,
            'ndvi': ndvi,
            'month': month
        }
    
    def _calculate_temperature_score(self, crop_params: Dict) -> Tuple[float, str]:
        temp = self.conditions['temp']
        temp_range = crop_params['temp_range']
        
        if temp_range[0] <= temp <= temp_range[1]:
            return 30, f"Ideal temperature: {temp:.1f}°C"
        elif temp < temp_range[0]:
            diff = temp_range[0] - temp
            score = max(0, 20 - diff * 1.5)
            return score, f"Temperature {temp:.1f}°C below ideal ({temp_range[0]}-{temp_range[1]}°C)"
        else:
            diff = temp - temp_range[1]
            score = max(0, 20 - diff * 1.2)
            return score, f"Temperature {temp:.1f}°C above ideal ({temp_range[0]}-{temp_range[1]}°C)"
    
    def _calculate_precipitation_score(self, crop_params: Dict) -> Tuple[float, str]:
        precip = self.conditions['precip']
        precip_range = crop_params['precip_range']
        
        if precip_range[0] <= precip <= precip_range[1]:
            return 30, f"Ideal precipitation: {precip:.1f}mm"
        elif precip < precip_range[0]:
            diff = precip_range[0] - precip
            score = max(0, 20 - diff / 5)
            return score, f"Precipitation {precip:.1f}mm below required ({precip_range[0]}-{precip_range[1]}mm)"
        else:
            diff = precip - precip_range[1]
            score = max(0, 20 - diff / 8)
            return score, f"Precipitation {precip:.1f}mm above recommended ({precip_range[0]}-{precip_range[1]}mm)"
    
    def _calculate_soil_score(self, crop_params: Dict) -> Tuple[float, str]:
        soil = self.conditions['soil']
        soil_range = crop_params.get('soil_range', (0.15, 0.35))
        
        if soil is None:
            return 0, "Soil data not available"
        
        if soil_range[0] <= soil <= soil_range[1]:
            return 20, f"Ideal soil moisture: {soil:.2f}"
        elif soil < soil_range[0]:
            diff = soil_range[0] - soil
            score = max(0, 12 - diff * 40)
            return score, f"Dry soil: {soil:.2f} (ideal >{soil_range[0]:.2f})"
        else:
            diff = soil - soil_range[1]
            score = max(0, 12 - diff * 40)
            return score, f"Waterlogged soil: {soil:.2f} (ideal <{soil_range[1]:.2f})"
    
    def _calculate_ndvi_score(self) -> Tuple[float, str]:
        ndvi = self.conditions['ndvi']
        
        if ndvi is None:
            return 0, "NDVI data not available"
        
        if ndvi >= 0.5:
            return 15, f"Excellent NDVI ({ndvi:.2f}) - Dense and healthy vegetation"
        elif ndvi >= 0.3:
            return 12, f"Good NDVI ({ndvi:.2f}) - Good vegetation cover"
        elif ndvi >= 0.2:
            return 8, f"Moderate NDVI ({ndvi:.2f}) - Developing vegetation"
        elif ndvi >= 0.1:
            return 4, f"Low NDVI ({ndvi:.2f}) - Sparse vegetation"
        else:
            return 2, f"Very low NDVI ({ndvi:.2f}) - Exposed soil"
    
    def _calculate_solar_score(self) -> Tuple[float, str]:
        solar = self.conditions['solar']
        
        if solar is None:
            return 0, "Radiation data not available"
        
        if solar >= 20:
            return 5, f"Excellent solar radiation: {solar:.1f} MJ/m²"
        elif solar >= 15:
            return 4, f"Good solar radiation: {solar:.1f} MJ/m²"
        elif solar >= 10:
            return 2, f"Moderate radiation: {solar:.1f} MJ/m²"
        else:
            return 1, f"Low radiation: {solar:.1f} MJ/m²"
    
    def _calculate_seasonal_score(self, crop_params: Dict) -> Tuple[float, str]:
        month = self.conditions['month']
        optimal_months = crop_params.get('optimal_months', [])
        
        if month in optimal_months:
            return 10, f"Ideal planting month ({calendar.month_name[month]})"
        elif optimal_months and abs(month - optimal_months[0]) <= 1:
            return 5, f"Near ideal period ({calendar.month_name[month]})"
        else:
            return 0, f"Non-ideal month for planting"
    
    def recommend_all(self) -> List[Dict[str, Any]]:
        results = []
        
        for crop_name, params in self.CROPS_DATABASE.items():
            temp_score, temp_detail = self._calculate_temperature_score(params)
            precip_score, precip_detail = self._calculate_precipitation_score(params)
            soil_score, soil_detail = self._calculate_soil_score(params)
            ndvi_score, ndvi_detail = self._calculate_ndvi_score()
            solar_score, solar_detail = self._calculate_solar_score()
            seasonal_score, seasonal_detail = self._calculate_seasonal_score(params)
            
            total_score = temp_score + precip_score + soil_score + ndvi_score + solar_score + seasonal_score
            
            if total_score >= 70:
                suitability_class = "high"
                suitability_text = "High"
                recommendation_text = "Excellent conditions for this crop"
            elif total_score >= 50:
                suitability_class = "moderate"
                suitability_text = "Moderate"
                recommendation_text = "Adequate conditions, monitor development"
            else:
                suitability_class = "low"
                suitability_text = "Low"
                recommendation_text = "Unfavorable conditions, consider alternatives"
            
            results.append({
                'name': crop_name,
                'icon': params['icon'],
                'score': total_score,
                'suitability_class': suitability_class,
                'suitability_text': suitability_text,
                'recommendation_text': recommendation_text,
                'temp_ideal': f"{params['temp_range'][0]}-{params['temp_range'][1]}°C",
                'precip_ideal': f"{params['precip_range'][0]}-{params['precip_range'][1]}mm",
                'description': params['description'],
                'planting_depth': params['planting_depth'],
                'spacing': params['spacing'],
                'cycle': params['cycle'],
                'expected_yield': params['expected_yield'],
                'water_requirement': params['water_requirement'],
                'market_value': params['market_value'],
                'details': {
                    'temperature': {'score': temp_score, 'detail': temp_detail},
                    'precipitation': {'score': precip_score, 'detail': precip_detail},
                    'soil': {'score': soil_score, 'detail': soil_detail},
                    'ndvi': {'score': ndvi_score, 'detail': ndvi_detail},
                    'solar': {'score': solar_score, 'detail': solar_detail},
                    'seasonal': {'score': seasonal_score, 'detail': seasonal_detail}
                }
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

class DashboardComponents:
    """Reusable dashboard components"""
    
    @staticmethod
    def render_header():
        """Render header with image"""
        if os.path.exists(Config.HEADER_IMAGE):
            st.markdown(f"""
            <div class="main-header">
                <img src="data:image/jpeg;base64,{DashboardComponents._get_image_base64(Config.HEADER_IMAGE)}" class="header-logo">
                <div class="header-content">
                    <h1>AgriSense Africa</h1>
                    <p>Smart Platform for Crop Recommendation</p>
                    <div class="header-tagline">Turning Farm Data into Better Harvests</div>
                    <p style="font-size: 0.8rem; margin-top: 0.5rem;">Version {Config.APP_VERSION} | {Config.COMPANY}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="main-header">
                <div class="header-content">
                    <h1>🌾 AgriSense Africa</h1>
                    <p>Smart Platform for Crop Recommendation</p>
                    <div class="header-tagline">Turning Farm Data into Better Harvests</div>
                    <p style="font-size: 0.8rem; margin-top: 0.5rem;">Version {Config.APP_VERSION} | {Config.COMPANY}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def _get_image_base64(image_path):
        """Convert image to base64"""
        import base64
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    
    @staticmethod
    def render_metrics(data: pd.DataFrame):
        """Render main metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="Temperature",
                value=f"{data['temp_c'].mean():.1f}°C",
                delta=f"{data['temp_c'].mean() - data['temp_c'].shift(12).mean():.1f}°C" if len(data) > 12 else None
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="Precipitation",
                value=f"{data['precip_mm'].mean():.1f} mm",
                delta=None
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="Wind Speed",
                value=f"{data['wind_speed'].mean():.1f} m/s",
                delta=None
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="Solar Radiation",
                value=f"{data['solar_mj'].mean():.1f} MJ/m²",
                delta=None
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_soil_analysis(data: pd.DataFrame):
        """Render soil analysis"""
        st.markdown("### Soil Moisture Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="soil-card">
                <h4 style="color: white;">Surface Layer</h4>
                <div class="big-metric">{data['swvl1'].mean():.3f}</div>
                <p>m³/m³ (0-7cm)</p>
                <small>Surface layer moisture</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="soil-card">
                <h4 style="color: white;">Deep Layer</h4>
                <div class="big-metric">{data['swvl2'].mean():.3f}</div>
                <p>m³/m³ (7-28cm)</p>
                <small>Root zone moisture</small>
            </div>
            """, unsafe_allow_html=True)
        
        layer1 = data['swvl1'].mean()
        layer2 = data['swvl2'].mean()
        
        if layer2 > layer1:
            st.success("Good infiltration: Water penetrating into deeper layers")
        elif layer1 > layer2 + 0.05:
            st.warning("Compromised drainage: Water accumulated on surface")
        else:
            st.info("Uniform profile: Balanced moisture throughout soil profile")
    
    @staticmethod
    def render_ndvi_analysis(ndvi_data: Optional[Dict], year: int, month: int):
        """Render NDVI analysis"""
        if ndvi_data is None:
            st.warning("NDVI data not available for this period")
            return
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            im = ax.imshow(ndvi_data['data'], cmap='RdYlGn', vmin=-0.2, vmax=0.8)
            plt.colorbar(im, ax=ax, label='NDVI', fraction=0.046, pad=0.04)
            ax.set_title(f'NDVI Vegetation Index\n{calendar.month_name[month]} {year}', 
                        fontsize=12, fontweight='bold', color=Config.TEXT_DARK)
            ax.axis('off')
            st.pyplot(fig)
        
        with col2:
            st.markdown("### Statistics")
            st.metric("Mean Value", f"{ndvi_data['mean']:.4f}")
            st.metric("Standard Deviation", f"{ndvi_data['std']:.4f}")
            st.metric("Minimum", f"{ndvi_data['min']:.4f}")
            st.metric("Maximum", f"{ndvi_data['max']:.4f}")
            
            st.markdown("### Interpretation")
            if ndvi_data['mean'] < 0.1:
                st.error("Very sparse vegetation - Exposed soil. Preparation and irrigation needed.")
            elif ndvi_data['mean'] < 0.3:
                st.warning("Sparse vegetation - Regular conditions for cultivation.")
            elif ndvi_data['mean'] < 0.5:
                st.success("Moderate vegetation - Good conditions for planting.")
            else:
                st.success("Dense and healthy vegetation - Excellent conditions.")
    
    @staticmethod
    def render_recommendations(recommendations: List[Dict]):
        """Render crop recommendations"""
        if not recommendations:
            st.info("Analyzing data to generate recommendations...")
            return
        
        st.markdown("## Crop Recommendations")
        
        top_crops = recommendations[:3]
        cols = st.columns(3)
        
        for idx, crop in enumerate(top_crops):
            with cols[idx]:
                card_class = f"crop-{crop['suitability_class']}"
                score_percent = crop['score']
                
                st.markdown(f"""
                <div class="recommendation-card {card_class}">
                    <h3 style="margin: 0 0 0.5rem 0;">{crop['icon']} {crop['name']}</h3>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {score_percent}%;"></div>
                    </div>
                    <p><strong>Compatibility:</strong> {score_percent:.0f}%</p>
                    <p><strong>Suitability:</strong> {crop['suitability_text']}</p>
                    <p><strong>Ideal temperature:</strong> {crop['temp_ideal']}</p>
                    <p><strong>Ideal precipitation:</strong> {crop['precip_ideal']}</p>
                    <p><strong>Description:</strong> {crop['description']}</p>
                    <p><strong>Water requirement:</strong> {crop['water_requirement']}</p>
                    <p><strong>Market value:</strong> {crop['market_value']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander("View detailed analysis of all crops"):
            for crop in recommendations:
                score_percent = crop['score']
                border_color = Config.SUCCESS_COLOR if crop['score'] >= 70 else Config.WARNING_COLOR if crop['score'] >= 50 else Config.DANGER_COLOR
                st.markdown(f"""
                <div style="padding: 1rem; margin: 0.5rem 0; border-left: 4px solid {border_color}; background: {Config.GRADIENT_CARD}; border-radius: 10px;">
                    <h4>{crop['icon']} {crop['name']} - {score_percent:.0f}% compatible</h4>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {score_percent}%;"></div>
                    </div>
                    <p><strong>{crop['recommendation_text']}</strong></p>
                    <p>{crop['description']}</p>
                    <details>
                        <summary>Technical details</summary>
                        <ul>
                            <li><strong>Planting:</strong> Depth {crop['planting_depth']}, Spacing {crop['spacing']}</li>
                            <li><strong>Cycle:</strong> {crop['cycle']}</li>
                            <li><strong>Expected yield:</strong> {crop['expected_yield']}</li>
                            <li><strong>Water requirement:</strong> {crop['water_requirement']}</li>
                        </ul>
                    </details>
                </div>
                """, unsafe_allow_html=True)
    
    @staticmethod
    def render_management_tips(data: pd.DataFrame, ndvi: Optional[float]):
        """Render management tips based on actual daily data"""
        tips = []
        
        # Calculate daily statistics for the period
        daily_precip = data.groupby(data['valid_time'].dt.date)['precip_mm'].sum()
        daily_temp_max = data.groupby(data['valid_time'].dt.date)['temp_c'].max()
        daily_temp_min = data.groupby(data['valid_time'].dt.date)['temp_c'].min()
        daily_soil = data.groupby(data['valid_time'].dt.date)['swvl1'].mean()
        
        # Precipitation analysis - count consecutive dry days
        dry_days = (daily_precip < 1).astype(int)
        consecutive_dry = 0
        max_consecutive_dry = 0
        for day in dry_days:
            if day == 1:
                consecutive_dry += 1
                max_consecutive_dry = max(max_consecutive_dry, consecutive_dry)
            else:
                consecutive_dry = 0
        
        total_precip = daily_precip.sum()
        rainy_days = (daily_precip > 1).sum()
        
        if max_consecutive_dry >= 15:
            tips.append(("Extended drought", f"{max_consecutive_dry} consecutive days without rain. Urgent irrigation needed.", "danger"))
        elif max_consecutive_dry >= 10:
            tips.append(("Prolonged dry spell", f"{max_consecutive_dry} days without rain. Monitor soil moisture.", "warning"))
        elif total_precip < 30:
            tips.append(("Low monthly rainfall", f"Only {total_precip:.1f}mm total. Consider irrigation or drought-tolerant crops.", "warning"))
        elif total_precip > 200:
            tips.append(("Excessive rainfall", f"{total_precip:.1f}mm total. Risk of waterlogging and erosion.", "warning"))
        
        # Temperature stress analysis
        heat_stress_days = (daily_temp_max > 35).sum()
        cold_stress_days = (daily_temp_min < 15).sum()
        
        if heat_stress_days > 5:
            tips.append(("Heat stress", f"{heat_stress_days} days with temperatures above 35°C. Increase irrigation frequency.", "warning"))
        elif cold_stress_days > 5:
            tips.append(("Cold stress", f"{cold_stress_days} days with temperatures below 15°C. Protect young plants.", "warning"))
        
        # Soil moisture analysis
        avg_soil = data['swvl1'].mean()
        min_soil = data['swvl1'].min()
        
        if min_soil < 0.12:
            tips.append(("Critical soil dryness", f"Minimum moisture {min_soil:.2f} m³/m³. Immediate irrigation required.", "danger"))
        elif avg_soil < 0.18:
            tips.append(("Dry soil conditions", f"Average moisture {avg_soil:.2f} m³/m³. Consider irrigation before planting.", "warning"))
        elif avg_soil > 0.45:
            tips.append(("Waterlogged soil", f"Average moisture {avg_soil:.2f} m³/m³. Improve drainage.", "warning"))
        elif 0.20 <= avg_soil <= 0.35:
            tips.append(("Ideal moisture", f"Average moisture {avg_soil:.2f} m³/m³. Optimal conditions.", "success"))
        
        # NDVI analysis
        if ndvi is not None:
            if ndvi < 0.15:
                tips.append(("Poor vegetation cover", f"NDVI {ndvi:.2f}. Soil exposed. Use cover crops or mulch.", "warning"))
            elif ndvi > 0.6:
                tips.append(("Excellent vegetation", f"NDVI {ndvi:.2f}. Healthy crops, maintain current management.", "success"))
        
        # Wind analysis
        avg_wind = data['wind_speed'].mean()
        max_wind = data['wind_speed'].max()
        
        if max_wind > 15:
            tips.append(("Strong winds", f"Maximum wind speed {max_wind:.1f} m/s. Risk of crop lodging.", "warning"))
        elif avg_wind > 8:
            tips.append(("Persistent winds", f"Average wind speed {avg_wind:.1f} m/s. Consider windbreaks.", "info"))
        
        # Solar radiation analysis
        avg_solar = data['solar_mj'].mean()
        
        if avg_solar < 12:
            tips.append(("Low solar radiation", f"Average {avg_solar:.1f} MJ/m². May affect crop growth.", "info"))
        elif avg_solar > 22:
            tips.append(("High solar radiation", f"Average {avg_solar:.1f} MJ/m². Risk of sunscald, provide shade for sensitive crops.", "warning"))
        
        if tips:
            st.markdown("### Management Tips")
            
            # Sort tips by priority
            priority_order = {"danger": 0, "warning": 1, "success": 2, "info": 3}
            tips.sort(key=lambda x: priority_order.get(x[2], 4))
            
            for title, message, tip_type in tips:
                if tip_type == "success":
                    st.success(f"**{title}** - {message}")
                elif tip_type == "danger":
                    st.error(f"**{title}** - {message}")
                elif tip_type == "warning":
                    st.warning(f"**{title}** - {message}")
                else:
                    st.info(f"**{title}** - {message}")
        else:
            st.success("Favorable conditions for planting! All parameters within optimal ranges.")
    
    @staticmethod
    def render_climate_dashboard(df: pd.DataFrame, year: int):
        """Render complete climate dashboard"""
        yearly_data = df[df['year'] == year]
        monthly_avg = yearly_data.groupby('month').agg({
            'temp_c': 'mean',
            'precip_mm': 'mean',
            'swvl1': 'mean',
            'swvl2': 'mean',
            'solar_mj': 'mean'
        }).reset_index()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Average Monthly Temperature',
                'Monthly Precipitation',
                'Soil Moisture',
                'Solar Radiation'
            ),
            vertical_spacing=0.15,
            horizontal_spacing=0.12
        )
        
        fig.add_trace(
            go.Scatter(
                x=monthly_avg['month'],
                y=monthly_avg['temp_c'],
                mode='lines+markers',
                name='Temperature',
                line=dict(color=Config.ACCENT_COLOR, width=3),
                marker=dict(size=8, color=Config.ACCENT_COLOR),
                fill='tozeroy',
                fillcolor=f'rgba(230,126,34,0.1)'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=monthly_avg['month'],
                y=monthly_avg['precip_mm'],
                name='Precipitation',
                marker_color=Config.INFO_COLOR,
                opacity=0.7
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=monthly_avg['month'],
                y=monthly_avg['swvl1'],
                mode='lines+markers',
                name='0-7cm',
                line=dict(color='#8B4513', width=2),
                marker=dict(size=6)
            ),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=monthly_avg['month'],
                y=monthly_avg['swvl2'],
                mode='lines+markers',
                name='7-28cm',
                line=dict(color=Config.PRIMARY_COLOR, width=2),
                marker=dict(size=6)
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=monthly_avg['month'],
                y=monthly_avg['solar_mj'],
                mode='lines+markers',
                name='Radiation',
                line=dict(color=Config.WARNING_COLOR, width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(230,126,34,0.1)'
            ),
            row=2, col=2
        )
        
        months_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        for row in [1, 2]:
            for col in [1, 2]:
                fig.update_xaxes(
                    title_text="Month",
                    tickmode='array',
                    tickvals=list(range(1, 13)),
                    ticktext=months_labels,
                    row=row, col=col
                )
        
        fig.update_yaxes(title_text="Temperature (°C)", row=1, col=1)
        fig.update_yaxes(title_text="Precipitation (mm)", row=1, col=2)
        fig.update_yaxes(title_text="Moisture (m³/m³)", row=2, col=1)
        fig.update_yaxes(title_text="Radiation (MJ/m²)", row=2, col=2)
        
        fig.update_layout(
            height=700,
            showlegend=True,
            title_text=f"Complete Climate Analysis - {year}",
            title_font_size=18,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function"""
    
    inject_custom_css()
    DashboardComponents.render_header()
    
    with st.spinner("Loading climate data..."):
        climate_data = load_climate_data()
    
    if climate_data is None:
        st.error("Unable to load data. Please check the files.")
        return
    
    with st.sidebar:
        st.markdown("## Controls")
        st.markdown("---")
        
        years = sorted(climate_data['year'].unique())
        selected_year = st.selectbox(
            "Year",
            years,
            index=len(years) - 1
        )
        
        selected_month = st.selectbox(
            "Month",
            list(range(1, 13)),
            format_func=lambda x: calendar.month_name[x]
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        **AgriSense Africa** is a smart platform that uses:
        - Historical climate data (2018-2023)
        - NDVI satellite imagery
        - Two-layer soil moisture analysis
        
        Recommendations are generated considering 6 factors simultaneously.
        """)
        
        st.markdown("---")
        st.markdown("### Analyzed Crops")
        crops_list = list(CropRecommender.CROPS_DATABASE.keys())
        st.write(", ".join(crops_list))
    
    filtered_data = climate_data[
        (climate_data['year'] == selected_year) & 
        (climate_data['month'] == selected_month)
    ]
    
    if filtered_data.empty:
        st.warning(f"No data available for {calendar.month_name[selected_month]} {selected_year}")
        return
    
    with st.spinner("Loading satellite data..."):
        ndvi_data = load_ndvi_data(selected_year, selected_month)
    
    temp = filtered_data['temp_c'].mean()
    precip = filtered_data['precip_mm'].mean()
    soil = filtered_data['swvl1'].mean()
    solar = filtered_data['solar_mj'].mean()
    ndvi = ndvi_data['mean'] if ndvi_data else None
    
    recommender = CropRecommender(temp, precip, soil, solar, ndvi, selected_month)
    recommendations = recommender.recommend_all()
    
    st.markdown(f"### Period: **{calendar.month_name[selected_month]} {selected_year}**")
    
    DashboardComponents.render_metrics(filtered_data)
    DashboardComponents.render_soil_analysis(filtered_data)
    
    st.markdown("### Vegetation Index")
    DashboardComponents.render_ndvi_analysis(ndvi_data, selected_year, selected_month)
    
    st.markdown("---")
    DashboardComponents.render_recommendations(recommendations)
    
    # Pass the full daily data for management tips
    DashboardComponents.render_management_tips(filtered_data, ndvi)
    
    st.markdown("---")
    st.markdown("## Complementary Analysis")
    
    tab1, tab2 = st.tabs(["Climate Dashboard", "Monthly Data"])
    
    with tab1:
        DashboardComponents.render_climate_dashboard(climate_data, selected_year)
    
    with tab2:
        monthly_data = climate_data[climate_data['year'] == selected_year].groupby('month').agg({
            'temp_c': 'mean',
            'precip_mm': 'mean',
            'swvl1': 'mean',
            'swvl2': 'mean',
            'solar_mj': 'mean'
        }).round(2)
        monthly_data.columns = ['Temperature (°C)', 'Precipitation (mm)',
                                'Moisture 0-7cm', 'Moisture 7-28cm', 'Radiation (MJ/m²)']
        st.dataframe(monthly_data, use_container_width=True)
    
    st.markdown(f"""
    <div class="footer">
        <p><strong>AgriSense Africa</strong> - Smart Platform for Sustainable Agriculture</p>
        <p>Estimated productivity increase: 20-30% with adoption of recommendations</p>
        <p style="font-size: 0.75rem;">© 2026 {Config.COMPANY} | Version {Config.APP_VERSION}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()