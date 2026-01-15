import streamlit as st
import requests
import pandas as pd

# Configurações visuais do SAPEM
st.set_page_config(page_title="SAPEM 2026", layout="wide")
st.title("📊 SAPEM | Inteligência Esportiva")

# Sua chave ativa
token = "d63fcb8845c2461da566eed3df05770e"
headers = {'X-Auth-Token': token}

# Barra lateral para escolher a liga
st.sidebar.header("Configurações")
liga_escolhida = st.sidebar.selectbox(
    "Selecione a Liga:",
    ["Premier League", "Liga Portuguesa", "La Liga (Espanha)"]
)

# Dicionário de códigos das ligas
codigos = {
    "Premier League": "PL",
    "Liga Portuguesa": "PPL",
    "La Liga (Espanha)": "PD"
}

# Função para puxar dados reais com proteção contra erros
@st.cache_data
def carregar_dados(codigo_liga):
    url = f"https://api.football-data.org/v4/competitions/{codigo_liga}/standings"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except:
        return None

data = carregar_dados(codigos[liga_escolhida])

# Verifica se os dados chegaram corretamente para evitar o erro da imagem 6621
if data and 'standings' in data:
    tabela_bruta = data['standings'][0]['table']
    df = pd.DataFrame(tabela_bruta)
    
    # Organiza a tabela para exibição
    df_exibir = df[['position', 'team', 'points']].copy()
    df_exibir['team'] = df_exibir['team'].apply(lambda x: x['name'])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"🏆 Tabela: {liga_escolhida}")
        st.table(df_exibir.set_index('position'))
    
    with col2:
        st.subheader("🔍 Análise por Equipa")
        time_input = st.selectbox("Escolha a equipa para analisar:", df_exibir['team'].tolist())
        st.success(f"O {time_input} está sendo analisado com sucesso!")
else:
    st.error("Erro ao carregar dados. Por favor, aguarde 1 minuto e recarregue a página.")
