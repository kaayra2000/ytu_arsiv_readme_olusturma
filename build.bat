@echo off
:: Build Script for Windows
:: Script'in bulunduğu dizine geç
cd /d "%~dp0"

CHCP 65001 >nul
git config --global i18n.commitEncoding utf-8
git config --global i18n.logOutputEncoding utf-8

echo PyInstaller Build Script
echo ========================================

:: Proje dizinini ve sanal ortam dizinini belirleyin
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%venv"

:: Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python bulunamadi!
    pause
    exit /b 1
)

:: Sanal ortam oluştur
if not exist "%VENV_DIR%" (
    echo venv bulunamiyor, olusturuluyor...
    python -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo venv olusturulamadi!
        pause
        exit /b 1
    )
    echo venv olusturuldu.
)

:: Sanal ortamı aktifle
call "%VENV_DIR%\Scripts\activate"

:: pip güncelle
pip install --upgrade pip

:: Projeyi pyproject.toml ile kur (dev bağımlılıklarıyla)
echo pyproject.toml ile kurulum yapiliyor...
pip install -e ".[dev]"

if %errorlevel% neq 0 (
    echo Kurulum basarisiz!
    pause
    exit /b 1
)
echo Kurulum tamamlandi.

:: spec_dosyalari dizinine geç
set "SPEC_DIR=%PROJECT_DIR%spec_dosyalari"
cd /d "%SPEC_DIR%"

if not exist "main.spec" (
    echo main.spec bulunamadi!
    pause
    exit /b 1
)

echo Build basliyor...

:: Build al
pyinstaller main.spec --distpath ../dist --workpath ../build --noconfirm

if %errorlevel% equ 0 (
    echo ========================================
    echo Build basariyla tamamlandi!
    echo Executable: %PROJECT_DIR%dist\main.exe
    echo ========================================
) else (
    echo Build basarisiz oldu!
    pause
    exit /b 1
)

call deactivate
pause
exit /b 0
