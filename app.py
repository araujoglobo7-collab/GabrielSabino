import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime, timedelta

st.set_page_config(
    layout="wide",
    page_title="Sabino OS",
    page_icon=":crystal_ball:",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg: #F6F5FA;
    --bg2: #FFFFFF;
    --surface: #FFFFFF;
    --surface2: #EFECF8;
    --border: #DDD8F0;
    --border-strong: #C4BCDF;
    --accent: #6B21A8;
    --accent2: #10B981;
    --accent-light: rgba(107,33,168,0.07);
    --green: #10B981;
    --red: #C92A2A;
    --purple: #6B21A8;
    --text: #1A1225;
    --text-muted: #5B4E72;
    --text-dim: #9588AA;
}
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
[data-testid="stHeader"], #MainMenu, footer, .stDeployButton { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { transform: none !important; width: 240px !important; min-width: 240px !important; }
[data-testid="stAppViewContainer"] { background: var(--bg) !important; }
.block-container { padding: 1.5rem 1.5rem 2rem !important; max-width: 100% !important; }
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 12px rgba(107,33,168,0.06) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    overflow-x: auto !important;
    box-shadow: 0 1px 4px rgba(107,33,168,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 9px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #fff !important;
    box-shadow: 0 2px 8px rgba(107,33,168,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 20px !important;
    box-shadow: 0 1px 4px rgba(107,33,168,0.05) !important;
}
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(107,33,168,0.25) !important;
}
.stButton > button:hover {
    background: #4C1D95 !important;
    transform: translateY(-1px) !important;
}
.stTextInput input, .stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 14px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(107,33,168,0.12) !important;
}
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
hr { border-color: var(--border) !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "logado" not in st.session_state:
    st.session_state.logado = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df_projetos" not in st.session_state:
    st.session_state.df_projetos = None
if "estado_selecionado" not in st.session_state:
    st.session_state.estado_selecionado = None
if "projeto_chat_mapa" not in st.session_state:
    st.session_state.projeto_chat_mapa = None
if "chat_mapa_history" not in st.session_state:
    st.session_state.chat_mapa_history = []

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.logado:

    LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: transparent; overflow: hidden; }
  #stage {
    width: 100%; height: 100%;
    position: relative;
    display: flex; align-items: center; justify-content: center;
    background: transparent;
  }
  canvas { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; }
  #wizard { position: relative; z-index: 2; width: min(280px, 78vw); margin-top: 10px;
    animation: float 5s ease-in-out infinite;
    filter: drop-shadow(0 12px 32px rgba(107,33,168,0.3));
  }
  @keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-14px);} }

  .head-g { animation: nod 6s ease-in-out infinite; transform-origin: 130px 110px; }
  @keyframes nod { 0%,100%{transform:rotate(0);} 30%{transform:rotate(-3deg);} 70%{transform:rotate(2deg);} }

  .eye { animation: blink 5s infinite; }
  .el { transform-origin: 108px 96px; }
  .er { transform-origin: 152px 96px; }
  @keyframes blink { 0%,85%,100%{transform:scaleY(1);} 89%{transform:scaleY(0.05);} }

  .orb { animation: orbpulse 2s ease-in-out infinite; transform-origin: 218px 108px; }
  @keyframes orbpulse { 0%,100%{transform:scale(1);} 50%{transform:scale(1.18);} }

  .robe { animation: sway 7s ease-in-out infinite; transform-origin: 130px 220px; }
  @keyframes sway { 0%,100%{transform:rotate(0deg);} 50%{transform:rotate(1.5deg);} }

  .arm-r { animation: armwave 3.5s ease-in-out infinite; transform-origin: 185px 195px; }
  @keyframes armwave { 0%,100%{transform:rotate(0);} 50%{transform:rotate(-10deg);} }

  .mp { animation: mfloat 2.5s ease-in-out infinite; }
  .mp1{animation-delay:0s;} .mp2{animation-delay:.6s;} .mp3{animation-delay:1.2s;} .mp4{animation-delay:1.8s;}
  @keyframes mfloat { 0%{transform:translateY(0) scale(1);opacity:1;} 100%{transform:translateY(-28px) scale(0.1);opacity:0;} }

  .star { animation: twinkle 2s ease-in-out infinite; }
  .s1{animation-delay:0s;} .s2{animation-delay:.4s;} .s3{animation-delay:.8s;} .s4{animation-delay:1.2s;}
  @keyframes twinkle { 0%,100%{opacity:0.4;transform:scale(0.8) rotate(0deg);} 50%{opacity:1;transform:scale(1.2) rotate(20deg);} }

  .hud {
    position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%);
    font-size: 9px; letter-spacing: 3px; color: rgba(107,33,168,0.55);
    font-family: monospace; white-space: nowrap; z-index: 3;
    animation: pulse 2.5s ease-in-out infinite;
  }
  @keyframes pulse { 0%,100%{opacity:0.4;} 50%{opacity:1;} }
