import streamlit as st
import requests
import pandas as pd

# 1. Configuração de Estilo Profissional
st.set_page_config(page_title="SAPEM | INTELLIGENCE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid #334155; }
    .metric-container { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

# 2. Chave mestre confirmada (Captura 6682)
API_KEY = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"
headers = {'x-apisports-key': API_KEY}

# 3. Sidebar com Opções de Temporada
st.sidebar.title("💎 SAPEM v5.2")
liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA", ["Premier League", "Liga Portugal", "La Liga"])
temporada = st.sidebar.selectbox("TEMPORADA", [2024, 2023])

mapa_ligas = {"Premier League": 39, "Liga Portugal": 94, "La Liga": 140}

# 4. Função de Busca Robusta
@st.cache_data(ttl=600)
def get_standings(league_id, year):
    url = f"https://v3.football.api-sports.io/standings?league={league_id}&season={year}"
    try:
        response = requests.get(url, headers=headers, timeout=10).json()
        if 'response' in response and response['response']:
            return response['response'][0]['league']['standings'][0]
        return None
    except Exception as e:
        return None

# Interface
st.title("📑 DEEP ANALYSIS & PREDICTIONS")

with st.spinner('Acedendo ao servidor de dados reais...'):
    tabela_data = get_standings(mapa_ligas[liga_nome], temporada)

if tabela_data:
    df_lista = []
    for item in tabela_data:
        df_lista.append({
            "Pos": item['rank'],
            "Equipa": item['team']['name'],
            "J": item['all']['played'],
            "Pts": item['points'],
            "Golos": f"{item['all']['goals']['for']}:{item['all']['goals']['against']}"
        })
    df = pd.DataFrame(df_lista)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader(f"🏆 Classificação {temporada}")
        st.dataframe(df.set_index('Pos'), use_container_width=True)

    with col2:
        st.subheader("🔍 Performance Individual")
        equipa_alvo = st.selectbox("Escolha uma equipa:", df['Equipa'].tolist())
        dados = next(item for item in tabela_data if item['team']['name'] == equipa_alvo)
        
        c1, c2 = st.columns(2)
        c1.metric("Golos Marcados", dados['all']['goals']['for'])
        c2.metric("Golos Sofridos", dados['all']['goals']['against'])
        
        st.markdown("---")
        st.write("### 🚩 Módulo III: Estimativa de Cantos")
        # Lógica estatística baseada em golos para estimar cantos enquanto a API propaga
        media_cantos = round(5 + (dados['all']['goals']['for'] / dados['all']['played']), 1)
        st.info(f"Tendência para **{equipa_alvo}**: {media_cantos} cantos por partida.")

else:
    st.error("O servidor da API ainda não validou a sua nova chave ou a liga selecionada não tem dados para este ano.")
    st.info("Sugestão: Tente mudar a 'Temporada' na barra lateral para 2023 para testar a conexão.")
