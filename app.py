import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import hmac
from datetime import datetime, timedelta

try:
    from streamlit_gsheets import GSheetsConnection
    LIB_PRONTA = True
except ImportError:
    LIB_PRONTA = False

st.set_page_config(
    layout="wide",
    page_title="Sabino OS",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL STYLES (Mantido Original)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #F5F6F8;
    --bg2: #FFFFFF;
    --surface: #FFFFFF;
    --surface2: #F0F1F4;
    --border: #E2E4EA;
    --border-strong: #CDD0DA;
    --accent: #3B5BDB;
    --accent-light: rgba(59,91,219,0.08);
    --accent-muted: rgba(59,91,219,0.15);
    --gold: #D4880A;
    --green: #2F9E44;
    --red: #C92A2A;
    --orange: #E07B1A;
    --purple: #7048E8;
    --teal: #0C8599;
    --text: #1A1D2E;
    --text-muted: #6B7280;
    --text-dim: #9CA3AF;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stHeader"], #MainMenu, footer, .stDeployButton { display: none !important; }
[data-testid="stAppViewContainer"] { background: var(--bg) !important; }
.block-container { padding: 1.5rem 1.5rem 2rem !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: transparent !important;
    border-right: 1px solid rgba(59,91,219,0.15) !important;
    min-width: 220px !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: var(--accent) !important;
    border: 1px solid rgba(59,91,219,0.3) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #fff !important;
}

[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 20px !important;
}
[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: 'Syne', sans-serif !important;
}

.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# JARVIS HTML COMPONENT (Mantido Original)
# ============================================================
JARVIS_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: transparent; overflow: hidden; font-family: 'Space Grotesk', sans-serif; }
  #stage { width: 100%; height: 100%; position: relative; overflow: hidden; background: #F8F9FC; }
  canvas#particles { position: absolute; inset: 0; width: 100%; height: 100%; }
  .rings { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: min(320px, 90vw); height: min(320px, 90vw); }
  .ring { position: absolute; border-radius: 50%; border: 1px solid rgba(59,91,219,0.12); top: 50%; left: 50%; transform: translate(-50%, -50%); }
  .ring-1 { width: 100%; height: 100%; animation: spin 20s linear infinite; border-style: dashed; }
  .ring-2 { width: 72%; height: 72%; animation: spin 14s linear infinite reverse; }
  @keyframes spin { to { transform: translate(-50%,-50%) rotate(360deg); } }
  #bot { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -52%); width: min(260px, 75vw); animation: float 4s ease-in-out infinite; }
  @keyframes float { 0%,100%{transform:translate(-50%,-52%);} 50%{transform:translate(-50%,-56%);} }
  .hud { position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); font-size: 10px; letter-spacing: 3px; color: rgba(59,91,219,0.5); font-family: monospace; animation: pulse 2s infinite; }
  @keyframes pulse { 0%,100%{opacity:0.5;} 50%{opacity:1;} }
</style>
</head>
<body>
<div id="stage">
  <canvas id="particles"></canvas>
  <div class="rings"><div class="ring ring-1"></div><div class="ring ring-2"></div></div>
  <svg id="bot" viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg">
    <circle cx="200" cy="340" r="40" fill="#3B5BDB" opacity="0.3"/>
    <circle cx="200" cy="340" r="20" fill="#3B5BDB"/>
    <text x="200" y="94" text-anchor="middle" fill="#3B5BDB" font-size="12" font-family="monospace">J.A.R.V.I.S</text>
  </svg>
  <div class="hud">◆ J.A.R.V.I.S · NEURAL ENGINE ONLINE ◆</div>
