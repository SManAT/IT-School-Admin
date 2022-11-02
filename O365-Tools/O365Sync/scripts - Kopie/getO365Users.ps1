#Set UTF-8-----------------------
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$User = "{% username %}"
$strPass = ConvertTo-SecureString -String "{% password %}" -AsPlainText -Force
$UserCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ($User, $strPass)

Connect-AzureAD -Credential $UserCredential

$_default_log = '{% path %}licensedUsers.csv'
Get-AzureADUser -All $true | Where-Object -FilterScript {$_.userType -ne 'Guest'} | select DisplayName,`
    UserPrincipalName,GivenName,Surname,Mail,UserType,AccountEnabled,`
    @{name='Licensed';expression={if($_.AssignedLicenses){$TRUE}else{$False}}},`
    @{name='Plan';expression={if($_.AssignedPlans){$TRUE}else{$False}}},ObjectId | export-csv $_default_log -NoTypeInformation -Encoding UTF8
