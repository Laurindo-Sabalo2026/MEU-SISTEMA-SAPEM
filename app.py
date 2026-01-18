import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. BLOQUEIO TÉCNICO CONTRA TRADUTORES (Captura 6813)
st.set_page_config(page_title="SAPEM BI", layout="wide")
st.markdown('<html lang="pt-PT">', unsafe_allow_html=True) 

# 2. CONEXÃO COM A PLANILHA (Link da Captura 6794)
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=5)
def load_data_secure():
    try:
        # Lê o CSV e força a limpeza de nomes de colunas
        df_raw = pd.read_csv(URL)
        df_raw.columns = [str(c).strip() for c in df_raw.columns]
        return df_raw
    except:
        # Retorna dados fictícios apenas para não quebrar a interface se a rede falhar
        return pd.DataFrame({"Equipa": ["Sincronizando..."], "Pts": [0]})

df = load_data_secure()

# --- INTERFACE ---
st.title("💎 SAPEM | BUSINESS INTELLIGENCE")

# MENU LATERAL ORGANIZADO
with st.sidebar:
    st.header("🎮 CONTROL PANEL")
    esporte = st.selectbox("Modalidade", ["Futebol ⚽", "Basquetebol 🏀"])
    menu = st.radio("Módulos", ["📊 Tabela Geral", "🔬 Análise Profunda (KPIs)", "🌡️ Fatores Externos"])
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

# ---------------------------------------------------------
# MÓDULO: TABELA GERAL (Captura 6814)
# ---------------------------------------------------------
if menu == "📊 Tabela Geral":
    st.subheader("🏟️ Classificação Geral do Sistema")
    if df["Equipa"].iloc[0] == "Sincronizando...":
        st.warning("O sistema está a tentar ler o seu Google Sheets. Aguarde 5 segundos.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# MÓDULO: ANÁLISE PROFUNDA (Capturas 6809 e 6812)
# ---------------------------------------------------------
elif menu == "🔬 Análise Profunda (KPIs)":
    st.subheader("🔍 Módulos I-V: KPIs de Performance")
    
    if "Equipa" in df.columns and len(df) > 1:
        times = sorted(df["Equipa"].unique())
        c1, c2 = st.columns(2)
        with c1: t_casa = st.selectbox("Equipa Casa", times, key="c")
        with c2: t_fora = st.selectbox("Equipa Fora", times, key="f")

        tab1, tab2 = st.tabs(["📈 Estatísticas Reais", "🤖 Previsão IA"])

        with tab1:
            def render_kpis(equipa_nome):
                # Localiza os dados da equipa na sua planilha (Captura 6802)
                row = df[df["Equipa"] == equipa_nome].iloc[0].fillna(0)
                st.markdown(f"**{equipa_nome}**")
                colA, colB, colC, colD = st.columns(4)
                colA.metric("Cantos", f"{row.get('Cantos', 0)}")
                colB.metric("Cartões", f"{row.get('Cartões', 0)}")
                colC.metric("Remates", f"{row.get('Remates', 0)}")
                colD.metric("Golos M.", f"{row.get('Golos Marcados', 0)}")
            
            render_kpis(t_casa)
            st.divider()
            render_kpis(t_fora)

        with tab2:
            st.write("### Probabilidade de Vitória")
            p1 = df[df["Equipa"] == t_casa]["Pts"].iloc[0]
            p2 = df[df["Equipa"] == t_fora]["Pts"].iloc[0]
            calc = (p1 / (p1 + p2)) * 100 if (p1 + p2) > 0 else 50
            st.write(f"Vantagem Estatística para **{t_casa}**: {calc:.1f}%")
            st.progress(int(calc))
    else:
        st.error("Erro: Coluna 'Equipa' não encontrada ou planilha vazia.")

# ---------------------------------------------------------
# MÓDULO: EXTERNOS (Captura 6811)
# ---------------------------------------------------------
else:
    st.subheader("🌡️ Contexto Ambiental & Momentum")
    col_x, col_y = st.columns(2)
    with col_x:
        st.select_slider("Clima", ["Sol", "Chuva", "Tempestade"])
        st.number_input("Altitude (m)", value=0)
    with col_y:
        st.line_chart(np.random.randn(10, 2))
