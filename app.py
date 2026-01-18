import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO BÁSICA
st.set_page_config(page_title="SAPEM PRO v9.1", layout="wide")

# Interface simplificada para evitar erros de CSS
st.title("💎 PORTAL SAPEM PROFISSIONAL")
st.markdown("---")

# 2. LIGAÇÃO DIRETA AO TEU GOOGLE SHEETS
# Link extraído da sua Captura 6794
URL_SISTEMA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE8YnGNNpBx1bdES3fZAS1kKoQiW2q66WuKy-EO3Zb_W61zKRuO7JuoTebY9UTfim1J7MDfnrmRb3p/pub?output=csv"

@st.cache_data(ttl=15)
def buscar_dados():
    try:
        dados = pd.read_csv(URL_SISTEMA)
        return dados
    except Exception as e:
        return pd.DataFrame({"Status": ["A carregar dados..."], "Info": [str(e)]})

df = buscar_dados()

# 3. NAVEGAÇÃO
menu = st.sidebar.radio("Navegar para:", ["📊 Tabela de Classificação", "🧮 Calculadora de Probabilidades"])

if menu == "📊 Tabela de Classificação":
    st.subheader("🏆 Classificação em Tempo Real")
    st.write("Dados sincronizados com o seu Google Sheets.")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    if st.button("🔄 Atualizar Agora"):
        st.cache_data.clear()
        st.rerun()

elif menu == "🧮 Calculadora de Probabilidades":
    st.subheader("🎯 Simulador de Confrontos")
    
    if "Equipa" in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            casa = st.selectbox("Equipa Visitada", df["Equipa"].unique())
        with col2:
            fora = st.selectbox("Equipa Visitante", df["Equipa"].unique())
        
        if st.button("CALCULAR CHANCES"):
            pts_casa = df[df["Equipa"] == casa]["Pts"].iloc[0]
            pts_fora = df[df["Equipa"] == fora]["Pts"].iloc[0]
            
            soma = (pts_casa + pts_fora) if (pts_casa + pts_fora) > 0 else 1
            percentagem = (pts_casa / soma) * 100
            
            st.metric(f"Favoritismo: {casa}", f"{percentagem:.1f}%")
            st.progress(int(percentagem))
            st.balloons()
    else:
        st.warning("Aguardando sincronização de colunas do Google Sheets...")
