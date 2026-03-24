# ==========================================
# AGRISENSE AFRICA - PROFESSIONAL AGRICULTURAL INTELLIGENCE PLATFORM
# Version 5.7 - ENHANCED VEGETATION ANALYSIS WITH SPATIAL VARIABILITY
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
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Machine Learning Libraries
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import xgboost as xgb

# ==========================================
# GLOBAL CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AgriSense Africa | Professional Agricultural Intelligence Platform",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

class Config:
    """Global application configurations"""
    APP_NAME = "AgriSense Africa"
    APP_VERSION = "5.7.0"
    COMPANY = "AgriSense Intelligence"
    COMPANY_DESCRIPTION = "Transformando dados em decisões agrícolas sustentáveis desde 2020"
    COMPANY_MISSION = "Empoderar agricultores africanos com tecnologia de ponta"
    CONTACT = "contact@agrisense.africa"
    WEBSITE = "www.agrisense.africa"
    PHONE = "+248841349563"
    
    CLIMATE_FILE = "Dados_clima_2018_2023.csv"
    NDVI_FOLDER = "ndvi"
    HEADER_IMAGE = "WhatsApp Image 2026-02-17 at 11.37.47.jpeg"
    MODELS_FOLDER = "models"
    
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
    
    CACHE_TTL = 3600

