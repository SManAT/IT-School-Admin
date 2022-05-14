Import-Module ActiveDirectory
# User accounts, by default, are created without a password. 
# If you provide a password, an attempt will be made to set that password however, this can fail due to password policy 
# restrictions. The user account will still be created and you may use Set-ADAccountPassword to set the password on 
# that account. In order to ensure that accounts remain secure, user accounts will never be enabled unless a 
# valid password is set or PasswordNotRequired is set to $True.
# The account is created if the password fails for any reason.

$PW_ = "Newton123"
$ADSplat = @{
    UserPrincipalName     = "c.hagmann@schule.local"
    # Usernaem for Pre-Win Logon Style Domain\name
    SamAccountName        = "c.hagmann"
    Name                  = "Hagmann Christina"
    GivenName             = "Christina"
    Surname               = "Hagmann"
    Enabled               = $True
    DisplayName           = "Christina Hagmann"
    Country               = "AT"
    Path                  = "OU=Lehrer,OU=Benutzer,DC=schule,DC=local"
    ChangePasswordAtLogon = $True
    AccountPassword       = (ConvertTo-SecureString $PW_ -AsPlainText -Force)
    HomeDrive             = "Z:"
    HomeDirectory         = "\\daddy.schule.local\homes$\c.hagmann"
    ProfilePath           = "\\daddy.schule.local\profiles$\c.hagmann"
}

New-ADUser @ADSplat

#$NewPwd = ConvertTo-SecureString "Newton123" -AsPlainText -Force
#Set-ADAccountPassword -Identity "Hagmann Christina" -NewPassword $NewPwd -Reset