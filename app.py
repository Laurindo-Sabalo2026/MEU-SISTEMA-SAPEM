import streamlit as st
import requests
import pandas as pd

# 1. Configuração da Página e Estilo Visual Refinado
st.set_page_config(page_title="SAPEM | PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1a1c24; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111217; }
    
    /* Melhora o contraste dos cartões de métricas */
    div[data-testid="metric-container"] {
        background-color: #262932;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #007bff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    
    /* Força o texto das métricas a ficar branco */
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 2. Configurações de Dados
token = "d63fcb8845c2461da566eed3df05770e"
headers = {'X-Auth-Token': token}

# 3. Interface - Barra Lateral Estilizada
st.sidebar.markdown("<h2 style='text-align: center; color: #007bff;'>SAPEM PRO</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
liga_selecionada = st.sidebar.selectbox(
    "SELECIONE A LIGA",
    ["Premier League", "Liga Portuguesa", "La Liga (Espanha)"]
)

config = {
    "Premier League": {"id": "PL", "cor": "#3d195d"},
    "Liga Portuguesa": {"id": "PPL", "cor": "#005baa"},
    "La Liga (Espanha)": {"id": "PD", "cor": "#ee1c2e"}
}

# 4. Cabeçalho Principal Dinâmico
st.markdown(f"<h1 style='color: white;'>INFORMAÇÕES ATUALIZADAS</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color: {config[liga_selecionada]['cor']}; font-size: 20px;'>⚽ {liga_selecionada}</p>", unsafe_allow_html=True)

@st.cache_data
def buscar_dados(codigo):
    url = f"https://api.football-data.org/v4/competitions/{codigo}/standings"
    try:
        res = requests.get(url, headers=headers)
        return res.json()
    except: return None

dados = buscar_dados(config[liga_selecionada]["id"])

if dados and 'standings' in dados:
    tabela = dados['standings'][0]['table']
    df = pd.DataFrame(tabela)
    df['Equipa'] = df['team'].apply(lambda x: x['name'])
    
    col_tabela, col_analise = st.columns([1, 1.2])
    
    with col_tabela:
        st.markdown("### 📊 CLASSIFICAÇÃO")
        st.dataframe(df[['position', 'Equipa', 'points']].set_index('position'), use_container_width=True, height=450)
    
    with col_analise:
        st.markdown("### 🔍 ANÁLISE TÁTICA")
        selecao = st.selectbox("Escolha a Equipa:", df['Equipa'].tolist())
        
        info = df[df['Equipa'] == selecao].iloc[0]
        pj, gm, gs = info['playedGames'], info['goalsFor'], info['goalsAgainst']
        
        # Grid de métricas igual ao design premium
        m1, m2 = st.columns(2)
        m3, m4 = st.columns(2)
        
        m1.metric("Vitórias", info['won'])
        m2.metric("Média Golos", f"{gm/pj:.2f}")
        m3.metric("Solidez Defensiva", f"{gs/pj:.2f}")
        m4.metric("Pontos Totais", info['points'])
        
        st.markdown("---")
        aprov = (info['points']/(pj*3))*100
        if aprov > 65:
            st.success(f"💎 **ELITE SAPEM:** O {selecao} domina o campeonato com {aprov:.1f}% de aproveitamento.")
        else:
            st.info(f"📊 **ANÁLISE:** O {selecao} mantém um ritmo de {aprov:.1f}%.")
else:
    st.error("Erro ao carregar dados. Tente novamente em 1 minuto.")
