@echo off
setlocal

REM Batch file to build the LOS Automation GUI executable using PyInstaller spec file

cd /d "%~dp0"

echo ==========================================
echo Building LOS Automation Suite...
echo ==========================================

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

REM Clean up previous builds
if exist build (
    echo Cleaning build directory...
    rmdir /s /q build
)
if exist dist (
    echo Cleaning dist directory...
    rmdir /s /q dist
)

REM Build the executable using the spec file
echo.
echo Running PyInstaller with spec file...
echo.

python -m PyInstaller --noconfirm LOSAutomationGUI.spec

if errorlevel 0 (
    echo.
    echo ==========================================
    echo SUCCESS: Executable built successfully!
    echo.
    echo Copying essential files to dist folder...
    
    if not exist "dist\config.json" copy "config.json" "dist\"
    if not exist "dist\Data" xcopy /E /I "Data" "dist\Data"
    
    echo.
    echo Location: %~dp0dist\LOSAutomationGUI.exe
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo ERROR: Failed to build executable.
    echo ==========================================
)

pause
