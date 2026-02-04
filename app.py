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
PLAKA_SAYISI = 81

# --- YENİ MADALYA KATALOGU (GÜNCELLENDİ) ---
MADALYA_KATALOGU = {
    "Metropol Faresi": {
        "ikon": "🏙️", 
        "desc": "3'ten fazla metropolü (34, 06, 35, 16, 01, 41, 27, 42) kemiren."
    },
    "Evliya Çelebi": {
        "ikon": "🌍", 
        "desc": "Her coğrafi bölgeden (7 Bölge) en az bir ganimeti olan."
    },
    "Zoru Siken": {
        "ikon": "💪", 
        "desc": "Nüfusu 300 binden düşük 5 farklı şehri avlayan (Zor işi seven)."
    },
    "Flash": {
        "ikon": "⚡", 
        "desc": "24 saat içerisinde 2 farklı plaka yakalayan hız tutkunu."
    },
    "İstanbul'un Sefiri": {
        "ikon": "🌉", 
        "desc": "34 (İstanbul) plakasını ele geçiren semtin abisi."
    },
    "Yağmur Duası": {
        "ikon": "☔", 
        "desc": "06 (Ankara) plakasını alan (Gri gökyüzünün efendisi)."
    },
    "Bok Kokusu": {
        "ikon": "🦨", 
        "desc": "35 (İzmir) plakasını alan."
    },
    "Hamsi": {
        "ikon": "🐟", 
        "desc": "61 (Trabzon) plakasını alan."
    },
    "Gökhan'ın Namusu": {
        "ikon": "🛡️", 
        "desc": "61 (Trabzon) plakasını ele geçiren (Gökhan'ın emaneti)."
    },
    "Nurullah'ın Namusu": {
        "ikon": "🕊️", 
        "desc": "31 (Hatay) plakasını ele geçiren (Nurullah'ın emaneti)."
    },
    "2002-2018 CHP": {
        "ikon": "🏖️", 
        "desc": "5'ten fazla sahil şehrine (Ege/Akdeniz kıyı şeridi) sahip olan."
    }
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
    return avcilar, plakalar, madalyalar

# --- APP BAŞLANGICI ---
st.set_page_config(page_title="BC Plaka Takip", page_icon="🚙", layout="wide")

if 'veri_cache' not in st.session_state or st.query_params.get("refresh"):
    with st.spinner("Sunucudan veriler çekiliyor..."):
        avcilar, plakalar, madalyalar = veri_yukle_hepsi()
        st.session_state['avcilar'] = avcilar
        st.session_state['plakalar'] = plakalar
        st.session_state['madalyalar'] = madalyalar

avcilar = st.session_state['avcilar']
plakalar = st.session_state['plakalar']
madalyalar = st.session_state['madalyalar']

# --- SIDEBAR: YÖNETİCİ ---
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

        st.divider()
        with st.expander("🏅 Madalya Dağıtım Ofisi", expanded=True):
            if not avcilar:
                st.warning("Önce avcı ekleyin.")
            else:
                hedef_avci = st.selectbox("Kime Verilecek?", avcilar)
                mevcutlar = madalyalar.get(hedef_avci, [])
                secilen_madalya = st.selectbox("Hangi Madalya?", list(MADALYA_KATALOGU.keys()))
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Tak ➕", use_container_width=True):
                        if hedef_avci not in madalyalar: madalyalar[hedef_avci] = []
                        if secilen_madalya not in madalyalar[hedef_avci]:
                            madalyalar[hedef_avci].append(secilen_madalya)
                            github_update_json(FILE_MADALYALAR, madalyalar, "Madalya takildi")
                            st.success(f"{secilen_madalya} takıldı!")
                            st.rerun()
                        else:
                            st.warning("Zaten var.")
                with c2:
                    if st.button("Sök ➖", use_container_width=True):
                        if hedef_avci in madalyalar and secilen_madalya in madalyalar[hedef_avci]:
                            madalyalar[hedef_avci].remove(secilen_madalya)
                            github_update_json(FILE_MADALYALAR, madalyalar, "Madalya sokuldu")
                            st.warning(f"{secilen_madalya} geri alındı!")
                            st.rerun()
                            
                st.caption(f"**{hedef_avci}** Sahibinin Rozetleri:")
                if mevcutlar:
                    st.write(", ".join([f"{MADALYA_KATALOGU[m]['ikon']} {m}" for m in mevcutlar]))
                else:
                    st.write("-")
    else:
        admin_mode = False
        st.info("Veri girişi ve madalya dağıtımı sadece yöneticiye aittir.")

# --- ANA EKRAN ---
st.title("🚙 Plaka Avı (BC Serisi)")
st.markdown("---")

if admin_mode: col1, col2 = st.columns([1, 2])
else: col2 = st.container()

# --- SOL KOLON ---
if admin_mode:
    with col1:
        st.subheader("📝 Kayıt Girişi")
        boslar = sorted([p for p, d in plakalar.items() if d is None])
        if not boslar:
            st.success("Bitti! 🎉")
        else:
            if not avcilar: st.warning("Avcı yok!")
            else:
                with st.form("kayit"):
                    plaka = st.selectbox("Plaka:", boslar, format_func=lambda x: f"{x} BC ({TURKIYE_VERISI.get(x,{}).get('il','?')})")
                    sonu = st.text_input("Plaka Sonu:", placeholder="123", max_chars=5)
                    avci = st.selectbox("Bulan:", avcilar)
                    tarih = st.date_input("Tarih:", value=date.today(), format="DD/MM/YYYY")
                    if st.form_submit_button("Kaydet ✅"):
                        t_fmt = tarih.strftime("%d/%m/%Y")
                        tam = f"{plaka} BC {sonu}" if sonu else f"{plaka} BC"
                        plakalar[plaka] = {"sahibi": avci, "tarih": t_fmt, "tam_plaka": tam, "plaka_sonu": sonu}
                        github_update_json(FILE_PLAKALAR, plakalar, "Plaka eklendi")
                        st.success("Kaydedildi!")
                        st.rerun()

# --- SAĞ KOLON ---
with col2:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Liderlik & Rozetler", "ℹ️ Madalya Rehberi", "📈 Zaman", "🗺️ Bölge", "📋 Liste"])
    
    with tab1:
        skorlar = {isim: 0 for isim in avcilar}
        for _, d in plakalar.items():
            if d: skorlar[d["sahibi"]] += 1
            
        if sum(skorlar.values()) > 0:
            df = pd.DataFrame(list(skorlar.items()), columns=["İsim", "Puan"])
            df = df.sort_values("Puan", ascending=False).reset_index(drop=True)
            def rozet_getir(isim):
                if isim not in madalyalar or not madalyalar[isim]: return ""
                return " ".join([MADALYA_KATALOGU[m]['ikon'] for m in madalyalar[isim]])
            df["Rozetler"] = df["İsim"].apply(rozet_getir)
            st.dataframe(df, hide_index=True, use_container_width=True,
                column_config={
                    "Puan": st.column_config.ProgressColumn("Skor", format="%d", min_value=0, max_value=81),
                    "Rozetler": st.column_config.TextColumn("Kazanılan Rozetler")
                })
        else: st.info("Henüz veri yok.")

    with tab2:
        st.markdown("### 🎖️ Madalya ve Unvan Kataloğu")
        st.write("Bu rozetler, üstün başarı gösteren avcılara **Game Master (Admin)** tarafından takılır.")
        st.divider()
        cols = st.columns(2)
        keys = list(MADALYA_KATALOGU.keys())
        for i, k in enumerate(keys):
            with cols[i % 2]:
                ikon = MADALYA_KATALOGU[k]['ikon']
                aciklama = MADALYA_KATALOGU[k]['desc']
                st.info(f"**{ikon} {k}**\n\n{aciklama}")

    with tab3:
        data_time = []
        for _, d in plakalar.items():
            if d:
                try:
                    dt = pd.to_datetime(d["tarih"], dayfirst=True)
                    data_time.append({"Tarih": dt, "İsim": d["sahibi"]})
                except: pass
        if data_time:
            df_t = pd.DataFrame(data_time)
            df_p = df_t.pivot_table(index='Tarih', columns='İsim', aggfunc='size', fill_value=0).cumsum()
            st.line_chart(df_p)
        else: st.info("Veri yok.")

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
