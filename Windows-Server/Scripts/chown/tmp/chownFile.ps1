$ACL = Get-ACL "Z:\Desktop\TestOwner\Astrid\charles darwin.xps"
$Group = New-Object System.Security.Principal.NTAccount("SCHULE\s.hagmann")
$ACL.SetOwner($Group)
Set-Acl "Z:\Desktop\TestOwner\Astrid\charles darwin.xps" -AclObject $ACL
