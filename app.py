import streamlit as st
import pandas as pd
import json
import os
from datetime import date
from collections import Counter
from github import Github

# --- AYARLAR ---
YONETICI_SIFRESI = "enver123" 

FILE_PLAKALAR = "plaka_data.json"
FILE_AVCILAR = "avcilar.json"
FILE_MADALYALAR = "madalyalar.json"
FILE_TANIMLAR = "madalya_tanimlari.json"
PLAKA_SAYISI = 81

# --- VARSAYILAN KATALOG ---
VARSAYILAN_KATALOG = {
    "Metropol Faresi": {"ikon": "🏙️", "desc": "3'ten fazla metropolü (34, 06, 35...) kemiren."},
    "Evliya Çelebi": {"ikon": "🌍", "desc": "Her coğrafi bölgeden (7 Bölge) ganimeti olan."},
    "Zoru Siken": {"ikon": "💪", "desc": "Nüfusu 300 binden düşük 5 şehri avlayan."},
    "Flash": {"ikon": "⚡", "desc": "24 saatte 2 plaka yakalayan hız tutkunu."},
    "İstanbul'un Sefiri": {"ikon": "🌉", "desc": "34 (İstanbul) plakasını ele geçiren."},
    "Yağmur Duası": {"ikon": "☔", "desc": "06 (Ankara) plakasını alan."},
    "Bok Kokusu": {"ikon": "🦨", "desc": "35 (İzmir) plakasını alan."},
    "Hamsi": {"ikon": "🐟", "desc": "61 (Trabzon) plakasını alan."},
    "Gökhan'ın Namusu": {"ikon": "🛡️", "desc": "61 (Trabzon) plakasını ele geçiren."},
    "Nurullah'ın Namusu": {"ikon": "🕊️", "desc": "31 (Hatay) plakasını ele geçiren."},
    "2002-2018 CHP": {"ikon": "🏖️", "desc": "5'ten fazla sahil şehrine sahip olan."}
}

# --- GITHUB BAĞLANTISI ---
try:
    GITHUB_TOKEN = st.secrets["github"]["token"]
    REPO_NAME = st.secrets["github"]["repo_name"]
except:
    st.error("Lütfen Streamlit Secrets ayarlarını yapın.")
    st.stop()

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

def github_update_json(filename, new_data, commit_message="Veri Guncelleme"):
    try:
        repo = get_repo()
        try:
            contents = repo.get_contents(filename)
            repo.update_file(contents.path, commit_message, json.dumps(new_data, indent=4, ensure_ascii=False), contents.sha)
        except:
            repo.create_file(filename, commit_message, json.dumps(new_data, indent=4, ensure_ascii=False))
        return True
    except Exception as e:
        st.error(f"GitHub Hatası: {e}")
        return False

