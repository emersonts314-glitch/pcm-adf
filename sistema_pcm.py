import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime, date, timedelta
import os
import numpy as np
import requests

# --- CONEXÃO COM A NUVEM (SUPABASE VIA API DIRETA) ---
# Substitua os valores abaixo pelos seus dados do Supabase
SUPABASE_URL = "https://dgitrtndyisotaowpsch.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRnaXRydG5keWlzb3Rhb3dwc2NoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1MTU0MTQsImV4cCI6MjA4NzA5MTQxNH0.-EjzxfPhyVSsErcstOt8D2nITVxmC3wFoXQTbYtqn1o"

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="PCM - ADF Ondulados", layout="wide", page_icon="🏭")

# --- ARQUIVOS LOCAIS (HÍBRIDO) ---
NOME_ARQUIVO_LOGO = 'logo.png' 

NOMES_POSSIVEIS_LUB = [
    'dados_lubrificacao.csv',
    'dados_lubrificacao.csv.csv',
    'CONTROLE DE LUBRIFICAÇÃO.xlsx - Dados.csv',
    'Dados.csv'
]

NOMES_POSSIVEIS_ESTOQUE = [
    'estoque_lubrificantes.csv',
    'estoque_lubrificantes.csv.csv',
    'CONTROLE DE LUBRIFICAÇÃO.xlsx - controle de lubrificantes.csv',
    'controle de lubrificantes.csv'
]

# ==============================================================================
# --- 📝 LISTAS DE CADASTRO ---
# ==============================================================================

