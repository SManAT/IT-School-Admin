Import-Module ActiveDirectory
Get-AdUser -Filter "Name -eq '%NACHNAME% %VORNAME%'"
