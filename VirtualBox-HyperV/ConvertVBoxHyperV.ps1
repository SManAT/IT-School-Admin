$HddPath = "F:\Virtual Machines\VirtualBox\Machines\life-2021-10-Klon\"
$TargetPath = "H:\HyperV\Virtual Hard Disks\"
$Hdd = "life-2021-10-Klon-disk1.vdi"

$VBoxPath = "C:\Program Files\Oracle\VirtualBox\"
# dont change after this line -----------------------


#Set UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
#Admin Privileges----------------
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
Write  'Running PS with Administrator Rights'
#Run as Admin--------------------

$TargetHdd = $Hdd -replace ".vdi$", ".vhd"

$TPath = Join-Path -Path $TargetPath -ChildPath $TargetHdd
$HPath = Join-Path -Path $HddPath -ChildPath $Hdd

# Delete Medium if exists
$AllArgs = @('closemedium', 'disk', '$TPath', '--delete')
Invoke-Expression "& '$($VBoxPath)VBoxManage.exe' $AllArgs"
     
# ----------------------------
Write-Output "Convert $HPath > $TPath"

$AllArgs = @('clonemedium', '$HPath', '$TPath', '--format VHD')
Invoke-Expression "& '$($VBoxPath)VBoxManage.exe' $AllArgs"

# ----------------------------
# to VHDX wit Cmdlet
$TargetHddX = $TargetHdd -replace ".vhd$", ".vhdx"
$TXPath = Join-Path -Path $TargetPath -ChildPath $TargetHddX
Convert-VHD -Path $TPath -DestinationPath $TXPath

# Delete File vhd
Remove-Item $TPath

Write-Output "Exit in 5 Sekunden ..."
Start-Sleep -s 5
