import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA (ESTRITAMENTE CLEAN) ---
st.set_page_config(layout="wide", page_title="JARVIS | Gabriel Sabino", page_icon="👔")

# Tratamento de Conexão Cloud
try:
    from streamlit_gsheets import GSheetsConnection
    LIB_PRONTA = True
except ImportError:
    LIB_PRONTA = False

# --- ESTILO CSS MASTER (CLEAN UX & RESPONSIVIDADE) ---
st.markdown("""
    <style>
    /* Reset para Branco Total */
    .stApp { background-color: #FFFFFF; }
    header { visibility: hidden; }
    
    /* Sidebar Corporativa */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #E0E0E0;
        min-width: 250px !important;
    }
    
    /* Fontes e Textos */
    h1, h2, h3, p, span { font-family: 'Inter', sans-serif !important; color: #1B2631 !important; }
    
    /* Botões e Inputs */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #1B2631;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #FF8C00; color: white; }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .stMetric { padding: 10px; border: 1px solid #EEE; border-radius: 10px; margin-bottom: 5px; }
        div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
        .mapa-iframe { height: 500px !important; }
    }
    
    /* Cards do Mapa */
    .card-mapa {
        background: #FFFFFF;
        border-radius: 6px;
        padding: 8px;
        margin-bottom: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid #1B2631;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN CLEAN ---
with st.sidebar:
    st.markdown("### 🔐 Autenticação")
    senha = st.text_input("Credencial de Acesso", type="password", placeholder="Digite sua senha...")
    st.markdown("---")

if senha == "gsr17":
    if not LIB_PRONTA:
        st.error("Módulos de conexão em carregamento...")
        st.stop()

    # --- BANCO DE DADOS ---
    STATUS_OPCOES = ["Reunião", "A Iniciar", "Em Andamento", "Projetos Futuros", "Concluído"]
    CORES_MAP = {"Reunião": "#1B2631", "A Iniciar": "#5D6D7E", "Em Andamento": "#2E86C1", "Projetos Futuros": "#AED6F1", "Concluído": "#28B463"}
    URL_DB = "https://docs.google.com/spreadsheets/d/1SRUQwYW4acuehJ9St0bo2A2AFGW2UDKROzWQ1Y1mBJg/edit#gid=0"
    
    conn = st.connection("gsheets", type=GSheetsConnection)

    def carregar_dados():
        colunas = ["Projeto", "Data Inicial", "Prazo", "Status", "Foco", "Escopo", "Detalhamento", "Resultado Esperado"]
        try:
            df = conn.read(spreadsheet=URL_DB, ttl="0")
            if df is not None and not df.empty:
                for col in ["Data Inicial", "Prazo"]:
                    df[col] = pd.to_datetime(df[col], errors='coerce').fillna(pd.Timestamp.now())
                return df[colunas].dropna(subset=["Projeto"])
        except: pass
        return pd.DataFrame(columns=colunas)

    if 'df_projetos' not in st.session_state:
        st.session_state.df_projetos = carregar_dados()

    # --- SIDEBAR OPERACIONAL ---
    with st.sidebar:
        st.markdown(f"**Operador:** Gabriel Sabino")
        if st.button("🔄 SINCRONIZAR BANCO"):
            st.cache_data.clear()
            st.session_state.df_projetos = carregar_dados()
            st.rerun()
        st.link_button("📝 EDITAR PLANILHA", URL_DB)
        st.info(f"Projetos Ativos: {len(st.session_state.df_projetos)}")

    # --- NAVEGAÇÃO PRINCIPAL ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ MAPA", "📋 TRELLO", "📝 BANCO", "✍️ NOTAS", "📊 BI"])

    # ABA 1: MAPA ESTRATÉGICO (VISÃO AMPLA)
    with tab1:
        def gerar_mapa_html(df):
            atividades = df.to_dict('records')
            salas = {
                "Reunião": {"t": "2%", "l": "1%", "w": "98%", "h": "18%", "n": "🤝 REUNIÃO ESTRATÉGICA"},
                "A Iniciar": {"t": "22%", "l": "1%", "w": "31%", "h": "76%", "n": "🚀 BACKLOG"},
                "Em Andamento": {"t": "22%", "l": "34.5%", "w": "31%", "h": "48%", "n": "⚙️ EM EXECUÇÃO"},
                "Projetos Futuros": {"t": "72%", "l": "34.5%", "w": "31%", "h": "26%", "n": "📅 PIPELINE"},
                "Concluído": {"t": "22%", "l": "68%", "w": "31%", "h": "76%", "n": "✅ FINALIZADOS"}
            }
            html_final = ""
            for status, pos in salas.items():
                cards_html = ""
                for a in [x for x in atividades if x.get('Status') == status]:
                    cor = CORES_MAP.get(status, "#CCC")
                    cards_html += f'''<div class="card-mapa" style="border-left-color:{cor}">
                        <b style="font-size:11px;">{str(a.get("Projeto")).upper()}</b><br>
                        <span style="font-size:9px; color:#555;">{a.get("Foco")}</span></div>'''
                html_final += f'''<div style="position:absolute; top:{pos["t"]}; left:{pos["l"]}; width:{pos["w"]}; height:{pos["h"]}; background:#F8F9FA; border:1px solid #DDD; border-radius:8px;">
                    <div style="font-size:10px; font-weight:bold; padding:8px; border-bottom:1px solid #EEE;">{pos["n"]}</div>
                    <div style="padding:8px; overflow-y:auto; height:80%;">{cards_html}</div></div>'''
            return f'<div class="mapa-iframe" style="position:relative; width:100%; height:82vh; background:white;">{html_final}</div>'
        
        components.html(gerar_mapa_html(st.session_state.df_projetos), height=800)

    # ABA 2: TRELLO (VISÃO DE FLUXO)
    with tab2:
        cols = st.columns(len(STATUS_OPCOES))
        for i, status in enumerate(STATUS_OPCOES):
            with cols[i]:
                st.markdown(f"**{status.upper()}**")
                for a in st.session_state.df_projetos[st.session_state.df_projetos['Status'] == status].to_dict('records'):
                    with st.container():
                        st.markdown(f"""<div style="background:#FFF; border:1px solid #EEE; padding:10px; border-radius:8px; margin-bottom:10px; border-top:3px solid {CORES_MAP[status]};">
                            <small>{a.get('Projeto')}</small><br><b>{a.get('Foco')}</b></div>""", unsafe_allow_html=True)

    # ABA 3: BANCO (DADOS BRUTOS)
    with tab3:
        st.markdown("### Base de Dados Master")
        st.dataframe(st.session_state.df_projetos, use_container_width=True, height=600)

    # ABA 4: NOTAS
    with tab4:
        st.text_area("Bloco de Notas Estratégico", height=500, placeholder="Escreva aqui suas ideias...")

    # ABA 5: BI (GRÁFICOS E MÉTRICAS)
    with tab5:
        df = st.session_state.df_projetos
        if not df.empty:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Projetos", len(df))
            m2.metric("Ativos", len(df[df['Status'] == 'Em Andamento']))
            m3.metric("Concluídos", len(df[df['Status'] == 'Concluído']))
            m4.metric("% Entrega", f"{(len(df[df['Status']=='Concluído'])/len(df)*100):.1f}%")
            
            st.markdown("---")
            c_left, c_right = st.columns(2)
            with c_left:
                st.markdown("**Carga Operacional**")
                st.bar_chart(df['Status'].value_counts())
            with c_right:
                st.markdown("**Detalhamento por Status**")
                st.table(df['Status'].value_counts())
        else:
            st.warning("Sem dados para exibir indicadores.")

else:
    st.markdown("<h2 style='text-align:center;'>Aguardando Identificação do Operador</h2>", unsafe_allow_html=True)
    st.stop()
