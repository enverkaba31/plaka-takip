import streamlit as st
import pandas as pd

def liderlik_tablosu_olustur(avcilar, plakalar, madalyalar, tanimlar, plaka_sayisi):
    """
    Liderlik tablosunu ve madalya tooltip'lerini çizer.
    """
    
    # 1. Skorları Hesapla
    skorlar = {isim: 0 for isim in avcilar}
    for _, d in plakalar.items():
        if d and d["sahibi"] in skorlar:
            skorlar[d["sahibi"]] += 1
            
    # 2. Veri Yoksa Bilgi Ver
    if sum(skorlar.values()) == 0:
        st.info("Henüz veri girişi yapılmamış.")
        return

    # 3. DataFrame Oluştur ve Sırala
    df = pd.DataFrame(list(skorlar.items()), columns=["İsim", "Puan"])
    df = df.sort_values("Puan", ascending=False).reset_index(drop=True)
    
    # 4. CSS Stilleri (Tooltip ve Progress Bar İçin)
    st.markdown("""
    <style>
        .custom-table {width: 100%; border-collapse: collapse; font-family: sans-serif;}
        .custom-table th, .custom-table td {padding: 12px; text-align: left; border-bottom: 1px solid #444;}
        .custom-table tr:hover {background-color: #262730;}
        
        /* Tooltip (İpucu Balonu) Stili */
        .tooltip {position: relative; display: inline-block; cursor: help; font-size: 20px; margin-right: 8px;}
        
        /* Progress Bar Stili */
        .bar-bg {background-color: #31333F; width: 100%; border-radius: 4px; height: 8px; margin-top: 5px;}
        .bar-fill {background-color: #FF4B4B; height: 100%; border-radius: 4px;}
    </style>
    """, unsafe_allow_html=True)
    
    st.write("##### 📊 Puan Durumu")

    # 5. HTML Tabloyu Oluştur
    rows_html = ""
    for index, row in df.iterrows():
        isim = row['İsim']
        puan = row['Puan']
        yuzde = (puan / plaka_sayisi) * 100
        
        # Madalyaları Hazırla
        rozetler_html = ""
        kisi_madalyalar = madalyalar.get(isim, [])
        for m in kisi_madalyalar:
            if m in tanimlar:
                ikon = tanimlar[m]['ikon']
                desc = tanimlar[m]['desc']
                # Tooltip HTML'i (Mouse üzerine gelince açıklama çıkar)
                rozetler_html += f'<span class="tooltip" title="{m}: {desc}">{ikon}</span>'
        
        # Satır HTML'i
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
    
    # Tabloyu Birleştir
    full_table = f"""
    <table class="custom-table">
        <thead><tr style="color: #999;"><th>İsim</th><th>Skor</th><th>Rozetler (Üzerine Gel)</th></tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    """
    
    # Ekrana Bas
    st.markdown(full_table, unsafe_allow_html=True)
