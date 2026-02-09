import streamlit as st
import random
import datetime
from collections import Counter

# --- METİN MOTORU (DATA BANK) ---
MANSET_SABLONLARI = [
    "BC'DE YER YERİNDEN OYNADI: {avci} ŞOV YAPIYOR!",
    "OPERASYON BAŞARIYLA TAMAMLANDI: {plaka} ARTIK BİZİM!",
    "FLAŞ GELİŞME: {sehir} DÜŞTÜ, KONSEY KARIŞTI!",
    "İSTİHBARAT DOĞRULADI: {avci} HEDEFİ 12'DEN VURDU!",
    "SOKAKLAR ONDAN SORULUR: {avci} DURDURULAMIYOR!",
    "PLAKA AVCILIĞINDA YENİ DÖNEM: {plaka} KAYITLARA GEÇTİ!",
    "GÖZLER ONA ÇEVRİLDİ: {avci} BUGÜN TARİH YAZDI!",
    "BİR GECE ANSIZIN GELEBİLİRİM DEMİŞTİ: {plaka} PAKETLENDİ!",
]

ALT_MANSETLER = [
    "Görgü tanıkları şokta: 'Böyle bir operasyon görmedik' dediler.",
    "Merkezden tebrik mesajı gecikmedi. Baronlar memnun.",
    "Rakipler kıskançlıktan çatlıyor. Piyasa alt üst oldu.",
    "Sessiz sedasız halletti, kimse ruhunu bile duymadı.",
    "Adeta bir hayalet gibi iz sürdü ve sonuca ulaştı.",
    "Bu başarı dilden dile dolaşmaya başladı bile.",
]

KOSE_YAZISI_BASLIKLARI = [
    "Sessizliğin Sesi", "Fırtına Öncesi", "Racon ve Adalet", 
    "Kurtlar Sofrası", "Bugün Neler Oldu?", "İz Sürenler"
]

KOSE_YAZISI_ICERIK_DOLU = [
    "Bugün piyasa hareketliydi yeğen. Birileri çalışıyor, birileri yatıyor. {lider} kardeşimi tebrik ederim, masaya yumruğunu vurdu. Ama diğerleri nerede? Bu alem boşluğu affetmez.",
    "Çakallar pusuda beklerken {lider} aslan gibi sahaya indi. Gelen istihbaratlar yüzümüzü güldürdü. {toplam} plaka az iş değil. Devamını bekliyoruz.",
    "Eskiden buralar dutluktu, şimdi {lider} sayesinde plaka tarlasına döndü. Çalışan kazanır, elması kızarır. Bu operasyon tarihe geçer.",
    "Bazı günler vardır, tarih yazılır. Bugün o günlerden biri. Ekip zehir gibi. {lider} başı çekiyor ama arkası da sağlam gelmeli. Uyuma BC!",
]

KOSE_YAZISI_ICERIK_BOS = [
    "Bugün yaprak kımıldamıyor. Herkes tatilde mi? Yoksa büyük bir operasyonun hazırlığı mı var? Sessizlik hayra alamet değildir yeğen...",
    "Masa boş, çaylar soğuk. Bugün istihbarat akışı kesildi. Ajanlarımız uyuyor mu? Bu sessizlik fırtına öncesi sessizliği olsun diye dua ediyoruz.",
    "Paslandık mı ne? Bugün tek bir plaka bile düşmedi. Alemin gözü üzerimizde, bu durgunluk bize yakışmaz. Yarın telafi bekliyorum.",
    "Rüzgar esmiyor, yaprak düşmüyor. Bugün kayıtlara 'Sessiz Gün' olarak geçti. Umarım yarın telafi edilir, yoksa Baron kızacak.",
]

EKONOMI_YORUMLARI = [
    "Plaka Borsası: YÜKSELİŞTE 📈", "Plaka Borsası: DURGUN 📉", 
    "Benzin: HEP PAHALI ⛽", "Moral: ZİRVEDE 🔥", "Risk Primi: DÜŞÜK 🟢"
]

# --- YARDIMCI FONKSİYONLAR ---

def tarih_formatla(tarih_str):
    """DD/MM/YYYY formatını datetime objesine çevirir"""
    try:
        return datetime.datetime.strptime(tarih_str, "%d/%m/%Y").date()
    except:
        return None

def gunun_yildizini_bul(gunluk_veriler):
    """O gün en çok plaka bulanı bulur"""
    if not gunluk_veriler: return None, 0
    avcilar = [v['sahibi'] for v in gunluk_veriler]
    counts = Counter(avcilar)
    top_avci = counts.most_common(1)[0]
    return top_avci[0], top_avci[1] # (İsim, Sayı)

def rastgele_haber_uret(lider, plaka_kodu, sehir_adi, toplam_sayi):
    """Parametrelere göre rastgele şablon seçip doldurur"""
    sablon = random.choice(MANSET_SABLONLARI)
    haber = sablon.format(avci=lider, plaka=plaka_kodu, sehir=sehir_adi)
    alt = random.choice(ALT_MANSETLER)
    return haber, alt

def kose_yazisi_yaz(lider, toplam_sayi):
    """Gölge Adam köşe yazısı yazar"""
    baslik = random.choice(KOSE_YAZISI_BASLIKLARI)
    
    if toplam_sayi > 0:
        sablon = random.choice(KOSE_YAZISI_ICERIK_DOLU)
        icerik = sablon.format(lider=lider, toplam=toplam_sayi)
    else:
        sablon = random.choice(KOSE_YAZISI_ICERIK_BOS)
        icerik = sablon
        
    return baslik, icerik

