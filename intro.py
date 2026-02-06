import streamlit as st
import time
import base64
import random
import os

def get_base64_of_bin_file(bin_file):
    """Resmi HTML içinde göstermek için şifreler ve SATIR ATLAMA KARAKTERLERİNİ TEMİZLER"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        # .replace("\n", "") kısmı o ekrana dökülen yazıları engeller
        return base64.b64encode(data).decode().replace("\n", "")
    except:
        return None

def intro_yap():
    """
    Site açılışında logo yağmuru ve hoşgeldin yazısı.
    """
    
    if 'intro_yapildi' in st.session_state and st.session_state['intro_yapildi']:
        return

    # Intro alanı
    intro_placeholder = st.empty()
    
    img_path = "fotograflar/bclogo.jpeg"
    if not os.path.exists(img_path):
        st.session_state['intro_yapildi'] = True
        return
        
    img_b64 = get_base64_of_bin_file(img_path)
    if not img_b64:
        st.session_state['intro_yapildi'] = True
        return

    # --- BALONCUKLARI OLUŞTUR ---
    baloncuklar_html = ""
    for i in range(30): # 30 Baloncuk
        left_pos = random.randint(1, 95)
        delay = random.uniform(0, 1.5)
        duration = random.uniform(2.5, 4.5)
        size = random.randint(60, 130)
        
        # Resmi CSS ile değil, doğrudan img etiketiyle veriyoruz (Daha garanti)
        # Ancak bu sefer base64 temizlendiği için sorun çıkarmayacak
        baloncuklar_html += f"""
        <div class="bubble" style="left: {left_pos}%; animation-delay: {delay}s; animation-duration: {duration}s; width: {size}px; height: {size}px;">
            <img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
        </div>
        """

    full_html = f"""
    <style>
        /* Siyah perde - En üst katman */
        #intro-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #0e1117;
            z-index: 9999999; /* Çok yüksek Z-Index */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }}
        
        .welcome-container {{
            text-align: center;
            z-index: 10;
            animation: fadeIn 1.5s ease-in-out;
        }}

        .welcome-text {{
            font-size: 80px;
            font-weight: 900;
            color: #ffffff;
            text-shadow: 0 0 25px #FF4B4B;
            font-family: 'Arial', sans-serif;
            margin: 0;
            line-height: 1.2;
        }}
        
        .sub-text {{
            font-size: 30px;
            color: #cccccc;
            margin-top: 10px;
            font-weight: 300;
            letter-spacing: 5px;
        }}

        .bubble {{
            position: absolute;
            top: -150px;
            border-radius: 50%;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
            opacity: 0.9;
            animation-name: fall;
            animation-timing-function: linear;
            animation-fill-mode: forwards;
        }}

        @keyframes fall {{
            0% {{ top: -150px; transform: rotate(0deg); }}
            100% {{ top: 110vh; transform: rotate(360deg); }}
        }}
        
        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: scale(0.8); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
    </style>

    <div id="intro-overlay">
        <div class="welcome-container">
            <div class="welcome-text">HOŞ GELDİNİZ</div>
            <div class="sub-text">BC EKİBİ</div>
        </div>
        {baloncuklar_html}
    </div>
    """

    # HTML'i ekrana bas
    with intro_placeholder.container():
        st.markdown(full_html, unsafe_allow_html=True)
    
    # 4 saniye bekle
    time.sleep(4)
    
    # Temizle
    intro_placeholder.empty()
    st.session_state['intro_yapildi'] = True
    st.balloons()
