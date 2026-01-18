import streamlit as st
import pandas as pd
import numpy as np

# 1. ESTILO E CONFIGURAÇÃO
st.set_page_config(page_title="SAPEM | INTELLIGENCE BI", layout="wide")

# Forçar remoção de estilos que causam erro com tradutor
st.markdown("""<style> .stMetric { border: 1px solid #ddd; padding: 10px; border-radius: 5px; } </style>""", unsafe_allow_name=True)

# 2. CONEXÃO COM O BANCO DE DADOS (Captura 6794)
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=2)
def carregar_dados():
    try:
        # Lê o CSV e garante que os nomes das colunas não tenham espaços
        df = pd.read_csv(URL)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame({"Equipa": ["Carregando..."], "Pts": [0]})

df = carregar_dados()

# 3. NAVEGAÇÃO (Capturas 6811/6809)
st.sidebar.title("🎮 PAINEL DE CONTROLO")
mod = st.sidebar.selectbox("Modalidade", ["Futebol ⚽", "Basquetebol 🏀"])
liga = st.sidebar.selectbox("Liga", ["Liga Portugal", "Girabola", "Premier League"])
menu = st.sidebar.radio("Nível de Análise", ["📅 Dashboard", "🔬 Deep Analysis (Módulos I-V)", "🌡️ Fatores Externos"])

# 4. MÓDULO: DEEP ANALYSIS (Onde estão os teus dados reais)
if menu == "🔬 Deep Analysis (Módulos I-V)":
    st.title("🔬 Painel de Informações Atualizadas")
    
    # Seleção de Equipas da sua lista real
    lista_equipas = df["Equipa"].tolist()
    col1, col2 = st.columns(2)
    with col1: casa = st.selectbox("Equipa Casa", lista_equipas, index=0)
    with col2: fora = st.selectbox("Equipa Fora", lista_equipas, index=1 if len(lista_equipas)>1 else 0)

    aba1, aba2, aba3 = st.tabs(["📊 Performance (Mód. III/IV)", "🎯 Inteligência (Mód. V)", "📜 H2H"])

    with aba1:
        st.subheader("KPIs de Desempenho (Dados Sincronizados)")
        
        def display_stats(nome_equipa):
            # Puxa a linha da equipa selecionada
            stats = df[df["Equipa"] == nome_equipa].iloc[0].fillna(0)
            st.markdown(f"📊 **{nome_equipa}**")
            k1, k2, k3, k4 = st.columns(4)
            # Conecta com os nomes exatos das tuas colunas no Google Sheets
            k1.metric("Média Cantos", stats.get('Cantos', 0))
            k2.metric("Média Cartões", stats.get('Cartões', 0))
            k3.metric("Remates", stats.get('Remates', 0))
            k4.metric("Golos Marc.", stats.get('Golos Marcados', 0))

        display_stats(casa)
        st.divider()
        display_stats(fora)

    with aba2:
        st.subheader("🎯 Probabilidades Preditivas")
        pts_casa = df[df["Equipa"] == casa]["Pts"].iloc[0]
        pts_fora = df[df["Equipa"] == fora]["Pts"].iloc[0]
        total = pts_casa + pts_fora if (pts_casa + pts_fora) > 0 else 1
        prob = (pts_casa / total) * 100
        
        st.write(f"Chance de Vitória {casa}: **{prob:.1f}%**")
        st.progress(int(prob))

# 5. OUTROS MÓDULOS (Dashboard e Contexto)
elif menu == "📅 Dashboard":
    st.subheader("📈 Classificação Geral")
    st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "🌡️ Fatores Externos":
    st.subheader("⛈️ Contexto & Momentum")
    c1, c2 = st.columns(2)
    with c1:
        st.select_slider("Tempo", ["Sol", "Chuva", "Chuva Forte"])
        st.number_input("Altitude (m)", value=0)
    with c2:
        st.line_chart(np.random.randn(10, 2))