</style>
</head>
<body>
<div id="stage">
  <canvas id="cv"></canvas>

  <svg id="wizard" viewBox="0 0 260 420" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="gHat" cx="50%" cy="20%">
        <stop offset="0%" stop-color="#7C3AED"/>
        <stop offset="100%" stop-color="#1E0A36"/>
      </radialGradient>
      <radialGradient id="gRobe" cx="50%" cy="15%">
        <stop offset="0%" stop-color="#5B21B6"/>
        <stop offset="100%" stop-color="#1E0A36"/>
      </radialGradient>
      <radialGradient id="gFace" cx="45%" cy="35%">
        <stop offset="0%" stop-color="#F5DEB3"/>
        <stop offset="100%" stop-color="#C8A96A"/>
      </radialGradient>
      <radialGradient id="gOrb" cx="40%" cy="35%">
        <stop offset="0%" stop-color="#6EE7B7"/>
        <stop offset="60%" stop-color="#10B981"/>
        <stop offset="100%" stop-color="#064E3B"/>
      </radialGradient>
      <linearGradient id="gBeard" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#E5E7EB"/>
        <stop offset="100%" stop-color="#D1D5DB"/>
      </linearGradient>
      <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <filter id="bigglow"><feGaussianBlur stdDeviation="7"/></filter>
      <filter id="shadow"><feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#1E0A36" flood-opacity="0.4"/></filter>
    </defs>

    <!-- Shadow on ground -->
    <ellipse cx="118" cy="413" rx="62" ry="7" fill="#4C1D95" opacity="0.18" filter="url(#bigglow)"/>

    <!-- ===== ROBE / BODY ===== -->
    <g class="robe">
      <!-- Main robe -->
      <path d="M68 200 Q52 240 38 310 Q28 360 35 405 L205 405 Q212 360 202 310 Q188 240 172 200 Z"
            fill="url(#gRobe)"/>
      <!-- Robe center seam -->
      <path d="M120 200 Q118 280 116 405" stroke="#7C3AED" stroke-width="1.5" fill="none" opacity="0.4"/>
      <!-- Robe highlight left -->
      <path d="M68 200 Q58 250 50 320 L90 320 Q88 250 82 200 Z" fill="#7C3AED" opacity="0.25"/>
      <!-- Robe collar -->
      <path d="M80 198 Q120 210 160 198 L158 185 Q120 196 82 185 Z" fill="#A855F7" opacity="0.7"/>
      <!-- Belt -->
      <rect x="70" y="238" width="120" height="10" rx="5" fill="#4C1D95"/>
      <ellipse cx="120" cy="243" rx="10" ry="7" fill="#7C3AED"/>
      <ellipse cx="120" cy="243" rx="5" ry="4" fill="#10B981" filter="url(#glow)"/>
      <!-- Stars on robe -->
      <text x="75" y="285" font-size="16" class="star s1">&#11088;</text>
      <text x="148" y="310" font-size="12" class="star s2">&#10024;</text>
      <text x="60" y="340" font-size="10" class="star s3">&#11088;</text>
      <text x="155" y="260" font-size="10" class="star s4">&#10024;</text>
      <!-- Moon on robe -->
      <text x="95" y="360" font-size="18" opacity="0.7">&#9790;</text>
      <!-- Feet / boots -->
      <ellipse cx="88" cy="404" rx="26" ry="9" fill="#1E0A36"/>
      <ellipse cx="150" cy="404" rx="26" ry="9" fill="#1E0A36"/>
      <rect x="68" y="390" width="40" height="16" rx="8" fill="#2E1065"/>
      <rect x="130" y="390" width="40" height="16" rx="8" fill="#2E1065"/>
    </g>

    <!-- ===== LEFT ARM ===== -->
    <path d="M68 200 Q48 220 40 255 Q36 272 44 280 Q54 286 62 272 Q66 256 72 232 L80 208 Z"
          fill="#3B0764" filter="url(#shadow)"/>
    <!-- Left hand (old, wrinkled) -->
    <ellipse cx="44" cy="281" rx="13" ry="11" fill="url(#gFace)"/>
    <!-- Fingers -->
    <line x1="34" y1="276" x2="30" y2="268" stroke="#C8A96A" stroke-width="4" stroke-linecap="round"/>
    <line x1="38" y1="272" x2="35" y2="263" stroke="#C8A96A" stroke-width="4" stroke-linecap="round"/>
    <line x1="44" y1="270" x2="42" y2="261" stroke="#C8A96A" stroke-width="4" stroke-linecap="round"/>
    <line x1="50" y1="272" x2="50" y2="263" stroke="#C8A96A" stroke-width="4" stroke-linecap="round"/>

    <!-- ===== RIGHT ARM + STAFF ===== -->
    <g class="arm-r">
      <path d="M172 200 Q192 218 200 250 Q205 268 198 278 Q188 285 180 272 Q176 255 170 230 L162 208 Z"
            fill="#3B0764" filter="url(#shadow)"/>
      <!-- Right hand -->
      <ellipse cx="197" cy="279" rx="13" ry="11" fill="url(#gFace)"/>
      <!-- Staff -->
      <line x1="200" y1="275" x2="218" y2="85" stroke="#5C3A1E" stroke-width="7" stroke-linecap="round"/>
      <line x1="200" y1="275" x2="218" y2="85" stroke="#92400E" stroke-width="4" stroke-linecap="round" opacity="0.6"/>
      <!-- Staff glow line -->
      <line x1="218" y1="85" x2="218" y2="130" stroke="#10B981" stroke-width="2" opacity="0.5" filter="url(#glow)"/>
      <!-- ORB on staff -->
      <g class="orb">
        <ellipse cx="218" cy="78" rx="24" ry="24" fill="#10B981" opacity="0.2" filter="url(#bigglow)"/>
        <ellipse cx="218" cy="78" rx="18" ry="18" fill="url(#gOrb)" filter="url(#glow)"/>
        <ellipse cx="218" cy="78" rx="10" ry="10" fill="#6EE7B7" opacity="0.5"/>
        <ellipse cx="213" cy="73" rx="5" ry="5" fill="white" opacity="0.75"/>
        <!-- Orb inner symbols -->
        <text x="218" y="83" font-size="10" text-anchor="middle" fill="white" opacity="0.8">&#9670;</text>
      </g>
      <!-- Magic particles -->
      <circle class="mp mp1" cx="232" cy="65" r="3.5" fill="#10B981"/>
      <circle class="mp mp2" cx="204" cy="58" r="2.5" fill="#A855F7"/>
      <circle class="mp mp3" cx="238" cy="80" r="2" fill="#FDE68A"/>
      <circle class="mp mp4" cx="210" cy="50" r="3" fill="#10B981"/>
    </g>

    <!-- ===== HEAD GROUP ===== -->
    <g class="head-g">
      <!-- HAT -->
      <!-- Brim -->
      <ellipse cx="118" cy="52" rx="58" ry="11" fill="#2E1065" filter="url(#shadow)"/>
      <!-- Cone body -->
      <path d="M118 0 L74 52 L162 52 Z" fill="url(#gHat)" filter="url(#shadow)"/>
      <!-- Hat highlight -->
      <path d="M118 5 L102 52 L118 52 Z" fill="#A855F7" opacity="0.2"/>
      <!-- Hat band with buckle -->
      <rect x="74" y="47" width="88" height="9" rx="4" fill="#7C3AED" opacity="0.9"/>
      <rect x="110" y="44" width="16" height="14" rx="3" fill="#A855F7"/>
      <rect x="113" y="47" width="10" height="8" rx="2" fill="#10B981" opacity="0.8"/>
      <!-- Hat stars -->
      <text x="100" y="35" font-size="9" fill="#FDE68A" class="star s2">&#9733;</text>
      <text x="126" y="28" font-size="7" fill="#10B981" class="star s4">&#9670;</text>
      <!-- Hat tip glow -->
      <ellipse cx="118" cy="4" rx="6" ry="6" fill="#A855F7" opacity="0.6" filter="url(#glow)"/>

      <!-- NECK (wrinkled, old) -->
      <rect x="106" y="148" width="24" height="22" rx="5" fill="#C8A96A"/>
      <!-- Neck wrinkles -->
      <line x1="110" y1="155" x2="126" y2="155" stroke="#A07845" stroke-width="1" opacity="0.5"/>
      <line x1="110" y1="161" x2="126" y2="161" stroke="#A07845" stroke-width="1" opacity="0.5"/>

      <!-- FACE - older, bigger nose, wrinkled -->
      <ellipse cx="118" cy="108" rx="42" ry="46" fill="url(#gFace)" filter="url(#shadow)"/>
      <!-- Cheek shading -->
      <ellipse cx="96" cy="115" rx="12" ry="9" fill="#D4956A" opacity="0.3"/>
      <ellipse cx="140" cy="115" rx="12" ry="9" fill="#D4956A" opacity="0.3"/>
      <!-- Forehead wrinkles -->
      <path d="M96 80 Q118 76 140 80" stroke="#A07845" stroke-width="1.2" fill="none" opacity="0.5"/>
      <path d="M100 87 Q118 83 136 87" stroke="#A07845" stroke-width="1" fill="none" opacity="0.4"/>
      <!-- Under-eye wrinkles -->
      <path d="M94 107 Q100 110 106 107" stroke="#A07845" stroke-width="0.8" fill="none" opacity="0.5"/>
      <path d="M130 107 Q136 110 142 107" stroke="#A07845" stroke-width="0.8" fill="none" opacity="0.5"/>

      <!-- Bushy old eyebrows -->
      <path d="M90 86 Q102 79 114 84" stroke="#9CA3AF" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M122 84 Q134 79 146 86" stroke="#9CA3AF" stroke-width="4" fill="none" stroke-linecap="round"/>
      <!-- Eyebrow hairs -->
      <path d="M92 84 Q97 81 102 83" stroke="white" stroke-width="1.5" fill="none" opacity="0.6"/>
      <path d="M124 83 Q129 80 134 84" stroke="white" stroke-width="1.5" fill="none" opacity="0.6"/>

      <!-- LEFT EYE (wise, small) -->
      <g class="eye el">
        <ellipse cx="106" cy="100" rx="12" ry="11" fill="white"/>
        <ellipse cx="106" cy="100" rx="8" ry="8" fill="#4C1D95"/>
        <ellipse cx="106" cy="100" rx="4" ry="4" fill="#1E0A36"/>
        <ellipse cx="109" cy="97" rx="2.5" ry="2.5" fill="white" opacity="0.85"/>
        <!-- Wisdom glow -->
        <ellipse cx="106" cy="100" rx="8" ry="8" fill="#7C3AED" opacity="0.25" filter="url(#glow)"/>
        <!-- Crow's feet -->
        <path d="M118 96 Q122 94 124 91" stroke="#A07845" stroke-width="0.8" fill="none" opacity="0.6"/>
        <path d="M118 100 Q122 100 125 99" stroke="#A07845" stroke-width="0.8" fill="none" opacity="0.6"/>
        <path d="M118 104 Q122 106 124 109" stroke="#A07845" stroke-width="0.8" fill="none" opacity="0.6"/>
      </g>

      <!-- RIGHT EYE -->
      <g class="eye er">
        <ellipse cx="150" cy="100" rx="12" ry="11" fill="white"/>
        <ellipse cx="150" cy="100" rx="8" ry="8" fill="#4C1D95"/>
        <ellipse cx="150" cy="100" rx="4" ry="4" fill="#1E0A36"/>
        <ellipse cx="153" cy="97" rx="2.5" ry="2.5" fill="white" opacity="0.85"/>
        <ellipse cx="150" cy="100" rx="8" ry="8" fill="#7C3AED" opacity="0.25" filter="url(#glow)"/>
        <!-- Crow's feet -->
        <path d="M138 96 Q134 94 132 91" stroke="#A07845" stroke-width="0.8" fill="none" opacity="0.6"/>
        <path d="M138 100 Q134 100 131 99" stroke="#A07845" stroke-width="0.8" fill="none" opacity="0.6"/>
        <path d="M138 104 Q134 106 132 109" stroke="#A07845" stroke-width="0.8" fill="none" opacity="0.6"/>
      </g>

      <!-- BIG NOSE (old wizard) -->
      <path d="M115 108 Q110 118 105 124 Q112 130 118 128 Q124 130 131 124 Q126 118 121 108 Z"
            fill="#C8A96A" opacity="0.9"/>
      <!-- Nose tip -->
      <ellipse cx="118" cy="126" rx="9" ry="7" fill="#B8936A"/>
      <!-- Nostril -->
      <ellipse cx="113" cy="127" rx="3" ry="2" fill="#A07845" opacity="0.5"/>
      <ellipse cx="123" cy="127" rx="3" ry="2" fill="#A07845" opacity="0.5"/>

      <!-- Mustache (bushy) -->
      <path d="M96 132 Q107 127 118 130 Q129 127 140 132 Q130 140 118 138 Q106 140 96 132 Z"
            fill="#D1D5DB" opacity="0.95"/>
      <!-- Mustache texture -->
      <path d="M100 132 Q110 128 118 130" stroke="#E5E7EB" stroke-width="1.5" fill="none"/>
      <path d="M118 130 Q126 128 136 132" stroke="#E5E7EB" stroke-width="1.5" fill="none"/>

      <!-- LONG BEARD (old wizard) -->
      <path d="M86 138 Q74 165 70 195 Q68 220 72 250 Q80 290 88 330 Q100 355 118 365 Q136 355 148 330 Q156 290 164 250 Q168 220 166 195 Q162 165 150 138 Q136 130 118 134 Q100 130 86 138 Z"
            fill="url(#gBeard)" opacity="0.97"/>
      <!-- Beard center line -->
      <path d="M118 140 Q116 220 115 365" stroke="#E5E7EB" stroke-width="1.5" fill="none" opacity="0.5"/>
      <!-- Beard side lines -->
      <path d="M96 145 Q88 200 82 260" stroke="#E5E7EB" stroke-width="1" fill="none" opacity="0.4"/>
      <path d="M140 145 Q148 200 154 260" stroke="#E5E7EB" stroke-width="1" fill="none" opacity="0.4"/>
      <!-- Beard wave lines -->
      <path d="M88 200 Q100 195 112 200 Q124 205 136 200" stroke="#D1D5DB" stroke-width="1" fill="none" opacity="0.6"/>
      <path d="M84 240 Q98 235 114 240 Q130 245 142 240" stroke="#D1D5DB" stroke-width="1" fill="none" opacity="0.5"/>
      <path d="M86 280 Q100 275 116 280 Q132 285 146 280" stroke="#D1D5DB" stroke-width="1" fill="none" opacity="0.4"/>
      <!-- Beard tip -->
      <path d="M105 355 Q118 370 131 355 Q122 362 118 363 Q114 362 105 355 Z" fill="#D1D5DB"/>

      <!-- Ears (big, old) -->
      <ellipse cx="76" cy="108" rx="10" ry="13" fill="url(#gFace)"/>
      <ellipse cx="76" cy="108" rx="6" ry="8" fill="#C8A96A" opacity="0.5"/>
      <ellipse cx="160" cy="108" rx="10" ry="13" fill="url(#gFace)"/>
      <ellipse cx="160" cy="108" rx="6" ry="8" fill="#C8A96A" opacity="0.5"/>
    </g>
  </svg>

  <div class="hud">&#128302; FEITICO ATIVO &middot; AGUARDANDO BRUXO &#128302;</div>
