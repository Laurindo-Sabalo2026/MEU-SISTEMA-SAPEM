import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SAPEM | FORÇA BRUTA", layout="wide")

# Chave confirmada
CHAVE = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"
HEADERS = {'x-apisports-key': CHAVE}

st.sidebar.title("💎 SAPEM v5.9")
liga = st.sidebar.selectbox("LIGA", ["Premier League", "La Liga", "Liga Portugal"])
ids = {"Premier League": 39, "La Liga": 140, "Liga Portugal": 94}

st.title("📑 ACESSO DIRETO AOS DADOS")

# Botão que ignora o teste de status e vai direto ao que importa
if st.button('🚀 CARREGAR DADOS DIRETAMENTE'):
    with st.spinner('Acedendo ao banco de dados principal...'):
        # Pulamos o teste de "status" e vamos direto para a classificação de 2024
        url = f"https://v3.football.api-sports.io/standings?league={ids[liga]}&season=2024"
        
        try:
            res = requests.get(url, headers=HEADERS, timeout=20).json()
            
            if res.get('response'):
                dados = res['response'][0]['league']['standings'][0]
                df = pd.DataFrame([{
                    "Pos": i['rank'], 
                    "Equipa": i['team']['name'], 
                    "Pts": i['points'],
                    "J": i['all']['played']
                } for i in dados])
                
                st.success(f"✅ DADOS CONECTADOS COM SUCESSO!")
                st.table(df.set_index('Pos'))
                st.balloons()
            else:
                # Se ainda falhar, mostramos o erro real dos dados
                st.error("O servidor de dados ainda não reconheceu a sua chave.")
                st.json(res)
        except Exception as e:
            st.error(f"Erro de conexão: {e}")

st.sidebar.warning("Nota: Se falhar na Premier League, tente mudar para 'La Liga' para testar outro servidor.")
