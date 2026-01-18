import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURAÇÃO BÁSICA (Sem CSS complexo para evitar erros de tradução)
st.set_page_config(page_title="SAPEM BI", layout="wide")

st.title("💎 SAPEM | BUSINESS INTELLIGENCE")

# 2. CONEXÃO DIRETA COM OS DADOS (Link da Captura 6794)
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=5)
def load_sapem_data():
    try:
        # Carrega os dados e limpa nomes de colunas
        data = pd.read_csv(URL)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except Exception as e:
        return pd.DataFrame({"Equipa": ["Erro de Conexão"], "Pts": [0]})

df = load_sapem_data()

# 3. BARRA LATERAL (Navegação por Níveis)
st.sidebar.header("🎮 MENU DE CONTROLO")
esporte = st.sidebar.selectbox("Nível 1: Esporte", ["Futebol ⚽", "Basquetebol 🏀"])
liga = st.sidebar.selectbox("Nível 2: Liga", ["Liga Portugal", "Premier League", "Girabola"])
aba = st.sidebar.radio("Nível 3: Análise", ["📅 Geral", "🔬 Deep Analysis (H2H)", "🌡️ Clima & Tendência"])

# ---------------------------------------------------------
# MÓDULO: GERAL (Tabela Completa)
# ---------------------------------------------------------
if aba == "📅 Geral":
    st.subheader(f"🏟️ Tabela Geral: {liga}")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# MÓDULO: DEEP ANALYSIS (Módulos III, IV e V)
# ---------------------------------------------------------
elif aba == "🔬 Deep Analysis (H2H)":
    st.subheader("🔍 Painel de Análise Profunda")
    
    if "Equipa" in df.columns:
        lista = df["Equipa"].unique()
        c1, c2 = st.columns(2)
        with c1: t_casa = st.selectbox("Equipa Casa", lista, key="casa")
        with c2: t_fora = st.selectbox("Equipa Fora", lista, key="fora")

        tab_perf, tab_ia = st.tabs(["📊 Performance Reais", "🎯 Probabilidades"])

        with tab_perf:
            def plot_metrics(time):
                row = df[df["Equipa"] == time].iloc[0]
                st.write(f"### {time}")
                # Busca as colunas da sua Captura 6802
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Cantos", row.get("Cantos", 0))
                m2.metric("Cartões", row.get("Cartões", 0))
                m3.metric("Remates", row.get("Remates", 0))
                m4.metric("Golos M.", row.get("Golos Marcados", 0))
            
            plot_metrics(t_casa)
            st.divider()
            plot_metrics(t_fora)
            
        with tab_ia:
            st.write("### Análise Preditiva (IA)")
            pts_c = df[df["Equipa"] == t_casa]["Pts"].iloc[0]
            pts_f = df[df["Equipa"] == t_fora]["Pts"].iloc[0]
            calc = (pts_c / (pts_c + pts_f)) * 100 if (pts_c + pts_f) > 0 else 50
            st.write(f"Probabilidade de vitória {t_casa}: **{calc:.1f}%**")
            st.progress(int(calc))

# ---------------------------------------------------------
# MÓDULO: FATORES EXTERNOS
# ---------------------------------------------------------
else:
    st.subheader("🌡️ Clima, Altitude & Momentum")
    col_clima, col_graph = st.columns(2)
    with col_clima:
        st.select_slider("Condição", ["Sol", "Chuva", "Neve"])
        alt = st.number_input("Altitude (m)", value=0)
        if alt > 1500: st.warning("⚠️ Atenção: Performance física reduzida devido à altitude.")
    with col_graph:
        st.line_chart(np.random.randn(10, 2))
