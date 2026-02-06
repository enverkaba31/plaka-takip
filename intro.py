import streamlit as st
import time
import base64
import random

def get_base64_of_bin_file(bin_file):
    """Resmi HTML içinde göstermek için şifreler"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def intro_yap():
    """
    Site açılışında logo yağmuru ve hoşgeldin yazısı.
    """
    
    # Eğer intro daha önce yapıldıysa tekrar yapma (Sayfa yenilenince çalışmasın)
    if 'intro_yapildi' in st.session_state and st.session_state['intro_yapildi']:
        return

    # Intro alanı (Boş bir kutu oluşturuyoruz)
    intro_placeholder = st.empty()
    
    try:
        img_b64 = get_base64_of_bin_file("fotograflar/bclogo.jpeg")
    except:
        # Resim yoksa intro yapmadan geç
        st.session_state['intro_yapildi'] = True
        return

    # --- HTML & CSS ANİMASYONU ---
    # Rastgele pozisyonlarda baloncuklar oluştur
    baloncuklar_html = ""
    for i in range(25): # 25 tane baloncuk
        left_pos = random.randint(0, 90) # Ekranın %0 ile %90'ı arasında
        delay = random.uniform(0, 1.5) # Rastgele gecikme
        duration = random.uniform(2, 4) # Rastgele düşüş hızı
        size = random.randint(40, 100) # Rastgele boyut
        
        baloncuklar_html += f"""
        <div class="bubble" style="left: {left_pos}%; animation-delay: {delay}s; animation-duration: {duration}s; width: {size}px; height: {size}px;">
            <img src="data:image/jpeg;base64,{img_b64}">
        </div>
        """

    full_html = f"""
    <style>
        /* Tam Ekran Kaplama */
        #intro-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: #0e1117; /* Sitenin arka plan rengi */
            z-index: 999999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }}
        
        /* Hoşgeldin Yazısı */
        .welcome-text {{
            font-size: 80px;
            font-weight: bold;
            color: white;
            text-shadow: 0 0 20px #FF4B4B;
            z-index: 10;
            animation: fadeIn 1s ease-in-out;
            font-family: sans-serif;
        }}

        /* Baloncuk Stili */
        .bubble {{
            position: absolute;
            top: -150px; /* Ekranın üstünden başla */
            border-radius: 50%;
            overflow: hidden;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
            animation-name: fall;
            animation-timing-function: linear;
            animation-fill-mode: forwards;
        }}
        
        .bubble img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        /* Düşme Animasyonu */
        @keyframes fall {{
            0% {{ top: -150px; opacity: 1; transform: rotate(0deg); }}
            80% {{ opacity: 1; }}
            100% {{ top: 110%; opacity: 0; transform: rotate(360deg); }} /* Ekranın altına git */
        }}
        
        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: scale(0.5); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
    </style>

    <div id="intro-overlay">
        <div class="welcome-text">HOŞ GELDİNİZ</div>
        {baloncuklar_html}
    </div>
    """

    # HTML'i ekrana bas
    with intro_placeholder.container():
        st.markdown(full_html, unsafe_allow_html=True)
    
    # 3.5 saniye bekle (Animasyon sürsün)
    time.sleep(3.5)
    
    # İntroyu temizle
    intro_placeholder.empty()
    
    # İntro bitti diye işaretle
    st.session_state['intro_yapildi'] = True
    
    # Finalde konfetiler patlasın (Streamlit'in kendi efekti)
    st.balloons()
