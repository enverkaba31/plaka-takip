import streamlit as st
import json
import random
from datetime import date
from github import Github

# --- 1. AYARLAR & GÜVENLİK ---
st.set_page_config(
    page_title="BC Plaka Takip",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MODÜLLERİ ÇAĞIR ---
try:
    from animasyon import intro_yap  
    from liderlik import liderlik_tablosu_olustur
    from harita import harita_sayfasi_olustur
    from madalyalar import madalya_sayfasi_olustur 
    from liste import liste_sayfasi_olustur
    from radyo import radyo_widget
    from bcbirbiriniencokgorenuyeler import etkilesim_sayfasi_olustur
    from gazete import gazete_sayfasi_olustur
    from profil import profil_sayfasi
except ImportError as e:
    st.error(f"🚨 KRİTİK HATA: Modüller eksik! ({e})")
    st.stop()

# --- 3. GÖRSEL ŞÖLEN (CUSTOM CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1 {
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 0px 0px 20px rgba(255, 75, 75, 0.5);
    }
    div[data-testid="stMetric"] {
        background-color: #1E1E1E; padding: 15px; border-radius: 10px;
        border: 1px solid #333; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stButton>button {
        width: 100%; border-radius: 20px; font-weight: bold; transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02); box-shadow: 0 0 15px rgba(255, 75, 75, 0.5);
    }
    [data-testid="stSidebar"] { background-image: linear-gradient(#1A1A1A, #0E0E0E); }
</style>
""", unsafe_allow_html=True)

# --- 4. İNTRO & RADYO ---
try:
    intro_yap() 
except:
    pass

radyo_widget()

# --- 5. VERİ BAĞLANTILARI ---
try:
    GITHUB_TOKEN = st.secrets["github"]["token"]
    REPO_NAME = st.secrets["github"]["repo_name"]
    YONETICI_SIFRESI = st.secrets["admin_password"]
except:
    st.error("⛔ SİSTEM HATASI: Gizli anahtarlar (Secrets) bulunamadı!")
    st.stop()

# Dosya İsimleri
FILES = {
    "plaka": "plaka_data.json",
    "avci": "avcilar.json",
    "madalya": "madalyalar.json",
    "tanim": "madalya_tanimlari.json"
}

# Sabitler
PLAKA_SAYISI = 81
GEOJSON_URL = "https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json"
RENK_PALETI = ["#DC143C", "#008000", "#1E90FF", "#FFD700", "#9932CC", "#FF8C00", "#00CED1"]
BOLGE_MERKEZLERI = {
    "Marmara": {"lat": 40.2, "lon": 28.0}, "Ege": {"lat": 38.5, "lon": 28.5},
    "Akdeniz": {"lat": 36.8, "lon": 33.0}, "İç Anadolu": {"lat": 39.0, "lon": 33.5},
    "Karadeniz": {"lat": 40.8, "lon": 37.0}, "Doğu Anadolu": {"lat": 39.0, "lon": 41.0},
    "Güneydoğu Anadolu": {"lat": 37.5, "lon": 40.0}
}
TURKIYE_VERISI = {
    "01": {"il": "Adana", "bolge": "Akdeniz"}, "02": {"il": "Adıyaman", "bolge": "Güneydoğu Anadolu"},
    "03": {"il": "Afyonkarahisar", "bolge": "Ege"}, "04": {"il": "Ağrı", "bolge": "Doğu Anadolu"},
    "05": {"il": "Amasya", "bolge": "Karadeniz"}, "06": {"il": "Ankara", "bolge": "İç Anadolu"},
    "07": {"il": "Antalya", "bolge": "Akdeniz"}, "08": {"il": "Artvin", "bolge": "Karadeniz"},
    "09": {"il": "Aydın", "bolge": "Ege"}, "10": {"il": "Balıkesir", "bolge": "Marmara"},
    "11": {"il": "Bilecik", "bolge": "Marmara"}, "12": {"il": "Bingöl", "bolge": "Doğu Anadolu"},
    "13": {"il": "Bitlis", "bolge": "Doğu Anadolu"}, "14": {"il": "Bolu", "bolge": "Karadeniz"},
    "15": {"il": "Burdur", "bolge": "Akdeniz"}, "16": {"il": "Bursa", "bolge": "Marmara"},
    "17": {"il": "Çanakkale", "bolge": "Marmara"}, "18": {"il": "Çankırı", "bolge": "İç Anadolu"},
    "19": {"il": "Çorum", "bolge": "Karadeniz"}, "20": {"il": "Denizli", "bolge": "Ege"},
    "21": {"il": "Diyarbakır", "bolge": "Güneydoğu Anadolu"}, "22": {"il": "Edirne", "bolge": "Marmara"},
    "23": {"il": "Elazığ", "bolge": "Doğu Anadolu"}, "24": {"il": "Erzincan", "bolge": "Doğu Anadolu"},
    "25": {"il": "Erzurum", "bolge": "Doğu Anadolu"}, "26": {"il": "Eskişehir", "bolge": "İç Anadolu"},
    "27": {"il": "Gaziantep", "bolge": "Güneydoğu Anadolu"}, "28": {"il": "Giresun", "bolge": "Karadeniz"},
    "29": {"il": "Gümüşhane", "bolge": "Karadeniz"}, "30": {"il": "Hakkari", "bolge": "Doğu Anadolu"},
    "31": {"il": "Hatay", "bolge": "Akdeniz"}, "32": {"il": "Isparta", "bolge": "Akdeniz"},
    "33": {"il": "Mersin", "bolge": "Akdeniz"}, "34": {"il": "İstanbul", "bolge": "Marmara"},
    "35": {"il": "İzmir", "bolge": "Ege"}, "36": {"il": "Kars", "bolge": "Doğu Anadolu"},
    "37": {"il": "Kastamonu", "bolge": "Karadeniz"}, "38": {"il": "Kayseri", "bolge": "İç Anadolu"},
    "39": {"il": "Kırklareli", "bolge": "Marmara"}, "40": {"il": "Kırşehir", "bolge": "İç Anadolu"},
    "41": {"il": "Kocaeli", "bolge": "Marmara"}, "42": {"il": "Konya", "bolge": "İç Anadolu"},
    "43": {"il": "Kütahya", "bolge": "Ege"}, "44": {"il": "Malatya", "bolge": "Doğu Anadolu"},
    "45": {"il": "Manisa", "bolge": "Ege"}, "46": {"il": "Kahramanmaraş", "bolge": "Akdeniz"},
    "47": {"il": "Mardin", "bolge": "Güneydoğu Anadolu"}, "48": {"il": "Muğla", "bolge": "Ege"},
    "49": {"il": "Muş", "bolge": "Doğu Anadolu"}, "50": {"il": "Nevşehir", "bolge": "İç Anadolu"},
    "51": {"il": "Niğde", "bolge": "İç Anadolu"}, "52": {"il": "Ordu", "bolge": "Karadeniz"},
    "53": {"il": "Rize", "bolge": "Karadeniz"}, "54": {"il": "Sakarya", "bolge": "Marmara"},
    "55": {"il": "Samsun", "bolge": "Karadeniz"}, "56": {"il": "Siirt", "bolge": "Güneydoğu Anadolu"},
    "57": {"il": "Sinop", "bolge": "Karadeniz"}, "58": {"il": "Sivas", "bolge": "İç Anadolu"},
    "59": {"il": "Tekirdağ", "bolge": "Marmara"}, "60": {"il": "Tokat", "bolge": "Karadeniz"},
    "61": {"il": "Trabzon", "bolge": "Karadeniz"}, "62": {"il": "Tunceli", "bolge": "Doğu Anadolu"},
    "63": {"il": "Şanlıurfa", "bolge": "Güneydoğu Anadolu"}, "64": {"il": "Uşak", "bolge": "Ege"},
    "65": {"il": "Van", "bolge": "Doğu Anadolu"}, "66": {"il": "Yozgat", "bolge": "İç Anadolu"},
    "67": {"il": "Zonguldak", "bolge": "Karadeniz"}, "68": {"il": "Aksaray", "bolge": "İç Anadolu"},
    "69": {"il": "Bayburt", "bolge": "Karadeniz"}, "70": {"il": "Karaman", "bolge": "İç Anadolu"},
    "71": {"il": "Kırıkkale", "bolge": "İç Anadolu"}, "72": {"il": "Batman", "bolge": "Güneydoğu Anadolu"},
    "73": {"il": "Şırnak", "bolge": "Güneydoğu Anadolu"}, "74": {"il": "Bartın", "bolge": "Karadeniz"},
    "75": {"il": "Ardahan", "bolge": "Doğu Anadolu"}, "76": {"il": "Iğdır", "bolge": "Doğu Anadolu"},
    "77": {"il": "Yalova", "bolge": "Marmara"}, "78": {"il": "Karabük", "bolge": "Karadeniz"},
    "79": {"il": "Kilis", "bolge": "Güneydoğu Anadolu"}, "80": {"il": "Osmaniye", "bolge": "Akdeniz"},
    "81": {"il": "Düzce", "bolge": "Karadeniz"},
}

# --- 6. YARDIMCI FONKSİYONLAR ---
def get_repo():
    g = Github(GITHUB_TOKEN)
    return g.get_repo(REPO_NAME)

def github_read_json(filename):
    try:
        repo = get_repo()
        contents = repo.get_contents(filename)
        return json.loads(contents.decoded_content.decode())
    except:
        return None

def github_update_json(filename, new_data, commit_message="Operasyon Kaydı"):
    try:
        repo = get_repo()
        try:
            contents = repo.get_contents(filename)
            repo.update_file(contents.path, commit_message, json.dumps(new_data, indent=4, ensure_ascii=False), contents.sha)
        except:
            repo.create_file(filename, commit_message, json.dumps(new_data, indent=4, ensure_ascii=False))
        return True
    except:
        return False

def format_plaka(no): return f"{int(no):02d}"

# --- 7. VERİLERİ YÜKLE ---
def veri_yukle():
    avcilar = github_read_json(FILES["avci"]) or []
    plakalar_raw = github_read_json(FILES["plaka"])
    
    bos_plaka = {format_plaka(i): None for i in range(1, PLAKA_SAYISI + 1)}
    plakalar = bos_plaka.copy()
    
    if plakalar_raw:
        if "plakalar" in plakalar_raw: plakalar_raw = plakalar_raw["plakalar"]
        for k, v in plakalar_raw.items():
            k_fmt = format_plaka(k)
            plakalar[k_fmt] = v
            
    madalyalar = github_read_json(FILES["madalya"]) or {}
    tanimlar = github_read_json(FILES["tanim"]) or {}
    return avcilar, plakalar, madalyalar, tanimlar

if 'veri_cache' not in st.session_state or st.query_params.get("refresh"):
    avcilar, plakalar, madalyalar, tanimlar = veri_yukle()
    st.session_state['avcilar'] = avcilar
    st.session_state['plakalar'] = plakalar
    st.session_state['madalyalar'] = madalyalar
    st.session_state['tanimlar'] = tanimlar
else:
    avcilar = st.session_state['avcilar']
    plakalar = st.session_state['plakalar']
    madalyalar = st.session_state['madalyalar']
    tanimlar = st.session_state['tanimlar']

# --- 8. ANA ARAYÜZ (LAYOUT) ---

st.title("B.C. Boş İşler Müdürlüğü 🕵️‍♂️")
st.caption("Plaka Avı Sistemi")
st.divider()

col1, col2 = st.columns([1, 3], gap="medium")

# --- SIDEBAR: YÖNETİCİ PANELİ ---
admin_mode = False
with st.sidebar:
    st.header("🔒 NEK Paneli")
    
    # Giriş Paneli
    if st.text_input("🔑 Erişim Şifresi:", type="password") == YONETICI_SIFRESI:
        admin_mode = True
        st.success("YETKİ VERİLDİ: ADMIN")
        st.divider()
        
        # Admin İşlemleri
        with st.expander("👤 Personel İşleri"):
            yeni_isim = st.text_input("Avcı Ekle:")
            if st.button("Kaydı Tamamla"):
                if yeni_isim and yeni_isim not in avcilar:
                    avcilar.append(yeni_isim)
                    github_update_json(FILES["avci"], avcilar, "Yeni Avcı")
                    st.rerun()
            
            silinecek = st.selectbox("Avcı Sil:", avcilar, index=None)
            if st.button("İlişiği Kes") and silinecek:
                avcilar.remove(silinecek)
                github_update_json(FILES["avci"], avcilar, "Avcı silindi")
                st.rerun()

        with st.expander("🎖️ Madalya Dağıtım"):
            if avcilar:
                kime = st.selectbox("Kime:", avcilar)
                ne = st.selectbox("Ne:", list(tanimlar.keys()) if tanimlar else [])
                c1, c2 = st.columns(2)
                if c1.button("Tak"):
                    if kime not in madalyalar: madalyalar[kime] = []
                    if ne not in madalyalar[kime]:
                        madalyalar[kime].append(ne)
                        github_update_json(FILES["madalya"], madalyalar)
                        st.toast(f"{kime} madalyayı kaptı! 🏅")
                        st.rerun()
                if c2.button("Sök"):
                    if kime in madalyalar and ne in madalyalar[kime]:
                        madalyalar[kime].remove(ne)
                        github_update_json(FILES["madalya"], madalyalar)
                        st.rerun()
        
        # --- YENİ MADALYA EKLEME ---
        with st.expander("📝 Yeni Madalya Tasarla"):
            m_ad = st.text_input("Madalya İsmi:")
            m_ikon = st.text_input("İkon (Emoji):", value="🏅")
            m_desc = st.text_input("Açıklama:")
            if st.button("Envantere Ekle"):
                if m_ad:
                    tanimlar[m_ad] = {"ikon": m_ikon, "desc": m_desc}
                    github_update_json(FILES["tanim"], tanimlar, "Yeni madalya")
                    st.rerun()

    else:
        st.info("Sadece yetkili personel.")

# --- SOL KOLON (OPERASYON & LOGO) ---
with col1:
    # İstatistik Kutusu
    bulunan_sayisi = sum(1 for v in plakalar.values() if v is not None)
    kalan_sayisi = PLAKA_SAYISI - bulunan_sayisi
    ilerleme = bulunan_sayisi / PLAKA_SAYISI
    
    st.metric(label="🎯 Bulunan Plakalar", value=bulunan_sayisi, delta=f"Kalan: {kalan_sayisi}")
    st.progress(ilerleme)
    
    st.divider()

    if admin_mode:
        st.subheader("📝 Plaka Kaydı")
        boslar = sorted([p for p, d in plakalar.items() if d is None])
        
        if not boslar:
            st.balloons()
            st.success("GÖREV TAMAMLANDI! TÜM PLAKALAR BULUNDU! 🏆")
        else:
            if not avcilar:
                st.error("Önce avcı ekleyin!")
            else:
                with st.form("kayit_formu", border=True):
                    secilen_plaka = st.selectbox("Hedef Plaka:", boslar, format_func=lambda x: f"{x} - {TURKIYE_VERISI.get(x,{}).get('il','?')}")
                    sonu = st.text_input("Plaka Sonu (Opsiyonel):", placeholder="Örn: 1907")
                    notu = st.text_area("Not:", placeholder="Nerede görüldü? Hikayesi ne?")
                    avci = st.selectbox("Bulan:", avcilar)
                    tarih = st.date_input("Bulma Tarihi:", value=date.today())
                    
                    if st.form_submit_button("Plakayı Avla 🔫"):
                        t_fmt = tarih.strftime("%d/%m/%Y")
                        tam = f"{secilen_plaka} BC {sonu}" if sonu else f"{secilen_plaka} BC"
                        
                        plakalar[secilen_plaka] = {
                            "sahibi": avci, 
                            "tarih": t_fmt, 
                            "tam_plaka": tam, 
                            "plaka_sonu": sonu, 
                            "not": notu
                        }
                        
                        if github_update_json(FILES["plaka"], plakalar, f"{secilen_plaka} bulundu"):
                            st.success(f"Tebrikler {avci}! {secilen_plaka} plakası düştü! 🔥")
                            st.balloons()
                            import time
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("Bağlantı hatası! Tekrar dene.")
    else:
        # LOGO GÖSTERİMİ
        try:
            st.image("fotograflar/bclogo.jpeg", use_container_width=True)
            st.caption("BC Resmi Logosu © 2026")
        except:
            st.warning("Logo yüklenemedi. Dosya yolunu kontrol et.")

# --- SAĞ KOLON (VERİ MERKEZİ) ---
with col2:
    # 8 Sekmeli Yapı (Sıralama Güncellendi)
    tab_titles = [
        "📰 BC Gazete",
        "🏆 Liderlik", 
        "📋 Detaylı Liste",
        "🗺️ Harita", 
        "🪪 Ajan Profili", 
        "🎖️ Madalyalar", 
        "🤝 Birbirini En Çok Görenler",
    ]
    
    t0, t1, t2, t3, t4, t5, t6, t7 = st.tabs(tab_titles)
    
    with t0:
        gazete_sayfasi_olustur(plakalar, TURKIYE_VERISI)
        
    with t1:
        st.markdown("###")
        liderlik_tablosu_olustur(avcilar, plakalar, madalyalar, tanimlar, PLAKA_SAYISI)
        
    with t2:
        st.markdown("###")
        liste_sayfasi_olustur(plakalar, TURKIYE_VERISI)

    with t3:
        st.markdown("### 🗺️ Operasyon Haritası")
        harita_sayfasi_olustur(plakalar, avcilar, TURKIYE_VERISI, BOLGE_MERKEZLERI, RENK_PALETI, GEOJSON_URL)

    with t4: 
        profil_sayfasi(avcilar, plakalar, madalyalar, tanimlar, TURKIYE_VERISI)

    with t5: 
        st.markdown("###")
        madalya_sayfasi_olustur(tanimlar, madalyalar)

    with t6:
        etkilesim_sayfasi_olustur()


