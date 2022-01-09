Import-Module ActiveDirectory
Get-AdUser -Filter "Name -eq '%VORNAME% %NACHNAME%'"
