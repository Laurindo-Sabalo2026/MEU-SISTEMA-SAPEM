import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DE ESTILO PREMIUM (Azul e Dourado)
st.set_page_config(page_title="SAPEM PRO v9.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #001f3f; color: white; }
    h1, h2, h3 { color: #FFD700 !important; font-family: 'Arial Black'; }
    .stMetric { background-color: #002d5a; padding: 20px; border-radius: 15px; border: 2px solid #FFD700; }
    .stButton>button { background-color: #FFD700; color: #001f3f; font-weight: bold; border-radius: 10px; height: 3em; }
    .stDataFrame { border: 1px solid #FFD700; border-radius: 10px; }
    </style>
    """, unsafe_allow_name=True)

# 2. LIGAÇÃO DIRETA AO TEU GOOGLE SHEETS
# Este é o link que extraímos da tua Captura 6794
URL_SISTEMA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=15) # Atualiza quase em tempo real (15 segundos)
def buscar_dados():
    try:
        return pd.read_csv(URL_SISTEMA)
    except:
        return pd.DataFrame({"Aviso": ["A ligar ao Google Sheets..."]})

df = buscar_dados()

# 3. INTERFACE E FERRAMENTAS
st.title("💎 PORTAL SAPEM PROFISSIONAL")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/5329/5329944.png", width=100)
st.sidebar.title("PAINEL DE GESTÃO")
menu = st.sidebar.radio("Navegar para:", ["📊 Tabela de Classificação", "🧮 Calculadora de Probabilidades", "📢 Sobre o Sistema"])

if menu == "📊 Tabela de Classificação":
    st.subheader("🏆 Classificação Realizada por Ti")
    st.write("Estes dados são lidos diretamente da tua folha 'BANCO_DADOS_SAPEM'.")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info("💡 Dica: Muda um valor no Google Sheets e atualiza esta página para ver a mudança!")

elif menu == "🧮 Calculadora de Probabilidades":
    st.subheader("🎯 Simulador de Confrontos SAPEM")
    if "Equipa" in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            casa = st.selectbox("Selecione a Equipa visitada", df["Equipa"].unique())
        with col2:
            fora = st.selectbox("Selecione a Equipa visitante", df["Equipa"].unique())
        
        if st.button("GERAR ANÁLISE DE VITÓRIA"):
            val_casa = df[df["Equipa"] == casa]["Pts"].iloc[0]
            val_fora = df[df["Equipa"] == fora]["Pts"].iloc[0]
            
            # Cálculo de força relativa
            soma = (val_casa + val_fora) if (val_casa + val_fora) > 0 else 1
            percentagem = (val_casa / soma) * 100
            
            st.markdown("---")
            st.metric(label=f"Favoritismo do {casa}", value=f"{percentagem:.1f}%")
            st.progress(int(percentagem))
            st.balloons()
    else:
        st.error("Erro: Coluna 'Equipa' não encontrada na folha de cálculo.")

elif menu == "📢 Sobre o Sistema":
    st.subheader("O teu sistema está Online! ✅")
    st.write("Desenvolvido por: Laurindo Sabalo")
    st.write("Tecnologia: Streamlit + Google Cloud Data")
    st.success("O sistema está a funcionar com os teus próprios servidores de dados.")
