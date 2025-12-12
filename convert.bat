@echo off
REM Notion to Obsidian Converter - Windows Batch Script
REM Usage: convert.bat <input_directory> <output_directory>

echo ========================================
echo Notion to Obsidian Converter
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if arguments are provided
if "%~1"=="" (
    echo Usage: convert.bat ^<input_directory^> ^<output_directory^>
    echo.
    echo Example:
    echo   convert.bat "C:\NotionExport" "C:\ObsidianVault"
    echo.
    pause
    exit /b 1
)

if "%~2"=="" (
    echo Usage: convert.bat ^<input_directory^> ^<output_directory^>
    echo.
    echo Example:
    echo   convert.bat "C:\NotionExport" "C:\ObsidianVault"
    echo.
    pause
    exit /b 1
)

REM Run the converter
echo Converting from: %~1
echo Converting to:   %~2
echo.
echo Please wait...
echo.

python notion_to_obsidian.py "%~1" "%~2" --verbose

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Conversion completed successfully!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Conversion failed. Please check errors above.
    echo ========================================
)

echo.
pause
