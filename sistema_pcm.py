import streamlit as st
import pandas as pd
import requests
from datetime import date
import numpy as np

# --- CONEXÃO ---
SUPABASE_URL = "https://dgitrtndyisotaowpsch.supabase.co"
SUPABASE_KEY = "SUA_CHAVE_AQUI" # COLOQUE SUA CHAVE AQUI

st.set_page_config(page_title="PCM ADF", layout="wide")

def carregar_dados():
    try:
        url = f"{SUPABASE_URL}/rest/v1/ordens_servico?select=*"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        response = requests.get(url, headers=headers)
        return pd.DataFrame(response.json())
    except:
        return pd.DataFrame()

def salvar_no_banco(item):
    url = f"{SUPABASE_URL}/rest/v1/ordens_servico"
    headers = {
        "apikey": SUPABASE_KEY, 
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    res = requests.post(url, headers=headers, json=[item])
    return res.status_code

# --- INTERFACE ---
df_atual = carregar_dados()

st.title("🏭 Sistema PCM - ADF Ondulados")

# Gerando o ID
prox_id = int(df_atual['ID'].max() + 1) if not df_atual.empty else 1
st.subheader(f"Nova Ordem de Serviço: #{prox_id}")

col1, col2 = st.columns(2)
maquina = col1.selectbox("Máquina", ["MÁQUINA DE PAPEL", "ONDULADEIRA", "HIDRAPULPER", "OUTROS"])
tecnico = col2.selectbox("Técnico", ["MARCOS", "ADEMIR", "LUAN", "ISRAEL"])
servico = st.text_area("Descrição do Serviço", key="desc_input")

# BOTÃO DIRETO (SEM FORMULÁRIO PARA NÃO TRAVAR)
if st.button("EMITIR ORDEM DE SERVIÇO", type="primary"):
    if not servico:
        st.warning("⚠️ Por favor, descreva o problema antes de salvar.")
    else:
        dados = {
            "ID": prox_id,
            "Data_Emissao": str(date.today()),
            "Maquina": maquina,
            "Responsavel": tecnico,
            "Descricao_Pedido": servico,
            "Status": "ABERTA",
            "Diagnostico": None, # Garante que envie nulo se o banco permitir
            "Solucao": None
        }
        
        with st.spinner('Salvando na nuvem...'):
            resultado = salvar_no_banco(dados)
            
            if resultado in [200, 201, 204]:
                st.success(f"✅ SUCESSO! OS #{prox_id} foi gravada no banco.")
                st.balloons()
                st.info("A página irá recarregar em 3 segundos...")
                import time
                time.sleep(3)
                st.rerun()
            else:
                st.error(f"❌ Erro no Banco: Código {resultado}. Tente novamente.")