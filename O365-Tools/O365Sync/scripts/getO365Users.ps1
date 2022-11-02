# Set UTF-8-----------------------
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$User = "{% username %}"
$strPass = ConvertTo-SecureString -String "{% password %}" -AsPlainText -Force
$UserCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ($User, $strPass)

Connect-AzureAD -Credential $UserCredential

$Csvfile = '{% path %}'
Get-AzureADUser -All $true | 
    Where-Object -FilterScript {$_.userType -ne 'Guest'} | 
    Select -Property DisplayName,UserPrincipalName,GivenName,Surname,Mail,UserType,AccountEnabled,
        @{name='Licensed';expression={if($_.AssignedLicenses){$TRUE}else{$False}}},
        @{name='Plan';expression={if($_.AssignedPlans){$TRUE}else{$False}}},ObjectId | 
    Export-Csv -Encoding UTF8 -Path $Csvfile -NoTypeInformation #-Delimiter ";"
