import pandas as pd
import json
import os
import shutil

from icerik_kontrol import *
import sys
# Mevcut dosyanın bulunduğu dizini al
current_directory = os.path.dirname(os.path.abspath(__file__))
# Göreceli yol (örneğin, bu dizinden 'readme_guncelleme_arayuzu_python' klasörüne giden yol)
relative_path = os.path.join("..", "readme_guncelleme_arayuzu_python")
# Göreceli yolu tam yola çevir
absolute_path = os.path.join(current_directory, relative_path)
# Tam yolu sys.path listesine ekle
sys.path.append(absolute_path)
from degiskenler import *
from konfigurasyon_json_kontrol import konfigurasyon_ilklendirme_islemleri
ANAHTAR_VE_LINKLER = konfigurasyon_ilklendirme_islemleri(KONFIGURASYON_JSON_PATH)
HOCA_OYLAMA_LINKI_CSV = ANAHTAR_VE_LINKLER.get(HOCA_OYLAMA_CSV_ANAHTARI, HOCA_OYLAMA_LINKI_CSV)
HOCA_YORULMALA_LINKI_CSV = ANAHTAR_VE_LINKLER.get(HOCA_YORUMLAMA_CSV_ANAHTARI, HOCA_YORULMALA_LINKI_CSV)
# Google Sheets dosyasının URL'si
yildizlar_sheets_url = HOCA_OYLAMA_LINKI_CSV
def guncelle_ogrenci_gorusleri(data, sheets_url):
    # Google Sheets verisini indir
    df = pd.read_csv(sheets_url)
    df = df.dropna()  # NaN içeren tüm satırları kaldır
    
    # Her hoca için yorumları güncelle
    for index, row in df.iterrows():
        hoca_adi = row[HOCA_SEC]
        kisi = row[ISMIN_NASIL_GOZUKSUN_HOCA]
        yorum = row[HOCA_HAKKINDAKI_YORUMUN]
        # icerikKontrol = IcerikKontrol("hoca")
        if not pd.isna(yorum):# and icerikKontrol.pozitif_mi(yorum):
            # yorum = icerikKontrol.metin_on_isleme(yorum)
            for hoca in data[HOCALAR]:
                if hoca[AD] == hoca_adi:
                    # Eğer bu kisi için daha önce bir yorum yapılmışsa, güncelle
                    gorus_var_mi = False
                    if OGRENCI_GORUSLERI not in hoca:
                        hoca[OGRENCI_GORUSLERI] = []
                    for gorus in hoca[OGRENCI_GORUSLERI]:
                        if gorus[KISI].lower() == kisi.lower():
                            gorus[YORUM] = yorum
                            gorus_var_mi = True
                            break
                    
                    # Yeni yorum ekle
                    if not gorus_var_mi:
                        hoca[OGRENCI_GORUSLERI].append({KISI: kisi.lower().title(), YORUM: yorum})
    # icerikKontrol.dosya_yaz()
# Google Sheets URL'si
yorumlar_sheets_url = HOCA_YORULMALA_LINKI_CSV

# Veriyi indir ve DataFrame olarak oku
yildizlar_df = pd.read_csv(yildizlar_sheets_url)


# Sadece sayısal sütunları al ve ortalama hesapla
yildizlar_numeric_columns = yildizlar_df.columns.drop([ZAMAN_DAMGASI, HOCA_SEC])  # Sayısal olmayan sütunları çıkar
yildizlar_grouped = yildizlar_df.groupby(HOCA_SEC)[yildizlar_numeric_columns].mean()

# Hocaların aldığı oyların (yani kaç defa seçildiğinin) frekansını hesapla
hoca_oy_sayisi = yildizlar_df[HOCA_SEC].value_counts()

# En yüksek oy sayısına sahip hocayı bul
en_populer_hoca = hoca_oy_sayisi.idxmax()
en_populer_hoca_oy_sayisi = hoca_oy_sayisi.max()

# JSON dosyasını oku
json_file_path = HOCALAR_JSON_NAME  # JSON dosyasının yolu
with open(os.path.join("..",json_file_path), 'r', encoding='utf-8') as file:
    data = json.load(file)
data[EN_POPULER_HOCA] = {HOCA_ADI:en_populer_hoca, OY_SAYISI:int(en_populer_hoca_oy_sayisi)}
for hoca in data[HOCALAR]:
    name = hoca.get(AD)
    if name in yildizlar_grouped.index:
        hoca[ANLATIM_PUANI] = int(yildizlar_grouped.loc[name, DERSI_NE_KADAR_GÜZEL_ANLATIR] * 10)
        hoca[KOLAYLIK_PUANI] = int(yildizlar_grouped.loc[name, DERSINI_GECMEK_NE_KADAR_KOLAYDIR] * 10) 
        hoca[OGRETME_PUNAI] = int(yildizlar_grouped.loc[name, DERSI_NE_KADAR_IYI__OGRETIR] * 10)
        hoca[EGLENCE_PUANI] = int(yildizlar_grouped.loc[name, DERSI_NE_KADAR_EGLENCELI_ANLATIR] * 10)
        hoca[OY_SAYISI] = int(hoca_oy_sayisi[name])

# Fonksiyonu çağır ve JSON dosyasını güncelle
guncelle_ogrenci_gorusleri(data, yorumlar_sheets_url)


with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# Dosyayı kopyalamak için:
shutil.copy(json_file_path, os.path.join("..",json_file_path))