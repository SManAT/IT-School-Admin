#PowerShell benötig UTF-8 mit BOM 
$User = "{% username %}"
$strPass = ConvertTo-SecureString -String "{% password %}" -AsPlainText -Force
$UserCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ($User, $strPass)

Connect-AzureAD -Credential $UserCredential

#-------------------------------------------------------------------------------
$PasswordProfile=New-Object -TypeName Microsoft.Open.AzureAD.Model.PasswordProfile
$PasswordProfile.Password="{% user_password %}"
$DisplayName = "{% displayname %}"
$GivenName = "{% vorname %}"
$SurName = "{% nachname %}"
$UserPrincipalName = "{% principal %}"
$MailNickName = "{% mailnick %}"
$planName="{% plan %}"

#User anlegen
New-AzureADUser -DisplayName $DisplayName -GivenName $GivenName -SurName $SurName -UserPrincipalName $UserPrincipalName -UsageLocation AT -MailNickName $MailNickName -PasswordProfile $PasswordProfile -AccountEnabled $true

#Lizenz zuweisen
$License = New-Object -TypeName Microsoft.Open.AzureAD.Model.AssignedLicense
$License.SkuId = (Get-AzureADSubscribedSku | Where-Object -Property SkuPartNumber -Value $planName -EQ).SkuID
$LicensesToAssign = New-Object -TypeName Microsoft.Open.AzureAD.Model.AssignedLicenses
$LicensesToAssign.AddLicenses = $License
Set-AzureADUserLicense -ObjectId $UserPrincipalName -AssignedLicenses $LicensesToAssign
