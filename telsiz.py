import streamlit as st
import json
import datetime
from github import Github

# --- AYARLAR ---
FILE_TELSIZ = "telsiz_logs.json"

# --- GITHUB BAĞLANTISI ---
def get_repo():
    try:
        token = st.secrets["github"]["token"]
        repo_name = st.secrets["github"]["repo_name"]
        g = Github(token)
        return g.get_repo(repo_name)
    except:
        return None

def github_read_json(filename):
    try:
        repo = get_repo()
        if not repo: return []
        contents = repo.get_contents(filename)
        return json.loads(contents.decoded_content.decode())
    except:
        return [] # Dosya yoksa boş liste dön

def github_update_json(filename, new_data, commit_message="Telsiz Kaydi"):
    try:
        repo = get_repo()
        if not repo: return False
        try:
            contents = repo.get_contents(filename)
            repo.update_file(contents.path, commit_message, json.dumps(new_data, indent=4, ensure_ascii=False), contents.sha)
        except:
            repo.create_file(filename, commit_message, json.dumps(new_data, indent=4, ensure_ascii=False))
        return True
    except:
        return False

# --- TELSİZ MODÜLÜ ---
def telsiz_widget():
    st.markdown("""
    <style>
        .telsiz-container {
            background-color: #000;
            border: 2px solid #00FF00;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            height: 400px;
            overflow-y: auto;
            box-shadow: 0 0 10px #00FF00;
        }
        .telsiz-msg {
            margin-bottom: 8px;
            border-bottom: 1px dashed #333;
            padding-bottom: 4px;
        }
        .telsiz-time { color: #00FF00; font-weight: bold; font-size: 0.8em; }
        .telsiz-user { color: #FFD700; font-weight: bold; text-transform: uppercase; }
        .telsiz-text { color: #EEE; }
        .telsiz-input { border: 1px solid #00FF00 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("📻 Kriptolu Telsiz Hattı")

    # 1. KULLANICI GİRİŞİ (SESSION STATE)
    if "telsiz_kod_adi" not in st.session_state:
        col1, col2 = st.columns([3, 1])
        with col1:
            kod_adi = st.text_input("Giriş için Kod Adı (Nick) Girin:", placeholder="Örn: Akbaba", key="nick_input")
        with col2:
            st.write("") # Boşluk
            st.write("") 
            if st.button("Hatta Bağlan 📡"):
                if kod_adi:
                    st.session_state["telsiz_kod_adi"] = kod_adi
                    st.success("Bağlantı kuruldu. Dinlemede kalın.")
                    st.rerun()
                else:
                    st.warning("Kod adı boş olamaz!")
        return # Giriş yapmadıysa aşağıyı gösterme

    # 2. TELSİZ ARAYÜZÜ
    kod_adi = st.session_state["telsiz_kod_adi"]
    
    # Çıkış Butonu (Sağ üstte küçük)
    if st.button(f"Bağlantıyı Kes ({kod_adi})", type="secondary", use_container_width=False):
        del st.session_state["telsiz_kod_adi"]
        st.rerun()

    # Mesajları Çek
    logs = github_read_json(FILE_TELSIZ) or []

    # Mesajları Göster (Terminal Tarzı)
    st.markdown('<div class="telsiz-container">', unsafe_allow_html=True)
    if not logs:
        st.markdown('<div class="telsiz-text" style="text-align:center; opacity:0.5;">-- Sinyal Yok --</div>', unsafe_allow_html=True)
    
    for log in logs[-50:]: # Son 50 mesajı göster
        t = log.get("time", "00:00")
        u = log.get("user", "BİLİNMEYEN")
        m = log.get("msg", "")
        
        st.markdown(f"""
        <div class="telsiz-msg">
            <span class="telsiz-time">[{t}]</span> 
            <span class="telsiz-user">{u}:</span> 
            <span class="telsiz-text">{m}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. MESAJ GÖNDERME
    msg = st.chat_input(f"{kod_adi} olarak anons geç...")
    
    if msg:
        now = datetime.datetime.now().strftime("%H:%M")
        new_entry = {"user": kod_adi, "msg": msg, "time": now}
        
        # Listeye ekle ve son 50'yi tut
        logs.append(new_entry)
        if len(logs) > 50:
            logs = logs[-50:]
            
        # Kaydet
        if github_update_json(FILE_TELSIZ, logs, f"Telsiz: {kod_adi}"):
            st.toast("Anons geçildi. Tamam.", icon="📡")
            import time
            time.sleep(1) # GitHub işleminin oturması için minik bekleme
            st.rerun()
        else:
            st.error("Sinyal kesildi! (GitHub Hatası)")
