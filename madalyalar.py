import streamlit as st

def madalya_sayfasi_olustur(tanimlar, madalya_sahipleri):
    """
    Madalya kataloğunu listeler.
    
    Argümanlar:
    - tanimlar: madalya_tanimlari.json dosyasından gelen veri.
    - madalya_sahipleri: madalyalar.json dosyasından gelen veri (Kimde ne var).
    """
    
    st.markdown("### 🎖️ Madalya ve Unvan Kataloğu")
    st.caption("Bu rozetler, özel başarı gösteren avcılara Yönetici tarafından verilir.")
    st.divider()

    # Eğer tanımlar dosyası boşsa veya okunamazsa
    if not tanimlar:
        st.warning("Madalya tanımları bulunamadı. (madalya_tanimlari.json boş veya okunamadı)")
        return

    # Grid yapısı (2 sütunlu)
    cols = st.columns(2)
    madalya_isimleri = list(tanimlar.keys())

    for i, madalya_adi in enumerate(madalya_isimleri):
        # 1. Tanımı al (madalya_tanimlari.json'dan)
        detay = tanimlar[madalya_adi]
        ikon = detay.get("ikon", "🏅")
        aciklama = detay.get("desc", "Açıklama yok.")
        
        # 2. Sahipleri bul (madalyalar.json'dan)
        # Veri yapısı: {"Enver": ["Metropol Faresi", "Flash"], "Ali": ["Flash"]}
        # Biz bunu tersine çevirip "Flash kimde var?" diye bakıyoruz.
        alanlar = [kisi for kisi, rozetler in madalya_sahipleri.items() if madalya_adi in rozetler]
        
        alanlar_text = "**Sahipleri:** "
        if alanlar:
            alanlar_text += ", ".join(alanlar)
        else:
            alanlar_text += "_Henüz kimse kazanmadı._"

        # 3. Kartı çiz
        with cols[i % 2]:
            st.info(f"### {ikon} {madalya_adi}\n\n{aciklama}\n\n---\n{alanlar_text}")
