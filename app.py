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

    # Bruxo velho — cabelo e barba brancos, curvado, rugas, cajado mais trabalhado
    LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: transparent; font-family: 'Inter', sans-serif; overflow: hidden; }
  #stage { width: 100%; height: 100%; position: relative; background: transparent; display: flex; align-items: center; justify-content: center; }
  canvas { position: absolute; inset: 0; width: 100%; height: 100%; }

  /* Humanoid Old Wizard */
  #humanoid {
    position: relative;
    z-index: 2;
    width: min(260px, 75vw);
    margin-top: 20px;
    animation: float 5s ease-in-out infinite;
    filter: drop-shadow(0 8px 32px rgba(107,33,168,0.25));
  }
  @keyframes float {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-10px); }
  }

  /* Head animations — slower, more weary */
  .head-group { animation: headtilt 8s ease-in-out infinite; transform-origin: 110px 95px; }
  @keyframes headtilt { 0%,100%{transform:rotate(0);} 40%{transform:rotate(-3deg);} 75%{transform:rotate(2deg);} }

  .eye { animation: blink 7s infinite; }
  .eye-l { transform-origin: 88px 82px; }
  .eye-r { transform-origin: 128px 82px; }
  @keyframes blink { 0%,85%,100%{transform:scaleY(1);} 88%{transform:scaleY(0.06);} }

  /* Robe sway — slower for old wizard */
  .robe { animation: robesway 8s ease-in-out infinite; transform-origin: 110px 220px; }
  @keyframes robesway { 0%,100%{transform:rotate(0);} 50%{transform:rotate(1.5deg);} }

  /* Magic orb pulse */
  .orb { animation: orbpulse 2.5s ease-in-out infinite; transform-origin: 168px 125px; }
  @keyframes orbpulse { 0%,100%{transform:scale(1);opacity:0.85;} 50%{transform:scale(1.15);opacity:1;} }

  /* Stars */
  .star { animation: twinkle 2s ease-in-out infinite; }
  .s1{animation-delay:0s;} .s2{animation-delay:.4s;} .s3{animation-delay:.8s;} .s4{animation-delay:1.2s;}
  @keyframes twinkle { 0%,100%{opacity:0.3;transform:scale(0.8);} 50%{opacity:1;transform:scale(1.2);} }

  /* Arm with staff — slower */
  .arm-staff { animation: staffwave 5s ease-in-out infinite; transform-origin: 155px 175px; }
  @keyframes staffwave { 0%,100%{transform:rotate(0);} 50%{transform:rotate(-5deg);} }

  /* Beard flow */
  .beard { animation: beardway 6s ease-in-out infinite; transform-origin: 110px 130px; }
  @keyframes beardway { 0%,100%{transform:skewX(0);} 50%{transform:skewX(1.5deg);} }

  /* Particles */
  .magic-particle { animation: magicfloat 3.5s ease-in-out infinite; }
  .mp1{animation-delay:0s;} .mp2{animation-delay:.6s;} .mp3{animation-delay:1.2s;} .mp4{animation-delay:1.8s;}
  @keyframes magicfloat { 0%{transform:translateY(0) scale(1);opacity:1;} 100%{transform:translateY(-35px) scale(0);opacity:0;} }

  .hud {
    position: absolute; bottom: 10px; left: 50%;
    transform: translateX(-50%);
    font-size: 9px; letter-spacing: 3px; color: rgba(107,33,168,0.6);
    font-family: monospace; white-space: nowrap;
    animation: pulse 2s ease-in-out infinite;
    z-index: 3;
  }
  @keyframes pulse { 0%,100%{opacity:0.5;} 50%{opacity:1;} }
