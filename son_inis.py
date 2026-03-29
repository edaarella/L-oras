import numpy as np
import matplotlib.pyplot as plt
import heapq

print("Uçuş Bilgisayarı Başlatılıyor...")
print("Ana veri bağlantısı koptu! Lidar simülasyonu (B Planı) devreye alınıyor...")

# --- 1. GERÇEKÇİ AY YÜZEYİ HARİTASI OLUŞTURMA (LİDAR SİMÜLASYONU) ---
boyut = 100
x, y = np.meshgrid(np.linspace(-5, 5, boyut), np.linspace(-5, 5, boyut))
# Temel yüzey pürüzleri
ay_yuzeyi = np.random.normal(0, 0.3, (boyut, boyut)) 

# Yüzeye 3 farklı boyutta krater ekliyoruz (Derinlikleri eksi değer)
ay_yuzeyi -= 20 * np.exp(-((x - 0)**2 + (y - 0)**2) / 3.0)      # Merkezdeki Dev Krater
ay_yuzeyi -= 12 * np.exp(-((x - 3)**2 + (y - 2)**2) / 1.5)      # Sağdaki Orta Krater
ay_yuzeyi -= 8 * np.exp(-((x + 2.5)**2 + (y + 2.5)**2) / 0.8)   # Sol Alt Küçük Krater

# --- 2. TEHLİKE (HAZARD) ANALİZİ VE EĞİM HESABI ---
print("Yüzey taraması tamamlandı. Tehlikeli eğimler hesaplanıyor...")
gy, gx = np.gradient(ay_yuzeyi)
egim_matrisi = np.sqrt(gx**2 + gy**2)

maksimum_guvenli_egim = 1.2
# 1 olan yerler krater yamacı (tehlikeli), 0 olan yerler düzlük (güvenli)
engel_matrisi = np.where(egim_matrisi > maksimum_guvenli_egim, 1, 0)

# --- 3. A* OTONOM NAVİGASYON ALGORİTMASI ---
def astar_rotasi(engel_matrisi, baslangic, hedef):
    komsular = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
    kapatilanlar = set()
    gelis_yonu = {}
    g_skoru = {baslangic: 0}
    f_skoru = {baslangic: np.abs(baslangic[0] - hedef[0]) + np.abs(baslangic[1] - hedef[1])}
    
    acik_liste = []
    heapq.heappush(acik_liste, (f_skoru[baslangic], baslangic))

    while acik_liste:
        _, aktif = heapq.heappop(acik_liste)

        if aktif == hedef:
            yol = []
            while aktif in gelis_yonu:
                yol.append(aktif)
                aktif = gelis_yonu[aktif]
            yol.append(baslangic)
            return yol[::-1]

        kapatilanlar.add(aktif)

        for i, j in komsular:
            komsu = (aktif[0] + i, aktif[1] + j)
            if 0 <= komsu[0] < engel_matrisi.shape[0] and 0 <= komsu[1] < engel_matrisi.shape[1]:
                if engel_matrisi[komsu[0]][komsu[1]] == 1: 
                    continue # Tehlikeli bölge, buradan geçme
                if komsu in kapatilanlar:
                    continue
                
                maliyet = 1.414 if i != 0 and j != 0 else 1
                gecici_g = g_skoru[aktif] + maliyet

                if komsu not in g_skoru or gecici_g < g_skoru[komsu]:
                    gelis_yonu[komsu] = aktif
                    g_skoru[komsu] = gecici_g
                    f_skoru[komsu] = gecici_g + (np.abs(komsu[0] - hedef[0]) + np.abs(komsu[1] - hedef[1]))
                    heapq.heappush(acik_liste, (f_skoru[komsu], komsu))
    return []

# Aracın sol üstten (10, 10) başlayıp sağ alta (90, 90) inmesi gerekiyor
arac_konumu = (10, 10)
hedef_konum = (90, 90)

print("Hedefe ulaşmak için otonom kaçış manevrası (A*) hesaplanıyor...")
bulunan_yol = astar_rotasi(engel_matrisi, arac_konumu, hedef_konum)

# --- 4. GÖREV KONTROL GÖRSELLEŞTİRMESİ ---
fig, ax = plt.subplots(1, 2, figsize=(16, 7))

# Sol Panel: Yükseklik Haritası (Kuş Bakışı)
im1 = ax[0].imshow(ay_yuzeyi, cmap='copper')
ax[0].set_title('Araç Lidar Verisi: Yüzey Topografyası')
fig.colorbar(im1, ax=ax[0], label='Derinlik')

# Sağ Panel: Tehlike Haritası ve Otonom Rota
ax[1].imshow(engel_matrisi, cmap='Greys')
ax[1].set_title('Otonom İniş: Tehlike Haritası (Siyah) ve Hedef Rotası (Cyan)')

if bulunan_yol:
    y_kord, x_kord = zip(*bulunan_yol)
    ax[1].plot(x_kord, y_kord, color='cyan', linewidth=3, label='Otonom Rota')

ax[1].plot(arac_konumu[1], arac_konumu[0], 'bo', markersize=10, label='Başlangıç İrtifası')
ax[1].plot(hedef_konum[1], hedef_konum[0], 'go', markersize=10, label='Güvenli İniş Noktası')
ax[1].legend()

plt.tight_layout()
plt.show()
print("GÖREV BAŞARILI: Araç güvenli bölgeye iniş yaptı!")