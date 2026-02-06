import streamlit as st
import time
import base64
import random
import os

def get_base64_of_bin_file(bin_file):
    """Resmi şifreler ve satır sonlarını temizler (Yazı hatasını önler)"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode().replace("\n", "")
    except:
        return None

def intro_yap():
    """
    Optimize edilmiş intro. Resmi sadece CSS'e gömer.
    """
    
    # Daha önce yapıldıysa tekrar çalışma
    if 'intro_yapildi' in st.session_state and st.session_state['intro_yapildi']:
        return

    intro_placeholder = st.empty()
    
    # Resmi al
    img_path = "fotograflar/bclogo.jpeg"
    img_b64 = None
    
    if os.path.exists(img_path):
        img_b64 = get_base64_of_bin_file(img_path)
    
    # Resim yoksa veya hata varsa introyu geç
    if not img_b64:
        st.session_state['intro_yapildi'] = True
        return

    # --- BALONCUKLARI OLUŞTUR ---
    # Not: Burada img tag'i YOK. Sadece boş kutular var. Resmi CSS verecek.
    baloncuklar_html = ""
    for i in range(20): # 20 Baloncuk yeterli
        left_pos = random.randint(5, 95)
        delay = random.uniform(0, 1.5)
        duration = random.uniform(3, 5)
        size = random.randint(60, 120)
        
        baloncuklar_html += f"""
        <div class="bubble" style="left: {left_pos}%; animation-delay: {delay}s; animation-duration: {duration}s; width: {size}px; height: {size}px;"></div>
        """

    # --- TEK SEFERLİK CSS TANIMI ---
    full_html = f"""
    <style>
        #intro-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #0e1117; z-index: 999999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }}
        
        .welcome-text {{
            font-size: 80px; font-weight: bold; color: white;
            text-shadow: 0 0 20px #FF4B4B; z-index: 10;
            animation: fadeIn 1s ease-in-out; text-align: center;
        }}
        
        /* İŞTE SİHİR BURADA: Resim sadece burada tanımlı */
        .bubble {{
            position: absolute; top: -150px;
            background-image: url('data:image/jpeg;base64,{img_b64}');
            background-size: cover; background-position: center;
            border-radius: 50%;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
            opacity: 0.9;
            animation-name: fall; animation-timing-function: linear; animation-fill-mode: forwards;
        }}

        @keyframes fall {{
            0% {{ top: -150px; transform: rotate(0deg); }}
            100% {{ top: 110vh; transform: rotate(360deg); }}
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    </style>

    <div id="intro-overlay">
        <div class="welcome-text">HOŞ GELDİNİZ<br><span style="font-size:30px; color:#ccc;">BC EKİBİ</span></div>
        {baloncuklar_html}
    </div>
    """

    with intro_placeholder.container():
        st.markdown(full_html, unsafe_allow_html=True)
    
    time.sleep(4)
    intro_placeholder.empty()
    st.session_state['intro_yapildi'] = True
    st.balloons()
