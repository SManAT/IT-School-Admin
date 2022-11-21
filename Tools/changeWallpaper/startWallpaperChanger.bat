@echo off
IF /i "%username%"=="Student" goto start

echo "Not User Student ..."
goto commonexit

:languageDE
echo German
goto commonexit


:commonexit
rem bye