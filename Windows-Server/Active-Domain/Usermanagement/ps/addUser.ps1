Import-Module ActiveDirectory
New-ADUser `
  -Name "%NACHNAME% %VORNAME%" `
  -GivenName "%VORNAME%" `
  -Surname "%NACHNAME%" `
  -UserPrincipalName "%USERNAME%" `
  -AccountPassword (ConvertTo-SecureString "%PASSWORD%" -AsPlainText -Force) `
  -Path "OU=%GRUPPE_SHORT%,%OUUSERS%" `
  -ChangePasswordAtLogon 1 `
  -Enabled 1 `
  -DisplayName "%VORNAME% %NACHNAME%" `
  -HomeDrive "%HOMEDRIVE%" `
  -HomeDirectory "%HOMEDIR%%username%" `
  -ProfilePath "%PROFILEDIR%%username%"