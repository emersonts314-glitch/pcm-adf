import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime, date, timedelta
import os
import numpy as np
import requests

# --- CONEXÃO COM A NUVEM ---
SUPABASE_URL = "https://dgitrtndyisotaowpsch.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRnaXRydG5keWlzb3Rhb3dwc2NoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1MTU0MTQsImV4cCI6MjA4NzA5MTQxNH0.-EjzxfPhyVSsErcstOt8D2nITVxmC3wFoXQTbYtqn1o"

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="PCM - ADF Ondulados", layout="wide", page_icon="🏭")

# --- LISTAS DE CADASTRO ---
LISTA_MAQUINAS = ["ESTEIRA DE ALIMENTAÇÃO DO HIDRAPULPER","HIDRAPULPER 1","DESCONTAMINADOR","BOMBA DE MASSA O HIDRAPULPER 1","CCM 1 (PREPARO DE MASSA)","TRANSFORMADOR 1 (PREPARO DE MASSA)","BOMBA DE ÁGUA DO DESCONTAMINADOR","REFINADOR 1","PENEIRA VIBRATÓRIA","TURBO SEPARADOR","DEPURADOR PRIMÁRIO (DPI)","DEPURADOR HR 12 (FINE SCREEN-1° ESTÁGIO)","DEPURADOR HR 18 (FINE SCREEN-2° ESTÁGIO)","DEPURADOR HR 24 (FINE SCREEN-3° ESTÁGIO)","BOMBA DE ÁGUA DE  DILUIÇÃO DO HR 18","BOMBA DE ÁGUA DE  DILUIÇÃO DO HR 12","1° ESTÁGIO DE CLEANER","2° ESTÁGIO DE CLEANER","BOMBA DE MASSA DO 2° ESTÁGIO DE CLEANER","SIDE HILL 1","SIDE HILL 2","PENEIRA ESTÁTICA DO REJEITO DO HR 12","TM 1 (TANQUE DE MASSA)","TM 2 (TANQUE DE MASSA)","TM 3 (TANQUE DE MASSA)","TM 4 (TANQUE DE MASSA)","TA 1 (TANQUE DE ÁGUA)","TA 2 (TANQUE DE ÁGUA)","AGITADOR DO TM 1","AGITADOR DO TM 2","AGITADOR DO TM 3","AGITADOR DO TM 4","CLEANER DE ALTA CONSISTÊNCIA (HD)","BOMBA DE ÁGUA DO POÇO ARTESIANO","BOMBA DE ÁGUA DE COMBATE A INCÊNDIO 1","BOMBA DE ÁGUA DE COMBATE A INCÊNDIO 2","BOMBA DE ÁGUA DE COMBATE A INCÊNDIO 3","BOMDA DE ÁGUA DE ALIMENTAÇÃO DO PREPARO DE MASSA","BOMBA DE MASSA DO 1° ESTÁGIO DO CLEANER","BOMBA DE ÁGUA DE DILUIÇÃO DO FINE SCREEN","BOMBA DE ÁGUA DE LIMPEZA","BOMBA DE ÁGUA DE ELUTRIAÇÃO DOS CLEANERS","BOMBA DE ÁGUA DO HIDRAPULPER 2/SILO","BOMBA DE ÁGUA DO CONTROLE DE CONSISTÊNCIA","BOMBA DE MASSA DO TANQUE 2 (REFINADOR)","BOMBA DE MASSA DE TRANSBORDO CANALETA 1","BOMBA DE MASSA DE TRANSBORDO CANALETA 2","BOMBA DE MASSA DO TM 1","BOMBA DE MASSA DO TM 3","BOMBA DE MASSA DO TM 4 (GRAMATURA)","ROSCA DE REJEITO DE AREIA","BOMBA DO SEPARADOR DE VÁCUO PK","BOMBA DE VÁCUO 1 (MESA PLANA)","BOMBA DE VÁCUO 2 (ROLO DE SUCÇÃO)","BOMBA DE VÁCUO 3 (FELTRO)","BOMBA DE VÁCUO 4 (FELTRO)","MÁQUINA DE PAPEL","UNIDADE HIDRÁULICA DAS PRENSAS","VENTILADOR DE BAIXO VÁCUO (ROLO PICADO)","EXAUSTOR DO FILTRO DE MANGA","CCM 2 (MÁQUINA DE PAPEL)","QGBT","TRANSFORMADOR 2","COMPRESSOR DE PARAFUSO 1","COMPRESSOR DE PARAFUSO 2","PICADOR DE REFILE DA REBOBINADEIRA","BOMBA DE MISTURA","BOMBA DE SELAGEM DO VÁCUO","EXAUSTOR DE BAIXO VÁCUO DA MESA","DEPURADOR CABEÇA DE MÁQUINA (HR 24)","BOMBA DO WIREPIT","BOMBA DO COUCHPIT","AGITADOR DO COUCHPIT","ATENUADOR DE PULSAÇÃO","CAIXA DE ENTRADA DA MESA PLANA","CHUVEIRO OSCILADOR","ROLO CABECEIRA","ROLO DE SUCÇÃO","ROLO ACIONADOR","ROLO RASPADOR","1° PRENSA","2° PRENSA","CHUVEIRO OSCILADOR DO FILTRO TANDEM","CHUVEIRO OSCILADOR DA 1° PRENSA","CHUVEIRO OSCILADOR DA 2° PRENSA","ROLO PICKUP","CILINDRO SECADOR BABY","ESTICADOR DE CORDA DO 1° GRUPO","RASPAS DST 1","RASPAS DST 2","RASPAS DST 3","ESTICADOR DE CORDA DO 2° GRUPO","ESTICADOR DE CORDA DO 3° GRUPO","UNIDADE HIDRÁULICA DA SECAGEM","TANQUE SEPARADOR DO CONDENSADO DO 1° GRUPO","BOMBA DO BICO DE CORTE","BOMBA DO CHUVEIRO OSCILADOR","CAVALETE DE CONTROLE DO 1° GRUPO","CAVALETE DE CONTROLE DO 2° GRUPO","CAVALETE DE CONTROLE DO 3° GRUPO","COLETOR DE DISTRIBUIÇÃO DE VAPOR","ENROLADEIRA","MONOVIA","HIDRAPULPER 2","BOMBA DE MASSA DO HIDRAPULPER 2","FILTRO SEPARADOR DE REFILE","CORTADOR DE TUBETE","DESENROLADEIRA","REBOBINADEIRA","LAVA BOTAS","BALANÇA 1","BALANÇA RODOVIÁRIA","ROTA DE INSPEÇÃO 1", "ROTA DE INSPEÇÃO 2", "ROTA DE INSPEÇÃO 3", "ROTA DE INSPEÇÃO 4","ROTA DE INSPEÇÃO 5", "ROTA DE INSPEÇÃO 6", "ROTA DE INSPEÇÃO 7", "ROTA DE INSPEÇÃO 8","ROTA DE INSPEÇÃO 9","ROTA DE INSPEÇÃO 10", "ROTA DE INSPEÇÃO 11", "ROTA DE INSPEÇÃO 12","ROTA DE LUBRIFICAÇÃO","UTILIDADES","ONDULADEIRA","ROTA DE INSPEÇÃO DOS PAINÉIS","INSPEÇÃO VISUAL","SETOR MANUTENÇÃO","SETOR ONDULADEIRA","SETOR PREPARO DE MASSA","SETOR PÁTIO"]
LISTA_SETORES = ["MECÂNICA", "ELÉTRICA", "PREDIAL", "UTILIDADES"]
LISTA_TIPOS_MANUTENCAO = ["PREVENTIVA", "CORRETIVA EMERGENCIAL", "CORRETIVA PROGRAMADA", "PREDITIVA", "MELHORIA", "LUBRIFICAÇÃO"]
LISTA_TECNICOS = ["MARCOS", "ADEMIR", "LUAN", "ISRAEL", "ANDERSON", "JGA", "IVAN", "DIEYSON", "GILMAR","LUCAS","FERNANDO"]

