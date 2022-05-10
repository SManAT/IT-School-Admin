Import-Module ActiveDirectory
# User accounts, by default, are created without a password. 
# If you provide a password, an attempt will be made to set that password however, this can fail due to password policy 
# restrictions. The user account will still be created and you may use Set-ADAccountPassword to set the password on 
# that account. In order to ensure that accounts remain secure, user accounts will never be enabled unless a 
# valid password is set or PasswordNotRequired is set to $True.
# The account is created if the password fails for any reason.

$PW_ = "%PASSWORD%"
$ADSplat = @{
    UserPrincipalName     = "%USERNAME%"
    # Usernaem for Pre-Win Logon Style Domain\name
    SamAccountName        = "%LOGIN_NAME%"
    Name                  = "%NACHNAME% %VORNAME%"
    GivenName             = "%VORNAME%"
    Surname               = "%NACHNAME%"
    Enabled               = $True
    DisplayName           = "%VORNAME% %NACHNAME%"
    Country               = "AT"
    Path                  = "OU=%GRUPPE_SHORT%,%OUUSERS%"
    ChangePasswordAtLogon = $True
    AccountPassword       = (ConvertTo-SecureString $PW_ -AsPlainText -Force)
    HomeDrive             = "%HOMEDRIVE%"
    HomeDirectory         = "%HOMEDIR%%USERNAME_SHORT%"
    ProfilePath           = "%HOMEDIR%%USERNAME_SHORT%\AppData\Roaming"
}

New-ADUser @ADSplat

#$NewPwd = ConvertTo-SecureString "%PASSWORD%" -AsPlainText -Force
#Set-ADAccountPassword -Identity "%NACHNAME% %VORNAME%" -NewPassword $NewPwd -Reset