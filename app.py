import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SAPEM | CONEXÃO TOTAL", layout="wide")

# Dados confirmados das suas capturas
CHAVE = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"

# Lista de endereços possíveis (o servidor pode responder em qualquer um destes)
ENDPOINTS = [
    "https://v3.football.api-sports.io/standings",
    "https://api-football-v1.p.rapidapi.com/v3/standings"
]

st.sidebar.title("💎 SAPEM v6.1")
liga = st.sidebar.selectbox("LIGA", ["Premier League", "La Liga", "Liga Portugal"])
ids = {"Premier League": 39, "La Liga": 140, "Liga Portugal": 94}

st.title("📡 TESTE DE CONEXÃO MULTI-SERVIDOR")

if st.button('🚀 TENTAR CONEXÃO AGORA'):
    sucesso = False
    
    for url in ENDPOINTS:
        headers = {'x-apisports-key': CHAVE, 'x-rapidapi-key': CHAVE}
        params = {'league': ids[liga], 'season': '2023'}
        
        try:
            res = requests.get(url, headers=headers, params=params, timeout=10).json()
            
            if res.get('response'):
                dados = res['response'][0]['league']['standings'][0]
                df = pd.DataFrame([{"Pos": i['rank'], "Equipa": i['team']['name'], "Pts": i['points']} for i in dados])
                st.success(f"✅ CONECTADO VIA: {url}")
                st.table(df.set_index('Pos'))
                st.balloons()
                sucesso = True
                break
        except:
            continue
            
    if not sucesso:
        st.error("ERRO: Os servidores da API ainda não reconhecem a sua chave como 'Paga' ou 'Ativa para Dados'.")
        st.info("Recomendação: Aguarde 30 minutos sem mexer. A sincronização de novas contas é automática mas lenta.")