</div>

<script>
const cv = document.getElementById('cv');
const ctx = cv.getContext('2d');
function resize(){ cv.width=cv.offsetWidth; cv.height=cv.offsetHeight; }
resize(); window.addEventListener('resize', resize);
const P = Array.from({length:28}, () => ({
  x: Math.random()*cv.width, y: Math.random()*cv.height,
  vx: (Math.random()-0.5)*0.35, vy: (Math.random()-0.5)*0.35,
  r: Math.random()*2+0.4,
  c: ['#6B21A8','#10B981','#A855F7','#FDE68A'][Math.floor(Math.random()*4)]
}));
function tick(){
  ctx.clearRect(0,0,cv.width,cv.height);
  P.forEach(p=>{
    p.x+=p.vx; p.y+=p.vy;
    if(p.x<0||p.x>cv.width) p.vx*=-1;
    if(p.y<0||p.y>cv.height) p.vy*=-1;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle=p.c; ctx.shadowBlur=8; ctx.shadowColor=p.c; ctx.fill();
  });
  requestAnimationFrame(tick);
}
tick();
</script>
</body>
</html>
"""

    col_bot, col_gap, col_form = st.columns([1.1, 0.05, 0.85])
    with col_bot:
        components.html(LOGIN_HTML, height=640, scrolling=False)
    with col_form:
        st.markdown("""
        <div style="padding:48px 0 28px 0;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:4px;
              color:#6B21A8;margin-bottom:16px;">&#128302; SISTEMA ATIVO</div>
          <div style="font-size:38px;margin-bottom:8px;">&#129497;&#8205;&#9794;&#65039;</div>
          <div style="font-family:'Syne',sans-serif;font-size:42px;font-weight:800;
              color:#6B21A8;line-height:1;margin-bottom:4px;">Bem-vindo,</div>
          <div style="font-family:'Syne',sans-serif;font-size:42px;font-weight:800;
              color:#10B981;line-height:1;margin-bottom:24px;">Sabino.</div>
          <p style="color:#5B4E72;font-size:14px;line-height:1.9;margin-bottom:0;">
            O feitico aguarda, Bruxo.<br>
            Insira sua credencial para<br>
            acessar o hub operacional.
          </p>
        </div>
        """, unsafe_allow_html=True)

        senha = st.text_input("CREDENCIAL SECRETA", type="password", placeholder="••••••••", label_visibility="visible")

        if st.button("&#128302;  INVOCAR ACESSO", use_container_width=True):
            if senha == "gsr17":
                st.session_state.logado = True
                st.rerun()
            else:
                st.markdown("""
                <div style="background:rgba(201,42,42,0.06);border:1px solid rgba(201,42,42,0.2);
                    border-radius:10px;padding:12px 16px;color:#C92A2A;font-size:13px;margin-top:8px;">
                  &#10007; &nbsp; Feitico invalido. Acesso negado, impostor!
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:28px;padding:16px;border:1px solid #DDD8F0;border-radius:10px;background:#EFECF8;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2px;color:#5B4E72;line-height:2.2;">
            &#9670; GRIMORIUM &middot; AES-256<br>
            &#9670; SESSAO &middot; MONITORADA<br>
            &#9670; ACESSO &middot; REGISTRADO
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# ============================================================
# DATA LOADING
# ============================================================
STATUS_OPCOES = ["Reuniao", "A Iniciar", "Em Andamento", "Projetos Futuros", "Concluido"]
STATUS_COLORS = {
    "Reuniao":          "#7048E8",
    "A Iniciar":        "#6B21A8",
    "Em Andamento":     "#7C3AED",
    "Projetos Futuros": "#0C8599",
    "Concluido":        "#10B981"
}
URL_DB = "https://docs.google.com/spreadsheets/d/1SRUQwYW4acuehJ9St0bo2A2AFGW2UDKROzWQ1Y1mBJg/edit#gid=0"

