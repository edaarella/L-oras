import numpy as np
import matplotlib.pyplot as plt

# 500x500 piksellik bir alan yaratıyoruz
X, Y = np.meshgrid(np.linspace(-3, 3, 500), np.linspace(-3, 3, 500))

# 1. ORTADAKİ DEV KRATER
yukseklik_verisi = -50 * np.exp(-(X**2 + Y**2)) 

# 2. YÜZEY DALGALANMALARI (Dağlar ve tepeler)
yukseklik_verisi += 15 * np.sin(X*3) * np.cos(Y*3)

# 3. SENSÖR GÜRÜLTÜSÜ (Bunu 3'ten 0.2'ye düşürdük ki algoritmamız büyük resmi görebilsin)
yukseklik_verisi += np.random.normal(0, 0.2, (500, 500))

print("Navigasyon algoritmaları çalıştırılıyor...")

# Eğim (Gradyan) hesaplama
gy, gx = np.gradient(yukseklik_verisi)
egim_matrisi = np.sqrt(gx**2 + gy**2)

# Otonom iniş için güvenli eşik değeri (Bunu da biraz kıstık)
maksimum_guvenli_egim = 1.0 
guvenli_alanlar_maskesi = egim_matrisi < maksimum_guvenli_egim

# --- GÖRSELLEŞTİRME ---
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

ax[0].imshow(yukseklik_verisi, cmap='terrain')
ax[0].set_title('Ay Yüzeyi Yükseklik Haritası (DEM)')

ax[1].imshow(guvenli_alanlar_maskesi, cmap='Greens')
ax[1].set_title(f'Otonom İniş: Güvenli Bölgeler (Yeşil)')

plt.show()