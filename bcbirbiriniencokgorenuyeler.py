import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def etkilesim_sayfasi_olustur():
    st.markdown("### 🤝 BC Reel'de Birbirini Görenler (Ekim 2025)")
    st.caption("Veri Kaynağı: 10.10.2025 Tarihli İstihbarat Raporu")
    
    # 1. VERİ SETİ
    data = [
        {"Üye": "Yaız Abi", "Skor": 9, "Gördükleri": ["Gökan Abi", "Eren Dizdar", "Kaan", "Enes", "MertEr", "Mert Amlı", "Enver", "Yiit", "Sado"]},
        {"Üye": "Gökan Abi", "Skor": 9, "Gördükleri": ["Eren Dizdar", "Kaan", "Enes", "Yaız Abi", "Sado", "Yiit", "Enver", "Baybora", "MMusa"]},
        {"Üye": "Enes", "Skor": 8, "Gördükleri": ["Gökan Abi", "Eren Dizdar", "Kaan", "Yaız Abi", "MertEr", "Mert Amlı", "Enver", "Sado"]},
        {"Üye": "Enver", "Skor": 8, "Gördükleri": ["Gökan Abi", "Yiit", "Kaan", "Eren Dizdar", "Enes", "Yaız Abi", "Baybora", "Mert Amlı"]},
        {"Üye": "Kaan", "Skor": 8, "Gördükleri": ["Gökan Abi", "Eren Dizdar", "Enes", "Yaız Abi", "Sado", "Yiit", "Enver", "Baybora"]},
        {"Üye": "Yiit", "Skor": 8, "Gördükleri": ["Gökan Abi", "Kaan", "Enver", "Eren Dizdar", "Baybora", "Yaız Abi", "Murat Akma", "Orospu Caner"]},
        {"Üye": "Eren Dizdar", "Skor": 7, "Gördükleri": ["Gökan Abi", "Enes", "Yaız Abi", "Kaan", "Sado", "Yiit", "Enver"]},
        {"Üye": "Sado", "Skor": 5, "Gördükleri": ["Gökan Abi", "Enes", "Kaan", "Eren Dizdar", "Yaız Abi"]},
        {"Üye": "Baybora", "Skor": 4, "Gördükleri": ["Yiit", "Gökan Abi", "Kaan", "Enver"]}, 
        {"Üye": "Mert Amlı", "Skor": 4, "Gördükleri": ["Enes", "Yaız Abi", "MertEr", "Enver"]},
        {"Üye": "MertEr", "Skor": 3, "Gördükleri": ["Mert Amlı", "Enes", "Yaız Abi"]},
        {"Üye": "Murat Akma", "Skor": 1, "Gördükleri": ["Yiit"]},
        {"Üye": "Orospu Caner", "Skor": 1, "Gördükleri": ["Yiit"]},
        {"Üye": "MMusa", "Skor": 1, "Gördükleri": ["Gökan Abi"]},
        {"Üye": "Cenker Glassmaker", "Skor": 0, "Gördükleri": []},
        {"Üye": "Hakkı :D", "Skor": 0, "Gördükleri": []},
        {"Üye": "Görkem Deveci", "Skor": 0, "Gördükleri": []},
        {"Üye": "Ali Eren Kurt", "Skor": 0, "Gördükleri": []}
    ]
    
    df = pd.DataFrame(data)

    # 2. METRİKLER
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Buluşma", "66+") 
    c2.metric("Liderler", "Yaız & Gökan", "9 Kişi")
    c3.metric("Ayın En Sosyali", "Yaız Abi")

    st.divider()

    # 3. GRAFİK (Bar Chart - Daha Renkli)
    fig = px.bar(df.sort_values("Skor", ascending=True), 
                 x="Skor", y="Üye", 
                 orientation='h', 
                 title="📊 Skor Tablosu",
                 text="Skor",
                 color="Skor",
                 color_continuous_scale="Reds")
    fig.update_layout(showlegend=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 4. KİM KİMİ GÖRDÜ MATRİSİ (REVİZE EDİLDİ)
    st.subheader("🕵️ Kim Kimi Gördü Matrisi")
    
    # Tüm üyelerin listesi
    tum_uyeler = sorted([d["Üye"] for d in data])
    
    # Matris verisini sayısal olarak hazırla
    # 0: Görmedi (Koyu Gri)
    # 1: Gördü (Yeşil)
    # 0.2: Kendisi (Boşluk/Siyah)
    
    z_values = []
    text_values = [] # Üzerine gelince yazacak yazı
    
    for row_person in data:
        z_row = []
        text_row = []
        sahip = row_person["Üye"]
        gordukleri = row_person["Gördükleri"]
        
        for col_person in tum_uyeler:
            if sahip == col_person:
                z_row.append(0.2) # Kendisi
                text_row.append("Kendisi")
            elif col_person in gordukleri:
                z_row.append(1) # Gördü
                text_row.append(f"{sahip} -> {col_person} GÖRDÜ")
            else:
                z_row.append(0) # Görmedi
                text_row.append("Görmedi")
        
        z_values.append(z_row)
        text_values.append(text_row)
        
    # Heatmap Çiz (Custom Colors)
    # Renk Skalası: 0 -> Koyu Gri, 0.2 -> Siyah, 1 -> Yeşil
    colorscale = [
        [0.0, 'rgb(40, 40, 40)'],   # Görmedi (Koyu Gri)
        [0.2, 'rgb(0, 0, 0)'],      # Kendisi (Siyah)
        [1.0, 'rgb(0, 255, 100)']   # Gördü (Parlak Yeşil)
    ]

    fig_matrix = go.Figure(data=go.Heatmap(
        z=z_values,
        x=tum_uyeler,
        y=[d["Üye"] for d in data],
        text=text_values,
        hoverinfo="text",
        colorscale=colorscale,
        showscale=False, # Yandaki renk çubuğunu gizle
        xgap=1, # Kutucuklar arası boşluk (X ekseni)
        ygap=1  # Kutucuklar arası boşluk (Y ekseni)
    ))

    fig_matrix.update_layout(
        title="Etkileşim Grid'i",
        xaxis_nticks=len(tum_uyeler), # Tüm isimleri göster
        yaxis_nticks=len(data),       # Tüm isimleri göster
        width=800,
        height=800,
        xaxis_side="top", # İsimleri yukarı al (daha rahat okunur)
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickangle=-45) # İsimleri biraz eğik yaz sığsın
    )
    
    st.plotly_chart(fig_matrix, use_container_width=True)

    # 5. DETAYLI TABLO (Genişletilebilir)
    with st.expander("📋 Detaylı Listeyi Gör"):
        # Tabloyu daha şık hale getirelim
        formatted_df = df.copy()
        formatted_df["Gördükleri"] = formatted_df["Gördükleri"].apply(lambda x: ", ".join(x) if x else "-")
        st.dataframe(formatted_df, use_container_width=True)
