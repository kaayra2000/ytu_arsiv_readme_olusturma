import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
import json
import requests
import select
from degiskenler import *


class ScriptRunnerThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, paths):
        QThread.__init__(self)
        self.google_forum_islemleri_path, self.readme_olustur_path = paths

    def run(self):
        try:
            subprocess.run(
                "python3 hoca_icerikleri_guncelle.py\n",
                shell=True,
                cwd=self.google_forum_islemleri_path,
                check=True,
            )
            subprocess.run(
                "python3 ders_icerikleri_guncelle.py\n",
                shell=True,
                cwd=self.google_forum_islemleri_path,
                check=True,
            )
            subprocess.run(
                "python3 readme_olustur.py\n",
                shell=True,
                cwd=self.readme_olustur_path,
                check=True,
            )
            self.finished.emit()
        except subprocess.CalledProcessError as e:
            self.error.emit(str(e))


# Uzun süren işlemi gerçekleştirecek thread sınıfı
class HocaKaydetThread(QThread):
    finished = pyqtSignal()  # İşlem bittiğinde sinyal göndermek için
    error = pyqtSignal(str)  # Hata mesajı için sinyal

    def __init__(self, hoca, data, parent):
        super().__init__()
        self.hoca = hoca
        self.data = data
        self.parent = parent

    def run(self):
        ad = self.parent.adInput.text()
        if not ad:
            self.error.emit("Hoca adı boş olamaz!")
            return

        ofis = self.parent.ofisInput.text().strip()
        link = self.parent.linkInput.text().strip()
        erkek_mi = self.parent.erkekMiInput.currentText() == "Evet"
        dersler = self.parent.secilenDersleriDondur()
        hoca_aktif_gorevde_mi = self.parent.aktifGorevdeInput.currentText() == "Evet"
        if link and not self.parent.check_url(link):
            self.error.emit("Güncelleme başarısız!!!")
            return  # Eğer URL geçerli değilse fonksiyondan çık
        if self.hoca:  # Düzenleme modunda
            self.hoca.update(
                {
                    AD: self.parent.unvanInput.currentText() + " " + ad,
                    OFIS: ofis,
                    LINK: link,
                    ERKEK_MI: erkek_mi,
                    DERSLER: dersler,
                    HOCA_AKTIF_GOREVDE_MI: hoca_aktif_gorevde_mi,
                }
            )
        else:  # Ekleme modunda
            yeni_hoca = {
                AD: self.parent.unvanInput.currentText() + " " + ad,
                OFIS: ofis,
                LINK: link,
                ERKEK_MI: erkek_mi,
                DERSLER: dersler,
                HOCA_AKTIF_GOREVDE_MI: hoca_aktif_gorevde_mi,
            }
            self.data[HOCALAR].append(yeni_hoca)
        self.finished.emit()


