Set-Item -Path WSMan:\localhost\Service\Auth\credSSP -Value $true

# enables CredSSP authentication on the client
Enable-WSManCredSSP -Role "Server"
