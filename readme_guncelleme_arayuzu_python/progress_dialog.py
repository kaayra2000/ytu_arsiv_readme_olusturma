from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressDialog, QPushButton, QVBoxLayout, QDialog, QMessageBox


class CustomProgressDialog(QProgressDialog):
    def __init__(self, title, parent=None):
        super(CustomProgressDialog, self).__init__(title, None, 0, 0, parent)
        self.init_ui()

    def init_ui(self):
        # İptal butonunu kaldır
        self.setCancelButton(None)
        # Pencere başlık çubuğunu kaldır
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        self.setWindowModality(Qt.WindowModal)
        self.setMinimumDuration(0)
        self.setAutoClose(True)

        # ProgressBar stilini özelleştir
        self.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
            }"""
        )

        # Sürekli dönen bir hale getir
        self.setRange(0, 0)
class CustomProgressDialogWithCancel(QDialog):
    def __init__(self, title, parent=None, fonksiyon = None):
        super().__init__(parent)
        self.progress_dialog = CustomProgressDialog(title, parent)
        self.progress_dialog.setModal(False)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.fonksiyon = fonksiyon
        self.iptale_basildi = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        # İptal butonunu oluştur ve bağla
        self.iptal_butonu = QPushButton("İptal", self)
        self.iptal_butonu.clicked.connect(self.fonksiyon)

        # ProgressBar ve İptal butonunu layout'a ekle
        layout.addWidget(self.progress_dialog)
        layout.addWidget(self.iptal_butonu)

        # Layout'u pencereye ayarla
        self.setLayout(layout)
    def close(self):
        self.progress_dialog.close()
        super().close()

    def closeEvent(self, event):
        self.close()
        super().closeEvent(event)
    def setLabelText(self, text):
        self.progress_dialog.setLabelText(text)