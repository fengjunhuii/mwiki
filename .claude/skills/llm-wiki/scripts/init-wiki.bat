@echo off
REM init-wiki.bat — Initialize a wiki vault for codebase analysis (Windows)
REM Usage: init-wiki.bat <project-path> [--name <wiki-name>]

setlocal enabledelayedexpansion

set "PROJECT_PATH="
set "WIKI_NAME="

:parse_args
if "%~1"=="" goto :done_args
if /I "%~1"=="--name" (
    set "WIKI_NAME=%~2"
    shift
    shift
    goto :parse_args
)
set "PROJECT_PATH=%~1"
shift
goto :parse_args

:done_args

if "%PROJECT_PATH%"=="" (
    echo Usage: init-wiki.bat ^<project-path^> [--name ^<wiki-name^>]
    echo   project-path: Path to the source code project to analyze
    echo   --name: Optional wiki directory name ^(default: ^<project-dir^-Wiki^)
    exit /b 1
)

if not exist "%PROJECT_PATH%" (
    echo Error: Project directory does not exist: %PROJECT_PATH%
    exit /b 1
)

REM Derive wiki name from project directory
if "%WIKI_NAME%"=="" (
    for %%F in ("%PROJECT_PATH%") do set "WIKI_NAME=%%~nF-Wiki"
)

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "SKILL_ROOT=%SCRIPT_DIR%.."
set "ASSETS_DIR=%SKILL_ROOT%\assets"

REM Create wiki directory structure
echo Creating wiki: %WIKI_NAME%
mkdir "%WIKI_NAME%" 2>nul
mkdir "%WIKI_NAME%\entities" 2>nul
mkdir "%WIKI_NAME%\concepts" 2>nul
mkdir "%WIKI_NAME%\changelog" 2>nul
mkdir "%WIKI_NAME%\_archive" 2>nul
mkdir "%WIKI_NAME%\.cache" 2>nul

REM Get current date
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value') do set "dt=%%a"
set "DATE=%dt:~0,4%-%dt:~4,2%-%dt:~6,2%"

REM Copy template files (basic copy - sed replacement done by Claude)
if exist "%ASSETS_DIR%\schema-template.md" (
    copy /y "%ASSETS_DIR%\schema-template.md" "%WIKI_NAME%\SCHEMA.md" >nul
    echo   Created SCHEMA.md
)
if exist "%ASSETS_DIR%\index-template.md" (
    copy /y "%ASSETS_DIR%\index-template.md" "%WIKI_NAME%\index.md" >nul
    echo   Created index.md
)
if exist "%ASSETS_DIR%\readme-template.md" (
    copy /y "%ASSETS_DIR%\readme-template.md" "%WIKI_NAME%\README.md" >nul
    echo   Created README.md
)
if exist "%ASSETS_DIR%\log-template.md" (
    copy /y "%ASSETS_DIR%\log-template.md" "%WIKI_NAME%\log.md" >nul
    echo   Created log.md
)
if exist "%ASSETS_DIR%\purpose-template.md" (
    copy /y "%ASSETS_DIR%\purpose-template.md" "%WIKI_NAME%\purpose.md" >nul
    echo   Created purpose.md
)

echo   Created .gitignore
(
echo .cache/
echo *.tmp
) > "%WIKI_NAME%\.gitignore"

echo.
echo Wiki vault created: %WIKI_NAME%\
echo Source project: %PROJECT_PATH%
echo.
echo Next steps:
echo   1. Use '/llm-wiki scan' to analyze the project structure
echo   2. Use '/llm-wiki analyze' to deep-dive into modules
echo   3. Use '/llm-wiki generate' to create wiki pages

endlocal
