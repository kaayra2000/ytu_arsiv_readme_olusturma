"""
Ekran çözünürlüğüne göre dinamik boyut hesaplama yardımcı modülü.

Bu modül, pencere boyutlarını kullanıcının ekran çözünürlüğüne göre
oranlanmış şekilde hesaplar.
"""

from PyQt6.QtGui import QGuiApplication


def get_screen_size():
    """
    Mevcut ekranın kullanılabilir boyutunu döndürür.
    
    Returns:
        tuple: (genişlik, yükseklik) piksel cinsinden veya None eğer ekran alınamazsa
    """
    try:
        app = QGuiApplication.instance()
        if app is None:
            return None
        
        screen = QGuiApplication.primaryScreen()
        if screen is None:
            return None
            
        geometry = screen.availableGeometry()
        return geometry.width(), geometry.height()
    except Exception:
        return None


def calculate_minimum_size(base_width, base_height, reference_width=1920, reference_height=1080):
    """
    Referans çözünürlüğe göre oranlanmış minimum boyut döndürür.
    
    Referans çözünürlük varsayılan olarak 1920x1080 (Full HD) alınır.
    Eğer ekran çözünürlüğü referanstan küçükse, boyutlar orantılı olarak küçültülür.
    Eğer ekran çözünürlüğü referanstan büyükse, boyutlar değiştirilmez.
    
    Args:
        base_width: Temel genişlik (referans çözünürlük için)
        base_height: Temel yükseklik (referans çözünürlük için)
        reference_width: Referans ekran genişliği (varsayılan 1920)
        reference_height: Referans ekran yüksekliği (varsayılan 1080)
    
    Returns:
        tuple: (hesaplanan_genişlik, hesaplanan_yükseklik)
    """
    screen_size = get_screen_size()
    
    # Eğer ekran boyutu alınamazsa (QApplication henüz başlatılmamış), 
    # base değerleri olduğu gibi döndür
    if screen_size is None:
        return base_width, base_height
    
    screen_w, screen_h = screen_size
    
    # Ekran/referans oranını hesapla
    width_ratio = screen_w / reference_width
    height_ratio = screen_h / reference_height
    
    # En küçük oranı al (1.0'ı aşmamak için - büyük ekranlarda büyütme yapma)
    ratio = min(width_ratio, height_ratio, 1.0)
    
    # Çok küçük ekranlar için minimum bir oran belirle
    ratio = max(ratio, 0.5)
    
    return int(base_width * ratio), int(base_height * ratio)


def calculate_scroll_area_size(base_width, base_height):
    """
    Kaydırılabilir alanlar için boyut hesaplar.
    
    Args:
        base_width: Temel genişlik
        base_height: Temel yükseklik
    
    Returns:
        tuple: (hesaplanan_genişlik, hesaplanan_yükseklik)
    """
    return calculate_minimum_size(base_width, base_height)