# --- SABİT VERİLER (KOORDİNATLAR EKLENDİ) ---
TURKIYE_VERISI = {
    "01": {"il": "Adana", "bolge": "Akdeniz", "lat": 37.0000, "lon": 35.3213},
    "02": {"il": "Adıyaman", "bolge": "Güneydoğu Anadolu", "lat": 37.7648, "lon": 38.2786},
    "03": {"il": "Afyonkarahisar", "bolge": "Ege", "lat": 38.7507, "lon": 30.5567},
    "04": {"il": "Ağrı", "bolge": "Doğu Anadolu", "lat": 39.7191, "lon": 43.0503},
    "05": {"il": "Amasya", "bolge": "Karadeniz", "lat": 40.6499, "lon": 35.8353},
    "06": {"il": "Ankara", "bolge": "İç Anadolu", "lat": 39.9334, "lon": 32.8597},
    "07": {"il": "Antalya", "bolge": "Akdeniz", "lat": 36.8969, "lon": 30.7133},
    "08": {"il": "Artvin", "bolge": "Karadeniz", "lat": 41.1828, "lon": 41.8183},
    "09": {"il": "Aydın", "bolge": "Ege", "lat": 37.8444, "lon": 27.8458},
    "10": {"il": "Balıkesir", "bolge": "Marmara", "lat": 39.6484, "lon": 27.8826},
    "11": {"il": "Bilecik", "bolge": "Marmara", "lat": 40.1451, "lon": 29.9799},
    "12": {"il": "Bingöl", "bolge": "Doğu Anadolu", "lat": 38.8851, "lon": 40.4983},
    "13": {"il": "Bitlis", "bolge": "Doğu Anadolu", "lat": 38.4006, "lon": 42.1095},
    "14": {"il": "Bolu", "bolge": "Karadeniz", "lat": 40.7392, "lon": 31.6089},
    "15": {"il": "Burdur", "bolge": "Akdeniz", "lat": 37.7204, "lon": 30.2908},
    "16": {"il": "Bursa", "bolge": "Marmara", "lat": 40.1885, "lon": 29.0610},
    "17": {"il": "Çanakkale", "bolge": "Marmara", "lat": 40.1553, "lon": 26.4142},
    "18": {"il": "Çankırı", "bolge": "İç Anadolu", "lat": 40.6013, "lon": 33.6134},
    "19": {"il": "Çorum", "bolge": "Karadeniz", "lat": 40.5506, "lon": 34.9556},
    "20": {"il": "Denizli", "bolge": "Ege", "lat": 37.7765, "lon": 29.0864},
    "21": {"il": "Diyarbakır", "bolge": "Güneydoğu Anadolu", "lat": 37.9144, "lon": 40.2306},
    "22": {"il": "Edirne", "bolge": "Marmara", "lat": 41.6771, "lon": 26.5557},
    "23": {"il": "Elazığ", "bolge": "Doğu Anadolu", "lat": 38.6810, "lon": 39.2264},
    "24": {"il": "Erzincan", "bolge": "Doğu Anadolu", "lat": 39.7500, "lon": 39.5000},
    "25": {"il": "Erzurum", "bolge": "Doğu Anadolu", "lat": 39.9000, "lon": 41.2700},
    "26": {"il": "Eskişehir", "bolge": "İç Anadolu", "lat": 39.7767, "lon": 30.5206},
    "27": {"il": "Gaziantep", "bolge": "Güneydoğu Anadolu", "lat": 37.0662, "lon": 37.3833},
    "28": {"il": "Giresun", "bolge": "Karadeniz", "lat": 40.9128, "lon": 38.3895},
    "29": {"il": "Gümüşhane", "bolge": "Karadeniz", "lat": 40.4600, "lon": 39.4700},
    "30": {"il": "Hakkari", "bolge": "Doğu Anadolu", "lat": 37.5833, "lon": 43.7333},
    "31": {"il": "Hatay", "bolge": "Akdeniz", "lat": 36.4018, "lon": 36.3498},
    "32": {"il": "Isparta", "bolge": "Akdeniz", "lat": 37.7648, "lon": 30.5566},
    "33": {"il": "Mersin", "bolge": "Akdeniz", "lat": 36.8000, "lon": 34.6333},
    "34": {"il": "İstanbul", "bolge": "Marmara", "lat": 41.0082, "lon": 28.9784},
    "35": {"il": "İzmir", "bolge": "Ege", "lat": 38.4192, "lon": 27.1287},
    "36": {"il": "Kars", "bolge": "Doğu Anadolu", "lat": 40.6172, "lon": 43.0974},
    "37": {"il": "Kastamonu", "bolge": "Karadeniz", "lat": 41.3887, "lon": 33.7827},
    "38": {"il": "Kayseri", "bolge": "İç Anadolu", "lat": 38.7312, "lon": 35.4787},
    "39": {"il": "Kırklareli", "bolge": "Marmara", "lat": 41.7333, "lon": 27.2167},
    "40": {"il": "Kırşehir", "bolge": "İç Anadolu", "lat": 39.1425, "lon": 34.1709},
    "41": {"il": "Kocaeli", "bolge": "Marmara", "lat": 40.8533, "lon": 29.8815},
    "42": {"il": "Konya", "bolge": "İç Anadolu", "lat": 37.8667, "lon": 32.4833},
    "43": {"il": "Kütahya", "bolge": "Ege", "lat": 39.4167, "lon": 29.9833},
    "44": {"il": "Malatya", "bolge": "Doğu Anadolu", "lat": 38.3552, "lon": 38.3095},
    "45": {"il": "Manisa", "bolge": "Ege", "lat": 38.6191, "lon": 27.4289},
    "46": {"il": "Kahramanmaraş", "bolge": "Akdeniz", "lat": 37.5858, "lon": 36.9371},
    "47": {"il": "Mardin", "bolge": "Güneydoğu Anadolu", "lat": 37.3212, "lon": 40.7245},
    "48": {"il": "Muğla", "bolge": "Ege", "lat": 37.2153, "lon": 28.3636},
    "49": {"il": "Muş", "bolge": "Doğu Anadolu", "lat": 38.9462, "lon": 41.7539},
    "50": {"il": "Nevşehir", "bolge": "İç Anadolu", "lat": 38.6939, "lon": 34.6857},
    "51": {"il": "Niğde", "bolge": "İç Anadolu", "lat": 37.9667, "lon": 34.6833},
    "52": {"il": "Ordu", "bolge": "Karadeniz", "lat": 40.9839, "lon": 37.8764},
    "53": {"il": "Rize", "bolge": "Karadeniz", "lat": 41.0201, "lon": 40.5234},
    "54": {"il": "Sakarya", "bolge": "Marmara", "lat": 40.7569, "lon": 30.3783},
    "55": {"il": "Samsun", "bolge": "Karadeniz", "lat": 41.2867, "lon": 36.33},
    "56": {"il": "Siirt", "bolge": "Güneydoğu Anadolu", "lat": 37.9333, "lon": 41.95},
    "57": {"il": "Sinop", "bolge": "Karadeniz", "lat": 42.0231, "lon": 35.1531},
    "58": {"il": "Sivas", "bolge": "İç Anadolu", "lat": 39.7477, "lon": 37.0179},
    "59": {"il": "Tekirdağ", "bolge": "Marmara", "lat": 40.9833, "lon": 27.5167},
    "60": {"il": "Tokat", "bolge": "Karadeniz", "lat": 40.3167, "lon": 36.55},
    "61": {"il": "Trabzon", "bolge": "Karadeniz", "lat": 41.0015, "lon": 39.7178},
    "62": {"il": "Tunceli", "bolge": "Doğu Anadolu", "lat": 39.1079, "lon": 39.5401},
    "63": {"il": "Şanlıurfa", "bolge": "Güneydoğu Anadolu", "lat": 37.1591, "lon": 38.7969},
    "64": {"il": "Uşak", "bolge": "Ege", "lat": 38.6823, "lon": 29.4082},
    "65": {"il": "Van", "bolge": "Doğu Anadolu", "lat": 38.4891, "lon": 43.4089},
    "66": {"il": "Yozgat", "bolge": "İç Anadolu", "lat": 39.8181, "lon": 34.8147},
    "67": {"il": "Zonguldak", "bolge": "Karadeniz", "lat": 41.4564, "lon": 31.7987},
    "68": {"il": "Aksaray", "bolge": "İç Anadolu", "lat": 38.3687, "lon": 34.0370},
    "69": {"il": "Bayburt", "bolge": "Karadeniz", "lat": 40.2552, "lon": 40.2249},
    "70": {"il": "Karaman", "bolge": "İç Anadolu", "lat": 37.1759, "lon": 33.2287},
    "71": {"il": "Kırıkkale", "bolge": "İç Anadolu", "lat": 39.8468, "lon": 33.5153},
    "72": {"il": "Batman", "bolge": "Güneydoğu Anadolu", "lat": 37.8812, "lon": 41.1351},
    "73": {"il": "Şırnak", "bolge": "Güneydoğu Anadolu", "lat": 37.5164, "lon": 42.4611},
    "74": {"il": "Bartın", "bolge": "Karadeniz", "lat": 41.6344, "lon": 32.3375},
    "75": {"il": "Ardahan", "bolge": "Doğu Anadolu", "lat": 41.1105, "lon": 42.7022},
    "76": {"il": "Iğdır", "bolge": "Doğu Anadolu", "lat": 39.9196, "lon": 44.0404},
    "77": {"il": "Yalova", "bolge": "Marmara", "lat": 40.6500, "lon": 29.2667},
    "78": {"il": "Karabük", "bolge": "Karadeniz", "lat": 41.2061, "lon": 32.6204},
    "79": {"il": "Kilis", "bolge": "Güneydoğu Anadolu", "lat": 36.7184, "lon": 37.1212},
    "80": {"il": "Osmaniye", "bolge": "Akdeniz", "lat": 37.0742, "lon": 36.2476},
    "81": {"il": "Düzce", "bolge": "Karadeniz", "lat": 40.8438, "lon": 31.1565},
}

