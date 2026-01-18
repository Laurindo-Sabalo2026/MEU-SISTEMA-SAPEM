import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(page_title="SAPEM PRO", layout="wide")

# O LINK DA SUA CAPTURA 6820
URL_BRUTA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=5)
def carregar_dados():
    try:
        # Força a conexão externa para evitar o Erro de Sincronização (Captura 6824)
        cabecalho = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(URL_BRUTA, headers=cabecalho, timeout=10)
        if resposta.status_code == 200:
            df = pd.read_csv(StringIO(resposta.text))
            df.columns = [str(c).strip() for c in df.columns]
            return df
        return None
    except:
        return None

df = carregar_dados()

st.title("💎 PORTAL SAPEM PROFISSIONAL")

if df is not None:
    st.success("✅ Sistema Online e Sincronizado!")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.error("❌ Erro de Sincronização.")
    st.info("Verifique se o arquivo requirements.txt contém a palavra 'requests'.")
