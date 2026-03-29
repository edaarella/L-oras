import requests
import os

# --- GÖREV KONTROL: İNİŞ BÖLGESİ KOORDİNATLARI ---
# Ay'daki hedefimiz: Mare Tranquillitatis (Sessizlik Denizi) çevresi
# Bounding Box (BBOX) formatı: Min Boylam, Min Enlem, Maks Boylam, Maks Enlem
hedef_bbox = "23.4,0.6,23.5,0.7" 

print(f"Hedef koordinatlar kilitlendi (BBOX): {hedef_bbox}")
print("NASA Gezegen Veri Sistemi (PDS) / USGS Sunucularına bağlanılıyor...\n")

# Gerçek bir uzay ajansı API mimarisi (Temsili USGS/NASA Astreogeology Endpoint formatı)
# Not: NASA API'leri sürekli güncellendiği için bu kodda kavramsal bir indirme linki kullanıyoruz.
api_url = "https://planetarymaps.usgs.gov/mosaic/Lunar_LRO_LOLA_Global_LDEM_118m_Mar2014.tif"

dosya_adi = "gercek_ay_inis_bolgesi.tif"

try:
    print(f"Uydu verisi (LRO LOLA DEM) indiriliyor... Lütfen bekleyin (Bu işlem internet hızınıza göre birkaç saniye sürebilir).")
    
    # Sunucuya GET isteği (Request) atıyoruz
    cevap = requests.get(api_url, stream=True)
    
    # Eğer sunucu "200 OK" (Başarılı) yanıtı verirse dosyayı kaydet
    if cevap.status_code == 200:
        with open(dosya_adi, 'wb') as dosya:
            for chunk in cevap.iter_content(chunk_size=8192):
                dosya.write(chunk)
                
        print("-" * 50)
        print(f"✅ VERİ BAŞARIYLA İNDİRİLDİ!")
        print(f"Kaydedilen Dosya: {os.path.abspath(dosya_adi)}")
        print("-" * 50)
        print("Artık bu gerçek veriyi A* otonom navigasyon algoritmamıza besleyebiliriz!")
    else:
        print(f"Sunucu hatası! Hata kodu: {cevap.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Bağlantı sırasında kritik bir hata oluştu: {e}")