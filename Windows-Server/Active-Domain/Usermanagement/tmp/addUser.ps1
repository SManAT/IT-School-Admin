Import-Module ActiveDirectory
New-ADUser `
  -Name "Hans Moser" `
  -GivenName "Hans" `
  -Surname "Moser" `
  -UserPrincipalName "moser" `
  -AccountPassword (ConvertTo-SecureString "Newton123" -AsPlainText -Force) `
  -Path "OU=Lehrer,OU=Benutzer,DC=schule,DC=local" `
  -ChangePasswordAtLogon 1 `
  -Enabled 1 `
  -DisplayName "Hans Moser" `
  -HomeDrive "Z:" `
  -HomeDirectory "S:\PDC\homes%username%" `
  -ProfilePath "S:\PDC\profiles%username%"