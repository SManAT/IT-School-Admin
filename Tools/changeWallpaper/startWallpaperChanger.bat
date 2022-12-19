@echo off
rem only for this USer
IF /i "%username%"=="Student" goto start

echo "Not User Student ..."
goto commonexit

rem ==========================================================
:start

    rem Run only once
    SET USER=Student
    IF EXIST C:\Users\%USER%\AppData\wallpaper_init.txt GOTO END
        date /t >> C:\Users\%USER%\AppData\wallpaper_init.txt
       
        pip install . 
    :END

    rem Start Wallpaper Changer
    python changeWallpaper.py -g

    goto commonexit
rem ==========================================================
:commonexit
    rem bye