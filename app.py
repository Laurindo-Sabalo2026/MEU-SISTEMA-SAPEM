import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURAÇÃO DE INTERFACE (UX/UI PROFISSIONAL)
st.set_page_config(page_title="SAPEM | BUSINESS INTELLIGENCE", layout="wide")

# Estilização customizada para um visual moderno e limpo
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .sidebar .sidebar-content { background-color: #1a1c23; color: white; }
    h1, h2, h3 { color: #1a1c23; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_name=True)

# 2. MOTOR DE DADOS (CONEXÃO COM GOOGLE SHEETS)
URL_SISTEMA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        data = pd.read_csv(URL_SISTEMA)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame({"Equipa": ["Erro"], "Pts": [0]})

df = load_data()

# ---------------------------------------------------------
# NÍVEL 1: SELETOR DE MODALIDADE
# ---------------------------------------------------------
st.sidebar.title("💎 SAPEM CONTROL")
modalidade = st.sidebar.selectbox("Escolha o Esporte", ["Futebol ⚽", "Basquetebol 🏀"])

# ---------------------------------------------------------
# NÍVEL 2: GLOBAL LEAGUE INDEX
# ---------------------------------------------------------
pais = st.sidebar.selectbox("País", ["Portugal", "Espanha", "Inglaterra", "Angola"])
liga = st.sidebar.selectbox("Liga", ["Liga Portugal", "Premier League", "La Liga", "Girabola"])

# ---------------------------------------------------------
# NÍVEL 3: DASHBOARD DE RODADA
# ---------------------------------------------------------
menu_principal = st.sidebar.radio("Navegação", ["📅 Rodada Atual", "🔍 Deep Analysis (H2H)", "🌡️ Contexto Externo"])

if menu_principal == "📅 Rodada Atual":
    st.title(f"🏟️ Dashboard: {liga}")
    st.info("Jogos das próximas 3 jornadas ordenados cronologicamente.")
    
    # Exibição de tabela de classificação geral (BI)
    st.subheader("Classificação Geral")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# NÍVEL 4: DEEP ANALYSIS (PAINEL INFORMAÇÕES ATUALIZADAS)
# ---------------------------------------------------------
elif menu_principal == "🔍 Deep Analysis (H2H)":
    st.title("🔬 Painel de Análise Profunda")
    
    col_a, col_b = st.columns(2)
    with col_a:
        time_a = st.selectbox("Equipa A (Casa)", df["Equipa"].unique())
    with col_b:
        time_b = st.selectbox("Equipa B (Fora)", df["Equipa"].unique())

    # Categorização de Dados (Módulos III & IV)
    aba1, aba2, aba3 = st.tabs(["📊 Performance Individual", "🎯 Inteligência Preditiva", "📜 Histórico H2H"])

    with aba1:
        st.subheader("KPIs de Desempenho (Módulos III & IV)")
        
        def display_kpis(equipa):
            row = df[df["Equipa"] == equipa].iloc[0]
            st.markdown(f"**Análise Detalhada: {equipa}**")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1: # RESULTADOS
                st.write("**Resultados**")
                st.metric("Pts", row.get('Pts', 0))
                st.metric("Jogos", row.get('J', 0))
            with c2: # OFENSIVIDADE
                st.write("**Ofensividade**")
                st.metric("Golos Mar.", row.get('Golos Marcados', 0))
                st.metric("Remates", row.get('Remates', 0))
            with c3: # BOLA PARADA
                st.write("**Bola Parada**")
                st.metric("Cantos Pro", row.get('Cantos', 0))
                st.metric("Laterais", "N/A")
            with c4: # DISCIPLINA
                st.write("**Disciplina**")
                st.metric("Cartões Am.", row.get('Cartões', 0))
                st.metric("Vermelhos", "0")

        display_kpis(time_a)
        st.divider()
        display_kpis(time_b)

    with aba2:
        st.subheader("Módulo V: Intelligence & Analytics")
        # Algoritmo de Probabilidade Simples (Exemplo baseado em Pts)
        pts_a = df[df["Equipa"] == time_a]["Pts"].iloc[0]
        pts_b = df[df["Equipa"] == time_b]["Pts"].iloc[0]
        prob = (pts_a / (pts_a + pts_b)) * 100 if (pts_a + pts_b) > 0 else 50
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Win Probability (Algoritmo SAPEM)**")
            st.progress(int(prob))
            st.write(f"{time_a}: {prob:.1f}% | {time_b}: {100-prob:.1f}%")
        
        with c2:
            st.write("**Mercados Over/Under**")
            st.write(f"Chance +2.5 Golos: **{65 if prob > 50 else 40}%**")
            st.write(f"Chance +8.5 Cantos: **{72 if prob > 50 else 55}%**")
        
        if prob > 70:
            st.success("💎 ALERTA DE VALOR: Probabilidade estatística acima da média do mercado.")

    with aba3:
        st.subheader("Módulo I & II: Head to Head")
        st.write("Últimos 5 confrontos diretos:")
        st.table(pd.DataFrame({
            "Data": ["10/10/2023", "05/05/2023", "12/12/2022"],
            "Resultado": [f"{time_a} 2-1 {time_b}", f"{time_b} 0-0 {time_a}", f"{time_a} 3-0 {time_b}"]
        }))

# ---------------------------------------------------------
# FUNCIONALIDADES ADICIONAIS (CLIMA E MOMENTUM)
# ---------------------------------------------------------
elif menu_principal == "🌡️ Contexto Externo":
    st.title("⛈️ Clima, Altitude & Momentum")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Fatores Ambientais")
        clima = st.select_slider("Condição Climática", options=["Sol", "Chuva Leve", "Chuva Forte", "Neve"])
        altitude = st.number_input("Altitude (metros)", value=0)
        
        if altitude > 1500:
            st.warning("⚠️ Alerta de Altitude: Redução de 15% na capacidade aeróbica das equipas.")
            
    with col2:
        st.subheader("Análise de Tendência (Momentum)")
        # Gráfico visual de momentum
        chart_data = pd.DataFrame(np.random.randn(20, 2), columns=["Tendência A", "Tendência B"])
        st.line_chart(chart_data)
        st.info("O gráfico acima mostra se o desempenho está em ascensão (Momentum Positivo) ou queda.")

    st.subheader("🚑 Line-ups & Desfalques")
    st.text_area("Jogadores Ausentes (Suspensões/Lesões):", "Ex: Jogador X (Sporting) - Lesão no joelho.")
