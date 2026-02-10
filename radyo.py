import streamlit as st
import os
import random

def radyo_widget():
    """
    Klasördeki müzikleri tarar ve rastgele birini çalar.
    Şarkı değişmemesi için (sayfa yenilenmedikçe) session_state kullanır.
    """
    
    # 1. Müzik Klasörü Kontrolü
    MUZIK_KLASORU = "muzikler"
    
    if not os.path.exists(MUZIK_KLASORU):
        os.makedirs(MUZIK_KLASORU)
        st.warning(f"⚠️ '{MUZIK_KLASORU}' klasörü yoktu, oluşturdum. İçine MP3 atın!")
        return

    # Klasördeki mp3 dosyalarını listele
    sarkilar = [f for f in os.listdir(MUZIK_KLASORU) if f.endswith(('.mp3', '.wav', '.ogg'))]
    
    if not sarkilar:
        st.info(f"📻 Radyo sessiz... '{MUZIK_KLASORU}' klasörüne şarkı yükle.")
        return

    # 2. Şarkı Seçimi (Session State ile Hafızada Tutma)
    # Eğer hafızada seçili şarkı yoksa VEYA 'sonraki_sarki' butonuna basıldıysa yeni seç
    if 'calan_sarki' not in st.session_state or st.session_state.get('sarki_degistir', False):
        secilen = random.choice(sarkilar)
        st.session_state['calan_sarki'] = secilen
        st.session_state['sarki_degistir'] = False # Bayrağı indir

    secilen_sarki = st.session_state['calan_sarki']
    dosya_yolu = os.path.join(MUZIK_KLASORU, secilen_sarki)

    # 3. Arayüz (Player + Değiştir Butonu)
    with st.container():
        c1, c2 = st.columns([3, 1])
        
        with c1:
            st.markdown(f"🎵 **Şu an Çalıyor:** {secilen_sarki[:-4]}") # .mp3 uzantısını gizle
            st.audio(dosya_yolu, format="audio/mp3")
            
        with c2:
            st.write("") # Hizalama boşluğu
            st.write("") 
            # Bu butona basınca state'i güncelliyoruz, sayfa yenileniyor ve yeni şarkı seçiyor
            if st.button("Sıradaki ⏭️"):
                st.session_state['sarki_degistir'] = True
                st.rerun()
