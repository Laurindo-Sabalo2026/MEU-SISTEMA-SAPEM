import streamlit as st
import requests
import pandas as pd

# Configurações visuais do SAPEM
st.set_page_config(page_title="SAPEM 2026", layout="wide")
st.title("📊 SAPEM | Inteligência Esportiva")

# Sua chave ativa
token = "d63fcb8845c2461da566eed3df05770e"
headers = {'X-Auth-Token': token}

# Barra lateral para interação
st.sidebar.header("Análise por Equipa")
time_input = st.sidebar.text_input("Digite o nome da equipa (ex: Arsenal)", "Arsenal")

# Função para puxar dados reais
@st.cache_data
def carregar_dados():
    url = "https://api.football-data.org/v4/competitions/PD/standings"

data = carregar_dados()
tabela = data['standings'][0]['table']

# Divisão da tela em colunas para visual atraente
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🏆 Tabela Premier League")
    df_lista = [{'Pos': t['position'], 'Time': t['team']['name'], 'Pts': t['points']} for t in tabela]
    st.table(pd.DataFrame(df_lista).set_index('Pos'))

with col2:
    st.subheader(f"🔍 Resultado da Análise: {time_input}")
    stats = next((item for item in tabela if time_input.lower() in item['team']['name'].lower()), None)
    
    if stats:
        jogos = stats['playedGames']
        m_ataque = stats['goalsFor'] / jogos
        m_defesa = stats['goalsAgainst'] / jogos
        
        # Métricas em destaque (Cores automáticas)
        c1, c2, c3 = st.columns(3)
        c1.metric("Aproveitamento", f"{(stats['points']/(jogos*3))*100:.1f}%")
        c2.metric("Poder de Ataque", f"{m_ataque:.2f}")
        c3.metric("Solidez Defensiva", f"{m_defesa:.2f}")
        
        # Sugestão do Campo 5
        st.info("💡 **Campo 5: Sugestão do Sistema**")
        if m_ataque > 1.8:
            st.success(f"O {time_input} é dominante. Alta probabilidade de vitória para o próximo confronto.")
        else:
            st.warning("Análise sugere equilíbrio. Recomenda-se verificar o mercado de cantos ou golos.")
    else:
        st.error("Time não encontrado. Escreva conforme aparece na tabela ao lado.")

st.divider()
st.caption("Sistema SAPEM v1.0 | Dados: Football-Data.org | Jan 2026")
