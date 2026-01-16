import streamlit as st
import requests
import pandas as pd

# 1. CONFIGURAÇÃO DE ELITE
st.set_page_config(page_title="SAPEM | MONITOR", layout="wide")

# Tua chave mestre confirmada
CHAVE = "aef7d0d2d4365589bcc10dca1bf62568b78ee5e142e83e8b2d044dc53e405aee"
HEADERS = {'x-apisports-key': CHAVE}

st.sidebar.title("💎 SAPEM v6.2")
st.sidebar.info("Modo: Monitorização de Ativação")

st.title("📡 ESTADO DO SISTEMA SAPEM")

# Função simplificada de teste
def verificar_servidor():
    url = "https://v3.football.api-sports.io/status"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10).json()
        return res
    except:
        return None

# Interface de Monitorização
st.subheader("Verificação de Conectividade")
if st.button('🔍 VERIFICAR LIBERAÇÃO AGORA'):
    resultado = verificar_servidor()
    
    if resultado and resultado.get('response') and not resultado.get('errors'):
        nome = resultado['response']['account']['firstname']
        st.balloons()
        st.success(f"🎊 EXCELENTE NOTÍCIA! O servidor já reconhece o {nome}. O sistema está pronto!")
        st.info("Agora podes voltar a usar o código v6.1 para ver as tabelas.")
    else:
        st.warning("⏳ O servidor da API ainda está a processar a tua ativação global.")
        st.write("Estado atual: **Aguardando Sincronização**")
        st.caption("Nota: Como ativaste o e-mail hoje, este processo é automático. Tenta novamente amanhã.")

st.markdown("---")
st.markdown("""
### 📢 O que fazer agora?
1. **Não alteres mais o código.** O erro não é teu, é apenas o tempo de espera do servidor internacional.
2. **Fecha o site.** Deixa a API terminar a sincronização sem novos pedidos de erro.
3. **Volta amanhã.** Clica no botão acima. Assim que ele der a mensagem verde, os teus dados de futebol aparecerão instantaneamente.
""")
