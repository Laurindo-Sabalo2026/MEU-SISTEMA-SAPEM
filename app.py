import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURAÇÃO DE SEGURANÇA (Imune a Tradutores)
st.set_page_config(page_title="SAPEM PRO", layout="wide")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# 2. LINK DA SUA CAPTURA 6820 (VALIDADO)
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=5) # Atualiza a cada 5 segundos
def load_data():
    try:
        # Lê os dados reais do Google Sheets
        df = pd.read_csv(URL_CSV)
        # Limpa nomes de colunas para evitar erros de leitura
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        # Se falhar, mostra o erro técnico para correção
        st.error(f"Erro ao conectar: {e}")
        return pd.DataFrame()

df = load_data()

# 3. INTERFACE VISUAL (Baseada nas capturas 6799 e 6800)
st.title("💎 PORTAL SAPEM PROFISSIONAL")
st.markdown("---")

# BARRA LATERAL
with st.sidebar:
    st.header("🎮 PAINEL DE CONTROLO")
    menu = st.radio("Navegar para:", ["📊 Tabela de Classificação", "🧮 Calculadora de Probabilidades", "🔬 Deep Analysis (KPIs)"])
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

# --- MÓDULO: TABELA (Captura 6800) ---
if menu == "📊 Tabela de Classificação":
    st.subheader("🏆 Classificação em Tempo Real")
    if not df.empty:
        # Exibe a tabela exatamente como na sua captura 6802
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Aguardando sincronização com o Google Sheets...")

# --- MÓDULO: CALCULADORA ---
elif menu == "🧮 Calculadora de Probabilidades":
    st.subheader("🎯 Inteligência Preditiva")
    if not df.empty and "Equipa" in df.columns:
        col1, col2 = st.columns(2)
        equipes = df["Equipa"].tolist()
        with col1: c_casa = st.selectbox("Equipa Casa", equipes, index=0)
        with col2: c_fora = st.selectbox("Equipa Fora", equipes, index=1 if len(equipes)>1 else 0)
        
        pts_casa = df[df["Equipa"] == c_casa]["Pts"].iloc[0]
        pts_fora = df[df["Equipa"] == c_fora]["Pts"].iloc[0]
        
        total = pts_casa + pts_fora if (pts_casa + pts_fora) > 0 else 1
        prob = (pts_casa / total) * 100
        
        st.write(f"### Probabilidade de Vitória {c_casa}: {prob:.1f}%")
        st.progress(int(prob))

# --- MÓDULO: DEEP ANALYSIS (Captura 6809) ---
else:
    st.subheader("🔬 KPIs de Desempenho (Médias Reais)")
    if not df.empty and "Equipa" in df.columns:
        sel = st.selectbox("Selecione a Equipa para BI", df["Equipa"].unique())
        dados = df[df["Equipa"] == sel].iloc[0].fillna(0)
        
        # Conecta com as colunas da Captura 6802: Cantos, Cartões, Remates, Golos
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Média Cantos", dados.get("Cantos", 0))
        k2.metric("Média Cartões", dados.get("Cartões", 0))
        k3.metric("Remates", dados.get("Remates", 0))
        k4.metric("Golos Marc.", dados.get("Golos Marcados", 0))
