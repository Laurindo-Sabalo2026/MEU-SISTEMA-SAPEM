import streamlit as st
import requests
import pandas as pd

# 1. Configuração da Página e Estilo Visual (CSS Personalizado)
st.set_page_config(page_title="SAPEM | PRO", layout="wide")

# CSS para criar o visual Dark Mode igual à imagem
st.markdown("""
    <style>
    /* Fundo principal */
    .stApp {
        background-color: #1a1c24;
        color: #ffffff;
    }
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #111217;
    }
    /* Cartões de métricas */
    div[data-testid="stMetricValue"] {
        background-color: #262932;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
    }
    /* Estilo dos títulos */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    /* Tabela personalizada */
    .stDataFrame {
        border: 1px solid #343a40;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Configurações de Dados
token = "d63fcb8845c2461da566eed3df05770e"
headers = {'X-Auth-Token': token}

# 3. Interface - Barra Lateral
st.sidebar.markdown("<h2 style='text-align: center;'>SAPEM PRO</h2>", unsafe_allow_html=True)
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

# 4. Cabeçalho Principal
st.markdown(f"<h1 style='color: {config[liga_selecionada]['cor']};'>INFORMAÇÕES ATUALIZADAS</h1>", unsafe_allow_html=True)
st.write(f"Campeonato Selecionado: **{liga_selecionada}**")

@st.cache_data
def buscar_dados(codigo):
    url = f"https://api.football-data.org/v4/competitions/{codigo}/standings"
    try:
        res = requests.get(url, headers=headers)
        return res.json()
    except:
        return None

dados = buscar_dados(config[liga_selecionada]["id"])

if dados and 'standings' in dados:
    tabela = dados['standings'][0]['table']
    df = pd.DataFrame(tabela)
    df['Equipa'] = df['team'].apply(lambda x: x['name'])
    
    # 5. Organização em Colunas (Layout da Imagem)
    col_menu, col_main = st.columns([0.8, 2])
    
    with col_menu:
        st.markdown("### 📊 ESTATÍSTICAS")
        st.dataframe(df[['position', 'Equipa', 'points']].set_index('position'), height=400)
    
    with col_main:
        st.markdown("### 🔍 ANÁLISE DE ELITE")
        selecao = st.selectbox("Escolha a Equipa:", df['Equipa'].tolist())
        
        info = df[df['Equipa'] == selecao].iloc[0]
        pj = info['playedGames']
        gm = info['goalsFor']
        gs = info['goalsAgainst']
        
        # Cartões de Métricas (Igual aos quadrados da imagem)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Vitórias", info['won'])
        c2.metric("Ataque", f"{gm/pj:.2f}")
        c3.metric("Defesa", f"{gs/pj:.2f}")
        c4.metric("Pontos", info['points'])
        
        st.markdown("---")
        # Alerta de Inteligência (Caixa colorida da imagem)
        aprov = (info['points']/(pj*3))*100
        if aprov > 65:
            st.info(f"🚀 **RELATÓRIO SAPEM:** O {selecao} apresenta um desempenho de elite. Probabilidade de vitória muito alta nos próximos jogos.")
        else:
            st.warning(f"⚠️ **RELATÓRIO SAPEM:** O {selecao} apresenta oscilações táticas. Recomenda-se análise de risco.")

else:
    st.error("Erro na conexão com os dados. Verifique sua chave API.")
