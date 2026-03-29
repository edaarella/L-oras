from astroquery.jplhorizons import Horizons
from datetime import datetime, timedelta
import numpy as np

# Zamanı ayarla (Bugünün tarihi ve yarının tarihi)
bugun = datetime.utcnow().strftime('%Y-%m-%d')
yarin = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')

print(f"NASA JPL Horizons Sunucularına bağlanılıyor... (Tarih: {bugun})")
print("Dünya merkezinden Ay'ın anlık vektörleri hesaplanıyor...\n")

try:
    # id='301' (Ay'ın evrensel kodu), location='500' (Dünya'nın merkezi)
    # NASA'dan bugünün vektörel (x,y,z) verilerini istiyoruz.
    ay_verisi = Horizons(id='301', location='500', epochs={'start': bugun, 'stop': yarin, 'step': '1d'})
    
    # Vektörleri al (Kilometre ve Saniye cinsinden)
    vektorler = ay_verisi.vectors(quantities='1') # 1: Pozisyon ve Hız vektörleri
    
    # Verileri tablodan çekip değişkenlere atayalım (Astronomik Birim - AU cinsinden gelir, Kilometreye çevireceğiz)
    # 1 AU (Astronomik Birim) = Yaklaşık 149,597,870.7 km
    au_to_km = 149597870.7
    
    x_km = vektorler['x'][0] * au_to_km
    y_km = vektorler['y'][0] * au_to_km
    z_km = vektorler['z'][0] * au_to_km
    
    # Uzaydaki gerçek uzaklığı hesaplama (Pisagor Teoreminin 3 Boyutlu hali)
    gercek_uzaklik_km = np.sqrt(x_km**2 + y_km**2 + z_km**2)
    
    print("-" * 50)
    print("🌕 NASA JPL HORIZONS ANLIK AY VERİSİ 🌕")
    print("-" * 50)
    print(f"X Ekseni Konumu : {x_km:,.2f} km")
    print(f"Y Ekseni Konumu : {y_km:,.2f} km")
    print(f"Z Ekseni Konumu : {z_km:,.2f} km")
    print("-" * 50)
    print(f"🚀 Dünya'nın Merkezinden Ay'a Şu Anki Gerçek Uzaklık: {gercek_uzaklik_km:,.2f} km")
    print("-" * 50)

except Exception as e:
    print(f"Bağlantı hatası oluştu: {e}")