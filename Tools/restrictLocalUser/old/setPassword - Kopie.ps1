#Set UTF-8-----------------------
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
#Admin Privileges----------------
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
Write  'Running PS with Administrator Rights'
#Run as Admin--------------------

# change Password from .\Student
$User = "Student"
$Password = "schule"
$password = $Password | ConvertTo-SecureString -AsPlainText -Force
Set-LocalUser -Name $User -Password $password -Verbose

Set-LocalUser -Name $User -UserMayChangePassword 0 -PasswordNeverExpires 1
