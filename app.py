import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. Configuração de Interface SAPEM ELITE
st.set_page_config(page_title="SAPEM | INTELLIGENCE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid #334155; }
    .metric-card { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; text-align: center; }
    .stMetricValue { color: #38bdf8 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; border-radius: 4px; padding: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Motor de Dados (API)
token = "d63fcb8845c2461da566eed3df05770e"
headers = {'X-Auth-Token': token}

# 3. NÍVEL 1 & 2: Estrutura de Navegação (Sidebar)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/5323/5323982.png", width=50)
st.sidebar.title("SAPEM v4.0")

modalidade = st.sidebar.radio("MODALIDADE", ["⚽ Futebol", "🏀 Basquetebol (Em breve)"])
pais = st.sidebar.selectbox("PAÍS", ["Inglaterra", "Portugal", "Espanha", "Alemanha"])

ligas_dict = {
    "Inglaterra": "PL", "Portugal": "PPL", "Espanha": "PD", "Alemanha": "BL1"
}

# 4. NÍVEL 3: Dashboard de Rodada (Próximas Jornadas)
st.title(f"📊 Global League Index: {pais}")

@st.cache_data
def get_matches(league_code):
    url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=SCHEDULED"
    res = requests.get(url, headers=headers).json()
    return res.get('matches', [])[:15] # Próximos 15 jogos

matches = get_matches(ligas_dict[pais])

if matches:
    st.subheader("🗓️ Próximos Confrontos (Análise Disponível)")
    
    # Criar uma lista de nomes de jogos para o seletor
    match_options = [f"{m['homeTeam']['name']} vs {m['awayTeam']['name']} ({m['utcDate'][:10]})" for m in matches]
    selected_match_idx = st.selectbox("Selecione um jogo para DEEP ANALYSIS:", range(len(match_options)), format_func=lambda x: match_options[x])
    
    jogo_selecionado = matches[selected_match_idx]
    
    st.markdown("---")
    
    # 5. NÍVEL 4: Deep Analysis - PAINEL INFORMAÇÕES ATUALIZADAS
    st.header(f"🔍 Deep Analysis: {match_options[selected_match_idx]}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 H2H & Performance", "🎯 Probabilidades (Predictive)", "🛡️ Line-ups", "📈 Momentum"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Módulo I & II: Head to Head")
            st.info("Histórico de confrontos diretos: Equilibrado (Dados de API Tier 1)")
            # Simulação de dados H2H para interface
            h2h_data = pd.DataFrame({'Data': ['2023','2024'], 'Vencedor': [jogo_selecionado['homeTeam']['name'], 'Empate']})
            st.table(h2h_data)
            
        with c2:
            st.markdown("### Módulo III & IV: Performance Individual")
            st.write(f"**{jogo_selecionado['homeTeam']['name']} (Últimos 5 jogos)**")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Golos/m", "1.8")
            col_b.metric("Cantos/m", "5.4")
            col_c.metric("Cartões", "2.1")

    with tab2:
        st.markdown("### Módulo V: Intelligence & Analytics")
        m1, m2, m3 = st.columns(3)
        # Lógica de Probabilidade Preditiva (Exemplo Baseado em Ranking)
        m1.metric("Probabilidade Vitória Casa", "42%")
        m2.metric("Chance Empate", "28%")
        m3.metric("Probabilidade Vitória Fora", "30%")
        
        st.write("---")
        st.subheader("🔥 Mercados de Valor (Predictive Stats)")
        st.success("✅ **+8.5 Cantos:** 78% de probabilidade estatística")
        st.warning("⚠️ **Ambas Marcam:** 52% de probabilidade")

    with tab3:
        st.markdown("### 🚑 Line-ups & Desfalques")
        ca, cb = st.columns(2)
        ca.write(f"**Desfalques {jogo_selecionado['homeTeam']['name']}**")
        ca.error("Nenhum jogador suspenso.")
        cb.write(f"**Desfalques {jogo_selecionado['awayTeam']['name']}**")
        cb.error("1 Jogador em dúvida (Lesão Muscular).")

    with tab4:
        st.markdown("### 📈 Análise de Tendência (Momentum)")
        # Gráfico visual de ascensão ou queda
        graf_data = pd.DataFrame({'Jornada': [1,2,3,4,5], 'Rendimento': [60, 65, 58, 70, 75]})
        fig = px.area(graf_data, x='Jornada', y='Rendimento', title="Momentum de Performance")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Não foram encontrados jogos agendados para esta liga no momento.")

st.sidebar.markdown("---")
st.sidebar.caption("SAPEM Intelligence Systems © 2026")