# --- ANA FONKSİYON ---

def gazete_sayfasi_olustur(plakalar, turkiye_verisi):
    st.markdown("""
    <style>
        .gazete-header {
            font-family: 'Times New Roman', serif;
            text-align: center;
            border-bottom: 3px double #444;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .gazete-title {
            font-size: 50px;
            font-weight: bold;
            color: #eee;
            text-shadow: 2px 2px 4px #000;
            letter-spacing: 2px;
        }
        .gazete-date {
            font-size: 16px;
            color: #aaa;
            font-style: italic;
        }
        .manset-kutu {
            background-color: #262730;
            padding: 20px;
            border: 1px solid #444;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .manset-title {
            font-size: 32px;
            font-weight: 900;
            color: #FF4B4B;
            font-family: 'Arial Black', sans-serif;
            line-height: 1.2;
        }
        .manset-spot {
            font-size: 18px;
            color: #ccc;
            margin-top: 10px;
            font-style: italic;
        }
        .kose-yazisi {
            background-color: #1E1E1E;
            padding: 15px;
            border-left: 4px solid #FFD700;
            margin-top: 10px;
        }
        .kose-baslik {
            font-weight: bold;
            font-size: 20px;
            color: #FFD700;
        }
        .kose-imza {
            text-align: right;
            font-weight: bold;
            font-family: 'Brush Script MT', cursive;
            color: #888;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # 1. VERİLERİ TARİHE GÖRE GRUPLA
    tarih_bazli = {}
    for plaka, detay in plakalar.items():
        if detay and detay.get("tarih"):
            t = detay["tarih"]
            # Tarih formatı kontrolü
            dt = tarih_formatla(t)
            if dt:
                if dt not in tarih_bazli: tarih_bazli[dt] = []
                tarih_bazli[dt].append({"plaka": plaka, **detay})

    # Tarihleri sırala (Yeniden eskiye)
    sirali_tarihler = sorted(tarih_bazli.keys(), reverse=True)
    
    if not sirali_tarihler:
        st.info("Henüz gazete basılacak kadar veri yok.")
        return

    # 2. TARİH SEÇİCİ
    st.markdown('<div class="gazete-header"><div class="gazete-title">BC RESMİ GAZETE</div><div class="gazete-date">"Gerçeklerin Yazıldığı Tek Yer"</div></div>', unsafe_allow_html=True)
    
    secilen_tarih = st.selectbox("📅 Arşivden Seç:", sirali_tarihler, format_func=lambda x: x.strftime("%d %B %Y, %A"))
    
    # 3. SEÇİLEN GÜNÜN VERİLERİ
    gunun_olaylari = tarih_bazli[secilen_tarih]
    toplam_olay = len(gunun_olaylari)
    lider, lider_skor = gunun_yildizini_bul(gunun_olaylari)
    
    # Veri hazırlığı (Rastgelelik için)
    ornek_olay = random.choice(gunun_olaylari)
    ornek_sehir = turkiye_verisi.get(ornek_olay['plaka'], {}).get('il', 'Bilinmeyen Şehir')
    
    # 4. İÇERİK ÜRETİMİ
    manset, spot = rastgele_haber_uret(lider, ornek_olay['plaka'], ornek_sehir, toplam_olay)
    ky_baslik, ky_icerik = kose_yazisi_yaz(lider, toplam_olay)
    
    # --- GAZETE DÜZENİ ---
    
    # Manşet Alanı
    st.markdown(f"""
    <div class="manset-kutu">
        <div class="manset-title">{manset}</div>
        <div class="manset-spot">{spot}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_news, col_column = st.columns([2, 1])
    
    with col_news:
        st.subheader("📍 Günün Raporu")
        st.markdown(f"**Tarih:** {secilen_tarih.strftime('%d.%m.%Y')} | **Toplam Operasyon:** {toplam_olay} | **Günün Lideri:** {lider}")
        st.divider()
        
        for olay in gunun_olaylari:
            p_kodu = olay['plaka']
            sehir = turkiye_verisi.get(p_kodu, {}).get('il', '')
            avci = olay['sahibi']
            notu = olay.get('not', '-')
            
            st.markdown(f"""
            #### 🚔 {p_kodu} - {sehir} Yakalandı!
            * **Operasyonu Yapan:** {avci}
            * **İstihbarat Notu:** *"{notu}"*
            """)
            st.markdown("---")
            
    with col_column:
        # Köşe Yazısı
        st.markdown(f"""
        <div class="kose-yazisi">
            <div class="kose-baslik">✒️ {ky_baslik}</div>
            <p style="margin-top:10px; font-family: serif; font-size: 17px;">{ky_icerik}</p>
            <div class="kose-imza">- Gölge Adam</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Piyasa Durumu
        st.subheader("💰 Piyasa")
        st.info(f"📊 {random.choice(EKONOMI_YORUMLARI)}")
        st.info(f"☁️ Operasyon Havası: {random.choice(['GÜNEŞLİ', 'PARÇALI BULUTLU', 'SİSLİ VE PUSLU', 'FIRTINALI'])}")
        
        st.divider()
        st.caption("BC Medya Grubu © 2026")
