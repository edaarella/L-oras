import numpy as np
import matplotlib.pyplot as plt

# --- UZAY SABİTLERİ (Kilometre cinsinden) ---
R_dunya = 6371
R_ay_yaricap = 1737
R_ay_yorunge = 384400  # Ay'ın Dünya'ya uzaklığı
R_bekleme_yorungesi = R_dunya + 200 # Roketin fırlatılıp Dünya etrafında döndüğü ilk yörünge (LEO)

# --- YÖRÜNGE MATEMATİĞİ (Hohmann Transferi) ---
# Transfer yörüngesi dev bir elipstir. Bu elipsin yarı büyük eksenini hesaplıyoruz:
a_transfer = (R_bekleme_yorungesi + R_ay_yorunge) / 2

# Elipsin basıklık oranı (Eccentricity)
e_transfer = 1 - (R_bekleme_yorungesi / a_transfer)

# Roketin uçuş açısı (0'dan Pi'ye, yani Dünya'dan Ay'a kadar yarım tur)
theta = np.linspace(0, np.pi, 200)

# Kutupsal koordinatlarda roketin Dünya'ya olan anlık uzaklığı (R) formülü:
r_transfer = (a_transfer * (1 - e_transfer**2)) / (1 + e_transfer * np.cos(theta))

# Kutupsal (R, Teta) koordinatları, grafikte çizmek için Kartezyen (X, Y) eksenine çeviriyoruz:
x_transfer = r_transfer * np.cos(theta)
y_transfer = r_transfer * np.sin(theta)

# --- GÖRSELLEŞTİRME VE SİMÜLASYON HARİTASI ---
fig, ax = plt.subplots(figsize=(10, 6))

# 1. Dünya'yı çiz
dunya = plt.Circle((0, 0), R_dunya, color='blue', label='Dünya')
ax.add_patch(dunya)

# 2. Ay'ın yörüngesini (Dairesel izi) çiz
ay_acisi = np.linspace(0, 2*np.pi, 200)
ax.plot(R_ay_yorunge * np.cos(ay_acisi), R_ay_yorunge * np.sin(ay_acisi), 'gray', linestyle='--', alpha=0.5, label='Ay Yörüngesi')

# 3. Ay'ın roket vardığı andaki konumunu çiz (Transfer rotasının bittiği yer)
ay = plt.Circle((-R_ay_yorunge, 0), R_ay_yaricap*10, color='gray', label='Ay (Hedef)') # Gözüksün diye yarıçapı 10'la çarptık
ax.add_patch(ay)

# 4. Roketin Uçuş Rotasını çiz
ax.plot(x_transfer, y_transfer, 'r-', linewidth=2, label='Roket Uçuş Rotası (Transfer)')

# Grafiği ayarla
ax.set_aspect('equal')
ax.set_title('Dünya\'dan Ay\'a Rota Planlaması (Astrodinamik Transfer)')
ax.set_xlabel('X Ekseni Uzaklık (km)')
ax.set_ylabel('Y Ekseni Uzaklık (km)')
ax.legend()
plt.grid(True)

plt.show()