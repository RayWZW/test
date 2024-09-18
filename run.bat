@echo off
setlocal

:: Define Python version and installation paths
set PYTHON_VERSION=3.12.0
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%
set DOWNLOAD_DIR=%USERPROFILE%\Downloads
set CLIENT_SCRIPT_URL=https://raw.githubusercontent.com/RayWZW/test/main/client.py
set CLIENT_SCRIPT=%DOWNLOAD_DIR%\client.py

:: Download Python installer
echo Downloading Python %PYTHON_VERSION% installer...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_INSTALLER_URL% -OutFile %PYTHON_INSTALLER%" 

:: Install Python with the Add to PATH option enabled
echo Installing Python %PYTHON_VERSION% and adding to PATH...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

:: Clean up installer
del %PYTHON_INSTALLER%

:: Verify Python installation and add to PATH manually if needed
echo Verifying Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo Python installation failed!
    exit /b 1
)

:: Ensure pip is up to date
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install required Python packages
echo Installing required Python packages...
python -m pip install opencv-python pyautogui pillow numpy

:: Check installations
echo Checking installed packages...
python -m pip list

:: Download client.py from GitHub
echo Downloading client.py from GitHub...
powershell -Command "Invoke-WebRequest -Uri %CLIENT_SCRIPT_URL% -OutFile %CLIENT_SCRIPT%" 

:: Run client.py script in a new command prompt window
echo Running client.py script...
start python "%CLIENT_SCRIPT%"

:: Notify user and exit
echo Installation and setup complete! Client script is running independently.
endlocal
exit
