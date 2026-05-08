import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime, timedelta

try
    from streamlit_gsheets import GSheetsConnection
    LIB_PRONTA = True
except ImportError
    LIB_PRONTA = False

st.set_page_config(
    layout=wide,
    page_title=Sabino OS,
 page_icon=":zap:",

    initial_sidebar_state=collapsed
)

# ============================================================
# GLOBAL STYLES
# ============================================================
st.markdown(
style
@import url('httpsfonts.googleapis.comcss2family=Interwght@300;400;500;600;700&family=Synewght@700;800&family=JetBrains+Monowght@400;500&display=swap');

root {
    --bg #F5F6F8;
    --bg2 #FFFFFF;
    --surface #FFFFFF;
    --surface2 #F0F1F4;
    --border #E2E4EA;
    --border-strong #CDD0DA;
    --accent #3B5BDB;
    --accent-light rgba(59,91,219,0.08);
    --accent-muted rgba(59,91,219,0.15);
    --gold #D4880A;
    --green #2F9E44;
    --red #C92A2A;
    --orange #E07B1A;
    --purple #7048E8;
    --teal #0C8599;
    --text #1A1D2E;
    --text-muted #6B7280;
    --text-dim #9CA3AF;
}

, before, after { box-sizing border-box; }

html, body, .stApp {
    font-family 'Inter', sans-serif !important;
    background var(--bg) !important;
    color var(--text) !important;
}

[data-testid=stHeader], #MainMenu, footer, .stDeployButton { display none !important; }
[data-testid=stAppViewContainer] { background var(--bg) !important; }
.block-container { padding 1.5rem 1.5rem 2rem !important; max-width 100% !important; }

 Sidebar 
[data-testid=stSidebar] {
    background var(--bg2) !important;
    border-right 1px solid var(--border) !important;
    min-width 220px !important;
    box-shadow 2px 0 12px rgba(0,0,0,0.04) !important;
}
[data-testid=stSidebar] .block-container { padding 1.5rem 1rem !important; }
[data-testid=stSidebar]  { color var(--text) !important; }

 Tabs 
.stTabs [data-baseweb=tab-list] {
    background var(--bg2) !important;
    border 1px solid var(--border) !important;
    border-radius 12px !important;
    padding 4px !important;
    gap 2px !important;
    overflow-x auto !important;
    box-shadow 0 1px 4px rgba(0,0,0,0.06) !important;
}
.stTabs [data-baseweb=tab] {
    background transparent !important;
    color var(--text-muted) !important;
    border-radius 9px !important;
    padding 8px 16px !important;
    font-size 13px !important;
    font-weight 500 !important;
    font-family 'Inter', sans-serif !important;
    white-space nowrap !important;
    transition all 0.2s !important;
    border none !important;
}
.stTabs [aria-selected=true] {
    background var(--accent) !important;
    color #fff !important;
    box-shadow 0 2px 8px rgba(59,91,219,0.3) !important;
}
.stTabs [data-baseweb=tab-panel] { padding-top 1.5rem !important; }

 Metrics 
[data-testid=stMetric] {
    background var(--surface) !important;
    border 1px solid var(--border) !important;
    border-radius 14px !important;
    padding 20px !important;
    transition all 0.2s !important;
    box-shadow 0 1px 4px rgba(0,0,0,0.05) !important;
}
[data-testid=stMetric]hover {
    border-color var(--accent) !important;
    box-shadow 0 4px 16px rgba(59,91,219,0.1) !important;
    transform translateY(-2px) !important;
}
[data-testid=stMetricLabel] {
    color var(--text-muted) !important;
    font-size 11px !important;
    letter-spacing 1px !important;
    text-transform uppercase !important;
    font-family 'JetBrains Mono', monospace !important;
}
[data-testid=stMetricValue] {
    color var(--accent) !important;
    font-family 'Syne', sans-serif !important;
    font-size 2rem !important;
}

 Buttons 
.stButton  button {
    background var(--accent) !important;
    color #fff !important;
    border none !important;
    border-radius 10px !important;
    font-family 'Inter', sans-serif !important;
    font-weight 600 !important;
    font-size 13px !important;
    transition all 0.2s !important;
    box-shadow 0 2px 8px rgba(59,91,219,0.25) !important;
}
.stButton  buttonhover {
    background #2f4cba !important;
    transform translateY(-1px) !important;
    box-shadow 0 4px 16px rgba(59,91,219,0.35) !important;
}

 Inputs 
.stTextInput input, .stTextArea textarea {
    background var(--surface) !important;
    border 1px solid var(--border) !important;
    border-radius 10px !important;
    color var(--text) !important;
    font-family 'Inter', sans-serif !important;
    font-size 14px !important;
    transition border-color 0.2s, box-shadow 0.2s !important;
    box-shadow 0 1px 3px rgba(0,0,0,0.05) !important;
}
.stTextInput inputfocus, .stTextArea textareafocus {
    border-color var(--accent) !important;
    box-shadow 0 0 0 3px rgba(59,91,219,0.12) !important;
}
.stTextInput label, .stTextArea label {
    color var(--text-muted) !important;
    font-size 12px !important;
    font-weight 500 !important;
    letter-spacing 0.5px !important;
}

 Dataframe 
[data-testid=stDataFrame] {
    border 1px solid var(--border) !important;
    border-radius 12px !important;
    overflow hidden !important;
    box-shadow 0 1px 4px rgba(0,0,0,0.05) !important;
}

 Divider 
hr { border-color var(--border) !important; }

 Link button 
.stLinkButton a {
    background var(--surface) !important;
    color var(--text) !important;
    border 1px solid var(--border) !important;
    border-radius 10px !important;
    font-size 13px !important;
    font-weight 500 !important;
}

 Scrollbar 
-webkit-scrollbar { width 4px; height 4px; }
-webkit-scrollbar-track { background var(--bg); }
-webkit-scrollbar-thumb { background var(--border-strong); border-radius 4px; }

 Chat bubbles 
.chat-bubble-user {
    background var(--accent);
    color #fff;
    border-radius 14px 14px 4px 14px;
    padding 12px 16px;
    max-width 75%;
    font-size 14px;
    line-height 1.5;
}
.chat-bubble-ai {
    background var(--surface);
    border 1px solid var(--border);
    border-radius 14px 14px 14px 4px;
    padding 12px 16px;
    max-width 80%;
    font-size 14px;
    color var(--text);
    line-height 1.6;
    box-shadow 0 1px 4px rgba(0,0,0,0.06);
}
.chat-msg-user { displayflex; justify-contentflex-end; margin8px 0; }
.chat-msg-ai   { displayflex; justify-contentflex-start; margin8px 0; }

@media (max-width 768px) {
    .block-container { padding 1rem 0.75rem 2rem !important; }
    [data-testid=stMetricValue] { font-size 1.5rem !important; }
    .stTabs [data-baseweb=tab] { padding 7px 10px !important; font-size 11px !important; }
}
style
, unsafe_allow_html=True)

