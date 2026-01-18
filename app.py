import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="SAPEM | INTELLIGENCE BI", layout="wide")

st.title("💎 SAPEM | BUSINESS INTELLIGENCE")
st.markdown("---")

# 2. CONEXÃO COM GOOGLE SHEETS
URL_SISTEMA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=5) # Cache baixo para atualização rápida
def load_data():
    try:
        data = pd.read_csv(URL_SISTEMA)
        # Limpeza automática de nomes de colunas (remove espaços e garante compatibilidade)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame({"Equipa": ["Erro"], "Pts": [0]})

df = load_data()

# ---------------------------------------------------------
# NAVEGAÇÃO LATERAL (UX)
# ---------------------------------------------------------
st.sidebar.title("🎮 PAINEL DE CONTROLO")
modalidade = st.sidebar.selectbox("Nível 1: Modalidade", ["Futebol ⚽", "Basquetebol 🏀"])
liga = st.sidebar.selectbox("Nível 2: Global League Index", ["Liga Portugal", "Girabola", "Premier League"])
menu = st.sidebar.radio("Nível 3: Menu de Análise", ["📅 Dashboard de Jornada", "🔬 Deep Analysis (Módulos I-V)", "🌡️ Fatores Externos"])

# ---------------------------------------------------------
# MÓDULO: DASHBOARD DE JORNADA
# ---------------------------------------------------------
if menu == "📅 Dashboard de Jornada":
    st.subheader(f"🏟️ Jornadas: {liga}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Ligas Monitorizadas", "12")
    c2.metric("Alertas de Valor", "5")
    c3.metric("Eficiência IA", "84%")
    
    st.write("### Classificação Atualizada")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# MÓDULO: DEEP ANALYSIS (O CORAÇÃO DO BI)
# ---------------------------------------------------------
elif menu == "🔬 Deep Analysis (Módulos I-V)":
    st.subheader("🔍 Painel de Informações Atualizadas")
    
    col_a, col_b = st.columns(2)
    with col_a: casa = st.selectbox("Equipa Casa", df["Equipa"].unique())
    with col_b: fora = st.selectbox("Equipa Fora", df["Equipa"].unique())

    tab1, tab2, tab3 = st.tabs(["📊 Performance (Mód. III/IV)", "🎯 Inteligência (Mód. V)", "📜 H2H (Mód. I/II)"])

    with tab1:
        st.write("### KPIs de Desempenho (Médias Reais)")
        def mostrar_stats(time):
            # Localiza a linha da equipa e garante que valores vazios virem 0
            stats = df[df["Equipa"] == time].iloc[0].fillna(0)
            st.markdown(f"📈 **{time}**")
            k1, k2, k3, k4 = st.columns(4)
            # Mapeamento direto das colunas da sua planilha (Captura 6802)
            k1.metric("Média Cantos", stats.get('Cantos', 0))
            k2.metric("Média Cartões", stats.get('Cartões', 0))
            k3.metric("Remates", stats.get('Remates', 0))
            k4.metric("Golos Marc.", stats.get('Golos Marcados', 0))
        
        mostrar_stats(casa)
        st.divider()
        mostrar_stats(fora)

    with tab2:
        st.write("### Predictive Stats & Analytics")
        v_casa = df[df["Equipa"] == casa]["Pts"].iloc[0]
        v_fora = df[df["Equipa"] == fora]["Pts"].iloc[0]
        prob = (v_casa / (v_casa + v_fora)) * 100 if (v_casa + v_fora) > 0 else 50
        
        st.write(f"Probabilidade de Vitória ({casa}): **{prob:.1f}%**")
        st.progress(int(prob))
        
        st.info("💡 Dica: O algoritmo SAPEM sugere analisar o mercado de Cantos se a média combinada for > 9.5.")

# ---------------------------------------------------------
# MÓDULO: FATORES EXTERNOS
# ---------------------------------------------------------
elif menu == "🌡️ Fatores Externos":
    st.subheader("⛈️ Contexto Ambiental & Momentum")
    c1, c2 = st.columns(2)
    with c1:
        clima = st.select_slider("Condição do Tempo", options=["Sol", "Chuva Leve", "Chuva Forte"])
        altitude = st.number_input("Altitude (metros)", value=0)
        if altitude > 1800: st.error("🚨 Altitude Crítica!")
    with c2:
        chart_data = pd.DataFrame(np.random.randn(10, 2), columns=["Momentum Casa", "Momentum Fora"])
        st.line_chart(chart_data)

    st.subheader("🚑 Line-ups & Desfalques")
    st.text_area("Notas sobre Lesionados:", "Ex: O capitão da Equipa B está fora por cartões.")
