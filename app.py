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
# CONFIGURAÇÃO GLOBAL
# ==========================================

# Configuração da página - deve ser a primeira chamada Streamlit
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
    APP_VERSION = "2.0.0"
    COMPANY = "AgriSense Intelligence"
    
    # Caminhos dos dados
    CLIMATE_FILE = "Dados_clima_2018_2023.csv"
    NDVI_FOLDER = "ndvi"
    
    # Limites para validação
    TEMP_MIN = -10
    TEMP_MAX = 50
    PRECIP_MAX = 500
    SOIL_MOISTURE_MAX = 0.6
    
    # Cores do tema
    PRIMARY_COLOR = "#2E7D32"
    SECONDARY_COLOR = "#FFC107"
    ACCENT_COLOR = "#2196F3"
    DANGER_COLOR = "#F44336"
    SUCCESS_COLOR = "#4CAF50"
    WARNING_COLOR = "#FF9800"
    
    # Configurações de cache
    CACHE_TTL = 3600  # 1 hora

# ==========================================
# ESTILOS CSS PROFISSIONAIS
# ==========================================

def inject_custom_css():
    """Injeta estilos CSS personalizados para uma experiência profissional"""
    st.markdown(f"""
    <style>
        /* Reset e configurações base */
        .stApp {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }}
        
        /* Header principal */
        .main-header {{
            background: linear-gradient(135deg, {Config.PRIMARY_COLOR} 0%, {Config.SUCCESS_COLOR} 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            animation: slideDown 0.5s ease-out;
        }}
        
        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Cards de métricas */
        .metric-card {{
            background: white;
            padding: 1.2rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(0,0,0,0.05);
            margin: 0.5rem 0;
        }}
        
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        
        /* Cards de recomendação */
        .recommendation-card {{
            background: white;
            padding: 1.2rem;
            border-radius: 15px;
            margin: 0.8rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            cursor: pointer;
            border-top: 4px solid;
        }}
        
        .recommendation-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.15);
        }}
        
        .crop-high {{ border-top-color: {Config.SUCCESS_COLOR}; background: linear-gradient(135deg, #fff 0%, #f1f8e9 100%); }}
        .crop-moderate {{ border-top-color: {Config.WARNING_COLOR}; background: linear-gradient(135deg, #fff 0%, #fff8e7 100%); }}
        .crop-low {{ border-top-color: {Config.DANGER_COLOR}; background: linear-gradient(135deg, #fff 0%, #ffebee 100%); }}
        
        /* Barra de progresso */
        .progress-container {{
            background: #e0e0e0;
            border-radius: 10px;
            height: 8px;
            margin: 10px 0;
            overflow: hidden;
        }}
        
        .progress-bar {{
            height: 100%;
            border-radius: 10px;
            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            background: linear-gradient(90deg, {Config.SUCCESS_COLOR}, {Config.PRIMARY_COLOR});
        }}
        
        /* Cards de solo */
        .soil-card {{
            background: linear-gradient(135deg, #5D4037 0%, #3E2723 100%);
            padding: 1rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }}
        
        .soil-card:hover {{
            transform: translateY(-3px);
        }}
        
        /* Informações e alertas */
        .info-box {{
            background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid {Config.ACCENT_COLOR};
            margin: 1rem 0;
        }}
        
        .success-box {{
            background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid {Config.SUCCESS_COLOR};
            margin: 1rem 0;
        }}
        
        .warning-box {{
            background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid {Config.WARNING_COLOR};
            margin: 1rem 0;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            border-radius: 15px;
            margin-top: 2rem;
            font-size: 0.9rem;
        }}
        
        /* Animações */
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.5s ease-in;
        }}
        
        /* Scrollbar personalizada */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {Config.PRIMARY_COLOR};
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {Config.SUCCESS_COLOR};
        }}
        
        /* Botões */
        .stButton > button {{
            background: linear-gradient(135deg, {Config.PRIMARY_COLOR}, {Config.SUCCESS_COLOR});
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s;
            width: 100%;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(46,125,50,0.3);
        }}
        
        /* Títulos */
        h1, h2, h3 {{
            color: {Config.PRIMARY_COLOR};
            font-weight: 600;
        }}
        
        /* Métricas grandes */
        .big-metric {{
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
            padding: 0;
            line-height: 1;
        }}
        
        /* Grid responsivo */
        .responsive-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# GERENCIAMENTO DE DADOS COM CACHE
# ==========================================

@st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
def load_climate_data() -> Optional[pd.DataFrame]:
    """
    Carrega e processa dados climáticos com validação robusta
    Returns:
        DataFrame processado ou None em caso de erro
    """
    try:
        # Verificar se arquivo existe
        if not os.path.exists(Config.CLIMATE_FILE):
            st.error(f"❌ Arquivo {Config.CLIMATE_FILE} não encontrado")
            return None
        
        # Carregar dados
        df = pd.read_csv(Config.CLIMATE_FILE)
        
        # Validar colunas essenciais
        required_cols = ['valid_time', 't2m', 'tp', 'u10', 'v10', 'ssrd', 'swvl1', 'swvl2']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Colunas ausentes: {missing_cols}")
            return None
        
        # Processar datas
        df['valid_time'] = pd.to_datetime(df['valid_time'])
        df['year'] = df['valid_time'].dt.year
        df['month'] = df['valid_time'].dt.month
        df['month_name'] = df['month'].apply(lambda x: calendar.month_abbr[x])
        
        # Converter unidades
        df['temp_c'] = df['t2m'] - 273.15  # Kelvin → Celsius
        df['precip_mm'] = df['tp'] * 1000  # metros → mm
        df['wind_speed'] = np.sqrt(df['u10']**2 + df['v10']**2)  # m/s
        df['solar_mj'] = df['ssrd'] / 1e6  # J/m² → MJ/m²
        
        # Validar valores
        df['temp_c'] = df['temp_c'].clip(Config.TEMP_MIN, Config.TEMP_MAX)
        df['precip_mm'] = df['precip_mm'].clip(0, Config.PRECIP_MAX)
        df['swvl1'] = df['swvl1'].clip(0, Config.SOIL_MOISTURE_MAX)
        df['swvl2'] = df['swvl2'].clip(0, Config.SOIL_MOISTURE_MAX)
        
        return df
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados climáticos: {str(e)}")
        return None

@st.cache_data(ttl=Config.CACHE_TTL, show_spinner=False)
def load_ndvi_data(year: int, month: int) -> Optional[Dict[str, Any]]:
    """
    Carrega dados NDVI com suporte a múltiplos formatos de arquivo
    """
    # Tentar diferentes formatos de nome de arquivo
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
            
            # Limpeza dos dados
            ndvi = np.where(ndvi < -1000, np.nan, ndvi)
            ndvi = np.clip(ndvi, -1, 1)
            
            # Calcular estatísticas
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
        st.warning(f"⚠️ Erro ao ler NDVI {ndvi_path}: {str(e)}")
        return None

# ==========================================
# SISTEMA DE RECOMENDAÇÃO INTELIGENTE
# ==========================================

class CropRecommender:
    """Sistema de recomendação de culturas baseado em múltiplos fatores"""
    
    # Base de conhecimento das culturas
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
        """
        Inicializa o recomendador com as condições atuais
        """
        self.conditions = {
            'temp': temperature,
            'precip': precipitation,
            'soil': soil_moisture,
            'solar': solar_radiation,
            'ndvi': ndvi,
            'month': month
        }
    
    def _calculate_temperature_score(self, crop_params: Dict) -> Tuple[float, str]:
        """Calcula pontuação para temperatura"""
        temp = self.conditions['temp']
        temp_range = crop_params['temp_range']
        
        if temp_range[0] <= temp <= temp_range[1]:
            return 30, f"🌡️ Temperatura ideal: {temp:.1f}°C"
        elif temp < temp_range[0]:
            diff = temp_range[0] - temp
            score = max(0, 20 - diff * 1.5)
            return score, f"⚠️ Temperatura {temp:.1f}°C abaixo do ideal ({temp_range[0]}-{temp_range[1]}°C)"
        else:
            diff = temp - temp_range[1]
            score = max(0, 20 - diff * 1.2)
            return score, f"⚠️ Temperatura {temp:.1f}°C acima do ideal ({temp_range[0]}-{temp_range[1]}°C)"
    
    def _calculate_precipitation_score(self, crop_params: Dict) -> Tuple[float, str]:
        """Calcula pontuação para precipitação"""
        precip = self.conditions['precip']
        precip_range = crop_params['precip_range']
        
        if precip_range[0] <= precip <= precip_range[1]:
            return 30, f"💧 Precipitação ideal: {precip:.1f}mm"
        elif precip < precip_range[0]:
            diff = precip_range[0] - precip
            score = max(0, 20 - diff / 5)
            return score, f"⚠️ Precipitação {precip:.1f}mm abaixo do necessário ({precip_range[0]}-{precip_range[1]}mm)"
        else:
            diff = precip - precip_range[1]
            score = max(0, 20 - diff / 8)
            return score, f"⚠️ Precipitação {precip:.1f}mm acima do recomendado ({precip_range[0]}-{precip_range[1]}mm)"
    
    def _calculate_soil_score(self, crop_params: Dict) -> Tuple[float, str]:
        """Calcula pontuação para umidade do solo"""
        soil = self.conditions['soil']
        soil_range = crop_params.get('soil_range', (0.15, 0.35))
        
        if soil is None:
            return 0, "📊 Dados de solo não disponíveis"
        
        if soil_range[0] <= soil <= soil_range[1]:
            return 20, f"🌱 Umidade do solo ideal: {soil:.2f}"
        elif soil < soil_range[0]:
            diff = soil_range[0] - soil
            score = max(0, 12 - diff * 40)
            return score, f"⚠️ Solo seco: {soil:.2f} (ideal >{soil_range[0]:.2f})"
        else:
            diff = soil - soil_range[1]
            score = max(0, 12 - diff * 40)
            return score, f"⚠️ Solo encharcado: {soil:.2f} (ideal <{soil_range[1]:.2f})"
    
    def _calculate_ndvi_score(self) -> Tuple[float, str]:
        """Calcula pontuação baseada no NDVI"""
        ndvi = self.conditions['ndvi']
        
        if ndvi is None:
            return 0, "🛰️ Dados NDVI não disponíveis"
        
        if ndvi >= 0.5:
            return 15, f"🟢 NDVI excelente ({ndvi:.2f}) - Vegetação densa e saudável"
        elif ndvi >= 0.3:
            return 12, f"🟢 NDVI bom ({ndvi:.2f}) - Boa cobertura vegetal"
        elif ndvi >= 0.2:
            return 8, f"🟡 NDVI moderado ({ndvi:.2f}) - Vegetação em desenvolvimento"
        elif ndvi >= 0.1:
            return 4, f"🟠 NDVI baixo ({ndvi:.2f}) - Vegetação esparsa"
        else:
            return 2, f"🔴 NDVI muito baixo ({ndvi:.2f}) - Solo exposto"
    
    def _calculate_solar_score(self) -> Tuple[float, str]:
        """Calcula pontuação baseada na radiação solar"""
        solar = self.conditions['solar']
        
        if solar is None:
            return 0, "☀️ Dados de radiação não disponíveis"
        
        if solar >= 20:
            return 5, f"☀️ Radiação solar excelente: {solar:.1f} MJ/m²"
        elif solar >= 15:
            return 4, f"☀️ Boa radiação solar: {solar:.1f} MJ/m²"
        elif solar >= 10:
            return 2, f"☀️ Radiação moderada: {solar:.1f} MJ/m²"
        else:
            return 1, f"☀️ Baixa radiação: {solar:.1f} MJ/m²"
    
    def _calculate_seasonal_score(self, crop_params: Dict) -> Tuple[float, str]:
        """Calcula pontuação baseada na sazonalidade"""
        month = self.conditions['month']
        optimal_months = crop_params.get('optimal_months', [])
        
        if month in optimal_months:
            return 10, f"📅 Mês ideal para plantio ({calendar.month_name[month]})"
        elif optimal_months and abs(month - optimal_months[0]) <= 1:
            return 5, f"📅 Período próximo ao ideal ({calendar.month_name[month]})"
        else:
            return 0, f"📅 Mês não ideal para plantio"
    
    def recommend_all(self) -> List[Dict[str, Any]]:
        """
        Gera recomendações para todas as culturas com pontuação detalhada
        """
        results = []
        
        for crop_name, params in self.CROPS_DATABASE.items():
            # Calcular pontuações individuais
            temp_score, temp_detail = self._calculate_temperature_score(params)
            precip_score, precip_detail = self._calculate_precipitation_score(params)
            soil_score, soil_detail = self._calculate_soil_score(params)
            ndvi_score, ndvi_detail = self._calculate_ndvi_score()
            solar_score, solar_detail = self._calculate_solar_score()
            seasonal_score, seasonal_detail = self._calculate_seasonal_score(params)
            
            # Pontuação total
            total_score = temp_score + precip_score + soil_score + ndvi_score + solar_score + seasonal_score
            
            # Determinar classe de suitaabilidade
            if total_score >= 70:
                suitability_class = "high"
                suitability_text = "Alta ✅"
                recommendation_text = "Condições excelentes para esta cultura"
            elif total_score >= 50:
                suitability_class = "moderate"
                suitability_text = "Moderada ⚠️"
                recommendation_text = "Condições adequadas, monitorar desenvolvimento"
            else:
                suitability_class = "low"
                suitability_text = "Baixa ❌"
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
        
        # Ordenar por pontuação
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

# ==========================================
# COMPONENTES DE VISUALIZAÇÃO
# ==========================================

class DashboardComponents:
    """Componentes reutilizáveis do dashboard"""
    
    @staticmethod
    def render_header():
        """Renderiza o cabeçalho da aplicação"""
        st.markdown(f"""
        <div class="main-header">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">🌾 {Config.APP_NAME}</h1>
            <p style="color: white; font-size: 1.1rem; margin-top: 0.5rem; opacity: 0.95;">
            Plataforma Inteligente para Recomendação de Culturas
            </p>
            <p style="color: white; font-size: 0.85rem; margin-top: 0.5rem; opacity: 0.8;">
            Versão {Config.APP_VERSION} | {Config.COMPANY}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_metrics(data: pd.DataFrame):
        """Renderiza métricas principais"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="🌡️ Temperatura",
                value=f"{data['temp_c'].mean():.1f}°C",
                delta=f"{data['temp_c'].mean() - data['temp_c'].shift(12).mean():.1f}°C" if len(data) > 12 else None
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="💧 Precipitação",
                value=f"{data['precip_mm'].mean():.1f} mm",
                delta=None
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="💨 Velocidade do Vento",
                value=f"{data['wind_speed'].mean():.1f} m/s",
                delta=None
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(
                label="☀️ Radiação Solar",
                value=f"{data['solar_mj'].mean():.1f} MJ/m²",
                delta=None
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_soil_analysis(data: pd.DataFrame):
        """Renderiza análise de solo com duas camadas"""
        st.markdown("### 💧 Análise da Umidade do Solo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="soil-card">
                <h4>📊 Camada Superficial</h4>
                <div class="big-metric">{data['swvl1'].mean():.3f}</div>
                <p>m³/m³ (0-7cm)</p>
                <small>Umidade na camada superficial do solo</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="soil-card">
                <h4>📊 Camada Profunda</h4>
                <div class="big-metric">{data['swvl2'].mean():.3f}</div>
                <p>m³/m³ (7-28cm)</p>
                <small>Umidade na camada de raízes</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Análise de gradiente
        layer1 = data['swvl1'].mean()
        layer2 = data['swvl2'].mean()
        
        if layer2 > layer1:
            st.success("🌊 **Boa infiltração:** Água penetrando nas camadas mais profundas")
        elif layer1 > layer2 + 0.05:
            st.warning("⚠️ **Drenagem comprometida:** Água acumulada na superfície")
        else:
            st.info("📊 **Perfil uniforme:** Umidade equilibrada no perfil do solo")
    
    @staticmethod
    def render_ndvi_analysis(ndvi_data: Optional[Dict], year: int, month: int):
        """Renderiza análise NDVI"""
        if ndvi_data is None:
            st.warning("⚠️ Dados NDVI não disponíveis para este período")
            return
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            im = ax.imshow(ndvi_data['data'], cmap='RdYlGn', vmin=-0.2, vmax=0.8)
            plt.colorbar(im, ax=ax, label='NDVI', fraction=0.046, pad=0.04)
            ax.set_title(f'Índice de Vegetação NDVI\n{calendar.month_name[month]} {year}', 
                        fontsize=12, fontweight='bold')
            ax.axis('off')
            st.pyplot(fig)
        
        with col2:
            st.markdown("### 📊 Estatísticas")
            st.metric("Valor Médio", f"{ndvi_data['mean']:.4f}")
            st.metric("Desvio Padrão", f"{ndvi_data['std']:.4f}")
            st.metric("Mínimo", f"{ndvi_data['min']:.4f}")
            st.metric("Máximo", f"{ndvi_data['max']:.4f}")
            
            # Interpretação
            st.markdown("### 🔍 Interpretação")
            if ndvi_data['mean'] < 0.1:
                st.error("🔴 **Vegetação muito escassa** - Solo exposto. Necessário preparo e irrigação.")
            elif ndvi_data['mean'] < 0.3:
                st.warning("🟡 **Vegetação esparsa** - Condições regulares para cultivo.")
            elif ndvi_data['mean'] < 0.5:
                st.success("🟢 **Vegetação moderada** - Boas condições para plantio.")
            else:
                st.success("🌿 **Vegetação densa e saudável** - Condições excelentes.")
    
    @staticmethod
    def render_recommendations(recommendations: List[Dict]):
        """Renderiza recomendações de culturas"""
        if not recommendations:
            st.info("📊 Analisando dados para gerar recomendações...")
            return
        
        st.markdown("## 🎯 Recomendações de Culturas")
        
        # Top 3 culturas em destaque
        top_crops = recommendations[:3]
        cols = st.columns(3)
        
        for idx, crop in enumerate(top_crops):
            with cols[idx]:
                card_class = f"crop-{crop['suitability_class']}"
                score_percent = crop['score']
                
                st.markdown(f"""
                <div class="recommendation-card {card_class}">
                    <h2 style="margin: 0; font-size: 2rem;">{crop['icon']} {crop['name']}</h2>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {score_percent}%;"></div>
                    </div>
                    <p><strong>Compatibilidade:</strong> {score_percent:.0f}%</p>
                    <p><strong>Suitabilidade:</strong> {crop['suitability_text']}</p>
                    <p><strong>🌡️ Temperatura ideal:</strong> {crop['temp_ideal']}</p>
                    <p><strong>💧 Precipitação ideal:</strong> {crop['precip_ideal']}</p>
                    <p><strong>📝 Descrição:</strong> {crop['description']}</p>
                    <p><strong>💧 Necessidade de água:</strong> {crop['water_requirement']}</p>
                    <p><strong>💰 Valor de mercado:</strong> {crop['market_value']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Expandir para todas as culturas
        with st.expander("📋 Ver análise detalhada de todas as culturas"):
            for crop in recommendations:
                score_percent = crop['score']
                st.markdown(f"""
                <div style="padding: 1rem; margin: 0.5rem 0; border-left: 4px solid {'#4CAF50' if crop['score'] >= 70 else '#FFC107' if crop['score'] >= 50 else '#F44336'}; background: #f9f9f9; border-radius: 8px;">
                    <h4>{crop['icon']} {crop['name']} - {score_percent:.0f}% compatível</h4>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {score_percent}%;"></div>
                    </div>
                    <p><strong>{crop['recommendation_text']}</strong></p>
                    <p>{crop['description']}</p>
                    <details>
                        <summary>📊 Detalhes técnicos</summary>
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
        """Renderiza dicas de manejo baseadas nas condições"""
        tips = []
        
        # Dicas baseadas na precipitação
        if precipitation < 40:
            tips.append(("💧 **Seca severa**", "Irrigação urgente necessária. Adie o plantio se não houver irrigação.", "warning"))
        elif precipitation < 80:
            tips.append(("⚠️ **Baixa precipitação**", "Considere irrigação suplementar ou culturas tolerantes à seca.", "warning"))
        elif precipitation > 200:
            tips.append(("🌧️ **Chuvas excessivas**", "Risco de erosão. Melhore a drenagem e evite culturas sensíveis.", "warning"))
        
        # Dicas baseadas na umidade do solo
        if soil_moisture < 0.15:
            tips.append(("🏜️ **Solo seco**", "Irrigue antes do plantio e aplique cobertura morta.", "warning"))
        elif soil_moisture > 0.40:
            tips.append(("💦 **Solo encharcado**", "Aguarde a drenagem antes de plantar. Evite culturas sensíveis.", "warning"))
        elif 0.20 <= soil_moisture <= 0.35:
            tips.append(("✅ **Umidade ideal**", "Condições ótimas para o desenvolvimento das culturas.", "success"))
        
        # Dicas baseadas na temperatura
        if temperature < 18:
            tips.append(("❄️ **Temperaturas baixas**", "Use variedades tolerantes ao frio ou aguarde o aquecimento.", "warning"))
        elif temperature > 35:
            tips.append(("🔥 **Calor intenso**", "Aumente a frequência de irrigação e use cobertura morta.", "warning"))
        
        # Dicas baseadas no NDVI
        if ndvi and ndvi < 0.2:
            tips.append(("🌱 **Solo exposto**", "Considere adubação verde para melhorar a fertilidade do solo.", "info"))
        
        if tips:
            st.markdown("### 💡 Dicas de Manejo")
            for title, message, tip_type in tips:
                if tip_type == "success":
                    st.success(f"**{title}** - {message}")
                elif tip_type == "warning":
                    st.warning(f"**{title}** - {message}")
                else:
                    st.info(f"**{title}** - {message}")
        else:
            st.success("✅ Condições favoráveis para o plantio!")
    
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
        
        # Criar figura com subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '🌡️ Temperatura Média Mensal',
                '💧 Precipitação Mensal',
                '🌱 Umidade do Solo',
                '☀️ Radiação Solar'
            ),
            vertical_spacing=0.15,
            horizontal_spacing=0.12
        )
        
        # Temperatura
        fig.add_trace(
            go.Scatter(
                x=monthly_avg['month'],
                y=monthly_avg['temp_c'],
                mode='lines+markers',
                name='Temperatura',
                line=dict(color='#F44336', width=3),
                marker=dict(size=8, color='#F44336'),
                fill='tozeroy',
                fillcolor='rgba(244,67,54,0.1)'
            ),
            row=1, col=1
        )
        
        # Precipitação
        fig.add_trace(
            go.Bar(
                x=monthly_avg['month'],
                y=monthly_avg['precip_mm'],
                name='Precipitação',
                marker_color='#2196F3',
                opacity=0.7
            ),
            row=1, col=2
        )
        
        # Umidade do solo
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
                line=dict(color='#D2691E', width=2),
                marker=dict(size=6)
            ),
            row=2, col=1
        )
        
        # Radiação Solar
        fig.add_trace(
            go.Scatter(
                x=monthly_avg['month'],
                y=monthly_avg['solar_mj'],
                mode='lines+markers',
                name='Radiação',
                line=dict(color='#FF9800', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(255,152,0,0.1)'
            ),
            row=2, col=2
        )
        
        # Configurar eixos
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
            title_text=f"📊 Análise Climática Completa - {year}",
            title_font_size=18,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# FUNÇÃO PRINCIPAL DA APLICAÇÃO
# ==========================================

def main():
    """Função principal da aplicação"""
    
    # Injetar CSS
    inject_custom_css()
    
    # Renderizar header
    DashboardComponents.render_header()
    
    # Carregar dados
    with st.spinner("🔄 Carregando dados climáticos..."):
        climate_data = load_climate_data()
    
    if climate_data is None:
        st.error("❌ Não foi possível carregar os dados. Verifique os arquivos.")
        return
    
    # Sidebar com controles
    with st.sidebar:
        st.markdown("## 🔍 Controles")
        st.markdown("---")
        
        years = sorted(climate_data['year'].unique())
        selected_year = st.selectbox(
            "📅 Ano",
            years,
            index=len(years) - 1,
            help="Selecione o ano para análise"
        )
        
        selected_month = st.selectbox(
            "📆 Mês",
            list(range(1, 13)),
            format_func=lambda x: calendar.month_name[x],
            help="Selecione o mês para análise"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Sobre")
        st.info(f"""
        **{Config.APP_NAME}** é uma plataforma inteligente que utiliza:
        - Dados climáticos históricos (2018-2023)
        - Imagens de satélite NDVI
        - Análise de humidade do solo em duas camadas
        
        As recomendações são geradas por um sistema de pontuação que considera 6 fatores simultaneamente.
        """)
        
        st.markdown("---")
        st.markdown("### 🌱 Culturas Analisadas")
        crops_list = list(CropRecommender.CROPS_DATABASE.keys())
        st.write(", ".join(crops_list))
    
    # Filtrar dados
    filtered_data = climate_data[
        (climate_data['year'] == selected_year) & 
        (climate_data['month'] == selected_month)
    ]
    
    if filtered_data.empty:
        st.warning(f"⚠️ Não há dados disponíveis para {calendar.month_name[selected_month]} de {selected_year}")
        return
    
    # Carregar NDVI
    with st.spinner("🛰️ Carregando dados de satélite..."):
        ndvi_data = load_ndvi_data(selected_year, selected_month)
    
    # Extrair condições atuais
    temp = filtered_data['temp_c'].mean()
    precip = filtered_data['precip_mm'].mean()
    soil = filtered_data['swvl1'].mean()
    solar = filtered_data['solar_mj'].mean()
    ndvi = ndvi_data['mean'] if ndvi_data else None
    
    # Gerar recomendações
    recommender = CropRecommender(temp, precip, soil, solar, ndvi, selected_month)
    recommendations = recommender.recommend_all()
    
    # Layout principal
    st.markdown(f"### 📍 Período: **{calendar.month_name[selected_month]} de {selected_year}**")
    
    # Métricas
    DashboardComponents.render_metrics(filtered_data)
    
    # Umidade do solo
    DashboardComponents.render_soil_analysis(filtered_data)
    
    # NDVI
    st.markdown("### 🛰️ Índice de Vegetação")
    DashboardComponents.render_ndvi_analysis(ndvi_data, selected_year, selected_month)
    
    # Recomendações
    st.markdown("---")
    DashboardComponents.render_recommendations(recommendations)
    
    # Dicas de manejo
    DashboardComponents.render_management_tips(temp, precip, soil, ndvi)
    
    # Análises complementares
    st.markdown("---")
    st.markdown("## 📈 Análises Complementares")
    
    tab1, tab2 = st.tabs(["📊 Dashboard Climático", "📋 Dados Mensais"])
    
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
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <p><strong>🌾 {Config.APP_NAME}</strong> - Plataforma Inteligente para Agricultura Sustentável</p>
        <p>🚀 Aumento estimado de produtividade: 20-30% com adoção das recomendações</p>
        <p style="font-size: 0.8rem;">© 2026 {Config.COMPANY} | Versão {Config.APP_VERSION}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PONTO DE ENTRADA
# ==========================================

if __name__ == "__main__":
    main()