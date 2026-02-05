import streamlit as st
import os
import base64
import streamlit.components.v1 as components

def radyo_widget():
    """
    Radyo modülü (Hata Ayıklama Modu ile)
    """
    # Klasör isminin tam olarak 'muzik' olduğundan emin ol (küçük harf)
    folder_name = "muzik"
    
    # Şu anki çalışma dizinini bul (Sunucu nerede çalışıyor?)
    current_dir = os.getcwd()
    target_path = os.path.join(current_dir, folder_name)

    # --- HATA AYIKLAMA (DEBUG) KISMI ---
    # Eğer klasör yoksa veya içi boşsa bize ipucu ver
    if not os.path.exists(target_path) or not os.listdir(target_path):
        with st.expander("⚠️ Radyo Arıza Raporu (Tıkla)", expanded=True):
            st.error(f"Program '{folder_name}' klasörünü bulamıyor!")
            st.write(f"📍 **Şu anki Konum:** `{current_dir}`")
            
            # Etrafta hangi dosya ve klasörler var?
            try:
                dosyalar = os.listdir(current_dir)
                st.write(f"📂 **Buradaki Dosyalar:** {dosyalar}")
            except:
                st.write("Dosya listesi alınamadı.")
                
            st.info("""
            **Çözüm İpuçları:**
            1. GitHub'da **'muzik'** adında (hepsi küçük harf) bir klasör var mı?
            2. Bu klasörün içi dolu mu? (Boş klasörleri GitHub görmez!)
            3. Şarkıların uzantısı .mp3 mü?
            """)
        return 
    # -------------------------------------

    # Şarkıları bul
    sarkilar = [f for f in os.listdir(target_path) if f.endswith(('.mp3', '.wav', '.ogg'))]

    if not sarkilar:
        st.warning(f"'{folder_name}' klasörü bulundu ama içi boş veya mp3 yok.")
        st.write(f"Klasördekiler: {os.listdir(target_path)}")
        return

    # --- RADYO ARAYÜZÜ ---
    
    # Şarkı Seçimi
    secilen_sarki = st.selectbox("📻 Frekans:", sarkilar, index=0, label_visibility="collapsed")
    
    # Dosya yolu
    file_path = os.path.join(target_path, secilen_sarki)

    # Base64 Çevirme (Müziği tarayıcıya gömmek için)
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            mime_type = "audio/mp3"
    except Exception as e:
        st.error(f"Dosya okuma hatası: {e}")
        return

    # --- JAVASCRIPT OYNATICI ---
    html_code = f"""
    <script>
        var audioPlayer = window.parent.document.getElementById("persistent-audio-player");

        if (!audioPlayer) {{
            audioPlayer = document.createElement('audio');
            audioPlayer.id = "persistent-audio-player";
            audioPlayer.controls = true;
            audioPlayer.style.position = "fixed";
            audioPlayer.style.bottom = "10px";
            audioPlayer.style.right = "10px";
            audioPlayer.style.zIndex = "9999";
            audioPlayer.style.width = "300px";
            audioPlayer.autoplay = true;
            audioPlayer.loop = true; 
            window.parent.document.body.appendChild(audioPlayer);
        }}

        var currentSource = audioPlayer.getAttribute("data-source-name");
        var newSourceName = "{secilen_sarki}";

        if (currentSource !== newSourceName) {{
            audioPlayer.src = "data:{mime_type};base64,{b64}";
            audioPlayer.setAttribute("data-source-name", newSourceName);
            var playPromise = audioPlayer.play();
            if (playPromise !== undefined) {{
                playPromise.then(_ => {{}}).catch(error => {{
                    console.log("Otomatik oynatma engellendi.");
                }});
            }}
        }}
    </script>
    """
    components.html(html_code, height=0)
    st.caption(f"🎵 Çalıyor: {secilen_sarki}")