# --- YARDIMCI FONKSİYONLAR ---
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
    tanimlar = github_read_json(FILE_TANIMLAR)
    if not tanimlar: tanimlar = VARSAYILAN_KATALOG
    return avcilar, plakalar, madalyalar, tanimlar

# --- APP BAŞLANGICI ---
st.set_page_config(page_title="BC Plaka Takip", page_icon="🚙", layout="wide")

if 'veri_cache' not in st.session_state or st.query_params.get("refresh"):
    with st.spinner("Sunucudan veriler çekiliyor..."):
        avcilar, plakalar, madalyalar, tanimlar = veri_yukle_hepsi()
        st.session_state['avcilar'] = avcilar
        st.session_state['plakalar'] = plakalar
        st.session_state['madalyalar'] = madalyalar
        st.session_state['tanimlar'] = tanimlar

avcilar = st.session_state['avcilar']
plakalar = st.session_state['plakalar']
madalyalar = st.session_state['madalyalar']
tanimlar = st.session_state['tanimlar']

# --- SIDEBAR: YÖNETİCİ ---
with st.sidebar:
    st.header("🔒 Yönetici Paneli")
    if st.text_input("Şifre:", type="password") == YONETICI_SIFRESI:
        admin_mode = True
        st.success("Admin Girişi ✅")
        st.divider()
        
        # 1. Avcılar
        with st.expander("👤 Avcı Yönetimi"):
            yeni_isim = st.text_input("Yeni İsim:")
            if st.button("Ekle", use_container_width=True):
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

        # 2. Madalya Editör
        with st.expander("🏅 Madalya Editörü"):
            islem_tipi = st.radio("İşlem:", ["Düzenle", "Yeni Ekle"], horizontal=True)
            if islem_tipi == "Düzenle":
                secilen_edit = st.selectbox("Seç:", list(tanimlar.keys()))
                if secilen_edit:
                    yeni_ikon = st.text_input("İkon:", value=tanimlar[secilen_edit]["ikon"])
                    yeni_desc = st.text_input("Açıklama:", value=tanimlar[secilen_edit]["desc"])
                    c1, c2 = st.columns(2)
                    if c1.button("Güncelle 💾"):
                        tanimlar[secilen_edit] = {"ikon": yeni_ikon, "desc": yeni_desc}
                        github_update_json(FILE_TANIMLAR, tanimlar, "Madalya update")
                        st.rerun()
                    if c2.button("Sil 🗑️"):
                        del tanimlar[secilen_edit]
                        github_update_json(FILE_TANIMLAR, tanimlar, "Madalya delete")
                        st.rerun()
            else:
                y_isim = st.text_input("Adı:")
                y_ikon = st.text_input("İkon:", value="🏅")
                y_desc = st.text_input("Açıklama:")
                if st.button("Oluştur ✨"):
                    if y_isim:
                        tanimlar[y_isim] = {"ikon": y_ikon, "desc": y_desc}
                        github_update_json(FILE_TANIMLAR, tanimlar, "Yeni madalya")
                        st.rerun()

        st.divider()
        # 3. Dağıtım
        with st.expander("🎁 Madalya Dağıt", expanded=True):
            if not avcilar: st.warning("Avcı yok.")
            else:
                h_avci = st.selectbox("Kime:", avcilar)
                mevcutlar = madalyalar.get(h_avci, [])
                s_madalya = st.selectbox("Madalya:", list(tanimlar.keys()))
                c1, c2 = st.columns(2)
                if c1.button("Tak ➕", use_container_width=True):
                    if h_avci not in madalyalar: madalyalar[h_avci] = []
                    if s_madalya not in madalyalar[h_avci]:
                        madalyalar[h_avci].append(s_madalya)
                        github_update_json(FILE_MADALYALAR, madalyalar, "Takildi")
                        st.rerun()
                if c2.button("Sök ➖", use_container_width=True):
                    if h_avci in madalyalar and s_madalya in madalyalar[h_avci]:
                        madalyalar[h_avci].remove(s_madalya)
                        github_update_json(FILE_MADALYALAR, madalyalar, "Sokuldu")
                        st.rerun()
                st.caption(f"**{h_avci}** Rozetleri:")
                if mevcutlar:
                    valid = [m for m in mevcutlar if m in tanimlar]
                    st.write(", ".join([f"{tanimlar[m]['ikon']} {m}" for m in valid]))
                else: st.write("-")
    else:
        admin_mode = False

