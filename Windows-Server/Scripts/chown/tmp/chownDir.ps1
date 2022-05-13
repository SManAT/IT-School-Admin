$ACL = Get-ACL "Z:\Desktop\TestOwner\Desktop"
$Group = New-Object System.Security.Principal.NTAccount("SCHULE\s.hagmann")
$ACL.SetOwner($Group)
Set-Acl -Path "Z:\Desktop\TestOwner\Desktop" -AclObject $ACL
