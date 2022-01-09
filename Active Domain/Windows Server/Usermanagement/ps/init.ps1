Import-Module ActiveDirectory


# Listing aller Befehle
Get-Command *-AD*

Get-Help New-ADUser

New-ADUser `
  -Name "Hans Moser" `
  -GivenName "Hans" `
  -Surname "Moser" `
  -UserPrincipalName "h.moser" `
  -AccountPassword (ConvertTo-SecureString "passwd" -AsPlainText -Force) `
  -Path "OU=Lehrer,OU=Benutzer,OU=Frauengasse,DC=schule,DC=local" `
  -ChangePasswordAtLogon 1 `
  -Enabled 1 `
  -DisplayName "Hans Moser" `
  -HomeDrive "Z:" `
  -HomeDirectory "pdc\home\h.moser" `
  -ProfilePath "\\pdc\profiles\%USERNAME%"