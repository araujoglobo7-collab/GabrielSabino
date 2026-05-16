import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime, timedelta

LIB_PRONTA = True

st.set_page_config(
    layout="wide",
    page_title="Sabino OS",
    page_icon=":zap:",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL STYLES
# ============================================================
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
    --accent-muted: rgba(107,33,168,0.14);
    --gold: #10B981;
    --green: #10B981;
    --red: #C92A2A;
    --orange: #7C3AED;
    --purple: #6B21A8;
    --teal: #0C8599;
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

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 220px !important;
    box-shadow: 2px 0 12px rgba(0,0,0,0.04) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    overflow-x: auto !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 9px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    white-space: nowrap !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #fff !important;
    box-shadow: 0 2px 8px rgba(59,91,219,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 20px !important;
    transition: all 0.2s !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
[data-testid="stMetric"]:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 4px 16px rgba(59,91,219,0.1) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(59,91,219,0.25) !important;
}
.stButton > button:hover {
    background: #2f4cba !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(59,91,219,0.35) !important;
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(59,91,219,0.12) !important;
}
.stTextInput label, .stTextArea label {
    color: var(--text-muted) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Link button */
.stLinkButton a {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 4px; }

/* Chat bubbles */
.chat-bubble-user {
    background: var(--accent);
    color: #fff;
    border-radius: 14px 14px 4px 14px;
    padding: 12px 16px;
    max-width: 75%;
    font-size: 14px;
    line-height: 1.5;
}
.chat-bubble-ai {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px 14px 14px 4px;
    padding: 12px 16px;
    max-width: 80%;
    font-size: 14px;
    color: var(--text);
    line-height: 1.6;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.chat-msg-user { display: flex; justify-content: flex-end; margin: 8px 0; }
.chat-msg-ai   { display: flex; justify-content: flex-start; margin: 8px 0; }

@media (max-width: 768px) {
    .block-container { padding: 0.75rem 0.5rem 2rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.4rem !important; }
    .stTabs [data-baseweb="tab"] { padding: 6px 8px !important; font-size: 10px !important; }
    section[data-testid="stSidebar"] { width: 100% !important; min-width: 100% !important; }
    [data-testid="stSidebar"] { width: 100% !important; }
    /* Stack columns on mobile */
    [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
    [data-testid="column"] { width: 100% !important; min-width: 100% !important; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# JARVIS LOGIN COMPONENT
# ============================================================
JARVIS_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: transparent; overflow: hidden; font-family: 'Space Grotesk', sans-serif; }

  #stage {
    width: 100%; height: 100%;
    position: relative; overflow: hidden;
    background: #F8F9FC;
  }

  canvas#particles { position: absolute; inset: 0; width: 100%; height: 100%; }

  /* Orbit rings */
  .rings { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: min(320px, 90vw); height: min(320px, 90vw); }
  .ring {
    position: absolute; border-radius: 50%;
    border: 1px solid rgba(59,91,219,0.12);
    top: 50%; left: 50%; transform: translate(-50%, -50%);
  }
  .ring-1 { width: 100%; height: 100%; animation: spin 20s linear infinite; border-style: dashed; border-color: rgba(59,91,219,0.15); }
  .ring-2 { width: 72%; height: 72%; animation: spin 14s linear infinite reverse; border-color: rgba(212,136,10,0.2); }
  .ring-3 { width: 48%; height: 48%; animation: spin 9s linear infinite; border-color: rgba(59,91,219,0.15); }

  /* Orbit dot */
  .orbit-dot {
    position: absolute; width: 6px; height: 6px;
    background: var(--c, #6B21A8); border-radius: 50%;
    box-shadow: 0 0 8px var(--c, #6B21A8);
    top: 0; left: 50%; transform: translateX(-50%) translateY(-3px);
  }
  .ring-1 .orbit-dot { --c: #6B21A8; }
  .ring-2 .orbit-dot { --c: #7C3AED; }

  @keyframes spin { to { transform: translate(-50%,-50%) rotate(360deg); } }

  /* SVG robot */
  #bot {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -52%);
    width: min(260px, 75vw);
    filter: drop-shadow(0 0 16px rgba(59,91,219,0.15)) drop-shadow(0 8px 24px rgba(0,0,0,0.12));
    animation: float 4s ease-in-out infinite;
  }
  @keyframes float { 0%,100%{ transform: translate(-50%,-52%); } 50%{ transform: translate(-50%,-56%); } }

  .jv-head { animation: headtilt 6s ease-in-out infinite; transform-origin: 200px 230px; }
  @keyframes headtilt { 0%,100%{ transform: rotate(0); } 30%{ transform: rotate(-3deg); } 70%{ transform: rotate(3deg); } }

  .eye { animation: blink 5s infinite; }
  @keyframes blink { 0%,90%,100%{ transform: scaleY(1); } 93%{ transform: scaleY(0.05); } }
  .eye-l { transform-origin: 163px 148px; }
  .eye-r { transform-origin: 237px 148px; }

  .bar { animation: talk 0.2s ease-in-out infinite alternate; transform-origin: center bottom; }
  .b1{ animation-delay: 0s; } .b2{ animation-delay: .03s; } .b3{ animation-delay: .06s; }
  .b4{ animation-delay: .09s; } .b5{ animation-delay: .06s; } .b6{ animation-delay: .03s; } .b7{ animation-delay: .01s; }
  @keyframes talk { from{ transform: scaleY(0.15); } to{ transform: scaleY(1.3); } }

  .rotor { animation: spin 3s linear infinite; transform-origin: 200px 340px; }
  .arm-l { animation: armL 4s ease-in-out infinite; transform-origin: 88px 270px; }
  .arm-r { animation: armR 4s ease-in-out infinite; transform-origin: 312px 270px; }
  @keyframes armL { 0%,100%{ transform: rotate(0); } 50%{ transform: rotate(-9deg); } }
  @keyframes armR { 0%,100%{ transform: rotate(0); } 50%{ transform: rotate(9deg); } }

  /* HUD text */
  .hud {
    position: absolute; bottom: 12px; left: 50%;
    transform: translateX(-50%);
    font-size: 10px; letter-spacing: 3px; color: rgba(59,91,219,0.5);
    font-family: 'JetBrains Mono', monospace;
    white-space: nowrap;
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse { 0%,100%{ opacity: 0.5; } 50%{ opacity: 1; } }
</style>
</head>
<body>
<div id="stage">
  <canvas id="particles"></canvas>

  <div class="rings">
    <div class="ring ring-1"><div class="orbit-dot"></div></div>
    <div class="ring ring-2"><div class="orbit-dot"></div></div>
    <div class="ring ring-3"></div>
  </div>

  <svg id="bot" viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="gGold" cx="50%" cy="35%">
        <stop offset="0%" stop-color="#D4C090"/>
        <stop offset="60%" stop-color="#7C3AED"/>
        <stop offset="100%" stop-color="#6B5020"/>
      </radialGradient>
      <radialGradient id="gCyan" cx="50%" cy="50%">
        <stop offset="0%" stop-color="#1A1D2E"/>
        <stop offset="60%" stop-color="#6B21A8"/>
        <stop offset="100%" stop-color="#2A2D3A"/>
      </radialGradient>
      <linearGradient id="gMetal" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#9CA3AF"/>
        <stop offset="50%" stop-color="#ECEEF3"/>
        <stop offset="100%" stop-color="#E8EAEF"/>
      </linearGradient>
      <linearGradient id="gChest" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#F0F2F7"/>
        <stop offset="100%" stop-color="#E8EAEF"/>
      </linearGradient>
      <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <filter id="bigGlow"><feGaussianBlur stdDeviation="8"/></filter>
    </defs>

    <!-- Shadow -->
    <ellipse cx="200" cy="490" rx="100" ry="7" fill="#6B21A8" opacity="0.2" filter="url(#bigGlow)"/>

    <!-- Antenna -->
    <line x1="200" y1="38" x2="200" y2="78" stroke="#7C3AED" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="200" cy="32" r="6" fill="url(#gGold)" filter="url(#glow)">
      <animate attributeName="r" values="4;8;4" dur="1.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.7;1;0.7" dur="1.2s" repeatCount="indefinite"/>
    </circle>

    <!-- HEAD GROUP -->
    <g class="jv-head">
      <!-- Neck -->
      <rect x="182" y="232" width="36" height="24" rx="4" fill="url(#gMetal)" stroke="rgba(99,179,237,0.3)" stroke-width="1"/>
      <!-- Head -->
      <path d="M118 100 Q118 68 148 68 L252 68 Q282 68 282 100 L282 215 Q282 238 252 238 L148 238 Q118 238 118 215 Z" fill="url(#gMetal)"/>
      <path d="M118 100 Q118 68 148 68 L252 68 Q282 68 282 100 L282 215 Q282 238 252 238 L148 238 Q118 238 118 215 Z" fill="none" stroke="rgba(99,179,237,0.25)" stroke-width="1.5"/>
      <!-- Top band -->
      <path d="M128 78 Q128 72 138 72 L262 72 Q272 72 272 78 L272 100 L128 100 Z" fill="url(#gGold)" opacity="0.8"/>
      <text x="200" y="94" text-anchor="middle" fill="#E8EAEF" font-size="9" font-weight="700" letter-spacing="3" font-family="monospace">JARVIS</text>
      <!-- Visor bg -->
      <rect x="135" y="112" width="130" height="72" rx="10" fill="#F0F1F4"/>
      <rect x="135" y="112" width="130" height="72" rx="10" fill="url(#gCyan)" opacity="0.15"/>
      <rect x="135" y="112" width="130" height="72" rx="10" fill="none" stroke="rgba(59,91,219,0.3)" stroke-width="1.5"/>
      <line x1="135" y1="130" x2="265" y2="130" stroke="#6B21A8" stroke-width="0.3" opacity="0.4"/>
      <line x1="135" y1="148" x2="265" y2="148" stroke="#6B21A8" stroke-width="0.3" opacity="0.4"/>
      <line x1="135" y1="166" x2="265" y2="166" stroke="#6B21A8" stroke-width="0.3" opacity="0.4"/>
      <!-- Left Eye -->
      <g class="eye eye-l">
        <circle cx="163" cy="148" r="16" fill="#F0F1F4" stroke="rgba(200,169,110,0.5)" stroke-width="1.5"/>
        <circle cx="163" cy="148" r="10" fill="url(#gCyan)" filter="url(#glow)"/>
        <circle cx="166" cy="145" r="3" fill="white" opacity="0.8"/>
        <circle cx="163" cy="148" r="4" fill="#1A1E2A" opacity="0.6"/>
      </g>
      <!-- Right Eye -->
      <g class="eye eye-r">
        <circle cx="237" cy="148" r="16" fill="#F0F1F4" stroke="rgba(200,169,110,0.5)" stroke-width="1.5"/>
        <circle cx="237" cy="148" r="10" fill="url(#gCyan)" filter="url(#glow)"/>
        <circle cx="240" cy="145" r="3" fill="white" opacity="0.8"/>
        <circle cx="237" cy="148" r="4" fill="#1A1E2A" opacity="0.6"/>
      </g>
      <!-- Corner accents on visor -->
      <path d="M140 116 L152 116" stroke="#6B21A8" stroke-width="1.5" opacity="0.5"/>
      <path d="M140 116 L140 124" stroke="#6B21A8" stroke-width="1.5" opacity="0.5"/>
      <path d="M260 116 L248 116" stroke="#7C3AED" stroke-width="1.5" opacity="0.5"/>
      <path d="M260 116 L260 124" stroke="#7C3AED" stroke-width="1.5" opacity="0.5"/>
      <!-- Equalizer mouth -->
      <g transform="translate(164,210)">
        <rect class="bar b1" x="0"  y="-5"  width="6" height="10" rx="2" fill="#7C3AED" opacity="0.8"/>
        <rect class="bar b2" x="9"  y="-8"  width="6" height="16" rx="2" fill="#6B21A8"/>
        <rect class="bar b3" x="18" y="-11" width="6" height="22" rx="2" fill="#7C3AED" opacity="0.8"/>
        <rect class="bar b4" x="27" y="-14" width="6" height="28" rx="2" fill="#6B21A8"/>
        <rect class="bar b5" x="36" y="-11" width="6" height="22" rx="2" fill="#7C3AED" opacity="0.8"/>
        <rect class="bar b6" x="45" y="-8"  width="6" height="16" rx="2" fill="#6B21A8"/>
        <rect class="bar b7" x="54" y="-5"  width="6" height="10" rx="2" fill="#7C3AED" opacity="0.8"/>
      </g>
      <!-- Side vents -->
      <rect x="118" y="140" width="8" height="3" rx="1" fill="rgba(99,179,237,0.4)"/>
      <rect x="118" y="147" width="8" height="3" rx="1" fill="rgba(99,179,237,0.4)"/>
      <rect x="118" y="154" width="8" height="3" rx="1" fill="rgba(99,179,237,0.4)"/>
      <rect x="274" y="140" width="8" height="3" rx="1" fill="rgba(246,173,85,0.4)"/>
      <rect x="274" y="147" width="8" height="3" rx="1" fill="rgba(246,173,85,0.4)"/>
      <rect x="274" y="154" width="8" height="3" rx="1" fill="rgba(246,173,85,0.4)"/>
    </g>

    <!-- BODY -->
    <g>
      <path d="M100 264 Q100 255 118 255 L282 255 Q300 255 300 264 L300 420 Q300 440 282 440 L118 440 Q100 440 100 420 Z" fill="url(#gChest)"/>
      <path d="M100 264 Q100 255 118 255 L282 255 Q300 255 300 264 L300 420 Q300 440 282 440 L118 440 Q100 440 100 420 Z" fill="none" stroke="rgba(99,179,237,0.2)" stroke-width="1.5"/>
      <!-- Chest shoulders gold trim -->
      <path d="M100 264 L130 255 L160 255 L160 285 L100 285 Z" fill="url(#gGold)" opacity="0.7"/>
      <path d="M300 264 L270 255 L240 255 L240 285 L300 285 Z" fill="url(#gGold)" opacity="0.7"/>
      <!-- Chest lines -->
      <line x1="100" y1="290" x2="300" y2="290" stroke="rgba(99,179,237,0.15)" stroke-width="1"/>
      <line x1="100" y1="380" x2="300" y2="380" stroke="rgba(99,179,237,0.15)" stroke-width="1"/>
      <!-- ARC REACTOR -->
      <circle cx="200" cy="340" r="52" fill="#F0F1F4" stroke="rgba(99,179,237,0.1)" stroke-width="1"/>
      <circle cx="200" cy="340" r="46" fill="url(#gCyan)" filter="url(#bigGlow)" opacity="0.5"/>
      <circle cx="200" cy="340" r="40" fill="#F0F1F4"/>
      <circle cx="200" cy="340" r="36" fill="none" stroke="rgba(246,173,85,0.6)" stroke-width="2"/>
      <circle cx="200" cy="340" r="28" fill="none" stroke="rgba(99,179,237,0.8)" stroke-width="1.5"/>
      <circle cx="200" cy="340" r="18" fill="url(#gCyan)" filter="url(#glow)"/>
      <circle cx="200" cy="340" r="10" fill="white" opacity="0.95"/>
      <!-- Rotor ticks -->
      <g class="rotor">
        <line x1="200" y1="304" x2="200" y2="314" stroke="#7C3AED" stroke-width="2"/>
        <line x1="200" y1="366" x2="200" y2="376" stroke="#7C3AED" stroke-width="2"/>
        <line x1="164" y1="340" x2="174" y2="340" stroke="#7C3AED" stroke-width="2"/>
        <line x1="226" y1="340" x2="236" y2="340" stroke="#7C3AED" stroke-width="2"/>
        <line x1="177" y1="317" x2="183" y2="325" stroke="rgba(99,179,237,0.6)" stroke-width="1.5"/>
        <line x1="223" y1="317" x2="217" y2="325" stroke="rgba(99,179,237,0.6)" stroke-width="1.5"/>
        <line x1="177" y1="363" x2="183" y2="355" stroke="rgba(99,179,237,0.6)" stroke-width="1.5"/>
        <line x1="223" y1="363" x2="217" y2="355" stroke="rgba(99,179,237,0.6)" stroke-width="1.5"/>
      </g>
      <!-- Side status LEDs -->
      <circle cx="128" cy="316" r="4" fill="#2F9E44" filter="url(#glow)">
        <animate attributeName="opacity" values="0.3;0.9;0.3" dur="2s" repeatCount="indefinite"/>
      </circle>
      <circle cx="272" cy="316" r="4" fill="#6B21A8" filter="url(#glow)">
        <animate attributeName="opacity" values="0.3;0.9;0.3" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="128" cy="328" r="3" fill="#7C3AED">
        <animate attributeName="opacity" values="0.9;0.2;0.9" dur="0.8s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- LEFT ARM -->
    <g class="arm-l">
      <rect x="73" y="265" width="24" height="130" rx="11" fill="url(#gMetal)" stroke="rgba(99,179,237,0.2)" stroke-width="1"/>
      <rect x="78" y="265" width="14" height="30" rx="4" fill="url(#gGold)" opacity="0.6"/>
      <circle cx="85" cy="400" r="14" fill="url(#gMetal)" stroke="rgba(246,173,85,0.4)" stroke-width="1.5"/>
      <circle cx="85" cy="400" r="6" fill="url(#gGold)" opacity="0.8"/>
    </g>

    <!-- RIGHT ARM -->
    <g class="arm-r">
      <rect x="303" y="265" width="24" height="130" rx="11" fill="url(#gMetal)" stroke="rgba(99,179,237,0.2)" stroke-width="1"/>
      <rect x="308" y="265" width="14" height="30" rx="4" fill="url(#gGold)" opacity="0.6"/>
      <circle cx="315" cy="400" r="14" fill="url(#gMetal)" stroke="rgba(246,173,85,0.4)" stroke-width="1.5"/>
      <circle cx="315" cy="400" r="6" fill="url(#gGold)" opacity="0.8"/>
    </g>

    <!-- LEGS -->
    <rect x="138" y="440" width="48" height="48" rx="8" fill="url(#gMetal)" stroke="rgba(99,179,237,0.15)" stroke-width="1"/>
    <rect x="214" y="440" width="48" height="48" rx="8" fill="url(#gMetal)" stroke="rgba(99,179,237,0.15)" stroke-width="1"/>
    <rect x="134" y="485" width="58" height="14" rx="7" fill="url(#gGold)" opacity="0.7"/>
    <rect x="208" y="485" width="58" height="14" rx="7" fill="url(#gGold)" opacity="0.7"/>
  </svg>

  <div class="hud">&#128302; J.A.R.V.I.S &middot; FEITICO ATIVO &#128302;</div>
</div>

<script>
const cv = document.getElementById('particles');
const ctx = cv.getContext('2d');
function resize() { cv.width = cv.offsetWidth; cv.height = cv.offsetHeight; }
resize();
window.addEventListener('resize', resize);
const P = Array.from({length: 35}, () => ({
  x: Math.random()*cv.width, y: Math.random()*cv.height,
  vx: (Math.random()-0.5)*0.35, vy: (Math.random()-0.5)*0.35,
  r: Math.random()*1.6+0.4,
  c: Math.random()>0.5 ? '#6B21A8' : '#7C3AED'
}));
function tick(){
  ctx.clearRect(0,0,cv.width,cv.height);
  P.forEach(p => {
    p.x+=p.vx; p.y+=p.vy;
    if(p.x<0||p.x>cv.width) p.vx*=-1;
    if(p.y<0||p.y>cv.height) p.vy*=-1;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle=p.c; ctx.shadowBlur=6; ctx.shadowColor=p.c; ctx.fill();
  });
  for(let i=0;i<P.length;i++) for(let j=i+1;j<P.length;j++){
    const dx=P[i].x-P[j].x, dy=P[i].y-P[j].y, d=Math.sqrt(dx*dx+dy*dy);
    if(d<90){ ctx.strokeStyle=`rgba(59,91,219,${0.15*(1-d/90)})`; ctx.lineWidth=0.5;
      ctx.beginPath(); ctx.moveTo(P[i].x,P[i].y); ctx.lineTo(P[j].x,P[j].y); ctx.stroke(); }
  }
  requestAnimationFrame(tick);
}
tick();

// Voice greeting
setTimeout(() => {
  try {
    const u = new SpeechSynthesisUtterance('Bem-vindo, senhor Sabino. Sistema pronto para autenticacao.');
    u.lang='pt-BR'; u.rate=0.85; u.pitch=0.5; u.volume=0.8;
    speechSynthesis.speak(u);
  } catch(e){}
}, 1000);
</script>
</body>
</html>
"""

# ============================================================
# ============================================================
# ============================================================
# ============================================================
# ============================================================
# SESSION STATE
# ============================================================
if "logado" not in st.session_state:
    st.session_state.logado = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df_projetos" not in st.session_state:
    st.session_state.df_projetos = None
if "is_convidado" not in st.session_state:
    st.session_state.is_convidado = False
if "nome_convidado" not in st.session_state:
    st.session_state.nome_convidado = ""
if "login_step" not in st.session_state:
    st.session_state.login_step = "senha"
if "pw_erro" not in st.session_state:
    st.session_state.pw_erro = False

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.logado:

    hora_atual = datetime.now().hour
    if hora_atual < 12:
        saudacao = "Bom dia"
    elif hora_atual < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');
    [data-testid="stSidebar"],[data-testid="stHeader"],
    footer,[data-testid="stToolbar"]  { display:none !important; }
    html,body,.stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .block-container                  { background:#060912 !important;
                                        padding:0 !important;
                                        max-width:100% !important; }
    [data-testid="column"]            { padding:0 !important; }
    .stTextInput label                { display:none !important; }
    .stTextInput input {
        background: #0D0F22 !important;
        border: 1.5px solid rgba(107,33,168,.45) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-size: 16px !important;
        font-family: 'Inter', sans-serif !important;
        padding: 14px 16px !important;
        caret-color: #A855F7 !important;
        transition: all .2s !important;
    }
    .stTextInput input:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(107,33,168,.2) !important;
        background: #11102A !important;
    }
    .stTextInput input::placeholder { color: rgba(255,255,255,.2) !important; }
    .stButton > button {
        background: linear-gradient(135deg,#7C3AED,#4C1D95) !important;
        color: #fff !important; border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important; font-size: 15px !important;
        padding: 14px !important; width: 100% !important;
        box-shadow: 0 4px 18px rgba(107,33,168,.4) !important;
        transition: all .2s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(107,33,168,.6) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    jarvis_html = """<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:100%;height:100%;background:#060912;overflow:hidden;display:flex;align-items:center;justify-content:center;}
#pc{position:fixed;inset:0;pointer-events:none;}
#scene{position:relative;display:flex;align-items:center;justify-content:center;width:100%;height:100vh;}
#face-wrap{position:relative;display:flex;flex-direction:column;align-items:center;}
#face{width:clamp(200px,30vw,280px);filter:drop-shadow(0 0 36px rgba(107,33,168,.75));animation:float 4s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}
.fh{animation:ht 6s ease-in-out infinite;transform-origin:130px 130px;}
@keyframes ht{0%,100%{transform:rotate(0);}30%{transform:rotate(-4deg);}70%{transform:rotate(3deg);}}
.fe{animation:bl 4s infinite;}
.fel{transform-origin:95px 115px;}.fer{transform-origin:165px 115px;}
@keyframes bl{0%,85%,100%{transform:scaleY(1);}89%{transform:scaleY(.04);}}
.fm{animation:tk .35s ease-in-out infinite alternate;transform-origin:130px 162px;}
@keyframes tk{from{transform:scaleY(.08);}to{transform:scaleY(1);}}
.fs{animation:sc 2s linear infinite;}
@keyframes sc{0%{transform:translateY(-35px);opacity:0;}20%{opacity:1;}80%{opacity:1;}100%{transform:translateY(35px);opacity:0;}}
#bub{
  position:absolute;right:-210px;top:16px;
  width:195px;background:#fff;
  border:2px solid #6B21A8;
  border-radius:18px 18px 18px 4px;
  padding:16px 14px;
  box-shadow:0 8px 32px rgba(107,33,168,.3);
  animation:pop .6s 1s cubic-bezier(.34,1.56,.64,1) both;
  z-index:10;
}
@keyframes pop{from{opacity:0;transform:scale(.7) translateY(10px);}to{opacity:1;transform:scale(1) translateY(0);}}
#bub::before{content:'';position:absolute;left:-12px;top:22px;border:12px solid transparent;border-right-color:#6B21A8;border-left:none;}
#bub::after{content:'';position:absolute;left:-9px;top:24px;border:10px solid transparent;border-right-color:#fff;border-left:none;}
.btag{font-family:monospace;font-size:8px;letter-spacing:3px;color:#7C3AED;margin-bottom:7px;}
.btxt{font-size:16px;font-weight:800;color:#1A1225;line-height:1.35;}
.btxt span{color:#6B21A8;}
.bsub{font-size:11px;color:#9588AA;margin-top:7px;line-height:1.5;}
.hud{position:fixed;bottom:12px;left:50%;transform:translateX(-50%);font-family:monospace;font-size:9px;letter-spacing:3px;color:rgba(107,33,168,.4);white-space:nowrap;animation:ph 2s ease-in-out infinite;}
@keyframes ph{0%,100%{opacity:.3;}50%{opacity:.8;}}
@media(max-width:680px){
  #bub{right:auto;left:50%;transform:translateX(-50%) scale(.7);top:auto;bottom:-110px;}
  #bub::before,#bub::after{display:none;}
}
</style></head><body>
<canvas id="pc"></canvas>
<div id="scene">
  <div id="face-wrap">
    <svg id="face" viewBox="0 0 260 260" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="gh" cx="50%" cy="35%"><stop offset="0%" stop-color="#2A2D4A"/><stop offset="100%" stop-color="#0D0F1E"/></radialGradient>
      <radialGradient id="gv" cx="50%" cy="40%"><stop offset="0%" stop-color="#0A0D20"/><stop offset="100%" stop-color="#050712"/></radialGradient>
      <radialGradient id="ge" cx="40%" cy="35%"><stop offset="0%" stop-color="#A855F7"/><stop offset="100%" stop-color="#1E0856"/></radialGradient>
      <radialGradient id="gm" cx="50%" cy="0%"><stop offset="0%" stop-color="#7C3AED"/><stop offset="100%" stop-color="#4C1D95"/></radialGradient>
      <filter id="fw"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <filter id="fsw"><feGaussianBlur stdDeviation="10"/></filter>
    </defs>
    <circle cx="130" cy="130" r="115" fill="#6B21A8" opacity=".07" filter="url(#fsw)"/>
    <g class="fh">
      <rect x="18" y="18" width="224" height="224" rx="42" fill="url(#gh)"/>
      <rect x="18" y="18" width="224" height="224" rx="42" fill="none" stroke="rgba(107,33,168,.5)" stroke-width="2"/>
      <rect x="18" y="18" width="224" height="38" rx="42" fill="rgba(107,33,168,.22)"/>
      <rect x="18" y="44" width="224" height="12" fill="rgba(107,33,168,.12)"/>
      <text x="130" y="41" text-anchor="middle" fill="rgba(167,139,250,.85)" font-size="10" font-weight="700" letter-spacing="4" font-family="monospace">J . A . R . V . I . S</text>
      <rect x="32" y="68" width="196" height="136" rx="16" fill="url(#gv)"/>
      <rect x="32" y="68" width="196" height="136" rx="16" fill="none" stroke="rgba(107,33,168,.6)" stroke-width="1.5"/>
      <line x1="33" y1="93"  x2="227" y2="93"  stroke="#7C3AED" stroke-width=".5" opacity=".25"/>
      <line x1="33" y1="113" x2="227" y2="113" stroke="#7C3AED" stroke-width=".5" opacity=".25"/>
      <line x1="33" y1="133" x2="227" y2="133" stroke="#7C3AED" stroke-width=".5" opacity=".25"/>
      <line x1="33" y1="153" x2="227" y2="153" stroke="#7C3AED" stroke-width=".5" opacity=".25"/>
      <line x1="33" y1="173" x2="227" y2="173" stroke="#7C3AED" stroke-width=".5" opacity=".25"/>
      <rect class="fs" x="33" y="110" width="194" height="2.5" rx="1" fill="#10B981" opacity=".55" filter="url(#fw)"/>
      <path d="M36 72 L50 72" stroke="#A855F7" stroke-width="2" opacity=".8"/>
      <path d="M36 72 L36 84" stroke="#A855F7" stroke-width="2" opacity=".8"/>
      <path d="M224 72 L210 72" stroke="#10B981" stroke-width="2" opacity=".8"/>
      <path d="M224 72 L224 84" stroke="#10B981" stroke-width="2" opacity=".8"/>
      <path d="M36 200 L50 200" stroke="#A855F7" stroke-width="2" opacity=".8"/>
      <path d="M36 200 L36 188" stroke="#A855F7" stroke-width="2" opacity=".8"/>
      <path d="M224 200 L210 200" stroke="#10B981" stroke-width="2" opacity=".8"/>
      <path d="M224 200 L224 188" stroke="#10B981" stroke-width="2" opacity=".8"/>
      <g class="fe fel">
        <circle cx="93" cy="113" r="26" fill="#060912" stroke="rgba(167,139,250,.3)" stroke-width="1.5"/>
        <circle cx="93" cy="113" r="17" fill="url(#ge)" filter="url(#fw)"/>
        <circle cx="93" cy="113" r="8"  fill="#080A18" opacity=".55"/>
        <circle cx="100" cy="106" r="6" fill="white" opacity=".75"/>
      </g>
      <g class="fe fer">
        <circle cx="167" cy="113" r="26" fill="#060912" stroke="rgba(167,139,250,.3)" stroke-width="1.5"/>
        <circle cx="167" cy="113" r="17" fill="url(#ge)" filter="url(#fw)"/>
        <circle cx="167" cy="113" r="8"  fill="#080A18" opacity=".55"/>
        <circle cx="174" cy="106" r="6" fill="white" opacity=".75"/>
      </g>
      <g class="fm">
        <rect x="86" y="156" width="88" height="26" rx="13" fill="url(#gm)" filter="url(#fw)"/>
        <rect x="90" y="160" width="80" height="18" rx="9" fill="#060912" opacity=".35"/>
        <rect x="94" y="161" width="14" height="14" rx="4" fill="rgba(255,255,255,.15)"/>
        <rect x="112" y="161" width="14" height="14" rx="4" fill="rgba(255,255,255,.1)"/>
        <rect x="130" y="161" width="14" height="14" rx="4" fill="rgba(255,255,255,.15)"/>
        <rect x="148" y="161" width="14" height="14" rx="4" fill="rgba(255,255,255,.1)"/>
      </g>
      <circle cx="26" cy="98" r="5" fill="#10B981" filter="url(#fw)"><animate attributeName="opacity" values=".2;1;.2" dur="2s" repeatCount="indefinite"/></circle>
      <circle cx="234" cy="98" r="5" fill="#7C3AED" filter="url(#fw)"><animate attributeName="opacity" values=".2;1;.2" dur="1.5s" repeatCount="indefinite"/></circle>
      <circle cx="26" cy="112" r="3" fill="#7C3AED"><animate attributeName="opacity" values=".8;.1;.8" dur=".8s" repeatCount="indefinite"/></circle>
      <line x1="130" y1="18" x2="130" y2="3" stroke="#7C3AED" stroke-width="3" stroke-linecap="round"/>
      <circle cx="130" cy="-1" r="6" fill="#A855F7" filter="url(#fw)"><animate attributeName="r" values="4;9;4" dur="1.3s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;1;.6" dur="1.3s" repeatCount="indefinite"/></circle>
    </g>
    </svg>
    <div id="bub">
      <div class="btag">⬡ J.A.R.V.I.S ONLINE</div>
      <div class="btxt">SAUDACAO_PLACEHOLDER!<br><span>Gabriel</span> 👋</div>
      <div class="bsub">Digite sua senha para acessar o hub operacional.</div>
    </div>
  </div>
</div>
<div class="hud">⬡ J.A.R.V.I.S · HUB OPERACIONAL SABINO OS ⬡</div>
<script>
const pc=document.getElementById("pc"),ctx=pc.getContext("2d");
function r(){pc.width=window.innerWidth;pc.height=window.innerHeight;}
r();window.addEventListener("resize",r);
const p=Array.from({length:28},()=>({
  x:Math.random()*pc.width,y:Math.random()*pc.height,
  vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35,
  r:Math.random()*1.8+.4,c:Math.random()>.5?"#6B21A8":"#10B981"
}));
(function loop(){
  ctx.clearRect(0,0,pc.width,pc.height);
  p.forEach(q=>{q.x+=q.vx;q.y+=q.vy;
    if(q.x<0||q.x>pc.width)q.vx*=-1;
    if(q.y<0||q.y>pc.height)q.vy*=-1;
    ctx.beginPath();ctx.arc(q.x,q.y,q.r,0,Math.PI*2);
    ctx.fillStyle=q.c;ctx.shadowBlur=7;ctx.shadowColor=q.c;ctx.fill();});
  requestAnimationFrame(loop);
})();
</script>
</body></html>"""

    jarvis_html = jarvis_html.replace("SAUDACAO_PLACEHOLDER", saudacao)

    col_face, col_form = st.columns([1, 1])

    with col_face:
        components.html(jarvis_html, height=560, scrolling=False)

    with col_form:
        if st.session_state.login_step == "senha":
            components.html(f"""<!DOCTYPE html><html><head>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:100%;height:100%;background:#060912;display:flex;
  flex-direction:column;justify-content:center;
  padding:0 28px 0 8px;font-family:'Inter',sans-serif;}}
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@800&family=JetBrains+Mono:wght@400;500&display=swap');
.badge{{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:4px;
  color:#7C3AED;margin-bottom:12px;}}
.gs{{font-family:'Syne',sans-serif;font-size:56px;font-weight:800;
  color:#fff;line-height:.95;}}
.con{{font-family:'Syne',sans-serif;font-size:36px;font-weight:800;
  color:#10B981;line-height:1;}}
</style></head><body>
<div class="badge">⬡ IDENTIFICAÇÃO</div>
<div class="gs">GS</div>
<div class="con">Consulting</div>
</body></html>""", height=200, scrolling=False)

            senha = st.text_input("pw", type="password",
                placeholder="••••••••", label_visibility="collapsed", key="inp_senha")
            entrar = st.button("Entrar →", use_container_width=True, key="btn_entrar")

            if entrar and senha:
                if senha == "gr1723":
                    st.session_state.logado = True
                    st.session_state.is_convidado = False
                    st.session_state.nome_convidado = "Gabriel"
                    st.session_state.pw_erro = False
                    st.rerun()
                elif senha == "gsr17":
                    st.session_state.login_step = "nome_conv"
                    st.session_state.pw_erro = False
                    st.rerun()
                elif senha:
                    st.session_state.pw_erro = True
                    st.rerun()

            if st.session_state.pw_erro:
                st.markdown("""
                <div style="background:rgba(201,42,42,.08);border:1px solid rgba(201,42,42,.2);
                    border-radius:10px;padding:10px 14px;color:#F87171;font-size:13px;margin-top:4px;">
                  ❌ Senha incorreta.
                </div>""", unsafe_allow_html=True)

        else:
            components.html("""<!DOCTYPE html><html><head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:100%;height:100%;background:#060912;display:flex;
  flex-direction:column;justify-content:center;padding:0 28px 0 8px;}
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@800&family=JetBrains+Mono:wght@400&display=swap');
.badge{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:4px;color:#7C3AED;margin-bottom:12px;}
.t{font-family:'Syne',sans-serif;font-size:36px;font-weight:800;color:#fff;line-height:1.1;}
</style></head><body>
<div class="badge">⬡ ACESSO CONVIDADO</div>
<div class="t">Qual é o<br>seu nome?</div>
</body></html>""", height=160, scrolling=False)

            nome = st.text_input("nm", placeholder="Seu nome",
                label_visibility="collapsed", key="inp_nome")
            entrar2 = st.button("Entrar →", use_container_width=True, key="btn_entrar2")

            if entrar2 and nome:
                st.session_state.logado = True
                st.session_state.is_convidado = True
                st.session_state.nome_convidado = nome
                st.session_state.login_step = "senha"
                st.rerun()

    st.stop()


# DATA LOADING
# ============================================================
STATUS_OPCOES = ["Reuniao", "A Iniciar", "Em Andamento", "Projetos Futuros", "Concluido"]
STATUS_COLORS = {
    "Reuniao":          "#7048E8",
    "A Iniciar":        "#8BA8C8",
    "Em Andamento":     "#6B21A8",
    "Projetos Futuros": "#0C8599",
    "Concluido":        "#2F9E44"
}

URL_DB = "https://docs.google.com/spreadsheets/d/1SRUQwYW4acuehJ9St0bo2A2AFGW2UDKROzWQ1Y1mBJg/edit#gid=0"

def fix_encoding(text):
    if not isinstance(text, str):
        return text
    try:
        return text.encode('latin1').decode('utf-8')
    except:
        return text

@st.cache_data(ttl=300)
def carregar_dados():
    colunas = ["Projeto","Data Inicial","Prazo","Status","Foco","Escopo","Detalhamento","Resultado Esperado"]
    try:
        import requests
        sheet_id = "1SRUQwYW4acuehJ9St0bo2A2AFGW2UDKROzWQ1Y1mBJg"
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
        r = requests.get(csv_url, allow_redirects=True, timeout=15)
        r.raise_for_status()
        from io import StringIO
        df = pd.read_csv(StringIO(r.text), encoding='utf-8')
        if df is not None and not df.empty:
            for col in ["Projeto","Status","Foco","Escopo","Detalhamento","Resultado Esperado"]:
                if col in df.columns:
                    df[col] = df[col].apply(fix_encoding)
            df["Data Inicial"] = pd.to_datetime(df["Data Inicial"], errors="coerce").fillna(pd.Timestamp.now())
            df["Prazo"] = pd.to_datetime(df["Prazo"], errors="coerce").fillna(pd.Timestamp.now())
            cols_presentes = [c for c in colunas if c in df.columns]
            return df[cols_presentes].dropna(subset=["Projeto"])
    except Exception as e:
        st.sidebar.error(f"Erro: {e}")
    return pd.DataFrame(columns=colunas)

if st.session_state.df_projetos is None:
    st.session_state.df_projetos = carregar_dados()

df = st.session_state.df_projetos

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="padding:0 0 20px 0;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:3px;color:#6B21A8;margin-bottom:4px;">&#9679; SISTEMA ATIVO</div>
      <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
          color:#6B21A8;">
          SABINO OS</div>
      <div style="font-size:11px;color:#9CA3AF;margin-top:2px;">Hub Operacional v4.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("<div style='font-size:11px;color:#9CA3AF;letter-spacing:2px;margin-bottom:8px;'>ACOES</div>", unsafe_allow_html=True)

    if st.button("Sincronizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.session_state.df_projetos = carregar_dados()
        df = st.session_state.df_projetos
        st.success("Sincronizado!")
        st.rerun()

    if not st.session_state.is_convidado:
        st.link_button("Editar Planilha", URL_DB, use_container_width=True)

    st.divider()

    if not df.empty:
        total = len(df)
        concluidos = len(df[df["Status"] == "Concluido"])
        em_exec = len(df[df["Status"] == "Em Andamento"])
        taxa = round(concluidos/total*100, 1) if total > 0 else 0

        st.markdown(f"""
        <div style="display:flex;flex-direction:column;gap:8px;">
          <div style="background:#FFFFFF;border:1px solid #E8EAEF;border-radius:10px;padding:12px 14px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9CA3AF;margin-bottom:4px;">PROJETOS</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#6B21A8;">{total}</div>
          </div>
          <div style="background:#FFFFFF;border:1px solid #E8EAEF;border-radius:10px;padding:12px 14px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9CA3AF;margin-bottom:4px;">CONCLUSAO</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#2F9E44;">{taxa}%</div>
          </div>
          <div style="background:#FFFFFF;border:1px solid #E8EAEF;border-radius:10px;padding:12px 14px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9CA3AF;margin-bottom:4px;">EM EXECUCAO</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#7C3AED;">{em_exec}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if st.button("Sair", use_container_width=True):
        st.session_state.logado = False
        st.session_state.is_convidado = False
        st.session_state.nome_convidado = ""
        st.session_state.df_projetos = None
        st.rerun()

# ============================================================
# HEADER
# ============================================================
now = datetime.now()
usuario_nome = st.session_state.nome_convidado.upper() if st.session_state.is_convidado else "GABRIEL SABINO"
usuario_cor  = "#7C3AED" if st.session_state.is_convidado else "#6B21A8"
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
    padding:16px 24px;border:1px solid #E2E4EA;border-radius:14px;
    background:#FFFFFF;backdrop-filter:blur(10px);margin-bottom:{"8px" if st.session_state.is_convidado else "24px"};">
  <div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:4px;color:#6B21A8;margin-bottom:4px;">&#9679; HUB OPERACIONAL</div>
    <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
        color:{usuario_cor};">
        {usuario_nome}</div>
  </div>
  <div style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:10px;color:#9CA3AF;letter-spacing:1px;">
    <div style="color:#2F9E44;margin-bottom:4px;">&#9679; JARVIS ONLINE</div>
    <div>{now.strftime('%A, %d %b %Y')}</div>
    <div>{now.strftime('%H:%M')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Banner convidado
if st.session_state.is_convidado:
    st.markdown("""
    <div style="background:rgba(124,58,237,0.07);border:1px solid rgba(124,58,237,0.25);
        border-radius:10px;padding:10px 18px;margin-bottom:18px;
        display:flex;align-items:center;gap:10px;">
      <span style="font-size:18px;">🔒</span>
      <div>
        <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#7C3AED;font-weight:700;">
          ACESSO CONVIDADO</span>
        <span style="font-size:12px;color:#5B4E72;margin-left:10px;">
          Rosto não reconhecido. Acesso em modo leitura.</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🤖 CHAT IA",
    "⚡ VISAO GERAL",
    "📋 KANBAN",
    "🗂️ DADOS",
    "🗺️ MAPEAMENTO GS",
    "✍️ NOTAS",
    "📅 CALENDARIO"
])

# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# TAB 1 — CHAT IA
# ─────────────────────────────────────────────
with tab1:
    # Convidado: vê histórico mas não envia
    if st.session_state.is_convidado:
        st.markdown("""
        <div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2);
            border-radius:12px;padding:12px 18px;margin-bottom:16px;
            display:flex;align-items:center;gap:10px;">
          <span style="font-size:16px;">🔒</span>
          <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#7C3AED;">
            MODO LEITURA — envio de mensagens disponível apenas para Gabriel</span>
        </div>
        """, unsafe_allow_html=True)
        if not st.session_state.chat_history:
            st.info("Nenhuma conversa ainda.")
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display:flex;justify-content:flex-end;margin:10px 0;gap:8px;">
                      <div style="background:linear-gradient(135deg,#6B21A8,#4C1D95);color:#fff;
                          border-radius:14px 14px 4px 14px;padding:10px 16px;max-width:75%;font-size:14px;">
                        {msg["content"]}
                      </div>
                    </div>""", unsafe_allow_html=True)
                else:
                    content = msg["content"].replace(chr(10), "<br>")
                    st.markdown(f"""
                    <div style="display:flex;gap:10px;margin:10px 0;">
                      <div style="background:#FFFFFF;border:1px solid #DDD8F0;border-radius:4px 14px 14px 14px;
                          padding:12px 16px;max-width:85%;font-size:14px;color:#1A1225;line-height:1.7;">
                        {content}
                      </div>
                    </div>""", unsafe_allow_html=True)

    else:
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
            <div style="background:#FFFFFF;border:1px solid #DDD8F0;border-radius:16px;padding:20px;">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #DDD8F0;">
                <div style="width:48px;height:48px;background:linear-gradient(135deg,#6B21A8,#4C1D95);
                    border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;
                    box-shadow:0 4px 12px rgba(107,33,168,0.3);">🤖</div>
                <div>
                  <div style="font-weight:700;font-size:14px;color:#1A1225;">J.A.R.V.I.S</div>
                  <div style="font-size:11px;color:#6B21A8;font-family:'JetBrains Mono',monospace;">● ONLINE</div>
                </div>
              </div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9588AA;margin-bottom:12px;">
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
            <div style="background:linear-gradient(135deg,#6B21A8,#4C1D95);border-radius:16px;
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
                  <div style="width:44px;height:44px;background:linear-gradient(135deg,#6B21A8,#4C1D95);
                      border-radius:50%;display:flex;align-items:center;justify-content:center;
                      font-size:22px;flex-shrink:0;box-shadow:0 2px 8px rgba(107,33,168,0.3);">🤖</div>
                  <div style="background:#FFFFFF;border:1px solid #DDD8F0;border-radius:4px 16px 16px 16px;
                      padding:16px 20px;max-width:90%;box-shadow:0 2px 8px rgba(107,33,168,0.07);">
                    <div style="font-weight:700;color:#6B21A8;margin-bottom:8px;font-size:15px;">🔮 Salve, Bruxo! 🧙‍♂️</div>
                    <div style="font-size:14px;color:#1A1225;line-height:1.7;">
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
                      <div style="background:linear-gradient(135deg,#6B21A8,#4C1D95);color:#fff;
                          border-radius:16px 16px 4px 16px;padding:12px 18px;max-width:75%;
                          font-size:14px;line-height:1.5;box-shadow:0 2px 8px rgba(107,33,168,0.25);">
                        {msg["content"]}
                      </div>
                      <div style="width:36px;height:36px;background:#DDD8F0;border-radius:50%;
                          display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">🧙‍♂️</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    content = msg["content"].replace(chr(10), "<br>")
                    st.markdown(f"""
                    <div style="display:flex;align-items:flex-start;gap:12px;margin:12px 0;">
                      <div style="width:44px;height:44px;background:linear-gradient(135deg,#6B21A8,#4C1D95);
                          border-radius:50%;display:flex;align-items:center;justify-content:center;
                          font-size:22px;flex-shrink:0;box-shadow:0 2px 8px rgba(107,33,168,0.3);">🤖</div>
                      <div style="background:#FFFFFF;border:1px solid #DDD8F0;border-radius:4px 16px 16px 16px;
                          padding:16px 20px;max-width:85%;font-size:14px;line-height:1.7;color:#1A1225;
                          box-shadow:0 2px 8px rgba(107,33,168,0.07);">
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

            now_ts = pd.Timestamp.now()
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
                    urgentes["dias"] = (urgentes["Prazo"] - now_ts).dt.days
                    urgentes = urgentes.sort_values("dias")

                    if any(w in q for w in ["risco", "atraso", "urgente", "critico"]):
                        top = urgentes.head(5)
                        linhas = ""
                        for _, r in top.iterrows():
                            d = int((r["Prazo"] - now_ts).days)
                            emoji = "🔴" if d < 7 else "🟡" if d < 30 else "🟢"
                            linhas += f"\n{emoji} **{r['Projeto']}** — {d} dias ({r['Prazo'].strftime('%d/%m/%Y')})"
                        answer = f"**⚠️ Bruxo, esses sao os projetos em maior risco:**\n{linhas}\n\n💡 Os marcados em 🔴 precisam de atencao AGORA."

                    elif any(w in q for w in ["focar", "energia", "semana", "prioridade", "foco"]):
                        top = urgentes.head(3)
                        linhas = ""
                        for _, r in top.iterrows():
                            d = int((r["Prazo"] - now_ts).days)
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

💡 Proximo prazo critico: **{urgentes.iloc[0]["Projeto"] if not urgentes.empty else "N/A"}** — vence em {int(urgentes.iloc[0]["dias"]) if not urgentes.empty else 0} dias."""

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
            ("TOTAL", total, "#6B21A8"),
            ("EM EXECUCAO", em_exec, "#7C3AED"),
            ("CONCLUIDOS", concluidos, "#2F9E44"),
            ("BACKLOG", backlog, "#7048E8"),
            ("TAXA", f"{taxa}%", "#C92A2A" if taxa < 40 else "#7C3AED" if taxa < 70 else "#2F9E44"),
        ]
        for i, (label, val, cor) in enumerate(kpis):
            cols[i].markdown(f"""
            <div style="background:#FFFFFF;border:1px solid #DDD8F0;
                border-radius:14px;padding:20px 18px;
                border-top:3px solid {cor};box-shadow:0 2px 8px rgba(107,33,168,0.07);">
              <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9588AA;margin-bottom:8px;">{label}</div>
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
            <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#6B21A8;margin-bottom:16px;">
            &#9670; PROJETOS ATIVOS — CARDS COMPLETOS
            </div>
            """, unsafe_allow_html=True)

            ativos = df_vg[df_vg["Status"].isin(["A Iniciar", "Em Andamento"])].copy()
            ativos = ativos.sort_values("Prazo")

            if not ativos.empty:
                for _, r in ativos.iterrows():
                    dias = (r["Prazo"] - pd.Timestamp.now()).days
                    cor = "#C92A2A" if dias < 7 else "#7C3AED" if dias < 30 else "#2F9E44"
                    label = "URGENTE" if dias < 7 else "ATENCAO" if dias < 30 else "OK"
                    foco = str(r.get("Foco", "")) if pd.notna(r.get("Foco")) else "—"
                    escopo = str(r.get("Escopo", "")) if pd.notna(r.get("Escopo")) else "—"
                    detalhamento = str(r.get("Detalhamento", "")) if pd.notna(r.get("Detalhamento")) else ""
                    resultado = str(r.get("Resultado Esperado", "")) if pd.notna(r.get("Resultado Esperado")) else ""
                    status_cor = STATUS_COLORS.get(r.get("Status",""), "#6B21A8")
                    data_ini = r["Data Inicial"].strftime("%d/%m/%Y") if pd.notna(r.get("Data Inicial")) else "—"

                    st.markdown(f"""
                    <div style="background:#FFFFFF;border:1px solid #DDD8F0;
                        border-left:4px solid {cor};border-radius:12px;padding:16px;margin-bottom:12px;
                        box-shadow:0 2px 8px rgba(107,33,168,0.07);">
                      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
                        <div style="font-weight:700;font-size:15px;color:#1A1225;flex:1;">{r['Projeto']}</div>
                        <div style="display:flex;gap:6px;flex-shrink:0;margin-left:8px;">
                          <span style="background:{status_cor}22;color:{status_cor};border:1px solid {status_cor}44;
                              padding:2px 8px;border-radius:20px;font-size:10px;font-family:'JetBrains Mono',monospace;">{r.get('Status','')}</span>
                          <span style="background:{cor};color:#fff;padding:3px 10px;border-radius:20px;
                              font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;">{dias}d · {label}</span>
                        </div>
                      </div>
                      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:10px;">
                        <div style="background:#F6F5FA;border-radius:8px;padding:8px 10px;">
                          <div style="font-size:9px;color:#9588AA;letter-spacing:1px;margin-bottom:3px;">FOCO</div>
                          <div style="font-size:12px;color:#1A1225;font-weight:500;">{foco}</div>
                        </div>
                        <div style="background:#F6F5FA;border-radius:8px;padding:8px 10px;">
                          <div style="font-size:9px;color:#9588AA;letter-spacing:1px;margin-bottom:3px;">INICIO</div>
                          <div style="font-size:12px;color:#1A1225;font-weight:500;">{data_ini}</div>
                        </div>
                        <div style="background:{cor}11;border-radius:8px;padding:8px 10px;border:1px solid {cor}33;">
                          <div style="font-size:9px;color:#9588AA;letter-spacing:1px;margin-bottom:3px;">PRAZO</div>
                          <div style="font-size:12px;color:{cor};font-weight:700;">{r['Prazo'].strftime('%d/%m/%Y')}</div>
                        </div>
                      </div>
                      <div style="background:#F6F5FA;border-radius:8px;padding:10px 12px;margin-bottom:6px;">
                        <div style="font-size:9px;color:#9588AA;letter-spacing:1px;margin-bottom:4px;">ESCOPO</div>
                        <div style="font-size:13px;color:#1A1225;line-height:1.5;">{escopo}</div>
                      </div>
                      {"<div style='background:#F6F5FA;border-radius:8px;padding:10px 12px;margin-bottom:6px;'><div style='font-size:9px;color:#9588AA;letter-spacing:1px;margin-bottom:4px;'>DETALHAMENTO</div><div style='font-size:13px;color:#1A1225;line-height:1.5;'>"+detalhamento+"</div></div>" if detalhamento and detalhamento != "—" else ""}
                      {"<div style='background:#6B21A811;border:1px solid #6B21A833;border-radius:8px;padding:10px 12px;'><div style='font-size:9px;color:#6B21A8;letter-spacing:1px;margin-bottom:4px;'>RESULTADO ESPERADO</div><div style='font-size:13px;color:#1A1225;line-height:1.5;'>"+resultado+"</div></div>" if resultado and resultado != "—" else ""}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhum projeto ativo encontrado com os filtros atuais.")

        with col_b:
            st.markdown("""
            <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#6B21A8;margin-bottom:16px;">
            &#9670; DISTRIBUICAO
            </div>
            """, unsafe_allow_html=True)

            dist = df["Status"].value_counts().reindex(STATUS_OPCOES, fill_value=0)
            for status, count in dist.items():
                if count == 0:
                    continue
                pct = count / total * 100
                cor = STATUS_COLORS.get(status, "#6B21A8")
                st.markdown(f"""
                <div style="margin-bottom:12px;">
                  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-size:12px;color:#5B4E72;font-weight:500;">{status}</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:12px;color:{cor};font-weight:700;">{count}</span>
                  </div>
                  <div style="background:#DDD8F0;border-radius:4px;height:6px;overflow:hidden;">
                    <div style="background:{cor};width:{pct:.0f}%;height:100%;border-radius:4px;box-shadow:0 0 8px {cor}88;"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 3 — KANBAN
# ─────────────────────────────────────────────
with tab3:
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#6B21A8;margin-bottom:20px;">
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
            cor = STATUS_COLORS.get(status, "#6B21A8")
            projetos = df_kb[df_kb["Status"] == status]
            count = len(projetos)

            with cols[i]:
                st.markdown(f"""
                <div style="background:#FFFFFF;border:1px solid #DDD8F0;
                    border-top:2px solid {cor};box-shadow:0 1px 4px rgba(107,33,168,0.07);border-radius:12px;padding:12px 14px;margin-bottom:12px;
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
                    cor_prazo = "#C92A2A" if dias < 7 else "#7C3AED" if dias < 30 else "#2F9E44"
                    st.markdown(f"""
                    <div style="background:#FFFFFF;border:1px solid #DDD8F0;
                        border-left:3px solid {cor};border-radius:10px;padding:12px;margin-bottom:8px;
                        box-shadow:0 1px 4px rgba(107,33,168,0.06);">
                      <div style="font-weight:600;font-size:13px;color:#1A1225;margin-bottom:6px;line-height:1.3;">{row['Projeto']}</div>
                      {"<div style='font-size:11px;color:#5B4E72;margin-bottom:4px;'>🎯 "+foco+"</div>" if foco else ""}
                      {"<div style='font-size:11px;color:#5B4E72;margin-bottom:4px;'>📋 "+escopo+"</div>" if escopo else ""}
                      <div style="display:flex;justify-content:space-between;margin-top:6px;">
                        <span style="font-size:10px;color:#9588AA;">📅 {data_str}</span>
                        <span style="font-size:10px;color:{cor_prazo};font-weight:600;">⏰ {prazo_str}</span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 4 — DADOS
# ─────────────────────────────────────────────
with tab4:
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#6B21A8;margin-bottom:16px;">
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

        st.markdown(f"<div style='font-size:12px;color:#9588AA;margin-bottom:8px;'>{len(df_d)} projetos encontrados</div>", unsafe_allow_html=True)
        st.dataframe(df_d, use_container_width=True, height=500)

# ─────────────────────────────────────────────
# TAB 5 — MAPEAMENTO GS
# ─────────────────────────────────────────────
with tab5:
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#6B21A8;margin-bottom:20px;">
    &#9670; MAPEAMENTO GEOGRAFICO DE PROJETOS
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.warning("Sem dados carregados.")
    else:
        ESTADOS_COORDS = {
            "AC": (-9.0238, -70.812, "Acre"),
            "AL": (-9.5713, -36.782, "Alagoas"),
            "AP": (1.4102, -51.770, "Amapa"),
            "AM": (-3.4168, -65.856, "Amazonas"),
            "BA": (-12.9718, -38.501, "Bahia"),
            "CE": (-3.7172, -38.543, "Ceara"),
            "DF": (-15.7801, -47.929, "Distrito Federal"),
            "ES": (-19.1834, -40.308, "Espirito Santo"),
            "GO": (-16.6864, -49.264, "Goias"),
            "MA": (-2.5297, -44.302, "Maranhao"),
            "MT": (-12.6819, -56.921, "Mato Grosso"),
            "MS": (-20.7722, -54.785, "Mato Grosso do Sul"),
            "MG": (-18.5122, -44.555, "Minas Gerais"),
            "PA": (-1.9981, -54.930, "Para"),
            "PB": (-7.2399, -36.782, "Paraiba"),
            "PR": (-24.8950, -51.551, "Parana"),
            "PE": (-8.8137, -36.954, "Pernambuco"),
            "PI": (-6.6077, -42.285, "Piaui"),
            "RJ": (-22.9068, -43.172, "Rio de Janeiro"),
            "RN": (-5.7945, -36.341, "Rio Grande do Norte"),
            "RS": (-30.0346, -51.217, "Rio Grande do Sul"),
            "RO": (-11.5057, -63.580, "Rondonia"),
            "RR": (2.7376, -62.075, "Roraima"),
            "SC": (-27.5954, -48.548, "Santa Catarina"),
            "SP": (-23.5505, -46.633, "Sao Paulo"),
            "SE": (-10.9472, -37.073, "Sergipe"),
            "TO": (-10.1753, -48.298, "Tocantins"),
        }

        CIDADE_ESTADO = {
            "ponta negra": "RN", "natal": "RN", "mossoro": "RN", "caico": "RN",
            "fortaleza": "CE", "caucaia": "CE", "juazeiro": "CE", "sobral": "CE",
            "recife": "PE", "olinda": "PE", "caruaru": "PE", "madalena": "PE", "piedade": "PE",
            "joao pessoa": "PB", "campina grande": "PB", "paraiba": "PB",
            "salvador": "BA", "feira de santana": "BA", "vitoria da conquista": "BA",
            "sao paulo": "SP", "campinas": "SP", "santos": "SP", "sorocaba": "SP",
            "rio de janeiro": "RJ", "niteroi": "RJ", "duque de caxias": "RJ",
            "belo horizonte": "MG", "uberlandia": "MG", "contagem": "MG",
            "brasilia": "DF", "taguatinga": "DF",
            "manaus": "AM", "parintins": "AM",
            "belem": "PA", "santarem": "PA",
            "porto alegre": "RS", "caxias do sul": "RS", "pelotas": "RS",
            "curitiba": "PR", "londrina": "PR", "maringa": "PR",
            "goiania": "GO", "anapolis": "GO",
            "florianopolis": "SC", "joinville": "SC", "blumenau": "SC",
            "cuiaba": "MT", "sinop": "MT",
            "campo grande": "MS", "dourados": "MS",
            "macapa": "AP", "porto velho": "RO", "rio branco": "AC",
            "boa vista": "RR", "palmas": "TO", "macaiba": "RN",
            "jaboatao": "PE", "jaboatao dos guararapes": "PE",
        }

        def extrair_estado(nome_projeto):
            if not isinstance(nome_projeto, str):
                return None
            nome_lower = nome_projeto.lower()
            import re
            match = re.search(r'/\s*([A-Z]{2})', nome_projeto)
            if match:
                uf = match.group(1)
                if uf in ESTADOS_COORDS:
                    return uf
            for cidade, uf in CIDADE_ESTADO.items():
                if cidade in nome_lower:
                    return uf
            return None

        df_mapa = df.copy()
        df_mapa["UF"] = df_mapa["Projeto"].apply(extrair_estado)
        df_mapa = df_mapa.dropna(subset=["UF"])

        if df_mapa.empty:
            st.warning("Nenhum projeto com localizacao identificada. Certifique-se que os projetos tem formato 'Cidade/UF - Cliente'.")
        else:
            resumo_estados = df_mapa.groupby("UF").agg(
                total=("Projeto", "count"),
                projetos=("Projeto", lambda x: list(x))
            ).reset_index()

            if "estado_selecionado" not in st.session_state:
                st.session_state.estado_selecionado = None
            if "projeto_chat_mapa" not in st.session_state:
                st.session_state.projeto_chat_mapa = None
            if "chat_mapa_history" not in st.session_state:
                st.session_state.chat_mapa_history = []

            col_mapa, col_info = st.columns([1.6, 1])

            with col_mapa:
                map_data = []
                for _, row in resumo_estados.iterrows():
                    uf = row["UF"]
                    if uf in ESTADOS_COORDS:
                        lat, lon, nome = ESTADOS_COORDS[uf]
                        map_data.append({
                            "uf": uf, "nome": nome,
                            "lat": lat, "lon": lon,
                            "total": int(row["total"])
                        })

                map_markers = ""
                for m in map_data:
                    cor_marker = "#C92A2A" if m["total"] >= 5 else "#7C3AED" if m["total"] >= 3 else "#6B21A8"
                    radius = 15 + m["total"] * 5
                    map_markers += f"""
                    L.circleMarker([{m['lat']}, {m['lon']}], {{
                        radius: {radius},
                        fillColor: '{cor_marker}',
                        color: '#fff',
                        weight: 2,
                        opacity: 1,
                        fillOpacity: 0.85
                    }}).addTo(map)
                    .bindPopup('<b>{m["nome"]} ({m["uf"]})</b><br>{m["total"]} projeto(s)')
                    .on('click', function() {{
                        window.parent.postMessage({{type:'estado_click', uf:'{m["uf"]}', nome:'{m["nome"]}'}}, '*');
                    }});
                    L.marker([{m['lat']}, {m['lon']}], {{
                        icon: L.divIcon({{
                            html: '<div style="background:transparent;color:#fff;font-weight:800;font-size:11px;text-align:center;margin-top:-4px;">{m["total"]}</div>',
                            iconSize: [20, 20],
                            iconAnchor: [10, 10]
                        }})
                    }}).addTo(map);
                    """

                mapa_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  body {{ margin: 0; padding: 0; background: #F6F5FA; }}
  #map {{ width: 100%; height: 520px; border-radius: 16px; }}
  .leaflet-popup-content-wrapper {{ border-radius: 10px; font-family: 'Inter', sans-serif; }}
  .info-box {{
    position: absolute; bottom: 20px; left: 20px; z-index: 1000;
    background: rgba(255,255,255,0.95); border: 1px solid #DDD8F0;
    border-radius: 12px; padding: 12px 16px;
    font-family: monospace; font-size: 11px; color: #6B21A8;
  }}
</style>
</head>
<body>
<div id="map"></div>
<div class="info-box">&#9670; {len(df_mapa)} projetos mapeados em {len(map_data)} estados</div>
<script>
  var map = L.map('map', {{ zoomControl: true, scrollWheelZoom: true }})
    .setView([-14.235, -51.925], 4);

  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
    attribution: '&copy; OpenStreetMap &copy; CARTO',
    subdomains: 'abcd', maxZoom: 19
  }}).addTo(map);

  {map_markers}

  map.on('popupopen', function(e) {{
    map.flyTo(e.popup.getLatLng(), 7, {{ animate: true, duration: 1.2 }});
  }});

  // Sobrevoo automático em loop contínuo
  var _pts = [];
  map.eachLayer(function(l){{ if(l.getLatLng) _pts.push(l.getLatLng()); }});
  var _i=0;
  function _fly(){{
    if(_pts.length<2) return;
    var pt=_pts[_i%_pts.length];
    map.flyTo(pt, 6, {{animate:true,duration:3}});
    _i++;
    setTimeout(_fly, 5500);
  }}
  setTimeout(_fly, 3000);
</script>
</body>
</html>
                """

                components.html(mapa_html, height=540)

            with col_info:
                estados_disponiveis = sorted(resumo_estados["UF"].tolist())
                estado_sel = st.selectbox(
                    "🗺️ Selecione o Estado",
                    options=["Todos"] + estados_disponiveis,
                    format_func=lambda x: f"{x} — {ESTADOS_COORDS[x][2]}" if x != "Todos" and x in ESTADOS_COORDS else x,
                    key="estado_sel"
                )

                if estado_sel == "Todos":
                    df_estado = df_mapa.copy()
                    titulo_estado = "Todos os Estados"
                else:
                    df_estado = df_mapa[df_mapa["UF"] == estado_sel].copy()
                    nome_estado = ESTADOS_COORDS.get(estado_sel, ("","",""))[2]
                    titulo_estado = f"{nome_estado} ({estado_sel})"

                st.markdown(f"""
                <div style="background:#6B21A8;color:#fff;border-radius:10px;padding:10px 14px;margin-bottom:12px;text-align:center;">
                  <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;opacity:0.8;">PROJETOS</div>
                  <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;">{len(df_estado)}</div>
                  <div style="font-size:11px;opacity:0.9;">{titulo_estado}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9588AA;margin-bottom:8px;">
                PROJETOS NO ESTADO
                </div>
                """, unsafe_allow_html=True)

                projeto_selecionado = None
                for idx, row in df_estado.sort_values("Prazo").iterrows():
                    dias = (row["Prazo"] - pd.Timestamp.now()).days
                    cor = "#C92A2A" if dias < 7 else "#7C3AED" if dias < 30 else "#2F9E44"
                    status_cor = STATUS_COLORS.get(row.get("Status",""), "#6B21A8")
                    if st.button(
                        f"{'🔴' if dias < 7 else '🟡' if dias < 30 else '🟢'} {row['Projeto'][:35]}",
                        key=f"proj_mapa_{idx}",
                        use_container_width=True
                    ):
                        st.session_state.projeto_chat_mapa = row.to_dict()
                        st.session_state.chat_mapa_history = []

                if st.session_state.projeto_chat_mapa:
                    proj = st.session_state.projeto_chat_mapa
                    dias_p = (pd.Timestamp(proj["Prazo"]) - pd.Timestamp.now()).days
                    cor_p = "#C92A2A" if dias_p < 7 else "#7C3AED" if dias_p < 30 else "#2F9E44"

                    st.markdown(f"""
                    <div style="background:#FFFFFF;border:1px solid #DDD8F0;border-left:4px solid {cor_p};
                        border-radius:12px;padding:14px;margin-top:12px;">
                      <div style="font-weight:700;color:#1A1225;font-size:13px;margin-bottom:8px;">{proj.get('Projeto','')}</div>
                      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;">
                        <div style="background:#F6F5FA;border-radius:6px;padding:6px 8px;">
                          <div style="font-size:8px;color:#9588AA;">STATUS</div>
                          <div style="font-size:11px;color:#6B21A8;font-weight:600;">{proj.get('Status','')}</div>
                        </div>
                        <div style="background:{cor_p}11;border-radius:6px;padding:6px 8px;">
                          <div style="font-size:8px;color:#9588AA;">PRAZO</div>
                          <div style="font-size:11px;color:{cor_p};font-weight:700;">{pd.Timestamp(proj['Prazo']).strftime('%d/%m/%Y')} ({dias_p}d)</div>
                        </div>
                      </div>
                      <div style="font-size:11px;color:#5B4E72;line-height:1.5;">
                        🎯 {proj.get('Foco','')}<br>
                        📋 {proj.get('Escopo','') or '—'}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("""
                    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#6B21A8;margin-bottom:6px;">
                    🤖 JARVIS — PERGUNTE SOBRE ESTE PROJETO
                    </div>
                    """, unsafe_allow_html=True)

                    for msg in st.session_state.chat_mapa_history:
                        if msg["role"] == "user":
                            st.markdown(f"""
                            <div style="display:flex;justify-content:flex-end;margin:6px 0;">
                              <div style="background:linear-gradient(135deg,#6B21A8,#4C1D95);color:#fff;
                                  border-radius:12px 12px 3px 12px;padding:8px 12px;max-width:85%;font-size:13px;">
                                {msg['content']}
                              </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background:#F6F5FA;border:1px solid #DDD8F0;border-radius:3px 12px 12px 12px;
                                padding:10px 12px;font-size:13px;color:#1A1225;line-height:1.6;margin:6px 0;">
                              🤖 {msg['content'].replace(chr(10), '<br>')}
                            </div>
                            """, unsafe_allow_html=True)

                    chat_m_input = st.text_input(
                        "chat_mapa_in",
                        placeholder="Pergunta sobre este projeto...",
                        label_visibility="collapsed",
                        key="chat_mapa_input"
                    )
                    if st.button("Perguntar", use_container_width=True, key="btn_chat_mapa"):
                        if chat_m_input:
                            st.session_state.chat_mapa_history.append({"role": "user", "content": chat_m_input})
                            q_m = chat_m_input.lower()
                            p = st.session_state.projeto_chat_mapa
                            dias_resp = (pd.Timestamp(p["Prazo"]) - pd.Timestamp.now()).days
                            cor_r = "🔴 URGENTE" if dias_resp < 7 else "🟡 ATENCAO" if dias_resp < 30 else "🟢 OK"

                            if any(w in q_m for w in ["prazo", "quando", "vence", "data"]):
                                resp = f"Prazo: **{pd.Timestamp(p['Prazo']).strftime('%d/%m/%Y')}** — {dias_resp} dias restantes. Status: {cor_r}"
                            elif any(w in q_m for w in ["escopo", "o que", "trata"]):
                                resp = f"**Escopo:** {p.get('Escopo','—')}\n\n**Detalhamento:** {p.get('Detalhamento','—')}"
                            elif any(w in q_m for w in ["resultado", "entrega", "objetivo"]):
                                resp = f"**Resultado Esperado:** {p.get('Resultado Esperado','—')}"
                            elif any(w in q_m for w in ["status", "situacao", "como"]):
                                resp = f"Status atual: **{p.get('Status','—')}**\nFoco: **{p.get('Foco','—')}**\nDias restantes: **{dias_resp}d** ({cor_r})"
                            elif any(w in q_m for w in ["foco", "prioridade"]):
                                resp = f"Foco: **{p.get('Foco','—')}**"
                            else:
                                resp = f"""**{p.get('Projeto','')}**
Status: {p.get('Status','—')} | Foco: {p.get('Foco','—')}
Prazo: {pd.Timestamp(p['Prazo']).strftime('%d/%m/%Y')} ({dias_resp}d) {cor_r}
Escopo: {p.get('Escopo','—')}"""
                            st.session_state.chat_mapa_history.append({"role": "assistant", "content": resp})
                            st.rerun()

# ─────────────────────────────────────────────
# TAB 6 — NOTAS
# ─────────────────────────────────────────────
with tab6:
    if st.session_state.is_convidado:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;">
          <div style="font-size:52px;margin-bottom:16px;">🔒</div>
          <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#6B21A8;margin-bottom:8px;">
            Acesso Restrito</div>
          <div style="font-size:14px;color:#5B4E72;">
            Notas disponíveis apenas para Gabriel.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;color:#6B21A8;margin-bottom:16px;">
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
        <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1px;color:#9588AA;margin-top:8px;text-align:right;">
        Notas sao locais e nao sao salvas entre sessoes
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# TAB 7 — CALENDÁRIO
# ─────────────────────────────────────────────
with tab7:
    if df.empty:
        st.warning("Sem dados carregados.")
    else:
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            filtro_nome_cal = st.text_input("🔍 Buscar", placeholder="Nome do projeto...", key="cal_nome")
        with fc2:
            filtro_status_cal = st.multiselect("Status", STATUS_OPCOES, default=[], key="cal_status", placeholder="Todos")
        with fc3:
            filtro_mes_cal = st.selectbox("Mês", ["Todos","Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"], key="cal_mes")

        df_cal = df.copy()
        if filtro_nome_cal:
            df_cal = df_cal[df_cal["Projeto"].str.contains(filtro_nome_cal, case=False, na=False)]
        if filtro_status_cal:
            df_cal = df_cal[df_cal["Status"].isin(filtro_status_cal)]
        if filtro_mes_cal != "Todos":
            mes_num = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                       "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"].index(filtro_mes_cal) + 1
            df_cal = df_cal[df_cal["Data Inicial"].dt.month == mes_num]

        import json as _json
        eventos = []
        for _, row in df_cal.iterrows():
            cor = STATUS_COLORS.get(row.get("Status",""), "#6B21A8")
            eventos.append({
                "nome": str(row["Projeto"])[:45],
                "inicio": row["Data Inicial"].strftime("%Y-%m-%d"),
                "fim": row["Prazo"].strftime("%Y-%m-%d"),
                "status": str(row.get("Status","")),
                "foco": str(row.get("Foco",""))[:40] if pd.notna(row.get("Foco")) else "",
                "cor": cor,
                "dias": int((row["Prazo"] - pd.Timestamp.now()).days)
            })

        eventos_json = _json.dumps(eventos, ensure_ascii=False)
        status_colors_json = _json.dumps(STATUS_COLORS)

        CAL_HTML = f"""<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#F6F5FA;font-family:'Inter',sans-serif;color:#1A1225;padding:0 0 20px;}}

/* Nav */
.nav{{
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 20px;background:#fff;
  border:1px solid #DDD8F0;border-radius:14px;
  margin-bottom:14px;
  box-shadow:0 1px 6px rgba(107,33,168,.07);
}}
.nav-title{{font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:#6B21A8;}}
.nav-sub{{font-size:11px;color:#9588AA;font-family:'JetBrains Mono',monospace;letter-spacing:1px;}}
.nav-right{{display:flex;gap:8px;align-items:center;}}
.nbtn{{
  width:36px;height:36px;border-radius:50%;
  border:1px solid #DDD8F0;background:#fff;
  cursor:pointer;font-size:18px;color:#6B21A8;
  display:flex;align-items:center;justify-content:center;
  transition:all .18s;
}}
.nbtn:hover{{background:#6B21A8;color:#fff;border-color:#6B21A8;}}
.ntod{{
  padding:7px 16px;border-radius:8px;
  border:1px solid #6B21A8;background:transparent;
  color:#6B21A8;font-size:12px;font-weight:600;
  cursor:pointer;transition:all .18s;font-family:'Inter',sans-serif;
}}
.ntod:hover{{background:#6B21A8;color:#fff;}}

/* Grade */
.grid{{
  display:grid;grid-template-columns:repeat(7,1fr);
  gap:1px;background:#E8E4F4;
  border-radius:14px;overflow:hidden;
  border:1px solid #DDD8F0;
  box-shadow:0 2px 12px rgba(107,33,168,.08);
}}
.dh{{
  background:#EFECF8;padding:10px 4px;text-align:center;
  font-family:'JetBrains Mono',monospace;font-size:10px;
  font-weight:600;letter-spacing:1.5px;color:#6B21A8;
}}
.dc{{
  background:#fff;min-height:96px;padding:5px 4px;
  transition:background .12s;position:relative;
  overflow:hidden;
}}
.dc.om{{background:#FAFAFA;}}
.dc.tod .dn{{
  background:#6B21A8;color:#fff;border-radius:50%;
  width:24px;height:24px;display:flex;align-items:center;
  justify-content:center;font-weight:700;
}}
.dn{{font-size:12px;font-weight:600;color:#1A1225;display:inline-flex;
    width:24px;height:24px;align-items:center;justify-content:center;
    margin-bottom:3px;}}
.dc.om .dn{{color:#C4BCDF;}}

/* Evento — só nome, sem poluição */
.ev{{
  border-radius:4px;padding:2px 6px 2px 8px;
  font-size:11px;font-weight:600;
  margin-bottom:2px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  cursor:pointer;transition:opacity .15s, filter .15s;
  line-height:1.5;
  position:relative;
}}
.ev:hover{{opacity:.85;filter:brightness(1.05);}}
.ev.is-start{{border-left:3px solid rgba(0,0,0,.2)!important;}}
.more{{font-size:10px;color:#9588AA;font-weight:500;padding:1px 4px;cursor:pointer;}}
.more:hover{{color:#6B21A8;}}

/* Tooltip card — cinza limpo */
#tt{{
  position:fixed;
  background:#1C1828;
  border:1px solid rgba(255,255,255,.08);
  border-radius:14px;
  padding:16px 18px;
  width:248px;
  box-shadow:0 12px 40px rgba(0,0,0,.4);
  z-index:9999;
  display:none;
  pointer-events:none;
}}
#tt.show{{display:block;animation:ttIn .15s ease;}}
@keyframes ttIn{{from{{opacity:0;transform:translateY(6px);}}to{{opacity:1;transform:translateY(0);}}}}
.tt-nome{{font-weight:700;font-size:14px;color:#fff;margin-bottom:10px;line-height:1.4;}}
.tt-badge{{
  display:inline-flex;align-items:center;padding:3px 10px;
  border-radius:20px;font-size:10px;font-weight:700;
  font-family:'JetBrains Mono',monospace;letter-spacing:.5px;
  margin-bottom:10px;
}}
.tt-row{{
  display:flex;align-items:flex-start;gap:8px;
  font-size:12px;color:rgba(255,255,255,.6);
  margin-bottom:6px;line-height:1.4;
}}
.tt-row .lbl{{color:rgba(255,255,255,.35);font-size:10px;
  font-family:'JetBrains Mono',monospace;letter-spacing:.5px;
  min-width:40px;margin-top:1px;}}
.tt-row .val{{color:rgba(255,255,255,.85);font-size:12px;}}
.tt-dias{{
  margin-top:8px;padding:8px 10px;border-radius:8px;
  background:rgba(255,255,255,.05);
  font-size:12px;font-weight:600;text-align:center;
}}

/* Legenda */
.leg{{
  display:flex;flex-wrap:wrap;gap:8px;
  margin-top:14px;padding:12px 16px;
  background:#fff;border:1px solid #DDD8F0;border-radius:10px;
}}
.li{{display:flex;align-items:center;gap:6px;font-size:11px;color:#5B4E72;}}
.ld{{width:10px;height:10px;border-radius:3px;flex-shrink:0;}}

@media(max-width:600px){{
  .dc{{min-height:64px;padding:3px 2px;}}
  .dn{{font-size:10px;width:20px;height:20px;}}
  .ev{{font-size:9px;padding:1px 4px;}}
  .nav-title{{font-size:18px;}}
  #tt{{width:200px;font-size:11px;}}
}}
</style></head><body>

<div class="nav">
  <div>
    <div class="nav-title" id="nav-title"></div>
    <div class="nav-sub" id="nav-sub"></div>
  </div>
  <div class="nav-right">
    <button class="ntod" onclick="goToday()">Hoje</button>
    <button class="nbtn" onclick="chM(-1)">&#8249;</button>
    <button class="nbtn" onclick="chM(1)">&#8250;</button>
  </div>
</div>

<div class="grid" id="grid"></div>
<div class="leg" id="leg"></div>
<div id="tt"></div>

<script>
const EVS={eventos_json};
const SC={status_colors_json};
const DS=['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'];
const MS=['Janeiro','Fevereiro','Março','Abril','Maio','Junho',
          'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];

const hoje=new Date();
let Y=hoje.getFullYear(), M=hoje.getMonth();

function pd(s){{return new Date(s+'T00:00:00');}}
function sd(a,b){{return a.getFullYear()===b.getFullYear()&&a.getMonth()===b.getMonth()&&a.getDate()===b.getDate();}}

function evDay(y,m,d){{
  const dt=new Date(y,m,d);
  return EVS.filter(e=>{{const i=pd(e.inicio),f=pd(e.fim);return dt>=i&&dt<=f;}});
}}

function render(){{
  const g=document.getElementById('grid');
  g.innerHTML='';
  DS.forEach(d=>{{const h=document.createElement('div');h.className='dh';h.textContent=d;g.appendChild(h);}});
  document.getElementById('nav-title').textContent=MS[M]+' '+Y;
  const cnt=evDay(Y,M,1).length + evDay(Y,M,15).length;
  document.getElementById('nav-sub').textContent=EVS.length+' projetos no portfólio';

  const fd=new Date(Y,M,1).getDay();
  const dim=new Date(Y,M+1,0).getDate();
  const dip=new Date(Y,M,0).getDate();
  const tot=Math.ceil((fd+dim)/7)*7;

  for(let i=0;i<tot;i++){{
    const cell=document.createElement('div');
    cell.className='dc';
    let day,mo=M,yr=Y,om=false;
    if(i<fd){{day=dip-fd+i+1;mo=M-1;yr=Y;if(mo<0){{mo=11;yr--;}}om=true;}}
    else if(i>=fd+dim){{day=i-fd-dim+1;mo=M+1;yr=Y;if(mo>11){{mo=0;yr++;}}om=true;}}
    else{{day=i-fd+1;}}
    if(om)cell.classList.add('om');
    const isT=!om&&sd(new Date(yr,mo,day),hoje);
    if(isT)cell.classList.add('tod');
    const dn=document.createElement('div');dn.className='dn';dn.textContent=day;cell.appendChild(dn);
    if(!om){{
      const evs=evDay(yr,mo,day);
      if(evs.length)cell.style.background='#FDFCFF';
      evs.slice(0,3).forEach(e=>{{
        const div=document.createElement('div');
        div.className='ev'+(sd(pd(e.inicio),new Date(yr,mo,day))?' is-start':'');
        div.style.background=e.cor+'20';
        div.style.color=e.cor;
        div.style.borderLeft=sd(pd(e.inicio),new Date(yr,mo,day))?'3px solid '+e.cor:'3px solid transparent';
        div.textContent=e.nome;
        div.onmouseenter=function(ev){{showTT(e,ev);}};
        div.onmouseleave=hideTT;
        cell.appendChild(div);
      }});
      if(evs.length>3){{const m=document.createElement('div');m.className='more';m.textContent='+' +(evs.length-3)+' mais';cell.appendChild(m);}}
    }}
    g.appendChild(cell);
  }}
  renderLeg();
}}

function renderLeg(){{
  const l=document.getElementById('leg');l.innerHTML='';
  const seen={{}};
  EVS.forEach(e=>{{if(!seen[e.status]){{seen[e.status]=1;
    const item=document.createElement('div');item.className='li';
    item.innerHTML=`<div class="ld" style="background:${{e.cor}}"></div><span>${{e.status}}</span>`;
    l.appendChild(item);}}}});
}}

function showTT(e,ev){{
  const tt=document.getElementById('tt');
  const d=e.dias;
  const dc=d<0?'#F87171':d<7?'#F59E0B':'#10B981';
  const dtxt=d<0?Math.abs(d)+' dias em atraso':d===0?'Vence hoje':d+' dias restantes';
  tt.innerHTML=`
    <div class="tt-nome">${{e.nome}}</div>
    <span class="tt-badge" style="background:${{e.cor}}22;color:${{e.cor}};border:1px solid ${{e.cor}}44">${{e.status}}</span>
    <div class="tt-row"><span class="lbl">INÍCIO</span><span class="val">${{fmtD(e.inicio)}}</span></div>
    <div class="tt-row"><span class="lbl">PRAZO</span><span class="val">${{fmtD(e.fim)}}</span></div>
    ${{e.foco?`<div class="tt-row"><span class="lbl">FOCO</span><span class="val">${{e.foco}}</span></div>`:''}}
    <div class="tt-dias" style="color:${{dc}}">${{dtxt}}</div>
  `;
  tt.classList.add('show');
  positionTT(ev);
}}

function positionTT(ev){{
  const tt=document.getElementById('tt');
  const x=Math.min(ev.clientX+14, window.innerWidth-262);
  const y=Math.min(ev.clientY+14, window.innerHeight-240);
  tt.style.left=x+'px'; tt.style.top=y+'px';
}}

function hideTT(){{document.getElementById('tt').classList.remove('show');}}
function fmtD(s){{const[y,m,d]=s.split('-');return d+'/'+m+'/'+y;}}
function chM(dir){{M+=dir;if(M>11){{M=0;Y++;}}if(M<0){{M=11;Y--;}}render();}}
function goToday(){{Y=hoje.getFullYear();M=hoje.getMonth();render();}}

render();
</script></body></html>"""

        components.html(CAL_HTML, height=840, scrolling=True)
