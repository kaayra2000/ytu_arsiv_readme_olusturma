from PyQt6.QtWidgets import (QComboBox, QDialog,QPushButton, QSizePolicy, QHBoxLayout, QLineEdit, QMessageBox, QVBoxLayout, QLabel, QFileDialog)
from metin_islemleri import elideText
import json
import os
from PyQt6.QtCore import QCoreApplication
import shutil
from degiskenler import DOKUMANLAR_REPO_YOLU_ANAHTARI ,KONFIGURASYON_JSON_PATH, JSON_DOSYALARI_DEPOSU_DOSYA_YOLU, EKLE_BUTONU_STILI, BIR_UST_DIZIN, MAAS_ISTATISTIKLERI_TXT_ADI
class KonfigurasyonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setMinimumWidth(600)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Konfigürasyon Düzenleyici")
        
        # Ana layout
        self.mainLayout = QVBoxLayout()
        self.comboBoxLayout = QHBoxLayout()
        self.jsonDepoLayout= QHBoxLayout()
        self.setLayout(self.mainLayout)
        
        # Sol tarafta seçenekler listesi
        self.comboBox = QComboBox()
        self.comboBox.currentIndexChanged.connect(self.onOptionSelected)
        self.comboBoxLayout.addWidget(self.comboBox)
        
        # Sağ tarafta seçeneğin değerini gösterecek QLineEdit
        self.valueEdit = QLineEdit()
        self.valueEdit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.comboBoxLayout.addWidget(self.valueEdit)
        self.mainLayout.addLayout(self.comboBoxLayout)

        self.kaydetButton = QPushButton("Json Kaydet")
        self.kaydetButton.setStyleSheet(EKLE_BUTONU_STILI)
        self.kaydetButton.clicked.connect(self.konfKaydet)
        self.jsonDepoLabel = QLabel("Json Dosyaları Yolu")
        self.yol = self.dosya_yolu_olustur()
        self.jsonDepoButton = QPushButton(elideText(self.yol, max_length=80))
        self.jsonDepoButton.setToolTip(self.yol)
        self.jsonDepoButton.clicked.connect(self.jsonDepoSec)
        self.jsonDepoLayout.addWidget(self.jsonDepoLabel)
        self.jsonDepoLayout.addWidget(self.jsonDepoButton)
        self.mainLayout.addWidget(self.kaydetButton)
        self.mainLayout.addLayout(self.jsonDepoLayout)
        self.depoKaydet = QPushButton("Json Dosyaları Yolu Kaydet")
        self.depoKaydet.clicked.connect(self.depoDosyasiKaydet)
        self.depoKaydet.setStyleSheet(EKLE_BUTONU_STILI)
        self.mainLayout.addWidget(self.depoKaydet)
        self.readConfig()
    def jsonDepoSec(self):
        # Kullanıcıya bir klasör seçtirme ve seçilen klasörün yolunu alma
        secilenKlasorYolu = QFileDialog.getExistingDirectory(self, "Klasör Seç", self.jsonDepoButton.toolTip())
        if secilenKlasorYolu:
            # Klasör seçildiyse, jsonDepoButton'un metnini güncelle
            self.jsonDepoButton.setText(elideText(secilenKlasorYolu, max_length=80))
            self.jsonDepoButton.setToolTip(secilenKlasorYolu)
    def depoDosyasiKaydet(self):
        secilenYol = self.jsonDepoButton.toolTip()
        if secilenYol == self.yol:
            QMessageBox.critical(self, "Hata", "Farklı bir klasör seçmediniz...")
            return
        # Kullanıcıya onay sorusu sor
        cevap = QMessageBox.question(self, "Değişiklikleri Kaydet", "Değişiklikleri kaydetmek istediğinize emin misiniz?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if cevap == QMessageBox.StandardButton.No:
            QMessageBox.information(self, "İptal", "Değişiklik Kaydedilmedi")
            return
        json_dosyalari = self.klasordeki_json_dosyalari(self.yol)
        json_dosyalari.append(MAAS_ISTATISTIKLERI_TXT_ADI)
        try:
            dokumanlar_goreceli_yol = self.config[DOKUMANLAR_REPO_YOLU_ANAHTARI]
            dokumanlar_gercek_yol = os.path.abspath(os.path.join(self.yol, dokumanlar_goreceli_yol))
            # Mevcut çalışma dizinini al
            cwd = os.getcwd()
            cwd = os.path.join(cwd,BIR_UST_DIZIN)
            # Seçilen yolun, cwd'ye göre göreceli yolunu hesapla
            goreceliYol = os.path.relpath(secilenYol, cwd)
            dokumanlar_yeni_goreceli_yol = os.path.relpath(dokumanlar_gercek_yol,secilenYol).replace(os.path.sep, "/")
            self.config[DOKUMANLAR_REPO_YOLU_ANAHTARI] = dokumanlar_yeni_goreceli_yol
            self.konfJsonaYaz()
            # İşletim sistemi farklılıklarını dikkate al
            goreceliYol = goreceliYol.replace(os.path.sep, "\n")
            # Göreceli yolu dosyaya kaydet
            with open(JSON_DOSYALARI_DEPOSU_DOSYA_YOLU, "w", encoding="utf-8") as dosya:
                dosya.write(goreceliYol)
            
            for jsonDosyasi in json_dosyalari:
                if not self.dosyaKopyala(self.yol, jsonDosyasi, secilenYol):
                    QMessageBox.critical(self, "Hata", f"{jsonDosyasi} dosyası kopyalanamadı")
            self.yol = secilenYol            
            QMessageBox.information(self, "Başarılı", "Değişiklikler başarıyla kaydedildi. Uygulamayı yeniden başlatın...")
            QCoreApplication.instance().quit()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Depo dosyası güncellenirken bir hata oluştu: {e}")

    def readConfig(self):
        try:
            with open(KONFIGURASYON_JSON_PATH, "r", encoding="utf-8") as file:
                self.config = json.load(file)
                for key in self.config.keys():
                    self.comboBox.addItem(key)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Konfigürasyon dosyası okunamadı: {e}")
    
    def konfKaydet(self):
        # Kullanıcıya onay sorusu sor
        cevap = QMessageBox.question(self, "Değişiklikleri Kaydet", "Değişiklikleri kaydetmek istediğinize emin misiniz?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if cevap == QMessageBox.StandardButton.No:
            QMessageBox.information(self, "İptal", "Değişiklik Kaydedilmedi")
            return
        try:
            # Seçili anahtarın yeni değerini config sözlüğüne kaydetme
            selectedKey = self.comboBox.currentText()  # Seçili anahtar
            newValue = self.valueEdit.text()  # Kullanıcı tarafından girilen yeni değer
            self.config[selectedKey] = newValue
            self.konfJsonaYaz()
            QMessageBox.information(self, "Başarılı", "Değişiklikler başarıyla kaydedildi.")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Konfigürasyon dosyası kaydedilemedi: {e}")

    def konfJsonaYaz(self):
        # Güncellenmiş config sözlüğünü JSON dosyasına yazma
        with open(KONFIGURASYON_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump(self.config, file, ensure_ascii=False, indent=4)
    def onOptionSelected(self, index):
        if index >= 0:
            selectedKey = self.comboBox.itemText(index)
            self.valueEdit.setText(self.config.get(selectedKey, ""))
    def dosya_yolu_olustur(self):
        try:
            # Dosya okuma
            with open(JSON_DOSYALARI_DEPOSU_DOSYA_YOLU, "r", encoding="utf-8") as dosya:
                icerik = dosya.read().strip().split("\n")
                # Dosya içeriğinden yolu parse etme
                relative_path = os.path.join(BIR_UST_DIZIN,*icerik)
                # Mevcut çalışma dizinini al
                cwd = os.getcwd()
                # CWD'ye göre tam yolu oluşturma
                tam_yol = os.path.join(cwd, relative_path)
                # İşletim sistemi farklılıklarını göz önünde bulundurarak doğru ayırıcıyı kullan
                tam_yol = os.path.normpath(tam_yol)
                return tam_yol
        except Exception as e:
            QMessageBox.critical(self,"Hata",f"Hata: {e}")
            return None
    def klasordeki_json_dosyalari(self, klasor_yolu):
        # JSON dosyalarını saklayacak bir liste oluştur
        json_dosyalari = []

        # Belirtilen klasördeki tüm dosya ve klasör isimlerini listele
        for dosya in os.listdir(klasor_yolu):
            # Eğer dosya .json uzantısına sahipse listeye ekle
            if dosya.endswith(".json"):
                json_dosyalari.append(dosya)
        
        return json_dosyalari

    def dosyaKopyala(self, eski_yol, dosya_adi, yeni_yol):
        try:
            # Eski dosyanın tam yolunu oluştur
            eski_dosya_yolu = os.path.join(eski_yol, dosya_adi)
            
            # Yeni dosyanın tam yolunu oluştur
            yeni_dosya_yolu = os.path.join(yeni_yol, dosya_adi)
            
            # Dosyayı eski yoldan yeni yola taşı
            shutil.copy(eski_dosya_yolu, yeni_dosya_yolu)
            return True
        except Exception as e:
            return False