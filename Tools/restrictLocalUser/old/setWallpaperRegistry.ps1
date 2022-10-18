#Set UTF-8-----------------------
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
#Admin Privileges----------------
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
Write  'Running PS with Administrator Rights'
#Run as Admin--------------------


# Wallpaper
New-Item -Path HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies -Name System –Force

New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Name "Wallpaper" -Value "$Env:AppData\wallpapers\wallpaper.jpg"

# 0 (Centered), 1 (Tiled), 2 (Stretched)
New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Policies\System" -Name "WallpaperStyle" -Value 2



