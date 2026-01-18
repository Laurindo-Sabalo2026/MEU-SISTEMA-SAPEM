import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(page_title="PORTAL SAPEM", layout="wide")

# 2. SEU LINK DA CAPTURA 6820
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=5)
def carregar_dados_seguro():
    try:
        # Usa o 'requests' para simular um navegador e evitar o bloqueio
        response = requests.get(URL_CSV, timeout=10)
        if response.status_code == 200:
            # Transforma o texto recebido em uma tabela (DataFrame)
            dados_brutos = StringIO(response.text)
            df = pd.read_csv(dados_brutos)
            df.columns = [str(c).strip() for c in df.columns]
            return df
        else:
            return None
    except Exception:
        return None

# Tenta carregar os dados
df_sapem = carregar_dados_seguro()

# 3. INTERFACE VISUAL
st.title("💎 PORTAL SAPEM PROFISSIONAL")
st.divider()

# Menu Lateral
menu = st.sidebar.radio("Navegar:", ["📊 Classificação", "🔬 Deep Analysis"])

if menu == "📊 Classificação":
    st.subheader("🏆 Dados Sincronizados (Google Sheets)")
    
    if df_sapem is not None:
        # Exibe a tabela da sua Captura 6802
        st.dataframe(df_sapem, use_container_width=True, hide_index=True)
        st.success("✅ Conexão estabelecida com sucesso!")
    else:
        st.error("❌ Erro de Sincronização.")
        st.info("DICA: Vá ao Google Sheets, clique em 'Publicar na Web' e verifique se selecionou 'CSV'.")

else:
    st.subheader("🔍 KPIs de Desempenho")
    if df_sapem is not None and "Equipa" in df_sapem.columns:
        equipa = st.selectbox("Selecione a Equipa", df_sapem["Equipa"].unique())
        stats = df_sapem[df_sapem["Equipa"] == equipa].iloc[0]
        
        # Painel de métricas
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Cantos", stats.get("Cantos", 0))
        c2.metric("Cartões", stats.get("Cartões", 0))
        c3.metric("Remates", stats.get("Remates", 0))
        c4.metric("Golos M.", stats.get("Golos Marcados", 0))
    else:
        st.warning("Aguardando dados para análise.")

# Botão de atualização
if st.sidebar.button("🔄 Forçar Atualização"):
    st.cache_data.clear()
    st.rerun()