</style>
</head>
<body>
<div id="stage">
  <canvas id="cv"></canvas>

  <svg id="humanoid" viewBox="0 0 220 420" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="gPurple2" cx="50%" cy="30%">
        <stop offset="0%" stop-color="#9D7FEA"/>
        <stop offset="100%" stop-color="#3B1278"/>
      </radialGradient>
      <radialGradient id="gRobe2" cx="50%" cy="20%">
        <stop offset="0%" stop-color="#6D28D9"/>
        <stop offset="100%" stop-color="#1E0856"/>
      </radialGradient>
      <radialGradient id="gSkin2" cx="50%" cy="40%">
        <stop offset="0%" stop-color="#F5D9B0"/>
        <stop offset="100%" stop-color="#C4956A"/>
      </radialGradient>
      <radialGradient id="gOrb2" cx="50%" cy="40%">
        <stop offset="0%" stop-color="#34D399"/>
        <stop offset="60%" stop-color="#059669"/>
        <stop offset="100%" stop-color="#064E3B"/>
      </radialGradient>
      <linearGradient id="gStaff" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#7C5C2A"/>
        <stop offset="50%" stop-color="#A0783A"/>
        <stop offset="100%" stop-color="#5A3E18"/>
      </linearGradient>
      <filter id="glow2"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <filter id="softglow2"><feGaussianBlur stdDeviation="7"/></filter>
    </defs>

    <!-- Shadow (offset right since wizard leans) -->
    <ellipse cx="115" cy="413" rx="52" ry="5" fill="#3B1278" opacity="0.18" filter="url(#softglow2)"/>

    <!-- ══════════════ ROBE / CLOAK ══════════════ -->
    <g class="robe">
      <!-- Main robe — slightly asymmetric (leans on staff) -->
      <path d="M58 185 Q44 215 32 305 Q26 360 38 390 L185 390 Q195 360 190 305 Q180 215 165 185 Z"
            fill="url(#gRobe2)" opacity="0.97"/>
      <!-- Inner robe highlight -->
      <path d="M78 185 Q72 225 68 305 L152 305 Q148 225 142 185 Z"
            fill="#7C3AED" opacity="0.22"/>
      <!-- Robe hem -->
      <path d="M32 390 Q58 400 115 397 Q172 400 185 390 L190 384 Q168 394 115 391 Q58 394 32 384 Z"
            fill="#9D7FEA" opacity="0.45"/>
      <!-- Moon on robe -->
      <text x="80" y="290" font-size="18" text-anchor="middle" class="star s1" fill="#C4B5FD">☽</text>
      <!-- Stars on robe -->
      <text x="142" y="265" font-size="13" text-anchor="middle" class="star s2" fill="#DDD6FE">✦</text>
      <text x="65" y="330" font-size="11" text-anchor="middle" class="star s3" fill="#C4B5FD">✦</text>
      <text x="155" y="310" font-size="9"  text-anchor="middle" class="star s4" fill="#A78BFA">✦</text>
    </g>

    <!-- BODY under robe collar -->
    <rect x="76" y="168" width="68" height="28" rx="6" fill="#4C1D95" opacity="0.85"/>
    <!-- Collar trim -->
    <path d="M76 168 Q110 178 144 168" stroke="#9D7FEA" stroke-width="2" fill="none" opacity="0.7"/>

    <!-- NECK -->
    <rect x="100" y="142" width="22" height="20" rx="4" fill="#C4956A"/>

    <!-- ══════════════ HEAD GROUP ══════════════ -->
    <g class="head-group">

      <!-- HAT — tall, slightly tilted -->
      <!-- Brim -->
      <ellipse cx="110" cy="38" rx="50" ry="10" fill="#3B1278" transform="rotate(-3 110 38)"/>
      <!-- Cone — tall and dramatic -->
      <path d="M108 0 L68 40 L152 40 Z" fill="url(#gPurple2)" transform="rotate(-2 110 20)"/>
      <!-- Hat wrinkle band -->
      <path d="M70 33 Q110 27 150 33" stroke="#7C3AED" stroke-width="3" fill="none" opacity="0.6"/>
      <!-- Hat band buckle -->
      <rect x="101" y="29" width="18" height="9" rx="2" fill="#C4956A" opacity="0.8"/>
      <rect x="105" y="31" width="10" height="5" rx="1" fill="#7C3AED" opacity="0.7"/>
      <!-- Hat star -->
      <text x="105" y="22" font-size="11" text-anchor="middle" class="star s4" fill="#FDE68A">★</text>

      <!-- FACE — rounder, aged -->
      <!-- Head shape slightly wider at jaw for jowls -->
      <ellipse cx="110" cy="92" rx="38" ry="44" fill="url(#gSkin2)"/>
      <!-- Jowls / cheek sag -->
      <ellipse cx="78"  cy="108" rx="10" ry="8" fill="#C4956A" opacity="0.35"/>
      <ellipse cx="142" cy="108" rx="10" ry="8" fill="#C4956A" opacity="0.35"/>
      <!-- Age spots subtly -->
      <circle cx="88" cy="82" r="2" fill="#B07A4A" opacity="0.2"/>
      <circle cx="130" cy="78" r="1.5" fill="#B07A4A" opacity="0.2"/>

      <!-- Wrinkles — forehead -->
      <path d="M88 65 Q110 60 132 65" stroke="#B07A4A" stroke-width="0.8" fill="none" opacity="0.45"/>
      <path d="M92 58 Q110 54 128 58" stroke="#B07A4A" stroke-width="0.6" fill="none" opacity="0.3"/>
      <!-- Crow's feet left -->
      <path d="M75 88 Q72 84 74 80" stroke="#B07A4A" stroke-width="0.8" fill="none" opacity="0.4"/>
      <path d="M75 88 Q71 88 72 84" stroke="#B07A4A" stroke-width="0.8" fill="none" opacity="0.35"/>
      <!-- Crow's feet right -->
      <path d="M145 88 Q148 84 146 80" stroke="#B07A4A" stroke-width="0.8" fill="none" opacity="0.4"/>
      <path d="M145 88 Q149 88 148 84" stroke="#B07A4A" stroke-width="0.8" fill="none" opacity="0.35"/>
      <!-- Nasolabial lines -->
      <path d="M85 100 Q82 112 86 118" stroke="#B07A4A" stroke-width="0.7" fill="none" opacity="0.35"/>
      <path d="M135 100 Q138 112 134 118" stroke="#B07A4A" stroke-width="0.7" fill="none" opacity="0.35"/>

      <!-- Thick bushy WHITE eyebrows — arched, bushy -->
      <path d="M78 70 Q88 62 102 66" stroke="#E8E8E8" stroke-width="4.5" fill="none" stroke-linecap="round"/>
      <path d="M78 70 Q88 62 102 66" stroke="white" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.7"/>
      <path d="M118 66 Q132 62 142 70" stroke="#E8E8E8" stroke-width="4.5" fill="none" stroke-linecap="round"/>
      <path d="M118 66 Q132 62 142 70" stroke="white" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.7"/>
      <!-- Eyebrow wild tufts -->
      <path d="M80 68 L76 63" stroke="#DEDEDE" stroke-width="2" stroke-linecap="round"/>
      <path d="M140 68 L144 63" stroke="#DEDEDE" stroke-width="2" stroke-linecap="round"/>

      <!-- Left Eye — smaller, more hooded -->
      <g class="eye eye-l">
        <ellipse cx="88" cy="82" rx="10" ry="9" fill="white"/>
        <!-- Hooded lid -->
        <path d="M78 78 Q88 73 98 78" fill="#C4956A" opacity="0.5"/>
        <ellipse cx="88" cy="83" rx="6" ry="6.5" fill="#3B1278"/>
        <ellipse cx="88" cy="83" rx="3.5" ry="3.5" fill="#1A0A2E"/>
        <ellipse cx="91" cy="80" rx="2" ry="2" fill="white" opacity="0.85"/>
        <!-- Subtle purple iris glow -->
        <ellipse cx="88" cy="83" rx="6" ry="6.5" fill="#7C3AED" opacity="0.25" filter="url(#glow2)"/>
      </g>

      <!-- Right Eye -->
      <g class="eye eye-r">
        <ellipse cx="132" cy="82" rx="10" ry="9" fill="white"/>
        <path d="M122 78 Q132 73 142 78" fill="#C4956A" opacity="0.5"/>
        <ellipse cx="132" cy="83" rx="6" ry="6.5" fill="#3B1278"/>
        <ellipse cx="132" cy="83" rx="3.5" ry="3.5" fill="#1A0A2E"/>
        <ellipse cx="135" cy="80" rx="2" ry="2" fill="white" opacity="0.85"/>
        <ellipse cx="132" cy="83" rx="6" ry="6.5" fill="#7C3AED" opacity="0.25" filter="url(#glow2)"/>
      </g>

      <!-- Nose — larger, bulbous -->
      <ellipse cx="110" cy="96" rx="7" ry="6" fill="#C4956A" opacity="0.65"/>
      <ellipse cx="106" cy="98" rx="3" ry="2.5" fill="#B07A4A" opacity="0.3"/>
      <ellipse cx="114" cy="98" rx="3" ry="2.5" fill="#B07A4A" opacity="0.3"/>

      <!-- Smile — subtle, warm -->
      <path d="M96 112 Q110 122 124 112" stroke="#92400E" stroke-width="1.8" fill="none" stroke-linecap="round"/>
      <!-- Lip lines -->
      <path d="M102 113 Q110 118 118 113" stroke="#A0522D" stroke-width="1" fill="none" opacity="0.4"/>

      <!-- Ears — larger with age -->
      <ellipse cx="72" cy="90" rx="9" ry="12" fill="url(#gSkin2)"/>
      <ellipse cx="72" cy="90" rx="5" ry="7" fill="#C4956A" opacity="0.4"/>
      <ellipse cx="148" cy="90" rx="9" ry="12" fill="url(#gSkin2)"/>
      <ellipse cx="148" cy="90" rx="5" ry="7" fill="#C4956A" opacity="0.4"/>

      <!-- WHITE HAIR — flowing out from hat sides -->
      <path d="M72 55 Q60 75 65 100 Q62 110 68 125" stroke="#E8E8E8" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M72 55 Q58 80 62 108 Q60 118 65 130" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" opacity="0.6"/>
      <path d="M148 55 Q160 75 155 100 Q158 110 152 125" stroke="#E8E8E8" stroke-width="5" fill="none" stroke-linecap="round"/>
      <path d="M148 55 Q162 80 158 108 Q160 118 155 130" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" opacity="0.6"/>

      <!-- LONG WHITE BEARD — flowing down, layered -->
      <g class="beard">
        <!-- Beard base wide -->
        <path d="M80 125 Q75 155 72 185 Q70 210 78 230 Q95 255 110 260 Q125 255 142 230 Q150 210 148 185 Q145 155 140 125 Q125 132 110 133 Q95 132 80 125 Z"
              fill="#E8E8E8"/>
        <!-- Beard mid layer -->
        <path d="M84 125 Q80 158 78 190 Q76 215 85 238 Q98 257 110 260 Q122 257 135 238 Q144 215 142 190 Q140 158 136 125 Q123 131 110 132 Q97 131 84 125 Z"
              fill="#F0F0F0" opacity="0.8"/>
        <!-- Beard highlight -->
        <path d="M100 128 Q100 160 102 200 Q103 230 110 248" stroke="white" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.7"/>
        <path d="M120 128 Q119 165 118 205 Q117 232 110 248" stroke="white" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.5"/>
        <!-- Beard tip wisps -->
        <path d="M100 248 Q105 265 108 272" stroke="#D0D0D0" stroke-width="2" fill="none" stroke-linecap="round"/>
        <path d="M110 255 Q110 270 110 278" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <path d="M120 248 Q115 265 112 272" stroke="#D0D0D0" stroke-width="2" fill="none" stroke-linecap="round"/>
        <!-- Moustache -->
        <path d="M94 118 Q102 124 110 121 Q118 124 126 118" stroke="#D0D0D0" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        <path d="M94 118 Q102 124 110 121 Q118 124 126 118" stroke="white" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="0.7"/>
      </g>

    </g>

    <!-- ══════════════ LEFT ARM (holding robe, slightly bent) ══════════════ -->
    <path d="M72 185 Q54 198 48 230 Q44 252 52 262 Q60 268 67 258 Q70 240 74 218 L80 192 Z"
          fill="#4C1D95"/>
    <!-- Left hand — aged -->
    <ellipse cx="52" cy="264" rx="11" ry="9" fill="url(#gSkin2)"/>
    <!-- Knuckle lines -->
    <path d="M44 262 Q52 258 60 262" stroke="#C4956A" stroke-width="0.8" fill="none" opacity="0.5"/>

    <!-- ══════════════ RIGHT ARM — holding staff ══════════════ -->
    <g class="arm-staff">
      <path d="M148 185 Q164 195 170 218 Q175 240 168 255 L160 242 Q158 220 154 200 L144 190 Z"
            fill="#4C1D95"/>
      <!-- Right hand -->
      <ellipse cx="166" cy="257" rx="11" ry="9" fill="url(#gSkin2)"/>
      <path d="M158 255 Q166 251 174 255" stroke="#C4956A" stroke-width="0.8" fill="none" opacity="0.5"/>

      <!-- STAFF — gnarled, wooden -->
      <path d="M166 248 Q164 220 168 180 Q171 145 170 115 Q169 95 168 80"
            stroke="url(#gStaff)" stroke-width="6" fill="none" stroke-linecap="round"/>
      <!-- Staff grain lines -->
      <path d="M166 248 Q164 220 168 180 Q171 145 170 115 Q169 95 168 80"
            stroke="#FDE68A" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="0.3"/>
      <!-- Staff knot / knurl details -->
      <ellipse cx="169" cy="175" rx="5" ry="4" fill="#7C5C2A" opacity="0.8"/>
      <ellipse cx="170" cy="140" rx="4" ry="3" fill="#7C5C2A" opacity="0.6"/>
      <!-- Staff gnarled tip curl -->
      <path d="M168 80 Q162 68 155 62 Q148 56 152 50 Q157 44 165 48"
            stroke="url(#gStaff)" stroke-width="5" fill="none" stroke-linecap="round"/>

      <!-- ORB on staff top — glowing green -->
      <g class="orb">
        <ellipse cx="163" cy="47" rx="20" ry="20" fill="#10B981" opacity="0.25" filter="url(#softglow2)"/>
        <ellipse cx="163" cy="47" rx="15" ry="15" fill="url(#gOrb2)" filter="url(#glow2)"/>
        <ellipse cx="163" cy="47" rx="9" ry="9" fill="#34D399" opacity="0.55"/>
        <ellipse cx="158" cy="42" rx="5" ry="5" fill="white" opacity="0.65"/>
        <!-- Orbits around the orb -->
        <circle cx="163" cy="47" r="19" fill="none" stroke="#10B981" stroke-width="0.7" opacity="0.4" stroke-dasharray="3 4"/>
      </g>

      <!-- Magic particles from orb -->
      <circle class="magic-particle mp1" cx="178" cy="35" r="3"   fill="#10B981" opacity="0.85"/>
      <circle class="magic-particle mp2" cx="148" cy="30" r="2"   fill="#A855F7" opacity="0.85"/>
      <circle class="magic-particle mp3" cx="183" cy="47" r="2.5" fill="#FDE68A" opacity="0.85"/>
      <circle class="magic-particle mp4" cx="152" cy="24" r="3"   fill="#34D399" opacity="0.85"/>
      <!-- Extra sparkles -->
      <text class="star s2" x="188" y="42" font-size="9" fill="#FDE68A">✦</text>
      <text class="star s3" x="145" y="20" font-size="8" fill="#A78BFA">✦</text>
    </g>

    <!-- Feet / shoes — pointy wizard shoes -->
    <path d="M82 388 Q78 395 58 400 Q52 402 55 407 Q60 410 80 406 Q100 403 105 395 L105 388 Z"
          fill="#2D1654"/>
    <path d="M138 388 Q142 395 162 400 Q168 402 165 407 Q160 410 140 406 Q120 403 115 395 L115 388 Z"
          fill="#2D1654"/>
    <!-- Shoe tips shine -->
    <path d="M58 400 Q54 403 56 406" stroke="#4C1D95" stroke-width="1.5" fill="none" opacity="0.6"/>
    <path d="M162 400 Q166 403 164 406" stroke="#4C1D95" stroke-width="1.5" fill="none" opacity="0.6"/>
  </svg>

  <div class="hud">&#128302; FEITICO ATIVO &middot; AGUARDANDO BRUXO &#128302;</div>
