Import-Module ActiveDirectory
New-ADUser `
  -Name "%VORNAME% %NACHNAME%" `
  -GivenName "%VORNAME%" `
  -Surname "%NACHNAME%" `
  -UserPrincipalName "%USERNAME%" `
  -AccountPassword (ConvertTo-SecureString "%PASSWORD%" -AsPlainText -Force) `
  -Path "OU=%GRUPPE%,%OUUSERS%" `
  -ChangePasswordAtLogon 1 `
  -Enabled 1 `
  -DisplayName "%VORNAME% %NACHNAME%" `
  -HomeDrive "%HOMEDRIVE%" `
  -HomeDirectory "%HOMEDIR%%username%" `
  -ProfilePath "%PROFILEDIR%%username%"