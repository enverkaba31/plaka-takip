import streamlit as st
import pandas as pd
import json
import os
from datetime import date
from collections import Counter
from github import Github, GithubException # Yeni kütüphanemiz

# --- AYARLAR ---
# Bu şifre sadece yönetici girişi içindir (Streamlit şifresi değil)
YONETICI_SIFRESI = "enver123" 

FILE_PLAKALAR = "plaka_data.json"
FILE_AVCILAR = "avcilar.json"
PLAKA_SAYISI = 81

# --- GITHUB BAĞLANTISI ---
# Streamlit Secrets'tan bilgileri çekiyoruz
try:
    GITHUB_TOKEN = st.secrets["github"]["token"]
    REPO_NAME = st.secrets["github"]["repo_name"]
except:
    st.error("Lütfen Streamlit Secrets ayarlarını yapın (Token ve Repo adı).")
    st.stop()

def get_repo():
    """GitHub deposuna bağlanır."""
    g = Github(GITHUB_TOKEN)
    return g.get_repo(REPO_NAME)

def github_read_json(filename):
    """GitHub'dan JSON dosyasını okur."""
    try:
        repo = get_repo()
        contents = repo.get_contents(filename)
        return json.loads(contents.decoded_content.decode())
    except Exception as e:
        # Dosya yoksa veya hata varsa boş dönebiliriz ama
        # başlangıçta dosyaları elle yüklediğin için burası çalışmalı.
        st.error(f"GitHub Okuma Hatası ({filename}): {e}")
        return None

def github_update_json(filename, new_data, commit_message="Veri Guncelleme"):
    """GitHub'daki JSON dosyasını günceller."""
    try:
        repo = get_repo()
        contents = repo.get_contents(filename)
        repo.update_file(
            path=contents.path,
            message=commit_message,
            content=json.dumps(new_data, ensure_ascii=False, indent=4),
            sha=contents.sha
        )
        return True
    except Exception as e:
        st.error(f"GitHub Yazma Hatası: {e}")
        return False