# --- FUNÇÕES DE DADOS ---
def carregar_dados():
    try:
        url = f"{SUPABASE_URL}/rest/v1/ordens_servico?select=*"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        response = requests.get(url, headers=headers)
        df = pd.DataFrame(response.json())
        if not df.empty:
            df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)
            for c in ['Data_Emissao', 'Data_Inicio', 'Data_Fim']:
                if c in df.columns:
                    df[c] = pd.to_datetime(df[c], errors='coerce').dt.date
        return df
    except: return pd.DataFrame()

def salvar_dados(df_to_save):
    try:
        # Prepara os dados: remove NaNs e garante formatos compatíveis
        df_final = df_to_save.copy()
        # Converte tudo para string para evitar erro de tipo no banco (Exceto ID)
        for col in df_final.columns:
            if col != 'ID':
                df_final[col] = df_final[col].apply(lambda x: str(x) if pd.notnull(x) and x != "" else None)
        
        records = df_final.to_dict(orient='records')
        for r in records: r['ID'] = int(r['ID'])

        url = f"{SUPABASE_URL}/rest/v1/ordens_servico"
        headers = {
            "apikey": SUPABASE_KEY, 
            "Authorization": f"Bearer {SUPABASE_KEY}", 
            "Content-Type": "application/json", 
            "Prefer": "resolution=merge-duplicates"
        }
        response = requests.post(url, headers=headers, json=records)
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Erro técnico ao salvar: {e}")
        if hasattr(e, 'response') and e.response is not None:
            st.warning(f"Detalhe do Banco: {e.response.text}")
        return False

