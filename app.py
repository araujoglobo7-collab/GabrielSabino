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
    --bg: #FDF6F0;
    --bg2: #FFFFFF;
    --surface: #FFFFFF;
    --surface2: #FEF0E6;
    --border: #F0D9C8;
    --border-strong: #E8C4A0;
    --accent: #E8720C;
    --accent-light: rgba(232,114,12,0.08);
    --accent-muted: rgba(232,114,12,0.15);
    --gold: #D4880A;
    --green: #2F9E44;
    --red: #C92A2A;
    --orange: #E8720C;
    --purple: #7048E8;
    --teal: #0C8599;
    --text: #1A1208;
    --text-muted: #6B5A4E;
    --text-dim: #9C8B82;
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
    .block-container { padding: 1rem 0.75rem 2rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
    .stTabs [data-baseweb="tab"] { padding: 7px 10px !important; font-size: 11px !important; }
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
    background: var(--c, #3B5BDB); border-radius: 50%;
    box-shadow: 0 0 8px var(--c, #3B5BDB);
    top: 0; left: 50%; transform: translateX(-50%) translateY(-3px);
  }
  .ring-1 .orbit-dot { --c: #3B5BDB; }
  .ring-2 .orbit-dot { --c: #D4880A; }

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
        <stop offset="60%" stop-color="#D4880A"/>
        <stop offset="100%" stop-color="#6B5020"/>
      </radialGradient>
      <radialGradient id="gCyan" cx="50%" cy="50%">
        <stop offset="0%" stop-color="#1A1D2E"/>
        <stop offset="60%" stop-color="#3B5BDB"/>
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
    <ellipse cx="200" cy="490" rx="100" ry="7" fill="#3B5BDB" opacity="0.2" filter="url(#bigGlow)"/>

    <!-- Antenna -->
    <line x1="200" y1="38" x2="200" y2="78" stroke="#D4880A" stroke-width="2.5" stroke-linecap="round"/>
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
      <line x1="135" y1="130" x2="265" y2="130" stroke="#3B5BDB" stroke-width="0.3" opacity="0.4"/>
      <line x1="135" y1="148" x2="265" y2="148" stroke="#3B5BDB" stroke-width="0.3" opacity="0.4"/>
      <line x1="135" y1="166" x2="265" y2="166" stroke="#3B5BDB" stroke-width="0.3" opacity="0.4"/>
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
      <path d="M140 116 L152 116" stroke="#3B5BDB" stroke-width="1.5" opacity="0.5"/>
      <path d="M140 116 L140 124" stroke="#3B5BDB" stroke-width="1.5" opacity="0.5"/>
      <path d="M260 116 L248 116" stroke="#D4880A" stroke-width="1.5" opacity="0.5"/>
      <path d="M260 116 L260 124" stroke="#D4880A" stroke-width="1.5" opacity="0.5"/>
      <!-- Equalizer mouth -->
      <g transform="translate(164,210)">
        <rect class="bar b1" x="0"  y="-5"  width="6" height="10" rx="2" fill="#D4880A" opacity="0.8"/>
        <rect class="bar b2" x="9"  y="-8"  width="6" height="16" rx="2" fill="#3B5BDB"/>
        <rect class="bar b3" x="18" y="-11" width="6" height="22" rx="2" fill="#D4880A" opacity="0.8"/>
        <rect class="bar b4" x="27" y="-14" width="6" height="28" rx="2" fill="#3B5BDB"/>
        <rect class="bar b5" x="36" y="-11" width="6" height="22" rx="2" fill="#D4880A" opacity="0.8"/>
        <rect class="bar b6" x="45" y="-8"  width="6" height="16" rx="2" fill="#3B5BDB"/>
        <rect class="bar b7" x="54" y="-5"  width="6" height="10" rx="2" fill="#D4880A" opacity="0.8"/>
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
        <line x1="200" y1="304" x2="200" y2="314" stroke="#D4880A" stroke-width="2"/>
        <line x1="200" y1="366" x2="200" y2="376" stroke="#D4880A" stroke-width="2"/>
        <line x1="164" y1="340" x2="174" y2="340" stroke="#D4880A" stroke-width="2"/>
        <line x1="226" y1="340" x2="236" y2="340" stroke="#D4880A" stroke-width="2"/>
        <line x1="177" y1="317" x2="183" y2="325" stroke="rgba(99,179,237,0.6)" stroke-width="1.5"/>
        <line x1="223" y1="317" x2="217" y2="325" stroke="rgba(99,179,237,0.6)" stroke-width="1.5"/>
        <line x1="177" y1="363" x2="183" y2="355" stroke="rgba(99,179,237,0.6)" stroke-width="1.5"/>
        <line x1="223" y1="363" x2="217" y2="355" stroke="rgba(99,179,237,0.6)" stroke-width="1.5"/>
      </g>
      <!-- Side status LEDs -->
      <circle cx="128" cy="316" r="4" fill="#2F9E44" filter="url(#glow)">
        <animate attributeName="opacity" values="0.3;0.9;0.3" dur="2s" repeatCount="indefinite"/>
      </circle>
      <circle cx="272" cy="316" r="4" fill="#3B5BDB" filter="url(#glow)">
        <animate attributeName="opacity" values="0.3;0.9;0.3" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="128" cy="328" r="3" fill="#D4880A">
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

  <div class="hud">&#9670; J.A.R.V.I.S &middot; NEURAL ENGINE ONLINE &#9670;</div>
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
  c: Math.random()>0.5 ? '#3B5BDB' : '#D4880A'
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
# SESSION STATE
# ============================================================
if "logado" not in st.session_state:
    st.session_state.logado = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "df_projetos" not in st.session_state:
    st.session_state.df_projetos = None

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.logado:
    st.markdown("""
    <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 20px;
        border:1px solid #E2E4EA;border-radius:10px;
        background:#F8F9FC;backdrop-filter:blur(10px);
        margin-bottom:28px;font-family:'JetBrains Mono',monospace;font-size:10px;
        letter-spacing:2px;color:rgba(99,179,237,0.5);">
      <span>&#9670; SABINO OS &middot; v4.0</span>
      <span style="color:#2F9E44;">&#9679; SISTEMA ONLINE</span>
      <span>AES-256 ENCRYPTED</span>
    </div>
    """, unsafe_allow_html=True)

    col_bot, col_gap, col_form = st.columns([1.05, 0.05, 0.9])

    with col_bot:
        components.html(JARVIS_HTML, height=560, scrolling=False)

    with col_form:
        st.markdown("""
        <div style="padding:40px 0 24px 0;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:4px;
              color:#3B5BDB;margin-bottom:12px;">&#9679; J.A.R.V.I.S ONLINE</div>
          <div style="font-family:'Syne',sans-serif;font-size:42px;font-weight:800;
              background:linear-gradient(135deg,#D4880A 0%,#3B5BDB 100%);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              line-height:1;margin-bottom:8px;">SABINO<br>OS</div>
          <p style="color:#6B7280;font-size:14px;line-height:1.7;margin-top:12px;">
            Bem-vindo, <span style="color:#D4880A;font-weight:600;">Senhor Sabino</span>.<br>
            Aguardando autenticacao para<br>acesso ao hub operacional.
          </p>
        </div>
        """, unsafe_allow_html=True)

        senha = st.text_input(
            "CREDENCIAL",
            type="password",
            placeholder="••••••••",
            label_visibility="visible"
        )

        if st.button("AUTENTICAR", use_container_width=True):
            if senha == "gsr17":
                st.session_state.logado = True
                st.rerun()
            else:
                st.markdown("""
                <div style="background:rgba(201,42,42,0.06);border:1px solid rgba(201,42,42,0.2);
                    border-radius:10px;padding:12px 16px;color:#C92A2A;font-size:13px;margin-top:8px;">
                  &#10007; &nbsp; Credencial invalida. Acesso negado.
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:28px;padding:16px;border:1px solid #E8EAEF;
            border-radius:10px;background:#F8F9FC;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2px;
              color:#6B7280;line-height:2;">
            PROTOCOLO &middot; AES-256<br>
            SESSAO &middot; MONITORADA<br>
            ACESSO &middot; LOG REGISTRADO
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
    "A Iniciar":        "#8BA8C8",
    "Em Andamento":     "#E8720C",
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
            # Fix encoding for text columns
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
      <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:3px;color:#3B5BDB;margin-bottom:4px;">&#9679; SISTEMA ATIVO</div>
      <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
          background:linear-gradient(135deg,#D4880A,#3B5BDB);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
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
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#3B5BDB;">{total}</div>
          </div>
          <div style="background:#FFFFFF;border:1px solid #E8EAEF;border-radius:10px;padding:12px 14px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9CA3AF;margin-bottom:4px;">CONCLUSAO</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#2F9E44;">{taxa}%</div>
          </div>
          <div style="background:#FFFFFF;border:1px solid #E8EAEF;border-radius:10px;padding:12px 14px;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;color:#9CA3AF;margin-bottom:4px;">EM EXECUCAO</div>
            <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#D4880A;">{em_exec}</div>
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
    padding:16px 24px;border:1px solid #E2E4EA;border-radius:14px;
    background:#FFFFFF;backdrop-filter:blur(10px);margin-bottom:24px;">
  <div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:4px;color:#3B5BDB;margin-bottom:4px;">&#9679; HUB OPERACIONAL</div>
    <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
        background:linear-gradient(135deg,#D4880A,#3B5BDB);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        GABRIEL SABINO</div>
  </div>
  <div style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:10px;color:#9CA3AF;letter-spacing:1px;">
    <div style="color:#2F9E44;margin-bottom:4px;">&#9679; JARVIS ONLINE</div>
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
