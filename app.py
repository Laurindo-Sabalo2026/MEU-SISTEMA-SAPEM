import streamlit as st
import requests
import pandas as pd

# 1. Configuração e Estética SAPEM ELITE
st.set_page_config(page_title="SAPEM | ELITE 2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1a1c24; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111217; border-right: 1px solid #343a40; }
    
    /* Cartões de Métricas Estilizados */
    div[data-testid="metric-container"] {
        background-color: #262932;
        padding: 25px;
        border-radius: 15px;
        border-bottom: 4px solid #007bff;
        transition: 0.3s;
    }
    div[data-testid="metric-container"]:hover { transform: translateY(-5px); background-color: #2e323d; }
    
    [data-testid="stMetricLabel"] { color: #888ea8 !important; font-size: 14px !important; text-transform: uppercase; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800 !important; }
    
    /* Tabela e Cabeçalhos */
    h1, h2, h3 { font-family: 'Inter', sans-serif; letter-spacing: -1px; }
    .stDataFrame { border: 1px solid #343a40; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Configurações de Acesso
token = "d63fcb8845c2461da566eed3df05770e"
headers = {'X-Auth-Token': token}

# 3. Sidebar Profissional
st.sidebar.markdown("<h1 style='text-align: center; color: #007bff;'>SAPEM</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #666;'>Inteligência Esportiva v2.0</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

liga_nome = st.sidebar.selectbox("MODALIDADE / LIGA", ["Premier League", "Liga Portuguesa", "La Liga (Espanha)"])

config = {
    "Premier League": {"id": "PL", "cor": "#3d195d"},
    "Liga Portuguesa": {"id": "PPL", "cor": "#005baa"},
    "La Liga (Espanha)": {"id": "PD", "cor": "#ee1c2e"}
}

# 4. Funções de Busca
@st.cache_data
def carregar_dados_sapem(endpoint):
    url = f"https://api.football-data.org/v4/competitions/{config[liga_nome]['id']}/{endpoint}"
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except: return None

# 5. Topo: Próximos Jogos (Baseado na imagem de referência)
st.markdown(f"### 🗓️ Agenda de Jogos: {liga_nome}")
jogos_data = carregar_dados_sapem("matches?status=SCHEDULED")
if jogos_data and 'matches' in jogos_data and len(jogos_data['matches']) > 0:
    proximo = jogos_data['matches'][0]
    st.info(f"⚽ **DESTAQUE:** {proximo['homeTeam']['name']} vs {proximo['awayTeam']['name']} | 📅 {proximo['utcDate'][:10]}")
else:
    st.write("Sem jogos agendados para os próximos dias.")

st.markdown("---")

# 6. Conteúdo Principal
standings = carregar_dados_sapem("standings")
if standings and 'standings' in standings:
    df = pd.DataFrame(standings['standings'][0]['table'])
    df['Equipa'] = df['team'].apply(lambda x: x['name'])
    
    col_l, col_r = st.columns([1, 1.2])
    
    with col_l:
        st.markdown("### 🏆 CLASSIFICAÇÃO ATUAL")
        st.dataframe(df[['position', 'Equipa', 'points']].set_index('position'), use_container_width=True, height=400)
        
    with col_r:
        st.markdown("### 🔍 RAIO-X DE PERFORMANCE")
        time = st.selectbox("Selecione o Alvo:", df['Equipa'].tolist())
        stats = df[df['Equipa'] == time].iloc[0]
        
        m1, m2 = st.columns(2); m3, m4 = st.columns(2)
        m1.metric("VITÓRIAS", stats['won'])
        m2.metric("GOLOS / JOGO", f"{stats['goalsFor']/stats['playedGames']:.2f}")
        m3.metric("DEFESA (MÉDIA)", f"{stats['goalsAgainst']/stats['playedGames']:.2f}")
        m4.metric("APROVEITAMENTO", f"{(stats['points']/(stats['playedGames']*3))*100:.1f}%")
        
        st.markdown("---")
        st.success(f"📈 **RELATÓRIO FINAL:** O {time} ocupa a {stats['position']}ª posição com {stats['points']} pontos.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 SAPEM Intelligence Systems")
