import streamlit as st
import requests
import pandas as pd

# Configuração Base
st.set_page_config(page_title="SAPEM | INTELLIGENCE", layout="wide")

# Estilo para esconder erros técnicos do utilizador
st.markdown("<style>.stException {display:none;} </style>", unsafe_allow_html=True)

# Sua chave real do painel API-Football
API_KEY = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"
headers = {'x-apisports-key': API_KEY}

st.sidebar.title("💎 SAPEM v5.3")
liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA", ["Premier League", "Liga Portugal", "La Liga"])
mapa_ligas = {"Premier League": 39, "Liga Portugal": 94, "La Liga": 140}

@st.cache_data(ttl=300)
def fetch_data(league_id):
    # Tenta 2024 primeiro, depois 2023 como backup automático
    for ano in [2024, 2023]:
        url = f"https://v3.football.api-sports.io/standings?league={league_id}&season={ano}"
        try:
            res = requests.get(url, headers=headers, timeout=10).json()
            if res.get('response'):
                return res['response'][0]['league']['standings'][0], ano
        except:
            continue
    return None, None

st.title("📑 DEEP ANALYSIS & PREDICTIONS")

dados, ano_ativo = fetch_data(mapa_ligas[liga_nome])

if dados:
    st.success(f"Dados carregados com sucesso (Temporada {ano_ativo})")
    df = pd.DataFrame([{
        "Pos": i['rank'], "Equipa": i['team']['name'], 
        "Pts": i['points'], "J": i['all']['played']
    } for i in dados])
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.dataframe(df.set_index('Pos'), use_container_width=True)
    with col2:
        equipa = st.selectbox("Análise Detalhada:", df['Equipa'].tolist())
        st.info(f"Módulo III: Tendência de Cantos para {equipa} em processamento...")
else:
    st.warning("⚠️ A sua chave de API ainda está em processo de ativação pelo servidor.")
    st.info("Isto demora geralmente 30 a 60 minutos após o registo. Por favor, tente atualizar a página daqui a pouco.")
    # Debug para você ver o que a API está respondendo
    test_req = requests.get("https://v3.football.api-sports.io/status", headers=headers).json()
    st.write("Estado da Chave:", test_req.get('errors', 'Sem erros reportados'))
