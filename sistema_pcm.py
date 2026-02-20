import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime, date, timedelta
import os
import numpy as np
import requests

# --- CONEXÃO COM A NUVEM (SUPABASE VIA API DIRETA) ---
SUPABASE_URL = "https://dgitrtndyisotaowpsch.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRnaXRydG5keWlzb3Rhb3dwc2NoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1MTU0MTQsImV4cCI6MjA4NzA5MTQxNH0.-EjzxfPhyVSsErcstOt8D2nITVxmC3wFoXQTbYtqn1o"

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="PCM - ADF Ondulados", layout="wide", page_icon="🏭")

# --- ARQUIVOS LOCAIS RESTANTES ---
NOME_ARQUIVO_LOGO = 'logo.png' 
NOMES_POSSIVEIS_ESTOQUE = ['estoque_lubrificantes.csv', 'estoque_lubrificantes.csv.csv', 'CONTROLE DE LUBRIFICAÇÃO.xlsx - controle de lubrificantes.csv', 'controle de lubrificantes.csv']

# ==============================================================================
# --- 📝 LISTAS DE CADASTRO PADRÃO ---
# ==============================================================================

LISTA_MAQUINAS = ["ESTEIRA DE ALIMENTAÇÃO DO HIDRAPULPER","CALDEIRA NOVA","CALDEIRA VELHA","HIDRAPULPER 1","DESCONTAMINADOR","BOMBA DE MASSA O HIDRAPULPER 1","CCM 1 (PREPARO DE MASSA)","TRANSFORMADOR 1 (PREPARO DE MASSA)","BOMBA DE ÁGUA DO DESCONTAMINADOR","REFINADOR 1","PENEIRA VIBRATÓRIA","TURBO SEPARADOR","DEPURADOR PRIMÁRIO (DPI)","DEPURADOR HR 12 (FINE SCREEN-1° ESTÁGIO)","DEPURADOR HR 18 (FINE SCREEN-2° ESTÁGIO)","DEPURADOR HR 24 (FINE SCREEN-3° ESTÁGIO)","BOMBA DE ÁGUA DE  DILUIÇÃO DO HR 18","BOMBA DE ÁGUA DE  DILUIÇÃO DO HR 12","1° ESTÁGIO DE CLEANER","2° ESTÁGIO DE CLEANER","BOMBA DE MASSA DO 2° ESTÁGIO DE CLEANER","SIDE HILL 1","SIDE HILL 2","PENEIRA ESTÁTICA DO REJEITO DO HR 12","TM 1 (TANQUE DE MASSA)","TM 2 (TANQUE DE MASSA)","TM 3 (TANQUE DE MASSA)","TM 4 (TANQUE DE MASSA)","TA 1 (TANQUE DE ÁGUA)","TA 2 (TANQUE DE ÁGUA)","AGITADOR DO TM 1","AGITADOR DO TM 2","AGITADOR DO TM 3","AGITADOR DO TM 4","CLEANER DE ALTA CONSISTÊNCIA (HD)","BOMBA DE ÁGUA DO POÇO ARTESIANO","BOMBA DE ÁGUA DE COMBATE A INCÊNDIO 1","BOMBA DE ÁGUA DE COMBATE A INCÊNDIO 2","BOMBA DE ÁGUA DE COMBATE A INCÊNDIO 3","BOMDA DE ÁGUA DE ALIMENTAÇÃO DO PREPARO DE MASSA","BOMBA DE MASSA DO 1° ESTÁGIO DO CLEANER","BOMBA DE ÁGUA DE DILUIÇÃO DO FINE SCREEN","BOMBA DE ÁGUA DE LIMPEZA","BOMBA DE ÁGUA DE ELUTRIAÇÃO DOS CLEANERS","BOMBA DE ÁGUA DO HIDRAPULPER 2/SILO","BOMBA DE ÁGUA DO CONTROLE DE CONSISTÊNCIA","BOMBA DE MASSA DO TANQUE 2 (REFINADOR)","BOMBA DE MASSA DE TRANSBORDO CANALETA 1","BOMBA DE MASSA DE TRANSBORDO CANALETA 2","BOMBA DE MASSA DO TM 1","BOMBA DE MASSA DO TM 3","BOMBA DE MASSA DO TM 4 (GRAMATURA)","ROSCA DE REJEITO DE AREIA","BOMBA DO SEPARADOR DE VÁCUO PK","BOMBA DE VÁCUO 1 (MESA PLANA)","BOMBA DE VÁCUO 2 (ROLO DE SUCÇÃO)","BOMBA DE VÁCUO 3 (FELTRO)","BOMBA DE VÁCUO 4 (FELTRO)","MÁQUINA DE PAPEL","UNIDADE HIDRÁULICA DAS PRENSAS","VENTILADOR DE BAIXO VÁCUO (ROLO PICADO)","EXAUSTOR DO FILTRO DE MANGA","CCM 2 (MÁQUINA DE PAPEL)","QGBT","TRANSFORMADOR 2","COMPRESSOR DE PARAFUSO 1","COMPRESSOR DE PARAFUSO 2","PICADOR DE REFILE DA REBOBINADEIRA","BOMBA DE MISTURA","BOMBA DE SELAGEM DO VÁCUO","EXAUSTOR DE BAIXO VÁCUO DA MESA","DEPURADOR CABEÇA DE MÁQUINA (HR 24)","BOMBA DO WIREPIT","BOMBA DO COUCHPIT","AGITADOR DO COUCHPIT","ATENUADOR DE PULSAÇÃO","CAIXA DE ENTRADA DA MESA PLANA","CHUVEIRO OSCILADOR","ROLO CABECEIRA","ROLO DE SUCÇÃO","ROLO ACIONADOR","ROLO RASPADOR","1° PRENSA","2° PRENSA","CHUVEIRO OSCILADOR DO FILTRO TANDEM","CHUVEIRO OSCILADOR DA 1° PRENSA","CHUVEIRO OSCILADOR DA 2° PRENSA","ROLO PICKUP","CILINDRO SECADOR BABY","ESTICADOR DE CORDA DO 1° GRUPO","RASPAS DST 1","RASPAS DST 2","RASPAS DST 3","ESTICADOR DE CORDA DO 2° GRUPO","ESTICADOR DE CORDA DO 3° GRUPO","UNIDADE HIDRÁULICA DA SECAGEM","TANQUE SEPARADOR DO CONDENSADO DO 1° GRUPO","BOMBA DO BICO DE CORTE","BOMBA DO CHUVEIRO OSCILADOR","CAVALETE DE CONTROLE DO 1° GRUPO","CAVALETE DE CONTROLE DO 2° GRUPO","CAVALETE DE CONTROLE DO 3° GRUPO","COLETOR DE DISTRIBUIÇÃO DE VAPOR","ENROLADEIRA","MONOVIA","HIDRAPULPER 2","BOMBA DE MASSA DO HIDRAPULPER 2","FILTRO SEPARADOR DE REFILE","CORTADOR DE TUBETE","DESENROLADEIRA","REBOBINADEIRA","LAVA BOTAS","BALANÇA 1","BALANÇA RODOVIÁRIA","ROTA DE INSPEÇÃO 1", "ROTA DE INSPEÇÃO 2", "ROTA DE INSPEÇÃO 3", "ROTA DE INSPEÇÃO 4","ROTA DE INSPEÇÃO 5", "ROTA DE INSPEÇÃO 6", "ROTA DE INSPEÇÃO 7", "ROTA DE INSPEÇÃO 8","ROTA DE INSPEÇÃO 9","ROTA DE INSPEÇÃO 10", "ROTA DE INSPEÇÃO 11", "ROTA DE INSPEÇÃO 12","ROTA DE LUBRIFICAÇÃO","UTILIDADES","ONDULADEIRA","ROTA DE INSPEÇÃO DOS PAINÉIS","INSPEÇÃO VISUAL","SETOR MANUTENÇÃO","SETOR ONDULADEIRA","SETOR PREPARO DE MASSA","SETOR PÁTIO","ROTA DE INSPEÇÃO 13d"]
LISTA_SETORES = ["MECÂNICA", "ELÉTRICA", "PREDIAL", "UTILIDADES"]
LISTA_TIPOS_MANUTENCAO = ["PREVENTIVA", "CORRETIVA EMERGENCIAL", "CORRETIVA PROGRAMADA", "PREDITIVA", "MELHORIA", "LUBRIFICAÇÃO"]
LISTA_TIPOS_PROBLEMA = ["MECÂNICO", "ELÉTRICO", "HIDRÁULICO", "PNEUMÁTICO", "OPERACIONAL", "LUBRIFICAÇÃO", "INSTRUMENTAÇÃO", "ESTRUTURAL", "OUTROS", "VAZAMENTO DE ÁGUA/MASSA", "VAZAMENTO DE AR", "VAZAMENTO DE ÓLEO", "QUEBRA DE ROLAMENTO", "ROMPIMENTO DE CORREIA", "QUEBRA DE ENGRENAGEM OU POLIA", "SELAMENTO","FUSIVEL/DISJUNTOR QUEIMADO","QUEBRA DE MANCAL/BUCHA", "QUEIMA DE MOTOR/BOMBA","DESALINHAMENTO","PARAFUSOS SOLTOS/QUEBRADOS","OBSTRUÇÃO POR CORPO ESTRANHO","VEDAÇÕES/VÁLVULAS COM PROBLEMA","PROBLEMA NO PORTÃO DE ENTRADA","MOTOR DESARMADO","SISTEMA ELÉTRICO EM FALHA","CORRENTE/CORREIA FORA DO LUGAR","PROBELMA NO REDUTOR"]
LISTA_TECNICOS = ["MARCOS", "LUAN", "ISRAEL", "ANDERSON", "JGA", "IVAN", "DIEYSON", "GILMAR","LUCAS","FERNANDO"]

