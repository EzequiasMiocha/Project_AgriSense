# ==========================================
# AGRISENSE AFRICA - PROFESSIONAL AGRICULTURAL INTELLIGENCE PLATFORM
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
# CONFIGURAÇÃO GLOBAL
# ==========================================

# Configuração da página
st.set_page_config(
    page_title="AgriSense Africa | Plataforma Agrícola Inteligente",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "AgriSense Africa - Plataforma Inteligente para Agricultura Sustentável"
    }
)

# Constantes
class Config:
    """Configurações globais da aplicação"""
    APP_NAME = "AgriSense Africa"
    APP_VERSION = "1.0.0"
    COMPANY = "AgriSense Intelligence"
    
    # Caminhos dos dados
    CLIMATE_FILE = "Dados_clima_2018_2023.csv"
    NDVI_FOLDER = "ndvi"
    HEADER_IMAGE = "WhatsApp Image 2026-02-17 at 11.37.47.jpeg"
    
    # Limites para validação
    TEMP_MIN = -10
    TEMP_MAX = 50
    PRECIP_MAX = 500
    SOIL_MOISTURE_MAX = 0.6
    
    # Nova paleta de cores profissional
    PRIMARY_COLOR = "#1A4D3E"      # Verde musgo profundo
    SECONDARY_COLOR = "#D9B48B"    # Bege terroso
    ACCENT_COLOR = "#E67E22"       # Laranja terracota
    DANGER_COLOR = "#C44536"       # Terracota queimado
    SUCCESS_COLOR = "#2C7A47"      # Verde folha
    WARNING_COLOR = "#E67E22"      # Laranja terracota
    INFO_COLOR = "#3498DB"         # Azul suave
    BACKGROUND_LIGHT = "#FDF8F0"   # Off-white cremoso
    BACKGROUND_DARK = "#2C3E2F"    # Verde muito escuro
    TEXT_DARK = "#2C3E2F"          # Cor de texto principal
    TEXT_LIGHT = "#FDF8F0"         # Cor de texto claro
    
    # Gradientes
    GRADIENT_HEADER = f"linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SUCCESS_COLOR} 100%)"
    GRADIENT_CARD = "linear-gradient(135deg, #FFFFFF 0%, #FDF8F0 100%)"
    GRADIENT_SOIL = f"linear-gradient(135deg, {PRIMARY_COLOR} 0%, {BACKGROUND_DARK} 100%)"
    
    # Configurações de cache
    CACHE_TTL = 3600

# ==========================================
# ESTILOS CSS PROFISSIONAIS
# ==========================================

def inject_custom_css():
    """Injeta estilos CSS personalizados"""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{
            font-family: 'Inter', sans-serif;
        }}
        
        .stApp {{
            background-color: {Config.BACKGROUND_LIGHT};
        }}
        
        /* Header com imagem */
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
        
        /* Cards de métricas */
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
        
        /* Cards de recomendação */
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
        
        /* Barra de progresso */
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
        
        /* Cards de solo */
        .soil-card {{
            background: {Config.GRADIENT_SOIL};
            padding: 1rem;
            border-radius: 16px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        /* Boxes informativas */
        .info-box, .success-box, .warning-box {{
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left-width: 4px;
            border-left-style: solid;
        }}
        
        .info-box {{
            background: rgba(52, 152, 219, 0.08);
            border-left-color: {Config.INFO_COLOR};
        }}
        
        .success-box {{
            background: rgba(44, 122, 71, 0.08);
            border-left-color: {Config.SUCCESS_COLOR};
        }}
        
        .warning-box {{
            background: rgba(230, 126, 34, 0.08);
            border-left-color: {Config.WARNING_COLOR};
        }}
        
        /* Footer */
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
        
        /* Títulos */
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
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {Config.TEXT_LIGHT};
            border-right: 1px solid rgba(217, 180, 139, 0.2);
        }}
        
        /* Botões */
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
        
        /* Scrollbar */
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
        
        /* Tabs */
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

# ==========================================
# GERENCIAMENTO DE DADOS
# ==========================================

