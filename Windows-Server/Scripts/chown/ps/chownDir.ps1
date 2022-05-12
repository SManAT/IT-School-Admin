# get ACL Object
$ACL = Get-ACL %PATH%
$Group = New-Object System.Security.Principal.NTAccount("SCHULE\c.hagmann")
$ACL.SetOwner($Group)
# set Owner of File
Set-Acl %PATH% -AclObject $ACL

# set Owner of Path
#Set-Acl -Path .\smithb\profile.v2 -AclObject $ACL