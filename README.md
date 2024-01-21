
# Üniversite Ders Notları Readme Oluşturucu
Bu reponun amacı temel olarak herhangi bir üniversitenin herhangi bir bölümündeki öğrencilerin oluşturduğu ders notları reposuna readme oluşturma işini kolaylaştırmaktır.

## Gereksinimleri İndirme 📦

Projeyi başarıyla çalıştırabilmek için aşağıdaki adımları izleyerek gerekli kütüphaneleri ve bağımlılıkları yükleyiniz:

1. **Python 3 Kurulumu:** Projeyi çalıştırmak için Python 3'ün bilgisayarınızda yüklü olması gerekmektedir. Python'ı [buradan](https://www.python.org/downloads/) indirebilirsiniz (linux için `sudo apt install python3`). Kurulum tamamlandıktan sonra terminali açın ve `python3 --version` komutu ile kurulumun başarılı olduğunu doğrulayın. 🐍

2. **Pip3 Kurulumu:** Pip, Python paketlerini yönetmek için kullanılan bir araçtır. Python 3 ile birlikte genellikle otomatik olarak yüklenir. Kurulumunu doğrulamak için terminali açın ve `pip3 --version` komutunu çalıştırın. Eğer kurulu değilse, [Pip'in resmi belgelerini](https://pip.pypa.io/en/stable/installing/) takip ederek kurulum yapabilirsiniz.(linux için `sudo apt install python3-pip`) 🛠️

3. **Gerekli Kütüphanelerin Yüklenmesi:** Projede kullanılan kütüphaneleri yüklemek için, terminalinize `pip3 install -r gereksinimler.txt` komutunu girin. Bu komut, `gereksinimler.txt` dosyasında listelenen tüm paketleri yükleyecektir. 📚
## Nasıl Kullanılır

Proje dosyaları arasında, hocalar, dersler, dönemler ve diğer bilgileri içeren JSON formatında çeşitli dosyalar bulunmaktadır. Bu dosyalar, projenin çeşitli yerlerinde kullanılarak dinamik bir içerik oluşturur.

Örneğin:
- `hocalar.json` hoca bilgilerini içerir ve README'leri oluşturmakta kullanılır.
- `dersler.json` ders bilgilerini tutar.
- `donemler.json` dönem bilgilerini tutar.
- `giris.json` README dosyasının giriş bilgilerini içerir.

Bu dosyalarla birlikte, her dersin ve her dönemin klasöründe README dosyaları oluşturulur.


### Arayüzü Çalıştırmak

Bu bölümde, projenin arayüzünün nasıl çalıştırılacağı adım adım açıklanmaktadır.

1. **json_depo_bilgileri.txt Dosyasının Hazırlanması:**
   Projede, `json_depo_bilgileri.txt` dosyasının kök dizinde olması gerekmektedir. Bu dosya yoksa, arayüz tarafından otomatik olarak oluşturulur. Dosya, JSON dosyalarının hangi klasörde tutulacağını belirtir. Örneğin:
   ```
   ..
   YTU_Bilgisayar_Muhendisligi_Arsiv
   json_dosyalari
   ```
   Bu yapıya göre, JSON dosyaları `YTU_Bilgisayar_Muhendisligi_Arsiv/json_dosyalari` klasöründe oluşur.

2. **Konfigürasyon Dosyasının Oluşturulması:**
   `json_depo_bilgileri.txt` dosyasında belirtilen yolda `konfigurasyon.json` dosyası oluşturulmalıdır. Bu dosya yoksa, arayüz tarafından otomatik olarak oluşturulur. Dosyanın içeriği aşağıdaki gibi olmalıdır:
   ```json
   {
       "github_url": "https://github.com/baselkelziye/YTU_Bilgisayar_Muhendisligi_Arsiv",
       "hoca_yorumlama": "https://forms.gle/WbwDxHUz6ebJA7t36",
       "hoca_oylama": "https://forms.gle/s6ZMrQG4q578pEzm7",
       "ders_yorumlama": "https://forms.gle/SzNmK1w4rVaKE4ee8",
       "ders_oylama": "https://forms.gle/3njZjmhm215YCAxe6",
       "ders_oylama_csv": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDFicOFbJu9Fnc4Hl0mFuuaC0L4PiEmUFkkJrgocwWGWs1wB3TyN1zd4okW8svC6IT2HMIe64NQUUy/pub?output=csv",
       "ders_yorumlama_csv": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQvGyGLQxobIpaVdQItSpqEoiwJ0DIIHE9kVvCHhfKQ7yYR16c2tI_ix4Z9d2tA4aLt2c4fTLGxlL-s/pub?output=csv",
       "hoca_oylama_csv": "https://docs.google.com/spreadsheets/d/1w386auUiJaGwoUAmmkEgDtIRSeUplmDz0AZkM09xPTk/export?format=csv",
       "hoca_yorumlama_csv": "https://docs.google.com/spreadsheets/d/1mexaMdOeB-hWLVP4MI_xmnKwGBuwoRDk6gY9zXDycyI/export?format=csv",
       "dokumanlar_repo_yolu": "..",
       "cikmislar": "https://drive.google.com/drive/folders/1LI_Bo7kWqI2krHTw0noUFl9crfZSlrZh"
   }
   ```
- `github_url`: Bu anahtarın karşısına ders dökümanlarının tutulduğu GitHub reposunun adresini ekleyin.
- `hoca_yorumlama`: Bu anahtara, hoca yorumlamak için oluşturulan Google Form anketinin linkini ekleyin. Eğer anket henüz oluşturulmadıysa, soru tipleri ve sıralaması [bu örnektekiyle](https://forms.gle/WbwDxHUz6ebJA7t36) birebir aynı olmalıdır.
- `hoca_oylama`: Bu anahtara, hoca oylamak için oluşturulan Google Form anketinin linkini ekleyin. Eğer anket henüz oluşturulmadıysa, soru tipleri ve sıralaması [bu örnektekiyle](https://forms.gle/s6ZMrQG4q578pEzm7) birebir aynı olmalıdır.
- `ders_yorumlama`: Bu anahtara, ders yorumlamak için oluşturulan Google Form anketinin linkini ekleyin. Eğer anket henüz oluşturulmadıysa, soru tipleri ve sıralaması [bu örnektekiyle](https://forms.gle/SzNmK1w4rVaKE4ee8) birebir aynı olmalıdır.
- `ders_oylama`: Bu anahtara, ders oylamak için oluşturulan Google Form anketinin linkini ekleyin. Eğer anket henüz oluşturulmadıysa, soru tipleri ve sıralaması [bu örnektekiyle](https://forms.gle/3njZjmhm215YCAxe6) birebir aynı olmalıdır.
- `ders_oylama_csv`: Bu anahtara, ders oylamak için oluşturulan Google Form anketinin içeriğinin kaydedildiği dosyanın CSV formatındaki linkini ekleyin.
- `ders_yorumlama_csv`: Bu anahtara, ders yorumlamak için oluşturulan Google Form anketinin içeriğinin kaydedildiği dosyanın CSV formatındaki linkini ekleyin.
- `hoca_oylama_csv`: Bu anahtara, hoca oylamak için oluşturulan Google Form anketinin içeriğinin kaydedildiği dosyanın CSV formatındaki linkini ekleyin.
- `ders_yorumlama_csv`: Bu anahtara, hoca yorumlamak için oluşturulan Google Form anketinin içeriğinin kaydedildiği dosyanın CSV formatındaki linkini ekleyin.
- `dokumanlar_repo_yolu`: Bu anahtara, göreceli olarak ders dökümanlarının tutulduğu GitHub reposunun yolunu verin. Örneğin, `../..` olarak belirlenirse, `README.md` dosyaları iki üst dizini kök dizin olarak kabul eder.
- `cikmislar`: İsteğe bağlı olarak boş bırakılabilir. Ders notlarının vb. tutulduğu herhangi bir dış kaynak linki varsa bu alana ekleyebilirsiniz.

**Not:** Google Sheets'ten CSV dosyasını nasıl linke dönüştüreceğinizi bilmiyorsanız, [bu adresteki](https://blog.golayer.io/google-sheets/export-google-sheets-to-csv) `Export Google Sheets to CSV Automatically` başlığına göz atabilirsiniz.


3. **Arayüzün Çalıştırılması:**
   Yukarıdaki dosyalar hazırlandıktan sonra, Windows'ta arayüzü çalıştırmak için `arayuz.bat` dosyası açılmalıdır.
    **Arayüz Butonlarının İşlevleri:**

   - **Giriş Güncelle:** 
    - Kök dizindeki README.md dosyasının girişle ilgili kısımlarını düzenleme ekranını açar.
    - Ekranda şunlar bulunur:
        - **Başlık:** Giriş kısmının başlığı.
        - **Açıklama:** Giriş kısmının açıklaması.
        - **İçindekiler Ekle:** İçindekiler çapası ekleme işleminin yapıldığı ekran. Örneğin, [Repo Kullanımı](#-repo-kullanımı) tıklandığında doğrudan o başlığa gitmeyi sağlayan çapa oluşturulur. Bu ekranda "İçerik Başlığı" gözükecek başlığı, "İçerik Çapası" ise gidilecek çapayı temsil eder.
        - **İçindekiler:** Düzenlenmek istenen içindekiler elemanına tıklanır ve düzenleme ekranı açılır. Ekleme ekranıyla aynı ekran açılır.
    - **Repo Kullanımı Düzenle:**
        - Repoyla alakalı kullanıcıya bilgi verme işi bu ekranda yapılır.
        - **Başlık:** Burada "Repo Kullanımı" kısmının başlığı düzenlenir.
        - **Talimat Ekle/Düzenle:** Talimat ekleme-düzenleme işlemi yapılır. Tıklandığında talimat ekleme-düzenleme ekranı açılır. Bu ekranda:
            - **Talimatlar:** Düzenlenmek istenen talimatın üstüne tıklanır ve düzenleme ekranı açılır. Burada talimatın yeni hali girilip kaydedilebilir. Sil butonuyla ilgili talimat silinir.
            - **Talimat Ekle:** Bu buton talimat ekleme ekranını açar.
        - **Kavram Ekle/Düzenle:** Kavram ekleme-düzenleme işlemi yapılır. Tıklandığında kavram ekleme ekranı açılır. Bu ekranda:
            - **Kavramlar:** Açıklamaları düzenlenmek istenen kavramın üstüne tıklanır. Üstüne tıklanan kavramın açıklamalar düzenleme ekranı açılır. Bu ekranda:
            - **Açıklamalar:** Düzenlenmek istenen açıklamanın düzenle butonuna basılır. Silinmek istenen açıklamanın sil butonuna basılır.
            - **Açıklama Ekle Butonu:** Bu buton ilgili kavram için açıklama ekle ekranına yönlendirir.
            - Kavramın yanında **Adı Düzenle** butonu bulunur. Butona tıklanınca ilgili kavramın adını düzenlemek için ekran açılır. Onun yanında da sil butonu bulunur. Bu da ilgili kavramı silmeye yarar.
            - **Kavram Ekle:** Bu buton kavram ekleme ekranına yönlendirir.
        - **Açıklama Ekle/Düzenle:**
        - Bu repo ile ilgili açıklama ekleme/düzenleme ekranına yönlendirir. Bu ekranda:
            - **Açıklamalar:** Düzenlenmek istenen açıklamanın üstüne tıklanırsa düzenleme ekranı açılır. Silinmek istenen açıklamanın sağındaki sil butonuna tıklanabilir.
            - **Açıklama Ekle:** Açıklama ekleme işlemini gerçekleştirir.



### Projeyi Çalıştırmak
Ders/Hoca vb. içeriklerini güncelleme arayüzünü çalıştırmak istiyorsanız
Linux için
```bash
./arayuz.sh
```
Windows için
```bat
arayuz.bat
```
dosyasını çalıştırmanız gerekiyor.


README.md içeriklerinin json dosyalarına göre güncellenmesini istiyorsanız
Linux için
```bash
./readme_guncelle.sh
```
Windows için
```bat
readme_guncelle.bat
```
dosyasını çalıştırmanız gerekiyor.

Oy/Yorumların google formdan çekilip json dosyalarının oylara göre göre güncellenmesini istiyorsanız
Linux için
```bash
./google_form_guncelle.sh
```
Windows için
```bat
google_form_guncelle.bat
```
dosyasını çalıştırmanız gerekiyor.

Eğer rutin şekilde google form girdilerinin dinlenip güncelleme işlemi yapılmasını istiyorsanız
Linux için
```bash
./rutin_kontrol.sh
```
Windows için
```bat
rutin_kontrol.bat
```
dosyasını çalıştırmanız gerekiyor.

Üst klasördeki dosyalarda yapılan değişiklikleri githuba yüklemek için
Linux için
```bash
./degisiklikleri_githuba_yolla.sh
```
Windows için
```bat
degisiklikleri_githuba_yolla.bat
```
dosyasını çalıştırmanız gerekiyor.


Üst klasördeki dosyalarda yapılan değişiklikleri githubdan çekmek için
Linux için
```bash
./degisiklikleri_githubdan_cek.sh
```
Windows için
```bat
degisiklikleri_githubdan_cek.bat
```
dosyasını çalıştırmanız gerekiyor.

ℹ️ Bu işlem risklidir. Eğer yerelde yapılmış değişiklikler varsa kaybolabilir !!!!

Arayüz kodundaki güncellemeleri almak için
Linux için
```bash
./arayuzu_githubla_esitle.sh
```
Windows için
```bat
arayuzu_githubla_esitle.bat
```
dosyasını çalıştırmanız gerekiyor.
