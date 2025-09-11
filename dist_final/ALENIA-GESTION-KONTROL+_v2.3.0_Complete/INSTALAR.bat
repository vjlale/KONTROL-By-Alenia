@echo off
title ALENIA GESTION-KONTROL+ v2.3.0 - Instalador
color 0A

echo.
echo ═══════════════════════════════════════════════════════════════
echo     [SOFTWARE] ALENIA GESTION-KONTROL+ v2.3.0
echo     INSTALADOR INTELIGENTE
echo ═══════════════════════════════════════════════════════════════
echo.

echo [CHECK] Verificando sistema...
echo.

REM Verificar Windows 64-bit
wmic os get osarchitecture | find "64-bit" >nul
if errorlevel 1 (
    echo [ERROR] ERROR: Este software requiere Windows 64-bit
    pause
    exit /b 1
)

echo [OK] Sistema compatible detectado
echo.

echo [SETUP] Creando acceso directo en Escritorio...
set "desktop=%USERPROFILE%\Desktop"
set "target=%~dp0KONTROL-PLUS.exe"
set "shortcut=%desktop%\KONTROL+ Gestión.lnk"

powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%target%'; $shortcut.IconLocation = '%target%'; $Shortcut.Save()"

if exist "%shortcut%" (
    echo [OK] Acceso directo creado en Escritorio
) else (
    echo [WARNING] No se pudo crear acceso directo
)

echo.
echo [QUESTION] ¿Desea ejecutar KONTROL+ ahora? (S/N)
set /p choice=

if /i "%choice%"=="S" (
    echo.
    echo [START] Iniciando KONTROL+...
    start "" "%target%"
) else (
    echo.
    echo [INFO] Puede iniciar KONTROL+ desde:
    echo    → Doble clic en KONTROL-PLUS.exe
    echo    → Acceso directo en Escritorio
)

echo.
echo [OK] Instalación completada exitosamente
echo.
echo [SOPORTE] Soporte técnico: +54 351 6875178
echo [EMAIL] Email: alenia.online@gmail.com
echo.
pause
