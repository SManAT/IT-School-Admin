@echo off

rem Run only once ====
SET LOCK=wallpaper_init.lock
IF EXIST %APPDATA%\%LOCK% GOTO NORMAL
  date /t > %APPDATA%\%LOCK%
  pip install . 

:NORMAL
  rem only for this User
  IF /i "%username%"=="Student" goto START
  echo "Not User Student ..."
  GOTO COMMONEXIT

:START
    rem Start Wallpaper Changer
    python changeWallpaper.py -g
    
:COMMONEXIT
    rem bye
