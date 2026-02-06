import streamlit as st
import time
import random
import datetime

def intro_yap():
    """
    Resimsiz, dinamik gün mesajlı ve 'bomba' efektli intro.
    """
    
    if 'intro_yapildi' in st.session_state and st.session_state['intro_yapildi']:
        return

    intro_placeholder = st.empty()

    # --- 1. GÜNÜ BELİRLE VE MESAJI OLUŞTUR ---
    bugun = datetime.datetime.today().strftime('%A')
    
    gunler_tr = {
        'Monday': 'PAZARTESİLER',
        'Tuesday': 'SALILAR',
        'Wednesday': 'ÇARŞAMBALAR',
        'Thursday': 'PERŞEMBELER',
        'Friday': 'CUMALAR',
        'Saturday': 'CUMARTESİLER',
        'Sunday': 'PAZARLAR'
    }
    
    secilen_gun = gunler_tr.get(bugun, 'GÜNLER')
    ana_mesaj = f"HAYIRLI<br>{secilen_gun}"

    # --- 2. RASTGELE "HOŞ GELDİNİZ" YAZILARI ---
    bg_text_html = ""
    for _ in range(30): # 30 tane arka plan yazısı
        top = random.randint(0, 90)
        left = random.randint(0, 90)
        size = random.randint(10, 30)
        opacity = random.uniform(0.1, 0.3) # Silik olsun
        rotation = random.randint(-45, 45)
        
        bg_text_html += f"""
        <div style="position: absolute; top: {top}%; left: {left}%; font-size: {size}px; 
                    opacity: {opacity}; transform: rotate({rotation}deg); color: gray; font-family: monospace;">
            HOŞ GELDİNİZ
        </div>
        """

    # --- 3. BALONCUKLARI OLUŞTUR (YUKARI VE AŞAĞI) ---
    baloncuklar_html = ""
    for i in range(40): # 40 tane baloncuk
        left_pos = random.randint(1, 98)
        delay = random.uniform(0, 1.5)
        duration = random.uniform(2, 3.5)
        size = random.randint(20, 80)
        
        # Yazı tura at: %50 ihtimalle yukarıdan, %50 aşağıdan gelsin
        yon = random.choice(["moveDown", "moveUp"])
        
        # Renk (Mavi ve Beyaz tonları)
        renk = random.choice(["rgba(0, 174, 255, 0.6)", "rgba(255, 255, 255, 0.5)", "rgba(0, 255, 150, 0.5)"])
        
        baloncuklar_html += f"""
        <div class="bubble" style="
            left: {left_pos}%; 
            width: {size}px; height: {size}px; 
            background: {renk};
            animation: {yon} {duration}s ease-in infinite; 
            animation-delay: {delay}s;">
        </div>
        """

    # --- CSS ve HTML ---
    full_html = f"""
    <style>
        #intro-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #0e1117; z-index: 999999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            overflow: hidden;
        }}
        
        /* Ana Mesaj (Ortadaki) */
        .center-msg {{
            font-size: 70px; font-weight: 900; color: #fff;
            text-align: center; z-index: 50;
            text-shadow: 0 0 30px #FF4B4B, 0 0 60px #FF4B4B;
            animation: pulse 1s infinite alternate;
            line-height: 1.1;
        }}

        /* Baloncuk Stili */
        .bubble {{
            position: absolute;
            border-radius: 50%;
            box-shadow: inset 0 0 10px rgba(255,255,255,0.5);
            backdrop-filter: blur(2px);
            z-index: 40;
        }}

        /* Animasyonlar */
        @keyframes moveDown {{
            0% {{ top: -10%; opacity: 1; transform: scale(1); }}
            80% {{ opacity: 0.8; transform: scale(1.2); }}
            100% {{ top: 110%; opacity: 0; transform: scale(3); }} /* Patlama efekti (büyüyüp kaybolma) */
        }}

        @keyframes moveUp {{
            0% {{ bottom: -10%; opacity: 1; transform: scale(1); }}
            80% {{ opacity: 0.8; transform: scale(1.2); }}
            100% {{ bottom: 110%; opacity: 0; transform: scale(3); }} /* Patlama efekti */
        }}
        
        @keyframes pulse {{
            from {{ transform: scale(1); text-shadow: 0 0 20px #FF4B4B; }}
            to {{ transform: scale(1.1); text-shadow: 0 0 50px #FF0000; }}
        }}
    </style>

    <div id="intro-overlay">
        {bg_text_html}
        
        <div class="center-msg">{ana_mesaj}</div>
        
        {baloncuklar_html}
    </div>
    """

    with intro_placeholder.container():
        st.markdown(full_html, unsafe_allow_html=True)
    
    # 4 saniye oynat
    time.sleep(4)
    
    # Temizle ve Siteyi Aç
    intro_placeholder.empty()
    st.session_state['intro_yapildi'] = True
    
    # Konfetilerle Final
    st.balloons()