# --- INTERFACE ---
df = carregar_dados()
menu = st.sidebar.radio("MENU", ["1. Emitir Ordem", "2. Dashboard"])

if menu == "1. Emitir Ordem":
    st.title("📄 Nova Ordem de Serviço")
    prox_id = int(df['ID'].max() + 1) if not df.empty else 1
    st.subheader(f"OS #{prox_id}")
    
    with st.container():
        col1, col2 = st.columns(2)
        dt = col1.date_input("Data", date.today())
        maq = col1.selectbox("Máquina", LISTA_MAQUINAS)
        setor = col2.selectbox("Setor", LISTA_SETORES)
        tipo = col2.selectbox("Tipo", LISTA_TIPOS_MANUTENCAO)
        resp = st.selectbox("Responsável", LISTA_TECNICOS)
        desc = st.text_area("Descrição do Serviço")
        
        if st.button("EMITIR ORDEM DE SERVIÇO", type="primary"):
            if not desc:
                st.warning("⚠️ Descreva o serviço antes de emitir.")
            else:
                # Cria o dicionário garantindo que campos vazios sejam None (NULL no banco)
                nova_os = {
                    "ID": prox_id, "Data_Emissao": dt, "Maquina": maq, "Responsavel": resp,
                    "Tipo_Manutencao": tipo, "Setor": setor, "Descricao_Pedido": desc, "Status": "ABERTA",
                    "Diagnostico": None, "Solucao": None, "Tecnico": None, "Horas_Totais": 0.0
                }
                df_envio = pd.concat([df, pd.DataFrame([nova_os])], ignore_index=True)
                if salvar_dados(df_envio):
                    st.success(f"✅ OS #{prox_id} salva com sucesso!")
                    st.balloons()
                    st.rerun()

elif menu == "2. Dashboard":
    st.title("📊 Indicadores")
    if not df.empty:
        st.plotly_chart(px.bar(df, x="Maquina", title="OS por Máquina"))
    else: st.info("Carregando dados da nuvem...")