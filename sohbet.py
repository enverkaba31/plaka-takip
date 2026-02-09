import streamlit as st
import json
import datetime
import time
from github import Github

# --- AYARLAR ---
FILE_CHAT = "chat_logs.json"

# --- GITHUB FONKSİYONLARI ---
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
        return []

def github_update_json(filename, new_data, commit_message="Chat Mesaji"):
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

# --- CANLI SOHBET PARÇASI (FRAGMENT) ---
# Bu kısım her 4 saniyede bir kendi kendine yenilenir!
# Böylece tüm sayfa donmaz ama mesajlar sürekli akar.
@st.fragment(run_every=4)
def mesaj_akisi_kutusu(current_user):
    # GitHub'dan son mesajları çek
    messages = github_read_json(FILE_CHAT) or []
    
    # Mesaj Kutusu (Yüksekliği sabit, scroll yapılabilir)
    with st.container(height=500):
        if not messages:
            st.info("📭 Henüz mesaj yok. Sessizliği boz!")
        
        for msg in messages:
            is_me = (msg["user"] == current_user)
            # Avatar ve Hizalama
            if is_me:
                avatar = "😎"
            else:
                avatar = "👤"
            
            # Baloncukları Çiz
            with st.chat_message("user" if is_me else "assistant", avatar=avatar):
                st.markdown(f"**{msg['user']}**: {msg['text']}")
                st.caption(f"🕒 {msg['time']}")

# --- ANA SOHBET MODÜLÜ ---
def sohbet_sayfasi():
    st.markdown("## 💬 BC Operasyon Hattı")
    st.caption("🟢 Hat Güvenli. Mesajlar otomatik güncellenir.")

    # 1. KULLANICI ADI KONTROLÜ
    if "chat_username" not in st.session_state:
        st.warning("Hatta girmek için kod adını belirle.")
        col1, col2 = st.columns([3, 1])
        with col1:
            kullanici_adi = st.text_input("Kod Adı:", placeholder="Örn: Polat", label_visibility="collapsed")
        with col2:
            if st.button("Giriş Yap 🚀"):
                if kullanici_adi:
                    st.session_state["chat_username"] = kullanici_adi
                    st.rerun()
        return

    # Kullanıcı giriş yapmışsa:
    current_user = st.session_state["chat_username"]
    
    # Üst Bar (Kullanıcı Bilgisi ve Çıkış)
    col_u, col_btn = st.columns([6, 1])
    col_u.success(f"📡 Bağlı: **{current_user}**")
    if col_btn.button("Çıkış", type="primary"):
        del st.session_state["chat_username"]
        st.rerun()

    # 2. OTOMATİK YENİLENEN MESAJ KUTUSU
    # Burası sihirli kısım. Sadece bu fonksiyon 4 saniyede bir çalışır.
    mesaj_akisi_kutusu(current_user)

    # 3. MESAJ GÖNDERME (SABİT KALIR)
    if prompt := st.chat_input("Mesajını yaz..."):
        # Zaman damgası
        now = datetime.datetime.now().strftime("%H:%M")
        
        # Mevcut mesajları oku (Hata olmasın diye tekrar okuyoruz)
        messages = github_read_json(FILE_CHAT) or []
        
        # Yeni mesajı ekle
        new_msg = {
            "user": current_user,
            "text": prompt,
            "time": now
        }
        
        # Son 100 mesajı tut (Dosya şişmesin)
        messages.append(new_msg)
        if len(messages) > 100:
            messages = messages[-100:]
            
        # GitHub'a kaydet
        # Spinner koymuyoruz ki akışkan olsun, zaten fragment güncelleyecek
        if github_update_json(FILE_CHAT, messages, f"Msg: {current_user}"):
            # Mesaj gittiği an sayfayı bir kere yenile ki kendi mesajımızı hemen görelim
            # Beklemeye gerek yok.
            st.rerun()
        else:
            st.error("İletilemedi!")
