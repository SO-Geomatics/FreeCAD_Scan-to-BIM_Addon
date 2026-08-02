REM ============================================================================
REM ScanToBIM Installation
REM ============================================================================

@echo off
setlocal

cd /d "%~dp0"

echo **********  ScanToBIM Installation *************
echo ************************************************
echo.

REM 0) Checking environnement variable FREECAD_HOME
if not defined FREECAD_HOME (
    echo ERROR : Env. variable FREECAD_HOME doesn't exist.
	echo Please create "FREECAD_HOME" env. variable before running this script
	pause
    exit /b 1
)

REM Defining repertories
set "SOURCE1=HOME_MOD_ScanToBIM\ScanToBIM"
set "TARGET1=%FREECAD_HOME%\Mod\ScanToBIM"
REM to test without FREECAD_HOM -> set "TARGET1=C:\Users\Admin\Desktop\Mod\ScanToBIM"
set "TYPE1=       Addon Files       "

set "SOURCE2=HOME_DATA_MOD_ScanToBIM\ScanToBIM"
set "TARGET2=%FREECAD_HOME%\data\Mod\ScanToBIM"
REM to test without FREECAD_HOM -> set "TARGET2=C:\Users\Admin\Desktop\Data\Mod\ScanToBIM"
set "TYPE2= Addon Ressources Files  "


REM ===== Addon Files =====
call :COPY_DIR "%SOURCE1%" "%TARGET1%" "%TYPE1%"
if errorlevel 1 exit /b 1


REM ===== Addon Ressources Files =====
call :COPY_DIR "%SOURCE2%" "%TARGET2%" "%TYPE2%"
if errorlevel 1 exit /b 1


echo.
echo All repertories successfully copied.
pause
exit /b 0


REM =================================================
REM Copy function
REM =================================================
:COPY_DIR

set "SOURCE=%~1"
set "TARGET=%~2"
set "TYPE=%~3"

echo ==========%TYPE%=============
echo.
echo Source      : %SOURCE%
echo Destination : %TARGET%

REM Checking source
if not exist "%SOURCE%" (
    echo ERROR : Source doesn't exist.
    exit /b 1
)

REM Deleting existing repertory
if exist "%TARGET%" (
    echo Deleting existing repertory...

    rmdir /s /q "%TARGET%"

    if exist "%TARGET%" (
        echo ERROR : Impossible to delete %TARGET%.
        exit /b 1
    )
)

REM Creating
echo Copying...

xcopy "%SOURCE%" "%TARGET%" /E /I /H /Y

if not exist "%TARGET%" (
    echo ERROR : Copy failed.
    exit /b 1
)

echo Success.
echo.
exit /b 0