# --- ANA EKRAN ---
st.title("🚙 Plaka Avı (BC Serisi)")
st.markdown("---")

if admin_mode: col1, col2 = st.columns([1, 2])
else: col2 = st.container()

# --- SOL (GİRİŞ) ---
if admin_mode:
    with col1:
        st.subheader("📝 Kayıt Girişi")
        boslar = sorted([p for p, d in plakalar.items() if d is None])
        if not boslar:
            st.success("Bitti! 🎉")
        else:
            if not avcilar: st.warning("Avcı ekle!")
            else:
                with st.form("kayit"):
                    plaka = st.selectbox("Plaka:", boslar, format_func=lambda x: f"{x} BC ({TURKIYE_VERISI.get(x,{}).get('il','?')})")
                    sonu = st.text_input("Plaka Sonu:", placeholder="123", max_chars=5)
                    avci = st.selectbox("Bulan:", avcilar)
                    tarih = st.date_input("Tarih:", value=date.today(), format="DD/MM/YYYY")
                    if st.form_submit_button("Kaydet ✅"):
                        t_fmt = tarih.strftime("%d/%m/%Y")
                        tam = f"{plaka} BC {sonu}" if sonu else f"{plaka} BC"
                        plakalar[plaka] = {
                            "sahibi": avci, 
                            "tarih": t_fmt, 
                            "tam_plaka": tam, 
                            "plaka_sonu": sonu
                        }
                        github_update_json(FILE_PLAKALAR, plakalar, "Plaka eklendi")
                        st.success("Kaydedildi!")
                        st.rerun()

