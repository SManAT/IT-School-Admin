# we use a Certificate, that schould be created on Linux
# be sure to have certificate.pem file in same directory

$certname = "ansible_certificate.pem"

Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $true

## Import Certificate ###################################################################
# Trusted Root Certificate Authorities

$cert = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Certificate2
$cert.Import("$certname")

$store_name = [System.Security.Cryptography.X509Certificates.StoreName]::Root
$store_location = [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine

$store = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Store -ArgumentList $store_name, $store_location

$store.Open("MaxAllowed")
$store.Add($cert)
$store.Close()

# Trusted People
$cert = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Certificate2
$cert.Import("$certname")

$store_name = [System.Security.Cryptography.X509Certificates.StoreName]::TrustedPeople
$store_location = [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine
$store = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Store -ArgumentList $store_name, $store_location
$store.Open("MaxAllowed")
$store.Add($cert)
$store.Close()

