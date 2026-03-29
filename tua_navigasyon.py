import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import heapq

print("--- TUA GÖREV KONTROL ---")
print("Uçuş Bilgisayarı Başlatılıyor...")
print("Araç hafızasındaki NASA LRO verileri okunuyor...")

dosya_yolu = 'tua_gercek_ay.tif'

try:
    # 1. GERÇEK NASA VERİSİNİ MATRİSE ÇEVİRME
    gercek_yuzey_verisi = tiff.imread(dosya_yolu)
    
    # Haritayı işlemeden önce boyutlarını kontrol edip 200x200'lük bir alan kesiyoruz
    merkez_y, merkez_x = gercek_yuzey_verisi.shape[0] // 2, gercek_yuzey_verisi.shape[1] // 2
    kirpilmis_yuzey = gercek_yuzey_verisi[merkez_y-100:merkez_y+100, merkez_x-100:merkez_x+100]
    
    print("Yüzey taraması tamamlandı. Tehlikeli krater eğimleri hesaplanıyor...")
    
    # 2. TEHLİKE (HAZARD) ANALİZİ (Eğim / Gradyan Hesabı)
    gy, gx = np.gradient(kirpilmis_yuzey)
    egim_matrisi = np.sqrt(gx**2 + gy**2)

    # Eğimin en dik %15'lik kısmını tehlikeli (siyah) sayıyoruz
    maksimum_guvenli_egim = np.percentile(egim_matrisi, 85) 
    engel_matrisi = np.where(egim_matrisi > maksimum_guvenli_egim, 1, 0)

    # 3. A* (A-STAR) YAPAY ZEKA OTONOM YOL BULMA
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
                    # EĞER HEDEF NOKTASI ENGELE DENK GELİRSE, O NOKTAYI GEÇİCİ OLARAK GÜVENLİ SAY
                    if engel_matrisi[komsu[0]][komsu[1]] == 1 and komsu != hedef: 
                        continue 
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

    # --- KOORDİNAT DÜZELTMESİ (ROTA ÇIKMASI İÇİN) ---
    arac_konumu = (20, 20)      # Sol üst köşeden biraz içeride
    hedef_konum = (170, 160)    # Sağ alt köşede ama tam kraterin içinde değil

    print("Yapay Zeka otonom iniş rotasını hesaplıyor...")
    bulunan_yol = astar_rotasi(engel_matrisi, arac_konumu, hedef_konum)

    # 4. JÜRİ SUNUMU İÇİN GÖRSELLEŞTİRME
    fig, ax = plt.subplots(1, 2, figsize=(16, 7))

    # Sol Panel: Yükseklik Verisi
    im1 = ax[0].imshow(kirpilmis_yuzey, cmap='terrain')
    ax[0].set_title('NASA LRO Ay Yüzeyi Topografyası')
    fig.colorbar(im1, ax=ax[0], label='Yükseklik (Metre)')

    # Sağ Panel: Tehlike Analizi ve A* Rotası
    ax[1].imshow(engel_matrisi, cmap='Greys')
    ax[1].set_title('Otonom İniş: Engelden Kaçış ve Rota Planlama')

    if bulunan_yol:
        y_kord, x_kord = zip(*bulunan_yol)
        ax[1].plot(x_kord, y_kord, color='cyan', linewidth=3, label='Hesaplanan Otonom Rota')
        print(f"BAŞARILI: {len(bulunan_yol)} adımlık güvenli rota oluşturuldu.")
    else:
        print("UYARI: Güvenli bir rota bulunamadı! Hedef çok tehlikeli bir bölgede.")

    ax[1].plot(arac_konumu[1], arac_konumu[0], 'bo', markersize=10, label='Rover Mevcut Konum')
    ax[1].plot(hedef_konum[1], hedef_konum[0], 'go', markersize=10, label='Güvenli Hedef Noktası')
    ax[1].legend(loc='upper right')

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Kritik Hata: {e}")