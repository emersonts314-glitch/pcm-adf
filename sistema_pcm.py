import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import date

# --- CONFIGURAÇÕES DE CONEXÃO ---
SUPABASE_URL = "https://dgitrtndyisotaowpsch.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRnaXRydG5keWlzb3Rhb3dwc2NoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1MTU0MTQsImV4cCI6MjA4NzA5MTQxNH0.-EjzxfPhyVSsErcstOt8D2nITVxmC3wFoXQTbYtqn1o"

def carregar_dados():
    try:
        url = f"{SUPABASE_URL}/rest/v1/ordens_servico?select=*"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        response = requests.get(url, headers=headers)
        return pd.DataFrame(response.json())
    except:
        return pd.DataFrame()

def salvar_dados(registro):
    url = f"{SUPABASE_URL}/rest/v1/ordens_servico"
    headers = {
        "apikey": SUPABASE_KEY, 
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    # Tratamento para garantir que campos vazios sejam enviados como nulos
    for chave, valor in registro.items():
        if valor == "" or pd.isna(valor):
            registro[chave] = None
            
    response = requests.post(url, headers=headers, json=[registro])
    return response

# --- INTERFACE DO USUÁRIO ---
st.title("Sistema PCM - ADF Ondulados")
df = carregar_dados()

menu = st.sidebar.radio("Navegação", ["Emitir Ordem", "Dashboard"])

if menu == "Emitir Ordem":
    st.subheader("Nova Ordem de Serviço")
    prox_id = int(df['ID'].max() + 1) if not df.empty else 1
    
    with st.form("form_os"):
        col1, col2 = st.columns(2)
        maq = col1.selectbox("Máquina", ["UTILIDADES", "MÁQUINA DE PAPEL", "ONDULADEIRA"])
        resp = col2.selectbox("Responsável", ["LUCAS", "MARCOS", "ADEMIR"])
        desc = st.text_area("Descrição do Serviço")
        
        if st.form_submit_button("EMITIR ORDEM DE SERVIÇO"):
            nova_os = {
                "ID": prox_id,
                "Data_Emissao": str(date.today()),
                "Maquina": maq,
                "Responsavel": resp,
                "Descricao_Pedido": desc,
                "Status": "ABERTA",
                "Diagnostico": "", # Será tratado como None pela função salvar_dados
                "Solucao": ""
            }
            res = salvar_dados(nova_os)
            if res.status_code in [200, 201, 204]:
                st.success(f"OS #{prox_id} emitida com sucesso!")
                st.rerun()
            else:
                st.error(f"Erro ao salvar: {res.status_code}")
                st.write(res.text)