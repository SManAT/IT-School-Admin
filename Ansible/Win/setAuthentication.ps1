# we use a Certifikate, that schould be created on Linux
# be sure to have certificate.pem file in same directory

$certname = "ansible_certificate.pem"
$username = "ansible"
$pwd = "plaintext"

Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $true

## Import Certificate ###################################################################

$cert = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Certificate2
$cert.Import("$certname")

$store_name = [System.Security.Cryptography.X509Certificates.StoreName]::Root
$store_location = [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine

$store = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Store -ArgumentList $store_name, $store_location

$store.Open("MaxAllowed")
$store.Add($cert)
$store.Close()

## Mapp Certificate to User #############################################################

$password = ConvertTo-SecureString -String "$pwd" -AsPlainText -Force
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username, $password

# This is the issuer thumbprint which in the case of a self generated cert
# is the public key thumbprint, additional logic may be required for other
# scenarios
$thumbprint = (Get-ChildItem -Path cert:\LocalMachine\root | Where-Object { $_.Subject -eq "CN=$username" }).Thumbprint

New-Item -Path WSMan:\localhost\ClientCertificate `
    -Subject "$username@localhost" `
    -URI * `
    -Issuer $thumbprint `
    -Credential $credential `
    -Force