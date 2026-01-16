import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO VISUAL
st.set_page_config(page_title="SAPEM | FINAL", layout="wide")

# 2. SUA CHAVE MESTRA (Confirmada na captura 6722)
CHAVE = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"

# Cabeçalhos duplos para garantir a aceitação do servidor
HEADERS = {
    'x-apisports-key': CHAVE,
    'x-rapidapi-key': CHAVE
}

st.sidebar.title("💎 SAPEM v5.7")
liga = st.sidebar.selectbox("ESCOLHA A LIGA", ["Premier League", "La Liga", "Liga Portugal"])
mapa_ids = {"Premier League": 39, "La Liga": 140, "Liga Portugal": 94}

st.title("📑 ANÁLISE PROFISSIONAL SAPEM")

# 3. FUNÇÃO DE LIGAÇÃO DIRETA
def conectar():
    url = "https://v3.football.api-sports.io/status"
    try:
        # Forçamos o pedido sem cache para o servidor ler a ativação nova
        res = requests.get(url, headers=HEADERS, timeout=20).json()
        return res
    except:
        return None

# 4. BOTÃO DE ATIVAÇÃO NO SITE
if st.button('🔄 VALIDAR CONEXÃO AGORA'):
    dados = conectar()
    
    if dados and dados.get('response') and not dados.get('errors'):
        nome = dados['response']['account']['firstname']
        st.success(f"✅ SUCESSO TOTAL! Bem-vindo, {nome}. O sistema está online.")
        
        # Carregar a Tabela Real
        id_liga = mapa_ids[liga]
        url_tab = f"https://v3.football.api-sports.io/standings?league={id_liga}&season=2023"
        res_tab = requests.get(url_tab, headers=HEADERS).json()
        
        if res_tab.get('response'):
            tabela = res_tab['response'][0]['league']['standings'][0]
            df = pd.DataFrame([{
                "Pos": i['rank'], 
                "Equipa": i['team']['name'], 
                "Pts": i['points'],
                "J": i['all']['played']
            } for i in tabela])
            
            st.subheader(f"🏆 Classificação Atual: {liga}")
            st.table(df.set_index('Pos'))
            st.balloons()
    else:
        st.error("❌ O servidor ainda está a processar a sua chave.")
        st.info("DICA: Como o seu campo IP está limpo, clique no botão acima novamente em 2 minutos.")
        if dados: st.json(dados)
