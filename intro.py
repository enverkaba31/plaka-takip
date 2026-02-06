import streamlit as st
import time
import base64
import random
import os

def get_base64_of_bin_file(bin_file):
    """Resmi HTML içinde göstermek için şifreler"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

def intro_yap():
    """
    Site açılışında logo yağmuru ve hoşgeldin yazısı.
    """
    
    # Session State kontrolü: İntro yapıldıysa tekrar yapma
    if 'intro_yapildi' in st.session_state and st.session_state['intro_yapildi']:
        return

    # Intro alanı
    intro_placeholder = st.empty()
    
    # Resmi bul ve şifrele
    img_path = "fotograflar/bclogo.jpeg"
    if not os.path.exists(img_path):
        # Resim yoksa intro yapmadan geç
        st.session_state['intro_yapildi'] = True
        return
        
    img_b64 = get_base64_of_bin_file(img_path)
    if not img_b64:
        return

    # --- HTML & CSS ANİMASYONU ---
    
    # Baloncukları oluştur (Resmi her seferinde gömmek yerine CSS Class kullanacağız)
    baloncuklar_html = ""
    for i in range(25): # 25 Baloncuk
        left_pos = random.randint(0, 95)
        delay = random.uniform(0, 2)
        duration = random.uniform(3, 5)
        size = random.randint(50, 120)
        
        # Sadece boş div oluşturuyoruz, resmi CSS ile vereceğiz
        baloncuklar_html += f"""
        <div class="bubble" style="left: {left_pos}%; animation-delay: {delay}s; animation-duration: {duration}s; width: {size}px; height: {size}px;"></div>
        """

    full_html = f"""
    <style>
        #intro-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #0e1117;
            z-index: 999999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }}
        
        .welcome-text {{
            font-size: 80px;
            font-weight: bold;
            color: white;
            text-shadow: 0 0 20px #FF4B4B;
            z-index: 10;
            animation: fadeIn 1s ease-in-out;
            font-family: sans-serif;
            text-align: center;
        }}

        /* Resmi burada TEK SEFER tanımlıyoruz */
        .bubble {{
            position: absolute;
            top: -150px;
            border-radius: 50%;
            background-image: url('data:image/jpeg;base64,{img_b64}'); /* Resim burada */
            background-size: cover;
            background-position: center;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
            opacity: 0.8;
            animation-name: fall;
            animation-timing-function: linear;
            animation-fill-mode: forwards;
        }}

        @keyframes fall {{
            0% {{ top: -150px; transform: rotate(0deg); }}
            100% {{ top: 110%; transform: rotate(360deg); }}
        }}
        
        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: scale(0.5); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
    </style>

    <div id="intro-overlay">
        <div class="welcome-text">HOŞ GELDİNİZ<br><span style="font-size:30px; color:#aaa;">BC EKİBİ</span></div>
        {baloncuklar_html}
    </div>
    """

    # HTML'i ekrana bas
    with intro_placeholder.container():
        st.markdown(full_html, unsafe_allow_html=True)
    
    # Bekle
    time.sleep(4.5)
    
    # Temizle
    intro_placeholder.empty()
    st.session_state['intro_yapildi'] = True
    st.balloons()