# --- SAĞ (RAPORLAR) ---
with col2:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Liderlik", "🗺️ Harita", "ℹ️ Rehber", "🌍 Bölge", "📋 Liste"])
    
    with tab1:
        skorlar = {isim: 0 for isim in avcilar}
        for _, d in plakalar.items():
            if d: skorlar[d["sahibi"]] += 1
        if sum(skorlar.values()) > 0:
            df = pd.DataFrame(list(skorlar.items()), columns=["İsim", "Puan"])
            df = df.sort_values("Puan", ascending=False).reset_index(drop=True)
            def rozet_getir(isim):
                if isim not in madalyalar or not madalyalar[isim]: return ""
                return " ".join([tanimlar[m]['ikon'] for m in madalyalar[isim] if m in tanimlar])
            df["Rozetler"] = df["İsim"].apply(rozet_getir)
            st.dataframe(df, hide_index=True, use_container_width=True,
                column_config={
                    "Puan": st.column_config.ProgressColumn("Skor", format="%d", min_value=0, max_value=81),
                    "Rozetler": st.column_config.TextColumn("Kazanılan Rozetler")
                })
        else: st.info("Veri yok.")

    # --- YENİ EKLENEN HARİTA SEKMESİ ---
    with tab2:
        st.subheader("📍 Türkiye Durumu")
        
        map_data = []
        for p_kodu, info in TURKIYE_VERISI.items():
            detay = plakalar.get(p_kodu)
            
            # Bulunanlar YEŞİL, Bulunmayanlar KIRMIZI
            color = "#00CC00" if detay else "#FF0000"
            size = 50000 if detay else 20000 # Bulunan noktalar daha büyük
            
            tooltip = f"{info['il']} ({p_kodu})"
            if detay:
                tooltip += f"\nAvcı: {detay['sahibi']}\nTarih: {detay['tarih']}"
            
            map_data.append({
                "lat": info["lat"], 
                "lon": info["lon"], 
                "color": color, 
                "size": size,
                "tooltip": tooltip
            })
            
        st.map(pd.DataFrame(map_data), latitude="lat", longitude="lon", color="color", size="size", zoom=4.5)
        st.caption("🟢 Yeşil: Bulundu | 🔴 Kırmızı: Aranıyor")
    # -----------------------------------

    with tab3:
        st.markdown("### 🎖️ Madalya Kataloğu")
        st.divider()
        cols = st.columns(2)
        keys = list(tanimlar.keys())
        for i, k in enumerate(keys):
            with cols[i % 2]:
                ikon = tanimlar[k]['ikon']
                aciklama = tanimlar[k]['desc']
                st.info(f"**{ikon} {k}**\n\n{aciklama}")

    with tab4:
        bolgeler = sorted(list(set(d["bolge"] for d in TURKIYE_VERISI.values())))
        secilen = st.selectbox("Bölge:", bolgeler)
        p_list = [k for k, v in TURKIYE_VERISI.items() if v["bolge"] == secilen]
        bulunan = [p for p in p_list if plakalar[p]]
        sahipler = [plakalar[p]["sahibi"] for p in bulunan]
        lider_txt = "Sahipsiz"
        if sahipler:
            cnt = Counter(sahipler)
            mx = max(cnt.values())
            liderler = [k for k, v in cnt.items() if v == mx]
            lider_txt = f"👑 {liderler[0]}" if len(liderler)==1 else f"⚔️ {', '.join(liderler)}"
        st.metric("Bölge Hakimi", lider_txt)
        st.progress(len(bulunan)/len(p_list))
        lst = []
        for p in p_list:
            d = plakalar[p]
            lst.append({"Şehir": TURKIYE_VERISI[p]["il"], "Durum": "✅" if d else "❌", "Detay": d["tam_plaka"] if d else "-", "Avcı": d["sahibi"] if d else "-"})
        st.dataframe(pd.DataFrame(lst), hide_index=True, use_container_width=True)

    with tab5:
        lst = []
        for p, d in plakalar.items():
            if d: lst.append({"Kod": p, "Tam Plaka": d["tam_plaka"], "Şehir": TURKIYE_VERISI[p]["il"], "Bulan": d["sahibi"]})
        if lst: st.dataframe(pd.DataFrame(lst), hide_index=True, use_container_width=True)
        else: st.info("Boş.")
