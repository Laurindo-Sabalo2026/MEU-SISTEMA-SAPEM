import streamlit as st
import pandas as pd
import numpy as np

# 1. PROTEÇÃO CONTRA TRADUTOR E CONFIGURAÇÃO
st.set_page_config(page_title="SAPEM BI", layout="wide")

# 2. LINK DA PLANILHA (Certifique-se de que é o link CSV da captura 6794)
URL_BASE = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=2)
def carregar_dados_sapem():
    try:
        # Tenta ler a planilha ignorando erros de SSL ou cache
        df = pd.read_csv(URL_BASE, on_bad_lines='skip', storage_options={'User-Agent': 'Mozilla/5.0'})
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        # Se falhar, mostra o erro técnico para sabermos o que é
        st.error(f"Erro de Conexão: {e}")
        return pd.DataFrame({"Equipa": ["Erro"], "Pts": [0], "Cantos": [0], "Cartões": [0]})

df = carregar_dados_sapem()

# --- INTERFACE PROFISSIONAL ---
st.title("💎 SAPEM | BUSINESS INTELLIGENCE")

with st.sidebar:
    st.header("⚙️ CONTROL PANEL")
    menu = st.radio("Módulos", ["📊 Tabela Geral", "🔬 Deep Analysis", "🌡️ Fatores Externos"])
    if st.button("🔄 Forçar Sincronização"):
        st.cache_data.clear()
        st.rerun()

# --- MÓDULO 1: TABELA GERAL ---
if menu == "📊 Tabela Geral":
    st.subheader("🏟️ Dados Sincronizados")
    if not df.empty and df["Equipa"].iloc[0] != "Erro":
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("A ligar ao Google Sheets... Se demorar, verifique se a planilha está 'Publicada na Web'.")

# --- MÓDULO 2: DEEP ANALYSIS ---
elif menu == "🔬 Deep Analysis":
    if "Equipa" in df.columns and len(df) > 1:
        equipes = sorted(df["Equipa"].unique())
        c1, c2 = st.columns(2)
        with c1: casa = st.selectbox("Casa", equipes)
        with c2: fora = st.selectbox("Fora", equipes)

        # KPIs Reais da Captura 6802
        def mostrar_bi(nome):
            dado = df[df["Equipa"] == nome].iloc[0]
            st.markdown(f"📊 **{nome}**")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Cantos", dado.get("Cantos", 0))
            k2.metric("Cartões", dado.get("Cartões", 0))
            k3.metric("Remates", dado.get("Remates", 0))
            k4.metric("Golos M.", dado.get("Golos Marcados", 0))
        
        mostrar_bi(casa)
        st.divider()
        mostrar_bi(fora)
    else:
        st.warning("Dados insuficientes para análise profunda.")

# --- MÓDULO 3: EXTERNOS ---
else:
    st.subheader("🌡️ Clima & Tendência")
    st.line_chart(np.random.randn(10, 2))
