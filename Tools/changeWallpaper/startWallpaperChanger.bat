@echo off

rem Starterscript for explicit use in somewhere, NOT for general Usage

rem Run only once ===================
SET LOCK=wallpaper_init.lock
IF EXIST %APPDATA%\%LOCK% GOTO START
  date /t > %APPDATA%\%LOCK%
  pip install -e C:\ProgramData\Common-Software\changeWallpaper\

:START
    rem Start Wallpaper Changer
    python C:\ProgramData\Common-Software\changeWallpaper\src\changeWallpaper.py -g
    
:COMMONEXIT
    rem bye
