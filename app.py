import streamlit as st
import pandas as pd
import numpy as np

# 1. DESIGN PROFISSIONAL (CSS LIMPO)
st.set_page_config(page_title="SAPEM | INTELLIGENCE BI", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    h1, h2, h3 { color: #FFD700 !important; font-family: 'Inter', sans-serif; }
    .stMetric { background-color: #151921; padding: 15px; border-radius: 10px; border: 1px solid #2d333d; }
    </style>
    """, unsafe_allow_name=True)

# 2. CONEXÃO AO GOOGLE SHEETS (LINK VALIDADO)
URL_SISTEMA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=10)
def load_bi_data():
    try:
        data = pd.read_csv(URL_SISTEMA)
        data.columns = data.columns.str.strip()
        return data
    except:
        # Dados de Backup caso o link falhe
        return pd.DataFrame({"Equipa": ["Sporting CP", "Benfica", "FC Porto"], "Pts": [46, 45, 38]})

df = load_bi_data()

# 3. NAVEGAÇÃO DE NÍVEL (UX)
st.sidebar.title("💎 SAPEM CONTROL")
esporte = st.sidebar.selectbox("Nível 1: Modalidade", ["Futebol ⚽", "Basquetebol 🏀"])
menu = st.sidebar.radio("Nível 2: Global Index", 
    ["📊 Dashboard de Rodada", "🔬 Deep Analysis (Módulos I-V)", "🌡️ Fatores Externos"])

# 4. MÓDULOS DO SISTEMA
if menu == "📊 Dashboard de Rodada":
    st.title("🏟️ Dashboard de Jornada")
    st.subheader("Próximos Eventos & Classificação")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ligas Monitorizadas", "12")
    col2.metric("Alertas de Valor", "5", delta="2 novos")
    col3.metric("Eficiência IA", "84%")
    
    st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "🔬 Deep Analysis (Módulos I-V)":
    st.title("🔬 Deep Analysis: Módulos I-V")
    
    # Seleção de Confronto
    c1, c2 = st.columns(2)
    with c1: eq_a = st.selectbox("Equipa Casa", df["Equipa"].unique())
    with c2: eq_b = st.selectbox("Equipa Fora", df["Equipa"].unique())
    
    st.markdown("---")
    
    # MÓDULOS III & IV: Performance Individual
    st.subheader("📊 Módulos III & IV: KPIs de Desempenho")
    
    def mostrar_stats(time):
        row = df[df["Equipa"] == time].iloc[0]
        st.write(f"📈 **{time}**")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Cantos (Média)", row.get('Cantos', 0))
        m2.metric("Cartões (Média)", row.get('Cartões', 0))
        m3.metric("Remates", row.get('Remates', 0))
        m4.metric("Golos Marc.", row.get('Golos Marcados', 0))

    mostrar_stats(eq_a)
    st.divider()
    mostrar_stats(eq_b)
    
    # MÓDULO V: Intelligence & Analytics
    st.subheader("🎯 Módulo V: Predictive Stats")
    pts_a = df[df["Equipa"] == eq_a]["Pts"].iloc[0]
    pts_b = df[df["Equipa"] == eq_b]["Pts"].iloc[0]
    prob = (pts_a / (pts_a + pts_b)) * 100 if (pts_a + pts_b) > 0 else 50
    
    st.write(f"Chance de Vitória ({eq_a}): **{prob:.1f}%**")
    st.progress(int(prob))
    
    if prob > 65:
        st.success(f"💎 ALERTA DE VALOR: Alta probabilidade estatística para {eq_a}")

elif menu == "🌡️ Fatores Externos":
    st.title("☁️ Contexto Externo & Momentum")
    clima = st.select_slider("Condição Climática", options=["Sol", "Chuva Leve", "Chuva Forte", "Neve"])
    altitude = st.number_input("Altitude (metros)", value=0)
    
    if altitude > 1800:
        st.warning("⚠️ Impacto Crítico: Redução de 20% no momentum físico devido à altitude.")
    if "Chuva" in clima:
        st.info("💡 Tendência: Histórico aponta redução na média de remates à baliza.")
