import streamlit as st
import os
import base64
import streamlit.components.v1 as components

def radyo_widget():
    """
    Kalıcı (Sayfa değişince susmayan) ve Otomatik Başlayan Radyo.
    """
    folder_path = "muzik"
    
    # Klasör kontrolü
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        st.error("Müzik klasörü yoktu, oluşturuldu. İçine şarkı atın.")
        return

    # Şarkıları bul
    try:
        sarkilar = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav', '.ogg'))]
    except:
        sarkilar = []

    if not sarkilar:
        st.caption("📻 Radyo sessiz... (Klasör boş)")
        return

    # --- ŞARKI SEÇİMİ VE PLAYER ---
    # Kullanıcı buradan şarkı değiştirebilir
    secilen_sarki = st.selectbox("📻 Frekans:", sarkilar, index=0, label_visibility="collapsed")
    
    # Seçilen şarkının dosya yolunu bul
    file_path = os.path.join(folder_path, secilen_sarki)

    # --- Python ile Dosyayı Base64'e Çevir (Tarayıcıya Gömme İşlemi) ---
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        mime_type = "audio/mp3"  # Genelde mp3 kullanıldığı varsayılıyor

    # --- JAVASCRIPT HACK ---
    # Bu kod, Streamlit'in "her şeyi yenileme" huyunu aşar.
    # Müziği 'window' (tarayıcı penceresi) nesnesine yapıştırır.
    
    html_code = f"""
    <script>
        // 1. Daha önce oluşturduğumuz bir oynatıcı var mı kontrol et
        var audioPlayer = window.parent.document.getElementById("persistent-audio-player");

        if (!audioPlayer) {{
            // YOKSA: Yeni bir tane yarat (Sadece ilk girişte çalışır)
            audioPlayer = document.createElement('audio');
            audioPlayer.id = "persistent-audio-player";
            audioPlayer.controls = true;
            audioPlayer.style.position = "fixed";
            audioPlayer.style.bottom = "10px";
            audioPlayer.style.right = "10px";
            audioPlayer.style.zIndex = "9999";
            audioPlayer.style.width = "300px";
            audioPlayer.autoplay = true; // Otomatik başlat
            audioPlayer.loop = true;     // Döngüye al
            
            // Siteye ekle
            window.parent.document.body.appendChild(audioPlayer);
        }}

        // 2. Çalınacak şarkı değişti mi kontrol et
        // (Python'dan gelen yeni base64 verisi ile mevcut çalanı kıyasla)
        var currentSource = audioPlayer.getAttribute("data-source-name");
        var newSourceName = "{secilen_sarki}";

        if (currentSource !== newSourceName) {{
            // Şarkı değişmişse veya ilk defa açılıyorsa kaynağı güncelle
            audioPlayer.src = "data:{mime_type};base64,{b64}";
            audioPlayer.setAttribute("data-source-name", newSourceName);
            
            // Tarayıcı politikası gereği Promise ile oynatmayı dene
            var playPromise = audioPlayer.play();
            if (playPromise !== undefined) {{
                playPromise.then(_ => {{
                    // Otomatik başladı
                }}).catch(error => {{
                    // Tarayıcı engelledi (Kullanıcı etkileşimi bekliyor)
                    console.log("Otomatik oynatma engellendi, kullanıcı tıklaması bekleniyor.");
                }});
            }}
        }}
    </script>
    """

    # Görünmez bir HTML bileşeni olarak sayfaya ekle
    components.html(html_code, height=0)
    
    # Kullanıcıya bilgi ver
    st.caption(f"🎵 Çalıyor: {secilen_sarki} (Sayfa değişse de susmaz)")
