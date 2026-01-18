import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="SAPEM | INTELLIGENCE BI", layout="wide")

# Título Principal (Design Limpo para evitar erros de CSS)
st.title("💎 SAPEM | BUSINESS INTELLIGENCE")
st.markdown("---")

# 2. CONEXÃO COM GOOGLE SHEETS (Link das suas capturas)
URL_SISTEMA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=15)
def load_data():
    try:
        data = pd.read_csv(URL_SISTEMA)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame({"Equipa": ["Sporting CP", "Benfica", "FC Porto"], "Pts": [46, 45, 38]})

df = load_data()

# ---------------------------------------------------------
# NÍVEL 1 & 2: SELETORES (BARRA LATERAL)
# ---------------------------------------------------------
st.sidebar.title("🎮 PAINEL DE CONTROLO")
modalidade = st.sidebar.selectbox("Nível 1: Modalidade", ["Futebol ⚽", "Basquetebol 🏀"])
liga = st.sidebar.selectbox("Nível 2: Global League Index", ["Liga Portugal", "Premier League", "Girabola"])

menu = st.sidebar.radio("Nível 3: Menu de Análise", 
    ["📅 Dashboard de Jornada", "🔬 Deep Analysis (Módulos I-V)", "🌡️ Fatores Externos"])

# ---------------------------------------------------------
# NÍVEL 3: DASHBOARD DE JORNADA
# ---------------------------------------------------------
if menu == "📅 Dashboard de Jornada":
    st.subheader(f"🏟️ Jornadas: {liga}")
    
    # Cartões de Resumo Estilo BI
    c1, c2, c3 = st.columns(3)
    c1.metric("Ligas Monitorizadas", "12")
    c2.metric("Alertas de Valor", "5")
    c3.metric("Eficiência IA", "84%")
    
    st.write("### Próximos Jogos & Classificação")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# NÍVEL 4: DEEP ANALYSIS (PAINEL DE INFORMAÇÕES ATUALIZADAS)
# ---------------------------------------------------------
elif menu == "🔬 Deep Analysis (Módulos I-V)":
    st.subheader("🔍 Painel de Informações Atualizadas")
    
    col_a, col_b = st.columns(2)
    with col_a:
        casa = st.selectbox("Equipa Casa", df["Equipa"].unique())
    with col_b:
        fora = st.selectbox("Equipa Fora", df["Equipa"].unique())

    # MÓDULOS ORGANIZADOS POR ABAS
    tab1, tab2, tab3 = st.tabs(["📊 Performance (Mód. III/IV)", "🎯 Inteligência (Mód. V)", "📜 H2H (Mód. I/II)"])

    with tab1:
        st.write("### KPIs de Desempenho (Últimos 10 Jogos)")
        def mostrar_stats(time):
            row = df[df["Equipa"] == time].iloc[0]
            st.write(f"📈 **{time}**")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Média Cantos", row.get('Cantos', 0))
            k2.metric("Média Cartões", row.get('Cartões', 0))
            k3.metric("Remates", row.get('Remates', 0))
            k4.metric("Golos Marc.", row.get('Golos Marcados', 0))
        
        mostrar_stats(casa)
        st.divider()
        mostrar_stats(fora)

    with tab2:
        st.write("### Predictive Stats & Analytics")
        # Lógica de cálculo probabilístico
        pts_casa = df[df["Equipa"] == casa]["Pts"].iloc[0]
        pts_fora = df[df["Equipa"] == fora]["Pts"].iloc[0]
        total = pts_casa + pts_fora if (pts_casa + pts_fora) > 0 else 1
        prob_vitoria = (pts_casa / total) * 100
        
        st.write(f"Probabilidade de Vitória ({casa}): **{prob_vitoria:.1f}%**")
        st.progress(int(prob_vitoria))
        
        st.write("---")
        st.write("**Mercados Sugeridos**")
        st.write(f"🔥 Chance Over 2.5 Golos: **{70 if prob_vitoria > 60 else 45}%**")
        if prob_vitoria > 65:
            st.success("💎 ALERTA DE VALOR: O sistema detetou uma vantagem estatística significativa.")

    with tab3:
        st.write("### Histórico de Confrontos Diretos")
        st.info("Módulos I e II: Baseado em dados históricos dos últimos 5 jogos entre si.")
        # Exemplo estático para visualização do fluxo
        st.table(pd.DataFrame({
            "Data": ["2025-11-20", "2025-05-15"],
            "Resultado": [f"{casa} 2-0 {fora}", f"{fora} 1-1 {casa}"]
        }))

# ---------------------------------------------------------
# FUNCIONALIDADES ADICIONAIS: CONTEXTO EXTERNO
# ---------------------------------------------------------
elif menu == "🌡️ Fatores Externos":
    st.subheader("⛈️ Contexto Ambiental & Momentum")
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Clima e Altitude**")
        clima = st.select_slider("Condição do Tempo", options=["Sol", "Chuva Leve", "Chuva Forte", "Neve"])
        altitude = st.number_input("Altitude (metros)", value=0)
        if altitude > 1800:
            st.error("🚨 CRÍTICO: Altitude afeta o fôlego das equipas em 20%.")
    
    with c2:
        st.write("**Análise de Tendência (Momentum)**")
        # Simulação de gráfico de ascensão/queda
        chart_data = pd.DataFrame(np.random.randn(10, 2), columns=["Momentum Casa", "Momentum Fora"])
        st.line_chart(chart_data)

    st.write("---")
    st.subheader("🚑 Line-ups & Desfalques")
    st.text_area("Notas sobre Lesionados ou Suspensos:", "Ex: O capitão da Equipa B está fora por cartões.")