LISTA_MAQUINAS = [
    "ESTEIRA DE ALIMENTAÇÃO DO HIDRAPULPER","HIDRAPULPER 1","DESCONTAMINADOR","BOMBA DE MASSA O HIDRAPULPER 1","CCM 1 (PREPARO DE MASSA)","TRANSFORMADOR 1 (PREPARO DE MASSA)"
,"BOMBA DE ÁGUA DO DESCONTAMINADOR","REFINADOR 1","PENEIRA VIBRATÓRIA","TURBO SEPARADOR","DEPURADOR PRIMÁRIO (DPI)","DEPURADOR HR 12 (FINE SCREEN-1° ESTÁGIO)"
,"DEPURADOR HR 18 (FINE SCREEN-2° ESTÁGIO)","DEPURADOR HR 24 (FINE SCREEN-3° ESTÁGIO)","BOMBA DE ÁGUA DE  DILUIÇÃO DO HR 18","BOMBA DE ÁGUA DE  DILUIÇÃO DO HR 12"
,"1° ESTÁGIO DE CLEANER","2° ESTÁGIO DE CLEANER","BOMBA DE MASSA DO 2° ESTÁGIO DE CLEANER","SIDE HILL 1","SIDE HILL 2","PENEIRA ESTÁTICA DO REJEITO DO HR 12"
,"TM 1 (TANQUE DE MASSA)","TM 2 (TANQUE DE MASSA)","TM 3 (TANQUE DE MASSA)","TM 4 (TANQUE DE MASSA)","TA 1 (TANQUE DE ÁGUA)","TA 2 (TANQUE DE ÁGUA)"
,"AGITADOR DO TM 1","AGITADOR DO TM 2","AGITADOR DO TM 3","AGITADOR DO TM 4","CLEANER DE ALTA CONSISTÊNCIA (HD)","BOMBA DE ÁGUA DO POÇO ARTESIANO"
,"BOMBA DE ÁGUA DE COMBATE A INCÊNDIO 1","BOMBA DE ÁGUA DE COMBATE A INCÊNDIO 2","BOMBA DE ÁGUA DE COMBATE A INCÊNDIO 3","BOMDA DE ÁGUA DE ALIMENTAÇÃO DO PREPARO DE MASSA"
,"BOMBA DE MASSA DO 1° ESTÁGIO DO CLEANER","BOMBA DE ÁGUA DE DILUIÇÃO DO FINE SCREEN","BOMBA DE ÁGUA DE LIMPEZA","BOMBA DE ÁGUA DE ELUTRIAÇÃO DOS CLEANERS"
,"BOMBA DE ÁGUA DO HIDRAPULPER 2/SILO","BOMBA DE ÁGUA DO CONTROLE DE CONSISTÊNCIA","BOMBA DE MASSA DO TANQUE 2 (REFINADOR)","BOMBA DE MASSA DE TRANSBORDO CANALETA 1"
,"BOMBA DE MASSA DE TRANSBORDO CANALETA 2","BOMBA DE MASSA DO TM 1","BOMBA DE MASSA DO TM 3","BOMBA DE MASSA DO TM 4 (GRAMATURA)","ROSCA DE REJEITO DE AREIA"
,"BOMBA DO SEPARADOR DE VÁCUO PK","BOMBA DE VÁCUO 1 (MESA PLANA)","BOMBA DE VÁCUO 2 (ROLO DE SUCÇÃO)","BOMBA DE VÁCUO 3 (FELTRO)","BOMBA DE VÁCUO 4 (FELTRO)"
,"MÁQUINA DE PAPEL","UNIDADE HIDRÁULICA DAS PRENSAS","VENTILADOR DE BAIXO VÁCUO (ROLO PICADO)","EXAUSTOR DO FILTRO DE MANGA","CCM 2 (MÁQUINA DE PAPEL)"
,"QGBT","TRANSFORMADOR 2","COMPRESSOR DE PARAFUSO 1","COMPRESSOR DE PARAFUSO 2","PICADOR DE REFILE DA REBOBINADEIRA","BOMBA DE MISTURA","BOMBA DE SELAGEM DO VÁCUO"
,"EXAUSTOR DE BAIXO VÁCUO DA MESA","DEPURADOR CABEÇA DE MÁQUINA (HR 24)","BOMBA DO WIREPIT","BOMBA DO COUCHPIT","AGITADOR DO COUCHPIT","ATENUADOR DE PULSAÇÃO"
,"CAIXA DE ENTRADA DA MESA PLANA","CHUVEIRO OSCILADOR","ROLO CABECEIRA","ROLO DE SUCÇÃO","ROLO ACIONADOR","ROLO RASPADOR","1° PRENSA","2° PRENSA"
,"CHUVEIRO OSCILADOR DO FILTRO TANDEM","CHUVEIRO OSCILADOR DA 1° PRENSA","CHUVEIRO OSCILADOR DA 2° PRENSA","ROLO PICKUP","CILINDRO SECADOR BABY"
,"ESTICADOR DE CORDA DO 1° GRUPO","RASPAS DST 1","RASPAS DST 2","RASPAS DST 3","ESTICADOR DE CORDA DO 2° GRUPO","ESTICADOR DE CORDA DO 3° GRUPO"
,"UNIDADE HIDRÁULICA DA SECAGEM","TANQUE SEPARADOR DO CONDENSADO DO 1° GRUPO","BOMBA DO BICO DE CORTE","BOMBA DO CHUVEIRO OSCILADOR","CAVALETE DE CONTROLE DO 1° GRUPO"
,"CAVALETE DE CONTROLE DO 2° GRUPO","CAVALETE DE CONTROLE DO 3° GRUPO","COLETOR DE DISTRIBUIÇÃO DE VAPOR","ENROLADEIRA","MONOVIA","HIDRAPULPER 2"
,"BOMBA DE MASSA DO HIDRAPULPER 2","FILTRO SEPARADOR DE REFILE","CORTADOR DE TUBETE","DESENROLADEIRA","REBOBINADEIRA","LAVA BOTAS","BALANÇA 1","BALANÇA RODOVIÁRIA"
,"ROTA DE INSPEÇÃO 1", "ROTA DE INSPEÇÃO 2", "ROTA DE INSPEÇÃO 3", "ROTA DE INSPEÇÃO 4","ROTA DE INSPEÇÃO 5", "ROTA DE INSPEÇÃO 6", "ROTA DE INSPEÇÃO 7", "ROTA DE INSPEÇÃO 8",
"ROTA DE INSPEÇÃO 9","ROTA DE INSPEÇÃO 10", "ROTA DE INSPEÇÃO 11", "ROTA DE INSPEÇÃO 12","ROTA DE LUBRIFICAÇÃO","UTILIDADES","ONDULADEIRA"
,"ROTA DE INSPEÇÃO DOS PAINÉIS","INSPEÇÃO VISUAL","SETOR MANUTENÇÃO","SETOR ONDULADEIRA","SETOR PREPARO DE MASSA","SETOR PÁTIO"
]