# --- LÓGICA DE LISTA DE PEÇAS DA NUVEM ---
LISTA_PECAS_SUGESTAO_PADRAO = [
    "ROLAMENTO NU310", "ROLAMENTO 3310","ROLAMENTO 6207","ROLAMENTO 22315 EAE C3","ROLAMENTO 22318 EJW C3",
    "CORREIA C70","CORREIA 5V 1500","RETENTOR 110X130X13","DISCO DO REFINADOR","FACA DE ONDULADEIRA",
    "ROLAMENTO 23222","MOTOR GENÉRICO","CORREIA 5V 1250","CORREIA LISA 70X1700","BUCHA INOX 179X60",
    "ROLAMENTO 6205","ROLAMENTO 6001","ROLAMENTO 6303","CORREIA C156","ROLAMENTO 22216","BUCHA H316",
    "CORREIA C100","CORREIA 1060","ROLAMENTO UC209","MANCAL FC 209","CORREIA 270H","CORREIA B60",
    "CORREIA 131","ROLAMENTO 6208","CORREIA C119","ACOPLAMENTO AT 25"
]

def carregar_lista_pecas_nuvem():
    try:
        url = f"{SUPABASE_URL}/rest/v1/lista_pecas?select=nome_peca"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
            return [item['nome_peca'] for item in dados if item.get('nome_peca')]
        return []
    except:
        return []

pecas_nuvem = carregar_lista_pecas_nuvem()
# Junta a lista padrão com a da nuvem, remove duplicadas e põe em ordem alfabética
LISTA_PECAS_SUGESTAO = sorted(list(set(LISTA_PECAS_SUGESTAO_PADRAO + pecas_nuvem)))

# --- FUNÇÕES BÁSICAS ---
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

def ler_csv_inteligente(caminho):
    if not caminho or not os.path.exists(caminho): return pd.DataFrame()
    encodings = ['utf-8', 'latin1', 'cp1252']
    separadores = [';', ','] 
    for enc in encodings:
        for sep in separadores:
            try:
                df = pd.read_csv(caminho, sep=sep, encoding=enc)
                if df.shape[1] > 1: return df
            except: continue
    try: return pd.read_csv(caminho)
    except: return pd.DataFrame()

def formatar_data_br(valor):
    if not valor or str(valor).lower() in ['nan', 'nat', 'none', '']: return ""
    try:
        if isinstance(valor, (date, datetime)): return valor.strftime('%d/%m/%Y')
        return datetime.strptime(str(valor)[:10], '%Y-%m-%d').strftime('%d/%m/%Y')
    except: return str(valor)

def limpar_valor(v): return "" if pd.isna(v) or str(v).lower() in ['nan','nat','none'] else str(v)
def get_image_base64(path):
    if not path or not os.path.exists(path): return None
    with open(path, "rb") as img: return base64.b64encode(img.read()).decode()

# ==============================================================================
# --- ☁️ FUNÇÕES SUPABASE (ORDENS DE SERVIÇO) ---
# ==============================================================================
def carregar_dados():
    colunas = ["ID", "Data_Emissao", "Maquina", "Responsavel", "Tipo_Manutencao", "Setor", "Descricao_Pedido", "Status", "Diagnostico", "Solucao", "Pecas_Trocadas", "Observacao_Maq", "Tecnico", "Data_Inicio", "Data_Fim", "Horas_Totais", "Data_Inicio_Hora", "Data_Fim_Hora", "Pendencia", "Status_Pendencia", "Tipo_Problema"]
    try:
        url = f"{SUPABASE_URL}/rest/v1/ordens_servico?select=*"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
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
        st.error(f"Erro ao carregar OS do Supabase: {e}")
        return pd.DataFrame(columns=colunas)

def salvar_unica_linha_supabase(registro_dict):
    try:
        r = registro_dict.copy()
        r['ID'] = int(r['ID'])
        for col in ['Data_Emissao', 'Data_Inicio', 'Data_Fim']:
            if r.get(col): r[col] = str(r[col])
        for chave, valor in r.items():
            if pd.isna(valor) or valor == "" or valor == "None": r[chave] = None
            elif isinstance(valor, (int, float)): pass
            else: r[chave] = str(valor)

        url = f"{SUPABASE_URL}/rest/v1/ordens_servico"
        headers = {
            "apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates" 
        }
        response = requests.post(url, headers=headers, json=[r])
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar na nuvem: {e}")
        return False

def salvar_dados_massa(df_to_save):
    for index, row in df_to_save.iterrows():
        salvar_unica_linha_supabase(row.to_dict())

