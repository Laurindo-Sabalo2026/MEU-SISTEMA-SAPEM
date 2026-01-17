import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SAPEM | SISTEMA INDEPENDENTE", layout="wide")

st.sidebar.title("💎 SAPEM v7.0")
st.sidebar.info("Modo: Dados Diretos (Ativo)")

st.title("⚽ Portal de Dados SAPEM")
st.markdown("---")

# 2. MOTOR DE DADOS (Independente de API externa)
def carregar_classificacao(liga):
    if liga == "Premier League":
        dados = {
            "Pos": [1, 2, 3, 4, 5],
            "Equipa": ["Liverpool", "Man. City", "Arsenal", "Aston Villa", "Tottenham"],
            "Pts": [45, 43, 40, 38, 36],
            "J": [20, 20, 20, 20, 20]
        }
    elif liga == "Liga Portugal":
        dados = {
            "Pos": [1, 2, 3, 4, 5],
            "Equipa": ["Sporting CP", "Benfica", "FC Porto", "Braga", "Vitória SC"],
            "Pts": [46, 45, 38, 33, 30],
            "J": [18, 18, 18, 18, 18]
        }
    else:
        dados = {
            "Pos": [1, 2, 3, 4, 5],
            "Equipa": ["Real Madrid", "Girona", "Barcelona", "Atlético Madrid", "Athletic Bilbao"],
            "Pts": [48, 48, 41, 38, 38],
            "J": [19, 19, 19, 19, 19]
        }
    return pd.DataFrame(dados)

# 3. INTERFACE DO UTILIZADOR
col1, col2 = st.columns([1, 3])

with col1:
    escolha = st.radio("Selecione a Liga:", ["Premier League", "La Liga", "Liga Portugal"])

with col2:
    st.subheader(f"🏆 Tabela de Classificação: {escolha}")
    df = carregar_classificacao(escolha)
    st.table(df.set_index('Pos'))

st.markdown("---")
st.success("✅ Sistema operacional e independente de chaves externas.")
st.balloons()
