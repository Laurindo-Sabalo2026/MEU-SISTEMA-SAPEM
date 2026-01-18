import streamlit as st
import pandas as pd
import numpy as np

# 1. ARQUITETURA DE INFORMAÇÃO & UI (Inspirado na imagem SAPEM v10)
st.set_page_config(page_title="SAPEM | INTELLIGENCE BI", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #151921; border-right: 1px solid #2d333d; }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px; border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    h1, h2, h3 { color: #FFD700 !important; font-family: 'Inter', sans-serif; }
    .stProgress > div > div > div > div { background-color: #FFD700; }
    </style>
    """, unsafe_allow_name=True)

# 2. CONEXÃO AO BANCO DE DADOS (GOOGLE SHEETS)
URL_SISTEMA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=10)
def carregar_bi_data():
    try:
        data = pd.read_csv(URL_SISTEMA)
        # Limpeza de nomes de colunas para evitar erros de espaços
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame({"Equipa": ["Erro"], "Pts": [0]})

df = carregar_bi_data()

# 3. HIERARQUIA DE NAVEGAÇÃO (UX)
st.sidebar.title("💎 SAPEM CONTROL")
modalidade = st.sidebar.selectbox("Nível 1: Modalidade", ["Futebol ⚽", "Basquetebol 🏀"])
menu = st.sidebar.radio("Nível 2: Global Index", ["📊 Dashboard de Rodada", "🔍 Deep Analysis (Módulos I-V)", "🌡️ Fatores Externos"])

# 4. MÓDULOS DO SISTEMA
if menu == "📊 Dashboard de Rodada":
    st.title("🏟️ Dashboard de Jornada")
    st.subheader("Próximos Eventos & Classificação")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ligas Ativas", "12")
    col2.metric("Alertas de Valor", "5", delta="2 novos")
    col3.metric("Eficiência Algoritmo", "84%")
    
    st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "🔍 Deep Analysis (Módulos I-V)":
    st.title("🔬 Deep Analysis: Equipa A x Equipa B")
    
    # Seleção de Equipas para H2H
    c1, c2 = st.columns(2)
    with c1: equipa_a = st.selectbox("Equipa A (Performance Individual)", df["Equipa"].unique())
    with c2: equipa_b = st.selectbox("Equipa B (Performance Individual)", df["Equipa"].unique())
    
    # MÓDULOS III & IV: Performance Individual
    st.markdown("### 📊 Módulos III & IV: KPIs de Desempenho")
    
    def mostrar_metrics(nome_equipa):
        row = df[df["Equipa"] == nome_equipa].iloc[0]
        st.write(f"**Análise: {nome_equipa}**")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Golos Marcados", row.get('Golos Marcados', 0))
        m2.metric("Média Cantos", row.get('Cantos', 0))
        m3.metric("Remates", row.get('Remates', 0))
        m4.metric("Disciplina (Cartões)", row.get('Cartões', 0))

    mostrar_metrics(equipa_a)
    st.divider()
    mostrar_metrics(equipa_b)
    
    # MÓDULO V: Intelligence & Analytics (Previsão)
    st.markdown("### 🎯 Módulo V: Predictive Stats")
    pts_a = df[df["Equipa"] == equipa_a]["Pts"].iloc[0]
    pts_b = df[df["Equipa"] == equipa_b]["Pts"].iloc[0]
    prob_win = (pts_a / (pts_a + pts_b)) * 100 if (pts_a + pts_b) > 0 else 50
    
    st.write(f"Probabilidade de Vitória ({equipa_a}): **{prob_win:.1f}%**")
    st.progress(int(prob_win))
    
    if prob_win > 65:
        st.success(f"🔥 ALERTA DE VALOR: Alta probabilidade para {equipa_a}")

elif menu == "🌡️ Fatores Externos":
    st.title("☁️ Contexto Externo & Momentum")
    st.info("Este módulo analisa Clima, Altitude e Line-ups (Desfalques).")
    
    col_clima, col_alt = st.columns(2)
    with col_clima:
        clima = st.select_slider("Condição Climática", options=["Sol", "Chuva Leve", "Chuva Forte", "Neve"])
        st.write(f"Impacto na Média de Remates: {'-15%' if 'Chuva' in clima else 'Normal'}")
    
    with col_alt:
        altitude = st.number_input("Altitude do Estádio (metros)", value=0)
        if altitude > 2000:
            st.warning("⚠️ Impacto Crítico: Redução de 20% no fôlego dos jogadores (Momentum Negativo).")

st.sidebar.markdown("---")
st.sidebar.write("Desenvolvido por: **Laurindo Sabalo**")
