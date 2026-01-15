import streamlit as st
import requests
import pandas as pd

# 1. Configuração de Estilo de Alta Fidelidade (Visual Premium)
st.set_page_config(page_title="SAPEM | ELITE", layout="wide")

st.markdown("""
    <style>
    /* Fundo Principal Azul Marinho Profundo */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    
    /* Barra Lateral Estilizada */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }

    /* Cartões de Métricas Estilo Dashboard Profissional */
    div[data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Cores dos Textos */
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #38bdf8 !important; }
    
    /* Títulos e Tabelas */
    h1, h2, h3 { color: #f8fafc !important; font-family: 'Inter', sans-serif; }
    .stDataFrame { background-color: #1e293b; border-radius: 12px; }
    
    /* Destaque Azul da Imagem */
    .stInfo { background-color: #0369a1; border: none; color: white; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexão com Dados
token = "d63fcb8845c2461da566eed3df05770e"
headers = {'X-Auth-Token': token}

# 3. Sidebar (Igual ao Menu Lateral da Imagem)
st.sidebar.markdown("<h1 style='color: #38bdf8;'>SAPEM</h1>", unsafe_allow_html=True)
st.sidebar.write("---")
liga = st.sidebar.selectbox("ESCOLHA O CAMPEONATO", ["Premier League", "Liga Portuguesa", "La Liga"])

config = {
    "Premier League": "PL",
    "Liga Portuguesa": "PPL",
    "La Liga": "PD"
}

# 4. Conteúdo Principal
st.title("INFORMAÇÕES ATUALIZADAS")

@st.cache_data
def get_data():
    url = f"https://api.football-data.org/v4/competitions/{config[liga]}/standings"
    return requests.get(url, headers=headers).json()

data = get_data()

if 'standings' in data:
    df = pd.DataFrame(data['standings'][0]['table'])
    df['Equipa'] = df['team'].apply(lambda x: x['name'])
    
    # Linha de Destaque (Agenda)
    st.markdown(f"### 🗓️ Agenda de Jogos: {liga}")
    st.info(f"Próxima jornada disponível para análise tática avançada.")
    
    st.write("---")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("🏆 Classificação")
        st.dataframe(df[['position', 'Equipa', 'points']].set_index('position'), use_container_width=True)
        
    with col2:
        st.subheader("🔍 Raio-X de Performance")
        time_focus = st.selectbox("Selecione a Equipa", df['Equipa'].tolist())
        stats = df[df['Equipa'] == time_focus].iloc[0]
        
        # Grid de métricas
        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)
        
        c1.metric("VITÓRIAS", stats['won'])
        c2.metric("GOLOS / JOGO", f"{stats['goalsFor']/stats['playedGames']:.2f}")
        c3.metric("DEFESA (MÉDIA)", f"{stats['goalsAgainst']/stats['playedGames']:.2f}")
        c4.metric("PONTOS", stats['points'])
        
        # Caixa de Alerta (Igual à cor vermelha da imagem se o time estiver mal)
        aprov = (stats['points']/(stats['playedGames']*3))*100
        if aprov < 40:
            st.error(f"⚠️ ALERTA: O {time_focus} apresenta risco elevado de derrota.")
        else:
            st.success(f"✅ RELATÓRIO: {time_focus} mantém performance estável.")
