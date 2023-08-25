$User = "{% username %}"
$strPass = ConvertTo-SecureString -String "{% password %}" -AsPlainText -Force
$UserCredential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList ($User, $strPass)
Connect-AzureAD -Credential $UserCredential
