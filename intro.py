import streamlit as st
import time
import base64
import random
import os

def get_base64_of_bin_file(bin_file):
    """Resmi şifreler ve satır sonlarını temizler"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode().replace("\n", "")
    except:
        return None

def intro_yap():
    """
    Logoların görünmesi için boşlukları temizlenmiş intro.
    """
    
    if 'intro_yapildi' in st.session_state and st.session_state['intro_yapildi']:
        return

    intro_placeholder = st.empty()
    
    # Resmi al
    img_path = "fotograflar/bclogo.jpeg"
    img_b64 = None
    
    if os.path.exists(img_path):
        img_b64 = get_base64_of_bin_file(img_path)
    
    # Resim yoksa introyu geç
    if not img_b64:
        st.session_state['intro_yapildi'] = True
        return

    # --- BALONCUKLARI OLUŞTUR ---
    # DÜZELTME: HTML kodunu tek satırda birleştiriyoruz ki Markdown bunu "Kod Bloğu" sanmasın.
    baloncuklar_html = ""
    for i in range(25): 
        left_pos = random.randint(5, 95)
        delay = random.uniform(0, 1.5)
        duration = random.uniform(3, 5)
        size = random.randint(60, 120)
        
        # F-String içindeki girintileri sildim
        baloncuklar_html += f'<div class="bubble" style="left: {left_pos}%; animation-delay: {delay}s; animation-duration: {duration}s; width: {size}px; height: {size}px;"></div>'

    # --- CSS VE HTML ---
    full_html = f"""
    <style>
        #intro-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #0e1117; z-index: 999999;
            display: flex; flex-
