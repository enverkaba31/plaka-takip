import streamlit as st
import os
import base64
import streamlit.components.v1 as components

def radyo_widget():
    """
    Kalıcı Radyo - Otomatik Başlatma Garantili Versiyon
    """
    # 1. Klasör ve Dosya Kontrolü
    folder_name = "muzik"
    current_dir = os.getcwd()
    target_path = os.path.join(current_dir, folder_name)

    # Klasör yoksa oluştur
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    # Şarkıları bul
    try:
        sarkilar = [f for f in os.listdir(target_path) if f.endswith(('.mp3', '.wav', '.ogg'))]
    except:
        sarkilar = []

    if not sarkilar:
        # Eğer şarkı yoksa boş bir alan gösterip çık, hata verme
        return

    # 2. Arayüz (Şarkı Seçimi)
    # Burası Streamlit tarafında şarkı seçmek için
    secilen_sarki = st.selectbox("📻 Radyo Frekansı:", sarkilar, index=0, label_visibility="collapsed")
    
    file_path = os.path.join(target_path, secilen_sarki)

    # 3. Dosyayı Oku ve Kodla
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            mime_type = "audio/mp3"
    except:
        return

    # 4. JAVASCRIPT OYNATICI (SİHİRLİ KISIM)
    html_code = f"""
    <script>
        // Oynatıcıyı bul veya yarat
        var audioPlayer = window.parent.document.getElementById("persistent-audio-player");

        if (!audioPlayer) {{
            audioPlayer = document.createElement('audio');
            audioPlayer.id = "persistent-audio-player";
            audioPlayer.controls = true;
            
            // Görünüm ayarları (Sağ Alt Köşe)
            audioPlayer.style.position = "fixed";
            audioPlayer.style.bottom = "10px";
            audioPlayer.style.right = "10px";
            audioPlayer.style.zIndex = "9999";
            audioPlayer.style.width = "250px";
            audioPlayer.style.borderRadius = "20px";
            audioPlayer.style.boxShadow = "0px 0px 10px rgba(0,0,0,0.5)";
            
            // Özellikler
            audioPlayer.autoplay = true;
            audioPlayer.loop = true;
            audioPlayer.volume = 0.5; // Ses seviyesi %50 başlasın (Çok bağırmasın)
            
            window.parent.document.body.appendChild(audioPlayer);
        }}

        // Şarkı değiştiyse kaynağı güncelle
        var currentSource = audioPlayer.getAttribute("data-source-name");
        var newSourceName = "{secilen_sarki}";

        if (currentSource !== newSourceName) {{
            audioPlayer.src = "data:{mime_type};base64,{b64}";
            audioPlayer.setAttribute("data-source-name", newSourceName);
        }}

        // --- OTOMATİK BAŞLATMA ZORLAYICI ---
        var playPromise = audioPlayer.play();

        if (playPromise !== undefined) {{
            playPromise.then(_ => {{
                // Otomatik başladı, süper!
                console.log("Müzik başladı.");
            }}).catch(error => {{
                // Tarayıcı engelledi! Pusuya yatıyoruz.
                console.log("Otomatik oynatma engellendi. Tıklama bekleniyor...");
                
                // Kullanıcı sayfada HERHANGİ BİR YERE tıkladığı an çalıştır
                var startAudio = function() {{
                    audioPlayer.play();
                    // Bir kere çalıştıktan sonra bu dinleyiciyi kaldır (Tekrar tekrar çalışmasın)
                    window.parent.document.removeEventListener('click', startAudio);
                    window.parent.document.removeEventListener('keydown', startAudio);
                }};

                window.parent.document.addEventListener('click', startAudio);
                window.parent.document.addEventListener('keydown', startAudio);
            }});
        }}
    </script>
    """
    
    components.html(html_code, height=0)
