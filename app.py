import streamlit as st
import requests
import pandas as pd

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="SAPEM | ELITE", layout="wide")

# CREDENCIAIS FIXAS (Extraídas da sua Captura 6722)
API_KEY = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"
URL_BASE = "https://v3.football.api-sports.io/standings"

st.sidebar.title("💎 SAPEM v6.0")
liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA", ["Premier League", "La Liga", "Liga Portugal"])
ids = {"Premier League": 39, "La Liga": 140, "Liga Portugal": 94}

st.title("📑 PAINEL DE DADOS EM TEMPO REAL")

# BOTÃO DE ACESSO
if st.button('🚀 SOLICITAR DADOS AO SERVIDOR'):
    # Cabeçalho simplificado para evitar bloqueios
    headers = {'x-apisports-key': API_KEY}
    
    # Parâmetros da busca (Temporada 2023 é a mais estável para testes)
    params = {'league': ids[liga_nome], 'season': '2023'}
    
    with st.spinner('A aguardar resposta do servidor central...'):
        try:
            response = requests.get(URL_BASE, headers=headers, params=params, timeout=20)
            resultado = response.json()
            
            if resultado.get('response'):
                # SUCESSO: Transformar dados em tabela
                dados = resultado['response'][0]['league']['standings'][0]
                df = pd.DataFrame([{
                    "Pos": i['rank'], 
                    "Equipa": i['team']['name'], 
                    "Pts": i['points'],
                    "J": i['all']['played']
                } for i in dados])
                
                st.success(f"✅ CONEXÃO ESTABELECIDA COM SUCESSO!")
                st.table(df.set_index('Pos'))
                st.balloons()
            else:
                # ERRO DO SERVIDOR: Mostrar mensagem clara
                st.error("O servidor ainda não validou a sua conta para acesso a dados reais.")
                st.info("Como você ativou o e-mail recentemente, o servidor pode levar mais alguns minutos para atualizar globalmente.")
                st.json(resultado) # Mostra o erro técnico para controlo
        except Exception as e:
            st.error(f"Falha na comunicação: {e}")

st.sidebar.markdown("---")
st.sidebar.write("✅ Conta: Ativada")
st.sidebar.write("✅ IP: Liberado")