LISTA_SETORES = ["MECÂNICA", "ELÉTRICA", "PREDIAL", "UTILIDADES"]
LISTA_TIPOS_MANUTENCAO = ["PREVENTIVA", "CORRETIVA EMERGENCIAL", "CORRETIVA PROGRAMADA", "PREDITIVA", "MELHORIA", "LUBRIFICAÇÃO"]
LISTA_TIPOS_PROBLEMA = ["VAZAMENTO DE ÁGUA/MASSA", "VAZAMENTO DE AR", "VAZAMENTO DE ÓLEO", "QUEBRA DE ROLAMENTO", "ROMPIMENTO DE CORREIA", "QUEBRA DE ENGRENAGEM OU POLIA", "SELAMENTO","FUSIVEL/DISJUNTOR QUEIMADO", "QUEBRA DE MANCAL/BUCHA", "QUEIMA DE MOTOR/BOMBA","DESALINHAMENTO", "PARAFUSOS SOLTOS/QUEBRADOS","OBSTRUÇÃO POR CORPO ESTRANHO", "VEDAÇÕES/VÁLVULAS COM PROBLEMA","PROBLEMA ESTRUTURAL","MOTOR DESARMADO","PROBLEMA NO PORTÃO DE ENTRADA","SISTEMA ELÉTRICO EM FALHA"]
LISTA_PECAS_SUGESTAO = ["ROLAMENTO NU310", "ROLAMENTO 3310","ROLAMENTO 6207","ROLAMENTO 22315 EAE C3","ROLAMENTO 22318 EJW C3","CORREIA C70", "CORREIA 5V 1500","RETENTOR 110X130X13","DISCO DO REFINADOR","FACA DE ONDULADEIRA","ROLAMENTO 23222","MOTOR GENÉRICO","CORREIA 5V 1250", "CORREIA LISA 70X1700","BUCHA INOX 179X60","ROLAMENTO 6205","ROLAMENTO 6001","ROLAMENTO 6303","CORREIA C156","ROLAMENTO 22216", "BUCHA H316","CORREIA C100","CORREIA 270H","CORREIA B60","CORREIA 131","ROLAMENTO 6208"]
LISTA_TECNICOS = ["MARCOS", "ADEMIR", "LUAN", "ISRAEL", "ANDERSON", "JGA", "IVAN", "DIEYSON", "GILMAR","LUCAS","FERNANDO"]

# ==============================================================================

# --- FUNÇÕES DE ARQUIVO E FORMATAÇÃO ---
def encontrar_arquivo(lista_nomes):
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    for nome in lista_nomes:
        caminho = os.path.join(pasta_atual, nome)
        if os.path.exists(caminho): return caminho
    return None

def encontrar_logo():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    nomes = ['logo.png', 'logo.png.png', 'Logo.png', 'logo', 'LOGO.PNG']
    for nome in nomes:
        if os.path.exists(os.path.join(pasta_atual, nome)): return os.path.join(pasta_atual, nome)
    return None

CAMINHO_LOGO = encontrar_logo()

def formatar_data_br(valor):
    if not valor or str(valor).lower() in ['nan', 'nat', 'none', '']: return ""
    try:
        if isinstance(valor, (date, datetime)): return valor.strftime('%d/%m/%Y')
        return pd.to_datetime(valor).strftime('%d/%m/%Y')
    except: return str(valor)

# --- CARREGAMENTO DE DADOS (VERSÃO ESTÁVEL TEXTO) ---
def carregar_dados():
    colunas = ["ID", "Data_Emissao", "Maquina", "Responsavel", "Tipo_Manutencao", "Setor", "Descricao_Pedido", "Status", "Diagnostico", "Solucao", "Pecas_Trocadas", "Observacao_Maq", "Tecnico", "Data_Inicio", "Data_Fim", "Horas_Totais", "Data_Inicio_Hora", "Data_Fim_Hora", "Pendencia", "Status_Pendencia", "Tipo_Problema"]
    try:
        url = f"{SUPABASE_URL}/rest/v1/ordens_servico?select=*"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        dados = response.json()
        if not dados: return pd.DataFrame(columns=colunas)
        df = pd.DataFrame(dados)
        for col in colunas:
            if col not in df.columns: df[col] = None
        df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)
        df['Horas_Totais'] = pd.to_numeric(df['Horas_Totais'], errors='coerce').fillna(0.0)
        for c in ['Data_Emissao', 'Data_Inicio', 'Data_Fim']:
            df[c] = pd.to_datetime(df[c], errors='coerce').dt.date
        return df
    except Exception as e:
        st.error(f"⚠️ Erro ao carregar dados: {e}")
        return pd.DataFrame(columns=colunas)

# --- SALVAR DADOS (VERSÃO ESTÁVEL TEXTO) ---
def salvar_dados(df_to_save):
    try:
        df_clean = df_to_save.copy()
        for col in ['Data_Emissao', 'Data_Inicio', 'Data_Fim']:
            df_clean[col] = df_clean[col].apply(lambda x: str(x) if pd.notnull(x) and x != "" else None)
        records = df_clean.replace({np.nan: None, "": None}).to_dict(orient='records')
        for r in records: r['ID'] = int(r['ID'])
        url = f"{SUPABASE_URL}/rest/v1/ordens_servico"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates"}
        response = requests.post(url, headers=headers, json=records)
        response.raise_for_status()
    except Exception as e:
        st.error(f"⚠️ Erro ao salvar na nuvem: {e}")
        if hasattr(e, 'response') and e.response is not None: st.warning(f"Detalhe do Banco: {e.response.text}")

