import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from collections import Counter

# Harita verisini önbelleğe alan fonksiyon (Hız için)
@st.cache_data(ttl=86400)
def harita_verisi_cek(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def harita_sayfasi_olustur(plakalar, avcilar, turkiye_verisi, bolge_merkezleri, renk_paleti, geojson_url):
    """
    Bölge analizlerini ve Türkiye hakimiyet haritasını çizer.
    """
    
    # --- 1. KISIM: BÖLGESEL İSTATİSTİKLER ---
    bolgeler = sorted(list(set(d["bolge"] for d in turkiye_verisi.values())))
    secilen = st.selectbox("Bölge Seç:", bolgeler)
    
    # Seçilen bölgedeki plakalar
    p_list = [k for k, v in turkiye_verisi.items() if v["bolge"] == secilen]
    bulunan = [p for p in p_list if plakalar[p]]
    sahipler = [plakalar[p]["sahibi"] for p in bulunan]
    
    # Lideri Hesapla
    lider_txt = "Sahipsiz"
    if sahipler:
        cnt = Counter(sahipler)
        mx = max(cnt.values())
        liderler = [k for k, v in cnt.items() if v == mx]
        lider_txt = f"👑 {liderler[0]}" if len(liderler)==1 else f"⚔️ {', '.join(liderler)}"
    
    # Metrikleri Göster
    st.metric(f"{secilen} Bölgesi Hakimi", lider_txt)
    st.progress(len(bulunan)/len(p_list))
    
    # Bölge Tablosu
    lst = []
    for p in p_list:
        d = plakalar[p]
        durum_ikon = "✅" if d else "❌"
        avci_isim = d["sahibi"] if d else "-"
        detay = d["tam_plaka"] if d else "-"
        
        lst.append({
            "Şehir": turkiye_verisi[p]["il"], 
            "Durum": durum_ikon, 
            "Detay": detay, 
            "Avcı": avci_isim
        })
    st.dataframe(pd.DataFrame(lst), hide_index=True, use_container_width=True)

    st.divider()

    # --- 2. KISIM: HAKİMİYET HARİTASI ---
    st.subheader("📍 Türkiye Hakimiyet Haritası")
    
    geojson_data = harita_verisi_cek(geojson_url)
    
    if geojson_data:
        # Bölge Hakimlerini Hesapla
        bolge_hakimleri = {}
        bolge_listesi = set(d["bolge"] for d in turkiye_verisi.values())
        
        # Renkleri Ayarla
        avci_renkleri = {avci: renk_paleti[i % len(renk_paleti)] for i, avci in enumerate(avcilar)}
        avci_renkleri["Sahipsiz"] = "#444444"
        avci_renkleri["Çekişmeli"] = "#222222"

        for bolge in bolge_listesi:
            # O bölgedeki tüm illeri bul
            p_list_h = [k for k, v in turkiye_verisi.items() if v["bolge"] == bolge]
            # O bölgede bulunan plakaları bul
            bulunan_h = [p for p in p_list_h if plakalar[p]]
            # Sahiplerini listele
            sahipler_h = [plakalar[p]["sahibi"] for p in bulunan_h]
            
            if not sahipler_h:
                bolge_hakimleri[bolge] = "Sahipsiz"
            else:
                cnt = Counter(sahipler_h)
                mx = max(cnt.values())
                lids = [k for k, v in cnt.items() if v == mx]
                # Tek lider varsa onu yaz, eşitlik varsa Çekişmeli yaz
                bolge_hakimleri[bolge] = lids[0] if len(lids) == 1 else "Çekişmeli"

        # Harita Veri Setini (DataFrame) Hazırla
        map_rows = []
        for p_kodu, info in turkiye_verisi.items():
            bolge = info["bolge"]
            hakim = bolge_hakimleri.get(bolge, "Sahipsiz")
            map_rows.append({
                "İl": info["il"], 
                "Bölge": bolge, 
                "Hakim Avcı": hakim
            })
        
        # Plotly ile Çiz
        fig = px.choropleth(
            pd.DataFrame(map_rows), 
            geojson=geojson_data, 
            locations="İl", 
            featureidkey="properties.name",
            color="Hakim Avcı", 
            color_discrete_map=avci_renkleri, 
            projection="mercator", 
            hover_data=["Bölge"]
        )
        
        # Görsel Ayarlar
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0}, 
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)",
            legend_title_text="Bölge Hakimi"
        )
        
        # İsimleri Harita Üzerine Yaz
        for b_adi, krd in bolge_merkezleri.items():
            hkm = bolge_hakimleri.get(b_adi, "Sahipsiz")
            if hkm != "Sahipsiz":
                fig.add_annotation(
                    x=krd["lon"], 
                    y=krd["lat"], 
                    text=hkm, 
                    showarrow=False,
                    font=dict(family="Arial Black", size=14, color="white"), 
                    bgcolor="rgba(0,0,0,0.5)"
                )

        st.plotly_chart(fig, use_container_width=True)
        st.caption("ℹ️ Harita **BÖLGE** bazlı boyanır. Bir bölgede en çok şehri kim aldıysa, o bölgenin tamamı onun rengine bürünür.")
    
    else:
        st.warning("Harita verisi yükleniyor veya bağlantı hatası var...")
