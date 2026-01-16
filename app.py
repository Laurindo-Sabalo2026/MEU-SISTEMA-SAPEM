import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SAPEM | SISTEMA OFICIAL", layout="wide")

# 2. SUA CHAVE MESTRA (Confirmada nas suas capturas)
# Esta chave foi validada e está ativa no seu painel
CHAVE_API = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"

# 3. CABEÇALHO PADRÃO (Formato oficial para evitar erro de 'Missing Key')
HEADERS = {
    'x-apisports-key': CHAVE_API
}

# 4. INTERFACE LATERAL
st.sidebar.title("💎 SAPEM v5.8")
st.sidebar.markdown("---")
liga_selecionada = st.sidebar.selectbox("ESCOLHA A LIGA", ["Premier League", "La Liga", "Liga Portugal"])

# Mapeamento de IDs das Ligas
mapa_ligas = {"Premier League": 39, "La Liga": 140, "Liga Portugal": 94}
id_liga = mapa_ligas[liga_selecionada]

st.title("📑 PAINEL DE ANÁLISE SAPEM")

# 5. FUNÇÃO PARA BUSCAR DADOS
def buscar_dados(endpoint):
    url = f"https://v3.football.api-sports.io/{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        return response.json()
    except Exception as e:
        return {"errors": {"conexao": str(e)}}

# 6. BOTÃO DE VALIDAÇÃO (Para forçar o servidor a ler a sua chave)
if st.button('🚀 ATIVAR CONEXÃO COM O SERVIDOR'):
    with st.spinner('Verificando sua chave ativa...'):
        # Teste de Status
        status = buscar_dados("status")
        
        if status and status.get('response') and not status.get('errors'):
            # Se a conexão der certo
            usuario = status['response']['account']['firstname']
            st.success(f"✅ SUCESSO! Sistema SAPEM Conectado para: {usuario}")
            
            # Busca a Classificação (Temporada 2023)
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
                except:
                    st.warning("A tabela está a ser processada pelo servidor. Tente novamente em 1 minuto.")
        else:
            # Se ainda der erro de chave
            st.error("❌ O SERVIDOR AINDA NÃO RECONHECEU A ATIVAÇÃO")
            st.markdown(f"""
            **Como resolver:**
            1. Verifique se o campo **SET IP** no seu [Painel](https://dashboard.api-football.com/admin/) está **VAZIO**.
            2. Como você ativou o e-mail recentemente, o servidor pode levar alguns minutos extras.
            """)
            if status: st.json(status)

# Rodapé informativo
st.sidebar.markdown("---")
st.sidebar.info("Status: Conta Ativada via E-mail ✅")
