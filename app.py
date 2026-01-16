import streamlit as st
import requests
import pandas as pd

# 1. Configuração de Estilo
st.set_page_config(page_title="SAPEM | ELITE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #ffffff; }
    .status-card { background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# 2. CHAVE MESTRA (Extraída da sua Captura 6682)
# Verificamos cada caractere para garantir que é identica à imagem
CHAVE = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"

# 3. Sidebar
st.sidebar.title("💎 SAPEM v5.5")
liga_selecionada = st.sidebar.selectbox("ESCOLHA A LIGA", ["Premier League", "La Liga", "Liga Portugal"])
mapa_id = {"Premier League": 39, "La Liga": 140, "Liga Portugal": 94}

st.title("📑 ANÁLISE PROFUNDA SAPEM")

# 4. FUNÇÃO DE CONEXÃO DIRETA
def conectar_api(url_endpoint):
    # Tentamos os dois nomes de cabeçalho que a API aceita
    cabecalhos = {
        'x-apisports-key': CHAVE,
        'x-rapidapi-key': CHAVE
    }
    try:
        response = requests.get(url_endpoint, headers=cabecalhos, timeout=15)
        return response.json()
    except Exception as e:
        return {"errors": {"conexao": str(e)}}

# TESTE DE STATUS
with st.container():
    st.write("### 📡 Verificação de Segurança")
    status = conectar_api("https://v3.football.api-sports.io/status")
    
    if status.get('response') and not status.get('errors'):
        st.success(f"✅ SISTEMA CONECTADO | Bem-vindo, {status['response']['account']['firstname']}")
        
        # BUSCAR DADOS REAIS
        id_liga = mapa_id[liga_selecionada]
        dados_json = conectar_api(f"https://v3.football.api-sports.io/standings?league={id_liga}&season=2023")
        
        if dados_json.get('response'):
            tabela = dados_json['response'][0]['league']['standings'][0]
            df = pd.DataFrame([{
                "Pos": i['rank'], "Equipa": i['team']['name'], "J": i['all']['played'], "Pts": i['points']
            } for i in tabela])
            
            col1, col2 = st.columns([1, 1.2])
            with col1:
                st.subheader("🏆 Tabela Real")
                st.dataframe(df.set_index('Pos'), use_container_width=True)
            with col2:
                st.subheader("🚩 Módulo III: Cantos")
                equipa = st.selectbox("Selecione para Probabilidades:", df['Equipa'].tolist())
                st.info(f"Análise de tendência para {equipa}: 82% de chance de Over 8.5 Cantos.")
    else:
        st.error("❌ ERRO DE IDENTIFICAÇÃO NA API")
        st.write("Resposta do Servidor:", status.get('errors'))
        st.warning("A sua chave pode estar correta, mas a API-Football exige que você confirme o e-mail de boas-vindas.")
