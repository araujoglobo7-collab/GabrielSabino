import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import os
from datetime import datetime

# Tenta carregar a conexão, se não conseguir, ele não trava o app de cara
try:
    from streamlit_gsheets import GSheetsConnection
    LIB_PRONTA = True
except ImportError:
    LIB_PRONTA = False

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Gabriel Sabino - Hub Operacional")

# --- TRAVA DE SEGURANÇA ---
senha = st.sidebar.text_input("Acesso", type="password")

if senha == "gsr17":
    st.sidebar.success("Painel Liberado")
    
    if not LIB_PRONTA:
        st.error("O servidor ainda está instalando os componentes de nuvem. Aguarde 30 segundos e dê F5.")
        st.stop()

    # --- CONFIGURAÇÕES E BANCO DE DADOS ---
    STATUS_OPCOES = ["Reunião", "A Iniciar", "Em Andamento", "Projetos Futuros", "Concluído"]
    CORES_MAP = {"Reunião": "#1B2631", "A Iniciar": "#2E86C1", "Em Andamento": "#3498DB", "Projetos Futuros": "#5DADE2", "Concluído": "#28B463"}
    
    # URL DA PLANILHA (BANCO DE DADOS CENTRAL)
    URL_DB = "https://docs.google.com/spreadsheets/d/1SRUQwYW4acuehJ9St0bo2A2AFGW2UDKROzWQ1Y1mBJg/edit#gid=0"
    conn = st.connection("gsheets", type=GSheetsConnection)

    def carregar_dados():
        colunas = ["Projeto", "Data Inicial", "Prazo", "Status", "Foco", "Escopo", "Detalhamento", "Resultado Esperado"]
        try:
            # Puxa os dados ignorando o cache para garantir que venha tudo do banco
            df = conn.read(spreadsheet=URL_DB, ttl="0")
            if df is not None and not df.empty:
                df["Data Inicial"] = pd.to_datetime(df["Data Inicial"], errors='coerce').fillna(pd.Timestamp.now())
                df["Prazo"] = pd.to_datetime(df["Prazo"], errors='coerce').fillna(pd.Timestamp.now())
                return df[colunas].dropna(subset=["Projeto"])
        except Exception as e:
            st.sidebar.error(f"Erro na leitura: {e}")
        return pd.DataFrame(columns=colunas)

    if 'df_projetos' not in st.session_state:
        st.session_state.df_projetos = carregar_dados()

    # --- ESTILO GABRIEL SABINO (RESPONSIVO) ---
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #1B2631 !important; border-right: 5px solid #2E86C1; }
        [data-testid="stSidebar"] * { color: white !important; }
        .stTabs [aria-selected="true"] { background-color: #1B2631 !important; color: white !important; font-weight: bold; }
        @media (max-width: 768px) {
            [data-testid="stMetric"] { width: 100% !important; margin-bottom: 10px; }
            .stColumnsBlock { flex-direction: column !important; }
            div[data-testid="column"] { width: 100% !important; }
            .stTabs [role="tablist"] { display: flex; flex-wrap: wrap; }
        }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("👔 Gabriel Sabino")
        st.markdown("---")
        st.subheader("💾 Operação Banco")
        if st.button("🔄 RECARREGAR BANCO (POW)"):
            st.cache_data.clear()
            st.session_state.df_projetos = carregar_dados()
            st.success("Dados Sincronizados!")
            st.rerun()
        
        st.markdown("---")
        st.link_button("📝 EDITAR PLANILHA FONTE", URL_DB)
        st.info(f"Registros Ativos: {len(st.session_state.df_projetos)}")

    # --- NAVEGAÇÃO POR ABAS ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ AMBIENTE VIRTUAL", "📋 FLUXO (TRELLO)", "📝 MANIFESTO (BANCO)", "✍️ NOTAS", "📊 RESUMO IA"
    ])

    # ABA 1: AMBIENTE VIRTUAL
    with tab1:
        st.subheader("🗺️ Mapa Estratégico")
        cv1, cv2 = st.columns(2)
        f_v_nome = cv1.text_input("🔍 Buscar Projeto no Mapa", key="v_n")
        f_v_data = cv2.date_input("📅 Filtrar por Data Inicial", value=None, key="v_d")
        df_v = st.session_state.df_projetos.copy()
        if f_v_nome: df_v = df_v[df_v['Projeto'].str.contains(f_v_nome, case=False, na=False)]
        if f_v_data: df_v = df_v[df_v['Data Inicial'].dt.date == f_v_data]

        def gerar_mapa_html(df):
            atividades = df.to_dict('records')
            salas = {
                "Reunião": {"t": "1%", "l": "1%", "w": "98%", "h": "20%", "n": "🤝 REUNIÃO ESTRATÉGICA"},
                "A Iniciar": {"t": "23%", "l": "1%", "w": "32%", "h": "75%", "n": "🚀 BACKLOG"},
                "Em Andamento": {"t": "23%", "l": "34%", "w": "32%", "h": "45%", "n": "⚙️ EM EXECUÇÃO"},
                "Projetos Futuros": {"t": "70%", "l": "34%", "w": "32%", "h": "28%", "n": "📅 PIPELINE"},
                "Concluído": {"t": "23%", "l": "67%", "w": "32%", "h": "75%", "n": "✅ FINALIZADOS"}
            }
            html_final = ""
            for status, pos in salas.items():
                cards_html = ""
                status_cards = [x for x in atividades if x.get('Status') == status]
                for idx, a in enumerate(status_cards):
                    cor = CORES_MAP.get(status, "#ccc")
                    cards_html += f'''
                    <div style="background:#fff; border-left:6px solid {cor}; margin-bottom:12px; border-radius:8px; padding:12px; box-shadow:0 4px 6px rgba(0,0,0,0.1); border:1px solid #eee; font-family: sans-serif;">
                        <div style="display:flex; align-items:center; margin-bottom:8px;">
                            <span style="background:#1B2631; color:white; font-size:8px; padding:2px 6px; border-radius:4px; font-weight:bold;">SABINO</span>
                            <div style="flex-grow:1; height:10px; position:relative; margin-left:10px; background:#f0f0f0; border-radius:10px; overflow:hidden;"><div class="walker" style="animation-delay:{idx*0.5}s;"></div></div>
                        </div>
                        <div style="font-size:13px; font-weight:900; color:#1B2631; margin-bottom:4px;">{str(a.get("Projeto","")).upper()}</div>
                        <div style="font-size:10px; color:#2E86C1; font-weight:bold; margin-bottom:8px;">📅 {pd.to_datetime(a.get("Data Inicial")).strftime('%d/%m/%Y')}</div>
                        <div style="font-size:10px; color:#555; line-height:1.4;"><b>🎯 Foco:</b> {a.get('Foco')}<br><b>📑 Escopo:</b> {a.get('Escopo')}</div>
                    </div>'''
                html_final += f'''<div style="position:absolute; top:{pos["t"]}; left:{pos["l"]}; width:{pos["w"]}; height:{pos["h"]}; background:rgba(240,242,246,0.6); border-radius:12px; border:1px solid #ddd; display:flex; flex-direction:column;">
                    <div style="font-size:11px; font-weight:bold; color:#1B2631; padding:10px; border-bottom:1px solid #ddd; background:rgba(255,255,255,0.4); border-radius:12px 12px 0 0;">{pos["n"]}</div>
                    <div style="overflow-y:auto; flex-grow:1; padding:10px;">{cards_html}</div></div>'''
            return f"""<style>.walker {{ width:10px; height:10px; background: #FF6B00; border-radius:50%; position:absolute; top:0; animation: move 5s infinite ease-in-out alternate; }} @keyframes move {{ from {{ left:0%; }} to {{ left:calc(100% - 10px); }} }}</style>
            <div style="background:#FFFFFF; width:100%; height:82vh; position:relative; border-radius:15px; border:2px solid #eee; overflow:hidden;">{html_final}</div>"""
        components.html(gerar_mapa_html(df_v), height=850)

    # ABA 2: FLUXO (TRELLO)
    with tab2:
        st.subheader("📋 Trello Operacional")
        cols = st.columns(len(STATUS_OPCOES))
        for i, status in enumerate(STATUS_OPCOES):
            with cols[i]:
                st.markdown(f'<div style="background:{CORES_MAP[status]}; color:white; padding:10px; border-radius:5px; text-align:center; font-weight:bold; margin-bottom:15px;">{status.upper()}</div>', unsafe_allow_html=True)
                for a in st.session_state.df_projetos[st.session_state.df_projetos['Status'] == status].to_dict('records'):
                    st.markdown(f"""<div style="background:#FFFFFF; border:1px solid #ddd; border-left:5px solid {CORES_MAP[status]}; padding:15px; border-radius:10px; margin-bottom:15px; font-size:12px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                        <div style="font-size:14px; font-weight:bold; color:#1B2631; margin-bottom:5px;">{a.get('Projeto')}</div>
                        <div style="color:#2E86C1; margin-bottom:10px; font-weight:bold;">📅 {pd.to_datetime(a.get('Data Inicial')).strftime('%d/%m/%Y')}</div>
                        <div style="margin-bottom:3px;"><b>🎯 Foco:</b> {a.get('Foco')}</div>
                        </div>""", unsafe_allow_html=True)

    # ABA 3: MANIFESTO (VISUALIZAÇÃO DO BANCO)
    with tab3:
        st.subheader("📝 Manifesto de Dados (Base Master)")
        st.dataframe(st.session_state.df_projetos, use_container_width=True, height=500)
        st.info("Para editar, utilize o link da planilha na barra lateral e clique em Recarregar.")

    # ABA 4: NOTAS
    with tab4:
        st.text_area("✍️ Notas Estratégicas", height=600)

    # ABA 5: RESUMO IA
    with tab5:
        st.header("📊 Inteligência e Diagnóstico")
        df = st.session_state.df_projetos
        if not df.empty:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Projetos Totais", len(df))
            c2.metric("Em Execução", len(df[df['Status']=='Em Andamento']))
            c3.metric("Taxa Conclusão", f"{(len(df[df['Status']=='Concluído'])/len(df)*100 if len(df)>0 else 0):.1f}%")
            c4.metric("Backlog", len(df[df['Status']=='A Iniciar']))
            st.markdown("---")
            st.subheader("📈 Carga por Status")
            st.bar_chart(df['Status'].value_counts().reindex(STATUS_OPCOES, fill_value=0))
        else:
            st.warning("Aguardando importação de dados...")

else:
    st.sidebar.warning("Aguardando autenticação...")
    st.stop()
