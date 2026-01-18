import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="PORTAL SAPEM", layout="wide")

# 2. LINK DA SUA CAPTURA 6820 (CORRIGIDO COM ASPAS)
URL_DADOS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=5)
def puxar_dados():
    try:
        # Lê o CSV da sua planilha
        df = pd.read_csv(URL_DADOS)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        return None

df_principal = puxar_dados()

# 3. LAYOUT DO PORTAL
st.title("💎 PORTAL SAPEM PROFISSIONAL")
st.markdown("---")

# MENU LATERAL
menu = st.sidebar.radio("Navegar para:", ["📊 Tabela de Classificação", "🔬 Deep Analysis (KPIs)"])

if menu == "📊 Tabela de Classificação":
    st.subheader("🏆 Classificação em Tempo Real")
    
    if df_principal is not None:
        st.dataframe(df_principal, use_container_width=True, hide_index=True)
    else:
        st.error("❌ Erro de Conexão: Verifique se a planilha está 'Publicada na Web' como CSV.")

elif menu == "🔬 Deep Analysis (KPIs)":
    st.subheader("🔍 Módulos de Performance")
    
    if df_principal is not None and "Equipa" in df_principal.columns:
        lista_equipes = df_principal["Equipa"].unique()
        escolha = st.selectbox("Selecione a Equipa", lista_equipes)
        
        info = df_principal[df_principal["Equipa"] == escolha].iloc[0]
        
        # Mostra as métricas da sua planilha (Captura 6802)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Cantos", info.get("Cantos", 0))
        c2.metric("Cartões", info.get("Cartões", 0))
        c3.metric("Remates", info.get("Remates", 0))
        c4.metric("Golos M.", info.get("Golos Marcados", 0))
    else:
        st.warning("Conecte a planilha para habilitar a análise.")

# BOTÃO DE RECARGA
if st.sidebar.button("🔄 Forçar Atualização"):
    st.cache_data.clear()
    st.rerun()