</div>

<script>
const cv = document.getElementById('cv');
const ctx = cv.getContext('2d');
function resize(){ cv.width=cv.offsetWidth; cv.height=cv.offsetHeight; }
resize();
window.addEventListener('resize', resize);
const P = Array.from({length:30}, () => ({
  x: Math.random()*cv.width, y: Math.random()*cv.height,
  vx: (Math.random()-0.5)*0.4, vy: (Math.random()-0.5)*0.4,
  r: Math.random()*2+0.5,
  c: Math.random()>0.5 ? '#6B21A8' : '#10B981'
}));
function tick(){
  ctx.clearRect(0,0,cv.width,cv.height);
  P.forEach(p => {
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
        components.html(LOGIN_HTML, height=620, scrolling=False)

    with col_form:
        st.markdown("""
        <div style="padding:48px 0 28px 0;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:4px;
              color:#6B21A8;margin-bottom:16px;">&#128302; SISTEMA ATIVO</div>
          <div style="font-size:38px;margin-bottom:4px;">🧙‍♂️</div>
          <div style="font-family:'Syne',sans-serif;font-size:40px;font-weight:800;
              color:#6B21A8;line-height:1;margin-bottom:4px;">Bem-vindo,</div>
          <div style="font-family:'Syne',sans-serif;font-size:40px;font-weight:800;
              color:#10B981;line-height:1;margin-bottom:20px;">Sabino.</div>
          <p style="color:#5B4E72;font-size:14px;line-height:1.8;margin-bottom:0;">
            O feitico aguarda.<br>
            Insira sua credencial para<br>
            acessar o hub operacional.
          </p>
        </div>
        """, unsafe_allow_html=True)

        senha = st.text_input(
            "CREDENCIAL SECRETA",
            type="password",
            placeholder="••••••••",
            label_visibility="visible"
        )

        if st.button("🔮  INVOCAR ACESSO", use_container_width=True):
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
        <div style="margin-top:28px;padding:16px;border:1px solid #DDD8F0;
            border-radius:10px;background:#EFECF8;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2px;
              color:#5B4E72;line-height:2.2;">
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
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:4px;color:#6B21A8;margin-bottom:4px;">&#9679; HUB OPERACIONAL</div>
    <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
        color:#6B21A8;">
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🤖 CHAT IA",
    "⚡ VISAO GERAL",
    "📋 KANBAN",
    "🗂️ DADOS",
    "🗺️ MAPEAMENTO GS",
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
                    {msg['content']}
                  </div>
                  <div style="width:36px;height:36px;background:#DDD8F0;border-radius:50%;
                      display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">🧙‍♂️</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                content = msg['content'].replace(chr(10), '<br>')
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