def salvar_nova_peca_supabase(nome_peca):
    try:
        url = f"{SUPABASE_URL}/rest/v1/lista_pecas"
        headers = {
            "apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        # Envia apenas o nome da peça (o banco gera o ID sozinho)
        payload = [{"nome_peca": nome_peca}]
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar peça na nuvem: {e}")
        return False

# ==============================================================================
# --- ☁️ FUNÇÕES SUPABASE (LUBRIFICAÇÃO) ---
# ==============================================================================
def carregar_dados_lubrificacao():
    try:
        url = f"{SUPABASE_URL}/rest/v1/dados_lubrificacao?select=*"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        dados = response.json()
        if not dados: return pd.DataFrame()
        
        df = pd.DataFrame(dados)
        
        # Tratamento idêntico ao antigo CSV
        if 'ATIVO' in df.columns: df['ATIVO'] = df['ATIVO'].replace('', pd.NA).ffill()
        if 'SUBATIVO' in df.columns:
            df = df.dropna(subset=['SUBATIVO'])
            df = df[df['SUBATIVO'].astype(str).str.strip() != '']
        
        data_padrao = date(2026, 1, 25)
        def parse_data_universal(val):
            if pd.isna(val) or str(val).strip() == '' or str(val).strip() == 'None': return data_padrao
            texto = str(val).lower().strip()
            meses = {'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 'mai': '05', 'jun': '06',
                     'jul': '07', 'ago': '08', 'set': '09', 'out': '10', 'nov': '11', 'dez': '12'}
            for mt, mn in meses.items():
                if mt in texto: texto = texto.replace(mt, mn); break
            try:
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try: return datetime.strptime(texto, fmt).date()
                    except: continue
                if len(texto) <= 5 and '/' in texto:
                    return datetime.strptime(f"{texto}/2026", "%d/%m/%Y").date()
            except: pass
            return data_padrao

        if 'ULTIMA (DATA)' in df.columns:
            df['ULTIMA (DATA)'] = df['ULTIMA (DATA)'].apply(parse_data_universal)
        else: df['ULTIMA (DATA)'] = data_padrao

        if 'PERIODICIDADE (DIAS)' in df.columns:
            df['PERIODICIDADE (DIAS)'] = pd.to_numeric(df['PERIODICIDADE (DIAS)'], errors='coerce').fillna(0)
            def calc_prox(row):
                try: return row['ULTIMA (DATA)'] + timedelta(days=int(row['PERIODICIDADE (DIAS)']))
                except: return data_padrao
            df['PRÓXIMA (DATA)'] = df.apply(calc_prox, axis=1)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar lubrificação da nuvem: {e}")
        return pd.DataFrame()

def salvar_linha_lubrificacao_supabase(registro_dict):
    try:
        r = registro_dict.copy()
        
        # Limpa colunas que só existem no visual do Streamlit e não no Supabase
        colunas_para_remover = ['PRÓXIMA (DATA)', 'STATUS', 'ID_TEMP']
        for col in colunas_para_remover:
            if col in r: del r[col]
                
        if 'id' in r: r['id'] = int(r['id'])
        
        for chave, valor in r.items():
            if isinstance(valor, (date, datetime)): r[chave] = str(valor)
            elif pd.isna(valor) or valor == "" or valor == "None": r[chave] = None
            elif isinstance(valor, (int, float)): pass
            else: r[chave] = str(valor)

        url = f"{SUPABASE_URL}/rest/v1/dados_lubrificacao"
        headers = {
            "apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates"
        }
        res = requests.post(url, headers=headers, json=[r])
        res.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar lubrificação na nuvem: {e}")
        return False

# ==============================================================================
# --- FUNÇÕES DE LÓGICA E VISUAL ---
# ==============================================================================
def carregar_estoque():
    caminho = encontrar_arquivo(NOMES_POSSIVEIS_ESTOQUE)
    return ler_csv_inteligente(caminho)

def salvar_estoque(df):
    caminho = encontrar_arquivo(NOMES_POSSIVEIS_ESTOQUE)
    if not caminho:
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMES_POSSIVEIS_ESTOQUE[0])
    df.to_csv(caminho, index=False, sep=';', encoding='utf-8-sig')

def verificar_conflito_horario(df_banco, tecnicos_selecionados, dt_inicio_novo, dt_fim_novo):
    df_fechadas = df_banco[(df_banco['Status'] == 'FECHADA') & (df_banco['ID'] > 0)].copy()
    conflitos = []
    for _, row in df_fechadas.iterrows():
        try:
            tecnicos_row = str(row['Tecnico']).split(', ')
            tecnicos_em_comum = set(tecnicos_selecionados).intersection(tecnicos_row)
            if tecnicos_em_comum:
                data_ini_exist = pd.to_datetime(row['Data_Inicio']).date()
                hora_ini_exist = datetime.strptime(str(row['Data_Inicio_Hora']), "%H:%M:%S").time()
                dt_ini_exist = datetime.combine(data_ini_exist, hora_ini_exist)
                
                data_fim_exist = pd.to_datetime(row['Data_Fim']).date()
                hora_fim_exist = datetime.strptime(str(row['Data_Fim_Hora']), "%H:%M:%S").time()
                dt_fim_exist = datetime.combine(data_fim_exist, hora_fim_exist)
                
                if (dt_inicio_novo < dt_fim_exist) and (dt_fim_novo > dt_ini_exist):
                    for tec in tecnicos_em_comum:
                        conflitos.append(f"{tec} já está ocupado na OS #{row['ID']} ({dt_ini_exist.strftime('%d/%m %H:%M')} - {dt_fim_exist.strftime('%H:%M')})")
        except: continue
    return conflitos

def verificar_conflito_maquina(df_banco, maquina_alvo, dt_inicio_novo, dt_fim_novo):
    df_fechadas = df_banco[(df_banco['Status'] == 'FECHADA') & (df_banco['ID'] > 0) & (df_banco['Maquina'] == maquina_alvo)].copy()
    conflitos = []
    for _, row in df_fechadas.iterrows():
        try:
            data_ini_exist = pd.to_datetime(row['Data_Inicio']).date()
            hora_ini_exist = datetime.strptime(str(row['Data_Inicio_Hora']), "%H:%M:%S").time()
            dt_ini_exist = datetime.combine(data_ini_exist, hora_ini_exist)
            
            data_fim_exist = pd.to_datetime(row['Data_Fim']).date()
            hora_fim_exist = datetime.strptime(str(row['Data_Fim_Hora']), "%H:%M:%S").time()
            dt_fim_exist = datetime.combine(data_fim_exist, hora_fim_exist)
            
            if (dt_inicio_novo < dt_fim_exist) and (dt_fim_novo > dt_ini_exist):
                conflitos.append(f"A máquina {maquina_alvo} já tem trabalho na OS #{row['ID']} ({dt_ini_exist.strftime('%d/%m %H:%M')} - {dt_fim_exist.strftime('%H:%M')})")
        except: continue
    return conflitos

