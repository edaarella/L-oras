import numpy as np
import matplotlib.pyplot as plt
import heapq

# --- 1. A* (A-STAR) YAPAY ZEKA YOL BULMA ALGORİTMASI ---
def astar_rotasi(engel_matrisi, baslangic, hedef):
    # İleri, geri, sağ, sol ve çapraz hareketler
    komsular = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
    kapatilanlar = set()
    gelis_yonu = {}
    g_skoru = {baslangic: 0}
    # Heuristic (Kuş uçuşu tahmin)
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
            return yol[::-1] # Yolu baştan sona sırala

        kapatilanlar.add(aktif)

        for i, j in komsular:
            komsu = (aktif[0] + i, aktif[1] + j)
            
            # Harita sınırları dışına çıkmamak için
            if 0 <= komsu[0] < engel_matrisi.shape[0] and 0 <= komsu[1] < engel_matrisi.shape[1]:
                if engel_matrisi[komsu[0]][komsu[1]] == 1: # 1 demek krater/engel demek, oradan geçme
                    continue
                if komsu in kapatilanlar:
                    continue
                
                # Çapraz gitmek biraz daha maliyetlidir (Pisagor teoreminden ~1.41)
                maliyet = 1.414 if i != 0 and j != 0 else 1
                gecici_g = g_skoru[aktif] + maliyet

                if komsu not in g_skoru or gecici_g < g_skoru[komsu]:
                    gelis_yonu[komsu] = aktif
                    g_skoru[komsu] = gecici_g
                    h_skoru = np.abs(komsu[0] - hedef[0]) + np.abs(komsu[1] - hedef[1])
                    f_skoru[komsu] = gecici_g + h_skoru
                    heapq.heappush(acik_liste, (f_skoru[komsu], komsu))
    return [] # Yol bulunamazsa boş dön

# --- 2. AY HARİTASI VE SİMÜLASYON ORTAMI KURULUMU ---
harita_boyutu = 50
ay_yuzeyi = np.zeros((harita_boyutu, harita_boyutu))

# Ortaya dev bir krater (tehlikeli bölge) ekleyelim. 1 = Engel/Ölümcül bölge
ay_yuzeyi[15:35, 15:35] = 1 
ay_yuzeyi[20:30, 35:40] = 1 # Kraterin sağa doğru uzantısı

# Aracın konumu ve inmek istediği hedef
arac_konumu = (5, 5)   # Sol üst köşe
hedef_konum = (45, 45) # Sağ alt köşedeki güvenli düzlük

print("Yapay Zeka (A*) hedef için en güvenli rotayı hesaplıyor...")
bulunan_yol = astar_rotasi(ay_yuzeyi, arac_konumu, hedef_konum)

# --- 3. GÖRSELLEŞTİRME ---
fig, ax = plt.subplots(figsize=(8, 8))

# Haritayı çiz (0'lar güvenli, 1'ler tehlikeli)
ax.imshow(ay_yuzeyi, cmap='Greys')

# Kraterin etrafından dolanan rotayı çiz
if bulunan_yol:
    y_kord, x_kord = zip(*bulunan_yol)
    ax.plot(x_kord, y_kord, color='cyan', linewidth=3, label='Otonom Kaçış Rotası (A*)')

# Başlangıç ve Hedef noktalarını işaretle
ax.plot(arac_konumu[1], arac_konumu[0], 'bo', markersize=10, label='Aracın Konumu (Başlangıç)')
ax.plot(hedef_konum[1], hedef_konum[0], 'go', markersize=10, label='Güvenli İniş Alanı (Hedef)')

ax.set_title('Ay İniş Modülü: Gerçek Zamanlı Kraterden Kaçış Navigasyonu')
ax.legend()
plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
plt.show()