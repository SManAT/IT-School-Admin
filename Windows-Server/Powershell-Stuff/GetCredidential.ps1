$securestring = Get-Content $PSScriptRoot\Credidential.txt | ConvertTo-SecureString
Write $securestring