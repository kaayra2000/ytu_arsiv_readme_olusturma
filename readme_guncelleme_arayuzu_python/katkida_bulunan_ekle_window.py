from PyQt5.QtWidgets import (
    QLineEdit,
    QDialog,
    QPushButton,
    QVBoxLayout,
    QDesktopWidget,
    QLabel,
    QMessageBox,
    QComboBox,
)
from threadler import KatkiEkleThread
from progress_dialog import CustomProgressDialog
from degiskenler import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from close_event import closeEventHandler


class KatkidaBulunanEkleWindow(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setModal(True)
        self.is_programmatic_close = False
        self.parent = parent
        self.title = "Katkıda Bulunan Ekle"
        self.initUI()
        if os.path.exists(SELCUKLU_ICO_PATH):
            self.setWindowIcon(QIcon(SELCUKLU_ICO_PATH))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumSize(
            700, 200
        )  # Pencerenin en küçük olabileceği boyutu ayarlayın

        layout = QVBoxLayout()
        self.progressDialog = CustomProgressDialog("Kontrol Ediliyor...", self)
        self.progressDialog.close()
        # Ad ve GitHub Linki için giriş alanları
        self.name_label = QLabel("Ad")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_input = QLineEdit()
        self.github_label = QLabel("GitHub Kullanıcı Adı")
        self.github_label.setAlignment(Qt.AlignCenter)
        self.github_input = QLineEdit()
        self.katkida_bulunma_orani_label = QLabel("Katkıda Bulunma Oranı")
        self.katkida_bulunma_orani_label.setAlignment(Qt.AlignCenter)
        self.katkida_bulunma_orani = QComboBox()
        self.katkida_bulunma_orani.addItems(KATKIDA_BULUNMA_ORANI_DIZI)
        self.ekle_btn = QPushButton("Ekle", self)
        self.ekle_btn.setStyleSheet(EKLE_BUTONU_STILI)
        # Butona basıldığında ekleme işlevini çalıştır
        self.ekle_btn.clicked.connect(self.kaydet)

        # Arayüze elemanları ekle
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.github_label)
        layout.addWidget(self.github_input)
        layout.addWidget(self.katkida_bulunma_orani_label)
        layout.addWidget(self.katkida_bulunma_orani)
        layout.addWidget(self.ekle_btn)

        self.setLayout(layout)
        self.show()

    def closeEvent(self, event):
        closeEventHandler(self, event, self.is_programmatic_close)


    def kaydet(self):
        # Thread örneğini oluştur
        ad = self.name_input.text()
        github_kullanici_adi = self.github_input.text()
        self.thread = KatkiEkleThread(
            ad, github_kullanici_adi, KATKIDA_BULUNANLAR_JSON_PATH, self.katkida_bulunma_orani.currentText(),self
        )
        self.thread.finished.connect(self.islemSonucu)
        # ProgressDialog'u göster
        self.progressDialog.show()
        self.thread.start()

    def islemSonucu(self, success, message):
        self.progressDialog.close()
        if success:
            QMessageBox.information(self, "Başarılı", message)
            # Gerekli güncellemeleri yapın ve pencereyi kapatın
            self.parent.butonlariYenile()
            self.is_programmatic_close = True
            self.close()
        else:
            QMessageBox.warning(self, "Hata", message)
