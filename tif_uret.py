import numpy as np
import tifffile as tiff

print("TUA Simülasyon Verisi Üretiliyor...")

# 200x200 piksellik bir Ay yüzeyi matrisi oluşturuyoruz
boyut = 200
x, y = np.meshgrid(np.linspace(-5, 5, boyut), np.linspace(-5, 5, boyut))

# Zemine rastgele Ay tozu pürüzleri ekliyoruz
ay_yuzeyi = np.random.normal(0, 0.5, (boyut, boyut)) 

# 3 Adet ölümcül krater ekliyoruz (Derinlikleri eksi değer)
ay_yuzeyi -= 25 * np.exp(-((x - 0)**2 + (y - 0)**2) / 2.0)    
ay_yuzeyi -= 15 * np.exp(-((x - 2)**2 + (y - 3)**2) / 1.0)    
ay_yuzeyi -= 10 * np.exp(-((x + 3)**2 + (y + 2)**2) / 0.5)    

# Veriyi .tif olarak kaydediyoruz (Gerçek uzay ajansı formatı)
tiff.imwrite('tua_gercek_ay.tif', ay_yuzeyi.astype('float32'))

print("Başarılı! 'tua_gercek_ay.tif' dosyası oluşturuldu.")