import streamlit as st
from collections import Counter

def profil_sayfasi(avcilar, plakalar, madalyalar, tanimlar, turkiye_verisi):
    # CSS Stil Tanımları
    st.markdown("""
<style>
    .id-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 2px solid #444;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
        color: white;
        font-family: sans-serif;
        margin-bottom: 20px;
    }
    .id-header {
        border-bottom: 2px solid #FF4B4B;
        padding-bottom: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .agent-name {
        font-size: 32px;
        font-weight: 900;
        color: #FFF;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .agent-rank {
        font-size: 18px;
        color: #FFD700;
        font-weight: bold;
        font-family: monospace;
    }
    .info-grid {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .info-left {
        flex: 1;
    }
    .info-right {
        flex: 1;
        text-align: right;
        font-size: 60px;
    }
    .stats-container {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 10px;
    }
    .stat-box {
        background-color: #333;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #FF4B4B;
    }
    .stat-label {
        font-size: 12px;
        color: #aaa;
        text-transform: uppercase;
    }
    .badge-container {
        margin-top: 20px;
    }
    .badge-title {
        color: #FFD700;
        font-weight: bold;
        margin-bottom: 10px;
        border-bottom: 1px solid #444;
    }
    .badge-grid {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .badge-item {
        background: #222;
        padding: 8px;
        border-radius: 50%;
        font-size: 24px;
        border: 1px solid #555;
        cursor: help;
    }
    .stamp {
        position: absolute;
        bottom: 20px;
        right: 20px;
        color: rgba(255, 255, 255, 0.05);
        font-size: 80px;
        font-weight: 900;
        transform: rotate(-30deg);
        pointer-events: none;
        z-index: 0;
    }
</style>
""", unsafe_allow_html=True)

    # 1. AJAN SEÇİMİ
    col_sel, col_info = st.columns([1, 3])
    with col_sel:
        secilen_avci = st.selectbox("📂 Personel Dosyası Seç:", avcilar)
        
    if not secilen_avci:
        st.info("Lütfen bir ajan seçin.")
        return

    # 2. İSTATİSTİK HESAPLAMA
    my_plates = []
    my_regions = []
    
    for plaka_kodu, veri in plakalar.items():
        if veri and veri.get('sahibi') == secilen_avci:
            my_plates.append(veri)
            sehir_bilgisi = turkiye_verisi.get(plaka_kodu)
            if sehir_bilgisi:
                my_regions.append(sehir_bilgisi['bolge'])

    toplam_av = len(my_plates)
    
    # Rütbe Mantığı
    if toplam_av == 0: rutbe = "Stajyer 🧹"
    elif toplam_av < 5: rutbe = "Çaylak Ajan 👶"
    elif toplam_av < 15: rutbe = "Saha Ajanı 🔫"
    elif toplam_av < 30: rutbe = "Özel Harekat 🚔"
    elif toplam_av < 50: rutbe = "İstihbarat Şefi 🕵️"
    elif toplam_av < 70: rutbe = "Emniyet Müdürü ⭐"
    else: rutbe = "TEŞKİLAT BAŞKANI 👑"

    # Favori Bölge
    fav_bolge = Counter(my_regions).most_common(1)[0][0] if my_regions else "Bilinmiyor"
    
    # Madalyalar
    sahip_olunanlar = madalyalar.get(secilen_avci, [])
    
    badges_html = ""
    if sahip_olunanlar:
        for m in sahip_olunanlar:
            detay = tanimlar.get(m, {"ikon": "🏅", "desc": "Bilinmeyen Nişan"})
            badges_html += f'<div class="badge-item" title="{detay["desc"]}">{detay["ikon"]}</div>'
    else:
        badges_html = "<span style='color:#666; font-size:12px;'>Henüz madalya yok.</span>"

    # 3. HTML KART OLUŞTURMA (DİKKAT: SOLA YAPIŞIK YAZIYORUZ)
    card_html = f"""
<div class="id-card">
    <div class="stamp">GİZLİ</div>
    <div class="id-header">
        <div class="agent-name">{secilen_avci}</div>
        <div class="agent-rank">{rutbe}</div>
    </div>
    <div class="info-grid">
        <div class="info-left">
            <div style="color: #aaa; font-size: 14px; margin-bottom: 5px;">👤 PERSONEL KİMLİĞİ</div>
            <div style="color: #fff; font-family: monospace; line-height: 1.5;">
                KOD ADI: <span style="color: #FF4B4B;">{secilen_avci.upper()}</span><br>
                GÖREV YERİ: {fav_bolge.upper()} BÖLGESİ<br>
                DURUMU: <span style="color: #00FF00;">AKTİF</span>
            </div>
        </div>
        <div class="info-right">
            🕵️‍♂️
        </div>
    </div>
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-value">{toplam_av}</div>
            <div class="stat-label">TOPLAM İNFAZ</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{len(set(my_regions))}</div>
            <div class="stat-label">FETHEDİLEN BÖLGE</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{len(sahip_olunanlar)}</div>
            <div class="stat-label">MADALYA</div>
        </div>
    </div>
    <div class="badge-container">
        <div class="badge-title">🏅 ONUR NİŞANLARI</div>
        <div class="badge-grid">
            {badges_html}
        </div>
    </div>
</div>
"""
    
    # HTML'i Render Et
    st.markdown(card_html, unsafe_allow_html=True)

    # 4. SON FAALİYETLER
    st.write("")
    st.subheader("📁 Son Operasyon Kayıtları")
    
    son_isler = sorted(my_plates, key=lambda x: x.get('tarih', ''), reverse=True)[:5]
    
    if son_isler:
        for is_ in son_isler:
            p_tam = is_.get("tam_plaka", "???")
            notu = is_.get("not", "-")
            trh = is_.get("tarih", "-")
            st.info(f"🗓️ **{trh}** | 🚘 **{p_tam}** | 📝 *{notu}*")
    else:
        st.caption("Henüz operasyon kaydı bulunamadı.")