class KatkiEkleThread(QThread):
    finished = pyqtSignal(bool, str)  # İşlem sonucu ve mesaj için sinyal

    def __init__(self, ad, github_kullanici_adi, JSON_DOSYASI, parent=None):
        super(KatkiEkleThread, self).__init__(parent)
        self.ad = ad
        self.github_kullanici_adi = github_kullanici_adi
        self.github_url = f"https://github.com/{self.github_kullanici_adi}"
        self.JSON_DOSYASI = JSON_DOSYASI

    def run(self):
        try:
            # JSON dosyasını aç ve oku
            try:
                with open(self.JSON_DOSYASI, "r+", encoding="utf-8") as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = {KATKIDA_BULUNANLAR: []}
            if BOLUM_ADI not in data:
                data[BOLUM_ADI] = "Katkıda Bulunanlar"
            if BOLUM_ACIKLAMASI not in data:
                data[
                    BOLUM_ACIKLAMASI
                ] = "Bu bölümde reponun hazırlanmasında katkıda bulunan insanlar listelenmiştir. Siz de katkıda bulunmak isterseniz bizimle iletişime geçin. Ya da merge request gönderin."

            if not self.ad or not self.github_kullanici_adi:
                self.finished.emit(False, "Ad ve GitHub kullanıcı adı boş olamaz!")
                return
            # Kontrolleri gerçekleştir
            if any(
                kisi[AD].lower() == self.ad.lower() for kisi in data[KATKIDA_BULUNANLAR]
            ):
                self.finished.emit(False, "Bu isim zaten mevcut!")
            elif any(
                kisi[GITHUB_LINK] == self.github_url
                for kisi in data[KATKIDA_BULUNANLAR]
            ):
                self.finished.emit(False, "Bu GitHub linki zaten eklenmiş!")
            else:
                # GitHub URL'sinin varlığını kontrol et
                response = requests.get(self.github_url)
                if response.status_code == 404:
                    self.finished.emit(False, "GitHub kullanıcı adı geçerli değil!")
                    return

                # Yeni veriyi ekle ve dosyayı güncelle
                data[KATKIDA_BULUNANLAR].append(
                    {AD: self.ad, GITHUB_LINK: self.github_url}
                )
                with open(self.JSON_DOSYASI, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                self.finished.emit(True, "Katkıda bulunan eklendi!")
        except Exception as e:
            self.finished.emit(False, f"Bir hata oluştu: {e}")


class KatkiKaydetThread(QThread):
    finished = pyqtSignal(bool, str)  # İşlem sonucu ve mesaj için sinyal

    def __init__(self, kisi, ad, github_kullanici_adi, data, JSON_YOLU, parent=None):
        super(KatkiKaydetThread, self).__init__(parent)
        self.kisi = kisi
        self.ad = ad
        self.github_kullanici_adi = github_kullanici_adi
        self.data = data
        self.github_url = "https://github.com/" + self.github_kullanici_adi
        self.JSON_YOLU = JSON_YOLU

    def run(self):
        # GitHub linkinin varlığını kontrol et
        try:
            response = requests.get(self.github_url)
            if response.status_code == 404:
                self.finished.emit(False, "GitHub linki geçerli değil!")
                return
        except requests.exceptions.RequestException as e:
            self.finished.emit(
                False, f"GitHub linki kontrol edilirken bir hata oluştu: {e}"
            )
            return

        # Değişiklikleri uygula ve JSON dosyasını güncelle
        self.kisi[AD] = self.ad
        self.kisi[GITHUB_LINK] = self.github_url
        try:
            with open(self.JSON_YOLU, "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            self.finished.emit(True, "Katkıda bulunan güncellendi!")
        except Exception as e:
            self.finished.emit(False, f"Dosya yazılırken bir hata oluştu: {e}")


class CMDScriptRunnerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    info = pyqtSignal(str)

    def __init__(self, cmd, baslik = None):
        super().__init__()
        self.cmd = cmd
        self.calismaya_devam_et = True
        self.baslik = baslik
    def run(self):
        try:
            # Komutu subprocess.Popen ile çalıştır
            with subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1) as process:
                son_hata_mesaj = ""
                son_bilgi_mesaj = ""
                # stdout'tan sürekli olarak veri oku
                while True:
                    if not self.calismaya_devam_et:
                        mesaj = "İşlem kullanıcı tarafından iptal edildi."
                        bilgi = mesaj if self.baslik is None else f"{self.baslik}\n{mesaj}"
                        # Süreci durdur
                        process.terminate()  # ya da process.kill() kullanılabilir
                        self.error.emit(bilgi)
                        return
                    reads = [process.stdout.fileno(), process.stderr.fileno()]
                    readable, _, _ = select.select(reads, [], [])

                    for fd in readable:
                        if fd == process.stdout.fileno():
                            line = process.stdout.readline()
                            if line:
                                std_out = line.strip()
                                self.info.emit(std_out)
                                son_bilgi_mesaj = std_out
                        if fd == process.stderr.fileno():
                            line = process.stderr.readline()
                            if line:
                                std_err = line.strip()
                                self.info.emit(std_err)
                                son_hata_mesaj = std_err

                    if process.poll() is not None:
                        break  # Süreç tamamlandı
                # İşlem tamamlandığında çıkış kodunu kontrol et
                process.wait()
                if process.returncode == 0:
                    self.finished.emit(f"İşlem başarıyla tamamlandı.\nSon Mesaj: {son_bilgi_mesaj}")
                else:
                    if son_hata_mesaj == "":
                        son_hata_mesaj = son_bilgi_mesaj
                    # stderr'den hata mesajlarını oku ve emit et
                    self.error.emit(f"Komut başarısız oldu, çıkış kodu: {process.returncode}, Hata: {son_hata_mesaj}")

        except Exception as e:
            self.error.emit(f"Hata oluştu: {str(e)}")
    def durdur(self):
        self.calismaya_devam_et = False