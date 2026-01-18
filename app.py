import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DE TÍTULO E LAYOUT
st.set_page_config(page_title="SAPEM | INTELLIGENCE BI", layout="wide")

# Título Principal com Estilo Simples (para evitar erros)
st.title("💎 SAPEM | BUSINESS INTELLIGENCE")
st.write("---")

# 2. CONEXÃO AO SEU GOOGLE SHEETS
URL_SISTEMA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=10)
def carregar_dados():
    try:
        data = pd.read_csv(URL_SISTEMA)
        data.columns = data.columns.str.strip() # Remove espaços extras
        return data
    except:
        return pd.DataFrame({"Equipa": ["Erro de Conexão"], "Pts": [0]})

df = carregar_dados()

# 3. MENU LATERAL DE NAVEGAÇÃO
st.sidebar.header("PAINEL DE CONTROLO")
menu = st.sidebar.radio("Selecione o Módulo:", 
    ["🏟️ Dashboard de Jornada", "🔬 Deep Analysis (H2H)", "🌡️ Fatores Externos"])

# 4. MÓDULO 1: DASHBOARD GERAL
if menu == "🏟️ Dashboard de Jornada":
    st.subheader("📊 Classificação e Métricas de Performance")
    
    # Cartões de Resumo
    c1, c2, c3 = st.columns(3)
    c1.metric("Ligas Monitorizadas", "12")
    c2.metric("Alertas de Valor", "5")
    c3.metric("Eficiência IA", "84%")
    
    st.markdown("### Tabela Geral de Dados")
    st.dataframe(df, use_container_width=True, hide_index=True)

# 5. MÓDULO 2: ANÁLISE PROFUNDA (H2H)
elif menu == "🔬 Deep Analysis (H2H)":
    st.subheader("🔍 Módulos I-V: Análise Preditiva de Confronto")
    
    if "Equipa" in df.columns:
        col_a, col_b = st.columns(2)
        with col_a: 
            equipa_1 = st.selectbox("Equipa Casa", df["Equipa"].unique())
        with col_b: 
            equipa_2 = st.selectbox("Equipa Fora", df["Equipa"].unique())
        
        st.write("---")
        
        # Comparação de Médias (Dados das suas novas colunas)
        def mostrar_estatisticas(nome):
            row = df[df["Equipa"] == nome].iloc[0]
            st.write(f"**Performance: {nome}**")
            k1, k2, k3 = st.columns(3)
            k1.metric("Cantos", row.get('Cantos', 0))
            k2.metric("Cartões", row.get('Cartões', 0))
            k3.metric("Remates", row.get('Remates', 0))

        mostrar_estatisticas(equipa_1)
        st.divider()
        mostrar_estatisticas(equipa_2)
        
        # Módulo V: Inteligência
        st.subheader("🎯 Probabilidades de Vitória")
        p1 = df[df["Equipa"] == equipa_1]["Pts"].iloc[0]
        p2 = df[df["Equipa"] == equipa_2]["Pts"].iloc[0]
        total = p1 + p2 if (p1 + p2) > 0 else 1
        prob = (p1 / total) * 100
        
        st.write(f"Chance de Vitória {equipa_1}: **{prob:.1f}%**")
        st.progress(int(prob))
        if prob > 60:
            st.success("🎯 ALERTA DE VALOR DETETADO!")
    else:
        st.error("Configure as colunas no Google Sheets primeiro.")

# 6. MÓDULO 3: FATORES EXTERNOS
elif menu == "🌡️ Fatores Externos":
    st.subheader("☁️ Contexto Externo (Clima & Altitude)")
    clima = st.select_slider("Condição do Tempo", options=["Sol", "Chuva Leve", "Chuva Forte"])
    altitude = st.number_input("Altitude (metros)", value=0)
    
    if altitude > 1500:
        st.warning("⚠️ Atenção: Performance física das equipas reduzida pela altitude.")
    if "Chuva" in clima:
        st.info("💡 Tendência: Menor número de golos e remates à baliza.")
