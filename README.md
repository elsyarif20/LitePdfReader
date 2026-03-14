🚀 Deployment Guide: LitePDF Ultra Pro
Oleh: Liyas Syarifudin, S.Pd.I, M.Pd
Dokumen ini menjelaskan langkah-langkah untuk melakukan build, penandatanganan digital, dan distribusi aplikasi LitePDF agar siap digunakan oleh pengguna akhir.
________________________________________
1. Persiapan Lingkungan (Environment)
Pastikan semua library Python yang dibutuhkan sudah terinstal di Virtual Environment:
Bash
pip install customtkinter pymupdf pillow pdf2docx pytesseract python-docx
________________________________________
2. Proses Build Executable (.exe)
Gunakan PyInstaller untuk mengonversi skrip Python menjadi file eksekusi tunggal.
Bash
pyinstaller --noconsole --onefile --clean \
--add-data "app_icon.ico;." \
--icon=app_icon.ico \
--hidden-import=customtkinter \
--hidden-import=fitz \
--name "LitePDF" \
LitePDF.py
________________________________________
3. Proses Build Installer (.msi)
Gunakan WiX Toolset v4 untuk membuat paket installer agar aplikasi terdaftar secara resmi di sistem Windows (Program Files & Start Menu).
Bash
# Jalankan perintah build WiX
wix build Product.wxs -o LitePDF_v3.msi
________________________________________
4. Penandatanganan Digital (Digital Signing)
Langkah ini krusial agar aplikasi tidak diblokir oleh Windows SmartScreen dan memunculkan nama Bapak sebagai Verified Publisher.
PowerShell
# Gunakan SignTool dari Windows SDK
& "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe" sign /n "Liyas Syarifudin, S.Pd.I, M.Pd" /t http://timestamp.digicert.com /fd sha256 LitePDF_v3.msi
________________________________________
5. Distribusi ke Pengguna
Setelah file .msi siap dan tertanda tangan, deploy melalui salah satu jalur berikut:
A. Melalui Server Lokal (UGREEN)
1.	Salin file LitePDF_v3.msi ke folder sharing server.
2.	Alamat akses: \\IP_SERVER_UGREEN\Public\Apps\LitePDF\.
B. Melalui Portal Streamlit (Cloud)
1.	Upload file MSI ke GitHub Repository.
2.	Hubungkan ke Streamlit Cloud untuk membuat link unduhan publik.
________________________________________
6. Verifikasi Pasca-Instalasi
Setelah user menginstal, pastikan:
1.	Ikon muncul di Desktop dan Start Menu.
2.	Klik kanan file PDF -> Open With -> LitePDF berfungsi dengan baik.
3.	Versi yang muncul di Add/Remove Programs adalah V3.0.0
________________________________________
Catatan Keamanan:
Selalu simpan file sertifikat .pfx atau .cer di tempat yang aman. Jangan membagikan Private Key sertifikat kepada pihak luar.