# ============================================================
# JARVIS LOGIN COMPONENT
# ============================================================
JARVIS_HTML = 
!DOCTYPE html
html
head
meta name=viewport content=width=device-width, initial-scale=1.0
style
   { margin 0; padding 0; box-sizing border-box; }
  body { background transparent; overflow hidden; font-family 'Space Grotesk', sans-serif; }

  #stage {
    width 100%; height 100%;
    position relative; overflow hidden;
    background #F8F9FC;
  }

  canvas#particles { position absolute; inset 0; width 100%; height 100%; }

   Orbit rings 
  .rings { position absolute; top 50%; left 50%; transform translate(-50%, -50%); width min(320px, 90vw); height min(320px, 90vw); }
  .ring {
    position absolute; border-radius 50%;
    border 1px solid rgba(59,91,219,0.12);
    top 50%; left 50%; transform translate(-50%, -50%);
  }
  .ring-1 { width 100%; height 100%; animation spin 20s linear infinite; border-style dashed; border-color rgba(59,91,219,0.15); }
  .ring-2 { width 72%; height 72%; animation spin 14s linear infinite reverse; border-color rgba(212,136,10,0.2); }
  .ring-3 { width 48%; height 48%; animation spin 9s linear infinite; border-color rgba(59,91,219,0.15); }

   Orbit dot 
  .orbit-dot {
    position absolute; width 6px; height 6px;
    background var(--c, #3B5BDB); border-radius 50%;
    box-shadow 0 0 8px var(--c, #3B5BDB);
    top 0; left 50%; transform translateX(-50%) translateY(-3px);
  }
  .ring-1 .orbit-dot { --c #3B5BDB; }
  .ring-2 .orbit-dot { --c #D4880A; }

  @keyframes spin { to { transform translate(-50%,-50%) rotate(360deg); } }

   SVG robot 
  #bot {
    position absolute; top 50%; left 50%;
    transform translate(-50%, -52%);
    width min(260px, 75vw);
    filter drop-shadow(0 0 16px rgba(59,91,219,0.15)) drop-shadow(0 8px 24px rgba(0,0,0,0.12));
    animation float 4s ease-in-out infinite;
  }
  @keyframes float { 0%,100%{transformtranslate(-50%,-52%);} 50%{transformtranslate(-50%,-56%);} }

  .jv-head { animation headtilt 6s ease-in-out infinite; transform-origin 200px 230px; }
  @keyframes headtilt { 0%,100%{transformrotate(0);} 30%{transformrotate(-3deg);} 70%{transformrotate(3deg);} }

  .eye { animation blink 5s infinite; }
  @keyframes blink { 0%,90%,100%{transformscaleY(1);} 93%{transformscaleY(0.05);} }
  .eye-l { transform-origin 163px 148px; }
  .eye-r { transform-origin 237px 148px; }

  .bar { animation talk 0.2s ease-in-out infinite alternate; transform-origin center bottom; }
  .b1{animation-delay0s;} .b2{animation-delay.03s;} .b3{animation-delay.06s;}
  .b4{animation-delay.09s;} .b5{animation-delay.06s;} .b6{animation-delay.03s;} .b7{animation-delay.01s;}
  @keyframes talk { from{transformscaleY(0.15);} to{transformscaleY(1.3);} }

  .rotor { animation spin 3s linear infinite; transform-origin 200px 340px; }
  .arm-l { animation armL 4s ease-in-out infinite; transform-origin 88px 270px; }
  .arm-r { animation armR 4s ease-in-out infinite; transform-origin 312px 270px; }
  @keyframes armL { 0%,100%{transformrotate(0);} 50%{transformrotate(-9deg);} }
  @keyframes armR { 0%,100%{transformrotate(0);} 50%{transformrotate(9deg);} }

   HUD text 
  .hud {
    position absolute; bottom 12px; left 50%;
    transform translateX(-50%);
    font-size 10px; letter-spacing 3px; color rgba(59,91,219,0.5);
    font-family 'JetBrains Mono', monospace;
    white-space nowrap;
    animation pulse 2s ease-in-out infinite;
  }
  @keyframes pulse { 0%,100%{opacity0.5;} 50%{opacity1;} }
style
head
body
div id=stage
  canvas id=particlescanvas

  div class=rings
    div class=ring ring-1div class=orbit-dotdivdiv
    div class=ring ring-2div class=orbit-dotdivdiv
    div class=ring ring-3div
  div

  svg id=bot viewBox=0 0 400 500 xmlns=httpwww.w3.org2000svg
    defs
      radialGradient id=gGold cx=50% cy=35%
        stop offset=0% stop-color=#D4C090
        stop offset=60% stop-color=#D4880A
        stop offset=100% stop-color=#6B5020
      radialGradient
      radialGradient id=gCyan cx=50% cy=50%
        stop offset=0% stop-color=#1A1D2E
        stop offset=60% stop-color=#3B5BDB
        stop offset=100% stop-color=#2A2D3A
      radialGradient
      linearGradient id=gMetal x1=0 x2=0 y1=0 y2=1
        stop offset=0% stop-color=#9CA3AF
        stop offset=50% stop-color=#ECEEF3
        stop offset=100% stop-color=#E8EAEF
      linearGradient
      linearGradient id=gChest x1=0 x2=0 y1=0 y2=1
        stop offset=0% stop-color=#F0F2F7
        stop offset=100% stop-color=#E8EAEF
      linearGradient
      filter id=glowfeGaussianBlur stdDeviation=3 result=blurfeMergefeMergeNode in=blurfeMergeNode in=SourceGraphicfeMergefilter
      filter id=bigGlowfeGaussianBlur stdDeviation=8filter
    defs

    !-- Shadow --
    ellipse cx=200 cy=490 rx=100 ry=7 fill=#3B5BDB opacity=0.2 filter=url(#bigGlow)

    !-- Antenna --
    line x1=200 y1=38 x2=200 y2=78 stroke=#D4880A stroke-width=2.5 stroke-linecap=round
    circle cx=200 cy=32 r=6 fill=url(#gGold) filter=url(#glow)
      animate attributeName=r values=4;8;4 dur=1.2s repeatCount=indefinite
      animate attributeName=opacity values=0.7;1;0.7 dur=1.2s repeatCount=indefinite
    circle

    !-- HEAD GROUP --
    g class=jv-head
      !-- Neck --
      rect x=182 y=232 width=36 height=24 rx=4 fill=url(#gMetal) stroke=rgba(99,179,237,0.3) stroke-width=1

      !-- Head --
      path d=M118 100 Q118 68 148 68 L252 68 Q282 68 282 100 L282 215 Q282 238 252 238 L148 238 Q118 238 118 215 Z
            fill=url(#gMetal)
      !-- Head border --
      path d=M118 100 Q118 68 148 68 L252 68 Q282 68 282 100 L282 215 Q282 238 252 238 L148 238 Q118 238 118 215 Z
            fill=none stroke=rgba(99,179,237,0.25) stroke-width=1.5

      !-- Top band --
      path d=M128 78 Q128 72 138 72 L262 72 Q272 72 272 78 L272 100 L128 100 Z fill=url(#gGold) opacity=0.8
      !-- Brand text area --
      text x=200 y=94 text-anchor=middle fill=#E8EAEF font-size=9 font-weight=700 letter-spacing=3 font-family=monospaceJARVIStext

      !-- Visor bg --
      rect x=135 y=112 width=130 height=72 rx=10 fill=#F0F1F4
      !-- Visor glow overlay --
      rect x=135 y=112 width=130 height=72 rx=10 fill=url(#gCyan) opacity=0.15
      !-- Visor border --
      rect x=135 y=112 width=130 height=72 rx=10 fill=none stroke=rgba(59,91,219,0.3) stroke-width=1.5
      !-- Scan lines --
      line x1=135 y1=130 x2=265 y2=130 stroke=#3B5BDB stroke-width=0.3 opacity=0.4
      line x1=135 y1=148 x2=265 y2=148 stroke=#3B5BDB stroke-width=0.3 opacity=0.4
      line x1=135 y1=166 x2=265 y2=166 stroke=#3B5BDB stroke-width=0.3 opacity=0.4

      !-- Left Eye --
      g class=eye eye-l
        circle cx=163 cy=148 r=16 fill=#F0F1F4 stroke=rgba(200,169,110,0.5) stroke-width=1.5
        circle cx=163 cy=148 r=10 fill=url(#gCyan) filter=url(#glow)
        circle cx=166 cy=145 r=3 fill=white opacity=0.8
        circle cx=163 cy=148 r=4 fill=#1A1E2A opacity=0.6
      g
      !-- Right Eye --
      g class=eye eye-r
        circle cx=237 cy=148 r=16 fill=#F0F1F4 stroke=rgba(200,169,110,0.5) stroke-width=1.5
        circle cx=237 cy=148 r=10 fill=url(#gCyan) filter=url(#glow)
        circle cx=240 cy=145 r=3 fill=white opacity=0.8
        circle cx=237 cy=148 r=4 fill=#1A1E2A opacity=0.6
      g
      !-- Corner accents on visor --
      path d=M140 116 L152 116 stroke=#3B5BDB stroke-width=1.5 opacity=0.5
      path d=M140 116 L140 124 stroke=#3B5BDB stroke-width=1.5 opacity=0.5
      path d=M260 116 L248 116 stroke=#D4880A stroke-width=1.5 opacity=0.5
      path d=M260 116 L260 124 stroke=#D4880A stroke-width=1.5 opacity=0.5

      !-- Equalizer mouth --
      g transform=translate(164,210)
        rect class=bar b1 x=0  y=-5 width=6 height=10 rx=2 fill=#D4880A opacity=0.8
        rect class=bar b2 x=9  y=-8 width=6 height=16 rx=2 fill=#3B5BDB
        rect class=bar b3 x=18 y=-11 width=6 height=22 rx=2 fill=#D4880A opacity=0.8
        rect class=bar b4 x=27 y=-14 width=6 height=28 rx=2 fill=#3B5BDB
        rect class=bar b5 x=36 y=-11 width=6 height=22 rx=2 fill=#D4880A opacity=0.8
        rect class=bar b6 x=45 y=-8 width=6 height=16 rx=2 fill=#3B5BDB
        rect class=bar b7 x=54 y=-5 width=6 height=10 rx=2 fill=#D4880A opacity=0.8
      g

      !-- Side vents --
      rect x=118 y=140 width=8 height=3 rx=1 fill=rgba(99,179,237,0.4)
      rect x=118 y=147 width=8 height=3 rx=1 fill=rgba(99,179,237,0.4)
      rect x=118 y=154 width=8 height=3 rx=1 fill=rgba(99,179,237,0.4)
      rect x=274 y=140 width=8 height=3 rx=1 fill=rgba(246,173,85,0.4)
      rect x=274 y=147 width=8 height=3 rx=1 fill=rgba(246,173,85,0.4)
      rect x=274 y=154 width=8 height=3 rx=1 fill=rgba(246,173,85,0.4)
    g

    !-- BODY --
    g
      path d=M100 264 Q100 255 118 255 L282 255 Q300 255 300 264 L300 420 Q300 440 282 440 L118 440 Q100 440 100 420 Z
            fill=url(#gChest)
      path d=M100 264 Q100 255 118 255 L282 255 Q300 255 300 264 L300 420 Q300 440 282 440 L118 440 Q100 440 100 420 Z
            fill=none stroke=rgba(99,179,237,0.2) stroke-width=1.5

      !-- Chest shoulders gold trim --
      path d=M100 264 L130 255 L160 255 L160 285 L100 285 Z fill=url(#gGold) opacity=0.7
      path d=M300 264 L270 255 L240 255 L240 285 L300 285 Z fill=url(#gGold) opacity=0.7
      !-- Chest lines --
      line x1=100 y1=290 x2=300 y2=290 stroke=rgba(99,179,237,0.15) stroke-width=1
      line x1=100 y1=380 x2=300 y2=380 stroke=rgba(99,179,237,0.15) stroke-width=1

      !-- ARC REACTOR --
      circle cx=200 cy=340 r=52 fill=#F0F1F4 stroke=rgba(99,179,237,0.1) stroke-width=1
      !-- Glow base --
      circle cx=200 cy=340 r=46 fill=url(#gCyan) filter=url(#bigGlow) opacity=0.5
      !-- Rings --
      circle cx=200 cy=340 r=40 fill=#F0F1F4
      circle cx=200 cy=340 r=36 fill=none stroke=rgba(246,173,85,0.6) stroke-width=2
      circle cx=200 cy=340 r=28 fill=none stroke=rgba(99,179,237,0.8) stroke-width=1.5
      circle cx=200 cy=340 r=18 fill=url(#gCyan) filter=url(#glow)
      circle cx=200 cy=340 r=10 fill=white opacity=0.95
      !-- Rotor ticks --
      g class=rotor
        line x1=200 y1=304 x2=200 y2=314 stroke=#D4880A stroke-width=2
        line x1=200 y1=366 x2=200 y2=376 stroke=#D4880A stroke-width=2
        line x1=164 y1=340 x2=174 y2=340 stroke=#D4880A stroke-width=2
        line x1=226 y1=340 x2=236 y2=340 stroke=#D4880A stroke-width=2
        line x1=177 y1=317 x2=183 y2=325 stroke=rgba(99,179,237,0.6) stroke-width=1.5
        line x1=223 y1=317 x2=217 y2=325 stroke=rgba(99,179,237,0.6) stroke-width=1.5
        line x1=177 y1=363 x2=183 y2=355 stroke=rgba(99,179,237,0.6) stroke-width=1.5
        line x1=223 y1=363 x2=217 y2=355 stroke=rgba(99,179,237,0.6) stroke-width=1.5
      g

      !-- Side status LEDs --
      circle cx=128 cy=316 r=4 fill=#2F9E44 filter=url(#glow)
        animate attributeName=opacity values=0.3;0.9;0.3 dur=2s repeatCount=indefinite
      circle
      circle cx=272 cy=316 r=4 fill=#3B5BDB filter=url(#glow)
        animate attributeName=opacity values=0.3;0.9;0.3 dur=1.5s repeatCount=indefinite
      circle
      circle cx=128 cy=328 r=3 fill=#D4880A
        animate attributeName=opacity values=0.9;0.2;0.9 dur=0.8s repeatCount=indefinite
      circle
    g

    !-- LEFT ARM --
    g class=arm-l
      rect x=73 y=265 width=24 height=130 rx=11 fill=url(#gMetal) stroke=rgba(99,179,237,0.2) stroke-width=1
      rect x=78 y=265 width=14 height=30 rx=4 fill=url(#gGold) opacity=0.6
      circle cx=85 cy=400 r=14 fill=url(#gMetal) stroke=rgba(246,173,85,0.4) stroke-width=1.5
      circle cx=85 cy=400 r=6 fill=url(#gGold) opacity=0.8
    g

    !-- RIGHT ARM --
    g class=arm-r
      rect x=303 y=265 width=24 height=130 rx=11 fill=url(#gMetal) stroke=rgba(99,179,237,0.2) stroke-width=1
      rect x=308 y=265 width=14 height=30 rx=4 fill=url(#gGold) opacity=0.6
      circle cx=315 cy=400 r=14 fill=url(#gMetal) stroke=rgba(246,173,85,0.4) stroke-width=1.5
      circle cx=315 cy=400 r=6 fill=url(#gGold) opacity=0.8
    g

    !-- LEGS --
    rect x=138 y=440 width=48 height=48 rx=8 fill=url(#gMetal) stroke=rgba(99,179,237,0.15) stroke-width=1
    rect x=214 y=440 width=48 height=48 rx=8 fill=url(#gMetal) stroke=rgba(99,179,237,0.15) stroke-width=1
    rect x=134 y=485 width=58 height=14 rx=7 fill=url(#gGold) opacity=0.7
    rect x=208 y=485 width=58 height=14 rx=7 fill=url(#gGold) opacity=0.7
  svg

  div class=hud◆ J.A.R.V.I.S · NEURAL ENGINE ONLINE ◆div
div

script
const cv = document.getElementById('particles');
const ctx = cv.getContext('2d');
function resize() { cv.width = cv.offsetWidth; cv.height = cv.offsetHeight; }
resize();
window.addEventListener('resize', resize);
const P = Array.from({length35}, () = ({
  x Math.random()cv.width, y Math.random()cv.height,
  vx (Math.random()-0.5)0.35, vy (Math.random()-0.5)0.35,
  r Math.random()1.6+0.4,
  c Math.random()0.5'#3B5BDB''#D4880A'
}));
function tick(){
  ctx.clearRect(0,0,cv.width,cv.height);
  P.forEach(p={
    p.x+=p.vx; p.y+=p.vy;
    if(p.x0p.xcv.width) p.vx=-1;
    if(p.y0p.ycv.height) p.vy=-1;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI2);
    ctx.fillStyle=p.c; ctx.shadowBlur=6; ctx.shadowColor=p.c; ctx.fill();
  });
  for(let i=0;iP.length;i++) for(let j=i+1;jP.length;j++){
    const dx=P[i].x-P[j].x, dy=P[i].y-P[j].y, d=Math.sqrt(dxdx+dydy);
    if(d90){ ctx.strokeStyle=`rgba(59,91,219,${0.15(1-d90)})`; ctx.lineWidth=0.5;
      ctx.beginPath(); ctx.moveTo(P[i].x,P[i].y); ctx.lineTo(P[j].x,P[j].y); ctx.stroke(); }
  }
  requestAnimationFrame(tick);
}
tick();

 Voice greeting
setTimeout(()={
  try {
    const u = new SpeechSynthesisUtterance(Bem-vindo, senhor Sabino. Sistema pronto para autenticação.);
    u.lang=pt-BR; u.rate=0.85; u.pitch=0.5; u.volume=0.8;
    speechSynthesis.speak(u);
  } catch(e){}
}, 1000);
script
body
html


# ============================================================
# SESSION STATE
# ============================================================
if logado not in st.session_state
    st.session_state.logado = False
if chat_history not in st.session_state
    st.session_state.chat_history = []
if df_projetos not in st.session_state
    st.session_state.df_projetos = None

# ============================================================
# LOGIN
# ============================================================
if not st.session_state.logado
    # HUD bar
    st.markdown(
    div style=displayflex;justify-contentspace-between;align-itemscenter;padding10px 20px;
        border1px solid #E2E4EA;border-radius10px;
        background#F8F9FC;backdrop-filterblur(10px);
        margin-bottom28px;font-family'JetBrains Mono',monospace;font-size10px;
        letter-spacing2px;colorrgba(99,179,237,0.5);
      span◆ SABINO OS · v4.0span
      span style=color#2F9E44;● SISTEMA ONLINEspan
      spanAES-256 ENCRYPTEDspan
    div
    , unsafe_allow_html=True)

    col_bot, col_gap, col_form = st.columns([1.05, 0.05, 0.9])

    with col_bot
        components.html(JARVIS_HTML, height=560, scrolling=False)

    with col_form
        st.markdown(
        div style=padding40px 0 24px 0;
          div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing4px;
              color#3B5BDB;margin-bottom12px;● J.A.R.V.I.S ONLINEdiv
          div style=font-family'Syne',sans-serif;font-size42px;font-weight800;
              backgroundlinear-gradient(135deg,#D4880A 0%,#3B5BDB 100%);
              -webkit-background-cliptext;-webkit-text-fill-colortransparent;
              line-height1;margin-bottom8px;SABINObrOSdiv
          p style=color#6B7280;font-size14px;line-height1.7;margin-top12px;
            Bem-vindo, span style=color#D4880A;font-weight600;Senhor Sabinospan.br
            Aguardando autenticação parabracesso ao hub operacional.
          p
        div
        , unsafe_allow_html=True)

        senha = st.text_input(
            CREDENCIAL,
            type=password,
            placeholder=••••••••,
            label_visibility=visible
        )

        if st.button(⚡  AUTENTICAR, use_container_width=True)
            if senha == gsr17
                st.session_state.logado = True
                st.rerun()
            else
                st.markdown(
                div style=backgroundrgba(201,42,42,0.06);border1px solid rgba(201,42,42,0.2);
                    border-radius10px;padding12px 16px;color#C92A2A;font-size13px;margin-top8px;
                  ✗ &nbsp; Credencial inválida. Acesso negado.
                div
                , unsafe_allow_html=True)

        st.markdown(
        div style=margin-top28px;padding16px;border1px solid #E8EAEF;
            border-radius10px;background#F8F9FC;
          div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing2px;
              color#6B7280;line-height2;
            PROTOCOLO · AES-256br
            SESSÃO · MONITORADAbr
            ACESSO · LOG REGISTRADO
          div
        div
        , unsafe_allow_html=True)

    st.stop()

# ============================================================
# DATA LOADING
# ============================================================
STATUS_OPCOES = [Reunião, A Iniciar, Em Andamento, Projetos Futuros, Concluído]
STATUS_COLORS = {
    Reunião         #7048E8,
    A Iniciar       #8BA8C8,
    Em Andamento    #D4880A,
    Projetos Futuros#0C8599,
    Concluído       #2F9E44
}

URL_DB = httpsdocs.google.comspreadsheetsd1SRUQwYW4acuehJ9St0bo2A2AFGW2UDKROzWQ1Y1mBJgedit#gid=0

@st.cache_data(ttl=300)
def carregar_dados()
    colunas = [Projeto,Data Inicial,Prazo,Status,Foco,Escopo,Detalhamento,Resultado Esperado]
    if not LIB_PRONTA
        return pd.DataFrame(columns=colunas)
    try
        conn = st.connection(gsheets, type=GSheetsConnection)
        df = conn.read(spreadsheet=URL_DB, ttl=0)
        if df is not None and not df.empty
            df[Data Inicial] = pd.to_datetime(df[Data Inicial], errors='coerce').fillna(pd.Timestamp.now())
            df[Prazo] = pd.to_datetime(df[Prazo], errors='coerce').fillna(pd.Timestamp.now())
            return df[colunas].dropna(subset=[Projeto])
    except Exception as e
        st.sidebar.error(fErro GSheets {e})
    return pd.DataFrame(columns=colunas)

if st.session_state.df_projetos is None
    st.session_state.df_projetos = carregar_dados()

df = st.session_state.df_projetos

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar
    st.markdown(
    div style=padding0 0 20px 0;
      div style=font-family'JetBrains Mono',monospace;font-size9px;letter-spacing3px;color#3B5BDB;margin-bottom4px;● SISTEMA ATIVOdiv
      div style=font-family'Syne',sans-serif;font-size20px;font-weight800;
          backgroundlinear-gradient(135deg,#D4880A,#3B5BDB);-webkit-background-cliptext;-webkit-text-fill-colortransparent;
          SABINO OSdiv
      div style=font-size11px;color#9CA3AF;margin-top2px;Hub Operacional v4.0div
    div
    , unsafe_allow_html=True)

    st.divider()

    st.markdown(div style='font-size11px;color#9CA3AF;letter-spacing2px;margin-bottom8px;'AÇÕESdiv, unsafe_allow_html=True)

    if st.button(🔄  Sincronizar Dados, use_container_width=True)
        st.cache_data.clear()
        st.session_state.df_projetos = carregar_dados()
        df = st.session_state.df_projetos
        st.success(✓ Sincronizado!)
        st.rerun()

    st.link_button(📝  Editar Planilha, URL_DB, use_container_width=True)

    st.divider()

    if not df.empty
        total = len(df)
        concluidos = len(df[df['Status']=='Concluído'])
        em_exec = len(df[df['Status']=='Em Andamento'])
        taxa = round(concluidostotal100, 1) if total  0 else 0

        st.markdown(f
        div style=displayflex;flex-directioncolumn;gap8px;
          div style=background#FFFFFF;border1px solid #E8EAEF;
              border-radius10px;padding12px 14px;
            div style=font-family'JetBrains Mono',monospace;font-size9px;letter-spacing2px;color#9CA3AF;margin-bottom4px;PROJETOSdiv
            div style=font-family'Syne',sans-serif;font-size22px;font-weight800;color#3B5BDB;{total}div
          div
          div style=background#FFFFFF;border1px solid #E8EAEF;
              border-radius10px;padding12px 14px;
            div style=font-family'JetBrains Mono',monospace;font-size9px;letter-spacing2px;color#9CA3AF;margin-bottom4px;CONCLUSÃOdiv
            div style=font-family'Syne',sans-serif;font-size22px;font-weight800;color#2F9E44;{taxa}%div
          div
          div style=background#FFFFFF;border1px solid #E8EAEF;
              border-radius10px;padding12px 14px;
            div style=font-family'JetBrains Mono',monospace;font-size9px;letter-spacing2px;color#9CA3AF;margin-bottom4px;EM EXECUÇÃOdiv
            div style=font-family'Syne',sans-serif;font-size22px;font-weight800;color#D4880A;{em_exec}div
          div
        div
        , unsafe_allow_html=True)

    st.divider()
    if st.button(🚪  Sair, use_container_width=True)
        st.session_state.logado = False
        st.session_state.df_projetos = None
        st.rerun()

# ============================================================
# HEADER
# ============================================================
now = datetime.now()
st.markdown(f
div style=displayflex;justify-contentspace-between;align-itemscenter;
    padding16px 24px;border1px solid #E2E4EA;border-radius14px;
    background#FFFFFF;
    backdrop-filterblur(10px);margin-bottom24px;
  div
    div style=font-family'JetBrains Mono',monospace;font-size9px;letter-spacing4px;color#3B5BDB;margin-bottom4px;● HUB OPERACIONALdiv
    div style=font-family'Syne',sans-serif;font-size22px;font-weight800;
        backgroundlinear-gradient(135deg,#D4880A,#3B5BDB);-webkit-background-cliptext;-webkit-text-fill-colortransparent;
        GABRIEL SABINOdiv
  div
  div style=text-alignright;font-family'JetBrains Mono',monospace;font-size10px;color#9CA3AF;letter-spacing1px;
    div style=color#2F9E44;margin-bottom4px;● JARVIS ONLINEdiv
    div{now.strftime('%A, %d %b %Y')}div
    div{now.strftime('%H%M')}div
  div
div
, unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    ⚡ VISÃO GERAL,
    📋 KANBAN,
    📊 INTELIGÊNCIA,
    🗂️ DADOS,
    🤖 CHAT IA,
    ✍️ NOTAS
])

# ─────────────────────────────────────────────
# TAB 1 — VISÃO GERAL
# ─────────────────────────────────────────────
with tab1
    if df.empty
        st.warning(Nenhum dado carregado. Sincronize ou verifique a planilha.)
    else
        total = len(df)
        concluidos = len(df[df['Status']=='Concluído'])
        em_exec = len(df[df['Status']=='Em Andamento'])
        backlog = len(df[df['Status']=='A Iniciar'])
        futuros = len(df[df['Status']=='Projetos Futuros'])
        reuniao = len(df[df['Status']=='Reunião'])
        taxa = round(concluidostotal100, 1) if total  0 else 0

        # KPI cards
        cols = st.columns(5)
        kpis = [
            (TOTAL, total, #3B5BDB),
            (EM EXECUÇÃO, em_exec, #D4880A),
            (CONCLUÍDOS, concluidos, #2F9E44),
            (BACKLOG, backlog, #3B5BDB),
            (TAXA, f{taxa}%, #D4880A if taxa  70 else #2F9E44),
        ]
        for i, (label, val, cor) in enumerate(kpis)
            cols[i].markdown(f
            div style=background#F5F6F8;border1px solid #E2E4EA;
                border-radius14px;padding20px 18px;transitionall 0.2s;
                border-top2px solid {cor};box-shadow0 1px 4px rgba(0,0,0,0.05);
              div style=font-family'JetBrains Mono',monospace;font-size9px;letter-spacing2px;color#9CA3AF;margin-bottom8px;{label}div
              div style=font-family'Syne',sans-serif;font-size28px;font-weight800;color{cor};{val}div
            div
            , unsafe_allow_html=True)

        st.markdown(br, unsafe_allow_html=True)

        # Prazos críticos + distribuição
        col_a, col_b = st.columns([1.3, 1])

        with col_a
            st.markdown(
            div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing3px;color#3B5BDB;margin-bottom16px;
            ◆ PRAZOS CRÍTICOS
            div
            , unsafe_allow_html=True)

            ativos = df[df['Status'].isin(['A Iniciar','Em Andamento'])].copy()
            ativos = ativos.sort_values('Prazo').head(6)

            if not ativos.empty
                for _, r in ativos.iterrows()
                    dias = (r['Prazo'] - pd.Timestamp.now()).days
                    cor = #C92A2A if dias  7 else #D4880A if dias  30 else #2F9E44
                    label = URGENTE if dias  7 else ATENÇÃO if dias  30 else OK
                    foco = str(r.get('Foco',''))[30] if pd.notna(r.get('Foco')) else ''
                    st.markdown(f
                    div style=displayflex;align-itemscenter;justify-contentspace-between;
                        background#F8F9FC;border1px solid #E8EAEF;
                        border-left3px solid {cor};border-radius10px;padding12px 16px;margin-bottom8px;
                      div
                        div style=font-weight600;font-size14px;color#1A1D2E;{r['Projeto']}div
                        div style=font-size11px;color#9CA3AF;margin-top2px;{foco} · {r['Prazo'].strftime('%d%m%Y')}div
                      div
                      div style=background{cor};color#F0F1F4;padding4px 10px;border-radius20px;
                          font-family'JetBrains Mono',monospace;font-size10px;font-weight700;
                          white-spacenowrap;margin-left12px;
                        {dias}d · {label}
                      div
                    div
                    , unsafe_allow_html=True)
            else
                st.info(Nenhum projeto ativo com prazo definido.)

        with col_b
            st.markdown(
            div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing3px;color#3B5BDB;margin-bottom16px;
            ◆ DISTRIBUIÇÃO
            div
            , unsafe_allow_html=True)

            dist = df['Status'].value_counts().reindex(STATUS_OPCOES, fill_value=0)
            for status, count in dist.items()
                if count == 0 continue
                pct = count  total  100
                cor = STATUS_COLORS.get(status, #3B5BDB)
                st.markdown(f
                div style=margin-bottom10px;
                  div style=displayflex;justify-contentspace-between;margin-bottom4px;
                    span style=font-size12px;color#6B7280;{status}span
                    span style=font-family'JetBrains Mono',monospace;font-size11px;color{cor};{count}span
                  div
                  div style=background#F0F1F4;border-radius4px;height4px;overflowhidden;
                    div style=background{cor};width{pct.0f}%;height100%;border-radius4px;
                        box-shadow0 0 8px {cor};div
                  div
                div
                , unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 2 — KANBAN
# ─────────────────────────────────────────────
with tab2
    st.markdown(
    div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing3px;color#3B5BDB;margin-bottom20px;
    ◆ FLUXO OPERACIONAL
    div
    , unsafe_allow_html=True)

    if df.empty
        st.warning(Sem dados.)
    else
        cols = st.columns(len(STATUS_OPCOES))
        for i, status in enumerate(STATUS_OPCOES)
            cor = STATUS_COLORS.get(status, #3B5BDB)
            projetos = df[df['Status'] == status]
            count = len(projetos)

            with cols[i]
                st.markdown(f
                div style=background#F8F9FC;border1px solid #E8EAEF;
                    border-top2px solid {cor};box-shadow0 1px 4px rgba(0,0,0,0.05);border-radius12px;padding12px 14px;margin-bottom12px;
                    text-aligncenter;
                  div style=font-size10px;letter-spacing2px;color{cor};
                      font-family'JetBrains Mono',monospace;{status.upper()}div
                  div style=font-family'Syne',sans-serif;font-size20px;font-weight800;color{cor};margin-top2px;{count}div
                div
                , unsafe_allow_html=True)

                for _, row in projetos.iterrows()
                    data_str = pd.to_datetime(row.get('Data Inicial')).strftime('%d%m%Y') if pd.notna(row.get('Data Inicial')) else ''
                    foco = str(row.get('Foco',''))[28] if pd.notna(row.get('Foco')) else ''
                    st.markdown(f
                    div style=background#F8F9FC;border1px solid #E8EAEF;
                        border-left3px solid {cor};border-radius10px;padding12px;margin-bottom8px;
                      div style=font-weight600;font-size13px;color#1A1D2E;margin-bottom4px;
                          line-height1.3;{row['Projeto']}div
                      div style=font-size11px;color#9CA3AF;line-height1.5;
                        📅 {data_str}br🎯 {foco}
                      div
                    div
                    , unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 3 — INTELIGÊNCIA  RESUMO
# ─────────────────────────────────────────────
with tab3
    if df.empty
        st.warning(Sem dados para análise.)
    else
        total = len(df)
        concluidos = len(df[df['Status']=='Concluído'])
        em_exec = len(df[df['Status']=='Em Andamento'])
        backlog = len(df[df['Status']=='A Iniciar'])
        futuros = len(df[df['Status']=='Projetos Futuros'])
        taxa = round(concluidostotal100,1) if total0 else 0
        carga_total = em_exec + backlog

        # Diagnóstico
        if taxa = 70
            diag_cor = #2F9E44; diag_icon = 🟢; diag_txt = Performance Excepcional
            diag_desc = Pipeline acima da média. Momentum positivo.
        elif taxa = 40
            diag_cor = #D4880A; diag_icon = 🟡; diag_txt = Performance Estável
            diag_desc = Há espaço para acelerar o backlog.
        else
            diag_cor = #C92A2A; diag_icon = 🔴; diag_txt = Atenção Requerida
            diag_desc = Revisão estratégica recomendada.

        # Header diagnóstico
        st.markdown(f
        div style=background#F8F9FC;
            border1px solid {diag_cor}33;border-left4px solid {diag_cor};
            border-radius14px;padding20px 24px;margin-bottom24px;
            displayflex;align-itemscenter;justify-contentspace-between;
          div
            div style=font-family'JetBrains Mono',monospace;font-size9px;letter-spacing3px;color#9CA3AF;margin-bottom4px;DIAGNÓSTICO JARVISdiv
            div style=font-family'Syne',sans-serif;font-size20px;font-weight800;color{diag_cor};{diag_icon} {diag_txt}div
            div style=font-size13px;color#6B7280;margin-top4px;{diag_desc}div
          div
          div style=font-family'Syne',sans-serif;font-size48px;font-weight800;color{diag_cor};opacity0.3;{taxa}%div
        div
        , unsafe_allow_html=True)

        # Gráfico de barras por status
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1
            st.markdown(
            div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing3px;color#3B5BDB;margin-bottom16px;
            ◆ VOLUME POR STATUS
            div
            , unsafe_allow_html=True)

            dist = df['Status'].value_counts().reindex(STATUS_OPCOES, fill_value=0)
            max_val = max(dist.values) if max(dist.values)  0 else 1

            for status in STATUS_OPCOES
                count = dist.get(status, 0)
                pct = count  max_val  100
                cor = STATUS_COLORS.get(status, #3B5BDB)
                st.markdown(f
                div style=margin-bottom14px;
                  div style=displayflex;justify-contentspace-between;align-itemscenter;margin-bottom6px;
                    span style=font-size13px;color#6B7280;font-weight500;{status}span
                    span style=font-family'Syne',sans-serif;font-size16px;font-weight800;color{cor};{count}span
                  div
                  div style=background#F5F6F8;border-radius6px;height8px;overflowhidden;
                    div style=backgroundlinear-gradient(90deg,{cor},{cor}88);width{pct.0f}%;height100%;
                        border-radius6px;box-shadow0 0 10px {cor}55;
                        transitionwidth 0.8s ease;div
                  div
                div
                , unsafe_allow_html=True)

        with col_graf2
            st.markdown(
            div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing3px;color#3B5BDB;margin-bottom16px;
            ◆ PAINEL DE CARGA
            div
            , unsafe_allow_html=True)

            # Donut-style stats
            metricas = [
                (Em Execução, em_exec, #D4880A),
                (Backlog, backlog, #3B5BDB),
                (Futuros, futuros, #0C8599),
                (Reuniões, len(df[df['Status']=='Reunião']), #7048E8),
                (Concluídos, concluidos, #2F9E44),
            ]
            for label, val, cor in metricas
                pct_circle = val  total  100 if total  0 else 0
                st.markdown(f
                div style=displayflex;align-itemscenter;background#F8F9FC;
                    border1px solid #E8EAEF;border-radius10px;padding12px 14px;margin-bottom8px;
                  div style=width8px;height8px;border-radius50%;background{cor};
                      box-shadow0 0 8px {cor};margin-right12px;flex-shrink0;div
                  div style=flex1;
                    div style=font-size12px;color#6B7280;{label}div
                    div style=background#F5F6F8;border-radius3px;height3px;margin-top4px;
                      div style=background{cor};width{pct_circle.0f}%;height100%;border-radius3px;div
                    div
                  div
                  div style=font-family'Syne',sans-serif;font-size18px;font-weight800;color{cor};margin-left12px;{val}div
                div
                , unsafe_allow_html=True)

        st.markdown(br, unsafe_allow_html=True)

        # Timeline dos projetos ativos
        st.markdown(
        div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing3px;color#3B5BDB;margin-bottom16px;
        ◆ RADAR DE PROJETOS ATIVOS
        div
        , unsafe_allow_html=True)

        ativos = df[df['Status'].isin(['A Iniciar','Em Andamento','Reunião'])].sort_values('Prazo').head(8)
        if not ativos.empty
            cols_radar = st.columns(2)
            for idx, (_, row) in enumerate(ativos.iterrows())
                dias = (row['Prazo'] - pd.Timestamp.now()).days
                cor = #C92A2A if dias  7 else #D4880A if dias  30 else #2F9E44
                status_cor = STATUS_COLORS.get(row['Status'], #3B5BDB)
                escopo = str(row.get('Escopo',''))[60] if pd.notna(row.get('Escopo')) else ''

                with cols_radar[idx % 2]
                    st.markdown(f
                    div style=background#F8F9FC;border1px solid #E8EAEF;
                        border-radius12px;padding16px;margin-bottom10px;
                      div style=displayflex;justify-contentspace-between;align-itemsflex-start;margin-bottom8px;
                        div style=font-weight600;font-size14px;color#1A1D2E;flex1;padding-right8px;{row['Projeto']}div
                        span style=background{status_cor}22;color{status_cor};border1px solid {status_cor}44;
                            padding3px 8px;border-radius20px;font-size10px;white-spacenowrap;
                            font-family'JetBrains Mono',monospace;{row['Status']}span
                      div
                      div style=font-size12px;color#9CA3AF;margin-bottom10px;line-height1.5;{escopo}div
                      div style=displayflex;justify-contentspace-between;align-itemscenter;
                        span style=font-size11px;color#9CA3AF;📅 {row['Prazo'].strftime('%d%m%Y')}span
                        span style=background{cor}22;color{cor};padding2px 8px;border-radius10px;
                            font-family'JetBrains Mono',monospace;font-size10px;{dias}dspan
                      div
                    div
                    , unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 4 — DADOS BRUTOS
# ─────────────────────────────────────────────
with tab4
    st.markdown(
    div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing3px;color#3B5BDB;margin-bottom16px;
    ◆ BANCO DE DADOS OPERACIONAL
    div
    , unsafe_allow_html=True)

    if df.empty
        st.warning(Sem dados carregados.)
    else
        st.dataframe(df, use_container_width=True, height=500)

# ─────────────────────────────────────────────
# TAB 5 — CHAT IA ESTRATÉGICO
# ─────────────────────────────────────────────
# TAB 5 — CHAT IA
# ─────────────────────────────────────────────
with tab5
    # Header
    st.markdown(
    div style=displayflex;align-itemscenter;justify-contentspace-between;margin-bottom24px;
        padding-bottom16px;border-bottom1px solid #E2E4EA;
      div style=displayflex;align-itemscenter;gap10px;
        div style=width32px;height32px;background#3B5BDB;border-radius8px;
            displayflex;align-itemscenter;justify-contentcenter;font-size14px;🤖div
        div
          div style=font-weight700;font-size15px;color#1A1D2E;J.A.R.V.I.Sdiv
          div style=font-size11px;color#6B7280;Consultor estratégico · contexto do seu portfóliodiv
        div
      div
      div style=displayflex;align-itemscenter;gap6px;
        div style=width7px;height7px;background#2F9E44;border-radius50%;div
        span style=font-size11px;color#6B7280;font-family'JetBrains Mono',monospace;ONLINEspan
      div
    div
    , unsafe_allow_html=True)

    # Sugestões de perguntas
    sugestoes = [
        📌  Qual projeto tem maior risco de atraso,
        🎯  Onde focar energia essa semana,
        📊  Diagnóstico geral do portfólio,
        ⚡  Quais projetos posso acelerar,
        🔍  Identifique gargalos,
        📅  O que vence nos próximos 30 dias,
    ]

    pergunta_sugerida = None
    if not st.session_state.chat_history
        st.markdown(
        div style=font-size11px;color#9CA3AF;letter-spacing0.5px;margin-bottom10px;font-weight500;
        SUGESTÕES RÁPIDAS
        div
        , unsafe_allow_html=True)
        cols_s = st.columns(3)
        for i, s in enumerate(sugestoes)
            with cols_s[i % 3]
                if st.button(s, key=fsug_{i}, use_container_width=True)
                    pergunta_sugerida = s.split(  , 1)[-1]  # remove emoji prefix

    # Chat history
    if st.session_state.chat_history
        for msg in st.session_state.chat_history
            if msg[role] == user
                st.markdown(f
                div style=displayflex;justify-contentflex-end;margin12px 0;
                  div style=background#3B5BDB;color#fff;border-radius12px 12px 3px 12px;
                      padding10px 16px;max-width70%;font-size14px;line-height1.5;
                    {msg['content']}
                  div
                div
                , unsafe_allow_html=True)
            else
                # Render AI response with st.markdown for proper markdown support
                st.markdown(f
                div style=displayflex;align-itemsflex-start;gap8px;margin12px 0;
                  div style=width26px;height26px;background#3B5BDB;border-radius6px;flex-shrink0;
                      displayflex;align-itemscenter;justify-contentcenter;font-size11px;margin-top2px;🤖div
                  div style=background#FFFFFF;border1px solid #E2E4EA;border-radius3px 12px 12px 12px;
                      padding14px 18px;max-width85%;font-size14px;line-height1.7;color#1A1D2E;
                      box-shadow0 1px 4px rgba(0,0,0,0.06);
                    {msg['content'].replace(chr(10), 'br')}
                  div
                div
                , unsafe_allow_html=True)

    st.markdown(div style='height16px'div, unsafe_allow_html=True)

    # Input area
    col_input, col_btn = st.columns([6, 1])
    with col_input
        user_input = st.text_input(
            msg,
            value=pergunta_sugerida or ,
            placeholder=Pergunte algo sobre seus projetos...,
            label_visibility=collapsed,
            key=chat_input
        )
    with col_btn
        enviar = st.button(Enviar, use_container_width=True)

    if st.session_state.chat_history
        if st.button(🗑  Limpar, use_container_width=False)
            st.session_state.chat_history = []
            st.rerun()
    if (enviar or pergunta_sugerida) and (user_input or pergunta_sugerida)
        query = user_input or pergunta_sugerida

        # Prepare context from df
        if not df.empty
            projetos_ctx = []
            for _, row in df.iterrows()
                dias_prazo = (row['Prazo'] - pd.Timestamp.now()).days
                projetos_ctx.append({
                    projeto row.get('Projeto',''),
                    status row.get('Status',''),
                    foco str(row.get('Foco','')) if pd.notna(row.get('Foco')) else '',
                    escopo str(row.get('Escopo','')) if pd.notna(row.get('Escopo')) else '',
                    resultado_esperado str(row.get('Resultado Esperado','')) if pd.notna(row.get('Resultado Esperado')) else '',
                    dias_para_prazo dias_prazo,
                    prazo row['Prazo'].strftime('%d%m%Y')
                })
            ctx_str = json.dumps(projetos_ctx, ensure_ascii=False, indent=1)
        else
            ctx_str = Nenhum projeto carregado no momento.

        system_prompt = fVocê é J.A.R.V.I.S, o assistente estratégico de Gabriel Sabino — um consultor executivo de alta performance.

Você tem acesso ao portfólio de projetos de Gabriel
{ctx_str}

Regras
- Seja direto, preciso e estratégico. Zero enrolação.
- Use dados concretos do portfólio para embasar cada resposta.
- Formate com emojis, negrito e quebras de linha para facilitar leitura.
- Dê recomendações acionáveis e prioritizadas.
- Se identificar riscos, seja claro sobre impacto e urgência.
- Máximo de 400 palavras por resposta.
- Fale sempre em português brasileiro.

        st.session_state.chat_history.append({role user, content query})

        # Build messages for API
        messages = []
        for m in st.session_state.chat_history
            messages.append({role m[role], content m[content]})

        with st.spinner(J.A.R.V.I.S processando...)
            try
                import requests
                resp = requests.post(
                    httpsapi.anthropic.comv1messages,
                    headers={
                        Content-Type applicationjson,
                        x-api-key ,
                        anthropic-version 2023-06-01
                    },
                    json={
                        model claude-haiku-4-5-20251001,
                        max_tokens 800,
                        system system_prompt,
                        messages messages
                    },
                    timeout=45
                )
                data = resp.json()
                if data.get(content)
                    answer = data[content][0][text]
                elif data.get(error)
                    answer = f⚠️ API {data['error'].get('message','Erro desconhecido')}
                else
                    answer = f⚠️ Resposta inesperada {str(data)[200]}
            except Exception as e
                answer = f⚠️ Erro {str(e)}

        st.session_state.chat_history.append({role assistant, content answer})
        st.rerun()

    if st.session_state.chat_history
        if st.button(🗑️ Limpar conversa, use_container_width=False)
            st.session_state.chat_history = []
            st.rerun()

# ─────────────────────────────────────────────
# TAB 6 — NOTAS
# ─────────────────────────────────────────────
with tab6
    st.markdown(
    div style=font-family'JetBrains Mono',monospace;font-size10px;letter-spacing3px;color#3B5BDB;margin-bottom16px;
    ◆ NOTAS ESTRATÉGICAS
    div
    , unsafe_allow_html=True)

    st.text_area(
        Espaço livre para anotações, ideias e contexto,
        height=500,
        placeholder=Escreva suas anotações aqui...nnDicas estratégias, insights, próximos passos, contexto de reuniões...,
        label_visibility=visible
    )

    st.markdown(
    div style=font-family'JetBrains Mono',monospace;font-size9px;letter-spacing1px;color#9CA3AF;margin-top8px;text-alignright;
    ⚠ Notas são locais e não são salvas entre sessões
    div
    , unsafe_allow_html=True)