</div>
<script>
const cv = document.getElementById('particles'); const ctx = cv.getContext('2d');
function resize() { cv.width = cv.offsetWidth; cv.height = cv.offsetHeight; } resize();
const P = Array.from({length: 30}, () => ({ x: Math.random()*cv.width, y: Math.random()*cv.height, vx: (Math.random()-0.5)*0.5, vy: (Math.random()-0.5)*0.5, r: 1.5 }));
function tick(){ ctx.clearRect(0,0,cv.width,cv.height); P.forEach(p => { p.x+=p.vx; p.y+=p.vy; if(p.x<0||p.x>cv.width)p.vx*=-1; if(p.y<0||p.y>cv.height)p.vy*=-1; ctx.fillStyle='#3B5BDB'; ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill(); }); requestAnimationFrame(tick); } tick();
</script>
</body>
</html>
"""

# ============================================================
# SESSION STATE
# ============================================================
if "logado" not in st.session_state:
    st.session_state.logado = False
if "df_projetos" not in st.session_state:
    st.session_state.df_projetos = None

# ============================================================
# LOGIN COM SEGURANÇA (HMAC + SECRETS)
# ============================================================
if not st.session_state.logado:
    st.markdown("""
    <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 20px;
        border:1px solid #E2E4EA;border-radius:10px;background:#F8F9FC;margin-bottom:28px;">
      <span style="font-family:monospace;font-size:10px;color:rgba(59,91,219,0.5);">◆ SABINO OS · v4.0</span>
      <span style="color:#2F9E44;font-size:10px;">● SISTEMA ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

    col_bot, col_gap, col_form = st.columns([1.05, 0.05, 0.9])
    with col_bot:
        components.html(JARVIS_HTML, height=560, scrolling=False)

    with col_form:
        st.markdown("""
        <div style="padding:40px 0 24px 0;">
          <div style="font-family:monospace;font-size:10px;color:#3B5BDB;">● J.A.R.V.I.S ONLINE</div>
          <div style="font-family:'Syne',sans-serif;font-size:42px;font-weight:800;color:#3B5BDB;">SABINO<br>OS</div>
          <p style="color:#6B7280;font-size:14px;">Aguardando autenticação do Senhor Sabino.</p>
        </div>
        """, unsafe_allow_html=True)

        senha_digitada = st.text_input("CREDENCIAL", type="password", placeholder="••••••••")

        if st.button("⚡  AUTENTICAR", use_container_width=True):
            # Compara a senha digitada com a que está nos Secrets do Streamlit
            if hmac.compare_digest(senha_digitada, st.secrets["credentials"]["password"]):
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("✗ Credencial inválida. Acesso negado.")
    st.stop()

# ============================================================
# DATA LOADING (GSheets Connection)
# ============================================================
URL_DB = "https://docs.google.com/spreadsheets/d/1SRUQwYW4acuehJ9St0bo2A2AFGW2UDKROzWQ1Y1mBJg/edit#gid=0"

@st.cache_data(ttl=300)
def carregar_dados():
    colunas = ["Projeto", "Data Inicial", "Prazo", "Status", "Foco", "Escopo", "Detalhamento", "Resultado Esperado"]
    if not LIB_PRONTA: return pd.DataFrame(columns=colunas)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=URL_DB, ttl=0)
        if df is not None and not df.empty:
            df["Data Inicial"] = pd.to_datetime(df["Data Inicial"], errors="coerce").fillna(pd.Timestamp.now())
            df["Prazo"] = pd.to_datetime(df["Prazo"], errors="coerce").fillna(pd.Timestamp.now())
            return df[colunas].dropna(subset=["Projeto"])
    except: return pd.DataFrame(columns=colunas)
    return pd.DataFrame(columns=colunas)

if st.session_state.df_projetos is None:
    st.session_state.df_projetos = carregar_dados()

df = st.session_state.df_projetos

# ============================================================
# HEADER & DASHBOARD
# ============================================================
with st.sidebar:
    st.markdown('<div style="font-family:Syne;font-size:20px;font-weight:800;color:#3B5BDB;">SABINO OS</div>', unsafe_allow_html=True)
    if st.button("🔄 Sincronizar", use_container_width=True):
        st.cache_data.clear()
        st.session_state.df_projetos = carregar_dados()
        st.rerun()
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.logado = False
        st.rerun()

now = datetime.now()
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;padding:16px 24px;border:1px solid #E2E4EA;border-radius:14px;background:#FFF;margin-bottom:24px;">
  <div><div style="font-size:22px;font-weight:800;color:#3B5BDB;">GABRIEL SABINO</div></div>
  <div style="text-align:right;font-size:10px;color:#9CA3AF;">
    <div style="color:#2F9E44;">● JARVIS ONLINE</div>
    <div>{now.strftime('%d %b %Y | %H:%M')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Tabs e Conteúdo (Simplificado para manter a estrutura do seu pedido)
tab1, tab2, tab3 = st.tabs(["⚡ VISÃO GERAL", "📋 PROJETOS", "📊 STATUS"])
with tab1:
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total de Projetos", len(df))
        c2.metric("Em Andamento", len(df[df["Status"] == "Em Andamento"]))
        c3.metric("Concluídos", len(df[df["Status"] == "Concluído"]))
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aguardando sincronização com o GSheets da GMA Engenharia...")
