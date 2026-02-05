import streamlit as st
import pandas as pd
import json
import requests
from collections import Counter
from github import Github
import plotly.express as px

# --- AYARLAR ---
try:
    GITHUB_TOKEN = st.secrets["github"]["token"]
    REPO_NAME = st.secrets["github"]["repo_name"]
    YONETICI_SIFRESI = st.secrets["admin_password"]
except:
    st.error("Lütfen Streamlit Secrets ayarlarını yapın.")
    st.stop()

FILE_PLAKALAR = "plaka_data.json"
FILE_AVCILAR = "avcilar.json"
FILE_MADALYALAR = "madalyalar.json"
FILE_TANIMLAR = "madalya_tanimlari.json"
PLAKA_SAYISI = 81
GEOJSON_URL = "https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json"

# --- SABİT VERİLER ---
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

BOLGE_MERKEZLERI = {
    "Marmara": {"lat": 40.2, "lon": 28.0},
    "Ege": {"lat": 38.5, "lon": 28.5},
    "Akdeniz": {"lat": 36.8, "lon": 33.0},
    "İç Anadolu": {"lat": 39.0, "lon": 33.5},
    "Karadeniz": {"lat": 40.8, "lon": 37.0},
    "Doğu Anadolu": {"lat": 39.0, "lon": 41.0},
    "Güneydoğu Anadolu": {"lat": 37.5, "lon": 40.0}
}

RENK_PALETI = ["#DC143C", "#008000", "#1E90FF", "#FFD700", "#9932CC", "#FF8C00", "#00CED1"]

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
    "2002-2018 CHP": {"ikon": "🏖️", "desc": "5'ten fazla sahil şehrine sahip olan."},
    "Şark Görevi": {"ikon": "🪖", "desc": "Doğu'nun en sert illerini (30, 73, 62) toplayan asker."},
    "Trakya Lordu": {"ikon": "🌻", "desc": "Tekirdağ, Edirne, Kırklareli üçlüsünü 'beya' diyerek toplayan."},
    "Güneşe Ateş Eden": {"ikon": "🔥", "desc": "01 Adana'yı bulan. Acıya dayanıklı."},
    "Kutsal Topraklar": {"ikon": "📿", "desc": "Konya (42) ve Urfa (63) ile huzura eren."},
    "Bayburt Gerçeği": {"ikon": "👻", "desc": "69 Bayburt'u bulup varlığını kanıtlayan."},
    "Yazlıkçı": {"ikon": "🏖️", "desc": "Muğla (48) ve Antalya (07) ile bronzlaşan."},
    "Çift Okey": {"ikon": "🎲", "desc": "11, 22, 33... Çift sayı kodlu 3 şehir bulan."},
    "Plaka Mafyası": {"ikon": "🔫", "desc": "30 plakayı geçip racon kesen."},
    "Son Durak": {"ikon": "🏁", "desc": "81 Düzce'yi bulup haritayı kapatan."},
    "Holigan": {"ikon": "🧨", "desc": "Plaka sonu takım tarihi (1903/05/07/67) olanı yakalayan."},
    "Memur Spec": {"ikon": "💼", "desc": "Ankara, Kırıkkale, Eskişehir üçgenini kuran."}
}

# --- GITHUB İŞLEMLERİ ---
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

# --- YARDIMCI FONKSİYONLAR ---
def format_plaka(no): return f"{int(no):02d}"
def tarihi_duzelt(t): return t.split("-")[2]+"/"+t.split("-")[1]+"/"+t.split("-")[0] if "-" in t else t

# --- HIZLANDIRMA: HARİTAYI ÖNBELLEĞE AL ---
@st.cache_data(ttl=86400)
def harita_verisi_cek():
    try:
        r = requests.get(GEOJSON_URL)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

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
    else: 
        for k, v in VARSAYILAN_KATALOG.items():
            if k not in tanimlar:
                tanimlar[k] = v
    
    return avcilar, plakalar, madalyalar, tanimlar

