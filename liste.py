import streamlit as st
import pandas as pd

def liste_sayfasi_olustur(plakalar, turkiye_verisi):
    """
    Bulunan tüm plakaları, bulan kişiyi ve varsa hikayesini listeler.
    """
    
    st.markdown("### 📋 Kayıt Defteri")
    
    lst = []
    
    # Tüm plakaları tek tek kontrol et
    for p_kodu, detay in plakalar.items():
        if detay: # Eğer bu plaka bulunmuşsa (None değilse)
            
            # Not/Hikaye var mı? (Eski verilerde key olmayabilir, get ile alıyoruz)
            hikaye = detay.get("not", "")
            
            lst.append({
                "Kod": p_kodu,
                "Şehir": turkiye_verisi.get(p_kodu, {}).get("il", "?"),
                "Tam Plaka": detay["tam_plaka"],
                "Bulan": detay["sahibi"],
                "Tarih": detay.get("tarih", "-"),
                "Hikaye": hikaye
            })

    if lst:
        df = pd.DataFrame(lst)
        
        # Tabloyu ekrana bas
        st.dataframe(
            df, 
            hide_index=True, 
            use_container_width=True,
            column_config={
                "Kod": st.column_config.TextColumn("Kod", width="small"),
                "Şehir": st.column_config.TextColumn("Şehir", width="medium"),
                "Tam Plaka": st.column_config.TextColumn("Plaka", width="medium"),
                "Bulan": st.column_config.TextColumn("Avcı", width="medium"),
                "Tarih": st.column_config.TextColumn("Tarih", width="small"),
                "Hikaye": st.column_config.TextColumn("Notlar", width="large")
            }
        )
        
        # İstatistik
        bulunan_sayisi = len(lst)
        toplam_sayi = len(plakalar)
        st.caption(f"Toplam {toplam_sayi} şehirden {bulunan_sayisi} tanesi bulundu.")
        
    else:
        st.info("Henüz kayıt defteri boş. Sahaya inme vakti! 🚙")