def limpar_valor(v): return "" if pd.isna(v) or str(v).lower() in ['nan','nat','none'] else str(v)
def get_image_base64(path):
    if not path or not os.path.exists(path): return None
    with open(path, "rb") as img: return base64.b64encode(img.read()).decode()

# --- LÓGICA DE LUBRIFICAÇÃO (LOCAL) ---
def carregar_dados_lubrificacao():
    caminho = encontrar_arquivo(NOMES_POSSIVEIS_LUB)
    if not caminho: return pd.DataFrame()
    try:
        df = pd.read_csv(caminho, sep=';', encoding='latin1')
        if 'ULTIMA (DATA)' in df.columns: df['ULTIMA (DATA)'] = pd.to_datetime(df['ULTIMA (DATA)'], errors='coerce').dt.date
        return df
    except: return pd.DataFrame()

# --- APP PRINCIPAL ---
st.markdown("<style>h1, h2, h3 { color: #FFD700 !important; } div.stButton > button { background-color: #FFD700 !important; color: #000; font-weight: bold; }</style>", unsafe_allow_html=True)
df = carregar_dados()

with st.sidebar:
    if CAMINHO_LOGO: st.image(CAMINHO_LOGO, use_container_width=True)
    menu = st.radio("MENU", ["1. Emitir Ordem", "2. Baixar Ordem", "3. Dashboard", "4. Imprimir", "5. Gerenciar Banco"])
    st.caption("☁️ PCM ADF Ondulados - Online")

if menu == "1. Emitir Ordem":
    st.title("📄 Nova Ordem")
    with st.form("abertura"):
        prox_id = int(df['ID'].max() + 1) if not df.empty else 1
        st.metric("Próxima OS", f"#{prox_id}")
        col1, col2 = st.columns(2)
        dt = col1.date_input("Data Emissão", date.today())
        maq = col1.selectbox("Máquina", LISTA_MAQUINAS)
        setor = col2.selectbox("Setor", LISTA_SETORES)
        tipo = col2.selectbox("Tipo", LISTA_TIPOS_MANUTENCAO)
        resp = st.selectbox("Responsável", LISTA_TECNICOS)
        desc = st.text_area("Descrição do Serviço")
        if st.form_submit_button("EMITIR OS"):
            nova_os = {"ID": prox_id, "Data_Emissao": dt, "Maquina": maq, "Responsavel": resp, "Tipo_Manutencao": tipo, "Setor": setor, "Descricao_Pedido": desc, "Status": "ABERTA"}
            df = pd.concat([df, pd.DataFrame([nova_os])], ignore_index=True)
            salvar_dados(df)
            st.success("OS enviada para a nuvem!")
            st.rerun()

elif menu == "2. Baixar Ordem":
    st.title("🔧 Baixa de Ordem")
    abertas = df[df['Status'] == 'ABERTA']
    if abertas.empty: st.info("Sem ordens abertas.")
    else:
        sel = st.selectbox("Escolha a OS", abertas['ID'].astype(str) + " - " + abertas['Maquina'])
        idx = int(sel.split(" - ")[0])
        with st.form("baixa"):
            sol = st.text_area("Solução Aplicada")
            tecs = st.multiselect("Técnicos", LISTA_TECNICOS)
            h = st.number_input("Horas Totais", min_value=0.1, value=1.0)
            if st.form_submit_button("FINALIZAR"):
                idx_df = df[df['ID'] == idx].index[0]
                df.loc[idx_df, ['Status', 'Solucao', 'Tecnico', 'Horas_Totais', 'Data_Fim']] = ['FECHADA', sol, ", ".join(tecs), h, date.today()]
                salvar_dados(df)
                st.success("OS Baixada!")
                st.rerun()

elif menu == "3. Dashboard":
    st.title("📊 Indicadores")
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total de OS", len(df))
        c2.metric("Pendentes", len(df[df['Status'] == 'ABERTA']))
        c3.metric("Horas Totais", f"{df['Horas_Totais'].sum():.1f}h")
        st.plotly_chart(px.bar(df.groupby('Maquina').size().reset_index(name='Qtd'), x='Maquina', y='Qtd', title="OS por Máquina"))
    else: st.warning("Sem dados.")

elif menu == "5. Gerenciar Banco":
    st.title("🗄️ Banco de Dados")
    df_edit = st.data_editor(df, num_rows="dynamic")
    if st.button("SALVAR ALTERAÇÕES"):
        salvar_dados(df_edit)
        st.success("Banco de dados atualizado!")
        st.rerun()