# --- APP BAŞLANGICI ---
st.set_page_config(page_title="BC Plaka Takip", page_icon="🚙", layout="wide")

# Verileri Çek
if 'veri_cache' not in st.session_state or st.query_params.get("refresh"):
    with st.spinner("Veriler güncelleniyor..."):
        avcilar, plakalar, madalyalar, tanimlar = veri_yukle_hepsi()
        st.session_state['avcilar'] = avcilar
        st.session_state['plakalar'] = plakalar
        st.session_state['madalyalar'] = madalyalar
        st.session_state['tanimlar'] = tanimlar

avcilar = st.session_state['avcilar']
plakalar = st.session_state['plakalar']
madalyalar = st.session_state['madalyalar']
tanimlar = st.session_state['tanimlar']

# --- SIDEBAR (ADMİN) ---
with st.sidebar:
    st.header("🔒 Yönetici Paneli")
    if st.text_input("Şifre:", type="password") == YONETICI_SIFRESI:
        admin_mode = True
        st.success("Admin Girişi ✅")
        st.divider()
        
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

# Veri Girişi (Sadece Admin)
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
                    notu = st.text_area("Hikayesi (Opsiyonel):", placeholder="Örn: Köprü trafiğinde gördüm...")
                    avci = st.selectbox("Bulan:", avcilar)
                    tarih = st.date_input("Tarih:", value=date.today(), format="DD/MM/YYYY")
                    
                    # DÜZELTME: Submit butonu formun içine alındı
                    submitted = st.form_submit_button("Kaydet ✅")
                    
                    if submitted:
                        t_fmt = tarih.strftime("%d/%m/%Y")
                        tam = f"{plaka} BC {sonu}" if sonu else f"{plaka} BC"
                        plakalar[plaka] = {"sahibi": avci, "tarih": t_fmt, "tam_plaka": tam, "plaka_sonu": sonu, "not": notu}
                        github_update_json(FILE_PLAKALAR, plakalar, "Plaka eklendi")
                        st.success("Kaydedildi!")
                        st.rerun()

