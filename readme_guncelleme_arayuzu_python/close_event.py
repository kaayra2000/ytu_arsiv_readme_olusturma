from PyQt6.QtWidgets import QMessageBox


def closeEventHandler(parent, event, is_programmatic_close, has_changes=True):
    """
    Pencere kapatma olayını yönetir.
    
    Args:
        parent: Üst pencere
        event: Kapatma olayı
        is_programmatic_close: Programatik olarak mı kapatılıyor
        has_changes: Kaydedilmemiş değişiklik var mı (varsayılan True - eski davranış)
    """
    if is_programmatic_close:
        event.accept()
        return
    
    # Değişiklik yoksa direkt kapat
    if not has_changes:
        event.accept()
        return
        
    reply = QMessageBox.question(
        parent,
        "Kapat",
        "Değişiklikleri kaydetmeden kapatmak istediğine emin misin?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    if reply == QMessageBox.StandardButton.Yes:
        event.accept()
    else:
        event.ignore()
