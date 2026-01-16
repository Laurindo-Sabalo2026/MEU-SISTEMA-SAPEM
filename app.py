import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. Configuração de Layout e Estilo Premium (CSS)
st.set_page_config(page_title="SAPEM | ULTIMATE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid #334155; }
    
    /* Estilo dos Cards de Métricas */
    div[data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    [data-testid="stMetricValue"] { color: #38bdf8 !important; font-size: 2rem !important; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }

    /* Customização de Tabelas */
    .stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid #334155; }
    
    h1, h2, h3 { font-family: 'Inter', sans-serif; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Configurações de API
token = "d63fcb8845c2461da566eed3df05770e"
headers = {'X-Auth-Token': token}

# 3. Menu Lateral
st.sidebar.markdown("<h1 style='color: #38bdf8; text-align: center;'>SAPEM</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #94a3b8;'>Inteligência Esportiva v3.0</p>", unsafe_allow_html=True)
st.sidebar.write("---")
liga_escolhida = st.sidebar.selectbox("MODALIDADE / LIGA", ["Premier League", "Liga Portuguesa", "La Liga"])

config = {"Premier League": "PL", "Liga Portuguesa": "PPL", "La Liga": "PD"}

# 4. Busca de Dados
@st.cache_data
def carregar_dados_elite(codigo):
    url = f"https://api.football-data.org/v4/competitions/{codigo}/standings"
    return requests.get(url, headers=headers).json()

dados = carregar_dados_elite(config[liga_escolhida])

if 'standings' in dados:
    tabela = dados['standings'][0]['table']
    df = pd.DataFrame(tabela)
    df['Equipa'] = df['team'].apply(lambda x: x['name'])

    # CABEÇALHO DINÂMICO
    st.markdown(f"## 📊 {liga_escolhida.upper()} | Visão Geral")
    
    # BOX DE PRÓXIMO CONFRONTO (Igual ao topo da sua imagem)
    st.info("💡 **DICA SAPEM:** Alta probabilidade de golos na próxima jornada devido à média ofensiva das equipas de topo.")

    st.write("---")

    col_esq, col_dir = st.columns([1, 1.8])

    with col_esq:
        st.markdown("### 🏆 Classificação")
        st.dataframe(df[['position', 'Equipa', 'points']].set_index('position'), use_container_width=True, height=480)

    with col_dir:
        st.markdown("### 🔍 Análise de Performance Profissional")
        time_analise = st.selectbox("Escolha a Equipa Alvo:", df['Equipa'].tolist())
        stats = df[df['Equipa'] == time_analise].iloc[0]
        
        # Grid de Métricas (Cartões da imagem)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("VITÓRIAS", stats['won'])
        m2.metric("ATAQUE", f"{stats['goalsFor']/stats['playedGames']:.2f}")
        m3.metric("DEFESA", f"{stats['goalsAgainst']/stats['playedGames']:.2f}")
        m4.metric("PONTOS", stats['points'])

        st.markdown("---")
        
        # 5. GRÁFICO DE EVOLUÇÃO (O toque final que faltava!)
        st.markdown("### 📈 Tendência de Rendimento")
        # Criamos dados fictícios de tendência baseados nos pontos atuais para o gráfico
        tendencia = pd.DataFrame({
            'Jornada': range(1, 6),
            'Pontos Estimados': [stats['points']-12, stats['points']-9, stats['points']-6, stats['points']-3, stats['points']]
        })
        fig = px.line(tendencia, x='Jornada', y='Pontos Estimados', markers=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color="#94a3b8", margin=dict(l=0, r=0, t=30, b=0), height=250
        )
        fig.update_traces(line_color='#38bdf8', line_width=4)
        st.plotly_chart(fig, use_container_width=True)

        st.success(f"📌 O **{time_analise}** mantém um aproveitamento de {(stats['points']/(stats['playedGames']*3))*100:.1f}%.")
