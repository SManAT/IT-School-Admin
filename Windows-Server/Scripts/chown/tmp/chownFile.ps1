# get ACL Object
$ACL = Get-ACL Z:\Desktop\TestOwner\test.txt
$Group = New-Object System.Security.Principal.NTAccount("SCHULE\s.hagmann")
$ACL.SetOwner($Group)
# set Owner of File
Set-Acl Z:\Desktop\TestOwner\test.txt -AclObject $ACL