def fix_encoding(text):
    if not isinstance(text, str): return text
    try: return text.encode('latin1').decode('utf-8')
    except: return text

@st.cache_data(ttl=300)
def carregar_dados():
    colunas = ["Projeto","Data Inicial","Prazo","Status","Foco","Escopo","Detalhamento","Resultado Esperado"]
    try:
        import requests
        from io import StringIO
        sheet_id = "1SRUQwYW4acuehJ9St0bo2A2AFGW2UDKROzWQ1Y1mBJg"
        r = requests.get(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0", allow_redirects=True, timeout=15)
        r.raise_for_status()
        df = pd.read_csv(StringIO(r.text), encoding='utf-8')
        if df is not None and not df.empty:
            for col in ["Projeto","Status","Foco","Escopo","Detalhamento","Resultado Esperado"]:
                if col in df.columns: df[col] = df[col].apply(fix_encoding)
            df["Data Inicial"] = pd.to_datetime(df["Data Inicial"], errors="coerce").fillna(pd.Timestamp.now())
            df["Prazo"] = pd.to_datetime(df["Prazo"], errors="coerce").fillna(pd.Timestamp.now())
            cols_presentes = [c for c in colunas if c in df.columns]
            return df[cols_presentes].dropna(subset=["Projeto"])
    except Exception as e:
        st.sidebar.error(f"Erro: {e}")
    return pd.DataFrame(columns=["Projeto","Data Inicial","Prazo","Status","Foco","Escopo","Detalhamento","Resultado Esperado"])

if st.session_state.df_projetos is None:
    st.session_state.df_projetos = carregar_dados()
df = st.session_state.df_projetos

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="padding:0 0 20px 0;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:3px;color:#6B21A8;margin-bottom:4px;">&#128302; SISTEMA ATIVO</div>
      <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#6B21A8;">SABINO OS</div>
      <div style="font-size:11px;color:#9588AA;margin-top:2px;">Hub Operacional v4.0 &#129497;&#8205;&#9794;&#65039;</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("<div style='font-size:11px;color:#9588AA;letter-spacing:2px;margin-bottom:8px;'>ACOES</div>", unsafe_allow_html=True)
    if st.button("Sincronizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.session_state.df_projetos = carregar_dados()
        df = st.session_state.df_projetos
        st.success("Sincronizado!")
        st.rerun()
    st.link_button("Editar Planilha", URL_DB, use_container_width=True)
    st.divider()
    if not df.empty:
        total = len(df)
        concluidos = len(df[df["Status"] == "Concluido"])
        em_exec = len(df[df["Status"] == "Em Andamento"])
        taxa = round(concluidos/total*100, 1) if total > 0 else 0
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;gap:8px;">
          <div style="background:#FFFFFF;border:1px solid #DDD8F0;border-radius:10px;padding:12px 14px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9588AA;margin-bottom:4px;">PROJETOS</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#6B21A8;">{total}</div>
          </div>
          <div style="background:#FFFFFF;border:1px solid #DDD8F0;border-radius:10px;padding:12px 14px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9588AA;margin-bottom:4px;">CONCLUSAO</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#10B981;">{taxa}%</div>
          </div>
          <div style="background:#FFFFFF;border:1px solid #DDD8F0;border-radius:10px;padding:12px 14px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9588AA;margin-bottom:4px;">EM EXECUCAO</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#7C3AED;">{em_exec}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.divider()
    if st.button("Sair", use_container_width=True):
        st.session_state.logado = False
        st.session_state.df_projetos = None
        st.rerun()

# ============================================================
# HEADER
# ============================================================
now = datetime.now()
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
    padding:16px 24px;border:1px solid #DDD8F0;border-radius:14px;
    background:#FFFFFF;margin-bottom:24px;box-shadow:0 2px 8px rgba(107,33,168,0.06);">
  <div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:4px;color:#6B21A8;margin-bottom:4px;">&#128302; HUB OPERACIONAL</div>
    <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:#6B21A8;">GABRIEL SABINO &#129497;&#8205;&#9794;&#65039;</div>
  </div>
  <div style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:10px;color:#9588AA;letter-spacing:1px;">
    <div style="color:#10B981;margin-bottom:4px;">&#9679; JARVIS ONLINE</div>
    <div>{now.strftime('%A, %d %b %Y')}</div>
    <div>{now.strftime('%H:%M')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤖 CHAT IA",
    "⚡ VISAO GERAL",
    "📋 KANBAN",
    "🗂️ DADOS",
    "✍️ NOTAS"
])

# ─────────────────────────────────────────────
# TAB 1 — CHAT IA
# ─────────────────────────────────────────────
with tab1:
    sugestoes = [
        ("🔴", "Qual projeto tem maior risco de atraso"),
        ("🎯", "Onde focar energia essa semana"),
        ("📊", "Diagnostico geral do portfolio"),
        ("⚡", "Quais projetos posso acelerar"),
        ("🔍", "Identifique gargalos"),
        ("📅", "O que vence nos proximos 30 dias"),
    ]

    pergunta_sugerida = None

    col_chat, col_sugest = st.columns([2.5, 1])

    with col_sugest:
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #F0D9C8;border-radius:16px;padding:20px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #F0D9C8;">
            <div style="width:48px;height:48px;background:linear-gradient(135deg,#E8720C,#D4880A);
                border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;
                box-shadow:0 4px 12px rgba(232,114,12,0.3);">🤖</div>
            <div>
              <div style="font-weight:700;font-size:14px;color:#1A1208;">J.A.R.V.I.S</div>
              <div style="font-size:11px;color:#E8720C;font-family:'JetBrains Mono',monospace;">● ONLINE</div>
            </div>
          </div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9C8B82;margin-bottom:12px;">
            PERGUNTAS RAPIDAS
          </div>
        </div>
        """, unsafe_allow_html=True)

        for emoji, s in sugestoes:
            if st.button(f"{emoji}  {s}", key=f"sug_{s[:10]}", use_container_width=True):
                pergunta_sugerida = s

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️  Limpar conversa", use_container_width=True, key="limpar_chat"):
            st.session_state.chat_history = []
            st.rerun()

    with col_chat:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#E8720C,#D4880A);border-radius:16px;
            padding:20px 24px;margin-bottom:20px;display:flex;align-items:center;gap:16px;">
          <div style="font-size:36px;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.2));">🤖</div>
          <div>
            <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#fff;">J.A.R.V.I.S</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.8);">Consultor estrategico do seu portfolio</div>
          </div>
          <div style="margin-left:auto;background:rgba(255,255,255,0.2);border-radius:20px;padding:4px 12px;">
            <span style="font-size:11px;color:#fff;font-family:'JetBrains Mono',monospace;">● ATIVO</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown("""
            <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:16px;">
              <div style="width:44px;height:44px;background:linear-gradient(135deg,#E8720C,#D4880A);
                  border-radius:50%;display:flex;align-items:center;justify-content:center;
                  font-size:22px;flex-shrink:0;box-shadow:0 2px 8px rgba(232,114,12,0.3);">🤖</div>
              <div style="background:#FFFFFF;border:1px solid #F0D9C8;border-radius:4px 16px 16px 16px;
                  padding:16px 20px;max-width:90%;box-shadow:0 2px 8px rgba(232,114,12,0.08);">
                <div style="font-weight:700;color:#E8720C;margin-bottom:8px;font-size:15px;">✨ Salve, Bruxo! 🧙‍♂️</div>
                <div style="font-size:14px;color:#1A1208;line-height:1.7;">
                  Sistema ativo e pronto. Tenho acesso completo ao seu portfolio —
                  prazos, clientes, escopo, tudo.<br><br>
                  Me diz o que precisa, Bruxo. Use os botoes ao lado ou
                  manda sua pergunta aqui embaixo. 🔥
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;margin:12px 0;gap:8px;">
                  <div style="background:linear-gradient(135deg,#E8720C,#D4880A);color:#fff;
                      border-radius:16px 16px 4px 16px;padding:12px 18px;max-width:75%;
                      font-size:14px;line-height:1.5;box-shadow:0 2px 8px rgba(232,114,12,0.25);">
                    {msg['content']}
                  </div>
                  <div style="width:36px;height:36px;background:#F0D9C8;border-radius:50%;
                      display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">🧙‍♂️</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                content = msg['content'].replace(chr(10), '<br>')
                st.markdown(f"""
                <div style="display:flex;align-items:flex-start;gap:12px;margin:12px 0;">
                  <div style="width:44px;height:44px;background:linear-gradient(135deg,#E8720C,#D4880A);
                      border-radius:50%;display:flex;align-items:center;justify-content:center;
                      font-size:22px;flex-shrink:0;box-shadow:0 2px 8px rgba(232,114,12,0.3);">🤖</div>
                  <div style="background:#FFFFFF;border:1px solid #F0D9C8;border-radius:4px 16px 16px 16px;
                      padding:16px 20px;max-width:85%;font-size:14px;line-height:1.7;color:#1A1208;
                      box-shadow:0 2px 8px rgba(232,114,12,0.08);">
                    {content}
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        col_input, col_btn = st.columns([5, 1])
        with col_input:
            user_input = st.text_input(
                "msg",
                value=pergunta_sugerida or "",
                placeholder="Fala, Bruxo! O que precisa saber?",
                label_visibility="collapsed",
                key="chat_input"
            )
        with col_btn:
            enviar = st.button("Enviar", use_container_width=True)

    if (enviar or pergunta_sugerida) and (user_input or pergunta_sugerida):
        query = user_input or pergunta_sugerida
        st.session_state.chat_history.append({"role": "user", "content": query})

        now = pd.Timestamp.now()
        q = query.lower()

        try:
            if df.empty:
                answer = "⚠️ Nenhum projeto carregado. Sincronize a planilha primeiro, Bruxo!"
            else:
                ativos = df[df["Status"].isin(["A Iniciar", "Em Andamento"])]
                concluidos_df = df[df["Status"] == "Concluido"]
                em_exec = df[df["Status"] == "Em Andamento"]
                backlog = df[df["Status"] == "A Iniciar"]
                futuros = df[df["Status"] == "Projetos Futuros"]
                total = len(df)
                taxa = round(len(concluidos_df)/total*100, 1) if total > 0 else 0

                urgentes = ativos.copy()
                urgentes["dias"] = (urgentes["Prazo"] - now).dt.days
                urgentes = urgentes.sort_values("dias")

                if any(w in q for w in ["risco", "atraso", "urgente", "critico"]):
                    top = urgentes.head(5)
                    linhas = ""
                    for _, r in top.iterrows():
                        d = int((r["Prazo"] - now).days)
                        emoji = "🔴" if d < 7 else "🟡" if d < 30 else "🟢"
                        linhas += f"\n{emoji} **{r['Projeto']}** — {d} dias ({r['Prazo'].strftime('%d/%m/%Y')})"
                    answer = f"**⚠️ Bruxo, esses sao os projetos em maior risco:**\n{linhas}\n\n💡 Os marcados em 🔴 precisam de atencao AGORA."

                elif any(w in q for w in ["focar", "energia", "semana", "prioridade", "foco"]):
                    top = urgentes.head(3)
                    linhas = ""
                    for _, r in top.iterrows():
                        d = int((r["Prazo"] - now).days)
                        foco = str(r.get("Foco",""))[:50] if pd.notna(r.get("Foco")) else ""
                        linhas += f"\n🎯 **{r['Projeto']}** ({d}d) — {foco}"
                    answer = f"**🎯 Bruxo, o foco desta semana e:**\n{linhas}\n\n⚡ Concentre a magia nestes para evitar atrasos!"

                elif any(w in q for w in ["diagnostico", "geral", "portfolio", "situacao", "status"]):
                    answer = f"""**📊 Diagnostico do Portfolio, Bruxo:**

🔢 **Total de projetos:** {total}
✅ **Concluidos:** {len(concluidos_df)} ({taxa}%)
⚙️ **Em Andamento:** {len(em_exec)}
📋 **Backlog:** {len(backlog)}
🔮 **Futuros:** {len(futuros)}

{"🟢 **Performance Excepcional!** Pipeline acima da media!" if taxa >= 70 else "🟡 **Performance Estavel.** Ha espaco para acelerar o backlog." if taxa >= 40 else "🔴 **Atencao, Bruxo!** Revisao estrategica recomendada."}

💡 Proximo prazo critico: **{urgentes.iloc[0]['Projeto'] if not urgentes.empty else 'N/A'}** — vence em {int(urgentes.iloc[0]['dias']) if not urgentes.empty else 0} dias."""

                elif any(w in q for w in ["acelerar", "rapido", "adiantar"]):
                    top = urgentes[urgentes["dias"] > 30].head(4)
                    if top.empty:
                        answer = "⚡ Bruxo, todos os projetos ativos estao com prazo proximo. Conclua os urgentes primeiro!"
                    else:
                        linhas = "\n".join([f"⚡ **{r['Projeto']}** — {int(r['dias'])} dias" for _, r in top.iterrows()])
                        answer = f"**Projetos com prazo folgado para acelerar:**\n{linhas}\n\n✅ Aproveite o momento para adiantar, Bruxo!"

                elif any(w in q for w in ["gargalo", "problema", "bloqueio"]):
                    muitos_urgentes = urgentes[urgentes["dias"] < 14]
                    answer = f"""**🔍 Gargalos Identificados, Bruxo:**

{"🔴 **"+str(len(muitos_urgentes))+" projetos vencem em menos de 14 dias** — risco de sobrecarga!" if not muitos_urgentes.empty else "✅ Nenhum gargalo critico no momento."}

📋 **Backlog represado:** {len(backlog)} projetos aguardando inicio.
{"⚠️ Alto volume — considere priorizar ou redistribuir." if len(backlog) > 5 else "✅ Backlog em nivel saudavel."}"""

                elif any(w in q for w in ["30 dias", "vence", "prazo", "mes"]):
                    proximos = urgentes[urgentes["dias"] <= 30]
                    if proximos.empty:
                        answer = "✅ Bruxo, nenhum projeto vence nos proximos 30 dias. Tudo tranquilo!"
                    else:
                        linhas = ""
                        for _, r in proximos.iterrows():
                            d = int(r["dias"])
                            emoji = "🔴" if d < 7 else "🟡"
                            linhas += f"\n{emoji} **{r['Projeto']}** — {r['Prazo'].strftime('%d/%m/%Y')} ({d}d)"
                        answer = f"**📅 Vence nos proximos 30 dias ({len(proximos)} projetos):**\n{linhas}"

                else:
                    top3 = urgentes.head(3)
                    linhas = "\n".join([f"• **{r['Projeto']}** — {int(r['dias'])}d" for _, r in top3.iterrows()])
                    answer = f"""**🤖 Resumo Executivo, Bruxo:**

📊 Portfolio: **{total} projetos** | Conclusao: **{taxa}%**
⚙️ Em andamento: **{len(em_exec)}** | Backlog: **{len(backlog)}**

**Top prioridades agora:**
{linhas}

💬 Use os botoes ao lado para analises especificas!"""

        except Exception as e:
            answer = f"Erro interno: {str(e)}"

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

# ─────────────────────────────────────────────
# TAB 2 — VISAO GERAL
# ─────────────────────────────────────────────
with tab2:
    if df.empty:
        st.warning("Nenhum dado carregado. Sincronize ou verifique a planilha.")
    else:
        total = len(df)
        concluidos = len(df[df["Status"] == "Concluido"])
        em_exec = len(df[df["Status"] == "Em Andamento"])
        backlog = len(df[df["Status"] == "A Iniciar"])
        futuros = len(df[df["Status"] == "Projetos Futuros"])
        taxa = round(concluidos/total*100, 1) if total > 0 else 0

        cols = st.columns(5)
        kpis = [
            ("TOTAL", total, "#E8720C"),
            ("EM EXECUCAO", em_exec, "#D4880A"),
            ("CONCLUIDOS", concluidos, "#2F9E44"),
            ("BACKLOG", backlog, "#7048E8"),
            ("TAXA", f"{taxa}%", "#C92A2A" if taxa < 40 else "#D4880A" if taxa < 70 else "#2F9E44"),
        ]
        for i, (label, val, cor) in enumerate(kpis):
            cols[i].markdown(f"""
            <div style="background:#FFFFFF;border:1px solid #F0D9C8;
                border-radius:14px;padding:20px 18px;
                border-top:3px solid {cor};box-shadow:0 2px 8px rgba(232,114,12,0.08);">
              <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9C8B82;margin-bottom:8px;">{label}</div>
              <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:{cor};">{val}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            busca_vg = st.text_input("🔍 Buscar projeto/cliente", placeholder="Digite para filtrar...", key="filtro_vg")
        with fc2:
            status_vg = st.multiselect("Status", STATUS_OPCOES, default=[], key="status_vg", placeholder="Todos")
        with fc3:
            data_vg = st.date_input("Data inicial a partir de", value=None, key="data_vg")

        df_vg = df.copy()
        if busca_vg:
            df_vg = df_vg[df_vg["Projeto"].str.contains(busca_vg, case=False, na=False)]
        if status_vg:
            df_vg = df_vg[df_vg["Status"].isin(status_vg)]
        if data_vg:
            df_vg = df_vg[df_vg["Data Inicial"].dt.date >= data_vg]

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns([1.3, 1])

        with col_a:
            st.markdown("""
            <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#E8720C;margin-bottom:16px;">
            &#9670; PROJETOS ATIVOS — CARDS COMPLETOS
            </div>
            """, unsafe_allow_html=True)

            ativos = df_vg[df_vg["Status"].isin(["A Iniciar", "Em Andamento"])].copy()
            ativos = ativos.sort_values("Prazo")

            if not ativos.empty:
                for _, r in ativos.iterrows():
                    dias = (r["Prazo"] - pd.Timestamp.now()).days
                    cor = "#C92A2A" if dias < 7 else "#D4880A" if dias < 30 else "#2F9E44"
                    label = "URGENTE" if dias < 7 else "ATENCAO" if dias < 30 else "OK"
                    foco = str(r.get("Foco", "")) if pd.notna(r.get("Foco")) else "—"
                    escopo = str(r.get("Escopo", "")) if pd.notna(r.get("Escopo")) else "—"
                    detalhamento = str(r.get("Detalhamento", "")) if pd.notna(r.get("Detalhamento")) else ""
                    resultado = str(r.get("Resultado Esperado", "")) if pd.notna(r.get("Resultado Esperado")) else ""
                    status_cor = STATUS_COLORS.get(r.get("Status",""), "#E8720C")
                    data_ini = r["Data Inicial"].strftime("%d/%m/%Y") if pd.notna(r.get("Data Inicial")) else "—"

                    st.markdown(f"""
                    <div style="background:#FFFFFF;border:1px solid #F0D9C8;
                        border-left:4px solid {cor};border-radius:12px;padding:16px;margin-bottom:12px;
                        box-shadow:0 2px 8px rgba(232,114,12,0.08);">
                      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
                        <div style="font-weight:700;font-size:15px;color:#1A1208;flex:1;">{r['Projeto']}</div>
                        <div style="display:flex;gap:6px;flex-shrink:0;margin-left:8px;">
                          <span style="background:{status_cor}22;color:{status_cor};border:1px solid {status_cor}44;
                              padding:2px 8px;border-radius:20px;font-size:10px;font-family:'JetBrains Mono',monospace;">{r.get('Status','')}</span>
                          <span style="background:{cor};color:#fff;padding:3px 10px;border-radius:20px;
                              font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;">{dias}d · {label}</span>
                        </div>
                      </div>
                      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:10px;">
                        <div style="background:#FDF6F0;border-radius:8px;padding:8px 10px;">
                          <div style="font-size:9px;color:#9C8B82;letter-spacing:1px;margin-bottom:3px;">FOCO</div>
                          <div style="font-size:12px;color:#1A1208;font-weight:500;">{foco}</div>
                        </div>
                        <div style="background:#FDF6F0;border-radius:8px;padding:8px 10px;">
                          <div style="font-size:9px;color:#9C8B82;letter-spacing:1px;margin-bottom:3px;">INICIO</div>
                          <div style="font-size:12px;color:#1A1208;font-weight:500;">{data_ini}</div>
                        </div>
                        <div style="background:{cor}11;border-radius:8px;padding:8px 10px;border:1px solid {cor}33;">
                          <div style="font-size:9px;color:#9C8B82;letter-spacing:1px;margin-bottom:3px;">PRAZO</div>
                          <div style="font-size:12px;color:{cor};font-weight:700;">{r['Prazo'].strftime('%d/%m/%Y')}</div>
                        </div>
                      </div>
                      <div style="background:#FDF6F0;border-radius:8px;padding:10px 12px;margin-bottom:6px;">
                        <div style="font-size:9px;color:#9C8B82;letter-spacing:1px;margin-bottom:4px;">ESCOPO</div>
                        <div style="font-size:13px;color:#1A1208;line-height:1.5;">{escopo}</div>
                      </div>
                      {"<div style='background:#FDF6F0;border-radius:8px;padding:10px 12px;margin-bottom:6px;'><div style='font-size:9px;color:#9C8B82;letter-spacing:1px;margin-bottom:4px;'>DETALHAMENTO</div><div style='font-size:13px;color:#1A1208;line-height:1.5;'>"+detalhamento+"</div></div>" if detalhamento and detalhamento != "—" else ""}
                      {"<div style='background:#E8720C11;border:1px solid #E8720C33;border-radius:8px;padding:10px 12px;'><div style='font-size:9px;color:#E8720C;letter-spacing:1px;margin-bottom:4px;'>RESULTADO ESPERADO</div><div style='font-size:13px;color:#1A1208;line-height:1.5;'>"+resultado+"</div></div>" if resultado and resultado != "—" else ""}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhum projeto ativo encontrado com os filtros atuais.")

        with col_b:
            st.markdown("""
            <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#E8720C;margin-bottom:16px;">
            &#9670; DISTRIBUICAO
            </div>
            """, unsafe_allow_html=True)

            dist = df["Status"].value_counts().reindex(STATUS_OPCOES, fill_value=0)
            for status, count in dist.items():
                if count == 0:
                    continue
                pct = count / total * 100
                cor = STATUS_COLORS.get(status, "#E8720C")
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-size:12px;color:#6B5A4E;font-weight:500;">{status}</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:{cor};font-weight:700;">{count}</span>
                  </div>
                  <div style="background:#F0D9C8;border-radius:4px;height:6px;overflow:hidden;">
                    <div style="background:{cor};width:{pct:.0f}%;height:100%;border-radius:4px;box-shadow:0 0 8px {cor}88;"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 3 — KANBAN
# ─────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#E8720C;margin-bottom:20px;">
    &#9670; FLUXO OPERACIONAL
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("Sem dados.")
    else:
        fk1, fk2, fk3 = st.columns(3)
        with fk1:
            busca_kb = st.text_input("🔍 Buscar", placeholder="Projeto ou cliente...", key="filtro_kb")
        with fk2:
            status_kb = st.multiselect("Status", STATUS_OPCOES, default=[], key="status_kb", placeholder="Todos")
        with fk3:
            data_kb = st.date_input("Data inicial a partir de", value=None, key="data_kb")

        df_kb = df.copy()
        if busca_kb:
            df_kb = df_kb[df_kb["Projeto"].str.contains(busca_kb, case=False, na=False)]
        if status_kb:
            df_kb = df_kb[df_kb["Status"].isin(status_kb)]
        if data_kb:
            df_kb = df_kb[df_kb["Data Inicial"].dt.date >= data_kb]

        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(len(STATUS_OPCOES))
        for i, status in enumerate(STATUS_OPCOES):
            cor = STATUS_COLORS.get(status, "#E8720C")
            projetos = df_kb[df_kb["Status"] == status]
            count = len(projetos)

            with cols[i]:
                st.markdown(f"""
                <div style="background:#FFFFFF;border:1px solid #F0D9C8;
                    border-top:2px solid {cor};box-shadow:0 1px 4px rgba(232,114,12,0.08);border-radius:12px;padding:12px 14px;margin-bottom:12px;
                    text-align:center;">
                  <div style="font-size:10px;letter-spacing:2px;color:{cor};
                      font-family:'JetBrains Mono',monospace;">{status.upper()}</div>
                  <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:{cor};margin-top:2px;">{count}</div>
                </div>
                """, unsafe_allow_html=True)

                for _, row in projetos.iterrows():
                    data_str = pd.to_datetime(row.get("Data Inicial")).strftime("%d/%m/%Y") if pd.notna(row.get("Data Inicial")) else ""
                    prazo_str = pd.to_datetime(row.get("Prazo")).strftime("%d/%m/%Y") if pd.notna(row.get("Prazo")) else ""
                    foco = str(row.get("Foco", "")) if pd.notna(row.get("Foco")) else ""
                    escopo = str(row.get("Escopo", "")) if pd.notna(row.get("Escopo")) else ""
                    dias = (row["Prazo"] - pd.Timestamp.now()).days
                    cor_prazo = "#C92A2A" if dias < 7 else "#D4880A" if dias < 30 else "#2F9E44"
                    st.markdown(f"""
                    <div style="background:#FFFFFF;border:1px solid #F0D9C8;
                        border-left:3px solid {cor};border-radius:10px;padding:12px;margin-bottom:8px;
                        box-shadow:0 1px 4px rgba(232,114,12,0.06);">
                      <div style="font-weight:600;font-size:13px;color:#1A1208;margin-bottom:6px;line-height:1.3;">{row['Projeto']}</div>
                      {"<div style='font-size:11px;color:#6B5A4E;margin-bottom:4px;'>🎯 "+foco+"</div>" if foco else ""}
                      {"<div style='font-size:11px;color:#6B5A4E;margin-bottom:4px;'>📋 "+escopo+"</div>" if escopo else ""}
                      <div style="display:flex;justify-content:space-between;margin-top:6px;">
                        <span style="font-size:10px;color:#9C8B82;">📅 {data_str}</span>
                        <span style="font-size:10px;color:{cor_prazo};font-weight:600;">⏰ {prazo_str}</span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 4 — DADOS
# ─────────────────────────────────────────────
with tab4:
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#E8720C;margin-bottom:16px;">
    &#9670; BANCO DE DADOS OPERACIONAL
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("Sem dados carregados.")
    else:
        fd1, fd2, fd3 = st.columns(3)
        with fd1:
            busca_d = st.text_input("🔍 Buscar", placeholder="Projeto ou cliente...", key="filtro_d")
        with fd2:
            status_d = st.multiselect("Status", STATUS_OPCOES, default=[], key="status_d", placeholder="Todos")
        with fd3:
            data_d = st.date_input("Data inicial a partir de", value=None, key="data_d")

        df_d = df.copy()
        if busca_d:
            df_d = df_d[df_d["Projeto"].str.contains(busca_d, case=False, na=False)]
        if status_d:
            df_d = df_d[df_d["Status"].isin(status_d)]
        if data_d:
            df_d = df_d[df_d["Data Inicial"].dt.date >= data_d]

        st.markdown(f"<div style='font-size:12px;color:#9C8B82;margin-bottom:8px;'>{len(df_d)} projetos encontrados</div>", unsafe_allow_html=True)
        st.dataframe(df_d, use_container_width=True, height=500)

# ─────────────────────────────────────────────
# TAB 5 — NOTAS
# ─────────────────────────────────────────────
with tab5:
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#E8720C;margin-bottom:16px;">
    &#9670; NOTAS ESTRATEGICAS
    </div>
    """, unsafe_allow_html=True)

    st.text_area(
        "Espaco livre para anotacoes, ideias e contexto",
        height=500,
        placeholder="Escreva suas anotacoes aqui...\n\nDicas, estrategias, insights, proximos passos...",
        label_visibility="visible"
    )

    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1px;color:#9C8B82;margin-top:8px;text-align:right;">
    Notas sao locais e nao sao salvas entre sessoes
    </div>
    """, unsafe_allow_html=True)