# --- SABİT VERİLER (Şehirler) ---
TURKIYE_VERISI = {
    "01": {"il": "Adana", "bolge": "Akdeniz"},
    "02": {"il": "Adıyaman", "bolge": "Güneydoğu Anadolu"},
    "03": {"il": "Afyonkarahisar", "bolge": "Ege"},
    "04": {"il": "Ağrı", "bolge": "Doğu Anadolu"},
    "05": {"il": "Amasya", "bolge": "Karadeniz"},
    "06": {"il": "Ankara", "bolge": "İç Anadolu"},
    "07": {"il": "Antalya", "bolge": "Akdeniz"},
    "08": {"il": "Artvin", "bolge": "Karadeniz"},
    "09": {"il": "Aydın", "bolge": "Ege"},
    "10": {"il": "Balıkesir", "bolge": "Marmara"},
    "11": {"il": "Bilecik", "bolge": "Marmara"},
    "12": {"il": "Bingöl", "bolge": "Doğu Anadolu"},
    "13": {"il": "Bitlis", "bolge": "Doğu Anadolu"},
    "14": {"il": "Bolu", "bolge": "Karadeniz"},
    "15": {"il": "Burdur", "bolge": "Akdeniz"},
    "16": {"il": "Bursa", "bolge": "Marmara"},
    "17": {"il": "Çanakkale", "bolge": "Marmara"},
    "18": {"il": "Çankırı", "bolge": "İç Anadolu"},
    "19": {"il": "Çorum", "bolge": "Karadeniz"},
    "20": {"il": "Denizli", "bolge": "Ege"},
    "21": {"il": "Diyarbakır", "bolge": "Güneydoğu Anadolu"},
    "22": {"il": "Edirne", "bolge": "Marmara"},
    "23": {"il": "Elazığ", "bolge": "Doğu Anadolu"},
    "24": {"il": "Erzincan", "bolge": "Doğu Anadolu"},
    "25": {"il": "Erzurum", "bolge": "Doğu Anadolu"},
    "26": {"il": "Eskişehir", "bolge": "İç Anadolu"},
    "27": {"il": "Gaziantep", "bolge": "Güneydoğu Anadolu"},
    "28": {"il": "Giresun", "bolge": "Karadeniz"},
    "29": {"il": "Gümüşhane", "bolge": "Karadeniz"},
    "30": {"il": "Hakkari", "bolge": "Doğu Anadolu"},
    "31": {"il": "Hatay", "bolge": "Akdeniz"},
    "32": {"il": "Isparta", "bolge": "Akdeniz"},
    "33": {"il": "Mersin", "bolge": "Akdeniz"},
    "34": {"il": "İstanbul", "bolge": "Marmara"},
    "35": {"il": "İzmir", "bolge": "Ege"},
    "36": {"il": "Kars", "bolge": "Doğu Anadolu"},
    "37": {"il": "Kastamonu", "bolge": "Karadeniz"},
    "38": {"il": "Kayseri", "bolge": "İç Anadolu"},
    "39": {"il": "Kırklareli", "bolge": "Marmara"},
    "40": {"il": "Kırşehir", "bolge": "İç Anadolu"},
    "41": {"il": "Kocaeli", "bolge": "Marmara"},
    "42": {"il": "Konya", "bolge": "İç Anadolu"},
    "43": {"il": "Kütahya", "bolge": "Ege"},
    "44": {"il": "Malatya", "bolge": "Doğu Anadolu"},
    "45": {"il": "Manisa", "bolge": "Ege"},
    "46": {"il": "Kahramanmaraş", "bolge": "Akdeniz"},
    "47": {"il": "Mardin", "bolge": "Güneydoğu Anadolu"},
    "48": {"il": "Muğla", "bolge": "Ege"},
    "49": {"il": "Muş", "bolge": "Doğu Anadolu"},
    "50": {"il": "Nevşehir", "bolge": "İç Anadolu"},
    "51": {"il": "Niğde", "bolge": "İç Anadolu"},
    "52": {"il": "Ordu", "bolge": "Karadeniz"},
    "53": {"il": "Rize", "bolge": "Karadeniz"},
    "54": {"il": "Sakarya", "bolge": "Marmara"},
    "55": {"il": "Samsun", "bolge": "Karadeniz"},
    "56": {"il": "Siirt", "bolge": "Güneydoğu Anadolu"},
    "57": {"il": "Sinop", "bolge": "Karadeniz"},
    "58": {"il": "Sivas", "bolge": "İç Anadolu"},
    "59": {"il": "Tekirdağ", "bolge": "Marmara"},
    "60": {"il": "Tokat", "bolge": "Karadeniz"},
    "61": {"il": "Trabzon", "bolge": "Karadeniz"},
    "62": {"il": "Tunceli", "bolge": "Doğu Anadolu"},
    "63": {"il": "Şanlıurfa", "bolge": "Güneydoğu Anadolu"},
    "64": {"il": "Uşak", "bolge": "Ege"},
    "65": {"il": "Van", "bolge": "Doğu Anadolu"},
    "66": {"il": "Yozgat", "bolge": "İç Anadolu"},
    "67": {"il": "Zonguldak", "bolge": "Karadeniz"},
    "68": {"il": "Aksaray", "bolge": "İç Anadolu"},
    "69": {"il": "Bayburt", "bolge": "Karadeniz"},
    "70": {"il": "Karaman", "bolge": "İç Anadolu"},
    "71": {"il": "Kırıkkale", "bolge": "İç Anadolu"},
    "72": {"il": "Batman", "bolge": "Güneydoğu Anadolu"},
    "73": {"il": "Şırnak", "bolge": "Güneydoğu Anadolu"},
    "74": {"il": "Bartın", "bolge": "Karadeniz"},
    "75": {"il": "Ardahan", "bolge": "Doğu Anadolu"},
    "76": {"il": "Iğdır", "bolge": "Doğu Anadolu"},
    "77": {"il": "Yalova", "bolge": "Marmara"},
    "78": {"il": "Karabük", "bolge": "Karadeniz"},
    "79": {"il": "Kilis", "bolge": "Güneydoğu Anadolu"},
    "80": {"il": "Osmaniye", "bolge": "Akdeniz"},
    "81": {"il": "Düzce", "bolge": "Karadeniz"},
}

# --- YARDIMCI FONKSİYONLAR ---
def format_plaka(no):
    return f"{int(no):02d}"

def tarihi_duzelt(tarih_str):
    if "-" in tarih_str:
        try:
            parcalar = tarih_str.split("-")
            return f"{parcalar[2]}/{parcalar[1]}/{parcalar[0]}"
        except:
            return tarih_str
    return tarih_str

# --- VERİ YÖNETİMİ (GITHUB MODU) ---
def avcilari_yukle():
    data = github_read_json(FILE_AVCILAR)
    if data is None:
        return [] # Dosya yoksa veya hata varsa boş dön
    return data

def avcilari_kaydet(liste):
    success = github_update_json(FILE_AVCILAR, liste, "Avcı listesi güncellendi")
    if not success:
        st.error("Avcılar GitHub'a kaydedilemedi!")

def plakalari_yukle():
    bos_yapi = {format_plaka(i): None for i in range(1, PLAKA_SAYISI + 1)}
    
    data = github_read_json(FILE_PLAKALAR)
    
    if data is None:
        return bos_yapi # Dosya yoksa boş yapı dön
    
    # Veri temizliği ve formatlama
    try:
        if "plakalar" in data: data = data["plakalar"]
        
        temizlenmis_veri = bos_yapi.copy()
        for k, v in data.items():
            yeni_key = format_plaka(k)
            if v and "tarih" in v: v["tarih"] = tarihi_duzelt(v["tarih"])
            temizlenmis_veri[yeni_key] = v
            
        return temizlenmis_veri
    except Exception as e:
        st.error(f"Veri işleme hatası: {e}")
        return bos_yapi

