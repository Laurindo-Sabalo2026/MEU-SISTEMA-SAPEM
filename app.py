import streamlit as st
import requests
import pandas as pd

# Configuração de Interface
st.set_page_config(page_title="SAPEM | FORÇA BRUTA", layout="wide")

# A sua chave confirmada na Captura 6682
CHAVE_MESTRA = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"

# Tentativa de cabeçalhos múltiplos para forçar a entrada
headers = {
    'x-apisports-key': CHAVE_MESTRA,
    'x-rapidapi-key': CHAVE_MESTRA,
    'Authorization': CHAVE_MESTRA
}

st.sidebar.title("💎 SAPEM v5.4")
liga_nome = st.sidebar.selectbox("LIGA", ["Premier League", "Liga Portugal", "La Liga"])
mapa_ligas = {"Premier League": 39, "Liga Portugal": 94, "La Liga": 140}

st.title("📑 ANÁLISE PROFUNDA SAPEM")

# PASSO 1: TESTE DE STATUS DA CHAVE
st.subheader("📡 Status da Ligação")
try:
    check = requests.get("https://v3.football.api-sports.io/status", headers=headers, timeout=10).json()
    if check.get('response') and not check.get('errors'):
        st.success(f"✅ CONECTADO! Usuário: {check['response']['account']['firstname']}")
        
        # PASSO 2: CARREGAR DADOS SE O STATUS FOR POSITIVO
        url_dados = f"https://v3.football.api-sports.io/standings?league={mapa_ligas[liga_nome]}&season=2023"
        res_dados = requests.get(url_dados, headers=headers).json()
        
        if res_dados.get('response'):
            dados = res_dados['response'][0]['league']['standings'][0]
            df = pd.DataFrame([{"Pos": i['rank'], "Equipa": i['team']['name'], "Pts": i['points']} for i in dados])
            st.table(df.head(10))
        else:
            st.warning("Chave ativa, mas sem dados para esta liga específica.")
            
    else:
        st.error("❌ ERRO DE IDENTIFICAÇÃO")
        st.write("O servidor diz:", check.get('errors'))
        st.info("DICA: Entre no site da API-Football e verifique se o seu 'Dashboard' tem algum aviso de conta suspensa ou pendente.")

except Exception as e:
    st.error(f"Erro de Conexão Crítico: {e}")
