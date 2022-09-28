$Action = New-ScheduledTaskAction -Execute 'S:\Backups\Restic-Backup\backup.bat' -Argument '-NonInteractive -NoLogo -NoProfile'

# starte alle n Tage
$Trigger = New-ScheduledTaskTrigger -Daily -DaysInterval 5 -At 3am
$Settings = New-ScheduledTaskSettingsSet

# create Timer Task
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings

# read encrypted Password from file
# only this user on this pc get decrypt it
$SecurePassword = Get-Content $PSScriptRoot\Credidential.txt | ConvertTo-SecureString


$Username = "SCHULE\Administrator"
$UserCredential = New-Object System.Management.Automation.PSCredential -ArgumentList $Username,$SecurePassword
$PlainPassword = $UserCredential.GetNetworkCredential().Password 

Write $PlainPassword


# register it
Register-ScheduledTask -TaskName 'Backup with Restic' -InputObject $Task -User $Username -Password $PlainPassword