@st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
def load_climate_data() -> Optional[pd.DataFrame]:
    """Carrega e processa dados climáticos"""
    try:
        if not os.path.exists(Config.CLIMATE_FILE):
            st.error(f"Arquivo {Config.CLIMATE_FILE} não encontrado")
            return None
        
        df = pd.read_csv(Config.CLIMATE_FILE)
        
        required_cols = ['valid_time', 't2m', 'tp', 'u10', 'v10', 'ssrd', 'swvl1', 'swvl2']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Colunas ausentes: {missing_cols}")
            return None
        
        df['valid_time'] = pd.to_datetime(df['valid_time'])
        df['year'] = df['valid_time'].dt.year
        df['month'] = df['valid_time'].dt.month
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
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

@st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
def load_ndvi_data(year: int, month: int) -> Optional[Dict[str, Any]]:
    """Carrega dados NDVI"""
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
        st.warning(f"Erro ao ler NDVI: {str(e)}")
        return None

# ==========================================
# SISTEMA DE RECOMENDAÇÃO
# ==========================================

class CropRecommender:
    """Sistema de recomendação de culturas"""
    
    CROPS_DATABASE = {
        'Milho': {
            'icon': '🌽',
            'temp_range': (20, 30),
            'precip_range': (80, 150),
            'soil_range': (0.20, 0.35),
            'optimal_months': [10, 11, 12],
            'description': 'Cereal de alto valor nutritivo, boa para consumo e comercialização.',
            'planting_depth': '3-5 cm',
            'spacing': '80 x 40 cm',
            'cycle': '90-120 dias',
            'expected_yield': '3-5 ton/ha',
            'water_requirement': 'Moderado',
            'market_value': 'Alto'
        },
        'Arroz': {
            'icon': '🌾',
            'temp_range': (22, 32),
            'precip_range': (150, 250),
            'soil_range': (0.30, 0.45),
            'optimal_months': [11, 12, 1, 2],
            'description': 'Cereal básico, alta demanda no mercado.',
            'planting_depth': '2-3 cm',
            'spacing': '25 x 25 cm',
            'cycle': '120-150 dias',
            'expected_yield': '4-6 ton/ha',
            'water_requirement': 'Alto',
            'market_value': 'Muito Alto'
        },
        'Feijão Nhemba': {
            'icon': '🫘',
            'temp_range': (20, 35),
            'precip_range': (60, 120),
            'soil_range': (0.15, 0.30),
            'optimal_months': [11, 12, 1],
            'description': 'Leguminosa rica em proteína, fixa nitrogênio no solo.',
            'planting_depth': '3-4 cm',
            'spacing': '50 x 20 cm',
            'cycle': '70-90 dias',
            'expected_yield': '1-2 ton/ha',
            'water_requirement': 'Baixo',
            'market_value': 'Alto'
        },
        'Mandioca': {
            'icon': '🌿',
            'temp_range': (18, 35),
            'precip_range': (100, 200),
            'soil_range': (0.15, 0.35),
            'optimal_months': [10, 11, 12, 1, 2],
            'description': 'Raiz resistente à seca, segurança alimentar.',
            'planting_depth': '5-8 cm',
            'spacing': '100 x 80 cm',
            'cycle': '240-360 dias',
            'expected_yield': '15-25 ton/ha',
            'water_requirement': 'Baixo',
            'market_value': 'Médio'
        },
        'Algodão': {
            'icon': '🧶',
            'temp_range': (20, 35),
            'precip_range': (70, 130),
            'soil_range': (0.20, 0.35),
            'optimal_months': [10, 11, 12],
            'description': 'Cultura comercial de alta rentabilidade.',
            'planting_depth': '2-3 cm',
            'spacing': '80 x 40 cm',
            'cycle': '140-180 dias',
            'expected_yield': '2-3 ton/ha',
            'water_requirement': 'Moderado',
            'market_value': 'Muito Alto'
        },
        'Amendoim': {
            'icon': '🥜',
            'temp_range': (22, 32),
            'precip_range': (80, 150),
            'soil_range': (0.15, 0.30),
            'optimal_months': [11, 12, 1],
            'description': 'Leguminosa oleaginosa, boa para rotação.',
            'planting_depth': '3-5 cm',
            'spacing': '60 x 20 cm',
            'cycle': '100-120 dias',
            'expected_yield': '1.5-2.5 ton/ha',
            'water_requirement': 'Baixo',
            'market_value': 'Alto'
        },
        'Batata Doce': {
            'icon': '🍠',
            'temp_range': (18, 30),
            'precip_range': (70, 150),
            'soil_range': (0.15, 0.35),
            'optimal_months': [11, 12, 1, 2],
            'description': 'Raiz nutritiva, boa para consumo e comercialização.',
            'planting_depth': '3-5 cm',
            'spacing': '80 x 30 cm',
            'cycle': '90-120 dias',
            'expected_yield': '10-15 ton/ha',
            'water_requirement': 'Moderado',
            'market_value': 'Médio'
        },
        'Tomate': {
            'icon': '🍅',
            'temp_range': (18, 28),
            'precip_range': (80, 120),
            'soil_range': (0.25, 0.40),
            'optimal_months': [4, 5, 6, 7],
            'description': 'Hortaliça de alta demanda, boa rentabilidade.',
            'planting_depth': '1-2 cm',
            'spacing': '100 x 50 cm',
            'cycle': '90-120 dias',
            'expected_yield': '40-60 ton/ha',
            'water_requirement': 'Alto',
            'market_value': 'Muito Alto'
        },
        'Cebola': {
            'icon': '🧅',
            'temp_range': (15, 28),
            'precip_range': (60, 100),
            'soil_range': (0.20, 0.35),
            'optimal_months': [5, 6, 7, 8],
            'description': 'Hortaliça de alto valor comercial.',
            'planting_depth': '1-2 cm',
            'spacing': '30 x 10 cm',
            'cycle': '120-150 dias',
            'expected_yield': '20-30 ton/ha',
            'water_requirement': 'Moderado',
            'market_value': 'Alto'
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
            return 30, f"Temperatura ideal: {temp:.1f}°C"
        elif temp < temp_range[0]:
            diff = temp_range[0] - temp
            score = max(0, 20 - diff * 1.5)
            return score, f"Temperatura {temp:.1f}°C abaixo do ideal ({temp_range[0]}-{temp_range[1]}°C)"
        else:
            diff = temp - temp_range[1]
            score = max(0, 20 - diff * 1.2)
            return score, f"Temperatura {temp:.1f}°C acima do ideal ({temp_range[0]}-{temp_range[1]}°C)"
    
    def _calculate_precipitation_score(self, crop_params: Dict) -> Tuple[float, str]:
        precip = self.conditions['precip']
        precip_range = crop_params['precip_range']
        
        if precip_range[0] <= precip <= precip_range[1]:
            return 30, f"Precipitação ideal: {precip:.1f}mm"
        elif precip < precip_range[0]:
            diff = precip_range[0] - precip
            score = max(0, 20 - diff / 5)
            return score, f"Precipitação {precip:.1f}mm abaixo do necessário ({precip_range[0]}-{precip_range[1]}mm)"
        else:
            diff = precip - precip_range[1]
            score = max(0, 20 - diff / 8)
            return score, f"Precipitação {precip:.1f}mm acima do recomendado ({precip_range[0]}-{precip_range[1]}mm)"
    
    def _calculate_soil_score(self, crop_params: Dict) -> Tuple[float, str]:
        soil = self.conditions['soil']
        soil_range = crop_params.get('soil_range', (0.15, 0.35))
        
        if soil is None:
            return 0, "Dados de solo não disponíveis"
        
        if soil_range[0] <= soil <= soil_range[1]:
            return 20, f"Humidade do solo ideal: {soil:.2f}"
        elif soil < soil_range[0]:
            diff = soil_range[0] - soil
            score = max(0, 12 - diff * 40)
            return score, f"Solo seco: {soil:.2f} (ideal >{soil_range[0]:.2f})"
        else:
            diff = soil - soil_range[1]
            score = max(0, 12 - diff * 40)
            return score, f"Solo encharcado: {soil:.2f} (ideal <{soil_range[1]:.2f})"
    
    def _calculate_ndvi_score(self) -> Tuple[float, str]:
        ndvi = self.conditions['ndvi']
        
        if ndvi is None:
            return 0, "Dados NDVI não disponíveis"
        
        if ndvi >= 0.5:
            return 15, f"NDVI excelente ({ndvi:.2f}) - Vegetação densa e saudável"
        elif ndvi >= 0.3:
            return 12, f"NDVI bom ({ndvi:.2f}) - Boa cobertura vegetal"
        elif ndvi >= 0.2:
            return 8, f"NDVI moderado ({ndvi:.2f}) - Vegetação em desenvolvimento"
        elif ndvi >= 0.1:
            return 4, f"NDVI baixo ({ndvi:.2f}) - Vegetação esparsa"
        else:
            return 2, f"NDVI muito baixo ({ndvi:.2f}) - Solo exposto"
    
    def _calculate_solar_score(self) -> Tuple[float, str]:
        solar = self.conditions['solar']
        
        if solar is None:
            return 0, "Dados de radiação não disponíveis"
        
        if solar >= 20:
            return 5, f"Radiação solar excelente: {solar:.1f} MJ/m²"
        elif solar >= 15:
            return 4, f"Boa radiação solar: {solar:.1f} MJ/m²"
        elif solar >= 10:
            return 2, f"Radiação moderada: {solar:.1f} MJ/m²"
        else:
            return 1, f"Baixa radiação: {solar:.1f} MJ/m²"
    
    def _calculate_seasonal_score(self, crop_params: Dict) -> Tuple[float, str]:
        month = self.conditions['month']
        optimal_months = crop_params.get('optimal_months', [])
        
        if month in optimal_months:
            return 10, f"Mês ideal para plantio ({calendar.month_name[month]})"
        elif optimal_months and abs(month - optimal_months[0]) <= 1:
            return 5, f"Período próximo ao ideal ({calendar.month_name[month]})"
        else:
            return 0, f"Mês não ideal para plantio"
    
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
                suitability_text = "Alta"
                recommendation_text = "Condições excelentes para esta cultura"
            elif total_score >= 50:
                suitability_class = "moderate"
                suitability_text = "Moderada"
                recommendation_text = "Condições adequadas, monitorar desenvolvimento"
            else:
                suitability_class = "low"
                suitability_text = "Baixa"
                recommendation_text = "Condições desfavoráveis, considere alternativas"
            
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

# ==========================================
# COMPONENTES DE VISUALIZAÇÃO
# ==========================================

class DashboardComponents:
    """Componentes reutilizáveis do dashboard"""
    
    @staticmethod
    def render_header():
        """Renderiza o cabeçalho com imagem"""
        # Verificar se a imagem existe
        if os.path.exists(Config.HEADER_IMAGE):
            st.markdown(f"""
            <div class="main-header">
                <img src="data:image/jpeg;base64,{DashboardComponents._get_image_base64(Config.HEADER_IMAGE)}" class="header-logo">
                <div class="header-content">
                    <h1>AgriSense Africa</h1>
                    <p>Plataforma Inteligente para Recomendação de Culturas</p>
                    <div class="header-tagline">Turning Farm Data into Better Harvests</div>
                    <p style="font-size: 0.8rem; margin-top: 0.5rem;">Versão {Config.APP_VERSION} | {Config.COMPANY}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="main-header">
                <div class="header-content">
                    <h1>🌾 AgriSense Africa</h1>
                    <p>Plataforma Inteligente para Recomendação de Culturas</p>
                    <div class="header-tagline">Turning Farm Data into Better Harvests</div>
                    <p style="font-size: 0.8rem; margin-top: 0.5rem;">Versão {Config.APP_VERSION} | {Config.COMPANY}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def _get_image_base64(image_path):
        """Converte imagem para base64"""
        import base64
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    
    @staticmethod
    def render_metrics(data: pd.DataFrame):
        """Renderiza métricas principais"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="Temperatura",
                value=f"{data['temp_c'].mean():.1f}°C",
                delta=f"{data['temp_c'].mean() - data['temp_c'].shift(12).mean():.1f}°C" if len(data) > 12 else None
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="Precipitação",
                value=f"{data['precip_mm'].mean():.1f} mm",
                delta=None
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="Velocidade do Vento",
                value=f"{data['wind_speed'].mean():.1f} m/s",
                delta=None
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="Radiação Solar",
                value=f"{data['solar_mj'].mean():.1f} MJ/m²",
                delta=None
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_soil_analysis(data: pd.DataFrame):
        """Renderiza análise de solo"""
        st.markdown("### Análise da Umidade do Solo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="soil-card">
                <h4 style="color: white;">Camada Superficial</h4>
                <div class="big-metric">{data['swvl1'].mean():.3f}</div>
                <p>m³/m³ (0-7cm)</p>
                <small>Umidade na camada superficial</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="soil-card">
                <h4 style="color: white;">Camada Profunda</h4>
                <div class="big-metric">{data['swvl2'].mean():.3f}</div>
                <p>m³/m³ (7-28cm)</p>
                <small>Umidade na camada de raízes</small>
            </div>
            """, unsafe_allow_html=True)
        
        layer1 = data['swvl1'].mean()
        layer2 = data['swvl2'].mean()
        
        if layer2 > layer1:
            st.success("Boa infiltração: Água penetrando nas camadas mais profundas")
        elif layer1 > layer2 + 0.05:
            st.warning("Drenagem comprometida: Água acumulada na superfície")
        else:
            st.info("Perfil uniforme: Humidade equilibrada no perfil do solo")
    
    @staticmethod
    def render_ndvi_analysis(ndvi_data: Optional[Dict], year: int, month: int):
        """Renderiza análise NDVI"""
        if ndvi_data is None:
            st.warning("Dados NDVI não disponíveis para este período")
            return
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            im = ax.imshow(ndvi_data['data'], cmap='RdYlGn', vmin=-0.2, vmax=0.8)
            plt.colorbar(im, ax=ax, label='NDVI', fraction=0.046, pad=0.04)
            ax.set_title(f'Índice de Vegetação NDVI\n{calendar.month_name[month]} {year}', 
                        fontsize=12, fontweight='bold', color=Config.TEXT_DARK)
            ax.axis('off')
            st.pyplot(fig)
        
        with col2:
            st.markdown("### Estatísticas")
            st.metric("Valor Médio", f"{ndvi_data['mean']:.4f}")
            st.metric("Desvio Padrão", f"{ndvi_data['std']:.4f}")
            st.metric("Mínimo", f"{ndvi_data['min']:.4f}")
            st.metric("Máximo", f"{ndvi_data['max']:.4f}")
            
            st.markdown("### Interpretação")
            if ndvi_data['mean'] < 0.1:
                st.error("Vegetação muito escassa - Solo exposto. Necessário preparo e irrigação.")
            elif ndvi_data['mean'] < 0.3:
                st.warning("Vegetação esparsa - Condições regulares para cultivo.")
            elif ndvi_data['mean'] < 0.5:
                st.success("Vegetação moderada - Boas condições para plantio.")
            else:
                st.success("Vegetação densa e saudável - Condições excelentes.")
    
    @staticmethod
    def render_recommendations(recommendations: List[Dict]):
        """Renderiza recomendações de culturas"""
        if not recommendations:
            st.info("Analisando dados para gerar recomendações...")
            return
        
        st.markdown("## Recomendações de Culturas")
        
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
                    <p><strong>Compatibilidade:</strong> {score_percent:.0f}%</p>
                    <p><strong>Suitabilidade:</strong> {crop['suitability_text']}</p>
                    <p><strong>Temperatura ideal:</strong> {crop['temp_ideal']}</p>
                    <p><strong>Precipitação ideal:</strong> {crop['precip_ideal']}</p>
                    <p><strong>Descrição:</strong> {crop['description']}</p>
                    <p><strong>Necessidade de água:</strong> {crop['water_requirement']}</p>
                    <p><strong>Valor de mercado:</strong> {crop['market_value']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander("Ver análise detalhada de todas as culturas"):
            for crop in recommendations:
                score_percent = crop['score']
                border_color = Config.SUCCESS_COLOR if crop['score'] >= 70 else Config.WARNING_COLOR if crop['score'] >= 50 else Config.DANGER_COLOR
                st.markdown(f"""
                <div style="padding: 1rem; margin: 0.5rem 0; border-left: 4px solid {border_color}; background: {Config.GRADIENT_CARD}; border-radius: 10px;">
                    <h4>{crop['icon']} {crop['name']} - {score_percent:.0f}% compatível</h4>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {score_percent}%;"></div>
                    </div>
                    <p><strong>{crop['recommendation_text']}</strong></p>
                    <p>{crop['description']}</p>
                    <details>
                        <summary>Detalhes técnicos</summary>
                        <ul>
                            <li><strong>Plantio:</strong> Profundidade {crop['planting_depth']}, Espaçamento {crop['spacing']}</li>
                            <li><strong>Ciclo:</strong> {crop['cycle']}</li>
                            <li><strong>Produtividade esperada:</strong> {crop['expected_yield']}</li>
                            <li><strong>Necessidade hídrica:</strong> {crop['water_requirement']}</li>
                        </ul>
                    </details>
                </div>
                """, unsafe_allow_html=True)
    
    @staticmethod
    def render_management_tips(temperature: float, precipitation: float, 
                                soil_moisture: float, ndvi: Optional[float]):
        """Renderiza dicas de manejo"""
        tips = []
        
        if precipitation < 40:
            tips.append(("Seca severa", "Irrigação urgente necessária. Adie o plantio se não houver irrigação.", "warning"))
        elif precipitation < 80:
            tips.append(("Baixa precipitação", "Considere irrigação suplementar ou culturas tolerantes à seca.", "warning"))
        elif precipitation > 200:
            tips.append(("Chuvas excessivas", "Risco de erosão. Melhore a drenagem e evite culturas sensíveis.", "warning"))
        
        if soil_moisture < 0.15:
            tips.append(("Solo seco", "Irrigue antes do plantio e aplique cobertura morta.", "warning"))
        elif soil_moisture > 0.40:
            tips.append(("Solo encharcado", "Aguarde a drenagem antes de plantar. Evite culturas sensíveis.", "warning"))
        elif 0.20 <= soil_moisture <= 0.35:
            tips.append(("Humidade ideal", "Condições ótimas para o desenvolvimento das culturas.", "success"))
        
        if temperature < 18:
            tips.append(("Temperaturas baixas", "Use variedades tolerantes ao frio ou aguarde o aquecimento.", "warning"))
        elif temperature > 35:
            tips.append(("Calor intenso", "Aumente a frequência de irrigação e use cobertura morta.", "warning"))
        
        if ndvi and ndvi < 0.2:
            tips.append(("Solo exposto", "Considere adubação verde para melhorar a fertilidade do solo.", "info"))
        
        if tips:
            st.markdown("### Dicas de Manejo")
            for title, message, tip_type in tips:
                if tip_type == "success":
                    st.success(f"**{title}** - {message}")
                elif tip_type == "warning":
                    st.warning(f"**{title}** - {message}")
                else:
                    st.info(f"**{title}** - {message}")
        else:
            st.success("Condições favoráveis para o plantio!")
    
    @staticmethod
    def render_climate_dashboard(df: pd.DataFrame, year: int):
        """Renderiza dashboard climático completo"""
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
                'Temperatura Média Mensal',
                'Precipitação Mensal',
                'Umidade do Solo',
                'Radiação Solar'
            ),
            vertical_spacing=0.15,
            horizontal_spacing=0.12
        )
        
        fig.add_trace(
            go.Scatter(
                x=monthly_avg['month'],
                y=monthly_avg['temp_c'],
                mode='lines+markers',
                name='Temperatura',
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
                name='Precipitação',
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
                name='Radiação',
                line=dict(color=Config.WARNING_COLOR, width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(230,126,34,0.1)'
            ),
            row=2, col=2
        )
        
        months_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        for row in [1, 2]:
            for col in [1, 2]:
                fig.update_xaxes(
                    title_text="Mês",
                    tickmode='array',
                    tickvals=list(range(1, 13)),
                    ticktext=months_labels,
                    row=row, col=col
                )
        
        fig.update_yaxes(title_text="Temperatura (°C)", row=1, col=1)
        fig.update_yaxes(title_text="Precipitação (mm)", row=1, col=2)
        fig.update_yaxes(title_text="Umidade (m³/m³)", row=2, col=1)
        fig.update_yaxes(title_text="Radiação (MJ/m²)", row=2, col=2)
        
        fig.update_layout(
            height=700,
            showlegend=True,
            title_text=f"Análise Climática Completa - {year}",
            title_font_size=18,
            hovermode='x unified',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# FUNÇÃO PRINCIPAL
# ==========================================

def main():
    """Função principal da aplicação"""
    
    inject_custom_css()
    DashboardComponents.render_header()
    
    with st.spinner("Carregando dados climáticos..."):
        climate_data = load_climate_data()
    
    if climate_data is None:
        st.error("Não foi possível carregar os dados. Verifique os arquivos.")
        return
    
    with st.sidebar:
        st.markdown("## Controles")
        st.markdown("---")
        
        years = sorted(climate_data['year'].unique())
        selected_year = st.selectbox(
            "Ano",
            years,
            index=len(years) - 1
        )
        
        selected_month = st.selectbox(
            "Mês",
            list(range(1, 13)),
            format_func=lambda x: calendar.month_name[x]
        )
        
        st.markdown("---")
        st.markdown("### Sobre")
        st.info("""
        **AgriSense Africa** é uma plataforma inteligente que utiliza:
        - Dados climáticos históricos (2018-2023)
        - Imagens de satélite NDVI
        - Análise de humidade do solo em duas camadas
        
        As recomendações são geradas considerando 6 fatores simultaneamente.
        """)
        
        st.markdown("---")
        st.markdown("### Culturas Analisadas")
        crops_list = list(CropRecommender.CROPS_DATABASE.keys())
        st.write(", ".join(crops_list))
    
    filtered_data = climate_data[
        (climate_data['year'] == selected_year) & 
        (climate_data['month'] == selected_month)
    ]
    
    if filtered_data.empty:
        st.warning(f"Não há dados disponíveis para {calendar.month_name[selected_month]} de {selected_year}")
        return
    
    with st.spinner("Carregando dados de satélite..."):
        ndvi_data = load_ndvi_data(selected_year, selected_month)
    
    temp = filtered_data['temp_c'].mean()
    precip = filtered_data['precip_mm'].mean()
    soil = filtered_data['swvl1'].mean()
    solar = filtered_data['solar_mj'].mean()
    ndvi = ndvi_data['mean'] if ndvi_data else None
    
    recommender = CropRecommender(temp, precip, soil, solar, ndvi, selected_month)
    recommendations = recommender.recommend_all()
    
    st.markdown(f"### Período: **{calendar.month_name[selected_month]} de {selected_year}**")
    
    DashboardComponents.render_metrics(filtered_data)
    DashboardComponents.render_soil_analysis(filtered_data)
    
    st.markdown("### Índice de Vegetação")
    DashboardComponents.render_ndvi_analysis(ndvi_data, selected_year, selected_month)
    
    st.markdown("---")
    DashboardComponents.render_recommendations(recommendations)
    DashboardComponents.render_management_tips(temp, precip, soil, ndvi)
    
    st.markdown("---")
    st.markdown("## Análises Complementares")
    
    tab1, tab2 = st.tabs(["Dashboard Climático", "Dados Mensais"])
    
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
        monthly_data.columns = ['Temperatura (°C)', 'Precipitação (mm)',
                                'Umidade 0-7cm', 'Umidade 7-28cm', 'Radiação (MJ/m²)']
        st.dataframe(monthly_data, use_container_width=True)
    
    st.markdown(f"""
    <div class="footer">
        <p><strong>AgriSense Africa</strong> - Plataforma Inteligente para Agricultura Sustentável</p>
        <p>Aumento estimado de produtividade: 20-30% com adoção das recomendações</p>
        <p style="font-size: 0.75rem;">© 2026 {Config.COMPANY} | Versão {Config.APP_VERSION}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()