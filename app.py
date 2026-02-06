import streamlit as st
import json
import requests
from datetime import date
from github import Github

# --- MODÜLLERİ İÇERİ AKTAR ---
try:
    from intro import intro_yap  # İntro modülü
    from liderlik import liderlik_tablosu_olustur
    from harita import harita_sayfasi_olustur
    from madalyalar import madalya_sayfasi_olustur
    from liste import liste_sayfasi_olustur
    from radyo import radyo_widget
    from bcbirbiriniencokgorenuyeler import etkilesim_sayfasi_olustur
except ImportError as e:
    st.error(f"Modül hatası: {e}. Dosyaların eksiksiz olduğundan emin ol.")
    st.stop()

# --- GÜVENLİK VE AYARLAR ---
st.set_page_config(page_title="BC Plaka Takip", page_icon="🚙", layout="wide")

# --- İNTRO (SİTE AÇILINCA ÇALIŞIR) ---
try:
    intro_yap()
except Exception as e:
    # İntro çalışmazsa siteyi bozma, devam et
    pass

# --- GITHUB BAĞLANTISI ---
try:
    GITHUB_TOKEN = st.secrets["github"]["token"]
    REPO_NAME = st.secrets["github"]["repo_name"]
    YONETICI_SIFRESI = st.secrets["admin_password"]
except:
    st.error("Lütfen Streamlit Secrets ayarlarını kontrol edin.")
    st.stop()

# --- DOSYA İSİMLERİ ---
FILE_PLAKALAR = "plaka_data.json"
FILE_AVCILAR = "avcilar.json"
FILE_MADALYALAR = "madalyalar.json"
FILE_TANIMLAR = "madalya_tanimlari.json"

# --- SABİT VERİLER ---
PLAKA_SAYISI = 81
GEOJSON_URL = "https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json"
RENK_PALETI = ["#DC143C", "#008000", "#1E90FF", "#FFD700", "#9932CC", "#FF8C00", "#00CED1"]

