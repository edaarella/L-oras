import numpy as np

# --- UZAY VE FİZİK SABİTLERİ ---
MU_DUNYA = 398600  # Dünya'nın standart kütleçekim parametresi (km^3/s^2)
YARICAP_DUNYA = 6371 # Dünya'nın yarıçapı (km)

# 1. Roketin Dünya etrafındaki bekleme yörüngesi (LEO)
irtifa_leo = 200 # km
r_leo = YARICAP_DUNYA + irtifa_leo

# 2. NASA JPL'den aldığımız anlık Ay uzaklığı 
# (Önceki NASA kodundan aldığın anlık mesafeyi buraya yazabilirsin, şimdilik ortalama bir değer girelim)
r_ay = 384400 # km 

# --- YÖRÜNGE HESAPLAMALARI ---
# Adım 1: LEO'daki aracın mevcut hızı (Dairesel yörünge hızı formülü)
v_leo = np.sqrt(MU_DUNYA / r_leo)

# Adım 2: Transfer Elipsinin Yarı Büyük Ekseni (a)
a_transfer = (r_leo + r_ay) / 2

# Adım 3: Vis-Viva Denklemi ile fırlatma anında (Perigee) gereken hız
v_tli = np.sqrt(MU_DUNYA * (2 / r_leo - 1 / a_transfer))

# Adım 4: GEREKEN NET YAKIT GÜCÜ (DELTA-V)
delta_v = v_tli - v_leo

print("-" * 50)
print("🚀 TRANS-LUNAR INJECTION (TLI) YAKIT/HIZ HESAPLAMASI 🚀")
print("-" * 50)
print(f"Bekleme Yörüngesi (LEO) Mevcut Hızı : {v_leo:.3f} km/s")
print(f"Ay'a Gidiş İçin Çıkılması Gereken Hız : {v_tli:.3f} km/s")
print("-" * 50)
print(f"🔥 MOTORDAN İSTENEN MINIMUM DELTA-V   : {delta_v:.3f} km/s")
print("-" * 50)
print("Not: Bu değer, saniyede hızımızı kaç km artırmamız gerektiğini gösterir.")