def plakalari_kaydet(veri):
    success = github_update_json(FILE_PLAKALAR, veri, "Plaka verisi güncellendi")
    if success:
        st.toast("Veriler GitHub'a kalıcı olarak kaydedildi! ☁️", icon="✅")
    else:
        st.error("Kaydetme başarısız! Token izinlerini kontrol edin.")


# --- UYGULAMA BAŞLANGICI ---
st.set_page_config(page_title="BC Plaka Takip", page_icon="🚙", layout="wide")

# Session State Yönetimi
if 'avci_listesi' not in st.session_state:
    with st.spinner("Veriler GitHub'dan çekiliyor..."):
        st.session_state['avci_listesi'] = avcilari_yukle()

# Plakaları her seferinde taze çekelim ki senkron olsun
if 'plaka_verisi' not in st.session_state or st.query_params.get("refresh"):
     with st.spinner("Plakalar güncelleniyor..."):
        st.session_state['plaka_verisi'] = plakalari_yukle()

avcilar = st.session_state['avci_listesi']
plakalar = st.session_state['plaka_verisi']

# --- SIDEBAR: YÖNETİCİ GİRİŞİ ---
with st.sidebar:
    st.header("🔒 Yönetici Paneli")
    girilen_sifre = st.text_input("Yönetici Şifresi:", type="password")
    
    if girilen_sifre == YONETICI_SIFRESI:
        admin_mode = True
        st.success("Yönetici Girişi Aktif ✅")
        st.divider()
        with st.expander("👤 Avcı İşlemleri (Admin)"):
            yeni_isim = st.text_input("Yeni İsim Ekle:")
            if st.button("Ekle", use_container_width=True):
                if yeni_isim and yeni_isim not in avcilar:
                    avcilar.append(yeni_isim)
                    avcilari_kaydet(avcilar)
                    st.rerun()
            st.divider()
            if avcilar:
                silinecek = st.selectbox("Avcı Sil:", avcilar, index=None)
                if st.button("Sil") and silinecek:
                    avcilar.remove(silinecek)
                    avcilari_kaydet(avcilar)
                    st.rerun()
    else:
        admin_mode = False
        st.info("Veri girişi sadece yöneticiye açıktır.")

# --- ANA EKRAN ---
st.title("🚙 Plaka Avı (BC Serisi) - Online")
st.markdown("---")

if admin_mode:
    col1, col2 = st.columns([1, 2])
else:
    col2 = st.container()

# --- KOLON 1: VERİ GİRİŞİ (ADMİN) ---
if admin_mode:
    with col1:
        st.subheader("📝 Kayıt Girişi")
        bos_plakalar = [p for p, d in plakalar.items() if d is None]
        bos_plakalar.sort()
        
        if not bos_plakalar:
            st.balloons()
            st.success("Tamamlandı!")
        else:
            if not avcilar:
                st.warning("⚠️ Avcı ekleyin!")
            else:
                with st.form("kayit_form"):
                    def liste_gorunumu(plaka_kodu):
                        sehir_adi = TURKIYE_VERISI.get(plaka_kodu, {}).get("il", "Bilinmiyor")
                        return f"{plaka_kodu} BC ({sehir_adi})"

                    secilen_plaka = st.selectbox("Plaka Seç:", bos_plakalar, format_func=liste_gorunumu)
                    plaka_sonu = st.text_input("Plakanın Devamı (Sayılar):", placeholder="Örn: 123", max_chars=5)
                    secilen_avci = st.selectbox("Bulan Kişi:", avcilar)
                    raw_tarih = st.date_input("Tarih:", value=date.today(), format="DD/MM/YYYY")
                    
                    secilen_il = TURKIYE_VERISI.get(secilen_plaka, {}).get("il", "")
                    st.caption(f"📍 Bölge: {secilen_il}")
                    
                    if st.form_submit_button("Kaydet ✅"):
                        formatli_tarih = raw_tarih.strftime("%d/%m/%Y")
                        tam_plaka_str = f"{secilen_plaka} BC {plaka_sonu}" if plaka_sonu else f"{secilen_plaka} BC"
                        
                        plakalar[secilen_plaka] = {
                            "sahibi": secilen_avci,
                            "tarih": formatli_tarih,
                            "tam_plaka": tam_plaka_str,
                            "plaka_sonu": plaka_sonu
                        }
                        plakalari_kaydet(plakalar)
                        st.success(f"{tam_plaka_str} başarıyla kaydedildi!")
                        st.rerun()