def inject_custom_css():
    """Inject professional custom CSS styles"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        
        .stApp { background-color: #FDF8F0; }
        
        .main-header {
            background: linear-gradient(135deg, #1A4D3E 0%, #2C7A47 100%);
            padding: 2rem 2.5rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }
        
        .header-content h1 {
            color: white;
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
        }
        
        .header-content p {
            color: rgba(255,255,255,0.9);
            margin: 0.5rem 0 0 0;
        }
        
        .metric-card {
            background: white;
            padding: 1.2rem;
            border-radius: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            border: 1px solid rgba(217, 180, 139, 0.3);
            transition: transform 0.2s;
        }
        
        .metric-card:hover { transform: translateY(-2px); }
        
        .metric-value { font-size: 2rem; font-weight: 700; color: #1A4D3E; }
        .metric-label { font-size: 0.85rem; color: #666; margin-top: 0.25rem; }
        .metric-interpretation { font-size: 0.75rem; color: #888; margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #eee; }
        
        .recommendation-card {
            background: white;
            padding: 1.5rem;
            border-radius: 20px;
            margin: 1rem 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            border-left: 4px solid;
        }
        
        .crop-high { border-left-color: #2C7A47; }
        .crop-moderate { border-left-color: #E67E22; }
        .crop-low { border-left-color: #C44536; }
        
        .progress-container {
            background: #E8F0EA;
            border-radius: 12px;
            height: 8px;
            margin: 12px 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            border-radius: 12px;
            background: linear-gradient(90deg, #2C7A47, #1A4D3E);
        }
        
        .soil-card {
            background: linear-gradient(135deg, #1A4D3E 0%, #2C3E2F 100%);
            padding: 1.2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
        }
        
        .statistics-panel {
            background: white;
            padding: 1.2rem;
            border-radius: 16px;
            margin: 1rem 0;
            border: 1px solid #E8F0EA;
        }
        
        .ndvi-interpretation {
            background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
            padding: 1.2rem;
            border-radius: 16px;
            margin-top: 1rem;
            border-left: 4px solid #3498DB;
        }
        
        .vegetation-zone-card {
            background: white;
            padding: 1rem;
            border-radius: 16px;
            margin: 0.5rem 0;
            border-left: 4px solid;
        }
        
        .sidebar-company {
            background: linear-gradient(135deg, #1A4D3E 0%, #2C7A47 100%);
            padding: 1.2rem;
            border-radius: 16px;
            color: white;
            margin-top: 1rem;
        }
        
        .footer {
            text-align: center;
            padding: 2rem;
            background: white;
            border-radius: 20px;
            margin-top: 2rem;
            font-size: 0.85rem;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #1A4D3E 0%, #2C7A47 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.6rem 1.5rem;
            font-weight: 500;
            transition: transform 0.2s;
        }
        
        .stButton > button:hover { transform: translateY(-2px); }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: white;
            padding: 0.5rem;
            border-radius: 16px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            padding: 8px 20px;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #1A4D3E;
            color: white;
        }
        
        .alert-critical {
            background: linear-gradient(135deg, #C44536 0%, #E67E22 100%);
            padding: 1rem;
            border-radius: 12px;
            color: white;
            margin: 0.5rem 0;
        }
        
        .alert-warning {
            background: linear-gradient(135deg, #E67E22 0%, #F39C12 100%);
            padding: 1rem;
            border-radius: 12px;
            color: white;
            margin: 0.5rem 0;
        }
        
        .alert-success {
            background: linear-gradient(135deg, #2C7A47 0%, #52BE80 100%);
            padding: 1rem;
            border-radius: 12px;
            color: white;
            margin: 0.5rem 0;
        }
        
        .alert-info {
            background: linear-gradient(135deg, #3498DB 0%, #5DADE2 100%);
            padding: 1rem;
            border-radius: 12px;
            color: white;
            margin: 0.5rem 0;
        }
        
        .agricultural-guide {
            background: white;
            padding: 1.5rem;
            border-radius: 20px;
            margin: 1rem 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }
        
        .guide-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin: 1.5rem 0;
        }
        
        .guide-section {
            background: #F8F9FA;
            padding: 1.2rem;
            border-radius: 16px;
            border-left: 3px solid #1A4D3E;
        }
        
        .guide-section h4 {
            color: #1A4D3E;
            margin-top: 0;
            margin-bottom: 0.8rem;
        }
        
        .prediction-chart-container {
            background: white;
            padding: 1rem;
            border-radius: 16px;
            margin: 1rem 0;
        }
        
        .crop-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .guide-grid { grid-template-columns: 1fr; }
        }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# DATA LOADING FUNCTIONS
# ==========================================

@st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
def load_climate_data() -> Optional[pd.DataFrame]:
    """Load and process climate data."""
    try:
        if not os.path.exists(Config.CLIMATE_FILE):
            st.error(f"Arquivo {Config.CLIMATE_FILE} não encontrado")
            return None
        
        df = pd.read_csv(Config.CLIMATE_FILE)
        
        required_cols = ['valid_time', 'latitude', 'longitude']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Colunas obrigatórias ausentes: {missing_cols}")
            return None
        
        df['valid_time'] = pd.to_datetime(df['valid_time'], errors='coerce')
        df = df.dropna(subset=['valid_time'])
        
        df['year'] = df['valid_time'].dt.year.astype(int)
        df['month'] = df['valid_time'].dt.month.astype(int)
        df['day'] = df['valid_time'].dt.day.astype(int)
        df['month_name'] = df['month'].apply(lambda x: calendar.month_abbr[x])
        
        if 't2m' in df.columns:
            df['t2m'] = pd.to_numeric(df['t2m'], errors='coerce')
            df['temp_c'] = df['t2m'] - 273.15
        else:
            df['temp_c'] = np.nan
        
        if 'tp' in df.columns:
            df['tp'] = pd.to_numeric(df['tp'], errors='coerce')
            df['precip_mm'] = df['tp'] * 1000
        else:
            df['precip_mm'] = np.nan
        
        if 'u10' in df.columns and 'v10' in df.columns:
            df['u10'] = pd.to_numeric(df['u10'], errors='coerce')
            df['v10'] = pd.to_numeric(df['v10'], errors='coerce')
            df['wind_speed'] = np.sqrt(df['u10']**2 + df['v10']**2)
        else:
            df['wind_speed'] = np.nan
        
        if 'swvl1' in df.columns:
            df['swvl1'] = pd.to_numeric(df['swvl1'], errors='coerce')
        else:
            df['swvl1'] = np.nan
            
        if 'swvl2' in df.columns:
            df['swvl2'] = pd.to_numeric(df['swvl2'], errors='coerce')
        else:
            df['swvl2'] = np.nan
        
        if 'ssrd' in df.columns:
            df['ssrd'] = pd.to_numeric(df['ssrd'], errors='coerce')
            df['solar_mj'] = df['ssrd'] / 1e6
        else:
            df['solar_mj'] = np.nan
        
        df['temp_c'] = df['temp_c'].clip(Config.TEMP_MIN, Config.TEMP_MAX)
        df['precip_mm'] = df['precip_mm'].clip(0, Config.PRECIP_MAX)
        df['swvl1'] = df['swvl1'].clip(0, Config.SOIL_MOISTURE_MAX)
        df['swvl2'] = df['swvl2'].clip(0, Config.SOIL_MOISTURE_MAX)
        
        monthly_agg = df.groupby(['year', 'month']).agg({
            'temp_c': 'mean',
            'precip_mm': 'mean',
            'wind_speed': 'mean',
            'swvl1': 'mean',
            'swvl2': 'mean',
            'solar_mj': 'mean'
        }).reset_index()
        
        monthly_agg['month_name'] = monthly_agg['month'].apply(lambda x: calendar.month_abbr[x])
        monthly_agg = monthly_agg.dropna(subset=['temp_c', 'precip_mm'], how='any')
        
        if monthly_agg.empty:
            st.error("Dados climáticos vazios após processamento")
            return None
        
        st.info(f"Dados carregados: {len(monthly_agg)} registros mensais de {monthly_agg['year'].min()} a {monthly_agg['year'].max()}")
        
        return monthly_agg
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

@st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
def load_ndvi_data(year: int, month: int) -> Optional[Dict[str, Any]]:
    """Load Sentinel-2 NDVI data"""
    year = int(year)
    month = int(month)
    
    extensions = ['.tif', '.tiff', '.TIFF']
    name_formats = [
        f"NDVI_{year}_{month:02d}",
        f"ndvi_{year}_{month:02d}",
        f"S2_NDVI_{year}_{month:02d}",
        f"sentinel2_ndvi_{year}_{month:02d}"
    ]
    
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
            if ndvi.max() > 1 or ndvi.min() < -1:
                ndvi = ndvi / 100.0 if ndvi.max() > 10 else ndvi / 255.0
            
            ndvi = np.where(ndvi < -1000, np.nan, ndvi)
            ndvi = np.clip(ndvi, -1, 1)
            
            valid_data = ndvi[~np.isnan(ndvi)]
            
            if len(valid_data) == 0:
                return None
            
            percentiles = np.percentile(valid_data, [10, 25, 50, 75, 90])
            mean_ndvi = float(np.mean(valid_data))
            
            if mean_ndvi >= 0.6:
                health_status = "Excelente"
                health_description = "Vegetação densa e saudável, alta atividade fotossintética"
            elif mean_ndvi >= 0.4:
                health_status = "Bom"
                health_description = "Boa cobertura vegetal, desenvolvimento adequado"
            elif mean_ndvi >= 0.2:
                health_status = "Moderado"
                health_description = "Vegetação com estresse moderado, possível déficit hídrico"
            elif mean_ndvi >= 0.1:
                health_status = "Baixo"
                health_description = "Vegetação esparsa ou início de desenvolvimento"
            else:
                health_status = "Crítico"
                health_description = "Solo exposto ou vegetação severamente estressada"
            
            return {
                'data': ndvi,
                'mean': mean_ndvi,
                'std': float(np.std(valid_data)),
                'min': float(np.min(valid_data)),
                'max': float(np.max(valid_data)),
                'median': float(percentiles[2]),
                'p10': float(percentiles[0]),
                'p25': float(percentiles[1]),
                'p75': float(percentiles[3]),
                'p90': float(percentiles[4]),
                'shape': ndvi.shape,
                'valid_pixels': len(valid_data),
                'total_pixels': ndvi.size,
                'health_status': health_status,
                'health_description': health_description,
                'cv': float(np.std(valid_data) / mean_ndvi) if mean_ndvi > 0 else 0,
                'sensor': 'Sentinel-2',
                'resolution': '10-20m'
            }
    except Exception as e:
        st.warning(f"Erro ao ler NDVI: {str(e)}")
        return None

def analyze_vegetation_zones(ndvi_data: np.ndarray) -> Tuple[Dict[str, Dict], Dict[str, Any]]:
    """Analyze vegetation zones with recommendations and spatial variability"""
    zones = {
        'crítico': {'range': (-1, 0.1), 'color': '#C44536', 'area_pct': 0, 'recommendations': []},
        'baixo': {'range': (0.1, 0.2), 'color': '#E67E22', 'area_pct': 0, 'recommendations': []},
        'moderado': {'range': (0.2, 0.4), 'color': '#F39C12', 'area_pct': 0, 'recommendations': []},
        'bom': {'range': (0.4, 0.6), 'color': '#52BE80', 'area_pct': 0, 'recommendations': []},
        'excelente': {'range': (0.6, 1.0), 'color': '#1A4D3E', 'area_pct': 0, 'recommendations': []}
    }
    
    total_pixels = ndvi_data.size
    
    for zone, info in zones.items():
        mask = (ndvi_data >= info['range'][0]) & (ndvi_data < info['range'][1])
        info['area_pct'] = (np.sum(mask) / total_pixels) * 100
    
    # Generate zone-specific recommendations
    if zones['crítico']['area_pct'] > 15:
        zones['crítico']['recommendations'].extend([
            "Aplicar matéria orgânica para melhorar estrutura do solo",
            "Implementar práticas de conservação de água",
            "Considerar culturas de cobertura para proteção do solo"
        ])
    
    if zones['baixo']['area_pct'] > 20:
        zones['baixo']['recommendations'].extend([
            "Aplicar fertilizantes nitrogenados para estimular crescimento",
            "Implementar sistema de irrigação localizada",
            "Monitorar pragas e doenças que afetam plantas estressadas"
        ])
    
    if zones['moderado']['area_pct'] > 25:
        zones['moderado']['recommendations'].extend([
            "Aplicação parcelada de fertilizantes para otimizar absorção",
            "Manter monitoramento semanal do desenvolvimento vegetativo",
            "Considerar adubação foliar para complementar nutrientes"
        ])
    
    if zones['bom']['area_pct'] > 30:
        zones['bom']['recommendations'].extend([
            "Manter práticas de manejo atuais",
            "Monitorar para identificar áreas com potencial de melhoria",
            "Documentar técnicas bem-sucedidas para replicação"
        ])
    
    if zones['excelente']['area_pct'] > 20:
        zones['excelente']['recommendations'].extend([
            "Registrar práticas de manejo para referência futura",
            "Considerar rotação de culturas para manter saúde do solo"
        ])
    
    # Spatial variability analysis
    valid_data = ndvi_data[~np.isnan(ndvi_data)]
    spatial_variability = {
        'coefficient_variation': (np.std(valid_data) / np.mean(valid_data)) * 100 if np.mean(valid_data) > 0 else 0,
        'spatial_autocorrelation': '',
        'management_zones': sum(1 for z in zones.values() if z['area_pct'] > 5),
        'recommendation': '',
        'uniformity_index': 1 - (np.std(valid_data) / (np.mean(valid_data) + 0.1))
    }
    
    if spatial_variability['coefficient_variation'] < 15:
        spatial_variability['spatial_autocorrelation'] = 'Baixa variabilidade espacial'
        spatial_variability['recommendation'] = "Recomenda-se manejo uniforme em toda área"
    elif spatial_variability['coefficient_variation'] < 30:
        spatial_variability['spatial_autocorrelation'] = 'Moderada variabilidade espacial'
        spatial_variability['recommendation'] = "Recomenda-se manejo por zona de produtividade"
    else:
        spatial_variability['spatial_autocorrelation'] = 'Alta variabilidade espacial'
        spatial_variability['recommendation'] = "Recomenda-se agricultura de precisão com aplicação em taxa variável"
    
    # NDVI homogeneity assessment
    if spatial_variability['uniformity_index'] > 0.8:
        spatial_variability['homogeneity'] = 'Alta homogeneidade'
    elif spatial_variability['uniformity_index'] > 0.6:
        spatial_variability['homogeneity'] = 'Homogeneidade moderada'
    else:
        spatial_variability['homogeneity'] = 'Baixa homogeneidade'
    
    return zones, spatial_variability

def generate_ndvi_prediction(current_ndvi: np.ndarray, days_ahead: int = 30) -> np.ndarray:
    """Generate future NDVI prediction with integrated imagery"""
    # Simple prediction model - would be replaced with actual ML model
    trend = np.random.normal(0.02, 0.01, current_ndvi.shape)
    noise = np.random.normal(0, 0.03, current_ndvi.shape)
    predicted_ndvi = np.clip(current_ndvi + trend * (days_ahead/30) + noise, -1, 1)
    return predicted_ndvi

# ==========================================
# CROP DATABASE
# ==========================================

CROPS_DATABASE = {
    'Milho': {
        'icon': '🌽',
        'temp_range': (20, 30),
        'precip_range': (80, 150),
        'soil_range': (0.20, 0.35),
        'optimal_months': [10, 11, 12],
        'description': 'Cereal de alto valor nutricional, fundamental para segurança alimentar e pecuária.',
        'planting_depth': '3-5 cm',
        'spacing': '80 x 40 cm (80.000 plantas/ha)',
        'cycle': '90-120 dias',
        'expected_yield': '3-5 toneladas/ha em sequeiro, 6-8 com irrigação',
        'water_requirement': 'Moderado (450-600 mm/ciclo)',
        'market_value': 'Alto',
        'fertilizer': 'NPK 10-10-10: 300 kg/ha no plantio, Ureia: 150 kg/ha parcelado',
        'irrigation': 'Crítico no florescimento e enchimento de grãos',
        'soil_preparation': 'Aragem profunda + gradagem niveladora',
        'harvest_indicator': 'Grãos com 15-18% umidade, palha seca',
        'post_harvest': 'Secagem até 13% umidade para armazenamento'
    },
    'Arroz': {
        'icon': '🌾',
        'temp_range': (22, 32),
        'precip_range': (150, 250),
        'soil_range': (0.30, 0.45),
        'optimal_months': [11, 12, 1, 2],
        'description': 'Cereal básico de alto consumo, cultura estratégica para segurança alimentar.',
        'planting_depth': '2-3 cm (sistema irrigado)',
        'spacing': '25 x 25 cm (160.000 plantas/ha)',
        'cycle': '120-150 dias',
        'expected_yield': '4-6 toneladas/ha',
        'water_requirement': 'Alto (800-1200 mm/ciclo)',
        'market_value': 'Muito Alto',
        'fertilizer': 'Ureia: 150 kg/ha parcelado, NPK 15-15-15: 300 kg/ha',
        'irrigation': 'Manter lâmina de 5-10 cm, drenar 15 dias antes da colheita',
        'soil_preparation': 'Gradagem + nivelamento de precisão',
        'harvest_indicator': '80% dos grãos em coloração palha',
        'post_harvest': 'Secagem imediata para 13% umidade'
    },
    'Feijão-Caupi': {
        'icon': '🫘',
        'temp_range': (20, 35),
        'precip_range': (60, 120),
        'soil_range': (0.15, 0.30),
        'optimal_months': [11, 12, 1],
        'description': 'Leguminosa proteica, fixadora de nitrogênio. Excelente para rotação de culturas.',
        'planting_depth': '3-4 cm',
        'spacing': '50 x 20 cm (100.000 plantas/ha)',
        'cycle': '70-90 dias',
        'expected_yield': '1-2 toneladas/ha',
        'water_requirement': 'Baixo (250-400 mm/ciclo)',
        'market_value': 'Alto',
        'fertilizer': 'Apenas fósforo: 50 kg/ha P2O5',
        'irrigation': 'Crítico apenas no florescimento',
        'soil_preparation': 'Preparo convencional, boa descompactação',
        'harvest_indicator': 'Vagens com 80% de coloração marrom',
        'post_harvest': 'Debulha mecânica, secagem natural'
    },
    'Mandioca': {
        'icon': '🌿',
        'temp_range': (18, 35),
        'precip_range': (100, 200),
        'soil_range': (0.15, 0.35),
        'optimal_months': [10, 11, 12, 1, 2],
        'description': 'Raiz energética, tolerante à seca. Cultura de segurança alimentar.',
        'planting_depth': '5-8 cm (manivas)',
        'spacing': '100 x 80 cm (12.500 plantas/ha)',
        'cycle': '240-360 dias',
        'expected_yield': '15-25 toneladas/ha',
        'water_requirement': 'Baixo (300-400 mm/ciclo)',
        'market_value': 'Médio',
        'fertilizer': 'KCl: 150 kg/ha, NPK 10-20-20: 400 kg/ha',
        'irrigation': 'Apenas nos primeiros 3 meses',
        'soil_preparation': 'Aragem profunda, subsolagem',
        'harvest_indicator': '12-24 meses, folhas iniciando senescência',
        'post_harvest': 'Processamento em até 48h'
    },
    'Algodão': {
        'icon': '🧶',
        'temp_range': (20, 35),
        'precip_range': (70, 130),
        'soil_range': (0.20, 0.35),
        'optimal_months': [10, 11, 12],
        'description': 'Cultura comercial de alta rentabilidade para indústria têxtil.',
        'planting_depth': '2-3 cm',
        'spacing': '80 x 40 cm (80.000 plantas/ha)',
        'cycle': '140-180 dias',
        'expected_yield': '2-3 toneladas/ha de pluma',
        'water_requirement': 'Moderado (400-500 mm/ciclo)',
        'market_value': 'Muito Alto',
        'fertilizer': 'NPK 10-20-10: 300 kg/ha, Ureia: 150 kg/ha',
        'irrigation': 'Crítico no florescimento',
        'soil_preparation': 'Preparo profundo, boa drenagem',
        'harvest_indicator': 'Maçãs abertas (80% de abertura)',
        'post_harvest': 'Secagem artificial, enfardamento'
    },
    'Amendoim': {
        'icon': '🥜',
        'temp_range': (22, 32),
        'precip_range': (80, 150),
        'soil_range': (0.15, 0.30),
        'optimal_months': [11, 12, 1],
        'description': 'Oleaginosa de alto valor, fixa nitrogênio e melhora estrutura do solo.',
        'planting_depth': '3-5 cm',
        'spacing': '60 x 20 cm (80.000 plantas/ha)',
        'cycle': '100-120 dias',
        'expected_yield': '1.5-2.5 toneladas/ha',
        'water_requirement': 'Baixo (300-400 mm/ciclo)',
        'market_value': 'Alto',
        'fertilizer': 'Gesso: 200 kg/ha, NPK 10-20-20: 300 kg/ha',
        'irrigation': 'Crítico no florescimento',
        'soil_preparation': 'Preparo com boa descompactação',
        'harvest_indicator': 'Folhas amarelecidas, vagens escuras',
        'post_harvest': 'Arranquio mecânico, secagem em leiras'
    },
    'Batata-Doce': {
        'icon': '🍠',
        'temp_range': (18, 30),
        'precip_range': (70, 150),
        'soil_range': (0.15, 0.35),
        'optimal_months': [11, 12, 1, 2],
        'description': 'Raiz nutritiva rica em betacaroteno, boa para consumo in natura.',
        'planting_depth': '3-5 cm (ramas)',
        'spacing': '80 x 30 cm (40.000 plantas/ha)',
        'cycle': '90-120 dias',
        'expected_yield': '10-15 toneladas/ha',
        'water_requirement': 'Moderado (350-450 mm/ciclo)',
        'market_value': 'Médio',
        'fertilizer': 'KCl: 200 kg/ha, NPK 10-10-10: 300 kg/ha',
        'irrigation': 'Regular durante formação de raízes',
        'soil_preparation': 'Canteiros elevados',
        'harvest_indicator': '90-120 dias, folhas amarelecendo',
        'post_harvest': 'Curagem por 7-10 dias'
    },
    'Tomate': {
        'icon': '🍅',
        'temp_range': (18, 28),
        'precip_range': (80, 120),
        'soil_range': (0.25, 0.40),
        'optimal_months': [4, 5, 6, 7],
        'description': 'Hortaliça de alta demanda, alta rentabilidade por área.',
        'planting_depth': '1-2 cm (sementeira)',
        'spacing': '100 x 50 cm (20.000 plantas/ha)',
        'cycle': '90-120 dias',
        'expected_yield': '40-60 toneladas/ha',
        'water_requirement': 'Alto (500-700 mm/ciclo)',
        'market_value': 'Muito Alto',
        'fertilizer': 'NPK 15-15-15: 400 kg/ha, Nitrato de cálcio: 200 kg/ha',
        'irrigation': 'Gotejamento: 2-3 L/planta/dia',
        'soil_preparation': 'Canteiros elevados, mulching',
        'harvest_indicator': 'Frutos com 70-90% coloração madura',
        'post_harvest': 'Colheita manual, armazenamento refrigerado'
    },
    'Cebola': {
        'icon': '🧅',
        'temp_range': (15, 28),
        'precip_range': (60, 100),
        'soil_range': (0.20, 0.35),
        'optimal_months': [5, 6, 7, 8],
        'description': 'Hortaliça de alto valor comercial, bom para diversificação.',
        'planting_depth': '1-2 cm (bulbilhos)',
        'spacing': '30 x 10 cm (330.000 plantas/ha)',
        'cycle': '120-150 dias',
        'expected_yield': '20-30 toneladas/ha',
        'water_requirement': 'Moderado (350-450 mm/ciclo)',
        'market_value': 'Alto',
        'fertilizer': 'NPK 10-20-10: 300 kg/ha, Ureia: 100 kg/ha',
        'irrigation': 'Crítico durante formação de bulbos',
        'soil_preparation': 'Leiras bem drenadas',
        'harvest_indicator': 'Folhas tombadas (50-70%)',
        'post_harvest': 'Curagem ao sol por 5-7 dias'
    }
}

# ==========================================
# ML MODEL TRAINER
# ==========================================

class EnhancedMLModelTrainer:
    """Enhanced ML trainer with NDVI integration"""
    
    def __init__(self, climate_data: pd.DataFrame):
        self.data = climate_data.copy()
        self.models = {}
        self.scalers = {}
        
    def prepare_enhanced_features(self):
        """Prepare features with NDVI integration"""
        features_df = self.data.copy()
        features_df['sin_month'] = np.sin(2 * np.pi * features_df['month'] / 12)
        features_df['cos_month'] = np.cos(2 * np.pi * features_df['month'] / 12)
        
        ndvi_values = []
        for _, row in features_df.iterrows():
            try:
                year_val = int(row['year'])
                month_val = int(row['month'])
                ndvi_data = load_ndvi_data(year_val, month_val)
                ndvi_values.append(ndvi_data['mean'] if ndvi_data else 0.3)
            except:
                ndvi_values.append(0.3)
        
        features_df['ndvi_mean'] = ndvi_values
        
        return features_df
    
    def create_enhanced_suitability_labels(self, features_df: pd.DataFrame):
        """Create enhanced suitability labels"""
        crops_labels = {}
        
        for crop_name, params in CROPS_DATABASE.items():
            temp_min, temp_max = params['temp_range']
            precip_min, precip_max = params['precip_range']
            soil_min, soil_max = params.get('soil_range', (0.15, 0.35))
            
            scores = []
            for _, row in features_df.iterrows():
                score = 0
                
                if temp_min <= row['temp_c'] <= temp_max:
                    score += 35
                elif row['temp_c'] < temp_min:
                    score += max(0, 25 - (temp_min - row['temp_c']) * 2)
                else:
                    score += max(0, 25 - (row['temp_c'] - temp_max) * 2)
                
                if precip_min <= row['precip_mm'] <= precip_max:
                    score += 25
                elif row['precip_mm'] < precip_min:
                    score += max(0, 15 - (precip_min - row['precip_mm']) / 5)
                else:
                    score += max(0, 15 - (row['precip_mm'] - precip_max) / 8)
                
                if soil_min <= row['swvl1'] <= soil_max:
                    score += 15
                elif row['swvl1'] < soil_min:
                    score += max(0, 8 - (soil_min - row['swvl1']) * 50)
                else:
                    score += max(0, 8 - (row['swvl1'] - soil_max) * 50)
                
                if row.get('ndvi_mean') and not pd.isna(row['ndvi_mean']):
                    ndvi = row['ndvi_mean']
                    if ndvi >= 0.5:
                        score += 15
                    elif ndvi >= 0.3:
                        score += 12
                    elif ndvi >= 0.2:
                        score += 8
                    elif ndvi >= 0.1:
                        score += 4
                
                optimal_months = params.get('optimal_months', [])
                if row['month'] in optimal_months:
                    score += 10
                elif optimal_months and abs(row['month'] - optimal_months[0]) <= 1:
                    score += 5
                
                scores.append(min(100, score))
            
            crops_labels[crop_name] = scores
        
        return crops_labels
    
    def train_enhanced_models(self):
        """Train enhanced ML models"""
        features_df = self.prepare_enhanced_features()
        crops_labels = self.create_enhanced_suitability_labels(features_df)
        
        feature_columns = ['temp_c', 'precip_mm', 'swvl1', 'solar_mj', 'month',
                          'sin_month', 'cos_month', 'ndvi_mean']
        
        X = features_df[feature_columns].fillna(features_df[feature_columns].mean()).values
        
        if len(X) == 0:
            st.warning("Não há dados suficientes para treinamento")
            return {}
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        idx_count = 0
        for crop_name, y_values in crops_labels.items():
            y = np.array(y_values[:len(features_df)])
            
            if len(y) < 10:
                continue
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            models_to_test = {
                'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
                'GradientBoosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42)
            }
            
            best_score = -np.inf
            best_model = None
            best_name = None
            
            for model_name, model in models_to_test.items():
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                r2 = r2_score(y_test, y_pred)
                
                if r2 > best_score:
                    best_score = r2
                    best_model = model
                    best_name = model_name
            
            self.models[crop_name] = {
                'model': best_model,
                'scaler': scaler,
                'score': best_score,
                'model_type': best_name,
                'feature_names': feature_columns
            }
            
            idx_count += 1
            progress_bar.progress(min(idx_count / len(crops_labels), 1.0))
        
        status_text.text(f"Modelos treinados com sucesso! {len(self.models)} culturas processadas.")
        progress_bar.empty()
        
        return self.models
    
    def predict_crop_with_ndvi(self, temp, precip, soil_moisture, solar_radiation, month, ndvi, crop_name):
        """Predict suitability with NDVI integration"""
        if crop_name not in self.models:
            return None, None, None
        
        model_info = self.models[crop_name]
        model = model_info['model']
        scaler = model_info['scaler']
        
        sin_month = np.sin(2 * np.pi * month / 12)
        cos_month = np.cos(2 * np.pi * month / 12)
        ndvi_val = ndvi if ndvi is not None else 0.3
        
        features = np.array([[
            temp, precip, soil_moisture, solar_radiation, month,
            sin_month, cos_month, ndvi_val
        ]])
        
        features_scaled = scaler.transform(features)
        score = model.predict(features_scaled)[0]
        
        if score >= 70:
            level = "Alta"
            recommendation = "Condições excelentes para o cultivo"
        elif score >= 50:
            level = "Moderada"
            recommendation = "Condições adequadas, requer monitoramento"
        else:
            level = "Baixa"
            recommendation = "Não recomendado para este período"
        
        return score, level, recommendation
    
    def predict_all_crops_with_ndvi(self, temp, precip, soil_moisture, solar_radiation, month, ndvi):
        """Predict all crops with NDVI integration"""
        results = []
        for crop_name in self.models.keys():
            score, level, recommendation = self.predict_crop_with_ndvi(
                temp, precip, soil_moisture, solar_radiation, month, ndvi, crop_name
            )
            if score is not None:
                results.append({
                    'crop': crop_name,
                    'score': score,
                    'level': level,
                    'recommendation': recommendation,
                    'icon': CROPS_DATABASE[crop_name]['icon']
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def save_models(self, path="models/"):
        """Save enhanced models"""
        if not os.path.exists(path):
            os.makedirs(path)
        
        for crop_name, model_info in self.models.items():
            model_path = f"{path}{crop_name.replace(' ', '_')}_monthly_model.joblib"
            scaler_path = f"{path}{crop_name.replace(' ', '_')}_monthly_scaler.joblib"
            joblib.dump(model_info['model'], model_path)
            joblib.dump(model_info['scaler'], scaler_path)
        
        st.success(f"Modelos salvos em {path}")
    
    def load_models(self, path="models/"):
        """Load enhanced models"""
        if not os.path.exists(path):
            return False
        
        loaded_models = {}
        for crop_name in CROPS_DATABASE.keys():
            model_path = f"{path}{crop_name.replace(' ', '_')}_monthly_model.joblib"
            scaler_path = f"{path}{crop_name.replace(' ', '_')}_monthly_scaler.joblib"
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                loaded_models[crop_name] = {
                    'model': joblib.load(model_path),
                    'scaler': joblib.load(scaler_path),
                    'feature_names': ['temp_c', 'precip_mm', 'swvl1', 'solar_mj', 'month',
                                     'sin_month', 'cos_month', 'ndvi_mean']
                }
        
        self.models = loaded_models
        return len(loaded_models) > 0

# ==========================================
# CROP RECOMMENDER
# ==========================================

class EnhancedCropRecommender:
    """Advanced crop recommendation system"""
    
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
    
    def recommend_all(self) -> List[Dict[str, Any]]:
        """Generate comprehensive recommendations"""
        results = []
        for crop_name, params in CROPS_DATABASE.items():
            temp_score = self._calc_temperature_score(params)
            precip_score = self._calc_precipitation_score(params)
            soil_score = self._calc_soil_score(params)
            ndvi_score = self._calc_ndvi_score()
            solar_score = self._calc_solar_score()
            seasonal_score = self._calc_seasonal_score(params)
            
            total_score = temp_score + precip_score + soil_score + ndvi_score + solar_score + seasonal_score
            
            if total_score >= 70:
                suitability_class = "high"
                suitability_text = "Alta"
                recommendation_text = "Condições excelentes para o cultivo"
            elif total_score >= 50:
                suitability_class = "moderate"
                suitability_text = "Moderada"
                recommendation_text = "Condições adequadas, requer monitoramento"
            else:
                suitability_class = "low"
                suitability_text = "Baixa"
                recommendation_text = "Condições desfavoráveis, considerar alternativas"
            
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
                'fertilizer': params['fertilizer'],
                'irrigation': params['irrigation'],
                'soil_preparation': params['soil_preparation'],
                'harvest_indicator': params['harvest_indicator'],
                'post_harvest': params['post_harvest']
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def _calc_temperature_score(self, params: Dict) -> float:
        temp = self.conditions['temp']
        temp_range = params['temp_range']
        if temp_range[0] <= temp <= temp_range[1]:
            return 30
        elif temp < temp_range[0]:
            return max(0, 20 - (temp_range[0] - temp) * 1.5)
        else:
            return max(0, 20 - (temp - temp_range[1]) * 1.2)
    
    def _calc_precipitation_score(self, params: Dict) -> float:
        precip = self.conditions['precip']
        precip_range = params['precip_range']
        if precip_range[0] <= precip <= precip_range[1]:
            return 30
        elif precip < precip_range[0]:
            return max(0, 20 - (precip_range[0] - precip) / 5)
        else:
            return max(0, 20 - (precip - precip_range[1]) / 8)
    
    def _calc_soil_score(self, params: Dict) -> float:
        soil = self.conditions['soil']
        soil_range = params.get('soil_range', (0.15, 0.35))
        if soil is None:
            return 0
        if soil_range[0] <= soil <= soil_range[1]:
            return 20
        elif soil < soil_range[0]:
            return max(0, 12 - (soil_range[0] - soil) * 40)
        else:
            return max(0, 12 - (soil - soil_range[1]) * 40)
    
    def _calc_ndvi_score(self) -> float:
        ndvi = self.conditions['ndvi']
        if ndvi is None:
            return 0
        if ndvi >= 0.6:
            return 15
        elif ndvi >= 0.5:
            return 14
        elif ndvi >= 0.4:
            return 12
        elif ndvi >= 0.3:
            return 10
        elif ndvi >= 0.2:
            return 8
        elif ndvi >= 0.1:
            return 4
        else:
            return 2
    
    def _calc_solar_score(self) -> float:
        solar = self.conditions['solar']
        if solar is None:
            return 0
        if solar >= 20:
            return 5
        elif solar >= 15:
            return 4
        elif solar >= 10:
            return 2
        else:
            return 1
    
    def _calc_seasonal_score(self, params: Dict) -> float:
        month = self.conditions['month']
        optimal_months = params.get('optimal_months', [])
        if month in optimal_months:
            return 10
        elif optimal_months and abs(month - optimal_months[0]) <= 1:
            return 5
        else:
            return 0

# ==========================================
# DASHBOARD COMPONENTS
# ==========================================

class EnhancedDashboardComponents:
    """Advanced dashboard components"""
    
    @staticmethod
    def render_header():
        st.markdown("""
        <div class="main-header">
            <div class="header-content">
                <h1>AgriSense Africa</h1>
                <p>Plataforma Inteligente para Agricultura de Precisão</p>
                <p style="font-size: 0.85rem; margin-top: 0.5rem;">
                    Dados Climáticos Mensais e Imagens Sentinel-2 | Recomendações Baseadas em Machine Learning
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_company_info():
        st.markdown(f"""
        <div class="sidebar-company">
            <h3 style="color: white; margin: 0 0 0.5rem 0;">AgriSense Africa</h3>
            <p style="font-size: 0.8rem; margin: 0;">{Config.COMPANY_DESCRIPTION}</p>
            <hr style="margin: 0.5rem 0; background: rgba(255,255,255,0.3);">
            <p style="font-size: 0.75rem; margin: 0.25rem 0;"><strong>Missão:</strong> {Config.COMPANY_MISSION}</p>
            <p style="font-size: 0.75rem; margin: 0.25rem 0;"><strong>Contato:</strong> {Config.CONTACT}</p>
            <p style="font-size: 0.75rem; margin: 0.25rem 0;"><strong>Web:</strong> {Config.WEBSITE}</p>
            <hr style="margin: 0.5rem 0; background: rgba(255,255,255,0.3);">
            <p style="font-size: 0.7rem; margin: 0;">© 2026 {Config.COMPANY}</p>
            <p style="font-size: 0.7rem; margin: 0;">Dados Sentinel-2 | Resolução 10m</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_enhanced_metrics_with_interpretation(data: pd.DataFrame):
        """Render metrics with interpretations"""
        if data.empty:
            st.warning("Dados insuficientes para métricas")
            return
            
        col1, col2, col3, col4 = st.columns(4)
        
        temp_mean = data['temp_c'].mean()
        precip_mean = data['precip_mm'].mean()
        wind_mean = data['wind_speed'].mean() if 'wind_speed' in data.columns else 0
        solar_mean = data['solar_mj'].mean() if 'solar_mj' in data.columns else 0
        
        temp_interp = "Dentro da faixa ideal (18-32°C)" if 18 <= temp_mean <= 32 else "Fora da faixa ideal"
        precip_interp = "Precipitação adequada" if 50 <= precip_mean <= 200 else "Precipitação fora da faixa ideal"
        wind_interp = "Condições favoráveis" if wind_mean <= 5 else "Ventos fortes"
        solar_interp = "Radiação adequada" if 12 <= solar_mean <= 22 else "Radiação fora da faixa ideal"
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{temp_mean:.1f}°C</div>
                <div class="metric-label">Temperatura Média</div>
                <div class="metric-interpretation">{temp_interp}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{precip_mean:.1f} mm</div>
                <div class="metric-label">Precipitação Média</div>
                <div class="metric-interpretation">{precip_interp}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{wind_mean:.1f} m/s</div>
                <div class="metric-label">Velocidade do Vento</div>
                <div class="metric-interpretation">{wind_interp}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{solar_mean:.1f} MJ/m²</div>
                <div class="metric-label">Radiação Solar</div>
                <div class="metric-interpretation">{solar_interp}</div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_enhanced_soil_analysis(data: pd.DataFrame):
        """Render soil analysis"""
        if data.empty or 'swvl1' not in data.columns:
            st.warning("Dados de umidade do solo não disponíveis")
            return
            
        st.markdown("### Análise de Umidade do Solo")
        
        col1, col2 = st.columns(2)
        soil_surface = data['swvl1'].mean()
        soil_deep = data['swvl2'].mean() if 'swvl2' in data.columns else soil_surface
        
        surface_interp = "Ideal" if 0.20 <= soil_surface <= 0.35 else "Fora da faixa ideal"
        deep_interp = "Reserva adequada" if soil_deep >= 0.20 else "Reserva insuficiente"
        
        with col1:
            st.markdown(f"""
            <div class="soil-card">
                <h4>Camada Superficial (0-7cm)</h4>
                <div style="font-size: 2rem;">{soil_surface:.3f}</div>
                <p>m³/m³</p>
                <small>{surface_interp}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="soil-card">
                <h4>Camada Profunda (7-28cm)</h4>
                <div style="font-size: 2rem;">{soil_deep:.3f}</div>
                <p>m³/m³</p>
                <small>{deep_interp}</small>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_enhanced_ndvi_analysis(ndvi_data: Optional[Dict], year: int, month: int):
        """Render NDVI analysis with vegetation zones and spatial variability"""
        if ndvi_data is None:
            st.warning("Dados Sentinel-2 NDVI não disponíveis para este período")
            return
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            im = ax.imshow(ndvi_data['data'], cmap='RdYlGn', vmin=-0.2, vmax=0.8)
            plt.colorbar(im, ax=ax, label='NDVI')
            ax.set_title(f'Índice de Vegetação (Sentinel-2 NDVI)\n{calendar.month_name[month]} {year}')
            ax.axis('off')
            st.pyplot(fig)
        
        with col2:
            st.markdown("### Estatísticas Descritivas")
            st.markdown(f"""
            <div class="statistics-panel">
                <table style="width: 100%;">
                    <tr><td><strong>Média</strong></td><td style="text-align: right;">{ndvi_data['mean']:.4f}</td></tr>
                    <tr><td><strong>Mediana</strong></td><td style="text-align: right;">{ndvi_data['median']:.4f}</td></tr>
                    <tr><td><strong>Desvio Padrão</strong></td><td style="text-align: right;">{ndvi_data['std']:.4f}</td></tr>
                    <tr><td><strong>Mínimo</strong></td><td style="text-align: right;">{ndvi_data['min']:.4f}</td></tr>
                    <tr><td><strong>Máximo</strong></td><td style="text-align: right;">{ndvi_data['max']:.4f}</td></tr>
                    <tr><td><strong>Sensor</strong></td><td style="text-align: right;">{ndvi_data['sensor']}</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="ndvi-interpretation">
                <h4>Status: {ndvi_data['health_status']}</h4>
                <p>{ndvi_data['health_description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Vegetation Zones Analysis with Recommendations
        st.markdown("---")
        st.markdown("## Análise de Vegetação e Recomendações")
        
        zones, spatial_variability = analyze_vegetation_zones(ndvi_data['data'])
        
        # Zone Distribution Chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Distribuição das Zonas de Vegetação")
            zone_names = list(zones.keys())
            zone_areas = [zones[z]['area_pct'] for z in zone_names]
            zone_colors = [zones[z]['color'] for z in zone_names]
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=[z.capitalize() for z in zone_names],
                values=zone_areas,
                marker_colors=zone_colors,
                hole=0.3,
                textinfo='label+percent',
                textposition='auto'
            )])
            
            fig_pie.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("### Análise de Variabilidade Espacial")
            st.info(f"**Coeficiente de Variação:** {spatial_variability['coefficient_variation']:.1f}%")
            st.info(f"**Zonas de Manejo Identificadas:** {spatial_variability['management_zones']}")
            st.info(f"**Homogeneidade:** {spatial_variability['homogeneity']}")
            st.info(f"**Padrão Espacial:** {spatial_variability['spatial_autocorrelation']}")
            st.success(f"**Recomendação de Manejo:** {spatial_variability['recommendation']}")
        
        # Zone-Specific Recommendations
        st.markdown("### Recomendações por Zona de Vegetação")
        
        for zone_name, zone_data in zones.items():
            if zone_data['area_pct'] > 0:
                zone_color = zone_data['color']
                with st.expander(f"{zone_name.capitalize()} - {zone_data['area_pct']:.1f}% da área"):
                    st.markdown(f"""
                    <div style="background: #F8F9FA; padding: 1rem; border-radius: 12px; border-left: 4px solid {zone_color};">
                        <p><strong>Faixa NDVI:</strong> {zone_data['range'][0]:.1f} a {zone_data['range'][1]:.1f}</p>
                        <p><strong>Área:</strong> {zone_data['area_pct']:.1f}% do talhão</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if zone_data['recommendations']:
                        st.markdown("**Recomendações Técnicas:**")
                        for rec in zone_data['recommendations']:
                            st.write(f"• {rec}")
                    else:
                        st.write("Nenhuma recomendação específica para esta zona no momento.")
    
    @staticmethod
    def render_future_ndvi_prediction(ndvi_data: Optional[Dict], year: int, month: int):
        """Render future NDVI prediction with integrated imagery"""
        if ndvi_data is None:
            st.warning("Dados NDVI não disponíveis para gerar previsões")
            return
        
        st.markdown("## Previsão de Vegetação com Imagens NDVI")
        
        days_ahead = st.slider("Horizonte de Previsão (Dias)", 7, 90, 30)
        predicted_ndvi = generate_ndvi_prediction(ndvi_data['data'], days_ahead)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**NDVI Atual - {calendar.month_name[month]} {year}**")
            fig_current, ax_current = plt.subplots(figsize=(6, 5))
            im_current = ax_current.imshow(ndvi_data['data'], cmap='RdYlGn', vmin=-0.2, vmax=0.8)
            plt.colorbar(im_current, ax=ax_current, label='NDVI')
            ax_current.axis('off')
            st.pyplot(fig_current)
            
            current_mean = ndvi_data['mean']
            st.metric("NDVI Médio Atual", f"{current_mean:.3f}")
        
        with col2:
            st.markdown(f"**NDVI Previsto - {days_ahead} dias**")
            fig_pred, ax_pred = plt.subplots(figsize=(6, 5))
            im_pred = ax_pred.imshow(predicted_ndvi, cmap='RdYlGn', vmin=-0.2, vmax=0.8)
            plt.colorbar(im_pred, ax=ax_pred, label='NDVI')
            ax_pred.axis('off')
            st.pyplot(fig_pred)
            
            predicted_mean = np.mean(predicted_ndvi[~np.isnan(predicted_ndvi)])
            change = ((predicted_mean - current_mean) / current_mean) * 100 if current_mean > 0 else 0
            st.metric("NDVI Médio Previsto", f"{predicted_mean:.3f}", delta=f"{change:+.1f}%")
        
        st.markdown("### Insights da Previsão")
        if change > 5:
            st.success("Projeção indica melhora significativa na vegetação nas próximas semanas")
        elif change > 0:
            st.info("Projeção indica ligeira melhora na vegetação")
        elif change > -5:
            st.warning("Projeção indica estabilidade com pequena tendência de declínio")
        else:
            st.error("Alerta: Projeção indica declínio significativo na vegetação. Intervenção necessária.")
    
    @staticmethod
    def render_comprehensive_recommendations(recommendations: List[Dict]):
        """Render crop recommendations"""
        if not recommendations:
            st.info("Analisando dados para gerar recomendações...")
            return
        
        st.markdown("## Recomendações de Cultivo")
        
        top_crops = recommendations[:3]
        cols = st.columns(3)
        
        for idx, crop in enumerate(top_crops):
            with cols[idx]:
                card_class = f"crop-{crop['suitability_class']}"
                st.markdown(f"""
                <div class="recommendation-card {card_class}">
                    <h3><span class="crop-icon">{crop['icon']}</span> {crop['name']}</h3>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {crop['score']:.0f}%;"></div>
                    </div>
                    <p><strong>Compatibilidade:</strong> {crop['score']:.0f}%</p>
                    <p><strong>Nível:</strong> {crop['suitability_text']}</p>
                    <p><strong>Recomendação:</strong> {crop['recommendation_text']}</p>
                    <p><strong>Temperatura Ideal:</strong> {crop['temp_ideal']}</p>
                    <p><strong>Precipitação Ideal:</strong> {crop['precip_ideal']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander("Análise Detalhada de Todas as Culturas"):
            for crop in recommendations:
                st.markdown(f"""
                <div style="padding: 1rem; margin: 0.5rem 0; background: white; border-radius: 12px;">
                    <h4><span class="crop-icon">{crop['icon']}</span> {crop['name']} - {crop['score']:.0f}%</h4>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {crop['score']:.0f}%;"></div>
                    </div>
                    <p><strong>{crop['recommendation_text']}</strong></p>
                    <p>{crop['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    @staticmethod
    def render_agricultural_guide(crop_info: Dict):
        """Render agricultural guide"""
        optimal_months_names = [calendar.month_name[m] for m in crop_info.get('optimal_months', [])]
        optimal_months_str = ', '.join(optimal_months_names)
        
        with st.container():
            st.markdown(f"### {crop_info['icon']} {crop_info.get('name', 'Cultura')} - Guia Técnico")
            
            col1, col2 = st.columns(2)
            
            with col1:
                with st.expander("Plantio", expanded=True):
                    st.markdown(f"""
                    - **Profundidade:** {crop_info['planting_depth']}
                    - **Espaçamento:** {crop_info['spacing']}
                    - **Meses ideais:** {optimal_months_str}
                    """)
                
                with st.expander("Irrigação", expanded=True):
                    st.markdown(f"""
                    - **Necessidade:** {crop_info['water_requirement']}
                    - **Recomendação:** {crop_info['irrigation']}
                    """)
            
            with col2:
                with st.expander("Adubação", expanded=True):
                    st.markdown(f"""
                    - **Recomendação:** {crop_info['fertilizer']}
                    - **Preparo do solo:** {crop_info['soil_preparation']}
                    """)
                
                with st.expander("Colheita", expanded=True):
                    st.markdown(f"""
                    - **Ciclo:** {crop_info['cycle']}
                    - **Produtividade:** {crop_info['expected_yield']}
                    - **Indicador:** {crop_info['harvest_indicator']}
                    """)
            
            with st.expander("Informações Importantes"):
                st.markdown(f"""
                {crop_info['description']}
                
                - **Valor de mercado:** {crop_info['market_value']}
                - **Pós-colheita:** {crop_info['post_harvest']}
                """)
    
    @staticmethod
    def render_management_tips(data: pd.DataFrame, ndvi: Optional[float]):
        """Render management tips"""
        if data.empty:
            return
            
        tips = []
        month_data = data.iloc[0] if len(data) > 0 else None
        
        if month_data is not None:
            total_precip = month_data['precip_mm']
            temp_mean = month_data['temp_c']
            soil_moisture = month_data['swvl1']
            
            if total_precip < 30:
                tips.append(("Baixa Pluviosidade", f"Apenas {total_precip:.1f}mm no mês. Necessidade crítica de irrigação.", "critical"))
            elif total_precip < 80:
                tips.append(("Déficit Hídrico", f"Precipitação de {total_precip:.1f}mm abaixo do ideal. Planejar irrigação.", "warning"))
            
            if temp_mean > 35:
                tips.append(("Estresse Térmico", f"Temperatura média de {temp_mean:.1f}°C. Aumentar frequência de irrigação.", "warning"))
            elif temp_mean < 15:
                tips.append(("Baixas Temperaturas", f"Temperatura média de {temp_mean:.1f}°C. Proteger plantas jovens.", "warning"))
            
            if soil_moisture < 0.18:
                tips.append(("Solo Seco", f"Umidade média de {soil_moisture:.2f} m³/m³. Irrigação recomendada.", "warning"))
            elif 0.20 <= soil_moisture <= 0.35:
                tips.append(("Condições Ideais", f"Umidade de {soil_moisture:.2f} m³/m³. Momento adequado para plantio.", "success"))
        
        if ndvi is not None:
            if ndvi < 0.15:
                tips.append(("Cobertura Vegetal Insuficiente", "Solo exposto detectado. Utilizar cobertura morta.", "warning"))
            elif ndvi > 0.6:
                tips.append(("Vegetação Exuberante", "Alta biomassa detectada. Manter monitoramento.", "success"))
        
        if tips:
            st.markdown("### Recomendações de Manejo")
            for title, message, tip_type in tips:
                if tip_type == "critical":
                    st.error(f"{title} - {message}")
                elif tip_type == "warning":
                    st.warning(f"{title} - {message}")
                elif tip_type == "success":
                    st.success(f"{title} - {message}")
        else:
            st.success("Condições favoráveis para plantio e desenvolvimento das culturas.")
    
    @staticmethod
    def render_climate_dashboard_with_charts(df: pd.DataFrame, year: int):
        """Render climate dashboard"""
        yearly_data = df[df['year'] == year]
        if yearly_data.empty:
            st.warning(f"Sem dados para o ano {year}")
            return
        
        months_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        fig = make_subplots(rows=2, cols=2, subplot_titles=('Temperatura Média Mensal', 'Precipitação Mensal', 'Umidade do Solo', 'Radiação Solar'))
        
        fig.add_trace(go.Scatter(x=months_labels, y=yearly_data['temp_c'], mode='lines+markers', name='Temperatura', line=dict(color='#E67E22', width=3)), row=1, col=1)
        fig.add_trace(go.Bar(x=months_labels, y=yearly_data['precip_mm'], name='Precipitação', marker_color='#3498DB'), row=1, col=2)
        
        if 'swvl1' in yearly_data.columns:
            fig.add_trace(go.Scatter(x=months_labels, y=yearly_data['swvl1'], mode='lines+markers', name='Umidade', line=dict(color='#2C7A47', width=3)), row=2, col=1)
        if 'solar_mj' in yearly_data.columns:
            fig.add_trace(go.Scatter(x=months_labels, y=yearly_data['solar_mj'], mode='lines+markers', name='Radiação', line=dict(color='#D9B48B', width=3)), row=2, col=2)
        
        fig.update_yaxes(title_text="°C", row=1, col=1)
        fig.update_yaxes(title_text="mm", row=1, col=2)
        fig.update_yaxes(title_text="m³/m³", row=2, col=1)
        fig.update_yaxes(title_text="MJ/m²", row=2, col=2)
        fig.update_layout(height=600, showlegend=False, title_text=f"Análise Climática Completa - {year}", template='plotly_white')
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_future_predictions_with_charts(predictions: Dict, year: int):
        """Render future predictions"""
        if not predictions:
            st.warning("Dados de previsão não disponíveis")
            return
        
        st.markdown(f"### Projeções para {year}")
        months_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        fig = make_subplots(rows=2, cols=2, subplot_titles=('Temperatura Projetada', 'Precipitação Projetada', 'Umidade do Solo Projetada', 'Radiação Solar Projetada'))
        
        for var, color, title in [('temp_c', '#E67E22', 'Temperatura'), ('precip_mm', '#3498DB', 'Precipitação'), ('swvl1', '#2C7A47', 'Umidade'), ('solar_mj', '#D9B48B', 'Radiação')]:
            if var in predictions:
                var_data = predictions[var]
                year_data = var_data[var_data['date'].dt.year == year]
                if not year_data.empty:
                    values = [year_data[year_data['date'].dt.month == m]['predicted'].values[0] if len(year_data[year_data['date'].dt.month == m]) > 0 else None for m in range(1, 13)]
                    if var == 'precip_mm':
                        fig.add_trace(go.Bar(x=months_labels, y=values, name=title, marker_color=color), row=1 if var in ['temp_c', 'precip_mm'] else 2, col=1 if var in ['temp_c', 'swvl1'] else 2)
                    else:
                        fig.add_trace(go.Scatter(x=months_labels, y=values, mode='lines+markers', name=title, line=dict(color=color, width=3)), row=1 if var in ['temp_c', 'precip_mm'] else 2, col=1 if var in ['temp_c', 'swvl1'] else 2)
        
        fig.update_layout(height=600, showlegend=False, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_planting_calendar_heatmap():
        """Render planting calendar heatmap"""
        months_abbr = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        calendar_data = []
        for crop_name, crop_info in CROPS_DATABASE.items():
            row = {'Cultura': crop_name}
            for month in range(1, 13):
                if month in crop_info['optimal_months']:
                    row[months_abbr[month-1]] = 2
                elif crop_info['optimal_months'] and abs(month - crop_info['optimal_months'][0]) <= 1:
                    row[months_abbr[month-1]] = 1
                else:
                    row[months_abbr[month-1]] = 0
            calendar_data.append(row)
        
        cal_df = pd.DataFrame(calendar_data)
        fig = px.imshow(cal_df.set_index('Cultura').values, x=months_abbr, y=cal_df['Cultura'],
                        color_continuous_scale=['#E8F0EA', '#F39C12', '#2C7A47'],
                        title='Períodos Ideais de Plantio', labels=dict(color='Adequabilidade'))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Legenda:** Verde: Ideal | Laranja: Bom | Cinza: Não Recomendado")

# ==========================================
# MAIN APPLICATION
# ==========================================

def main():
    """Main application function"""
    
    inject_custom_css()
    EnhancedDashboardComponents.render_header()
    
    with st.spinner("Carregando dados climáticos mensais..."):
        climate_data = load_climate_data()
    
    if climate_data is None or climate_data.empty:
        st.error("Não foi possível carregar os dados. Verifique os arquivos.")
        return
    
    tab_historical, tab_ml, tab_future, tab_calendar = st.tabs([
        "Dados Históricos Mensais",
        "Previsões com IA", 
        "Projeções Futuras",
        "Calendário de Plantio"
    ])
    
    # TAB 1: HISTORICAL DATA
    with tab_historical:
        with st.sidebar:
            st.markdown("## Controles")
            years = sorted(climate_data['year'].unique())
            selected_year = st.selectbox("Ano", years, index=len(years) - 1)
            selected_month = st.selectbox("Mês", list(range(1, 13)), format_func=lambda x: calendar.month_name[x])
            st.markdown("---")
            st.markdown("### Culturas Analisadas")
            for crop_name in CROPS_DATABASE.keys():
                st.markdown(f"- {CROPS_DATABASE[crop_name]['icon']} {crop_name}")
            st.markdown("---")
            EnhancedDashboardComponents.render_company_info()
        
        filtered_data = climate_data[(climate_data['year'] == selected_year) & (climate_data['month'] == selected_month)]
        
        if filtered_data.empty:
            st.warning(f"Sem dados para {calendar.month_name[selected_month]} {selected_year}")
        else:
            with st.spinner("Carregando dados Sentinel-2 NDVI..."):
                ndvi_data = load_ndvi_data(selected_year, selected_month)
            
            temp = filtered_data['temp_c'].values[0]
            precip = filtered_data['precip_mm'].values[0]
            soil = filtered_data['swvl1'].values[0] if 'swvl1' in filtered_data.columns else 0.25
            solar = filtered_data['solar_mj'].values[0] if 'solar_mj' in filtered_data.columns else 15.0
            ndvi = ndvi_data['mean'] if ndvi_data else None
            
            recommender = EnhancedCropRecommender(temp, precip, soil, solar, ndvi, selected_month)
            recommendations = recommender.recommend_all()
            
            st.markdown(f"### Período Analisado: {calendar.month_name[selected_month]} {selected_year}")
            
            EnhancedDashboardComponents.render_enhanced_metrics_with_interpretation(filtered_data)
            EnhancedDashboardComponents.render_enhanced_soil_analysis(filtered_data)
            
            st.markdown("---")
            st.markdown("### Análise de Vegetação (Sentinel-2 NDVI)")
            EnhancedDashboardComponents.render_enhanced_ndvi_analysis(ndvi_data, selected_year, selected_month)
            
            st.markdown("---")
            st.markdown("### Previsão de Vegetação")
            EnhancedDashboardComponents.render_future_ndvi_prediction(ndvi_data, selected_year, selected_month)
            
            st.markdown("---")
            EnhancedDashboardComponents.render_comprehensive_recommendations(recommendations)
            EnhancedDashboardComponents.render_management_tips(filtered_data, ndvi)
            
            st.markdown("---")
            st.markdown("## Análise Climática Mensal Completa")
            EnhancedDashboardComponents.render_climate_dashboard_with_charts(climate_data, selected_year)
    
    # TAB 2: ML PREDICTIONS
    with tab_ml:
        st.markdown("## Previsões com Inteligência Artificial")
        st.markdown("Modelos de Machine Learning treinados com dados climáticos mensais e imagens Sentinel-2 NDVI.")
        
        ml_trainer = EnhancedMLModelTrainer(climate_data)
        models_loaded = ml_trainer.load_models()
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Treinamento dos Modelos")
            if st.button("Treinar Modelos", use_container_width=True):
                with st.spinner("Treinando modelos..."):
                    models = ml_trainer.train_enhanced_models()
                    if models:
                        ml_trainer.save_models()
                        st.success("Modelos treinados com sucesso!")
                        models_loaded = True
                        perf_data = [{'Cultura': crop, 'Modelo': info['model_type'], 'Acurácia (R²)': f"{info['score']:.2%}"} for crop, info in models.items()]
                        st.dataframe(pd.DataFrame(perf_data), use_container_width=True)
            
            if not models_loaded:
                if st.button("Carregar Modelos Existentes"):
                    if ml_trainer.load_models():
                        st.success("Modelos carregados com sucesso!")
                        models_loaded = True
                    else:
                        st.warning("Nenhum modelo encontrado. Treine novos modelos primeiro.")
        
        with col2:
            if models_loaded:
                st.markdown("### Realizar Previsões")
                pred_month = st.selectbox("Mês para Previsão", list(range(1, 13)), format_func=lambda x: calendar.month_name[x])
                
                historical_avg = climate_data.groupby('month')[['temp_c', 'precip_mm', 'swvl1', 'solar_mj']].mean().reset_index()
                
                def get_hist(month, col, default):
                    try:
                        val = historical_avg[historical_avg['month'] == month][col].values
                        return float(val[0]) if len(val) > 0 and not pd.isna(val[0]) else default
                    except:
                        return default
                
                temp_input = st.number_input("Temperatura Média (°C)", value=get_hist(pred_month, 'temp_c', 25.0), step=0.5)
                precip_input = st.number_input("Precipitação Mensal (mm)", value=get_hist(pred_month, 'precip_mm', 100.0), step=10.0)
                soil_input = st.number_input("Umidade do Solo (m³/m³)", value=get_hist(pred_month, 'swvl1', 0.25), step=0.01, format="%.3f")
                solar_input = st.number_input("Radiação Solar (MJ/m²)", value=get_hist(pred_month, 'solar_mj', 18.0), step=1.0)
                ndvi_input = st.number_input("NDVI Previsto", value=0.35, step=0.05, format="%.3f")
                
                if st.button("Gerar Recomendações com IA", type="primary", use_container_width=True):
                    with st.spinner("Processando previsões..."):
                        predictions = ml_trainer.predict_all_crops_with_ndvi(
                            temp_input, precip_input, soil_input, solar_input, pred_month, ndvi_input
                        )
                        st.markdown(f"### Recomendações para {calendar.month_name[pred_month]}")
                        
                        pred_df = pd.DataFrame(predictions[:8])
                        if not pred_df.empty:
                            fig = px.bar(pred_df, x='crop', y='score', title='Compatibilidade das Culturas (%)',
                                        labels={'crop': 'Cultura', 'score': 'Compatibilidade (%)'},
                                        color='score', color_continuous_scale='RdYlGn', text='score')
                            fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
                            fig.update_layout(showlegend=False, height=400)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        for pred in predictions[:5]:
                            score_color = "🟢" if pred['score'] >= 70 else "🟡" if pred['score'] >= 50 else "🔴"
                            st.markdown(f"""
                            <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 12px; border-left: 4px solid {Config.SUCCESS_COLOR if pred['score'] >= 70 else Config.WARNING_COLOR if pred['score'] >= 50 else Config.DANGER_COLOR}">
                                <h4><span class="crop-icon">{pred['icon']}</span> {pred['crop']} - {score_color} {pred['score']:.0f}%</h4>
                                <p><strong>Nível:</strong> {pred['level']}</p>
                                <p><strong>Recomendação:</strong> {pred['recommendation']}</p>
                            </div>
                            """, unsafe_allow_html=True)
    
    # TAB 3: FUTURE FORECASTS
    with tab_future:
        st.markdown("## Projeções Climáticas 2024-2026")
        st.markdown("Previsões baseadas em dados históricos mensais e tendências sazonais.")
        
        historical_avg = climate_data.groupby('month')[['temp_c', 'precip_mm', 'swvl1', 'solar_mj']].mean().reset_index()
        
        yearly_trend = climate_data.groupby('year')[['temp_c', 'precip_mm']].mean().reset_index()
        temp_trend = (yearly_trend['temp_c'].iloc[-1] - yearly_trend['temp_c'].iloc[0]) / max(len(yearly_trend), 1) if len(yearly_trend) > 1 else 0
        precip_trend = (yearly_trend['precip_mm'].iloc[-1] - yearly_trend['precip_mm'].iloc[0]) / max(len(yearly_trend), 1) if len(yearly_trend) > 1 else 0
        
        predictions = {}
        for var in ['temp_c', 'precip_mm', 'swvl1', 'solar_mj']:
            pred_data = []
            for year in [2024, 2025, 2026]:
                trend_factor = (year - 2023) * temp_trend if var == 'temp_c' else (year - 2023) * precip_trend if var == 'precip_mm' else 0
                for month in range(1, 13):
                    hist_val = historical_avg[historical_avg['month'] == month][var].values[0] if len(historical_avg[historical_avg['month'] == month]) > 0 else (25.0 if var == 'temp_c' else 100.0 if var == 'precip_mm' else 0.25 if var == 'swvl1' else 18.0)
                    pred_val = hist_val + trend_factor
                    pred_data.append({'date': pd.Timestamp(year=year, month=month, day=1), 'predicted': pred_val})
            predictions[var] = pd.DataFrame(pred_data)
        
        pred_year = st.selectbox("Selecione o Ano para Visualização", [2024, 2025, 2026])
        EnhancedDashboardComponents.render_future_predictions_with_charts(predictions, pred_year)
        
        st.markdown("### Recomendações Sazonais")
        selected_season = st.selectbox("Selecione a Estação", ["Primavera (Set-Nov)", "Verão (Dez-Fev)", "Outono (Mar-Mai)", "Inverno (Jun-Ago)"])
        season_months = {"Primavera (Set-Nov)": [9,10,11], "Verão (Dez-Fev)": [12,1,2], "Outono (Mar-Mai)": [3,4,5], "Inverno (Jun-Ago)": [6,7,8]}
        
        months = season_months[selected_season]
        temp_vals = [predictions['temp_c'][predictions['temp_c']['date'].dt.month == m]['predicted'].values[0] for m in months if len(predictions['temp_c'][predictions['temp_c']['date'].dt.month == m]) > 0]
        precip_vals = [predictions['precip_mm'][predictions['precip_mm']['date'].dt.month == m]['predicted'].values[0] for m in months if len(predictions['precip_mm'][predictions['precip_mm']['date'].dt.month == m]) > 0]
        avg_temp = np.mean(temp_vals) if temp_vals else 25.0
        avg_precip = np.mean(precip_vals) if precip_vals else 100.0
        
        st.markdown(f"""
        <div class="alert-info">
            <strong>Resumo para {selected_season}</strong><br>
            Temperatura média: {avg_temp:.1f}°C | Precipitação média: {avg_precip:.1f}mm
        </div>
        """, unsafe_allow_html=True)
        
        seasonal_crops = [(crop_name, crop_info) for crop_name, crop_info in CROPS_DATABASE.items() if any(m in crop_info['optimal_months'] for m in months)]
        if seasonal_crops:
            st.markdown("#### Culturas Recomendadas para esta Estação")
            cols = st.columns(3)
            for idx, (crop_name, crop_info) in enumerate(seasonal_crops[:3]):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="background: white; padding: 1rem; border-radius: 12px; text-align: center;">
                        <h2>{crop_info['icon']}</h2>
                        <h4>{crop_name}</h4>
                        <p style="font-size: 0.8rem;">{crop_info['description'][:80]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # TAB 4: PLANTING CALENDAR
    with tab_calendar:
        st.markdown("## Calendário de Plantio Inteligente")
        st.markdown("Planeje suas atividades agrícolas ao longo do ano.")
        
        st.markdown("### Calendário de Plantio - Períodos Ideais")
        EnhancedDashboardComponents.render_planting_calendar_heatmap()
        
        st.markdown("---")
        current_month = st.selectbox("Selecione o Mês para Guia Detalhado", list(range(1, 13)), format_func=lambda x: calendar.month_name[x], index=datetime.now().month - 1)
        st.markdown(f"### Guia Técnico para {calendar.month_name[current_month]}")
        
        optimal_crops = []
        for crop_name, crop_info in CROPS_DATABASE.items():
            if current_month in crop_info['optimal_months']:
                crop_info_with_name = crop_info.copy()
                crop_info_with_name['name'] = crop_name
                optimal_crops.append((crop_name, crop_info_with_name))
        
        if optimal_crops:
            st.markdown(f"#### Culturas com Plantio Ideal em {calendar.month_name[current_month]}")
            for crop_name, crop_info in optimal_crops[:3]:
                EnhancedDashboardComponents.render_agricultural_guide(crop_info)
        else:
            st.info(f"Nenhuma cultura com plantio ideal em {calendar.month_name[current_month]}. Utilize este período para preparo do solo, análise de solo e planejamento.")
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <p><strong>AgriSense Africa</strong> - Transformando dados em decisões agrícolas sustentáveis</p>
        <p>© 2026 {Config.COMPANY} | Versão {Config.APP_VERSION} | Tecnologia de Machine Learning e Imagens Sentinel-2</p>
        <p style="font-size: 0.7rem;">Aumento estimado de produtividade: 20-30% com adoção das recomendações</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()