# Raporlar
with col2:
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Liderlik", "ℹ️ Rehber", "🌍 Bölge & Harita", "📋 Liste"])
    
    # 1. LİDERLİK TABLOSU (HTML DÜZELTİLDİ)
    with tab1:
        skorlar = {isim: 0 for isim in avcilar}
        for _, d in plakalar.items():
            if d: skorlar[d["sahibi"]] += 1
        if sum(skorlar.values()) > 0:
            df = pd.DataFrame(list(skorlar.items()), columns=["İsim", "Puan"])
            df = df.sort_values("Puan", ascending=False).reset_index(drop=True)
            
            # CSS Stilini ayırıyoruz (Render hatasını önler)
            st.markdown("""
            <style>
                .custom-table {width: 100%; border-collapse: collapse; font-family: sans-serif;}
                .custom-table th, .custom-table td {padding: 12px; text-align: left; border-bottom: 1px solid #444;}
                .custom-table tr:hover {background-color: #262730;}
                .tooltip {position: relative; display: inline-block; cursor: help; font-size: 20px; margin-right: 8px;}
                .bar-bg {background-color: #31333F; width: 100%; border-radius: 4px; height: 8px; margin-top: 5px;}
                .bar-fill {background-color: #FF4B4B; height: 100%; border-radius: 4px;}
            </style>
            """, unsafe_allow_html=True)
            
            # Tabloyu oluştur (Girintileri kaldırdık)
            rows_html = ""
            for index, row in df.iterrows():
                isim = row['İsim']
                puan = row['Puan']
                yuzde = (puan / PLAKA_SAYISI) * 100
                
                rozetler_html = ""
                kisi_madalyalar = madalyalar.get(isim, [])
                for m in kisi_madalyalar:
                    if m in tanimlar:
                        ikon = tanimlar[m]['ikon']
                        desc = tanimlar[m]['desc']
                        # Tooltip (Title attribute)
                        rozetler_html += f'<span class="tooltip" title="{m}: {desc}">{ikon}</span>'
                
                rows_html += f"""
                <tr>
                    <td style="width: 25%;"><strong>{isim}</strong></td>
                    <td style="width: 40%;">
                        <div style="display: flex; align-items: center;">
                            <span style="font-weight: bold; margin-right: 10px;">{puan}</span>
                            <div class="bar-bg"><div class="bar-fill" style="width: {yuzde}%;"></div></div>
                        </div>
                    </td>
                    <td>{rozetler_html}</td>
                </tr>"""
            
            # Tabloyu birleştir ve bas
            full_table = f"""
            <table class="custom-table">
                <thead><tr style="color: #999;"><th>İsim</th><th>Skor</th><th>Rozetler (Üzerine Gel)</th></tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
            """
            st.markdown(full_table, unsafe_allow_html=True)
            
        else: st.info("Veri yok.")

    # 2. REHBER
    with tab2:
        st.markdown("### 🎖️ Madalya Kataloğu")
        st.divider()
        cols = st.columns(2)
        keys = list(tanimlar.keys())
        for i, k in enumerate(keys):
            with cols[i % 2]:
                ikon = tanimlar[k]['ikon']
                aciklama = tanimlar[k]['desc']
                st.info(f"**{ikon} {k}**\n\n{aciklama}")

    # 3. BÖLGE VE HARİTA
    with tab3:
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

        st.divider()
        st.subheader("📍 Türkiye Hakimiyet Haritası")
        
        geojson_data = harita_verisi_cek()
        if geojson_data:
            bolge_hakimleri = {}
            bolge_listesi = set(d["bolge"] for d in TURKIYE_VERISI.values())
            avci_renkleri = {avci: RENK_PALETI[i % len(RENK_PALETI)] for i, avci in enumerate(avcilar)}
            avci_renkleri["Sahipsiz"] = "#444444"
            avci_renkleri["Çekişmeli"] = "#222222"

            for bolge in bolge_listesi:
                p_list_h = [k for k, v in TURKIYE_VERISI.items() if v["bolge"] == bolge]
                bulunan_h = [p for p in p_list_h if plakalar[p]]
                sahipler_h = [plakalar[p]["sahibi"] for p in bulunan_h]
                if not sahipler_h: bolge_hakimleri[bolge] = "Sahipsiz"
                else:
                    cnt = Counter(sahipler_h)
                    mx = max(cnt.values())
                    lids = [k for k, v in cnt.items() if v == mx]
                    bolge_hakimleri[bolge] = lids[0] if len(lids) == 1 else "Çekişmeli"

            map_rows = []
            for p_kodu, info in TURKIYE_VERISI.items():
                map_rows.append({"İl": info["il"], "Bölge": info["bolge"], "Hakim Avcı": bolge_hakimleri.get(info["bolge"], "Sahipsiz")})
            
            fig = px.choropleth(
                pd.DataFrame(map_rows), geojson=geojson_data, locations="İl", featureidkey="properties.name",
                color="Hakim Avcı", color_discrete_map=avci_renkleri, projection="mercator", hover_data=["Bölge"]
            )
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            
            for b_adi, krd in BOLGE_MERKEZLERI.items():
                hkm = bolge_hakimleri.get(b_adi, "Sahipsiz")
                if hkm != "Sahipsiz":
                    fig.add_annotation(x=krd["lon"], y=krd["lat"], text=hkm, showarrow=False,
                        font=dict(family="Arial Black", size=14, color="white"), bgcolor="rgba(0,0,0,0.5)")

            st.plotly_chart(fig, use_container_width=True)
        else: st.warning("Harita yükleniyor...")

    # 4. LİSTE
    with tab4:
        lst = []
        for p, d in plakalar.items():
            if d: lst.append({"Kod": p, "Tam Plaka": d["tam_plaka"], "Şehir": TURKIYE_VERISI[p]["il"], "Bulan": d["sahibi"]})
        if lst: st.dataframe(pd.DataFrame(lst), hide_index=True, use_container_width=True)
        else: st.info("Boş.")
