"""
AGRISENSE AFRICA - PRESENTATION MODE
Intelligent Agricultural Platform to Increase Production
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import base64
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AgriSense Africa | Presentation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for presentation
st.markdown("""
<style>
    /* Presentation Mode Styles */
    .stApp {
        background: linear-gradient(135deg, #FDF8F0 0%, #FFFFFF 100%);
    }
    
    .presentation-slide {
        min-height: 80vh;
        padding: 2rem;
        border-radius: 24px;
        background: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .slide-title {
        font-size: 3rem;
        font-weight: 700;
        color: #1A4D3E;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .slide-subtitle {
        font-size: 1.5rem;
        color: #2C7A47;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .metric-big {
        font-size: 3rem;
        font-weight: 800;
        color: #1A4D3E;
        text-align: center;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #666;
        text-align: center;
    }
    
    .highlight {
        background: linear-gradient(120deg, #D9B48B 0%, #D9B48B 40%, transparent 40%);
        padding: 0 0.2rem;
    }
    
    .stat-card {
        background: #F8F9FA;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border-left: 4px solid #1A4D3E;
        margin: 1rem 0;
    }
    
    .model-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-top: 4px solid #2C7A47;
        height: 100%;
    }
    
    .footer-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        border-top: 1px solid #eee;
        text-align: center;
    }
    
    hr {
        margin: 2rem 0;
    }
    
    .big-number {
        font-size: 4rem;
        font-weight: 800;
        color: #1A4D3E;
    }
</style>
""", unsafe_allow_html=True)

def create_slide_container():
    """Create a container for each slide"""
    return st.container()

def slide_1_title():
    """Slide 1: Title"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        
        # Logo area
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<p style="text-align: center; font-size: 5rem;">🌾</p>', unsafe_allow_html=True)
        
        st.markdown('<h1 class="slide-title">AgriSense Africa</h1>', unsafe_allow_html=True)
        st.markdown('<h2 class="slide-subtitle">Intelligent Agricultural Platform<br>to Increase Production</h2>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown("""
            <div style="text-align: center;">
                <p><strong>Francisco Macucule</strong></p>
                <p><strong>Prof. James Chibueze</strong></p>
                <p><strong>Dr. Mark Johnson</strong></p>
                <p style="margin-top: 1rem;">26 January 2026</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def slide_2_problem():
    """Slide 2: The Problem"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        st.markdown('<h1 class="slide-title">O Desafio</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="stat-card">
                <h3>📉 Baixa Produtividade</h3>
                <p>Produtividade abaixo do potencial devido à falta de informações precisas</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="stat-card">
                <h3>💧 Altos Custos</h3>
                <p>Uso excessivo de água, fertilizantes e pesticidas sem necessidade</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card">
                <h3>📱 Informação Fragmentada</h3>
                <p>Dados climáticos, de solo e agrícolas não integrados em uma única plataforma</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="stat-card">
                <h3>🌍 Acesso Limitado</h3>
                <p>Falta de tecnologia acessível para pequenos agricultores</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def slide_3_solution():
    """Slide 3: Our Solution"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        st.markdown('<h1 class="slide-title">Nossa Solução</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem;">Uma plataforma digital que combina:</p>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        
        icons = ["📡", "🌤️", "🌱", "🤖"]
        titles = ["Satélite", "Clima", "Solo", "IA"]
        descs = ["NDVI Sentinel-2", "Previsões + Histórico", "Umidade + Temperatura", "Recomendações Personalizadas"]
        
        for i, (col, icon, title, desc) in enumerate(zip(cols, icons, titles, descs)):
            with col:
                st.markdown(f"""
                <div class="model-card" style="text-align: center;">
                    <p style="font-size: 3rem;">{icon}</p>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<h3 style="text-align: center;">🎯 Resultado: Recomendações Claras e Acionáveis</h3>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def slide_4_architecture():
    """Slide 4: Technical Architecture"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        st.markdown('<h1 class="slide-title">Arquitetura Técnica</h1>', unsafe_allow_html=True)
        
        # Flowchart using plotly
        fig = go.Figure()
        
        # Add nodes
        nodes = [
            "📡 Satélite\nSentinel-2",
            "🌤️ Clima\nERA5",
            "🌱 Solo\nSensores",
            "📊 NDVI\nAnalysis",
            "🔮 ML Models\nXGBoost/RF/GB",
            "✅ Recomendações\nAgrícolas"
        ]
        
        # Create a simple flowchart visualization
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="model-card" style="text-align: center;">
                <p style="font-size: 2rem;">📡</p>
                <h4>Satélite Sentinel-2</h4>
                <p>NDVI 10m resolução</p>
                <p style="color: #2C7A47;">↓</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="model-card" style="text-align: center;">
                <p style="font-size: 2rem;">🌱</p>
                <h4>Solo</h4>
                <p>Umidade (swvl1, swvl2)</p>
                <p style="color: #2C7A47;">↓</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="model-card" style="text-align: center;">
                <p style="font-size: 2rem;">📊</p>
                <h4>Análise NDVI</h4>
                <p>Zonas de Vegetação</p>
                <p>Saúde das Culturas</p>
                <p style="color: #2C7A47;">↓</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="model-card" style="text-align: center;">
                <p style="font-size: 2rem;">🌤️</p>
                <h4>Clima ERA5</h4>
                <p>Temperatura, Precipitação</p>
                <p>Radiação Solar</p>
                <p style="color: #2C7A47;">↓</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="model-card" style="text-align: center; margin-top: 1rem;">
            <p style="font-size: 2rem;">🤖</p>
            <h4>Modelos de Machine Learning</h4>
            <p>XGBoost | Random Forest | Gradient Boosting</p>
            <p style="color: #2C7A47;">↓</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="model-card" style="text-align: center; background: linear-gradient(135deg, #1A4D3E 0%, #2C7A47 100%); color: white;">
            <p style="font-size: 2rem;">✅</p>
            <h4 style="color: white;">Recomendações Personalizadas</h4>
            <p>Quando plantar | Quando irrigar | Como fertilizar | Como colher</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def slide_5_models():
    """Slide 5: ML Models Selection"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        st.markdown('<h1 class="slide-title">Modelos de IA</h1>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="model-card">
                <h2 style="color: #1A4D3E;">XGBoost</h2>
                <p><strong>Por que escolhemos:</strong></p>
                <ul>
                    <li>Excelente para séries temporais</li>
                    <li>Regularização L1/L2 integrada</li>
                    <li>High accuracy com dados limitados</li>
                    <li>Feature importance nativa</li>
                </ul>
                <p><strong>Vantagem:</strong> Melhor performance em competições de dados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="model-card">
                <h2 style="color: #2C7A47;">Random Forest</h2>
                <p><strong>Por que escolhemos:</strong></p>
                <ul>
                    <li>Ensemble de árvores</li>
                    <li>Robustez contra outliers</li>
                    <li>Menos propenso a overfitting</li>
                    <li>Feature importance interpretável</li>
                </ul>
                <p><strong>Vantagem:</strong> Estabilidade e robustez</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="model-card">
                <h2 style="color: #E67E22;">Gradient Boosting</h2>
                <p><strong>Por que escolhemos:</strong></p>
                <ul>
                    <li>Corrige erros sequencialmente</li>
                    <li>Alta precisão</li>
                    <li>Bom para datasets pequenos</li>
                    <li>Boosting de desempenho</li>
                </ul>
                <p><strong>Vantagem:</strong> Performance consistente</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="background: #F8F9FA; padding: 1rem; border-radius: 12px; text-align: center;">
            <h3>🎯 Ensemble Model</h3>
            <p>Combina os 3 modelos com pesos dinâmicos baseados no desempenho → <strong>Redução de 15-20% no erro</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def slide_6_metrics():
    """Slide 6: Performance Metrics"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        st.markdown('<h1 class="slide-title">Métricas de Avaliação</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="stat-card">
                <p class="big-number">R² > 0.85</p>
                <p><strong>R² Score</strong> - 85-95% da variância explicada</p>
                <p><small>Quanto maior, melhor o modelo explica os dados</small></p>
            </div>
            
            <div class="stat-card">
                <p class="big-number">RMSE < 0.08</p>
                <p><strong>RMSE</strong> - Erro quadrático médio em NDVI</p>
                <p><small>Penaliza erros grandes</small></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card">
                <p class="big-number">MAE < 0.06</p>
                <p><strong>MAE</strong> - Erro absoluto médio</p>
                <p><small>Fácil interpretação em unidades de NDVI</small></p>
            </div>
            
            <div class="stat-card">
                <p class="big-number">Gap < 15%</p>
                <p><strong>Overfitting Gap</strong> - Diferença treino/teste</p>
                <p><small>Garante que o modelo generaliza bem</small></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1A4D3E 0%, #2C7A47 100%); padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
            <h3 style="color: white;"> Validação Robusta</h3>
            <p>Treino: 2018-2023 (6 anos) | Teste: 2024-2026 (2 anos)</p>
            <p><small>Time series split - sem data leakage</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def slide_7_results():
    """Slide 7: Expected Results"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        st.markdown('<h1 class="slide-title">Resultados Esperados</h1>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="text-align: center;">
                <p style="font-size: 4rem;">📈</p>
                <p class="big-number">+20-30%</p>
                <p><strong>Aumento na Produtividade</strong></p>
                <p>por hectare</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center;">
                <p style="font-size: 4rem;">💧</p>
                <p class="big-number">-15-25%</p>
                <p><strong>Redução no Uso de Água</strong></p>
                <p>com irrigação otimizada</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center;">
                <p style="font-size: 4rem;">🌱</p>
                <p class="big-number">-20%</p>
                <p><strong>Redução em Fertilizantes</strong></p>
                <p>aplicação precisa</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="stat-card">
                <h3>✅ Benefícios para Agricultores</h3>
                <ul>
                    <li>Recomendações claras e acionáveis</li>
                    <li>Plataforma funcional mesmo offline</li>
                    <li>Redução de custos de insumos</li>
                    <li>Melhor planejamento de safra</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card">
                <h3>🌍 Impacto</h3>
                <ul>
                    <li>Segurança alimentar melhorada</li>
                    <li>Agricultura climática inteligente</li>
                    <li>Modernização do setor agrícola</li>
                    <li>Alinhamento com ODS</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def slide_8_demo():
    """Slide 8: Demo"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        st.markdown('<h1 class="slide-title">Demonstração</h1>', unsafe_allow_html=True)
        
        st.info("📱 **Pronto para Demonstração ao Vivo**")
        
        st.markdown("""
        <div style="margin-top: 2rem;">
            <h3>Funcionalidades da Plataforma:</h3>
            <ul>
                <li>📊 Análise NDVI com múltiplos colormaps (RdYlGn, Spectral, Viridis)</li>
                <li>🌡️ Dados climáticos históricos e previsões</li>
                <li>🌱 Análise de umidade do solo</li>
                <li>🤖 Previsões NDVI com modelos XGBoost Ensemble</li>
                <li>🌽 Recomendações de cultivo por mês</li>
                <li>📅 Calendário de plantio inteligente</li>
                <li>📊 Visualizações interativas com Plotly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: #E8F0EA; padding: 1rem; border-radius: 12px;">
                <h4>📊 Dashboard Principal</h4>
                <p>Análise mensal de clima e vegetação</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #E8F0EA; padding: 1rem; border-radius: 12px;">
                <h4>🔮 Previsões 2026-2027</h4>
                <p>Forecast NDVI com intervalos de confiança</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def slide_9_next_steps():
    """Slide 9: Next Steps"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        st.markdown('<h1 class="slide-title">Próximos Passos</h1>', unsafe_allow_html=True)
        
        timeline = [
            ("✅", "Plataforma Funcional", "Completo", "#2C7A47"),
            ("🔄", "Teste Piloto", "Em andamento", "#E67E22"),
            ("📊", "Coleta de Feedback", "Aguardando", "#3498DB"),
            ("🌍", "Expansão Regional", "Planejado", "#3498DB"),
            ("📱", "App Mobile Offline", "Em desenvolvimento", "#E67E22"),
            ("📈", "Escala Nacional", "2027", "#1A4D3E")
        ]
        
        for icon, task, status, color in timeline:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 1rem 0; padding: 1rem; background: #F8F9FA; border-radius: 12px; border-left: 4px solid {color};">
                <span style="font-size: 2rem; margin-right: 1rem;">{icon}</span>
                <div style="flex: 1;">
                    <strong style="font-size: 1.1rem;">{task}</strong>
                    <br>
                    <small>Status: {status}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h3>📅 Cronograma</h3>
            <p><strong>Q1-Q2 2026:</strong> Teste piloto em Chokwe, Gaza</p>
            <p><strong>Q3-Q4 2026:</strong> Avaliação e melhorias</p>
            <p><strong>2027:</strong> Expansão para outras províncias</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def slide_10_thanks():
    """Slide 10: Thank You"""
    with create_slide_container():
        st.markdown('<div class="presentation-slide">', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <p style="font-size: 5rem;">🌾</p>
            <h1 class="slide-title">Obrigado!</h1>
            <p style="font-size: 1.2rem;">Vamos juntos transformar a agricultura em Moçambique</p>
            
            <hr style="margin: 2rem auto; width: 50%;">
            
            <div style="margin-top: 2rem;">
                <p><strong>📧 Email:</strong> AgriSense.africa@gmail.com</p>
                <p><strong>📱 Telefone:</strong> +258841349563</p>
                <p><strong>🌐 Website:</strong> www.agrisense.africa</p>
                <p><strong>📍 Região Piloto:</strong> Chokwe, Gaza, Moçambique</p>
            </div>
            
            <hr style="margin: 2rem auto; width: 50%;">
            
            <p style="font-size: 0.9rem; color: #666;">
                "Turning Farm Data into Better Harvests"
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main presentation function"""
    
    # Initialize session state for slide navigation
    if 'slide' not in st.session_state:
        st.session_state.slide = 0
    
    slides = [
        ("🌾", slide_1_title),
        ("❓", slide_2_problem),
        ("💡", slide_3_solution),
        ("🏗️", slide_4_architecture),
        ("🤖", slide_5_models),
        ("📊", slide_6_metrics),
        ("📈", slide_7_results),
        ("🎬", slide_8_demo),
        ("🚀", slide_9_next_steps),
        ("🙏", slide_10_thanks)
    ]
    
    # Navigation buttons
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
    with col1:
        if st.session_state.slide > 0:
            if st.button("◀ Anterior", use_container_width=True):
                st.session_state.slide -= 1
                st.rerun()
    
    with col2:
        st.markdown(f"<p style='text-align: center;'><strong>Slide {st.session_state.slide + 1} de {len(slides)}</strong></p>", unsafe_allow_html=True)
    
    with col3:
        # Progress bar
        progress = (st.session_state.slide + 1) / len(slides)
        st.progress(progress)
    
    with col4:
        if st.session_state.slide < len(slides) - 1:
            if st.button("Próximo ▶", use_container_width=True):
                st.session_state.slide += 1
                st.rerun()
    
    with col5:
        # Slide indicators
        dots = ""
        for i in range(len(slides)):
            if i == st.session_state.slide:
                dots += "● "
            else:
                dots += "○ "
        st.markdown(f"<p style='text-align: right;'>{dots}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display current slide
    slides[st.session_state.slide][1]()

if __name__ == "__main__":
    main()