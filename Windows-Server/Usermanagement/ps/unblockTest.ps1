powershell.exe -ExecutionPolicy ByPass -File "Z:\Dokumente\GitHub\IT-School-Admin\Windows-Server\Active-Domain\Usermanagement\tmp\existsGroup.ps1"

# Get-ExecutionPolicy -List
# MachinePolicy    Unrestricted

# Zuerst die GPO PowerShell setzen
# Set-ItemProperty -Path HKLM:\Software\Policies\Microsoft\Windows\PowerShell -Name ExecutionPolicy -Value ByPass 