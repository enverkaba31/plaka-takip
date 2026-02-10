import streamlit as st
import os
import random

def radyo_widget():
    # 1. Klasör Ayarları
    MUZIK_KLASORU = "muzikler"
    
    # Klasör yoksa uyarı ver ve çık
    if not os.path.exists(MUZIK_KLASORU):
        st.warning(f"⚠️ '{MUZIK_KLASORU}' klasörü bulunamadı. Lütfen oluşturun.")
        return

    # Müzik dosyalarını çek
    sarkilar = [f for f in os.listdir(MUZIK_KLASORU) if f.endswith(('.mp3', '.wav', '.ogg'))]
    
    if not sarkilar:
        st.info("Radio Silent... 📻 (Klasör boş)")
        return

    # 2. Session State Yönetimi (Hafıza)
    # Eğer daha önce bir şarkı seçilmediyse veya 'degistir' komutu geldiyse yeni seç
    if 'calan_sarki' not in st.session_state:
        st.session_state['calan_sarki'] = random.choice(sarkilar)
    
    # 3. Arayüz
    secilen = st.session_state['calan_sarki']
    dosya_yolu = os.path.join(MUZIK_KLASORU, secilen)
    
    with st.container():
        # Başlık ve Buton Yan Yana
        c1, c2 = st.columns([3, 1])
        
        with c1:
            st.markdown(f"### 📻 {secilen}")
            # Audio player
            st.audio(dosya_yolu, format="audio/mp3")
            
        with c2:
            st.write("") # Hizalama için boşluk
            st.write("")
            # Bu butona basınca şarkıyı hafızadan silip sayfayı yeniliyoruz
            # Böylece yukarıdaki 'if' bloğu tekrar çalışıp yeni rastgele şarkı seçiyor.
            if st.button("Kanal Değiştir ⏭️"):
                yeni_sarki = random.choice(sarkilar)
                # Aynı şarkının gelmesini engellemek için basit döngü
                while len(sarkilar) > 1 and yeni_sarki == st.session_state['calan_sarki']:
                    yeni_sarki = random.choice(sarkilar)
                
                st.session_state['calan_sarki'] = yeni_sarki
                st.rerun()
