@echo off

rem Run only once ===================
SET LOCK=wallpaper_init.lock
IF EXIST %APPDATA%\%LOCK% GOTO START
  date /t > %APPDATA%\%LOCK%
  pip install -e .

:START
    rem Start Wallpaper Changer
    python src/changeWallpaper.py -g
    
:COMMONEXIT
    rem bye
