$VBoxPath = "C:\Program Files\Oracle\VirtualBox\"
$HddPath = "H:\WinServer20220\Clients\DC1\"
$TargetPath = "H:\HyperV\Virtual Hard Disks\"

$Hdd = "WinServer20220.vdi"

# dont change after this line -----------------------


#Set UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
#Admin Privileges----------------
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
Write  'Running PS with Administrator Rights'
#Run as Admin--------------------


$TargetHdd = $Hdd -replace ".vdi$", ".vhd"

# Delete Medium if exists
$AllArgs = @('closemedium', 'disk', '$TargetPath$TargetHdd', '--delete')
Invoke-Expression "& '$($VBoxPath)VBoxManage.exe' $AllArgs"
     
# ----------------------------
Write-Output "Convert $HddPath$Hdd > $TargetPath$TargetHdd"

$AllArgs = @('clonemedium', '$HddPath$Hdd', '$TargetPath$TargetHdd', '--format VHD')
Invoke-Expression "& '$($VBoxPath)VBoxManage.exe' $AllArgs"

# ----------------------------
# to VHDX wit Cmdlet
$TargetHddX = $TargetHdd -replace ".vhd$", ".vhdx"
Convert-VHD -Path $TargetPath$TargetHdd -DestinationPath $TargetPath$TargetHddX

# Delete File vhd
Remove-Item $TargetPath$TargetHdd

Write-Output "Exit in 5 Sekunden ..."
Start-Sleep -s 5