BOLGE_MERKEZLERI = {
    "Marmara": {"lat": 40.2, "lon": 28.0},
    "Ege": {"lat": 38.5, "lon": 28.5},
    "Akdeniz": {"lat": 36.8, "lon": 33.0},
    "İç Anadolu": {"lat": 39.0, "lon": 33.5},
    "Karadeniz": {"lat": 40.8, "lon": 37.0},
    "Doğu Anadolu": {"lat": 39.0, "lon": 41.0},
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

# --- YARDIMCI FONKSİYONLAR ---
def get_repo():
    if not GITHUB_TOKEN: return None
    g = Github(GITHUB_TOKEN)
    return g.get_repo(REPO_NAME)

def github_read_json(filename):
    try:
        repo = get_repo()
        if not repo: return None
        contents = repo.get_contents(filename)
        return json.loads(contents.decoded_content.decode())
    except:
        return None

def github_update_json(filename, new_data, commit_message="Veri Guncelleme"):
    try:
        repo = get_repo()
        if not repo: return False
        try:
            contents = repo.get_contents(filename)
            repo.update_file(contents.path, commit_message, json.dumps(new_data, indent=4, ensure_ascii=False), contents.sha)
        except:
            repo.create_file(filename, commit_message, json.dumps(new_data, indent=4, ensure_ascii=False))
        return True
    except Exception as e:
        st.error(f"GitHub Hatası: {e}")
        return False

def format_plaka(no): return f"{int(no):02d}"
def tarihi_duzelt(t): return t.split("-")[2]+"/"+t.split("-")[1]+"/"+t.split("-")[0] if "-" in t else t

# --- VERİ YÜKLEME ---
def veri_yukle_hepsi():
    avcilar = github_read_json(FILE_AVCILAR) or []
    plakalar_raw = github_read_json(FILE_PLAKALAR)
    bos_plaka = {format_plaka(i): None for i in range(1, PLAKA_SAYISI + 1)}
    plakalar = bos_plaka.copy()
    if plakalar_raw:
        if "plakalar" in plakalar_raw: plakalar_raw = plakalar_raw["plakalar"]
        for k, v in plakalar_raw.items():
            k_fmt = format_plaka(k)
            if v and "tarih" in v: v["tarih"] = tarihi_duzelt(v["tarih"])
            plakalar[k_fmt] = v
    madalyalar = github_read_json(FILE_MADALYALAR) or {}
    tanimlar = github_read_json(FILE_TANIMLAR) or {}
    return avcilar, plakalar, madalyalar, tanimlar

# --- APP BAŞLANGICI ---
if 'veri_cache' not in st.session_state or st.query_params.get("refresh"):
    with st.spinner("Veriler yükleniyor..."):
        avcilar, plakalar, madalyalar, tanimlar = veri_yukle_hepsi()
        st.session_state['avcilar'] = avcilar
        st.session_state['plakalar'] = plakalar
        st.session_state['madalyalar'] = madalyalar
        st.session_state['tanimlar'] = tanimlar

avcilar = st.session_state['avcilar']
plakalar = st.session_state['plakalar']
madalyalar = st.session_state['madalyalar']
tanimlar = st.session_state['tanimlar']

# --- ARAYÜZ ---
st.title("BC PLAKA AVI 👖🐟")
radyo_widget()
st.markdown("---")

admin_mode = False
col1, col2 = st.columns([1, 3])

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔒 Yönetici")
    if st.text_input("Şifre:", type="password") == YONETICI_SIFRESI:
        admin_mode = True
        st.success("Admin: Aktif ✅")
        st.divider()
        with st.expander("👤 Avcı Ekle/Sil"):
            yeni_isim = st.text_input("Yeni Avcı:")
            if st.button("Ekle"):
                if yeni_isim and yeni_isim not in avcilar:
                    avcilar.append(yeni_isim)
                    github_update_json(FILE_AVCILAR, avcilar, "Avci eklendi")
                    st.rerun()
            if avcilar:
                sil = st.selectbox("Sil:", avcilar, index=None)
                if st.button("Sil") and sil:
                    avcilar.remove(sil)
                    github_update_json(FILE_AVCILAR, avcilar, "Avci silindi")
                    st.rerun()
        with st.expander("🏅 Madalya Dağıt"):
            if not avcilar: st.warning("Avcı yok.")
            else:
                h_avci = st.selectbox("Kime:", avcilar)
                if tanimlar:
                    s_madalya = st.selectbox("Madalya:", list(tanimlar.keys()))
                    c1, c2 = st.columns(2)
                    if c1.button("Tak ➕"):
                        if h_avci not in madalyalar: madalyalar[h_avci] = []
                        if s_madalya not in madalyalar[h_avci]:
                            madalyalar[h_avci].append(s_madalya)
                            github_update_json(FILE_MADALYALAR, madalyalar, "Madalya verildi")
                            st.rerun()
                    if c2.button("Sök ➖"):
                        if h_avci in madalyalar and s_madalya in madalyalar[h_avci]:
                            madalyalar[h_avci].remove(s_madalya)
                            github_update_json(FILE_MADALYALAR, madalyalar, "Madalya alindi")
                            st.rerun()
        with st.expander("✏️ Madalya Tanımla"):
            y_isim = st.text_input("Madalya Adı:")
            y_ikon = st.text_input("İkon:", value="🏅")
            y_desc = st.text_input("Açıklama:")
            if st.button("Oluştur/Güncelle"):
                if y_isim:
                    tanimlar[y_isim] = {"ikon": y_ikon, "desc": y_desc}
                    github_update_json(FILE_TANIMLAR, tanimlar, "Madalya tanimi guncellendi")
                    st.rerun()

# --- SOL KOLON (KAYIT) ---
with col1:
    if admin_mode:
        st.subheader("📝 Kayıt")
        boslar = sorted([p for p, d in plakalar.items() if d is None])
        if not boslar:
            st.success("Tüm plakalar bulundu!")
        else:
            if not avcilar: st.warning("Önce avcı ekleyin!")
            else:
                with st.form("kayit_formu"):
                    plaka = st.selectbox("Plaka:", boslar, format_func=lambda x: f"{x} ({TURKIYE_VERISI.get(x,{}).get('il','?')})")
                    sonu = st.text_input("Sonu:", placeholder="123", max_chars=5)
                    notu = st.text_area("Not:", placeholder="Hikayesi...")
                    avci = st.selectbox("Bulan:", avcilar)
                    tarih = st.date_input("Tarih:", value=date.today())
                    submitted = st.form_submit_button("Kaydet ✅")
                    if submitted:
                        t_fmt = tarih.strftime("%d/%m/%Y")
                        tam = f"{plaka} BC {sonu}" if sonu else f"{plaka} BC"
                        plakalar[plaka] = {"sahibi": avci, "tarih": t_fmt, "tam_plaka": tam, "plaka_sonu": sonu, "not": notu}
                        github_update_json(FILE_PLAKALAR, plakalar, f"{plaka} bulundu")
                        st.success(f"{plaka} Kaydedildi!")
                        st.rerun()
    else:
        # --- LOGO İŞLEMİ ---
        st.info("Veri girişi için yönetici girişi yapın.")
        try:
            st.image("fotograflar/bclogo.jpeg", use_container_width=True)
        except:
            st.warning("Logo bulunamadı: 'fotograflar/bclogo.jpeg'")

# --- SAĞ KOLON (MODÜLLER) ---
with col2:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Liderlik", "🗺️ Harita", "🎖️ Madalyalar", "📋 Liste", "🤝 Görülenler"])
    
    with tab1: liderlik_tablosu_olustur(avcilar, plakalar, madalyalar, tanimlar, PLAKA_SAYISI)
    with tab2: harita_sayfasi_olustur(plakalar, avcilar, TURKIYE_VERISI, BOLGE_MERKEZLERI, RENK_PALETI, GEOJSON_URL)
    with tab3: madalya_sayfasi_olustur(tanimlar, madalyalar)
    with tab4: liste_sayfasi_olustur(plakalar, TURKIYE_VERISI)
    with tab5: etkilesim_sayfasi_olustur()
