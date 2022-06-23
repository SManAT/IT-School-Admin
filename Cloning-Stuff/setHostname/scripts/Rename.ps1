#Set UTF-8-----------------------
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
#Admin Privileges----------------
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
Write  'Running PS with Administrator Rights'
#Run as Admin--------------------

$User = "{% localadmin %}"
$strPass = ConvertTo-SecureString -String "{% localadminpasswd %}" -AsPlainText -Force
$Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ($User, $strPass)

Start-Sleep -s 2

Rename-Computer -ComputerName (hostname) -NewName "{% newhostname %}" -LocalCredential $Credential

Start-Sleep -s 2
