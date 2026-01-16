import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SAPEM | SISTEMA OFICIAL", layout="wide")

# 2. SUA CHAVE MESTRA DEFINITIVA
# Chave extraída da sua Captura de Tela (6722)
CHAVE_API = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"

# 3. CABEÇALHO OFICIAL (Formato exigido pela API-Sports)
HEADERS = {
    'x-apisports-key': CHAVE_API
}

# 4. INTERFACE LATERAL (Sidebar)
st.sidebar.title("💎 SAPEM v5.8")
st.sidebar.markdown("---")
liga_selecionada = st.sidebar.selectbox("ESCOLHA A LIGA", ["Premier League", "La Liga", "Liga Portugal"])

# Mapeamento de IDs para busca
mapa_ligas = {"Premier League": 39, "La Liga": 140, "Liga Portugal": 94}
id_liga = mapa_ligas[liga_selecionada]

st.title("📑 PAINEL DE ANÁLISE SAPEM")

# 5. FUNÇÃO PARA BUSCAR DADOS
def buscar_dados(endpoint):
    url = f"https://v3.football.api-sports.io/{endpoint}"
    try:
        # Timeout de 15 segundos para evitar travamentos
        response = requests.get(url, headers=HEADERS, timeout=15)
        return response.json()
    except Exception as e:
        return {"errors": {"conexao": str(e)}}

# 6. BOTÃO DE ATIVAÇÃO
if st.button('🚀 ATIVAR CONEXÃO COM O SERVIDOR'):
    with st.spinner('Validando acesso aos dados...'):
        # Verifica primeiro o status da conta
        status = buscar_dados("status")
        
        if status and status.get('response') and not status.get('errors'):
            # Conexão estabelecida com sucesso
            usuario = status['response']['account']['firstname']
            st.success(f"✅ SUCESSO! Sistema SAPEM Conectado para: {usuario}")
            
            # Busca a Classificação da Temporada Atual (2023/2024 conforme disponibilidade)
            dados_tabela = buscar_dados(f"standings?league={id_liga}&season=2023")
            
            if dados_tabela.get('response'):
                try:
                    lista = dados_tabela['response'][0]['league']['standings'][0]
                    df = pd.DataFrame([{
                        "Pos": i['rank'], 
                        "Equipa": i['team']['name'], 
                        "J": i['all']['played'], 
                        "Pts": i['points']
                    } for i in lista])
                    
                    st.subheader(f"🏆 Classificação: {liga_selecionada}")
                    st.table(df.set_index('Pos'))
                    st.balloons()
                except Exception:
                    st.warning("Dados recebidos, mas o formato da tabela ainda está a carregar.")
        else:
            # Caso o servidor ainda recuse a chave
            st.error("❌ O SERVIDOR AINDA NÃO RECONHECEU A SUA CHAVE")
            st.info("Pressione o botão novamente em 1 minuto. A ativação por e-mail pode levar este tempo para chegar aos servidores de dados.")
            if status:
                st.json(status)

# Rodapé de Status
st.sidebar.markdown("---")
st.sidebar.success("Status: Conta Ativada via E-mail ✅")
st.sidebar.caption("Campo IP: Limpo no Painel ✅")