# --- KOLON 2: RAPORLAR ---
with col2:
    tab1, tab2, tab3 = st.tabs(["🏆 Liderlik & Karne", "🗺️ Bölgesel Durum", "📋 Tüm Liste"])
    
    # 1. SEKME: LİDERLİK
    with tab1:
        skor_dict = {isim: 0 for isim in avcilar}
        for _, detay in plakalar.items():
            if detay:
                isim = detay["sahibi"]
                if isim not in skor_dict: skor_dict[isim] = 0
                skor_dict[isim] += 1
        
        if sum(skor_dict.values()) > 0:
            df_skor = pd.DataFrame(list(skor_dict.items()), columns=["İsim", "Puan"])
            df_skor = df_skor.sort_values("Puan", ascending=False).reset_index(drop=True)
            
            st.markdown("##### 📊 Genel Sıralama")
            st.bar_chart(df_skor.set_index("İsim"), color="#FF4B4B")
            st.divider()
            
            st.markdown("### 🕵️ Avcı Karnesi")
            profil_secimi = st.selectbox("Avcı Seçiniz:", df_skor["İsim"].unique())
            
            if profil_secimi:
                kisi_koleksiyonu = []
                for p, d in plakalar.items():
                    if d and d["sahibi"] == profil_secimi:
                        sehir = TURKIYE_VERISI.get(p, {}).get("il", "-")
                        kisi_koleksiyonu.append({
                            "Plaka": d["tam_plaka"],
                            "Şehir": sehir,
                            "Tarih": d["tarih"]
                        })
                
                if kisi_koleksiyonu:
                    df_kisi = pd.DataFrame(kisi_koleksiyonu)
                    st.dataframe(df_kisi, hide_index=True, use_container_width=True)
                else:
                    st.warning("Kayıt yok.")
        else:
            st.info("Veri bekleniyor...")

    # 2. SEKME: BÖLGESEL
    with tab2:
        bolgeler = sorted(list(set(d["bolge"] for d in TURKIYE_VERISI.values())))
        secilen_bolge = st.selectbox("🌍 Bölge Seçin:", bolgeler)
        
        bolge_plakalari = [k for k, v in TURKIYE_VERISI.items() if v["bolge"] == secilen_bolge]
        toplam_bolge = len(bolge_plakalari)
        
        bolge_avcilari = []
        bulunan_sayisi = 0
        for p in bolge_plakalari:
            detay = plakalar.get(p)
            if detay:
                bulunan_sayisi += 1
                bolge_avcilari.append(detay["sahibi"])
        
        sahip_text = "Henüz Fethedilmedi 🏳️"
        sahip_renk = "gray"
        if bolge_avcilari:
            counts = Counter(bolge_avcilari)
            max_count = max(counts.values())
            liderler = [k for k, v in counts.items() if v == max_count]
            
            if len(liderler) == 1:
                sahip_text = f"👑 Bölgenin Sahibi: {liderler[0]}"
                sahip_renk = "green"
            else:
                sahip_text = f"⚔️ Bölgenin Sahipleri: {', '.join(liderler)}"
                sahip_renk = "orange"

        st.markdown(f":{sahip_renk}[**{sahip_text}**]")
        c1, c2 = st.columns(2)
        c1.metric("Toplam İl", f"{toplam_bolge}")
        c2.metric("Bulunan", f"{bulunan_sayisi}")
        st.progress(bulunan_sayisi / toplam_bolge if toplam_bolge > 0 else 0)
        
        durum_listesi = []
        for p_kodu in bolge_plakalari:
            sehir = TURKIYE_VERISI[p_kodu]["il"]
            detay = plakalar.get(p_kodu)
            if detay:
                durum_listesi.append({"Şehir": sehir, "Durum": "✅ Bulundu", "Plaka Detayı": detay['tam_plaka'], "Avcı": detay['sahibi']})
            else:
                durum_listesi.append({"Şehir": sehir, "Durum": "❌", "Plaka Detayı": f"{p_kodu} BC", "Avcı": "-"})
        st.dataframe(pd.DataFrame(durum_listesi), hide_index=True, use_container_width=True)

    # 3. SEKME: LİSTE
    with tab3:
        dolu_liste = []
        for p, d in plakalar.items():
            if d:
                il_adi = TURKIYE_VERISI.get(p, {}).get("il", "-")
                dolu_liste.append({"Plaka Kod": p, "Tam Plaka": d.get("tam_plaka", f"{p} BC"), "Şehir": il_adi, "Bulan": d["sahibi"], "Tarih": d["tarih"]})
        if dolu_liste:
            st.dataframe(pd.DataFrame(dolu_liste).sort_values("Plaka Kod"), hide_index=True, use_container_width=True)
        else:
            st.info("Kayıt yok.")