def configurar_estilo_visual():
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 3px solid #FFD700; }
        section[data-testid="stSidebar"] * { color: #000000 !important; }
        div.stButton > button { background-color: #FFD700 !important; color: #000000 !important; border: 2px solid #000000 !important; font-weight: bold !important; }
        div.stButton > button:hover { background-color: #FFEA00 !important; border-color: #333333 !important; }
        div[data-testid="stMetric"] { background-color: #111111 !important; border: 1px solid #FFD700 !important; padding: 10px; border-radius: 5px; color: white !important; }
        div[data-testid="stMetricLabel"] { color: #FFD700 !important; }
        div[data-testid="stMetricValue"] { color: #ffffff !important; }
        h1, h2, h3 { color: #FFD700 !important; }
        button[kind="secondary"] { background-color: #ff4b4b !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

def gerar_html_impressao(dados_os):
    logo_base64 = get_image_base64(CAMINHO_LOGO)
    img_tag = f'<img src="data:image/png;base64,{logo_base64}" style="max-height: 70px; max-width: 200px;">' if logo_base64 else ''
    
    data_emissao_br = formatar_data_br(dados_os['Data_Emissao'])
    data_ini_br = formatar_data_br(dados_os.get('Data_Inicio', ''))
    data_fim_br = formatar_data_br(dados_os.get('Data_Fim', ''))
    hora_ini = limpar_valor(dados_os.get('Data_Inicio_Hora',''))
    hora_fim = limpar_valor(dados_os.get('Data_Fim_Hora',''))
    t_ini = f"{data_ini_br} {hora_ini}".strip()
    t_fim = f"{data_fim_br} {hora_fim}".strip()
    
    html_template = f"""
    <html>
    <head>
        <title>OS #{dados_os['ID']}</title>
        <style>
            @page {{ size: A4; margin: 5mm; }}
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 10px; background-color: white !important; color: black !important; -webkit-print-color-adjust: exact; font-size: 12px; }}
            .container {{ width: 100%; max-width: 100%; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; border: 2px solid black; padding: 5px; margin-bottom: 5px; height: 75px; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5px; border: 1px solid black; padding: 5px; margin-bottom: 5px; }}
            .label {{ font-weight: bold; font-size: 11px; }}
            .section-title {{ background-color: #ddd; padding: 3px; border: 1px solid black; font-weight: bold; text-align: center; margin-top: 5px; font-size: 12px; -webkit-print-color-adjust: exact; border-bottom: none; }}
            .box-grande {{ border: 1px solid black; min-height: 180px; padding: 5px; margin-bottom: 5px; white-space: pre-wrap; }}
            .box-medio {{ border: 1px solid black; min-height: 100px; padding: 5px; margin-bottom: 5px; white-space: pre-wrap; }}
            .tabela-form {{ width: 100%; border-collapse: collapse; margin-bottom: 5px; font-size: 11px; }}
            .tabela-form th {{ border: 1px solid black; padding: 2px; text-align: center; font-weight: bold; background-color: white; }}
            .tabela-form td {{ border: 1px solid black; padding: 2px; height: 18px; }}
            .assinaturas {{ margin-top: 30px; display: flex; justify-content: center; }}
            .linha-assinatura {{ border-top: 1px solid black; width: 50%; text-align: center; padding-top: 2px; font-size: 11px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>{img_tag}</div>
                <div style="text-align: right;">
                    <div><span class="label">DATA EMISSÃO:</span> {data_emissao_br}</div>
                    <div><span class="label">NÚMERO DA ORDEM:</span> <strong style="font-size: 16px;">#{dados_os['ID']}</strong></div>
                </div>
            </div>
            <div class="info-grid">
                <div><span class="label">MÁQUINA:</span> {limpar_valor(dados_os['Maquina'])}</div>
                <div><span class="label">RESPONSÁVEL:</span> {limpar_valor(dados_os['Responsavel'])}</div>
                <div><span class="label">TIPO MANUT.:</span> {limpar_valor(dados_os['Tipo_Manutencao'])}</div>
                <div><span class="label">SETOR:</span> {limpar_valor(dados_os['Setor'])}</div>
            </div>
            <div class="section-title" style="border-bottom: 1px solid black;">DESCRIÇÃO DO PROBLEMA / SERVIÇO (SOLICITANTE)</div>
            <div class="box-grande" style="border-top: none;">{limpar_valor(dados_os['Descricao_Pedido'])}</div>
            <div class="section-title" style="border-bottom: 1px solid black;">APONTAMENTO TÉCNICO (MANUTENÇÃO)</div>
            <div><span class="label">DIAGNÓSTICO (CAUSA RAIZ):</span></div>
            <div class="box-medio">{limpar_valor(dados_os['Diagnostico'])}</div>
            <div><span class="label">SOLUÇÃO APLICADA:</span></div>
            <div class="box-medio">{limpar_valor(dados_os['Solucao'])}</div>
            <div class="section-title">PEÇAS TROCADAS</div>
            <table class="tabela-form">
                <thead><tr><th style="width: 50%;">NOME DA PEÇA</th><th style="width: 30%;">CÓDIGO INTERNO</th><th style="width: 20%;">QTD</th></tr></thead>
                <tbody><tr><td>{limpar_valor(dados_os['Pecas_Trocadas'])}</td><td></td><td></td></tr><tr><td>&nbsp;</td><td></td><td></td></tr><tr><td>&nbsp;</td><td></td><td></td></tr><tr><td>&nbsp;</td><td></td><td></td></tr></tbody>
            </table>
            <div class="section-title">APONTAMENTO DE TEMPO DE TRABALHO</div>
            <table class="tabela-form">
                <thead><tr><th style="width: 30%;">NOME DO TÉCNICO</th><th style="width: 25%;">DATA/HORA INICIO</th><th style="width: 25%;">DATA/HORA FIM</th><th style="width: 20%;">STATUS</th></tr></thead>
                <tbody>
                    <tr><td>{limpar_valor(dados_os['Tecnico'])}</td><td>{t_ini}</td><td>{t_fim}</td><td>FECHADA</td></tr>
                    <tr><td>&nbsp;</td><td></td><td></td><td></td></tr>
                    <tr><td>&nbsp;</td><td></td><td></td><td></td></tr>
                    <tr><td>&nbsp;</td><td></td><td></td><td></td></tr>
                </tbody>
            </table>
            <div class="assinaturas"><div class="linha-assinatura">Assinatura do Responsável</div></div>
        </div>
        <script>window.onload = function() {{ window.print(); }}</script>
    </body>
    </html>
    """
    return html_template

def gerar_html_lubrificacao(df_imprimir):
    logo_base64 = get_image_base64(CAMINHO_LOGO)
    img_tag = f'<img src="data:image/png;base64,{logo_base64}" style="max-height: 60px;">' if logo_base64 else 'ADF ONDULADOS'
    linhas_html = ""
    for index, row in df_imprimir.iterrows():
        linhas_html += f"""<tr><td>{row.get('ATIVO', '')}</td><td>{row.get('SUBATIVO', '')}</td><td>{row.get('LUBRIFICANTE', '')}</td><td>{row.get('QTD(G)', '')}</td><td style="text-align: center;"><div style="width: 20px; height: 20px; border: 1px solid black; margin: auto;"></div></td></tr>"""
    html = f"""<html><head><style>body {{ font-family: Arial, sans-serif; font-size: 12px; }} table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }} th, td {{ border: 1px solid black; padding: 5px; text-align: left; }} th {{ background-color: #f2f2f2; }} .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 20px; }}</style></head><body><div class="header"><div>{img_tag}</div><div style="text-align: right;"><h2>ROTA DE LUBRIFICAÇÃO</h2><p>Data de Impressão: {date.today().strftime('%d/%m/%Y')}</p></div></div><table><thead><tr><th style="width: 25%">MÁQUINA</th><th style="width: 35%">PONTO / COMPONENTE</th><th style="width: 25%">LUBRIFICANTE</th><th style="width: 10%">QTD</th><th style="width: 5%">OK</th></tr></thead><tbody>{linhas_html}</tbody></table><br><br><div style="display: flex; justify-content: space-between; margin-top: 30px;"><div style="border-top: 1px solid black; width: 40%; text-align: center;">Técnico Responsável</div><div style="border-top: 1px solid black; width: 40%; text-align: center;">Supervisor</div></div><script>window.print();</script></body></html>"""
    return html

# --- APP PRINCIPAL ---
configurar_estilo_visual()
df = carregar_dados()

with st.sidebar:
    if CAMINHO_LOGO: st.image(CAMINHO_LOGO, use_container_width=True)
    st.markdown("---")
    
    # --- SISTEMA DE BLOQUEIO (SENHA) ---
    st.markdown("### 🔐 Acesso")
    senha = st.text_input("Digite a senha para editar:", type="password")
    
    # SENHA DO SISTEMA (Você pode mudar "adf2026" para o que quiser)
    if senha == "adf2026":
        st.success("🔓 Modo Administrador Liberado")
        # Menus que VOCÊ pode ver:
        itens_menu = [
            "1. Emitir Ordem", "2. Baixar Ordem", "3. Dashboard", "4. Imprimir Ordem", 
            "5. Gerenciar Registros", "6. Histórico de Peças", "7. Controle de Lubrificação",
            "8. OS Pendentes", "9. Pendências de Máquinas"
        ]
    else:
        st.info("👁️ Modo Apenas Leitura")
        # Menus que PESSOAS SEM SENHA podem ver:
        itens_menu = [
            "1. Emitir Ordem","3. Dashboard", "4. Imprimir Ordem", "8. OS Pendentes"
        ]

    st.markdown("---")
    menu = st.radio("NAVEGAÇÃO", itens_menu)
    
    st.markdown("---")
    st.markdown("**PCM - ADF Ondulados**")
    st.caption("☁️ Nuvem Ativa (Supabase)")
# ==============================================================================
# 1. EMITIR ORDEM
# ==============================================================================
if menu == "1. Emitir Ordem":
    st.title("📄 Nova Ordem de Serviço")
    with st.form("form_abertura"):
        col1, col2, col3 = st.columns(3)
        if not df.empty:
            proximo_id = int(df['ID'].max()) + 1
        else:
            proximo_id = 1
        c1 = col1.metric("Número da Ordem", f"#{proximo_id}")
        data_emissao = col1.date_input("Data da Emissão", date.today(), format="DD/MM/YYYY")
        maquina = col2.selectbox("Máquina", LISTA_MAQUINAS)
        setor = col2.selectbox("Setor", LISTA_SETORES)
        responsavel = col3.selectbox("Responsável", LISTA_TECNICOS)
        tipo_manut = col3.selectbox("Tipo", LISTA_TIPOS_MANUTENCAO)
        descricao = st.text_area("Descrição do Serviço", height=100)
        
        btn_enviar = st.form_submit_button("EMITIR ORDEM DE SERVIÇO")
        
        if btn_enviar:
            if not descricao:
                st.warning("⚠️ Preencha a descrição do problema.")
            else:
                nova_os = {
                    "ID": proximo_id, "Data_Emissao": data_emissao, "Maquina": maquina, "Responsavel": responsavel,
                    "Tipo_Manutencao": tipo_manut, "Setor": setor, "Descricao_Pedido": descricao, "Status": "ABERTA",
                    "Diagnostico": None, "Solucao": None, "Pecas_Trocadas": None, "Observacao_Maq": None, "Tecnico": None, 
                    "Data_Inicio": None, "Data_Fim": None, "Horas_Totais": 0.0,
                    "Data_Inicio_Hora": None, "Data_Fim_Hora": None,
                    "Pendencia": None, "Status_Pendencia": None, "Tipo_Problema": None
                }
                if salvar_unica_linha_supabase(nova_os):
                    st.success(f"✅ OS #{proximo_id} enviada com sucesso para a nuvem!")
                    st.balloons()
                    import time
                    time.sleep(2)
                    st.rerun()

# ==============================================================================
# 2. BAIXAR ORDEM
# ==============================================================================
elif menu == "2. Baixar Ordem":
    st.title("🔧 Baixa Técnica")
    abertas = df[df['Status'] == 'ABERTA']
    if abertas.empty: st.info("Nenhuma ordem pendente.")
    else:
        sel = st.selectbox("Selecione a Ordem", abertas['ID'].astype(str) + " - " + abertas['Maquina'])
        idx_selecionado = int(sel.split(" - ")[0])
        
        os_d = df[df['ID'] == idx_selecionado].iloc[0]
        st.write(f"**Problema:** {os_d['Descricao_Pedido']}")
        
        st.markdown("---")
        st.subheader("📦 Peças Utilizadas")
        pecas_selecionadas = st.multiselect("Selecione as peças:", LISTA_PECAS_SUGESTAO)
        pecas_com_qtd_os = []
        if pecas_selecionadas:
            st.caption("👇 Informe a quantidade:")
            cols_p = st.columns(len(pecas_selecionadas))
            for i, peca in enumerate(pecas_selecionadas):
                with cols_p[i if i < 4 else 0]:
                    qtd = st.number_input(f"Qtd {peca}", min_value=1, value=1, key=f"qtd_os_{peca}")
                    pecas_com_qtd_os.append(f"{peca} ({qtd}un)")
        
        with st.form("baixa"):
            tipo_prob = st.selectbox("Classificação do Problema", LISTA_TIPOS_PROBLEMA, index=None, placeholder="Selecione caso haja defeito...")
            solucao = st.text_area("Solução Aplicada")
            obs_maq = st.text_area("Observação da Máquina")
            
            st.markdown("---")
            pendencia_txt = st.text_area("⚠️ Registrar Pendência (Se houver algo por fazer)", placeholder="Descreva o que ficou pendente na máquina...")
            st.markdown("### ⏱️ Lançamento de Horas e Técnicos")
            tecnicos_sel = st.multiselect("Técnicos Executantes", LISTA_TECNICOS)
            c1, c2, c3, c4 = st.columns(4)
            d_ini = c1.date_input("Data Início", date.today(), format="DD/MM/YYYY")
            h_ini = c2.time_input("Hora Início", value=datetime.strptime("08:00", "%H:%M").time())
            d_fim = c3.date_input("Data Fim", date.today(), format="DD/MM/YYYY")
            h_fim = c4.time_input("Hora Fim", value=datetime.strptime("17:00", "%H:%M").time())
            
            if st.form_submit_button("FINALIZAR ORDEM (DIGITAL)"):
                tipo_manut_atual = str(os_d['Tipo_Manutencao']).upper()
                eh_corretiva = "CORRETIVA" in tipo_manut_atual
                
                if not tecnicos_sel: st.error("Selecione pelo menos um técnico.")
                elif eh_corretiva and not tipo_prob:
                    st.error("⚠️ Para Ordens CORRETIVAS, é obrigatório selecionar a Classificação do Problema.")
                else:
                    dt_ini = datetime.combine(d_ini, h_ini)
                    dt_fim = datetime.combine(d_fim, h_fim)
                    if dt_fim < dt_ini: st.error("Erro: Data Fim menor que Início.")
                    else:
                        conflitos_tec = verificar_conflito_horario(df, tecnicos_sel, dt_ini, dt_fim)
                        conflitos_maq = verificar_conflito_maquina(df, os_d['Maquina'], dt_ini, dt_fim)
                        
                        if conflitos_tec or conflitos_maq:
                            for c in conflitos_tec: st.error(f"❌ {c}")
                            for c in conflitos_maq: st.error(f"❌ {c}")
                            st.warning("Não foi possível finalizar devido aos conflitos.")
                        else:
                            tecnicos_nomes = ", ".join(tecnicos_sel)
                            dur = (dt_fim - dt_ini).total_seconds() / 3600
                            pecas_str = ", ".join(pecas_com_qtd_os) if pecas_com_qtd_os else None
                            status_pend = "ABERTA" if pendencia_txt else None
                            tipo_final = tipo_prob if tipo_prob else "NÃO SE APLICA"
                            
                            dados_atualizados = os_d.to_dict()
                            dados_atualizados.update({
                                'Status': 'FECHADA',
                                'Solucao': solucao,
                                'Tecnico': tecnicos_nomes,
                                'Horas_Totais': round(dur, 2),
                                'Pecas_Trocadas': pecas_str,
                                'Observacao_Maq': obs_maq,
                                'Data_Inicio': d_ini,
                                'Data_Fim': d_fim,
                                'Data_Inicio_Hora': h_ini.strftime("%H:%M:%S"),
                                'Data_Fim_Hora': h_fim.strftime("%H:%M:%S"),
                                'Pendencia': pendencia_txt,
                                'Status_Pendencia': status_pend,
                                'Tipo_Problema': tipo_final
                            })
                            
                            if salvar_unica_linha_supabase(dados_atualizados):
                                st.success("✅ Ordem finalizada e salva na nuvem!")
                                import time
                                time.sleep(2)
                                st.rerun()

# ==============================================================================
# 3. DASHBOARD
# ==============================================================================
elif menu == "3. Dashboard":
    st.title("📊 Análise de Ordens de Serviço")
    st.markdown("### 📅 Filtro de Período")
    col_f1, col_f2 = st.columns([1, 2])
    opcao_filtro = col_f1.selectbox("Selecione o Período:", 
                                    ["Todo o Período", "Últimos 7 Dias", "Últimos 15 Dias", "Últimos 30 Dias", "Mês Atual", "Mês Passado", "Personalizado"])
    
    df_reais = df[df['ID'] > 0].copy()
    df_dash = df_reais.copy()
    hoje = date.today()
    
    dt_inicio_filtro = None
    dt_fim_filtro = hoje

    if opcao_filtro == "Últimos 7 Dias": dt_inicio_filtro = hoje - timedelta(days=7)
    elif opcao_filtro == "Últimos 15 Dias": dt_inicio_filtro = hoje - timedelta(days=15)
    elif opcao_filtro == "Últimos 30 Dias": dt_inicio_filtro = hoje - timedelta(days=30)
    elif opcao_filtro == "Mês Atual": dt_inicio_filtro = date(hoje.year, hoje.month, 1)
    elif opcao_filtro == "Mês Passado":
        primeiro_dia_mes_atual = hoje.replace(day=1)
        dt_fim_filtro = primeiro_dia_mes_atual - timedelta(days=1)
        dt_inicio_filtro = dt_fim_filtro.replace(day=1)
    elif opcao_filtro == "Personalizado":
        intervalo = col_f2.date_input("Selecione o intervalo:", [hoje - timedelta(days=30), hoje], format="DD/MM/YYYY")
        if len(intervalo) == 2:
            dt_inicio_filtro = intervalo[0]
            dt_fim_filtro = intervalo[1]
    
    if dt_inicio_filtro:
        df_dash = df_reais[(df_reais['Data_Emissao'] >= dt_inicio_filtro) & (df_reais['Data_Emissao'] <= dt_fim_filtro)]

    st.markdown("---")
    if df_dash.empty: st.info("Sem dados neste período.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", len(df_dash))
        c2.metric("Abertas", len(df_dash[df_dash['Status']=='ABERTA']))
        c3.metric("Preventivas", len(df_dash[df_dash['Tipo_Manutencao']=='PREVENTIVA']))
        c4.metric("Corretivas", len(df_dash[df_dash['Tipo_Manutencao'].astype(str).str.contains('CORRETIVA', na=False)]))
        st.markdown("---")
        g1 = df_dash.groupby(['Maquina', 'Tipo_Manutencao']).size().reset_index(name='Qtd')
        st.plotly_chart(px.bar(g1, x='Maquina', y='Qtd', color='Tipo_Manutencao', barmode='group'))
        
        st.subheader("Horas Totais por Tipo de Manutenção")
        g_horas_tipo = df_dash.groupby('Tipo_Manutencao')['Horas_Totais'].sum().reset_index()
        fig_horas_tipo = px.bar(g_horas_tipo, x='Tipo_Manutencao', y='Horas_Totais', text_auto=True, color='Tipo_Manutencao')
        st.plotly_chart(fig_horas_tipo, use_container_width=True)
        
        st.markdown("---")
        st.subheader("🏆 Top 10 Máquinas com Mais Horas Apontadas")
        top_horas_maq = df_dash.groupby('Maquina')['Horas_Totais'].sum().reset_index()
        top_horas_maq = top_horas_maq.sort_values(by='Horas_Totais', ascending=False).head(10)
        st.plotly_chart(px.bar(top_horas_maq, x='Maquina', y='Horas_Totais', text_auto=True))
        
        c_g1, c_g2 = st.columns(2)
        with c_g1:
            st.markdown("##### 🔧 Top 10 - Horas em Corretiva")
            df_corr = df_dash[df_dash['Tipo_Manutencao'].astype(str).str.contains("CORRETIVA", na=False)]
            top_corr = df_corr.groupby('Maquina')['Horas_Totais'].sum().reset_index().sort_values(by='Horas_Totais', ascending=False).head(10)
            st.plotly_chart(px.bar(top_corr, x='Maquina', y='Horas_Totais', text_auto=True, color_discrete_sequence=['#FF4B4B']))
            
        with c_g2:
            st.markdown("##### 🛡️ Top 10 - Horas em Prev./Lub.")
            df_prev = df_dash[df_dash['Tipo_Manutencao'].isin(['PREVENTIVA', 'LUBRIFICAÇÃO'])]
            top_prev = df_prev.groupby('Maquina')['Horas_Totais'].sum().reset_index().sort_values(by='Horas_Totais', ascending=False).head(10)
            st.plotly_chart(px.bar(top_prev, x='Maquina', y='Horas_Totais', text_auto=True, color_discrete_sequence=['#00CC96']))
        
        st.markdown("---")
        st.subheader("🔍 Quais problemas mais ocorrem?")
        if 'Tipo_Problema' in df_dash.columns:
            df_probs = df_dash[
                (df_dash['Tipo_Problema'].notna()) & 
                (df_dash['Tipo_Problema'] != "") & 
                (df_dash['Tipo_Problema'] != "NÃO SE APLICA")
            ]
            if not df_probs.empty:
                contagem_prob = df_probs['Tipo_Problema'].value_counts().reset_index()
                contagem_prob.columns = ['Tipo', 'Qtd']
                fig_prob = px.pie(contagem_prob, values='Qtd', names='Tipo', hole=0.4)
                st.plotly_chart(fig_prob)
            else:
                st.info("Nenhum problema registrado no período.")

        st.markdown("---")
        st.subheader("Horas por Técnico (Neste Período)")
        df_tec = df_dash[df_dash['Status']=='FECHADA'].copy()
        if not df_tec.empty and 'Tecnico' in df_tec.columns:
            df_tec['Tecnico'] = df_tec['Tecnico'].str.split(', ')
            df_tec = df_tec.explode('Tecnico')
            g3 = df_tec.groupby('Tecnico')['Horas_Totais'].sum().reset_index().sort_values(by='Horas_Totais', ascending=False)
            st.plotly_chart(px.bar(g3, x='Tecnico', y='Horas_Totais', text_auto=True))

# ==============================================================================
# 4. IMPRIMIR ORDEM
# ==============================================================================
elif menu == "4. Imprimir Ordem":
    st.title("🖨️ Central de Impressão")
    if not df.empty:
        sel = st.selectbox("Selecione OS", df['ID'].astype(str)+" - "+df['Maquina'])
        idx = int(sel.split(" - ")[0])
        if st.button("Gerar PDF"):
            h = gerar_html_impressao(df[df['ID']==idx].iloc[0])
            st.download_button("Baixar Arquivo", h, f"OS_{idx}.html", "text/html")

# ==============================================================================
# 5. GERENCIAR REGISTROS (NUVEM)
# ==============================================================================
elif menu == "5. Gerenciar Registros":
    st.title("🗑️ Gerenciamento de Banco de Dados")
    
    # --- NOVO: CADASTRAR PEÇA NA NUVEM ---
    with st.expander("➕ Cadastrar Nova Peça no Sistema", expanded=False):
        with st.form("form_nova_peca", clear_on_submit=True):
            nova_peca = st.text_input("Nome da Nova Peça (Ex: ROLAMENTO 6204)").upper().strip()
            
            if st.form_submit_button("SALVAR NOVA PEÇA NA NUVEM"):
                if nova_peca and nova_peca not in LISTA_PECAS_SUGESTAO:
                    if salvar_nova_peca_supabase(nova_peca):
                        st.success(f"✅ Peça '{nova_peca}' cadastrada com sucesso na Nuvem!")
                        import time
                        time.sleep(2)
                        st.rerun()
                elif nova_peca in LISTA_PECAS_SUGESTAO:
                    st.warning("⚠️ Esta peça já existe no sistema.")
                else:
                    st.warning("⚠️ Digite um nome válido.")
                    
    st.markdown("---")
    
    st.info("⚠️ Ao salvar alterações aqui, a nuvem inteira será sobrescrita. Cuidado!")
    df_editado = st.data_editor(
        df, num_rows="dynamic", use_container_width=True,
        column_config={
            "Data_Emissao": st.column_config.DateColumn("Data Emissão", format="DD/MM/YYYY"),
            "Data_Inicio": st.column_config.DateColumn("Data Início", format="DD/MM/YYYY"),
            "Data_Fim": st.column_config.DateColumn("Data Fim", format="DD/MM/YYYY"),
        }
    )
    if st.button("💾 SALVAR TODAS AS ALTERAÇÕES NA NUVEM"):
        with st.spinner("Enviando tabela inteira..."):
            salvar_dados_massa(df_editado)
        st.success("Banco de dados atualizado com sucesso!")
        st.rerun()
        
    st.markdown("---")
    st.markdown("##### Exclusão Rápida")
    sel = st.selectbox("Selecione para Excluir", df['ID'].astype(str) + " - " + df['Maquina'])
    if st.button("❌ EXCLUIR REGISTRO"):
        id_excluir = int(sel.split(" ")[0])
        url_delete = f"{SUPABASE_URL}/rest/v1/ordens_servico?ID=eq.{id_excluir}"
        headers_delete = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        requests.delete(url_delete, headers=headers_delete)
        st.success("Excluído!")
        st.rerun()

# ==============================================================================
# 6. HISTÓRICO DE PEÇAS
# ==============================================================================
elif menu == "6. Histórico de Peças":
    st.title("🔩 Histórico")
    maq = st.selectbox("Máquina", LISTA_MAQUINAS)
    
    st.markdown("### 📝 Adicionar Ocorrência Manual (Sem Gerar OS)")
    st.info("Use para registrar trocas rápidas ou ajustes que não tiveram OS.")
    
    c1, c2 = st.columns(2)
    d_man = c1.date_input("Data da Ocorrência", date.today(), format="DD/MM/YYYY")
    t_man = c2.selectbox("Técnico Responsável", LISTA_TECNICOS)
    
    p_man = st.multiselect("Quais peças foram trocadas?", LISTA_PECAS_SUGESTAO)
    
    pecas_com_qtd = []
    if p_man:
        st.caption("👇 Informe a quantidade para cada peça selecionada:")
        cols = st.columns(len(p_man))
        for i, peca in enumerate(p_man):
            with cols[i if i < 4 else 0]:
                qtd = st.number_input(f"Qtd {peca}", min_value=1, value=1, key=f"qtd_{peca}")
                pecas_com_qtd.append(f"{peca} ({qtd}un)")
    
    motivo = st.text_area("Por que trocou? (Diagnóstico)")
    obs_man = st.text_area("Observação Adicional")
    
    if st.button("💾 SALVAR NO HISTÓRICO"):
        id_manual = int(datetime.now().timestamp()) * -1
        pecas_final = ", ".join(pecas_com_qtd) if pecas_com_qtd else None
        
        nova_reg = {
            "ID": id_manual, "Data_Emissao": d_man, "Maquina": maq, "Responsavel": "MANUAL",
            "Tipo_Manutencao": "CORRETIVA", "Setor": "MECÂNICA", "Descricao_Pedido": "Apontamento Manual (Sem OS)",
            "Status": "FECHADA", "Diagnostico": motivo, "Solucao": "Troca/Ajuste Manual", 
            "Pecas_Trocadas": pecas_final, "Observacao_Maq": obs_man,
            "Tecnico": t_man, "Data_Inicio": None, "Data_Fim": None, "Horas_Totais": 0.0,
            "Pendencia": None, "Status_Pendencia": None, "Tipo_Problema": "MECÂNICO"
        }
        if salvar_unica_linha_supabase(nova_reg):
            st.success("✅ Registro adicionado ao histórico com sucesso!")
            import time
            time.sleep(2)
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"#### 📜 Histórico da Máquina: {maq}")
    
    filtro = df[(df['Maquina'] == maq) & (df['Status'] == 'FECHADA')]
    filtro['Pecas_Trocadas'] = filtro['Pecas_Trocadas'].fillna('').astype(str)
    tem_peca = filtro['Pecas_Trocadas'].str.strip() != ""
    eh_manual = filtro['ID'] < 0
    filtro = filtro[tem_peca | eh_manual]
    
    if not filtro.empty:
        filtro = filtro.sort_values(by='Data_Emissao', ascending=False)
        for i, r in filtro.iterrows():
            d = formatar_data_br(r['Data_Emissao'])
            id_visivel = "MANUAL" if r['ID'] < 0 else f"OS #{r['ID']}"
            
            with st.expander(f"{id_visivel} - {d} (Téc: {r['Tecnico']})"):
                if r['Pecas_Trocadas'] and str(r['Pecas_Trocadas']).strip() != "":
                    st.markdown(f"**🔧 Peças:** {r['Pecas_Trocadas']}")
                st.markdown(f"**❓ Motivo/Diagnóstico:** {r['Diagnostico']}")
                st.markdown(f"**📝 Observação:** {r['Observacao_Maq']}")
                st.caption(f"Solução: {r['Solucao']}")
    else: st.info("Nenhum histórico encontrado para esta máquina.")

# ==============================================================================
# 7. CONTROLE DE LUBRIFICAÇÃO (AGORA TOTALMENTE NA NUVEM)
# ==============================================================================
elif menu == "7. Controle de Lubrificação":
    st.title("🛢️ Lubrificação")
    df_lub = carregar_dados_lubrificacao()
    df_est = carregar_estoque()
    
    if df_lub.empty: 
        st.error("Tabela de lubrificação não encontrada no banco ou vazia.")
    else:
        td = date.today()
        def stt(r):
            if pd.isna(r.get('PRÓXIMA (DATA)')): return "S/D"
            if r['PRÓXIMA (DATA)'] < td: return "🔴 Vencida"
            if r['PRÓXIMA (DATA)'] == td: return "🟡 Hoje"
            return "🟢 No Prazo"
            
        df_lub['STATUS'] = df_lub.apply(stt, axis=1)
        
        c1,c2,c3 = st.columns(3)
        c1.metric("Vencidas", len(df_lub[df_lub['STATUS'].str.contains("Vencida")]))
        c2.metric("Hoje", len(df_lub[df_lub['STATUS'].str.contains("Hoje")]))
        c3.metric("Total", len(df_lub))
        
        c_f1, c_f2, c_f3 = st.columns(3)
        stat = c_f1.multiselect("Status", ["🔴 Vencida", "🟡 Hoje", "🟢 No Prazo"], default=["🔴 Vencida", "🟡 Hoje"])
        maq = c_f2.multiselect("Máquina", df_lub['ATIVO'].unique())
        subs_unicos = sorted(list(set(df_lub['SUBATIVO'].dropna().astype(str).unique())))
        sub = c_f3.multiselect("Componente (Subativo)", subs_unicos)
        
        view = df_lub.copy()
        if stat: view = view[view['STATUS'].isin(stat)]
        if maq: view = view[view['ATIVO'].isin(maq)]
        if sub: view = view[view['SUBATIVO'].isin(sub)]
        
        if not view.empty:
            if st.button("🖨️ IMPRIMIR ROTA"):
                h = gerar_html_lubrificacao(view)
                st.download_button("Baixar Rota", h, "rota.html", "text/html")
                
        def cor(v):
            if "Vencida" in v: return 'color: red; font-weight: bold'
            if "Hoje" in v: return 'color: orange; font-weight: bold'
            return 'color: green'
            
        vd = view[['ATIVO','SUBATIVO','LUBRIFICANTE','STATUS','PRÓXIMA (DATA)']].copy()
        vd['PRÓXIMA (DATA)'] = vd['PRÓXIMA (DATA)'].apply(formatar_data_br)
        st.dataframe(vd.style.map(cor, subset=['STATUS']))
        
        with st.form("bx"):
            st.markdown(f"**Itens Listados:** {len(view)}")
            check_all = st.checkbox("✅ SELECIONAR TODOS OS ITENS LISTADOS ACIMA PARA BAIXA")
            
            # Usamos o ID real do banco agora para a chave
            view['ID_TEMP'] = view.index
            opts = view.apply(lambda x: f"{x.get('ATIVO')} - {x.get('SUBATIVO')}", axis=1)
            sels = st.multiselect("Ou selecione manualmente:", opts.index, format_func=lambda i: opts[i])
            dt_real = st.date_input("Data Realização", date.today(), format="DD/MM/YYYY")
            
            if st.form_submit_button("CONFIRMAR BAIXA"):
                if check_all: itens_para_baixa = view.index.tolist()
                else: itens_para_baixa = sels
                
                if not itens_para_baixa: 
                    st.warning("Selecione itens.")
                else:
                    with st.spinner("Registrando baixas na nuvem..."):
                        for i in itens_para_baixa:
                            # Converte a linha específica em dicionário
                            linha_atualizada = df_lub.loc[i].to_dict()
                            
                            # Atualiza a data
                            linha_atualizada['ULTIMA (DATA)'] = str(dt_real)
                            
                            # Envia apenas essa máquina específica para o Supabase
                            salvar_linha_lubrificacao_supabase(linha_atualizada)
                            
                    st.success(f"✅ Baixa realizada em {len(itens_para_baixa)} itens na Nuvem!")
                    import time
                    time.sleep(2)
                    st.rerun()
                    
        with st.expander("📦 Estoque de Lubrificantes"):
            if not df_est.empty:
                ne = st.data_editor(df_est, num_rows="dynamic")
                if st.button("Salvar Estoque"):
                    salvar_estoque(ne)
                    st.success("Salvo localmente!")

# ==============================================================================
# 8. OS PENDENTES
# ==============================================================================
elif menu == "8. OS Pendentes":
    st.title("🚨 OS Pendentes")
    ab = df[df['Status'] == 'ABERTA']
    if ab.empty: st.success("Nenhuma pendência!")
    else:
        tecs = ab['Responsavel'].unique()
        c1, c2 = st.columns(2)
        c1.metric("Pendências", len(ab))
        c2.metric("Técnicos Envolvidos", len(tecs))
        for t in tecs:
            ost = ab[ab['Responsavel'] == t]
            with st.expander(f"👷 {t} - {len(ost)} OS", expanded=True):
                tb = ost[['ID', 'Data_Emissao', 'Maquina', 'Tipo_Manutencao', 'Descricao_Pedido']].copy()
                tb['Data_Emissao'] = tb['Data_Emissao'].apply(formatar_data_br)
                st.table(tb)

# ==============================================================================
# 9. PENDÊNCIAS DE MÁQUINAS
# ==============================================================================
elif menu == "9. Pendências de Máquinas":
    st.title("⚠️ Gestão de Pendências")
    st.markdown("---")
    
    with st.expander("➕ Adicionar Pendência Manual (Sem OS)", expanded=False):
        with st.form("form_pend_manual"):
            c1, c2 = st.columns(2)
            maq_sel = c1.selectbox("Máquina", LISTA_MAQUINAS)
            tec_sel = c2.selectbox("Técnico", LISTA_TECNICOS)
            pend_desc = st.text_area("Descrição da Pendência")
            dt_pend = st.date_input("Data", date.today(), format="DD/MM/YYYY")
            
            if st.form_submit_button("💾 SALVAR PENDÊNCIA"):
                id_man = int(datetime.now().timestamp()) * -1
                novo_reg = {
                    "ID": id_man, "Data_Emissao": dt_pend, "Maquina": maq_sel, "Responsavel": "MANUAL",
                    "Tipo_Manutencao": "CORRETIVA", "Setor": "MECÂNICA", "Descricao_Pedido": "Pendência Manual",
                    "Status": "FECHADA", "Diagnostico": None, "Solucao": None, 
                    "Pecas_Trocadas": None, "Observacao_Maq": None,
                    "Tecnico": tec_sel, "Data_Inicio": None, "Data_Fim": dt_pend, "Horas_Totais": 0.0,
                    "Pendencia": pend_desc, "Status_Pendencia": "ABERTA", "Tipo_Problema": "MECÂNICO"
                }
                if salvar_unica_linha_supabase(novo_reg):
                    st.success("Pendência Registrada na Nuvem!")
                    import time
                    time.sleep(2)
                    st.rerun()
    
    st.markdown("---")
    
    if 'Pendencia' in df.columns:
        pendencias = df[
            (df['Pendencia'].notna()) & 
            (df['Pendencia'] != "") & 
            (df['Status_Pendencia'] == 'ABERTA')
        ]
        
        if pendencias.empty:
            st.success("✅ Nenhuma pendência em aberto nas máquinas!")
        else:
            maquinas_com_pendencia = pendencias['Maquina'].unique()
            for maq in maquinas_com_pendencia:
                pend_da_maq = pendencias[pendencias['Maquina'] == maq]
                with st.expander(f"🚨 {maq} ({len(pend_da_maq)} pendências)", expanded=True):
                    for index, row in pend_da_maq.iterrows():
                        col_a, col_b = st.columns([4, 1])
                        with col_a:
                            origem = f"OS #{row['ID']}" if row['ID'] > 0 else "MANUAL"
                            st.markdown(f"**📄 Origem:** {origem} | **👨‍🔧 Técnico:** {row['Tecnico']} | **📅 Data:** {formatar_data_br(row['Data_Fim'])}")
                            st.error(f"{row['Pendencia']}")
                        with col_b:
                            st.write("") 
                            if st.button("✅ RESOLVER", key=f"btn_solve_{row['ID']}_{index}"):
                                dados_resolver = row.to_dict()
                                dados_resolver['Status_Pendencia'] = "RESOLVIDA"
                                if salvar_unica_linha_supabase(dados_resolver):
                                    st.success("Resolvida na Nuvem!")
                                    st.rerun()
                        st.divider()
    else:
        st.info("Nenhuma pendência registrada ainda.")