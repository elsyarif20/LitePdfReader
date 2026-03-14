@echo off
set PUBLISHER="Liyas Syarifudin, S.Pd.I, M.Pd"
set MSI_NAME=LitePDF_Ultra_Pro_v3.msi
set SIGNTOOL="C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe"

echo [1/3] Membangun Executable...
call venv\Scripts\activate
pyinstaller --noconsole --onefile --clean --add-data "app_icon.ico;." --icon=app_icon.ico --hidden-import=pytesseract --hidden-import=pdf2docx LitePDF.py

echo [2/3] Membangun Installer MSI...
wix build Product.wxs -o %MSI_NAME%

echo [3/3] Menandatangani Digital...
if exist %SIGNTOOL% (
    %SIGNTOOL% sign /n %PUBLISHER% /t http://timestamp.digicert.com /fd sha256 %MSI_NAME%
) else (
    echo SignTool tidak ditemukan. MSI tetap dibuat tanpa tanda tangan.
)

echo.
echo PROSES SELESAI! File MSI Bapak siap dibagikan.
pause