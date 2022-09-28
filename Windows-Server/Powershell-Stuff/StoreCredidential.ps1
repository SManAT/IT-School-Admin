$credential = Get-Credential
$credential.Password | ConvertFrom-SecureString | Out-File $PSScriptRoot\Credidential.txt