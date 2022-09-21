Import-Module ActiveDirectory

$PW_ = '%PASSWORD%'
$ADSplat = @{
    UserPrincipalName     = '%USERNAME%'
    # Username for Pre-Win Logon Style Domain\name
    # max length 20
    SamAccountName        = '%LOGIN_NAME%'
    Name                  = '%NACHNAME% %VORNAME%'
    GivenName             = '%VORNAME%'
    Surname               = '%NACHNAME%'
    Enabled               = $True
    DisplayName           = '%VORNAME% %NACHNAME%'
    Country               = 'AT'
    Path                  = 'OU=%GRUPPE_SHORT%,%OUUSERS%'
    ChangePasswordAtLogon = $True
    AccountPassword       = (ConvertTo-SecureString $PW_ -AsPlainText -Force)
    HomeDrive             = '%HOMEDRIVE%'
    HomeDirectory         = '%HOMEDIR%%USERNAME_SHORT%'
    ProfilePath           = '%PROFILEDIR%%USERNAME_SHORT%'
    EmailAddress          = '%EMAIL%'
}

New-ADUser @ADSplat