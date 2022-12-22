@echo off

rem Run only once ====
IF EXIST wallpaper_init.txt GOTO END
  date /t >> C:\Users\%USER%\AppData\wallpaper_init.txt       
  pip install . 
:END

rem only for this User
IF /i "%username%"=="Student" goto start
echo "Not User Student ..."
goto commonexit

:start
    rem Start Wallpaper Changer
    python changeWallpaper.py -g

    goto commonexit
:commonexit
    rem bye