import streamlit as st
import time
import random
import datetime

def intro_yap():
    if 'intro_yapildi' in st.session_state and st.session_state['intro_yapildi']:
        return

    intro_placeholder = st.empty()

    # --- GÜN MESAJI ---
    gunler = {
        'Monday': 'PAZARTESİLER', 'Tuesday': 'SALILAR', 'Wednesday': 'ÇARŞAMBALAR',
        'Thursday': 'PERŞEMBELER', 'Friday': 'CUMALAR', 'Saturday': 'CUMARTESİLER', 'Sunday': 'PAZARLAR'
    }
    bugun = datetime.datetime.today().strftime('%A')
    mesaj = f"HAYIRLI<br>{gunler.get(bugun, 'GÜNLER')}"

    # --- ARKA PLAN YAZILARI ---
    bg_html = ""
    for _ in range(40):
        t, l, s = random.randint(0, 95), random.randint(0, 95), random.randint(15, 35)
        o, r = random.uniform(0.1, 0.3), random.randint(-30, 30)
        bg_html += f'<div style="position:absolute; top:{t}%; left:{l}%; font-size:{s}px; opacity:{o}; transform:rotate({r}deg); color:#444; white-space:nowrap;">HOŞ GELDİNİZ</div>'

    # --- BALONCUKLAR ---
    bub_html = ""
    for _ in range(50):
        l, d, dur, sz = random.randint(1, 98), random.uniform(0, 1.5), random.uniform(2, 4), random.randint(20, 80)
        anim = random.choice(["moveDown", "moveUp"])
        color = random.choice(["#00aeff", "#ffffff", "#00ff96", "#ff4b4b"])
        bub_html += f'<div class="bubble" style="left:{l}%; width:{sz}px; height:{sz}px; background:{color}; animation:{anim} {dur}s ease-in infinite; animation-delay:{d}s;"></div>'

    # --- CSS & HTML ---
    full_code = f"""
    <style>
        #intro-overlay {{ position:fixed; top:0; left:0; width:100vw; height:100vh; background:#0e1117; z-index:999999; display:flex; flex-direction:column; justify-content:center; align-items:center; overflow:hidden; }}
        .center-msg {{ font-size:70px; font-weight:900; color:#fff; text-align:center; z-index:100; text-shadow:0 0 40px #FF4B4B; animation:pulse 1s infinite alternate; font-family:sans-serif; line-height:1.1; }}
        .bubble {{ position:absolute; border-radius:50%; opacity:0.6; box-shadow:inset 0 0 10px rgba(255,255,255,0.3); z-index:50; }}
        @keyframes moveDown {{ 0% {{ top:-10%; }} 100% {{ top:110%; }} }}
        @keyframes moveUp {{ 0% {{ bottom:-10%; }} 100% {{ bottom:110%; }} }}
        @keyframes pulse {{ from {{ transform:scale(1); }} to {{ transform:scale(1.05); }} }}
    </style>
    <div id="intro-overlay">
        {bg_html}
        <div class="center-msg">{mesaj}</div>
        {bub_html}
    </div>
    """
    
    with intro_placeholder.container():
        st.markdown(full_code, unsafe_allow_html=True)
    
    time.sleep(4)
    intro_placeholder.empty()
    st.session_state['intro_yapildi'] = True
    st.balloons()
