import streamlit as st
import pandas as pd
import plotly.express as px

def etkilesim_sayfasi_olustur():
    st.markdown("### 🤝 BC Reel'de Birbirini Görenler (Ekim 2025)")
    st.caption("Veri Kaynağı: 10.10.2025 Tarihli İstihbarat Raporu")
    
    # 1. VERİ SETİ (PDF'ten alındı ve temizlendi)
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

    # 3. GRAFİK (Bar Chart)
    fig = px.bar(df.sort_values("Skor", ascending=True), 
                 x="Skor", y="Üye", 
                 orientation='h', 
                 title="📊 Kim Kaç Kişiyi Gördü?",
                 text="Skor",
                 color="Skor",
                 color_continuous_scale="Viridis")
    fig.update_layout(showlegend=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

    # 4. KİM KİMİ GÖRDÜ MATRİSİ (Heatmap)
    st.subheader("🕵️ Kim Kimi Gördü Matrisi")
    st.caption("Yeşil: Gördü | Siyah: Görmedi")
    
    # Tüm üyelerin listesi
    tum_uyeler = sorted([d["Üye"] for d in data])
    
    # Matris verisini hazırla
    matrix_data = []
    for row_person in data:
        row = []
        sahip = row_person["Üye"]
        gordukleri = row_person["Gördükleri"]
        
        for col_person in tum_uyeler:
            if sahip == col_person:
                row.append(None) # Kendisi (Gri)
            elif col_person in gordukleri:
                row.append(1) # Gördü (Yeşil)
            else:
                row.append(0) # Görmedi (Siyah)
        matrix_data.append(row)
        
    # Heatmap Çiz
    fig_matrix = px.imshow(matrix_data,
                           x=tum_uyeler,
                           y=[d["Üye"] for d in data],
                           color_continuous_scale=["#111", "#00FF00"], # Siyah -> Yeşil
                           aspect="auto")
    fig_matrix.update_traces(showscale=False)
    fig_matrix.update_layout(xaxis_nticks=len(tum_uyeler), height=600)
    st.plotly_chart(fig_matrix, use_container_width=True)
    

    # 5. DETAYLI TABLO
    with st.expander("📋 Detaylı Listeyi Gör"):
        st.dataframe(df, use_container_width=True)
